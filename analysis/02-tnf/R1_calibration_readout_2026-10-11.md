---
type: readout
project: anthropic-adaptyv-2026
arm: R1 — gate calibration against published pH switches
prereg: analysis/02-tnf/PREREG-R1-GATE-CALIBRATION-2026-10-11.md
written: 2026-10-11 1:20 PM EDT
cost: ~$0
---

# R1 — the gate FAILS calibration, and it gets our own target's sign backwards

16 published complexes, 9 measured switches and 7 measured non-switches, each scored at problem 2's
pH pair with its own chain assignment and with its **published direction recorded before scoring**.

| bar | threshold | result |
|---|---|---|
| **K1** | positives separate from negatives, p < 0.05 | **FAIL — p = 0.1332** |
| **K2** | sensitivity ≥ 0.60 at specificity ≥ 0.70 | **FAIL — direction correct in 8 of 16 = 50%** |
| **K3** | shuffles below true negatives | not reached; K1/K2 settle it |

**50% on a two-way sign call is chance.** Positives' median |log₁₀ ratio| is 0.805 against the
negatives' 0.661 — the two classes are not separated.

## 🔴 The single most damning row is our own target

| | published | gate |
|---|---|---|
| **`3WD5` adalimumab / TNF-α** | **9× WEAKER at pH 6.0** (off-rate, 7.4 vs 6.0 — the exact assay pair) | **3.2715, the TIGHTEN direction** |

The gate calls the sign **backwards** on the one molecule in the world where we have both a measured
two-pH number *and* our own target. Its authors attribute that 9× to CDR-H1 His35, CDR-H2 His56 and
**TNF-α His73** — the residue our gate independently identifies as the only helping target site. It
finds the right residue and then gets the direction wrong.

## The full table

| pdb | class | want | published | gate | call |
|---|---|---|--:|--:|---|
| 5B71 | pos | release | 1105× | **0.0145** | hit |
| 9X1H | pos | release | 120× | 0.9438 | hit |
| **3WD5** | pos | release | **9×** | **3.2715** | **miss** |
| 5I5K | pos | release | 21× | 3.2917 | miss |
| 1BRS | pos | release | ~1200× | 3.8334 | miss |
| 4K71 | pos | tighten | 760× | **6873.09** | hit |
| 7SU0 | pos | tighten | 77× | 140.32 | hit |
| 7SU1 | pos | tighten | 20× | 6.3872 | hit |
| 8TBQ | pos | tighten | 1000× | **0.1045** | miss |
| 5HYS | neg | flat | 1.31× | **1.0000** | hit |
| 5TRU | neg | flat | 1.1× | 1.1734 | hit |
| 9MI6 | neg | flat | 1.8× | 1.9220 | hit |
| 9S60 | neg | flat | 1.65× | 5.4442 | miss |
| 6FGB | neg | flat | 1.34× | 4.5803 | miss |
| 3SQO | neg | flat | 1.3× | 8.1101 | miss |
| **8J6F** | neg | flat | **2.2×** | **45.4182** | **miss** |

Negatives measured between 1.1× and 2.2× come back anywhere from **1.00 to 45.4**. Tocilizumab is
measured at 2.2× and the gate returns **45.4×**.

## What this settles, and what it does not

**Pre-registered consequence, unchanged:** K1/K2 failing means **objective 2 keeps today's wording —
a predicted direction, uncalibrated.** That was fixed in advance precisely so this outcome could not
be rationalised.

**It also goes further than "not demonstrated."** The point estimate sits **at chance**, which is
positive evidence of no signal rather than an absence of evidence. It corroborates the internal
result exactly: 5.8% of our designs clear the gate against 5.6% of composition-matched shuffles.
Two independent routes, one internal and one external, agree the quantity does not discriminate.

🔴 **n = 16, so this is the underpowered pilot the prereg declared, and I am not claiming the gate is
proven broken.** A 50% sign rate on 16 molecules is also consistent with modest true accuracy. What
it does establish is that there is **no evidence FOR the gate**, and that is enough to decide how to
report.

## Consequence for every pH claim in this project

**`quadH_E3Q_k12`'s "below 1.0 in 5 of 5 seeds" must stop being presented as evidence of pH
selectivity.** Seed replication shows a reading is *reproducible*; this arm shows the reading does
not track measured pH behaviour. The same applies to arm G's corrected direction, arm H's passes,
and E1's 214 poses. They remain real measurements **of the gate** and say nothing established about
pH.

Honest summary of the day's pH work: we built a binding-coupled protonation calculation, localised
its output to specific residues, corrected its sign deliberately and reproducibly — and then
discovered the instrument does not predict the thing it was built to predict. The design work stands
as binder design. The pH objective does not.

---

# ADDENDUM, 1:35 PM EDT - n = 18, and the diagnosis sharpens

The FcRn slice added two structure-backed positives with the engineered Fc in the structure itself:
4N0U (IgG1 Fc YTE / FcRn, 170x, ternary with HSA stripped since the measurement did not involve
albumin) and 7Q15 (efgartigimod MST-HN Fc / FcRn, 20x). Both tighten-direction, both called
correctly (12.54 and 2.73).

| | n = 16 | n = 18 |
|---|--:|--:|
| pooled direction accuracy | 8/16 = 50% | 10/18 = 56% |
| K1 Mann-Whitney p | 0.1332 | 0.1288 - still FAIL |

**The rise is a selection effect, not an improvement.** Both additions sit in the one direction the
gate already handled well.

| declared | n | correct |
|---|--:|--:|
| tighten | 6 | 5 |
| release | 5 | 2 |
| flat | 7 | 3 |

## The real diagnosis: a prior, not an accuracy

**The gate returns a ratio above 1.0 for 14 of 18 structures - 78% - median 3.56.** It does not
discriminate; it predicts tightening almost regardless of input. That explains every stratum at
once: 5/6 where tightening is real, 2/5 and 3/7 where it is not.

A constant predictor always answering ">1" scores 6/18 = 33%. The gate scores 10/18 = 56%, i.e.
**four molecules better than answering the same thing every time.** That is what it actually adds.

It also explains the internal null that prompted R1: if the output is mostly >1, then on problem 2 -
which needs < 1 - only the tail ever qualifies, and a composition-matched shuffle lands in that tail
as often as a design. **5.8% against 5.6% was this same prior seen from the inside.**

## Corrections the FcRn slice supplied

- **No structure exists of wild-type human IgG1 Fc with human FcRn.** A UniProt join
  (P55899 n P01857) returns only 4N0U and 7Q15, both engineered; the only wild-type Fc-FcRn
  complexes are rat (1I1A, 1FRT). Wild-type IgG cannot be a negative here.
- **Every wild-type neutral-pH value in this literature is censored** - >10,000 nM, ND, NB, NA,
  >60 uM across six studies, never a number. Left-censored detection limits; affinity maturation is
  what lifts neutral-pH binding into range. Reading any as a value would inflate selectivity.
- **Absolute KD is not transferable across platforms**: YTE at acidic pH spans 215 nM (SPR) to
  3.09 nM (switchSENSE), ~70x for one mutation. Only within-paper, within-format fold-changes
  compare - which is how this set was built.
- **Avidity is a 7-11x factor and itself pH-dependent**: YTE reads KD,affinity 3.09 nM against
  KD,avidity 0.29 nM at pH 6.0, with avidity abolished at pH 7.4.
- 5BJZ is maltose binding protein, unrelated to FcRn. 6FGB is FcRn + a Fab, which is exactly how
  this set used it, so nothing to correct there.

## Verdict

Unchanged, and better explained. K1 still fails. The instrument carries a directional prior rather
than discriminating power, so no pH claim in this submission rests on it.
