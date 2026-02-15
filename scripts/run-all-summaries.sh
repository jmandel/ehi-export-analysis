#!/usr/bin/env bash
# Run JSON summary extraction across all completed analyses.
#
# Finds every abstraction/<vendor>--<product>/ directory that has an
# analysis.md and runs run-summary.sh to produce summary.json.
# Skips directories that already have summary.json (default).
#
# Usage:
#   ./scripts/run-all-summaries.sh [options]
#
# Options:
#   -j, --jobs N      Parallel jobs (default: 1)
#   --force           Remove existing summary.json and re-run
#   --dry-run         Print commands without executing
#   --backend <b>     LLM backend (default: copilot)
#   --model <m>       Model override
#   --filter <glob>   Only process dirs matching glob (e.g. "aarista*")

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
JOBS=1
FORCE=false
DRY_RUN=false
BACKEND_ARG=""
MODEL_ARG=""
FILTER=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    -j|--jobs)     JOBS="$2"; shift 2 ;;
    --force)       FORCE=true; shift ;;
    --dry-run)     DRY_RUN=true; shift ;;
    --backend)     BACKEND_ARG="--backend $2"; shift 2 ;;
    --model)       MODEL_ARG="--model $2"; shift 2 ;;
    --filter)      FILTER="$2"; shift 2 ;;
    -h|--help)
      sed -n '2,/^$/{ s/^# \?//; p }' "$0"
      exit 0
      ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

commands=()
total=0
skipped=0
forced=0

for analysis_dir in "$ROOT_DIR"/abstraction/*/; do
  dir_name=$(basename "$analysis_dir")

  # Only process vendor--product dirs (contain --)
  [[ "$dir_name" == *"--"* ]] || continue

  # Must have analysis.md
  [[ -f "$analysis_dir/analysis.md" ]] || continue

  # Apply filter if set
  if [[ -n "$FILTER" ]]; then
    # shellcheck disable=SC2254
    case "$dir_name" in $FILTER) ;; *) continue ;; esac
  fi

  total=$((total + 1))

  if [[ -f "$analysis_dir/summary.json" ]]; then
    if [[ "$FORCE" == true ]]; then
      forced=$((forced + 1))
      if [[ "$DRY_RUN" == false ]]; then
        rm -f "$analysis_dir/summary.json"
      fi
    else
      skipped=$((skipped + 1))
      continue
    fi
  fi

  commands+=("./scripts/run-summary.sh --analysis-dir \"$analysis_dir\" $BACKEND_ARG $MODEL_ARG")
done

queued=${#commands[@]}
echo "=== EHI Summary Extraction Batch ===" >&2
echo "Total analyses: $total" >&2
echo "Skipped (done): $skipped" >&2
[[ "$FORCE" == true ]] && echo "Forced recompute: $forced" >&2
echo "Queued: $queued" >&2
echo "Parallelism: $JOBS" >&2
echo "" >&2

if [[ $queued -eq 0 ]]; then
  echo "Nothing to do." >&2
  exit 0
fi

if [[ "$DRY_RUN" == true ]]; then
  printf '%s\n' "${commands[@]}"
  exit 0
fi

# Run with controlled parallelism
LOG_DIR=$(mktemp -d)
trap 'rm -rf "$LOG_DIR"' EXIT

succeeded=0
failed=0
fail_list=()

run_one() {
  local idx=$1 cmd=$2 stream=${3:-false}
  local logfile="$LOG_DIR/job-$idx.log"
  echo "[$(date +%H:%M:%S)] START ($((idx+1))/$queued): $cmd" >&2
  if [[ "$stream" == true ]]; then
    if eval "$cmd" 2>&1 | tee "$logfile"; then
      echo "[$(date +%H:%M:%S)] DONE  ($((idx+1))/$queued): $cmd" >&2
      return 0
    else
      echo "[$(date +%H:%M:%S)] FAIL  ($((idx+1))/$queued): $cmd" >&2
      return 1
    fi
  elif eval "$cmd" > "$logfile" 2>&1; then
    echo "[$(date +%H:%M:%S)] DONE  ($((idx+1))/$queued): $cmd" >&2
    return 0
  else
    echo "[$(date +%H:%M:%S)] FAIL  ($((idx+1))/$queued): $cmd" >&2
    tail -5 "$logfile" >&2
    return 1
  fi
}

if [[ "$JOBS" -eq 1 ]]; then
  for i in "${!commands[@]}"; do
    if run_one "$i" "${commands[$i]}" true; then
      succeeded=$((succeeded + 1))
    else
      failed=$((failed + 1))
      fail_list+=("${commands[$i]}")
    fi
  done
else
  # Parallel execution via background jobs with a semaphore
  fifo="$LOG_DIR/fifo"
  mkfifo "$fifo"
  exec 3<>"$fifo"
  for ((t=0; t<JOBS; t++)); do echo >&3; done

  results_file="$LOG_DIR/results"
  touch "$results_file"

  for i in "${!commands[@]}"; do
    read -r <&3
    (
      if run_one "$i" "${commands[$i]}"; then
        echo "OK" >> "$results_file"
      else
        echo "FAIL ${commands[$i]}" >> "$results_file"
      fi
      echo >&3
    ) &
  done
  wait

  exec 3>&-
  succeeded=$(grep -c '^OK$' "$results_file" 2>/dev/null || true)
  failed=$(grep -c '^FAIL' "$results_file" 2>/dev/null || true)
  while IFS= read -r line; do
    fail_list+=("${line#FAIL }")
  done < <(grep '^FAIL ' "$results_file" 2>/dev/null || true)
fi

echo "" >&2
echo "=== Batch Complete ===" >&2
echo "Succeeded: $succeeded" >&2
echo "Failed:    $failed" >&2

if [[ $failed -gt 0 ]]; then
  echo "" >&2
  echo "Failed commands:" >&2
  printf '  %s\n' "${fail_list[@]}" >&2
  exit 1
fi
