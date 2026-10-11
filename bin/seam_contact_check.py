#!/usr/bin/env python3
"""Did the generator honour seam conditioning? Count H73 sites the binder actually reaches.

PREREG: analysis/02-tnf/PREREG-ROUTES-123-2026-10-11.md  (bar S2's premise)

Run BEFORE spending folds. If a seam-conditioned backbone pool reaches no more H73 sites than a
pool conditioned on something else, the conditioning did nothing and screening it would measure
the generator's default behaviour at $20 a pool.

NUMBERING. Genie 3 writes target protomers 1..152 and the binder as 83 UNK. Mature TNF-alpha
histidines {15, 73, 78} appear at {10, 68, 73}, so mature H73 is PDB residue 68 -- verified by
matching the His TUPLE, not by assuming an offset.
"""
import sys, os, glob, argparse
import gemmi

H73_PDB = 68
HIS_TUPLE = (10, 68, 73)


def analyse(path, cutoff):
    st = gemmi.read_structure(path)
    st.setup_entities(); st.remove_ligands_and_waters(); st.remove_hydrogens()
    m = st[0]
    unk = [c for c in m if {r.name for r in c} == {"UNK"}]
    tgt = [c for c in m if {r.name for r in c} != {"UNK"}]
    if len(unk) != 1 or len(tgt) != 3:
        return None, f"{len(unk)} UNK chain(s), {len(tgt)} target chain(s)"
    for c in tgt:
        if tuple(r.seqid.num for r in c if r.name == "HIS") != HIS_TUPLE:
            return None, f"chain {c.name} His tuple is not {HIS_TUPLE}"
    bat = [a.pos for r in unk[0] for a in r]
    out = []
    for c in tgt:
        res = next((r for r in c if r.seqid.num == H73_PDB), None)
        if res is None or res.name != "HIS":
            return None, f"chain {c.name} has no HIS at {H73_PDB}"
        d = min(a.pos.dist(b) for a in res for b in bat)
        out.append((c.name, d))
    return out, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("globs", nargs="+")
    ap.add_argument("--cutoff", type=float, default=8.0)
    a = ap.parse_args()
    for g in a.globs:
        paths = sorted(glob.glob(g))
        label = g.split("genie3-out/")[-1].split("/")[0] if "genie3-out" in g else g
        hist, refused, dists = {0: 0, 1: 0, 2: 0, 3: 0}, 0, []
        for p in paths:
            r, err = analyse(p, a.cutoff)
            if err:
                refused += 1; continue
            n = sum(1 for _, d in r if d <= a.cutoff)
            hist[n] += 1
            dists.append(sorted(d for _, d in r))
        n = sum(hist.values())
        print(f"\n{label}: {n} backbones scored, {refused} refused, contact cutoff {a.cutoff} A")
        if not n:
            continue
        for k in (0, 1, 2, 3):
            print(f"    {k} H73 reached: {hist[k]:4d}  ({100*hist[k]/n:5.1f}%)")
        print(f"    >=2 H73 reached: {hist[2]+hist[3]:4d}  ({100*(hist[2]+hist[3])/n:5.1f}%)")
        import statistics as st
        print(f"    nearest / 2nd-nearest H73 distance, median: "
              f"{st.median(d[0] for d in dists):.1f} A / {st.median(d[1] for d in dists):.1f} A")


if __name__ == "__main__":
    main()
