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
import sys, os, glob, shutil, subprocess, argparse, importlib.util
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



def ca_design(pdb, tag, nseq, blen):
    """CA-only ProteinMPNN on a Genie 3 backbone. Designs chain D, A/B/C fixed, cysteine banned.

    WHY NOT run_depth_rounds.redesign(). Genie 3 emits CA-ONLY coordinates -- 83 CA atoms for the
    83-residue binder, and the target protomers likewise carry CA plus the conditioning histidine's
    sidechain. ProteinMPNN's default featuriser needs N, CA, C and O, so it masked every binder
    position and returned EIGHTY-THREE X's. The length assertion passed (83 == 83) and nothing else
    looked wrong, so 240 complexes were folded against a binder with no sequence: constant pLDDT
    0.7493-0.7497 across 210 scored designs, DockQ 0.013-0.075, lrms 30-40 A. That cost ~$6.70 and
    read exactly like a real S1 failure.

    protein_mpnn_run.py --ca_only loads ca_model_weights/ and is built for this case. It REFUSES
    to combine with --use_soluble_model ("CA-SolubleMPNN is not available yet", sys.exit), so this
    leg runs the vanilla CA weights -- a DECLARED deviation from the protocol's SolubleMPNN. The
    established SolubleMPNN redesign still applies later, on the PREDICTED complex, which is what
    the depth loop has always done; it cannot apply here because no prediction exists yet.
    """
    work = f"/tmp/armS_{tag}_mpnn"
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(f"{work}/in")
    shutil.copy(pdb, f"{work}/in/parent.pdb")
    r = lambda *c: subprocess.run(c, cwd=_rdr.MPNN, check=True, capture_output=True, text=True)
    r(_rdr.MPNN_PY, "helper_scripts/parse_multiple_chains.py",
      f"--input_path={work}/in", f"--output_path={work}/p.jsonl", "--ca_only")
    r(_rdr.MPNN_PY, "helper_scripts/assign_fixed_chains.py",
      f"--input_path={work}/p.jsonl", f"--output_path={work}/c.jsonl", "--chain_list", "D")
    r(_rdr.MPNN_PY, "protein_mpnn_run.py", "--jsonl_path", f"{work}/p.jsonl",
      "--chain_id_jsonl", f"{work}/c.jsonl", "--out_folder", work,
      "--num_seq_per_target", str(nseq), "--sampling_temp", "0.1",
      "--seed", "37", "--batch_size", "1", "--ca_only",
      "--omit_AAs", "CX")
    lines = [l.strip() for l in open(f"{work}/seqs/parent.fa") if l.strip()]
    seqs = [l for l in lines if not l.startswith(">")][1:]
    out = []
    for q in seqs:
        q = q.split("/")[-1]
        if len(q) != blen:
            sys.exit(f"{tag}: sequence length {len(q)} != binder {blen}")
        # THE GUARD THIS FUNCTION EXISTS FOR. A masked backbone returns X and every other check
        # passes, so poly-X is rejected explicitly rather than inferred from a downstream score.
        nx = q.count("X")
        if nx:
            sys.exit(f"{tag}: {nx} X residue(s) survived -- the backbone was not featurised")
        if "C" in q:
            sys.exit(f"{tag}: cysteine survived the ban")
        out.append(q)
    if len(out) != nseq:
        sys.exit(f"{tag}: {len(out)} sequences, expected {nseq}")
    return out


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
            seqs = ca_design(rl, f"{a.tag}_{stem}", a.nseq, blen)
        except SystemExit as e:
            print(f"  REFUSED {stem}: design -- {e}"); n_ref += 1; continue
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
