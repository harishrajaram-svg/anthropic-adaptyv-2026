#!/usr/bin/env python3
"""Arm H: SolubleMPNN on a predicted complex, D/E banned only at the gate-attributed positions.

PREREG: analysis/02-tnf/PREREG-H-REBUILD-2026-10-11.md

Uses mpnn_constraints.emit() with a NARROW iface list, so the acid ban covers exactly the named
positions rather than the whole interface. Arm A banned acids at every interface position during
design and reached 0 of 224 on pose; that is a different operation from this one.

H4 is verified on the OUTPUT SEQUENCES. --omit_AA_jsonl loads only if the file exists and otherwise
designs unconstrained while printing a note to stdout, so a wrong path is indistinguishable from an
applied constraint unless the result is checked.
"""
import sys, os, glob, json, shutil, subprocess, argparse, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gemmi
_s = importlib.util.spec_from_file_location("_rdr", os.path.join(HERE, "run_depth_rounds.py"))
_rdr = importlib.util.module_from_spec(_s); _s.loader.exec_module(_rdr)
import mpnn_constraints as mc
from build_sizematched_null import trimer

PARENTS = {
    "L49H_E4Q":  ("runs/G-neutral-out/*/tnfa_corrected_3_L0r4k0_L49H_E4Q/*.cif",  [7, 10, 20, 28]),
    "quadH_E3Q": ("runs/G-neutral-out/*/tnfa_corrected_3_L0r4k0_quadH_E3Q/*.cif", [7, 20, 28]),
    "s3_22k4":   ("runs/S-margin-out/Smargin/tnfa_seam_s3_22k4/*.cif",            [6, 56, 61, 69, 82]),
}


def best_template(pattern):
    """Highest complex pLDDT -- a structural criterion, fixed in the prereg, not the outcome."""
    best, bp = None, -1.0
    for cif in sorted(glob.glob(pattern)):
        sc = cif.replace(".cif", "_scores.json")
        if not os.path.exists(sc):
            continue
        p = json.load(open(sc)).get("plddt", -1)
        if p > bp:
            best, bp = cif, p
    return best, bp


def design(cif, tag, banned, nseq):
    work = f"/tmp/armH_{tag}"
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(f"{work}/in")
    st = gemmi.read_structure(cif)
    st.setup_entities(); st.remove_ligands_and_waters(); st.remove_hydrogens()
    if sorted(c.name for c in st[0]) != list("ABCD"):
        sys.exit(f"REFUSED: {cif} chains {sorted(c.name for c in st[0])}")
    blen = sum(1 for _ in st[0]["D"])
    st.write_pdb(f"{work}/in/parent.pdb")
    r = lambda *c: subprocess.run(c, cwd=_rdr.MPNN, check=True, capture_output=True, text=True)
    r(_rdr.MPNN_PY, "helper_scripts/parse_multiple_chains.py",
      f"--input_path={work}/in", f"--output_path={work}/p.jsonl")
    r(_rdr.MPNN_PY, "helper_scripts/assign_fixed_chains.py",
      f"--input_path={work}/p.jsonl", f"--output_path={work}/c.jsonl", "--chain_list", "D")
    cpath, items = mc.emit("parent", "D", banned, [], f"{work}/cons",
                           force_his=False, n_res=blen, omit_acids=True)
    r(_rdr.MPNN_PY, "protein_mpnn_run.py", "--jsonl_path", f"{work}/p.jsonl",
      "--chain_id_jsonl", f"{work}/c.jsonl", "--out_folder", work,
      "--num_seq_per_target", str(nseq), "--sampling_temp", "0.1",
      "--seed", "37", "--batch_size", "1", "--use_soluble_model",
      "--omit_AAs", "CX", "--omit_AA_jsonl", cpath)
    lines = [l.strip() for l in open(f"{work}/seqs/parent.fa") if l.strip()]
    seqs = [l for l in lines if not l.startswith(">")][1:]
    out = []
    for q in seqs:
        q = q.split("/")[-1]
        if len(q) != blen:
            sys.exit(f"{tag}: length {len(q)} != {blen}")
        if "X" in q or "C" in q:
            sys.exit(f"{tag}: X or C survived the ban")
        bad = [p for p in banned if q[p - 1] in "DE"]          # H4
        if bad:
            sys.exit(f"{tag}: H4 FAILED -- acid at banned position(s) {bad} "
                     f"({[q[p-1] for p in bad]}); omit_AA_jsonl did not apply")
        out.append(q)
    if len(out) != nseq:
        sys.exit(f"{tag}: {len(out)} sequences, expected {nseq}")
    return out, items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nseq", type=int, default=16)
    ap.add_argument("--out", default="runs/H-rebuild-in")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    tnf = trimer()
    n = 0
    for tag, (pat, banned) in PARENTS.items():
        cif, pl = best_template(pat)
        if cif is None:
            print(f"  REFUSED {tag}: no template with scores"); continue
        seqs, items = design(cif, tag, banned, a.nseq)
        print(f"  {tag}: template pLDDT {pl:.4f}, D/E banned at {banned}, "
              f"{len(seqs)} seqs, omit items {len(items)}")
        for k, s in enumerate(seqs):
            nm = f"tnfa_H_{tag}_k{k}"
            with open(os.path.join(a.out, nm + ".faa"), "w") as fh:
                for c in "ABC":
                    fh.write(f">protein|{c}\n{tnf}\n")
                fh.write(f">protein|D\n{s}\n")
            n += 1
    print(f"\nwrote {n} fold inputs to {a.out}  (H4 verified on every accepted sequence)")


if __name__ == "__main__":
    main()
