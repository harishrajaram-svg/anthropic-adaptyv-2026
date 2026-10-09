#!/usr/bin/env python3
"""Per-lineage review of one depth round against the previous one.

Written because the loop was running unattended and nobody could see WHICH lineage was carrying
the improvement. A single headline number per round hides the thing that matters: whether all
four lineages are advancing or one is dragging three dead ones along at 8 folds a round.

    depth_report.py <round-number>
"""
import csv
import os
import re
import statistics as st
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(HERE))
STATE = "analysis/02-tnf/depth_rounds"
GATE = 10.0
LIN = re.compile(r"_L(\d+)r\d+k\d+$")
LIN_OLD = re.compile(r"_r\d+p(\d+)k\d+$")


def lin(i):
    m = LIN.search(i) or LIN_OLD.search(i)
    if not m:
        raise ValueError(f"REFUSED: no lineage in {i!r}")
    return m.group(1)


def load(n):
    p = f"{STATE}/round{n}.tsv"
    if not os.path.exists(p):
        return None
    rx = re.compile(rf"_L\d+r{n}k\d+$") if n > 1 else re.compile(r"_r1p\d+k\d+$")
    return [r for r in csv.DictReader(open(p), delimiter="\t") if rx.search(r["id"])]


def best_per_lineage(rows):
    b = {}
    for r in rows:
        k = lin(r["id"])
        if k not in b or float(r["ca_sc_dockq"]) > float(b[k]["ca_sc_dockq"]):
            b[k] = r
    return b


def main(n):
    cur = load(n)
    if not cur:
        sys.exit(f"REFUSED: round {n} not scored yet")
    prev = load(n - 1)
    bc, bp = best_per_lineage(cur), best_per_lineage(prev) if prev else {}
    dq = [float(r["ca_sc_dockq"]) for r in cur]
    lr = [float(r["lrms"]) for r in cur]
    print(f"ROUND {n} — {len(cur)} designs scored, {sum(1 for x in lr if x <= GATE)} inside "
          f"the {GATE} A gate")
    print(f"  best CA sc_DockQ {max(dq):.4f}   best ligand RMSD {min(lr):.3f} A   "
          f"median RMSD {st.median(lr):.3f} A")
    if prev:
        pdq = max(float(r["ca_sc_dockq"]) for r in prev)
        plr = min(float(r["lrms"]) for r in prev)
        print(f"  vs round {n-1}: DockQ {pdq:.4f} -> {max(dq):.4f} ({max(dq)-pdq:+.4f}), "
              f"RMSD {plr:.3f} -> {min(lr):.3f} ({min(lr)-plr:+.3f} A)")
    print(f"\n  {'lin':>3} {'backbone':>8} {'best design':32s} {'DockQ':>7} {'ΔDockQ':>8} "
          f"{'RMSD':>8} {'ΔRMSD':>8} {'in gate':>8}  verdict")
    for k in sorted(bc, key=int):
        r = bc[k]
        d, l = float(r["ca_sc_dockq"]), float(r["lrms"])
        sub = [x for x in cur if lin(x["id"]) == k]
        ng = sum(1 for x in sub if float(x["lrms"]) <= GATE)
        if k in bp:
            pd_, pl = float(bp[k]["ca_sc_dockq"]), float(bp[k]["lrms"])
            dd, dl = f"{d-pd_:+8.4f}", f"{l-pl:+8.3f}"
            moved = d - pd_
        else:
            dd, dl, moved = "       —", "       —", None
        if l > GATE:
            verdict = "DEAD — outside the gate"
        elif moved is None:
            verdict = "new"
        elif moved >= 0.01:
            verdict = "advancing"
        elif moved > -0.01:
            verdict = "FLAT"
        else:
            verdict = "regressing"
        print(f"  {k:>3} {r['backbone']:>8} {r['id']:32s} {d:7.4f} {dd} {l:8.3f} {dl} "
              f"{ng:5d}/{len(sub)}  {verdict}")
    live = [k for k in bc if float(bc[k]["lrms"]) <= GATE]
    print(f"\n  lineages inside the gate: {len(live)} of {len(bc)}  "
          f"(backbones {sorted({bc[k]['backbone'] for k in live})})")
    dead = [k for k in bc if k not in live]
    if dead:
        tags = ", ".join("L%s (bb %s)" % (k, bc[k]["backbone"]) for k in sorted(dead, key=int))
        print(f"  lineages outside the gate, still costing 8 folds a round: {tags}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(int(sys.argv[1]))
