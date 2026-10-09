# Our own constraint pushed every design out of the band where every measured binder lives

`as_of: 2026-10-08 21:50 ET` · instrument `bin/comp_filter.py` (6 selftests) · **$0**

## The filter, and it is two cuts rather than three

All 12 wet-lab-confirmed TNF-alpha binders in the released campaign sit in a narrow chemical band.
Eleven of twelve carry **one or two histidines** — the eight winners carry exactly one, at position
16, inside a conserved `ELH(E/Q)LL` motif — and every one has **pI between 4.53 and 5.26**.

| | admits | |
|---|---|---|
| 12 measured binders | **11** | |
| 138 measured non-binders | **23** | |
| precision inside the filter | **32.4%** | against an 8.0% base rate |
| enrichment | **4.04×** | Fisher two-sided **p = 1.96e-07** |

A net-charge cut was in the first version and the selftest killed it. Removing `netq <= -3` admits
**not one** extra non-binder across the 150, because `pI <= 5.5` already implies it. It would have
read in the write-up as a third independent line of evidence while doing nothing. Net charge is
still computed and reported; it does not gate. `T5b` now asserts that inertness, so if it ever
stops being inert the tool says so instead of quietly carrying a decorative term.

**Provenance is disclosed.** These cuts were chosen after seeing which designs bound, and about
eleven features were examined against the same 12 binders, of which 11 live in 3 sequence
families. The effective sample is roughly **3 independent successes, not 34 designs**. This ships
as a filter with a stated post-hoc provenance, never as "put a histidine at position 16."

## Applied to our own pools, which are the same 50 backbones

| pool | n | median His | median net charge | median pI | passes |
|---|---|---|---|---|---|
| seed sequences, `runs/g50mono-in` | 100 | **0** | −8 | **4.73** | **32** |
| submitted-arm sequences, the Genie 48 | 48 | **3** | 0 | **7.01** | **2** |

Those are not two different design sets. They are the same 50 Genie 3 backbones before and after
one step. The step is the SolubleMPNN pass that applies `bin/mpnn_constraints.py`, whose
`MAX_FORCED_HIS = 8` forces histidines in to build the pH switch objective 2 asks for.

**So our own pH-switch constraint moved the pool from inside the measured binder band to outside
it.** Histidines 0 → 3, pI 4.73 → 7.01 — and the binders' entire range is 4.53 to 5.26, so the
median of our 48 sits above every measured design on this target. 28 of 48 carry more histidines
than any of the 150, and 6 carry more than three, where there is no measured precedent at all.

And the constraint did not buy the switch it cost us. The pH gate run earlier the same day found
**63% of moving sites point the wrong way**, the median design binding 2.8× *tighter* at pH 6.0,
and 76% of movers with no counter-charge within 6 A — desolvation, not mechanism. We paid the full
chemistry price and got an inverted switch.

The two surviving designs of the 48 are `tnfa_corrected_45_s2` (His 1, pI 5.39) and
`tnfa_corrected_5_s1` (His 2, pI 4.61).

## Why this matters more than it looks

The reopen was costed on the assumption that new backbones had to be generated: 120 Genie 3
samples at $2.76, plus monomer folds, before any candidate existed. **32 candidates already exist
on disk**, from backbones already generated, already past the 0.70 monomer floor (98 of 100
cleared it, median pLDDT 0.824). What has never been done is co-folding them **as complexes** —
only the 48 post-constraint sequences were.

That is 32 folds, **$1.19**, about 31 minutes in one container.

## The honest tension, which is not an error

Objectives 1 and 2 pull against each other here. Every measured binder on this target is acidic
with one histidine. A pH switch between 7.4 and 6.0 needs titratable histidines at the interface.
Nothing in the released data tells us whether the 12 binders switch — nobody measured pH on them.
So "match the binder chemistry" and "build a switch" are in genuine conflict, and this file does
not resolve it. What it establishes is narrower: the way we resolved it — up to eight forced
histidines — put us outside the only measured envelope we have, and the switch did not arrive.

## Artifacts

| file | contents |
|---|---|
| `bin/comp_filter.py` | the filter, 6 selftests, `--validate` refuses below 2× enrichment |
| `analysis/02-tnf/compfilter_seedpool_2026-10-08.tsv` | all 100 seed sequences with features and verdict |
| `analysis/02-tnf/compfilter_genie48_2026-10-08.tsv` | all 48 submitted-arm sequences, same columns |
