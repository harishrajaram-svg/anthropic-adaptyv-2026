---
type: preregistration
project: anthropic-adaptyv-2026
problem: 02-tnf-alpha
arm: H — rebuild the hold while keeping the attributed positions non-titratable
status: PRE-REGISTERED — written 2026-10-11 11:47 AM EDT, BEFORE any redesign runs
cost: ~80 folds, ~$5
---

# Arm H — arm G corrected the direction and lost the hold; recover the hold without giving the
# direction back

Arm G established both halves of a bind. G1/G4: neutralising the gate-attributed binder glutamates
corrects the pH direction, replicated (L49H_E4Q 0.8538, 5 of 5 below 1.0; quadH_E3Q 0.9468, 4 of 5),
and a count-matched control on NON-contributing glutamates does not (1.4968, 0 of 5). G2: the same
residues carry the binding — three arbitrary glutamates cost 0.30 of margin, the three the gate
blames cost **0.91** — so both targeted variants miss +6.3473, by **0.0125** and **0.1225**.

Deleting those residues is therefore the wrong operation. This arm keeps them non-titratable and
asks SolubleMPNN to **rebuild the hold elsewhere on the binder face**. That is now possible because
full-atom predicted complexes exist; CA-only ProteinMPNN could not use soluble weights, which is why
arm S had to skip this step.

## Parents and their bans

Template per parent: the seed whose **complex pLDDT is highest** — a structural criterion, fixed here,
not the gate or the margin, so the template is not chosen on the outcome.

| parent | margin now | gap to +6.3473 | D/E banned at |
|---|--:|--:|---|
| `L49H_E4Q` | +6.3348 | **0.0125** | 7, 10, 20, 28 |
| `quadH_E3Q` | +6.2248 | 0.1225 | 7, 20, 28 |
| `s3_22k4` | +4.5849 | 1.7624 | 6, 56, 61, 69, 82 |

`s3_22k4`'s ban is the **union** of every wrong-direction binder site seen across its 5 seeds, because
its attribution is diffuse — only GLU6 recurs in 5 of 5, against GLU56 at 2 of 5 and GLU61/69/82 at 1
of 5 each. It is carried despite a 1.76 gap because its **target-owned product is below 1.0 in 5 of 5
seeds (median 0.6212)** with ≥2 H73 engaged in all five, which no other molecule here achieves.

Constraints: cysteine banned chain-wide and D/E banned **only at the listed positions** via
`mpnn_constraints.emit(force_his=False, omit_acids=True)` with a narrow `iface` list. This is not arm
A — arm A banned acids at *every* interface position during design and reached 0 of 224 on pose.

16 sequences per parent, 48 designs, 1-seed screen; then 5 seeds plus matched nulls plus monomers on
the best 3 by pose.

## Bars

| bar | threshold | meaning |
|---|---|---|
| **H1** | any design 5-seed margin ≥ **+6.3473** | the hold is rebuilt |
| **H2** | that design's gate median **< 1.0** in ≥4 of 5 seeds | without giving the direction back |
| **H3** | 5-seed monomer pLDDT ≥ **0.70** | it still folds |
| **H4** | post-hoc verification: **no D or E** at any banned position in any accepted sequence | the constraint actually applied |

**H1+H2 together is the only result that matters.** Either alone has already been achieved — arm M
has the margin without the direction, arm G has the direction without the margin.

🔴 **H4 is not decoration.** `--omit_AA_jsonl` loads only if the file exists and otherwise designs
unconstrained while printing a line to stdout, so the constraint is verified on the output sequences,
never assumed from the argument list.

## 🔴 What this cannot do

ESMFold2 is pH-agnostic; an H1+H2 pass is a design with a measured hold and a *replicated predicted
direction*, which is strictly more than anything in the submission and strictly less than a measured
switch. The gate's magnitude remains noise (pooled SD 1.499) and only its sign is reportable.
Objective 2 stays reported as not demonstrated. Nothing here can reach the **Mon Oct 12, 7:59 AM EDT**
close as a validated design.
