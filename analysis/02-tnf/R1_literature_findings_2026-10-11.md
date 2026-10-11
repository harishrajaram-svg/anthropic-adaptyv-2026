---
type: findings
project: anthropic-adaptyv-2026
arm: R1 — calibration set assembly
prereg: analysis/02-tnf/PREREG-R1-GATE-CALIBRATION-2026-10-11.md
written: 2026-10-11 12:55 PM EDT
status: set assembled from literature; NOT yet scored
---

# R1 set assembly — n = 10 with a structure of the switch itself, so the prereg's pilot fallback fires

## Against the pre-registered bars

The prereg fixed: **n < 20 → report as an underpowered pilot with the exact n and no claim of
calibration.** Molecules with **both** a two-pH measurement **and** a complex structure of the
pH-switch molecule itself: **ten.**

| molecule | target | pH pair | fold | PDB | role |
|---|---|---|--:|---|---|
| SKY59 / crovalimab | C5 | 7.4 / 5.8 | 1,105 | 5B71 | positive |
| eculizumab | C5 | 7.4 / 6.0 | 21 | 5I5K | positive |
| RAY121 | C1r₂s₂ | 7.4 / 6.0 | 120 | 9X1H | positive |
| A01 | α-cobratoxin | 7.4 / 5.5 | 19.7 | 9FYT / 9HUO / 9HXO | positive |
| Ipi.105 | CTLA-4 | 6.0 / 7.4 | 77 | 7SU0 | positive, **opposite direction** |
| Ipi.106 | CTLA-4 | 6.0 / 7.4 | >20 | 7SU1 | positive, opposite direction |
| SNS-101 | VISTA | 5.8 / 7.4 | ~1,000 over range | 8TBQ | positive, opposite direction |
| **D11** | α-cobratoxin | 7.4 / 5.5 | ~1 | 9FYS / 9HUB | **NEGATIVE** |
| **omalizumab** | IgE-Fc | 7.4 / 6.0 | ~1.3 | 5HYS / 5G64 | **NEGATIVE** |
| **bH1-Fab parent** | HER2 | 5.0 / 7.4 | ~4 wrong way | 3BE1 | **NEGATIVE/control** |

**The negative set exists**, which was the live risk. Beyond the three above, measured
pH-independent controls with numbers but no own-structure: NPH-IgG1 (0.9), J16 (1.3), J10 (1.7),
IGKV3-15*01 parent (1.5), ipilimumab parent (1.1), G532Ctrl (0.599). Several are the **wild-type
parent of an engineered switch in the same paper**, which is the best-matched negative available.

## 🔴 The single most valuable row is on OUR target

**Schröter 2015** (mAbs, 10.4161/19420862.2014.985993) reports a histidine-engineered
**anti-TNF-α** series with two-pH **off-rates** and the parent complex structure **3WD5**
(adalimumab Fab + TNF-α):

| | kd at 7.4 | kd at 6.0 | fold |
|---|--:|--:|--:|
| adalimumab (parent) | 0.55e-5 s⁻¹ | 4.81e-5 s⁻¹ | 9 |
| PSV#1 | 3.26e-5 | 754e-5 | 231 |
| PSV#2 | 9.35e-5 | 7340e-5 | 785 |
| PSV#3 | 21.8e-5 | 11000e-5 | 505 |

Measured at exactly **7.4 / 6.0**, the assay pair, on **TNF-α**, with a parent-complex structure.
Testing the gate here is worth more than a broad sweep: same target, same pH pair, a graded series,
and its own parent as the low-fold comparator.

## 🔴 Reasons not to pool these naively

1. **Fold-change is not one quantity.** The set mixes KD ratios, off-rate ratios and one
   range-spanning figure. Acidic arms are 5.0, 5.5, 5.8, 6.0, 6.5, 6.8 and one 7.2-referenced
   neutral arm. **Stratify; do not average.**
2. **Direction is mixed** — four of the ten switch the opposite way (CTLA-4, VISTA), which the
   prereg already required scoring per molecule against its own published direction.
3. **SKY59's switch is substantially ANTIGEN-side** (C5 His70/72/110, with mutants quantified), and
   RAY121 has histidines on both sides. For a binder-side predictor those will look anomalous for a
   real reason, not a failure.
4. **One paper contradicts itself by two orders of magnitude** — ALXN1210 appears as 8,151-fold in
   Table 1 and ~45-fold in Table 3 of the same publication, same variable region. Pick deliberately
   or exclude.
5. **Schröter's picomolar KDs sit at the instrument floor** (authors note adalimumab's 4.6 pM is
   ~10x tighter than published against a ~100 pM BLI limit). **Use the off-rates, not the KDs.**
6. A circulating PDB id is wrong: omalizumab + IgE-Fc is **not** 2XQY (that is a pseudorabies
   glycoprotein H with an unrelated Fab). Use 5HYS / 5G64.

## 🔴 Coverage is incomplete, and three specific gaps would each add a structure-backed row

The search hit paywalls, PMC captchas and a tooling failure partway through, so these are **not
assessed**, merely unreached: **Murtaugh 2011 / 3QSK** (an engineered pH switch in complex with
RNase A — the only such structure in the non-antibody space), **Johnston 2019 / 6MVL** (VISTA
pH-selective Fab, two-pH SPR in Extended Data), and **ARGX-117 / 8ACF + 8ACI** (complex solved at
two different pH values, KD pair not found). Also unreached: Kroetsch 2018, Engler 2018,
Traxlmayr 2014. **The FcRn positive-control slice never completed** and needs re-running; note that
wild-type Fc/FcRn is usually reported as "no detectable binding at pH 7.4", i.e. one-sided.

## Where this leaves R1

Per the prereg, **n = 10 fires the underpowered-pilot fallback: exact n reported, no claim of
calibration.** The bar is not softened. But the Schröter TNF-α series is a better experiment than
the headline bar anticipated — four molecules, one target, the exact assay pH pair, a graded fold
range from 9x to 785x, and a parent structure. If the gate cannot order **that**, it is not
measuring pH response, and that conclusion does not need n = 50.
