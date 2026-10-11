---
type: pre-registration
project: anthropic-adaptyv-2026
problem: 02-tnf-alpha
arm: W2 lateral charge steering
written: 2026-10-11, BEFORE any number was computed
---

# W2 pre-registration — lateral electrostatic steering on the six shipped designs

## The quantity

Not proton linkage. The screened-Coulomb (Debye-Huckel) interaction energy between the
binder's interface charges and the target's contact-patch charges, evaluated at pH 7.4 and
pH 6.0 with Henderson-Hasselbalch occupancies on model pKa values:

    U(pH) = SUM_ij  332 * q_i(pH) * q_j(pH) / (78.5 * r_ij) * exp(-r_ij / 7.8)   kcal/mol

i over titratable binder residues within the interface shell, j over titratable target
residues within the patch shell, r_ij in Angstrom, kappa^-1 = 7.8 A (150 mM, 310 K),
eps_r = 78.5. This is the functional form Schreiber's steering treatment uses and it is
NOT the failed binding-coupled gate; no PROPKA bound/free leg appears anywhere in it.

    ddG_steer = U(6.0) - U(7.4)

POSITIVE ddG_steer = the interface becomes less electrostatically favourable on
acidification = the RELEASE direction.

## Bars, fixed now

- **W2-1 (materiality).** A switch worth claiming is >= 10x in K_D. At 310 K that is
  2.303 * R * T * log10(10) = **1.42 kcal/mol**. For this angle to be alive, an achievable
  mutation set must deliver **ddG_steer >= +1.42 kcal/mol**. Below that, the charge swing is
  too small to move a nanomolar interaction and the angle is dead on magnitude.
- **W2-2 (sign, as built).** At least one of the six shipped designs must already have
  **ddG_steer > 0**. Report all six regardless.
- **W2-3 (achievability).** The search space is **<= 3 point mutations** on binder residues
  that are in the interface shell but NOT in heavy-atom contact (< 4.5 A) with the target —
  rim only, pose-sparing by construction. A candidate mutation must also satisfy
  **dU(7.4) <= +0.25 kcal/mol** (it may not throw away the hold at neutral pH). If the best
  pose-sparing triple cannot reach +1.42, state by what factor it falls short.
- **W2-4 (honesty).** If the required charge-product change exceeds what three mutations can
  buy by more than 2x, the angle is DEAD and I say so. A negative result is the result.

## Reference charge arithmetic, stated now

Only histidine titrates appreciably between 7.4 and 6.0 on model pKa: dq_His = +0.648 e.
Asp/Glu move +0.019 e and +0.001 e. So any pH dependence here is carried by histidines —
the binder's, the target's, or both — and a pH-independent charge mutation (Glu->Lys) can
only act as a MULTIPLIER on the target's own histidine swing, never as a switch by itself.
That multiplier route is the one thing in this arm that needs no binder histidine, and
therefore sidesteps closed items 1 and 2.

## What would kill it
Target contact patches that are net NEGATIVE: then a binder gaining positive charge is
pulled IN at pH 6.0 (tightening), and the lever points the wrong way by construction.
