---
type: preregistration
project: anthropic-adaptyv-2026
problem: 02-tnf-alpha (instrument-level, applies to problem 1 too)
arm: R1 — calibrate the binding-coupled pH gate against published switches
status: PRE-REGISTERED — written 2026-10-11 12:30 PM EDT, BEFORE any external structure is scored
cost: ~$0–5
---

# R1 — does the gate separate KNOWN pH-dependent binders from known non-switches?

## Why this outranks more design

Every pH result this project has, including today's H1+H2 passes, rests on one instrument that has
**never been calibrated against a measured switch.** Adaptyv's released campaign carries no pH
labels. And the one internal check available says the readout does not discriminate:

| | designs | composition-matched shuffled nulls | ratio |
|---|--:|--:|--:|
| gate **total** < 1.0 | 70/1200 = **5.8%** | 8/144 = **5.6%** | **1.05x** |

A scrambled sequence clears the bar as often as a designed binder. Replication across seeds — which
`quadH_E3Q_k12` passed 5 of 5 — shows a reading is **reproducible**, not that it is **real**. Only an
external positive/negative set can tell those apart, and nothing we fold can substitute for it.

## 🔴 A code change is required, and it is the risky part

`ph_gate_all.family()` identifies the target by **histidine fingerprint** against four registered
constructs — `CROP`, `D3`, `ECD` (EGFR) and `TNF`. Every other complex is **REFUSED** with "target
family unrecognised". That fail-closed behaviour is load-bearing: it is what kept 1,551 mouse poses
out of the E1 pool and what makes `orient_multi` safe.

**Declared change:** add an explicit `--target-chains` / `--binder-chain` override that bypasses
`family()` **only when the caller names both**, leaving the fingerprint path as the default and
untouched. Required alongside it:

1. A mutation test that the override **cannot activate implicitly** — absent the flags, an
   unregistered target still refuses.
2. Re-running the existing selftest (currently 11/11) and **one committed TNF artifact** reproduced
   byte-for-byte after the change, before any external structure is scored. If that artifact moves,
   the change is reverted and R1 stops.

## Sets

**Positive set** — a published binder with a **measured** affinity or rate at two pH values spanning
roughly 6.0 and 7.4, a ratio the authors call a switch, and a structure (crystal/cryo-EM) or a
modellable complex. Classes expected: pH-switch and "recycling" antibodies, histidine-engineered
conditional binders, engineered pH-dependent affinity variants.

**Negative set** — a binder **measured at both pH values** with no appreciable change, matched as
far as possible on class and size. **Without a real negative set this exercise measures nothing**,
so a positive-only collection is not an acceptable fallback.

🔴 **Direction is per molecule.** Known switches go both ways: some weaken on acidification (what
problem 2 wants, `--problem 2`, ratio < 1) and some strengthen (problem 1's direction). Each positive
is scored against **its own** published direction, recorded from the paper before scoring. Scoring
everything as problem 2 would count a correct problem-1 prediction as a failure.

## Bars

| bar | threshold |
|---|---|
| **K1** | positives separate from negatives, Mann-Whitney one-sided **p < 0.05** |
| **K2** | **sensitivity ≥ 0.60** at **specificity ≥ 0.70** |
| **K3** | the shuffled-binder rate on *these same structures* is below the negatives' rate |

**K1+K2 pass → the gate is calibrated**, and objective 2 can be reported as a predicted direction
with a measured error rate. **Fail → objective 2 stays worded exactly as it is today**, uncalibrated,
which costs nothing but the time.

K3 exists because the 5.8%-vs-5.6% result is the reason for this arm; if shuffles score like true
negatives on external structures too, that is the finding and it closes the instrument question.

## 🔴 n ≈ 50 may not exist

Known switches with **both** a measured two-pH ratio **and** a usable structure are plausibly
**10–20**, not 50. **Fallback, fixed now:** report the n actually found, and at **n < 20** report it
as an underpowered pilot with the exact n and **no claim of calibration**. The bar is not softened to
fit the n, and the n is not padded with molecules missing either the measurement or the structure.

## 🔴 What a pass cannot do

It does not make objective 2 a demonstrated switch — ESMFold2 is pH-agnostic. It would make the gate
an instrument with a known error rate instead of an uncalibrated number, which changes what may be
*claimed*, not what was *built*. Nothing here alters any design already made or any margin measured.
