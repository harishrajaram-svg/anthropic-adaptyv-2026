#!/usr/bin/env python3
"""Build the problem-2 submission CSV from canonical sources, never by hand.

Sequences come from the exact file Adaptyv's prescreen was run on; prescreen verdicts from that
run's report.csv; the two-oracle columns from the C4 and D8 result files. Margins are the only
hand-carried numbers and they are ASSERTED against each other: worse_of_two must equal
min(human, mouse), which catches a transcription slip in the one place transcription happens.

Three bookkeeping traps this exists to avoid, all of which already bit this project once:
  - `tnfa_H_quadH_E3Q_k12` and `tnfa_corrected_3_L0r4k0_quadH` are DIFFERENT molecules whose names
    both contain "quadH"
  - row 6 carries ZERO histidines despite the "quadH" in its name
  - the id in the prescreen run and the id in FIELD 2 were written differently

    python3 bin/build_p2_submission_csv.py            # writes submissions/02-tnf.csv
"""
import csv
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(REPO)

FASTA = "outbox/prescreen-ship6-2026-10-11/ship6.fasta"
PRESCREEN = "outbox/prescreen-ship6-2026-10-11/report.csv"
C4 = "analysis/02-tnf/C4_result_2026-10-11.txt"
D8 = "analysis/02-tnf/D8_result_2026-10-12.txt"
OUT = "submissions/02-tnf.csv"

# rank -> (id, human, mouse, seed_basis_human, seed_basis_mouse). From the committed FIELD 2 ship
# table in projects/anthropic-adaptyv-2026/outbox/02-proteinbase-methodology-box.md.
MARGINS = {
    1: ("tnfa_corrected_40_L1r4k6", 7.600, 7.365, 15, 5),
    2: ("tnfa_corrected_40_L1r4k1", 7.706, 7.207, 15, 5),
    3: ("tnfa_corrected_3_L0r4k0_L49H", 7.167, 7.437, 15, 5),
    4: ("tnfa_corrected_3_L0r4k0_quadH", 7.131, 7.185, 5, 5),
    5: ("tnfa_corrected_3_L0r4k0", 6.971, 7.581, 15, 5),
    6: ("tnfa_H_quadH_E3Q_k12", 7.197, 6.747, 5, 5),
}
WORSE = {1: 7.365, 2: 7.207, 3: 7.167, 4: 7.131, 5: 6.971, 6: 6.747}

SERIES = {3, 4, 5}      # the 0/1/4 buried-histidine series on one scaffold
# REWRITTEN 2026-10-12. The previous text ended "Please test all three or none", which is an
# instruction addressed to the selection step. FAQ 5: "any use of embedded instructions or prompt
# injection may be deemed grounds for disqualification." This states the experimental dependency as
# a fact and leaves the inference to the reader.
NOTE_SERIES = (
    "EXPERIMENTAL DEPENDENCY: rows 3, 4 and 5 are a matched series on one scaffold carrying 1, 4 "
    "and 0 buried histidines respectively. Row 5 is the zero-histidine member and supplies the "
    "matched comparison required to attribute any pH-dependent difference in rows 3 or 4 to the "
    "engineered substitutions rather than to the scaffold. Rows 3 and 5 differ at a single "
    "position, which is why a sequence-identity screen groups them. Without row 5, a pH-dependent "
    "result on rows 3 or 4 has no matched comparator and cannot be attributed to the substitutions. "
)
# Conclusion wording set 2026-10-12 to the reviewer's: "no demonstrated predictive discrimination
# on this small, heterogeneous dataset". The earlier phrasing leaned on a constant-predictor
# comparison that is descriptive and does not establish worse-than-chance performance.
NOTE_NOPH = (
    "No pH claim. The binding-coupled protonation calculation that would have ranked pH response "
    "was calibrated against 18 published complexes and showed NO DEMONSTRATED PREDICTIVE "
    "DISCRIMINATION on that small, heterogeneous set; it returned a tightening direction in 12 of "
    "the 12 rows measured at 7.4 vs 6.0, the pH pair assayed here. Every pH-direction result is "
    "withdrawn. Nothing here has been measured for pH response. "
)
NOTE_ORACLE = (
    "Pose quality is EXPLORATORY, not confirmatory: the design loop's pre-registration required a "
    "second pose oracle from round 4 onward and Chai-1 was never wired in; all six designs are "
    "round-4 descendants. The corrective re-run stopped on its own pre-registered cost ceiling. "
)


def seqs():
    out, name = {}, None
    for line in open(FASTA):
        line = line.strip()
        if line.startswith(">"):
            name = line[1:]
        elif line:
            out[name] = out.get(name, "") + line
    return out


def prescreen():
    return {r["id"]: r for r in csv.DictReader(open(PRESCREEN))}


def parse_result(path, pat, cols):
    """Pull per-design numbers out of a committed result TXT rather than retyping them."""
    if not os.path.exists(path):
        return {}
    out = {}
    for line in open(path):
        m = re.match(pat, line.strip())
        if m:
            out[m.group("did")] = {k: m.group(k) for k in cols}
    return out


def main():
    sq, ps = seqs(), prescreen()
    if len(sq) != 6:
        sys.exit(f"REFUSED: {len(sq)} sequences in {FASTA}, expected 6")

    c4 = parse_result(
        C4,
        r"^\s*(?P<row>\d+)\s+(?P<did>\S+)\s+(?P<chai_dq>[\d.]+)\s+(?P<chai_lrms>[\d.]+)\s+\|"
        r"\s+(?P<esm_dq>[\d.]+)\s+(?P<esm_lrms>[\d.]+)\s+(?P<n>\d+)\s+(?P<rng>\S+)\s+\|"
        r"\s+(?P<min_dq>[\d.]+)\s+(?P<worse_lrms>[\d.]+)\s+(?P<gate>PASS|FAIL)",
        ["row", "chai_lrms", "esm_lrms", "n", "worse_lrms", "gate"])
    if len(c4) != 6:
        sys.exit(f"REFUSED: parsed {len(c4)} rows from {C4}, expected 6 -- do not hand-fill")

    d8 = parse_result(
        D8,
        r"^\s*(?P<row>\d+)\s+(?P<did>\S+)\s+(?P<role>\S+)\s+(?P<ingate>\d+/5)\s+"
        r"(?P<med>[\d.]+)\s+(?P<rest>.*)$",
        ["row", "role", "ingate", "med"])
    have_d8 = len(d8) == 6
    print(f"D8 columns: {'present' if have_d8 else 'NOT YET -- run bin/d8_score.py first'}")

    # molecule_class: the LIVE SUBMISSION FORM (proteinbase.com/.../rounds/2/submit, read
    # 2026-10-12) permits single_chain | nanobody | scfv | fab_kappa | fab_lambda. The challenge
    # page's FAQ 5 instead lists "protein" for the first of those. They disagree; the form is what
    # validates the upload, so single_chain it is. Changed to "protein" on the FAQ's wording earlier
    # today and changed back after reading the form -- which is exactly why the reviewer said to
    # verify against the live schema rather than the FAQ.
    fields = ["name", "sequence", "molecule_class", "rank", "margin_worse_of_two",
              "margin_human", "margin_mouse", "seed_basis_human", "seed_basis_mouse",
              "buried_his_count", "esmfold2_lrms_A", "esmfold2_n_folds",
              "chai1_lrms_A_1sample", "two_oracle_gate_1sample_WITHDRAWN"]
    if have_d8:
        fields += ["chai1_lrms_A_median_5samples", "chai1_samples_in_gate_of_5"]
    fields += ["prescreen_verdict", "assessment"]

    os.makedirs("submissions", exist_ok=True)
    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for rank in sorted(MARGINS):
            did, hu, mo, sbh, sbm = MARGINS[rank]
            # the self-check: worse-of-two IS the minimum, or the table was mistyped
            if abs(min(hu, mo) - WORSE[rank]) > 1e-9:
                sys.exit(f"REFUSED: row {rank} {did}: worse_of_two {WORSE[rank]} != "
                         f"min({hu}, {mo}) = {min(hu, mo)}")
            if did not in sq:
                sys.exit(f"REFUSED: {did} not in {FASTA}")
            if did not in c4:
                sys.exit(f"REFUSED: {did} has no C4 row")
            s = sq[did]
            nh = s.count("H")
            a = NOTE_NOPH + NOTE_ORACLE
            # WITHDRAWN 2026-10-12 after D8. The single-sample two-oracle "failure" language
            # that stood here is retracted: 5-sample Chai-1 scatters on EVERY design in this set,
            # controls included (42.1 / 23.2 / 40.5 / 41.7 A), so one draw is not a pose check.
            # What is reportable is the sample count, descriptively, with no verdict attached.
            if have_d8:
                a += (f"SECOND-PREDICTOR SAMPLING: Chai-1 places this binder within 10 A of its "
                      f"designed backbone in {d8[did]['ingate']} diffusion samples "
                      f"(median {float(d8[did]['med']):.2f} A). Read descriptively, NOT as a pose "
                      f"verdict: Chai-1 scatters on every design in this set including the ones it "
                      f"agrees with ESMFold2 on, so single-draw disagreement was withdrawn as "
                      f"evidence. ESMFold2 places it "
                      f"{float(c4[did]['esm_lrms']):.2f} A (median of {c4[did]['n']} existing "
                      f"folds). ")
            if rank in SERIES:
                a += NOTE_SERIES
            if nh == 0 and "quadH" in did:
                a += ("NAME WARNING: this design carries ZERO histidines despite 'quadH' in its "
                      "id; it comes from an unconstrained redesign branch that removed them. ")
            a += ("Computational candidate, not shown to bind. 83 aa de novo miniprotein. "
                  f"{nh} histidine(s). Ranked on worse-of-two-species interface-PAE margin, the "
                  "only instrument here with an external calibration.")
            row = dict(name=did, sequence=s, molecule_class="single_chain", rank=rank,
                       margin_worse_of_two=f"{WORSE[rank]:.3f}",
                       margin_human=f"{hu:.3f}", margin_mouse=f"{mo:.3f}",
                       seed_basis_human=sbh, seed_basis_mouse=sbm,
                       buried_his_count=nh,
                       esmfold2_lrms_A=c4[did]["esm_lrms"],
                       esmfold2_n_folds=c4[did]["n"],
                       chai1_lrms_A_1sample=c4[did]["chai_lrms"],
                       two_oracle_gate_1sample_WITHDRAWN=c4[did]["gate"],
                       prescreen_verdict=ps[did]["verdict"], assessment=a)
            if have_d8:
                row["chai1_lrms_A_median_5samples"] = d8[did]["med"]
                row["chai1_samples_in_gate_of_5"] = d8[did]["ingate"]
            w.writerow(row)
    n = sum(1 for _ in open(OUT)) - 1
    print(f"wrote {OUT}: {n} rows, {len(fields)} columns")
    print("  His counts:", {MARGINS[r][0]: sq[MARGINS[r][0]].count("H") for r in sorted(MARGINS)})


if __name__ == "__main__":
    main()
