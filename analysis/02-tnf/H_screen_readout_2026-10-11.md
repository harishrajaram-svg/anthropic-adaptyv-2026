---
type: readout
project: anthropic-adaptyv-2026
problem: 02-tnf-alpha
arm: H screen (48 designs, 1 seed)
prereg: analysis/02-tnf/PREREG-H-REBUILD-2026-10-11.md
written: 2026-10-11 11:58 AM EDT
---

# Arm H screen — the rebuild recovers the hold and five designs keep the direction

48 designs, 1 seed each, no matched nulls. **Interface PAE is a PROXY for the margin here,**
not the margin: every matched null measured today sits at 14.5-14.9, so a design's pae_if_mean
orders candidates and implies a margin, but H1 is not passed until the 5-seed run with its own
nulls says so.

## Per parent

| parent | own pae | best redesign | recovered | gap to close | own gate | redesigns gate<1.0 |
|---|--:|--:|--:|--:|--:|--:|
| `L49H_E4Q` | 8.297 | **7.332** | **+0.965** | 0.0125 | 0.8538 | 2 of 16 |
| `quadH_E3Q` | 8.628 | **7.559** | **+1.068** | 0.1225 | 0.9468 | 4 of 16 |
| `s3_22k4` | 9.213 | **8.367** | **+0.846** | 1.7624 | 0.8097 | 5 of 16 |

## Designs satisfying both halves at screen level (gate < 1.0 AND pae < 9.0)

| design | pae_if_mean | gate total | target-owned | binder-owned |
|---|--:|--:|--:|--:|
| `L49H_E4Q_k15` | 7.332 | **0.686** | 0.655 | 1.000 |
| `quadH_E3Q_k12` | 7.559 | **0.933** | 0.875 | 1.000 |
| `L49H_E4Q_k11` | 7.719 | **0.720** | 0.687 | 1.000 |
| `s3_22k4_k3` | 8.367 | **0.364** | 0.293 | 1.329 |
| `s3_22k4_k6` | 8.610 | **0.496** | 0.367 | 1.364 |

**5 of 48.** The medians are poor — L49H_E4Q 1.354, quadH_E3Q 2.126, s3_22k4 3.502 — so this is a handful-of-48 result, normal for constrained MPNN at temp 0.1 but not a broad success.

## What the binder-owned column shows

Three of the five carry **binder-owned exactly 1.000**: `L49H_E4Q_k15`, `L49H_E4Q_k11` and
`quadH_E3Q_k12`. No binder site contributes to the proton linkage at all, so their whole
direction comes from the target (H73 and Glu146). That is the state arm G reached by DELETING
the glutamates and paying 0.91 of margin for it; here the same state arrives with the hold
rebuilt instead.

`s3_22k4`'s redesigns keep binder-owned at 1.22-1.36 and still reach the lowest totals
(0.345-0.496) because their target-owned is 0.29-0.37. Its direction was never the problem.

## 🔴 s3_22k4 still fails on the hold

It recovered 0.85 against a 1.76 gap, so one round of redesign did not close half the distance.
Its direction remains the best in the project and its binding does not clear the bar.

## Next, and what it costs

5 seeds plus matched nulls plus monomers on the three with binder-owned 1.000, which is H1/H2/H3
properly measured: 3 designs x 5 seeds x 2 + 3 monomers x 5 = **45 folds, ~$2**.

H2 is the bar that can still fail: these are one-seed gate readings, and R1 showed this morning
that a single favourable seed can be noise — `40_L3r2k2` looked right at seed 5 and came back
0 of 4 on unseen seeds. Five seeds is the test.
