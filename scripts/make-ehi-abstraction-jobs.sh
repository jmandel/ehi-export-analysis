#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  scripts/make-ehi-abstraction-jobs.sh [--backend <backend>] [--model <model>]

Scans all results/ directories, extracts product names from chpl-metadata.json,
and writes one wrapper invocation per product to scripts/ehi-abstraction-jobs.txt.

Options:
  --backend  LLM backend (default: copilot)
  --model    Model override (default: per-backend default)
  -h, --help Show this message

Environment:
  OUTPUT_BASE_DIR  Override abstraction output base (default: abstraction)
EOF
}

BACKEND="copilot"
MODEL=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --backend) BACKEND="${2:?Missing value for --backend}"; shift 2 ;;
    --model)   MODEL="${2:?Missing value for --model}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown arg: $1"; usage; exit 1 ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

RESULTS_DIR="$ROOT_DIR/results"
PRODUCT_LIST_FILE="$ROOT_DIR/scripts/ehi-distinct-products.txt"
JOBS_FILE="$ROOT_DIR/scripts/ehi-abstraction-jobs.txt"
OUTPUT_BASE_DIR="${OUTPUT_BASE_DIR:-abstraction}"

: > "$PRODUCT_LIST_FILE"
: > "$JOBS_FILE"

job_count=0
skipped=0

for result_dir in "$RESULTS_DIR"/*/; do
  [ -d "$result_dir" ] || continue

  dir_name="$(basename "$result_dir")"

  if [[ ! -f "$result_dir/chpl-metadata.json" ]]; then
    echo "SKIP (no chpl-metadata.json): $dir_name" >&2
    skipped=$((skipped + 1))
    continue
  fi

  # Get unique product names from chpl-metadata.json
  # Some files use "product_name", others use "name"
  mapfile -t products < <(
    jq -r '[.products[] | (.product_name // .name // empty)] | unique | .[]' \
      "$result_dir/chpl-metadata.json" 2>/dev/null | sed 's/\r$//'
  )

  if [[ ${#products[@]} -eq 0 ]]; then
    echo "SKIP (no product names): $dir_name" >&2
    skipped=$((skipped + 1))
    continue
  fi

  for product in "${products[@]}"; do
    product="$(printf "%s" "$product" | sed -E 's/^\s+|\s+$//g' | tr -d '\r')"
    [ -n "$product" ] || continue

    # Slugify: lowercase, non-alnum to underscore, trim underscores
    slug="$(printf "%s" "$product" | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9' '_' | sed -E 's/^_+|_+$//g')"
    [ -n "$slug" ] || continue

    # Save product name (one per line, preserving multi-word names)
    printf '%s\n' "$product" >> "$PRODUCT_LIST_FILE"

    # Build command — backend/model flags only when non-default
    cmd="./scripts/wrap-codex-yolo-single-product.sh"
    cmd+=" --dir \"${dir_name}\""
    cmd+=" --product \"${product}\""
    cmd+=" --output \"${OUTPUT_BASE_DIR}/${dir_name}/${slug}.json\""
    if [[ "$BACKEND" != "copilot" ]]; then
      cmd+=" --backend \"${BACKEND}\""
    fi
    if [[ -n "$MODEL" ]]; then
      cmd+=" --model \"${MODEL}\""
    fi

    printf '%s\n' "$cmd" >> "$JOBS_FILE"
    job_count=$((job_count + 1))
  done
done

# Deduplicate product list (preserving full multi-word names)
sort -u -o "$PRODUCT_LIST_FILE" "$PRODUCT_LIST_FILE"
product_count=$(wc -l < "$PRODUCT_LIST_FILE")

cat <<EOF
Generated abstraction job list:
  Distinct products: ${product_count}
  Jobs:              ${job_count}
  Skipped dirs:      ${skipped}
  Product list:      ${PRODUCT_LIST_FILE}
  Job invocations:   ${JOBS_FILE}
  Backend:           ${BACKEND}${MODEL:+ (model: $MODEL)}

Run all jobs sequentially:
  while IFS= read -r cmd; do eval "\$cmd"; done < "${JOBS_FILE}"

Run N jobs in parallel:
  xargs -a "${JOBS_FILE}" -P 4 -I{} bash -c "{}"
EOF
