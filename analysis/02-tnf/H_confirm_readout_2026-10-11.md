---
type: readout
project: anthropic-adaptyv-2026
problem: 02-tnf-alpha
arm: H confirmation — 5 seeds, matched nulls, monomers
prereg: analysis/02-tnf/PREREG-H-REBUILD-2026-10-11.md
written: 2026-10-11 12:15 PM EDT
cost: 45 folds, ~$2
---

# Arm H confirmation — `quadH_E3Q_k12` passes H1, H2 and H3, the first design to do both

| design | H1 margin ≥ +6.3473 | H2 gate < 1.0, ≥4/5 | H3 pLDDT ≥ 0.70 | verdict |
|---|---|---|---|---|
| **`quadH_E3Q_k12`** | **PASS +7.1968** (SD 0.189) | **PASS 0.8710, 5 of 5** | **PASS 0.8764** | **H1+H2+H3** |
| `L49H_E4Q_k11` | **PASS +6.8737** (SD 0.134) | **PASS 0.9724, 4 of 5** | PASS 0.9188 | H1+H2+H3, marginal |
| `L49H_E4Q_k15` | PASS **+7.3212** (SD 0.141) | **FAIL 0.9517, 3 of 5** | PASS 0.9158 | H2 fails the ≥4/5 bar |

Per-seed gate totals:

- `quadH_E3Q_k12` — 0.643, 0.828, 0.871, 0.908, 0.979 → **5 of 5 below 1.0**
- `L49H_E4Q_k11` — 0.891, 0.918, 0.972, 0.982, 1.307 → 4 of 5
- `L49H_E4Q_k15` — 0.829, 0.864, 0.952, 1.187, 1.317 → 3 of 5, **fails**

`L49H_E4Q_k15` has the best margin in the set and is reported as a **failure** because the
pre-registered bar was ≥4 of 5 seeds, not a median. It is not rounded up.

## What was recovered

Arm G corrected the direction and broke the hold; the rebuild restores it without giving the
direction back:

| | margin | gate median |
|---|--:|--:|
| `quadH` (arm M parent) | +7.1306 | 1.7935, 0 of 5 |
| `quadH_E3Q` (arm G) | +6.2248 **FAIL** | 0.9468, 4 of 5 |
| **`quadH_E3Q_k12`** (arm H) | **+7.1968 PASS** | **0.8710, 5 of 5** |

The margin is back to the parent's value and the direction is better than arm G's. Monomer pLDDT
also improved on its parent (0.8764 against 0.8134). **H1+H2 together is what the pre-registration
named as the only result that matters**, since arm M already had the margin without the direction
and arm G the direction without the margin.

## 🔴 Three limits that bound this, and the first is the big one

**1. The instrument is still uncalibrated, and it does not discriminate.** Against
composition-matched shuffled binders, designs clear the gate's total product at **5.8%** against the
nulls' **5.6%** — ratio 1.05x. So "below 1.0 in 5 of 5 seeds" means the reading is **reproducible,
not that it is real**. Replication rules out seed noise; it says nothing about whether the quantity
predicts pH behaviour. That is exactly what ROADMAP R1 exists to settle.

**2. These designs carry ZERO histidines.** SolubleMPNN redesigned the whole binder chain and
removed His49 from the `L49H` line and all four buried histidines from the `quadH` line. So the
quad's **+3.064 kcal/mol fold-destabilisation mechanism is gone**, and no binder-side titratable
group remains — the entire predicted direction comes from target H73 and Glu146. These cannot
switch by the intended mechanism, and inherit the caveat the box already carries for `3_L4r5k2`.
This was my oversight: the redesign was constrained only on acid positions, and ProteinMPNN's
`fixed_positions_jsonl` would have preserved the histidines. ROADMAP R3 is that re-run.

**3. Not yet shippable.** No mouse margin, no liability screen, no dedup check against the ship set
for either passing design. 20 folds (~$1) plus two local screens closes that.

ESMFold2 is pH-agnostic. Objective 2 stays reported as not demonstrated.
