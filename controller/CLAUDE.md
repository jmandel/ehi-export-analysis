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

```bash
# Analysis: deep review of collected artifacts → analysis.md
./scripts/run-analysis.sh --dir <vendor>--<family>        # single
./scripts/run-all-analyses.sh -j 4                         # batch (skips done)
./scripts/run-all-analyses.sh --force --filter "epic*"     # force redo

# Summary: extract structured JSON from analysis.md → summary.json
./scripts/run-summary.sh --analysis-dir abstraction/<vendor>--<family>  # single
./scripts/run-all-summaries.sh -j 4                                     # batch
./scripts/run-all-summaries.sh --force -j 4                             # after schema change
```

The summary schema lives in `abstraction/ehi-summary-schema.ts`. Add fields with
JSDoc comments explaining derivation — the pipeline picks them up automatically.

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
