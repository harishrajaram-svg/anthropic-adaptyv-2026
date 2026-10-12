---
type: readout
arm: D3 — re-checking the 18 benchmark pH labels (reviewer's ask of 2026-10-11)
status: IN PROGRESS — 14 of 18 rows reported, 3 claims independently re-verified by me
date: 2026-10-12, 10:00 AM EDT
---

# D3 — the benchmark labels, re-checked. The set is in worse shape than the accuracy figure implied.

The reviewer asked for the published ratios in the 18-row calibration set to be re-checked against
their sources, and for each complex to carry its pHs, endpoint, chain assignments and **related
variants**. Four parallel verifications are running; this records what is in and verified so far.
Each was briefed to return **NOT FOUND** rather than reconstruct a number, to quote a source
sentence or named table for every value, and explicitly **not** to adjust toward our recorded figure.

## 🔴 Independently re-verified by me, not taken on a subagent's word

**5HYS — NOT FOUND, and this one removes a row.** I fetched Pennington et al. 2016
(*Nat Commun* 7:11610, PMC4873975) myself. Its SPR runs in **one** buffer; the only other pH values
in the paper are a ficin digestion (6.0), a protein-G wash gradient and an acid elution. **No K_D,
k_on or k_off is reported at two pH values, and the paper contains no pH-dependence analysis of
omalizumab:IgE at all.** Our recorded "1.3×, flat, 7.4/6.0" has no source. The honest status is
**unmeasured, not measured-and-flat** — so 5HYS cannot serve as a non-switch control and comes out
of the set.

**7Q15 — our number is real but attributed to the wrong paper.** I fetched Ulrichts et al. 2018
(*JCI* 128:4372, PMC6159959) myself: *"efgartigimod has equilibrium dissociation constants for human
FcRn of 14.2 nM and 320 nM at pH 6.0 and pH 7.4"* → **22.5×**, and in the Discussion *"the affinity
of efgartigimod at pH 7.3–7.4 is approximately 20-fold lower than that at pH 6.0."* That is where
our 20× came from. It is **not** in 7Q15's own paper (Brinkhaus 2022), whose reported value for the
crystallised species is different.

## Reported by the verifications, corroborated where I could check it

| PDB | verdict | what is wrong, and the correct source |
|---|---|---|
| **5B71** | ✅ MATCH | 1.52e-10 → 1.68e-7 M = **1105×**, K_D by SPR, **in the structure paper itself** (Fukuzawa 2017). Clean. |
| **7SU0** | ✅ MATCH | **77.1×** exact (2.7e-7 / 3.5e-9 M), Lee 2022 Table 1. Clean on value. |
| **6FGB** | ✅ MATCH | **1.34×** (79/59 pM), Fab′ row — format-matched to the deposited chains. Clean. |
| **5TRU** | ✅ value MATCH | 1.1× correct, but the two-pH data is in **Lee 2022 (mAbs)**, not the 5TRU structure paper (Ramagopal 2017 PNAS), which reports no SPR at all. Our endpoint descriptor "8-point pH series" is also wrong: Table 1 is **2-point**, with a ~13-point series in a figure carrying no tabulated numbers. |
| **5I5K** | ✅ value MATCH | **21×** correct (0.033 → 0.69 nM), but from **Sheridan 2018 (PLoS One)** Table 1, not the structure paper. ⚠️ And that paper frames 21× as the **inadequate** baseline its programme existed to fix — *"not expected to dissociate efficiently in the endosome"* — so calling it a "switch" is numerically true and functionally backwards. |
| **4N0U** | 🔴 MIS-ATTRIBUTED | The structure paper (Oganesyan 2014 JBC) reports **no K_D at all** — a single-concentration SPR response comparison at pH 6.0 vs 7.4. Our "170×, switchSENSE, 7.4/5.8" belongs to **Reusch 2024 (mAbs)**: 2.84 nM at pH 5.8 → 494 nM at pH 7.4. Different paper, different technique, different molecular format (full IgG vs the Fc fragment crystallised). |
| **7Q15** | 🔴 MISMATCH | Structure paper's own value is **~37×** (1220 → 33 nM, read from Fig. 1a). Our 20× is Ulrichts 2018's number for the same molecule on a different instrument. Pick one and cite it. |
| **7SU1** | 🔴 MISMATCH IN KIND | The pH 7.4 K_D is **censored**: the paper reports **">5e-7 M"**, so the entry is **">20×", a lower bound**, not a point estimate. Our table stores 20× as a value, which also puts the ordering backwards — the paper's prose makes Ipi.106 the *more* pH-selective of the pair, not the less. |

## 🔴 The independence problem is far worse than we told the reviewer

We reported that the set "rests on 17 independent molecules, not 18" because `4N0U` ~ `7Q15` are
0.990 identical. That understated it in two ways, both now documented from the papers themselves:

- **`5TRU`, `7SU0` and `7SU1` are one antibody lineage from one table in one paper.** 5TRU is
  ipilimumab; 7SU0 (Ipi.105) and 7SU1 (Ipi.106) are engineered pH-selective variants of it, sharing
  five substitutions, with Ipi.106 adding a sixth. All three ratios come from **Lee 2022 Table 1**,
  same assay, same run series. **5TRU is not an independent non-switch control relative to the other
  two — it is their parent, measured in the same experiment by the same group.**
- **`4N0U` and `7Q15` are a parent/variant pair**, differing by H433K/N434F on a shared YTE Fc, and
  7Q15's structure was solved using **4N0U as the molecular-replacement model**. One lineage.

So 18 rows contain at most **14 independent lineages**, and with 5HYS unmeasured, **13 usable**. Of
the five entries in one verification batch, only `6FGB` was independent of all the others.

## What this does and does not change

**It does not rescue or reverse the calibration failure.** Every correction so far is to a
magnitude, a citation, or the independence count — **not one of them flips a direction call**, which
is the quantity the accuracy figure counts. 7Q15 at 37× instead of 20× is still "tighten" and still
a hit; 7SU1 at ">20×" is still "tighten" and still a hit.

**It does make every accuracy figure we have quoted less meaningful than it looked.** A set of 18
rows that is really ~13 independent observations, with one row carrying no measurement at all and
several ratios attributed to papers that do not contain them, cannot support a percentage to two
significant figures. The failure verdict stands; the precision around it does not.

## Batch 3 — the newest entries. All five are published; two more rows lose measured status.

**9MI6 — NOT A MEASURED RATIO, and I verified this one myself.** I fetched Seth et al. 2025
(*mAbs* 17:2461191, PMC11834464). Verbatim: *"Nipocalimab bound with high affinity at both endosomal
and physiologic pH to human FcRn (equilibrium dissociation constant [K_D] **≤31.7 pM**, pH 6.0; K_D
**≤57.8 pM**, pH 7.4, respectively)."* **Both values are upper bounds.** Our 1.8× is the correct
arithmetic on two printed bounds, and a ratio of two bounds carries no information about the true
ratio — both affinities sit below the instrument's quantitation floor. The row's **class is still
right for a better reason**: the paper states *"pH-independent high-binding affinity to FcRn"* and
*"its pH-independent, high-affinity binding."* So keep 9MI6 as a non-switch on the authors' own
statement and drop the 1.8× as a measurement.

| PDB | verdict | what is wrong, and the correct source |
|---|---|---|
| **9X1H** | ✅ MATCH, cleanest in the set | **120.4×** (31.3 nM at pH 6.0 / 0.260 nM at pH 7.4), K_D by SPR at 37 °C, **printed as 120.4 in the paper's own Table 4**, in the structure paper itself. Trap noted and avoided: the same paper prints 71.0, 181.8, 44 and 117 for sibling variants and earlier pH pairs; 117 is close to our 120 but is a different variant at pH 5.8. |
| **8TBQ** | ✅ MATCH | **1009×** (0.35 nM at pH 5.8 / 353 nM at pH 7.4), K_D by SPR, in the structure paper. Our descriptor "reported as a range not a point" is **wrong and in our favour** — the two endpoints are point values; the paper's "0.35–5.9 nM" range describes the pH 5.8–6.4 span, a different statement. |
| **9S60** | 🔴 METHOD WRONG — **my error** | Ratio **1.65×** correct and class correct, but the endpoint is **SPR on a Biacore T200, not ITC.** I recorded "K_D (ITC)" in the endpoint audit. The verification reports zero occurrences of "ITC", "isothermal" or "calorimet" anywhere in the article XML; the paper's orthogonal methods are SEC, nano-DSF, CETSA and enzyme inhibition. Also worth noting the direction: 1.65× **tighter** at acidic pH, not weaker. |
| **8J6F** | 🔴 NOT FOUND | The structure paper (Wang 2024, *Cell Rep*) is **not reachable** — 403 at the publisher, no PMC copy, no repository PDF — so abstract only, and the abstract never mentions pH. **Our 2.2× is unverified: neither confirmed nor refuted.** The likely true source is a different, closed-access paper (Igawa 2010, *Nat Biotechnol*, PMID 20953198), which is about engineering tocilizumab for pH-dependent release and whose abstract names the 7.4/6.0 pair — but no number was read from it. |

## Where the set stands with 14 of 18 verified

| status | rows |
|---|---|
| ✅ clean — value correct AND measured in the structure paper | `5B71`, `6FGB`, `7SU0`, `8TBQ`, `9X1H` |
| ⚠️ value correct but the measurement lives in a **different** paper | `5TRU`, `5I5K`, `4N0U`, (`7Q15`) |
| 🔴 value wrong | `7Q15` (37× in its own paper, not 20×), `7SU1` (a censored bound, not 20×) |
| 🔴 not a measured ratio | `9MI6` (ratio of two upper bounds) |
| 🔴 no retrievable measurement | `5HYS` (none exists), `8J6F` (paper unreachable) |
| 🔴 endpoint method wrong in our record | `9S60` (SPR, not ITC) |
| pending | `1BRS`, `3SQO`, `3WD5`, `4K71` |

**Five of fourteen are clean.** The arithmetic is deliberately **not** recomputed until all 18 are
in, so it is recomputed once rather than drifting row by row.
