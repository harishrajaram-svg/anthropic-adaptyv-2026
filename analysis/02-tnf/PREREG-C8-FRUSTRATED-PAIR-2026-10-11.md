---
type: preregistration
project: anthropic-adaptyv-2026
problem: 02-tnf-alpha
arm: C8 frustrated cation pair
status: PRE-REGISTERED — written 2026-10-11 2:06 AM EDT, BEFORE any C8 fold exists
---

# C8 — swap a charge the target does not want

## The inversion this arm rests on

Every earlier route asked *where can a histidine go*, so the histidine always had a deficit to climb
out of: forcing one collapsed the pose, substituting one lost the hold (A3, 0 of 11), repairing the
shell around one recovered 59% of the loss and stabilised the wrong geometry (C7), and selecting a
native one found 48 designs of which none holds above +5.05 (C6).

C8 asks instead: **where is there already a charge the target does not want?** A binder Lys/Arg
pointing at a target Lys/Arg is a **frustrated like-charge pair**, mildly unfavourable at pH 7.4.
Replacing that binder cation with histidine is predicted to work in both directions:

- **pH 7.4** — histidine neutral, the like-charge repulsion is **relieved**, so binding may improve
- **pH 6.0** — histidine protonated, the repulsion returns, the interface is pushed apart

The substitution pays for itself on the binding side instead of owing. That is the opposite economics
of every arm above, and it is why this is worth folding.

## The scan, and why only one candidate survives

Across the 9 designs in this project that hold, exactly **two** frustrated cation-cation pairs exist,
and both sit in the two designs being submitted:

| design | position | target partner | d | status |
|---|---|---|--:|---|
| `40_L1r4k1` | R27 | LYS112 chain A | 5.06 Å | **excluded** — C3 measured R27 as the dominant anchor (R27A → +0.283, null territory), and A3's `relR27H` read +0.270 |
| **`3_L0r4k0`** | **K31** | **LYS112 chain B** | **4.86 Å** | **the candidate**; nearest carboxylate 5.10 Å |

C3 is what excludes the first, which is the second time tonight that scan has prevented a spend.

**LYS112 is conserved in mouse as K111** (pairwise alignment of the two constructs we fold, 79.5%
identity), so unlike mechanism B's H73 a switch here is compatible with objective 3.

`3_L0r4k0` carries **zero histidines**, so no existing histidine can confound the result — the
confound that made A3 uninterpretable until its `ctrlH61Q` control landed.

## What folds, and the control series

The parent plus four single substitutions at position 31, each with a composition-matched null
(`random.Random(20261006)`), 5 seeds: **10 complexes, 50 folds, 5 shards, ~$4.**

| variant | what it isolates |
|---|---|
| parent `3_L0r4k0` | baseline, folded **in-run** (pooled 15-seed +6.971) |
| **K31H** | the mechanism |
| **K31Q** | non-titratable, same loss of positive charge — the control problem 1 learned the hard way, when Gln arms switched at the same rate as the His arms (4% vs 6%, p = 0.53) |
| **K31A** | side-chain deletion; the C3-style cost of simply losing the lysine |
| **K31R** | cation retained, different shape; perturbation control |

## Bars — fixed now

| bar | threshold | meaning |
|---|---|---|
| **C8-B1** | K31H median margin ≥ **+6.347** | it still holds |
| **C8-B2** | K31H ≥ **+6.971** (the parent) | the neutral-pH rationale is real and the swap is free or favourable |
| **C8-B3** | His31 releasing geometry in ≥ **3 of 5** seeds | the mechanism is installed and the pose is stable |

**B1 AND B3 ⇒ a pH candidate on a design we are already shipping.** The headroom is **0.62 units**
before the floor, and K31A measures directly whether the lysine was worth more than that.

**Interpretation fixed in advance:**
- K31H ≈ K31Q ≈ K31R ⇒ position 31 is tolerant and the histidine went in cleanly
- K31H ≪ K31Q ⇒ the histidine specifically is badly accommodated — the E62 pattern from A3/C3
- K31A ≫ K31H ⇒ the cost is the histidine, not the lost lysine, and a shell repair is the follow-up
- all four below the floor ⇒ position 31 carries real binding and the frustrated pair was not free

## If it passes, what ships

`3_L0r4k0` and `3_L0r4k0_K31H` as a **matched pair** — identical molecules but for one titratable
residue, with K31Q and K31A as declared in-silico controls. `submission-basis-p2.md` names that
0-His matched control "the load-bearing arm" and "the thing most entrants will omit". A measured
ratio between the pair is a real objective-2 result at any hit rate, and it is interpretable in
either direction. Two slots of twenty.

## 🔴 What C8 cannot do

ESMFold2 is pH-agnostic. B3 is a geometric arrangement in a predicted pose; the pH argument is
electrostatic reasoning about a measured distance, not a prediction from a model that sees protons.
No pKa is computed — PROPKA was retired here because its within-design noise exceeded its
between-design signal. **No C8 result may be called a demonstrated pH switch.** One launch, ~$4, no
continuation without a new decision.
