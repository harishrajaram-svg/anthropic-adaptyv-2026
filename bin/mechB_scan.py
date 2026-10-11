"""Mechanism B, geometric: does a PARTNER cation sit against a TARGET histidine?

At pH 6.0 a target His protonates. If a partner Lys/Arg cation is its nearest charged
neighbour, protonation gives like-charge repulsion -> RELEASE, and nothing titratable is
required in the binder at all. If a partner carboxylate is nearest, protonation attracts
-> TIGHTENS (problem 1's error).

Fixed before any result is read:
  ring N = HIS ND1, NE2
  cation = LYS NZ, ARG NE/NH1/NH2      acid = ASP OD1/OD2, GLU OE1/OE2
  RELEASE  : d_cat <= 6.0 and d_cat < d_acid
  TIGHTEN  : d_acid <= 6.0 and d_acid <= d_cat
Cross-chain only. This is geometry, NOT a pKa calculation and NOT a pH measurement.
"""
import math, sys
import gemmi

CUT = 6.0
RING = {"ND1", "NE2"}
CAT = {("LYS","NZ"),("ARG","NE"),("ARG","NH1"),("ARG","NH2")}
ACD = {("ASP","OD1"),("ASP","OD2"),("GLU","OE1"),("GLU","OE2")}

def load(path):
    st = gemmi.read_structure(str(path))
    st.setup_entities()
    st.remove_alternative_conformations(); st.remove_hydrogens()
    return st

def scan(path, target_len=None):
    """Returns (verdict, rows). target_len: if given, only His in chains of that residue
    count count as target histidines (our designs: 157). Otherwise 140-180 (TNF-like)."""
    st = load(path)
    model = st[0]
    lens = {ch.name: len([r for r in ch if gemmi.find_tabulated_residue(r.name) and gemmi.find_tabulated_residue(r.name).is_amino_acid()]) for ch in model}
    def is_target(cn):
        n = lens[cn]
        return n == target_len if target_len else (140 <= n <= 180)
    his, cats, acds = [], [], []
    for ch in model:
        for r in ch:
            for a in r:
                key = (r.name, a.name)
                if r.name == "HIS" and a.name in RING and is_target(ch.name):
                    his.append((ch.name, r.seqid.num, a.pos))
                if not is_target(ch.name):
                    if key in CAT: cats.append((ch.name, r.seqid.num, r.name, a.pos))
                    if key in ACD: acds.append((ch.name, r.seqid.num, r.name, a.pos))
    rows = []
    for hc, hn, hp in his:
        dc = min(((hp.dist(p), f"{rn}{num}", c) for c, num, rn, p in cats
                  if c != hc), default=(999, "-", "-"))
        da = min(((hp.dist(p), f"{rn}{num}", c) for c, num, rn, p in acds
                  if c != hc), default=(999, "-", "-"))
        if min(dc[0], da[0]) > CUT: continue
        call = "RELEASE" if (dc[0] <= CUT and dc[0] < da[0]) else "tighten"
        rows.append((f"{hc}:HIS{hn}", dc[0], dc[1], da[0], da[1], call))
    verdict = "RELEASE" if any(r[5] == "RELEASE" for r in rows) else (
              "tighten" if rows else "no-contact")
    return verdict, rows, lens

if __name__ == "__main__":
    tl = int(sys.argv[1]) if sys.argv[1].isdigit() else None
    for p in sys.argv[2:]:
        try:
            v, rows, lens = scan(p, tl)
        except Exception as e:
            print(f"{p}: ERROR {e}"); continue
        print(f"\n{p}  chains={lens}  VERDICT={v}")
        for r in rows:
            print(f"   {r[0]:14} d_cat {r[1]:6.2f} ({r[2]:>6}) "
                  f"d_acid {r[3]:6.2f} ({r[4]:>6})  {r[5]}")
