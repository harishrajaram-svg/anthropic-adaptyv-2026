#!/usr/bin/env python3
"""Build the E1 epitope-sweep pool: one pose per unique BINDER SEQUENCE.

PREREG: analysis/02-tnf/PREREG-E1-EPITOPE-SWEEP-2026-10-11.md

WHY DEDUP IS ON SEQUENCE AND NOT ON DESIGN ID
---------------------------------------------
ROADMAP records that several design ids carry two distinct sequences, after an aborted run left a
parallel output tree, and that a first-match glob consequently ran 3 of 12 sequence screens on the
wrong molecule. This session independently found tnfa_corrected_40_L1r1k5 in the acidban, humansel
and v3 input trees carrying three different sequences behind one id. Keying on the id would average
across different molecules while reporting one name, so the key here is a hash of the binder chain's
own one-letter sequence, read out of the CIF.

Species is decided by the gate's histidine fingerprint (ph_gate_all.family), never by the path.
Only human TNF is a registered family, so mouse complexes and anything malformed are REFUSED and
counted, not silently admitted on the strength of a directory name.
"""
import sys, os, json, hashlib, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gemmi
from ph_gate_all import family

CAP = 1200


def one_letter(res):
    t = gemmi.find_tabulated_residue(res.name)
    return t.one_letter_code.upper() if t and t.one_letter_code else 'X'


def classify(path):
    """-> (kind, binder_seq, nprot) ; kind in {'ok','not_human','bad_chains','unreadable'}"""
    try:
        st = gemmi.read_structure(path)
        st.setup_entities()
        model = st[0]
    except Exception:
        return 'unreadable', None, 0
    tgt, bnd = [], []
    for ch in model:
        if family(ch) is not None:
            tgt.append(ch.name)
        else:
            bnd.append(ch)
    if not tgt:
        return 'not_human', None, 0
    if len(bnd) != 1:
        return 'bad_chains', None, len(tgt)
    seq = ''.join(one_letter(r) for r in bnd[0])
    return 'ok', seq, len(tgt)


def dockq_index():
    """design id -> best ca_sc_dockq seen, for the prereg's cap ordering. Missing is fine."""
    best = {}
    for f in glob.glob('analysis/02-tnf/depth_rounds/round*.tsv'):
        with open(f) as fh:
            hdr = fh.readline().rstrip('\n').split('\t')
            if 'ca_sc_dockq_human' not in hdr:
                continue
            i_id, i_h = hdr.index('id'), hdr.index('ca_sc_dockq_human')
            for line in fh:
                p = line.rstrip('\n').split('\t')
                if len(p) <= max(i_id, i_h):
                    continue
                try:
                    v = float(p[i_h])
                except ValueError:
                    continue
                if v > best.get(p[i_id], -1):
                    best[p[i_id]] = v
    return best


def main():
    paths = [l.strip() for l in open(sys.argv[1]) if l.strip()]
    dq = dockq_index()
    pool, nulls, counts = {}, {}, {'ok': 0, 'not_human': 0, 'bad_chains': 0, 'unreadable': 0}
    for n, p in enumerate(paths, 1):
        if n % 250 == 0:
            print(f'  ...{n}/{len(paths)}  pool {len(pool)}  nulls {len(nulls)}', flush=True)
        kind, seq, nprot = classify(p)
        counts[kind] += 1
        if kind != 'ok':
            continue
        did = os.path.basename(p).split('_seed')[0]
        rec = {'path': p, 'id': did, 'nprot': nprot, 'dockq': dq.get(did),
               'seq_sha': hashlib.sha256(seq.encode()).hexdigest()[:12], 'len': len(seq)}
        tbl = nulls if os.path.basename(p).startswith('null_') else pool
        k = rec['seq_sha']
        # keep the representative with the best known pose; unknown loses to known
        cur = tbl.get(k)
        if cur is None or (rec['dockq'] or -1) > (cur['dockq'] or -1):
            tbl[k] = rec
    print(f'\nscanned {len(paths)}  ' + '  '.join(f'{k}={v}' for k, v in counts.items()))
    print(f'unique binder sequences: pool {len(pool)}  nulls {len(nulls)}')
    sel = sorted(pool.values(), key=lambda r: -(r['dockq'] if r['dockq'] is not None else -1))
    if len(sel) > CAP:
        print(f'CAP: {len(sel)} -> {CAP} by best available ca_sc_dockq (prereg)')
        sel = sel[:CAP]
    json.dump({'pool': sel, 'nulls': list(nulls.values()), 'counts': counts},
              open(sys.argv[2], 'w'), indent=1)
    with open(sys.argv[3], 'w') as fh:
        for r in sel:
            fh.write(r['path'] + '\n')
    print(f"wrote {sys.argv[2]} and {sys.argv[3]} ({len(sel)} poses, {len(nulls)} nulls)")


if __name__ == '__main__':
    main()
