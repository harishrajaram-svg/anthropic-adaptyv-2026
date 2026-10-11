---
type: preregistration
project: anthropic-adaptyv-2026
problem: 02-tnf-alpha
arm: C1/C2/C3 confidence triad
status: PRE-REGISTERED — written 2026-10-11 12:50 AM EDT, BEFORE any C1/C2/C3 fold exists
---

# C1/C2/C3 — three runs that can change what ships, or deflate what we are about to claim

## Why these three exist

D1 is answered (`40_L1r4k1` + `3_L4r5k2`). These runs do not look for a better design — three
design arms in a row came back negative and the design search stays closed. They test the three
things the submission is about to assert without having measured them on the molecules it ships.

**One launch each. ~$18 total. No continuation without a new decision.** Bars below are fixed now.

---

## C1 — monomer foldability of the ship set

**The hole.** METHODS limitation 50 reads *"no design in this submission clears the
monomer-foldability floor in the organisers' own protocol… it is the strongest single reason to
expect these designs not to bind."* That 0-of-35 is the **Mosaic** campaign. The depth-12 are not
Mosaic designs: they descend from the Genie3 backbones, whose 100 seed sequences cleared the 0.70
floor **98/100** (min 0.656, median 0.824, max 0.897 — `genie3_probe50_2026-10-08.tsv`). The depth
loop then ran four-plus rounds selected on the **complex** margin with monomer pLDDT nowhere in the
objective. `depth12_human_trimer_5seed` and `pae_interface_all` carry no binder-pLDDT column, so
the floor has never been measured on the 12, and we are about to ship two of them.

**Method.** Binder alone, ESMFold2, the same path that produced `genie3_monomer_floor_2026-10-08.tsv`
and the 98/100 figure (`runs/g50mono-in` convention: one chain, `>protein|<design>`). All 12
canonical sequences from `depth12_canonical_sequences_2026-10-09.tsv`. Seeds 1,2,3,4,5,42 — median
over 1-5 is primary, seed 42 reported separately because the 100 parents were measured at seed 42
only. 12 folds x 6 seeds = 72 folds of an 83-mer, ~3.3 s each.

| bar | threshold | meaning |
|---|---|---|
| **C1-M1** | binder-alone mean pLDDT ≥ **0.70** | the organisers' own default floor, `reference/anthropic-binder-design-protocol.md:100` |
| **C1-M2** | ≥ **0.656** | the worst of the 100 Genie3 parents — "no worse than the pool we came from" |

**Decision rules, fixed now so no swap is post hoc:**
1. Both shipped designs clear M1 ⇒ limitation 50 is **rescoped to the Mosaic set**, and FIELD 2
   states the ship set clears the organisers' pre-filter. This is the outcome that changes the
   submission most.
2. A shipped design fails M1 while a **same-cluster sibling** clears it AND holds a 5-seed margin
   ≥ +6.347 ⇒ **the sibling replaces it.**
3. All 12 fail M1 ⇒ reported as a finding — margin-only optimisation degraded monomer foldability
   relative to the parents it started from — and **the D1 pick stands unchanged.**

**What C1 cannot do.** The 150-assayed comparison in §8.5 used Boltz-2 at 1 binder : 3 protomers.
This is ESMFold2 on the binder alone. The internal comparison (12 children vs 100 parents, same
path) is matched; the comparison to the organisers' 146/150 stays order-of-magnitude placement, as
§8.5 already says of its own numbers.

---

## C2 — does the number in the CSV survive unseen seeds

**The hole.** The leader already changed once between seed draws: seed 42 put `40_L1r4k6` on top at
+7.492, seeds 1-5 put `40_L1r4k1` on top at +8.031, and the Spearman between the two orderings was
**0.538**. The CSV is about to claim +8.031 clears the measured binder median (+7.8144) on the
strength of one 5-seed draw.

**Method.** The 4 shortlist designs — `40_L1r4k1`, `40_L1r4k6`, `3_L4r5k2`, `3_L0r4k0` — and their
4 matched nulls, **copied byte-for-byte** from `runs/R-seedrep-H{1,2,3,4}-in` so the molecules are
provably the ones already scored. Seeds **6-15**, ten seeds never used on these designs. 8 complexes
x 10 seeds = 80 folds, 4 shards. Readout: median margin per design, `bin/pae_interface.py`
`pae_if_mean`, margin = null_median − design_median, seeds collapsed by median before any join.

| bar | threshold | meaning |
|---|---|---|
| **C2-R1** | `40_L1r4k1` median ≥ **+7.8144** | the headline survives on unseen seeds |
| **C2-R2** | `40_L1r4k1` median ≥ **+6.347** | at least the hold survives |
| **C2-R3** | Spearman(seeds 1-5 order, seeds 6-15 order) ≥ **0.6** | the shortlist order is reproducible |

**Decision rules, fixed now:**
1. R1 fails but R2 holds ⇒ nothing in the submission says `40_L1r4k1` clears the binder median. The
   **pooled 15-seed median** becomes the reported number everywhere.
2. R2 fails ⇒ `40_L1r4k1` is not the headline design, and D1 is **reopened** with the pooled numbers.
3. Within backbone 3, the member with the higher **pooled 15-seed** median ships — which settles
   `3_L4r5k2` vs `3_L0r4k0` on 15 seeds instead of 5, and may overturn tonight's D1 answer.

---

## C3 — is the margin reading the designed interface, or the sequence

**The hole, and why it is worth the most.** A3's most informative number was an accident: one
conservative His→Gln at position 61 dropped the margin from +8.031 to +0.916. That says the score
is sensitive to **a** mutation. It does not say the score is localised to the interface — a margin
that collapses on any point mutation anywhere is a fragile artifact, not an interface.

**Method.** Single X→**Ala** substitutions on `40_L1r4k1`, 6 at the interface and 6 distal, matched
by residue identity where a distal counterpart exists. Interface = side-chain tip within 5.0 Å of
target (`his_releasing_positions_40_L1r4k1_2026-10-10.txt`, 12 of 83 residues); distal = tip > 11 Å.
His61 is **excluded** — A3 already measured it.

| slot | interface (d_target Å) | distal control (d_target Å) | matched |
|---|---|---|:-:|
| acid | **E62** (2.30) | **E67** (16.82) | yes |
| polar | **T54** (2.78) | **N17** (12.39) | **no — see below** |
| aromatic | **Y20** (3.34) | **Y35** (16.75) | yes |
| base | **R27** (3.22) | **R71** (20.11) | yes |
| acid | **D50** (3.73) | **D1** (21.68) | yes, but **N-terminal** |
| base | **K53** (4.08) | **K15** (21.41) | yes |

⚠️ **Two mismatches declared in advance.** The binder has exactly two threonines, T54 and T57, and
**both are interface** — no distal threonine exists, so that slot uses N17 (polar, small, uncharged,
mid-chain) and is not type-matched. And the only distal aspartate is **D1**, a terminus, where a
mutation may read as inert for reasons that have nothing to do with location. Both are reported as
such; neither is dropped after the fact.

13 designs (6 interface + 6 distal + **the unmutated parent, folded in-run**) + 13 composition-matched
nulls = 26 complexes, 5 seeds = **130 folds**, 6 shards. The parent is included so the comparison is
within-run rather than against the Oct 9 number. Nulls are a `random.Random(20261006)` shuffle of
each variant's own binder chain, target untouched — the `bin/build_sizematched_null.py` convention,
**verified to reproduce an existing null byte-for-byte before anything is staged.**

| bar | threshold | meaning |
|---|---|---|
| **C3-S1** | mean margin drop across the 6 interface knockouts ≥ **3.0** | the interface carries the signal |
| **C3-S2** | mean margin drop across the 6 distal knockouts ≤ **1.5** | distal positions do not |
| **C3-S3** | one-sided Mann-Whitney on the two sets of 6 drops, **p ≤ 0.05** | the separation is not noise (exact minimum for 6v6 is p = 0.0011) |

**S1 AND S2 AND S3 ⇒ the margin is interface-localised**, which is the strongest statement this
project can make about `40_L1r4k1` and goes in FIELD 2. Any other combination is reported as
measured. **If the distal set collapses as hard as the interface set, the +8.031 is fragile to point
mutation anywhere and that weakens the headline claim** — it gets written up as a limitation, not
buried.

## 🔴 What C3 CANNOT do — declared in advance

C3 measures where **ESMFold2's interface PAE signal** lives on this molecule. It is not a binding
measurement, not an affinity measurement, and has nothing to do with pH. "Interface-localised"
means the predictor's score depends on the residues the design places at the interface — a
statement about our instrument's read of our design, nothing more. No C3 result may be described as
measured binding, measured hot-spot energetics, or experimental validation.

## Known durability hazard (unchanged from A3)

ESMFold2 returns results only at the END of a batch and the local copy is written by the **local**
entrypoint, so a dead shell loses it (`--detach` does not protect). Every fold commits to the
Volume as it lands. Recovery:
`mkdir -p runs/recover && cd runs/recover && modal volume get esmfold2-runs <RUN>`
