---
type: preregistration
project: anthropic-adaptyv-2026
problem: 02-tnf-alpha
arm: C11 implicated-glutamate substitution
status: PRE-REGISTERED — written 2026-10-11 3:36 AM EDT, BEFORE any C11 fold exists
---

# C11 — the reviewer's focused experiment, in silico

## Where this comes from

PK's fifth reply (2026-10-09, filed tonight after 33 hours in Gmail only) specified the experiment:

> "identify the residues driving the predicted reverse effect and check whether their involvement is
> consistent across plausible poses… compare the parent with an implicated Asp-to-Asn or Glu-to-Gln
> substitution, alongside a comparable substitution at an uninvolved exposed site."

C10 did the identification. On the binding-coupled quantity — the protonation change between free
partners and complex, free leg by partner deletion in place, composed over all 78-79 sites — **30 of
30 poses across six molecules point the wrong way**, and three binder glutamates drive it:

| site | median ratio | consistency |
|---|--:|--:|
| **binder GLU28** | 1.432× | **30/30 poses** |
| binder GLU20 | 1.476× | 27/30 |
| binder GLU7 | 1.349× | 29/30 |

All three sit at the interface (d_target 4.01, 2.09, 3.82 Å), which corroborates the acid-rich
interface explanation rather than assuming it.

## The pair

| | substitution | d_target | neighbours ≤8 Å | status |
|---|---|--:|--:|---|
| **test** | **E28Q** | 4.01 Å | 42 | implicated in **30/30** poses, 1.432× |
| **control** | **E61Q** | 24.8 Å | 42 | never appears in the contributing list |

E61 was chosen because its burial matches E28's exactly (42 neighbours each) while sitting 24.8 Å
from the target — same chemistry, same local packing density, different location. Glu→Gln removes
the titratable proton while preserving size and shape, which is the substitution PK named.

2 designs + 2 composition-matched nulls, 5 seeds = **20 folds, ~$2**, B200. Then
`bin/ph_gate_multisite.py --problem 2` on both, at $0.

## Bars — fixed now, and framed around the noise

C10 measured the parent's own composed ratio spanning **1.284–4.258** across five seeds. The
magnitude of this instrument is unusable at that spread and this arm does not pretend otherwise:
**the readout is direction and selectivity, not the ratio.**

| bar | threshold | meaning |
|---|---|---|
| **C11-P1** | E28Q median composed ratio **< parent median 2.874** | removing the implicated proton reduces the inversion |
| **C11-P2** | **all 5** E28Q seeds below 2.874, and **not** all 5 E61Q seeds below it | the reduction is selective to the implicated residue, not a response to any Glu→Gln |
| **C11-B1** | E28Q margin ≥ **+6.347** | binding survives the substitution |

**P1 AND P2 AND B1 supports GLU28 as a driver of the inverted pH response.** P1 without P2 means any
Glu→Gln does it and the residue is not implicated. B1 failing means the substitution destroyed the
thing we were trying to explain, which PK also anticipated: "loss of binding at both pHs… would
leave the mechanism unresolved."

## 🔴 What C11 cannot do

It cannot demonstrate a pH switch, and it cannot make these designs releasable at pH 6.0 — the
measured direction is inverted and this arm tests *why*, not how to fix it. PK's own caveat stands
and is adopted verbatim in the writeup: "the substitution changes other local interactions too, so
it would support rather than conclusively prove a protonation mechanism." The bench version —
binding at both pH values with folding and solubility checks at both — is the lab's, not ours.
One launch, ~$2, no continuation without a new decision.
