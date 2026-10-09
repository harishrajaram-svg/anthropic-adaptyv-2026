# Stage A result — GO, and the win is entirely in the tail

`as_of: 2026-10-08 22:25 ET` · bars pre-registered at `5002b49`, before any fold ran
32 folds, seed 42, ~$1.20. App `ap-Z2pWEVRGbNR2wFNbIKfwc2`, finished 22:16.

## Verdict

**GO.** 4 of 32 reach ligand RMSD <= 10.0 A against a pre-registered bar of **>= 3 of 32**.
4 of 32 were refused by the target-superposition control, inside the pre-registered tolerance of 6.

| | stage A (pre-constraint, n=28) | the 48 (post-constraint, n=40) |
|---|---|---|
| CA sc_DockQ, median | 0.0295 | 0.0251 |
| CA sc_DockQ, **best** | **0.6057** | 0.0865 |
| Fnat, median | 0.0000 | 0.0000 |
| Fnat, **best** | **0.5000** | 0.0263 |
| LRMS, median | 28.642 A | 31.117 A |
| LRMS, **best** | **2.773 A** | 15.034 A |

The four that cleared:

| design | CA sc_DockQ | Fnat | LRMS |
|---|---|---|---|
| `tnfa_corrected_40_s2` | **0.6057** | **0.500** | **2.773 A** |
| `tnfa_corrected_40_s1` | 0.4127 | 0.286 | 5.508 A |
| `tnfa_corrected_3_s1` | 0.3433 | 0.227 | 5.786 A |
| `tnfa_corrected_9_s2` | 0.2890 | 0.235 | 8.191 A |

## What is real, and it is a change of regime rather than an increment

The best design reproduces **half** of its designed interface contacts and sits **2.77 A** from the
designed pose. The best of the 48 reproduced **2.6%** of its contacts at 15.03 A, and the best of
all 40 never cleared 15 A. Fnat 0.50 against a prior ceiling of 0.026 is a nineteen-fold
difference, and it is not a threshold artifact: three more designs land between 5.5 and 8.2 A,
where nothing in this project had previously gone.

`tnfa_corrected_40_s1` and `_s2` are two **independent ProteinMPNN sequences on the same backbone**,
and both clear. That is an internal replication on backbone 40, which is worth more than two
unrelated singletons.

## What is NOT established, and the matched pairs are the reason

17 of the 32 share a backbone and an id with a design already folded post-constraint; 2 were
refused, leaving **15 matched pairs** — same backbone, same designed pose, the constraint the only
difference.

**Pre-constraint is better on LRMS in 9 of 15. One-sided sign test p = 0.304.** Median LRMS moves
26.5 -> 31.6 A. So **the matched-pair design does not establish that the histidine constraint
caused the pose failure.** Across the bulk of the pairs the difference is noise.

What moved is the tail, and there the effect is large: the two best pre-constraint designs in the
paired set, `40_s2` at 2.77 A and `3_s1` at 5.79 A, have post-constraint partners at **29.3 A** and
**42.3 A**. The reading this supports is narrow and should be written that way: removing the
constraint did not shift the population, it restored the *possibility* of a rare good pose. On 15
pairs that is a hypothesis with one supporting tail, not a demonstrated mechanism.

## Three things that bound what this buys

**1. Three backbones, not four designs.** The four successes sit on backbones 40, 9 and 3. Counting
designs overstates the independent evidence by a third.

**2. Two of the four carry cysteine, including the best one.** `40_s2` carries one and `40_s1`
carries two, and this project's default is Cys-free for de novo work. So of the four designs that
cleared the pose gate, **two are submissible as they stand** — `3_s1` and `9_s2`. The single best
pose in the project's history is on a design the liability rule excludes.

This does **not** disqualify them as stage-B *parents*. The loop redesigns the binder sequence every
round, so cysteine can be bred out rather than carried: the fix is to pass ProteinMPNN an explicit
cysteine ban (`--omit_AAs C`) in every redesign, which should be added to the stage-B command
before it runs and is not a change of bar.

**3. The composition critique from the addendum stands unchanged.** All four carry exactly one
histidine and pI 4.83-5.33, matching the measured binders. All four also sit at glutamate 20.5-28.9%
against the winners' 10.8-18.1%, and at Pro+Gly 3.6% against their 8.4%. They match the winners'
two scalars by a route the winners did not take. A good pose on our own backbone is what cleared
here; nothing about this result says the chemistry is right.

## What it licenses

Exactly what the pre-registration said a GO licenses: **a pose surviving the gate is reachable on
our backbones.** It does not license a claim about chemistry, about binding, or about the
constraint's causal role. Stage B — up to 10 rounds, ~$8.90, Chai-1 mandatory as a second referee
from round 4 — is now *eligible* to be proposed, and per the standing rule it needs its own
explicit yes.

## One operational note for whoever runs the next fold

The local entrypoint **did not write its outputs**: the run logged `Runner terminated` and
`runs/A-depthA-out` did not exist afterwards. All 32 folds were recovered intact from the
`esmfold2-runs` Volume, which is exactly what the per-fold commit was built for:

    mkdir -p runs/A-depthA-out && cd runs/A-depthA-out && modal volume get esmfold2-runs AdepthA

This is the third time the local-write path has failed on this project and the first time nothing
was lost. The durability fix works; the local write should not be trusted as the only copy.

## Artifacts

| file | contents |
|---|---|
| `analysis/02-tnf/depthA_pose_2026-10-08.tsv` | 28 scored designs: CA sc_DockQ, Fnat, LRMS, iRMS |
| `runs/A-depthA-in/` | the 32 complex inputs, target identical to the 48's |
| `runs/A-depthA-out/AdepthA/` | 32 co-folds, recovered from the Volume |
