#!/usr/bin/env python3
"""R1 endpoint split and variant detection, on reviewer request (2026-10-11).

The reviewer's two asks, verbatim: "Separate kinetic and affinity endpoints before finalizing the
calibration accuracy" and "For each complex, list the experimental pHs, endpoint, chain assignments
and related variants."

R1_endpoint_audit_2026-10-11.md answered the first halfway -- it NAMED the kinetic rows without
recomputing accuracy without them -- and omitted related variants entirely. This does both.

VARIANTS ARE DERIVED, NOT ASSERTED. Pairwise binder-chain identity is computed from the deposited
structures in runs/R1-pdb/, because "these two are the same antibody" is exactly the claim that
should rest on content rather than on a name or a memory. It matters for a reason the accuracy
figure hides: if two rows are the same molecule, the set holds fewer independent observations than
it has rows.

    python3 bin/r1_endpoint_split.py
"""
import glob
import itertools
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(HERE))

# (class, want, published_ratio, gate) straight from analysis/02-tnf/R1_corrected_stats.txt
ROWS = {
    "1BRS": ("pos", "release", 1200.0, 3.8334),
    "3SQO": ("neg", "flat", 1.3, 8.1101),
    "3WD5": ("pos", "release", 9.0, 3.2715),
    "4K71": ("pos", "tighten", 760.0, 6873.0912),
    "4N0U": ("pos", "tighten", 170.0, 12.5429),
    "5B71": ("pos", "release", 1105.0, 0.0145),
    "5HYS": ("neg", "flat", 1.3, 2.6084),
    "5I5K": ("pos", "release", 21.0, 3.2917),
    "5TRU": ("neg", "flat", 1.1, 1.1734),
    "6FGB": ("neg", "flat", 1.3, 4.5803),
    "7Q15": ("pos", "tighten", 20.0, 2.7318),
    "7SU0": ("pos", "tighten", 77.0, 140.3163),
    "7SU1": ("pos", "tighten", 20.0, 6.3872),
    "8J6F": ("neg", "flat", 2.2, 45.4182),
    "8TBQ": ("pos", "tighten", 1000.0, 0.1045),
    "9MI6": ("neg", "flat", 1.8, 1.9220),
    "9S60": ("neg", "flat", 1.6, 5.4442),
    "9X1H": ("pos", "release", 120.0, 1.9088),
}

# (basic pH, acidic pH, endpoint, endpoint_class) from R1_endpoint_audit_2026-10-11.md.
# endpoint_class: "affinity" = the quoted ratio is an equilibrium constant ratio (KD or Ki);
#                 "kinetic"  = the quoted ratio is a RATE ratio and nothing else.
# A row reporting BOTH is "affinity", because the ratio we scored against is the KD ratio; it is
# marked so the reader can see which rows had a rate measurement alongside.
META = {
    "1BRS": (8.0, 5.0, "Ki", "affinity", False),
    "3SQO": (7.4, 6.0, "KD + kd", "affinity", True),
    "3WD5": (7.4, 6.0, "koff ratio", "kinetic", True),
    "4K71": (7.4, 6.0, "KD + ka/kd", "affinity", True),
    "4N0U": (7.4, 5.8, "KD (switchSENSE)", "affinity", False),
    "5B71": (7.4, 5.8, "KD", "affinity", False),
    "5HYS": (7.4, 6.0, "KD", "affinity", False),
    "5I5K": (7.4, 6.0, "KD", "affinity", False),
    "5TRU": (7.4, 6.0, "KD, 8-point series", "affinity", False),
    "6FGB": (7.4, 6.0, "KD + ka/kd", "affinity", True),
    "7Q15": (7.4, 6.0, "KD (SPR)", "affinity", False),
    "7SU0": (7.4, 6.0, "KD", "affinity", False),
    "7SU1": (7.4, 6.0, "KD", "affinity", False),
    "8J6F": (7.4, 6.0, "KD and kd", "affinity", True),
    "8TBQ": (7.4, 5.8, "KD, range endpoints", "affinity", False),
    "9MI6": (7.4, 6.0, "KD, both bounded", "affinity", False),
    "9S60": (7.0, 6.0, "KD (ITC)", "affinity", False),
    "9X1H": (7.4, 6.0, "KD", "affinity", False),
}

# binder chains, from the endpoint audit's chain assignments
BINDER = {
    "1BRS": "D", "3SQO": "H+L", "3WD5": "H+L", "4K71": "A", "4N0U": "E", "5B71": "A+B",
    "5HYS": "A+B", "5I5K": "H+L", "5TRU": "H+L", "6FGB": "H+L", "7Q15": "E", "7SU0": "H+L",
    "7SU1": "H+L", "8J6F": "H+L", "8TBQ": "H+L", "9MI6": "H+L", "9S60": "B", "9X1H": "H+L",
}
TARGET = {
    "1BRS": "A", "3SQO": "A+P", "3WD5": "A", "4K71": "B+C", "4N0U": "A+B", "5B71": "E",
    "5HYS": "G", "5I5K": "B", "5TRU": "C", "6FGB": "A+B", "7Q15": "A+B", "7SU0": "C",
    "7SU1": "C", "8J6F": "I", "8TBQ": "P", "9MI6": "A+B", "9S60": "A", "9X1H": "A",
}

AA3 = {"ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C", "GLN": "Q", "GLU": "E",
       "GLY": "G", "HIS": "H", "ILE": "I", "LEU": "L", "LYS": "K", "MET": "M", "PHE": "F",
       "PRO": "P", "SER": "S", "THR": "T", "TRP": "W", "TYR": "Y", "VAL": "V"}


def binder_seq(pdb):
    """Concatenated one-letter sequence of the binder chains, from the deposited structure."""
    import gemmi
    st = gemmi.read_structure(f"runs/R1-pdb/{pdb}.cif")
    st.setup_entities()
    st.remove_ligands_and_waters()
    want = BINDER[pdb].split("+")
    out = []
    for cn in want:
        ch = st[0].find_chain(cn)
        if ch is None:
            return None
        out.append("".join(AA3.get(r.name, "X") for r in ch))
    return "".join(out)


def identity(a, b):
    """Ungapped identity over the shorter sequence, anchored at the N-terminus.

    Crude on purpose: it only has to separate 'the same antibody' (>0.90) from 'a different one'
    (<0.70 for a shared germline framework). A real alignment would change the third decimal and
    not the call.
    """
    n = min(len(a), len(b))
    if n == 0:
        return 0.0
    return sum(1 for i in range(n) if a[i] == b[i]) / n


def accuracy(keys):
    """Direction accuracy and ratio>1 rate over a subset. -> dict"""
    hit = 0
    for k in keys:
        cls, want, _pub, gate = ROWS[k]
        got = "release" if gate < 1.0 else ("tighten" if gate > 2.0 else "flat")
        # The call rule from R1: <1.0 release, >2.0 tighten, between is flat. Pinned in selftest.
        if got == want:
            hit += 1
    above = sum(1 for k in keys if ROWS[k][3] > 1.0)
    return dict(n=len(keys), correct=hit, acc=hit / len(keys) if keys else 0.0,
                above1=above, above1_rate=above / len(keys) if keys else 0.0)


def selftest():
    # the call rule must reproduce the committed 8/18
    a = accuracy(list(ROWS))
    assert (a["n"], a["correct"]) == (18, 8), a
    assert a["above1"] == 16, a
    print(f"  ok  S1 reproduces the committed figures: {a['correct']}/18 direction, "
          f"{a['above1']}/18 above 1.0")
    # every row carries metadata
    assert set(ROWS) == set(META) == set(BINDER) == set(TARGET)
    print("  ok  S2 all 18 rows carry pHs, endpoint, and chain assignments")
    # the kinetic row is named and is exactly one
    kin = [k for k, v in META.items() if v[3] == "kinetic"]
    assert kin == ["3WD5"], kin
    print(f"  ok  S3 exactly one pure-kinetic row: {kin[0]}")
    print("selftest: 3/3\n")


def main():
    selftest()
    seqs = {k: binder_seq(k) for k in sorted(ROWS)}
    missing = [k for k, v in seqs.items() if v is None]
    if missing:
        sys.exit(f"REFUSED: could not read binder chains for {missing}")

    print("=" * 100)
    print("PER-COMPLEX TABLE (reviewer request: pHs, endpoint, chain assignments, related variants)")
    print("=" * 100)
    # derive variant groups from binder-chain identity
    pairs = []
    for a, b in itertools.combinations(sorted(ROWS), 2):
        idt = identity(seqs[a], seqs[b])
        if idt >= 0.90:
            pairs.append((a, b, idt))
    group = {}
    for a, b, _ in pairs:
        g = group.get(a) or group.get(b) or f"V{len(set(group.values())) + 1}"
        group[a] = group[b] = g

    print(f"\n{'pdb':6s} {'pHs':12s} {'endpoint':22s} {'tgt':8s} {'bdr':6s} "
          f"{'class':5s} {'want':8s} {'pub':>9s} {'gate':>11s} {'call':5s} variant")
    for k in sorted(ROWS):
        cls, want, pub, gate = ROWS[k]
        hi, lo, ep, epc, both = META[k]
        got = "release" if gate < 1.0 else ("tighten" if gate > 2.0 else "flat")
        tag = group.get(k, "-")
        print(f"{k:6s} {f'{hi}/{lo}':12s} {ep:22s} {TARGET[k]:8s} {BINDER[k]:6s} "
              f"{cls:5s} {want:8s} {pub:9.1f} {gate:11.4f} "
              f"{'HIT' if got == want else 'miss':5s} {tag}")

    print("\nVariant pairs detected from deposited binder chains (identity >= 0.90):")
    if pairs:
        for a, b, idt in pairs:
            print(f"  {a} ~ {b}   binder identity {idt:.3f}  ->  NOT independent observations")
    else:
        print("  none")

    print("\n" + "=" * 100)
    print("ACCURACY BY SUBSET  (reviewer: separate kinetic and affinity endpoints)")
    print("=" * 100)
    allk = sorted(ROWS)
    aff = [k for k in allk if META[k][3] == "affinity"]
    kin = [k for k in allk if META[k][3] == "kinetic"]
    pair6074 = [k for k in allk if META[k][0] == 7.4 and META[k][1] == 6.0]
    aff6074 = [k for k in pair6074 if META[k][3] == "affinity"]
    # one row per variant group, keeping the first alphabetically, to count independent molecules
    seen, indep = set(), []
    for k in aff6074:
        g = group.get(k, k)
        if g in seen:
            continue
        seen.add(g)
        indep.append(k)

    for label, keys in [
        ("all rows, as reported", allk),
        ("affinity endpoints only (drops the rate-ratio row)", aff),
        ("pure-kinetic rows", kin),
        ("exact 6.0/7.4 pair, any endpoint", pair6074),
        ("exact 6.0/7.4 pair AND affinity endpoint", aff6074),
        ("...and one row per molecule (variants collapsed)", indep),
    ]:
        if not keys:
            print(f"{label:52s} n=0")
            continue
        a = accuracy(keys)
        print(f"{label:52s} n={a['n']:2d}  direction {a['correct']:2d}/{a['n']:<2d} "
              f"= {a['acc']:5.1%}   ratio>1 {a['above1']:2d}/{a['n']:<2d} = {a['above1_rate']:5.1%}")

    print("\nWhat a constant predictor scores on each subset, for comparison:")
    for label, keys in [("all rows", allk), ("6.0/7.4 + affinity", aff6074)]:
        best = max(sum(1 for k in keys if ROWS[k][1] == w) for w in ("release", "tighten", "flat"))
        print(f"  {label:20s} always-answer-the-commonest-label: {best}/{len(keys)} "
              f"= {best / len(keys):.1%}")

    print("\nRows excluded from the matched subset, and why:")
    for k in allk:
        why = []
        if META[k][3] == "kinetic":
            why.append("rate ratio, not an equilibrium ratio")
        if not (META[k][0] == 7.4 and META[k][1] == 6.0):
            why.append(f"pH pair {META[k][0]}/{META[k][1]}, not 7.4/6.0")
        if k in group and k not in indep and k in aff6074:
            why.append(f"variant of {group[k]} partner, collapsed")
        if why:
            print(f"  {k}: {'; '.join(why)}")


if __name__ == "__main__":
    main()
