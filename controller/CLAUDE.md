# EHI Export Analysis — Controller Guide

This file is for a Claude instance acting as the **controller** of the wiggum
collection loop. Load it explicitly when you need to manage the loop:

    claude -p "$(cat controller/CLAUDE.md) <your instruction>"

## Project Overview

Automated collection and characterization of EHI (Electronic Health
Information) export documentation from ~448 ONC-certified EHR products
listed in CHPL. The pipeline has three layers:

1. **Collection** (wiggum loop) — per-product-family research & download
2. **Analysis** (abstraction) — deep per-family analysis producing analysis.md
3. **Summary** (extraction) — structured JSON from analysis.md

### Product Phases (target groupings)

Targets are split into prioritized groups in `work/phases/`:

| File | Description | Count |
|------|-------------|-------|
| `phase-1-comprehensive-ehrs.json` | Full EHRs with broad certification | 207 |
| `phase-2-cpoe-no-fhir.json` | CPOE-certified without FHIR API | varies |
| `phase-3-api-and-specialty.json` | API-focused and specialty systems | varies |
| `phase-3-other.json` | Other systems | varies |
| `phase-4-minimal.json` | Minimally certified products | varies |

### Agent Phases (per-target stages)

Each target goes through two agent stages:

| Phase | Prompt | Completion marker | Output |
|-------|--------|-------------------|--------|
| 1 (research) | `wiggum/prompts/1-research.md` | `sources.json` | `product-research.md` + `sources.json` |
| 2 (download) | `wiggum/prompts/2-download.md` | `files.json` | Downloads + `ehi-export-report.md` |

Use `--phase both` to run research then download per target in one pass.
Use `--phase 1` or `--phase 2` to run a single stage.

## Directory Naming Convention

All results and abstraction dirs use `<vendor-slug>--<family-slug>` format:

```
results/aarista-technology-llc--aarista/           # collection output
abstraction/aarista-technology-llc--aarista/        # analysis output (mirrors results)
```

Multi-product vendors are split by product family. Families are defined in
`work/product-families.json` and expanded into per-family targets by
`scripts/expand-targets-by-family.ts`.

## Key Directories

```
work/targets.json                    # 448 URL-level targets sorted by product_count desc
work/family-targets.json             # Family-expanded targets (one per product family)
work/product-families.json           # Product family groupings for multi-product vendors
work/phases/                         # Phased target lists (subsets of targets.json)
work/target-metadata/NNNN.json       # Per-target CHPL metadata (enriched)
results/<vendor>--<family>/          # Per-family collection output
  chpl-metadata.json                 # CHPL metadata filtered to this family's products
  product-research.md                # Phase 1: narrative research report
  sources.json                       # Phase 1 completion marker
  downloads/                         # Phase 2: downloaded artifacts
  ehi-export-report.md               # Phase 2: coverage assessment report
  files.json                         # Phase 2 completion marker
  phase1-log.txt                     # Phase 1 agent log
  phase2-log.txt                     # Phase 2 agent log
abstraction/<vendor>--<family>/      # Per-family analysis output (same slug as results)
  analysis.md                        # Deep analysis document
  analysis/                          # Scripts and data produced during analysis
  metadata.json                      # Traceability: developer, CHPL products, timestamps
  summary.json                       # Structured JSON extracted from analysis.md
chpl-data/all-active-listings.json   # CHPL bulk download (~148MB)
wiggum/
  loop.ts                            # Main orchestration loop (Bun TypeScript)
  prompts/1-research.md              # Phase 1 prompt template
  prompts/2-download.md              # Phase 2 prompt template
  prompts/ehi-scope-reference.md     # Shared EHI scope definition (inlined into prompts)
  logs/loop-exit.log                 # EXIT trap log — check here when loop dies
  00-fetch-export-urls.sh            # Build targets.json from CHPL
  status.sh                          # Quick progress check
abstraction/
  abstraction-prompt.md              # Analysis prompt template
  ehi-summary-schema.ts             # TypeScript interface for summary.json extraction
scripts/
  expand-targets-by-family.ts        # Generate family-targets.json from targets + families
  run-analysis.sh                    # Single-family analysis runner
  run-all-analyses.sh                # Batch analysis runner (parallelism, skip-done)
  run-summary.sh                     # Single-family summary extraction
  run-all-summaries.sh               # Batch summary extraction
controller/CLAUDE.md                 # This file
```

## Running the Collection Loop

### Prerequisites: generate family-expanded targets

```bash
# First time or after updating product-families.json:
bun run scripts/expand-targets-by-family.ts
# Produces work/family-targets.json (one entry per product family)
```

### Start collection

```bash
# Using the TypeScript loop with family targets:
nohup env LLM_BACKEND=claude CLAUDE_MODEL=opus TIMEOUT=1800 STALE_TIMEOUT=300 \
  bun run wiggum/loop.ts \
  --targets work/family-targets.json \
  --phase both \
  --reverse --resume \
  > /tmp/wiggum-loop.log 2>&1 &
```

**Important**: Use `nohup` to keep the loop running if your session disconnects.

The loop creates `results/<vendor>--<family>/` directories with chpl-metadata
filtered to just the products in that family. Prompt templates receive
`{{FAMILY}}`, `{{FOCUS_PRODUCT}}`, and `{{FOCUS_VERSION}}` variables so the
agent focuses on the newest certified product in each family.

### Key flags

| Flag | Description |
|------|-------------|
| `--targets <file>` | Which target list to use (default: `work/targets.json`) |
| `--phase <1\|2\|both>` | Agent phase: research, download, or both |
| `--reverse` | Iterate from end of list backwards |
| `--resume` | Skip targets with existing completion marker |
| `--only <N>` | Run only target index N |
| `--index <N>` | Start from target index N |

### Key environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_BACKEND` | shelley | Backend: `claude`, `shelley`, or `gemini` |
| `CLAUDE_MODEL` | opus | Model for claude backend |
| `SHELLEY_MODEL` | claude-opus-4.6 | Model for shelley backend |
| `TIMEOUT` | 1800 | Per-target timeout in seconds (30 min) |
| `STALE_TIMEOUT` | 300 | Watchdog: kill agent if log stale for N seconds (5 min) |
| `DISCOURAGE_SUBAGENTS` | (empty) | Set non-empty to discourage subagent use |

## Loop Features

### EXIT trap
On any exit (success or failure), the loop logs to `wiggum/logs/loop-exit.log`
with the exit code. Check this file first when the loop dies unexpectedly.

### Stale-output watchdog
A per-agent background watchdog monitors the log file. If no output is written
for `STALE_TIMEOUT` seconds (default 300 = 5 min), the watchdog kills the agent.
The loop marks the target as failed and moves on to the next one.

### Prompt template includes
Prompts support `{{PLACEHOLDER}}` syntax. Variables like `{{URL}}`, `{{FAMILY}}`,
`{{FOCUS_PRODUCT}}`, `{{FOCUS_VERSION}}`, `{{DEVELOPERS}}`, `{{PRODUCTS}}`,
`{{CHPL_IDS}}`, `{{OUTPUT_DIR}}` are replaced with target-specific values.
A placeholder like `{{EHI_SCOPE_REFERENCE}}` that doesn't match a variable is
treated as a file include — loaded from `wiggum/prompts/ehi-scope-reference.md`
(key lowercased, underscores to hyphens).

## Monitoring

**Live log (agent output + loop messages):**
```bash
tail -f /tmp/wiggum-loop.log
```

**Current target's per-phase log:**
```bash
tail -f results/<vendor>--<family>/phase1-log.txt
```

**Count completed:**
```bash
echo "Phase 1: $(find results -name 'sources.json' | wc -l)"
echo "Phase 2: $(find results -name 'files.json' | wc -l)"
echo "Analyses: $(find abstraction -name 'analysis.md' | wc -l)"
echo "Summaries: $(find abstraction -name 'summary.json' | wc -l)"
```

**Recent completions from git log:**
```bash
git log --oneline --since="1 hour ago" -- 'results/*/sources.json' 'results/*/files.json'
```

**Check if loop is running:**
```bash
ps aux | grep -E 'loop\.ts|claude.*dangerous' | grep -v grep
```

**Check exit log for failures:**
```bash
cat wiggum/logs/loop-exit.log
```

## Killing and Restarting

**Kill everything:**
```bash
pkill -f 'wiggum/loop.ts'
sleep 1
pkill -f 'claude -p --dangerously'
```

**Clean up incomplete results before restarting:**
```bash
for d in results/*/; do
  if [ ! -f "$d/sources.json" ] && [ ! -f "$d/files.json" ]; then
    echo "removing incomplete: $(basename $d)"
    rm -rf "$d"
  fi
done
```

Then restart with `--resume` — it skips targets with existing completion markers.

## Post-Collection Pipelines

### Analysis (produces analysis.md)

```bash
# Single family:
./scripts/run-analysis.sh --dir aarista-technology-llc--aarista

# All families (skips done by default):
./scripts/run-all-analyses.sh -j 4

# Force redo:
./scripts/run-all-analyses.sh --force --filter "aarista*"
```

### Summary extraction (produces summary.json from analysis.md)

```bash
# Single:
./scripts/run-summary.sh --analysis-dir abstraction/aarista-technology-llc--aarista

# All:
./scripts/run-all-summaries.sh -j 4

# After changing ehi-summary-schema.ts, force re-extract:
./scripts/run-all-summaries.sh --force -j 4
```

The summary schema is in `abstraction/ehi-summary-schema.ts`. Add fields there
with JSDoc comments explaining how to derive them — the pipeline picks up new
fields automatically.

## How the Pipeline Works

1. `expand-targets-by-family.ts` reads `targets.json` + `product-families.json`
   → produces `family-targets.json` with one entry per product family
2. `loop.ts` reads a family target list
3. For each family target, creates `results/<vendor>--<family>/` with
   chpl-metadata filtered to that family's CHPL products
4. Renders prompt template with family context (FAMILY, FOCUS_PRODUCT, etc.)
5. Agent runs; watchdog monitors for staleness
6. Each phase produces its completion marker (`sources.json` or `files.json`)
7. Loop git-commits and pushes after each successful target
8. Post-collection: `run-all-analyses.sh` iterates `results/*--*/` dirs,
   produces `abstraction/<same-slug>/analysis.md`
9. Post-analysis: `run-all-summaries.sh` extracts structured JSON per schema

## Setup From Scratch

### 1. Download CHPL bulk data (if missing)

```bash
ls chpl-data/all-active-listings.json 2>/dev/null || \
  (mkdir -p chpl-data && curl -sL \
    'https://chpl.healthit.gov/rest/listings/download?listingType=active&format=json' \
    -H 'api-key: 12909a978483dfb8ecd0596c98ae9094' \
    -o chpl-data/all-active-listings.json)
```

### 2. Generate targets and metadata

```bash
./wiggum/00-fetch-export-urls.sh
```

This produces `work/targets.json` (448 targets) and the phase files.

### 3. Generate family-expanded targets

```bash
bun run scripts/expand-targets-by-family.ts
```

This produces `work/family-targets.json` (476 family targets).
