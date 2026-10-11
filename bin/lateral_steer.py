#!/usr/bin/env python3
"""W2: screened-Coulomb (Debye-Huckel) steering energy of a binder/target interface at two pH.

PREREG: analysis/02-tnf/PREREG-W2-LATERAL-STEERING-2026-10-11.md

This is NOT the binding-coupled protonation gate. There is no PROPKA call, no bound/free
leg and no linkage ratio anywhere in this file. The quantity is the long-range electrostatic
interaction energy between the two sets of titratable side chains that face each other across
the interface, at pH 7.4 and pH 6.0, with Henderson-Hasselbalch occupancies:

    U(pH) = SUM_ij  COUL * q_i(pH) q_j(pH) / (EPS * r_ij) * exp(-r_ij / DEBYE)

    ddG_steer = U(6.0) - U(7.4);  POSITIVE = less favourable at pH 6.0 = RELEASE.

Because U is BILINEAR in the charges, each binder residue's contribution to ddG_steer is
independent of every other binder residue's identity at fixed geometry. That makes the
<=3-mutation search exact rather than greedy-approximate, and it is why this file can report
a per-position per-amino-acid table instead of folding 20^3 variants.
"""
import sys, os, math, argparse, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gemmi
from ph_gate_all import family
from patch_charge_screen import charge, sidechain_centre, MODEL_PKA

COUL = 332.0637      # kcal*A/(mol*e^2)
EPS = 78.5           # bulk water at 310 K
DEBYE = 7.8          # A, 150 mM 1:1 electrolyte
PHS = (7.4, 6.0)
RT = 0.001987204 * 310.15            # kcal/mol
TENFOLD = 2.302585 * RT              # 1.42 kcal/mol = 10x in K_D


def heavy(res):
    return [a for a in res if a.element.name != 'H']


def _ref(res):
    for a in res:
        if a.name == 'CA':
            return a.pos
    return res[0].pos


def min_dist(r1, r2, prefilter=22.0):
    # CA prefilter: no two side chains can touch if their CAs are 22 A apart, and the
    # all-atom loop over a 471-residue trimer is 2.5M distance calls per structure without it.
    if _ref(r1).dist(_ref(r2)) > prefilter:
        return 1e9
    best = 1e9
    for a in heavy(r1):
        for b in heavy(r2):
            d = a.pos.dist(b.pos)
            if d < best:
                best = d
    return best


# Mouse mature TNF-alpha (P06804 Leu80-Leu235, 156-mer) carries a DIFFERENT histidine
# fingerprint from human, so ph_gate_all.family() returns None for it and a mouse complex
# would have both chains classified as binder. It fails closed rather than silently, but the
# mouse leg is half of this objective's worse-of-two selection, so name it here.
MOUSE_TNF = (15, 20, 77)


def is_target(ch):
    if family(ch) is not None:
        return True
    hs = tuple(r.seqid.num for r in ch if r.name == 'HIS')
    return hs == MOUSE_TNF and len(ch) > 120


def titratable(res):
    return res.name in MODEL_PKA


def energy(pairs, qb, qt):
    """pairs: list of (bi, tj, r). qb/qt: dict index -> charge."""
    u = 0.0
    for bi, tj, r in pairs:
        u += COUL * qb[bi] * qt[tj] / (EPS * r) * math.exp(-r / DEBYE)
    return u


def selftest():
    # 1. Two unit charges, 10 A apart, no screening check against hand arithmetic.
    r = 10.0
    want = COUL * 1.0 * 1.0 / (EPS * r) * math.exp(-r / DEBYE)
    assert abs(want - 0.1177) < 0.001, want
    print(f'  ok  unit +/+ pair at 10 A = {want:+.4f} kcal/mol (repulsive, screened)')
    # 2. Sign convention: like charges repel (positive U), unlike attract (negative U).
    pairs = [(0, 0, 10.0)]
    assert energy(pairs, {0: +1.0}, {0: +1.0}) > 0
    assert energy(pairs, {0: +1.0}, {0: -1.0}) < 0
    print('  ok  like charges give U > 0, unlike give U < 0')
    # 3. ddG sign convention. A POSITIVE binder facing a POSITIVE target patch that gains
    #    charge on acidification must give ddG_steer > 0 (release). This is the whole arm.
    qb74, qb60 = {0: +1.0}, {0: +1.0}                    # pH-independent Lys on binder
    qt74, qt60 = {0: charge('HIS', 7.4)}, {0: charge('HIS', 6.0)}
    dd = energy(pairs, qb60, qt60) - energy(pairs, qb74, qt74)
    assert dd > 0, dd
    print(f'  ok  Lys(binder)/His(target) at 10 A: ddG_steer = {dd:+.4f} > 0 = RELEASE')
    # 4. MUTATION: flip the binder to NEGATIVE and the same target His must now TIGHTEN.
    dd_neg = (energy(pairs, {0: -1.0}, qt60) - energy(pairs, {0: -1.0}, qt74))
    assert dd_neg < 0, dd_neg
    assert abs(dd_neg + dd) < 1e-12
    print(f'  ok  MUTATION: Glu(binder)/His(target) ddG_steer = {dd_neg:+.4f} < 0 = TIGHTEN')
    # 5. MUTATION: bilinearity. Doubling one binder charge doubles its contribution exactly.
    a = energy(pairs, {0: +1.0}, qt60); b = energy(pairs, {0: +2.0}, qt60)
    assert abs(b - 2 * a) < 1e-12
    print('  ok  MUTATION: U is exactly bilinear in the charges (the <=3-mut search is exact)')
    # 6. The 10x reference energy.
    assert abs(TENFOLD - 1.4206) < 0.002, TENFOLD
    print(f'  ok  10x in K_D at 310.15 K = {TENFOLD:.4f} kcal/mol')
    # 7. Screening must matter: unscreened is >3x the screened value at 10 A.
    unscr = COUL / (EPS * r)
    assert unscr / want > 3.0
    print(f'  ok  screening is not ignored: unscreened {unscr:+.4f} vs screened {want:+.4f}')
    print('selftest OK')


def analyse(path, contact_cut=4.5, shell_cut=10.0, patch_radius=14.0, verbose=True):
    st = gemmi.read_structure(path)
    st.setup_entities()
    st.remove_hydrogens()
    model = st[0]
    tgt_chains = [c for c in model if is_target(c)]
    bnd_chains = [c for c in model if not is_target(c)]
    if not tgt_chains or len(bnd_chains) != 1:
        return None
    binder = bnd_chains[0]
    tres = [(c.name, r) for c in tgt_chains for r in c]

    # ---- interface definition, geometric only
    bmin = {}
    for r in binder:
        d = min(min_dist(r, tr) for _, tr in tres)
        bmin[r.seqid.num] = d
    iface_contact = [r for r in binder if bmin[r.seqid.num] < contact_cut]
    iface_shell = [r for r in binder if bmin[r.seqid.num] < shell_cut]
    if not iface_contact:
        return None
    # epitope centroid = centroid of target residues in contact with the binder
    epi = [(cn, r) for cn, r in tres if min(min_dist(r, br) for br in binder) < contact_cut]
    pts = [sidechain_centre(r) for _, r in epi]
    pts = [p for p in pts if p]
    cx = sum(p.x for p in pts) / len(pts)
    cy = sum(p.y for p in pts) / len(pts)
    cz = sum(p.z for p in pts) / len(pts)
    centre = gemmi.Position(cx, cy, cz)

    # ---- target patch: titratable target residues within patch_radius of the epitope centroid
    tpatch = []
    for cn, r in tres:
        if not titratable(r):
            continue
        p = sidechain_centre(r)
        if p and p.dist(centre) <= patch_radius:
            tpatch.append((cn, r, p))

    # ---- binder charge carriers: titratable residues in the interface SHELL
    bcarry = [(r, sidechain_centre(r)) for r in iface_shell if titratable(r)]
    bcarry = [(r, p) for r, p in bcarry if p]

    pairs = []
    for i, (br, bp) in enumerate(bcarry):
        for j, (cn, tr, tp) in enumerate(tpatch):
            pairs.append((i, j, max(bp.dist(tp), 2.5)))

    q = {}
    for ph in PHS:
        q[ph] = ({i: charge(br.name, ph) for i, (br, _) in enumerate(bcarry)},
                 {j: charge(tr.name, ph) for j, (_, tr, _) in enumerate(tpatch)})
    u74 = energy(pairs, *q[7.4])
    u60 = energy(pairs, *q[6.0])

    qb = {ph: sum(charge(br.name, ph) for br, _ in bcarry) for ph in PHS}
    qt = {ph: sum(charge(tr.name, ph) for _, tr, _ in tpatch) for ph in PHS}
    nhis_t = sum(1 for _, tr, _ in tpatch if tr.name == 'HIS')
    nhis_b = sum(1 for br, _ in bcarry if br.name == 'HIS')

    # ---- per-position, per-identity ddG_steer, exact by bilinearity
    muts = []
    for i, (br, bp) in enumerate(bcarry + [(r, sidechain_centre(r)) for r in iface_shell
                                           if not titratable(r) and sidechain_centre(r)]):
        pass
    cand = [(r, sidechain_centre(r)) for r in iface_shell if sidechain_centre(r)]
    for br, bp in cand:
        rp = [(0, j, max(bp.dist(tp), 2.5)) for j, (_, _, tp) in enumerate(tpatch)]
        base_dd = (energy(rp, {0: charge(br.name, 6.0)}, q[6.0][1])
                   - energy(rp, {0: charge(br.name, 7.4)}, q[7.4][1]))
        base_u74 = energy(rp, {0: charge(br.name, 7.4)}, q[7.4][1])
        for aa in ('LYS', 'ARG', 'HIS', 'GLN', 'GLU', 'ASP'):
            if aa == br.name:
                continue
            dd = (energy(rp, {0: charge(aa, 6.0)}, q[6.0][1])
                  - energy(rp, {0: charge(aa, 7.4)}, q[7.4][1]))
            new_u74 = energy(rp, {0: charge(aa, 7.4)}, q[7.4][1])
            muts.append(dict(pos=br.seqid.num, wt=br.name, mut=aa,
                             d_ddG=dd - base_dd, d_u74=new_u74 - base_u74,
                             mindist=bmin[br.seqid.num]))
    return dict(path=path, name=os.path.basename(path),
                n_iface_contact=len(iface_contact), n_iface_shell=len(iface_shell),
                n_bcarry=len(bcarry), n_tpatch=len(tpatch),
                nhis_t=nhis_t, nhis_b=nhis_b,
                qb74=qb[7.4], qb60=qb[6.0], qt74=qt[7.4], qt60=qt[6.0],
                u74=u74, u60=u60, ddG=u60 - u74, muts=muts,
                epitope=[f"{cn}{r.seqid.num}{gemmi.find_tabulated_residue(r.name).one_letter_code.upper()}"
                         for cn, r in epi])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('paths', nargs='*')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--muts', action='store_true', help='print the top rim mutations')
    ap.add_argument('--json', default=None)
    a = ap.parse_args()
    if a.selftest:
        selftest(); return
    rows = []
    print(f"{'design':52s} {'nHisT':>5s} {'nHisB':>5s} {'qB7.4':>7s} {'qB6.0':>7s} "
          f"{'qT7.4':>7s} {'qT6.0':>7s} {'U7.4':>7s} {'U6.0':>7s} {'ddG':>7s}")
    for p in a.paths:
        r = analyse(p)
        if r is None:
            print(f"{os.path.basename(p):52s}  SKIP (chain layout)"); continue
        rows.append(r)
        print(f"{r['name'][:52]:52s} {r['nhis_t']:5d} {r['nhis_b']:5d} "
              f"{r['qb74']:+7.2f} {r['qb60']:+7.2f} {r['qt74']:+7.2f} {r['qt60']:+7.2f} "
              f"{r['u74']:+7.3f} {r['u60']:+7.3f} {r['ddG']:+7.3f}")
    if rows:
        dd = [r['ddG'] for r in rows]
        print(f"\nddG_steer kcal/mol: min {min(dd):+.3f}  max {max(dd):+.3f}  "
              f"median {sorted(dd)[len(dd)//2]:+.3f}")
        print(f"BAR W2-1: need ddG_steer >= +{TENFOLD:.3f} (10x K_D at 310 K) -> "
              f"{'PASS' if max(dd) >= TENFOLD else 'FAIL'}")
        print(f"BAR W2-2: at least one design with ddG_steer > 0 -> "
              f"{'PASS' if max(dd) > 0 else 'FAIL'} ({sum(1 for x in dd if x > 0)}/{len(dd)})")
    if a.muts:
        for r in rows:
            ok = [m for m in r['muts'] if m['mindist'] >= 4.5 and m['d_u74'] <= 0.25]
            ok.sort(key=lambda m: -m['d_ddG'])
            best3, used = [], set()
            for m in ok:
                if m['pos'] in used:
                    continue
                best3.append(m); used.add(m['pos'])
                if len(best3) == 3:
                    break
            tot = sum(m['d_ddG'] for m in best3)
            print(f"\n{r['name'][:60]}  as built ddG {r['ddG']:+.3f}")
            for m in best3:
                print(f"    {m['wt']}{m['pos']}{m['mut']:>4s}  d_ddG {m['d_ddG']:+.4f}  "
                      f"dU(7.4) {m['d_u74']:+.4f}  min-dist {m['mindist']:.1f} A")
            print(f"    best pose-sparing triple: {tot:+.4f}  -> engineered ddG "
                  f"{r['ddG'] + tot:+.4f}  (bar +{TENFOLD:.3f}, "
                  f"short by {TENFOLD / max(r['ddG'] + tot, 1e-9):.1f}x)")
    if a.json:
        json.dump(rows, open(a.json, 'w'), indent=1, default=str)


if __name__ == '__main__':
    main()
