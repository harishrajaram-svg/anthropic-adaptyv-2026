# Pre-registration — pose control on measured binders, and structural breadth of the Genie 48

`as_of: 2026-10-08 20:35 ET`
Committed **before any DockQ or TM-score number in this file's scope exists.** Both stages
cost $0: HTTP download plus local CPU. Neither launches a job, spends on Modal, or touches
the live app `ap-gz7W6OayBW3WfvYx5RwwI3`.

## Why this exists

Section 6.10f reports CA-DockQ median 0.0251, Fnat median 0.0000 and ligand RMSD median
31.12 A across 40 of our designs, and the record reads that as a verdict on the designs:
the predictor never puts the binder where it was designed to go. That reading has never
been controlled. The alternative is that our configuration — ESMFold2, single-sequence on
both chains, no target MSA — cannot place **any** binder on this target, in which case the
31 A is a property of the instrument and every interface statistic we have (the pae margin,
AUC 0.794, the contact census AUC 0.889) scores an interface the predictor invented.

The organisers' own protocol says so explicitly at `reference/anthropic-binder-design-protocol.md:260`:
when a substantial fraction of top designs are pose_FAIL, treat the instrument as suspect
before the designs. We have not done that. This is the control.

It is also the honest reason this runs rather than a new design arm: **either branch stops the
reopen.** A FAIL rewrites three documents that currently overstate what we measured. A PASS
says the 31 A is ours. Neither authorises generation. Stage 3 of the costed plan is not
approved and is not in scope here.

## Stage 1 — pose control

**Construction.** For each of the 12 wet-lab-confirmed TNF-alpha binders in
`reference/anthropic-campaign/tnfa_designs.tsv` (`binder_final` true), compare
*their* ESMFold2 prediction with *our* ESMFold2 prediction **of the identical sequence**:

- reference pose: `reference/anthropic-campaign/pose-control/<full_name>__ef2full_1to3.cif`,
  downloaded from `data/designs/TNFa/<full_name>/insilico/predicted_ef2full_1to3.cif` in the
  released dataset. Binder is chain **A**, target chains B/C/D.
- our pose: `runs/A-posctrl-out/Aposctrl/pos_<uuid8>_L<len>/*.cif`, already on disk from the
  section 6.10e positive control. Binder is chain **D**, target chains A/B/C.
- instrument: `bin/sc_dockq.py`, CA-only, contact cut 8.0 A, symmetry-maximised over all
  permutations of the three target chains, with its target-superposition control
  (`TARGET_RMSD_MAX = 4.0`) left in force.
- both target constructs are the identical 157-residue mature chain numbered 1-157, so the
  numbering **offset is 0** and the 2026-10-08 register-shift bug cannot recur. Verified
  before this file was written; 12/12 pairs have byte-identical binder sequences on both
  sides and an identical target 157-mer on both sides.

This is an instrument control, not design material. The CIFs land in a directory that is
never an input path to `bin/design-genie3.sh`, SolubleMPNN or Mosaic, and all 12 uuids are
already excluded from every scoring pool.

**Statistics, named before they exist.** Median CA sc_DockQ, median Fnat and median ligand
RMSD (LRMS) over the 12 matched pairs.

**Bar.**

- **PASS** = median LRMS <= 10.0 A **AND** median Fnat >= 0.10
- **FAIL** = median LRMS > 15.0 A **OR** median Fnat < 0.05
- anything between the two **resolves as FAIL** — fail closed. "Ambiguous" is how the Genie
  arm's 5.64 bar got honoured in the wrong direction; it does not get a second chance here.

**Negative control, also pre-registered, and it can void a PASS.** Pairing a reference pose
with the *wrong* fold of the same length gives a null for the same statistic: 8 Genie3
binders at L=83 give 8x7 = 56 mismatched pairs, 4 PXDesign at L=80 give 4x3 = 12, so 68 in
all. A matched median LRMS inside 10 A means nothing if parking any binder near a large
homotrimer also lands inside 10 A.

- the matched 12 must separate from the 68 mismatched on LRMS at **AUC >= 0.75** (lower LRMS
  = matched), with a two-sided permutation p <= 0.05 at 20,000 permutations
- if it does not, the verdict is **VOID**, not PASS, whatever the matched medians read

**Refusals are reported, never dropped.** `sc_dockq.py` returns REFUSED when its target
control fails. If more than 2 of the 12 matched pairs refuse, the stage verdict is
**REFUSED** — neither PASS nor FAIL — and the cause is diagnosed before anything is written
into the record.

**What each branch obliges.** FAIL: rewrite section 6.10f, limitation 51 and the methodology
box's FIELD 2 to state that our configuration cannot place a measured binder, and that the
margin instruments therefore score a predicted interface of unknown relation to the designed
one. PASS: 6.10f's 31 A stands as a design failure, and the pose gate is a validated screen.
Either way nothing is generated.

## Stage 2 — structural breadth of the Genie 48

The family analysis established that our 48 designs are 48 **sequence** families (every design
a singleton at identity >= 0.55; max pairwise 0.543 over 1,128 pairs; corroborated by
`outbox/prescreen-genie48/report.csv` reporting `cluster_size = 1` for all 48). It flagged
**structural** breadth as UNVERIFIED: 48 distinct sequences at fixed L=83 from one generator
may be one fold.

**Construction.** Extract the binder chain (chain D, full-atom) from each of the 48 co-folds
in `runs/A-cofold-out/Acofold/tnfa_corrected_*_s*/*.cif` and run `tools/foldseek/bin/foldseek`
all-vs-all in TM-align mode. The Genie 3 backbones at
`runs/genie3-out/probe50/tnfa_corrected/pdbs/` are **CA-only** (539 CA atoms, one per residue),
so they are reported as a secondary read only if foldseek accepts them; the primary object is
the predicted full-atom fold of the sequence we would actually submit.

**Statistic.** Number of single-linkage clusters at **TM-score >= 0.5**, the conventional
same-fold threshold, over the 48.

**Bar.**

- **>= 20 clusters** — the breadth claim stands as written
- **< 10 clusters** — `submissions/02-tnf-METHODS.md:1259` and every "48 families" statement
  get qualified to "48 sequence families, N structural clusters" before they ship
- **10-19** — partial; the count is stated explicitly in both documents, no adjective

**Hard stop.** If stage 2 is not finished by **Fri Oct 9, 10:00 PM EDT**, it is dropped. Items
17b and 17e outrank it.

## What is out of scope

Stage 2 of this file also carries three recomputed discrepancies for the record: the
CA-versus-all-atom DockQ scale mismatch behind "0 of 40 passing the protocol's 0.23"; the
`sc_dockq` NaNs in the organisers' released table; and `bin/mpnn_constraints.py`'s
`MAX_FORCED_HIS` running opposite to the measured histidine distribution. Those are write-ups
of numbers recomputed from committed artifacts, not new measurements, and they carry no bar.

Stages 3-5 of the costed plan — regeneration under a compositional filter, predict-then-redesign
depth rounds, nomination — are **not approved and not pre-registered here.** Nothing in this
file authorises a `modal` command.
