---
type: prereg
project: anthropic-adaptyv-2026
problem: 02-tnf-alpha
arm: T — the fold route's deciding quantity, dG_unfold of the binder monomer
written: 2026-10-11, BEFORE any Rosetta run in this arm
parent: analysis/02-tnf/M_quad_readout_2026-10-11.md
prior-art: analysis/02-tnf/R8_prior_art_ahn2025_2026-10-11.md
---

# Pre-register arm T — measure dG_unfold, the number arm M said nobody has

Arm M left the fold route resting on **+3.064 kcal/mol of protonation-linked fold
destabilisation against an unknown dG_unfold**, and said in its own readout that nothing on
hand measures the denominator. This arm attacks the denominator.

Nothing in this arm touches the binding-coupled protonation gate that failed external
calibration in R1. The quantity here is monomer folding stability, a different quantity
measured by a different instrument.

## T0 — the requirement, derived before any measurement

Two-state linkage, only the folded binder binds:

    K_unf    = exp(-dG_unfold/RT)
    KD_app   = KD_folded * (1 + K_unf)
    switch   = KD_app(6.0)/KD_app(7.4) = (1 + K_unf*exp(DD/RT)) / (1 + K_unf)

with RT = 0.5924 kcal/mol at 25 C and DD = +3.064 kcal/mol (arm M's measured sum).
Computed in `scratch/linkage.py`, run before the bars below were written:

| dG_unfold(7.4) | switch at DD=+3.064 |
|--:|--:|
| 10.0 | 1.00x |
| 6.0 | 1.01x |
| 4.0 | 1.20x |
| 3.0 | 2.10x |
| 2.0 | 6.79x |
| 1.0 | 28.4x |

Inverted: **2x requires dG_unfold <= 3.06, 10x requires <= 1.73, and the published 79x would
require <= 0.13 kcal/mol** — a protein 44% unfolded at pH 7.4. A corollary the arithmetic
hands over for free: to a first approximation **DD must roughly equal dG_unfold** to buy 2x,
so at arm M's measured +0.775 kcal/mol per buried histidine a 6 kcal/mol scaffold needs
**~8 buried histidines** and a 10 kcal/mol scaffold needs **~13**.

## Bars, fixed now

**T1 — the verdict bar, on dG_unfold of `3_L0r4k0_quadH`:**

| band | verdict |
|---|---|
| dG_unfold <= 3.06 kcal/mol | **ALIVE** — +3.064 buys >= 2x, matching the only published 7.4/6.0 datapoint |
| 3.06 < dG_unfold <= 6.00 | **NEEDS COUNT** — the four histidines are not enough; 6-8 buried His is the ask |
| dG_unfold > 6.00 kcal/mol | **COSMETIC** — +3.064 produces < 1.01x and the quad as built is not a switch |

**T2 — the instrument bar. Any instrument used for T1 must first pass both controls or its
output is reported as uncalibrated and the T1 verdict is marked untrustworthy:**

- negative control: a solvent-exposed conservative substitution must score |ddG| <= 1.0 kcal/mol
- positive control: a buried hydrophobic -> Ala truncation must score ddG >= +1.5 kcal/mol
  (destabilising), the sign and rough size the experimental literature on core cavities gives

**T3 — self-consistency.** The parent -> quad ddG computed forward on the parent's structure and
backward on the quad's own structure must agree to within 2.0 kcal/mol. If they do not, the
instrument is reported as non-reproducible on this scaffold.

## Instruments to be tried, in order

1. **PyRosetta cartesian ddG** (`ref2015_cart`, installed: PyRosetta-4 2026.39). Gives **ddG, not
   dG.** It can therefore answer "how much stability did installing four buried histidines already
   cost at neutral pH" but **cannot by itself answer T1**, which needs an absolute.
2. **Rosetta pH mode** (`-pH_mode -value_pH`), never run in this project (item D). An independent
   check on arm M's +3.064, from a different instrument than PROPKA.
3. If neither yields an absolute dG_unfold, **say so plainly** and name the cheapest experimental
   proxy instead. Declared in advance: that is the acceptable outcome, not a failure to report.

## Structures, fixed now

- parent: `runs/C1-mono-out/C1mono/tnfa_corrected_3_L0r4k0/..._seed1_sample_12.cif` (pLDDT 0.9104)
- quad: `biomodals/runs/M-quad-out/Mquad/tnfa_corrected_3_L0r4k0_quadH_mono/..._seed1_sample_10.cif` (pLDDT 0.8169)
- `L49H` has no monomer fold of its own; its ddG is computed on the parent structure by mutation,
  which is what the cartesian ddG protocol does in any case.

Positions in the 83-mer parent
`SMEEVKELLELLKLMIKRKEPIELILSEFEKLLEETKTEEEKELVIDFLIEELGLSRKEAEELLSLPKEERKKRLSEILEKLR`:
V45, L49, L53, L63, L64.

## Spend

CPU only. 0 GPU folds budgeted. Cap for this arm is 150 folds; if it closes at 0, that is reported.
