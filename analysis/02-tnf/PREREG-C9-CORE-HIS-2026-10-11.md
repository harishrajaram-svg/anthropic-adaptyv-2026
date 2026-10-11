---
type: preregistration
project: anthropic-adaptyv-2026
problem: 02-tnf-alpha
arm: C9 buried core histidine
status: PRE-REGISTERED — written 2026-10-11 2:21 AM EDT, BEFORE any C9 fold exists
---

# C9 — put the titratable residue where it cannot compete with the binding

## The assumption the seven closed routes shared

Every pH route in this project put the titratable residue **at the interface contact**: §4's anchor
plan, the constrained designer, A3's substitutions, C4's target histidine, C6's native interface
histidines, C7's shell rebuild, C8's frustrated pair. Tonight's measurements say why they all failed
the same way — on this target the residues that carry the binding and the positions where a
protonated histidine would push the interface apart are **disjoint**:

- **C3**: the margin is carried by Arg27, Thr54 and Tyr20, none of them titratable; six distal
  alanines moved it only 0.198-0.569.
- **C6**: 48 designs carry a native releasing histidine with geometry replicating 5/5, and none
  holds above +5.05.
- **C7**: the shell repair that recovers 59% of a substitution's cost stabilises the histidine
  against a carboxylate.
- **C8**: at K31 the histidine costs 1.476, worse than deleting the residue (0.961), and the
  frustrated-pair premise was false (K31Q costs 0.330 rather than gaining).

## The mechanism this arm uses instead

A **buried histidine in the binder's own core** acts through the binder's fold, not through the
contact. Neutral and packed at pH 7.4; protonated at pH 6.0, where a desolvated charge with no polar
partner costs several kcal/mol of fold stability, so the binder loses its own structure and with it
its binding surface. Precedent for the class: influenza hemagglutinin's low-pH transition and the
diphtheria toxin T-domain both turn on buried-histidine protonation.

**It cannot compete with Arg27/Thr54/Tyr20 because it is not near them**, which is the obstruction
every closed route hit.

## The sites exist, measured on the design's own fold

`tnfa_corrected_3_L0r4k0` (pooled +6.971, **zero histidines**) has **28** positions that are buried
(≥45 binder heavy atoms within 8 Å of the side-chain tip), **non-interface** (>11 Å from the target)
and have **no polar partner** within 4 Å to stabilise a charged imidazole. The eight folded here:

| position | native | d_target | neighbours ≤8 Å | note |
|---|---|--:|--:|---|
| **29** | Phe | 13.7 Å | 90 | aromatic → imidazole, most volume-conservative |
| **48** | Phe | 12.5 Å | 90 | same |
| 5 | Val | 11.1 Å | **104** | most buried in the molecule |
| 75 | Leu | 12.9 Å | 99 | |
| 49 | Leu | 17.5 Å | 98 | |
| 9 | Leu | 16.1 Å | 92 | |
| 55 | Leu | 20.0 Å | 92 | |
| 79 | Leu | 12.2 Å | 92 | |

Zero existing histidines means a single substitution makes the molecule unambiguous: one titratable
residue, nowhere near the contact, with the parent as its own matched 0-His control.

## Two stages, the cheap one first

**Stage 1 — does the core tolerate a histidine at all?** This is a *monomer* question and monomer
folds cost ~3 s. The 8 variants plus the parent **folded in-run**, binder alone, seeds 1-5 = **45
folds, ~$1**, B200.

| bar | threshold |
|---|---|
| **C9-M1** | binder-alone pLDDT ≥ **0.70**, the organisers' own floor |
| **C9-M2** | within **0.05** of the in-run parent (C1 measured it at 0.910) |

Variants failing M1 are dropped and never folded in complex. If **0 of 8** clear M1, the arm stops
here for ~$1 and the finding is that this core will not host an ionisable residue.

**Stage 2 — does it still bind?** The top 3 survivors by pLDDT, each with a composition-matched null
(`random.Random(20261006)`), human trimer, 5 seeds = **40 folds, ~$3**, B200.

| bar | threshold |
|---|---|
| **C9-B1** | median margin ≥ **+6.347** |
| **C9-B2** | ≥ **+6.971**, the parent — the substitution is free |
| **C9-B3** | the histidine is still buried **in the complex pose**, re-measured rather than assumed |

The headroom is **0.62 units**, and C3 measured non-interface substitutions at 0.198-0.569, so a
core substitution should land inside the budget **if the fold survives stage 1**. Free throughout:
pI must stay below 6.0 (one histidine on a 4.83 background lands near 5.0), no cysteines.

## If it passes, what ships

`3_L0r4k0` and `3_L0r4k0_X##H` as a **matched pair** — identical but for one buried titratable
residue. `submission-basis-p2.md` names that 0-His matched control "the load-bearing arm" and "the
thing most entrants will omit."

## 🔴 What C9 cannot do, stated plainly because this one has a specific trap

ESMFold2 is pH-agnostic and no pKa is computed, so C9 shows only that the histidine is buried, the
fold survives at neutral and the design still binds. **The magnitude is unknown**: burial in an
83-residue bundle may not shift the pKa enough to titrate between 7.4 and 6.0, and PROPKA was
retired here because its within-design noise exceeded its between-design signal.

🔴 **And the mechanism's failure mode at pH 6.0 is loss of structure, which the assay cannot
distinguish from aggregation.** That is the same ambiguity that disqualified the pI-6.83 candidate
tonight. The difference is that here it is the *intended* mechanism rather than an artifact — and
the methods document must say so outright, so that a reviewer reading "no binding at pH 6.0" knows
we predicted unfolding and did not predict a clean electrostatic release. **No C9 result may be
described as a demonstrated pH switch.**

One launch per stage, ~$4 total, no continuation without a new decision.

---

## AMENDMENT 2 — arithmetic correction, written 2026-10-11 2:28 AM, before any stage-2 fold exists

Stage 2 as specified said "top 3 survivors, each with a null, 5 seeds = **40 folds**". Three designs
plus three nulls is **6 complexes x 5 seeds = 30 folds**, not 40. The fold count was wrong; the
design is unchanged. Stage 2 runs 30 folds.

**Stage 1 result, for the record, before stage 2 lands:** 8 of 8 variants clear M1 and 6 of 8 clear
M2. Parent 0.911; F29H 0.906, L75H 0.905, L49H 0.900, V5H 0.895, F48H 0.887, L55H 0.887, L9H 0.859,
L79H 0.816. The core tolerates a histidine at every site tested. The prereg's top-3 rule selects
F29H, L75H and L49H; the three M2 passers below them are a declared reserve and folding them would
require a further amendment.
