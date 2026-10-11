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

---

# AMENDMENT 1 — W2-5 read out, and it reorders the ladder. 2026-10-11, BEFORE any W2 fold exists.

`bin/cart_ddg_fold.py` (selftest 5/5), ref2015_cart, local repack + cartesian minimisation in an
8.0 Å sphere, 3 iterations per leg, on the highest-pLDDT `quadH` monomer (seed 2, pLDDT 0.8177).
No GPU, no spend.

**Sign control, declared in advance with a known answer.** The quad's four histidines run in
reverse must be stabilising. Three of four are: H45V **−7.311**, H53L **−3.668**, H64L **−0.366**;
H63L comes out **+2.899** (+2.686 at 6 iterations, so not iteration noise). The diagnostic explains
it rather than excusing it: **H63L+H64L together is +0.165** — reverting the *pair* is free, while
reverting *one* member is not. His63 and His64 are a cooperative buried pair, which is the exact
motif Ahn/Coventry/Baker's 79x switch is built from. Single-site reversion breaks a pair and is
therefore the wrong unit; the cumulative number is the trustworthy one, and **all four in reverse is
−14.580**. I am treating the aggregate control as passed and the per-site control as passed 3 of 4
with a mechanism, and recording that this is weaker than what the prereg asked for.

**The measured exchange rate, r = ΔΔG_install per His / 0.775:**

| set (on `quadH`) | His | ΔΔG_install | pH-linked gain | r |
|---|--:|--:|--:|--:|
| the quad itself, reverse-measured | 4 | **+14.580** | +3.064 | **4.70** |
| +I78H | 5 | −0.190 | +0.632 | −0.25 |
| +I16H | 5 | +5.164 | +0.607 | +6.66 |
| +L82H | 5 | +5.003 | +0.348 | +6.46 |
| +E41H | 5 | **+29.860** | +0.485 | **+38.5** |
| +A60H | 5 | **+40.651** | +0.387 | **+52.5** |
| +I78H,L82H | 6 | **−2.633** | +0.980 | **−2.69** |
| +I78H,I16H | 6 | +2.250 | +1.239 | **+1.82** |
| +I78H,I16H,L82H | 7 | +3.337 | +1.587 | **+2.10** |
| +I78H,I16H,E41H | 7 | +32.509 | +1.724 | +18.9 |
| +I78H,I16H,E41H,A60H | 8 | +45.546 | +2.111 | +21.6 |
| +I78H,I16H,E41H,A60H,L82H | 9 | +45.053 | +2.459 | +18.3 |

**W2-5 verdict: SPLIT, and the split is the finding.** r ≤ 3.0 holds for the cheap additions
(1.82 at six histidines, 2.10 at seven) and fails by an order of magnitude the moment E41H or A60H
enters (18–22). So the count lever is **not** uniformly self-defeating — but the pre-declared rank
order, which ranks positions by pH-linked destabilisation, is **anti-correlated with
affordability**: E41H and A60H are ranks 3 and 4 by destabilisation and the two most expensive
positions by a factor of six. A60H is Ala→His at burial 111, the tightest position in the core;
E41H buries a histidine where a glutamate was. Rosetta on a fixed predicted backbone overstates
clashes, so +30 to +45 REU is not a free energy — but it is a clash signal at a magnitude no
amount of protocol slack explains away.

**What I am changing, and what I am not.** The four pre-registered ladder steps H6/H7/H8/H9 still
run exactly as declared, because the prereg committed to running their monomer folds whatever
W2-5 said, and because ESMFold2 on H7/H8/H9 is an **independent instrument's verdict on the same
claim** — if Rosetta is right that E41H and A60H are clashes, pLDDT should sag there and not at H6.
I add **one** step, and its selection rule is stated here before its fold exists:

- **W2-H7c** = `quadH` + I78H + I16H + L82H. **Seven** buried histidines. Chosen by maximising
  predicted Σ destabilisation subject to r ≤ 3.0 — i.e. selected on the W2-5 instrument, which is
  a measurement made before this step existed but **after** the prereg was written. It is a
  **post-hoc-ordered** design and is marked as such wherever it is reported.
  Additive Σ prediction **+4.588**, which clears W2-2 (+4.50) by 0.088 — far too thin to call in
  advance, so PROPKA on its own monomer decides it.
- **W2-parent** = `3_L0r4k0` monomer, 5 folds. Not a design. It exists so the install cost can be
  measured **forward from the parent's own backbone** and compared to the −14.580 measured
  backward from `quadH`'s. Agreement would make r a number; disagreement bounds the fixed-backbone
  artifact. Either way it is reported.

Revised spend: 6 monomer inputs × 5 seeds = **30 folds**, then complex + null (10 folds) for each
step clearing W2-1 and W2-2. Cap unchanged at 150.
