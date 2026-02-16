#!/usr/bin/env bash
# Run EHI export analysis on a single vendor's collected results.
#
# Renders the analysis prompt template, invokes an LLM agent, and
# expects it to produce analysis.md + analysis/ artifacts.
#
# Usage:
#   ./scripts/run-analysis.sh --dir <results-slug> [--output-dir <dir>] [--backend <backend>] [--model <model>]

set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  ./scripts/run-analysis.sh --dir <results-dir-name> [options]

Options:
  --dir        Directory name under results/ (required, e.g. "vendor--product")
  --output-dir Output directory (default: abstraction/<dir>)
  --backend    LLM backend: copilot, codex (default: copilot)
  --model      Model override (default: claude-opus-4.6-fast for copilot)
  -h, --help   Show this message

Examples:
  ./scripts/run-analysis.sh --dir aarista-technology-llc--aarista
  ./scripts/run-analysis.sh --dir practice-fusion--practice-fusion-ehr --backend codex
EOF
}

TARGET_DIRNAME=""
OUTPUT_DIR=""
BACKEND="copilot"
MODEL=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dir)        TARGET_DIRNAME="$2"; shift 2 ;;
    --output-dir) OUTPUT_DIR="$2"; shift 2 ;;
    --backend)    BACKEND="$2"; shift 2 ;;
    --model)      MODEL="$2"; shift 2 ;;
    -h|--help)    usage; exit 0 ;;
    *)            echo "Unknown arg: $1"; usage; exit 1 ;;
  esac
done

if [[ -z "$TARGET_DIRNAME" ]]; then
  echo "Missing required --dir argument."
  usage
  exit 1
fi

# Set default model per backend
if [[ -z "$MODEL" ]]; then
  case "$BACKEND" in
    copilot) MODEL="claude-opus-4.6-fast" ;;
    codex)   MODEL="gpt-5.3-codex-spark" ;;
    *)       echo "Unknown backend: $BACKEND"; exit 1 ;;
  esac
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RESULTS_DIR="$ROOT_DIR/results/$TARGET_DIRNAME"

if [[ ! -d "$RESULTS_DIR" ]]; then
  echo "Results folder not found: $RESULTS_DIR"
  exit 2
fi

# Derive product name from chpl-metadata
PRODUCT_NAME=""
if [[ -f "$RESULTS_DIR/chpl-metadata.json" ]]; then
  PRODUCT_NAME=$(jq -r '.products[0].product_name // empty' "$RESULTS_DIR/chpl-metadata.json" 2>/dev/null)
fi
if [[ -z "$PRODUCT_NAME" ]]; then
  PRODUCT_NAME="$TARGET_DIRNAME"
fi

# Output dir mirrors results dir name: abstraction/<same-slug>
if [[ -z "$OUTPUT_DIR" ]]; then
  OUTPUT_DIR="$ROOT_DIR/abstraction/$TARGET_DIRNAME"
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

mkdir -p "$OUTPUT_DIR"

# Symlink results artifacts into the output dir so the agent can use ./downloads,
# ./product-research.md, etc. instead of navigating ../../results/<slug>/
for item in "$RESULTS_DIR"/downloads "$RESULTS_DIR"/*.md "$RESULTS_DIR"/*.json; do
  [ -e "$item" ] || continue
  linkname="$OUTPUT_DIR/$(basename "$item")"
  [ -e "$linkname" ] || ln -s "$item" "$linkname"
done

# Write metadata.json for traceability — chpl-metadata is already family-filtered
jq -n \
  --arg dir_slug "$TARGET_DIRNAME" \
  --arg product_name "$PRODUCT_NAME" \
  --arg results_dir "results/$TARGET_DIRNAME" \
  --arg created_at "$(date -Iseconds)" \
  --arg ehi_documentation_url "$(jq -r '.url // empty' "$RESULTS_DIR/chpl-metadata.json" 2>/dev/null || true)" \
  --argjson products "$(jq '.products // []' "$RESULTS_DIR/chpl-metadata.json" 2>/dev/null || echo '[]')" \
  --argjson developer "$(jq '.developer // {}' "$RESULTS_DIR/chpl-metadata.json" 2>/dev/null || echo '{}')" \
  '{
    dir_slug: $dir_slug,
    product_name: $product_name,
    results_dir: $results_dir,
    created_at: $created_at,
    ehi_documentation_url: $ehi_documentation_url,
    developer: $developer,
    certified_products: $products
  }' > "$OUTPUT_DIR/metadata.json"

# Render the prompt template
PROMPT_FILE=$(mktemp)
trap 'rm -f "$PROMPT_FILE"' EXIT

bun -e '
const fs = require("fs");
const [tmplPath, ehiPath, outPath, resultsDir, outputDir, productName] = process.argv.slice(1);
let tmpl = fs.readFileSync(tmplPath, "utf8");
const vars = {
  RESULTS_DIR: resultsDir,
  OUTPUT_DIR: outputDir,
  PRODUCT_NAME: productName,
  EHI_SCOPE_REFERENCE: fs.readFileSync(ehiPath, "utf8"),
};
tmpl = tmpl.replace(/\{\{(\w+)\}\}/g, (_, k) => vars[k] || "{{" + k + "}}");
fs.writeFileSync(outPath, tmpl);
' "$ROOT_DIR/abstraction/abstraction-prompt.md" \
  "$ROOT_DIR/wiggum/prompts/ehi-scope-reference.md" \
  "$PROMPT_FILE" \
  "$RESULTS_DIR" \
  "$OUTPUT_DIR" \
  "$PRODUCT_NAME"

echo "=== EHI Export Analysis ==="
echo "Target:  $TARGET_DIRNAME"
echo "Product: $PRODUCT_NAME"
echo "Results: $RESULTS_DIR"
echo "Output:  $OUTPUT_DIR"
echo "Backend: $BACKEND ($MODEL)"
echo "Prompt:  $(wc -c < "$PROMPT_FILE") bytes"
echo ""

set +e
case "$BACKEND" in
  copilot)
    cd "$OUTPUT_DIR"
    "$CLI_BIN" \
      --yolo \
      --model "$MODEL" \
      -p "$(cat "$PROMPT_FILE")"
    ;;
  codex)
    cd "$OUTPUT_DIR"
    "$CLI_BIN" exec \
      --full-auto \
      --sandbox danger-full-access \
      --model "$MODEL" \
      - < "$PROMPT_FILE"
    ;;
esac
cli_exit_code=$?
set -e

if [[ $cli_exit_code -ne 0 ]]; then
  echo "$BACKEND exited with code $cli_exit_code."
  exit "$cli_exit_code"
fi

# Verify output exists
if [[ ! -f "$OUTPUT_DIR/analysis.md" ]]; then
  echo "WARNING: analysis.md was not created at $OUTPUT_DIR/analysis.md"
  echo "The agent may have written to a different path."
  exit 7
fi

echo ""
echo "=== Done ==="
echo "Analysis: $OUTPUT_DIR/analysis.md"
if [[ -d "$OUTPUT_DIR/analysis" ]]; then
  echo "Scripts/data: $OUTPUT_DIR/analysis/ ($(find "$OUTPUT_DIR/analysis" -type f | wc -l) files)"
fi
