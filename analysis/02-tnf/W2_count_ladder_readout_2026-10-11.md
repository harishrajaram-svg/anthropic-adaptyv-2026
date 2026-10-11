---
type: readout
project: anthropic-adaptyv-2026
problem: 02-tnf-alpha
arm: W2 — targeted recreation, count not depth
prereg: analysis/02-tnf/PREREG-W2-COUNT-LADDER-2026-10-11.md (+ amendment 1)
written: 2026-10-11
cost: 70 folds on B200, ~$3.15. All PyRosetta, PROPKA and analysis local and free.
---

# W2 — the count route has a ceiling, it is +4.5 kcal/mol, and the reason is that histidines un-bury each other

**One design beats the project record and the route's own extrapolation table is wrong.**

`W2_H7c` = `3_L0r4k0_quadH` + I78H + I16H + L82H. **Seven** buried histidines. It passes all four
design bars. And the two steps above it on the pre-registered ladder do not merely fail — they
measure *why* the route stops, which is the more useful half of this arm.

## The bars

| bar | threshold | `W2_H7c` | verdict |
|---|---|--:|---|
| **W2-1** | 5-seed monomer pLDDT ≥ 0.70 | **0.8070** (0.8042–0.8089) | **PASS** |
| **W2-2** | Σ fold-destabilisation ≥ +4.50 kcal/mol | **+4.572** | **PASS** |
| **W2-3** | 5-seed human margin ≥ +6.3473 | **+7.037** (SD 0.102) | **PASS** |
| **W2-4** | ≥6 His scored by PROPKA in all 5 seeds | **35 of 35** (7 × 5) | **PASS** |
| **W2-5** | exchange rate r ≤ 3.0 | **undecided — see below** | not a free energy |

Mouse, run because this project selects on worse-of-two: **+7.244** (SD 0.058). Worse-of-two
**+7.037**, against `quadH`'s +7.131. **Three extra buried histidines and +1.508 kcal/mol of Σ cost
0.094 of margin.**

`Σ = +4.572` is **49% above the project record** (`quadH`, +3.064) and it is the largest
pH-responsive energy measured anywhere in this problem. For scale, the gate's best reproducible
interface term is +0.133 kcal/mol, so this is **34x the best the interface has ever offered.**

## The whole ladder, which is the actual result

| step | His | ΔΔG_install vs parent | monomer pLDDT | Σ destab (PROPKA) | human margin |
|---|--:|--:|--:|--:|--:|
| `3_L0r4k0` parent | 0 | 0 | **0.9105** | 0 | +6.967 |
| `3_L0r4k0_quadH` | 4 | +14.580 | 0.8169 | +3.064 | +7.131 |
| `W2_H6` | 6 | +16.830 | 0.7806 | +3.851 | +6.739 |
| **`W2_H7c`** | **7** | **+17.917** | **0.8070** | **+4.572** | **+7.037** |
| `W2_H7` | 7 | +47.089 | **0.6921** | +4.520 | **+4.734** |
| `W2_H8` | 8 | +60.126 | **0.5556** | +4.212 | not run |
| `W2_H9` | 9 | +59.633 | **0.5571** | +4.482 | not run |

**Σ peaks at seven histidines and then falls.** Arm M's extrapolation table said 8 buried His
→ 4 kcal/mol and 11 → 8. Measured: 8 His gives **+4.212**, *less* than 7 gives. **That table is
wrong above about seven, and this arm corrects the most load-bearing number in the fold route.**

## 🔴 Why Σ saturates — measured residue by residue

The per-histidine ceiling (+0.775) is not what stops it. What stops it is that **adding
histidines un-buries the histidines already there**, and the pKa depression is bought entirely
with burial.

| step | mean burial of its His | H64 burial | H64 pKa | H53 burial | H53 pKa |
|---|--:|--:|--:|--:|--:|
| `quadH` | **94.2** | 89 | — | 84 | — |
| `W2_H6` | 83.8 | 89 | 4.33 | 88 | 3.64 |
| `W2_H7c` | 78.1 | 91 | 4.01 | 83 | 3.62 |
| `W2_H7` | 83.1 | 80 | 4.68 | 92 | 3.39 |
| `W2_H8` | 73.4 | **72** | **6.08** | 76 | 5.03 |
| `W2_H9` | 70.6 | **52** | **6.11** | 70 | 5.36 |

His64 goes from burial 89 and pKa 4.01 (seven histidines, folded) to burial 52 and pKa 6.11 (nine
histidines, pLDDT 0.557). At pKa 6.11 it contributes +0.314 instead of +0.769 — it has stopped
being a switch because it has stopped being buried. His16 does the same (68 → 43, pKa 5.59 → 6.12).
**The count lever destroys its own mechanism, and it does so by the same physics that creates it.**

## The matched pair, which is the sharpest thing here

`W2_H7` and `W2_H7c` have **the same count** (7) and **the same Σ to within 0.052** (+4.520 vs
+4.572). They differ by one position: E41H against L82H.

| | `W2_H7` (E41H) | `W2_H7c` (L82H) |
|---|--:|--:|
| ΔΔG_install of that one mutation | **+29.860** | +5.003 |
| monomer pLDDT | 0.6921 | **0.8070** |
| human margin | +4.734 | **+7.037** |

**Count is not the lever. Position is.** And the ordering was called in advance: PyRosetta
`cartesian_ddg` was run and committed *before any W2 fold existed* and said E41H and A60H were
clashes at +29.9 and +40.7 REU while I78H/I16H/L82H were +5 or free. ESMFold2 — an independent
instrument that knows nothing about Rosetta's energy function — then collapsed the ladder at exactly
those two positions and nowhere else. **Spearman(ΔΔG_install, pLDDT) = −0.964 over the seven
molecules.** This is the first PyRosetta in the project (`bin/cart_ddg_fold.py`, selftest 5/5) and
its ordering is the only reason `W2_H7c` exists: the pre-registered rank order, which ranked by
pH-linked destabilisation, put E41H and A60H at ranks 3 and 4 and would have produced nothing.

## 🔴 W2-5: the exchange rate is real as an ordering and NOT a free energy

The bar asked for r = ΔΔG_install per His / 0.775, PASS if r ≤ 3.0. I am not claiming a pass,
because the number fails its own consistency check.

| check | result |
|---|---|
| sign control, per site | 3 of 4 (H63L positive; **diagnosed** — H63/H64 are a cooperative pair, reverting the pair is +0.165 while reverting one member is not) |
| sign control, aggregate | PASS (all four in reverse, **−14.580**) |
| **antisymmetry** ΔΔG(A→B) = −ΔΔG(B→A) | **FAILS by +10.315 REU**: forward from the parent backbone **+24.895**, reverse from `quadH`'s **−14.580** |
| single-site antisymmetry | **worse** — V45H is **−7.199** and H45V is **−7.311**, both negative, so a single-site ddG here is dominated by relief of strain in whichever backbone was not built for that residue |

Antisymmetric estimate for installing the quad: **+19.738 REU over 4 His, +4.934 each, r = 6.37**,
with a range of 4.7–8.0 depending on which backbone you stand on. So: **the route spends roughly
5–8 kcal/mol of pH-independent stability per +0.775 kcal/mol of pH-linked destabilisation it buys.**
That ratio is reportable as an order of magnitude and not as a measurement, and I would not have
known it was unreliable without running both directions — which the prereg's sign control is what
forced.

## 🔴 What this does not establish — the window arithmetic, and it is not encouraging

The route needs **0 < ΔG_fold(7.4) < Σ**. For `W2_H7c` that window is **0 to +4.572 kcal/mol**.
Rosetta says installing its seven histidines already spent +17.9 (from `quadH`'s backbone) to
+28.6 (from the parent's) relative to `3_L0r4k0`. For `W2_H7c` to sit inside its own window,
`3_L0r4k0` would have to be **18–33 kcal/mol** stable. De novo three-helix miniproteins of this size
do not reach the top of that range. So either:

- the install cost is inflated — which the antisymmetry failure says it is — and `W2_H7c` is still
  **far too stable** for +4.572 to unfold it, which is arm M's unresolved problem unchanged; or
- the install cost is roughly right and `W2_H7c` is **already unfolded at pH 7.4**, which ESMFold2
  at pLDDT 0.8070 and a +7.037 margin both contradict.

Both branches say the same thing: **ΔG_fold is still the deciding quantity, it is still unmeasured,
and after this arm I can say why PyRosetta cannot be the instrument that measures it.** Nothing here
demonstrates pH-dependent release. ESMFold2 is pH-agnostic. PROPKA on deeply buried histidines is
its weakest regime, and `W2_H7c`'s H45 at pKa 2.01 is a 4.5-unit depression and the single most
questionable number in this readout.

🔴 The prereg's declared tension held and should be read as declared: `W2_H7c` passing W2-1 at
**0.8070** — barely below the quad's 0.8169 and nowhere near the 0.70 floor — means the ladder did
**not** move ΔG_fold(7.4) toward the window in any way ESMFold2 can see. A high-pLDDT pass is the
weaker outcome and it is what happened.

## Liability, and a note on shipping

| design | pI | q(7.4) | q(6.0) | Δq | identity vs `quadH` |
|---|--:|--:|--:|--:|--:|
| `quadH` | 5.02 | −7.05 | −4.65 | +2.40 | 1.0000 |
| `W2_H7c` | **5.42** | −6.94 | −3.18 | **+3.76** | **0.9639** |

pI is clear of the 6.0–7.4 assay window, and the 28% glutamate flag is inherited from the parent and
carried by designs already shipping. **`W2_H7c` cannot ship alongside `3_L0r4k0_quadH`**: 0.9639
identity is over the organisers' 0.95 `batch_duplicate` threshold. Of the ladder only `W2_H9`
(0.9398) clears it, and `W2_H9` fails W2-1 and W2-2. **So this arm produces no addition to the ship
set — it produces a substitution candidate and a corrected ceiling.** Whether to substitute is
Harish's call, not mine: `W2_H7c` trades 0.094 of worse-of-two margin for +1.508 kcal/mol of a
predicted quantity that no measurement in this project validates.

## Spend

| stage | work | folds |
|---|---|--:|
| W2-5 | PyRosetta `cart_ddg_fold.py`, 16 mutation sets × 2 legs × 3 iterations, local | 0 |
| A | 6 monomers (5 ladder steps + the parent) × 5 seeds | 30 |
| B | 3 human complexes + 3 matched nulls × 5 seeds | 30 |
| C | `W2_H7c` mouse complex + matched null × 5 seeds | 10 |
| | **total, against a 150 cap** | **70** (~$3.15) |

## Artifacts

- `bin/cart_ddg_fold.py` — the new instrument, selftest 5/5
- `analysis/02-tnf/W2_cart_ddg_2026-10-11.txt` — every ddG run, both backbones
- `analysis/02-tnf/W2_sigma_2026-10-11.txt` — per-position pKa and Σ for all five steps
- `runs/W2-mono-in|out`, `runs/W2-cx-in`, `runs/W2-cxA-in|out`, `runs/W2-mouse-in|out`

## The one cheap decisive thing left, and it costs nothing

Make the antisymmetry check pass. `bin/relax_chain.py` already wraps OpenMM + ff14SB, which is what
this project substitutes for FastRelax. Relax **both** the parent and the `quadH` backbones before
measuring, then redo the forward and reverse legs. If the +10.315 REU gap closes to within ~2, r
becomes a number rather than a range, and r × 7 against the published 5–15 kcal/mol stability range
for de novo miniproteins of this size **decides whether `W2_H7c` is inside its window or far above
it** — which is the question arm M opened and this arm has not closed. Zero folds, zero dollars,
local CPU. If it does not close, the honest conclusion is that no instrument in this project can
measure ΔG_fold and the fold route cannot be advanced further by computation alone.
