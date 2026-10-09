---
type: pre-registration
project: anthropic-adaptyv-2026
problem: 02-tnf-alpha
arm: constrained restart (D2)
written: 2026-10-09 ~13:00 ET
status: COMMITTED BEFORE ANY DESIGN OF THIS ARM EXISTS
---

# Pre-registration — the constrained restart

Committed before a single design of this arm exists. Every bar below is fixed at this commit.
If a bar is missed, that is the result; it is not grounds for a further arm.

## 1 · What this arm varies against the depth arm (METHODS §6.10h, §6.12)

| held | varied |
|---|---|
| generator Genie3, fired ONCE per lineage; rounds are sequence-only | **mouse trimer co-folded EVERY round**, selection on the worse of the two species |
| sequence designer SolubleMPNN | **1-2 histidines required** at cation-reachable interface positions |
| predict-then-redesign on the predicted complex, same root_backbone_id | `MAX_FORCED_HIS` **8 -> 2** |
| ranking instrument `pae_interface_mean` (ef2full), unchanged | **12 rounds** (the depth arm ran 5) |

Mouse is a **trimer** (3 x 156 + 83 = 551 res), not the dimer of §6.10d. §6.12(b) measured the dimer
inflating margins a median +16% and running 6.8x noisier. Mouse is scored with the **wide offset set**
`(0,5,-5,4,-4,6,-6)`: the standard set under-reads mouse by up to 0.134 because the designed target
chains are human at 152 residues against a 156-residue mouse prediction.

## 2 · Lineages, and the selection rule each one uses

8 lineages x 4 children = 32 designs/round; x 2 species = **64 folds/round**; fuse **800**.

| lineages | backbones | selection | status |
|---|---|---|---|
| 6 | 40, 3, 16, 10, 9, probe50-unused-A | `ca_sc_dockq` only | **CLEAN** — shippable |
| 1 | 40 | **4:1 ipSAE + sc_DockQ** per protocol line 115 | **DECLARED CONTAMINATED** |
| 1 | probe50-unused-B | `ca_sc_dockq`, **no histidine constraint** | His control |

**Frozen decision C1 is UPHELD for the submission.** Six lineages never see the ranking instrument;
`select_parent` continues to raise on any undeclared confidence field. The 4:1 lineage is fenced:

- its designs are marked in the sheet and **are not a submission source**, whatever they score;
- they are **excluded from any claim that our ranker predicted our own designs**;
- if the 4:1 lineage outperforms the clean six, that is a **reported finding**, not a reason to ship
  from it. Deciding this now is the point of writing it down now.

What this buys: a controlled head-to-head, same backbone, 12 rounds, between the protocol's
selection rule and ours. The released campaign ran 4:1 throughout and so contains no such control.

## 3 · The selection formula, exactly

Per round, per species, over all 32 children of that round:

1. z-score `ipSAE_min` and `ca_sc_dockq` within the round;
2. blend: clean lineages use `ca_sc_dockq` alone; the 4:1 lineage uses `4*z(ipSAE) + 1*z(sc_DockQ)`;
3. **take the WORSE of the two species** for each design;
4. best-per-lineage becomes that lineage's parent (`select_per_lineage`, not a global top-k — a
   global top-k collapsed the beam onto one backbone after one round in the depth arm).

## 4 · Bars, fixed now

**Baseline to beat.** The depth arm at 5 rounds, re-scored at 5 seeds (seeds 1-5, 42 excluded):
median margin **+6.938**, best **+8.031** (`40_L1r4k1`), **10 of 12** clearing the measured
non-binder median **+6.3473**, and **1 of 12** above the measured binder median **+7.8144**.

| # | bar | verdict if missed |
|---|---|---|
| B1 | **>= 3 of the final clean set above +7.8144** (5-seed, human) | 12 rounds did not beat 5 rounds; depth is saturated below the binder band |
| B2 | at least 1 design above the measured binder **max +8.2091** | no design in this project has ever exceeded a real binder; missing it is expected, clearing it is the headline |
| B3 | the worse-of-two-species blend improves monotonically over any 4 consecutive rounds | the loop is not optimising; stop at the plateau and bank the folds |
| B4 | **>= 6 of the final clean set carry 1-2 histidines AND stay >= +6.3473** | the pH mechanism is not reachable without paying the binding bar |

**B4 is the falsifiable histidine test.** If the unconstrained control lineage exceeds the mean of the
constrained clean lineages by **> 1.0 margin unit**, the constraint LOSES and objective 2 is recorded
as unaddressed by declaration rather than by accident. No unconstrained SolubleMPNN baseline has ever
existed in this project (§9); this arm creates one.

## 5 · Stopping rule, and the fuse

Hard stop at **800 folds**. 12 rounds x 64 = 768, leaving 32 folds of headroom.
Early stop if B3 fails: no improvement in the blend over 4 consecutive rounds ends the arm and the
remaining folds are NOT respent on a further condition.

## 6 · What this arm cannot answer, stated in advance

- **No mouse labelled control exists.** A mouse margin above +6.3473 means "beats its own null by more
  than the human non-binder median margin". It is not evidence any design binds mouse TNF-alpha.
- **The ranking instrument's honest ceiling is ~0.70** (§6.11, out-of-sample 0.674-0.702 across 16
  targets). Small differences between designs are not resolvable and no bar here pretends otherwise.
- **Single-seed selection inside the loop is noisy.** §6.12(a) measured Spearman 0.538 between
  single-seed and 5-seed orderings. The protocol (line 147) promotes to 5 seeds BEFORE parent
  selection; at 5 seeds that is 320 folds/round and unaffordable against this fuse. We select at 1
  seed and 5-seed only the survivors. This is a known, declared weakness of this arm.
- **Depth does not buy affinity.** Within target, Spearman(rounds, log K_D) among the release's
  binders is -0.092 (§6.11). Nothing here predicts how tightly anything binds.

---

# AMENDMENT 1 — 2026-10-09 ~14:00 ET, before any design of this arm exists

Recorded as an amendment rather than an edit to the text above, so the original and the change are
both readable. Nothing had been generated or folded when this was written; the fuse stands at 0.

## A1.1 · The histidine control was confounded, and is moved

§2 placed the unconstrained-histidine control on an **unscreened probe50 backbone**. That control
could not have answered B4: an underperforming lineage there is indistinguishable between "the
histidine constraint was load-bearing" and "that backbone was a dud". Worse, the only sequences
those backbones carry are Genie-48 ones, measured 2026-10-09 at CA sc_DockQ **0.008-0.087** — the
noise floor — against backbone 40's 0.6057.

**Both controls now sit on backbone 40, sharing lineage L1's parent**, so each isolates exactly one
variable against a matched comparator.

## A1.2 · Seven lineages, not eight

Of **42** pose-screened backbones, only **5** are inside the 10 A entry gate. There is no good sixth
distinct backbone: the next candidate, backbone 19, sits at **11.47 A**, which the runner's own
auto-selection refuses. Seeding a lineage the entry gate rejects is a deviation with no argument
behind it, so it is dropped rather than taken.

| L | backbone | parent | dockq | lrms | role | C1 status |
|---|---|---|--:|--:|---|---|
| 0 | 16 | `tnfa_corrected_16_s1` | 0.6655 | 2.023 | clean + His | CLEAN |
| 1 | 40 | `tnfa_corrected_40_s2` | 0.6057 | 2.773 | clean + His — **the reference** | CLEAN |
| 2 | 10 | `tnfa_corrected_10_s2` | 0.4061 | 5.330 | clean + His | CLEAN |
| 3 | 3 | `tnfa_corrected_3_s1` | 0.3433 | 5.786 | clean + His | CLEAN |
| 4 | 9 | `tnfa_corrected_9_s2` | 0.2890 | 8.191 | clean + His (retired at 3 rounds in the depth arm) | CLEAN |
| 5 | 40 | `tnfa_corrected_40_s2` | 0.6057 | 2.773 | **no histidine constraint** — B4 control | CLEAN |
| 6 | 40 | `tnfa_corrected_40_s2` | 0.6057 | 2.773 | **4:1 ipSAE+sc_DockQ** — C1 control | **CONTAMINATED** |

**Six of seven lineages remain C1-clean and shippable.** Three sit on backbone 40; that concentrates
the SEARCH and is the price of matched controls. It does not touch the submission's structural
diversity, which is decided at the pick, not here.

## A1.3 · Fourteen rounds

7 lineages x 4 children x 2 species = **56 folds/round**. 14 x 56 = **784** against the 800 fuse,
16 folds of headroom. `MAX_ROUNDS` moves **12 -> 14**.

This is the amendment's one real gain and the reason to prefer seven lineages over eight: every
Genie3 TNF binder in the released campaign sits at **8-12 rounds**, and **0 of 37** zero-round TNF
designs bound anything. The depth arm stopped at 5. Fourteen clears the whole observed band.

**B1-B4 are unchanged.** The baseline to beat is unchanged. The stopping rule is unchanged
(patience 4). Nothing below §4 of the original is altered.

---

# AMENDMENT 2 — 2026-10-09 ~14:15 ET. The constrained restart is DEAD. This is what runs instead.

## A2.1 · What killed it, measured

The D1 dry run (7 lineages, 56 folds, tag `cr1`) put **0 of 28 children inside the 10 A pose gate**.
Parents were CA sc_DockQ 0.289-0.666 at lrms 2.0-8.2; children came back median 0.027, best 0.124,
lrms median 30.9. Every lineage lost 0.25-0.57 dockq in one round.

A 3-arm diagnostic on one parent (`tnfa_corrected_40_s2`, 0.6057 / 2.773 A), 4 children each, tag
`diag1`, isolated it:

| arm | best dockq | delta | best lrms | in gate |
|---|--:|--:|--:|--:|
| His only, **no** acid ban | 0.0702 | -0.5355 | 17.391 | 0/4 |
| acid ban only, **no** His | 0.0521 | -0.5536 | 20.634 | 0/4 |
| **neither** | **0.2860** | -0.3197 | **6.147** | **1/4** |

**It is not the acid ban specifically — His-only is equally destructive.** Writing a per-position
constraint file *at all* collapses the interface; 19 of 83 positions is enough regardless of which
residues are restricted. **Objective 2 is not reachable through `omit_AA_jsonl` in this pipeline,
and B4 cannot be tested as written.** B4 is retired, not failed: it was never measurable.

Stated as a caveat rather than buried: the clean arm's 0.2860 is a **best-of-4** against the depth
arm's per-round best of ~0.62, which was **best-of-8**. Under-sampling is a live alternative to
"one round of unconstrained redesign loses a third of the pose", and A2.2 restores 8 children.

## A2.2 · The arm that runs: an UNCONSTRAINED continuation, 6 lineages, 4 backbones

No constraint file beyond the cysteine ban — the only configuration that holds pose. The depth arm
ended round 5 with **4 lineages on only TWO backbones**, and backbones 16 and 10 were never in the
loop at all, so two fresh lineages are seeded alongside the four continued ones.

| L | seed | backbone | true depth at start | note |
|---|---|---|--:|---|
| 0 | round-5 survivor, lineage 0 | 3 | 5 | continued |
| 1 | round-5 survivor, lineage 1 | 40 | 5 | continued |
| 2 | round-5 survivor, lineage 4 | 3 | 5 | continued |
| 3 | round-5 survivor, lineage 5 | 40 | 5 | continued |
| 4 | `tnfa_corrected_16_s1` | 16 | 0 | **fresh** — best single pose in the project, 0.6655 |
| 5 | `tnfa_corrected_10_s2` | 10 | 0 | **fresh** — never entered a loop |

6 lineages x 8 children x 2 species = **96 folds/round**; 8 x 96 = **768** against the 800 fuse.
Continued lineages reach **true depth 13**, fresh ones **8**. Both inside the 8-12 band where every
released Genie3 TNF binder sits. `MAX_ROUNDS` 14 -> **8**; `SEQS_PER_PARENT` 4 -> **8**.

**Depth is recorded per lineage, not read off the round counter**, because this run has two depths
in flight; `_true_depth()` parses it from the design id.

**Mouse stays in every round, as a trimer.** Step 0 earned it: the selection score agrees across
species at Spearman **+0.762** above the noise floor (n=8), with 5 of 6 top designs shared, against
**+0.084** for the margin score.

## A2.3 · What is unchanged

B1, B2 and B3 stand exactly as written. The baseline to beat stands. Patience 4 stands. C1 stands:
the clean lineages never see the ranking instrument. **The 4:1 contaminated lineage is DROPPED from
this run** — with 6 slots and 4 backbones to carry, a selection-rule control is a luxury; the C1
question stays open and unmeasured rather than being answered badly.

## A2.4 · A bug this run would have hit, fixed first

`RUN_TAG` scoped the Volume names and input dirs but not the round TSV or the per-species output
dirs, so `diag1`'s round 1 destroyed `cr1`'s round 1 on local disk. Recovered from the Volume --
the "never trust the local entrypoint write" rule paying off -- and now fixed: writes are
tag-scoped and readers fall back to the untagged names so rounds 1-5 of the depth arm still resolve.
Left unfixed, round N of this run would have overwritten round N of the depth arm.
