#!/usr/bin/env python3
"""D8: score 5 Chai-1 diffusion samples per shipped design against its Genie 3 backbone.

Governed by PREREG-D8-CHAI-CONSENSUS-2026-10-12.md. Bars, frozen before any fold existed:
  D8a  per design, median lrms over 5 samples and how many of 5 land inside POSE_GATE_LRMS
  D8b  sample 0 at seed 42 reproduces C4's single-draw lrms to within 0.5 A (a wiring check)
  D8c  the CONTROL rows -- 3, 4, 5, which passed C4 -- keep >=4 of 5 samples inside the gate

Reuses bin/c4_score.py's ESMFold2 index: existing folds only, never a refold (C4c).
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

_s = importlib.util.spec_from_file_location("dl", "bin/depth_loop.py")
dl = importlib.util.module_from_spec(_s)
sys.modules["dl"] = dl
_s.loader.exec_module(dl)

DESIGNED = "runs/genie3-out/probe50/tnfa_corrected/pdbs"
GATE = dl.POSE_GATE_LRMS

# (row, design, backbone, C4 one-sample lrms, role) -- C4 values from C4_result_2026-10-11.txt
ROWS = [
    (1, "tnfa_corrected_40_L1r4k6", "40", 26.134, "tested"),
    (2, "tnfa_corrected_40_L1r4k1", "40", 35.871, "tested"),
    (3, "tnfa_corrected_3_L0r4k0_L49H", "3", 2.890, "CONTROL"),
    (4, "tnfa_corrected_3_L0r4k0_quadH", "3", 2.365, "CONTROL"),
    (5, "tnfa_corrected_3_L0r4k0", "3", 2.920, "CONTROL"),
    (6, "tnfa_H_quadH_E3Q_k12", "3", 36.661, "tested"),
]


def score(designed_pdb, cif):
    offs = dl.numbering_offsets(designed_pdb, cif, "A", "D")
    r = dl._scd.sc_dockq(designed_pdb, cif, d_bind="A", p_bind="D", offsets=offs)
    return None if r is None else (r[0], r[2])


def main():
    print(f"{'#':>2} {'design':30s} {'role':8s} {'in-gate':>8s} {'med lrms':>9s} "
          f"{'lrms samples (A)':40s} {'med dq':>7s}")
    out = []
    for row, did, bb, c4_lrms, role in ROWS:
        dpdb = f"{DESIGNED}/tnfa_corrected_{bb}.pdb"
        cifs = sorted(glob.glob(f"runs/corr-d8-out/d8_b*/{did}/pred.model_idx_*.cif"),
                      key=lambda p: int(p.rsplit("_", 1)[1].split(".")[0]))
        if len(cifs) != 5:
            sys.exit(f"REFUSED: {did} has {len(cifs)} sample(s), expected 5")
        res = []
        for c in cifs:
            r = score(dpdb, c)
            if r is None:
                sys.exit(f"REFUSED: scorer returned nothing for {c}")
            res.append(r)
        lrms = [x[1] for x in res]
        dqs = [x[0] for x in res]
        n_in = sum(1 for x in lrms if x <= GATE)
        out.append((row, did, role, n_in, statistics.median(lrms), lrms,
                    statistics.median(dqs), c4_lrms, dqs))
        print(f"{row:>2} {did:30s} {role:8s} {f'{n_in}/5':>8s} "
              f"{statistics.median(lrms):9.3f} "
              f"{' '.join(f'{x:7.2f}' for x in lrms):40s} {statistics.median(dqs):7.4f}")

    print("\n--- D8b: does sample 0 at seed 42 reproduce C4's single draw? ---")
    ok_b = True
    for row, did, role, n_in, med, lrms, mdq, c4_lrms, dqs in out:
        d = abs(lrms[0] - c4_lrms)
        flag = "ok" if d <= 0.5 else "DRIFT"
        if d > 0.5:
            ok_b = False
        print(f"  row {row}: sample0 {lrms[0]:8.3f}  C4 {c4_lrms:8.3f}  delta {d:6.3f}  {flag}")
    print(f"  D8b {'PASS' if ok_b else 'FAIL'}")

    print("\n--- D8c: do the CONTROL rows hold (>=4 of 5 inside the gate)? ---")
    ctrl = [x for x in out if x[2] == "CONTROL"]
    ok_c = all(x[3] >= 4 for x in ctrl)
    for x in ctrl:
        print(f"  row {x[0]}: {x[3]}/5 inside {GATE} A  {'ok' if x[3] >= 4 else 'SCATTERED'}")
    print(f"  D8c {'PASS -- the predictor is placing these binders consistently' if ok_c else 'FAIL -- the control scattered, see prereg outcome 3'}")

    print("\n--- D8a: the three C4 failures, sampled ---")
    tested = [x for x in out if x[2] == "tested"]
    for x in tested:
        print(f"  row {x[0]}: {x[3]}/5 inside the gate, median {x[4]:.3f} A, "
              f"range {min(x[5]):.2f}-{max(x[5]):.2f}")
    fail4 = all(x[3] <= 1 for x in tested)      # >=4 of 5 OUTSIDE the gate
    soft = any(x[3] >= 2 for x in tested)

    print("\n=== PRE-REGISTERED VERDICT ===")
    if not ok_c:
        print("OUTCOME 3: the control scattered. C4 is WITHDRAWN as evidence about the designs")
        print("  and becomes a statement about the predictor. Submission text changes accordingly.")
    elif fail4:
        print("OUTCOME 1: rows 1/2/6 fail in >=4 of 5 samples and the control holds.")
        print("  The disagreement is SYSTEMATIC, not a draw. C4 stops being suggestive.")
        print("  Ranking unchanged (margin is the calibrated instrument); the failure is")
        print("  flagged harder and the shipping call goes to Harish with evidence.")
    elif soft:
        print("OUTCOME 2: at least one tested row lands inside the gate in >=2 of 5 samples.")
        print("  C4's single draw was unrepresentative; severity SOFTENED in the submitted")
        print("  text and the sample spread reported in place of the single number.")
    else:
        print("MIXED: between outcomes 1 and 2 -- report the spread per design, claim nothing more.")


if __name__ == "__main__":
    main()
