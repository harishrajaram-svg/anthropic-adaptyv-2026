---
type: readout
arm: D3 — re-checking the 18 benchmark pH labels (reviewer's ask of 2026-10-11)
status: IN PROGRESS — 9 of 18 rows reported, 2 claims independently re-verified by me
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

**Pending:** `1BRS`, `3SQO`, `3WD5`, `4K71` and `8J6F`, `8TBQ`, `9MI6`, `9S60`, `9X1H`. The 9-series
entries are recent and may come back deposited-but-unpublished, which would itself be a finding
about how the set was built. The arithmetic is deliberately **not** recomputed until all 18 are in,
so it is recomputed once rather than drifting row by row.
