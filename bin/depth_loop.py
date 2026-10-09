#!/usr/bin/env python3
"""Predict-then-redesign loop control, with the oracle rule enforced in code.

WHAT THE LOOP IS. The organisers' documented procedure: take a design whose predicted complex
passes the pose gate, feed that PREDICTED complex -- not the designed one -- back into a sequence
design model with the target chains held fixed, re-score, and repeat while the metric improves,
keeping every round under the same root backbone. They mandate >= 2 rounds and >= 5 on hard
targets. We ran zero, and their zero-round cell is 0 of 37.

WHY THIS FILE EXISTS RATHER THAN A SHELL PIPELINE. The loop's danger is not mechanical, it is
governance. Frozen decision C1 forbids a design objective that uses our ranking instrument,
because designing on the ranker makes December's question unanswerable. A predict-then-redesign
loop makes its co-folder the design oracle by construction. The resolution pre-registered in
analysis/02-tnf/PREREG-DEPTH-ARM-2026-10-08.md is that selection reads ONE statistic -- CA
sc_DockQ against the designed backbone, which is agreement with a reference the predictor never
sees -- and never a confidence score, which is the predictor's opinion of itself.

A rule in a document is honoured by whoever remembers it. So select_parent() REFUSES any row that
still carries a confidence field. You cannot select on ipSAE here by forgetting; you have to
delete the guard, which shows up in a diff.

    depth_loop.py --selftest
    depth_loop.py --score --designed-dir <genie pdbs> --cofold-dir <run out> --out <tsv>
    depth_loop.py --select --rounds <tsv,tsv,...>      # continuation verdict + next parents
"""
import csv
import glob
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("_scd", os.path.join(HERE, "sc_dockq.py"))
_scd = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_scd)

# ---- the pre-registered selector, and everything it may not look at
SELECTOR_KEY = "ca_sc_dockq"
POSE_GATE_LRMS = 10.0        # stage-A entry bar; a parent regressing above this stops the arm
MIN_DELTA = 0.01             # per-round improvement required to continue
PATIENCE = 2                 # consecutive flat rounds before stopping
MAX_ROUNDS = 10              # cap, not target

FORBIDDEN_IN_SELECTION = frozenset({
    "ipsae_min", "ipsae_max", "ipsae", "iptm", "iptm_pae", "ptm",
    "plddt", "plddt_binder", "plddt_target",
    "pae_interface_min", "pae_interface_mean", "pae",
})


class OracleViolation(Exception):
    """Raised when selection is handed a confidence score. Not catchable by accident."""


def select_parent(rows):
    """Best row by CA sc_DockQ. REFUSES if any row still carries a confidence field.

    Strip confidence columns before calling. That strip is the audit trail: a reader of the
    caller can see exactly which statistics reached the decision.
    """
    if not rows:
        raise ValueError("REFUSED: no rows to select from")
    for r in rows:
        leaked = FORBIDDEN_IN_SELECTION & {k.lower() for k in r}
        if leaked:
            raise OracleViolation(
                f"REFUSED: selection was handed confidence field(s) {sorted(leaked)}. "
                f"Frozen decision C1 and PREREG-DEPTH-ARM allow exactly one selector: "
                f"{SELECTOR_KEY}. Strip these columns before selecting.")
        if SELECTOR_KEY not in r:
            raise ValueError(f"REFUSED: row {r.get('id')} has no {SELECTOR_KEY}")
    return max(rows, key=lambda r: float(r[SELECTOR_KEY]))


def continuation(best_per_round):
    """(verdict, reason) from the sequence of per-round best selector values."""
    n = len(best_per_round)
    if n == 0:
        raise ValueError("REFUSED: no rounds scored")
    if n >= MAX_ROUNDS:
        return "STOP", f"round cap reached ({MAX_ROUNDS})"
    if n == 1:
        return "CONTINUE", "round 1 scored, no prior round to compare"
    flat = 0
    for i in range(n - 1, 0, -1):
        if best_per_round[i] - best_per_round[i - 1] < MIN_DELTA:
            flat += 1
        else:
            break
    if flat >= PATIENCE:
        return "STOP", (f"{flat} consecutive rounds improved by < {MIN_DELTA} "
                        f"(last: {best_per_round[-PATIENCE-1:]})")
    return "CONTINUE", (f"round {n} improved by "
                        f"{best_per_round[-1] - best_per_round[-2]:+.4f}")


def pose_regressed(rows):
    """True if every row sits worse than the entry gate -- the arm's other stop."""
    return all(float(r["lrms"]) > POSE_GATE_LRMS for r in rows)


def score_round(designed_dir, cofold_dir, expect=None):
    """One row per co-folded design: CA sc_DockQ against its own Genie 3 backbone.

    Joins on the backbone index parsed from the design id, NOT on file order. Refuses on a
    missing or duplicated backbone rather than scoring the wrong pair.

    `expect` is a compiled regex every design id must match. IT IS NOT OPTIONAL IN PRACTICE.
    On 2026-10-09 an aborted round-2 run had already written 20 folds to the Volume under the
    same run name; the relaunch recovered all 52, and because the stale ids parsed to the same
    lineage LABELS as the new ones, two lineages were won by designs from the collapsed beam and
    backbone 3 was dropped for the second time in one night. Stale folds in a shared namespace
    are indistinguishable from fresh ones unless the id format is checked.
    """
    import re as _re
    designed = {}
    for p in sorted(glob.glob(os.path.join(designed_dir, "tnfa_corrected_*.pdb"))):
        idx = os.path.basename(p)[len("tnfa_corrected_"):-len(".pdb")]
        if idx in designed:
            raise SystemExit(f"REFUSED: duplicate backbone index {idx} in {designed_dir}")
        designed[idx] = p
    if not designed:
        raise SystemExit(f"REFUSED: no backbones in {designed_dir}")

    rows, refused = [], []
    seen = set()
    for d in sorted(glob.glob(os.path.join(cofold_dir, "tnfa_corrected_*"))):
        if not os.path.isdir(d):
            continue
        did = os.path.basename(d)
        if expect is not None and not expect.search(did):
            continue                      # a stale fold from an earlier run under this name
        if did in seen:
            raise SystemExit(f"REFUSED: duplicate design dir {did} -- collapse seeds first")
        seen.add(did)
        idx = did[len("tnfa_corrected_"):].split("_")[0]
        if idx not in designed:
            raise SystemExit(f"REFUSED: {did} has no backbone tnfa_corrected_{idx}.pdb")
        cifs = [f for f in sorted(glob.glob(os.path.join(d, "*.cif")))]
        if len(cifs) != 1:
            raise SystemExit(f"REFUSED: {did} holds {len(cifs)} cif(s); expected exactly 1")
        r = _scd.sc_dockq(designed[idx], cifs[0], d_bind="A", p_bind="D", offsets=(0, 5, -5))
        if r is None:
            refused.append(did)
            continue
        rows.append(dict(id=did, backbone=idx, ca_sc_dockq=round(r[0], 4),
                         fnat=round(r[1], 4), lrms=round(r[2], 3), irms=round(r[3], 3)))
    return rows, refused


def selftest():
    import tempfile

    # T1 the selector picks the best CA sc_DockQ
    rows = [dict(id="a", ca_sc_dockq=0.11, lrms=20.0),
            dict(id="b", ca_sc_dockq=0.42, lrms=8.0),
            dict(id="c", ca_sc_dockq=0.30, lrms=9.0)]
    assert select_parent(rows)["id"] == "b"
    print("  ok  T1 selector picks the best CA sc_DockQ")

    # T2 THE GUARD. A confidence field in the row must REFUSE, not be ignored.
    for bad in ("ipsae_min", "iptm_pae", "plddt_binder", "pae_interface_mean", "IPSAE_MAX"):
        leaky = [dict(r, **{bad: 0.99}) for r in rows]
        try:
            select_parent(leaky)
        except OracleViolation as e:
            assert bad.lower() in str(e), str(e)
        else:
            raise AssertionError(f"selection accepted a {bad} column -- the guard is dead")
    print("  ok  T2 GUARD: selection refuses ipsae/iptm/plddt/pae columns, case-insensitively")

    # T3 MUTATION: emptying the forbidden set must break T2. Proves T2 tests the guard
    # and not something incidental.
    global FORBIDDEN_IN_SELECTION
    keep = FORBIDDEN_IN_SELECTION
    FORBIDDEN_IN_SELECTION = frozenset()
    try:
        select_parent([dict(r, ipsae_min=0.99) for r in rows])
    except OracleViolation:
        raise AssertionError("mutation did not disarm the guard -- T2 may be vacuous")
    finally:
        FORBIDDEN_IN_SELECTION = keep
    # and the guard must be live again now that the set is restored
    try:
        select_parent([dict(r, ipsae_min=0.99) for r in rows])
    except OracleViolation:
        pass
    else:
        raise AssertionError("the guard did not come back after the mutation")
    print("  ok  T3 MUTATION: clearing the forbidden set lets a leak through and restoring it")
    print("      re-arms the guard, so T2 tests the guard rather than something incidental")

    # T4 continuation rule
    assert continuation([0.10])[0] == "CONTINUE"
    assert continuation([0.10, 0.25])[0] == "CONTINUE"
    assert continuation([0.10, 0.25, 0.255])[0] == "CONTINUE", "one flat round must not stop"
    assert continuation([0.10, 0.25, 0.255, 0.256])[0] == "STOP", "two flat rounds must stop"
    assert continuation([0.1] * MAX_ROUNDS)[0] == "STOP"
    v, why = continuation([0.10, 0.25, 0.255, 0.256])
    print(f"  ok  T4 continuation: one flat round continues, two stop ({why})")

    # T5 a pose regression across every row is a stop
    assert pose_regressed([dict(lrms=31.0), dict(lrms=12.0)])
    assert not pose_regressed([dict(lrms=31.0), dict(lrms=9.0)])
    print(f"  ok  T5 pose regression: all rows above {POSE_GATE_LRMS} A is a stop")

    # T6 score_round refuses a duplicated design dir (the Aposctrl5 seed collision)
    d = tempfile.mkdtemp()
    os.makedirs(os.path.join(d, "des"))
    open(os.path.join(d, "des", "tnfa_corrected_7.pdb"), "w").close()
    os.makedirs(os.path.join(d, "cof", "tnfa_corrected_7_s1"))
    try:
        score_round(os.path.join(d, "des"), os.path.join(d, "cof"))
    except SystemExit as e:
        assert "expected exactly 1" in str(e), str(e)
    else:
        raise AssertionError("a design dir with no cif must refuse")
    print("  ok  T6 score_round refuses a design dir without exactly one structure")

    # T7 score_round refuses a co-fold with no matching backbone
    os.makedirs(os.path.join(d, "cof2", "tnfa_corrected_99_s1"))
    open(os.path.join(d, "cof2", "tnfa_corrected_99_s1", "x.cif"), "w").close()
    try:
        score_round(os.path.join(d, "des"), os.path.join(d, "cof2"))
    except SystemExit as e:
        assert "no backbone" in str(e), str(e)
    else:
        raise AssertionError("an unmatched design must refuse, not be scored against the wrong backbone")
    print("  ok  T7 score_round refuses a design with no matching backbone (no silent mis-join)")

    # T8 THE STALE-FOLD GUARD. A round-2 tree holding one fresh id and one id from an aborted
    # earlier run under the same name must yield ONLY the fresh one.
    import re as _re2
    d2 = tempfile.mkdtemp()
    os.makedirs(os.path.join(d2, "des"))
    open(os.path.join(d2, "des", "tnfa_corrected_40.pdb"), "w").close()
    for did in ("tnfa_corrected_40_L1r2k5", "tnfa_corrected_40_r2p0k5"):
        os.makedirs(os.path.join(d2, "cof", did))
        open(os.path.join(d2, "cof", did, "x.cif"), "w").close()
    seen = []
    orig = _scd.sc_dockq
    try:
        _scd.sc_dockq = lambda *a, **k: (seen.append(a[1]) or (0.5, 0.5, 5.0, 1.0))
        rows, _ = score_round(os.path.join(d2, "des"), os.path.join(d2, "cof"),
                              expect=_re2.compile(r"_L\d+r2k\d+$"))
    finally:
        _scd.sc_dockq = orig
    ids = sorted(r["id"] for r in rows)
    assert ids == ["tnfa_corrected_40_L1r2k5"], ids
    print("  ok  T8 GUARD: a stale `_r2p0k5` fold sharing the Volume name is skipped; "
          "only the fresh `_L1r2k5` is scored")
    # T8b MUTATION: without `expect` BOTH are scored, which is the 2026-10-09 bug
    try:
        _scd.sc_dockq = lambda *a, **k: (0.5, 0.5, 5.0, 1.0)
        rows2, _ = score_round(os.path.join(d2, "des"), os.path.join(d2, "cof"))
    finally:
        _scd.sc_dockq = orig
    assert len(rows2) == 2, len(rows2)
    print("      MUTATION: dropping `expect` scores both, reproducing the contamination")
    print("\nself-tests passed: 8")
    return 0


if __name__ == "__main__":
    a = sys.argv
    if len(a) == 1 or "--selftest" in a:
        sys.exit(selftest())
    if "--score" in a:
        rows, refused = score_round(a[a.index("--designed-dir") + 1],
                                    a[a.index("--cofold-dir") + 1])
        out = a[a.index("--out") + 1]
        with open(out, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=["id", "backbone", "ca_sc_dockq", "fnat",
                                               "lrms", "irms"], delimiter="\t")
            w.writeheader()
            w.writerows(rows)
        n_gate = sum(1 for r in rows if r["lrms"] <= POSE_GATE_LRMS)
        print(f"scored {len(rows)}, refused {len(refused)} {refused}")
        print(f"reaching lrms <= {POSE_GATE_LRMS} A: {n_gate}")
        print(f"best CA sc_DockQ {max((r['ca_sc_dockq'] for r in rows), default=0):.4f}, "
              f"best lrms {min((r['lrms'] for r in rows), default=0):.3f} A")
        print(f"wrote {out}")
    elif "--select" in a:
        files = a[a.index("--rounds") + 1].split(",")
        best = []
        for f in files:
            rows = list(csv.DictReader(open(f), delimiter="\t"))
            best.append(float(select_parent(rows)[SELECTOR_KEY]))
        v, why = continuation(best)
        print(f"per-round best {SELECTOR_KEY}: {best}")
        print(f"VERDICT: {v} -- {why}")
    else:
        sys.exit(__doc__)
