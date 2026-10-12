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
