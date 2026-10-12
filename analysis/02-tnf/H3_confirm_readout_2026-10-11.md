---
type: readout
project: anthropic-adaptyv-2026
problem: 02-tnf-alpha
arm: R3b — confirmation of the pinned candidates
written: 2026-10-11 12:38 PM EDT
cost: 30 folds, ~$1.40
---

# R3b — `quadH_E3Q_k14` passes all three bars AND keeps the fold mechanism; the seam line is dead

| design | H1 margin ≥ +6.3473 | H2 gate < 1.0, ≥4/5 | H3 pLDDT ≥ 0.70 | His kept |
|---|---|---|---|---|
| **`quadH_E3Q_k14`** | **PASS +6.7049** (SD 0.293) | **PASS 0.8233, 5 of 5** | **PASS 0.8396** | **4 (45/53/63/64)** |
| `s3_22k4_k3` | **FAIL +5.2112** (SD 2.685) | **FAIL 1.5811, 1 of 5** | **FAIL 0.6997** | 0 |

Per-seed gate: k14 — 0.772, 0.803, 0.823, 0.856, 0.967. `s3_22k4_k3` — 0.517, 1.543, 1.581, 2.841,
**38.932**.

## The seam line is finished

`s3_22k4_k3` had the best screen numbers in R3 (pae 7.759, gate 0.574) and fails every bar on
confirmation: margin 5.21 with **SD 2.685**, a gate that swings from 0.517 to 38.9 across five
refolds of one sequence, and a monomer that does not clear the fold floor at 0.6997. The screen's
single-seed PAE flattered it. Three rounds — arm S, R3, R3b — and the seam epitope never produced a design that holds.

🔴 **Reframed 2026-10-11 on reviewer feedback: UNRESOLVED, not closed.** Conditioning demonstrably moved the geometry onto the seam (11 of 40 backbones reached ≥2 His73 against 2 of 50 controls, p = 1.9e-3). What failed is a *computational* binding criterion, which does not establish that the seam cannot bind. Revisiting it properly would need a small matched seam-versus-control comparison at the same generation budget and folding criteria, the intended contacts checked with **both** predictors, and a continuation criterion fixed in advance — and it ranks below the corrected depth-arm evaluation.

## Two designs now pass H1+H2+H3, and they trade against each other

| | margin | gate median | His | fold mechanism |
|---|--:|--:|--:|---|
| `quadH_E3Q_k12` | **+7.1968** | 0.8710, 5/5 | **0** | **gone** |
| `quadH_E3Q_k14` | +6.7049 | **0.8233**, 5/5 | **4** | **+3.064 kcal/mol intact** |

k14 pays **0.49 of margin** to keep all four buried histidines, and buys a slightly better direction
with it. That is the whole trade and it is a judgement call, not a bar.

🔴 The screen's PAE proxy over-promised on k14: 7.900 against k12's 7.769 suggested near parity, and
the confirmed margins differ by 0.49. **Single-seed interface PAE orders candidates; it does not
measure the margin.** Noted because R3's ranking rested on it.

## 🔴 What still bounds both

**His contributing = 0** in all five seeds of k14, as R3 established four other ways. So k14's
predicted pH **direction** comes from target H73 and Glu146, and its four histidines serve a
**separate** fold-destabilisation mechanism this gate cannot see. Two mechanisms in one molecule,
one visible to this instrument and **neither calibrated** — the 5.8%-vs-5.6% shuffled-null result
stands, and R1 is what settles it.

Neither passing design has a **mouse margin, liability screen or dedup check** yet. 20 folds (~$1)
plus two local screens closes that, and it is required before either can ship.
