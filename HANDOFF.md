# HANDOFF — Anthropic × Adaptyv 2026, Track 3 (all challenges)
# Updated 2026-10-12 9:55 AM EDT. Covers BOTH challenges; problem 1 is closed and archived below.

**Read order on a cold start:** this file → `projects/anthropic-adaptyv-2026/ROADMAP.md` (the live
plan) → `challenges/02-tnf-alpha.md` §1–§48. Then nothing else unless a link below says so.

---

## 🔴 AS OF 2026-10-12 9:55 AM: SIX DESIGNS SHIP. THE SECOND-ORACLE FAILURE WAS WITHDRAWN BY D8.

**Supersedes every status block below, including the 2:55 AM three-design one.** The deadline moved:
problem 2 now closes **Mon Oct 19, 7:59 AM EDT**. Nothing is uploaded yet.

**WHAT SHIPS — six designs, ranked on worse-of-two-species margin.** Full table and the reasoning in
`projects/anthropic-adaptyv-2026/outbox/02-proteinbase-methodology-box.md` (FIELD 2, the live text,
2,825 words / 16,863 chars against a known 20,000 cap). Sequences:
`outbox/prescreen-ship6-2026-10-11/ship6.fasta`.

**THE THREE THINGS A COLD START MUST KNOW:**

1. 🔴 **Objective 2 is unaddressed and the instrument that would have addressed it failed
   calibration.** On the 12 published complexes with an equilibrium endpoint at 7.4 vs 6.0 — the
   assay pair Adaptyv runs — the binding-coupled gate returns a ratio above 1.0 in **12 of 12** and
   its direction accuracy, 6/12, **equals a constant predictor on that subset.** All pH claims are
   withdrawn. `analysis/02-tnf/R1_endpoint_audit_2026-10-11.md`.

2. 🔴 **A pre-registration was breached and the correction stopped on its own ceiling.** The depth
   arm required a second pose oracle from round 4 onward; Chai-1 was never wired in, and all six
   designs are round-4 descendants. The corrective rounds-4–5 re-run was pre-registered
   (`PREREG-CORR-TWO-ORACLE-2026-10-11.md` + 3 amendments) and **stopped** when Chai-1 measured
   157.7 s/fold against a frozen 120 s ceiling — not money, the arm was ~$9.
   `analysis/02-tnf/CORR_phase0_readout.md`.

3. 🔴 **C4 rescored the six on Chai-1 and three looked like failures — then D8 WITHDREW that.**
   `analysis/02-tnf/C4_readout_2026-10-11.md`, then
   `analysis/02-tnf/D8_readout_2026-10-12.md`, which is the one that matters. Five samples per
   design, with the three C4 *passes* as a matched control: **every design throws a sample 20–42 Å
   out, controls included** (42.1 / 23.2 / 40.5 / 41.7 Å). A single Chai-1 draw is not a usable pose
   check on this system, so C4 measured the predictor. In-gate counts over 5 samples:
   **0/5 · 0/5 · 4/5 · 3/5 · 4/5 · 2/5**. What survives descriptively, with no test attached: Chai-1
   never places rows 1–2 on target and usually places rows 3–5 there. **The missing-oracle
   disclosure and the exploratory-not-confirmatory label are unchanged — D8 removed our own
   evidence, not the admission.** C4's single-draw table, for the record:

   | row | design | Chai-1 lrms | ESMFold2 median (n folds) | gate |
   |--:|---|--:|--:|---|
   | 1 | `40_L1r4k6` | 26.13 Å | 1.99 (17) | **FAIL** |
   | 2 | `40_L1r4k1` | 35.87 Å | 1.74 (22) | **FAIL** |
   | 3 | `3_L0r4k0_L49H` | 2.89 Å | 2.46 (15) | pass |
   | 4 | `3_L0r4k0_quadH` | 2.37 Å | 2.63 (5) | pass |
   | 5 | `3_L0r4k0` | 2.92 Å | 3.06 (22) | pass |
   | 6 | `quadH_E3Q_k12` | 36.66 Å | 4.71 (6) | **FAIL** |

   **Ranking NOT changed** under either result — the margin is the calibrated instrument and pose
   agreement was never the ranking basis.

**D8 IS DONE: outcome 3 of the three pre-registered outcomes** — the control scattered. $0.83, 30
structures. Two incidental measurements worth keeping: 5 Chai-1 samples cost **1.5×** one sample
(225–251 s/design), not 5×, because the diffusion batches them; and both D8 containers first died on
a transient `ConnectionError` at the `.remote()` call with nothing billed (failed logs kept as
`runs/depth_logs/corr_d8_b*.FAILED-connerr.log`).

**RUNNING RIGHT NOW:** four parallel verifications of the 18 benchmark pH labels — the reviewer's one
untouched ask. Each is briefed to return NOT FOUND rather than reconstruct a number, to quote the
source for every value, and not to adjust toward our recorded figure.

**OPEN, and all of them are Harish's:** D1 ship six or swap the 7-His design (rec: ship six) · D2
send the drafted PK email at `outbox/02-pk-corrective-arm-and-c4.txt` (rec: after D8) · D3 re-check
the 18 benchmark labels, bounded 12 rows or full 18 (PK's one untouched ask) · D4 upload timing
(rec: before Sat night, to keep the 24h retry window) · D6 row-6 id spelling (rec: the full
`tnfa_H_quadH_E3Q_k12`) · D7 ship all six as ranked or only rows 3/4/5 — **D8 is what decides this**.

**TWO TRAPS, both self-inflicted and both fixed:**
- Row 6 `quadH_E3Q_k12` carries **ZERO histidines** despite its name (unpinned arm-H branch;
  SolubleMPNN removed all four). Flagged in FIELD 2's table.
- Yesterday I wrote **estimated clock times** into four committed files, two of them
  pre-registrations, and every one landed in the future. All reset from git commit timestamps.
  **Run `date` before writing any time into any artifact here.**

---

## 🟢 AS OF 2026-10-11 2:55 AM: THREE DESIGNS SHIP, AND ONE OF THEM CARRIES A TITRATABLE RESIDUE AT NO COST. Nothing running.

**Supersedes the 1:00 AM block below.** C9 (`PREREG-C9-CORE-HIS-2026-10-11.md`, 3 amendments, all
pre-fold) put a histidine in the binder's **own buried core** instead of at the interface, where it
cannot compete with the residues that carry the binding. Readout:
`C9_core_his_readout_2026-10-11.txt`.

**WHAT SHIPS, ranked:**

| # | design | human (15 seeds) | mouse | monomer | pI | His | prescreen |
|--:|---|--:|--:|--:|--:|--:|---|
| 1 | `tnfa_corrected_3_L0r4k0_L49H` | **+7.167** | 7.437 | 0.900 | 4.91 | **1, buried 5/5** | batch_duplicate |
| 2 | `tnfa_corrected_40_L1r4k1` | +7.706 | 7.207 | 0.885 | 4.65 | 1 (interface, inverted) | pass |
| 3 | `tnfa_corrected_3_L0r4k0` | +6.971 | 7.476 | 0.911 | 4.83 | 0 | batch_duplicate |

Rows 1 and 3 are a **matched pair one residue apart**. Row 1 is ranked first because the organisers
rank pH-selectivity first and affinity third, and it is the only design carrying a mechanism; the
order is a declared nomination priority, not an affinity prediction.

🔴 **The pair trips `batch_duplicate` on both members** (0.95 identity / 0.80 coverage within a
batch; rank 8 of 10 in the prescreen's own disqualification order). `40_L1r4k1` + `L49H` alone both
read `pass`. Harish took the flag knowingly at 2:55 AM to get the in-assay control that problem 1
did without. **This must be declared in the methods, not left for the reviewer to find.**

**Why C9 worked where seven arms failed:** the histidine is buried 12-16 Å from the target with no
polar partner inside 7 Å, so it never competes with Arg27/Thr54/Tyr20. L49H beat its parent on
**fifteen seeds each** (+7.167 vs +6.971), and the gain **grew** on ten unseen seeds (+0.33) rather
than deflating as the leader's did in C2.

**What is NOT claimed:** no pH switch is demonstrated. ESMFold2 is pH-agnostic, no pKa was computed,
and the predicted mechanism is **fold destabilisation at pH 6.0** argued from established biophysics
(influenza HA, diphtheria T-domain). Its failure mode is **loss of structure, which the assay cannot
distinguish from aggregation** — the methods document says so outright.

---

## 🟢 AS OF 2026-10-11 1:00 AM: THE SHIP SET CLEARS THE ORGANISERS' MONOMER FLOOR, THE HEADLINE MARGIN DEFLATED BELOW THE BINDER MEDIAN, AND THE INTERFACE IS PROVEN LOCALISED. Nothing running on C1/C2/C3.

**Supersedes the Oct 9 block below on three points.** Pre-registered at `fd513b1` before any fold
existed (`PREREG-CONFIDENCE-TRIAD-2026-10-11.md`). 282 folds, ~$15. Results in
`C1_monomer_floor_2026-10-11.tsv`, `C2_pooled15_margins_2026-10-11.tsv`,
`C3_interface_specificity_2026-10-11.tsv`.

**WHAT SHIPS: `tnfa_corrected_40_L1r4k1` + `tnfa_corrected_3_L0r4k0`.** The backbone-3 slot moved
off `3_L4r5k2` on the pre-registered rule, not after the fact.

| | result | bar | verdict |
|---|---|---|---|
| **C1** monomer floor | **12 of 12** clear 0.70; ship set 0.885 / 0.910; median 0.885 vs the parents' 0.824 | M1 ≥ 0.70 | **PASS** |
| **C2** fresh seeds 6-15 | leader +7.657 fresh, **pooled 15-seed +7.706** | R1 ≥ +7.8144 | **FAIL** |
| | all four ≥ +6.347; order replicates at **Spearman +1.000** | R2, R3 | **PASS** |
| **C3** Ala scan | interface drop **3.927** vs distal **0.406**, 9.7x, exact p **0.0043** | S1/S2/S3 | **PASS** |

🔴 **Limitation 50 must be rescoped.** Its "no design in this submission clears the
monomer-foldability floor… the strongest single reason to expect these designs not to bind" is the
**Mosaic 35**, measured at 0 of 35. The depth-12 clear it 12 of 12, and both shipped designs sit
above the median of the organisers' own 150 assayed designs (0.853). The cross-tool comparison stays
order-of-magnitude placement per §8.5; the 12-vs-100-parents comparison is matched and firm.

🔴 **No design clears the measured binder median any more.** +8.031 was a 5-seed draw; ten unseen
seeds give +7.657 and the pooled 15 give +7.706, against the +7.8144 binder median. Per decision
rule 1 the pooled number is now the reported figure everywhere, and the claim becomes "beats the
median thing that did not bind, does not reach the median thing that did." The ordering, by
contrast, is solid: Spearman +1.000 across ten unseen seeds.

🟢 **The margin is interface-localised, with a matched distal control.** Six interface alanines drop
the margin a mean 3.927; six distal alanines drop it 0.406. **R27 is the dominant anchor** — R27A
reads +0.283, into null territory, a larger effect than His61's. E62A and K53A are not load-bearing.
The in-run parent reproduced +8.031 at +8.015. This is the strongest mechanistic statement the
project can make about its own design and it belongs in FIELD 2.

---

## 🔴 AS OF 2026-10-09 10:10 PM: THE SECOND ARM IS ALSO A NEGATIVE. NOTHING DISPLACES `40_L1r4k1` AT +8.031. Nothing running. Nothing spending.

**READ THIS FIRST. It supersedes every block below.** Detail in METHODS **§6.12, §6.13, §6.14** and
AMENDMENTs 1-3 of `analysis/02-tnf/PREREG-CONSTRAINED-RESTART-2026-10-09.md`. ~1,570 folds today,
**~$38**. Verified against `modal app list`, not assumed.

### What ships, and the one decision left

**`tnfa_corrected_40_L1r4k1`, 5-seed human margin +8.031**, is the best design in this project and
the only one above the measured binder median (+7.8144). It was not displaced by anything today.

**D1 is the only open decision and it is Harish's:** which of the 12 depth-arm designs to submit.
Three structural clusters; **backbone 16 fails on both species and drops.** With mouse included:

| design | bb | human | mouse | min | pH-clean |
|---|--:|--:|--:|--:|:-:|
| `40_L1r4k1` | 40 | **8.031** | 7.207 | 7.207 | yes |
| `3_L0r5k2` | 3 | 7.504 | 7.522 | **7.504** | **NO -- pI 6.63 in the assay window** |
| `40_L1r4k6` | 40 | 7.415 | 7.365 | 7.365 | yes |
| `3_L4r5k2` | 3 | 6.378 | **8.686** | 6.378 | yes |

10 of 12 clear the non-binder median on BOTH species; 1 of 12 clears the binder median (human only).
Suggested: `40_L1r4k1` plus one from backbone 3 -- `3_L4r5k2` for the strongest mouse number in the
set, or `3_L0r4k0` (6.967/7.581). ⚠️ **CORRECTION 2026-10-11 1:10 AM: this line said `3_L0r4k0` was "clean" and avoided the Glu flag. It is not. `depth12_liability_2026-10-09.tsv` records n_flags=1 for BOTH — E at 28% in `3_L0r4k0` and 27% in `3_L4r5k2`. Re-run confirms. The liability axis is a TIE between them, and this prose was carried into a D1 decision table before it was checked against the committed artifact.** Fewer than 20 is
explicitly fine. **`3_L0r5k2` is the trap: best cross-species minimum and the only liability failure.**

### The v3 arm, in one paragraph

6 lineages / 4 backbones / 8 children / mouse trimer every round / worse-of-two selection /
unconstrained. **Stopped itself at round 10 of 16 on pose regression**, 960 of 1,536 folds, ~$23.
Ten rounds never beat the seeded parent of 0.6655. Its human tail -- the 14 best by human pose,
which the selector never carried -- was margin-scored at 5 seeds: best **+7.637**, **B1 FAIL (0 of
14 above +7.8144), B2 FAIL (0 above +8.2091)**. A negative on the selector and on the bars.

🔴 **The transferable lesson, and it was a design error of ours:** mouse scored uniformly ~0.2 below
human, so `min(human, mouse)` was mouse almost always and the arm was **a mouse-only run that
discarded its human gains in selection**. Human `ca_sc_dockq` reached **0.7776** -- better than any
design this project has made -- while the selector's ceiling was 0.5427; 30 designs cleared 0.60 on
human and **zero** did on the worse-of-two. The +0.762 cross-species Spearman that justified
mouse-every-round was measured ABOVE the noise floor; inside the floor it is +0.280, and the
population fell into the floor by round 3. **Next time: primary species as selector, secondary as an
END GATE, and measure the per-objective score GAP before choosing a composite selector.**
`LESSONS-FOR-NEXT-PROBLEM.md` §§9-12.

### Objective 2 is closed, with evidence rather than silence

**No design can be rated favourably, and the reason is geometric.** Of the 12: **0 have the release
direction available, 7 have it INVERTED** (His61 sits 2.18-2.49 A from a target carboxylate against
4.73-5.63 A to LYS65 -- protonation tightens the grip, which is problem 1's direction), and **5 carry
no histidine at all**. Charge swing +0.96 to +1.41 units, uniform.

And nothing could have told us otherwise: the campaign released **no pH column across 1,440
designs**, so there are no labels to calibrate against -- against 354 labelled binders for objective
1 and 154 labelled mouse calls for objective 3. Three instruments were built and all three failed
their controls (`his_cation_gate` 0 PASS on 9 real crystallographic TNF-alpha complexes, one of them
presenting 32 interface histidines; `dddg_elec` at chance on 82 labelled variants; the PROPKA
linkage gate with within-design noise exceeding its between-design signal). Installing the mechanism
also fails by matched control: 0.6349/0.5053/0.6203 unconstrained against 0.0126/0.0309/0.0772 with
two histidines forced, same parent, same seed, 94-95% identity.

### ⚠️ A sequence-identity error found in our own work -- read before any new analysis of the 12

Several design ids carry **two distinct sequences** (an aborted round-2 run left a parallel
`depthB2`/`depthB2v2` tree). A first-match glob selected **different molecules for different
analyses**: 3 of 12 had their sequence-based screens run on a sequence at **0.446-0.663 identity** to
the one actually scored. The **margins are unaffected** -- all 12 replication folds verified to match
one of their own design's folds at identity 1.000 -- but the prescreen and liability screens were
re-run, and the structural work was recomputed on one canonical molecule per design.

**`analysis/02-tnf/depth12_canonical_sequences_2026-10-09.tsv` is now the single source of truth for
these twelve sequences. Read it; do not glob the run directories.**

### Re-run on the canonical set, both clean

- **Pre-submission screen 12/12 pass**, now with PDB, SwissProt, THPdb **and USPTO patents** all
  searched (prior-art arm 99.7 s vs 12.8 s without patents). Still unsearched: the three antibody
  arms (PLAbDab 404 at OPIG) and `proteinbase_public`; recorded per row.
- **Liability 1 of 12 flagged**: `3_L0r5k2` (pI 6.63 inside 6.0-7.4, near-neutral at both pH).
  Three carry a lone Glu-composition flag at 27-28%. Zero cysteines, sequons or deamidation motifs
  across all twelve.

### Still to do

| # | task | who | time |
|---|---|---|---|
| 1 | ~~D1: pick what ships~~ — **FINAL 2:55 AM: THREE designs — `40_L1r4k1` + `3_L0r4k0` + `3_L0r4k0_L49H`**, the last two a matched pair one buried histidine apart. Harish accepted the `batch_duplicate` flag on the pair to put the control in the lab. Earlier: revised 1:00 AM on C2 evidence from `3_L4r5k2` to `3_L0r4k0`.** The backbone-3 slot moved off `3_L4r5k2` under the pre-registered pooled-15-seed rule (+6.971 vs +6.424, and `3_L0r4k0` is also Glu-flag-free with the set's best monomer pLDDT). ROADMAP §'D1 — ANSWERED'. | Harish | ✅ |
| 2 | Rewrite methodology box FIELD 2 -- still describes the 35 Mosaic designs | me | 90 min |
| 3 | Upload, designate, attach | me | 30 min |

**Clocks:** last upload preserving a 24 h retry **Sun Oct 11 07:59 EDT**; hard close Mon Oct 12
07:59. All 24 gates green at this block's commit.

---

## 🟡 SUPERSEDED — AS OF 2026-10-09 1:30 PM: THE DEPTH ARM REPLICATED ON UNSEEN SEEDS. THE MOUSE DIMER WAS THE WRONG CONSTRUCT. THE 12 DESIGNS ARE 3 FOLDS. Nothing running. Nothing spending.

**READ THIS BLOCK FIRST. It supersedes the 9:15 AM block immediately below, which is correct but
incomplete and overstates two things.** Full detail in METHODS **§6.12**. 480 folds on H100, seeds
1-5 with 42 excluded, **$11.64**. Verified against `modal app list`, not assumed.

**The control ran first.** Re-scoring the 12 seed-42 pairs reproduced
`depth_margins_2026-10-09.tsv` at **12 of 12, max absolute difference 0.00000**.

| | seed 42 | seeds 1-5 | verdict |
|---|--:|--:|---|
| clearing +6.347 | 10 / 12 | **10 / 12** | the level replicates |
| median margin | +7.058 | +6.938 | -0.120 |
| best | +7.492 `40_L1r4k6` | +8.031 **`40_L1r4k1`** | **the leader changed** |
| Spearman between the orderings | — | **0.538** | the ranking does NOT replicate |

**So the margin can say which cluster to ship and cannot say which member.** §6.10c's lesson on a
second population: a best-of-N on single seeds finds a real tail and gets the order inside it wrong.

### Four things that are now known and were not at 9:15 AM

1. 🔴 **The mouse DIMER is the wrong construct and every mouse number in §6.10d rests on it.** On a
   mouse trimer the dimer **inflates** the margin by a median **+16%** (spread -78% to +40%), is
   **6.8x noisier** (SD 1.520 vs 0.225), and produced a false reading: `40_L5r5k6` read **+1.579**
   on the dimer ("does not engage mouse") and **+7.254**, mid-pack, on the trimer. §7's adalimumab
   control predicted the dimer would *lose* 14%; it *gains* 16%, so that control does not transfer.
   **Why the dimer existed:** §6.6's OOM is a **34.24 GiB allocation inside the gradient
   computation** on a 48 GB L40S — a Mosaic design-time limit. Scoring builds no gradient graph and
   a mouse trimer is 551 residues against the human trimer's 554 we fold throughout. All 12 trimer
   runs completed with **zero** OOM at 28.4 s/fold. The constraint was carried into a stage where it
   never applied.
2. **The species do not track, measured trimer against trimer for the first time: Spearman
   +0.084.** The dimer flattered it at +0.448. The level is fine on both species (all 12 beat their
   own mouse-trimer null); the ranking does not transfer. **No mouse labelled control exists**, so
   "11 of 12 clear +6.347 on mouse" means *beats its own null by more than the human non-binder
   median margin* — not that anything would bind mouse.
3. **The 12 designs are 3 folds.** Foldseek TM-align, binder chain only: **3 clusters at TM >= 0.5**
   under single, complete and greedy linkage alike, and they are the parent backbones exactly —
   **40 (x7), 3 (x3), 16 (x2)**. Within-backbone TM **0.982-1.000**; between, 0.432-0.490. Method
   validated by reproducing the 48-design precedent at max abs difference **0.0**. The set is worth
   about **3 slots, not 12**, and design diversity is one of three stated selection criteria.
4. **What the bar actually is.** +6.347 is the measured **non-binder median**, so half of all
   measured non-binders clear it by construction. The best design beats **70% of non-binders and
   17% of binders**; the worst, 43% and 0%. The highest non-binder (8.625) exceeds the highest
   binder (8.209), so the instrument's top end carries no label information. Stage A's best sat at
   ~47% / 8%, so five rounds moved the leader to 70% / 17%: real, and short of the target.

### 🔴 TWO CORRECTIONS TO WHAT I WROTE EARLIER TODAY

- **"The 12 separate completely from the 48 on `design_mean`" is wrong.** Under replication `16_s1`
  moves 8.599 -> **9.145**, past stage A's best of 8.862. It is **11 of 12**, not 12 of 12. Built on
  one draw.
- **"+6.287 is wrong, the artifact says +6.027" was backwards** and is retracted. METHODS §6.10c
  reads `22_s1` at seed 42 = **+6.027** and 5-seed median = **+6.287**, under "the best margin
  replicates on seeds it was not selected on". Both are real; **+6.287 is the replicated one**. The
  nine places carrying +6.287 were NOT swept and should not be.

### Screens on the 12, all clean, all new

- **Prescreen 12/12 pass**: whole-sequence identity to the 4,964-entry corpus **0.000**,
  binding-region 0.28-0.37 against a 0.80 cut. Run `--skip-prior-art` as both precedents were, so it
  means no known-binder match and no within-batch duplicate, **not** no public prior art.
- **Liability 11/12 clean on pH and charge**: pI **4.53-5.47** for eleven, against measured binders'
  4.53-5.26 and stage A's median 7.01. Zero cysteines, sequons, deamidation motifs. `3_L0r5k2` is
  the exception at pI 6.63, inside the assayed window.
- **Objective 2 is unaddressed and the composition says why:** 5 of 12 carry **zero** histidines, 7
  exactly one, none more. The pH 7.4->6.0 swing is ~**+1 charge unit for every design** — uniform,
  small, and from acid protonation rather than a histidine switch.

### The decision this leaves

**D1 is still Harish's and it is now a different question.** Not "ship 10 of 12" but "ship the best
survivor of each of 2-3 clusters, chosen on something other than the margin, and say so". Backbone
**16** fails the bar in every read (human seed 42, human 5-seed, mouse trimer) and is the cluster to
drop. Fewer than 20 is explicitly fine.

**W1 is DONE:** the out-of-sample AUC **0.674-0.702** now appears in METHODS §4.5, limitation 51 and
the methodology box, each cross-referencing §6.11. **All 24 gates green.**

---

## 🟡 SUPERSEDED (correct but incomplete) — AS OF 2026-10-09 9:15 AM: A DEPTH ARM RAN FIVE ROUNDS AND 10 OF 12 DESIGNS NOW CLEAR THE PRE-REGISTERED MARGIN BAR.

**READ THIS BLOCK FIRST. It supersedes the 2026-10-08 blocks below, which said the design search
was closed. It was reopened on 2026-10-08 at 10:27 PM with Harish's explicit approval and it
worked.**

✅ **NOTHING IS RUNNING.** Verified against `modal app list`, not assumed. Last jobs finished
9:00 AM (45 pose folds + 12 null folds, both clean, 0 errors).

### The result, in one table

| | the 48 (0 optimisation rounds) | the depth arm's 12 (5 rounds) |
|---|---|---|
| margin, median, single seed | **+0.320** | **+7.058** |
| best, single seed (42) | +6.027 | **+7.492** |
| best, **five-seed median (seeds 1-5)** | **+6.287** | **NOT MEASURED** |
| clearing **+6.347**, single seed | **0 of 48** | **10 of 12** |
| best ligand RMSD | 15.034 A | **1.575 A** |
| best CA sc_DockQ | 0.0865 | **0.6400** |

🔴 **THE DEPTH ARM'S MARGINS ARE SINGLE-SEED AND UNREPLICATED. THIS IS ITS BIGGEST WEAKNESS AND
THE NEXT MEASUREMENT ANYONE SHOULD RUN.** §4.6 puts single-seed margin noise at 0.858 and a
pure-noise best-of-48 at 1.91. §6.10c exists because the 48's +6.027 "had exactly the shape of a
selection artefact" — it was answered by re-folding the top 8 and their nulls at five seeds
EXCLUDING the selection seed, where the best held at +6.287. The depth arm has had no such
replication, so its +7.492 is a best-of-12 single draw carrying the same risk. **96 folds, ~$3.56,
~1.5 h** re-folds the twelve and their nulls at seeds 1-5. Until then the claim is "ten of twelve
clear the bar on one seed."

A correction caught by a peer session on 2026-10-09 and verified here: an earlier note in this
file said the 48's best margin is "+6.027, not +6.287". That was backwards. **+6.027 is the
single-seed value and +6.287 is the independently replicated five-seed median** — both are real,
+6.287 is the better-supported one, and it is live in roughly nine places that are correct as
written. Do not sweep them.

The **+6.347** bar is the measured non-binder median from `labelled_control_2026-10-08.tsv`,
committed to git at **`5002b49`** before any depth-arm design existed. The measured BINDER median
is **+7.814** and **none of the 12 reaches it on a single seed** — ceiling +7.492. ⚠️ **Superseded
by §6.12: at 5 seeds the ceiling is +8.031 (`40_L1r4k1`), which IS above the binder median and beats
9 of the 12 measured binders.** On single seeds every one sits in the band
between a typical measured non-binder and a typical measured binder.

Same generator, same sequence designer, overlapping backbones (backbone 3 is in both lists). The
only difference is five rounds of predict-then-redesign.

### What ran, and where it is

| artifact | what |
|---|---|
| `analysis/02-tnf/PREREG-DEPTH-ARM-2026-10-08.md` | the bars, committed first |
| `analysis/02-tnf/depth_rounds/round{1..5}.tsv` | 32 designs per round, pose-scored |
| `analysis/02-tnf/depthA_pose_2026-10-08.tsv` | stage A, 28 scored, 4 cleared the 10 A gate |
| `analysis/02-tnf/seed68_partial_pose_2026-10-09.tsv` + `seed45_pose_2026-10-09.tsv` | the 68, complete |
| `runs/A-margin12-out/Amargin12` | the 12 own-sequence nulls behind the margins above |
| `bin/run_depth_rounds.py` (8 selftests) | the round runner, `--one-round`, `--parents`, `--resume-after` |
| `bin/depth_loop.py` (8 selftests) | scoring + the oracle guard + the stale-fold guard |
| `bin/depth_report.py` | per-lineage round review |
| `bin/comp_filter.py` (6 selftests) | the chemistry filter |
| `bin/validate_selection_rule.py` (4 selftests) | the 16-target validation |

Per-round best CA sc_DockQ: **0.6057 (stage A) → 0.6249 → 0.6484 → 0.6148 → 0.6343 → 0.6400.**
Population moved much more than the leader: median ligand RMSD **26.0 → 4.564 A**, designs inside
the 10 A gate **9 → 24 of 32**. Spend on the arm: **192 folds + 12 nulls + 68 pose folds ≈ $10.**

### THE THREE THINGS THE DESIGNS STILL DO NOT HAVE — read before submitting any of them

1. **No pH mechanism.** Of the 8 best, **3 carry zero histidines and 5 carry exactly one.** The
   pH 7.4 → 6.0 charge swing they show (+1.0 to +1.4) is **acid protonation, not histidine**, and
   its sign at the interface is unknown. The loop had **no histidine constraint**, so it bred the
   mechanism out of 9 of its 32 round-1 designs. Objective 2 is unaddressed.
2. **No mouse data.** Never folded against mouse TNF-alpha. The only evidence is the 48, where
   human and mouse margins correlate **+0.107** and the best mouse design ranked 44th of 48.
   Objective 3 is unaddressed.
3. **The margin instrument is weaker than this project long believed.** See the correction block
   below: its honest out-of-sample discrimination is **~0.70**, not 0.901.

### THE AGREED NEXT STEP, not yet started

Harish called the depth arm at round 5 and asked for **a full restart with the constraints baked
in**: fold against **human and mouse every round** selecting on the worse of the two, and
**require 1–2 histidines** at cation-reachable interface positions in every redesign. Design
notes and the costing are in `projects/anthropic-adaptyv-2026/LESSONS-FOR-NEXT-PROBLEM.md` §1 and
the "where that leaves the architecture" reasoning in the ROADMAP. **Nothing is pre-registered for
it yet and nothing has been launched.**

Mechanics known: `--omit_AAs` can forbid a residue but **cannot require one**; requiring histidine
means fixing or biasing positions, and `bin/mpnn_constraints.py` builds those files but its
`MAX_FORCED_HIS = 8` must drop to **2** — its current setting is what pushed the 48 outside the
measured binder band in the first place.

### 🔴 CORRECTIONS TO THIS PROJECT'S OWN RECORD, measured 2026-10-09 on all 1,440 released designs

`analysis/02-tnf/SELECTION-RULE-ALL-TARGETS-2026-10-08.md`. 354 binders, 16 targets, 113,550
co-fold rows. **Three of four headline findings from the TNF-alpha slice did not survive:**

| claim, from the 150-design slice | measured on all 16 targets, within-target |
|---|---|
| best in-silico metric AUC 0.963 | **0.748**, and **0.674–0.702 out of sample** |
| `plddt_binder` anti-correlates (AUC 0.000) | **0.678 — normal direction** |
| interface size discriminates at 0.954 | **0.633** |
| the chemistry filter enriches 4.04× | **1.18×**, p = 0.055 |

**What survived and generalises: optimisation depth.** 16.2 / 20.5 / 26.7 / 32.9 / **52.9%** across
0, 1, 2–3, 4–7, 8–12 rounds, trend **p = 1.1e-16**; within target **37.5% vs 17.4%**, Fisher
**p = 2.1e-12**; for **Genie 3 specifically 38.6% vs 12.1%** (p = 0.0003) and **SolubleMPNN
36.6% vs 18.5%** (p < 0.0001) — our exact pipeline, a 3.2× lift. It also survives the strict
both-vendors-agree label (29.0% vs 12.5%).

**Depth does NOT buy affinity:** within target, Spearman(rounds, log K_D) among binders = **−0.092**.
It converts non-binders into weak binders.

**The labels themselves disagree.** Of 1,235 designs assayed by both vendors they disagree on
**35.0%** of the 389 where either saw binding, and **28.5% of the 354 published binders rest on a
single vendor.** No ranker can reach AUC 1.0 against that, and small AUC differences are not
meaningful.

**One number I got wrong in BOTH directions, now settled:** the 48's best margin is **+6.027 at
seed 42** and **+6.287 as the five-seed median** (§6.10c, seeds 1-5, excluding the selection seed).
I first repeated +6.287 without its provenance, then "corrected" it to +6.027, which was backwards
— the replicated figure is the stronger one. And "the chemistry-rejected pool poses better" was a 15-design artifact —
the complete 68 gives **4 of 56 = 7.1%** clearing the pose gate against the filter-passed pool's
**14.3%** (Fisher p = 0.43, so not significant either way, but the direction reversed).

### Bugs found and fixed in the arm's own tooling, all with regression tests

1. **Beam collapse.** A global top-4 put all four slots on one backbone after ONE round. Fixed to
   best-per-lineage (`select_per_lineage`, T7 + a mutation test).
2. **Stale folds.** An aborted round-2 run's 20 folds shared a Volume name, were silently recovered
   into the next round's scoring, and dropped backbone 3 a second time. Fixed with an expected-id
   regex plus a per-launch `RUN_TAG` (T8 + T8b mutation).
3. **Discarded fold logs.** `capture_output=True` hid the per-fold timings, so a slowdown could not
   be diagnosed. Now written to `runs/depth_logs/`. This also revealed that **my Volume-count
   progress estimates were undercounting all night** — the rounds were never slow, folds ran at a
   steady 55.0 s throughout.

---

## 🟡 SUPERSEDED — AS OF 2026-10-08 9:10 PM: the Genie arm failed, and the instrument has now been controlled and CLEARED. Nothing running. Nothing spending. The design search is CLOSED.

✅ **NOTHING IS RUNNING.** `modal app list` shows `ap-gz7W6OayBW3WfvYx5RwwI3` (`Aposctrl5`) in
state **stopped**, finished around 7:20 PM; all **168 of 168** folds landed locally
(`runs/A-posctrl5-out/Aposctrl5`, 42 designs × 4 extra seeds). Total Modal spend for the day
~$3.00. No job has been launched since. **Caution for anyone re-running the contact census or the
margin on that tree:** `iface_contacts.py:176` derives its row id from the containing directory, so
`Aposctrl5` emits 4 rows per id and a `{row['id']: row}` join silently keeps the last. Collapse
seeds explicitly first.

🆕 **THE POSE CONTROL RAN TONIGHT AND PASSED.** Bars pre-registered and committed at `a4974d3`
before any number existed; result at `analysis/02-tnf/POSE-CONTROL-RESULT-2026-10-08.md`, new
METHODS §6.10g, commits `0da0b5a` and `369c9ef`. $0 spent — 4.3 MB of HTTP and local CPU.

- The 12 measured binders folded in **our** configuration reproduce the campaign's own ESMFold2
  pose of the identical sequence to **median ligand RMSD 1.57 A**, Fnat 0.942, CA sc_DockQ 0.866,
  worst case 3.01 A, 0 of 12 refused. Bar was 10 A and Fnat 0.10.
- Our 40 designs read median LRMS 31.1 A, best 15.0 A. **The worst measured binder is 5× better
  placed than our best design and the distributions never overlap.** §6.10f's 31 A is a verdict on
  our designs; the predictor is exonerated. "CA-only is deflated" is dead as an excuse — a real
  binder reaches 0.866 on the same CA-only scale.
- Still uncalibrated: designed-against-predicted. The release has **no designed structure for any
  of the 150** designs, only per-arm predictions, so the control is prediction-against-prediction
  of one sequence. The 0.23 threshold remains imported, not reproduced.
- 8 of the 12 measured binders carry a **null `sc_dockq` on every row** of the released co-folding
  table — exactly ranks 1-8 — while the protocol puts `pose_dockq` in its mandatory-non-null set.
  The pose gate was not recorded, in the public release, for the recipe that made 8 of their 12.

🆕 **OUR 48 ARE ONE FOLD, AND IT IS NOT THE WINNERS' FOLD.** Foldseek TM-align 48×48: median
pairwise TM 0.458; at the pre-registered TM ≥ 0.5 there are **3 single-linkage clusters with 46 of
48 in one** (complete linkage 18 — the verdict survives the most conservative read). So the honest
claim is **48 sequence families, 3 structural clusters**: we bought sequence breadth and almost no
structural breadth. Against the 12 measured binders' own folds, **0 of 48 reach TM 0.6 for the
8-member winning family** (best 0.570, `tnfa_corrected_11_s1`) while **12 of 48 clear it for the 4
PXDesign binders** (best 0.825). Our fold space overlaps the family that went 4/57 and misses the
one that went 8/10 in its deep cell.

**Two pre-registered arms ran on 10-07 and both returned nulls**, and both
carried hard stops written before the run. Those stops are honoured: **no further design arms.**

| arm | what it varied | pre-registered bar | result |
|---|---|---|---|
| **A** (§45) | the gradient estimator — 4-sample averaging, momentum 0.9 → 0.0 | ≥ +0.12 acts, < +0.02 null | **+0.0078 ± 0.0124 → NULL** |
| **Region I** (§47) | the **epitope** — a second site 15.42 Å away | same bar | **−0.0092 ± 0.0126 → NULL** |

**Twenty-four trajectories now, seven conditions, two structurally unrelated epitopes.** The interface
term improved in none of them. Best `iptm_repred` anywhere is **0.2468** (arm A) against the **0.45**
gate we set before any number existed. 0 of 35 designs clear it (the 10-07 export
of `design_inventory.py --export` regenerated 25 -> 35).

**What survives as the explanation:** term interaction across 20 weighted terms on three legs.
Condition 3 is direct evidence — tripling the interface weights made results *worse*. Testing it
means stripping terms, and the terms *are* objectives 1 and 2, so the suspect cannot be fixed
without abandoning the brief.

**Spend:** ~$36 before today, ~$9 arm A, ~$9 Region I, ~$3 lost to two launch mistakes of mine.
**The $49 wave money is unspent and now has nothing to buy.**

### Arm A's endpoints were the project's best, and that is a trap, not a lead
Median 0.2159, max 0.2468 — above every other condition. **On a null trajectory.** §6.3 is why
endpoints are secondary: an endpoint cannot tell a badly-tuned method from one that is not
optimising. Do not reopen arm A on the strength of its endpoints.

---

## 📌 THE SUBMISSION IS PLAN C, AND THREE THINGS CHANGED TODAY THAT MAKE IT EASIER

**1. 🟢 THE NOVELTY GATE STOPS BEING A SUBMISSION FILTER — portal switches 2026-10-08.**
Simon (Adaptyv), 2026-10-07 6:46 PM:
> "switching to a **sequence based presubmission screening, which will flag only submitted sequences
> with resemblance to known TNFa binders** … **Novelty will still be computed but only after
> submission** together with other metrics on Proteinbase."

Offline tool: **`github.com/adaptyvbio/binder-prescreen`** — *"so that you can check your submissions
(or have Claude check them) before you submit."* Sequence-based, no structure needed.
**Consequence:** problem 1's novelty roulette (opposite verdicts on byte-identical sequences, cost us
a backbone family and the only two-site mechanism) **cannot recur**. Submit the best 20 by our own
ranking. ⚠️ Novelty has not vanished — it moves post-submission and **feeds selection**, so keep
reporting our levels honestly. **`binder-prescreen` was run on all 35 on 10-07; re-run it on
the final 20 before uploading.**

**2. Fewer than 20 designs is explicitly fine.** Tudor, 2026-10-02:
> "It's ok if you want to submit less than 20 … **we will not pick just 1-2** (so a bit more to give
> some statistical power)."
So padding to 20 buys nothing. Relevant because **§9 already says a matched histidine-removal
control is uninformative when the parent does not bind** — 0 of 35 bind, so the 4 control slots are
better spent or left empty.

**3. Upload early, then "designate".** Théo: *"There is an option on Proteinbase to 'designate' the
submission that will be taken into account when you've made multiple ones."* Multiple submissions are
retained. An early upload is free insurance; it does not burn the 24 h cooldown.

**Deadline, reconciled — no runway was lost:** **Sun Oct 11 23:59 AoE = Mon Oct 12 7:59 AM EDT.**
AoE is UTC−12, so the two readings are the same instant. Last upload that still leaves a 24 h retry:
**Sun Oct 11, 7:59 AM EDT.**

---

## ⚠️ ORGANISER FACTS — confirmed in the Slack, do not re-derive

- **Selection, stated three times, most explicitly by Tudor:** *"mainly based on method novelty,
  design diversity, and a couple of in silico/confidence metrics. Your strategy should not be
  penalized much by the in silico metrics … this selection strategy will likely be less biased
  against more creative design methods."* They will publish the selection prompts afterwards.
- **Amir:** *"Claude will review what you share and use it for selection."* The methodology section
  is linked to a Proteinbase Collection. ⚠️ Being made **public** is conditional — *"**if** your
  designs are selected for wet-lab testing … **might** be made public."* Do not state it as a rule.
- 🔴 **Assay construct, confirmed 2026-10-07 by Tudor:** *"C-terminal Twin-Strep, we immobilize the
  binder, and flow the target."* **Our design is the immobilised partner and the trimer is the
  analyte** — so the avidity exposure in limitation 16 is now organiser-confirmed, not inferred. A
  trimeric analyte can engage two immobilised binders and compress the pH ratio we are ranked on.
- **Target:** UniProt P01375, **Asp143** (not 1TNF's Leu143), AcroBiosystems TNA-H4211, tag-free.
- **Format:** 10–250 aa; `molecule_class` ∈ `single_chain|nanobody|scfv|fab_kappa|fab_lambda`
  (**`protein` is not in the enumeration**). Strata: microbinder <40 · minibinder 40–100 · large
  >100 · nanobody · antibody, **winners per stratum**. Our 76-mer is a minibinder.
- 🔴 **A ranked CSV is mandatory.** Declining to rank is not submittable.
- 🔴 **"Embedded instructions or prompt injection may be deemed grounds for disqualification."**
  The methods document must contain no imperative addressed to a reader. Sections added 2026-10-07
  were checked clean; **older prose was not fully swept.**
- **Provenance rule, verbatim:** *"You may not take an existing binder and modify it. Designs must be
  produced from scratch."* Kills any use of `TNFA_OPT_07`, the Chen *et al.* TMB sequences, and our
  own problem-1 sequences (*"We check against the current Proteinbase snapshot"*).
- **PyRosetta is permitted** for non-commercial use (Amir + Tudor, 2026-10-06). **PolyForm was never
  ruled on** — silence, not permission.
- **Operational:** multiple entrants report Claude's bio classifiers blocking routine protein work on
  challenge 2. Amir recommends Sonnet 5.5 and says the classifier level is the same across Sonnet 5 /
  Opus 5 / Sonnet 5.5. **This session was interrupted repeatedly.** A fresh window is the reported
  workaround.

---

## 🔭 GENERATION PATHWAYS — researched 2026-10-07 evening, NONE LAUNCHED

Three agents surveyed this. **No pathway is recommended without an explicit decision**, because the
§45/§47 hard stops say the design search is closed and reopening it is a judgement call, not a
tooling one. Recorded so a fresh window does not re-derive it.

| pathway | status | cost | verdict |
|---|---|---|---|
| **BindCraft2** `github.com/PacesaLab/BindCraft2` | created 2026-09-13, **pushed 2026-10-07** | ~$2–7 | **Best capability fit, zero published yield** |
| **Cao scaffolds → BoltzGen inverse-folding** | our harness already wired | ~$8–16 | Nearly zero setup; His pins at generation |
| **Genie 3** `aqlaboratory/genie3`, Apache-2.0 | public weights | cheap | **8 of the organisers' 12 TNF-α binders are variants of ONE Genie 3 backbone** |
| **Proton-PottsMPNN** | MIT, weights in repo | ~$0 (CPU) | The only model taking protonation state as **input** |
| **Germinal** | 🔴 **TRIED HERE 2026-10-02 AND FAILED** | ~$80 for 20 | **Out** |
| BoltzGen `nanobody-anything` | — | — | Externally measured **zero on TNF-α, both arms** |
| RFantibody · RIFdock · Chai-2 · Latent-X · IgDesign | — | — | No wrapper / 100k CPU-h / not available / needs a parent |

**Germinal is out on measured grounds, not theory.** `runs/egfr-d3-scfv/`: four attempts on
2026-10-02, **zero designs**, abandoned in 52 min with a `STOPPED_germinal_boxed_out` tombstone.
Failures: `No module named 'yaml'` · return code 1 · `No module named 'pkg_resources'` ·
`ValueError: Unrecognized amino acid token: A` inside vendored `colabdesign/iglm/model.py`. Three
never reached the design stage. Also ~$80 for 20 designs (over budget), hard-requires PyRosetta, and
**§26 measured that our ranking instrument substantially fails on nanobody format** while a ranked
CSV is mandatory.

**BindCraft2, what is actually verified:** ships `scaffolds/{VHH,scFv,Fab,ARP}.cif`;
`examples/pdl1_vhh.json` does fixed-scaffold CDR-only design with variable CDR lengths,
`min_scaffold_sequence_retained_final: 1.0` and `max_off_paratope_contact_final: 0.0`;
`pdl1_crossreactive_detarget.json` carries **two orthologs as a native joint objective** plus
negative design; `pdl1_homotrimer.json` exists. License is source-available, free for any purpose
except hosted resale, **no PyRosetta**. 🔴 **Unverified: yield. No paper, no wet-lab numbers.** pH is
not an input. VRAM ≈ 2.0 × (3.4 GB + 38 kB·N²) → full trimer + 100 aa ≈ 30 GB → **one worker on an
L40S; truncate to a protomer pair or an epitope shell.**

🔴 **RULES TRAP:** BindCraft and BoltzGen both ship **adalimumab** and **golimumab** Fab scaffolds.
Both are anti-TNF-α drugs. Using either as a framework against TNF-α is *"taking an existing binder
and modifying it."* The `nanobody_scaffolds/` set is clean. **Check every scaffold against the
target.**

**Honest expectations if any of this ever runs.** The Baker pH paper's TNF-α row: **72 designs → 48
retained binding → 3 pH-sensitive**, best 79× weaker and that at **pH 5.4**, not 6.0. At a 20-design
cap that is **~0.8 expected switches**. The best computational pH-**6.0** result anywhere is **>2×**.

---

## 🔴 2026-10-08 EVENING — THE GENIE ARM, AND THE TWO MEASUREMENTS THAT SETTLE IT

Full write-up in METHODS §6.10a–f. Total spend today ~$35.

**The arm works mechanically.** Genie 3 at 39.9 s and $0.023 per backbone, 3.39 GB peak, 4 chains
of a 4-chain ceiling. **98 of 100** seed sequences clear the 0.70 monomer floor against **0 of 35**
for the Mosaic designs. 48 designs co-folded, best margin **+6.287** on five seeds that excluded
the selected one, which cleared the pre-registered 5.64 bar.

**Then two measurements that should have come first.**

**1. The margin is validated, and our designs fall below NON-binders (§6.10e).** 12 measured
binders vs 30 measured non-binders through our own configuration: **AUC 0.794, p = 0.0010**. On
that scale binders sit at **+7.814** and non-binders at **+6.347**, while our 48 sit at **+0.320**
with a best of +6.287. **1 of 48** reaches the weakest real binder; **0 of 48** reach a typical
non-binder. The pre-registered bar of 5.64 was anchored on TNFR2, a natural receptor, when the
relevant population is designed binders — so it was set *below* the non-binder median. It was met
and it was mis-set; both are in the record.

**2. Pose agreement is near zero (§6.10f).** The protocol ranks on ipSAE **and sc_DockQ**, 4:1, at
every promotion step. We never computed sc_DockQ. It gives median **0.025**, **0 of 40** passing
the protocol's 0.23, **Fnat ≈ 0**, ligand RMSD median **31 Å** — the predictor does not put the
binder at the designed epitope — and it is **uncorrelated with our margin** (r = −0.159). So every
margin in this work scored an interface we did not design.

**What the arm did establish, and it is worth keeping:**

| | |
|---|---|
| sequence variance **1.6×** backbone variance | SD 1.462 vs 0.931; which sequence matters more than which backbone |
| best-of-4 by MPNN score is worthless | 4 of 24 alternates beat the pick; the new best **+6.459** came from a backbone ranked 7th of 8 |
| their 8 binders are **ONE** family | 23 Genie3 designs in 10 families; one family of 8 gave 8/8 binders, the other nine gave zero |
| objective 3 is near-chance | mouse median **−1.264**, below its own scramble; human/mouse r = +0.122 |
| novelty | **16–21 of 48 at level 2**, zero at level 4, driven by fold similarity (median TM 0.732) not sequence (median identity 0.000) |
| prescreen | **48/48 pass**, `outbox/prescreen-genie48/` |

**One design is not bad at anything:** `tnfa_corrected_30_s1` — human +5.814, mouse +1.991, pH
linkage 0.149. Not good at anything either.

**Two dramatic results today were bugs the controls caught before they were reported**: a
design/null display collision in the Stage A margins, and a five-residue register shift in
sc_DockQ that the target-superposition control exposed. Both tools now refuse rather than report
when their own control fails.

**What this closes.** Stage C — 1000 backbones, 200 co-folds, ~$47 — is **not justified**. Not by
the pre-registration's ambiguity clause but by a clear negative on a validated instrument. And the
plan as written was structurally wrong anyway: 1000 backbones × 1 sequence each scales the axis
that matters least.

---

## 🔴 2026-10-08 — THE RANKER WAS NEVER TESTED AGAINST A NULL OF THE RIGHT SIZE, AND NOW IT IS

Two folds, ~$0.35, `analysis/02-tnf/SIZEMATCHED-NULL-2f.md`. Apps `ap-snCV8ziLzEWYsls08s9Vh2`,
`ap-ihYnoYl5TTQ2UhM8vJA4Kp`.

The control band folded on 10-07 (`p2_control_band_2026-10-08.tsv`) shuffles the 164-residue TNFR2
ectodomain, so all five controls score at 302,382 cross-chain residue pairs. The designs are 76 or
84 residues — 219,486 / 227,022 pairs. `pae_interface_mean` averages over those pairs, so that band
was **never a yardstick for the designs**. Mine: I recommended that run without checking
size-matching first.

| null | binder | pae_if_min | pae_if_mean | pairs |
|---|---|---|---|---|
| `neg_shuffled_L76_1` | 76 | 0.854 | **14.248** | 219,486 |
| `neg_shuffled_L84_1` | 84 | 0.855 | **14.996** | 227,022 |

| | n | design mean | median | null mean | beat it |
|---|---|---|---|---|---|
| L76 | 21 | 11.218–16.586 | 14.047 | 14.248 | 15/21 |
| L84 | 14 | 13.945–15.434 | 14.648 | 14.996 | 10/14 |

**25 of 35 beat their size-matched null on the mean** (one-sided binomial p = 0.0083), and **the
same 25 beat it on the min** — so at this configuration the two metrics rank the designs
identically, which is the part of item 2d that was answerable without an MSA path.

**Above chance, and almost nothing biologically.** TNFR2 scores 7.713 where its own shuffles score
~18.99 — a margin of 11.28. Best L76 design: 3.03 below its null, **27%** of that margin. Best L84:
1.05, **9%**. Median design: 0.20 / 0.35, **2–3%**. The median design is not distinguishable from a
shuffle of its own length and composition. §48 reached the same verdict from Anthropic's 150
measured designs; this reaches it from controls folded on our own configuration.

⚠️ Caveats, stated in the file: one draw per length (n=1, no interval), and the 27% assumes the
null-relative gap cancels the size offset to first order rather than exactly. **2d is not closed** —
`pae_interface_min` was selected at AUC 0.901 on the MSA-fed arm and our configuration has none.

### The liability screen fired, and it is near-binding on the submission

`bin/express_qc_p2.py` (thresholds declared before any problem-2 design existed) on all 35.
`analysis/02-tnf/p2_liability_screen_2026-10-08.txt` + `p2_liability_2026-10-08.tsv`.

| flag | hits |
|---|---|
| pI **inside** the assayed 6.0–7.4 | **13/35** |
| pI within 0.5 of an assay pH | 5/35 |
| near-neutral net charge at an assay pH | 15/35 |
| **any pH/charge flag** | **20/35** |
| no flag of any kind | 7/35 |
| composition / homopolymer / GRAVY / free Cys | 0/35 |

pI range 4.49–11.21, median 6.43. L76: 10/21 inside the range; L84: 3/14.

The hazard was predictable from the assay alone and is written into the tool's docstring: problem 2
is measured at **two** pH values and the mechanism is installed with **histidines**, whose pKa sits
between them by construction. The better the mechanism is installed, the likelier the binder's pI
lands inside its own measurement window.

**Consequence for nomination: 20 slots, and only 15 of 35 are clean on both pH and charge.**
Liability can no longer be a tiebreak — it has to be a term in the ranking, or five slots go to
designs sitting at their solubility minimum during the measurement that decides them. Problem 1 lost
a VHH to exactly this (pI 6.38, assay 6.5) and the QC in place then had no pI term at all.

### Timing fact worth keeping
The first fold took ~19 minutes, the second ~4. The difference is a **cold model fetch**: the
container downloaded 11 weight files (1:44) then loaded for 117 s before folding. `score-esmfold2.sh`
sizes `MODAL_TIMEOUT` from the **fold** only, so its 5-minute estimate is blind to the fetch. The
timeout is a ceiling and Modal bills actual use, so nothing was lost — but do not read the estimate
as wall-clock on a cold image.

---

## 🔬 THE CALIBRATION WAS TOO GENEROUS, AND THIS IS STILL OWED IN THE WRITE-UP

We have been quoting the organisers' own **12/150 = 8%** on TNF-α as our calibration, in METHODS
§6.5, limitation 19 and the public methodology box. **Their campaign required only binding.** Their
protocol (`reference/anthropic-binder-design-protocol.md`, TNF-α is target #10) states the goals as
*"1) high-affinity binders zero-shot and 2) high overall hit rate"*, contains **no pH requirement at
all**, and makes cross-species *"a secondary objective pursued only without compromising affinity or
hit rate."*

**So 8% is the one-objective ceiling, not our calibration.** We are asked for three things at once,
and the added one has no computational precedent at pH 6.0. All three places need qualifying —
it reframes our negative result as the three-objective version of a task whose one-objective version
runs at 8% on the organisers' own instrumentation.

---

## ✅ CORRECTIONS SHIPPED 2026-10-07 — all guarded, do not reintroduce

| what was wrong | now | guard |
|---|---|---|
| Mosaic installed from an **unpinned** git URL all campaign | pinned `b94b9d4eb99…`, in the wrapper **and** the tracked patch | `bin/check-pins.sh`, mutation-tested |
| METHODS §2: positional 68 *"deleted in mouse"*, with an argument built on it | it is **H→Y**; the single gap is at **mature 71 (Ser)**, not an epitope position | `bin/check_species_map.py`, 6 mutations |
| *"an L40S cannot hold three protomers"* | human trimer = 456 res / **532 tokens, 21.7 s/step, runs**. The **dual-species** graph with a mouse trimer (~976 tokens) is what OOMs | stated in §6.6 |
| methodology box: `+20%` effect size | **`+31%`** — §11 fixed it at 7:35 AM and it was never carried across | — |
| ROADMAP: methodology *"linked to a public Collection"* | conditional — *may* be public *if* selected | — |
| novelty gate = *"3 of 4 checks"* | a **4-level scale, bar at Level ≥ 3** | — |

**`bin/gate_sweep.py` now runs 24 gates** (`check_species_map` and `check_published_counts` added
since the 21 of 10-06). The methodology box no longer states a gate count at all, which is why
`check_published_counts.py` audits every surface that does -- it was extended on 10-08 to cover
gate counts after this file and ROADMAP.md were both found still saying 22.
⚠️ I briefly wrote "15 of 15" into that box from a bad regex — fixed, but re-read it before upload.

---

## 🔧 TOOLING ADDED 2026-10-07 — one command each

```
python3 bin/check_species_map.py                  mouse mapping + gap + Region I, from sequence
python3 analysis/02-tnf/region1_verify.py         Region I by motif, in all three numbering schemes
bash    bin/check-pins.sh                         Mosaic revision pin, wrapper AND patch
python3 analysis/02-tnf/loss_traj.py LOG --block 13   the trajectory read; the ONLY decisive statistic
bash    bin/probe-grad-noise.sh  <tag> <L> <seed>     arm A (GRAD_SAMPLES/MOMENTUM_SOFT env)
bash    bin/probe-region1.sh     <tag> <L> <seed>     the Region I arm
python3 bin/gate_sweep.py                         all 24 gates
python3 bin/express_qc_p2.py <designs.csv>        liability screen (pI at BOTH assay pH values)
python3 bin/build_sizematched_null.py <design> <out.faa>   a null at a design's own length
python3 bin/pae_interface.py --dir <run>          pae_if_min / pae_if_mean / n_pairs
python3 bin/check_published_counts.py             limitation AND gate counts, every surface
```

**Launcher guards, learned the hard way today:** a tag containing whitespace is refused, length and
seed must be digits, and every launcher echoes its resolved config **before** launching. This exists
because `set -- $a` in a **zsh** loop does not word-split, so four runs silently became four
identical `L=76 seed=0` runs. Also: **every TNF launcher must name `--epitope` on both legs** —
`DEFAULT_EPITOPE` is problem 1's **EGFR** site and inheriting it designs against the wrong protein.

---

## 📋 WHAT IS LEFT — all writing, except the upload

1. **Three documents now overstate the ranker**, listed in `analysis/02-tnf/CONFIG-COMPARABILITY-2d.md`:
   METHODS §4.5, limitation 51, and the box's FIELD 2 point 4 each present `pae_interface_min` as
   selected at AUC 0.901, which was measured on the MSA-fed arm. 2f adds the finding that at **our**
   configuration the min and the mean rank the 35 identically, so the claim to make is "either metric,
   same order, margin 2–3% of a real binder's" — not an AUC we did not measure here.
2. **METHODS:** fold in arm A (§6.6) and Region I (new §6.7) with both hard stops recorded as
   honoured; qualify §6.5's 8% per the section above; add the pH-6.0 ceiling with citations
   (Ahn *et al.* bioRxiv 2025.09.29.678932; Schröter 2014 doi:10.4161/19420862.2014.985993); state
   that **no structure predictor represents the pH-6.0 state**; note our **2** His-cation contacts sit
   at the published floor where working designs had **8 and 11**; record Germinal as an attempted,
   failed arm; add the size-matched null band and the liability screen.
3. **Sweep older prose for reader-addressed imperatives** — disqualification risk, not style.
4. **Three stale claims — resolved 2026-10-09, two of the three pointers were wrong.**
   `submission-basis-p2.md` was **already fixed** on 10-08 (item 7 reads `single_chain` with a dated
   note). `setup-checklist.md:24` **is fixed** — the top line no longer reads as a settled "avoid
   it" when the status is installed/never-run with the licence question open. Problem 1's **§27 is
   the wrong reference**: it is limitation 27, on the tethered-versus-extended footprint, and has no
   PyRosetta content. The PyRosetta text lives in **§12 Declarations**, already corrected 10-05 with
   a 10-08 addendum. ⚠️ **But §12 now contradicts itself and it is Harish's call:** a 🟢 "RESOLVED
   2026-10-06 by the organisers" block declares "no licence breach", directly below a 🔶 addendum
   saying the determination "is still ours to make". The 🟢 block settles a question Harish owns.
   Left untouched.
5. **Nominate ≤20 + ranking rationale.** The screen changed what this is: **only 15 of 35 clear
   both the pH and charge flags**, so liability is a ranking term, not a tiebreak. Needs the item-1
   decision first.
6. **Re-run `binder-prescreen`** on the final 20 (10-07's pass was on all 35).
7. **Upload early, designate, attach methods, finalise.** ⬅ **Harish's**
8. **Send the reviewer their 4 artifacts.** ⬅ **Harish's** — critical path, see the note below.
9. Optional, $0, still unasked under his own name: **does a large K_D shift with binding at both pH
   values qualify, or must binding be undetectable at 6.0?** It decides whether any single-site
   design counts. Two other teams asked; never answered.
10. Open and undecided: **a Modal cap.** October billed **$590.71 with no credit balance**, while
    project documents still record $168.44 from 10-04 — stale by ~$420. Yesterday and today added
    ~$2. Nothing is running, but no cap exists.

**⚠️ ROUTE SCIENTIFIC JUDGEMENT TO THE REVIEWER, NOT TO CLAUDE.** Across 2026-10-07/08 more than six of my
responses were stopped mid-generation by a safety classifier, every one of them on explanatory prose
about this project, while every tool call, file write, commit and GPU run completed. Execution here
is reliable; reasoning delivered in prose is not. That makes item 8 critical path rather than
courtesy. Artifacts and tables have gone through consistently — prefer them.

## 🧭 THE PLAN LIVES IN `ROADMAP.md` IN THE OTHER REPO

`~/code/context-directory/projects/anthropic-adaptyv-2026/ROADMAP.md` (updated 2026-10-08 9:20 AM).
Everything below this line is problem 1, closed and archived.

---

# ══════════ PROBLEM 1 — CLOSED, ARCHIVE BELOW ══════════

**✅ SUBMITTED 2026-10-07. 16 designs, all 16 cleared novelty. Nothing owed.**
Methodology box pasted, METHODS attached, repo public and pushed, gates green.

**The one carry-forward lesson:** the resubmission swapped the set's *composition*, not its size.
Both designs the 10-05 check rejected were accepted on 10-06, and two it had passed at 3/4 were
rejected — **on byte-identical sequences.** Their novelty check is not stable, so every novelty
level we state is one run of their pipeline on one day. METHODS limitation 37; lessons 10 and 11
in `projects/anthropic-adaptyv-2026/lessons-problem-1.md`.

Everything below this line is the problem-1 record, kept because the lessons carry forward. **No
action in it is outstanding.**

---

## 1. STATE — everything below is verified, not remembered

**Submission: `submissions/01-egfr.csv`, 16 designs** (the resubmission set, as accepted). Track 3
allows 20 — see METHODS §11. *(This line read "18 designs" until 2026-10-07; the paragraph two
below has recorded the drop to 16 since 10-06, so the file contradicted itself for a day.)*
Ranked on the two-partner histidine-only pH product, not the superseded target-only basis.
`bin/check_discards.py` PASSES, exit 0. **`bin/gate_sweep.py`: 14 gates, all green at 16
designs** (d63c61f).

🔴 **Both counts in this paragraph were stale and are corrected 2026-10-06.** It read
"18 designs" and "12 gates: 11 green, `novelty_coverage` RED". What happened in between, from
the commit record rather than from this file: the 18-row set **was** pushed to Proteinbase on
10/5 ≈ 12:35 PM, their novelty filter scored 16 at 3/4 and **two at 2/4**, and it **blocked the
submission** until those two were removed — `bc_s360518_mpnn9_A22D` (Level 3 on our gate at
qTM 0.7924, clearing the cliff by 0.0076; limitation 33 named it in advance as the sharpest
eligibility exposure in the set) and `h370_020_vhh`. Removed as an INELIGIBLE map in
`bin/emit_submission_csv.py`, so a re-emit cannot reinstate them. `novelty_coverage` went green
on 10/5 when foldseek was reinstalled and the gate re-run — all four unlevelled chains cleared
Level 3. **`rimA02_d3_rimA_14_vhh` PASSED at 3/4**, which retires the ANARCI worry recorded
elsewhere: the one surviving antibody-format row is known-good on their gate.

✅ **ANSWERED 2026-10-06 11:50 AM, from the portal. IT WAS UPLOADED AND IT IS DESIGNATED.**
~~UNRECORDED: was the corrected 16-row set ever successfully uploaded?~~

Read first-hand while logged in as `harishrajaram-svg`:
- The profile carries a collection **"[Anthropic × Adaptyv] Submission 1", 16 proteins, marked
  DESIGNATED**, created 10/5. Its 16 AA lengths match `submissions/01-egfr.csv` exactly.
- `/rounds/1/submit` returns *"You've already submitted today … again after 6 Oct, 16:49 UTC."*
  A blocked upload does not start that cooldown, so the accepted submission went in at
  **5 Oct 16:49 UTC = 12:49 PM EDT**, fourteen minutes after `d63c61f` removed the two designs
  their novelty filter rejected.

**DESIGNATED means it is the one that counts, so no nomination step is outstanding.** Nothing is
owed on problem 1. The only thing still live is an opportunity, not a risk: challenge 1 stayed
open until Wed 10/7 7:59 AM and one further submission was available from 12:49 PM on 10/6 —
submissions are retained with the designated one counting, so an upload could not have lost what
was already banked.

🔴 **The 10-row table that stood here is replaced, 2026-10-06 — it was wrong twice over.**
It listed 10 of 16 shipped designs, it still carried `h370_020_vhh`, which Proteinbase rejected,
and its numbers came from the **`ph_ratio_target_only_SUPERSEDED`** column — contradicting the
sentence directly above it, which declares the ranking basis to be the two-partner his-only
product. Below is all 16, generated from `submissions/01-egfr.csv` on that declared basis
(`ph_ratio_6p5_over_7p4_his_only_CONSERVATIVE`), never typed. The basis change reorders the set
heavily — the four S15D designs drop from ranks 1–4 to 11–14 — so the CSV's own
`ph_rank_range_across_bases` is carried in the last column. **If the intended ranking key is a
different column, say so; this table follows the sentence above it.**

     1  5.656  rimA01_r15_L133E                              hu 0.5978  mo 0.4338  150aa  rank-range 1-6   
     2  5.546  c5_cf_short__boltzgen_egfr_cropfree_short_48  hu 0.2415  mo 0.1812   70aa  rank-range 2-10  
     3  4.838  rimA02_d3_rimA_14_vhh                         hu 0.2186  mo 0.4468  129aa  rank-range 3-13    nanobody
     4  4.812  c5_cr_crop_patch__boltzgen_egfr_crop_patch_05 hu 0.1320  mo 0.2041   66aa  rank-range 4-11  
     5  4.256  rimA01_r15_boltzgen_egfr_d3_rimA_20           hu 0.5938  mo 0.5668  150aa  rank-range 3-14  
     6  3.545  ss_bc_s831683_mpnn6_S15D_S62H_routeA          hu 0.7654  mo 0.7443   65aa  rank-range 4-11  
     7  3.526  d2c_mpnn13_S88D_serasp                        hu 0.6031  mo 0.5283  147aa  rank-range 5-9   
     8  3.180  cons_gap_h370_only__boltzgen_egfr_h370_018    hu 0.4566  mo 0.2150   90aa  rank-range 4-15  
     9  2.914  bcr_d3acid3_l60_s647537_mpnn3                 hu 0.5736  mo 0.1681   60aa  rank-range 10-16 
    10  2.747  bcr_d3acid3_l60_s647537_mpnn11                hu 0.4429  mo 0.2342   60aa  rank-range 11-17 
    11  1.835  bc_s831683_mpnn6_S15D                         hu 0.7803  mo 0.7507   65aa  rank-range 2-13  
    12  1.774  bc_s831683_mpnn19_S15D                        hu 0.8077  mo 0.7859   65aa  rank-range 3-14  
    13  1.062  bc_s831683_mpnn9_S15D                         hu 0.8040  mo 0.8037   65aa  rank-range 7-16  
    14  1.023  bc_s831683_mpnn8_S15D                         hu 0.7760  mo 0.7637   65aa  rank-range 8-17  
    15  0.737  bc_d3acid_l65_s831683_mpnn11                  hu 0.7963  mo 0.7838   65aa  rank-range 5-17  
    16  0.627  bc_s831683_mpnn9_WT                           hu 0.7857  mo 0.7840   65aa  rank-range 12-18 

**Methods document: `submissions/01-egfr-METHODS.md`, 12 sections, DONE.** Nothing is owed to
it. Leads with §4.4.

**Git remote: EXISTS, public, pushed.**
<https://github.com/harishrajaram-svg/anthropic-adaptyv-2026> — 200 on the README, the methods
doc, the CSV. *(Renamed from `adaptyv-egfr-ph-switch` on 2026-10-07; the old URL 301-redirects.)* The README is a submission front door, not the old setup log (that moved to
`docs/setup-notes-2026-09-18.md`).

Every pH number is the MEDIAN over every ESMFold2 refold pose of that exact binder sequence,
pooled across runs, joined to affinity BY SEQUENCE in `analysis/01-egfr/master_rank.json`.
**That file is the only source for both columns. Do not re-derive either from a run name.**

---

## 2. [2026-10-04] The result that changed that day — control recovery

`expctrl`/`ctrl2` had written raw PAE matrices and **no `*_10_10.txt`**, so the ipSAE step had
never run on them and the only measured-outcome test in the project was unavailable. Backfilled
`bin/ipsae_min.py --dir` over all 8 shards: **270 poses, 0 failures.** `truenull` was scored
after (200 poses; it is the superseded 1-shuffle×5-seed design, kept for n only).

**The panel is 10 negatives and ONE positive. Do not quote an AUC off it** — with one positive
every summary statistic is just "where does that one molecule rank", and an earlier draft of
METHODS §4.4 led with AUC 0.80 / 1.00 before this was corrected. Report ranks.

**Human leg: 8 of 10 RIGHT-CENSORED molecules rank below the measured binder, 2 rank ABOVE it.**
They are molecules with no reported KD, not molecules measured not to bind (the reviewer, 2026-10-04;
METHODS §4.1) — this line said "MEASURED non-binders" after that correction had landed.
The top-scoring molecule in the entire measured panel is one with no reported KD (right-censored, not a measured zero) —
`EXPNEG_gitter-yolo10` at 0.5893 against human EGF's 0.3549 — and it reads a **5.27× pH ratio,
rank 18 of the 246 rankable at n ≥ 5**, the top 7.3%. "Rank 8 of 2,009" appeared here and in README, and "8th of 132" replaced it without reproducing either; METHODS §7
records it as a ~15× overstatement, because 1,877 of that denominator were never rankable.

**Requiring both species: the one quantified binder outranks all ten no-KD molecules.** Both
molecules that beat it on human are at **exactly 0.0000 on mouse, 5 of 5 dead seeds** — no
interface at all, so the filter does not rest on a margin that a bigger panel could erode.
That mechanism is the defensible part; the ordering statistic is not. Cross-reactivity came
from the brief and is the only specificity filter here that measured data supports at all.

**The matched null is degenerate:** 12/12 shuffles at exactly 0.0000, 5/5 dead seeds. So
`affinity_above_null` means "above zero" and carries almost nothing. **CDR decoys on the real
5 nM VHH framework also read 0.0000 — same as the real VHH** — so the nanobody blind spot is
total, not the partial 0/2 of the old panel.

Artifacts: `analysis/01-egfr/control_recovery.{json,tsv}`. Written up as METHODS §4.4 + §4.5.

---

## 3. [2026-10-04] Decisions made that day — do not relitigate

- **Submission cut 20 → 10** (Harish, 3:30 PM). Ranks 11–20 did not stand on a measurement:
  8 read below 1.0× on the 0.702× analytic acid-weakening extreme. (Corrected 2026-10-05:
  that is NOT a "no switch" reading — no linkage gives 1.0 — and a pile-up on an analytic
  extreme indicates protonation-model saturation, so those 8 are uninterpretable on this
  gate, which is still a reason not to submit them but a different reason.) `bg04_r03`
  was 1.94× with 0.0000/0.0000 and an unpaired cysteine. `LIMIT = 10` in
  `bin/emit_submission_csv.py`, reasoning recorded in the docstring.
- **Six of ten slots on one backbone** (`d3acid_l65_s831683`) — four S15D sequences, mpnn11, and
  the matched WT. Deliberate: diversity traded for wet-lab replication of the only causal result.
- **Tier-2 sort key: MOOT and left unchanged.** At LIMIT = 10 no tier-2 design ships. Not edited
  blind at submission time.
- **Repo public** (Harish, 3:30 PM), full history including the error-correction commits.
- Standing: one submission made LATE; affinity gate retired (`MIN_AFFINITY = None`); mouse
  dropped as a tier-2 sort key; Mosaic gated for problems 2–5; S88D replaces its parent.

**New fact worth carrying:** inverting the linkage equation, the four S15D ratios imply
pKa_bound of 8.89 / 9.11 / 8.98 / 8.98 — the whole 5.40–5.46× spread is **0.22 pKa units wide**
and the four are NOT distinguishable from each other. Do not claim rank 1 beats rank 4.

---

## 4. WHAT WAS LEFT — one item survives, and it is still open

1. ~~**UPLOAD, and upload early enough to resubmit.**~~ ✅ **DONE** — uploaded 10-05 12:49 PM EDT,
   designated, 16 designs, all cleared novelty on the 10-06 re-check. The VHH worry recorded here
   resolved: `rimA02_d3_rimA_14_vhh` passed at 3/4, and `h370_020_vhh` was one of the two the
   10-05 check rejected and is not in the shipped set.
2. 🔴 **STILL OPEN — send the reviewer their artifacts.** All of their asks are done and **still
   unsent**: `outbox/ipsae-fixtures/` (8 cases, `run_fixtures.py --check`, VHH-zero trace),
   `outbox/CONTROL-TABLE.md`, `outbox/PREREGISTRATION.md`, and the construct audit. §4.4 answers
   their control-recovery ask and they should see it. **This is ROADMAP item 19 and it is Harish's
   to send** — the Gmail connector drafts only, it never sends.
3. ~~Optional: better designs hiding in the `sd`/`sd2` arms of `master_rank.json`.~~ **Moot** —
   problem 1 is submitted and designated, and iterating on a submitted design is disallowed.

---

## 5. TOOLING

    bin/ph_gate_refolds.py      pH gate on ESMFold2 refolds -- run on ALL 131 run dirs
    bin/ph_pool_by_sequence.py  ONE ratio per MOLECULE, pooled by binder sequence
    bin/master_rank.py          pH + affinity joined BY SEQUENCE -- the single ranking table
    bin/instrument_v2.py        ipSAE_min, v1 max / v2 median over seeds   (--self-test)
    bin/ipsae_min.py --dir D    *** writes the _10_10.txt every other reader parses ***
    bin/novelty_gate.py         FOLDSEEK=tools/foldseek/bin/foldseek ... --db tools/fsdb/pdb
    bin/antibody_novelty.py     Adaptyv's ANTIBODY branch (CDRH3)          (--selftest)
    bin/express_qc.py           expression liabilities (OVERWRITES express_qc.tsv)
    bin/emit_submission_csv.py  builds the CSV                             (--selftest)
    bin/check_discards.py       hard gate: nothing unmeasured may outrank a submitted design
    bin/bindcraft-sync.sh       pull BindCraft output off the Modal volume. RUN AFTER EVERY JOB.

**Proton-PottsMPNN** (third pH predictor, local CPU):
    HBPLUS_PATH=/tmp/HBPLUS/hbplus/hbplus DYLD_LIBRARY_PATH=/opt/homebrew/opt/libomp/lib \
      /tmp/ProtonPottsMPNN/.venv/bin/python /tmp/ppm_batch.py <list.txt> <out.csv>
  `/tmp` IS NOT PERSISTENT. Rebuild: clone github.com/christian-creator/ProtonPottsMPNN,
  `./install.sh`, build HBPLUS from github.com/RomanLas/HBPLUS (`make` in `hbplus/`).

**Standing traps, all of which have bitten:**
  - **a fold job is not a scored job.** ESMFold2 writes `*_ipsae.json` (raw PAE); the ipSAE
    step that writes `*_10_10.txt` is separate, and EVERY reader in `bin/` parses the latter.
    8 control shards sat "done" and unscored for hours because of this. After any fold job:
    `bin/ipsae_min.py --dir <rundir>`.
  - **names are not identities.** The same molecule appears under up to 3 run names, so a
    name-keyed `n` read 1 where 11 poses existed. Join on the binder SEQUENCE. Broke 5
    analyses; `master_rank.py` exists so it cannot happen a 6th time. A 6th instance did
    surface today and the CHECK caught it — one of `check_discards`' 45 "rejections" is an
    alias of a submitted design (METHODS §10).
  - novelty: **high structural similarity ALONE (TM >= 0.80) is Level 2**, no sequence
    condition. Missing that clause produced the bogus "0/120 pass novelty". 114 of 238 clear.
  - zsh does NOT word-split unquoted variables (broke 3 scripts)
  - chain order is NOT consistent: 29 of 69 run dirs have the TARGET in chain A. Use
    `ph_gate_all.orient()`. Broke 3 analyses.
  - construct numbering differs: crop H433=123, d3 H433=99, ECD H433=409. UniProt = PDB + 24.
  - `python3` has gemmi+propka; `.venv` has numpy but NOT gemmi
  - ProcessPoolExecutor cannot fork from a heredoc -- write a real .py file
  - score-esmfold2.sh cd's into biomodals/, so OUT_DIR must start `../`
