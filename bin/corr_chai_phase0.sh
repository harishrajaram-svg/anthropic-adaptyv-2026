#!/usr/bin/env bash
# PHASE 0 of the CORR arm (PREREG-CORR-TWO-ORACLE-2026-10-11.md): measure Chai-1's per-fold
# cost. The ORIGINAL depth-arm prereg made this the precondition for continuing past round 3,
# and that condition was never checked -- so it is checked here before any round-4 fold.
#
# Two folds, SEQUENTIAL and separately timed: the first pays container start + model load
# (cold), the second is the warm rate. Both numbers matter, because modal_chai1.py takes ONE
# fasta per remote call, so every fold in a real round pays its own container start. That makes
# the cold number the honest per-fold cost of this wrapper as it stands.
#
# Absolute paths throughout: this script cd's into biomodals/, and a relative --out-dir landing
# in the wrong tree has already cost one arm's output in this project.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
IN="$ROOT/runs/corr-chai-p0-in"
OUT="$ROOT/runs/corr-chai-p0-out"
LOG="$ROOT/runs/corr_chai_p0_timing.tsv"
mkdir -p "$OUT" "$ROOT/runs/depth_logs"
[[ -s "$LOG" ]] || printf 'order\tdesign\twall_s\trc\tlog\n' > "$LOG"

cd "$ROOT/biomodals"
i=0
for f in "$IN"/*.faa; do
  i=$((i+1))
  did="$(basename "$f" .faa)"
  lg="$ROOT/runs/depth_logs/corr_p0_${did}.log"
  echo "[p0] fold $i/2  $did  -> $lg"
  t0=$(date +%s)
  set +e
  # One diffusion sample, seed 42 -- prereg amendment A1. The wrapper default is FIVE
  # samples, which would force a which-model-index rule and make score_round refuse the
  # directory outright. One sample mirrors the ESMFold2 arm's --num-diffusion-samples 1.
  GPU="${GPU:-A100}" TIMEOUT="${TIMEOUT:-30}" \
    modal run modal_chai1.py \
      --input-faa "$f" \
      --out-dir "$OUT" \
      --run-name "p0_$did" \
      --chai1-kwargs "{'num_diffn_samples': 1}" > "$lg" 2>&1
  rc=$?
  set -e
  t1=$(date +%s)
  printf '%d\t%s\t%d\t%d\t%s\n' "$i" "$did" "$((t1-t0))" "$rc" "$lg" >> "$LOG"
  echo "[p0] fold $i done in $((t1-t0))s rc=$rc"
done
echo "[p0] timing written to $LOG"
cat "$LOG"
