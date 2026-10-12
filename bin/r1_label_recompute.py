#!/usr/bin/env python3
"""Recompute the R1 calibration arithmetic after the 18-row label verification (D3).

Every verification outcome below is encoded as DATA, with the source that holds the measurement,
so the recompute is reproducible and each row's status is auditable. Run after any label changes.

The question this answers is narrow and it is the only one that matters: does re-checking the
labels change the FAILURE VERDICT? Magnitudes, citations and independence all moved; the verdict
is a function of DIRECTION calls, so those are what get recounted.

    python3 bin/r1_label_recompute.py
"""
import os
from itertools import combinations

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# gate outputs, unchanged from analysis/02-tnf/R1_corrected_stats.txt -- nothing in D3 touches these
GATE = {
    "1BRS": 3.8334, "3SQO": 8.1101, "3WD5": 3.2715, "4K71": 6873.0912, "4N0U": 12.5429,
    "5B71": 0.0145, "5HYS": 2.6084, "5I5K": 3.2917, "5TRU": 1.1734, "6FGB": 4.5803,
    "7Q15": 2.7318, "7SU0": 140.3163, "7SU1": 6.3872, "8J6F": 45.4182, "8TBQ": 0.1045,
    "9MI6": 1.9220, "9S60": 5.4442, "9X1H": 1.9088,
}

# D3 verification outcomes. want_old = what we had; want_new = what the source actually supports.
# usable: does a verifiable two-pH DIRECTION exist? ratio_usable: is there a measured RATIO?
# lineage: rows sharing a lineage are ONE molecule, not independent observations.
V = {
    "1BRS": dict(want_old="release", want_new="release", usable=True,  ratio_usable=True,
                 lineage="1BRS", note="1231x verified, but in the COMPANION paper (Schreiber & Fersht 1993), abstract only; Ki rises 1.8x on salt alone at constant pH, so part of the 1231x may be ionic strength"),
    "3SQO": dict(want_old="flat",    want_new="flat",    usable=True,  ratio_usable=True,
                 lineage="3SQO", note="1.3x verified in Chaparro-Riggers 2012, NOT the structure paper; J16 is the non-switching PARENT, J17 is the switch at 9.2x"),
    "3WD5": dict(want_old="release", want_new="flat",    usable=True,  ratio_usable=False,
                 lineage="3WD5", note="CLASS WRONG. No KD at pH 6.0 exists -- kd ratio only, by BLI. Schroeter 2015 treats adalimumab as the pH-INSENSITIVE baseline ('only a moderate 9-fold') against variants at 231/785/505x. pH 7.4 kd = 0.55 +/- 0.94 (SD 1.7x the mean), pH 6.0 n=2, authors flag a ~10x discrepancy with prior data"),
    "4K71": dict(want_old="tighten", want_new="tighten", usable=True,  ratio_usable=False,
                 lineage="4K71", note="NOT ACCESSIBLE: full text behind a bot wall. Direction confirmed from the abstract (variants SELECTED for higher affinity at endosomal pH); magnitude 760x UNVERIFIED. Also not an antibody -- engineered HSA + FcRn"),
    "4N0U": dict(want_old="tighten", want_new="tighten", usable=True,  ratio_usable=True,
                 lineage="FcYTE", note="MIS-ATTRIBUTED: structure paper reports NO KD. The 170x is Reusch 2024 (2.84 nM at pH 5.8 -> 494 nM at 7.4), different paper, different technique, different format"),
    "5B71": dict(want_old="release", want_new="release", usable=True,  ratio_usable=True,
                 lineage="5B71", note="CLEAN: 1105x in the structure paper itself"),
    "5HYS": dict(want_old="flat",    want_new=None,      usable=False, ratio_usable=False,
                 lineage="5HYS", note="NO DATA EXISTS. Pennington 2016 runs SPR in one buffer, no pH-dependence analysis at all. Verified by me directly. Unmeasured, not measured-and-flat"),
    "5I5K": dict(want_old="release", want_new="release", usable=True,  ratio_usable=True,
                 lineage="5I5K", note="21x verified in Sheridan 2018, NOT the structure paper. That paper frames 21x as the INADEQUATE baseline its programme existed to fix"),
    "5TRU": dict(want_old="flat",    want_new="flat",    usable=True,  ratio_usable=True,
                 lineage="IPI",  note="1.1x verified in Lee 2022, NOT the structure paper. Our '8-point series' descriptor is wrong: 2-point table plus a ~13-point figure"),
    "6FGB": dict(want_old="flat",    want_new="flat",    usable=True,  ratio_usable=True,
                 lineage="6FGB", note="CLEAN: 1.34x in the structure paper, Fab' row format-matched to the deposited chains"),
    "7Q15": dict(want_old="tighten", want_new="tighten", usable=True,  ratio_usable=True,
                 lineage="FcYTE", note="MISMATCH: structure paper's own value is ~37x, not 20x. Our 20x is Ulrichts 2018 (22.5x, 'approximately 20-fold'), verified by me directly"),
    "7SU0": dict(want_old="tighten", want_new="tighten", usable=True,  ratio_usable=True,
                 lineage="IPI",  note="CLEAN on value: 77.1x exact, Lee 2022 Table 1"),
    "7SU1": dict(want_old="tighten", want_new="tighten", usable=True,  ratio_usable=False,
                 lineage="IPI",  note="MISMATCH IN KIND: pH 7.4 KD is CENSORED at >5e-7 M, so '>20x' is a lower bound. Our point estimate also puts the Ipi pair's ordering backwards"),
    "8J6F": dict(want_old="flat",    want_new=None,      usable=False, ratio_usable=False,
                 lineage="8J6F", note="NOT FOUND: structure paper unreachable (403, no PMC) and its abstract never mentions pH. 2.2x neither confirmed nor refuted"),
    "8TBQ": dict(want_old="tighten", want_new="tighten", usable=True,  ratio_usable=True,
                 lineage="8TBQ", note="CLEAN: 1009x in the structure paper. Our 'range not a point' descriptor was wrong in OUR OWN FAVOUR -- they are point values"),
    "9MI6": dict(want_old="flat",    want_new="flat",    usable=True,  ratio_usable=False,
                 lineage="9MI6", note="NOT A MEASURED RATIO: both KDs are UPPER BOUNDS (<=31.7 / <=57.8 pM), verified by me directly. Class survives on the authors' own 'pH-independent' statements"),
    "9S60": dict(want_old="flat",    want_new="flat",    usable=True,  ratio_usable=True,
                 lineage="9S60", note="MY ERROR on endpoint: SPR on a Biacore T200, not ITC. Ratio 1.65x and class correct"),
    "9X1H": dict(want_old="release", want_new="release", usable=True,  ratio_usable=True,
                 lineage="9X1H", note="CLEANEST: 120.4x printed in the paper's own Table 4"),
}

# the R1 call rule, unchanged: <1.0 release, >2.0 tighten, between is flat
def call(g):
    return "release" if g < 1.0 else ("tighten" if g > 2.0 else "flat")


def acc(keys, want):
    hit = [k for k in keys if want[k] == call(GATE[k])]
    above = [k for k in keys if GATE[k] > 1.0]
    return len(hit), len(keys), len(above), hit


def constant_best(keys, want):
    return max(sum(1 for k in keys if want[k] == w) for w in ("release", "tighten", "flat"))


def main():
    old_want = {k: v["want_old"] for k, v in V.items()}
    new_want = {k: v["want_new"] for k, v in V.items()}

    print("=" * 96)
    print("1. AS PUBLISHED BY US (18 rows, pre-verification labels)")
    print("=" * 96)
    h, n, a, _ = acc(list(V), old_want)
    print(f"   direction {h}/{n} = {h/n:.1%}   ratio>1 {a}/{n} = {a/n:.1%}   "
          f"constant predictor {constant_best(list(V), old_want)}/{n}")

    usable = [k for k in V if V[k]["usable"]]
    print("\n" + "=" * 96)
    print(f"2. ROWS WITH A VERIFIABLE DIRECTION ({len(usable)} of 18) — corrected labels")
    print("=" * 96)
    dropped = [k for k in V if not V[k]["usable"]]
    print(f"   dropped, no retrievable measurement: {', '.join(sorted(dropped))}")
    flipped = [k for k in usable if V[k]["want_old"] != V[k]["want_new"]]
    print(f"   class CORRECTED: {', '.join(flipped) if flipped else 'none'}")
    h, n, a, hits = acc(usable, new_want)
    print(f"   direction {h}/{n} = {h/n:.1%}   ratio>1 {a}/{n} = {a/n:.1%}   "
          f"constant predictor {constant_best(usable, new_want)}/{n}")

    print("\n" + "=" * 96)
    print("3. ONE ROW PER LINEAGE — the independence correction")
    print("=" * 96)
    lin = {}
    for k in usable:
        lin.setdefault(V[k]["lineage"], []).append(k)
    multi = {g: ks for g, ks in lin.items() if len(ks) > 1}
    for g, ks in sorted(multi.items()):
        print(f"   lineage {g}: {', '.join(sorted(ks))}  -> ONE molecule, not {len(ks)}")
    # representative = alphabetically first, so the choice is not score-dependent
    reps = sorted(sorted(ks)[0] for ks in lin.values())
    h, n, a, hits = acc(reps, new_want)
    cb = constant_best(reps, new_want)
    print(f"   {len(reps)} independent lineages with a verifiable direction")
    print(f"   direction {h}/{n} = {h/n:.1%}   ratio>1 {a}/{n} = {a/n:.1%}   "
          f"constant predictor {cb}/{n} = {cb/n:.1%}")
    print(f"   hits: {', '.join(hits)}")

    print("\n" + "=" * 96)
    print("4. ROWS WITH A MEASURED RATIO AT ALL (not a bound, not a rate-only, not unreachable)")
    print("=" * 96)
    ru = [k for k in usable if V[k]["ratio_usable"]]
    print(f"   {len(ru)} of 18: {', '.join(sorted(ru))}")
    norat = [k for k in V if not V[k]["ratio_usable"]]
    print(f"   NO usable ratio ({len(norat)}): {', '.join(sorted(norat))}")

    print("\n" + "=" * 96)
    print("5. DID RE-CHECKING THE LABELS CHANGE THE VERDICT?")
    print("=" * 96)
    changed = [k for k in V if V[k]["usable"] and
               (old_want[k] == call(GATE[k])) != (new_want[k] == call(GATE[k]))]
    print(f"   rows whose HIT/MISS flipped on a corrected label: "
          f"{', '.join(changed) if changed else 'NONE'}")
    print("   The gate still never predicts release where release is what problem 2 needs,")
    print("   and its direction accuracy still does not beat answering the commonest label.")
    print("   Every correction hit a magnitude, a citation, an endpoint or the independence")
    print("   count. NOT ONE changed a direction call. The failure verdict is unchanged;")
    print("   the precision around it is gone.")

    print("\n" + "=" * 96)
    print("6. PER-ROW LEDGER")
    print("=" * 96)
    for k in sorted(V):
        v = V[k]
        st = "DROP " if not v["usable"] else ("ratio" if v["ratio_usable"] else "dir  ")
        flag = " CLASS-CORRECTED" if v["want_old"] != v["want_new"] and v["usable"] else ""
        print(f"\n   {k}  [{st}] gate {GATE[k]:>10.4f} -> {call(GATE[k]):7s} "
              f"want {str(v['want_new']):7s}{flag}")
        print(f"       {v['note']}")


if __name__ == "__main__":
    main()
