#!/usr/bin/env bash
# Run Phase 1 (product research) for a single vendor's results directory.
#
# Renders the research prompt template, invokes an LLM agent, and
# expects it to produce product-research.md + sources.json.
#
# Usage:
#   ./scripts/run-research.sh --dir <results-dir-name> [--backend <backend>] [--model <model>]

set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  ./scripts/run-research.sh --dir <results-dir-name> [options]

Options:
  --dir        Directory name under results/ (required, e.g. "vendor--product")
  --backend    LLM backend: copilot, codex (default: copilot)
  --model      Model override (default: claude-opus-4.6-fast for copilot)
  --prompt     Custom prompt file (default: wiggum/prompts/1-research.md)
  -h, --help   Show this message

Examples:
  ./scripts/run-research.sh --dir ezemrx-inc--ezemrx
  ./scripts/run-research.sh --dir epic-systems-corporation--epic-ehr --backend copilot
EOF
}

TARGET_DIRNAME=""
BACKEND="copilot"
MODEL=""
CUSTOM_PROMPT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dir)        TARGET_DIRNAME="$2"; shift 2 ;;
    --backend)    BACKEND="$2"; shift 2 ;;
    --model)      MODEL="$2"; shift 2 ;;
    --prompt)     CUSTOM_PROMPT="$2"; shift 2 ;;
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
OUTPUT_DIR="$ROOT_DIR/results/$TARGET_DIRNAME"

if [[ ! -d "$OUTPUT_DIR" ]]; then
  echo "Results folder not found: $OUTPUT_DIR"
  echo "Create it first with: mkdir -p results/$TARGET_DIRNAME/downloads"
  exit 2
fi

if [[ ! -f "$OUTPUT_DIR/chpl-metadata.json" ]]; then
  echo "chpl-metadata.json not found in $OUTPUT_DIR"
  echo "This file is required for research. Run build-metadata.ts first or copy from work/target-metadata/."
  exit 2
fi

# Extract template variables from chpl-metadata.json
URL=$(jq -r '.url // empty' "$OUTPUT_DIR/chpl-metadata.json" 2>/dev/null || true)
DEVELOPERS=$(jq -r '[.developer.name // empty] | join(", ")' "$OUTPUT_DIR/chpl-metadata.json" 2>/dev/null || true)
PRODUCTS=$(jq -r '[.products[].product_name // empty] | join(", ")' "$OUTPUT_DIR/chpl-metadata.json" 2>/dev/null || true)
CHPL_IDS=$(jq -r '[.products[].chpl_id // empty] | map(tostring) | join(", ")' "$OUTPUT_DIR/chpl-metadata.json" 2>/dev/null || true)

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

# Render the prompt template
PROMPT_TEMPLATE="${CUSTOM_PROMPT:-$ROOT_DIR/wiggum/prompts/1-research.md}"
PROMPT_FILE=$(mktemp)
trap 'rm -f "$PROMPT_FILE"' EXIT

bun -e '
const fs = require("fs");
const path = require("path");
const [tmplPath, outPath, url, developers, products, chplIds, outputDir, promptsDir] = process.argv.slice(1);
let tmpl = fs.readFileSync(tmplPath, "utf8");
const vars = {
  URL: url,
  DEVELOPERS: developers,
  PRODUCTS: products,
  CHPL_IDS: chplIds,
  OUTPUT_DIR: outputDir,
};
// Simple variable substitution
for (const [key, value] of Object.entries(vars)) {
  tmpl = tmpl.replaceAll("{{" + key + "}}", value);
}
// File includes for remaining {{PLACEHOLDERS}}
tmpl = tmpl.replace(/\{\{([A-Z_]+)\}\}/g, (match, key) => {
  const filename = key.toLowerCase().replace(/_/g, "-") + ".md";
  const filepath = path.join(promptsDir, filename);
  try { return fs.readFileSync(filepath, "utf8"); } catch { return match; }
});
fs.writeFileSync(outPath, tmpl);
' "$PROMPT_TEMPLATE" \
  "$PROMPT_FILE" \
  "$URL" \
  "$DEVELOPERS" \
  "$PRODUCTS" \
  "$CHPL_IDS" \
  "$OUTPUT_DIR" \
  "$ROOT_DIR/wiggum/prompts"

echo "=== Phase 1: Product Research ==="
echo "Target:     $TARGET_DIRNAME"
echo "Developer:  $DEVELOPERS"
echo "Products:   $PRODUCTS"
echo "Output:     $OUTPUT_DIR"
echo "Backend:    $BACKEND ($MODEL)"
echo "Prompt:     $(wc -c < "$PROMPT_FILE") bytes"
echo ""

set +e
case "$BACKEND" in
  copilot)
    cd "$ROOT_DIR"
    cat "$PROMPT_FILE" | "$CLI_BIN" \
      --yolo \
      --alt-screen off \
      --model "$MODEL"
    ;;
  codex)
    cd "$ROOT_DIR"
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

# Verify outputs
if [[ ! -f "$OUTPUT_DIR/product-research.md" ]]; then
  echo "WARNING: product-research.md was not created at $OUTPUT_DIR/product-research.md"
  exit 7
fi
if [[ ! -f "$OUTPUT_DIR/sources.json" ]]; then
  echo "WARNING: sources.json was not created at $OUTPUT_DIR/sources.json"
  exit 7
fi

echo ""
echo "=== Done ==="
echo "Research: $OUTPUT_DIR/product-research.md"
echo "Sources:  $OUTPUT_DIR/sources.json"
