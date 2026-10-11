---
type: preregistration
project: anthropic-adaptyv-2026
problem: 02-tnf-alpha
arm: R1 — replicate the two E1 candidates
status: PRE-REGISTERED — written 2026-10-11 9:04 AM EDT, BEFORE any margin or gate number is computed
---

# R1 — do `40_L3r2k2` and `40_L3r2k7` hold, and does the direction replicate?

E1 found two poses that both hold a pose and point the right way at one seed:

| design | DockQ human | mouse | total ratio | target | binder |
|---|--:|--:|--:|--:|--:|
| `40_L3r2k2` seed 5 | 0.7593 | 0.4171 | 0.7694 | 0.7820 | 0.9009 |
| `40_L3r2k7` seed 5 | 0.7417 | 0.3772 | 0.9556 | 1.4628 | 0.6405 |

**Most of this experiment is already on disk and I did not know that when I quoted a price.**
`runs/T-margin-4-out` holds `40_L3r2k2` at seeds 1–5 with its matched null, and `T-margin-2-out`
holds `40_L3r2k7` the same way. So the human margin and the 5-seed direction replication cost **$0**
and no folds. Only the mouse leg needs new compute: 2 designs x 5 seeds x (design + null) = **20
folds, ~$0.90**.

## Bars

| bar | threshold | meaning |
|---|---|---|
| **R1a** | 5-seed human margin ≥ **+6.3473** | it holds at all (non-binder median) |
| **R1b** | 5-seed human margin ≥ **+7.8144** | it holds as well as a real binder (binder median) |
| **R2** | gate ratio **< 1.0 in ≥4 of 5 seeds** | the direction replicates — the test C6 and C9 both failed |
| **R3** | 5-seed **mouse** margin ≥ **+6.3473** | cross-species hold, objective 3 |

**R1a + R2 is the result worth submitting**: a design with a measured hold whose predicted pH
direction survives seed replication. R1b would additionally put it level with the shipping leader.
R3 decides whether it answers cross-reactivity or is human-only.

## 🔴 The selection seed, declared before looking

`40_L3r2k2`'s pose was found at **seed 5**, and seed 5 is one of the five in `T-margin-4`. Seed 5
therefore **selected** this molecule and cannot also serve as evidence for it. R2 is scored two
ways and both get reported: over all five seeds, and over the **four unseen seeds 1–4**, which is
the honest number. Same treatment for `40_L3r2k7` at seed 5 in `T-margin-2`. If the two disagree,
the four-seed figure governs.

## 🔴 What cannot be measured here

`ph_gate_all.family` registers only human TNF, so the gate **refuses mouse complexes by design** —
that is the fail-closed behaviour that kept 1,551 mouse poses out of the E1 pool. There is
therefore **no mouse direction measurement** and R3 is a binding bar only. I am not registering a
mouse family today to manufacture one.

Margin is `median(null pae_if_mean) − median(design pae_if_mean)`, computed by importing
`pae_interface.score()` directly. It is **not** parsed from that script's printed table, which
truncates filenames at 43 characters and silently dropped every null the first time this was done.

## 🔴 What a pass does not establish

The gate's magnitude is noise (pooled SD 1.499); only the **sign** is reportable, so R2 is a sign
test and nothing is claimed about switch size. There is no calibration against the assay, because
the released campaign carries no pH labels. A full R1a+R2 pass is **a measured hold plus a predicted
direction that replicates** — strictly more than anything now in the submission, and strictly less
than a measured pH switch. Objective 2 would still be reported as not demonstrated.

Hard close: **Mon Oct 12, 7:59 AM EDT.**
