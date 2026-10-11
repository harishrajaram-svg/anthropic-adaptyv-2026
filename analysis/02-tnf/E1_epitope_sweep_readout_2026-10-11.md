---
type: readout
project: anthropic-adaptyv-2026
problem: 02-tnf-alpha
arm: E1 epitope sweep
prereg: analysis/02-tnf/PREREG-E1-EPITOPE-SWEEP-2026-10-11.md
written: 2026-10-11 9:00 AM EDT
cost: $0
---

# E1 readout — the stop condition did not fire, and the candidate was in the arm I called defective

1,344 poses scored (1,200 designs + 144 shuffled-binder nulls), 8 workers, 18 minutes, **$0**.
Zero refusals. Pool deduped on binder **sequence content**; 1,551 mouse complexes refused by the
gate's histidine fingerprint.

## Bars

| bar | threshold | result |
|---|---|---|
| **E1** | any pose `target_owned` < 1.0 | **PASS** — 214 of 1,200, min **0.2896** |
| **E2** | a ≥5-pose fingerprint class with median < 1.0 | **PASS** — 3 of 31 classes |
| **E3** | pool min ≥ 1.0 → stop | **did not fire** (min 0.2896) |
| **E4** | Glu146 raises `target_owned`, p < 0.05 | **PASS** — p = **8.5e-46** |

`target_owned` over the pool: min 0.2896, median 1.7307, max 427.59; 214 below 1.0.
`binder_owned`: min 0.1184, median 2.7739, 126 below 1.0. **Total: min 0.0671, 70 below 1.0.**

## E3 did not fire, so the target does not forbid it

The C13 decomposition saw target-owned above 1.0 in 9 of 9 and floor 1.318. At n=1,200 the floor is
**0.2896** and 214 poses are below 1.0. **TNF-alpha's own electrostatics do not close objective 2.**
My estimate an hour ago — best binder half 0.744 times best target half 1.318 = 0.981, "break-even"
— was drawn from nine molecules and understated the available budget by a wide margin.

## E4 confirms Glu146, and names the epitope to aim at

Glu146 contributes in 863 of 1,200 poses. Where it contributes, median `target_owned` is **2.4834**;
where it does not, **1.0538** (p = 8.5e-46). It is the single largest term in the problem.

The three passing fingerprint classes are all **H73 with little else**:

| class | n | median | min |
|---|--:|--:|--:|
| `H73` alone | 51 | **0.8697** | 0.4632 |
| `GLU110,H73` | 23 | 0.9668 | 0.5937 |
| `ASP143,H73` | 49 | 0.9983 | 0.3440 |
| `GLU146` (for contrast) | 46 | 1.1299 | 1.0505 |
| `GLU110,GLU146,H73` | 59 | 1.3636 | 0.5861 |

Target sites ranked by median contribution: GLU146 1.781x (n=863, max 24.7), **H73 0.799x (n=829)**,
ASP143 1.119x, GLU127 1.320x, GLU110 1.148x, GLU135 1.187x. H73 is the only target site whose median
helps.

## 🔴 The control, which limits what any of this means

Shuffled-binder nulls: median `target_owned` 1.5758 against the designs' 1.7307, **13 of 144 (9.0%)
below 1.0**, designs-vs-nulls one-sided p = **0.693**. A scrambled, non-binding chain reaches
`target_owned` < 1.0 almost as often as a designed one. So **`target_owned` < 1.0 on its own is close
to what random lands at and is nearly worthless as a selection criterion.** What the sweep licenses
is selection on the *epitope class*, which the E2 table shows does move the quantity by 1.6x between
`H73`-alone and `GLU110,GLU146,H73`; it does not license selection on the number itself, and it says
nothing about sequence design improving it.

## The two candidates, and where they came from

Joining the sweep against pose quality: of 58 poses at DockQ ≥ 0.60, **2 have total product < 1.0**.

| design | DockQ human | mouse | total | target | binder |
|---|--:|--:|--:|--:|--:|
| `40_L3r2k2` (seed 5) | **0.7593** | 0.4171 | **0.7694** | 0.7820 | 0.9009 |
| `40_L3r2k7` (seed 5) | 0.7417 | 0.3772 | 0.9556 | 1.4628 | 0.6405 |

**Both are from the v3 arm** — the one whose selector I called defective this morning. The best human
poses this project has produced all came from there, and two of its top six also point the right way.
C13-B3's "9 of 9 inverted" was measured on arm B's nine designs, which were the wrong nine.

`40_L3r2k2`, site by site: **no wrong-way site above 1.1x**, three helping.

| site | ratio | | free → bound |
|---|--:|---|---|
| target A/H73 | **0.808x** | helps | 5.40 → 3.00 |
| target C/GLU146 | **0.917x** | helps | 5.03 → 4.07 |
| binder HIS61 | **0.755x** | helps | 6.57 → 6.38 |
| target C/ASP143 | 1.055x | wrong | 4.35 → 4.91 |
| binder ASP50 | 1.089x | wrong | 3.64 → 4.99 |
| binder GLU47 | 1.095x | wrong | 4.54 → 5.14 |

## Two corrections to what I said earlier today

**His61 is not an anti-switch.** I wrote this morning that the gate and A3's `ctrlH61Q` control
agreed His61 tightens on protonation — "two methods, one answer." Here the same residue in the same
83-mer reads **0.755x, helping**, free 6.57 → bound 6.38, against 2.10x–3.40x wrong in every C13
design. The sign is a property of the **pose**, not of the residue. A3's result stands for the
shipping leader's pose; the general claim does not, and FIELD 2 should not make it.

**Glu146 is not deterministic.** In `40_L3r2k2` it reads 0.917x, helping — binding lowers its pKa
instead of raising it. E4's p = 8.5e-46 is an average over 863 poses, and the useful designs live in
its tail.

## What this does and does not establish

One seed per pose, and the gate's magnitude is noise (pooled SD 1.499) so only the sign is
reportable — 0.7694 against 1.0 sits inside that noise at n=1. Neither candidate has a 5-seed
margin, so **neither has been shown to bind**; DockQ is a pose score, not an affinity. Both fail
mouse at the pose level (0.4171, 0.3772), so neither answers the cross-reactivity objective. There
is no calibration against the assay.

## The measurement that would settle it

`40_L3r2k2` and `40_L3r2k7`: 5-seed margin on both species plus nulls, and the gate re-run on all
five seeds to test whether the sign replicates — the test C6 and C9 both failed. **40 folds, ~$1.80,
~15 minutes on B200.** That is the cheapest decisive experiment left in this problem, and unlike
everything else in objective 2 it would be a *measured* direction on a pose that also holds.
