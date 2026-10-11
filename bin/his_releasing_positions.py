"""$0 geometry scan: which binder positions on 40_L1r4k1 could host a RELEASING histidine.

Releasing = at pH 6.0 the protonated His+ meets a target CATION (repulsion -> release).
Tightening = His+ meets a target CARBOXYLATE (attraction -> grip, the error we made).
Reads the existing fold. No compute, no network.
"""
import sys, math
from collections import defaultdict

cif = sys.argv[1]

# minimal mmCIF atom_site parser
cols, rows, in_loop, hdr = [], [], False, False
for line in open(cif):
    s = line.strip()
    if s.startswith('_atom_site.'):
        cols.append(s.split('.')[1]); in_loop = True; hdr = True; continue
    if in_loop and hdr:
        if s.startswith('#') or s.startswith('loop_') or not s:
            if rows: break
            continue
        p = s.split()
        if len(p) != len(cols):
            if rows: break
            continue
        rows.append(p)
i = {c: n for n, c in enumerate(cols)}

atoms = []
for p in rows:
    if p[i['group_PDB']] != 'ATOM': continue
    atoms.append(dict(
        chain=p[i['label_asym_id']], resi=int(p[i['label_seq_id']]),
        resn=p[i['label_comp_id']], atom=p[i['label_atom_id']],
        x=float(p[i['Cartn_x']]), y=float(p[i['Cartn_y']]), z=float(p[i['Cartn_z']])))

bychain = defaultdict(list)
for a in atoms: bychain[a['chain']].append(a)
sizes = {c: len({a['resi'] for a in v}) for c, v in bychain.items()}
print("chains (residue counts):", sizes)

binder_chain = min(sizes, key=lambda c: sizes[c])
print(f"binder chain = {binder_chain} ({sizes[binder_chain]} res); target = everything else\n")

binder = [a for a in atoms if a['chain'] == binder_chain]
target = [a for a in atoms if a['chain'] != binder_chain]

CATION = {('LYS','NZ'),('ARG','NE'),('ARG','NH1'),('ARG','NH2')}
ACID   = {('ASP','OD1'),('ASP','OD2'),('GLU','OE1'),('GLU','OE2')}
t_cat = [a for a in target if (a['resn'], a['atom']) in CATION]
t_acd = [a for a in target if (a['resn'], a['atom']) in ACID]
t_all = [a for a in target if a['atom'] != 'H']
print(f"target charged groups in reach: {len(t_cat)} cation atoms, {len(t_acd)} carboxylate atoms")

def d(a, b):
    return math.dist((a['x'],a['y'],a['z']), (b['x'],b['y'],b['z']))

# per binder residue: use the side-chain tip (furthest heavy atom from CA) as the proxy
res = defaultdict(list)
for a in binder: res[a['resi']].append(a)

seq3to1 = {'ALA':'A','ARG':'R','ASN':'N','ASP':'D','CYS':'C','GLN':'Q','GLU':'E','GLY':'G',
           'HIS':'H','ILE':'I','LEU':'L','LYS':'K','MET':'M','PHE':'F','PRO':'P','SER':'S',
           'THR':'T','TRP':'W','TYR':'Y','VAL':'V'}

out = []
for resi in sorted(res):
    ats = res[resi]
    ca = next((a for a in ats if a['atom'] == 'CA'), None)
    if not ca: continue
    tip = max(ats, key=lambda a: d(a, ca))
    mind_all = min((d(tip, t) for t in t_all), default=999)
    mind_cat = min((d(tip, t) for t in t_cat), default=999)
    mind_acd = min((d(tip, t) for t in t_acd), default=999)
    out.append((resi, seq3to1.get(ats[0]['resn'],'X'), mind_all, mind_cat, mind_acd))

iface = [r for r in out if r[2] <= 5.0]
print(f"\ninterface residues (side-chain tip within 5.0 A of target): {len(iface)} of {len(out)}\n")

# A releasing candidate: a cation is reachable AND closer than any carboxylate
rel = [r for r in iface if r[3] <= 8.0 and r[3] < r[4]]
tig = [r for r in iface if r[4] <= 8.0 and r[4] <= r[3]]

print(f"{'pos':>4} {'aa':>3} {'d_target':>9} {'d_cation':>9} {'d_acid':>8}   call")
for r in sorted(iface, key=lambda r: r[3]):
    call = 'RELEASING candidate' if r in rel else ('tightening' if r in tig else '-')
    print(f"{r[0]:>4} {r[1]:>3} {r[2]:9.2f} {r[3]:9.2f} {r[4]:8.2f}   {call}")

print(f"\nSUMMARY: {len(rel)} releasing candidates, {len(tig)} tightening, "
      f"{len(iface)-len(rel)-len(tig)} neither")
print("current His positions in binder:",
      [resi for resi in sorted(res) if res[resi][0]['resn'] == 'HIS'])
