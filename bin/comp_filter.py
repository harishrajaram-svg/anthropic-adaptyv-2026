#!/usr/bin/env python3
"""The winners' compositional filter, measured on the released campaign and applied to ours.

WHY THIS EXISTS. All 12 wet-lab-confirmed TNF-alpha binders in the released campaign sit in a
narrow chemical band: 11 of 12 carry one or two histidines, every one is net-negative, and every
one has pI between 4.5 and 5.3. Our 48 submitted-arm designs sit outside it -- median three
histidines, net charge 0, pI 7.01 -- because bin/mpnn_constraints.py forces histidines in to build
a pH switch. The seed sequences BEFORE that step are inside the band.

PROVENANCE IS DISCLOSED, NOT HIDDEN. These three cuts were chosen after seeing which designs
bound, and roughly eleven features were examined against the same 12 binders, of which 11 live in
3 sequence families. So the effective sample is ~3 independent successes, not 34 designs. This is
a FILTER with a post-hoc provenance, never a rule, and it is not evidence that a histidine at
position 16 causes binding.

    comp_filter.py --selftest
    comp_filter.py --faa-dir <dir>            # filter a directory of .faa
    comp_filter.py --tsv <file> --seq-col sequence --id-col design
    comp_filter.py --validate                 # re-measure the filter on the released 150
"""
import csv
import glob
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

# pKa set and isoelectric() are reused from bin/express_qc_p2.py so the project carries ONE
# pI implementation. A second one would be a second answer.
sys.path.insert(0, HERE)
import importlib.util
_spec = importlib.util.spec_from_file_location("_qc", os.path.join(HERE, "express_qc_p2.py"))
_qc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_qc)
isoelectric = _qc.isoelectric

# ---- the filter: TWO cuts and a length floor
HIS_MIN, HIS_MAX = 1, 2       # 11 of 12 binders; the 12th carries zero
PI_MAX = 5.5                  # binders 4.53-5.26
LEN_MIN = 80                  # all 12 binders are 80 or 83

# NET CHARGE IS NOT A CUT, AND THE SELFTEST IS WHY. A netq <= -3 term was in the first version
# of this filter. T5 then showed it admits not one extra non-binder when removed: over the
# released 150, pI <= 5.5 already implies netq <= -3, so the term was decorative. It would have
# looked like a third independent line of evidence in the write-up while doing nothing. net_charge()
# is still computed and reported, because it is descriptive and cheap -- it just does not gate.
NETQ_REPORTED_NOT_GATED = True


def net_charge(seq):
    """Formal charge at neutral pH: K+R minus D+E. Not a pH-dependent quantity -- the
    pI below is the pH-dependent one, and they are reported separately on purpose."""
    return sum(seq.count(a) for a in "KR") - sum(seq.count(a) for a in "DE")


def features(seq):
    seq = seq.strip().upper()
    if not seq:
        raise ValueError("REFUSED: empty sequence")
    bad = set(seq) - set("ACDEFGHIKLMNPQRSTVWY")
    if bad:
        raise ValueError(f"REFUSED: non-standard residues {sorted(bad)}")
    return {
        "L": len(seq),
        "his": seq.count("H"),
        "netq": net_charge(seq),
        "pi": isoelectric(seq),
        "pro_gly_pct": 100.0 * (seq.count("P") + seq.count("G")) / len(seq),
    }


def passes(f):
    return (HIS_MIN <= f["his"] <= HIS_MAX
            and f["pi"] <= PI_MAX
            and f["L"] >= LEN_MIN)


def _fisher_two_sided(a, b, c, d):
    def lf(n):
        return math.lgamma(n + 1)

    def p(a, b, c, d):
        return math.exp(lf(a + b) + lf(c + d) + lf(a + c) + lf(b + d)
                        - lf(a + b + c + d) - lf(a) - lf(b) - lf(c) - lf(d))

    obs, tot = p(a, b, c, d), 0.0
    for i in range(0, min(a + b, a + c) + 1):
        j, k, l = a + b - i, a + c - i, d - (a - i)
        if j < 0 or k < 0 or l < 0:
            continue
        q = p(i, j, k, l)
        if q <= obs + 1e-12:
            tot += q
    return tot


def validate():
    """Re-measure the filter against the released labels. REFUSES if it stops enriching."""
    path = os.path.join(REPO, "reference/anthropic-campaign/tnfa_designs.tsv")
    rows = list(csv.DictReader(open(path), delimiter="\t"))
    if len(rows) != 150:
        raise SystemExit(f"REFUSED: expected 150 released designs, got {len(rows)}")
    pos = [r for r in rows if r["binder_final"].strip().lower() in ("true", "1", "yes")]
    neg = [r for r in rows if r not in pos]
    if len(pos) != 12:
        raise SystemExit(f"REFUSED: expected 12 measured binders, got {len(pos)}")
    pb = sum(passes(features(r["sequence"])) for r in pos)
    nb = sum(passes(features(r["sequence"])) for r in neg)
    prec = pb / (pb + nb)
    base = len(pos) / len(rows)
    pval = _fisher_two_sided(pb, len(pos) - pb, nb, len(neg) - nb)
    print(f"  admits {pb}/12 binders, {nb}/138 non-binders")
    print(f"  precision {prec:.1%} against a {base:.1%} base rate -> {prec/base:.2f}x enrichment")
    print(f"  Fisher two-sided p = {pval:.3g}")
    # fail closed: a filter that no longer enriches must not be used to spend money
    if prec / base < 2.0 or pval > 0.01:
        raise SystemExit("REFUSED: the filter no longer enriches on the released labels")
    return dict(binders_in=pb, nonbinders_in=nb, precision=prec,
                enrichment=prec / base, fisher_p=pval)


def selftest():
    # T1 the filter admits a known binder and rejects a histidine-loaded design
    path = os.path.join(REPO, "reference/anthropic-campaign/tnfa_designs.tsv")
    rows = list(csv.DictReader(open(path), delimiter="\t"))
    # EXACT name, and the label asserted. An endswith() match here silently selected
    # mythos_preview_multi_target_tnfa_rank02 -- a non-binder sharing the suffix -- which is
    # the join-on-names failure this project has a standing rule against.
    rank02 = next(r for r in rows if r["full_name"] == "opus_4_8_multi_target_tnfa_rank02")
    assert rank02["binder_final"].strip().lower() in ("true", "1", "yes"), "T1 fixture is not a binder"
    f = features(rank02["sequence"])
    assert passes(f), f"a measured binder must pass: {f}"
    print(f"  ok  T1 measured binder rank02 passes (his={f['his']} netq={f['netq']} pI={f['pi']:.2f})")

    # T2 MUTATION: add six histidines to that same binder -> must fail on the His cut alone
    mut = rank02["sequence"].strip()[:-6] + "HHHHHH"
    fm = features(mut)
    assert not passes(fm), "a 7-histidine variant must be rejected"
    assert fm["his"] >= 7, fm
    print(f"  ok  T2 MUTATION: +6 His on the same sequence -> rejected (his={fm['his']})")

    # T3 MUTATION: neutralise the charge -> must fail via pI, with His left intact
    s = rank02["sequence"].strip()
    neu = s.replace("E", "K", 12)
    fn = features(neu)
    assert not passes(fn), f"a charge-neutralised variant must be rejected: {fn}"
    print(f"  ok  T3 MUTATION: 12 E->K -> rejected (netq={fn['netq']} pI={fn['pi']:.2f})")

    # T4 the guard refuses malformed input rather than scoring it
    for bad in ("", "ACDEFX"):
        try:
            features(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"must refuse {bad!r}")
    print("  ok  T4 refuses empty and non-standard sequences")

    # T5 every cut is load-bearing: dropping any one changes the admitted count on the 150
    pos = [r for r in rows if r["binder_final"].strip().lower() in ("true", "1", "yes")]
    neg = [r for r in rows if r not in pos]
    full = sum(passes(features(r["sequence"])) for r in neg)
    drops = {}
    for cut in ("his", "pi"):
        def p2(f, cut=cut):
            ok = f["L"] >= LEN_MIN
            if cut != "his":
                ok &= HIS_MIN <= f["his"] <= HIS_MAX
            if cut != "pi":
                ok &= f["pi"] <= PI_MAX
            return ok
        drops[cut] = sum(p2(features(r["sequence"])) for r in neg)
        assert drops[cut] > full, f"dropping the {cut} cut admitted no extra non-binders -- it is inert"
    print(f"  ok  T5 both cuts load-bearing; non-binders admitted rises "
          f"{full} -> {drops} when each is dropped")
    # T5b the dropped net-charge term is confirmed inert rather than merely unused
    with_netq = sum(1 for r in neg if passes(features(r["sequence"]))
                    and features(r["sequence"])["netq"] <= -3)
    assert with_netq == full, (
        f"net charge is NOT inert after all ({with_netq} vs {full}) -- restore it as a cut")
    print(f"  ok  T5b net charge confirmed inert on the released 150 "
          f"({full} admitted either way), so it reports and does not gate")

    # T6 the validation gate fails closed
    v = validate()
    assert v["enrichment"] >= 2.0
    print(f"  ok  T6 validate() enriches {v['enrichment']:.2f}x and refuses below 2.0x")
    print("\nself-tests passed: 6")
    return 0


def _load_faa(d):
    out = {}
    for p in sorted(glob.glob(os.path.join(d, "*.faa"))):
        lines = [l.strip() for l in open(p) if l.strip()]
        out[os.path.basename(p)[:-4]] = "".join(l for l in lines if not l.startswith(">"))
    if not out:
        raise SystemExit(f"REFUSED: no .faa files in {d}")
    return out


def report(seqs, label, out_tsv=None):
    rows = []
    for k, s in sorted(seqs.items()):
        f = features(s)
        rows.append(dict(id=k, **{kk: f[kk] for kk in ("L", "his", "netq", "pi", "pro_gly_pct")},
                         passes=int(passes(f))))
    n = sum(r["passes"] for r in rows)
    import statistics as st
    print(f"\n{label}: n={len(rows)}, PASS {n}")
    print(f"  median his {st.median([r['his'] for r in rows])}, "
          f"netq {st.median([r['netq'] for r in rows])}, "
          f"pI {st.median([r['pi'] for r in rows]):.2f}")
    for r in rows:
        if r["passes"]:
            print(f"    {r['id']:26s} his={r['his']} netq={r['netq']:4d} "
                  f"pI={r['pi']:.2f} P+G={r['pro_gly_pct']:.1f}%")
    if out_tsv:
        with open(out_tsv, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]), delimiter="\t")
            w.writeheader()
            for r in rows:
                r = dict(r); r["pi"] = f"{r['pi']:.3f}"; r["pro_gly_pct"] = f"{r['pro_gly_pct']:.2f}"
                w.writerow(r)
        print(f"  wrote {out_tsv}")
    return rows


if __name__ == "__main__":
    a = sys.argv
    if len(a) == 1 or "--selftest" in a:
        sys.exit(selftest())
    if "--validate" in a:
        print("VALIDATION against the released 150:")
        validate()
        sys.exit(0)
    out = a[a.index("--out") + 1] if "--out" in a else None
    if "--faa-dir" in a:
        d = a[a.index("--faa-dir") + 1]
        report(_load_faa(d), d, out)
    elif "--tsv" in a:
        t = a[a.index("--tsv") + 1]
        idc = a[a.index("--id-col") + 1] if "--id-col" in a else "design"
        sqc = a[a.index("--seq-col") + 1] if "--seq-col" in a else "sequence"
        rows = list(csv.DictReader(open(t), delimiter="\t"))
        report({r[idc]: r[sqc] for r in rows}, t, out)
    else:
        sys.exit(__doc__)
