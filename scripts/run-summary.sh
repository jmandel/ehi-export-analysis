#!/usr/bin/env bash
# Extract structured JSON from a single vendor's analysis.md.
#
# Reads the TypeScript schema (abstraction/ehi-summary-schema.ts) and the
# vendor's analysis.md, then invokes an LLM to produce a conforming JSON file.
# The script is schema-agnostic — all field semantics live in the .ts comments.
#
# Usage:
#   ./scripts/run-summary.sh --analysis-dir <dir> [options]
#
# Options:
#   --analysis-dir  Path to abstraction/<vendor>--<product>/ directory (required)
#   --backend       LLM backend: copilot (default)
#   --model         Model override (default: claude-sonnet-4.5)
#   -h, --help      Show this message

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ANALYSIS_DIR=""
BACKEND="copilot"
MODEL=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --analysis-dir) ANALYSIS_DIR="$2"; shift 2 ;;
    --backend)      BACKEND="$2"; shift 2 ;;
    --model)        MODEL="$2"; shift 2 ;;
    -h|--help)
      sed -n '2,/^$/{ s/^# \?//; p }' "$0"
      exit 0
      ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

if [[ -z "$ANALYSIS_DIR" ]]; then
  echo "Missing required --analysis-dir argument."
  exit 1
fi

# Resolve to absolute path
ANALYSIS_DIR="$(cd "$ANALYSIS_DIR" && pwd)"

if [[ ! -f "$ANALYSIS_DIR/analysis.md" ]]; then
  echo "No analysis.md found in $ANALYSIS_DIR"
  exit 2
fi

SCHEMA_FILE="$ROOT_DIR/abstraction/ehi-summary-schema.ts"
if [[ ! -f "$SCHEMA_FILE" ]]; then
  echo "Schema file not found: $SCHEMA_FILE"
  exit 2
fi

# Set default model per backend — lighter model since this is extraction not analysis
if [[ -z "$MODEL" ]]; then
  case "$BACKEND" in
    copilot) MODEL="claude-sonnet-4.5" ;;
    codex)   MODEL="gpt-5.1-codex" ;;
    *)       echo "Unknown backend: $BACKEND"; exit 1 ;;
  esac
fi

# Resolve CLI binary
case "$BACKEND" in
  copilot)
    CLI_BIN="${COPILOT_BIN:-$(command -v copilot 2>/dev/null || true)}"
    if [[ -z "$CLI_BIN" ]]; then
      echo "copilot binary not found. Set COPILOT_BIN or install copilot."
      exit 3
    fi
    ;;
  codex)
    CLI_BIN="${CODEX_BIN:-$(command -v codex 2>/dev/null || true)}"
    if [[ -z "$CLI_BIN" ]]; then
      echo "codex binary not found. Set CODEX_BIN or install codex."
      exit 3
    fi
    ;;
esac

# Derive vendor slug from directory name
VENDOR_SLUG=$(basename "$ANALYSIS_DIR")
OUTPUT_FILE="$ANALYSIS_DIR/summary.json"

# Build the prompt
SCHEMA_CONTENT=$(cat "$SCHEMA_FILE")
ANALYSIS_CONTENT=$(cat "$ANALYSIS_DIR/analysis.md")

PROMPT="You are extracting structured data from an EHI export analysis document.

## Your task

Read the TypeScript interface below. It defines the exact JSON structure you must produce.
Every field has detailed JSDoc comments explaining how to derive its value from the analysis.
Follow those instructions precisely.

Read the analysis document below. Extract the required data and write a single JSON file
to: \`$OUTPUT_FILE\`

The JSON must conform to the TypeScript interface. Use the vendor slug \`$VENDOR_SLUG\` for
the vendor_slug field.

## TypeScript Schema

\`\`\`typescript
$SCHEMA_CONTENT
\`\`\`

## Analysis Document

$ANALYSIS_CONTENT

## Output instructions

1. Write ONLY the JSON file to \`$OUTPUT_FILE\`. Do not create any other files.
2. The JSON must be valid, properly formatted, and match the TypeScript interface exactly.
3. Do not include any fields not in the interface.
4. Do not wrap the JSON in markdown code fences — write raw JSON to the file.
5. If the analysis does not contain enough information to confidently score a field,
   use your best judgment based on what IS available. Never leave a field null."

echo "=== EHI Summary Extraction ==="
echo "Analysis: $ANALYSIS_DIR"
echo "Schema:   $SCHEMA_FILE"
echo "Output:   $OUTPUT_FILE"
echo "Backend:  $BACKEND ($MODEL)"
echo ""

set +e
case "$BACKEND" in
  copilot)
    "$CLI_BIN" \
      --yolo \
      --model "$MODEL" \
      --add-dir "$ROOT_DIR" \
      -p "$PROMPT"
    ;;
  codex)
    "$CLI_BIN" exec \
      --full-auto \
      --sandbox danger-full-access \
      --model "$MODEL" \
      --cd "$ROOT_DIR" \
      - <<< "$PROMPT"
    ;;
esac
cli_exit_code=$?
set -e

if [[ $cli_exit_code -ne 0 ]]; then
  echo "$BACKEND exited with code $cli_exit_code."
  exit "$cli_exit_code"
fi

# Verify output
if [[ ! -f "$OUTPUT_FILE" ]]; then
  echo "WARNING: summary.json was not created at $OUTPUT_FILE"
  exit 7
fi

# Validate JSON
if ! jq empty "$OUTPUT_FILE" 2>/dev/null; then
  echo "WARNING: summary.json is not valid JSON"
  exit 8
fi

echo ""
echo "=== Done ==="
echo "Summary: $OUTPUT_FILE"
jq . "$OUTPUT_FILE"
