---
type: preregistration
project: anthropic-adaptyv-2026
problem: 02-tnf-alpha
arm: W2 — targeted recreation, count not depth
parent: analysis/02-tnf/PREREG-ROUTES-123-2026-10-11.md (arm M), M_quad_readout_2026-10-11.md
status: PRE-REGISTERED — written 2026-10-11, BEFORE any W2 measurement exists
---

# W2 — the count ladder, and the window the route has to land in

## Where this starts

`3_L0r4k0_quadH`. Four buried histidines, PROPKA monomer pKa 2.43–4.55, summed pH-linked
fold-destabilisation **+3.064 kcal/mol**, monomer pLDDT 0.8169, human margin **+7.1306**, mouse
+7.185. Arm M measured that **per-histidine destabilisation saturates at +0.775 kcal/mol** because
the unfolded reference (His intrinsic pKa 6.5) fixes the numerator:

    destab(pKa_f) = RT·[ ln((1+10^(6.5−6.0))/(1+10^(pKa_f−6.0)))
                       − ln((1+10^(6.5−7.4))/(1+10^(pKa_f−7.4))) ],  RT = 0.5927
    destab(−∞) = +0.7749   ← the ceiling, per histidine

Depth is exhausted at 97–100% of that ceiling on all four quad sites. **The only lever left is
count.** This arm pulls it.

Nothing here touches the binding-coupled protonation gate. That gate failed external calibration
(R1: 10/18 on direction, p = 0.1288, ratio > 1 for 14 of 18) and no W2 selection reads it.

## The physics, stated so it can be wrong

The route wants the binder **folded at pH 7.4 and unfolded at pH 6.0**. That is a two-sided
window, not a one-sided maximisation:

    0 < ΔG_fold(7.4) < Σ destab

If ΔG_fold(7.4) is 8–10 kcal/mol — ordinary for a designed miniprotein — then Σ = 3.064 does
nothing, which is exactly what arm M's readout said it could not rule out. **Σ rising is only half
the job. ΔG_fold(7.4) must come down to meet it.**

Installing a histidine in a hydrophobic core does both: it adds +0.775 of pH-linked
destabilisation *and* it spends pH-independent stability (polar imidazole for Leu/Ile/Val). In this
mechanism that second cost is **an asset, not a tax** — it is the only thing in reach that lowers
ΔG_fold(7.4) toward the window. The quantity nobody in this project has measured is how much
stability each installed histidine actually spends. Call it the **exchange rate**:

    r = ΔΔG_install per histidine (pH-independent, neutral His)  /  0.775

- r ≈ 1: count scales the switch and the fold together; the window is hit by luck.
- r >> 1: a handful of histidines strips the whole scaffold; the molecule is dead at **both** pH
  values, which is a broken protein, not a switch, and the route is bounded by r.
- r << 1: Σ can be driven up almost for free, and the route is limited only by how many buried
  positions exist.

**PyRosetta `cartesian_ddg` measures r, it is free and local, and it has never been run in this
project.** It runs first, before any GPU spend, because it is the cheap decisive step.

## Selection rule — fixed here, before any W2 number exists

Positions come from `analysis/02-tnf/C9e_pka_scan_2026-10-11.tsv` (already measured, 100 folds,
5 seeds, 20 positions of this exact scaffold). Three filters, in this order, no cherry-picking:

1. **Non-interface.** Side-chain minimum heavy-atom distance to target chains A/B/C ≥ 8.0 Å in the
   `quadH` complex (median of 5 seeds). Closed item 1 is that forcing histidine at *interface*
   positions collapses the pose (0.6349 → 0.0126); this arm stays out of the interface by
   construction, which is also exactly how Ahn/Coventry/Baker's published 79x switch is built.
   Measured: the `quadH` interface is residues 7–31 (≤5.0 Å) and 3–35 plus 83 (≤8.0 Å). Every
   candidate below sits 9.5–21.2 Å out.
2. **Positive single-site destabilisation ≥ +0.30 kcal/mol**, from the C9e pKa by the formula
   above. This excludes the shallow sites outright, and it excludes the **six positions with
   single-site pKa above the 6.5 unfolded reference** (50, 65, 36, 76, 38, 47) because their
   contribution is *negative* — acidification would stabilise them. That sign trap is the reason
   the rule is written down before the ladder is built.
3. **Strict rank order** of that destabilisation. No subsetting on outcome.

The resulting pool, after the quad's own 45/53/63/64:

| rank | mut | pKa (single) | destab | burial | d to target |
|--:|---|--:|--:|--:|--:|
| 1 | I78H | 5.46 | +0.632 | 83 | 16.97 Å |
| 2 | I16H | 5.54 | +0.607 | 82 | 9.53 Å |
| 3 | E41H | 5.83 | +0.485 | 76 | 13.27 Å |
| 4 | A60H | 6.00 | +0.387 | 111 | 21.23 Å |
| 5 | L82H | 6.06 | +0.348 | 62 | 12.57 Å |

E41H deletes a **buried** glutamate 13.3 Å from the target and is not one of the three
gate-attributed glutamates (7, 20, 28) that closed item 9 covers.

The ladder is therefore forced, not chosen:

| name | mutations on top of `quadH` | buried His | Σ destab if additivity holds |
|---|---|--:|--:|
| **W2-H6** | +I78H +I16H | 6 | +4.30 |
| **W2-H7** | +I78H +I16H +E41H | 7 | +4.78 |
| **W2-H8** | +I78H +I16H +E41H +A60H | 8 | +5.17 |
| **W2-H9** | +I78H +I16H +E41H +A60H +L82H | 9 | +5.52 |

Those Σ figures are the additive *prediction* from single-site pKa. The quad's own additivity came
in at **102.1%** (depressions deepened on combination), so PROPKA on each ladder monomer is the
measurement and these numbers are the thing being tested, not the result.

## Bars — fixed now

| bar | threshold | why this number |
|---|---|---|
| **W2-1** | 5-seed monomer pLDDT median **≥ 0.70** | arm M's M1, unchanged, so the ladder is comparable to the quad's 0.8169 |
| **W2-2** | best ladder step's PROPKA-measured Σ destab **≥ +4.50 kcal/mol** | strictly beats the project record (+3.064) and clears arm M's "6 buried His → 4 kcal/mol" line with margin |
| **W2-3** | that step's 5-seed human complex margin **≥ +6.3473** | the project's standing hold bar, identical to M3 |
| **W2-4** | **≥ 6** histidines scored by PROPKA in **all 5** monomer seeds | the count actually got installed and is resolvable, not just present in the sequence |
| **W2-5** | PyRosetta `cartesian_ddg` **r reported, with a verdict**: PASS if r ≤ 3.0, so the ladder can plausibly land inside the window rather than demolishing the scaffold | this is the arm's own physics; r is a measurement I have not made and the bar is set before I make it |

**W2-5 runs first and it is free.** If r > 3.0 I will say the count lever is self-defeating and
report the number as the arm's result, and I will still run the ladder's monomer folds — because an
r that large is a prediction about ΔG_fold and ESMFold2's pLDDT on the ladder is the cheapest
independent check on whether the scaffold really is being stripped.

## 🔴 What a full pass would and would not be

A W2-1 through W2-5 pass is **a design with more predicted pH-linked fold destabilisation than
anything in this project, that still folds and still binds.** It is **not a switch.** ESMFold2 is
pH-agnostic and cannot show unfolding; PROPKA on deeply buried histidines is its weakest regime;
and the absolute ΔG_fold(7.4) that decides whether Σ matters is still unmeasured — Rosetta gives
only the *difference* r, not the parent's absolute stability. **No outcome of this arm demonstrates
pH-dependent release.** The honest ceiling is a better-instrumented prediction.

🔴 Declared tension, inherited from arm M: W2-1 passing at *high* pLDDT is not unambiguously good
news. A ladder that stays at 0.88 has not moved ΔG_fold(7.4) toward the window. The outcome this
route actually wants is pLDDT sagging toward the 0.70 floor while Σ rises and the margin holds —
and I am recording that here so that a high-pLDDT pass is not reported later as a cleaner win than
it is.

## Spend

| stage | work | folds | cost |
|---|---|--:|--:|
| W2-5 | PyRosetta cartesian_ddg, local CPU | 0 | **$0** |
| A | 4 ladder monomers × 5 seeds | 20 | ~$0.90 |
| B | complex + size-matched null for the steps that clear A, 10 folds each | ≤40 | ≤$1.80 |
| | **cap** | **150** | **$7** |
