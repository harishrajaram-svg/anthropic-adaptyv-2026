---
type: readout
project: anthropic-adaptyv-2026
problem: 02-tnf-alpha
arm: C13 overnight two-arm depth run
prereg: analysis/02-tnf/PREREG-C13-TWO-ARMS-2026-10-11.md
written: 2026-10-11 8:30 AM EDT
---

# C13 readout — both arms stopped themselves, and together they close objective 2

Arm A ran 04:11–04:59, 7 rounds, 448 folds (~$16.62). Arm B ran 04:08–05:39, 13 rounds, 832 folds
(~$30.87). Both stopped on the pre-registered plateau rule, neither hit the 1200-fold fuse or the
07:00 wall. Total ~$47.49 against the ~$80 estimate.

## Bars, as pre-registered

| bar | threshold | result |
|---|---|---|
| **A1** | any design `ca_sc_dockq` ≥ 0.60 | **FAIL** — 0 of 224, best **0.3407** |
| **A2** | 5-seed margin ≥ +6.347 | not measured; A1 leaves no pose to measure |
| **A3** | coupled ratio < 1.0, ≥4/5 seeds | not measured, same reason |
| **B1** | human margin ≥ +7.706 | not measured — see "the premise is falsified" |
| **B2** | mouse margin ≥ +6.347 at the end gate | **FAIL at the pose level** — 0 of 416 clear 0.60 on both species |
| **B3** | coupled ratio < 1.0 in ≥1 design | **FAIL** — 9 of 9 inverted, 4.93x to 157.60x |

## Arm A — the acid ban closes by measurement, not by n=4

224 designs, 0 ≥ 0.60, best 0.3407, best lrms 5.958 A. Round 0 (the unconstrained parent pool)
scored 0.6057 and every constrained round after it scored 0.25–0.34. The Oct 9 result was n=4 and
the honest objection was sample size; at n=224 the objection is gone. **An interface stripped of
carboxylates does not hold this pose.** A2/A3 were conditional on a pose existing and are not
reported.

## Arm B — the selector fix made it worse, which falsifies LESSONS §§9-12

The v3 arm's defect was real (it selected on `min(human, mouse)`, so mouse, ~0.2 lower, was almost
always the selector). Fixing it predicted better human poses. It produced **fewer and worse** ones:

| arm | selector | designs | n human ≥ 0.60 | best human |
|---|---|--:|--:|--:|
| v3 (defective) | `min(human, mouse)` | 480 | **30** | **0.7776** |
| B (fixed) | human | 416 | 9 | 0.6529 |

Arm B's trajectory declines monotonically after round 2 (0.6057, 0.6529, 0.6515, 0.6282, 0.4857,
... 0.4526). The worse-of-two selector was acting as a **regulariser**: requiring both species held
the lineages to poses that generalised, and removing that requirement let the loop chase a
human-specific optimum that did not survive its own next round. B1 is left unmeasured because the
hypothesis that justified spending folds on a margin measurement is dead — and the ceiling it
reached, 0.6529, is below the arm it was built to beat.

**B2 fails before any margin.** Zero of 416 designs clear 0.60 on both species. Best mouse anywhere
in the arm is 0.6119 (human 0.1347); best mouse among the nine 0.60+ human designs is 0.5561.
Cross-species does not survive when it is not selected on. Several of the best human poses are
actively bad on mouse (0.0731, 0.1261, 0.2385).

## B3 — the pincer, and the reason

All nine designs ≥ 0.60 human were scored with the binding-coupled gate (`bin/ph_gate_multisite.py`,
`--problem 2`, selftest 11/11 before the run). Problem 2 needs **ratio < 1.0**. Observed: **7.33,
22.20, 15.62, 9.02, 4.93, 157.60, 72.76, 9.28, 10.37** — nine of nine inverted, none close to 1.0.

The per-site breakdown is unanimous across the arm. Of 51 sites the gate moved:

- **40 push the wrong way**, 12 of them explicitly glutamate
- **every one of the 9 sites that helps is a histidine** — target H73, 0.372x to 0.444x in all nine

So the arithmetic of objective 2 on this target: the only site that wants to release is a target
histidine worth roughly 0.4x, and the interface carboxylates it must overcome are worth 5x to 157x
the other way. **Arm A proves an interface without those carboxylates cannot bind; arm B proves an
interface that binds has them and is inverted by them.** The two arms are a pincer and objective 2
has no route between them by this method.

**Independent confirmation of A3.** The gate reads binder **HIS61 at 3.10x–3.40x, wrong direction,
free 6.54–6.60 → bound 7.42** in every design that carries it. A3's `ctrlH61Q` control reached the
same conclusion by a different route — knocking His61 out collapsed the margin from +8.031 to
+0.916, so it is a load-bearing anchor that tightens on protonation. Two methods, one answer:
His61 is an anti-switch.

## What this does not say

The gate's magnitude is noise (pooled SD 1.499; ~123 seeds to resolve 0.5) and only the **sign** is
reportable — nine of nine is a sign result, at one seed per molecule. The ratio has no calibration
against the assay, because the released campaign carries no pH labels. This is a predicted
direction, consistently wrong, with the cause localised and now measured on both sides of the
constraint. It is not a measured switch, and it never could have been from here.

## Closure count

Objective 2 is now closed **nine** ways. C13 is the ninth, and the first that closes it by
exclusion on both sides rather than by one failed mechanism.
