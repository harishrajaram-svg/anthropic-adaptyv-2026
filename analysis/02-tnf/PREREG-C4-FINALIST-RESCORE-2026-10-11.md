---
type: preregistration (bar C4 of the CORR arm)
arm: C4 — rescoring the six shipped designs on the second oracle
status: PRE-REGISTERED 2026-10-11, 9:40 PM EDT, before any finalist has been folded by Chai-1
---

# C4 — do the six designs we are shipping survive the oracle the loop never consulted?

## What this is, and what the reviewer already said it is not

The reviewer, 2026-10-11: *"Rescoring only the six finalists with Chai-1 would be a useful
robustness check, but would not reproduce the intended selection process."* Both halves are
accepted. The corrective rounds-4–5 re-run — the half that WOULD have reproduced selection —
stopped on its own pre-registered cost ceiling (`PREREG-CORR-TWO-ORACLE-2026-10-11.md`, phase 0b:
157.7 s/fold against a frozen 120 s). This is the other half, the one the reviewer called useful,
and it is reported as a **robustness check on designs already chosen**, never as evidence that the
choosing was sound.

🔴 It cannot restore confirmatory status, and **two structure predictors agreeing still does not
establish binding.** What it can do is tell a reviewer deciding which designs reach a well whether
the second predictor puts our binders where we say they are.

## FROZEN: inputs

The exact six sequences submitted, from `outbox/prescreen-ship6-2026-10-11/ship6.fasta` (the same
file Adaptyv's prescreen was run on), each folded against the **human** sequence-corrected trimer:

| row | design | root backbone |
|--:|---|--:|
| 1 | `tnfa_corrected_40_L1r4k6` | 40 |
| 2 | `tnfa_corrected_40_L1r4k1` | 40 |
| 3 | `tnfa_corrected_3_L0r4k0_L49H` | 3 |
| 4 | `tnfa_corrected_3_L0r4k0_quadH` | 3 |
| 5 | `tnfa_corrected_3_L0r4k0` | 3 |
| 6 | `tnfa_H_quadH_E3Q_k12` | 3 |

Chai-1 at **one diffusion sample, seed 42**, batched in one container — identical settings to
phase 0 (amendment A1), so the phase-0 checkpoint numbers and these are on one scale. Scored by
`depth_loop.score_round`'s path: CA sc_DockQ and lrms against each design's own Genie 3 backbone,
numbering offsets derived, never fixed.

## FROZEN: what counts as what, decided now

| | |
|---|---|
| **C4a** | a design is **two-oracle consistent** if BOTH predictors place it within `POSE_GATE_LRMS` = 10.0 Å of its designed backbone |
| **C4b** | reported per design, not pooled: the full table goes in the submission whichever way it falls |
| **C4c** | ESMFold2's own numbers come from the committed round tables and existing folds — **no refolding**, so the comparison cannot be moved by a fresh ESMFold2 draw |

**Declared in advance, because it is the obvious way to fudge this:** if some designs pass and
others fail, **the ranking does not change.** Rows are ranked on worse-of-two-species margin, which
is the calibrated instrument; sc_DockQ agreement is a disclosure, not a selector. Re-ranking on a
quantity measured after the fact, on n=1 sample per design, is exactly the overfitting the breached
guard existed to prevent. A failing design stays in its current row **with the failure stated next
to it.**

**Prediction, written before folding.** Phase 0 scored the two round-3 parents: L0 agreed across
oracles (0.5813 vs 0.6037) and L1 did not (0.0214 / 34.1 Å vs 0.6148 / 1.789 Å). Rows 1 and 2
descend from L1; rows 3, 4, 5 from L0; row 6 from the L0 line via arm H. So the prediction is
**rows 1 and 2 fail C4a, rows 3–6 pass.** If rows 1 and 2 pass, the phase-0 L1 result does not
propagate to its children and should be de-emphasised. If rows 3–6 fail too, the disagreement is
general and the whole set's pose quality is in question.

Cost: 6 folds, one container, ~$0.55, ~18 minutes. Outside the CORR arm's 160-fold fuse, which
governed the rounds re-run; this spends 6 folds on molecules already chosen and generates no new
candidates.
