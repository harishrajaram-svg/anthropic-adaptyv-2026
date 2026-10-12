---
type: preregistration
arm: D8 — does C4's three-of-six failure survive sampling?
status: PRE-REGISTERED 2026-10-12, 9:25 AM EDT, before any 5-sample fold exists
---

# D8 — C4 was one diffusion draw per design. This samples it, with a control.

C4 scored each of the six shipped designs on **one** Chai-1 sample and found rows 1, 2 and 6 at
26.1, 35.9 and 36.7 Å from their designed backbones while rows 3, 4 and 5 agreed with ESMFold2 at
2.4–3.1 Å. One unsampled draw is the weakest version of that test, and the reviewer's standing
correction on the calibration applies here too: an underpowered measurement does not establish its
conclusion.

## 🔴 FROZEN: all six designs, not only the three that failed

**The three that PASSED are the control, and they are the reason this is worth running.** Sampling
only the failures could not distinguish "rows 1, 2 and 6 are robustly misplaced" from "five Chai-1
samples scatter on this system generally". Rows 3, 4 and 5 passing at one sample and holding at five
is what makes the failures mean something; rows 3, 4 and 5 also scattering would mean C4 said
little about any design and mostly measured the predictor.

| row | design | C4 one-sample lrms | C4 call |
|--:|---|--:|---|
| 1 | `tnfa_corrected_40_L1r4k6` | 26.134 Å | FAIL |
| 2 | `tnfa_corrected_40_L1r4k1` | 35.871 Å | FAIL |
| 3 | `tnfa_corrected_3_L0r4k0_L49H` | 2.890 Å | PASS — **control** |
| 4 | `tnfa_corrected_3_L0r4k0_quadH` | 2.365 Å | PASS — **control** |
| 5 | `tnfa_corrected_3_L0r4k0` | 2.920 Å | PASS — **control** |
| 6 | `tnfa_H_quadH_E3Q_k12` | 36.661 Å | FAIL |

## FROZEN: settings and scoring

| | |
|---|---|
| sampling | `num_diffn_samples=5`, **seed 42** — the same seed as C4, so sample 0 is expected to reproduce C4's number and is a built-in check that nothing else changed |
| inputs | byte-identical to the C4 input directory, which was built from `outbox/prescreen-ship6-2026-10-11/ship6.fasta` |
| ESMFold2 | unchanged, from existing folds as in C4c. **No refolding.** |
| containers | 2 × 3 designs, for wall time; `TIMEOUT=60` sized from 5 × ~69 s diffusion + ~89 s load ≈ 434 s/design |
| scoring | per sample: CA sc_DockQ and lrms against the design's own Genie 3 backbone, offsets derived |
| cost | 6 designs × 5 samples ≈ 2,600 GPU-s ≈ **$1.60** |

⚠️ **This is within-seed diffusion sampling, not seed replication.** Five samples at seed 42 test
whether the model places the binder consistently; they do not test seed-to-seed variation, which
would be a different and more expensive claim. Declared now so the result is not read as more than
it is.

## FROZEN: bars, and what each outcome does to the shipping decision

| bar | threshold |
|---|---|
| **D8a** | per design: median lrms over 5 samples, and **how many of 5** land within `POSE_GATE_LRMS` = 10.0 Å |
| **D8b** | sample 0 at seed 42 reproduces C4's lrms to within 0.5 Å — a wiring check, not a result |
| **D8c** | the control rows hold: rows 3, 4 and 5 keep ≥4 of 5 samples inside the gate |

**Decided now, before the numbers exist, because this is the decision the run is for:**

1. **If rows 1/2/6 fail in ≥4 of 5 samples AND D8c holds** — the disagreement is systematic, not a
   draw. C4 stops being suggestive. The submission reports it as a **sampled** two-oracle failure on
   three designs, and the shipping question goes to Harish with evidence rather than a caveat.
   **The ranking still does not change**: the margin instrument is the one with an external
   calibration, and `min(sc_DockQ)` was never the ranking basis. What changes is how loudly the
   failure is flagged, not the order.
2. **If rows 1/2/6 land inside the gate in ≥2 of 5 samples** — C4's one draw was unrepresentative
   and its severity is **softened in the submitted text**, with the sample spread reported in place
   of the single number.
3. **If D8c FAILS — the control rows scatter too** — then Chai-1 is not placing binders reliably on
   this system and **C4 is withdrawn as evidence about the designs**, becoming a statement about the
   predictor. This is the outcome that would most change what the submission says, and it is the one
   I think least likely, which is exactly why the control is in the run.

🔴 **No outcome here makes any design confirmatory, and none of it establishes binding.** Two
predictors agreeing bounds one failure mode. This also does not revive the corrective rounds-4–5
re-run, which stopped on its own cost ceiling and stays stopped: 5 samples per design makes the
per-fold cost worse, not better.

Close: **Mon Oct 19, 7:59 AM EDT.**
