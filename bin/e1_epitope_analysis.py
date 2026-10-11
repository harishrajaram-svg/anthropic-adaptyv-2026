#!/usr/bin/env python3
"""E1 analysis: split every pose's coupled product into target-owned and binder-owned.

PREREG: analysis/02-tnf/PREREG-E1-EPITOPE-SWEEP-2026-10-11.md
Bars, fixed before the sweep ran:
  E1  any pose with target_owned < 1.0
  E2  >=1 epitope fingerprint class with >=5 poses and median target_owned < 1.0
  E3  pool minimum target_owned >= 1.0  -> objective 2 closed on target electrostatics
  E4  target_owned higher when Glu146 contributes, Mann-Whitney one-sided p < 0.05

Protomer letters are stripped from site names before fingerprinting, because chain labelling is
arbitrary across this project's run directories (ph_gate_all.orient documents 29 of 69 directories
putting the target in chain A) and GLU146 on protomer A is the same residue as GLU146 on protomer C.
"""
import sys, os, json, glob, math, re, statistics as st
from collections import Counter, defaultdict

MIN_CLASS = 5


def mannwhitney_greater(x, y):
    """One-sided U test, H1: x stochastically greater than y. Normal approx, tie-corrected.

    No scipy in this environment. n here is in the hundreds, where the approximation is sound;
    it is NOT valid for the handful-sized groups, so the caller must check n and say so.
    """
    nx, ny = len(x), len(y)
    if nx == 0 or ny == 0:
        return None, None
    allv = sorted(x + y)
    ranks, i = {}, 0
    while i < len(allv):
        j = i
        while j + 1 < len(allv) and allv[j + 1] == allv[i]:
            j += 1
        r = (i + j) / 2.0 + 1.0
        ranks[allv[i]] = r
        i = j + 1
    rx = sum(ranks[v] for v in x)
    u = rx - nx * (nx + 1) / 2.0
    mu = nx * ny / 2.0
    tie = sum(t ** 3 - t for t in Counter(allv).values())
    n = nx + ny
    var = nx * ny / 12.0 * ((n + 1) - tie / (n * (n - 1)))
    if var <= 0:
        return u, None
    z = (u - mu) / math.sqrt(var)
    p = 0.5 * math.erfc(z / math.sqrt(2.0))          # upper tail
    return u, p


def strip_chain(key):
    """'target:A/GLU146' -> 'GLU146' ; 'binder:HIS61' -> 'HIS61'"""
    k = key.split(':', 1)[1]
    return k.split('/', 1)[1] if '/' in k else k


def load():
    recs = []
    for f in sorted(glob.glob('runs/E1-sweep/chunk_*.json')):
        recs += json.load(open(f))
    return recs


def main():
    recs = load()
    rows = []
    for m in recs:
        if m.get('verdict') != 'ok':
            rows.append({'file': m['file'], 'skip': m.get('verdict', 'no-verdict')})
            continue
        sites, contrib = m['sites'], m['contributing']
        pt = pb = 1.0
        tsites, bsites = [], []
        for k in contrib:
            s = sites[k]
            if k.startswith('target'):
                pt *= s['ratio']; tsites.append(strip_chain(k))
            else:
                pb *= s['ratio']; bsites.append(strip_chain(k))
        rows.append({
            'file': m['file'], 'skip': None,
            'is_null': os.path.basename(m['file']).startswith('null_'),
            'total': m['product'], 'target_owned': pt, 'binder_owned': pb,
            'glu146': 'GLU146' in tsites,
            'fp': ','.join(sorted(set(tsites))) or '(none)',
            'n_target_sites': len(tsites), 'n_binder_sites': len(bsites),
        })
    ok = [r for r in rows if not r['skip']]
    pool = [r for r in ok if not r['is_null']]
    nulls = [r for r in ok if r['is_null']]
    skipped = [r for r in rows if r['skip']]
    print(f'records {len(rows)}  scored {len(ok)}  pool {len(pool)}  nulls {len(nulls)}  '
          f'refused {len(skipped)}')
    if skipped:
        print('  refusals: ' + ', '.join(f'{k}={v}' for k, v in
                                         Counter(r['skip'] for r in skipped).most_common()))

    tv = [r['target_owned'] for r in pool]
    print(f'\nTARGET-OWNED product over {len(tv)} poses')
    print(f'  min {min(tv):.4f}   median {st.median(tv):.4f}   max {max(tv):.4f}')
    print(f'  below 1.0: {sum(1 for v in tv if v < 1.0)}   at/above: {sum(1 for v in tv if v >= 1.0)}')
    bv = [r['binder_owned'] for r in pool]
    print(f'BINDER-OWNED product: min {min(bv):.4f}  median {st.median(bv):.4f}  '
          f'below 1.0: {sum(1 for v in bv if v < 1.0)}')
    tot = [r['total'] for r in pool]
    print(f'TOTAL product: min {min(tot):.4f}  median {st.median(tot):.4f}  '
          f'below 1.0: {sum(1 for v in tot if v < 1.0)}')

    # ---- E1 / E3
    e1 = [r for r in pool if r['target_owned'] < 1.0]
    print(f'\nE1  any pose target_owned < 1.0 : {"PASS" if e1 else "FAIL"}  (n={len(e1)})')
    print(f'E3  pool minimum >= 1.0          : {"PASS -> STOP" if not e1 else "not fired"}'
          f'  (min {min(tv):.4f})')
    for r in sorted(e1, key=lambda r: r['target_owned'])[:15]:
        print(f'    {r["target_owned"]:7.4f}  binder {r["binder_owned"]:8.4f}  '
              f'total {r["total"]:9.4f}  {r["file"][:46]}  [{r["fp"]}]')

    # ---- E2
    cls = defaultdict(list)
    for r in pool:
        cls[r['fp']].append(r['target_owned'])
    big = {k: v for k, v in cls.items() if len(v) >= MIN_CLASS}
    passing = {k: v for k, v in big.items() if st.median(v) < 1.0}
    print(f'\nE2  fingerprint classes with >={MIN_CLASS} poses: {len(big)} of {len(cls)} distinct; '
          f'median < 1.0 in {len(passing)}  -> {"PASS" if passing else "FAIL"}')
    print(f'    {"n":>5s} {"median":>9s} {"min":>9s}  fingerprint')
    for k, v in sorted(big.items(), key=lambda kv: st.median(kv[1]))[:12]:
        print(f'    {len(v):5d} {st.median(v):9.4f} {min(v):9.4f}  {k[:70]}')

    # ---- E4
    g = [r['target_owned'] for r in pool if r['glu146']]
    ng = [r['target_owned'] for r in pool if not r['glu146']]
    u, p = mannwhitney_greater(g, ng)
    print(f'\nE4  Glu146 contributing (n={len(g)}, median '
          f'{st.median(g) if g else float("nan"):.4f}) vs not (n={len(ng)}, median '
          f'{st.median(ng) if ng else float("nan"):.4f})')
    print(f'    Mann-Whitney one-sided p = {p:.3e}  -> {"PASS" if p is not None and p < 0.05 else "FAIL"}'
          if p is not None else '    not evaluable')

    # ---- control
    if nulls:
        nv = [r['target_owned'] for r in nulls]
        print(f'\nCONTROL shuffled-binder nulls (n={len(nv)}): min {min(nv):.4f}  '
              f'median {st.median(nv):.4f}  below 1.0: {sum(1 for v in nv if v < 1.0)}')
        u2, p2 = mannwhitney_greater(tv, nv)
        print(f'    designs vs nulls, one-sided p = {p2:.3e}' if p2 is not None else '')

    # ---- which target residues carry it
    agg = defaultdict(list)
    for m in recs:
        if m.get('verdict') != 'ok' or os.path.basename(m['file']).startswith('null_'):
            continue
        for k in m['contributing']:
            if k.startswith('target'):
                agg[strip_chain(k)].append(m['sites'][k]['ratio'])
    print(f'\nTARGET sites by how often they contribute')
    print(f'    {"n":>5s} {"median":>8s} {"max":>9s}  residue')
    for k, v in sorted(agg.items(), key=lambda kv: -len(kv[1]))[:12]:
        print(f'    {len(v):5d} {st.median(v):8.3f} {max(v):9.3f}  {k}')

    with open('analysis/02-tnf/E1_epitope_sweep.tsv', 'w') as fh:
        fh.write('file\tis_null\ttotal\ttarget_owned\tbinder_owned\tglu146\t'
                 'n_target_sites\tn_binder_sites\tfingerprint\n')
        for r in sorted(ok, key=lambda r: r['target_owned']):
            fh.write(f"{r['file']}\t{int(r['is_null'])}\t{r['total']:.6f}\t"
                     f"{r['target_owned']:.6f}\t{r['binder_owned']:.6f}\t{int(r['glu146'])}\t"
                     f"{r['n_target_sites']}\t{r['n_binder_sites']}\t{r['fp']}\n")
    print('\nwrote analysis/02-tnf/E1_epitope_sweep.tsv')


if __name__ == '__main__':
    main()
