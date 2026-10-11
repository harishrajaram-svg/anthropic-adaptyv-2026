---
type: preregistration
project: anthropic-adaptyv-2026
problem: 02-tnf-alpha
arm: A3 pH series
status: PRE-REGISTERED — written 2026-10-10 11:55 PM EDT, BEFORE any A3 fold exists
---

# A3 — can a releasing histidine be installed on `40_L1r4k1` without losing the hold?

## Why this arm exists

Objective 2 (pH switching) is closed at zero: of the 12 depth-arm designs, **0 have the release
direction available, 7 have it INVERTED** and 5 carry no histidine. The inversion is specific and
geometric — His61 sits 2.18–2.49 Å from a target **carboxylate** against 4.73–5.63 Å to LYS65, so
protonation at pH 6.0 *tightens* the grip. That is problem 1's error repeated.

`bin/his_releasing_positions.py` scanned the leader's own fold for positions where a protonated
His⁺ would instead meet a target **cation** (repulsion → release). It found **5 candidates**:
E62 (d_cation 2.30 Å), D50 (5.05), R27 (5.06), L58 (6.36), T54 (6.97).

Objective 2 is the **first**-ranked judging criterion (affinity is third), and the organisers state
a weak but clearly pH-sensitive binder may outrank a high-affinity one that is not pH-sensitive.
A documented zero on the first criterion is worth ~$6 to attack.

## 🔴 What this arm CANNOT do — declared in advance

**ESMFold2 is pH-agnostic. A3 does not measure pH response.** It can show only (a) that the
substitution is tolerated at the pH-7.4 hold, and (b) that the installed His lands near a cation
rather than a carboxylate in the variant's **own** predicted pose. **No A3 result may be described
as a demonstrated pH switch**, in the methods document or anywhere else. The geometric call is a
hypothesis about pH 6.0, not a measurement of it.

## The design, and the fix applied before launch

As first staged (8:41 PM) the arm was **5 singles that all retained His61** — one releasing His and
one tightening His per molecule. A flat result would have been uninterpretable: it could not
separate "the releasing His did nothing" from "His61 cancelled it." Added before launch:

| set | n | His | what it isolates |
|---|--:|--:|---|
| `relXH` singles | 5 | 2 | releasing His installed, tightening His61 **retained** |
| `relXH_H61Q` doubles | 5 | 1 | releasing His **alone** — the clean test |
| `ctrlH61Q` | 1 | 0 | cost of removing His61 by itself, no releasing His |

11 designs + 11 composition-matched nulls = **22 complexes**, 5 seeds = **110 folds**, 6 shards.
Nulls are a `random.Random(20261006)` shuffle of the binder chain, target untouched — the same
convention and seed as `bin/build_sizematched_null.py`. **Control passed before staging:** the
procedure reproduced the already-staged singles and their nulls byte-for-byte.

## Bars — fixed now, not after the numbers land

Readout is the 5-seed **median** margin against each design's own matched null (seed-max flatters,
§30), plus `bin/his_geometry_verdict.py` re-run on each variant's own fold.

| bar | threshold | meaning |
|---|---|---|
| **A3-B1** hold retained | median margin ≥ **+6.347** | the measured non-binder median, this project's floor |
| **A3-B2** slot candidate | median margin ≥ **+7.8144** | the measured binder median, the bar `40_L1r4k1` itself clears at +8.031 |
| **A3-B3** geometry | installed His reads `RELEASING` (d_cation < d_acid) in ≥ **3 of 5** seeds | the mechanism is actually installed in the pose |

**A3-B2 + A3-B3 together** is the only combination that makes a variant a candidate to take a
submission slot. B1 + B3 without B2 is a real result and a reportable one, but it trades
first-criterion coverage for third-criterion strength and that trade is **Harish's call, not mine.**

## Controls that decide whether the arm is readable at all

- **C1 — `ctrlH61Q` below +6.347** ⇒ His61 is load-bearing for *binding*, and the releasing-His
  program on this backbone is dead whatever the doubles do. Report and stop.
- **C2 — singles vs doubles.** If doubles clear a bar their matched singles fail, His61 was
  cancelling the releasing His and the single-mutant arm was mis-designed. If both fail equally,
  the releasing position is the problem, not His61.
- **C3 — the parent is already measured at +8.031** (5 seeds, human trimer). Any variant scored
  here is read against that number, not against a fresh parent fold.

## Stopping rule and spend

**One launch. ~$6. No continuation without a new decision.** If 0 of 11 clear A3-B1 the arm is a
negative, it is written up as one, and **nothing about D1 changes.** Documented negatives are this
project's normal output: two arms before this one came back negative and were reported as such.

## Known durability hazard

ESMFold2 returns results only at the END of a batch and the local copy is written by the **local**
entrypoint, so a dead shell loses it (`--detach` does not protect). Every fold is committed to the
Volume as it lands. Recovery:
`mkdir -p runs/recover && cd runs/recover && modal volume get esmfold2-runs <RUN>`
