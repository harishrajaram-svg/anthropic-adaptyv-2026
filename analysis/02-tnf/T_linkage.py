#!/usr/bin/env python3
"""The fold route's REQUIRED stability window, from the two-state coupled equilibrium.

Only the folded binder binds.  K_unf = exp(-dG_unfold/RT).
KD_app = KD_folded * (1 + K_unf).
Acidification destabilises the fold by DD (kcal/mol, positive = destabilising).
switch = KD_app(6.0)/KD_app(7.4) = (1+K_unf*exp(DD/RT)) / (1+K_unf)
"""
import math
RT = 0.001987 * 298.15  # kcal/mol at 25 C

def switch(dG_unf, DD):
    k = math.exp(-dG_unf / RT)
    return (1.0 + k * math.exp(DD / RT)) / (1.0 + k)

def folded_frac(dG_unf):
    return 1.0 / (1.0 + math.exp(-dG_unf / RT))

DD = 3.064  # arm M's measured summed destabilisation at pH 6.0
print(f"RT = {RT:.4f} kcal/mol;  DD = +{DD} kcal/mol  (arm M, PROPKA, 4 buried His)")
print(f"protonation equilibrium shift exp(DD/RT) = {math.exp(DD/RT):.1f}x\n")
print(f"{'dG_unfold(7.4)':>15} {'frac folded 7.4':>16} {'frac folded 6.0':>16} {'switch ratio':>13}")
for g in [10,8,6,5,4,3.5,3,2.5,2,1.5,1,0.5,0.0,-0.5]:
    print(f"{g:>15.1f} {folded_frac(g):>16.4f} {folded_frac(g-DD):>16.4f} {switch(g,DD):>13.2f}x")

print("\nInverted: what dG_unfold(7.4) does a given switch REQUIRE at DD=+3.064?")
for target in [1.5, 2.0, 3.0, 5.0, 10.0, 79.0]:
    lo, hi = -5.0, 20.0
    for _ in range(200):
        mid = 0.5*(lo+hi)
        if switch(mid, DD) > target: lo = mid
        else: hi = mid
    print(f"  {target:>5.1f}x  requires dG_unfold <= {0.5*(lo+hi):>6.2f} kcal/mol"
          f"   (frac folded at 7.4 = {folded_frac(0.5*(lo+hi)):.4f})")

print("\nAnd how much DD would a STABLE scaffold need?")
for g in [4.0, 6.0, 8.0, 10.0]:
    for target in [2.0, 10.0]:
        lo, hi = 0.0, 40.0
        for _ in range(200):
            mid = 0.5*(lo+hi)
            if switch(g, mid) < target: lo = mid
            else: hi = mid
        n_his = (0.5*(lo+hi))/0.775
        print(f"  dG_unfold={g:>4.1f}, {target:>4.1f}x needs DD >= {0.5*(lo+hi):>5.2f} kcal/mol"
              f"  = {n_his:>5.1f} buried His at the +0.775 ceiling")
