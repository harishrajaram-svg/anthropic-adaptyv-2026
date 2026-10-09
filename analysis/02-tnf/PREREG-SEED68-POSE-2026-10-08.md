# Pre-registration — co-fold the 68 chemistry-rejected seed sequences

`as_of: 2026-10-08 23:35 ET` · committed before the folds are launched · **$2.56**

## Why

`comp_filter.py` cut 100 seed sequences to 32 on histidine count and pI. Those cuts were derived
from which designs **bound**, and tonight's stage A shows they carry no information about
**pose** — the 4 of 28 that reached the 10 A gate and the 24 that missed are chemically
indistinguishable (median His 1.0 both, pI 5.00 against 4.81, Pro+Gly 3.61% against 4.82%;
Spearman against ligand RMSD +0.39, −0.26, +0.15 on n = 28).

Pose is what admits a design to the depth loop. So the pool was gated on the wrong quantity, and
the 68 rejected sequences have never been tested on the quantity that matters.

It is also the fix for a failure that already happened: round 1 of stage B collapsed its beam onto
a single backbone because only 4 lineages on 3 backbones existed to begin with.

## What runs

The **68** sequences in `runs/g50mono-in` with `passes = 0` in
`analysis/02-tnf/compfilter_seedpool_2026-10-08.tsv`, built as 1-to-3 complexes against the same
157-residue TNF-α construct used for the 48 and for stage A (the builder refuses if it differs),
one seed (42), no nulls. 68 folds at $0.0377 ≈ **$2.56**, ~70 min including the model load.
Scored by `bin/depth_loop.py --score` against each design's own Genie 3 backbone.

## Statistics and bars, stated before the numbers exist

**Primary: the count of the 68 reaching ligand RMSD ≤ 10.0 A.** Expectation from the filtered
pool is 4/32 = 12.5%, so ~8 or 9.

**The test that decides whether the filter was carrying pose information after all:** Fisher
exact, two-sided, on 4/32 (filter-passers) against k/68 (filter-failers).

- **p > 0.05** ⇒ the filter carried no pose signal, excluding these 68 before co-folding was an
  error, and every design here clearing 10 A is a legitimate additional lineage.
- **p ≤ 0.05 with the failers passing at a lower rate** ⇒ the filter *did* carry pose information,
  the original gating was right, and this file records a $2.56 confirmation of that.
- **p ≤ 0.05 with the failers passing at a HIGHER rate** ⇒ the filter was actively harmful and the
  32-design stage A was the wrong 32. Stated as a possible outcome now so it cannot be explained
  away later.

More than 14 of 68 refused by the target-superposition control makes the verdict REFUSED rather
than a count, in proportion to stage A's tolerance of 6 in 32.

## What it does NOT authorise

**Nothing is added to the running depth loop.** That loop is at round 2 with 4 lineages and has
already been restarted once tonight; interrupting it again on the back of this would be the third
disruption and is not justified by a measurement that can wait until morning.

If this yields extra lineages, widening the loop is a **separate decision with a real trade-off**,
because the 400-fold spend fuse binds: 4 lineages × 8 sequences = 32 folds per round buys 10 rounds,
while 12 lineages × 8 = 96 folds per round buys only 4. The release says depth is where the lift
is (≥4 rounds, 2-3× across generators; 52.9% at 8-12 rounds pooled), so trading rounds for
lineages is not obviously right. That decision is Harish's, with the numbers in front of him.
