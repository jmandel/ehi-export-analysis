#!/usr/bin/env bash
# Run split abstractions from a shared results directory.
#
# For vendors like MEDITECH where one results dir covers multiple product lines,
# this script creates per-split abstraction directories with shared downloads
# and runs separate analyses for each.
#
# Usage:
#   ./scripts/run-split-analysis.sh --split-config work/splits/meditech.json [--backend ...] [--model ...]

set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  ./scripts/run-split-analysis.sh --split-config <file> [options]

Options:
  --split-config  JSON file defining splits (required)
  --backend       LLM backend: copilot, codex (default: copilot)
  --model         Model override (default: claude-opus-4.6-fast for copilot)
  --force         Remove existing analysis.md and re-run
  --dry-run       Print what would happen without executing
  -h, --help      Show this message

Split config format:
  {
    "source_dir": "vendor--product",
    "splits": [
      {
        "slug": "vendor--product-line-a",
        "focus": "Description of what to focus on",
        "products": ["Product A v1", "Product A v2"],
        "relevant_artifacts": ["config1.html", "data-dict.pdf"]
      }
    ]
  }

Examples:
  ./scripts/run-split-analysis.sh --split-config work/splits/meditech.json
  ./scripts/run-split-analysis.sh --split-config work/splits/meditech.json --force
EOF
}

SPLIT_CONFIG=""
BACKEND="copilot"
MODEL=""
FORCE=false
DRY_RUN=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --split-config) SPLIT_CONFIG="$2"; shift 2 ;;
    --backend)      BACKEND="$2"; shift 2 ;;
    --model)        MODEL="$2"; shift 2 ;;
    --force)        FORCE=true; shift ;;
    --dry-run)      DRY_RUN=true; shift ;;
    -h|--help)      usage; exit 0 ;;
    *)              echo "Unknown arg: $1"; usage; exit 1 ;;
  esac
done

if [[ -z "$SPLIT_CONFIG" ]]; then
  echo "Missing required --split-config argument."
  usage
  exit 1
fi

if [[ ! -f "$SPLIT_CONFIG" ]]; then
  echo "Split config not found: $SPLIT_CONFIG"
  exit 2
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

# Parse split config
SOURCE_DIR=$(jq -r '.source_dir' "$SPLIT_CONFIG")
SOURCE_PATH="$ROOT_DIR/results/$SOURCE_DIR"
SPLIT_COUNT=$(jq '.splits | length' "$SPLIT_CONFIG")

if [[ ! -d "$SOURCE_PATH" ]]; then
  echo "Source results directory not found: $SOURCE_PATH"
  exit 2
fi

echo "=== Split Analysis ==="
echo "Source:  $SOURCE_DIR"
echo "Splits:  $SPLIT_COUNT"
echo "Backend: $BACKEND ($MODEL)"
echo ""

for i in $(seq 0 $((SPLIT_COUNT - 1))); do
  SLUG=$(jq -r ".splits[$i].slug" "$SPLIT_CONFIG")
  FOCUS=$(jq -r ".splits[$i].focus" "$SPLIT_CONFIG")
  PRODUCTS=$(jq -r ".splits[$i].products | join(\", \")" "$SPLIT_CONFIG")
  ARTIFACTS=$(jq -r ".splits[$i].relevant_artifacts // [] | join(\", \")" "$SPLIT_CONFIG")

  SPLIT_OUTPUT="$ROOT_DIR/abstraction/$SLUG"

  echo "--- Split $((i+1))/$SPLIT_COUNT: $SLUG ---"
  echo "  Focus:    $FOCUS"
  echo "  Products: $PRODUCTS"
  if [[ -n "$ARTIFACTS" ]]; then
    echo "  Key artifacts: $ARTIFACTS"
  fi

  # Skip if already done (unless --force)
  if [[ -f "$SPLIT_OUTPUT/analysis.md" && "$FORCE" != true ]]; then
    echo "  SKIP: analysis.md already exists (use --force to redo)"
    echo ""
    continue
  fi

  if [[ "$DRY_RUN" == true ]]; then
    echo "  DRY RUN: would create $SPLIT_OUTPUT and run analysis"
    echo ""
    continue
  fi

  # Remove old analysis if forcing
  if [[ "$FORCE" == true && -f "$SPLIT_OUTPUT/analysis.md" ]]; then
    rm -f "$SPLIT_OUTPUT/analysis.md"
    rm -rf "$SPLIT_OUTPUT/analysis/"
  fi

  # Create split output dir
  mkdir -p "$SPLIT_OUTPUT"

  # Symlink shared downloads and result artifacts
  for item in "$SOURCE_PATH"/downloads "$SOURCE_PATH"/*.md "$SOURCE_PATH"/*.json; do
    [ -e "$item" ] || continue
    linkname="$SPLIT_OUTPUT/$(basename "$item")"
    # Remove stale symlinks, but don't overwrite real files
    if [[ -L "$linkname" ]]; then
      rm -f "$linkname"
    fi
    if [[ ! -e "$linkname" ]]; then
      ln -s "$item" "$linkname"
    fi
  done

  # Write split-specific metadata
  jq -n \
    --arg dir_slug "$SLUG" \
    --arg source_dir "results/$SOURCE_DIR" \
    --arg focus "$FOCUS" \
    --arg products "$PRODUCTS" \
    --arg created_at "$(date -Iseconds)" \
    '{
      dir_slug: $dir_slug,
      source_dir: $source_dir,
      split_focus: $focus,
      split_products: $products,
      created_at: $created_at
    }' > "$SPLIT_OUTPUT/metadata.json"

  # Build the prompt addendum for this split
  ADDENDUM="

## Split Analysis Context

This is a **split analysis**: the downloads/ directory contains documentation
for multiple product lines from the same vendor. Your analysis should focus
specifically on the following:

**Focus**: $FOCUS

**Products to analyze**: $PRODUCTS"

  if [[ -n "$ARTIFACTS" ]]; then
    ADDENDUM="$ADDENDUM

**Most relevant artifacts in downloads/**: $ARTIFACTS
Other artifacts in downloads/ may be for other product lines — include them
in your analysis only where they provide shared context (e.g., common export
infrastructure) but don't treat them as primary sources for this product line."
  fi

  ADDENDUM="$ADDENDUM

When assessing coverage, evaluate against what these specific products store,
not the vendor's entire portfolio."

  # Create a temporary prompt that appends the addendum to the standard analysis prompt
  PROMPT_FILE=$(mktemp)
  trap 'rm -f "$PROMPT_FILE"' EXIT

  # Derive product name for the prompt
  PRODUCT_NAME=$(echo "$PRODUCTS" | cut -d',' -f1 | xargs)

  bun -e '
const fs = require("fs");
const [tmplPath, ehiPath, outPath, resultsDir, outputDir, productName, addendum] = process.argv.slice(1);
let tmpl = fs.readFileSync(tmplPath, "utf8");
const vars = {
  RESULTS_DIR: resultsDir,
  OUTPUT_DIR: outputDir,
  PRODUCT_NAME: productName,
  EHI_SCOPE_REFERENCE: fs.readFileSync(ehiPath, "utf8"),
};
tmpl = tmpl.replace(/\{\{(\w+)\}\}/g, (_, k) => vars[k] || "{{" + k + "}}");
tmpl += addendum;
fs.writeFileSync(outPath, tmpl);
' "$ROOT_DIR/abstraction/abstraction-prompt.md" \
    "$ROOT_DIR/wiggum/prompts/ehi-scope-reference.md" \
    "$PROMPT_FILE" \
    "$SOURCE_PATH" \
    "$SPLIT_OUTPUT" \
    "$PRODUCT_NAME" \
    "$ADDENDUM"

  echo "  Running analysis..."

  # Resolve CLI binary
  case "$BACKEND" in
    copilot)
      CLI_BIN="${COPILOT_BIN:-$(command -v copilot 2>/dev/null || true)}"
      ;;
    codex)
      CLI_BIN="${CODEX_BIN:-$(command -v codex 2>/dev/null || true)}"
      ;;
  esac

  set +e
  case "$BACKEND" in
    copilot)
      cd "$SPLIT_OUTPUT"
      "$CLI_BIN" \
        --yolo \
        --model "$MODEL" \
        -p "$(cat "$PROMPT_FILE")"
      ;;
    codex)
      cd "$SPLIT_OUTPUT"
      "$CLI_BIN" exec \
        --full-auto \
        --sandbox danger-full-access \
        --model "$MODEL" \
        - < "$PROMPT_FILE"
      ;;
  esac
  cli_exit_code=$?
  set -e

  rm -f "$PROMPT_FILE"

  if [[ $cli_exit_code -ne 0 ]]; then
    echo "  FAILED: $BACKEND exited with code $cli_exit_code"
    echo ""
    continue
  fi

  if [[ ! -f "$SPLIT_OUTPUT/analysis.md" ]]; then
    echo "  WARNING: analysis.md was not created"
  else
    echo "  Done: $SPLIT_OUTPUT/analysis.md"
  fi
  echo ""
done

echo "=== Split Analysis Complete ==="
