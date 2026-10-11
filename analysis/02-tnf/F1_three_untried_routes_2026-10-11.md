---
type: analysis
project: anthropic-adaptyv-2026
problem: 02-tnf-alpha
written: 2026-10-11 9:20 AM EDT
status: ANALYSIS ONLY — no design run, no folds, nothing authorised
cost: $0
---

# Three routes to objective 2 that the ten closures did not test

Everything closed so far shares one assumption: the pH response comes from a **titratable group's
pKa shifting on binding**, read by the binding-coupled gate. Today established that this instrument
cannot support the claim — its seed-to-seed SD (1.499) exceeds the effect, binder-side signs are not
reproducible for a fixed sequence (His61 flips 3-wrong/2-right across five refolds of one molecule),
and selecting the extreme of 1,200 poses on it returns noise (R1: 0 of 4 unseen seeds).

Only one quantity in that instrument replicates: **target H73 helps, 5 of 5 refolds, median 0.7986x
over 829 poses.** The three routes below either multiply that term or leave the instrument behind.

## Route 1 — engage H73 on TWO protomers. Never once attempted.

**0 of 1,200 poses in the E1 pool engage more than one H73.** Not one. The geometry does not forbid
it, measured on a real folded complex:

| | |
|---|--:|
| H73–H73 cross-protomer, CA–CA | **21.58 / 22.02 / 22.07 Å** |
| our 83-mer binder's max CA–CA span | **35.3 Å** |
| nearest GLU146 to any H73 | **20.1–20.6 Å** |
| nearest ASP143 to any H73 | 18.4–19.0 Å |
| nearest GLU110 to any H73 | 10.4–11.1 Å |

The binder is large enough to bridge two H73 sites, and **the H73–H73 axis is 20 Å away from
Glu146** — the dominant opposing term (contributes in 863 of 1,200 poses, median 1.781x, E4
p = 8.5e-46). That distance is the point. Current poses engage one H73 *and* bury Glu146 because
they lie on a protomer face; a seam-spanning pose is oriented along a different axis and Glu146 is
plausibly outside the footprint.

Arithmetic from measured terms only: two H73 at 0.7986x gives **0.638x**; Glu110 at 1.148x comes
along at that distance for **0.732x**, or 0.841x if both protomers' Glu110 contribute. Compare the
already-measured `GLU110,H73` class — median **0.9668x** at n=23 with *one* H73.

🔴 Honest risk: every good pose this project has produced sits on one protomer face. A 22 Å
seam-spanning pose is a harder docking problem and DockQ may collapse the way arm A's did. The
premise is sound; the pose is the gamble.

## Route 2 — stop switching the interface and destabilise the FOLD. The data is already on disk.

C9e measured histidine pKa on monomers at 20 positions, 5 seeds, medians, pLDDT 0.84–0.91, and
classed each by its *binding* linkage. Re-read as **folding** linkage — pKa in the folded state
against His's intrinsic 6.5 in the unfolded reference — the classification **inverts**:

| variant | burial | pKa | C9 class | low-pH destabilisation |
|---|--:|--:|---|--:|
| V45H | 95 | 4.26 | **inert** | **+0.77 kcal/mol** |
| L63H | 91 | 4.30 | **inert** | **+0.76** |
| L53H | 85 | 4.58 | **inert** | **+0.75** |
| L64H | 85 | 5.03 | **inert** | **+0.72** |
| L44H | 72 | 6.25 | switch | +0.21 |
| S65H | 45 | 6.86 | switch | −0.33 |
| I50H | 77 | 7.19 | switch | **−0.60** (low pH *stabilises*) |

The two criteria are anti-correlated by construction: binding linkage wants pKa near the assay
window, folding linkage wants it deeply depressed. **The four positions C9 discarded as "inert" are
the four best fold-destabilisers, +3.00 kcal/mol summed** — against **+0.13 kcal/mol** for the gate's
best reproducible interface term (H73 at 0.7986x). In energy terms the core beats the interface by
more than twenty-fold, and it is measured on a far quieter instrument: single-chain PROPKA on a
high-pLDDT monomer, not a four-chain coupled gate whose noise exceeds its signal.

🔴 Honest risks, and they are real. +3.00 kcal/mol unfolds nothing if the scaffold is 10 kcal/mol
stable, so this needs a **deliberately marginal** scaffold — the opposite of what we have enforced
all week (C1: 12 of 12 clearing the 0.70 monomer floor at 0.885–0.910). Four buried histidines in one
83-mer core has never been folded; C9 measured them one at a time. ESMFold2 is pH-agnostic, so this
is a thermodynamic prediction and not a predicted structure change — C9's own readout says so. And
deeply buried ionizables are the weakest part of PROPKA's domain.

## Route 3 — long-range charge steering, on an instrument we have and have never used here

Net-charge repulsion is not proton linkage: a binder gaining positive charge at pH 6.0 can be
steered off an electropositive epitope without any pKa shifting on binding. The gate cannot see it;
`bin/dddg_elec.py` — a reimplementation of Rosetta's `fa_elec`, and PyRosetta is explicitly in scope
(organisers, 2026-10-06) — can. The screen is free: compute the epitope patch's net charge and the
binder's, at both pH values. If the H73 seam is electronegative this route is dead immediately,
which is worth knowing in one command. **Not yet run.**

## Where this leaves the submission

Nothing here produces a submittable design before **Mon Oct 12, 7:59 AM EDT**. Route 1 is a design
arm (~$30–40, ~2 h) whose output would still need 5-seed replication. Route 3's screen is free and
could be done now. Objective 2 stays reported as not demonstrated either way.
