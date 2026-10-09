#!/usr/bin/env python3
"""Validate the selection rule on the WHOLE released campaign: 1,440 designs, 354 binders,
16 targets -- not the 150-design / 12-binder TNF-alpha slice every prior number here rests on.

WHY POOLING ACROSS TARGETS WOULD BE A TRAP, AND WHY THIS SCRIPT REFUSES TO DO IT.
Measured hit rate ranges from 0% (Mature GDF-8, MBP) to 80% (TREM2). Pool all 1,440 designs and
any quantity correlated with WHICH TARGET it is -- binder length, target size, interface area --
scores a high AUC without carrying one bit about whether a given design binds. That is Simpson's
paradox, and on this dataset it is not hypothetical: the between-target variance dwarfs the
within-target signal.

So every AUC here is WITHIN-TARGET: concordant pairs are counted only between a binder and a
non-binder OF THE SAME TARGET, then summed across targets. Permutations shuffle labels within
target too. The pooled-across-targets figure is printed alongside, labelled as the trap, so the
size of the inflation is visible rather than assumed.

    validate_selection_rule.py --selftest
    validate_selection_rule.py --sweep        # 200 cells, within-target AUC, Bonferroni
    validate_selection_rule.py --holdout      # select on 8 targets, test on the other 8
    validate_selection_rule.py --rounds       # the optimization-depth effect, all 16 targets
    validate_selection_rule.py --composition  # the His/pI filter, all 16 targets
"""
import csv
import math
import re
import os
import random
import statistics as st
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
os.chdir(REPO)
D = "reference/anthropic-campaign"
# STOICHIOMETRY IS TARGET-SPECIFIC, AND TREATING IT AS A SHARED DIMENSION IS A BUG.
# TNF-alpha is the ONLY target with 1to3/3to3; 11 of 16 are 1to1, 5 have 1to2, 3 have 2to2,
# Cas9 adds `rnp`. A sweep over (model, stoichiometry) therefore produces cells that exist for
# ONE target, which silently collapses a 16-target analysis back to the TNF-alpha slice -- the
# first run of this script did exactly that and reported 12 positives against 138 negatives.
# Fix: each target is scored at its own "one binder against the full native oligomer"
# stoichiometry -- 1to1 for monomers, 1to2 for dimers, 1to3 for the trimer -- chosen as the
# 1toN label present with the largest N. That is the comparison section 7 argues for on
# biological grounds, and it is the only one defined for every target.
STOICH_RE = re.compile(r"^1to(\d+)$")

METRICS = ["ipsae_min", "ipsae_max", "iptm_pae", "plddt_binder", "plddt_target",
           "pae_interface_min", "pae_interface_mean", "sc_dockq",
           "n_interface_contacts", "has_clash"]
LOWER_IS_BETTER = {"pae_interface_min", "pae_interface_mean", "has_clash"}


def load():
    lab = {}
    for r in csv.DictReader(open(f"{D}/all_designs.tsv"), delimiter="\t"):
        lab[r["uuid"]] = r
    if len(lab) != 1440:
        sys.exit(f"REFUSED: expected 1440 designs, got {len(lab)}")
    # collapse seeds by mean per (uuid, model, stoich, metric)
    acc = defaultdict(lambda: defaultdict(list))
    for r in csv.DictReader(open(f"{D}/all_cofold.tsv"), delimiter="\t"):
        k = (r["uuid"], r["cofolding_model"], r["stoichiometry"])
        for m in METRICS:
            v = r[m].strip()
            if not v or v.lower() in ("nan", "none"):
                continue
            if v.lower() in ("true", "false"):      # has_clash ships as a boolean
                v = "1" if v.lower() == "true" else "0"
            acc[k][m].append(float(v))
    cells = {k: {m: st.mean(v) for m, v in d.items()} for k, d in acc.items()}
    # the canonical stoichiometry per target: the 1toN present with the largest N
    bytgt = defaultdict(set)
    for (u, mo, so) in cells:
        bytgt[lab[u]["target"]].add(so)
    canon = {}
    for t, ss in bytgt.items():
        c = [(int(m.group(1)), x) for x in ss for m in [STOICH_RE.match(x)] if m]
        if not c:
            sys.exit(f"REFUSED: target {t} has no 1toN stoichiometry among {sorted(ss)}")
        canon[t] = max(c)[1]
    return lab, cells, canon


def is_binder(r):
    return r["binder_final"].strip().lower() in ("true", "1", "yes")


def within_target_auc(pairs_by_target):
    """pairs_by_target: {target: (list_pos_scores, list_neg_scores)}. Higher = binder.
    Returns (auc, n_pos, n_neg, n_pairs, per_target_aucs)."""
    conc = tot = 0.0
    np_ = nn = 0
    per = {}
    for t, (P, N) in pairs_by_target.items():
        if not P or not N:
            continue
        c = sum(1.0 if a > b else (0.5 if a == b else 0.0) for a in P for b in N)
        conc += c; tot += len(P) * len(N)
        np_ += len(P); nn += len(N)
        per[t] = c / (len(P) * len(N))
    if tot == 0:
        return None
    return conc / tot, np_, nn, int(tot), per


def cell_scores(lab, cells, canon, model, metric):
    """{target: ([binder scores], [non-binder scores])} at each target's canonical stoichiometry."""
    out = defaultdict(lambda: ([], []))
    sign = -1.0 if metric in LOWER_IS_BETTER else 1.0
    for uuid, r in lab.items():
        c = cells.get((uuid, model, canon[r["target"]]))
        if not c or metric not in c:
            continue
        out[r["target"]][0 if is_binder(r) else 1].append(sign * c[metric])
    return out


def perm_p(pairs_by_target, obs, n=20000, seed=20261008):
    """Shuffle labels WITHIN target."""
    rng = random.Random(seed)
    pool = {t: (P + N, len(P)) for t, (P, N) in pairs_by_target.items() if P and N}
    hits = 0
    for _ in range(n):
        d = {}
        for t, (allv, k) in pool.items():
            v = allv[:]; rng.shuffle(v)
            d[t] = (v[:k], v[k:])
        a = within_target_auc(d)[0]
        if abs(a - 0.5) >= abs(obs - 0.5):
            hits += 1
    return (hits + 1) / (n + 1)


def sweep(verbose=True, keep_targets=None, loaded=None):
    lab, cells, canon = loaded or load()
    if keep_targets:
        lab = {u: r for u, r in lab.items() if r["target"] in keep_targets}
    models = sorted({k[1] for k in cells})
    res = []
    for mo in models:
        for me in METRICS:
            pb = cell_scores(lab, cells, canon, mo, me)
            r = within_target_auc(pb)
            if r is None:
                continue
            res.append(dict(model=mo, metric=me, auc=r[0], npos=r[1], nneg=r[2],
                            npairs=r[3], per=r[4]))
    res.sort(key=lambda x: -abs(x["auc"] - 0.5))
    if verbose:
        print(f"cells scanned: {len(res)}   Bonferroni bar 0.05/{len(res)} = {0.05/len(res):.2e}")
        print(f"{'model':9s} {'metric':22s} {'within':>8} {'POOLED':>8} {'pos':>5} {'neg':>5} {'targets':>8}")
        for x in res[:16]:
            pb = cell_scores(lab, cells, canon, x["model"], x["metric"])
            P = [v for t in pb for v in pb[t][0]]; N = [v for t in pb for v in pb[t][1]]
            pooled = sum(1.0 if a > b else (0.5 if a == b else 0.0)
                         for a in P for b in N) / (len(P) * len(N))
            print(f"{x['model']:9s} {x['metric']:22s} {x['auc']:8.4f} {pooled:8.4f} "
                  f"{x['npos']:5d} {x['nneg']:5d} {len(x['per']):8d}")
    return res, (lab, cells, canon)


def rounds_effect(loaded=None):
    lab, cells, canon = loaded or load()
    buckets = [(0, 0), (1, 1), (2, 3), (4, 7), (8, 99)]
    print(f"{'rounds':>8} {'designs':>8} {'binders':>8} {'rate':>7}   per-target rates")
    for lo, hi in buckets:
        sel = [r for r in lab.values()
               if r["n_optimization_rounds"].strip().isdigit()
               and lo <= int(r["n_optimization_rounds"]) <= hi]
        if not sel:
            continue
        b = sum(1 for r in sel if is_binder(r))
        byt = defaultdict(lambda: [0, 0])
        for r in sel:
            byt[r["target"]][0] += 1
            byt[r["target"]][1] += is_binder(r)
        shown = ", ".join(f"{t}:{v[1]}/{v[0]}" for t, v in sorted(byt.items())[:6])
        tag = f"{lo}" if lo == hi else f"{lo}-{hi if hi < 99 else '12'}"
        print(f"{tag:>8} {len(sel):8d} {b:8d} {b/len(sel):7.1%}   {shown}")
    # WITHIN-TARGET, so target difficulty cannot drive it
    print("\n  within-target: deep (>=4 rounds) vs shallow (<=1), per target")
    tot_d = tot_s = bd = bs = 0
    for t in sorted({r["target"] for r in lab.values()}):
        D = [r for r in lab.values() if r["target"] == t
             and r["n_optimization_rounds"].strip().isdigit()
             and int(r["n_optimization_rounds"]) >= 4]
        S = [r for r in lab.values() if r["target"] == t
             and r["n_optimization_rounds"].strip().isdigit()
             and int(r["n_optimization_rounds"]) <= 1]
        if not D or not S:
            continue
        d = sum(1 for r in D if is_binder(r)); s = sum(1 for r in S if is_binder(r))
        tot_d += len(D); tot_s += len(S); bd += d; bs += s
        print(f"    {t:16s} deep {d:3d}/{len(D):3d} = {d/len(D):6.1%}   "
              f"shallow {s:3d}/{len(S):3d} = {s/len(S):6.1%}")
    if tot_d and tot_s:
        print(f"    {'POOLED (paired targets)':16s} deep {bd}/{tot_d} = {bd/tot_d:.1%}   "
              f"shallow {bs}/{tot_s} = {bs/tot_s:.1%}")
    return None


def composition_effect(loaded=None):
    import importlib.util
    sp = importlib.util.spec_from_file_location("_cf", os.path.join(HERE, "comp_filter.py"))
    cf = importlib.util.module_from_spec(sp); sp.loader.exec_module(cf)
    lab, cells, canon = loaded or load()
    print(f"{'target':16s} {'in:bind/n':>12} {'rate':>7}   {'out:bind/n':>12} {'rate':>7}")
    ti = to = bi = bo = 0
    for t in sorted({r["target"] for r in lab.values()}):
        I = O = BI = BO = 0
        for r in lab.values():
            if r["target"] != t:
                continue
            try:
                p = cf.passes(cf.features(r["sequence"]))
            except ValueError:
                continue
            if p:
                I += 1; BI += is_binder(r)
            else:
                O += 1; BO += is_binder(r)
        ti += I; to += O; bi += BI; bo += BO
        if I:
            print(f"{t:16s} {BI:5d}/{I:<6d} {BI/I:7.1%}   {BO:5d}/{O:<6d} "
                  f"{(BO/O if O else 0):7.1%}")
    print(f"\n{'ALL 16':16s} {bi:5d}/{ti:<6d} {bi/ti:7.1%}   {bo:5d}/{to:<6d} {bo/to:7.1%}")
    print(f"enrichment over base rate: {(bi/ti)/((bi+bo)/(ti+to)):.2f}x")
    return None


def holdout(loaded=None):
    loaded = loaded or load()
    lab = loaded[0]
    tg = sorted({r["target"] for r in lab.values()})
    A, B = tg[0::2], tg[1::2]
    for name, fit, test in (("A->B", A, B), ("B->A", B, A)):
        rf, _ = sweep(verbose=False, keep_targets=fit, loaded=loaded)
        best = rf[0]
        rt, _ = sweep(verbose=False, keep_targets=test, loaded=loaded)
        got = next(x for x in rt if x["model"] == best["model"] and x["metric"] == best["metric"])
        champ = rt[0]
        print(f"{name}: selected {best['model']}/{best['metric']} on {len(fit)} targets "
              f"(AUC {best['auc']:.4f})")
        print(f"       -> held-out AUC {got['auc']:.4f} on {len(test)} targets "
              f"(best possible there was {champ['model']}/{champ['metric']} at {champ['auc']:.4f})")
    return None


def main():
    a = sys.argv
    L = load()
    if "--sweep" in a:
        res, _ = sweep(loaded=L)
        top = res[0]
        pv = perm_p(cell_scores(L[0], L[1], L[2], top["model"], top["metric"]), top["auc"])
        print(f"\ntop cell {top['model']}/{top['metric']}: within-target AUC {top['auc']:.4f}, "
              f"within-target permutation p = {pv:.5f}")
        print("per-target AUC: " + ", ".join(
            f"{t} {v:.2f}" for t, v in sorted(top["per"].items(), key=lambda kv: -kv[1])))
        print("\nmetric ceilings across the 10 models (within-target):")
        for me in METRICS:
            c = [x for x in res if x["metric"] == me]
            if c:
                b = max(c, key=lambda x: abs(x["auc"] - 0.5))
                print(f"   {me:22s} best {b['auc']:.4f} ({b['model']})")
    if "--rounds" in a:
        print()
        rounds_effect(L)
    if "--composition" in a:
        print()
        composition_effect(L)
    if "--holdout" in a:
        print()
        holdout(L)


def selftest():
    lab, cells, canon = load()
    print(f"  ok  canonical stoichiometry per target: " +
          ", ".join(f"{t}={v}" for t, v in sorted(canon.items())[:4]) + ", ...")
    print(f"  ok  loaded {len(lab)} designs, {len(cells)} design x model x stoich cells")
    nb = sum(1 for r in lab.values() if is_binder(r))
    assert nb == 354, nb
    print(f"  ok  {nb} measured binders across {len({r['target'] for r in lab.values()})} targets")
    # T2: a perfect separator must read 1.0 within target
    fake = {"A": ([1, 2, 3], [0, 0, 0]), "B": ([5, 6], [4, 4])}
    assert within_target_auc(fake)[0] == 1.0
    print("  ok  T2 a perfect within-target separator reads 1.0")
    # T3 MUTATION: a target-identity-only score must read ~0.5 within target and HIGH pooled
    byt = {}
    for i, t in enumerate(sorted({r["target"] for r in lab.values()})):
        P = [r for r in lab.values() if r["target"] == t and is_binder(r)]
        N = [r for r in lab.values() if r["target"] == t and not is_binder(r)]
        byt[t] = ([float(i)] * len(P), [float(i)] * len(N))
    w = within_target_auc(byt)[0]
    assert abs(w - 0.5) < 1e-9, w
    allP = [v for t in byt for v in byt[t][0]]; allN = [v for t in byt for v in byt[t][1]]
    c = sum(1.0 if x > y else (0.5 if x == y else 0.0) for x in allP for y in allN)
    pooled = c / (len(allP) * len(allN))
    print(f"  ok  T3 MUTATION: a score that encodes ONLY target identity reads within-target "
          f"{w:.3f} and pooled {pooled:.3f}")
    assert abs(pooled - 0.5) > 0.05, "pooling did not inflate -- the trap guard is vacuous"
    print("      so the within-target construction is what blocks the Simpson trap, not luck")
    # T4 orientation
    assert "pae_interface_min" in LOWER_IS_BETTER and "ipsae_min" not in LOWER_IS_BETTER
    print("  ok  T4 inverted metrics declared explicitly")
    print("\nself-tests passed: 4")
    return 0


if __name__ == "__main__":
    if len(sys.argv) == 1 or "--selftest" in sys.argv:
        sys.exit(selftest())
    main()
