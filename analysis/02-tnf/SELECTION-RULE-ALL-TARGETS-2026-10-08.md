# The selection rule on all 1,440 designs — most of our findings were TNF-α artifacts

`as_of: 2026-10-08 23:30 ET` · instrument `bin/validate_selection_rule.py` (4 selftests) · **$0**
1,440 designs · 354 measured binders · 16 targets · 113,550 co-fold rows

Every prior number in this project rests on the TNF-α slice: 150 designs, 12 binders, 8 of them
one sequence family. This is the same questions asked of the whole release.

## Two methodological traps, both of which bit before they were fixed

**1. Pooling across targets inflates everything.** Measured hit rate runs from 0% (MBP, Mature
GDF-8) to 80% (TREM2). Any quantity correlated with *which target* scores well without carrying
information about whether a design binds. The selftest makes this concrete: a score encoding
**only target identity** reads pooled AUC **0.663** and within-target **0.500**. So pooling hands
you 0.16 of free signal. Every AUC below is within-target — binder against non-binder of the same
target — with permutations shuffled within target.

**2. Stoichiometry is target-specific, and the first run of this script silently collapsed to
TNF-α because of it.** TNF-α is the *only* target with `1to3`/`3to3`; 11 of 16 are `1to1`, five
have `1to2`, three `2to2`, Cas9 adds `rnp`. Sweeping over (model, stoichiometry) produced cells
that exist for one target, and the run reported 12 positives against 138 negatives — the TNF-α
numbers — while claiming to cover 1,440 designs. Fixed by scoring each target at its own
one-binder-against-the-full-oligomer stoichiometry. **This is recorded because the failure was
invisible in the output except for the positive count.**

## What collapsed

| metric, best of 10 models | TNF-α only | **all 16, within-target** |
|---|---|---|
| `ipsae_max` | 0.963 (rf3) | **0.748** (ptxv2) |
| `pae_interface_min` | 0.957 (af3of3) | **0.737** (rf3) |
| `ipsae_min` | 0.952 (rf3) | **0.734** (of3) |
| `iptm_pae` | 0.947 (rf3) | **0.724** (rf3) |
| `plddt_target` | — | 0.706 (of3) |
| **`plddt_binder`** | **0.000 — anti-correlated** | **0.678 (rf3) — normal, above chance** |
| `sc_dockq` | 0.939 | **0.653** (of3) |
| **`n_interface_contacts`** | **0.954** | **0.633** (of3) |
| `has_clash` | — | 0.522 (afm3) |

**Out of sample it degrades further.** Selecting the best cell on 8 targets and testing on the
other 8: `of3/pae_interface_min` reads 0.800 on its fitting half and **0.674** on the held-out
half; `ptxv2/ipsae_min` reads 0.741 and **0.702**. So the honest out-of-sample performance of the
best *selectable* in-silico metric is **0.67–0.70**, not the 0.95 the TNF-α slice suggested.

**Per-target spread is enormous**, best cell: 15-PGDH 0.97, Latent GDF-8 0.92, TREM2 0.88,
PD-L1 0.86, RBX1 0.81, TNF-α 0.80, Nipah-G 0.80, EGFR 0.78, VEGF-A 0.72, IL-7Rα 0.65, TrkA 0.64,
BHRF1 0.64, Cas9 0.58, **BBF-14 0.39 — below chance.** The ranker is not reliable per target.

### Three claims of ours that do not survive, stated plainly

- **"`plddt_binder` anti-correlates with binding."** TNF-α only. Across 16 targets it reads 0.678,
  the normal direction. The AUC 0.000 was a property of one target's 12 binders.
- **"Interface size is the discriminator."** TNF-α only: 0.954 there, **0.633** across targets.
  Tonight's contact-census instrument was built on this premise and is a weaker instrument than
  its TNF-α validation implied.
- **"The compositional filter enriches 4×."** TNF-α only. Across all 16: 83/286 inside versus
  271/1154 outside, **29.0% against 23.5% — 1.18× enrichment, Fisher p = 0.055.** It is reversed
  on Latent GDF-8 (12.5% vs 25.0%) and TrkA (16.0% vs 24.6%). On TNF-α itself it remains strong
  (32.4% vs 0.9%), so it is a **target-specific signature**, not a general rule, and it was derived
  from TNF-α binders. Legitimate for designing against TNF-α; not evidence of anything else.

## What survives, and it is the strongest result here

**Optimization depth generalizes.** Monotonic across the whole release:

| rounds | designs | binders | rate |
|---|---|---|---|
| 0 | 538 | 87 | 16.2% |
| 1 | 215 | 44 | 20.5% |
| 2–3 | 322 | 86 | 26.7% |
| 4–7 | 280 | 92 | 32.9% |
| **8–12** | 85 | 45 | **52.9%** |

Trend across buckets **r = 0.219, z = 8.29, p = 1.1e-16**.

And it holds **within target**, so target difficulty cannot be driving it. Deep (≥4 rounds) versus
shallow (≤1), paired within each target: **137/365 = 37.5% against 131/753 = 17.4%**, Fisher
**p = 2.1e-12**. Per target, deep beats shallow in **9 of 11** targets with any difference — RBX1
62.1% vs 4.8%, PD-L1 73.0% vs 18.4%, IL-7Rα 73.0% vs 35.3%, Latent GDF-8 100% vs 4.4%, TNF-α
27.8% vs 2.6% — against two where it reverses (Cas9 7.7% vs 12.7%, BBF-14 3.0% vs 5.6%) and two
ties at zero (MBP, Mature GDF-8). Sign test on the 11 non-tied targets, **two-sided p = 0.065**.

So the design-level evidence is overwhelming and the target-level evidence is suggestive: depth
helps on most targets, and on two it did not help at all.

## What this means for what we are doing

**It validates tonight's stage B for the right reason, and invalidates the reason I gave.** The
depth arm is running because depth is the one thing in this dataset that transfers across targets.
It is **not** running because the compositional filter enriches 4× — that figure is TNF-α-specific —
and the 32 candidates it selected should be understood as "selected by a target-specific signature
derived from 12 binders", which is a much weaker warrant than it looked like four hours ago.

**It also deflates the instruments this project has been arguing about for three weeks.** The
choice between `ipsae_min` and `pae_interface_min`, the 0.901 figure, tonight's contact census at
0.889 — all of it is contest between metrics whose honest out-of-sample ceiling is about 0.70. The
gap between the best and the worst *usable* metric is smaller than the gap between TNF-α and the
truth.

## Artifacts

| file | contents |
|---|---|
| `bin/validate_selection_rule.py` | the instrument; `--sweep --rounds --composition --holdout` |
| `reference/anthropic-campaign/all_cofold.tsv` | 113,550 rows, all 16 targets (gitignored, refetchable) |
| `reference/anthropic-campaign/all_designs.tsv` | 1,440 designs with labels and `n_optimization_rounds` |
