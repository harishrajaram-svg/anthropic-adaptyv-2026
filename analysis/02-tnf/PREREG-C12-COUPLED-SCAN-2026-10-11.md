---
type: preregistration
project: anthropic-adaptyv-2026
problem: 02-tnf-alpha
arm: C12 coupled-ratio scan of the depth-12
status: PRE-REGISTERED — written 2026-10-11 3:50 AM EDT, BEFORE the scan runs
---

# C12 — does any design we already made point the right way?

C10 ran the binding-coupled gate on `3_L0r4k0` and five of its variants only: **30 of 30 poses
inverted**. The other two submitted backbones, **40** and **16**, have different acid layouts and
have never been measured on this quantity. The poses already exist, so this costs **$0** and no GPU.

**Method:** `bin/ph_gate_multisite.py --problem 2` on all **12** depth designs, 5 seeds each = 60
poses, from the committed Oct 9 replication folds (`runs/R-seedrep-H{1,2,3,4}-out`). Free leg by
partner deletion in place; composed over every titratable site on both partners, not the helping
ones; five guards; self-test passing.

**Direction of merit, problem 2:** ratio **< 1** = protonation weakens the complex = release at
pH 6.0, which is what the problem asks. Ratio > 1 = the inverted switch.

| bar | threshold | meaning |
|---|---|---|
| **C12-P1** | median composed ratio **< 1.0** over 5 seeds | the design points the right way |
| **C12-P2** | **≥ 4 of 5** seeds below 1.0 | the direction is consistent across poses, which is the check PK asked for |

**P1 AND P2 would make that design a pH candidate** — measured on the quantity the reviewer
specified, on a molecule that already passed the monomer floor, the liability screen and the
prior-art prescreen. It would then need its margin re-confirmed (already in hand for all 12) and
nothing else.

**If all 12 are inverted**, objective 2 closes with the strongest statement available to this
project: the inversion is a property of the entire design family, measured on the correct quantity
across every molecule we made, not inferred from composition.

🔴 **Declared before reading the output.** This instrument's magnitude is unusable — C11 measured a
pooled SD of **1.499** with three overlapping distributions, and ~123 seeds per arm would be needed
to resolve a 0.5 difference. **Only the sign and its consistency are reportable**, never the ratio.
And the ratio is uncalibrated against the assay, because the released campaign contains no pH
labels at all. A P1+P2 pass is a prediction with a measured direction, not a demonstrated switch.
