#!/usr/bin/env python3
"""Arm E screen: Henderson-Hasselbalch net charge of a target surface patch, at two pH values.

PREREG: analysis/02-tnf/PREREG-ROUTES-123-2026-10-11.md

This is a SCREEN, not a calculation. It uses MODEL pKa values, so it cannot know that a given
carboxylate on this particular surface is shifted -- PROPKA is the tool for that and the gate
already uses it. What this answers is only the sign question route 3 turns on: is the H73 seam
electropositive enough that a binder gaining positive charge at pH 6.0 would be steered OFF it.
An electronegative seam kills route 3 and costs nothing to find out.
"""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gemmi
from ph_gate_all import family

MODEL_PKA = {'ASP': (3.9, -1), 'GLU': (4.3, -1), 'HIS': (6.5, +1), 'CYS': (8.4, -1),
             'TYR': (10.5, -1), 'LYS': (10.5, +1), 'ARG': (12.5, +1)}
RADIUS = 12.0
PHS = (7.4, 6.0)


def charge(resname, ph):
    """Signed charge from Henderson-Hasselbalch.

    THE CONDITIONAL WAS INVERTED when first written (2026-10-11) and the first run of this
    screen reported the seam patch getting MORE NEGATIVE as pH fell, which is impossible: no
    group gains negative charge on acidification. Histidine read +0.240 at pH 6.0 against a
    correct +0.760, and glutamate read -0.001 at pH 7.4 against a correct -1.000, so the screen
    would have returned a confident FAIL for the wrong reason. selftest() pins all four numbers.

        acid, charged when DEprotonated : f = 1 / (1 + 10^(pKa - pH))
        base, charged when protonated   : f = 1 / (1 + 10^(pH - pKa))
    """
    if resname not in MODEL_PKA:
        return 0.0
    pka, sign = MODEL_PKA[resname]
    f = 1.0 / (1.0 + 10 ** ((pka - ph) if sign < 0 else (ph - pka)))
    return sign * f


def selftest():
    cases = [('GLU', 7.4, -1.000), ('GLU', 6.0, -0.981), ('ASP', 7.4, -1.000),
             ('LYS', 7.4, +0.999), ('ARG', 7.4, +1.000),
             ('HIS', 7.4, +0.112), ('HIS', 6.5, +0.500), ('HIS', 6.0, +0.760),
             ('CYS', 7.4, -0.091), ('CYS', 6.0, -0.004), ('ALA', 7.4, 0.0)]
    for rn, ph, want in cases:
        got = charge(rn, ph)
        assert abs(got - want) < 0.002, f'{rn} at pH {ph}: {got:+.4f} want {want:+.4f}'
    print(f'  ok  {len(cases)} model-pKa charges match Henderson-Hasselbalch')
    # MUTATION: acidification can never make any single group more negative
    for rn in MODEL_PKA:
        assert charge(rn, 6.0) >= charge(rn, 7.4) - 1e-9, rn
    print('  ok  MUTATION: no group gains negative charge as pH falls 7.4 -> 6.0')
    # MUTATION: the inverted conditional must be caught by the His and Glu pins
    bad = 1.0 / (1.0 + 10 ** (MODEL_PKA['HIS'][0] - 6.0))
    assert abs(bad - 0.240) < 0.002 and abs(charge('HIS', 6.0) - 0.760) < 0.002
    print('  ok  MUTATION: the original inverted branch (+0.240 for His at pH 6.0) is excluded')
    print('selftest OK')


def sidechain_centre(res):
    ats = [a for a in res if a.name not in ('N', 'CA', 'C', 'O')] or list(res)
    if not ats:
        return None
    x = sum(a.pos.x for a in ats) / len(ats)
    y = sum(a.pos.y for a in ats) / len(ats)
    z = sum(a.pos.z for a in ats) / len(ats)
    return gemmi.Position(x, y, z)


def centre_of(tgt, spec):
    """spec: list of (chain_name, resnum) -> midpoint of their sidechain centres."""
    pts = []
    for cn, num in spec:
        for ch in tgt:
            if ch.name != cn:
                continue
            for r in ch:
                if r.seqid.num == num:
                    p = sidechain_centre(r)
                    if p:
                        pts.append((p, r.name))
    if not pts:
        return None, []
    x = sum(p.x for p, _ in pts) / len(pts)
    y = sum(p.y for p, _ in pts) / len(pts)
    z = sum(p.z for p, _ in pts) / len(pts)
    return gemmi.Position(x, y, z), [n for _, n in pts]


def patch(tgt, centre, radius=RADIUS):
    out = []
    for ch in tgt:
        for r in ch:
            if r.name not in MODEL_PKA:
                continue
            p = sidechain_centre(r)
            if p and p.dist(centre) <= radius:
                out.append((ch.name, r.seqid.num, r.name, p.dist(centre)))
    return out


def main():
    if '--selftest' in sys.argv:
        selftest(); return
    path = sys.argv[1]
    st = gemmi.read_structure(path)
    st.setup_entities()
    model = st[0]
    tgt = [c for c in model if family(c) is not None]
    names = [c.name for c in tgt]
    print(f"{os.path.basename(path)}  target protomers {names}")
    if len(tgt) != 3:
        sys.exit(f"REFUSE: {len(tgt)} target protomers, need 3")

    specs = {
        'seam2 (A73+C73)':   [(names[0], 73), (names[2], 73)],
        'seam3 (all H73)':   [(n, 73) for n in names],
        'single H73 (A)':    [(names[0], 73)],
        'GLU146 patch (A)':  [(names[0], 146)],
        'GLU127 patch (A)':  [(names[0], 127)],
    }
    print(f"\npatch radius {RADIUS:.0f} A, model pKa, net charge in e")
    print(f"{'patch':22s} {'residues':>9s} {'pH 7.4':>9s} {'pH 6.0':>9s} {'delta':>8s}")
    res = {}
    for label, spec in specs.items():
        c, found = centre_of(tgt, spec)
        if c is None:
            print(f"{label:22s}  centre residues not found {spec}")
            continue
        pr = patch(tgt, c)
        q = {ph: sum(charge(rn, ph) for _, _, rn, _ in pr) for ph in PHS}
        res[label] = q
        print(f"{label:22s} {len(pr):9d} {q[7.4]:+9.2f} {q[6.0]:+9.2f} {q[6.0]-q[7.4]:+8.2f}")
        comp = {}
        for _, _, rn, _ in pr:
            comp[rn] = comp.get(rn, 0) + 1
        print(f"{'':22s} composition: " + ", ".join(f"{k} {v}" for k, v in sorted(comp.items())))

    print("\nBARS")
    for key in ('seam2 (A73+C73)', 'seam3 (all H73)'):
        if key not in res:
            continue
        q = res[key]
        e1 = q[7.4] > 0 and q[6.0] > 0
        print(f"  E1c {key}: net > 0 at BOTH pH -> {'PASS' if e1 else 'FAIL'} "
              f"({q[7.4]:+.2f} / {q[6.0]:+.2f})")
    if 'seam2 (A73+C73)' in res and 'GLU146 patch (A)' in res:
        a, b = res['seam2 (A73+C73)'][6.0], res['GLU146 patch (A)'][6.0]
        print(f"  E2c seam more positive than Glu146 patch at pH 6.0 -> "
              f"{'PASS' if a > b else 'FAIL'} ({a:+.2f} vs {b:+.2f})")


if __name__ == '__main__':
    main()
