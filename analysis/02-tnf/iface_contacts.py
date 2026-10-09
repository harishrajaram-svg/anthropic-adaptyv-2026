"""Interface contact census for TNF-alpha co-folds, computed not recalled.

DEFINITION (ours, stated because the organisers' own n_interface_contacts
definition is not published):
  residue_pairs = count of (binder residue, target residue) pairs with ANY
                  heavy-atom pair within CUT angstroms.
  atom_pairs    = count of heavy-atom pairs within CUT angstroms.
Hydrogens, waters and ligands excluded. CUT = 4.5 A, matching contacts.py.

The campaign table's 67-vs-47 split is NOT a yardstick for these numbers --
different predictors, possibly a different definition. The licensed comparison
is AUC against the measured labels through OUR OWN configuration.

CHAIN LAYOUT GUARD: refuses unless exactly 3 chains match human TNF-alpha at
>=0.90 identity and exactly 1 chain remains. A co-fold whose target failed to
assemble, or whose chains were relabelled by the wrapper, is REFUSED, not scored.
"""
import os, sys, glob, json
import gemmi

HUMAN = ("VRSSSRTPSDKPVAHVVANPQAEGQLQWLNRRANALLANGVELRDNQLVVPSEGLYLIYSQVLFKGQGCPSTHVLL"
         "THTISRIAVSYQTKVNLLSAIKSPCQRETPEGAEAKPWYEPIYLGGVFQLEKGDRLSAEINRPDYLDFAESGQVYFGIIAL")
CUT = 4.5

def _seq(ch):
    out = []
    for r in ch:
        t = gemmi.find_tabulated_residue(r.name)
        if t and t.is_amino_acid():
            out.append(t.one_letter_code.upper())
    return "".join(out)

def _is_tnf(seq, thresh=0.90):
    if len(seq) < 40:
        return False
    n = min(len(seq), len(HUMAN))
    ident = sum(a == b for a, b in zip(seq[:n], HUMAN[:n])) / n
    return ident >= thresh

def _heavy(res):
    return [a for a in res if a.element != gemmi.Element('H')]

def census(path, cut=CUT):
    """Returns a dict, or raises ValueError naming the reason for refusal."""
    st = gemmi.read_structure(path)
    st.setup_entities()
    st.remove_ligands_and_waters()
    st.remove_hydrogens()
    model = st[0]
    tnf, binder = [], []
    for ch in model:
        s = _seq(ch)
        if not s:
            continue
        (tnf if _is_tnf(s) else binder).append(ch)
    if len(tnf) != 3 or len(binder) != 1:
        raise ValueError(f"REFUSED chain layout: {len(tnf)} TNF chain(s), "
                         f"{len(binder)} other chain(s); expected 3 + 1")
    b = binder[0]
    res_pairs = 0
    atom_pairs = 0
    b_iface, t_iface = set(), set()
    per_protomer = {}
    for tch in tnf:
        n_here = 0
        for br in b:
            for tr in tch:
                hit = False
                for ba in _heavy(br):
                    for ta in _heavy(tr):
                        if ba.pos.dist(ta.pos) <= cut:
                            atom_pairs += 1
                            hit = True
                if hit:
                    res_pairs += 1
                    n_here += 1
                    b_iface.add(br.seqid.num)
                    t_iface.add((tch.name, tr.seqid.num))
        per_protomer[tch.name] = n_here
    return {
        "residue_pairs": res_pairs,
        "atom_pairs": atom_pairs,
        "binder_res_in_iface": len(b_iface),
        "target_res_in_iface": len(t_iface),
        "binder_len": len(_seq(b)),
        "protomers_contacted": sum(1 for v in per_protomer.values() if v > 0),
        "per_protomer": per_protomer,
    }

# ---------------------------------------------------------------- selftest
def _synth(dx):
    """Two-residue toy: 3 TNF chains (real seq) + a binder placed dx away."""
    st = gemmi.Structure()
    st.add_model(gemmi.Model("1"))
    m = st[0]
    for name in ("A", "B", "C"):
        ch = gemmi.Chain(name)
        for i, aa in enumerate(HUMAN[:45]):
            info = gemmi.find_tabulated_residue(gemmi.find_tabulated_residue('ALA').name)
            r = gemmi.Residue()
            r.name = {'V':'VAL','R':'ARG','S':'SER','T':'THR','P':'PRO','D':'ASP',
                      'K':'LYS','A':'ALA','H':'HIS','N':'ASN','Q':'GLN','E':'GLU',
                      'G':'GLY','L':'LEU','W':'TRP','C':'CYS','Y':'TYR','F':'PHE',
                      'I':'ILE','M':'MET'}[aa]
            r.seqid = gemmi.SeqId(i + 1, ' ')
            a = gemmi.Atom(); a.name = "CA"; a.element = gemmi.Element("C")
            a.pos = gemmi.Position(i * 3.8, 0, 0)
            r.add_atom(a)
            ch.add_residue(r)
        m.add_chain(ch)
    ch = gemmi.Chain("D")
    for i in range(50):
        r = gemmi.Residue(); r.name = "GLY"; r.seqid = gemmi.SeqId(i + 1, ' ')
        a = gemmi.Atom(); a.name = "CA"; a.element = gemmi.Element("C")
        a.pos = gemmi.Position(i * 3.8, dx, 0)
        r.add_atom(a)
        ch.add_residue(r)
    m.add_chain(ch)
    st.setup_entities()
    return st

def _count(st, cut=CUT):
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".cif", delete=False) as fh:
        p = fh.name
    st.make_mmcif_document().write_file(p)
    try:
        return census(p, cut)
    finally:
        os.unlink(p)

def selftest():
    ok = True
    # T1: binder 3.0 A away -> every binder residue contacts >=1 target residue,
    #     and it contacts all three protomers (they are superposed in the toy).
    r = _count(_synth(3.0))
    t1 = r["residue_pairs"] > 0 and r["protomers_contacted"] == 3
    print(f"T1 near (3.0 A): residue_pairs={r['residue_pairs']} "
          f"protomers={r['protomers_contacted']} -> {'PASS' if t1 else 'FAIL'}")
    ok &= t1
    # T2: binder 40 A away -> zero contacts
    r2 = _count(_synth(40.0))
    t2 = r2["residue_pairs"] == 0 and r2["atom_pairs"] == 0
    print(f"T2 far (40 A): residue_pairs={r2['residue_pairs']} -> {'PASS' if t2 else 'FAIL'}")
    ok &= t2
    # T3: monotonic in cutoff
    a = _count(_synth(5.0), cut=4.5)["residue_pairs"]
    b = _count(_synth(5.0), cut=6.0)["residue_pairs"]
    t3 = b >= a
    print(f"T3 monotonic in cut: 4.5A={a} 6.0A={b} -> {'PASS' if t3 else 'FAIL'}")
    ok &= t3
    # T4: chain-layout guard refuses a 2-chain structure
    st = _synth(3.0)
    del st[0]["B"], st[0]["C"]
    try:
        _count(st); t4 = False
    except ValueError as e:
        t4 = "REFUSED chain layout" in str(e)
    print(f"T4 guard refuses 1+1 layout -> {'PASS' if t4 else 'FAIL'}")
    ok &= t4
    # T5 MUTATION: a cutoff of 0 must give zero contacts. Fails if the
    #     distance comparison is ever inverted to >=.
    r5 = _count(_synth(3.0), cut=0.0)
    t5 = r5["residue_pairs"] == 0
    print(f"T5 mutation (cut=0 -> 0 contacts): {r5['residue_pairs']} -> {'PASS' if t5 else 'FAIL'}")
    ok &= t5
    print("SELFTEST", "PASS" if ok else "FAIL")
    return ok

if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    rows = []
    for pat in sys.argv[1:]:
        for f in sorted(glob.glob(pat)):
            name = os.path.basename(os.path.dirname(f))
            try:
                c = census(f)
                c["id"] = name
                rows.append(c)
            except ValueError as e:
                print(f"{name}\tREFUSED\t{e}", file=sys.stderr)
    cols = ["id", "residue_pairs", "atom_pairs", "binder_res_in_iface",
            "target_res_in_iface", "binder_len", "protomers_contacted"]
    print("\t".join(cols))
    for r in rows:
        print("\t".join(str(r[c]) for c in cols))
