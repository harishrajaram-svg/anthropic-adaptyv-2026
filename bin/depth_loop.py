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
PATIENCE = 4                 # consecutive flat rounds before stopping; PREREG s5
                             # (B3). 4 flat rounds costs 256 of the 800-fold fuse to
                             # confirm a plateau, which is the price of not stopping
                             # on noise -- single-seed ranking is Spearman 0.538.
MAX_ROUNDS = 16              # cap, not target. AMENDMENT 3. History today:
                             # 10 -> 12 -> 14 -> 8 -> 16, each move arithmetic from
                             # a changing lineage/children/species count, not drift.
                             # all 8 Genie3 TNF binders in the release sit at 8-12
                             # rounds and 0 of 37 zero-round TNF designs bound
                             # anything. The depth arm stopped at 5. 14 comes from
                             # AMENDMENT 2: 6 lineages x 8 children x 2 species =
                             # 96/round, so the 800 fuse buys 8. The four continued
                             # lineages carry 5 rounds already and reach TRUE depth
                             # 13; the two fresh ones reach 8. Both land inside the
                             # 8-12 band where every released TNF binder sits.

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


# ---- C5 + C8, 2026-10-09: two species, and the ipSAE the fenced lineage needs
_fab_spec = importlib.util.spec_from_file_location(
    "_fab", os.path.join(HERE, "..", "analysis", "02-tnf", "fab_ipsae.py"))
_fab = importlib.util.module_from_spec(_fab_spec)
_fab_spec.loader.exec_module(_fab)

IPSAE_RULE = "max_pair"          # pre-registered in fab_ipsae.RULES; METHODS s4 measured
                                 # max_pair and sum_pairs at 0.400 against the true affinity
                                 # order and top_contact at -0.200.


def ipsae_for(cif, target="ABC", binder="D"):
    """`max_pair` ipSAE over binder:target pairs only, or None.

    WHY NOT bin/ipsae_min.py. That module REFUSES any complex with more than one inter-chain
    pair, on purpose: a bare min() across pairs can report the target trimer's own internal
    packing (here ~0.86) as a binding score (here ~0.31). Our construct is 1 binder : 3
    protomers = 6 pairs, so it has no defined answer there. fab_ipsae.aggregate() is this
    project's multi-pair scorer: it filters to binder:target pairs, applies a pre-registered
    rule, and carries check_target_packing(), which fails closed when the TARGET has not folded
    -- the failure that was once nearly recorded as a spectacular selectivity result.
    """
    pae = str(cif).replace(".cif", "_ipsae.json")
    if not os.path.exists(pae):
        return None
    try:
        pairs = _fab.pair_minima(pae, cif)
        vals, why = _fab.aggregate(pairs, tuple(target), tuple(binder), struct=cif)
    except Exception:
        return None
    if not vals:
        return None
    return vals.get(IPSAE_RULE)


def combine_species(per_species, key=SELECTOR_KEY):
    """One row per design carrying the WORSE of each species' `key`.

    PREREG s3 step 3. Refuses rather than falls back when a design is missing from any species:
    a silent fall-back to the species that happens to be present is indistinguishable from
    "mouse was never folded", which is the whole thing this arm exists to stop doing.
    """
    if len(per_species) < 2:
        raise ValueError(f"REFUSED: combine_species needs >= 2 species, got {list(per_species)}")
    index = {}
    for sp, rows in per_species.items():
        seen = {}
        for r in rows:
            if r["id"] in seen:
                raise SystemExit(f"REFUSED: duplicate id {r['id']} in species {sp} "
                                 "-- collapse seeds before combining")
            seen[r["id"]] = r
        index[sp] = seen
    species = sorted(index)
    ids = set(index[species[0]])
    for sp in species[1:]:
        missing = ids ^ set(index[sp])
        if missing:
            raise SystemExit(
                f"REFUSED: {len(missing)} design(s) present in some species and not others, "
                f"e.g. {sorted(missing)[:3]}. Selecting on the worse of two species requires "
                "both; a partial join would silently select on one.")
    out = []
    for did in sorted(ids):
        rows = {sp: index[sp][did] for sp in species}
        worst_sp = min(species, key=lambda sp: float(rows[sp][key]))
        merged = dict(rows[worst_sp])
        merged["worse_species"] = worst_sp
        for sp in species:
            merged[f"{key}_{sp}"] = float(rows[sp][key])
        merged[key] = float(rows[worst_sp][key])
        out.append(merged)
    return out


# ---- the ONE fenced exception, added 2026-10-09
# PREREG-CONSTRAINED-RESTART-2026-10-09.md s2 runs a single DECLARED CONTAMINATED lineage on the
# organisers' own parent-selection rule (protocol line 115: rank on ipSAE and sc_DockQ together,
# per-target z-scores, ipSAE weighted 4 and sc_DockQ weighted 1) as a controlled head-to-head
# against our clean rule. The released campaign used 4:1 throughout, so it contains no such
# control.
#
# THIS IS A SIBLING, NOT A FLAG ON select_parent. select_parent protects six lineages and is left
# byte-identical: weakening it to admit one lineage would put all six behind a conditional. The
# fence here is three locks, all of which must be open:
#   1. an explicit acknowledgement token at the call site;
#   2. every row carries contaminated=True, so the marking travels with the design into the sheet;
#   3. the only confidence field permitted is the one the declared blend is built from.
# The prereg commits IN ADVANCE that designs selected this way are not a submission source
# whatever they score. If this lineage wins, that is a reported finding.
PROTOCOL_BLEND_KEY = "protocol_4to1_z"
PROTOCOL_BLEND_INPUTS = frozenset({"ipsae_min", "z_ipsae_min", "z_ca_sc_dockq"})
_CONTAM_ACK = "declared-contaminated-lineage-prereg-2026-10-09"


def protocol_4to1_blend(rows):
    """Add `protocol_4to1_z` = 4*z(ipsae_min) + 1*z(ca_sc_dockq), z-scored WITHIN the round.

    Z-scored within the round because the two terms are on unrelated scales and a raw 4:1 sum
    would be whichever term happens to have the wider spread. Population is the round, which is
    what "per-target z-scores" means for parent selection.
    """
    import statistics as _st
    if len(rows) < 2:
        raise ValueError("REFUSED: z-scoring needs at least 2 rows")
    out = []
    for key in ("ipsae_min", SELECTOR_KEY):
        vals = [float(r[key]) for r in rows]
        mu = _st.mean(vals)
        sd = _st.pstdev(vals)
        out.append([0.0] * len(rows) if sd == 0 else [(v - mu) / sd for v in vals])
    zi, zd = out
    for r, a, b in zip(rows, zi, zd):
        r["z_ipsae_min"] = round(a, 6)
        r["z_ca_sc_dockq"] = round(b, 6)
        r[PROTOCOL_BLEND_KEY] = round(4.0 * a + 1.0 * b, 6)
    return rows


def select_parent_declared_contaminated(rows, *, acknowledge):
    """Parent selection for the ONE fenced lineage. See the block comment above."""
    if acknowledge != _CONTAM_ACK:
        raise OracleViolation(
            "REFUSED: the 4:1 selector needs the explicit prereg acknowledgement token. "
            "It exists for ONE declared lineage and is not a general-purpose selector.")
    if not rows:
        raise ValueError("REFUSED: no rows to select from")
    for r in rows:
        if not r.get("contaminated"):
            raise OracleViolation(
                f"REFUSED: row {r.get('id')} is not marked contaminated=True. The marking must "
                "travel with the design so it can be excluded from the submission and from any "
                "claim that our ranker predicted our own designs.")
        leaked = (FORBIDDEN_IN_SELECTION - PROTOCOL_BLEND_INPUTS) & {k.lower() for k in r}
        if leaked:
            raise OracleViolation(
                f"REFUSED: row {r.get('id')} carries confidence field(s) {sorted(leaked)} that "
                f"are NOT inputs to the declared 4:1 blend. The fence admits exactly "
                f"{sorted(PROTOCOL_BLEND_INPUTS)}, nothing else.")
        if PROTOCOL_BLEND_KEY not in r:
            raise ValueError(
                f"REFUSED: row {r.get('id')} has no {PROTOCOL_BLEND_KEY}; "
                "call protocol_4to1_blend(rows) first")
    return max(rows, key=lambda r: float(r[PROTOCOL_BLEND_KEY]))


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


def _target_chain_len(path, binder_chain):
    """Modal CA count of the TARGET chains (i.e. every chain that is not the binder).

    Used to DERIVE the designed->predicted residue-numbering offset instead of hardcoding it.
    """
    from collections import Counter
    per = Counter()
    # Try the mmCIF reader, then fall back to ATOM-record parsing. NEVER raise: this function
    # only picks a numbering offset, and a crash here would take down a whole scoring round.
    # The fallback also covers a .cif-named file holding PDB-format text, which this repo's own
    # selftest fixtures do -- found when the first version of this crashed on them.
    if path.endswith((".cif", ".mmcif")):
        try:
            import gemmi
            st = gemmi.read_structure(path); st.setup_entities()
            for ch in st[0]:
                n = sum(1 for r in ch for a in r if a.name == "CA")
                if n:
                    per[ch.name] = n
        except Exception:
            per = Counter()
    if not per:
        try:
            for l in open(path):
                if l.startswith("ATOM") and l[12:16].strip() == "CA":
                    per[l[21]] += 1
        except Exception:
            return None
    tgt = [n for c, n in per.items() if c != binder_chain]
    if not tgt:
        return None
    return Counter(tgt).most_common(1)[0][0]


def numbering_offsets(designed_pdb, predicted_cif, d_bind="A", p_bind="D"):
    """(0, delta, -delta) where delta = predicted target length - designed target length.

    WHY DERIVED AND NOT HARDCODED. The call site used offsets=(0, 5, -5) because the Genie 3
    complex carries 152-residue target chains against a 157-residue human prediction, so 5 is
    the human delta. Scoring the SAME designs against a 156-residue MOUSE prediction needs 4,
    which that set does not contain -- measured 2026-10-09, it cost the best design 0.4944
    against its true 0.6286, and it moved 15 of 28 designs.

    Widening to a fixed 7-offset net was the wrong fix: on human it changed 3 of 28 designs by
    up to 0.0123 through spurious alignments, which would have silently moved committed numbers.
    Deriving delta gives mouse exactly the (0,4,-4) it needs -- identical to the wide net on
    every top design -- and leaves human on (0,5,-5), reproducing the committed artifact bit
    for bit. If either construct changes, this follows it; a magic number would not.
    """
    dl = _target_chain_len(designed_pdb, d_bind)
    pl = _target_chain_len(predicted_cif, p_bind)
    if dl is None or pl is None:
        return (0, 5, -5)                  # fall back to the human default rather than guess
    delta = pl - dl
    return (0,) if delta == 0 else (0, delta, -delta)


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
        offs = numbering_offsets(designed[idx], cifs[0], "A", "D")
        r = _scd.sc_dockq(designed[idx], cifs[0], d_bind="A", p_bind="D", offsets=offs)
        if r is None:
            refused.append(did)
            continue
        rows.append(dict(id=did, backbone=idx, ca_sc_dockq=round(r[0], 4),
                         fnat=round(r[1], 4), lrms=round(r[2], 3), irms=round(r[3], 3)))
    return rows, refused


def selftest():
    import tempfile

    # T0 (2026-10-09) the numbering offset must be DERIVED, not fixed. A fixed (0,5,-5) is
    # correct for a 157-residue human prediction against 152-residue designed target chains and
    # WRONG for a 156-residue mouse one, where it cost the best design 0.4944 against 0.6286.
    with tempfile.TemporaryDirectory() as _d:
        def _mk(path, tgt_len, binder_len, tgt_chains="BCD", bind="A"):
            with open(path, "w") as fh:
                i = 0
                for r in range(1, binder_len + 1):
                    i += 1
                    fh.write(f"ATOM  {i:5d}  CA  GLY {bind}{r:4d}    "
                             f"{r*3.8:8.3f}{0.0:8.3f}{0.0:8.3f}\n")
                for c in tgt_chains:
                    for r in range(1, tgt_len + 1):
                        i += 1
                        fh.write(f"ATOM  {i:5d}  CA  GLY {c}{r:4d}    "
                                 f"{r*3.8:8.3f}{20.0:8.3f}{0.0:8.3f}\n")
        _des = os.path.join(_d, "des.pdb"); _mk(_des, 152, 83)
        _hum = os.path.join(_d, "hum.pdb"); _mk(_hum, 157, 83, tgt_chains="ABC", bind="D")
        _mou = os.path.join(_d, "mou.pdb"); _mk(_mou, 156, 83, tgt_chains="ABC", bind="D")
        assert _target_chain_len(_des, "A") == 152
        assert numbering_offsets(_des, _hum, "A", "D") == (0, 5, -5), \
            numbering_offsets(_des, _hum, "A", "D")
        assert numbering_offsets(_des, _mou, "A", "D") == (0, 4, -4), \
            numbering_offsets(_des, _mou, "A", "D")
        # MUTATION: a fixed human set must NOT contain the mouse delta, which is the whole bug
        assert 4 not in (0, 5, -5), "the old fixed set cannot reach the mouse offset"
        # equal lengths need no offset at all
        _eq = os.path.join(_d, "eq.pdb"); _mk(_eq, 152, 83, tgt_chains="ABC", bind="D")
        assert numbering_offsets(_des, _eq, "A", "D") == (0,)
    print("  ok  T0 numbering offsets derived from construct lengths (human 5, mouse 4)")

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

    # T4 continuation rule. RETUNED 2026-10-09 with PATIENCE 2 -> 4 (PREREG s5). The old
    # assertions read "two flat rounds must stop" and correctly FAILED when the constant moved,
    # which is the test doing its job -- they are updated here rather than loosened.
    assert continuation([0.10])[0] == "CONTINUE"
    assert continuation([0.10, 0.25])[0] == "CONTINUE"
    _flat3 = [0.10, 0.25, 0.255, 0.256, 0.257]
    assert continuation(_flat3)[0] == "CONTINUE", \
        f"{PATIENCE - 1} flat rounds must not stop at patience {PATIENCE}"
    _flat4 = [0.10, 0.25, 0.255, 0.256, 0.257, 0.258]
    assert continuation(_flat4)[0] == "STOP", f"{PATIENCE} flat rounds must stop"
    assert continuation([0.1] * MAX_ROUNDS)[0] == "STOP"
    # MUTATION: the rule must count CONSECUTIVE flat rounds, not flat rounds anywhere. A real
    # improvement after a flat patch has to reset the counter, or a loop that is still climbing
    # gets killed by its own history.
    assert continuation([0.10, 0.101, 0.102, 0.103, 0.40])[0] == "CONTINUE", \
        "a genuine improvement must reset the patience counter"
    v, why = continuation(_flat4)
    print(f"  ok  T4 continuation: {PATIENCE - 1} flat rounds continue, {PATIENCE} stop ({why})")

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
    # ---- C4 fence, 2026-10-09: the declared-contaminated 4:1 lineage
    _c = [dict(id="a", ca_sc_dockq=0.60, ipsae_min=0.20, contaminated=True),
          dict(id="b", ca_sc_dockq=0.50, ipsae_min=0.40, contaminated=True)]
    protocol_4to1_blend(_c)
    # T9 the blend must actually weight ipSAE 4 and pose 1, so a worse-posed / better-ipSAE row
    # wins. If it came out 1:4 or 1:1, `a` would win and the head-to-head would test nothing.
    assert select_parent_declared_contaminated(_c, acknowledge=_CONTAM_ACK)["id"] == "b", _c
    assert abs(_c[1][PROTOCOL_BLEND_KEY] - 3.0) < 1e-9, _c[1]
    print("  ok  T9 the 4:1 blend weights ipSAE 4 : pose 1 and picks accordingly")
    # T10 lock 1: no acknowledgement token, no selection
    try:
        select_parent_declared_contaminated(_c, acknowledge="nope")
        raise AssertionError("T10: missing token was not refused")
    except OracleViolation:
        pass
    # T11 lock 2: rows must carry the contamination marking
    try:
        select_parent_declared_contaminated(
            [dict(id="c", ca_sc_dockq=1.0, ipsae_min=1.0, **{PROTOCOL_BLEND_KEY: 9.0})],
            acknowledge=_CONTAM_ACK)
        raise AssertionError("T11: unmarked row was not refused")
    except OracleViolation:
        pass
    # T12 lock 3: a confidence field that is NOT a blend input is still refused
    try:
        select_parent_declared_contaminated(
            [dict(id="d", ca_sc_dockq=1.0, ipsae_min=1.0, plddt=90.0, contaminated=True,
                  **{PROTOCOL_BLEND_KEY: 9.0})],
            acknowledge=_CONTAM_ACK)
        raise AssertionError("T12: undeclared confidence field was not refused")
    except OracleViolation:
        pass
    print("  ok  T10-T12 three locks: token, contamination marking, no undeclared confidence")
    # T13 MUTATION: the clean selector must have NO path that admits the blend inputs. This is
    # the property the whole fence exists to preserve -- six lineages depend on it.
    try:
        select_parent(_c)
        raise AssertionError("T13: select_parent admitted ipsae_min -- the fence leaked")
    except OracleViolation:
        pass
    try:
        select_parent([dict(id="e", ca_sc_dockq=0.5, **{PROTOCOL_BLEND_KEY: 9.0})])
    except OracleViolation:
        raise AssertionError("T13: the blend KEY alone is not a confidence field; "
                             "refusing it would mean the clean path cannot score a "
                             "contaminated row's pose, which is not the intent")
    print("  ok  T13 MUTATION: select_parent still refuses the blend inputs; fence does not leak")

    # ---- C5 + C8, 2026-10-09
    _h = [dict(id="a", ca_sc_dockq=0.60), dict(id="b", ca_sc_dockq=0.30)]
    _m = [dict(id="a", ca_sc_dockq=0.20), dict(id="b", ca_sc_dockq=0.50)]
    _c2 = combine_species({"human": _h, "mouse": _m})
    _by = {r["id"]: r for r in _c2}
    # T14 MUTATION: the WORSE of the two species, not the better. Taking the better would pick
    # design `a` (human 0.60) when its mouse score is 0.20 -- i.e. it would ship a design that
    # does not engage mouse at all, which is exactly what objective 3 forbids.
    assert _by["a"][SELECTOR_KEY] == 0.20, _by["a"]
    assert _by["b"][SELECTOR_KEY] == 0.30, _by["b"]
    assert _by["a"]["worse_species"] == "mouse" and _by["b"]["worse_species"] == "human"
    assert select_parent(_c2)["id"] == "b", "taking the worse must change the parent"
    # and the per-species values survive for audit
    assert _by["a"]["ca_sc_dockq_human"] == 0.60 and _by["a"]["ca_sc_dockq_mouse"] == 0.20
    print("  ok  T14 MUTATION: combine_species takes the WORSE species and changes the parent")
    # T15 the three silent-failure modes must all refuse
    for _label, _arg in (("one species", {"human": _h}),
                         ("design missing from a species", {"human": _h, "mouse": _m[:1]}),
                         ("duplicate id", {"human": _h + _h[:1], "mouse": _m + _m[:1]})):
        try:
            combine_species(_arg)
            raise AssertionError(f"T15: {_label} was not refused")
        except (SystemExit, ValueError):
            pass
    print("  ok  T15 combine_species refuses partial joins, single species and duplicate ids")
    # T16 the ipSAE rule must be a MAX over binder:target pairs and must never see the
    # target trimer's own packing, which runs ~0.86 against a real interface's ~0.31.
    _pairs = {frozenset(("A", "D")): 0.31, frozenset(("B", "D")): 0.29,
              frozenset(("C", "D")): 0.37,
              frozenset(("A", "B")): 0.86, frozenset(("A", "C")): 0.87,
              frozenset(("B", "C")): 0.86}
    _pm = {tuple(sorted(k)): v for k, v in _pairs.items()}
    _vals, _why = _fab.aggregate(_pm, ("A", "B", "C"), ("D",))
    assert _vals is not None, _why
    assert abs(_vals[IPSAE_RULE] - 0.37) < 1e-9, _vals
    assert _vals[IPSAE_RULE] < 0.5, "the rule leaked an intra-target pair"
    assert ipsae_for("/nonexistent/x.cif") is None, "a missing PAE file must give None, not a score"
    print(f"  ok  T16 ipSAE rule {IPSAE_RULE!r} maxes binder:target only, never target packing")
    # T17 the prereg's round cap and patience
    assert MAX_ROUNDS == 16, f"PREREG AMENDMENT 3 fixes 16 rounds, found {MAX_ROUNDS}"
    assert PATIENCE == 4, f"PREREG s5 fixes patience 4, found {PATIENCE}"
    print("  ok  T17 round cap 16 and patience 4 match the pre-registration")

    print("\nself-tests passed: 17")
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
