---
type: preregistration
project: anthropic-adaptyv-2026
problem: 02-tnf-alpha
arm: C4 mechanism-B (target histidine)
status: PRE-REGISTERED — written 2026-10-11 12:54 AM EDT, BEFORE any C4 fold exists
---

# C4 — put OUR cation against THEIR histidine

## Why this arm exists, and why it is not a repeat of A3

Every pH attempt in this project put the titratable group on **our** side: §4's R108/K166 plan, the
constrained designer (`omit_AA_jsonl`), and A3's post-hoc substitution. Both installation routes are
measured dead — forcing two histidines collapsed pose 0.6349/0.5053/0.6203 to 0.0126/0.0309/0.0772 at
94-95% identity, and A3 found His61 load-bearing (`ctrlH61Q` +8.031 → +0.916, 0 of 11 cleared B1).

The target carries **three histidines per protomer** (positions 15, 73, 78 in the fixture's own
numbering; nine across the trimer). If a **binder Lys/Arg** is the nearest charged group to a target
His, protonation at pH 6.0 gives like-charge repulsion → **release**, and *nothing titratable is
required in the binder at all*. That asks the generator for nothing, which is precisely what killed
every earlier attempt.

## The control ran first, and it is not encouraging

`mechB_scan` (geometry only: ring N of a target HIS vs partner LYS NZ / ARG NE,NH1,NH2 against
partner ASP/GLU carboxylate oxygens, 6.0 Å cross-chain cutoff, RELEASE = d_cat ≤ 6.0 and d_cat <
d_acid) on **25 real crystallographic TNF-α complexes**:

- **0 show RELEASE geometry.**
- 2 show tightening, both at **H73** (4G3Y: GLU53 at 3.71 Å; 9BN7: GLU61 at 3.58 Å).
- H15 and H78 are never approached by a charged partner group at all.

So H73 is the only interface-accessible target histidine, and when real binders reach it they reach
it with an acid. **There is no measured precedent for this mechanism on this target.** That is
declared here rather than discovered later.

Across the **712** human-trimer complexes this project has folded: 23 RELEASE, 127 tighten, 562 no
contact. On the **48** designs with measured stage-A margins, the single RELEASE design is `19_s1` at
margin **+0.512**, sc_dockq 0.0243, fnat 0.000, lrms 31.5 Å — the geometry appears where the binding
does not, consistent with the control. **None of the 12 finalists carry it.**

## 🔴 A correction to my own first read, before it propagated

The first pass used a **first-match glob** over fold trees — the same error
`depth12_canonical_sequences_2026-10-09.tsv` exists to prevent. It joined an interface-PAE value of
**7.752** to `3_L0r2k2`'s RELEASE geometry and I reported that pairing. Checked per fold, the two
numbers belong to **different molecules**:

| molecule | tree / fold | geometry | PAE |
|---|---|---|---|
| `SMEKVKQLLENLK…` | `depthB-r2-human-v3-out`, `sample_4` | **RELEASE** (LYS27 4.07 Å vs GLU28 8.04 Å) | **none** |
| `SLEKVKQLIENLK…` | `depthB-r2-out` `depthB2`/`depthB2v2`, `sample_2` | tighten (LYS31 8.95 Å vs GLU20 5.83 Å) | 7.752 |

**So no candidate in this arm has a measured hold.** C4 is a blind first measurement, not a
confirmation, and its prior is correspondingly weak.

## What folds

Four designs, each the exact sequence carrying the RELEASE geometry, taken from the named fold
rather than from a glob. `40_r1p1k7` is **excluded**: it has the geometry but a measured interface
PAE of 14.170, which is null territory.

| design | backbone | His in binder | release contact (seed 42, 1 fold) | release fold |
|---|--:|--:|---|---|
| `3_L0r2k2` | 3 | **0** | LYS27 4.07 Å vs GLU28 8.04 Å | `depthB-r2-human-v3-out/.../sample_4` |
| `3_L2r3k7` | 3 | 0 | ARG28 5.94 Å vs GLU20 6.63 Å | `depthB-r3-human-v3-out/.../sample_7` |
| `40_L3r5k2` | 40 | 1 | LYS24 5.89 Å vs GLU54 6.95 Å | `depthB-r5-human-v3-out/.../sample_10` |
| `10_L5r9k2` | 10 | 0 | see scan output | `depthB-r9-human-v3-out/.../sample_0` |

All four come out of the **v3 arm's human-side tree** — the designs the worse-of-two selector built
and then discarded. 4 designs + 4 composition-matched nulls = 8 complexes, 5 seeds = **40 folds**,
~$4. Nulls are the `random.Random(20261006)` shuffle convention, verified against an existing null
before staging.

## Bars — fixed now

| bar | threshold | meaning |
|---|---|---|
| **C4-B1** | median margin ≥ **+6.347** | a hold exists at all (non-binder median) |
| **C4-B2** | median margin ≥ **+7.8144** | slot candidate on affinity grounds (binder median) |
| **C4-B3** | release geometry in ≥ **3 of 5** seeds | the geometry is real and not a single-seed artifact |

**B1 AND B3 ⇒ a pH slot candidate**, shipped as a declared hypothesis with its own 0-His sequence as
its control. B2 is a bonus, not a requirement — the organisers rank pH-selectivity first and
affinity third. **B3 without B1 is worthless** (geometry on a molecule that does not hold), and
**B1 without B3 just means we found another binder**, which is reported but is not a pH result.

## 🔴 What C4 CANNOT do — declared in advance

ESMFold2 is **pH-agnostic**; C4 measures a hold at no particular pH plus a geometric arrangement. It
is not a pH measurement, not a pKa calculation, and not evidence of a switch. The target histidine's
own pKa is unknown here — the PROPKA route was retired on this project because within-design noise
exceeded between-design signal — so even the *direction* is a hypothesis about pH 6.0 rather than a
prediction of it. **No C4 result may be described as a demonstrated pH switch.** Mouse conservation
of the relevant histidine is **unverified**: the mouse construct has a His at renum 69 against
human's 68, which is adjacent and plausible but needs an alignment, and objective 3 requires it.

## Stopping rule and spend

**One launch, ~$4, no continuation without a new decision.** If 0 of 4 clear B1, objective 2 is
closed for the fourth time, with this number attached, and the submission says so.
