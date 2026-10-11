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

---

## AMENDMENT 3 — fresh seeds on L49H, written 2026-10-11 2:47 AM, before any stage-4 fold exists

Stage 2 measured L49H at +7.151 on seeds 1-5 against the parent's +6.976 on the same seeds. C2
measured a **0.33** shift between a five-seed draw and ten unseen seeds on the leader, so +0.175 is
inside the noise that draw can carry, and the parent holds **15** seeds against L49H's 5. Replacing
a 15-seed design with a 5-seed one is the error C2 exists to prevent.

**Stage 4:** L49H and its matched null on **seeds 6-15**, human trimer, 2 shards, B200 = **20 folds,
~$1**. The parent already carries seeds 1-15 from C2, so this makes the comparison 15 against 15.

| bar | threshold | meaning |
|---|---|---|
| **C9-R1** | L49H pooled 15-seed ≥ **+6.971** | not worse than the parent on equal evidence |
| **C9-R2** | ≥ **+6.347** | still holds at all |

**Decision rules, fixed now.** R1 and R2 pass ⇒ L49H may take the backbone-3 slot in place of its
parent, and the parent's measured numbers are reported as the in-silico control. R1 fails but R2
holds ⇒ the parent keeps the slot on its stronger estimate, and L49H is reported as a measured
equal-or-slightly-worse variant that carries the mechanism — a result either way. R2 fails ⇒ stage
2's +7.151 was a seed artifact and C2's lesson is confirmed a third time.

Whether the pair ships **together** is a separate question that this arm cannot settle, because the
prescreen flags a one-residue pair as `batch_duplicate` on both members.

---

## AMENDMENT 4 — the partially buried sites, written 2026-10-11 3:07 AM, before any stage-6 fold exists

Stage 5 measured His49 at pKa **4.81-4.82**, delta_protonation **0.058**, INERT — below the
pre-declared weak threshold of 0.10. The cause is the arm's own premise: burial suppresses the pKa
(model compound 5.98; this project's pre-registration records 1.5-2.5 units lost on burial), so the
desolvation that would make a buried imidazolium destabilising is what stops it forming.

**All eight sites folded in stage 1 were deeply buried (82-104 neighbours within 8 Å).** Of the 28
qualifying positions on `3_L0r4k0`, twenty were never tested, and several sit at **45-48
neighbours** — partially buried, where the pKa may survive nearer 6.0 while protonation still costs
the fold something. That is the narrow window this mechanism needs, and it has not been looked at.

**Stage 6:** all twenty remaining positions, one His substitution each, binder alone, seeds 1-5 =
**100 monomer folds, ~$2**, B200. Then `bin/propka_his.py` on every resulting structure.

Positions: 16, 36, 38, 41, 44, 45, 46, 47, 50, 53, 54, 60, 63, 64, 65, 66, 67, 76, 78, 82.
Gly54 and Pro67 are included knowing a substitution there may break the backbone; the fold screen
is what catches that, and it costs the same as any other site.

| bar | threshold | meaning |
|---|---|---|
| **C9-M1** | binder-alone pLDDT ≥ **0.70** | the fold survives |
| **C9-P1** | delta_protonation ≥ **0.10** | the histidine titrates measurably across 7.4 → 6.0 |
| **C9-P2** | delta_protonation ≥ **0.25** | a real switch by the instrument's own pre-declared bar |

**M1 AND P1 is the minimum for a site to be worth folding in complex.** If no site clears P1, the
buried-histidine mechanism is closed on this molecule by measurement rather than by argument, and
the pKa-versus-burial relationship across 28 positions is itself the reportable result.

**Declared in advance:** PROPKA gating was retired on this project for noise, and a buried histidine
is its hardest case, so P1 and P2 are screens, not measurements. A site clearing them would still
need a complex fold, a mouse leg and the prescreen before it could ship. One launch, ~$2, no
continuation without a new decision.

---

## AMENDMENT 5 — complex folds on the titrating sites, written 2026-10-11 3:18 AM, pre-fold

Stage 6 measured 14 of 20 positions clearing M1 and P2, with pKa 6.0-7.2 against row 1's His49 at
4.81. Spearman(burial, pKa) = **-0.600**: the stage-1 rule (deep burial AND no polar partner within
4 Å) selected exactly the sites where the proton never binds, and the sites that titrate are
moderately buried and often polar.

**Stage 7:** the four highest-delta sites that also fold well — **T36H, S76H, S65H, D47H** — against
the human trimer with composition-matched nulls, 5 seeds, 4 shards, B200 = **40 folds, ~$3**.
I46H (delta 0.644) is held in reserve rather than folded, to keep the launch at four.

| bar | threshold | meaning |
|---|---|---|
| **C9-B1** | median margin ≥ **+6.347** | it still holds |
| **C9-B2** | ≥ **+6.971** | the substitution is free, matching the parent |
| **C9-B4** | pKa re-measured **in the complex**, delta ≥ **0.25** | the titration survives the bound state, not just the monomer |
| **C9-B5** | the position stays **>11 Å from the target** in the complex, 5/5 seeds | it is not secretly an interface residue |

**B1 AND B4 AND B5 is the minimum for a pH candidate.** B2 as well would make it a free swap like
L49H was. Free screens first: `express_qc_p2` with pI required below 6.0 — D47H removes an aspartate
and so raises pI more than the others, which is checked before it folds, not after.

🔴 **What stage 7 still cannot establish.** PROPKA says the proton binds in the window; nothing in
this stack says protonation **destabilises** the fold, and the sites that titrate best are the ones
most able to accommodate a charge, so the destabilisation may be small. A pass here means "binds,
folds, and carries a histidine predicted half-protonated mid-assay" — one leg of the mechanism
measured, not two. **No result from this arm may be called a demonstrated pH switch.**
One launch, ~$3, no continuation without a new decision.
