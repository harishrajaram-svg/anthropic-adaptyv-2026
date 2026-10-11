---
type: preregistration
project: anthropic-adaptyv-2026
problem: 02-tnf-alpha
arm: C6 native releasing histidine
status: PRE-REGISTERED — written 2026-10-11 1:15 AM EDT, BEFORE any C6 fold exists
---

# C6 — select for a histidine the designer already placed, instead of installing one

## The move this project has never made

Every pH attempt has been **install-then-hope** or **ignore-the-mechanism**:

| attempt | what it did | why it failed |
|---|---|---|
| §4 / `omit_AA_jsonl` | forced 1-2 His at chosen positions during design | pose collapsed 0.6349 → 0.0126 at 94-95% identity |
| A3 | substituted His into the finished leader | 0 of 11 held; His61 was load-bearing (+8.031 → +0.916) |
| the depth arm | selected on margin alone, mechanism ignored | 0 of 12 releasing, 7 inverted, 5 no histidine |
| C4 | used the target's own histidine | geometry 2 of 5 seeds; H73 not conserved in mouse |

The untried move is **gate on geometry, optimise on margin**: take designs whose **own, unforced**
histidine already sits in a releasing geometry — placed by ProteinMPNN of its own accord, so the
pose was never fought — and ask whether any of them holds.

**The pool already contains them and nobody looked.** `bin/his_geometry_verdict.py` was run on the
12 finalists only. Run across all 5,340 folded designs (569 human-trimer, 83-mer binder):

| verdict | n |
|---|--:|
| **RELEASING** | **48** |
| tightening | 101 |
| no histidine | 350 |
| off-interface only | 70 |

The 7 His-bearing finalists all carry the **same His61**, so the project tested one histidine
arrangement, once. And the backbone-3 **L2 lineage carries His28 in a releasing geometry across
rounds 5, 8 and 9** — the margin-driven loop kept it through three rounds of optimisation without
ever selecting for it.

## Free screens ran first, and both came back green

- **Liability:** 24 of 26 candidates on surviving backbones are `express_qc_p2` CLEAN, pI **4.25-5.28**
  — far below the 6.0-7.4 assay window that killed `40_L3r5k2` (6.83) and `3_L0r5k2` (6.63). One
  histidine on an acidic background does not move pI into the window.
- **Mouse conservation of the partner cation**, by pairwise alignment of the two constructs actually
  folded (157 human vs 156 mouse, 79.5% identity):

| partner cation | mouse | consequence |
|---|---|---|
| **R32** | **R32, conserved** | a switch here can satisfy objective 3 |
| **R82** | **R81, conserved** | same |
| R138 | L137, **not conserved** | human-only switch at best |

⚠️ Numbering: these are read off the folded 157-mer fixture chains and aligned to the same mouse
construct used in the mouse runs, so they are internally consistent. §4's "R108/K166" are in a
different scheme and are **not** compared here.

## What folds

6 designs + 6 composition-matched nulls = 12 complexes, 5 seeds = **60 folds**, ~$5, 3 shards.
Sequences are taken from each design's own RELEASING fold and recorded in
`C6_provenance_2026-10-11.tsv` — never from a glob, after the error corrected in the C4 prereg.

| design | His | partner | d_cat Å | separation Å | mouse | round |
|---|--:|---|--:|--:|:-:|--:|
| `3_L2r9k5` | 28 | **R32** | 3.24 | **11.08** | **conserved** | 9 |
| `40_r2p0k3` | 61 | **R32** | 5.54 | 4.39 | **conserved** | 2 |
| `40_L3r3k1` | 61 | **R82** | 4.39 | 3.17 | **conserved** | 3 |
| `3_L2r5k4` | 28 | R138 | 5.67 | 3.91 | no | 5 |
| `3_L2r8k1` | 28 | R138 | 6.11 | 3.64 | no | 8 |
| `3_L2r9k1` | 28 | R138 | 4.85 | 3.41 | no | 9 |

The three R138 designs are included deliberately: if the mechanism holds only there, we learn the
geometry is achievable but species-restricted, which is a different and still reportable result.

## Bars — fixed now

| bar | threshold | meaning |
|---|---|---|
| **C6-B1** | median margin ≥ **+6.347** | it holds at all |
| **C6-B2** | median margin ≥ **+7.706** | it could take a slot on affinity as well |
| **C6-B3** | releasing geometry in ≥ **3 of 5** seeds | the geometry is structural, not a single-seed artifact |

**B1 AND B3 ⇒ a pH slot candidate**, and if its partner is R32 or R82 it is a *full-spec* candidate
rather than a human-only one. B3 alone is worthless. B1 alone just means we found another binder.
A B1+B3 pass on a conserved partner then needs a mouse leg and the prior-art prescreen before it
could ship — neither is in this arm.

## The prior is weak, and stating it is the point

Of the 12 releasing-His designs that have any interface-PAE measurement, the best is **9.382**
against the leader's 6.997 and nulls at 14.5-15.0 — a margin near +5.1, **below the floor**. Both the
stage-A analysis and C4 found releasing geometry anti-correlating with holds, which has a plausible
cause: the cation-rich patches sit away from where tight interfaces form. C6 tests the one subset
never measured — the depth-optimised members, from the rounds where margins climbed from +6 to +8.

## 🔴 What C6 cannot do

ESMFold2 is pH-agnostic. C6 measures a hold at no particular pH plus a geometric arrangement in the
design's own predicted pose. **No C6 result may be called a demonstrated pH switch**, and the pKa of
the histidine is not predicted — PROPKA was retired here because its within-design noise exceeded
its between-design signal. One launch, ~$5, no continuation without a new decision.
