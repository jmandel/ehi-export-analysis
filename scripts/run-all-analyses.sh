#!/usr/bin/env bash
# Run EHI export analyses across all collected results.
#
# Enumerates every product across all results/<slug>/ directories and
# runs run-analysis.sh for each. Supports parallelism, skip-done, and
# force-clean recompute.
#
# Usage:
#   ./scripts/run-all-analyses.sh [options]
#
# Options:
#   -j, --jobs N      Parallel jobs (default: 1)
#   --force           Remove existing output and re-run (default: skip done)
#   --dry-run         Print commands without executing
#   --backend <b>     LLM backend (default: copilot)
#   --model <m>       Model override
#   --filter <glob>   Only process results dirs matching glob (e.g. "epic*")

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

# Build the list of commands
commands=()
total=0
skipped=0
forced=0

for results_dir in "$ROOT_DIR"/results/*/; do
  slug=$(basename "$results_dir")

  # Only process family-scoped dirs (contain --)
  [[ "$slug" == *"--"* ]] || continue

  # Must have chpl-metadata and downloads
  [[ -f "$results_dir/chpl-metadata.json" ]] || continue

  # Apply filter if set
  if [[ -n "$FILTER" ]]; then
    # shellcheck disable=SC2254
    case "$slug" in $FILTER) ;; *) continue ;; esac
  fi

  output_dir="$ROOT_DIR/abstraction/$slug"
  total=$((total + 1))

  if [[ -f "$output_dir/analysis.md" ]]; then
    if [[ "$FORCE" == true ]]; then
      forced=$((forced + 1))
      if [[ "$DRY_RUN" == false ]]; then
        rm -rf "$output_dir"
      fi
    else
      skipped=$((skipped + 1))
      continue
    fi
  fi

  commands+=("./scripts/run-analysis.sh --dir \"$slug\" $BACKEND_ARG $MODEL_ARG")
done

queued=${#commands[@]}
echo "=== EHI Export Analysis Batch ===" >&2
echo "Total products: $total" >&2
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
  # Extract slug from command for persistent error log
  local slug
  slug=$(echo "$cmd" | grep -oP '(?<=--dir ")[^"]+')
  echo "[$(date +%H:%M:%S)] START ($((idx+1))/$queued): $cmd" >&2
  if [[ "$stream" == true ]]; then
    if eval "$cmd" 2>&1 | tee "$logfile"; then
      echo "[$(date +%H:%M:%S)] DONE  ($((idx+1))/$queued): $cmd" >&2
      return 0
    else
      echo "[$(date +%H:%M:%S)] FAIL  ($((idx+1))/$queued): $cmd" >&2
      if [[ -n "$slug" ]]; then
        mkdir -p "$ROOT_DIR/abstraction/$slug"
        cp "$logfile" "$ROOT_DIR/abstraction/$slug/analysis-error.log"
        echo "  Error log: abstraction/$slug/analysis-error.log" >&2
      fi
      return 1
    fi
  elif eval "$cmd" > "$logfile" 2>&1; then
    echo "[$(date +%H:%M:%S)] DONE  ($((idx+1))/$queued): $cmd" >&2
    return 0
  else
    echo "[$(date +%H:%M:%S)] FAIL  ($((idx+1))/$queued): $cmd" >&2
    tail -5 "$logfile" >&2
    if [[ -n "$slug" ]]; then
      mkdir -p "$ROOT_DIR/abstraction/$slug"
      cp "$logfile" "$ROOT_DIR/abstraction/$slug/analysis-error.log"
      echo "  Error log: abstraction/$slug/analysis-error.log" >&2
    fi
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
  # Seed the semaphore with $JOBS tokens
  for ((t=0; t<JOBS; t++)); do echo >&3; done 3>"$fifo" 3<"$fifo" &
  exec 3<>"$fifo"
  for ((t=0; t<JOBS; t++)); do echo >&3; done

  results_file="$LOG_DIR/results"
  touch "$results_file"

  for i in "${!commands[@]}"; do
    read -r <&3  # acquire semaphore slot
    (
      if run_one "$i" "${commands[$i]}"; then
        echo "OK" >> "$results_file"
      else
        echo "FAIL ${commands[$i]}" >> "$results_file"
      fi
      echo >&3  # release semaphore slot
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
