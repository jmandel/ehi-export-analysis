# EHI Export Analysis — Ops Runbook

## Quick Start: Run the Collection Loop

```bash
# 1. Generate family-expanded targets + phase files
#    (first time, or after editing product-families.json)
bun run scripts/expand-targets-by-family.ts

# 2. Start collection on phase 1 families (research + download)
nohup env LLM_BACKEND=claude CLAUDE_MODEL=opus TIMEOUT=1800 STALE_TIMEOUT=300 \
  bun run wiggum/loop.ts \
  --targets work/phases/phase-1-comprehensive-ehrs.json \
  --phase both \
  --reverse --resume \
  > /tmp/wiggum-loop.log 2>&1 &
```

Use `nohup` so the loop survives session disconnects. Use `--resume` to skip
already-completed targets.

### Target lists (pick one for `--targets`)

| File | Description | Families |
|------|-------------|----------|
| `work/phases/phase-1-comprehensive-ehrs.json` | CPOE + FHIR API (g)(10) — full EHRs | 217 |
| `work/phases/phase-2-cpoe-no-fhir.json` | CPOE without FHIR API | 99 |
| `work/phases/phase-3-other.json` | Everything else | 170 |
| `work/family-targets.json` | All families combined | 486 |

## Loop Flags

| Flag | Description |
|------|-------------|
| `--targets <file>` | Target list — use a phase file or `work/family-targets.json` |
| `--phase <1\|2\|both>` | `1` = research only, `2` = download only, `both` = both sequentially |
| `--reverse` | Process targets from end of list backwards |
| `--resume` | Skip targets that already have completion markers |
| `--only <N>` | Run only target index N |
| `--index <N>` | Start from target index N |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_BACKEND` | shelley | `claude`, `shelley`, or `gemini` |
| `CLAUDE_MODEL` | opus | Model when using claude backend |
| `SHELLEY_MODEL` | claude-opus-4.6 | Model when using shelley backend |
| `TIMEOUT` | 1800 | Per-target timeout (seconds) |
| `STALE_TIMEOUT` | 300 | Kill agent if no log output for this long (seconds) |

## Monitoring

```bash
# Live output
tail -f /tmp/wiggum-loop.log

# Per-target logs
tail -f results/<vendor>--<family>/phase1-log.txt

# Progress counts
echo "Phase 1: $(find results -name 'sources.json' | wc -l)"
echo "Phase 2: $(find results -name 'files.json' | wc -l)"
echo "Analyses: $(find abstraction -name 'analysis.md' | wc -l)"
echo "Summaries: $(find abstraction -name 'summary.json' | wc -l)"

# Is the loop running?
ps aux | grep -E 'loop\.ts|claude.*dangerous' | grep -v grep

# Check exit log (the loop logs here on any exit)
cat wiggum/logs/loop-exit.log
```

## Killing and Restarting

```bash
# Kill loop + agents
pkill -f 'wiggum/loop.ts'
sleep 1
pkill -f 'claude -p --dangerously'

# Clean up incomplete dirs (no completion marker from either phase)
for d in results/*/; do
  if [ ! -f "$d/sources.json" ] && [ ! -f "$d/files.json" ]; then
    echo "removing incomplete: $(basename $d)"
    rm -rf "$d"
  fi
done

# Restart with --resume
```

## Post-Collection: Analysis & Summary

### Analysis (produces analysis.md from collected artifacts)

The analysis pipeline reads everything in `results/<vendor>--<family>/` and
produces a deep narrative assessment in `abstraction/<vendor>--<family>/analysis.md`.
Uses the prompt template at `abstraction/abstraction-prompt.md`.

```bash
# Single family:
./scripts/run-analysis.sh --dir <vendor>--<family>

# All families with collected results (skips done by default):
./scripts/run-all-analyses.sh -j 4

# Force redo for specific vendors:
./scripts/run-all-analyses.sh --force --filter "epic*"

# Dry run — see what would execute:
./scripts/run-all-analyses.sh --dry-run

# Resume after interruption (same command — skips existing analysis.md):
./scripts/run-all-analyses.sh -j 4
```

Options for `run-all-analyses.sh`:

| Flag | Description |
|------|-------------|
| `-j, --jobs N` | Parallel jobs (default: 1, streams output) |
| `--force` | Remove existing analysis.md and re-run |
| `--dry-run` | Print commands without executing |
| `--backend <b>` | LLM backend (default: copilot) |
| `--model <m>` | Model override |
| `--filter <glob>` | Only process dirs matching glob |

Options for `run-analysis.sh`:

| Flag | Description |
|------|-------------|
| `--dir <slug>` | Results directory slug, e.g. `epic-systems-corporation--epic` |
| `--output-dir <dir>` | Override output directory (default: `abstraction/<slug>/`) |
| `--backend <b>` | LLM backend |
| `--model <m>` | Model override |

### Summary extraction (produces summary.json from analysis.md)

The summary pipeline reads `analysis.md` + the TypeScript schema at
`abstraction/ehi-summary-schema.ts` and extracts structured JSON.
Schema-agnostic: add fields to the `.ts` file with JSDoc comments
explaining how to derive them, and the pipeline picks them up automatically.

```bash
# Single family:
./scripts/run-summary.sh --analysis-dir abstraction/<vendor>--<family>

# All families with completed analyses (skips done by default):
./scripts/run-all-summaries.sh -j 4

# Force re-extract after schema changes:
./scripts/run-all-summaries.sh --force -j 4

# Filter to specific vendors:
./scripts/run-all-summaries.sh --filter "aarista*" --force
```

Options for `run-all-summaries.sh`:

| Flag | Description |
|------|-------------|
| `-j, --jobs N` | Parallel jobs (default: 1) |
| `--force` | Remove existing summary.json and re-run |
| `--dry-run` | Print commands without executing |
| `--backend <b>` | LLM backend (default: copilot) |
| `--model <m>` | Model override (default: claude-sonnet-4.5) |
| `--filter <glob>` | Only process dirs matching glob |

## How It All Fits Together

```
work/targets.json          448 URL-level targets from CHPL
        ↓  expand-targets-by-family.ts + work/product-families.json
work/family-targets.json   486 per-family targets (one per product family)
        ↓  wiggum/loop.ts
results/<vendor>--<family>/
  chpl-metadata.json       CHPL data filtered to this family
  product-research.md      Phase 1 output (+ sources.json marker)
  downloads/               Phase 2 downloads (+ files.json marker)
  ehi-export-report.md     Phase 2 coverage report
        ↓  scripts/run-all-analyses.sh
abstraction/<vendor>--<family>/
  analysis.md              Deep analysis document
  metadata.json            Traceability (developer, CHPL products, timestamps)
  analysis/                Scripts and intermediate data
        ↓  scripts/run-all-summaries.sh
  summary.json             Structured JSON per ehi-summary-schema.ts
```

### Directory naming

All dirs use `<vendor-slug>--<family-slug>`. Multi-product vendors are split by
family per `work/product-families.json`. Single-product vendors get
`<vendor>--<product>` automatically.

### Agent phases

| Phase | Prompt | Completion marker |
|-------|--------|-------------------|
| 1 (research) | `wiggum/prompts/1-research.md` | `sources.json` |
| 2 (download) | `wiggum/prompts/2-download.md` | `files.json` |

### Template variables in prompts

`{{URL}}`, `{{FAMILY}}`, `{{FOCUS_PRODUCT}}`, `{{FOCUS_VERSION}}`,
`{{DEVELOPERS}}`, `{{PRODUCTS}}`, `{{CHPL_IDS}}`, `{{OUTPUT_DIR}}`

Unmatched `{{PLACEHOLDER}}` → file include from `wiggum/prompts/<name>.md`
(lowercased, underscores → hyphens). E.g. `{{EHI_SCOPE_REFERENCE}}` →
`wiggum/prompts/ehi-scope-reference.md`.

### Stale-output watchdog

Per-agent background watchdog kills the agent if no log output for
`STALE_TIMEOUT` seconds (default 300). Loop marks target as failed and continues.

## Setup From Scratch

```bash
# 1. Download CHPL bulk data
mkdir -p chpl-data && curl -sL \
  'https://chpl.healthit.gov/rest/listings/download?listingType=active&format=json' \
  -H 'api-key: 12909a978483dfb8ecd0596c98ae9094' \
  -o chpl-data/all-active-listings.json

# 2. Generate targets + per-target metadata
./wiggum/00-fetch-export-urls.sh
bun run scripts/build-metadata.ts

# 3. Generate family-expanded targets + phase files
bun run scripts/expand-targets-by-family.ts
```

## Refreshing When New Products Appear

When CHPL adds new certified products or updates URLs:

```bash
# 1. Re-download bulk data
rm chpl-data/all-active-listings.json
mkdir -p chpl-data && curl -sL \
  'https://chpl.healthit.gov/rest/listings/download?listingType=active&format=json' \
  -H 'api-key: 12909a978483dfb8ecd0596c98ae9094' \
  -o chpl-data/all-active-listings.json

# 2. Regenerate targets + metadata
./wiggum/00-fetch-export-urls.sh
bun run scripts/build-metadata.ts

# 3. Review product-families.json for any new multi-product vendors
#    New vendors with multiple products need family groupings added manually.
#    Products not in any defined family trigger a WARNING — fix before running.

# 4. Regenerate family targets + phase files
bun run scripts/expand-targets-by-family.ts

# 5. Run the loop with --resume (skips already-collected families)
```

The pipeline is additive: `--resume` skips any family that already has completion
markers, so only new/changed families get processed.
