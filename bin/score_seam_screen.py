#!/usr/bin/env python3
"""Score an arm S screen: CA sc_DockQ against each design's own seam backbone, plus H73 reach.

PREREG: analysis/02-tnf/PREREG-ROUTES-123-2026-10-11.md  (bars S1, S2)

Reuses depth_loop's numbering_offsets() and sc_dockq.sc_dockq() unchanged. depth_loop.score_round()
itself cannot be reused because it parses the depth arms' `tnfa_corrected_<idx>_...` id format and
these ids are `tnfa_seam_<tag>_<idx>k<k>`, so the JOIN is reimplemented here -- on the backbone
index parsed from the id, refusing a missing or duplicated backbone rather than scoring the wrong
pair, which is the discipline score_round() exists to enforce.
"""
import sys, os, re, glob, json, argparse, importlib.util, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
_spec = importlib.util.spec_from_file_location("_dl", os.path.join(HERE, "depth_loop.py"))
_dl = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_dl)
_spec2 = importlib.util.spec_from_file_location("_scd", os.path.join(HERE, "sc_dockq.py"))
_scd = importlib.util.module_from_spec(_spec2); _spec2.loader.exec_module(_scd)
from seam_contact_check import analyse

ID = re.compile(r"^tnfa_seam_(?P<tag>[a-z0-9]+)_(?P<idx>\d+)k(?P<k>\d+)$")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--designed", required=True)
    ap.add_argument("--cofold", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--tsv", required=True)
    a = ap.parse_args()

    designed = {}
    for p in sorted(glob.glob(os.path.join(a.designed, "tnfa_corrected_*.pdb"))):
        idx = os.path.basename(p)[len("tnfa_corrected_"):-len(".pdb")]
        if idx in designed:
            raise SystemExit(f"REFUSED: duplicate backbone index {idx}")
        designed[idx] = p
    if not designed:
        raise SystemExit(f"REFUSED: no backbones in {a.designed}")
    # H73 reach per backbone, from the generated backbone (the premise, pre-fold)
    reach = {}
    for idx, p in designed.items():
        r, err = analyse(p, 8.0)
        reach[idx] = None if err else sum(1 for _, d in r if d <= 8.0)

    rows, refused, seen = [], [], set()
    for d in sorted(glob.glob(os.path.join(a.cofold, "*", "tnfa_seam_*"))):
        if not os.path.isdir(d):
            continue
        did = os.path.basename(d)
        m = ID.match(did)
        if not m or m.group("tag") != a.tag:
            continue
        if did in seen:
            raise SystemExit(f"REFUSED: duplicate design dir {did}")
        seen.add(did)
        idx = m.group("idx")
        if idx not in designed:
            raise SystemExit(f"REFUSED: {did} has no backbone tnfa_corrected_{idx}.pdb")
        cifs = sorted(glob.glob(os.path.join(d, "*.cif")))
        if len(cifs) != 1:
            raise SystemExit(f"REFUSED: {did} holds {len(cifs)} cif(s); expected 1")
        offs = _dl.numbering_offsets(designed[idx], cifs[0], "A", "D")
        r = _scd.sc_dockq(designed[idx], cifs[0], d_bind="A", p_bind="D", offsets=offs)
        if r is None:
            refused.append(did); continue
        sc = json.load(open(cifs[0].replace(".cif", "_scores.json")))
        rows.append(dict(id=did, backbone=idx, h73_backbone=reach[idx],
                         ca_sc_dockq=round(r[0], 4), fnat=round(r[1], 4),
                         lrms=round(r[2], 3), irms=round(r[3], 3),
                         plddt=round(sc.get("plddt", float("nan")), 4),
                         cif=cifs[0]))
    if not rows:
        raise SystemExit("REFUSED: no rows scored")
    fields = ["id", "backbone", "h73_backbone", "ca_sc_dockq", "fnat", "lrms", "irms", "plddt", "cif"]
    with open(a.tsv, "w") as fh:
        fh.write("\t".join(fields) + "\n")
        for r in sorted(rows, key=lambda r: -r["ca_sc_dockq"]):
            fh.write("\t".join(str(r[f]) for f in fields) + "\n")
    print(f"scored {len(rows)}, refused {len(refused)} -> {a.tsv}")
    dq = [r["ca_sc_dockq"] for r in rows]
    print(f"ca_sc_dockq: min {min(dq):.4f}  median {st.median(dq):.4f}  max {max(dq):.4f}")
    print(f"S1  any >= 0.60 -> {'PASS' if max(dq) >= 0.60 else 'FAIL'}  "
          f"(n>=0.60: {sum(1 for v in dq if v >= 0.60)}, n>=0.50: {sum(1 for v in dq if v >= 0.50)})")
    print("\nby H73 sites the BACKBONE reached:")
    print(f"  {'H73':>3s} {'n':>4s} {'median':>8s} {'max':>8s} {'n>=0.60':>8s}")
    for k in (0, 1, 2, 3):
        g = [r["ca_sc_dockq"] for r in rows if r["h73_backbone"] == k]
        if g:
            print(f"  {k:3d} {len(g):4d} {st.median(g):8.4f} {max(g):8.4f} "
                  f"{sum(1 for v in g if v >= 0.60):8d}")
    print("\ntop 12:")
    print(f"  {'DockQ':>7s} {'H73bb':>5s} {'lrms':>7s} {'pLDDT':>7s}  id")
    for r in sorted(rows, key=lambda r: -r["ca_sc_dockq"])[:12]:
        print(f"  {r['ca_sc_dockq']:7.4f} {r['h73_backbone']:5d} {r['lrms']:7.3f} "
              f"{r['plddt']:7.4f}  {r['id']}")


if __name__ == "__main__":
    main()
