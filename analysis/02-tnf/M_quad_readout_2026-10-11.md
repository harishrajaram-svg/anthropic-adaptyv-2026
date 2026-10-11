---
type: readout
project: anthropic-adaptyv-2026
problem: 02-tnf-alpha
arm: M — marginal scaffold, four buried histidines
prereg: analysis/02-tnf/PREREG-ROUTES-123-2026-10-11.md
written: 2026-10-11 9:45 AM EDT
cost: ~$0.70, 15 folds on B200
---

# Arm M readout — all three bars pass, and the route's own ceiling is now measured

Construct: **`tnfa_corrected_3_L0r4k0` + V45H + L53H + L63H + L64H**. The parent carries **zero**
histidines; the quad carries four. Construction was validated before use by rebuilding C9e's
`A60H` input from the canonical sequence TSV and requiring a byte-for-byte match — it matched, so
the mutation path is sound.

| bar | threshold | result |
|---|---|---|
| **M1** | 5-seed monomer pLDDT ≥ 0.70 | **PASS — 0.8169** (0.8152–0.8177) |
| **M2** | summed fold-destabilisation ≥ +2.00 kcal/mol | **PASS — +3.064** |
| **M3** | 5-seed complex margin ≥ +6.3473 | **PASS — +7.1306** (SD 0.112) |

## M3 — four buried histidines cost nothing in binding

| | design (s1–s5) | null median | margin | SD |
|---|---|--:|--:|--:|
| quad | 7.710 7.957 7.690 7.826 7.722 | 14.8526 | **+7.1306** | **0.112** |

That is **better than the parent's +6.967 human**, better than `40_L3r2k2`'s +6.7522, and the
tightest dispersion measured in this problem. Complex pLDDT median 0.8682. Burying four
histidines in the core did not cost the interface anything.

## M2 — the depressions not only survived being combined, they deepened

PROPKA 3.5.1 on the quad monomer, 5 seeds, all four sites scored in all five (20 measurements):

| pos | pKa in quad | pKa as a single (C9e) | shift | destab. in quad | % of ceiling |
|---|--:|--:|--:|--:|--:|
| H45 | **2.43** | 4.26 | **−1.83** | +0.775 | **100.0%** |
| H53 | 4.38 | 4.58 | −0.20 | +0.762 | 98.3% |
| H63 | 3.79 | 4.30 | −0.51 | +0.772 | 99.5% |
| H64 | 4.55 | 5.03 | −0.48 | +0.756 | 97.4% |
| **sum** | | | | **+3.064** | |

Additivity was an assumption and it held at **102.1%** — the singles predicted +3.001 and the quad
delivers +3.064. `propka_his.py` classes all 20 measurements **"inert"** because its `delta_protonation`
is a *binding* quantity (0.000–0.044 here); read as *folding* linkage the same numbers are at
97–100% of their maximum. That inversion is the whole premise of this arm and it is now confirmed on
the quadruple rather than inferred from singles.

## 🔴 The ceiling this arm also measured, which is a limit on the route

Fold-destabilisation per histidine **saturates at +0.775 kcal/mol** as pKa_folded falls, because the
unfolded reference (6.5) fixes the numerator. All four sites sit at 97–100% of it. **Depth is
exhausted; the only remaining lever is count:**

| target destabilisation | buried histidines needed |
|---|--:|
| 2 kcal/mol | 3 |
| 3 kcal/mol | 4 |
| 4 kcal/mol | 6 |
| 6 kcal/mol | 8 |
| 8 kcal/mol | 11 |

For scale, the gate's best **reproducible** interface term (H73 at 0.7986x) is **+0.133 kcal/mol**, so
the quad core is **23x** the best the interface has ever offered. That is the largest pH-responsive
energy measured anywhere in this project.

## 🔴 What this does not establish, and the number that decides it

**+3.064 kcal/mol against an unknown ΔG_fold.** If the quad is 8–10 kcal/mol stable — ordinary for a
designed miniprotein — then 3 kcal/mol does not unfold it and the route produces nothing. **pLDDT is
a confidence score and cannot be converted to stability**, so M1's 0.8169 does not answer this. The
parent sits at 0.910 and the quad at 0.8169, which is a drop in the direction this route wants, but
it is not a free energy. **Measuring ΔG_fold is the next thing this route needs and nothing on hand
measures it.**

ESMFold2 is pH-agnostic and cannot show unfolding, so no pH switch is demonstrated by any of the
above. The whole calculation rests on PROPKA pKa values for deeply buried histidines — its weakest
regime — and **H45 at pKa 2.43 is a four-unit depression and the single most questionable number
here**; it may be genuine desolvation or bad extrapolation, and the arm cannot tell which.

## Note on where the output landed

`OUT_DIR` was passed relative and `score-esmfold2.sh` cd's into `biomodals/`, so results are at
**`biomodals/runs/M-quad-out/Mquad`** rather than `runs/M-quad-out`. The script's own header warns
about this class of path bug; nothing was lost, all 45 files are present, and the readout reads them
in place.
