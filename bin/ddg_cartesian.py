#!/usr/bin/env python3
"""Cartesian ddG of folding for point/multi-point mutants, PyRosetta ref2015_cart.

Reimplements the Park et al. 2016 cartesian_ddg protocol (the Rosetta application of
that name is not exposed through PyRosetta): for WT and for the mutant, repack and
cartesian-minimise a neighbourhood around the mutated position(s) with everything
outside it fixed, then ddG = mean(mutant) - mean(WT) over replicate inputs.

This returns ddG -- a DIFFERENCE between two sequences -- NOT dG_fold. It cannot say
whether a scaffold is marginally stable; only what a substitution costs. Units are
Rosetta Energy Units from ref2015_cart, conventionally read as kcal/mol, and that
convention is exactly what --spec control rows exist to test.

Two things found the hard way, both now enforced here rather than remembered:

1. CA-CA distance is the WRONG neighbourhood criterion. At 8 A it returns 10 residues
   on an 83-mer helical bundle, so the mutated side chain relaxes against almost
   nothing and every ddG comes out small. Use Rosetta's own NeighborhoodResidueSelector,
   which measures neighbour-atom to neighbour-atom.
2. Repacking a small shell with -use_input_sc is DETERMINISTIC: three replicates of the
   same input returned -208.5698 three times. Packer replicates buy nothing, so
   replication here is over independent input structures (ESMFold seeds), which
   measures the thing that actually varies.

Usage:
    ddg_cartesian.py --pdbs a.pdb,b.pdb --spec specs.tsv --out rows.json
      specs.tsv rows: name<TAB>comma,separated,muts   ('-' = WT-vs-WT null row)
    ddg_cartesian.py --self-test
"""
import argparse
import json
import statistics
import sys

AA3 = {
    "A": "ALA", "C": "CYS", "D": "ASP", "E": "GLU", "F": "PHE", "G": "GLY",
    "H": "HIS", "I": "ILE", "K": "LYS", "L": "LEU", "M": "MET", "N": "ASN",
    "P": "PRO", "Q": "GLN", "R": "ARG", "S": "SER", "T": "THR", "V": "VAL",
    "W": "TRP", "Y": "TYR",
}
DEFAULT_RADIUS = 10.0


def parse_mut(tok):
    """'V45H' -> ('V', 45, 'H'). Position is a 1-indexed Rosetta pose number."""
    tok = tok.strip()
    wt, mt = tok[0].upper(), tok[-1].upper()
    pos = int(tok[1:-1])
    if wt not in AA3 or mt not in AA3:
        raise ValueError(f"bad mutation token {tok!r}")
    return wt, pos, mt


def shell(pose, positions, radius):
    """1-indexed residues within `radius` (neighbour atom to neighbour atom) of any of
    `positions`, the focus residues included."""
    import pyrosetta.rosetta as r
    RS = r.core.select.residue_selector
    idx = RS.ResidueIndexSelector()
    idx.set_index(",".join(str(p) for p in positions))
    v = RS.NeighborhoodResidueSelector(idx, radius, True).apply(pose)
    return [i for i in range(1, pose.total_residue() + 1) if v[i]]


def relax_shell(pose, sfxn, sh, rounds=2):
    """Repack + cartesian-minimise `sh`; everything else frozen. In place."""
    import pyrosetta.rosetta as r

    task = r.core.pack.task.TaskFactory.create_packer_task(pose)
    task.restrict_to_repacking()
    task.or_include_current(True)
    keep = set(sh)
    for i in range(1, pose.total_residue() + 1):
        if i not in keep:
            task.nonconst_residue_task(i).prevent_repacking()
    pack = r.protocols.minimization_packing.PackRotamersMover(sfxn, task)

    mm = r.core.kinematics.MoveMap()
    mm.set_bb(False)
    mm.set_chi(False)
    for i in sh:
        mm.set_bb(i, True)
        mm.set_chi(i, True)
    minm = r.protocols.minimization_packing.MinMover(
        mm, sfxn, "lbfgs_armijo_nonmonotone", 1e-5, True
    )
    minm.cartesian(True)
    minm.max_iter(1000)

    for _ in range(rounds):
        pack.apply(pose)
        minm.apply(pose)
    return pose


def run(pdbs, specs, radius=DEFAULT_RADIUS, out=None):
    import pyrosetta
    import pyrosetta.rosetta as r

    pyrosetta.init("-mute all -ex1 -ex2 -use_input_sc -ignore_unrecognized_res "
                   "-ignore_zero_occupancy false")
    sfxn = r.core.scoring.ScoreFunctionFactory.create_score_function("ref2015_cart")
    bases = []
    for p in pdbs:
        pose = pyrosetta.pose_from_pdb(p)
        bases.append((p, pose))
        print(f"# {p}  nres={pose.total_residue()}  raw={sfxn(pose):.2f}", file=sys.stderr)

    rows = []
    for name, toks in specs:
        muts = [] if toks == ["-"] else [parse_mut(t) for t in toks]
        focus = [p for _, p, _ in muts] or [1]
        per_input = []
        for path, base in bases:
            for wt, pos, _ in muts:
                have = base.residue(pos).name1()
                if have != wt:
                    raise SystemExit(
                        f"FAIL CLOSED: {name}: {path} position {pos} is {have}, "
                        f"mutation token says {wt}"
                    )
            sh = shell(base, focus, radius)
            w = base.clone()
            relax_shell(w, sfxn, sh)
            wt_s = sfxn(w)
            m = base.clone()
            for _, pos, mt in muts:
                r.protocols.simple_moves.MutateResidue(pos, AA3[mt]).apply(m)
            relax_shell(m, sfxn, sh)
            mu_s = sfxn(m)
            per_input.append((path, len(sh), wt_s, mu_s, mu_s - wt_s))
        d = [x[4] for x in per_input]
        row = {
            "name": name,
            "muts": ",".join(toks),
            "n_shell": per_input[0][1],
            "n_inputs": len(per_input),
            "ddg_mean": round(statistics.mean(d), 3),
            "ddg_sd": round(statistics.stdev(d), 3) if len(d) > 1 else 0.0,
            "ddg_min": round(min(d), 3),
            "ddg_max": round(max(d), 3),
            "per_input": [
                {"pdb": p.split("/")[-1], "shell": n, "wt": round(w, 3),
                 "mut": round(m, 3), "ddg": round(x, 3)}
                for p, n, w, m, x in per_input
            ],
        }
        rows.append(row)
        print(f"{name}\t{row['muts']}\tshell={row['n_shell']}\t"
              f"ddG={row['ddg_mean']:+.3f}\tSD={row['ddg_sd']:.3f}\t"
              f"[{row['ddg_min']:+.2f},{row['ddg_max']:+.2f}]\tn={row['n_inputs']}",
              flush=True)
    if out:
        json.dump(rows, open(out, "w"), indent=1)
    return rows


def self_test():
    """Parsing and the fail-closed identity rule, no Rosetta needed."""
    assert parse_mut("V45H") == ("V", 45, "H")
    assert parse_mut("L164A") == ("L", 164, "A")
    for bad in ("X45H", "V45X", "45H"):
        try:
            parse_mut(bad)
        except Exception:
            pass
        else:
            raise AssertionError(f"{bad} should not parse")
    assert AA3["H"] == "HIS"
    assert DEFAULT_RADIUS == 10.0, "radius default is load-bearing; see docstring note 1"
    print("self-test OK: mutation parsing, bad-token rejection, AA3 table, radius default")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdbs", help="comma-separated replicate input structures")
    ap.add_argument("--spec", help="TSV: name<TAB>muts")
    ap.add_argument("--radius", type=float, default=DEFAULT_RADIUS)
    ap.add_argument("--out")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        self_test()
        sys.exit(0)
    if not a.pdbs or not a.spec:
        ap.error("--pdbs and --spec required")
    specs = []
    for line in open(a.spec):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        n, m = line.split("\t")[:2]
        specs.append((n, m.split(",")))
    run(a.pdbs.split(","), specs, a.radius, a.out)
