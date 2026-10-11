---
type: preregistration
project: anthropic-adaptyv-2026
problem: 02-tnf-alpha
arm: C13 overnight two-arm depth run
status: PRE-REGISTERED — written 2026-10-11 4:20 AM EDT, BEFORE either arm launches
---

# C13 — can a design be made that does not invert, and does the v3 selector work when fixed?

## The finding that killed the refinement I was going to run

C10/C12 localised the inverted pH response to interface carboxylates. The obvious refinement was to
ban acids only in the **desolvated core** of the contact rather than wholesale, since the Oct 9
wholesale ban collapsed the pose (0 of 4). **Calibrating that threshold against the gate output
killed it:** of the **59** binder carboxylates the gate moved across 18 molecules, **59 invert and 0
help**, spanning 26 to 104 heavy-atom neighbours — from quite exposed to fully buried. There is no
desolvation threshold that separates safe acids from inverting ones because there are no safe ones.

So the correct constraint is the wholesale one, and the only honest objection to the Oct 9 result is
**n = 4**. Arm A tests it properly.

## Arm A — acid-banned interface, at scale

`DEPTH_ACID_BAN` on every lineage, `force_his=False` (forcing collapses the pose independently,
measured 0.0702 vs 0.0521 for the two single constraints). Fresh start from the Genie 3 backbone
pool, so this is new design rather than continuation.

| bar | threshold | meaning |
|---|---|---|
| **A1** | any design reaches `ca_sc_dockq` ≥ **0.60** | an acid-free interface can hold a pose at all |
| **A2** | any design's 5-seed margin ≥ **+6.347** | and it binds |
| **A3** | coupled ratio median **< 1.0** with ≥4/5 seeds | and it points the right way |

A1 failing at this scale closes the acid route by measurement rather than by n=4. A1+A2 without A3
means acid removal bought binding but not direction. **A1+A2+A3 is a conditional-binder candidate.**

## Arm B — the v3 arm done right

Unconstrained design, but `DEPTH_SELECT_SPECIES=human`: the primary species as the selector with
mouse still folded and recorded as an end gate. The v3 arm selected on `min(human, mouse)` when
mouse ran ~0.2 lower, so the selector was mouse almost always; human pose reached **0.7776** — the
best this project has produced — while the selector's ceiling was 0.5427 and **30 designs cleared
0.60 on human against zero on the worse-of-two**. That is LESSONS §§9-12 and it has never been run.

| bar | threshold | meaning |
|---|---|---|
| **B1** | any design's 5-seed human margin ≥ **+7.706** | beats what currently ships |
| **B2** | mouse margin ≥ **+6.347** at the end gate | cross-species survives without being selected on |
| **B3** | coupled ratio median < 1.0 in ≥1 design | a non-inverting design exists in a larger sample |

B3 is the part that answers the design question at n = hundreds instead of 12, and it costs nothing
beyond the folds the arm runs anyway.

## Fuses, because this runs unattended

| | |
|---|---|
| `DEPTH_MAX_FOLDS` | **1200 per arm** — refuses to launch a round that would cross it |
| `DEPTH_WALL_STOP` | **2026-10-11 07:00:00 EDT** — checked before every round, so nothing is still spending at wake-up |
| rounds | 10 maximum, and the loop stops itself early on pose regression (`PATIENCE`/`MIN_DELTA`) |
| isolation | `DEPTH_RUN_TAG=acidban` / `humansel`, which scopes both the Modal Volume and the state directory, so the arms cannot overwrite each other or the earlier runs |

Expected spend ~**$40 per arm** on B200 (768-960 folds each at 16.1 s, plus eight container loads
per round), so ~**$80 total**, capped by the fuse. Both arms self-report into
`analysis/02-tnf/depth_rounds/` per round, so a crash loses one round and not the night.

## 🔴 What C13 cannot do

Neither arm can demonstrate a pH switch — the coupled gate's magnitude is noise (pooled SD 1.499,
~123 seeds per arm to resolve 0.5) and only its **sign** is reportable, and the ratio has no
calibration against the assay because the released campaign contains no pH labels. A B3 or A3 pass
is a design whose predicted direction is correct, which is strictly more than anything in the
current submission has, and strictly less than a measured switch.
