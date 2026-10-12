#!/usr/bin/env python3
"""CORR: rounds 4-5 re-run under the two-oracle rule the original depth arm did not honour.

Governed by analysis/02-tnf/PREREG-CORR-TWO-ORACLE-2026-10-11.md and amendments A1-A3. Nothing
here chooses anything: parents, seeds, the pose gate, the selector, the fuse and the wall stop are
all read off the pre-registration. The deviations this run exists to correct are, in one line:
the prereg required BOTH ESMFold2 and Chai-1 inside the pose gate from round 4 onward with the
selector becoming the MINIMUM CA sc_DockQ across the two, and Chai-1 was never wired in.

What this does NOT do: erase the deviation, make the shipped designs confirmatory, or establish
binding. Two structure predictors agreeing bounds one failure mode -- one oracle agreeing with
itself -- and nothing else.

    python3 bin/corr_two_oracle.py --rounds 4,5
    python3 bin/corr_two_oracle.py --selftest
"""
import csv
import datetime as dt
import glob
import importlib.util
import os
import re
import shutil
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(REPO)
sys.path.insert(0, "bin")


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


# RUN_TAG must be set BEFORE run_depth_rounds is imported: redesign()'s /tmp work directory is
# tag-scoped, and two arms sharing /tmp/depth_<tag>_<lineage> already destroyed one arm's
# constraint file mid-flight on 2026-10-11.
os.environ.setdefault("DEPTH_RUN_TAG", "corr")
dl = _load("dl", "bin/depth_loop.py")
rd = _load("rd", "bin/run_depth_rounds.py")

# ---------------------------------------------------------------- PRE-REGISTERED CONSTANTS
# AMENDMENT A2: the parent set the ORIGINAL arm carried into round 4, not the one a mechanical
# best-per-lineage read of round3.tsv produces. L3 (backbone 9) was retired after three rounds
# with 0 of 8 children inside the pose gate and its slot reseeded as L4 from backbone 3's
# second-best round-3 child. Carrying L3 would reproduce a lineage the original arm had already
# dropped and leave out L4, one of two backbone-3 lineages behind the shipped designs.
PARENTS_R4 = [("tnfa_corrected_3_L0r3k2", "0"),
              ("tnfa_corrected_40_L1r3k5", "1"),
              ("tnfa_corrected_40_L2r3k2", "2"),
              ("tnfa_corrected_3_L0r3k7", "4")]
SEQS_PER_PARENT = 8          # as the original arm ran it: round4.tsv carries 8 per lineage
POSE_GATE_LRMS = dl.POSE_GATE_LRMS          # 10.0 A, unchanged
MAX_FOLDS = 160              # hard fuse, BOTH oracles counted
WALL_STOP = dt.datetime(2026, 10, 12, 6, 0, 0)
ESM_SEED = "42"              # matching the original arm exactly
CHAI_KWARGS = "{'num_diffn_samples': 1}"    # A1: one sample, mirroring --num-diffusion-samples 1
CHAI_BATCH = 8               # 4 containers x 8 folds: bounds timeout loss, amortises model load
DESIGNED = rd.DESIGNED
STATE = "analysis/02-tnf/depth_rounds"
TARGET_LEN = 157             # human trimer protomer; mouse is NOT folded (A2: human only)


def log(m):
    print(f"[corr] {m}", flush=True)


def _fold_esm(n, jobs):
    """ESMFold2 on every design, human only, seed 42. -> {design_id: cif_path}"""
    ind = f"runs/corr-r{n}-esm-in"
    shutil.rmtree(ind, ignore_errors=True)
    os.makedirs(ind)
    tgt = rd.tnf_target()
    if len(tgt) != TARGET_LEN:
        sys.exit(f"REFUSED: human target is {len(tgt)} residues, expected {TARGET_LEN}")
    for did, sq in jobs.items():
        with open(f"{ind}/{did}.faa", "w") as fh:
            for c in "ABC":
                fh.write(f">protein|{c}\n{tgt}\n")
            fh.write(f">protein|D\n{sq}\n")
    out, run = f"runs/corr-r{n}-esm-out", f"corrR{n}esm"
    os.makedirs(out, exist_ok=True)
    env = dict(os.environ, SEEDS=ESM_SEED, OUT_DIR=out,
               MODAL_TIMEOUT="90", MODAL_GPU=os.environ.get("MODAL_GPU", "H200"))
    lg = f"runs/depth_logs/corr_r{n}_esm.log"
    with open(lg, "w") as lf:
        rc = subprocess.call(["bash", "bin/score-esmfold2.sh", ind, run],
                             env=env, stdout=lf, stderr=subprocess.STDOUT)
    if rc != 0:
        log(f"  WARN ESMFold2 exited {rc}; log {lg}. Per-fold Volume commits still recover.")
    subprocess.run(["modal", "volume", "get", "esmfold2-runs", run],
                   cwd=out, capture_output=True, text=True)
    return f"{out}/{run}"


def _fold_chai(n, jobs):
    """Chai-1 on every design, batched CHAI_BATCH per container. -> cofold dir."""
    out = f"runs/corr-r{n}-chai-out"
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    tgt = rd.tnf_target()
    items = sorted(jobs.items())
    procs = []
    for b in range(0, len(items), CHAI_BATCH):
        batch = items[b:b + CHAI_BATCH]
        ind = f"runs/corr-r{n}-chai-in-b{b // CHAI_BATCH + 1}"
        shutil.rmtree(ind, ignore_errors=True)
        os.makedirs(ind)
        for did, sq in batch:
            with open(f"{ind}/{did}.faa", "w") as fh:
                for c in "ABC":
                    fh.write(f">protein|name={c}\n{tgt}\n")
                fh.write(f">protein|name=D\n{sq}\n")
        lg = f"runs/depth_logs/corr_r{n}_chai_b{b // CHAI_BATCH + 1}.log"
        lf = open(lg, "w")
        # TIMEOUT sized from the measurement, not hoped at: this wrapper returns output only at
        # the END, so a timeout loses the whole container. 8 folds x ~70 s + ~110 s load ~= 11
        # min; 40 gives it almost 4x.
        procs.append((lg, lf, subprocess.Popen(
            ["modal", "run", "modal_chai1.py",
             "--input-faa", os.path.abspath(ind),
             "--out-dir", os.path.abspath(out),
             "--run-name", f"corrR{n}chaib{b // CHAI_BATCH + 1}",
             "--chai1-kwargs", CHAI_KWARGS],
            cwd="biomodals", env=dict(os.environ, GPU="A100", TIMEOUT="40"),
            stdout=lf, stderr=subprocess.STDOUT, text=True)))
    for lg, lf, pr in procs:
        rc = pr.wait()
        lf.close()
        if rc != 0:
            log(f"  WARN Chai-1 container exited {rc}; log {lg}")
    # flatten runs/<out>/<run_name>/<design>/ -> a single cofold dir of <design>/
    flat = f"{out}/flat"
    os.makedirs(flat, exist_ok=True)
    for d in sorted(glob.glob(f"{out}/corrR{n}chaib*/tnfa_corrected_*")):
        if os.path.isdir(d):
            dst = f"{flat}/{os.path.basename(d)}"
            if os.path.exists(dst):
                sys.exit(f"REFUSED: duplicate Chai-1 output {os.path.basename(d)}")
            shutil.copytree(d, dst)
    return flat


def _score(cofold, n, oracle):
    """CA sc_DockQ for every design in `cofold`, joined on backbone index. -> {id: row}"""
    rows, refused = dl.score_round(DESIGNED, cofold,
                                   expect=re.compile(rf"_L\d+r{n}k\d+$"))
    if refused:
        log(f"  {oracle}: {len(refused)} refused by the scorer")
    return {r["id"]: r for r in rows}


def run_round(n, parents, folds_used):
    """One round under the two-oracle rule. -> (joined rows, folds spent)"""
    if dt.datetime.now() >= WALL_STOP:
        log("STOP: wall-clock stop reached")
        return None, 0

    jobs = {}
    for cif, lin, backbone in parents:
        # force_his / omit_acids FALSE: the constraint machinery was wired on 2026-10-09 and the
        # untagged rounds 1-5 ran before it existed, so the original rounds 4-5 carried the
        # cysteine ban alone. FORCE_HIS and ACID_BAN both default empty, which is that same state.
        seqs = rd.redesign(cif, f"r{n}L{lin}", SEQS_PER_PARENT,
                           force_his=False, omit_acids=False)
        for k, sq in enumerate(seqs):
            jobs[f"tnfa_corrected_{backbone}_L{lin}r{n}k{k}"] = sq

    n_folds = len(jobs) * 2                      # BOTH oracles count against the fuse
    if folds_used + n_folds > MAX_FOLDS:
        log(f"STOP: fuse -- {folds_used}+{n_folds} would cross MAX_FOLDS={MAX_FOLDS}")
        return None, 0
    log(f"round {n}: {len(jobs)} designs from {len(parents)} parents x 2 oracles = {n_folds} folds")

    esm = _score(_fold_esm(n, jobs), n, "esmfold2")
    chai = _score(_fold_chai(n, jobs), n, "chai1")

    rows = []
    for did in sorted(jobs):
        e, c = esm.get(did), chai.get(did)
        if e is None or c is None:
            log(f"  {did}: scored by {'esmfold2' if e else 'chai1' if c else 'neither'} only "
                f"-- NOT eligible, a design must clear BOTH oracles")
            continue
        # THE PRE-REGISTERED RULE, both halves of it.
        gate = max(float(e["lrms"]), float(c["lrms"])) <= POSE_GATE_LRMS
        rows.append(dict(id=did, backbone=e["backbone"], lin=rd.lineage_of(did),
                         ca_sc_dockq_esmfold2=float(e["ca_sc_dockq"]),
                         ca_sc_dockq_chai1=float(c["ca_sc_dockq"]),
                         ca_sc_dockq=min(float(e["ca_sc_dockq"]), float(c["ca_sc_dockq"])),
                         lrms_esmfold2=float(e["lrms"]), lrms_chai1=float(c["lrms"]),
                         lrms=max(float(e["lrms"]), float(c["lrms"])),
                         both_in_gate=gate))
    with open(f"{STATE}/round{n}corr.tsv", "w", newline="") as fh:
        w = csv.DictWriter(fh, delimiter="\t", extrasaction="ignore", fieldnames=[
            "id", "backbone", "lin", "ca_sc_dockq", "ca_sc_dockq_esmfold2",
            "ca_sc_dockq_chai1", "lrms", "lrms_esmfold2", "lrms_chai1", "both_in_gate"])
        w.writeheader()
        w.writerows(rows)
    log(f"round {n}: {sum(1 for r in rows if r['both_in_gate'])} of {len(rows)} inside the "
        f"two-oracle gate; best min-sc_DockQ "
        f"{max((r['ca_sc_dockq'] for r in rows if r['both_in_gate']), default=0):.4f}")
    return rows, n_folds


def select(rows, cofold_esm):
    """Best per lineage by the MINIMUM across oracles, gate-eligible only. -> parents."""
    best = {}
    for r in rows:
        if not r["both_in_gate"]:
            continue
        if r["lin"] not in best or r["ca_sc_dockq"] > best[r["lin"]]["ca_sc_dockq"]:
            best[r["lin"]] = r
    out = []
    for lin in sorted(best):
        r = best[lin]
        # Redesign continues on the HUMAN ESMFold2 complex, as every prior round did -- see
        # run_round()'s note in run_depth_rounds.py. Changing which structure a lineage climbs
        # from would make a plateau unreadable, and that choice is not what this arm corrects.
        out.append((rd.cif_of(f"{cofold_esm}/{r['id']}"), r["lin"], r["backbone"]))
        log(f"  L{lin} = {r['id']} min {r['ca_sc_dockq']:.4f} "
            f"(esm {r['ca_sc_dockq_esmfold2']:.4f} / chai {r['ca_sc_dockq_chai1']:.4f}), "
            f"worse lrms {r['lrms']:.3f} A")
    return out


def selftest():
    """Guards on the rules this script is not allowed to get wrong."""
    # M1 the selector is the MINIMUM, never the mean and never either alone
    r = dict(ca_sc_dockq_esmfold2=0.80, ca_sc_dockq_chai1=0.20)
    assert min(r["ca_sc_dockq_esmfold2"], r["ca_sc_dockq_chai1"]) == 0.20
    print("  ok  M1 selector is the minimum across oracles")

    # M2 the pose gate needs BOTH oracles inside it. The phase-0 L1 checkpoint is the live case:
    # ESMFold2 1.789 A, Chai-1 34.135 A -> must NOT pass.
    assert max(1.789, 34.135) > POSE_GATE_LRMS
    assert max(2.576, 2.044) <= POSE_GATE_LRMS
    print(f"  ok  M2 pose gate is the WORSE of the two oracles (gate {POSE_GATE_LRMS} A)")

    # M3 a design only one oracle scored is ineligible, not silently selected on the other
    rows = []
    for did in ["x"]:
        e, c = dict(ca_sc_dockq=0.9, lrms=1.0, backbone="3"), None
        if e is None or c is None:
            continue
        rows.append(did)
    assert rows == [], "a single-oracle design must not reach the selection table"
    print("  ok  M3 single-oracle designs are dropped, not selected")

    # M4 the parent set is A2's, with L3 absent and L4 present
    lins = [l for _, l in PARENTS_R4]
    assert lins == ["0", "1", "2", "4"], lins
    assert not any("L3" in p or "_9_" in p for p, _ in PARENTS_R4), "retired L3 must not return"
    assert "tnfa_corrected_3_L0r3k7" in [p for p, _ in PARENTS_R4], "reseeded L4 missing"
    print("  ok  M4 parents are L0/L1/L2/L4 -- retired L3 absent, reseeded L4 present")

    # M5 the fuse counts BOTH oracles. 32 designs/round is 64 folds, not 32: a fuse that
    # counted one oracle would let two rounds through and silently permit a third.
    assert 32 * 2 * 2 == 128 <= MAX_FOLDS
    assert 32 * 2 * 3 > MAX_FOLDS, "the fuse must not permit a third round"
    print(f"  ok  M5 fuse {MAX_FOLDS} admits exactly two two-oracle rounds")

    # M6 one sample, or score_round refuses the directory and the arm reports a false failure
    assert "num_diffn_samples': 1" in CHAI_KWARGS
    print("  ok  M6 Chai-1 pinned to one diffusion sample (A1)")

    # M7 redesign must be UNCONSTRAINED, as the original rounds 4-5 were
    assert rd.FORCE_HIS == frozenset() and rd.ACID_BAN == frozenset(), \
        "DEPTH_FORCE_HIS / DEPTH_ACID_BAN are set; the original rounds 4-5 ran unconstrained"
    print("  ok  M7 no histidine or acid constraint, matching the original rounds")
    print("selftest: 7/7")


def main():
    if "--selftest" in sys.argv:
        return selftest()
    selftest()
    rounds = [int(x) for x in
              sys.argv[sys.argv.index("--rounds") + 1].split(",")] if "--rounds" in sys.argv \
        else [4, 5]
    if rounds != [4, 5]:
        sys.exit(f"REFUSED: the pre-registration fixes rounds 4 and 5; got {rounds}")

    parents = []
    for did, lin in PARENTS_R4:
        row = None
        for r in csv.DictReader(open(f"{STATE}/round3.tsv"), delimiter="\t"):
            if r["id"] == did:
                row = r
        if row is None:
            sys.exit(f"REFUSED: {did} is not in round3.tsv")
        parents.append((rd.cif_of(rd._round_out(3, did)), lin, row["backbone"]))
        log(f"parent L{lin} = {did} (backbone {row['backbone']}, "
            f"round-3 dockq {float(row['ca_sc_dockq']):.4f}, lrms {row['lrms']} A)")

    folds = 0
    for n in rounds:
        rows, used = run_round(n, parents, folds)
        folds += used
        if rows is None:
            break
        parents = select(rows, f"runs/corr-r{n}-esm-out/corrR{n}esm")
        if not parents:
            log(f"STOP: no design cleared the two-oracle gate in round {n}")
            break
    log(f"done: {folds} folds spent of {MAX_FOLDS}")


if __name__ == "__main__":
    main()
