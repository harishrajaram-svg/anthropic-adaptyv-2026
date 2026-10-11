---
type: readout
project: anthropic-adaptyv-2026
problem: 02-tnf-alpha
arm: R1 replication of the E1 candidates
prereg: analysis/02-tnf/PREREG-R1-REPLICATE-L3R2-2026-10-11.md
written: 2026-10-11 9:10 AM EDT
cost: $0 — the folds were already on disk; the mouse leg was NOT run, see below
---

# R1 readout — the direction does not replicate, and the one seed that showed it is the seed that picked it

## Bars

| bar | threshold | `40_L3r2k2` | `40_L3r2k7` |
|---|---|---|---|
| **R1a** | human margin ≥ +6.3473 | **PASS, +6.7522** | **FAIL, +6.3255** |
| **R1b** | human margin ≥ +7.8144 | FAIL | FAIL |
| **R2** | ratio < 1.0 in ≥4 of 5 seeds | **FAIL — 1 of 5, 0 of 4 unseen** | **FAIL — 2 of 5, 1 of 4 unseen** |
| **R3** | mouse margin ≥ +6.3473 | **not run — moot** | not run — moot |

## The margins, which were already on disk

`T-margin-4` and `T-margin-2` held both designs at seeds 1–5 with matched nulls, so this cost
nothing. Margin = `median(null) − median(design)` on `pae_if_mean`, via an **import** of
`pae_interface.score()`, never a parse of its printed table.

| design | design medians (s1–s5) | null median | margin | per-seed SD |
|---|---|--:|--:|--:|
| `40_L3r2k2` | 7.686 7.691 8.042 7.736 8.152 | 14.4883 | **+6.7522** | **0.220** |
| `40_L3r2k7` | 7.566 11.157 8.318 11.117 8.121 | 14.6432 | +6.3255 | 1.739 |

`40_L3r2k2` holds, tightly — SD 0.220 across five seeds is the most stable margin measured in this
problem. It clears the non-binder median and does **not** clear the binder median, and at +6.7522 it
sits below the shipping leader (+8.031 human, +7.706 pooled over 15 seeds). `40_L3r2k7` misses R1a by
**0.0218** and its spread is 1.739, with two seeds at +3.5. Pre-registered bar, pre-registered
rejection.

## R2 is the result: the direction was a seed artifact

`40_L3r2k2`, same sequence, five refolds:

| seed | total ratio | | |
|---|--:|---|---|
| 1 | 1.5408 | wrong | |
| 2 | 2.0604 | wrong | |
| 3 | 3.9855 | wrong | |
| 4 | 1.5559 | wrong | |
| **5** | **0.7694** | right | **← the seed that selected it in E1** |

**0 of the 4 unseen seeds point the right way.** The five-seed median is **1.5559** — inverted. The
prereg declared seed 5 as the selection seed before any of this was computed, and that declaration
is the whole reason the result is interpretable: the single favourable observation is the one that
cannot serve as evidence. `40_L3r2k7` is the same story, 2 of 5 and 1 of 4 unseen (0.9692, i.e. at
the bar).

E1's null control had already said this would happen and I under-weighted it: 13 of 144
**shuffled** binders reached `target_owned` < 1.0, and designs-vs-nulls was p = 0.693. Taking the
minimum over 1,200 poses of a quantity whose seed-to-seed SD (1.499) exceeds the effect finds noise,
reliably. 214 of 1,200 below 1.0 against the nulls' 9% is roughly what chance predicts.

## The mechanism, and the only stable signal in the system

Same sequence, five refolds, the three sites that matter:

| site | s1 | s2 | s3 | s4 | s5 | verdict |
|---|--:|--:|--:|--:|--:|---|
| target **H73** | 0.362 | 0.574 | 0.829 | 0.798 | 0.808 | **helps in 5 of 5** |
| target **GLU146** | 2.097 | 1.199 | 1.637 | 2.181 | 0.917 | wrong in 4 of 5 |
| binder **HIS61** | 1.422 | 2.597 | 2.425 | 0.632 | 0.755 | **sign flips, 3 wrong / 2 right** |

**Target H73 is the only reproducible proton-linkage signal in this problem** — helping in 5 of 5
refolds here, and median 0.799x over 829 poses in E1. One site at ~0.8x cannot overcome Glu146 at
1.2x–2.2x in 4 of 5 refolds.

This also **corrects the correction I made an hour ago.** I wrote then that His61's sign "belongs to
the pose, not the residue." It is weaker than that: for a *fixed sequence*, His61's sign flips
between refolds. It is not reproducible at all, so no claim about His61's direction belongs in
FIELD 2 in either direction — only A3's measured knockout result, which is about the margin and not
about pH.

## Why the mouse leg was not run

R3 is moot and spending on it would be theatre. `40_L3r2k7` failed R1a, and `40_L3r2k2` failed R2 —
neither is a pH candidate, and `40_L3r2k2`'s margin is below what already ships, so a mouse number
could not change the submission. The 20 folds (~$0.90) were authorised and are **not** being spent.

## Standing

Objective 2 is now closed **ten** ways. E1 was the right experiment — it falsified the stop
condition it was built to test, found the dominant term (Glu146, p = 8.5e-46), and named the only
helping site (H73) — and then its candidate failed the replication that E1 itself could not run.
The submission is unchanged: objective 1 ships, objective 2 is reported as not demonstrated.

Hard close: **Mon Oct 12, 7:59 AM EDT.**
