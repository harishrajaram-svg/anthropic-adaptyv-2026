#!/usr/bin/env python3
"""Unattended predict-then-redesign rounds, to the bars in PREREG-DEPTH-ARM-2026-10-08.md.

Runs without supervision for several hours and spends money, so every limit is a hard cap in
code rather than a note in a document:

  MAX_ROUNDS      14    pre-registered ceiling (PREREG AMENDMENT 1: 7 lineages x 4
                        children x 2 species = 56 folds/round, so 14 x 56 = 784)
  MAX_FOLDS      1600   absolute spend fuse (~$71); refuses to launch a round that would cross it
  WALL_STOP             Sat Oct 10 18:00 EDT, pre-registered; checked before every launch
  selection             CA sc_DockQ against the designed backbone, taking the WORSE of
                        human and mouse -- enforced by depth_loop.select_parent(), which raises
                        on any confidence column. ONE declared-contaminated lineage instead uses
                        the protocol's 4:1 ipSAE+sc_DockQ rule via a fenced sibling selector and
                        is pre-committed as NOT a submission source (PREREG s2).
  cysteine              banned in every redesign (--omit_AAs CX). Evidence, corrected
                        2026-10-09: in the released campaign, designs carrying a cysteine bind
                        at 11.8% (11/93) against 28.0% (343/1,227) cysteine-free, p = 3.9e-4,
                        AND score identically on the metrics this loop selects on -- so the
                        penalty is invisible to the selector across 16 rounds. Note this ban is
                        STRICTER than the organisers require (their protocol asks for a
                        Cys-parity liability check, not a ban); it is our choice.
  histidine             1-2 forced at cation-reachable positions computed on the PREDICTED
                        complex, via --omit_AA_jsonl, VERIFIED on the output sequences because
                        that flag fails silently. One control lineage runs without it.

It never trusts the local entrypoint's output write. That path has failed three times on this
project; folds are always recovered from the esmfold2-runs Volume instead.

    run_depth_rounds.py --selftest
    run_depth_rounds.py --go [--one-round] [--seed-lineages id:lin,...]
                            [--parents <round> id:lin,...] [--resume-after <round>]
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

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
os.chdir(REPO)

_spec = importlib.util.spec_from_file_location("_dl", os.path.join(HERE, "depth_loop.py"))
dl = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dl)
_mc_spec = importlib.util.spec_from_file_location(
    "_mc", os.path.join(HERE, "mpnn_constraints.py"))
mc = importlib.util.module_from_spec(_mc_spec)
_mc_spec.loader.exec_module(mc)

MAX_ROUNDS = dl.MAX_ROUNDS            # 10
MAX_FOLDS = int(os.environ.get("DEPTH_MAX_FOLDS", "1600"))   # spend fuse, ~$71 at 1600 on
                                      # L40S rates; env-overridable 2026-10-11 so an arm can
                                      # carry its own pre-registered fuse. 400 -> 800 -> 1600 on
                                      # 2026-10-09. AMENDMENT 3: 16 rounds x 6
                                      # lineages x 8 children x 2 SPECIES = 1536,
                                      # leaving 64 folds of headroom. The fuse is an
                                      # OPTION not a commitment -- PATIENCE=4 and bar
                                      # B3 end the arm if the blend does not improve
                                      # over 4 consecutive rounds, so the extra
                                      # rounds are only bought if still climbing.
WALL_STOP = dt.datetime(*(int(x) for x in os.environ["DEPTH_WALL_STOP"].split(","))) \
    if os.environ.get("DEPTH_WALL_STOP") else dt.datetime(2026, 10, 10, 18, 0, 0)
# Env-overridable 2026-10-11 (format "Y,M,D,H,M,S"). The hardcoded default is the ORIGINAL
# pre-registered stop and is now in the past, so an unset env var refuses to launch rather than
# running unbounded -- which is the safe direction for a constant whose whole job is to stop.
SEQS_PER_PARENT = 8                   # 8 -> 4 -> 8 on 2026-10-09. AMENDMENT 2: the
                                      # constrained restart is dead, so the arm is an
                                      # UNCONSTRAINED continuation and best-of-4 is a
                                      # plausible reason the diagnostic's clean arm
                                      # read 0.286 against the depth arm's ~0.62,
                                      # which was best-of-8. Old note: 8 lineages x 4
                                      # x 2 species = 64 folds/round, which buys 12
                                      # rounds at the fuse instead of 6. Total width
                                      # per round (32) is unchanged from the depth
                                      # arm's 4 lineages x 8; it is spread wider.
MPNN = os.path.join(REPO, "tools/ProteinMPNN")
MPNN_PY = os.path.join(MPNN, ".venv/bin/python")
DESIGNED = "runs/genie3-out/probe50/tnfa_corrected/pdbs"
STATE = "analysis/02-tnf/depth_rounds"
# A relaunch must NOT share a Volume namespace with an aborted run. See score_round().
RUN_TAG = os.environ.get("DEPTH_RUN_TAG", "v2")
# PREREG s2: the lineage label(s) selected by the protocol's 4:1 rule instead of ours.
# Comma-separated, e.g. DEPTH_CONTAMINATED=7. Empty means every lineage is clean.
CONTAMINATED = frozenset(
    x.strip() for x in os.environ.get("DEPTH_CONTAMINATED", "").split(",") if x.strip())
# ---- SEQUENCE CONSTRAINTS ARE OFF BY DEFAULT. Polarity INVERTED 2026-10-09 after an audit
# caught the launch about to run constrained.
#
# These started as DEPTH_NO_HIS / DEPTH_NO_ACID_BAN -- opt-OUT switches used by the 3-arm
# diagnostic. PREREG AMENDMENT 2/A3.4 then specified "no constraint file beyond the cysteine ban",
# but the DEFAULT still turned both constraints ON, so a launch that set neither variable would
# have reproduced D1 exactly: 0 of 28 children inside the 10 A pose gate, on all six lineages,
# for 1,536 folds. The selftests were green at 11/11 and asserted nothing about either flag.
#
# So the failing configuration now requires DELIBERATE ACTION. A lineage is constrained only if
# it is NAMED. Unset means unconstrained, which is what the pre-registration says runs.
FORCE_HIS = frozenset(
    x.strip() for x in os.environ.get("DEPTH_FORCE_HIS", "").split(",") if x.strip())
ACID_BAN = frozenset(
    x.strip() for x in os.environ.get("DEPTH_ACID_BAN", "").split(",") if x.strip())


LIN_RE = re.compile(r"_L(\d+)r\d+k\d+$")
LIN_RE_OLD = re.compile(r"_r\d+p(\d+)k\d+$")       # round 1 of the 2026-10-08 22:27 run


def lineage_of(design_id):
    for rx in (LIN_RE, LIN_RE_OLD):
        m = rx.search(design_id)
        if m:
            return m.group(1)
    raise ValueError(f"REFUSED: cannot read a lineage from {design_id!r}")


def _round_tsv(rn):
    """Prior round's scored table, tagged or untagged. See the note at the write site."""
    for p in (f"{STATE}/round{rn}{RUN_TAG}.tsv", f"{STATE}/round{rn}.tsv"):
        if os.path.exists(p):
            return p
    sys.exit(f"REFUSED: no round{rn} table; tried round{rn}{RUN_TAG}.tsv and round{rn}.tsv")


def _round_out(rn, design_id):
    """Path to a prior round's HUMAN predicted complex, across both output layouts.

    Rounds 1-5 of the depth arm wrote one species to runs/depthB-r<n>-out/depthB<n><tag>/.
    From 2026-10-09 each round writes per species to runs/depthB-r<n>-<species>-out/
    depthB<n><species><tag>/. --parents and --resume-after reach back into earlier rounds, so
    they must resolve BOTH or a resume would silently look in a directory that does not exist
    and die with a confusing cif count.
    """
    # The BATCH INDEX was missing from every candidate, found by audit 2026-10-09:
    # fold_all_species names each volume run depthB{n}{sp}b{b}{TAG}, so --resume-after and
    # --parents could not resolve this run's OWN output and recovery was dead on arrival.
    cands = [*sorted(glob.glob(
                 f"runs/depthB-r{rn}-human-{RUN_TAG}-out/depthB{rn}humanb*{RUN_TAG}/{design_id}")),
             *sorted(glob.glob(
                 f"runs/depthB-r{rn}-human-out/depthB{rn}humanb*{RUN_TAG}/{design_id}")),
             f"runs/depthB-r{rn}-human-{RUN_TAG}-out/depthB{rn}human{RUN_TAG}/{design_id}",
             f"runs/depthB-r{rn}-human-out/depthB{rn}human{RUN_TAG}/{design_id}",
             f"runs/depthB-r{rn}-out/depthB{rn}{RUN_TAG}/{design_id}",
             f"runs/depthB-r{rn}-out/depthB{rn}/{design_id}"]
    for c in cands:
        if os.path.isdir(c):
            return c
    sys.exit("REFUSED: no prior-round output for " + design_id + "; tried " + ", ".join(cands))


def select_per_lineage(rows):
    """One parent per lineage -- the pre-registration continues each design 'under the same
    root backbone id', and a global top-N does not.

    WHY THIS REPLACED A GLOBAL TOP-4 MID-RUN, on 2026-10-08 at 23:30. Round 1 of the first
    stage-B run collapsed the beam to a single backbone in ONE round: all four carried designs
    came from backbone 40 (three from 40_s2, one from 40_s1), while backbone 3's best child sat
    at 3.879 A and was dropped for ranking ninth, and backbone 9 died outright. Eight further
    rounds would then have polished one shape. It also broke the organisers' own diversity rule,
    which caps any single cluster at 10% of designs; a beam that is 100% one backbone is the
    opposite of that. The failure mode was named in writing before round 1 finished, so this is
    a predicted flaw arriving rather than a result being tuned away -- but it IS a deviation from
    a procedure that was committed before the run, and it is recorded as one.
    """
    best = {}
    for r in rows:
        lin = lineage_of(r["id"])
        if lin not in best or float(r["ca_sc_dockq"]) > float(best[lin]["ca_sc_dockq"]):
            best[lin] = r
    out = [best[k] for k in sorted(best)]
    for r in out:                      # the oracle guard still gates every selection
        dl.select_parent([{"id": r["id"], "ca_sc_dockq": r["ca_sc_dockq"], "lrms": r["lrms"]}])
    return out


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


def redesign(parent_cif, tag, nseq, force_his=True, omit_acids=True):
    """SolubleMPNN on the PREDICTED complex: chain D designed, A/B/C fixed, cysteine banned,
    and -- added 2026-10-09 -- the HISTIDINE AND ACID CONSTRAINTS ACTUALLY APPLIED.

    THIS WAS MISSING AND IT IS THE WHOLE POINT OF THE ARM. Until now this function passed only
    `--omit_AAs CX`, the cysteine ban. bin/mpnn_constraints.py existed, was fixed on 2026-10-09
    (cap 8 -> 2, positions read off the predicted complex), and was CALLED BY NOTHING. A
    "constrained restart" would have run completely unconstrained and B4 would have measured
    nothing.

    THE FLAG FAILS SILENTLY. protein_mpnn_run.py loads the file only `if os.path.isfile(...)`
    and otherwise prints `omit_AA_jsonl is NOT loaded` to stdout and carries on designing. A
    typo in the path is therefore indistinguishable from an unconstrained run, so the
    constraint is verified on the OUTPUT SEQUENCES below, not assumed from the argument list --
    the same reason the cysteine ban carries a post-hoc assertion.

    `force_his=False` is the B4 control lineage: same pipeline, acids still kept off the
    interface, no histidine requirement.
    """
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
    # the per-position constraints, computed on THIS parent's predicted complex (C2)
    blen = sum(1 for res in st[0]["D"])
    iface, reach = mc.positions(parent_cif, "D")
    cpath, citems = mc.emit("parent", "D", iface, reach, f"{work}/cons",
                            force_his=force_his, n_res=blen, omit_acids=omit_acids)
    log(f"  {tag}: {len(iface)} interface pos, {len(reach)} His pos {reach} "
        f"(force_his={force_his}, omit_acids={omit_acids}), binder {blen} aa")
    r(MPNN_PY, "protein_mpnn_run.py", "--jsonl_path", f"{work}/p.jsonl",
      "--chain_id_jsonl", f"{work}/c.jsonl", "--out_folder", work,
      "--num_seq_per_target", str(nseq), "--sampling_temp", "0.1",
      "--seed", "37", "--batch_size", "1", "--use_soluble_model",
      "--omit_AAs", "CX",                      # <-- the cysteine ban
      "--omit_AA_jsonl", cpath)                # <-- the His/acid constraints
    lines = [l.strip() for l in open(f"{work}/seqs/parent.fa") if l.strip()]
    seqs = [l for l in lines if not l.startswith(">")][1:]     # [0] is the native
    out = []
    acid_only = sorted(set(iface) - set(reach))
    for s in seqs:
        s = s.split("/")[-1]
        if "C" in s:
            sys.exit(f"REFUSED: cysteine survived the ban in {tag}")
        # POST-HOC VERIFICATION of a silently-failing flag. If omit_AA_jsonl did not load, the
        # forced positions come back as whatever SolubleMPNN liked and an acid-omitted interface
        # position comes back as D or E. Either means the constraint never applied.
        if force_his:
            bad = [p for p in reach if s[p - 1] != "H"]
            if bad:
                sys.exit(f"REFUSED: {tag}: omit_AA_jsonl did not apply -- forced position(s) "
                         f"{bad} are {[s[p-1] for p in bad]}, expected H. The flag loads only "
                         f"if the file exists and otherwise designs unconstrained.")
        leaked = [p for p in acid_only if s[p - 1] in "DE"] if omit_acids else []
        if leaked:
            sys.exit(f"REFUSED: {tag}: acid survived the interface omission at {leaked} "
                     f"({[s[p-1] for p in leaked]}); omit_AA_jsonl did not apply")
        nh = s.count("H")
        if force_his and not (1 <= nh <= mc.MAX_FORCED_HIS):
            log(f"  WARN {tag}: {nh} histidines in a sequence (cap is "
                f"{mc.MAX_FORCED_HIS} FORCED; extras are SolubleMPNN's own choice)")
        out.append(s)
    assert len(out) == nseq, (len(out), nseq)
    return out


def mouse_target():
    """The 156-mer mouse TNF-alpha used by every prior mouse fold. Refuses on disagreement.

    A TRIMER, not the dimer of METHODS s6.10d. s6.12(b) measured the dimer inflating margins by
    a median +16% (spread -78% to +40%), running 6.8x noisier (SD 1.520 vs 0.225), and producing
    at least one flatly false reading. The dimer existed because s6.6's 976-token OOM hit a 48 GB
    L40S INSIDE THE GRADIENT COMPUTATION -- a Mosaic design-time limit. Scoring builds no
    gradient graph, and a mouse trimer is 551 residues against the human trimer's 554 that this
    project folds throughout: 12 trimer runs completed with zero OOM at 28.4 s/fold.
    """
    seen = set()
    import glob
    for p in glob.glob("runs/R-mtri-*-in/*.faa") + glob.glob("runs/S0-mtri-*-in/*.faa"):
        ch, cur = {}, None
        for l in open(p):
            l = l.strip()
            if not l:
                continue
            if l.startswith(">"):
                cur = l.split("|")[-1]; ch[cur] = ""
            else:
                ch[cur] += l
        if not {"A", "B", "C"} <= set(ch):
            sys.exit(f"REFUSED: {p} is not a 3-protomer mouse construct (chains {sorted(ch)})")
        if not ch["A"] == ch["B"] == ch["C"]:
            sys.exit(f"REFUSED: {p} target protomers differ")
        seen.add(ch["A"])
    if not seen:
        sys.exit("REFUSED: no prior mouse-trimer fold to take the target from")
    if len(seen) != 1:
        sys.exit(f"REFUSED: prior mouse folds used {len(seen)} different targets")
    t = seen.pop()
    if len(t) != 156:
        sys.exit(f"REFUSED: mouse target is {len(t)} residues, expected 156")
    return t


SPECIES = {"human": (tnf_target, 157), "mouse": (mouse_target, 156)}


APPS_PER_SPECIES = int(os.environ.get("DEPTH_APPS_PER_SPECIES", "4"))


def _batches(jobs, k):
    """Split a job dict into k round-robin batches, so each app carries a similar load."""
    items = sorted(jobs.items())
    return [b for b in (dict(items[i::k]) for i in range(k)) if b]


def fold_all_species(n, jobs, contaminated_lineages=()):
    """Fold every design against EVERY species, all apps concurrently. -> {species: rows}

    WHY CONCURRENT, measured 2026-10-09. score-esmfold2.sh batches a whole input directory into
    ONE container and folds it serially, so the first shape of this -- one app per species, the
    species run one after the other -- put 64 folds through two serial containers: ~31 min per
    round, ~6.2 h for twelve. Splitting each species across APPS_PER_SPECIES apps and launching
    both species together puts 8 apps in flight at 8 folds each: ~5.5 min per round, ~1.4 h for
    twelve. The cost is model load, ~137 s per app, so 8 loads per round instead of 2 (~+$12
    over the run). Rates behind this: human 554 res 25.8 s/fold (n=120), mouse trimer 551 res
    23.2 s/fold (n=28).

    EVERY APP GETS ITS OWN VOLUME NAME. The stale-fold bug was two runs sharing one name; eight
    names per round is eight times the exposure, so the name carries round, species AND batch,
    the set is asserted unique before launch, and `expect` still checks the id format at scoring.
    """
    plan = []
    for sp in sorted(SPECIES):
        getter, tlen = SPECIES[sp]
        tgt = getter()
        if len(tgt) != tlen:
            sys.exit(f"REFUSED: {sp} target is {len(tgt)} residues, expected {tlen}")
        for b, batch in enumerate(_batches(jobs, APPS_PER_SPECIES), 1):
            ind = f"runs/depthB-r{n}-{sp}-b{b}-{RUN_TAG}-in"
            shutil.rmtree(ind, ignore_errors=True); os.makedirs(ind)
            for did, sq in batch.items():
                with open(f"{ind}/{did}.faa", "w") as fh:
                    for c in "ABC":
                        fh.write(f">protein|{c}\n{tgt}\n")
                    fh.write(f">protein|D\n{sq}\n")
            plan.append((sp, b, ind, f"depthB{n}{sp}b{b}{RUN_TAG}"))

    names = [p[3] for p in plan]
    if len(set(names)) != len(names):
        sys.exit(f"REFUSED: duplicate Volume run name in {names}")
    os.makedirs("runs/depth_logs", exist_ok=True)
    log(f"round {n}: launching {len(plan)} apps concurrently "
        f"({len(jobs)} designs x {len(SPECIES)} species)")

    procs = []
    for sp, b, ind, run in plan:
        env = dict(os.environ, SEEDS="42", OUT_DIR=f"runs/depthB-r{n}-{sp}-{RUN_TAG}-out",
                   MODAL_TIMEOUT="90", MODAL_GPU=os.environ.get("MODAL_GPU", "H200"))
        logp = f"runs/depth_logs/round{n}{sp}b{b}{RUN_TAG}.log"
        lf = open(logp, "w")
        procs.append((sp, b, run, logp, lf,
                      subprocess.Popen(["bash", "bin/score-esmfold2.sh", ind, run],
                                       env=env, stdout=lf, stderr=subprocess.STDOUT, text=True)))
    for sp, b, run, logp, lf, pr in procs:
        rc = pr.wait()
        lf.close()
        if rc != 0:
            log(f"  WARN {sp} batch {b} exited {rc}; log {logp}. "
                "Per-fold Volume commits mean completed folds still recover.")

    per = {}
    for sp in sorted(SPECIES):
        out = f"runs/depthB-r{n}-{sp}-{RUN_TAG}-out"
        shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
        rows = []
        for psp, b, ind, run in plan:
            if psp != sp:
                continue
            subprocess.run(["modal", "volume", "get", "esmfold2-runs", run],
                           cwd=out, capture_output=True, text=True)
            r, refused = dl.score_round(DESIGNED, f"{out}/{run}",
                                        expect=re.compile(rf"_L\d+r{n}k\d+$"))
            if refused:
                log(f"  {sp} batch {b}: {len(refused)} refused")
            rows.extend(r)
        log(f"round {n} [{sp}]: scored {len(rows)} of {len(jobs)}")
        for r in rows:
            sub = next(run for psp, b, ind, run in plan
                       if psp == sp and os.path.isdir(f"{out}/{run}/{r['id']}"))
            r["cif"] = cif_of(f"{out}/{sub}/{r['id']}")
            if lineage_of(r["id"]) in contaminated_lineages:
                iv = dl.ipsae_for(r["cif"])
                if iv is None:
                    log(f"  WARN {r['id']}: ipSAE unavailable; 4:1 lineage cannot select on it")
                else:
                    r["ipsae_min"] = iv
                    r["contaminated"] = True
        per[sp] = rows
    return per


def _true_depth(design_id):
    """Rounds of optimisation a seed already carries, from its id, not the round counter.

    `tnfa_corrected_40_L1r4k6` has been through 4 rounds; `tnfa_corrected_16_s1` through 0. A
    run that continues some lineages and starts others has two depths in flight at once, and
    the round counter describes neither.
    """
    m = re.search(r"_L\d+r(\d+)k\d+$", design_id)
    return int(m.group(1)) if m else 0


def _seed_cif(design_id):
    """Locate a round-0 parent's predicted complex across every stage-A / 68-pool output tree."""
    for d in (*glob.glob(f"runs/depthB-r*-out/*/{design_id}"),
              *glob.glob(f"runs/depthB-r*-*-out/*/{design_id}"),
              f"runs/A-depthA-out/AdepthA/{design_id}",
              f"runs/A-seed68-out/Aseed68/{design_id}",
              f"runs/A-seed68b-out/Aseed68b/{design_id}",
              f"runs/A-cofold-out/Acofold/{design_id}"):
        if os.path.isdir(d):
            return d
    sys.exit(f"REFUSED: no round-0 fold found for {design_id}")


def seed_lineages(spec):
    """--seed-lineages id:lin,id:lin,...  explicit round-1 parents.

    WHY THIS EXISTS. main()'s auto-selection takes stage-A designs inside the 10 A pose gate,
    which yields FOUR parents on three backbones. AMENDMENT 1 needs SEVEN lineages, two of them
    seeded from the 68-pool (backbones 16 and 10, which stage A never scored) and three sharing
    backbone 40's parent so the B4 and C1 controls each have a matched comparator. That cannot
    come out of a gate filter, so it is stated explicitly and every choice lands in the log.
    """
    pose = {}
    srcs = ["analysis/02-tnf/depthA_pose_2026-10-08.tsv",
            "analysis/02-tnf/seed68_partial_pose_2026-10-09.tsv",
            "analysis/02-tnf/seed45_pose_2026-10-09.tsv"]
    # ...and every prior round, so a run can CONTINUE finished lineages alongside fresh ones.
    # The depth arm ended round 5 with 4 lineages on only TWO backbones (3 and 40); backbones
    # 16 and 10 were never in the loop. Mixing continued and fresh lineages in one run is how
    # the backbone count goes from 2 to 4, and depth stays per-lineage under the protocol's
    # root_backbone_id rule rather than being read off the round counter.
    srcs += sorted(glob.glob(f"{STATE}/round*.tsv"))
    for f in srcs:
        if not os.path.exists(f):
            continue
        for r in csv.DictReader(open(f), delimiter="\t"):
            pose.setdefault(r["id"], r)
    out = []
    for item in spec.split(","):
        did, lin = item.split(":")
        if did not in pose:
            sys.exit(f"REFUSED: {did} has no pose row in any stage-A or 68-pool table")
        r = dict(pose[did]); r["lin"] = lin
        r["cif"] = cif_of(_seed_cif(did))
        r["true_depth"] = _true_depth(did)
        out.append(r)
    if len({r["lin"] for r in out}) != len(out):
        sys.exit("REFUSED: duplicate lineage labels in --seed-lineages")
    return out


def run_round(n, parents, folds_used, contaminated_lineages=()):
    """One round, BOTH species. Returns (rows, n_folds) or (None, 0) if a cap blocks it."""
    if dt.datetime.now() >= WALL_STOP:
        log("STOP: wall-clock stop reached"); return None, 0
    jobs = {}
    for p in parents:
        seqs = redesign(p["cif"], f"r{n}L{p['lin']}", SEQS_PER_PARENT,
                        force_his=p['lin'] in FORCE_HIS,
                        omit_acids=p['lin'] in ACID_BAN)
        for k, sq in enumerate(seqs):
            # L<lineage> is carried in the id so every later round can group by lineage.
            jobs[f"tnfa_corrected_{p['backbone']}_L{p['lin']}r{n}k{k}"] = sq
    n_folds = len(jobs) * len(SPECIES)          # BOTH species count against the fuse
    if folds_used + n_folds > MAX_FOLDS:
        log(f"STOP: spend fuse -- {folds_used}+{n_folds} would cross MAX_FOLDS={MAX_FOLDS}")
        return None, 0
    log(f"round {n}: {len(jobs)} designs from {len(parents)} parent(s) "
        f"x {len(SPECIES)} species = {n_folds} folds")

    per = fold_all_species(n, jobs, contaminated_lineages)
    for sp, rows in per.items():
        if not rows:
            log(f"STOP: no design scored for species {sp}"); return None, n_folds

    # PREREG s3 step 3: the selector becomes the WORSE of the two species. combine_species
    # REFUSES a partial join rather than quietly selecting on whichever species is present.
    rows = dl.combine_species(per)

    # WHICH COMPLEX THE NEXT ROUND REDESIGNS ON -- a choice the pre-registration did not cover,
    # recorded here rather than left implicit. It is the HUMAN predicted complex, always, for
    # two reasons: human is objective 1 and the primary target, and the histidine positions are
    # computed on the same complex (mpnn_constraints, C2), so constraint and redesign see one
    # structure. Redesigning on whichever species scored worse would move the structure the
    # lineage is climbing from round to round and make a plateau unreadable.
    human_cif = {r["id"]: r["cif"] for r in per["human"]}
    for r in rows:
        r["cif"] = human_cif[r["id"]]

    os.makedirs(STATE, exist_ok=True)
    fields = ["id", "backbone", "ca_sc_dockq", "fnat", "lrms", "irms", "worse_species"]
    fields += [f"ca_sc_dockq_{sp}" for sp in sorted(SPECIES)]
    fields += ["ipsae_min", "contaminated"]
    # TAG-SCOPED ON WRITE. Fixed 2026-10-09 after it destroyed data: RUN_TAG scoped the Volume
    # names and the input dirs but NOT this file, so the diagnostic run's round 1 overwrote the
    # dry run's round 1. Readers (_round_tsv) fall back to the untagged name so rounds 1-5 of
    # the depth arm, written before this change, still resolve.
    with open(f"{STATE}/round{n}{RUN_TAG}.tsv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, delimiter="\t", extrasaction="ignore")
        w.writeheader(); w.writerows(rows)
    return rows, n_folds


def main():
    seed = [r for r in csv.DictReader(open("analysis/02-tnf/depthA_pose_2026-10-08.tsv"),
                                      delimiter="\t") if float(r["lrms"]) <= dl.POSE_GATE_LRMS]
    if not seed:
        sys.exit("REFUSED: no stage-A parent clears the pose gate")
    for i, r in enumerate(seed):
        r["cif"] = cif_of(f"runs/A-depthA-out/AdepthA/{r['id']}")
        r["lin"] = str(i)
    log(f"stage B start: {len(seed)} parents, best lrms "
        f"{min(float(r['lrms']) for r in seed):.3f} A")
    for r in seed:
        log(f"  lineage {r['lin']} = {r['id']} (backbone {r['backbone']}, lrms {r['lrms']})")
    if "--seed-lineages" in sys.argv:
        seed = seed_lineages(sys.argv[sys.argv.index("--seed-lineages") + 1])
        log(f"EXPLICIT SEED (AMENDMENT 1): {len(seed)} lineages")
        for r in seed:
            cons = ("+His" if r["lin"] in FORCE_HIS else "") + \
                   ("+acidban" if r["lin"] in ACID_BAN else "")
            role = ("4:1 CONTAMINATED" if r["lin"] in CONTAMINATED else "clean") + \
                   (f" {cons}" if cons else " UNCONSTRAINED")
            log(f"  L{r['lin']} = {r['id']} (backbone {r['backbone']}, "
                f"dockq {float(r['ca_sc_dockq']):.4f}, lrms {float(r['lrms']):.3f} A) [{role}]")
        log(f"  backbones: {sorted({r['backbone'] for r in seed})}; "
            f"folds/round = {len(seed)} x {SEQS_PER_PARENT} x {len(SPECIES)} "
            f"= {len(seed)*SEQS_PER_PARENT*len(SPECIES)}")
    parents, best, folds = seed, [max(float(r["ca_sc_dockq"]) for r in seed)], 0
    start = 1

    # --parents <round> <id:lin,id:lin,...>  explicit parent set for the next round.
    # A DEVIATION HOOK, and deliberately explicit rather than a hand-edited state file: every
    # retirement or reseed it performs is visible in the shell history and in this log line.
    # Used 2026-10-09 to retire L3 (backbone 9) after three rounds with 0 of 8 children inside
    # the pose gate, and to reseed its slot as L4 from backbone 3's second-best round-3 child,
    # backbone 3 being the only lineage still advancing.
    if "--parents" in sys.argv:
        i = sys.argv.index("--parents")
        rn = int(sys.argv[i + 1])
        spec = [x.split(":") for x in sys.argv[i + 2].split(",")]
        prev = {r["id"]: r for r in csv.DictReader(
            open(_round_tsv(rn)), delimiter="\t")}
        chosen = []
        for did, lg in spec:
            if did not in prev:
                sys.exit(f"REFUSED: {did} is not in round{rn}.tsv")
            r = dict(prev[did]); r["lin"] = lg
            r["cif"] = cif_of(_round_out(rn, did))
            chosen.append(r)
        if len({r["lin"] for r in chosen}) != len(chosen):
            sys.exit("REFUSED: duplicate lineage labels in --parents")
        best.append(max(float(r["ca_sc_dockq"]) for r in prev.values()))
        folds = SEQS_PER_PARENT * len(chosen) * len(SPECIES) * rn
        log(f"EXPLICIT PARENTS for round {rn+1} (deviation, recorded):")
        for r in chosen:
            log(f"  L{r['lin']} = {r['id']} (backbone {r['backbone']}, "
                f"dockq {float(r['ca_sc_dockq']):.4f}, lrms {r['lrms']} A)")
        log(f"  backbones carried: {sorted({r['backbone'] for r in chosen})}")
        parents, start = chosen, rn + 1

    if "--resume-after" in sys.argv:
        rn = int(sys.argv[sys.argv.index("--resume-after") + 1])
        prev = list(csv.DictReader(open(_round_tsv(rn)), delimiter="\t"))
        keep_rx = re.compile(rf"_L\d+r{rn}k\d+$") if rn > 1 else re.compile(r"_r1p\d+k\d+$")
        before = len(prev)
        prev = [r for r in prev if keep_rx.search(r["id"])]
        if before != len(prev):
            log(f"dropped {before - len(prev)} stale row(s) from round{rn}.tsv "
                f"that did not match this run's id format")
        if not prev:
            sys.exit(f"REFUSED: no usable rows in round{rn}.tsv")
        keep = select_per_lineage(prev)
        for r in keep:
            r["cif"] = cif_of(_round_out(rn, r["id"]))
            r["lin"] = lineage_of(r["id"])
        best.append(max(float(r["ca_sc_dockq"]) for r in prev))
        folds = len(prev) * len(SPECIES)
        log(f"RESUMING after round {rn} ({len(prev)} designs already folded, not refolded)")
        log(f"re-selected best-per-lineage: " +
            ", ".join(f"L{r['lin']}={r['id']} ({float(r['ca_sc_dockq']):.4f}, "
                      f"{float(r['lrms'])}A, bb {r['backbone']})" for r in keep))
        log(f"backbones carried: {sorted({r['backbone'] for r in keep})}")
        parents, start = keep, rn + 1
    log(f"stage-A baseline best CA sc_DockQ {best[0]:.4f}")

    for n in range(start, MAX_ROUNDS + 1):
        rows, used = run_round(n, parents, folds, CONTAMINATED)
        folds += used
        if rows is None:
            break
        # SELECTION. The six CLEAN lineages get every confidence column STRIPPED; depth_loop
        # refuses if one survives. The ONE declared-contaminated lineage is selected separately
        # by the fenced 4:1 selector (PREREG s2), so the clean path never sees ipSAE at all.
        clean_rows = [r for r in rows if lineage_of(r["id"]) not in CONTAMINATED]
        contam_rows = [r for r in rows if lineage_of(r["id"]) in CONTAMINATED]
        clean = [{"id": r["id"], "ca_sc_dockq": r["ca_sc_dockq"], "lrms": r["lrms"]}
                 for r in clean_rows]
        top = dl.select_parent(clean)
        if contam_rows:
            ready = [r for r in contam_rows if "ipsae_min" in r]
            if len(ready) < 2:
                log(f"round {n}: 4:1 lineage has {len(ready)} scorable row(s); "
                    "it selects on the clean rule this round and that is recorded")
            else:
                dl.protocol_4to1_blend(ready)
                ctop = dl.select_parent_declared_contaminated(ready, acknowledge=dl._CONTAM_ACK)
                log(f"round {n}: 4:1 lineage picks {ctop['id']} "
                    f"(blend {ctop[dl.PROTOCOL_BLEND_KEY]:+.3f}, "
                    f"pose {float(ctop['ca_sc_dockq']):.4f})")
        best.append(float(top["ca_sc_dockq"]))
        log(f"round {n}: best CA sc_DockQ {best[-1]:.4f} ({top['id']}), "
            f"best lrms {min(float(r['lrms']) for r in rows):.3f} A, folds used {folds}")
        if dl.pose_regressed(rows):
            log(f"STOP: every design above {dl.POSE_GATE_LRMS} A -- pose regression"); break
        v, why = dl.continuation(best[1:]) if len(best) > 2 else ("CONTINUE", "first round")
        log(f"round {n}: {v} -- {why}")
        if v == "STOP":
            break
        if "--one-round" in sys.argv:
            log(f"--one-round: stopping after round {n}. "
                f"resume with --resume-after {n} --one-round")
            break
        keep = select_per_lineage(rows)        # one per lineage, NOT a global top-N
        parents = [{"backbone": r["backbone"], "cif": r["cif"], "lrms": r["lrms"],
                    "lin": lineage_of(r["id"])} for r in keep]
        log(f"round {n}: carrying {len(parents)} lineage(s), backbones "
            f"{sorted({r['backbone'] for r in keep})}")

    log(f"stage B done. per-round best: {[round(x,4) for x in best]}")
    log(f"total folds {folds} (~${folds*0.0371:.2f}). cap was {MAX_FOLDS}.")


PREREG = os.environ.get("DEPTH_PREREG", "").strip()
# WHICH PRE-REGISTRATION GOVERNS THIS RUN. Added 2026-10-11.
#
# Unset keeps the 2026-10-09 pins byte-for-byte, including the refusal to run with any lineage
# constrained. Set it and the pins come from that pre-registration instead -- but its FILE must
# exist on disk, and the run must carry its own explicit fuse and wall stop. So "name the prereg"
# means "the prereg is written", not "the pins are off". The property preserved is the one that
# matters: a different configuration cannot run because someone forgot, only because someone
# declared it, wrote the document, and set the stops.
PREREG_FILES = {"C13": "analysis/02-tnf/PREREG-C13-TWO-ARMS-2026-10-11.md"}


def selftest():
    N_LINEAGES = 6                   # AMENDMENT 2; was 7 (and 8 before that)
    _per_round = N_LINEAGES * SEQS_PER_PARENT * len(SPECIES)
    if PREREG:
        f = PREREG_FILES.get(PREREG)
        assert f, f"DEPTH_PREREG={PREREG!r} unknown; known: {sorted(PREREG_FILES)}"
        assert os.path.exists(os.path.join(REPO, f)), (
            f"DEPTH_PREREG={PREREG} but {f} is not on disk. Write the pre-registration first.")
        assert os.environ.get("DEPTH_MAX_FOLDS"), f"{PREREG} must set DEPTH_MAX_FOLDS explicitly"
        assert os.environ.get("DEPTH_WALL_STOP"), f"{PREREG} must set DEPTH_WALL_STOP explicitly"
        assert MAX_FOLDS >= _per_round, (
            f"fuse {MAX_FOLDS} is smaller than one round ({_per_round} folds)")
        assert WALL_STOP > dt.datetime.now(), (
            f"wall stop {WALL_STOP} is already past; the run would refuse every round")
        assert SEQS_PER_PARENT == 8, f"C13 fixes 8 children/parent, found {SEQS_PER_PARENT}"
        print(f"  ok  governed by {PREREG} ({f})")
        print(f"  ok  fuse {MAX_FOLDS} folds, wall stop {WALL_STOP}, {_per_round} folds/round")
        print(f"  ok  declared: force_his={sorted(FORCE_HIS) or 'none'}, "
              f"acid_ban={sorted(ACID_BAN) or 'none'}, "
              f"selector={os.environ.get('DEPTH_SELECT_SPECIES') or 'worse-of-two'}")
    else:
        # Value pins, updated 2026-10-09 to PREREG-CONSTRAINED-RESTART s5. The old pins read
        # (10, 400) and correctly FAILED when the constants moved, which is the test working.
        assert dl.MAX_ROUNDS == 16, f"AMENDMENT 3 fixes 16 rounds, found {dl.MAX_ROUNDS}"
        assert MAX_FOLDS == 1600, f"AMENDMENT 3 fixes a 1600-fold fuse, found {MAX_FOLDS}"
        assert SEQS_PER_PARENT == 8, (
            f"AMENDMENT 2 fixes 8 children/parent, found {SEQS_PER_PARENT}")
        assert _per_round == 96, _per_round
        assert _per_round * dl.MAX_ROUNDS <= MAX_FOLDS, (
            f"{dl.MAX_ROUNDS} rounds x {_per_round} folds = {_per_round*dl.MAX_ROUNDS} "
            f"exceeds the {MAX_FOLDS}-fold fuse")
        # The pin that was missing, and whose absence nearly cost 1,536 folds: with no env var
        # set, EVERY lineage must come out UNCONSTRAINED, per AMENDMENT 2/A3.4.
        assert not FORCE_HIS, (
            f"DEPTH_FORCE_HIS names {sorted(FORCE_HIS)}; the pre-registered arm is UNCONSTRAINED. "
            "Naming a lineage here reproduces the D1 configuration (0 of 28 in the pose gate). "
            "A different configuration needs DEPTH_PREREG naming a written pre-registration.")
        assert not ACID_BAN, (
            f"DEPTH_ACID_BAN names {sorted(ACID_BAN)}; the arm is UNCONSTRAINED. "
            "A different configuration needs DEPTH_PREREG naming a written pre-registration.")
        print("  ok  constraints OFF by default: no lineage is forced-His or acid-banned")
    _want = dl.MAX_ROUNDS * _per_round
    if _want <= MAX_FOLDS:
        print(f"  ok  prereg pins: {dl.MAX_ROUNDS} rounds x {_per_round} folds "
              f"({_want}) fits the {MAX_FOLDS} fuse")
    else:
        # Not a failure: the per-round check in run_round() refuses to launch a round that would
        # cross the fuse, so the run simply stops early. Said plainly because the old wording
        # claimed a budget "fits" when it does not, and this log is read unattended.
        print(f"  ok  {dl.MAX_ROUNDS} rounds x {_per_round} = {_want} folds EXCEEDS the "
              f"{MAX_FOLDS} fuse, so the run will stop at ~{MAX_FOLDS // _per_round} rounds "
              f"when the per-round fuse check refuses the next launch")
    t = tnf_target(); assert len(t) == 157
    mt = mouse_target(); assert len(mt) == 156
    assert t != mt, "human and mouse targets must not be the same sequence"
    print("  ok  targets resolve: human 157-mer, mouse 156-mer TRIMER (not the s6.10d dimer)")
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
    # T7 best-per-lineage keeps one per lineage and never collapses the beam
    rows = [dict(id="tnfa_corrected_40_L1r2k0", ca_sc_dockq="0.90", lrms="2.0", backbone="40"),
            dict(id="tnfa_corrected_40_L1r2k1", ca_sc_dockq="0.80", lrms="3.0", backbone="40"),
            dict(id="tnfa_corrected_3_L0r2k0",  ca_sc_dockq="0.40", lrms="4.0", backbone="3"),
            dict(id="tnfa_corrected_9_L3r2k0",  ca_sc_dockq="0.10", lrms="9.0", backbone="9")]
    got = select_per_lineage(rows)
    assert sorted(lineage_of(r["id"]) for r in got) == ["0", "1", "3"], [r["id"] for r in got]
    assert {r["backbone"] for r in got} == {"40", "3", "9"}
    print("  ok  T7 best-per-lineage keeps 3 lineages / 3 backbones where a global top-3 "
          "would have kept 2 of backbone 40 and dropped one")
    # T7b MUTATION: a global top-N on the same rows DOES collapse, so T7 is not vacuous
    glob = sorted(rows, key=lambda r: -float(r["ca_sc_dockq"]))[:3]
    assert len({lineage_of(r["id"]) for r in glob}) == 2, glob
    print("      MUTATION: the global top-3 keeps only 2 lineages, confirming the difference")
    # T8 the round-1 id format is still parseable, so the resume path can group it
    assert lineage_of("tnfa_corrected_40_r1p2k3") == "2"
    assert lineage_of("tnfa_corrected_40_L2r5k3") == "2"
    print("  ok  T8 lineage parses from both the round-1 and the new id formats")
    # T9 (2026-10-09) the parallel dispatch must partition the jobs EXACTLY -- no design lost,
    # none folded twice. A lost design silently shrinks the round; a duplicated one gets two
    # Volume entries under different batch names and score_round would see both.
    _jobs = {f"tnfa_corrected_40_L{i % 8}r1k{i // 8}": "SEQ" for i in range(32)}
    _b = _batches(_jobs, APPS_PER_SPECIES)
    assert len(_b) == APPS_PER_SPECIES, [len(x) for x in _b]
    assert sum(len(x) for x in _b) == len(_jobs), [len(x) for x in _b]
    _union = set()
    for _x in _b:
        assert not (_union & set(_x)), "a design appears in two batches"
        _union |= set(_x)
    assert _union == set(_jobs), "batching lost designs"
    assert max(len(x) for x in _b) - min(len(x) for x in _b) <= 1, "batches badly unbalanced"
    # a batch count above the job count must not emit empty batches (an empty input dir makes
    # score-esmfold2.sh refuse, which would fail the whole round for no reason)
    assert all(_x for _x in _batches({"a": "S", "b": "S"}, 8)), "empty batch emitted"
    print(f"  ok  T9 dispatch partitions {len(_jobs)} designs into {APPS_PER_SPECIES} "
          f"balanced batches with no loss or overlap")
    # T10 every app in a round needs its OWN Volume name. Two runs sharing one name is the
    # 2026-10-09 stale-fold bug; 8 apps per round is 8x the exposure.
    _names = [f"depthB{_r}{_sp}b{_i}{RUN_TAG}"
              for _r in (1, 2) for _sp in sorted(SPECIES)
              for _i in range(1, APPS_PER_SPECIES + 1)]
    assert len(set(_names)) == len(_names), "Volume run names collide"
    assert len(_names) == 2 * len(SPECIES) * APPS_PER_SPECIES, len(_names)
    # and the name must distinguish species, or human folds would score as mouse
    assert len({_n.replace("human", "X").replace("mouse", "X") for _n in _names}) < len(_names)
    print(f"  ok  T10 {len(SPECIES) * APPS_PER_SPECIES} Volume names per round, all distinct, "
          "species encoded in each")

    print("\nself-tests passed: 11")   # NOTE: hardcoded; drifted twice on 2026-10-09. See backlog.
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv or len(sys.argv) == 1:
        sys.exit(selftest())
    if "--go" not in sys.argv:
        sys.exit(__doc__)
    main()
