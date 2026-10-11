---
type: preregistration
project: anthropic-adaptyv-2026
problem: 02-tnf-alpha
arm: C5 confirmation of 40_L3r5k2
status: PRE-REGISTERED — written 2026-10-11 1:07 AM EDT, BEFORE any C5 fold exists
---

# C5 — does `40_L3r5k2` survive the tests the ship set has already passed?

## Why

C4 produced `tnfa_corrected_40_L3r5k2` at **+8.143** (5 seeds), above `40_L1r4k1`'s 5-seed +8.031
and above its pooled 15-seed **+7.706**. It is from the v3 arm's discarded human-side tree and has
never been through any screen. C2 measured a **−0.374** shift between 5-seed and fresh-seed reads
two hours ago, so a 5-seed number is not a result yet. This arm applies to `40_L3r5k2` exactly the
tests the current ship set has passed, and nothing else.

**One launch, ~$5, 46 folds. No continuation without a new decision.**

## What folds

| run | content | folds |
|---|---|--:|
| **C5a** | human trimer, `40_L3r5k2` + its matched null, **seeds 6-15** | 20 |
| **C5b** | binder alone (C1 path), seeds 1-5 + 42 | 6 |
| **C5c** | mouse **trimer** (3 x 156, the construct §6.12 established), `40_L3r5k2` + null **and `40_L1r4k1` + null as an in-run comparability control** | 20 |

Mouse target chains are copied byte-for-byte from `runs/depthB-r1-mouse-b1-in`. Nulls are the
`random.Random(20261006)` shuffle convention, verified against an existing null before staging.
`40_L1r4k1` is folded in-run on the mouse leg because its Oct 9 mouse trimer read of **+7.207** then
serves as the yardstick inside this run rather than across runs.

Local, no GPU, run while the folds are in flight: `bin/express_qc_p2.py`, the prior-art prescreen,
Foldseek TM against the 12, and a sequence-identity check against the canonical set.

## Bars — fixed now

| bar | threshold | meaning |
|---|---|---|
| **C5-R1** | seeds 6-15 median margin ≥ **+7.706** | at least as good as what currently ships, on unseen seeds |
| **C5-R2** | ≥ **+6.347** | holds at all |
| **C5-M1** | binder-alone pLDDT ≥ **0.70** | the organisers' own floor, which the 12 clear 12/12 |
| **C5-X1** | mouse trimer 5-seed margin ≥ **+6.347** | objective 3, same convention as `depth12_mouse_trimer_5seed` |
| **C5-X1c** | in-run `40_L1r4k1` mouse margin within **±0.5** of +7.207 | the mouse comparison is sound rather than cross-run drift |
| **C5-Q1** | `express_qc_p2` clean, **pI outside 6.0-7.4** | the one liability that can manufacture a false positive |
| **C5-P1** | prior-art prescreen passes | eligibility |

## Decision rules, fixed before the numbers land

1. **R1 + M1 + X1 + Q1 + P1 all pass ⇒ it ships.** Whether it *replaces* `40_L1r4k1` or joins as a
   third design is decided by structure, not by preference: Foldseek **TM ≥ 0.5** to `40_L1r4k1`
   means one fold, so only the better of the two ships (that would be `40_L3r5k2` under R1);
   **TM < 0.5** means a distinct cluster and it can take a third slot.
2. **R1 fails, R2 passes ⇒ it displaces nothing**, and is reported as a measured co-candidate that
   did not beat the leader on unseen seeds.
3. **R2 fails ⇒ +8.143 was a seed artifact**, reported as such, and C2's lesson is confirmed twice.
4. **Any of M1 / Q1 / P1 fails ⇒ it cannot ship at any margin.** Q1 is not negotiable: a design that
   aggregates at pH 6.0 reports as "no binding at pH 6.0" and is indistinguishable from the
   successful switch this problem asks for.
5. X1 failing while R1 passes ⇒ it may ship **only** as a declared human-only design, and the
   methods say so; it does not displace a design that holds both species.

## What C5 cannot do

It cannot make `40_L3r5k2` a pH candidate — C4 closed that for all four of its designs, and this
molecule's own release geometry replicated in **2 of 5** seeds. C5 is about affinity, expression and
cross-species only. Its design-side interface PAE is **worse** than the leader's (7.805 vs 6.997);
the margin is the pre-registered instrument because the 150-design calibration selected it, and that
tension is reported in whatever the result turns out to be.
