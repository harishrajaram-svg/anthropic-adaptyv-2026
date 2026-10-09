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
