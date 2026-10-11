---
type: readout
project: anthropic-adaptyv-2026
problem: 02-tnf-alpha
arm: T — dG_fold of the binder monomer, the fold route's deciding quantity
prereg: analysis/02-tnf/PREREG-T-DGFOLD-2026-10-11.md
written: 2026-10-11
cost: $0.00, 0 GPU folds. CPU only.
---

# Arm T readout — the quad is not a 10 kcal/mol scaffold, and the route's ceiling at pH 6.0 is ~6x

Arm M said the fold route rested on **+3.064 kcal/mol against an unknown dG_fold** and that nothing
on hand measured the denominator. PyRosetta-4 2026.39 is in `.venv` and `cartesian_ddg` and pH mode
had never been run. Both were run. Nothing here touches the binding-coupled gate R1 condemned.

## Bars, and what happened to each

| bar | pre-declared | result |
|---|---|---|
| **T2 neg** | exposed conservative, \|ddG\| <= 1.0 | **PASS** — K17R +0.83 (SASA 191.7), E51Q +0.28 (SASA 146.1) |
| **T2 pos** | buried hydrophobic -> Ala, ddG >= +1.5 | **PASS** — L32A +4.89, F29A +7.13, V45A +5.71 |
| **T3** | forward and reverse agree within 2.0 | **🔴 FAIL — they disagree by 16.4 kcal/mol** |
| **T1** | dG_unfold band | **ALIVE on the bound, point value marked untrustworthy per T3** |

## 🔴 T3 failed, so read the sign and the bound, not the number

Three independent framings of the same quantity, ddG_fold(parent -> `quadH`):

| framing | ddG | SD | additivity vs the four singles |
|---|--:|--:|--:|
| forward, parent backbone, frozen outer shell | **+23.48** | 1.56 | 75.2% |
| full-pose FastRelax, each sequence on its own ESMFold backbone | **+14.76** | 7.40 | — |
| reverse, quad's own backbone, frozen outer shell | **+7.05** | 1.53 | **97.5%** |

Shell-matched WT-vs-WT nulls (self-mutations, identical shell and path) put the noise floor at
−0.49 ± 0.77 for the 42-residue quad shell, so none of this is packing noise. The first unmatched
null I ran came back +0.83 ± 1.38 and was wrong: it used the shell around residue 1, not the shell
under test. The matched nulls are the honest floor and they are at zero.

The reverse framing is the trustworthy one and the additivity column is why: on the quad's own
backbone the four reversions sum to −7.23 against a measured −7.05, **97.5% additive**, while the
forward direction is 75.2% additive. The forward number is a frozen-backbone artifact — it mutates
Val and Leu to His on a backbone never built to hold them and cannot relieve the clash.

**What survives the T3 failure is the sign and a one-sided bound, and those are what T1 needs.**
dG_unfold(quad) = dG_unfold(parent) − cost. For the quad to land in the pre-declared **COSMETIC**
band (dG_unfold > 6.00) the parent would need dG_unfold > **13.05 kcal/mol** even on the friendliest
cost of the three. No 83-residue, disulfide-free single domain in the literature reaches that —
ubiquitin 7.2, CI2 7.0, protein G B1 6.6, barnase 8.8, and Rocklin 2017's designed miniproteins top
out near 5 by proteolysis. **The route is not cosmetic. Arm M's open question is closed in the
route's favour.**

## 🔴 But the answer to "is it marginal ENOUGH" is that it is marginal TOO MUCH

The pre-registered linkage arithmetic gives a usable band of **1.32 kcal/mol** wide:
dG_unfold >= 1.74 to stay 95% folded at pH 7.4 (the objective's *hold*), and <= 3.06 to buy 2x at
+3.064 (the objective's *release*). The instruments disagree by 16.4. Nothing we have can aim into
a 1.32 kcal/mol window.

Scoring all 15 subsets of the quad's four histidines on the numbers measured today — reverse-frame
cost per position, arm M's PROPKA DD per position — subject to staying >=90% folded at pH 7.4:

| parent dG_unfold | best subset | switch | folded at 7.4 | full quad |
|--:|---|--:|--:|--:|
| 6.0 | H53/H63/H64 | 1.08x | 0.998 | disqualified |
| 7.0 | H53/H63/H64 | 1.01x | 1.000 | disqualified |
| 8.0 | H45/H63/H64 | 1.99x | 0.979 | disqualified |
| 9.0 | H45/H63/H64 | 1.19x | 0.996 | disqualified |
| **10.0** | **all four** | **6.11x** | 0.971 | 6.10x |
| 11.0 | all four | 1.97x | 0.994 | 1.97x |

**The shipped `quadH` fails the pH 7.4 hold for every parent stability below 10 kcal/mol**, and the
best switch available anywhere in the table is **6.11x, at exactly one parent value.** The winning
subset changes three times across the range. A 3 kcal/mol uncertainty in a number nothing measures
inverts the design choice.

## The per-position decomposition, which is the transferable part

Reverse frame, on the backbone that actually holds each histidine:

| pos | cost to carry the His (kcal/mol) | DD at pH 6.0 (PROPKA) | DD per kcal spent |
|---|--:|--:|--:|
| **H45** | **+5.72** | 0.775 | **0.14** |
| H53 | +2.21 | 0.762 | 0.35 |
| H63 | −0.63 (free) | 0.772 | — |
| H64 | −0.07 (free) | 0.756 | — |

**H45 alone is 81% of the quad's stability bill for 25% of its pH response.** H63 and H64 cost
nothing at pH 7.4 while PROPKA puts their pKa at 3.79 and 4.55 — which is not a contradiction but
the ideal case: the neutral tautomer is comfortable, the cation is not. Two instruments agree on
which residue carries the strain, since H45 is also the pKa 2.43 outlier arm M flagged as its single
most questionable number.

This separates two knobs arm M conflated. **Marginality and pH response are independent, and
histidines are a bad way to buy marginality** — H45 pays 7.4 kcal/mol per kcal of DD. The selection
axis is DD per kcal of stability spent, and it is computable for free in the reverse frame wherever
a mutant fold exists.

## 🔴 Rosetta pH mode is tested and it is inert — item D closes

| | pH 7.4 | pH 6.0 | delta |
|---|--:|--:|--:|
| `quadH` total | −232.968 | −233.820 | −0.852 |
| parent total (**zero histidines**) | −264.394 | −263.895 | **+0.499** |

pH mode initialises, and the packer does offer `HIS`/`HIS_D`/`HIS_P` at position 45. But
**`e_pH` carries weight 0.0 in ref2015**, and the protonation assignment is byte-identical at both
pH values (`45 HIS, 53 HIS_D, 63 HIS_D, 64 HIS_P`). The parent has no titratable histidine and still
moves 0.499 REU between pH values, which is impossible physics — so **pH mode fails its own null**
and the quad's 0.852 is the same noise. It cannot check arm M's +3.064 and nothing should be selected
on it. One side finding: Rosetta's packer puts H64 in the **protonated** state even at pH 7.4, which
contradicts PROPKA's pKa 4.55 for that position.

## What held up

ESMFold did keep the histidines buried — side-chain SASA H45 0.5, H53 13.2, H63 1.3, H64 29.5 Å²
against V45 0.0, L53 7.9, L63 1.0, L64 21.9 in the parent — and the fold did not move, CA RMSD
**0.641 Å** over 83 residues. The buried-histidine premise is intact. That ESMFold absorbed four
buried histidines with 0.64 Å of backbone change while Rosetta charges 7–23 kcal/mol for them is the
third instrument disagreement in this readout, and it is unresolved.

## What this does not establish

**No absolute dG_unfold was measured, because nothing on hand measures one.** Every number here is a
difference between two sequences. The literature ceiling used for the bound is literature, not an
instrument, and the ~10 kcal/mol figure is generous rather than typical. The switch column is
two-state linkage, which assumes only the folded binder binds and that acidification acts solely
through global unfolding; Ahn 2025's 79x at pH 5.4 on a binder that is still 7 nM at pH 7.4 is not
compatible with that assumption, so their mechanism is probably local rather than global and this
model may understate what is reachable.

## Spend

**$0.00. Zero GPU folds against a 150-fold cap.** PyRosetta on CPU: 12 forward rows, 10 matched-null
rows, 6 reverse rows, 10 full-pose relaxes, 4 pH-mode packs. Wall time under 15 minutes.

## Artifacts

- `bin/ddg_cartesian.py` (self-test passes; two footguns documented in its docstring)
- `analysis/02-tnf/T_ddg_forward.json`, `T_ddg_null.json`, `T_ddg_reverse.json`
- `analysis/02-tnf/T_linkage.py`, `analysis/02-tnf/T_scratch/` (10 converted monomer PDBs, specs)
