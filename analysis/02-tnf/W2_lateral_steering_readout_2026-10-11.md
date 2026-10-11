---
type: readout
project: anthropic-adaptyv-2026
problem: 02-tnf-alpha
arm: W2 lateral charge steering
prereg: analysis/02-tnf/PREREG-W2-LATERAL-STEERING-2026-10-11.md
written: 2026-10-11
verdict: DEAD on magnitude, by the bar fixed before measuring
gpu_spend: 0 folds, $0
---

# W2 — lateral electrostatic steering is real, points the right way on one design, and is 6x too small

## What was measured

Screened-Coulomb (Debye-Hückel) interaction energy between the binder's interface charges and
the target's contact-patch charges, at pH 7.4 and pH 6.0, Henderson-Hasselbalch occupancies on
model pKa. ε_r = 78.5, κ⁻¹ = 7.8 Å (150 mM, 310 K). `bin/lateral_steer.py`, 7 selftest pins
including two mutation tests on the sign convention and one on exact bilinearity.

**No PROPKA call, no bound/free leg, no linkage ratio appears anywhere in the instrument.**
Nothing here is selected on the gate that failed R1 calibration.

    ddG_steer = U(6.0) - U(7.4);   POSITIVE = less favourable at pH 6.0 = RELEASE.

35 complexes, all six shipped designs, human leg, 5-10 seeds each. 11 s of CPU.

## The result: every contact patch on human TNF-α is net NEGATIVE

| design | n seeds | qT 7.4 | qT 6.0 | qB 7.4 | ddG_steer | direction |
|---|---|---|---|---|---|---|
| 40_L1r4k6 | 5 | −0.98 … −2.16 | −0.16 … −1.16 | −1.89 … −3.89 | **−0.41 … −0.49** | tighten |
| 40_L1r4k1 | 5 | −1.07 … −2.07 | −0.16 … −1.15 | −0.89 … −1.89 | **−0.33 … −0.42** | tighten |
| 3_L0r4k0 | 5 | −0.87 … −1.16 | +0.60 … −0.17 | −2.00 … −3.00 | **−0.22 … −0.27** | tighten |
| 3_L0r4k0_L49H | 10 | −1.07 … −1.16 | −0.16 … −0.17 | −2.00 … −4.00 | **−0.21 … −0.27** | tighten |
| 3_L0r4k0_quadH | 5 | −0.87 … −1.16 | +0.60 … −0.17 | −2.00 … −3.00 | **−0.19 … −0.23** | tighten |
| **quadH_E3Q_k12** | 5 | −1.16 … −2.07 | −0.15 … −1.14 | **+2.00 … +4.00** | **+0.17 … +0.25** | **release** |

Every epitope these designs found is an **electronegative** patch that *loses* negative charge
on acidification. Five of the six binders carry a **negative** interface, so acidification pulls
them **in** — the wrong direction, reproducibly, across every seed.

`quadH_E3Q_k12` is the single exception and the only one whose sign is right. The reason is
exactly the route pre-registered as the one that sidesteps closed items 1 and 2: its interface
is net **positive** (+2 to +4 e), it has **zero** interface histidines, and the entire pH
dependence is supplied by the **target's** titration. It needs no binder histidine at all.
Arm E's electropositive-seam observation has a mirror image here — the shipped epitopes are
electronegative, which is why the His73 seam and these designs are opposite problems.

Mouse leg, same design, same sign: **+0.044** (14 Å) to **+0.105** (25 Å). Worse-of-two,
which is how this objective selects, is therefore **+0.044 kcal/mol = 1.08x in K_D.**

## Robustness

ddG_steer for `quadH_E3Q_k12` is **+0.237 / +0.217 / +0.230** at patch radii 14 / 20 / 25 Å.
The Debye screening kills everything past ~20 Å, so the number does not depend on where the
patch boundary is drawn. The independent recompute of the three-mutation variant agrees with the
per-position prediction to **0.0003 kcal/mol**, so the ≤3-mutation search is exact, not greedy.

## Against the pre-declared bars

- **W2-2 (sign), PASS.** 1 of 6 designs, 5 of 35 poses, ddG_steer > 0.
- **W2-1 (materiality), FAIL.** Bar +1.419 kcal/mol (10x K_D at 310.15 K). Best as built
  **+0.237** (human) = **1.5x**; **+0.044** on the selecting mouse leg = **1.08x**.
- **W2-3 (achievability), FAIL.** Best pose-sparing rim triple (min-dist ≥ 4.5 Å, dU(7.4) ≤ 0.25):
  E10H + I25R + L12H, **+0.258**, total **+0.495 = 2.3x**. Short of the bar by **2.9x**.
- **W2-4 (honesty), triggers.** 2.9x > 2x, so by the rule fixed before measuring, **the arm is dead.**

Unlimited rim mutations — mutating all ~21 shell positions to their best charged identity, which
is a wholesale interface rebuild and is exactly what closed item 3 showed cannot hold a pose at
all (0 of 224 reached DockQ 0.60) — reaches **+1.11 (6.6x)** for `quadH_E3Q_k12` and **+1.42
(10.0x)** for `3_L0r4k0_quadH`. The histidine-free version of that same 20-mutation rebuild
reaches only **+0.89 (4.3x)** and **+1.00 (5.1x)**.

## Why it cannot be rescued — the ceiling, stated as physics

Between pH 7.4 and 6.0 the only group that titrates appreciably is histidine: Δq = **+0.648 e**
(Glu moves +0.019, Asp +0.008). The binder cannot supply that swing — closed items 1 and 2 are
that interface histidines collapse the pose and post-hoc histidines lose the hold. So the swing
must come from the **target**, which cannot be mutated. The human contact patches of all six
designs contain **1 or 2 histidines**, giving Δq_target = **+0.65 to +1.47 e** total.

One unit of binder charge facing +1 e of target swing at 6–10 Å, through bulk water at 150 mM,
is worth **0.08–0.15 kcal/mol**. Reaching 1.42 kcal/mol therefore needs **10–18 effective charge
units** on the binder face, at close range, all pointing the same way — an interface made almost
entirely of lysine, which is not a binder. **The ceiling is set by one histidine on the target
side, and no amount of binder engineering raises it.**

The one parameter that would change the verdict is the dielectric: at ε_r = 20 the best triple
reaches **+1.79 (18x)** and two mutations suffice. That is not defensible here. The rim positions
were selected to be *out of heavy-atom contact* (≥ 4.5 Å) precisely so the mutations would be
pose-sparing, which means those charges are **solvent-exposed and fully hydrated** — bulk water
is the right ε. Claiming ε_r = 20 for a hydrated rim charge would also incur a desolvation
penalty larger than the Coulomb gain it buys. At κ⁻¹ = 12 Å (≈65 mM, a lower-salt buffer than
the McIlvaine's used in the published 79x SPR) the best triple still only reaches +0.81 = 3.7x.

## What is worth keeping

One free, defensible, gate-independent sentence for the methods write-up: **of the six shipped
designs, `quadH_E3Q_k12` is the only one whose long-range interfacial electrostatics shift in
the release direction on acidification, and it does so on both species legs and in all five
seeds** (+0.237 human, +0.044 mouse). The effect is 1.1–1.5x, far too small to be the switch,
but it is a real, reproducible, independently-computed property that distinguishes one shipped
molecule from the other five — and it is the only pH-direction claim in this project that does
not route through the failed gate.

It also says which design NOT to defend on this axis: `40_L1r4k6` and `40_L1r4k1` are steered
*toward* the target at pH 6.0 by −0.33 to −0.49 kcal/mol, a 1.5–2.3x headwind against whatever
the fold route delivers.

## Spend
**0 GPU folds, $0.** Nothing was folded, because the result is an analytic bound: the ceiling
follows from one histidine's 0.648 e at a measured distance, and a fold cannot move it.
