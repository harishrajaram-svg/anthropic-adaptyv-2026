---
type: preregistration
project: anthropic-adaptyv-2026
problem: 02-tnf-alpha
arm: E1 epitope sweep — is the inversion ours or the target's?
status: PRE-REGISTERED — written 2026-10-11 8:33 AM EDT, BEFORE the sweep runs
cost: $0 (local PROPKA, structures already on disk, no new folds)
---

# E1 — does any pose on human TNF-alpha keep the TARGET's own coupled product below 1.0?

## Why this is the question, and why nine closures never asked it

C13-B3 decomposed each inverted product into the part our binder sequence owns and the part the
target owns. **Target-owned product is above 1.0 in 9 of 9 molecules** (median 2.046, floor 1.318).
A binder contributing exactly nothing still leaves every pose inverted. Every one of the nine prior
closures operated on our side of the interface, so none of them could see this.

Two facts say the binder side is not the constraint:

- `40_L2r3k2` has **binder-owned product 0.744** — its own sequence linkage already points the right
  way, undesigned.
- Of 51 contributing sites, the 15 whose **bound** pKa lands inside 6.0–7.4 carry the damage
  (median 2.667x vs 1.138x outside). **Target Glu146 is 6 of those 15** — the same residue, in 6 of
  9 molecules, every time inside the window, 1.989x–4.635x.

Target-owned product spans 1.318 to 17.225 across nine poses, a 13x range, so the **pose** controls
it. This sweep asks how far.

## The quantity

For each pose, `target_owned = product of ratio over contributing sites whose owner is a target
protomer`, from `bin/ph_gate_multisite.py --problem 2` (ratio = K(6.0)/K(7.4); problem 2 wants
**< 1.0**). Recorded alongside it, per pose: `binder_owned`, total product, whether Glu146 appears
as a contributing site, each contributing target site with free/bound pKa, and the set of moved
target sites as the **epitope fingerprint**.

## Bars

| bar | threshold | meaning |
|---|---|---|
| **E1** | any pose with `target_owned` < **1.0** | a Glu146-sparing epitope exists; step 2 goes live |
| **E2** | ≥1 fingerprint class with ≥**5** poses and median `target_owned` < **1.0** | and it is a class, not a one-off |
| **E3** | pool minimum `target_owned` ≥ **1.0** | objective 2 is closed on the target's own electrostatics — **stop** |
| **E4** | `target_owned` is higher when Glu146 contributes than when it does not, Mann-Whitney one-sided p < 0.05 | the mechanistic claim, tested rather than asserted |

E1 and E3 are complements and one of them fires. **E2 is the bar that licenses spending money**:
E1 alone, without E2, is a single pose and this project has been burned by n=1 before.

## Pool, and the two traps it has to avoid

Human-trimer binder complexes already on disk under `runs/`. **Monomer folds excluded** (no target).
**Nulls excluded from the pool and run separately as a control.**

🔴 **Dedup is by binder SEQUENCE CONTENT, never by design id.** ROADMAP records that several ids
carry two distinct sequences after an aborted run left a parallel output tree, and that a
first-match glob ran 3 of 12 sequence screens on the wrong molecule. This session independently
found `tnfa_corrected_40_L1r1k5` present in the acidban, humansel and v3 input trees with different
sequences behind one id. Joining on id would silently average across different molecules. One
representative pose per unique binder sequence, sequence read out of the CIF itself.

🔴 **Species comes from the gate's own fingerprint, not from the path.** `orient_multi` identifies
every target protomer by histidine tuple and refuses anything that is not N protomers plus exactly
one binder, so mouse complexes and malformed inputs fail closed rather than entering the human pool
on the strength of a directory name.

**Cap: 1,200 poses.** If unique sequences exceed that, the pool is the 1,200 with the best available
`ca_sc_dockq`, because a pose that does not exist is not an epitope. The cap and the ordering are
fixed here, before any output.

## Control

The `null_tnfa_corrected_*` shuffled-binder poses run as a separate group. A shuffled binder has no
designed epitope, so if the null group's `target_owned` distribution is indistinguishable from the
design pool's, the quantity is reading the target's fixed electrostatics rather than anything about
the pose — which would make E1/E2 unreachable in principle and is worth knowing either way.

## 🔴 What E1 cannot do

The gate's **magnitude is noise** (pooled SD 1.499, ~123 seeds to resolve 0.5); only the **sign** is
reportable, and this is one seed per sequence. There is no calibration against the assay because the
released campaign carries no pH labels. The best arithmetic available — best observed binder half
0.744 times best observed target half 1.318 — is **0.981**, break-even and far inside that noise. So
a full E1+E2 pass licenses one ~$30 arm aimed at a *predicted direction*, not a measured switch.

**This does not touch the submission.** Objective 1 ships as it stands; hard close Mon Oct 12
7:59 AM EDT.
