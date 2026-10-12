# Workflow, parameters and settings — TNF-α conditional binder (Challenge 2, Track 3)

*Companion to the methodology box and to `02-tnf-METHODS.md`. The live submission form provides a
single methodology field, so this reproducibility detail is attached rather than pasted. Written
2026-10-12; revised at upload, when the submitted set went from six designs to four — see
`02-tnf-METHODS.md` §10.0 for why.*

---

**VERSION 2026-10-11 1:45 AM — this is the text to paste.** Rewritten for the arm that actually
ships (Genie 3 -> SolubleMPNN -> depth loop -> ESMFold2). The previous version described the Mosaic
pipeline throughout and is kept below as superseded. **1,193 words.**

<!-- ===== PASTE FROM HERE ===== -->

**The pipeline that produced the submitted designs is not the one this project started with.** An
earlier gradient-based arm (Mosaic over Boltz-2) produced 35 designs and none of them ships; its
parameters and the reason it failed are in the attached methods document, **§6 and §8**. What follows describes the arm that ships.

**1. Backbone generation — Genie 3.** 50 backbones, `cond_strategy=extended`, binder length 83,
against the sequence-corrected 1TNF trimer carrying **Asp143** at mature 143. A guard
(`bin/build_genie3_problem.py`) refuses the stock BinderBench TNF-α target, which carries Leu143 and
puts that residue inside its own declared interface; the wrapper re-checks Asp143 inside the
container on the bytes being folded. Another entrant reported losing designs to the same mismatch on
2026-10-05. Measured: 50 of 50 backbones span two protomers, median 42 cross-chain contact pairs,
$0.023 per backbone.

**2. Seed sequences — vanilla ProteinMPNN, CA-only, local CPU.** 2 per backbone, 100 total. 98 of
100 clear a 0.70 binder-alone pLDDT floor (median 0.824, min 0.656).

**3. The depth loop — `bin/run_depth_rounds.py`.** This is what moved the numbers, and the loop is
the method. Each round, for each surviving parent:

| step | tool and settings |
|---|---|
| redesign | SolubleMPNN (`protein_mpnn_run.py --use_soluble_model`), `--num_seq_per_target 8`, `--sampling_temp 0.1`, `--seed 37`, `--batch_size 1`, `--omit_AAs CX` — cysteine is removed from the alphabet, not penalised |
| redesign input | the **predicted complex from the previous round**, not the original backbone |
| co-fold | ESMFold2, **1 screening seed (42)** per design per species, human and mouse in parallel |
| select | interface-PAE margin and pose, 6 lineages x 8 children per round |

Design ids encode the lineage: `40_L1r4k1` is backbone 40, lineage 1, round 4, child 1. **All six
submitted designs descend from round 4** — rows 1, 2 and 5 are round-4 children directly, and rows
3, 4 and 6 are hand-built variants of the row-5 parent. No submitted design comes from round 5. (An
earlier version of this sentence said "the two submitted designs come from rounds 4 and 5", written
when two shipped; it is wrong on both counts and the round-4 fact matters, because the
pre-registration failure disclosed in FIELD 2 applies from round 4 onward and therefore covers every
design here.) Pre-registered ceilings governed the spend: the shipping arm's own ceiling was **10
rounds and 240 folds**, with a wall-clock stop; the 16-round, 1,600-fold figures belong to the
constrained-restart arm, which did not ship. The arm that ran after the shipping one stopped
itself at round 10 of 16 on pose regression and **576 permitted folds were not respent.**

**3b. The corrective two-oracle arm, pre-registered and stopped.**
`bin/corr_two_oracle.py` implements the rule the depth loop should have run from round 4: both
ESMFold2 and Chai-1 inside the pose gate, selector `min(CA sc_DockQ)` across the two, parents being
the round-3 checkpoints the original arm actually carried (L0, L1, L2 and the reseeded L4 — L3 had
been retired after three rounds with 0 of 8 children in the gate). It stopped at a pre-registered
**120 s/fold** ceiling: Chai-1 at one diffusion sample, seed 42, A100, 554-residue complex measures
**184.5 s/fold** one-complex-per-container and **157.7 s/fold** batched, because
`chai_lab.chai1.run_inference` loads its model inside every call — so unlike ESMFold2, batching
recovers container start only (~27 s). Anyone reproducing this should budget ~$0.09/fold for the
second oracle and not expect ESMFold2's batching economics to carry over.

**4. Folding and scoring — ESMFold2 at the protocol's final tier.** `bin/score-esmfold2.sh`, which
calls `modal_esmfold2.py` with `--num-loops 10 --num-sampling-steps 68 --num-diffusion-samples 1`.
The wrapper defaults (3 loops, 50 steps) are weaker than the published protocol and are not used.
Seeds **1-5** for every reported number, collapsed by **median** per design before any join;
seed-max flatters and is not used. Targets: human **3 x 157** residues
(`targets/validation-tnf/pos_tnf_tnfr2.faa`, chains A/B/C, binder as chain D), mouse **3 x 156**.
The mouse **trimer** is the construct for every reported mouse number — an earlier mouse **dimer**
inflated margins a median +16%, was 6.8x noisier, and produced one false reading; it was retired.
GPU: H100, measured 27.0 s per 554-residue fold.

**5. The ranker and the null — the one number everything rests on.** `bin/pae_interface.py`,
statistic `pae_if_mean`, fail-closed: it returns a score only when the chain labelling read off the
**output** structure accounts for every row of the PAE matrix, because chain labels change through
folding wrappers. Lower is better, so every reported quantity is a **margin**:

```
margin = median(null folds) - median(design folds)
```

The null is a **composition-matched shuffle of that design's own binder chain**, same length, same
residue counts, target chains untouched, generated by `random.Random(20261006)` — the seed is fixed
in `bin/build_sizematched_null.py` and every arm reproduces an existing null byte-for-byte before it
stages a new one. Two calibration constants come from the released campaign's own labels and are
used as reference lines, not as filters: **+6.3473** the non-binder median and **+7.8144** the binder
median.

**6. Confirmation runs on the submitted set**, each pre-registered with its bars before any of its
folds existed:

| run | what it does | settings |
|---|---|---|
| monomer floor | binder alone, the organisers' 0.70 default | ESMFold2, seeds 1-5 + 42, same path as the 100-parent measurement |
| seed replication | the shortlist re-scored on **seeds 6-15**, inputs copied byte-for-byte | 10 unseen seeds; the reported margin is the pooled 15-seed median |
| interface scan | 6 interface vs 6 distal single alanines, parent folded **in-run** | interface = side-chain tip within 5.0 Å of target; distal > 11 Å; exact one-sided Mann-Whitney on the two sets of 6 |

**6b. The submitted variant `3_L0r4k0_L49H`, and how it was made.** One substitution, Leu49→His, on
a design already in this submission. Position 49 came from a deterministic scan of that design's own
predicted complex for sites that are **buried** (≥45 binder heavy atoms within 8 Å of the side-chain
tip), **non-interface** (>11 Å from the target) and carry **no polar partner** within 4 Å: 28 of 83
positions qualify and eight were tested. Screening ran cheapest-first — binder-alone pLDDT on all
eight (45 folds, every one clearing the 0.70 floor), then the human trimer on the best three (30
folds), then the mouse trimer and ten unseen seeds on the one that led. **Nothing was redesigned
around the substitution and no optimisation was run against the mechanism**: the position was chosen
by geometry and the margin was measured afterwards. Burial was re-verified in the complex pose
rather than assumed from the template, in all five seeds. **Row 5** is the same molecule without the
substitution.

**7. Numbering.** Five schemes are live in this work and they do not agree. Our positional numbering
runs **+5** against the assay construct. Every mapped position was confirmed by residue identity
rather than arithmetic, and mouse indices are not the human ones — a deletion shifts the register.
The 157-residue human and 156-residue mouse constructs align at 79.5% identity, and that alignment
is what any cross-species residue claim here rests on.

**8. On "prompts".** No language model is in the generation path and no prompt produced a sequence.
Genie 3 is a diffusion model, ProteinMPNN an inverse-folding network, and the selection is a
threshold on a measured margin. Claude (Claude Code) wrote the wrappers, the instruments, the
analysis and the stopping rules, and acted as the engineer throughout; its decisions are recorded as
commits rather than as prompts. Conflating "prompt" with "parameter" would misdescribe the method.

**9. Reproducibility and the discipline that produced the negatives.** Every instrument carries a
`--selftest` that runs with no GPU, no account and no network, and the launchers refuse to start if
it fails. Self-tests include mutation tests asserting the *discarded* implementation fails, so a
test cannot pass if the fix it guards is reverted. Each arm was **pre-registered in version control
with its bars and its stopping rule before its first fold existed**, which is why the four negative
arms in this work are reportable rather than retrospective. Dependencies are pinned by commit —
Mosaic was installed from an unrevisioned git URL until 2026-10-07, which we found ourselves,
measured (the only upstream commits in our window changed a citation file and a README, +21/−0, no
Python), and guarded. Design ids were de-duplicated against a canonical sequence table after an
aborted run left a parallel output tree; sequence-derived screens are run from that table and never
from a directory glob. Pose caches run to tens of gigabytes, are gitignored, and are available on
request.

<!-- ===== PASTE TO HERE ===== -->

---
