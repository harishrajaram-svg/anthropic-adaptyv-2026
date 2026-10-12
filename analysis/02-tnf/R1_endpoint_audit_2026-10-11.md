# R1 endpoint audit, added 2026-10-11 on reviewer request

The reviewer's point: a K_D ratio and a k_off ratio are not the same quantity, and the accuracy
figure pooled them. Also flagged: adalimumab's 9x is ~9x FASTER DISSOCIATION at pH 6.0, not a
measured 9x loss of equilibrium affinity. Both are now stated that way in FIELD 2.

| pdb | experimental pHs | endpoint | target chains | binder chains | declared direction |
|---|---|---|---|---|---|
| 1BRS | 8.0 / 5.0 | Ki | A | D | release |
| 3SQO | 6.0 / 7.4 | KD + kd | A+P | H+L | flat |
| 3WD5 | 7.4 / 6.0 | koff ratio | A | H+L | release |
| 4K71 | 6.0 / 7.4 | KD + ka/kd | B+C | A | tighten |
| 4N0U | 5.8 / 7.4 | KD (switchSENSE) | A+B | E | tighten |
| 5B71 | 7.4 / 5.8 | KD | E | A+B | release |
| 5HYS | 6.0 / 7.4 | KD | G | A+B | flat |
| 5I5K | 7.4 / 6.0 | KD | B | H+L | release |
| 5TRU | 6.0 / 7.4 | KD, 8-point series | C | H+L | flat |
| 6FGB | 6.0 / 7.4 | KD + ka/kd | A+B | H+L | flat |
| 7Q15 | 6.0 / 7.4 | KD (SPR) | A+B | E | tighten |
| 7SU0 | 6.0 / 7.4 | KD | C | H+L | tighten |
| 7SU1 | 6.0 / 7.4 | KD | C | H+L | tighten |
| 8J6F | 6.0 / 7.4 | KD and kd | I | H+L | flat |
| 8TBQ | 5.8 / 7.4 | KD, range endpoints | P | H+L | tighten |
| 9MI6 | 6.0 / 7.4 | KD, both bounded | A+B | H+L | flat |
| 9S60 | 6.0 / 7.0 | KD (ITC) | A | B | flat |
| 9X1H | 7.4 / 6.0 | KD | A | H+L | release |

Endpoint mix: {'Ki': 1, 'KD': 16, 'koff': 1}.

**Rows whose endpoint is kinetic rather than affinity: 3WD5 (koff ratio) and 8J6F (both reported).**
Rows whose acidic arm is outside 6.0-6.5: 5B71 (5.8), 1BRS (5.0), 8TBQ (5.8), 4N0U (5.8).
Rows with a bounded rather than point value at one pH: 9MI6 (both bounded), 8TBQ (range only).

Consequence for the accuracy figure: 8 of 18 is a pooled number over mixed endpoints and mixed
acidic arms. It is reported as a failure to validate, not as a measured accuracy, and the benchmark
labels themselves still need re-checking before any accuracy figure is treated as final.

---

## Completed 2026-10-11 10:30 PM EDT: the split the reviewer asked for, and the variant check

The audit above named the kinetic rows but **did not recompute accuracy without them**, and omitted
"related variants" entirely. `bin/r1_endpoint_split.py` does both, selftest 3/3 (it reproduces the
committed 8/18 and 16/18 before computing anything new). Full output:
`analysis/02-tnf/R1_endpoint_split_2026-10-11.txt`.

| subset | n | direction | ratio > 1.0 |
|---|--:|--:|--:|
| all rows, as reported | 18 | 8/18 = 44.4% | 16/18 = 88.9% |
| affinity endpoints only (drops the rate-ratio row) | 17 | 8/17 = 47.1% | 15/17 = 88.2% |
| exact 6.0/7.4 pair, any endpoint | 13 | 6/13 = 46.2% | 13/13 = 100% |
| **exact 6.0/7.4 pair AND affinity endpoint** | **12** | **6/12 = 50.0%** | **12/12 = 100%** |

🔴 **The pooled figure was FLATTERING the instrument, for the second time.** On the only subset
that matches the assay pair Adaptyv runs — equilibrium endpoint, 7.4 against 6.0 — the gate returns
a ratio above 1.0 in **12 of 12**. It never once predicts release where release is what problem 2
needs. And its direction accuracy on that subset, **6 of 12**, is *exactly* what a constant
predictor scores there (always answer the commonest label: 6/12). Not approximately: identically.

So separating the endpoints does not rescue the calibration, it sharpens the failure. Dropping the
rate-ratio row moves 8/18 to 8/17, which is noise; restricting to the matched pH pair is what
matters, and it removes the four rows whose acidic arm was 5.8 or 5.0 — where a larger per-proton
term makes a release prediction easier — leaving a subset on which the instrument has no signal at
all.

**Related variants, derived rather than asserted.** Pairwise identity of the deposited binder
chains, computed from `runs/R1-pdb/`:

- **`4N0U` ~ `7Q15`, binder identity 0.990** — the same molecule twice. Both are `tighten`
  positives and **both are counted as hits** in the 8/18. So the headline rests on 17 independent
  molecules, not 18, and two of its eight hits are one observation. Neither survives into the
  matched subset (both are 5.8 on the acidic arm), so the matched figure is unaffected.
- No other pair reaches 0.90. The antibody rows share a germline framework and sit well below it.

Identity is ungapped and N-terminally anchored — crude on purpose. It only has to separate "the
same antibody" (0.99) from "a different one on a shared framework" (<0.70), and a real alignment
would move the third decimal, not the call.

**Still open, and stated as open:** the benchmark LABELS themselves. Every published ratio in the
table was read off a paper by us, and the reviewer asked for them to be re-checked. They have not
been. Until they are, no accuracy figure here — pooled or matched — should be treated as final, and
none is load-bearing for anything in the submission, because the pH claims are withdrawn either way.
