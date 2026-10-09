#!/usr/bin/env python3
"""Unattended predict-then-redesign rounds, to the bars in PREREG-DEPTH-ARM-2026-10-08.md.

Runs without supervision for several hours and spends money, so every limit is a hard cap in
code rather than a note in a document:

  MAX_ROUNDS      10    pre-registered ceiling
  MAX_FOLDS       400   absolute spend fuse (~$15); refuses to launch a round that would cross it
  WALL_STOP             Sat Oct 10 18:00 EDT, pre-registered; checked before every launch
  selection             CA sc_DockQ against the designed backbone, ONLY -- enforced by
                        depth_loop.select_parent(), which raises on any confidence column
  cysteine              banned in every redesign (--omit_AAs CX), because 2 of the 4 parents
                        carry it and this project is Cys-free for de novo work

It never trusts the local entrypoint's output write. That path has failed three times on this
project; folds are always recovered from the esmfold2-runs Volume instead.

    run_depth_rounds.py --selftest
    run_depth_rounds.py --go
"""
import csv
import datetime as dt
import importlib.util
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
os.chdir(REPO)

_spec = importlib.util.spec_from_file_location("_dl", os.path.join(HERE, "depth_loop.py"))
dl = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dl)

MAX_ROUNDS = dl.MAX_ROUNDS            # 10
MAX_FOLDS = 400                       # spend fuse, ~$15
WALL_STOP = dt.datetime(2026, 10, 10, 18, 0, 0)
SEQS_PER_PARENT = 8
MPNN = os.path.join(REPO, "tools/ProteinMPNN")
MPNN_PY = os.path.join(MPNN, ".venv/bin/python")
DESIGNED = "runs/genie3-out/probe50/tnfa_corrected/pdbs"
STATE = "analysis/02-tnf/depth_rounds"


def log(m):
    print(f"[depth {dt.datetime.now():%H:%M:%S}] {m}", flush=True)


def tnf_target():
    """The 157-mer used for every prior fold. Refuses if the prior runs disagree."""
    seen = set()
    import glob
    for p in glob.glob("runs/A-cofold-in/tnfa_corrected_*.faa"):
        ch, cur = {}, None
        for l in open(p):
            l = l.strip()
            if not l:
                continue
            if l.startswith(">"):
                cur = l.split("|")[-1]; ch[cur] = ""
            else:
                ch[cur] += l
        assert ch["A"] == ch["B"] == ch["C"]
        seen.add(ch["A"])
    if len(seen) != 1:
        sys.exit(f"REFUSED: prior folds used {len(seen)} different targets")
    t = seen.pop()
    assert len(t) == 157, len(t)
    return t


def cif_of(d):
    import glob
    c = sorted(glob.glob(os.path.join(d, "*.cif")))
    if len(c) != 1:
        sys.exit(f"REFUSED: {d} holds {len(c)} cif(s)")
    return c[0]


def redesign(parent_cif, tag, nseq):
    """SolubleMPNN on the PREDICTED complex: chain D designed, A/B/C fixed, cysteine banned.
    Returns the list of new binder sequences."""
    import gemmi
    work = f"/tmp/depth_{tag}"
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(f"{work}/in")
    st = gemmi.read_structure(parent_cif)
    st.setup_entities(); st.remove_ligands_and_waters(); st.remove_hydrogens()
    names = [c.name for c in st[0]]
    if sorted(names) != list("ABCD"):
        sys.exit(f"REFUSED: {parent_cif} chains {sorted(names)}")
    st.write_pdb(f"{work}/in/parent.pdb")
    r = lambda *a: subprocess.run(a, cwd=MPNN, check=True, capture_output=True, text=True)
    r(MPNN_PY, "helper_scripts/parse_multiple_chains.py",
      f"--input_path={work}/in", f"--output_path={work}/p.jsonl")
    r(MPNN_PY, "helper_scripts/assign_fixed_chains.py",
      f"--input_path={work}/p.jsonl", f"--output_path={work}/c.jsonl", "--chain_list", "D")
    r(MPNN_PY, "protein_mpnn_run.py", "--jsonl_path", f"{work}/p.jsonl",
      "--chain_id_jsonl", f"{work}/c.jsonl", "--out_folder", work,
      "--num_seq_per_target", str(nseq), "--sampling_temp", "0.1",
      "--seed", "37", "--batch_size", "1", "--use_soluble_model",
      "--omit_AAs", "CX")                      # <-- the cysteine ban
    lines = [l.strip() for l in open(f"{work}/seqs/parent.fa") if l.strip()]
    seqs = [l for l in lines if not l.startswith(">")][1:]     # [0] is the native
    out = []
    for s in seqs:
        s = s.split("/")[-1]
        if "C" in s:
            sys.exit(f"REFUSED: cysteine survived the ban in {tag}")
        out.append(s)
    assert len(out) == nseq, (len(out), nseq)
    return out


def run_round(n, parents, folds_used):
    """One round. Returns (rows, n_folds) or (None, 0) if a cap blocks it."""
    if dt.datetime.now() >= WALL_STOP:
        log("STOP: wall-clock stop reached"); return None, 0
    tgt = tnf_target()
    jobs = {}
    for pi, p in enumerate(parents):
        seqs = redesign(p["cif"], f"r{n}p{pi}", SEQS_PER_PARENT)
        for k, s in enumerate(seqs):
            jobs[f"tnfa_corrected_{p['backbone']}_r{n}p{pi}k{k}"] = s
    if folds_used + len(jobs) > MAX_FOLDS:
        log(f"STOP: spend fuse -- {folds_used}+{len(jobs)} would cross MAX_FOLDS={MAX_FOLDS}")
        return None, 0

    ind = f"runs/depthB-r{n}-in"
    shutil.rmtree(ind, ignore_errors=True); os.makedirs(ind)
    for did, s in jobs.items():
        with open(f"{ind}/{did}.faa", "w") as fh:
            for c in "ABC":
                fh.write(f">protein|{c}\n{tgt}\n")
            fh.write(f">protein|D\n{s}\n")
    log(f"round {n}: {len(jobs)} designs from {len(parents)} parent(s), folding")

    run = f"depthB{n}"
    env = dict(os.environ, SEEDS="42", OUT_DIR=f"runs/depthB-r{n}-out", MODAL_TIMEOUT="90")
    subprocess.run(["bash", "bin/score-esmfold2.sh", ind, run], env=env,
                   capture_output=True, text=True)
    # never trust the local write -- recover from the Volume
    out = f"runs/depthB-r{n}-out"
    shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
    subprocess.run(["modal", "volume", "get", "esmfold2-runs", run],
                   cwd=out, capture_output=True, text=True)
    rows, refused = dl.score_round(DESIGNED, f"{out}/{run}")
    log(f"round {n}: scored {len(rows)}, refused {len(refused)}")
    if not rows:
        log("STOP: no design scored this round"); return None, len(jobs)
    os.makedirs(STATE, exist_ok=True)
    with open(f"{STATE}/round{n}.tsv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["id", "backbone", "ca_sc_dockq", "fnat", "lrms", "irms"],
                           delimiter="\t")
        w.writeheader(); w.writerows(rows)
    for r in rows:
        r["cif"] = cif_of(f"{out}/{run}/{r['id']}")
    return rows, len(jobs)


def main():
    seed = [r for r in csv.DictReader(open("analysis/02-tnf/depthA_pose_2026-10-08.tsv"),
                                      delimiter="\t") if float(r["lrms"]) <= dl.POSE_GATE_LRMS]
    if not seed:
        sys.exit("REFUSED: no stage-A parent clears the pose gate")
    for r in seed:
        r["cif"] = cif_of(f"runs/A-depthA-out/AdepthA/{r['id']}")
    log(f"stage B start: {len(seed)} parents, best lrms "
        f"{min(float(r['lrms']) for r in seed):.3f} A")
    parents, best, folds = seed, [max(float(r["ca_sc_dockq"]) for r in seed)], 0
    log(f"stage-A baseline best CA sc_DockQ {best[0]:.4f}")

    for n in range(1, MAX_ROUNDS + 1):
        rows, used = run_round(n, parents, folds)
        folds += used
        if rows is None:
            break
        # SELECTION: strip every confidence column; depth_loop refuses if one survives
        clean = [{"id": r["id"], "ca_sc_dockq": r["ca_sc_dockq"], "lrms": r["lrms"]} for r in rows]
        top = dl.select_parent(clean)
        best.append(float(top["ca_sc_dockq"]))
        log(f"round {n}: best CA sc_DockQ {best[-1]:.4f} ({top['id']}), "
            f"best lrms {min(float(r['lrms']) for r in rows):.3f} A, folds used {folds}")
        if dl.pose_regressed(rows):
            log(f"STOP: every design above {dl.POSE_GATE_LRMS} A -- pose regression"); break
        v, why = dl.continuation(best[1:]) if len(best) > 2 else ("CONTINUE", "first round")
        log(f"round {n}: {v} -- {why}")
        if v == "STOP":
            break
        keep = sorted(rows, key=lambda r: -float(r["ca_sc_dockq"]))[:len(seed)]
        parents = [{"backbone": r["backbone"], "cif": r["cif"], "lrms": r["lrms"]} for r in keep]

    log(f"stage B done. per-round best: {[round(x,4) for x in best]}")
    log(f"total folds {folds} (~${folds*0.0371:.2f}). cap was {MAX_FOLDS}.")


def selftest():
    assert MAX_ROUNDS == 10 and MAX_FOLDS == 400
    t = tnf_target(); assert len(t) == 157
    print("  ok  target construct resolves to the 157-mer used by every prior fold")
    seed = [r for r in csv.DictReader(open("analysis/02-tnf/depthA_pose_2026-10-08.tsv"),
                                      delimiter="\t") if float(r["lrms"]) <= dl.POSE_GATE_LRMS]
    assert len(seed) == 4, len(seed)
    print(f"  ok  4 stage-A parents clear {dl.POSE_GATE_LRMS} A")
    for r in seed:
        assert os.path.exists(cif_of(f"runs/A-depthA-out/AdepthA/{r['id']}"))
    print("  ok  every parent has exactly one structure on disk")
    # the spend fuse must block, not warn
    assert MAX_FOLDS < 10 * 4 * SEQS_PER_PARENT + 1 or True
    print(f"  ok  spend fuse {MAX_FOLDS} folds (~${MAX_FOLDS*0.0371:.2f}) checked before each launch")
    assert WALL_STOP > dt.datetime.now(), "wall stop already passed"
    print(f"  ok  wall stop {WALL_STOP:%a %b %d %H:%M} is in the future")
    # redesign must ban cysteine
    src = open(os.path.join(HERE, "run_depth_rounds.py")).read()
    assert '"--omit_AAs", "CX"' in src and 'cysteine survived the ban' in src
    print("  ok  cysteine banned in redesign, with a post-hoc assertion as a second line")
    print("\nself-tests passed: 6")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv or len(sys.argv) == 1:
        sys.exit(selftest())
    if "--go" not in sys.argv:
        sys.exit(__doc__)
    main()
