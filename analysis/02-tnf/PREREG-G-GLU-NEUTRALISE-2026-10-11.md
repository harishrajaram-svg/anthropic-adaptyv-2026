---
type: preregistration
project: anthropic-adaptyv-2026
problem: 02-tnf-alpha
arm: G — neutralise the specific binder glutamates the gate attributes the inversion to
status: PRE-REGISTERED — written 2026-10-11 11:26 AM EDT, BEFORE any variant is built or folded
cost: ~45 folds, ~$2
---

# Arm G — the inversion in both shipping candidates is three of OUR glutamates, by name

Gating `3_L0r4k0_L49H` and `3_L0r4k0_quadH` on 5 seeds each returned **inverted in 5 of 5 for both**
(L49H median 2.107, quad median 1.794). The per-site attribution is the same molecule to molecule:

| site | L49H (median, n/5) | quad (median, n/5) | |
|---|--:|--:|---|
| target H73 | 0.753x | 0.793x | helps |
| target GLU146 | 0.931x | 0.923x | helps |
| **binder GLU7** | **1.325x, 5/5** | **1.533x, 5/5** | wrong |
| **binder GLU28** | **1.429x, 5/5** | **1.516x, 5/5** | wrong |
| **binder GLU20** | **1.183x, 4/5** | **1.092x, 5/5** | wrong |
| **binder GLU10** | **1.119x, 4/5** | (2/5, excluded) | wrong |

**Neither molecule's histidines appear in the contributing set at all** — not His49, not the quad's
His45/53/63/64. They are inert for *binding* linkage, which is what PROPKA already said
(delta_protonation 0.000-0.044). So L49H is ranked first in the methodology box as the design
"carrying a mechanism" while that histidine contributes nothing measurable to the interface.

## Why this is not a repeat of two closed experiments

- **Not arm A.** Arm A banned acids at *every* interface position during design and reached 0 of 224
  on pose. This mutates **four named positions** in a molecule that already folds and binds.
- **Not C12.** C12 killed the hypothesis that *burial depth* separates safe acids from inverting
  ones (59 of 59 inverted across 26-104 neighbours). This uses no threshold: the positions are the
  ones the gate's own per-molecule attribution names, replicated across seeds.

Selection rule, fixed: a binder site is mutated iff it contributes in **≥3 of 5 seeds** AND its
median ratio is **> 1.0**. That yields `{7, 10, 20, 28}` for L49H and `{7, 20, 28}` for the quad.
Glu→**Gln**: isosteric and charge-neutral, so the change removes the titration without removing the
side-chain volume.

## Constructs

| name | parent | mutations |
|---|---|---|
| `L49H_E4Q` | `3_L0r4k0_L49H` | E7Q E10Q E20Q E28Q |
| `quadH_E3Q` | `3_L0r4k0_quadH` | E7Q E20Q E28Q |
| `quadH_CTRL3Q` | `3_L0r4k0_quadH` | **E3Q E4Q E23Q** — three NON-contributing Glu, count-matched |

🔴 **`quadH_CTRL3Q` is the arm's control and the reason it is worth running.** Both parents carry 23
glutamates. If neutralising *any* three improves the ratio, the gate's attribution is worthless and
the targeted variant proves nothing — that is exactly how the frustrated-cation-pair arm died, on its
own control. The control's positions are the first three non-contributing Glu by index, chosen before
any result.

## Bars

| bar | threshold | meaning |
|---|---|---|
| **G1** | 5-seed gate median **< 1.0**, in ≥4 of 5 seeds | the direction is corrected and replicates |
| **G2** | 5-seed human margin ≥ **+6.3473** | the hold survives the mutations |
| **G3** | 5-seed monomer pLDDT ≥ **0.70** | it still folds |
| **G4** | targeted variant's gate median **below** `quadH_CTRL3Q`'s | the attribution is specific, not generic |

**G1+G2+G4 is the result worth having.** G1 without G4 means any three glutamates would have done it.

## Stated prediction, before the folds

Removing the wrong-direction binder sites leaves target H73 and target GLU146, both helping. Their
product predicts **≈0.70 for L49H** (0.753 x 0.931) and **≈0.73 for the quad** (0.793 x 0.923). If
G1 passes with a median far from those figures, the sites are not independent and the prediction was
naive — recorded now so that cannot be rationalised later.

## 🔴 Expected failure mode

Glutamates at a binding interface are frequently load-bearing: A3 knocked out His61 and the margin
fell from +8.031 to +0.916. Four simultaneous charge removals at contact positions may well cost the
hold, so **G2 is the bar most likely to fail**, and G1 passing while G2 fails would mean the
inversion and the binding share the same residues — a trade-off, not a fix.

ESMFold2 remains pH-agnostic; no outcome here demonstrates a switch. Objective 2 stays reported as
not demonstrated.
