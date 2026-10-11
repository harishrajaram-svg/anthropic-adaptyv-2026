#!/usr/bin/env python3
"""Arm S stage 2: SolubleMPNN sequences on seam-conditioned Genie 3 backbones, then fold inputs.

PREREG: analysis/02-tnf/PREREG-ROUTES-123-2026-10-11.md

WHY A RELABEL STEP EXISTS, AND WHY IT FAILS CLOSED
--------------------------------------------------
Genie 3 writes the BINDER as chain A (83 UNK residues) and the three target protomers as B/C/D.
run_depth_rounds.redesign() designs chain D with A/B/C fixed, which on a raw Genie 3 backbone would
redesign a TARGET PROTOMER and leave the binder untouched. The depth loop never hit this because it
ran on ESMFold PREDICTED complexes, which already carry target A/B/C and binder D.

ph_gate_all.family() cannot arbitrate here: it matches a histidine tuple in the ESMFold output's
numbering, and these PDBs use the generator's own numbering, so it reports every chain as "binder".
Identification is therefore by CONTENT -- the binder is the all-UNK chain, the targets are three
chains of equal length carrying identical real sequences -- and anything else is REFUSED.

Design is deliberately UNCONSTRAINED apart from the standing cysteine ban: force_his=False because
forcing histidine at interface positions collapsed the pose independently (0.6349 -> 0.0126), and
omit_acids=False because the wholesale acid ban cannot hold a pose at all (arm A, 0 of 224).
Layering either constraint now would confound S1 -- a failure could not be read as "the seam does
not dock" rather than "the constraint broke it", which is the confound that cost arm A its answer.
"""
import sys, os, glob, argparse, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gemmi

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("_rdr", os.path.join(HERE, "run_depth_rounds.py"))
_rdr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_rdr)                     # safe: its CLI is under __main__
from build_sizematched_null import trimer


def relabel(path, out_path):
    """Genie 3 layout -> target A/B/C + binder D. Refuses anything it cannot identify."""
    st = gemmi.read_structure(path)
    st.setup_entities(); st.remove_ligands_and_waters(); st.remove_hydrogens()
    model = st[0]
    unk, real = [], []
    for ch in model:
        names = {r.name for r in ch}
        (unk if names == {"UNK"} else real).append(ch)
    if len(unk) != 1:
        return None, f"{len(unk)} all-UNK chain(s); need exactly one (the binder)"
    if len(real) != 3:
        return None, f"{len(real)} sequence-bearing chain(s); need exactly three protomers"
    seqs = ["".join(r.name for r in c) for c in real]
    if len(set(seqs)) != 1:
        return None, f"the three protomers are not identical ({[len(s)//3 for s in seqs]} res)"
    binder_len = len(list(unk[0]))
    # rename via a scratch namespace so no two chains ever share a name mid-rename
    for i, ch in enumerate(real + unk):
        ch.name = f"_{i}"
    for ch in model:
        ch.name = {"_0": "A", "_1": "B", "_2": "C", "_3": "D"}[ch.name]
    st.setup_entities()
    st.write_pdb(out_path)
    return binder_len, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdb_glob")
    ap.add_argument("--tag", required=True)
    ap.add_argument("--nseq", type=int, default=8)
    ap.add_argument("--out", required=True)
    ap.add_argument("--limit", type=int)
    a = ap.parse_args()

    paths = sorted(glob.glob(a.pdb_glob))
    if a.limit:
        paths = paths[:a.limit]
    if not paths:
        sys.exit(f"REFUSED: no backbones matched {a.pdb_glob}")
    os.makedirs(a.out, exist_ok=True)
    work = f"/tmp/armS_{a.tag}_relabel"
    os.makedirs(work, exist_ok=True)
    tnf = trimer()
    n_ok = n_ref = n_seq = 0
    for p in paths:
        stem = os.path.splitext(os.path.basename(p))[0]
        rl = os.path.join(work, stem + "_ABCD.pdb")
        blen, err = relabel(p, rl)
        if err:
            print(f"  REFUSED {stem}: {err}"); n_ref += 1; continue
        try:
            seqs = _rdr.redesign(rl, f"{a.tag}_{stem}", a.nseq,
                                 force_his=False, omit_acids=False)
        except SystemExit as e:
            print(f"  REFUSED {stem}: redesign -- {e}"); n_ref += 1; continue
        n_ok += 1
        for k, s in enumerate(seqs):
            assert len(s) == blen, (len(s), blen)
            name = f"tnfa_seam_{a.tag}_{stem.split('_')[-1]}k{k}"
            with open(os.path.join(a.out, name + ".faa"), "w") as fh:
                for c in "ABC":
                    fh.write(f">protein|{c}\n{tnf}\n")
                fh.write(f">protein|D\n{s}\n")
            n_seq += 1
    print(f"\nbackbones {len(paths)}  designed {n_ok}  refused {n_ref}  fold inputs {n_seq}")
    print(f"wrote {a.out}")


if __name__ == "__main__":
    main()
