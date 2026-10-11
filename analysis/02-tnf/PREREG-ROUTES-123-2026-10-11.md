---
type: preregistration
project: anthropic-adaptyv-2026
problem: 02-tnf-alpha
arm: S (seam), M (marginal scaffold), E (charge steering)
status: PRE-REGISTERED — written 2026-10-11 9:21 AM EDT, BEFORE any of the three runs
---

# Routes 1-3, all three, bars fixed first

Context: `analysis/02-tnf/F1_three_untried_routes_2026-10-11.md`. Objective 2 is closed ten ways,
all ten through one instrument — the binding-coupled gate — whose seed SD (1.499) exceeds its
effect and whose binder-side signs do not reproduce for a fixed sequence (His61 flips 3-wrong /
2-right over five refolds of one molecule, R1). The single quantity that replicates is **target H73
helping, 5 of 5 refolds, median 0.7986x over 829 poses.**

## Arm S — seam-spanning design: engage H73 on TWO protomers

**0 of 1,200 poses in the E1 pool engage more than one H73.** Geometry permits it: H73–H73 is
21.58 / 22.02 / 22.07 Å CA–CA, the 83-mer spans 35.3 Å, and Glu146 — the dominant opposing term,
863 of 1,200 poses, median 1.781x, E4 p = 8.5e-46 — lies 20.1–20.6 Å off that axis.

New conditioning strategies added to `bin/build_genie3_problem.py` (selftest **10/10**, M6 pins that
`seam2`/`seam3` name His73 and nothing else, on 2 and 3 distinct protomers):

    seam2 -> A73 + C73        seam3 -> A73 + B73 + C73

| bar | threshold | meaning |
|---|---|---|
| **S1** | any design `ca_sc_dockq` ≥ **0.60** | a seam-spanning pose holds at all |
| **S2** | ≥1 design engages **≥2 H73** in the gate's contributing set | the premise is actually realised |
| **S3** | that design's **5-seed** gate median **< 1.0**, ≥4 of 5 seeds | and it points the right way, replicated |
| **S4** | 5-seed human margin ≥ **+6.3473** | and it binds |

**S2 is the bar that matters most**, because it is the one thing never achieved. S1 without S2 means
the generator ignored the conditioning and the arm says nothing about this route. S3 is scored on
**5 seeds from the start**, never on the selection seed alone — that is the error R1 caught.

🔴 Expected failure mode, declared: every good pose this project has produced lies on one protomer
face. A 22 Å seam-spanning pose is a harder docking problem and S1 may fail the way arm A's acid-ban
did (0 of 224). The premise is sound; the pose is the gamble.

## Arm M — marginal scaffold: four buried histidines, fold linkage not binding linkage

C9e measured His pKa on monomers at 20 positions, 5 seeds, pLDDT 0.84–0.91, and classed each by
*binding* linkage. Re-read as **folding** linkage (folded pKa against His's intrinsic 6.5 unfolded),
the four it discarded as "inert" are the four best low-pH destabilisers: V45H 4.26 (+0.77 kcal/mol),
L63H 4.30 (+0.76), L53H 4.58 (+0.75), L64H 5.03 (+0.72) — **+3.00 summed**, against **+0.13** for the
gate's best reproducible interface term. Identities verified against
`depth12_canonical_sequences_2026-10-09.tsv`: positions 45/53/63/64 of `3_L0r4k0` are V/L/L/L.
(The C9e TSV's `native` column reads L at 45 and is wrong there; the canonical sequence governs.)

Construct: **`3_L0r4k0` + V45H + L53H + L63H + L64H**, a quadruple never folded — C9e measured these
one at a time.

| bar | threshold | meaning |
|---|---|---|
| **M1** | 5-seed monomer pLDDT ≥ **0.70** | the quad still folds |
| **M2** | summed fold-destabilisation ≥ **+2.00 kcal/mol** from PROPKA on the QUAD monomer | the four pKa depressions survive being combined |
| **M3** | 5-seed complex margin ≥ **+6.3473** | it still binds |

**M2 is the real question**: four buried histidines in one core will interact, and additivity is an
assumption, not a measurement. M1 and M3 are the costs this route has to pay.

🔴 Declared tension: this route wants a **marginal** scaffold, which is the opposite of the monomer
floor enforced all week (C1: 12 of 12 at 0.885–0.910). A pass on M1 at high pLDDT would mean the quad
is still too stable for +3 kcal/mol to matter — so **M1 passing is not unambiguously good news**, and
that is recorded here rather than rationalised later.

🔴 ESMFold2 is pH-agnostic and cannot show unfolding. M2 is a thermodynamic prediction. No pH switch
is demonstrated by any outcome of this arm.

## Arm E — long-range charge steering

Net-charge repulsion is not proton linkage, and the gate cannot see it. Screen: Henderson-Hasselbalch
net charge of the target surface patch within **12 Å** of the H73-pair midpoint, at pH **7.4 and
6.0**, with the Glu146-centred patch as the contrast, using **model pKa values** (Asp 3.9, Glu 4.3,
His 6.5, Cys 8.4, Tyr 10.5, Lys 10.5, Arg 12.5) — declared as a screen, not a calculation.

| bar | threshold | meaning |
|---|---|---|
| **E1c** | seam patch net charge **> 0** at both pH | an electropositive epitope, so a binder gaining + charge is steered OFF — route live |
| **E2c** | seam patch more positive than the Glu146 patch | the seam is the right place to try it |

**E1c failing kills route 3 immediately**, which is the point of running a free screen first.
`bin/dddg_elec.py` (the organisers' named filter, PyRosetta in scope per their 2026-10-06 message)
is a **contact** pair-sum, not long-range steering, so it is run as a secondary read and not as E1c.

## Costs

| arm | compute | cost |
|---|---|---|
| **E** | local, no folds | **$0** |
| **M** | 5 monomer + 5 complex + 5 null = 15 folds | **~$0.70** |
| **S** | Genie 3 generation + MPNN + ESMFold screening, fused | **~$30–40** |

## 🔴 What none of this can do

Nothing here lands a submittable design before **Mon Oct 12, 7:59 AM EDT**. Objective 2 is reported
as not demonstrated regardless of outcome. A full S1–S4 pass would be a design with a measured hold
and a *replicated predicted direction* — strictly more than anything in the submission, strictly
less than a measured switch.

---

# AMENDMENT 1 — the quad's mouse leg, and the substitution rule, 2026-10-11 10:55 AM EDT

Written BEFORE the mouse folds launch and before any mouse number exists.

Arm M passed M1/M2/M3 and the quad `3_L0r4k0_quadH` cleared the liability screen (**pI 5.2**, clear of
the 6.0–7.4 assay window; its single flag is 28% glutamate, carried identically by its parent and by
the already-shipping `3_L4r5k2`). It is therefore a shipping candidate, which M1–M3 were not written
to decide.

**It cannot ship alongside its parent.** `3_L0r4k0_quadH` against `3_L0r4k0` is **79/83 = 0.9518
identity**, over the organisers' `batch_duplicate` threshold of 0.95. The choice is substitution, not
addition.

`3_L0r4k0`'s strongest feature is its MOUSE margin (+7.581 against its human +6.967). The quad has
never been folded against mouse, so the substitution is currently undecidable. 2 inputs x 5 seeds =
**10 folds, ~$0.45**.

| bar | threshold | meaning |
|---|---|---|
| **M4** | 5-seed mouse margin ≥ **+6.3473** | the quad engages mouse at all |

## Substitution rule, fixed now

Objective 3 is cross-reactivity, so the governing quantity is the **worse of the two species**, and
the parent's is **+6.967** (human 6.967, mouse 7.581).

- **Substitute the quad for `3_L0r4k0`** iff `min(human, mouse)` for the quad **> +6.967**, which
  given the quad's measured human +7.1306 means **mouse > +6.967**.
- **Otherwise keep `3_L0r4k0`** and the quad does not ship, whatever its pH properties, because a
  worse cross-species binder is not improved by a pH story this project cannot measure.

🔴 Note the asymmetry against the depth-arm selector argument, and that it is deliberate: the
worse-of-two was the wrong **design selector** (arm B, LESSONS §§9-12) because it discarded human
gains during optimisation. It is the right **shipping gate** because the assay measures both species
and objective 3 asks for both. Selecting and shipping are different decisions.

🔴 The quad's pH claim is unchanged by any mouse number: +3.064 kcal/mol is a predicted fold
destabilisation and ESMFold2 is pH-agnostic. The +1.96 e charge gain across the window (−7.30 →
−4.43, against the parent's +1.06 e) is a property of the sequence, not evidence of release.

---

# AMENDMENT 2 — Amendment 1's substitution rule optimised the wrong quantity, 2026-10-11 11:20 AM EDT

**Amendment 1's rule should not be acted on, and this is why.**

It said: substitute `3_L0r4k0_quadH` for `3_L0r4k0` iff the quad's worse-of-two exceeds +6.9670. The
quad's mouse came back +7.1851, worse-of-two +7.1306, and the rule fired.

**But `3_L0r4k0` is not in the submission on its margin.** It is the **matched control** for row 1,
`3_L0r4k0_L49H` — the two are one residue apart, 98.8% identical, and the methodology box states
plainly that *"the pair IS the experiment, and submitting only the variant would leave any
pH-dependent result with no in-assay control — the exact trap we fell into on problem 1, where a
1.432x ratio looked like a switch until matched arms pinning a non-titratable residue switched at
the same rate (4% vs 6%, p = 0.53)."*

Substituting the quad for it would delete that control and reintroduce that trap. Amendment 1 ranked
a control slot on affinity, which is a category error: **the control's job is to be identical except
at one position, not to bind well.** The margin comparison it ran was real and the numbers stand;
the decision it licensed does not.

Correct framing, for the human to decide rather than a rule to fire: the quad is a **third member of
the same scaffold family** — `3_L0r4k0` (0 buried His), `3_L0r4k0_L49H` (1), `3_L0r4k0_quadH` (4).
Shipping all three converts a matched pair into a **buried-histidine titration series with a shared
control**, which is a stronger experiment than the pair. It costs 4 of 20 slots and a **second**
`batch_duplicate` flag against the same control (quad vs parent is 0.9518).

Nothing is substituted or dropped on the strength of Amendment 1. The quad's bars M1-M4 all passed
and that record is unchanged.
