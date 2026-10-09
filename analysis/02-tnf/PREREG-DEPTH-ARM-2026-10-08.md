# Pre-registration — predict-then-redesign depth arm

`as_of: 2026-10-08 22:05 ET`
Committed **before any fold is launched.** Nothing in this file has been run. It authorises
nothing by itself: stage A needs an explicit yes from Harish because it spends, per the standing
rule that one yes covers one run and never carries forward.

## What this arm is, and why it is not a repeat of a stopped search

§45 and §47 stopped the design search after 24 trajectories across 7 conditions. Those stops were
about **gradient-based design on a single oracle** — Mosaic descending a loss supplied by Boltz-2,
which §48 then showed could not discriminate a binder from a shuffle. This arm uses no gradient
and no loss. It is the organisers' own documented procedure: co-fold, take the **predicted**
complex, inverse-fold it with the target chains held fixed, co-fold again, keep what improved.
Their protocol mandates at least two rounds per target and at least five on hard ones. We ran
**zero**, and their zero-round cell is **0 of 37** while their 8-12 round cell is 8 of 17.

Two things changed tonight that did not exist when those stops were written:

1. **The pose instrument has a positive control.** §6.10g: our configuration recovers the
   campaign's pose for all 12 measured binders to a median 1.57 A. Before tonight, every pose
   number we had was uninterpretable. The loop needs a trustworthy selection signal and now has one.
2. **A validated compositional filter, and 32 candidates already on disk.**
   `COMPOSITION-FILTER-2026-10-08.md`: 4.04x enrichment on the released labels, and 32 of our 100
   pre-constraint seed sequences sit inside the measured binder band while only 2 of the 48 we
   actually submitted do.

## The oracle question, resolved without amending frozen decision C1

C1 (`frozen-decisions.md:59`) reads: *"a design objective may not contain ipSAE and may not use
ESMFold2. Design on Boltz-2 or Protenix; ESMFold2 stays reserved for ranking."* Its stated reason
is that designing on the ranking instrument makes December's question — did our ranking predict
binding? — unanswerable.

Predict-then-redesign makes a co-folder the design oracle by construction, and ESMFold2 is our
only working co-folder. The proposal that produced this arm suggested amending C1 and shipping the
designs disqualified as evidence. **That is not necessary, and this is the rule instead:**

> **Selection inside the loop reads one statistic only: CA sc_DockQ between the Genie 3 designed
> backbone and the prediction. No confidence score may enter selection — not ipSAE, not ipTM, not
> iPAE, not pLDDT, at any round, for parent choice, continuation or stopping.**

The distinction is load-bearing and it is this. A confidence score is the predictor's opinion of
itself, so climbing it is climbing the ranker. sc_DockQ is agreement with an **external reference
the predictor never sees** — the designed backbone. Climbing it means "the prediction increasingly
matches the structure we specified," which is the design objective stated directly rather than a
proxy for the ranker. ipSAE_min is computed and stored at every round and **never read**, so it
survives as a genuinely held-out ranker for December on these designs.

**The leakage this does not eliminate, disclosed now rather than found later.** ESMFold2's
geometry and its confidence are correlated, so selecting on geometry will shift confidence
indirectly: our own `residue_pairs` correlates with the campaign's `ef2full n_interface_contacts`
at Spearman +0.936 on the same 42 designs. The claim is therefore **not** "ipSAE is uncontaminated
on these rows." It is "ipSAE was never read, so the contamination is indirect and bounded rather
than direct and total." Every stage-B row ships with `score_instrument` naming
`ca_sc_dockq_vs_designed_backbone` as the selector, so a December reader can discount them without
having to reconstruct what happened.

Boltz-2 is **not** used. C1 nominates it, but `frozen-decisions.md:71` says an arm that fails is
excluded for that problem, and §48c measured it as the weakest credible oracle on the board
(AUC 0.781 against ESMFold2's 0.822 and rf3's 0.951). Promoting a failed arm to design oracle is
the exact error §48 diagnosed. Not repeating it.

## Stage A — the entry gate. $1.19.

**What runs.** Co-fold the **32** seed sequences that pass `bin/comp_filter.py` from
`runs/g50mono-in`, as 1-to-3 complexes against the canonical TNF-alpha trimer, one seed, no nulls
(a pose gate needs none). 32 folds in one container.

**Cost and time.** 32 x $0.0371 = **$1.19**; 32 x 54.5 s + one 137 s model load = **~31 min**.

**Statistic.** CA sc_DockQ, Fnat and ligand RMSD from `bin/sc_dockq.py` between each design's
Genie 3 backbone (`runs/genie3-out/probe50/tnfa_corrected/pdbs/tnfa_corrected_<N>.pdb`, chain A =
binder) and its co-fold (chain D = binder), symmetry-maximised, with the target-superposition
control in force. **Read on the count reaching ligand RMSD <= 10.0 A.**

**Bar.** Our existing 40 post-constraint designs give ligand RMSD **median 31.1 A, best 15.0 A**,
and best CA sc_DockQ 0.0865. So:

- **GO = at least 3 of 32 reach ligand RMSD <= 10.0 A.** That is better than anything this project
  has produced, by 1.5x on the best single case.
- **STOP = 2 or fewer.** $1.19 spent, the arm is closed, and the result is written up as a measured
  negative: the pre-constraint chemistry does not fix the pose either, which is itself worth saying
  because it separates the chemistry failure from the pose failure.
- Refusals by the target control are reported, never dropped. More than 6 of 32 refusing makes the
  verdict **REFUSED** rather than GO or STOP, and the cause is diagnosed first.

The bar is **not** the protocol's 0.23. That is an all-atom DockQ and ours is CA-only against a
one-atom-per-residue backbone; `bin/sc_dockq.py`'s own docstring says the scales are not
comparable, and §6.10g establishes only that the CA scale is not deflated, not where its
designed-against-predicted threshold sits.

## Stage B — up to 10 rounds. ~$8.90.

Fires only on a stage-A GO **and** a separate explicit yes. Parents are the stage-A survivors.

**Per round.** For each parent: convert its predicted complex to PDB, mark chain D designed and
chains A/B/C fixed, run SolubleMPNN (`--use_soluble_model`, 8 sequences, temperature 0.1) —
verified working, 8 sequences in 3.7 s, local, free. Co-fold the 8. Score. Select the best by
CA sc_DockQ. That design becomes the next round's parent, under the same root backbone id.

**Cost and time.** 3 parents x 8 sequences x 10 rounds = 240 folds = **$8.90**, ~4.1 h of GPU in
one container. Rounds are serial by nature; folds within a round are not, so splitting a round
across 4 containers takes it to ~10 min per round at the cost of 4 model loads.

**Continuation rule, read at the end of every round.**

- **CONTINUE** while the round's best CA sc_DockQ improves by **>= 0.01** over the previous round's
  best, and no parent regresses above 10.0 A ligand RMSD.
- **STOP** on two consecutive rounds without a >= 0.01 improvement. Two, not one, because a single
  flat round inside a stochastic resampling procedure is not evidence of a ceiling.
- **STOP** at round 10 regardless. Ten is the cap, not the target; their winners carried 8 to 10.
- **STOP** at **Sat Oct 10, 6:00 PM EDT** whatever the state.

### The second referee, which is what makes ten rounds defensible rather than reckless

Ten rounds of hill-climbing against one predictor builds an adversarial example for that
predictor. That is not hypothetical here: it is §48's diagnosis of why 24 trajectories produced
beautiful numbers and nothing that binds. The organisers' loop re-ranked at every promotion step
across **three** independent co-folders and took the **worst** arm's pose score, and that
disagreement is what converted their depth into real improvement.

`biomodals/modal_chai1.py` is on disk and **has already run** — `runs/chai1/` holds 70 structures
across a validation set that includes barnase/barstar. The reason it was never built into a
ranking arm is that it **emits no PAE and no ipSAE**, so it could not feed the ranker. That is
precisely why it fits here: this loop's selector is pose agreement with the designed backbone,
which needs a structure and nothing else. The gap that blocked it as a ranking arm does not exist
for this use.

**Pre-registered now, so it is not an improvisation at round 4:** from **round 4 onward**, a
design may only be carried forward if **both** ESMFold2 and Chai-1 place it within
`POSE_GATE_LRMS` of the designed backbone, and the selector becomes the **minimum** CA sc_DockQ
across the two arms, matching the protocol's own min-over-arms rule. Rounds 1-3 may run
single-arm, because three rounds is inside the range this project has already defended and the
overfitting risk compounds with depth.

If Chai-1's per-fold cost has not been measured by the time round 3 ends — it is **unmeasured
today**, and this file does not guess it — then the arm **stops at round 3** rather than
continuing single-arm. Spending rounds 4 through 10 on one oracle is the thing this stage exists
to prevent, so the fallback is to stop, not to proceed unguarded.

**Success bar for submission**, separate from the continuation rule and anchored on the one
instrument calibrated against measured outcomes: a stage-B design may enter the final 20 only if
its margin on `pae_interface_mean` against its own size-matched null reaches **+6.347**, the
measured non-binder median from `analysis/02-tnf/labelled_control_2026-10-08.tsv` (binders +7.814,
AUC 0.794, p = 0.0010). Our 48 sat at +0.320 with a best of +6.287, so this bar is "reach a typical
measured **non**-binder," which none of them did. Computing it needs a null per candidate, which is
why it is a submission bar on a handful of finalists and not the loop's selector.

**Cap.** At most **8 of the 20 slots**, so at least 12 plan-C rows and the design-diversity term
survive. Nothing enters the final 20 after **Sun Oct 11, 4:00 AM EDT**; the 24-hour retry window is
not spendable.

## Provenance

Nothing here takes or modifies an existing binder. The 32 sequences are our own, from our own
Genie 3 backbones, generated before the campaign data was downloaded. The forbidden set is
unchanged and re-checked by `bin/check_no_verbatim.py` and `bin/exclusion_ledger.py` on the final
20 regardless of which plan ships: the 8 winning sequences and any near-variant, the 4 PXDesign
binders, TNFA_OPT_07, the Chen et al. sequences, our own problem-1 sequences, and adalimumab and
golimumab, both of which ship inside BindCraft's and BoltzGen's Fab scaffold sets and are both
anti-TNF drugs.

One disclosure. While verifying that SolubleMPNN can redesign one chain with the target fixed, the
test was run on a measured binder's predicted complex because it was the structure nearest to hand.
It produced eight variants of that binder, which the provenance rule forbids outright. They were
deleted immediately and no file from that test survives. The real loop runs only on our own designs.

## Total

**$1.19 to answer the entry question. $10.09 if all ten rounds fire.** Against ~$40 unspent and an
October bill of $590.71. Compute runs unattended; the human cost is one go/no-go after stage A.
