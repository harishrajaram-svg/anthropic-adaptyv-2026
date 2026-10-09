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

---

## Addendum, written at 22:45 ET while the stage-A fold was still running, so it is a bound on the premise and not a rationalisation of the result

The filter matches the winners' **summary statistic** by a **different mechanism**, and a two-cut
filter cannot see the difference. pI is a scalar; many compositions map onto the same value.

Median composition (and the submitted 48 for contrast):

| | E% | D% | E+D% | L% | K% | FWY% | P+G% |
|---|---|---|---|---|---|---|---|
| the 8 winners | 16.9 | **6.0** | 22.9 | **19.9** | 10.8 | **4.8** | **8.4** |
| our 32 filtered | **24.1** | 2.4 | 27.1 | 16.3 | 10.2 | 2.4 | 4.8 |
| our 48 submitted | 16.9 | 1.2 | 19.3 | 16.9 | **16.9** | 2.4 | 4.8 |

The winners' glutamate range is **10.8-18.1%**. Ours is **14.5-33.7%**, median 24.1, and **1 of 32**
falls inside their ceiling. They reach pI ~4.7 with moderate glutamate balanced by 6% aspartate
and a 19.9% leucine core. Our 32 reach it by loading glutamate to a quarter of the sequence with
aspartate at 2.4% — a poly-glutamate acid rod rather than a Leu-rich core. Both our pools also
miss the winners on aromatics (2.4% against 4.8%) and on the loop proxy (4.8% against 8.4%).

Note what this says about the 48, which is not what we assumed: their glutamate is **inside** the
winners' range. Their defect is lysine at 16.9% against the winners' 10.8%, which titrates the
acid away and lifts pI to 7.01. Two different failures, one per pool.

**What this bounds.** Stage A asks a **pose** question — does a pre-constraint sequence on these
backbones fold where it was designed to? The pose is set by the backbone and by whether the
sequence encodes it, so the composition critique does not predict the stage-A answer either way.
What it does mean is that a stage-A **GO must not be read as "we found the winners' chemistry."**
We found their histidine count and their pI, by a route they did not take, on a fold that is not
theirs (0 of 48 reach TM 0.6 against the winning family). A GO would license one claim only: that
a pose which survives the gate is reachable on our backbones. The express-QC screen underlines it
independently — 22 of 32 carry a flag, 8 of them cysteine, which the project's Cys-free default
excludes outright, leaving at most 24 of the 32 submissible whatever the pose says.

The honest version of the filter's limitation is that it should have cut on **composition** and not
only on the two scalars. A `D% >= 4` and `E% <= 18` pair would be the obvious addition. It is **not**
being added now: adding cuts after seeing which of our own designs pass, while the fold that tests
them is running, is exactly the post-hoc tuning this project pre-registers against. It goes on the
record as the next filter's pre-registered content, measured against the released labels first.
