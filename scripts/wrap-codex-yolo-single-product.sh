#!/usr/bin/env bash

# Force bash execution even if invoked via `sh`.
if [ -z "${BASH_VERSION:-}" ]; then
  exec /usr/bin/env bash "$0" "$@"
fi

set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  ./scripts/wrap-codex-yolo-single-product.sh --dir <target-dir> --product <target-product> --output <output-file> [--backend <backend>] [--model <model>]

Options:
  --dir       Directory name under results/ (required)
  --product   Target product family name (required)
  --output    Output JSON path (required)
  --backend   LLM backend: codex, copilot (default: copilot)
  --model     Model override (default: claude-opus-4.6-fast for copilot, gpt-5.3-codex-spark for codex)
  -h, --help  Show this message

Examples:
  ./scripts/wrap-codex-yolo-single-product.sh \
    --dir isalus-healthcare \
    --product "OfficeEMR" \
    --output abstraction/isalus-healthcare/officeemr.json

  ./scripts/wrap-codex-yolo-single-product.sh \
    --dir isalus-healthcare \
    --product "OfficeEMR" \
    --output abstraction/isalus-healthcare/officeemr.json \
    --backend codex --model gpt-5.3-codex-spark
EOF
}

log() {
  if [[ "${CODEX_WRAPPER_DEBUG:-}" == "1" ]]; then
    echo "[wrap] $*"
  fi
}

TARGET_DIRNAME=""
TARGET_PRODUCT_NAME=""
OUTPUT_FILE=""
BACKEND="copilot"
MODEL=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dir)
      TARGET_DIRNAME="$2"
      shift 2
      ;;
    --product)
      TARGET_PRODUCT_NAME="$2"
      shift 2
      ;;
    --output)
      OUTPUT_FILE="$2"
      shift 2
      ;;
    --backend)
      BACKEND="$2"
      shift 2
      ;;
    --model)
      MODEL="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown arg: $1"
      usage
      exit 1
      ;;
  esac
done

if [[ -z "$TARGET_DIRNAME" || -z "$TARGET_PRODUCT_NAME" || -z "$OUTPUT_FILE" ]]; then
  echo "Missing required argument(s)."
  usage
  exit 1
fi

# Set default model per backend if not specified
if [[ -z "$MODEL" ]]; then
  case "$BACKEND" in
    copilot) MODEL="claude-opus-4.6-fast" ;;
    codex)   MODEL="gpt-5.3-codex-spark" ;;
    *)
      echo "Unknown backend: $BACKEND (expected: codex, copilot)"
      exit 1
      ;;
  esac
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_DIR="$ROOT_DIR/results/$TARGET_DIRNAME"
mkdir -p "$(dirname "$OUTPUT_FILE")"

if [[ ! -d "$TARGET_DIR" ]]; then
  echo "Target folder not found: $TARGET_DIR"
  exit 2
fi

# Resolve backend binary
case "$BACKEND" in
  codex)
    CLI_BIN="${CODEX_BIN:-$(command -v codex 2>/dev/null || true)}"
    if [[ -z "$CLI_BIN" ]]; then
      echo "codex binary not found in PATH. Set CODEX_BIN or install codex."
      exit 3
    fi
    ;;
  copilot)
    CLI_BIN="${COPILOT_BIN:-$(command -v copilot 2>/dev/null || true)}"
    if [[ -z "$CLI_BIN" ]]; then
      echo "copilot binary not found in PATH. Set COPILOT_BIN or install copilot."
      exit 3
    fi
    ;;
  *)
    echo "Unknown backend: $BACKEND"
    exit 1
    ;;
esac

log "Parsed args: dir=$TARGET_DIRNAME product=$TARGET_PRODUCT_NAME output=$OUTPUT_FILE backend=$BACKEND model=$MODEL"
log "Running from: $ROOT_DIR"
log "Using CLI: $CLI_BIN"

PROMPT_FILE=$(mktemp)
trap 'rm -f "$PROMPT_FILE"' EXIT

# Render the prompt template using bun (safe with special chars in content).
# Note: in bun -e mode, process.argv is [bun, arg1, arg2, ...] — no script
# path — so real args start at index 1 (not 2 like node -e).
bun -e '
const fs = require("fs");
const [tmplPath, tsPath, ehiPath, outPath, targetDir, productName, outputFile] = process.argv.slice(1);
let tmpl = fs.readFileSync(tmplPath, "utf8");
const vars = {
  TARGET_DIRNAME: targetDir,
  TARGET_PRODUCT_NAME: productName,
  OUTPUT_FILE: outputFile,
  TS_INTERFACE: fs.readFileSync(tsPath, "utf8"),
  EHI_SCOPE_REFERENCE: fs.readFileSync(ehiPath, "utf8"),
};
tmpl = tmpl.replace(/\{\{(\w+)\}\}/g, (_, k) => vars[k] || "");
fs.writeFileSync(outPath, tmpl);
' "$ROOT_DIR/abstraction/abstraction-prompt.md" \
  "$ROOT_DIR/abstraction/ehi-abstraction-target.ts" \
  "$ROOT_DIR/wiggum/prompts/ehi-scope-reference.md" \
  "$PROMPT_FILE" \
  "$TARGET_DIRNAME" \
  "$TARGET_PRODUCT_NAME" \
  "$OUTPUT_FILE"

log "Launching $BACKEND with model ${MODEL}"
log "Prompt written to ${PROMPT_FILE} ($(wc -c < "$PROMPT_FILE") bytes)"

set +e
case "$BACKEND" in
  codex)
    "$CLI_BIN" exec \
      --full-auto \
      --sandbox danger-full-access \
      --model "$MODEL" \
      --cd "$ROOT_DIR" \
      - < "$PROMPT_FILE"
    ;;
  copilot)
    "$CLI_BIN" \
      --yolo \
      --model "$MODEL" \
      --add-dir "$ROOT_DIR" \
      -p "$(cat "$PROMPT_FILE")"
    ;;
esac
cli_exit_code=$?
set -e

if [[ $cli_exit_code -ne 0 ]]; then
  echo "$BACKEND exited with code $cli_exit_code."
  echo "Check CODEX_WRAPPER_DEBUG=1 for prompt/CLI details."
  exit "$cli_exit_code"
fi

if ! command -v bun >/dev/null 2>&1; then
  echo "bun is required to run schema validation. Install bun or run validation outside this wrapper."
  exit 6
fi

if [[ ! -f "$OUTPUT_FILE" ]]; then
  echo "Expected output file was not created: ${OUTPUT_FILE}"
  echo "The agent may have written to a different path than requested."
  exit 7
fi

if ! bun x ajv-cli@5 validate --spec=draft2020 --strict=true --all-errors -s abstraction/ehi-abstraction.schema.json -d "$OUTPUT_FILE"; then
  echo "Schema validation failed for ${OUTPUT_FILE}."
  exit 8
fi

if ! jq -e . "$OUTPUT_FILE" >/dev/null; then
  echo "Output is not valid JSON: ${OUTPUT_FILE}"
  exit 9
fi
