#!/usr/bin/env bash
# Generate run-analysis.sh commands for all collected results.
#
# For each results/<slug>/ directory, reads chpl-metadata.json to get
# the product name(s) and generates one command per distinct product
# platform (grouping versions together).
#
# Usage:
#   ./scripts/generate-analysis-commands.sh [--backend <backend>] [--model <model>]
#   ./scripts/generate-analysis-commands.sh > /tmp/run-all.sh && bash /tmp/run-all.sh
#
# Options:
#   --backend   LLM backend to use (default: copilot)
#   --model     Model override
#   --skip-done Skip vendors that already have an analysis.md

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_ARG=""
MODEL_ARG=""
SKIP_DONE=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --backend)   BACKEND_ARG="--backend $2"; shift 2 ;;
    --model)     MODEL_ARG="--model $2"; shift 2 ;;
    --skip-done) SKIP_DONE=true; shift ;;
    -h|--help)
      echo "Usage: ./scripts/generate-analysis-commands.sh [--backend <b>] [--model <m>] [--skip-done]"
      exit 0
      ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

slugify() {
  echo "$1" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]\+/-/g' | sed 's/^-\|-$//g' | cut -c1-60
}

echo "#!/usr/bin/env bash"
echo "# Generated $(date -Iseconds)"
echo "# EHI Export Analysis commands for all collected results"
echo "set -euo pipefail"
echo ""

count=0
skipped=0

for results_dir in "$ROOT_DIR"/results/*/; do
  slug=$(basename "$results_dir")
  meta="$results_dir/chpl-metadata.json"

  # Skip dirs without metadata
  [[ -f "$meta" ]] || continue

  # Get distinct product names
  mapfile -t products < <(jq -r '.products[].product_name' "$meta" 2>/dev/null | sort -u)

  if [[ ${#products[@]} -eq 0 ]]; then
    products=("$slug")
  fi

  for product in "${products[@]}"; do
    product_slug=$(slugify "$product")
    output_dir="$ROOT_DIR/abstraction/${slug}--${product_slug}"

    # Skip if already done
    if [[ "$SKIP_DONE" == true && -f "$output_dir/analysis.md" ]]; then
      skipped=$((skipped + 1))
      continue
    fi

    echo "./scripts/run-analysis.sh --dir \"$slug\" --product \"$product\" $BACKEND_ARG $MODEL_ARG"
    count=$((count + 1))
  done
done

echo ""
echo "# Total: $count commands ($skipped skipped)" >&2
