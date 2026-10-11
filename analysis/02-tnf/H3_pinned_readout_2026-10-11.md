---
type: readout
project: anthropic-adaptyv-2026
problem: 02-tnf-alpha
arm: R3 / H3 — the rebuild with histidine positions pinned
written: 2026-10-11 12:28 PM EDT
cost: 48 folds, ~$2
---

# R3 — the histidines can be kept for free, and they contribute nothing anyway

## The pin worked, and the hold did not care

| parent | own pae | unpinned best | **pinned best** | pin cost |
|---|--:|--:|--:|--:|
| `L49H_E4Q` | 8.297 | 7.332 | **7.496** | 0.164 |
| `quadH_E3Q` | 8.628 | 7.559 | **7.481** | **−0.078 (better)** |
| `s3_22k4` | 9.213 | 8.367 | **7.759** | n/a (no His to pin) |

H5 verified on all 48 output sequences: His49 preserved in all 16 of the `L49H` line, all four of
`45/53/63/64` preserved in the `quadH` line, and SolubleMPNN volunteered extra histidines at 29
and/or 33 in six of them. So **preserving the mechanism costs nothing on the hold** — the fear that
motivated this arm was unfounded.

## 🔴 And the direction got worse, which is the actual result

| pool | gate < 1.0 | median gate | (unpinned run) |
|---|--:|--:|--:|
| `L49H_E4Q` | 4 of 16 | 1.341 | 2 of 16, 1.354 |
| `quadH_E3Q` | **1 of 16** | **7.774** | 4 of 16, 2.126 |
| `s3_22k4` | 4 of 16 | 4.039 | 5 of 16, 3.502 |

The quad pool collapsed: median gate **7.774** pinned against 2.126 unpinned, and one design below
1.0 instead of four. Its best-PAE design, `quadH_E3Q_k6` — six histidines, pae 7.481, the best hold
in the whole arm — gates at **3.805** with binder-owned 3.713.

**The histidines are the reason.** Across every one of the top 12 designs, the count of histidine
sites appearing in the gate's contributing set is **zero**. Not one histidine, pinned or
volunteered, contributes to the binding-coupled pH response in any design in this arm.

That is now measured four independent ways: the `L49H` parent (His49 absent from the contributing
set in 5 of 5 seeds), the `quadH` parent (all four absent), arm G's variants, and these 48. **A
buried histidine's contribution to binding-coupled pH response in this system is consistently nil.**
The mechanism they would serve is *fold* destabilisation, which this gate cannot see at all — that
is arm M's quantity, not this one.

## Candidates that clear both halves at screen level

5 of 48, three of them carrying histidines that contribute nothing:

| design | pae | gate | target | binder | His (contributing) |
|---|--:|--:|--:|--:|---|
| `s3_22k4_k3` | 7.759 | **0.574** | 0.417 | 1.443 | 0 (0) |
| `s3_22k4_k6` | 8.540 | 0.505 | — | — | 0 (0) |
| `L49H_E4Q_k11` | 7.688 | 0.766 | 0.679 | 1.133 | 1 (0) |
| `quadH_E3Q_k14` | 7.900 | 0.790 | 0.714 | 1.000 | 4 (0) |
| `L49H_E4Q_k13` | 7.496 | 0.915 | 0.639 | 1.384 | 1 (0) |

`quadH_E3Q_k14` is the one worth confirming: it keeps all four buried histidines — so arm M's
**+3.064 kcal/mol fold mechanism is intact** — while clearing both screen halves. Its pH direction
still comes from the target, not from its own histidines, and that must be said plainly.

`s3_22k4_k3` closed 1.45 of the seam design's 1.76 margin gap and has the best direction here. Its
pin list was empty, so that is a second sampling draw rather than an effect of pinning.

## 🔴 Name collision, and why it matters

`tnfa_H_L49H_E4Q_k11` exists in **both** runs as a **different molecule**:

| run | His | sha256[:12] |
|---|--:|---|
| `runs/H-rebuild-in` (unpinned) | 0 | `4aeffb1b2567` |
| `runs/H3-pinned-in` (pinned) | 1 | `d80b55eff278` |

This is the exact trap ROADMAP documents — one id, two sequences, across parallel output trees — and
I reproduced it by reusing the same id scheme for both runs. Any join between these runs must be on
**sequence content**, never on the id. Nothing has been mis-joined: every number above was read from
its own run's directory.

## Next

5 seeds plus matched nulls plus monomers on `quadH_E3Q_k14` and `s3_22k4_k3`: 20 complex + 10
monomer = **30 folds, ~$1.40**. That is H1/H2/H3 measured properly on the two that matter.
