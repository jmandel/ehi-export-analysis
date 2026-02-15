#!/usr/bin/env bash
# EHI Export Documentation Collection Loop
#
# Iterates over targets.json, running one agent per URL per phase.
# Each agent call blocks until the agent finishes.
#
# Usage:
#   ./wiggum/loop.sh --targets work/phases/phase-1-comprehensive-ehrs.json --phase both
#   ./wiggum/loop.sh --phase 1               # run phase 1 (research)
#   ./wiggum/loop.sh --phase 2 --resume      # run phase 2, skip completed
#   ./wiggum/loop.sh --phase both             # run phase 1 then 2 per URL
#   ./wiggum/loop.sh --phase 1 --reverse     # iterate backwards
#   ./wiggum/loop.sh --phase 1 --index 42    # start from target index 42
#   ./wiggum/loop.sh --phase 1 --only 42     # run only target index 42
set -euo pipefail

export PATH="$HOME/.local/bin:$HOME/.bun/bin:$PATH"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOOP_LOG="$ROOT/wiggum/logs/loop-exit.log"
mkdir -p "$(dirname "$LOOP_LOG")"

cleanup() {
  local code=$?
  local ts
  ts=$(date '+%Y-%m-%d %H:%M:%S')
  if (( code != 0 )); then
    echo "[$ts] Loop exited with code $code (line ${BASH_LINENO[0]:-?}, command: ${BASH_COMMAND:-?})" | tee -a "$LOOP_LOG" >&2
  else
    echo "[$ts] Loop finished normally" | tee -a "$LOOP_LOG" >&2
  fi
}
trap cleanup EXIT
CONFIG_DIR="$ROOT/wiggum"
TARGETS="${TARGETS:-$ROOT/work/targets.json}"
RESULTS_DIR="$ROOT/results"

# LLM backend: "claude", "shelley" (default), or "gemini"
LLM_BACKEND="${LLM_BACKEND:-shelley}"

# Claude settings
CLAUDE_MODEL="${CLAUDE_MODEL:-opus}"

# Shelley settings — always Opus 4.6
SHELLEY_PROMPT="$CONFIG_DIR/shelley-prompt.ts"
SHELLEY_SERVER="${SHELLEY_SERVER:-http://localhost:9999}"
SHELLEY_MODEL="${SHELLEY_MODEL:-claude-opus-4.6}"
SHELLEY_USER="${SHELLEY_USER:-wiggum}"

# Gemini settings
GEMINI_MODEL="${GEMINI_MODEL:-gemini-3-pro-preview}"

# When set to any non-empty value, prompts discourage subagent use
DISCOURAGE_SUBAGENTS="${DISCOURAGE_SUBAGENTS:-}"

# Phase configuration
declare -A PHASE_PROMPT PHASE_MARKER PHASE_NAME
PHASE_PROMPT[1]="$ROOT/wiggum/prompts/1-research.md"
PHASE_MARKER[1]="sources.json"
PHASE_NAME[1]="research"
PHASE_PROMPT[2]="$ROOT/wiggum/prompts/2-download.md"
PHASE_MARKER[2]="files.json"
PHASE_NAME[2]="download"

# Run LLM — blocks until agent finishes.
# Prompt comes via stdin. First arg is working directory.
run_llm() {
  local cwd="$1"
  case "$LLM_BACKEND" in
    claude)
      cd "$cwd"
      claude -p --dangerously-skip-permissions \
        --model "$CLAUDE_MODEL" \
        --output-format stream-json
      ;;
    shelley)
      bun run "$SHELLEY_PROMPT" \
        -server "$SHELLEY_SERVER" \
        -cwd "$cwd" \
        -user "$SHELLEY_USER" \
        -model "$SHELLEY_MODEL" \
        -v
      ;;
    gemini)
      cd "$cwd"
      gemini -p "" --yolo --output-format text --model "$GEMINI_MODEL"
      ;;
    *)
      echo "Unknown LLM_BACKEND: $LLM_BACKEND" >&2
      return 1
      ;;
  esac
}

# Parse args
RESUME=false
REVERSE=false
START_INDEX=0
ONLY_INDEX=""
PHASE=""
while [[ $# -gt 0 ]]; do
  case $1 in
    --targets) TARGETS="$2"; shift 2 ;;
    --phase) PHASE="$2"; shift 2 ;;
    --resume) RESUME=true; shift ;;
    --reverse) REVERSE=true; shift ;;
    --index) START_INDEX="$2"; shift 2 ;;
    --only) ONLY_INDEX="$2"; shift 2 ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

if [[ -z "$PHASE" ]]; then
  echo "Error: --phase N is required (1=research, 2=download, both)"
  exit 1
fi

# Determine which phases to run
if [[ "$PHASE" == "both" ]]; then
  PHASES=(1 2)
  PHASE_LABEL="both (research+download)"
  COMPLETION_MARKER="${PHASE_MARKER[2]}"
else
  if [[ -z "${PHASE_PROMPT[$PHASE]:-}" ]]; then
    echo "Error: unknown phase $PHASE"
    exit 1
  fi
  PHASES=("$PHASE")
  PHASE_LABEL="${PHASE_NAME[$PHASE]}"
  COMPLETION_MARKER="${PHASE_MARKER[$PHASE]}"
fi

mkdir -p "$RESULTS_DIR"

if [[ ! -f "$TARGETS" ]]; then
  echo "No targets.json found. Run 00-fetch-export-urls.sh first."
  exit 1
fi

TOTAL=$(jq 'length' "$TARGETS")
echo "=== EHI Export Documentation Collection ==="
echo "Phase:   $PHASE ($PHASE_LABEL)"
case "$LLM_BACKEND" in
  claude)  _model_label="claude-${CLAUDE_MODEL}" ;;
  shelley) _model_label="$SHELLEY_MODEL" ;;
  gemini)  _model_label="$GEMINI_MODEL" ;;
  *)       _model_label="$LLM_BACKEND" ;;
esac
echo "Backend: $LLM_BACKEND ($_model_label)"
echo "Targets: $TARGETS ($TOTAL URLs)"
echo "Results: $RESULTS_DIR/"
echo ""

slugify() {
  echo "$1" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]\+/-/g' | sed 's/^-\|-$//g' | cut -c1-60
}

COMPLETED=0
FAILED=0
SKIPPED=0

commit_result() {
  local slug="$1"
  cd "$ROOT"
  git add "$RESULTS_DIR/$slug/" 2>/dev/null || true
  git diff --cached --quiet 2>/dev/null && return
  git commit -m "$slug: $PHASE_LABEL complete" \
    --author="wiggum <wiggum@ehi-export-analysis>" 2>/dev/null || true
  git push 2>/dev/null || true
}

run_target() {
  local idx="$1"
  local target
  target=$(jq -c ".[${idx}]" "$TARGETS")

  local url developers products chpl_ids slug output_dir
  url=$(echo "$target" | jq -r '.url')
  developers=$(echo "$target" | jq -r '.developers | join(", ")')
  products=$(echo "$target" | jq -r '.products | join(", ")')
  chpl_ids=$(echo "$target" | jq -r '.chpl_ids | map(tostring) | join(", ")')
  slug=$(slugify "$(echo "$target" | jq -r '.developers[0]')")

  local dev_count
  dev_count=$(echo "$target" | jq '.developers | length')
  if (( dev_count > 1 )); then
    slug="${slug}-and-others-${idx}"
  fi

  output_dir="$RESULTS_DIR/$slug"

  # Skip if fully done
  if [[ "$RESUME" == true && -f "$output_dir/$COMPLETION_MARKER" ]]; then
    echo "[$idx/$TOTAL] SKIP $slug"
    SKIPPED=$((SKIPPED + 1))
    return 0
  fi

  mkdir -p "$output_dir/downloads"

  # Copy CHPL metadata, filtered to only products in this phase target's chpl_ids
  local orig_idx
  orig_idx=$(echo "$target" | jq -r '.original_index // empty')
  local meta_idx="${orig_idx:-$idx}"
  local meta_file="$ROOT/work/target-metadata/$(printf '%04d' "$meta_idx").json"
  if [[ -f "$meta_file" ]]; then
    local phase_ids
    phase_ids=$(echo "$target" | jq -c '.chpl_ids')
    jq --argjson ids "$phase_ids" '.products |= [.[] | select(.chpl_id as $id | $ids | index($id))]' \
      "$meta_file" > "$output_dir/chpl-metadata.json"
    # Skip if no products matched (chpl_ids not in metadata)
    local product_count
    product_count=$(jq '.products | length' "$output_dir/chpl-metadata.json")
    if (( product_count == 0 )); then
      echo "  SKIP: no matching products in metadata"
      SKIPPED=$((SKIPPED + 1))
      rm -rf "$output_dir"
      return 0
    fi
  fi

  echo "[$idx/$TOTAL] $slug"
  echo "  URL: $url"
  echo "  Dev: $developers"

  local target_failed=false

  for phase in "${PHASES[@]}"; do
    local marker="${PHASE_MARKER[$phase]}"
    local label="${PHASE_NAME[$phase]}"
    local template="${PHASE_PROMPT[$phase]}"

    # Skip phase if already done
    if [[ -f "$output_dir/$marker" ]]; then
      echo "  phase $phase ($label): already done"
      continue
    fi

    echo "  phase $phase ($label): running..."

    # Render template: simple vars via sed, then file includes via awk
    local rendered
    rendered=$(sed \
      -e "s|{{URL}}|${url}|g" \
      -e "s|{{DEVELOPERS}}|${developers}|g" \
      -e "s|{{PRODUCTS}}|${products}|g" \
      -e "s|{{CHPL_IDS}}|${chpl_ids}|g" \
      -e "s|{{OUTPUT_DIR}}|${output_dir}|g" \
      "$template")

    # Inline file includes: {{FILE_REF}} → contents of prompts/file-ref.md
    local prompt
    prompt=$(echo "$rendered" | awk -v dir="$CONFIG_DIR/prompts" '{
      if (match($0, /\{\{([A-Z_]+)\}\}/, m)) {
        key = m[1]
        gsub(/_/, "-", key)
        cmd = "tr \"[:upper:]\" \"[:lower:]\" <<< \"" key "\""
        cmd | getline lower_key
        close(cmd)
        inc = dir "/" lower_key ".md"
        if ((getline line < inc) > 0) {
          print line
          while ((getline line < inc) > 0) print line
          close(inc)
        } else {
          print  # no file found, keep original line
        }
      } else {
        print
      }
    }')

    if [[ -n "$DISCOURAGE_SUBAGENTS" ]]; then
      prompt+=$'\n\n> **Note:** Avoid using subagents for this task. Work sequentially in a single conversation.\n'
    fi

    local log_file="$output_dir/phase${phase}-log.txt"

    # Run agent — blocks until it finishes or hits timeout.
    # A stale-output watchdog kills the agent if the log file hasn't
    # been written to in STALE_TIMEOUT seconds (default 300 = 5 min).
    local t0=$SECONDS
    export -f run_llm
    export LLM_BACKEND CLAUDE_MODEL SHELLEY_PROMPT SHELLEY_SERVER SHELLEY_MODEL SHELLEY_USER GEMINI_MODEL

    # Start agent in background, capture its PID.
    # Output goes to both the per-target log and stdout (for /tmp/wiggum-loop.log).
    timeout "${TIMEOUT:-1800}" bash -c 'run_llm "$1" <<< "$2"' _ "$ROOT" "$prompt" \
      2>&1 | tee "$log_file" &
    local agent_pid=$!

    # Stale-output watchdog: kill agent if log unchanged for STALE_TIMEOUT
    local stale_timeout="${STALE_TIMEOUT:-300}"
    (
      while kill -0 "$agent_pid" 2>/dev/null; do
        sleep 30
        if [[ -f "$log_file" ]]; then
          local age
          age=$(( $(date +%s) - $(stat -c %Y "$log_file") ))
          if (( age > stale_timeout )); then
            echo "  watchdog: log stale for ${age}s, killing agent (PID $agent_pid)" >&2
            kill "$agent_pid" 2>/dev/null || true
            break
          fi
        fi
      done
    ) &
    local watchdog_pid=$!

    # Wait for agent to finish
    wait "$agent_pid" 2>/dev/null
    local exit_code=$?
    kill "$watchdog_pid" 2>/dev/null || true
    wait "$watchdog_pid" 2>/dev/null || true

    if (( exit_code == 0 )); then
      echo "  phase $phase ($label): done ($(( SECONDS - t0 ))s)"
    elif (( exit_code == 124 )); then
      echo "  ⏰ phase $phase ($label): timed out after $(( ${TIMEOUT:-1800} / 60 ))m"
      target_failed=true
      break
    else
      echo "  phase $phase ($label): FAILED (exit $exit_code, $(( SECONDS - t0 ))s)"
      target_failed=true
      break
    fi
  done

  if [[ "$target_failed" == true ]]; then
    FAILED=$((FAILED + 1))
  else
    COMPLETED=$((COMPLETED + 1))
    commit_result "$slug"
  fi
}

# Main loop
if [[ -n "$ONLY_INDEX" ]]; then
  run_target "$ONLY_INDEX"
else
  if [[ "$REVERSE" == true ]]; then
    for (( i=TOTAL-1; i>=START_INDEX; i-- )); do
      run_target "$i"
    done
  else
    for (( i=START_INDEX; i<TOTAL; i++ )); do
      run_target "$i"
    done
  fi
fi

echo ""
echo "=== Done ==="
echo "Completed: $COMPLETED | Failed: $FAILED | Skipped: $SKIPPED"
