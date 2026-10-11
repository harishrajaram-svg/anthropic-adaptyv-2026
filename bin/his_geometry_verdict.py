"""For each of the 12: does its EXISTING histidine sit in a releasing geometry?

Releasing  = His side-chain tip nearer a target CATION than a target CARBOXYLATE
             -> protonation at pH 6.0 adds repulsion -> release.
Tightening = nearer a carboxylate -> protonation adds attraction -> grips harder.
$0, local, reads the committed folds.
"""
import csv, math, sys
from collections import defaultdict

CATION = {('LYS','NZ'),('ARG','NE'),('ARG','NH1'),('ARG','NH2')}
ACID   = {('ASP','OD1'),('ASP','OD2'),('GLU','OE1'),('GLU','OE2')}

def atoms_of(cif):
    cols, rows, hdr = [], [], False
    for line in open(cif):
        s = line.strip()
        if s.startswith('_atom_site.'):
            cols.append(s.split('.')[1]); hdr = True; continue
        if hdr:
            if s.startswith('#') or s.startswith('loop_') or not s:
                if rows: break
                continue
            p = s.split()
            if len(p) != len(cols):
                if rows: break
                continue
            rows.append(p)
    i = {c: n for n, c in enumerate(cols)}
    out = []
    for p in rows:
        if p[i['group_PDB']] != 'ATOM': continue
        out.append(dict(chain=p[i['label_asym_id']], resi=int(p[i['label_seq_id']]),
                        resn=p[i['label_comp_id']], atom=p[i['label_atom_id']],
                        x=float(p[i['Cartn_x']]), y=float(p[i['Cartn_y']]), z=float(p[i['Cartn_z']])))
    return out

def d(a,b): return math.dist((a['x'],a['y'],a['z']),(b['x'],b['y'],b['z']))

f = (l for l in open('analysis/02-tnf/depth12_canonical_sequences_2026-10-09.tsv') if not l.startswith('#'))
print(f"{'design':<14}{'His':>4}  {'pos':>4} {'d_tgt':>6} {'d_cat':>6} {'d_acid':>7}  verdict")
tally = defaultdict(int)
for r in csv.DictReader(f, delimiter='\t'):
    name = r['design'].replace('tnfa_corrected_','')
    ats = atoms_of(r['source_cif'])
    bychain = defaultdict(set)
    for a in ats: bychain[a['chain']].add(a['resi'])
    bc = min(bychain, key=lambda c: len(bychain[c]))
    binder = [a for a in ats if a['chain']==bc]
    target = [a for a in ats if a['chain']!=bc]
    t_cat = [a for a in target if (a['resn'],a['atom']) in CATION]
    t_acd = [a for a in target if (a['resn'],a['atom']) in ACID]
    t_all = [a for a in target if a['atom']!='H']

    his = sorted({a['resi'] for a in binder if a['resn']=='HIS'})
    if not his:
        print(f"{name:<14}{0:>4}  {'-':>4} {'-':>6} {'-':>6} {'-':>7}  NO HISTIDINE — cannot switch")
        tally['no_his'] += 1
        continue
    for resi in his:
        g = [a for a in binder if a['resi']==resi]
        ca = next(a for a in g if a['atom']=='CA')
        tip = max(g, key=lambda a: d(a,ca))
        dt = min((d(tip,t) for t in t_all), default=999)
        dc = min((d(tip,t) for t in t_cat), default=999)
        da = min((d(tip,t) for t in t_acd), default=999)
        if dt > 8.0:
            v, k = "not at the interface", 'off_iface'
        elif dc < da:
            v, k = "RELEASING", 'releasing'
        else:
            v, k = "tightening (inverted)", 'tightening'
        tally[k] += 1
        print(f"{name:<14}{len(his):>4}  {resi:>4} {dt:6.2f} {dc:6.2f} {da:7.2f}  {v}")

print(f"\nVERDICT over 12 designs: releasing {tally['releasing']} · "
      f"tightening {tally['tightening']} · off-interface {tally['off_iface']} · "
      f"no histidine {tally['no_his']}")
