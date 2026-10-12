---
type: preregistration
project: anthropic-adaptyv-2026
problem: 02-tnf-alpha
arm: CORR — the corrective two-oracle re-run of rounds 4 and 5
status: PRE-REGISTERED — written 2026-10-11 7:30 PM EDT. Everything below is frozen BEFORE any
        corrective fold exists and BEFORE any new result is inspected.
---

# CORR — re-running rounds 4–5 under the two-oracle rule the original arm did not honour

## Why this exists

`PREREG-DEPTH-ARM-2026-10-08.md` required, from **round 4 onward**, that a design be carried forward
only if **both ESMFold2 and Chai-1** place it within `POSE_GATE_LRMS` of the designed backbone, with
the selector becoming the **minimum CA sc_DockQ across the two arms**. It fixed the fallback in
advance: *"If Chai-1's per-fold cost has not been measured by the time round 3 ends … then the arm
**stops at round 3** rather than continuing single-arm. Spending rounds 4 through 10 on one oracle is
the thing this stage exists to prevent, so the fallback is to stop, not to proceed unguarded."*

**Chai-1 was never wired into the loop.** Rounds 4 onward ran on ESMFold2 alone and all six shipped
designs descend from round 4. The reviewer's position, 2026-10-11: disclosure is necessary but does
not restore confirmatory status, and the remedy is a bounded corrective run from the last compliant
round-3 checkpoints, with both predictors participating in selection as originally specified.

🔴 **This run cannot erase the deviation.** The original results are preserved untouched. Whatever
this produces is reported as a **prospective correction informed by exploratory work** — not as the
original arm's result, and not as evidence that the shipped designs were correctly selected.
🔴 **Agreement between two predictors still does not establish binding.** Both are structure
predictors. Concordance bounds one failure mode (one oracle agreeing with itself) and nothing else.

## FROZEN: the starting checkpoints

The last compliant state is the end of round 3. Checkpoints are the round-3 winner per lineage by
CA sc_DockQ, which is what `depth_loop.select_parent` does, computed from the committed
`analysis/02-tnf/depth_rounds/round3.tsv`:

| lineage | checkpoint | round-3 CA sc_DockQ | lrms |
|---|---|--:|--:|
| backbone 3, L0 | `tnfa_corrected_3_L0r3k2` | 0.6037 | 2.576 |
| backbone 40, L1 | `tnfa_corrected_40_L1r3k5` | 0.6148 | 1.789 |
| backbone 40, L2 | `tnfa_corrected_40_L2r3k2` | 0.4464 | 4.513 |
| backbone 9, L3 | `tnfa_corrected_9_L3r3k5` | 0.0311 | 27.245 |

**L0 and L1 are the lineages that produced the shipped designs** (`3_L0r4k0`; `40_L1r4k1`,
`40_L1r4k6`). L2 and L3 are carried for comparability and are expected to fail the pose gate, as
they did originally.

## FROZEN: the selection rule, as originally specified

1. Each round: SolubleMPNN redesign on the **predicted complex**, chain D designed, A/B/C fixed,
   cysteine banned, `force_his=False`, `omit_acids=False` — byte-identical settings to the original.
2. Each design folded by **ESMFold2 AND Chai-1**, both against the human trimer.
3. **Pose gate: a design advances only if BOTH predictors place it within `POSE_GATE_LRMS`** of its
   designed Genie-3 backbone.
4. **Selector = `min(CA sc_DockQ_ESMFold2, CA sc_DockQ_Chai-1)`** per design. Not the mean, not
   either alone.
5. One parent per lineage, best by that minimum. Lineage depth tracked on root backbone id.
6. Rounds 4 and 5 only. **The run stops at round 5** regardless of outcome: the original arm's
   shipped designs are round-4 children and round 5 is the first round the original arm also ran, so
   two rounds is the bounded scope. No extension without a new pre-registration.

## FROZEN: seeds, budget, stopping rule

| | |
|---|---|
| seeds | ESMFold2 screening **seed 42**, matching the original arm exactly; Chai-1 default seed |
| MPNN seed | **37**, as in `redesign()` — unchanged |
| designs/round | 8 per lineage × 4 lineages = **32** |
| folds/round | 32 ESMFold2 + 32 Chai-1 = **64** |
| **hard fold fuse** | **160 folds total** across both rounds and both oracles |
| **wall stop** | **2026-10-12 06:00 EDT**, checked before each round |
| cost ceiling | ~$8 if Chai-1 costs what ESMFold2 does; **see the precondition below** |

## 🔴 FROZEN PRECONDITION: Chai-1's per-fold cost, measured before round 4 runs

The original pre-registration made the corrective action conditional on this and we are honouring
the condition rather than waiving it. **Phase 0: fold exactly 2 complexes with Chai-1 and record
wall-clock seconds per fold and peak memory.** Then:

- **If measured cost ≤ 120 s/fold:** proceed to rounds 4–5 under the rule above.
- **If > 120 s/fold:** the 160-fold fuse would be exceeded on cost rather than count. **Do not
  proceed single-arm.** Report the corrective arm as **infeasible**, and per the reviewer, present
  the affected findings as **exploratory** in the submission. That is the fallback and it is chosen
  now, not after seeing a number.

Chai-1 has run in this project before (`runs/chai1/`, 70 structures, problem 1) so the wrapper works;
its cost has never been measured, which is exactly the gap the original fallback anticipated.

## Bars

| bar | threshold | meaning |
|---|---|---|
| **C1** | both oracles place ≥1 round-4 design within the pose gate | the two-oracle gate is passable at all |
| **C2** | ≥1 design reaches `min(both) ≥ 0.60` | and reaches the pose quality the original arm claimed on one oracle |
| **C3** | per-design ESMFold2-vs-Chai-1 CA sc_DockQ correlation, reported with n | how much the second oracle was actually adding |
| **C4** | do any of the three shipped round-4 designs survive the two-oracle gate when re-folded | the question the breach actually raises |

**C4 is the one that matters.** C1–C3 describe the corrective arm; C4 asks whether what we are
shipping would have survived the rule we broke. A C4 failure does not disqualify the designs — the
margin, not the pose score, is the binding evidence — but it would have to be disclosed in those
terms.

## 🔴 What this cannot do

It cannot un-run the original arm, make the shipped designs confirmatory, or establish binding.
Rescoring only the six finalists with Chai-1 would be a robustness check and would **not** reproduce
the intended selection process, which is why this re-runs the rounds instead. If phase 0 fails its
precondition, the honest outcome is to say the correction was infeasible and relabel the affected
findings exploratory.

Deadline: **Mon Oct 19, 7:59 AM EDT.**

---

## AMENDMENT A1 — 2026-10-11, 7:52 PM EDT: the Chai-1 configuration, fixed before any timing was read

The body above fixed seeds and the selector but **not Chai-1's sample count**, and the wrapper
default emits **five** diffusion samples per fold. That would have forced a "which model index"
selection rule the original pre-registration never specified, and `depth_loop.score_round` refuses
a design directory holding more than one `.cif` — correctly, since picking among five
after the fact is exactly the freedom a prereg exists to remove.

**FROZEN: Chai-1 runs at `num_diffn_samples=1`, seed 42**, with the wrapper's
`num_trunk_recycles=3` and `num_diffn_timesteps=200`. This mirrors the ESMFold2 arm exactly —
that arm runs `--num-diffusion-samples 1 --seed 42` — so each oracle contributes **one structure
per complex**, and no model-index rule is needed because there is only one model.

🔴 **Disclosure, because it bears on the cost gate.** Phase 0 was launched once at the wrapper
default (5 samples), then aborted ~1 minute in, before any fold returned and **before any
wall-clock number was recorded or read**: the timing file was verified header-only at the abort and
the Modal container was stopped (`ap-pJ6HXnjZZCdis9Hw11F95A`). **The 120 s/fold threshold in the
body is left exactly where it was written.** Note plainly that moving to one sample makes that
threshold *easier* to pass than the configuration first launched — the sample count was chosen to
match the ESMFold2 arm and to eliminate the model-index freedom, not to clear the gate, and it was
fixed while no timing existed to shop against. A reader who thinks 120 s was set too loosely should
discount the gate, not the measurement.

## AMENDMENT A2 — 2026-10-11, 8:05 PM EDT: the round-4 parent set was wrong in the body above

The body derived the checkpoints **mechanically** — best CA sc_DockQ per lineage in `round3.tsv` —
which yields L0, L1, L2 and **L3** (backbone 9, 0.0311, lrms 27.245). That is not the parent set the
original arm carried into round 4, so reproducing it would not reproduce the original selection.

`run_depth_rounds.main()`'s `--parents` hook records what actually happened, verbatim: *"Used
2026-10-09 to retire L3 (backbone 9) after three rounds with 0 of 8 children inside the pose gate,
and to reseed its slot as L4 from backbone 3's second-best round-3 child, backbone 3 being the only
lineage still advancing."* The original round-4 table confirms it: lineages **L0, L1, L2, L4**, with
L4 on backbone 3 and no backbone 9 anywhere.

That retirement happened **before** round 4 and is part of the compliant round-3 → round-4
transition, so the corrective run inherits it rather than re-deciding it.

**FROZEN, replacing the body's table — the four round-4 parents:**

| lineage | checkpoint | backbone | round-3 CA sc_DockQ | lrms | role |
|---|---|--:|--:|--:|---|
| L0 | `tnfa_corrected_3_L0r3k2` | 3 | 0.6037 | 2.576 | shipped lineage (`3_L0r4k0`) |
| L1 | `tnfa_corrected_40_L1r3k5` | 40 | 0.6148 | 1.789 | shipped lineage (`40_L1r4k1`, `40_L1r4k6`) |
| L2 | `tnfa_corrected_40_L2r3k2` | 40 | 0.4464 | 4.513 | carried, as originally |
| L4 | `tnfa_corrected_3_L0r3k7` | 3 | 0.6007 | 2.607 | **reseeded slot**, replacing retired L3 |

**L3 (backbone 9) is not carried**, exactly as in the original. The body's claim that L2 and L3 were
"carried for comparability and expected to fail the pose gate, as they did originally" was wrong on
L3: L3 never entered round 4. Spending a quarter of the fold budget on it would have burned the
budget on a lineage the original arm had already retired, and would have left the reseeded L4 — one
of two backbone-3 lineages feeding the shipped designs — out of the corrective run entirely.

Nothing else changes: the dual-oracle pose gate, the minimum-sc_DockQ selector, 8 children per
parent, seeds, the 160-fold fuse and the wall stop all stand as written. **Human only**, as the
original untagged rounds 4–5 were (`round4.tsv` and `round5.tsv` carry no mouse column), which is
what the body's 32-folds-per-oracle-per-round arithmetic already assumed.
