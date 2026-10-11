#!/usr/bin/env python3
"""cartesian_ddg for the FOLD route: how much pH-independent stability a buried histidine spends.

PREREG: analysis/02-tnf/PREREG-W2-COUNT-LADDER-2026-10-11.md (bar W2-5)

WHAT THIS MEASURES, AND WHAT IT IS NOT
    Arm M measured that pH-linked fold destabilisation saturates at +0.775 kcal/mol per buried
    histidine, so the only remaining lever is COUNT. But the window the route has to land in is
    two-sided:

        0 < dG_fold(7.4) < sum(destab)

    Sigma rising is half the job; dG_fold(7.4) must come DOWN to meet it. Installing a histidine
    in a hydrophobic core does both -- it adds +0.775 of pH-linked destabilisation AND it spends
    pH-independent stability. This file measures that second number, which is the one nobody in
    this project has measured.

        r = ddG_install per histidine / 0.775

    r >> 1 means a handful of histidines strips the scaffold and the molecule is dead at BOTH pH
    values -- a broken protein, not a switch. r <= 1 means count scales almost for free.

    This is a NEUTRAL-His calculation. Rosetta's default His is the neutral tautomer and pH_mode
    is NOT enabled here, deliberately: the protonated leg is already handled analytically by the
    PROPKA + Henderson-Hasselbalch term, and double-counting it here would inflate Sigma. So this
    number is pH-INDEPENDENT by construction.

    It is NOT the absolute dG_fold. Rosetta gives a DIFFERENCE between two sequences on one
    backbone. The parent's absolute stability remains unmeasured and that is stated in the prereg.

BUILT-IN SIGN CONTROL
    The four histidines of 3_L0r4k0_quadH are run in REVERSE (H45V/H53L/H63L/H64L, back to the
    parent). Leucine and valine in a hydrophobic core are better than imidazole, so those four
    reversions MUST come out negative (stabilising). If any comes out positive the protocol is
    not measuring what it claims and the forward numbers are not reportable. There is no
    threshold to tune here -- the sign is known in advance.

PROTOCOL
    Standard local cartesian_ddg recipe. For one mutation set:
      1. sphere = every residue with any heavy atom within RADIUS of any mutated position's CB
      2. WT leg:  repack the sphere, then cartesian-minimise bb+chi inside the sphere
      3. MUT leg: mutate, then the identical repack + minimise
      4. ddG = mean(MUT) - mean(WT) over N independent iterations (different pack seeds)
    Both legs are relaxed in the SAME sphere with the SAME protocol, which is the only way the
    difference means anything.

    cart_ddg_fold.py --selftest
    cart_ddg_fold.py --pdb <monomer.pdb> --muts I78H,I16H [--iters 3]
"""
import argparse
import os
import statistics as st
import sys

RADIUS = 8.0
AA3 = {"A": "ALA", "C": "CYS", "D": "ASP", "E": "GLU", "F": "PHE", "G": "GLY", "H": "HIS",
       "I": "ILE", "K": "LYS", "L": "LEU", "M": "MET", "N": "ASN", "P": "PRO", "Q": "GLN",
       "R": "ARG", "S": "SER", "T": "THR", "V": "VAL", "W": "TRP", "Y": "TYR"}
PER_HIS_CEILING = 0.7749          # arm M, analysis/02-tnf/M_fold_linkage.txt


def parse_mut(tok):
    """'I78H' -> ('I', 78, 'H'). Fails closed on anything else."""
    tok = tok.strip()
    if len(tok) < 3 or not tok[1:-1].isdigit():
        sys.exit(f"REFUSED: cannot parse mutation {tok!r}; expected e.g. I78H")
    wt, pos, mt = tok[0].upper(), int(tok[1:-1]), tok[-1].upper()
    if wt not in AA3 or mt not in AA3:
        sys.exit(f"REFUSED: unknown amino acid in {tok!r}")
    return wt, pos, mt


def _sphere(pose, positions):
    """Residue indices with a heavy atom within RADIUS of any mutated residue's CB (CA for Gly)."""
    import pyrosetta
    centres = []
    for p in positions:
        res = pose.residue(p)
        name = "CB" if res.has("CB") else "CA"
        centres.append(res.xyz(name))
    keep = set()
    for i in range(1, pose.total_residue() + 1):
        res = pose.residue(i)
        for j in range(1, res.nheavyatoms() + 1):
            xyz = res.xyz(j)
            if any(xyz.distance(c) <= RADIUS for c in centres):
                keep.add(i)
                break
    return sorted(keep)


def _relax_leg(pose, sphere, sf, seed_pose_ops=None):
    """Repack the sphere, then cartesian-minimise bb+chi inside it. In place."""
    import pyrosetta
    from pyrosetta.rosetta.core.pack.task import TaskFactory
    from pyrosetta.rosetta.protocols.minimization_packing import PackRotamersMover, MinMover

    tf = pyrosetta.rosetta.core.pack.task.TaskFactory.create_packer_task(pose)
    tf.restrict_to_repacking()
    sphere_set = set(sphere)
    for i in range(1, pose.total_residue() + 1):
        if i not in sphere_set:
            tf.nonconst_residue_task(i).prevent_repacking()
    PackRotamersMover(sf, tf).apply(pose)

    mm = pyrosetta.rosetta.core.kinematics.MoveMap()
    mm.set_bb(False)
    mm.set_chi(False)
    for i in sphere:
        mm.set_bb(i, True)
        mm.set_chi(i, True)
    minmover = MinMover(mm, sf, "lbfgs_armijo_nonmonotone", 1e-4, True)
    minmover.cartesian(True)
    minmover.max_iter(300)
    minmover.apply(pose)
    return sf(pose)


def ddg(pdb, muts, iters=3, quiet=True):
    """ddG_install in REU (~kcal/mol) for a mutation SET, relative to the pdb's own sequence."""
    import pyrosetta
    from pyrosetta.rosetta.protocols.simple_moves import MutateResidue

    pyrosetta.init("-mute all -ex1 -ex2 -use_input_sc -no_optH false -flip_HNQ", silent=quiet)
    sf = pyrosetta.create_score_function("ref2015_cart")
    base = pyrosetta.pose_from_pdb(pdb)

    parsed = [parse_mut(m) for m in muts]
    for wt, pos, mt in parsed:
        if pos < 1 or pos > base.total_residue():
            sys.exit(f"REFUSED: position {pos} outside 1..{base.total_residue()}")
        got = base.residue(pos).name1()
        if got != wt:
            sys.exit(f"REFUSED: {pdb} has {got} at {pos}, mutation string says {wt}. "
                     f"Wrong structure or wrong numbering -- failing closed.")

    sphere = _sphere(base, [p for _, p, _ in parsed])
    wt_e, mut_e = [], []
    for it in range(iters):
        pyrosetta.rosetta.numeric.random.rg().set_seed("mt19937", 1000 + it)

        w = base.clone()
        wt_e.append(_relax_leg(w, sphere, sf))

        m = base.clone()
        for _, pos, mt in parsed:
            MutateResidue(pos, AA3[mt]).apply(m)
        mut_e.append(_relax_leg(m, sphere, sf))

    return {
        "muts": ",".join(muts),
        "n_sphere": len(sphere),
        "iters": iters,
        "wt": st.mean(wt_e), "wt_sd": st.pstdev(wt_e) if iters > 1 else 0.0,
        "mut": st.mean(mut_e), "mut_sd": st.pstdev(mut_e) if iters > 1 else 0.0,
        "ddg": st.mean(mut_e) - st.mean(wt_e),
    }


def selftest():
    """Arithmetic and parsing only -- no structure, no Rosetta. ~0.01s.

    The protocol's own correctness check is the REVERSE-mutation sign control in the readout,
    which has a known answer; there is nothing here to pin that a passing unit test would catch.
    """
    assert parse_mut("I78H") == ("I", 78, "H")
    assert parse_mut("A60H") == ("A", 60, "H")
    for bad in ("X1H", "I78", "78H", "I7bH"):
        try:
            parse_mut(bad)
        except SystemExit:
            pass
        else:
            raise AssertionError(f"accepted malformed mutation {bad!r}")
    assert abs(PER_HIS_CEILING - 0.7749) < 1e-6
    # r is a ratio, so it must be reported per-histidine, not per-mutation-set
    assert abs((3.0 / 2) / PER_HIS_CEILING - 1.9357) < 1e-3
    print("cart_ddg_fold selftest OK (5 checks)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdb")
    ap.add_argument("--muts", help="comma-separated, e.g. I78H,I16H")
    ap.add_argument("--iters", type=int, default=3)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        selftest()
        sys.exit(0)
    if not a.pdb or not a.muts:
        sys.exit("usage: cart_ddg_fold.py --pdb <monomer.pdb> --muts I78H,I16H [--iters 3]")
    r = ddg(a.pdb, a.muts.split(","), a.iters)
    n = len(a.muts.split(","))
    print(f"{r['muts']}\tsphere={r['n_sphere']}\tddG={r['ddg']:+.3f}\t"
          f"per_mut={r['ddg']/n:+.3f}\tr={r['ddg']/n/PER_HIS_CEILING:+.2f}")
