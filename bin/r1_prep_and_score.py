#!/usr/bin/env python3
"""R1: strip each calibration structure to one copy of (target + binder), then score it.

PREREG: analysis/02-tnf/PREREG-R1-GATE-CALIBRATION-2026-10-11.md

WHY A PREP STEP. Most PDB entries hold several copies in the asymmetric unit. score_pose's
free-target leg deletes the binder chains and then asserts the remaining chain count equals the
target count, so any extra copy left in the file trips that assertion. Extracting exactly the named
chains is also the honest thing: scoring two copies of one complex would double-count it.

DIRECTION IS PER MOLECULE, as the prereg requires. `want` is what the gate should say at the
problem-2 pH pair (6.0 vs 7.4): 'release' = ratio < 1, 'tighten' = ratio > 1, 'flat' = near 1.
It is recorded here from the publication BEFORE scoring, never fitted afterwards.
"""
import os, sys, json, argparse, subprocess
import gemmi

HERE = os.path.dirname(os.path.abspath(__file__))

# pdb: (target_chains, binder_chains, class, published_fold, want, label)
SET = {
    # --- POSITIVES: weaker at acidic, i.e. problem 2's own direction -> expect ratio < 1
    '3WD5': (['A'], ['H', 'L'], 'pos', 9.0,    'release', 'adalimumab / TNF-alpha  *** our target'),
    '1BRS': (['A'], ['D'],      'pos', 1200.0, 'release', 'barnase / barstar, titrating acid pKa 6.4'),
    '5B71': (['E'], ['A', 'B'], 'pos', 1105.0, 'release', 'SKY59 crovalimab / C5 MG1'),
    '5I5K': (['B'], ['H', 'L'], 'pos', 21.0,   'release', 'eculizumab / C5'),
    '9X1H': (['B'], ['H', 'L'], 'pos', 120.0,  'release', 'RAY121 / C1s CUB'),
    # --- POSITIVES running the OTHER way: tighter at acidic -> expect ratio > 1
    '7SU0': (['C'], ['H', 'L'], 'pos', 77.0,   'tighten', 'Ipi.105 / CTLA-4'),
    '7SU1': (['C'], ['H', 'L'], 'pos', 20.0,   'tighten', 'Ipi.106 / CTLA-4'),
    '8TBQ': (['P'], ['H', 'L'], 'pos', 1000.0, 'tighten', 'SNS-101 / VISTA'),
    '4K71': (['B', 'C'], ['A'], 'pos', 760.0,  'tighten', 'HSA13 / FcRn + b2m'),
    # --- NEGATIVES: measured flat -> expect ratio near 1
    '5TRU': (['C'], ['H', 'L'], 'neg', 1.1,    'flat', 'ipilimumab / CTLA-4, 8-point series'),
    '6FGB': (['A', 'B'], ['H', 'L'], 'neg', 1.34, 'flat', 'rozanolixizumab / FcRn + b2m'),
    '5HYS': (['G'], ['H', 'L'], 'neg', 1.31,   'flat', 'omalizumab / IgE-Fc'),
    '3SQO': (['A', 'P'], ['H', 'L'], 'neg', 1.3, 'flat', 'J16 / PCSK9 + prodomain'),
    '8J6F': (['I'], ['H', 'L'], 'neg', 2.2,    'flat', 'tocilizumab / IL-6R'),
    '9MI6': (['A', 'B'], ['H', 'L'], 'neg', 1.8, 'flat', 'nipocalimab / FcRn + b2m'),
    '9S60': (['A'], ['B'],      'neg', 1.65,   'flat', 'DARPin 4m3 / cathepsin B'),
}


def prep(pdb, tg, bd, out):
    st = gemmi.read_structure(f'runs/R1-pdb/{pdb}.cif')
    st.setup_entities(); st.remove_ligands_and_waters(); st.remove_alternative_conformations()
    st.remove_hydrogens(); st.setup_entities()
    keep = set(tg) | set(bd)
    have = {c.name for c in st[0]}
    missing = keep - have
    if missing:
        return f'chains {sorted(missing)} absent; file has {sorted(have)}'
    while len(st) > 1:
        del st[1]
    for i in range(len(st[0]) - 1, -1, -1):
        if st[0][i].name not in keep:
            del st[0][i]
    st.setup_entities()
    got = sorted(c.name for c in st[0])
    if got != sorted(keep):
        return f'after stripping, chains are {got}, wanted {sorted(keep)}'
    st.make_mmcif_document().write_file(out)
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default='runs/R1-prepped')
    ap.add_argument('--only')
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    manifest = []
    for pdb, (tg, bd, cls, fold, want, label) in sorted(SET.items()):
        if a.only and pdb != a.only:
            continue
        dst = os.path.join(a.out, f'{pdb}.cif')
        err = prep(pdb, tg, bd, dst)
        if err:
            print(f'  REFUSED {pdb}: {err}'); continue
        manifest.append(dict(pdb=pdb, target=tg, binder=bd, cls=cls,
                             published_fold=fold, want=want, label=label, cif=dst))
        print(f'  {pdb}  target {"+".join(tg):6s} binder {"+".join(bd):4s}  '
              f'{cls}  {want:8s} {fold:>8.1f}x  {label}')
    json.dump(manifest, open(os.path.join(a.out, 'manifest.json'), 'w'), indent=1)
    print(f'\nprepped {len(manifest)} of {len(SET)} -> {a.out}/manifest.json')


if __name__ == '__main__':
    main()
