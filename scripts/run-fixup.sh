#!/usr/bin/env bash
# Run a fixup agent to repair collected EHI export results.
#
# The fixup agent sees the existing results + an issue description, and
# surgically patches the results directory. After fixup, rerun downstream
# stages (analysis, summary) with the normal scripts.
#
# Usage:
#   ./scripts/run-fixup.sh --dir <slug> --issue <N>
#   ./scripts/run-fixup.sh --dir <slug> --hint "description of what to fix"

set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  ./scripts/run-fixup.sh --dir <results-dir-name> [options]

Options:
  --dir        Directory name under results/ (required)
  --issue <N>  GitHub issue number to read fixup instructions from
  --hint "..." Inline fixup hint (alternative to --issue)
  --backend    LLM backend: copilot, codex (default: copilot)
  --model      Model override (default: claude-opus-4.6-fast for copilot)
  --cascade    After fixup, automatically rerun analysis + summary
  -h, --help   Show this message

Examples:
  ./scripts/run-fixup.sh --dir ezemrx-inc--ezemrx --issue 1
  ./scripts/run-fixup.sh --dir ezemrx-inc--ezemrx --hint "Missed PDF embedded in viewer widget"
  ./scripts/run-fixup.sh --dir ezemrx-inc--ezemrx --issue 1 --cascade
EOF
}

TARGET_DIRNAME=""
ISSUE_NUM=""
HINT=""
BACKEND="copilot"
MODEL=""
CASCADE=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dir)        TARGET_DIRNAME="$2"; shift 2 ;;
    --issue)      ISSUE_NUM="$2"; shift 2 ;;
    --hint)       HINT="$2"; shift 2 ;;
    --backend)    BACKEND="$2"; shift 2 ;;
    --model)      MODEL="$2"; shift 2 ;;
    --cascade)    CASCADE=true; shift ;;
    -h|--help)    usage; exit 0 ;;
    *)            echo "Unknown arg: $1"; usage; exit 1 ;;
  esac
done

if [[ -z "$TARGET_DIRNAME" ]]; then
  echo "Missing required --dir argument."
  usage
  exit 1
fi

if [[ -z "$ISSUE_NUM" && -z "$HINT" ]]; then
  echo "Must provide either --issue <N> or --hint \"text\"."
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
  exit 2
fi

# Get fixup hint from GitHub issue or inline
FIXUP_HINT=""
if [[ -n "$ISSUE_NUM" ]]; then
  echo "Fetching issue #$ISSUE_NUM..."
  ISSUE_JSON=$(gh issue view "$ISSUE_NUM" --repo "$(git -C "$ROOT_DIR" remote get-url origin | sed 's/.*github.com[:/]//;s/\.git$//')" --json title,body 2>/dev/null || true)
  if [[ -z "$ISSUE_JSON" ]]; then
    echo "Failed to fetch issue #$ISSUE_NUM. Provide --hint instead."
    exit 4
  fi
  ISSUE_TITLE=$(echo "$ISSUE_JSON" | jq -r '.title')
  ISSUE_BODY=$(echo "$ISSUE_JSON" | jq -r '.body')
  FIXUP_HINT="GitHub Issue #$ISSUE_NUM: $ISSUE_TITLE

$ISSUE_BODY"
else
  FIXUP_HINT="$HINT"
fi

# Extract template variables from chpl-metadata.json
URL=$(jq -r '.url // empty' "$OUTPUT_DIR/chpl-metadata.json" 2>/dev/null || true)
DEVELOPERS=$(jq -r '[.developer.name // empty] | join(", ")' "$OUTPUT_DIR/chpl-metadata.json" 2>/dev/null || true)
PRODUCTS=$(jq -r '[.products[].product_name // empty] | join(", ")' "$OUTPUT_DIR/chpl-metadata.json" 2>/dev/null || true)

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

# Archive current downloads as safety net
if [[ -d "$OUTPUT_DIR/downloads" && ! -d "$OUTPUT_DIR/downloads.pre-fixup" ]]; then
  echo "Archiving current downloads to downloads.pre-fixup..."
  cp -a "$OUTPUT_DIR/downloads" "$OUTPUT_DIR/downloads.pre-fixup"
fi

# Render the fixup prompt
PROMPT_FILE=$(mktemp)
trap 'rm -f "$PROMPT_FILE"' EXIT

bun -e '
const fs = require("fs");
const path = require("path");
const [tmplPath, outPath, url, developers, products, outputDir, fixupHint, promptsDir] = process.argv.slice(1);
let tmpl = fs.readFileSync(tmplPath, "utf8");
const vars = {
  URL: url,
  DEVELOPERS: developers,
  PRODUCTS: products,
  OUTPUT_DIR: outputDir,
  FIXUP_HINT: fixupHint,
};
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
' "$ROOT_DIR/wiggum/prompts/fixup.md" \
  "$PROMPT_FILE" \
  "$URL" \
  "$DEVELOPERS" \
  "$PRODUCTS" \
  "$OUTPUT_DIR" \
  "$FIXUP_HINT" \
  "$ROOT_DIR/wiggum/prompts"

echo "=== Fixup Agent ==="
echo "Target:     $TARGET_DIRNAME"
echo "Developer:  $DEVELOPERS"
echo "Issue:      ${ISSUE_NUM:-inline hint}"
echo "Hint:       $(echo "$FIXUP_HINT" | head -1)"
echo "Output:     $OUTPUT_DIR"
echo "Backend:    $BACKEND ($MODEL)"
echo ""

set +e
case "$BACKEND" in
  copilot)
    cd "$ROOT_DIR"
    "$CLI_BIN" \
      --yolo \
      --model "$MODEL" \
      -p "$(cat "$PROMPT_FILE")"
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

# Verify required markers still exist
if [[ ! -f "$OUTPUT_DIR/files.json" ]]; then
  echo "WARNING: files.json missing after fixup — something went wrong."
  exit 7
fi

echo ""
echo "=== Fixup Complete ==="
if [[ -f "$OUTPUT_DIR/fixup-log.md" ]]; then
  echo "Fixup log: $OUTPUT_DIR/fixup-log.md"
fi
echo ""

# Cascade: rerun downstream stages
if [[ "$CASCADE" == true ]]; then
  echo "=== Cascading: rerun analysis + summary ==="
  echo ""

  ABSTRACTION_DIR="$ROOT_DIR/abstraction/$TARGET_DIRNAME"

  # Remove old analysis to force rerun
  if [[ -f "$ABSTRACTION_DIR/analysis.md" ]]; then
    echo "Removing old analysis.md for rerun..."
    rm -f "$ABSTRACTION_DIR/analysis.md"
    rm -rf "$ABSTRACTION_DIR/analysis/"
  fi

  echo "Running analysis..."
  "$ROOT_DIR/scripts/run-analysis.sh" --dir "$TARGET_DIRNAME" --backend "$BACKEND" --model "$MODEL"

  # Remove old summary to force rerun
  if [[ -f "$ABSTRACTION_DIR/summary.json" ]]; then
    echo "Removing old summary.json for rerun..."
    rm -f "$ABSTRACTION_DIR/summary.json"
  fi

  echo "Running summary..."
  "$ROOT_DIR/scripts/run-summary.sh" --analysis-dir "$ABSTRACTION_DIR" --backend "$BACKEND" --model "$MODEL"

  echo ""
  echo "=== Cascade Complete ==="
fi
