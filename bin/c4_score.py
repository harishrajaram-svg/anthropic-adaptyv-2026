#!/usr/bin/env python3
"""C4: score the six shipped designs on both oracles against their Genie 3 backbones.

Governed by PREREG-C4-FINALIST-RESCORE-2026-10-11.md. C4c forbids refolding ESMFold2, so its
numbers come from folds that already exist on disk -- and from ALL of them, not one draw, so a
disagreement cannot be an artefact of whichever seed happened to be picked.

Designs are located BY BINDER SEQUENCE, not by directory name. Two reasons, both learned here:
row 4's human folds sit under biomodals/runs/ because a relative OUT_DIR was passed to a script
that cd's, and `tnfa_H_quadH_E3Q_k12` and `tnfa_corrected_3_L0r4k0_quadH` are different molecules
whose names both contain "quadH".
"""
import glob
import importlib.util
import os
import statistics
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(REPO)
sys.path.insert(0, "bin")

import gemmi

spec = importlib.util.spec_from_file_location("dl", "bin/depth_loop.py")
dl = importlib.util.module_from_spec(spec)
sys.modules["dl"] = dl
spec.loader.exec_module(dl)

DESIGNED = "runs/genie3-out/probe50/tnfa_corrected/pdbs"
ROWS = [  # (row, design id, root backbone) -- backbones as frozen in the pre-registration
    (1, "tnfa_corrected_40_L1r4k6", "40"),
    (2, "tnfa_corrected_40_L1r4k1", "40"),
    (3, "tnfa_corrected_3_L0r4k0_L49H", "3"),
    (4, "tnfa_corrected_3_L0r4k0_quadH", "3"),
    (5, "tnfa_corrected_3_L0r4k0", "3"),
    (6, "tnfa_H_quadH_E3Q_k12", "3"),
]


def ship_seqs():
    out, name = {}, None
    for line in open("outbox/prescreen-ship6-2026-10-11/ship6.fasta"):
        line = line.strip()
        if line.startswith(">"):
            name = line[1:]
        elif line:
            out[name] = out.get(name, "") + line
    return out


def score(designed_pdb, cif):
    offs = dl.numbering_offsets(designed_pdb, cif, "A", "D")
    r = dl._scd.sc_dockq(designed_pdb, cif, d_bind="A", p_bind="D", offsets=offs)
    return None if r is None else (r[0], r[2])      # (ca_sc_dockq, lrms)


def main():
    seqs = ship_seqs()
    # index every ESMFold2 human-trimer complex on disk by its binder sequence
    byseq = {}
    for pat in ("runs/**/*.cif", "biomodals/runs/**/*.cif"):
        for c in glob.glob(pat, recursive=True):
            if "corr-c4-out" in c or "corr-chai" in c:
                continue                            # Chai-1 output, not ESMFold2
            try:
                st = gemmi.read_structure(c)
                st.setup_entities()
                st.remove_ligands_and_waters()
                ch = {x.name: x for x in st[0]}
            except Exception:
                continue
            if sorted(ch) != list("ABCD") or len(ch["D"]) != 83 or len(ch["A"]) != 157:
                continue                            # not a human-trimer complex
            s = gemmi.one_letter_code([r.name for r in ch["D"]]).upper()
            byseq.setdefault(s, []).append(c)

    print(f"{'#':>2} {'design':30s} {'chai_dq':>7s} {'chai_lrms':>9s} | "
          f"{'esm_dq_med':>10s} {'esm_lrms_med':>12s} {'n':>3s} {'esm_lrms_range':>16s} | "
          f"{'min_dq':>7s} {'worse_lrms':>10s}  C4a")
    out = []
    for row, did, bb in ROWS:
        dpdb = f"{DESIGNED}/tnfa_corrected_{bb}.pdb"
        cc = f"runs/corr-c4-out/c4_ship6/{did}/pred.model_idx_0.cif"
        if not os.path.exists(cc):
            sys.exit(f"REFUSED: no Chai-1 output for {did}")
        chai = score(dpdb, cc)
        ef = [score(dpdb, c) for c in byseq.get(seqs[did], [])]
        ef = [x for x in ef if x is not None]
        if not ef:
            sys.exit(f"REFUSED: no existing ESMFold2 human complex found for {did} -- C4c "
                     f"forbids refolding, so this must be located, not regenerated")
        edq = statistics.median(x[0] for x in ef)
        elr = statistics.median(x[1] for x in ef)
        lo, hi = min(x[1] for x in ef), max(x[1] for x in ef)
        mind = min(chai[0], edq)
        worse = max(chai[1], elr)
        ok = worse <= dl.POSE_GATE_LRMS
        print(f"{row:>2} {did:30s} {chai[0]:7.4f} {chai[1]:9.3f} | "
              f"{edq:10.4f} {elr:12.3f} {len(ef):3d} {f'{lo:.2f}-{hi:.2f}':>16s} | "
              f"{mind:7.4f} {worse:10.3f}  {'PASS' if ok else 'FAIL'}")
        out.append((row, did, chai, edq, elr, len(ef), lo, hi, mind, worse, ok))

    print(f"\ntwo-oracle gate ({dl.POSE_GATE_LRMS} A on the WORSE oracle): "
          f"{sum(1 for x in out if x[10])} of {len(out)} pass")
    print("\nPREDICTION FROM THE PRE-REGISTRATION: rows 1-2 FAIL, rows 3-6 PASS")
    pred = {1: False, 2: False, 3: True, 4: True, 5: True, 6: True}
    hits = sum(1 for x in out if pred[x[0]] == x[10])
    print(f"scored: {hits} of 6 rows went the way the prediction said")
    for x in out:
        if pred[x[0]] != x[10]:
            print(f"  row {x[0]} {x[1]}: predicted {'PASS' if pred[x[0]] else 'FAIL'}, "
                  f"got {'PASS' if x[10] else 'FAIL'}")


if __name__ == "__main__":
    main()
