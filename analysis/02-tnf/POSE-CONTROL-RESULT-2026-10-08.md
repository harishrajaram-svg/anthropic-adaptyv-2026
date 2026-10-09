# Result — pose control and structural breadth

`as_of: 2026-10-08 20:55 ET`
Bars pre-registered at commit `a4974d3`, before any number in this file existed.
Cost: **$0.** No Modal, no GPU. 4.3 MB of HTTP and local CPU.

## Stage 1 — PASS

Their ESMFold2 pose against **our** ESMFold2 fold of the identical sequence, for all 12
wet-lab-confirmed TNF-alpha binders. CA-only DockQ, symmetry-maximised over the three target
chains, offset 0, target-superposition control in force. **0 of 12 refused.**

| statistic | measured over 12 | pre-registered bar |
|---|---|---|
| median CA sc_DockQ | **0.8663** | — |
| median Fnat | **0.9422** | PASS needs >= 0.10 |
| median ligand RMSD | **1.570 A** | PASS needs <= 10.0 A |
| range LRMS | 0.501 - 3.011 A | |

Verdict: **PASS.** Our single-sequence configuration, with no target MSA on either chain,
reproduces the organisers' MSA-based pose of every one of the 12 measured binders to within
3 A, and to 1.57 A at the median.

### What this settles

Section 6.10f reports, over 40 of our own designs (`analysis/02-tnf/stageA_scdockq_2026-10-08.tsv`):
median CA sc_DockQ 0.0251, median Fnat 0.0000, **median LRMS 31.117 A**, best LRMS 15.034 A,
best Fnat 0.0263. Against the 12 measured binders in the same instrument and the same
configuration: median LRMS 1.570 A, worst 3.011 A.

**The worst measured binder is five times better placed than our single best design, and the
two distributions do not overlap at any point.** The predictor is not incapable of placing a
binder at the correct epitope on this target. 6.10f's 31 A is a verdict on our designs.

### The negative control, and what it is actually worth

Pairing a reference pose with the wrong fold of matched length gives 68 mismatched pairs
(66 scored, 2 refused). Pooled, it clears the pre-registered bar: **AUC 0.8056** on LRMS with
matched lower, permutation p = **0.00065** at 20,000 permutations, against bars of 0.75 and 0.05.

But the pooled number is the wrong read, and the split says why:

| subset | matched median LRMS | mismatched median LRMS | AUC | perm p |
|---|---|---|---|---|
| Genie3 L=83 (n=8 vs 54) | 1.658 A | 1.981 A | 0.6921 | 0.0820 |
| PXDesign L=80 (n=4 vs 12) | 0.807 A | **12.498 A** | 0.9167 | 0.0136 |

The 8 Genie3 binders are one sequence family (pairwise identity 0.58-0.81) and **their own
poses sit 1.837 A from each other** (56 pairs, their structures only, our folds not involved),
so mismatching them does not produce a wrong pose — it produces the same pose on a different
sequence. Their 4 PXDesign poses sit **12.417 A** from each other, so that cell is a real null,
and there the instrument separates cleanly.

So the control's entire discriminating power comes from the PXDesign cell, and the honest
statement of what it establishes is narrower than the pooled AUC suggests: **where a wrong
pose exists, this instrument punishes it with 12.5 A.** The 1.57 A is therefore not an artifact
of parking anything near a large homotrimer. That is the reassurance the control was for, and
it holds — but it is carried by 4 designs, not 12.

### Residual limitation, stated because it bounds the inference

Stage 1 compares a prediction with a prediction of the **same sequence**. Section 6.10f compares
a **designed CA backbone** with a prediction. Those are not the same comparison, and the second
one still has no positive control, because the released dataset contains no
`designed_structure` for any of the 150 designs — only `insilico/predicted_*.cif`. Verified by
listing `data/designs/TNFa/opus_4_8_multi_target_tnfa_rank01/` through the HF datasets API.

What stage 1 licenses: the predictor is exonerated. What it does not license: a calibrated
designed-versus-predicted threshold.

## Stage 2a — the breadth claim must be qualified

Foldseek TM-align, all 48 against all 48, on the binder chain extracted full-atom from each
co-fold in `runs/A-cofold-out/Acofold` (48 extracted, all 83 residues, chain layout asserted).
1,128 off-diagonal pairs. **Median pairwise TM 0.4584**, mean 0.4703, range 0.3161-0.9198.

| TM threshold | single-linkage clusters | complete-linkage clusters |
|---|---|---|
| 0.45 | 1 | 15 |
| **0.50 (pre-registered)** | **3** (sizes 46, 1, 1) | **18** (largest 9) |
| 0.55 | 8 | 24 |
| 0.60 | 15 | 28 |

The pre-registered statistic — single linkage at TM >= 0.5 — gives **3 clusters, with 46 of the
48 in one.** That is below the bar of 10, so `submissions/02-tnf-METHODS.md:1259` and every
"48 families" statement get qualified. The verdict does not depend on the linkage: complete
linkage, the most conservative read available, gives 18, still under the bar of 20.

**The corrected claim: 48 sequence families, 3 structural clusters (18 under complete linkage).**
We bought sequence breadth and almost no structural breadth. Single linkage chains here because
the median pairwise TM, 0.458, sits just under the threshold — the 48 are all roughly one fold
at the edge of the same-fold definition.

## Stage 2a, second read — we never built the winning fold

The same aligner, our 48 against the 12 measured binders' own predicted binder folds:

| compared against | median of per-design best TM | max | ours at TM >= 0.5 | at >= 0.6 |
|---|---|---|---|---|
| the 8-member winning family | 0.4567 | **0.5703** | 10/48 | **0/48** |
| the 4 PXDesign binders | 0.5228 | **0.8247** | 27/48 | 12/48 |

Zero of our 48 reach TM 0.6 against the winning family, and our closest approach is 0.570
(`tnfa_corrected_11_s1`). Against the PXDesign binders we get to 0.825 (`tnfa_corrected_12_s2`).

So our fold space overlaps the family with the **lower** measured hit rate — PXDesign went
4 of 57 — and misses the family that went 8 of 10 in its deep cell. This is the first direct
structural statement of the gap, and it is consistent with the sequence-composition finding
(our designs are Lys-loaded, Asp-depleted, aromatic-poor, Pro+Gly-poor relative to the winners).

## Stage 2b — three record corrections, recomputed from committed artifacts

**1. The CA-versus-all-atom scale excuse is dead, and it inverts.** `METHODS:1209` tabulates
"protocol `pose_PASS` default 0.23 | 0 / 40 pass" and `:1224` excuses it: "no designed
structures, so sc_DockQ cannot be calibrated here against known-good designs." Stage 1 supplies
a calibration point the document says does not exist. A **real binder scores 0.8663 on our
CA-only scale**, so CA-only DockQ is not intrinsically deflated and cannot explain a reading of
0.0251. The 0.23 bar sits between the two by a wide margin. The correction is not "0.23 is not
comparable" — it is that our designs fail it by roughly tenfold, and the scale no longer offers
an excuse. `:1224` must be rewritten rather than deleted: the calibration is against their
*predicted* poses, not against designed structures, and that distinction is the residual
limitation above.

**2. The organisers' own winning arm shipped with no pose number.** In the released co-folding
table, 23 of 150 uuids carry NaN `sc_dockq`: Genie3 11 of 23, RFdiffusion3 8 of 40,
RFdiffusion 4 of 20, PXDesign 0 of 57, BoltzGen 0 of 8, BindCraft 0 of 2. Of the 12 measured
binders, **8 have NaN throughout all of their rows — and those 8 are exactly the winning
family, ranks 01 through 08.** Their own protocol puts `pose_dockq` in `mandatory_nonnull`
and states at `:134` that "the mechanical gate is pose_dockq non-null on every ranked row."
The pose gate we have been treating as the entry condition to their depth loop was **not
recorded for the recipe that produced 8 of their 12 binders.** Stated precisely: this is the
released record; their internal sheet may have held values the release dropped.

**3. `MAX_FORCED_HIS = 8` runs opposite to the measured data, and the error is a conflation.**
`bin/mpnn_constraints.py:61` sets the cap at 8 with the comment "the top of the 8-11 His-cation
contact range in working designs." That 8-11 is a count of histidine-cation **contacts**, not
of histidine **residues**. All 8 winners carry **exactly one histidine, at position 16**; one
carries a second at position 5. Their 150 designs run His {0: 108, 1: 37, 2: 4, 3: 1}, maximum
three. Our 48 run {1: 3, 2: 17, 3: 22, 4: 3, 5: 2, 7: 1} — 28 of 48 at or beyond the top of the
entire measured distribution and 6 strictly beyond it, where this target has no measured
precedent. The constraint builder was free to place up to eight.

## Artifacts

| file | contents |
|---|---|
| `analysis/02-tnf/pose_control_2026-10-08.tsv` | 12 matched + 66 mismatched pairs, DockQ/Fnat/LRMS/iRMS |
| `analysis/02-tnf/genie48_foldseek_tm_2026-10-08.tsv` | 48x48 foldseek TM-align output |
| `analysis/02-tnf/genie48_structural_clusters_2026-10-08.tsv` | cluster assignment at TM >= 0.5 |
| `analysis/02-tnf/genie48_vs_campaign_tm_2026-10-08.tsv` | best TM of each of our 48 to the winning family and to any measured binder |
| `reference/anthropic-campaign/pose-control/` | the 12 downloaded reference poses (gitignored, refetchable) |

## One instrument bug found

`bin/sc_dockq.py` raises `IndexError` at `:171` when the two binder chains have **unequal
length** — `db.index(k)` indexes the longer list against the shorter. Never reached in
production, because designed and predicted always carry the same sequence; reached here only
by an exploratory cross-length pairing that is not part of either pre-registered statistic.
Logged, not fixed, because fixing it changes a submitted instrument on deadline night.

## What this does and does not authorise

Stage 1 PASSED, which under the pre-registration means 6.10f stands as a design failure and
the pose gate is a validated screen. **The pre-registration is explicit that a PASS authorises
nothing by itself**; stage 3 of the costed plan — regeneration under a compositional filter —
remains unapproved and no `modal` command was issued.
