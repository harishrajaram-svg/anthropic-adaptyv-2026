---
type: readout
arm: CORR phase 0 — Chai-1 cost measurement and wiring check
prereg: PREREG-CORR-TWO-ORACLE-2026-10-11.md (+ amendments A1, A2)
date: 2026-10-11, 8:52 PM EDT
---

# CORR phase 0: the cost gate FAILS as written, and the wiring check found something

## 1. The measurement the original pre-registration asked for and never got

Two complexes, one diffusion sample, seed 42, A100, human trimer + binder (554 residues), each a
separate `modal run` invocation, sequentially timed:

| # | design | wall s | rc |
|--:|---|--:|--:|
| 1 | `tnfa_corrected_3_L0r3k2` | **184** | 0 |
| 2 | `tnfa_corrected_40_L1r3k5` | **185** | 0 |

**Mean 184.5 s/fold. There is no cold/warm spread** — 184 against 185 — because `modal_chai1.py`
takes one FASTA per remote call, so every fold pays its own container start and model load
(~110 s) on top of ~70 s of diffusion (199 steps at 2.86 it/s, from the log).

🔴 **The pre-registered gate was ≤ 120 s/fold, and every statistic of this sample exceeds it:**
min 184, mean 184.5, max 185. The ambiguity I was worried about in my own prereg — mean or max or
cold or warm — turns out not to matter, so no choice of statistic rescues the arm. **Under the rule
as frozen, the corrective arm stops and the affected findings are relabelled exploratory.**

**What the gate does NOT say, and should be read alongside it.** At Modal's A100 rate (~$2.10/hr,
$0.000583/s), 184.5 s is **~$0.108 per fold**. The arm needs 64 Chai-1 folds (32/round × 2 rounds),
so the Chai side is **~$6.90**, and with the ESMFold2 side the whole arm is **~$9–11** and well
under an hour of wall clock if folds run concurrently. **The threshold that blocks this run is a
time proxy I set for affordability, and the thing it was a proxy for is affordable.** The ORIGINAL
depth-arm prereg's condition was only that the cost *be measured* before continuing past round 3 —
"if Chai-1's per-fold cost has not been measured … the arm stops at round 3" — and it is now
measured. The 120 s number is mine, from this prereg, not inherited.

**A like-for-like caveat on the comparison.** ESMFold2's 25.8 s/fold is a *batched* number: the
local patch loops folds inside one container, so model load amortises across the batch. Chai-1's
184.5 s is *unbatched*, one container per fold. Comparing them is comparing unlike things, and the
120 s threshold was set with the batched figure in mind.

## 2. The wiring check: the pipeline works, and one of two checkpoints fails the second oracle

Amendment A1's one-sample setting produced **exactly one CIF** per fold with chains
**A/B/C = 157** (human trimer) and **D = 83** (binder) — the layout `depth_loop.score_round`
requires, offsets derived as `(0, 5, -5)`. Scored against each design's own Genie 3 backbone:

| checkpoint | lineage | Chai-1 sc_DockQ | ESMFold2 sc_DockQ | min | Chai-1 lrms | ESMFold2 lrms |
|---|---|--:|--:|--:|--:|--:|
| `tnfa_corrected_3_L0r3k2` | L0 | 0.5813 | 0.6037 | 0.5813 | **2.044** | 2.576 |
| `tnfa_corrected_40_L1r3k5` | L1 | **0.0214** | 0.6148 | 0.0214 | **34.135** | 1.789 |

🔴 **L1 is the lineage behind two of the six shipped designs** (`40_L1r4k1`, `40_L1r4k6`), and it is
the single best checkpoint ESMFold2 produced in round 3 — 0.6148, lrms 1.789 Å. **Chai-1 puts the
same binder 34.1 Å from its designed pose.** That checkpoint would **fail the two-oracle pose gate
outright** (34.135 > `POSE_GATE_LRMS` 10.0). L0, the other shipped lineage, agrees closely between
the two oracles.

**This is the failure mode the breached guard existed to catch, and it appears at the first place we
looked.** It is also, at n = 2, nowhere near conclusive. Three reasons to hold it loosely:

1. **n = 2.** One agreement, one disagreement.
2. **One diffusion sample.** A single Chai-1 draw is noisier than its 5-sample default; a 34 Å
   pose could be one bad draw. The one-sample setting was chosen (A1) to mirror the ESMFold2 arm
   and to avoid an arbitrary model-index rule, and it was fixed before any of this was visible.
3. **No MSA.** Chai-1 ran on ESM embeddings alone, which is the weaker configuration for it.

**It is a round-3 result and it changes nothing frozen.** Parents, seeds, the pose gate and the
minimum-sc_DockQ selector all stand exactly as amendments A1 and A2 left them. But it must be
declared, because anything that happens next is now **informed by it** — which is precisely the
"prospective correction informed by exploratory work" framing the reviewer asked for, and the
reason this paragraph exists rather than being discovered later in the repo.

## 3. Where that leaves the arm

Under the frozen rule: **stopped, findings exploratory.** The decision to run it anyway is not one
this phase can make for itself, because relaxing a threshold after seeing the number it failed is
the move the whole pre-registration discipline exists to prevent — even when, as here, the
threshold looks like the wrong instrument and the true cost is $7. Bar **C4** — do the shipped
designs survive the two-oracle gate — is now the most decision-relevant unknown in the submission,
and phase 0 is the first evidence that its answer might be no.

Spend for phase 0: **2 folds, ~$0.22.**

---

# Phase 0b: the patch worked, the prediction was wrong, and the arm stops

Amendment A3 predicted, in writing and before the number existed, **marginal ≈ 70 s** and **all-in
≈ 84 s** against the unchanged 120 s gate. Measured, same two complexes, one container:

| quantity | predicted (A3) | measured | gate | |
|---|--:|--:|--:|---|
| fold 1, load + fold | — | 163.6 s | | |
| **marginal per-fold** | **~70 s** | **157.7 s** | 120 s | 🔴 **fails** |
| **all-in at 8 folds/container** | **~84 s** | **157.7 s** | 120 s | 🔴 **fails** |
| container total, n=2 | — | 321.4 s | | |

**The prediction was wrong, and that is why it was written down.** Batching saved **26.8 s/fold**
(184.5 → 157.7) — container start and image pull, nothing more. The diffusion is ~69 s, so roughly
**89 s per call is model load that happens INSIDE `run_inference`**, on every invocation, whether or
not the container is reused. That is the difference from ESMFold2, whose patch loads the model once
*outside* its fold loop; `chai_lab.chai1.run_inference` is a single entry point that loads on entry,
so batching cannot reach it. Hoisting that load would mean reimplementing the library's internals,
and A3 foreclosed it in advance: **"no further re-measurement, no third framing."**

🔴 **The corrective arm therefore STOPS, under the rule as frozen.** Per the body and A3, the
affected findings are relabelled **exploratory** in the submission. The arm got as far as: a
pre-registration with two amendments, a working two-oracle pipeline, a 7/7 selftest on the selection
rule, and four folds.

**Said plainly, so no reader has to reconstruct it: the blocker is not money.** At ~$0.092/fold
(157.7 s × $0.000583/s) the full 64-fold Chai-1 side is **~$5.90** and the whole arm **~$9**, under
an hour of wall clock, with six days to the deadline. What stopped it is a per-fold time threshold
I set and then failed twice — once on a measurement that mixed in model load, once after a patch
that removed the wrong 27 seconds. A reader who concludes the threshold was the wrong instrument is
reading it correctly. It was still the instrument that was frozen, and the point of freezing one is
that it binds on the occasions when it costs something.

## The L1 disagreement, re-scored on the second container

Both checkpoints were folded again in the batched run. **Same seed (42), so this measures
determinism, not independent sampling:**

| checkpoint | Chai-1 unbatched | Chai-1 batched | ESMFold2 |
|---|--:|--:|--:|
| `3_L0r3k2` (L0) | 0.5813 / 2.044 Å | 0.5808 / 2.040 Å | 0.6037 / 2.576 Å |
| `40_L1r3k5` (L1) | **0.0214 / 34.135 Å** | **0.0214 / 34.108 Å** | 0.6148 / 1.789 Å |

This rules out a one-off glitch in a single container. It does **not** address the real caveat:
one diffusion sample at one seed. A different seed could place that binder differently, and nothing
here tests that. So the finding stands exactly where phase 0 left it — **n = 2 complexes, one seed,
one sample, no MSA, suggestive and not conclusive** — and it is reported as exploratory, which is
also what the arm's stop requires of it.

Phase 0 total spend: **4 Chai-1 folds, ~$0.45.**
