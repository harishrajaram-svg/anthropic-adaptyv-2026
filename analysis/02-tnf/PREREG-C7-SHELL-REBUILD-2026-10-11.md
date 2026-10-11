---
type: preregistration
project: anthropic-adaptyv-2026
problem: 02-tnf-alpha
arm: C7 shell rebuild around a pinned histidine
status: PRE-REGISTERED — written 2026-10-11 1:36 AM EDT, BEFORE any C7 sequence or fold exists
---

# C7 — pin the histidine where it is tolerated, and rebuild only its neighbourhood

## The decomposition this arm rests on, which did not exist before tonight

A3 measured what a histidine substitution costs. C3 measured what each position contributes.
Subtracting them separates two costs that were confounded in every earlier attempt. Both sets
change one residue on the same His61 background, so the subtraction is matched.

| position | →Ala (C3) | →His (A3) | cost of losing the native residue | extra cost of the histidine |
|---|--:|--:|--:|--:|
| **D50** | 3.706 | **4.097** | 4.31 | **none — His beats Ala by 0.39** |
| E62 | 7.508 | 1.566 | 0.51 | **+5.94** |
| T54 | 2.707 | 0.463 | 5.31 | +2.24 |
| R27 | 0.283 | 0.270 | 7.73 | ~0 (position gone either way) |

A3's uniform failure was not uniform. At **E62** the glutamate contributes almost nothing and the
histidine is actively badly accommodated. At **D50** the histidine costs nothing beyond deleting the
aspartate — and an aspartate's contribution is the kind of thing a redesigned neighbourhood can
partly replace. A point substitution has no repair mechanism; that is what A3 lacked, not a better
position.

**Second input: geometry replication is pose stability.** His50 in `relD50H` sits 4.39, 7.94, 15.68,
16.36 and 14.00 Å from the nearest target cation across five seeds — in three of five the pose has
wandered. C6's designs replicated 5/5 because they hold their pose. So the requirement is not
"place a histidine at a cation", it is **"hold a stable pose while a histidine sits at a cation"**,
and no arm has pursued both at once.

## What this arm does, and why it is not the restart that collapsed

The constrained restart forced histidines at many cation-reachable positions during **de novo**
design with the whole sequence in play, and collapsed the pose (0.6349/0.5053/0.6203 unconstrained
against 0.0126/0.0309/0.0772 constrained). C7 fixes **one** histidine on a **finished, high-margin**
molecule and lets SolubleMPNN repair **only its neighbourhood**. It is the depth loop — the one
procedure in this project that demonstrably moved margins, +0.320 to +6.938 — pointed at a single
position.

**Template:** `tnfa_corrected_40_L1r4k1_relD50H`, seed 1 fold. ⚠️ **Declared: that seed was chosen
because its pose is the best of the five** (His50 4.39 Å from ARG82, against 14-16 Å in three
others). Selecting the design template on pose is a selection on the input and is reported as such.

**Fixed, and why:** Arg27, Thr54, Tyr20 — C3 measured them at 7.73, 5.31 and 4.86 units, so they
carry the interface — plus His50 (the mechanism) and His61 (worth 7.1 units by A3's `ctrlH61Q`, so
arm A keeps it).

**Redesigned: 11 positions**, the shell whose side chains lie within 8.0 Å of His50's side chain and
are not fixed: **24, 31, 43, 46, 47, 48, 49, 51, 52, 53, 76**. Position 53 is in that shell and C3
measured it at 0.846, so it is cheap to move.

| arm | template | His61 | what it tests | deficit to close |
|---|---|:-:|---|--:|
| **A** | `relD50H` seed 1 | kept | can the shell recover Asp50's loss | **+2.25** to +6.347 |
| **B** | `relD50H_H61Q` seed 2 | **removed** | the clean mechanism, one releasing His and no tightening one | **+4.39** |

Arm B is the scientifically cleaner molecule — arm A carries a tightening His61 and a releasing
His50, so its net pH direction is ambiguous, which is the ambiguity A3's own prereg named. Arm B has
a far larger deficit. Both run because generation is free.

**Generation:** local SolubleMPNN (`--use_soluble_model`, `--omit_AAs CX`, sampling_temp 0.1, seed
37), 64 sequences per arm, positions outside the shell fixed via `make_fixed_positions_dict.py
--specify_non_fixed`. **Post-hoc verification, as the depth loop does it:** every output is checked
residue-by-residue against the template outside the shell, and refused if any fixed position moved
or if His50 or (arm A) His61 is absent — the fixed-positions file loads silently or not at all.

**Free screens before any fold:** `express_qc_p2` with pI required **below 6.0** (the parent sits at
4.65 and one histidine should not reach the assay window — the molecule that failed this tonight,
`40_L3r5k2`, was at 6.83), zero cysteines, and identity to the parent reported.

**Folds:** the best 8 of arm A and 4 of arm B by MPNN score, each with a composition-matched null
(`random.Random(20261006)`), 5 seeds = **120 folds**, split across H100 and H200 shards in parallel.
~$8.

## Bars — fixed now

| bar | threshold | meaning |
|---|---|---|
| **C7-B1** | median margin ≥ **+6.347** | the hold is recovered past the non-binder median |
| **C7-B2** | median margin ≥ **+7.706** | it would also match what currently ships |
| **C7-B3** | His50 releasing geometry in ≥ **3 of 5** seeds | the mechanism is installed and the pose is stable |

**B1 AND B3 is the result this project has never produced**: a design that holds TNF-α while
carrying a replicated releasing histidine. Arm A passing both is a real result with an ambiguous
net pH direction, stated. Arm B passing both is the clean one. B3 without B1 reproduces C6. B1
without B3 is another binder.

**Stopping rule: one generation, one fold launch, ~$8, no continuation without a new decision.**
If arm A's best fails B1, the shell-repair hypothesis is reported as measured-false and objective 2
closes for the sixth time.

## 🔴 What C7 cannot do

ESMFold2 is pH-agnostic, so B3 is a geometric arrangement in a predicted pose and nothing here is a
demonstrated pH switch. No histidine pKa is predicted. A B1+B3 pass ships as a **declared
hypothesis with its own matched controls** — the parent, `relD50H`, and `ctrlH61Q` are all already
measured, which is what makes the claim checkable rather than decorative.
