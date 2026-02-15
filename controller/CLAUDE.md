# EHI Export Analysis — Controller Guide

This file is for a Claude instance acting as the **controller** of the wiggum
collection loop. Load it explicitly when you need to manage the loop:

    claude -p "$(cat controller/CLAUDE.md) <your instruction>"

## Project Overview

Automated collection and characterization of EHI (Electronic Health
Information) export documentation from ~448 ONC-certified EHR products
listed in CHPL. The pipeline has two layers of "phases":

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

## Key Directories

```
work/targets.json                    # 448 targets sorted by product_count desc
work/phases/                         # Phased target lists (subsets of targets.jsoni
uork/target-metadata/NNNN.json       # Per-target CHPL metadata (enriched)
results/<slug>/                      # Per-vendor output
  chpl-metadata.json                 # Copy of target metadata
  product-research.md                # Phase 1: narrative research report
  sources.json                       # Phase 1 completion marker
  downloads/                         # Phase 2: downloaded artifacts
  ehi-export-report.md               # Phase 2: coverage assessment report
  files.json                         # Phase 2 completion marker
  phase1-log.txt                     # Phase 1 agent log
  phase2-log.txt                     # Phase 2 agent log
chpl-data/all-active-listings.json   # CHPL bulk download (~148MB)
wiggum/
  loop.sh                            # Main orchestration loop (with watchdog)
  prompts/1-research.md              # Phase 1 prompt template
  prompts/2-download.md              # Phase 2 prompt template
  prompts/ehi-scope-reference.md     # Shared EHI scope definition (inlined into prompts)
  log-handler.py                     # Stream-json → readable filter
  watch-results.sh                   # inotifywait watcher (legacy, watches analysis.json)
  logs/loop-exit.log                 # EXIT trap log — check here when loop dies
  00-fetch-export-urls.sh            # Build targets.json from CHPL
  status.sh                          # Quick progress check
abstraction/
  ehi-abstraction-target.ts          # TypeScript interface defining abstraction output shape
  ehi-abstraction.schema.json        # JSON Schema (generated from TS interface)
scripts/
  wrap-codex-yolo-single-product.sh  # Codex wrapper for single-product abstraction
controller/CLAUDE.md                 # This file
```

## Running the Loop

### Start collection (both research + download per target)

```bash
# Phase 1 products (comprehensive EHRs), backwards, using Claude Opus:
nohup env LLM_BACKEND=claude CLAUDE_MODEL=opus TIMEOUT=1800 STALE_TIMEOUT=300 \
  ./wiggum/loop.sh \
  --targets work/phases/phase-1-comprehensive-ehrs.json \
  --phase both \
  --reverse --resume \
  > /tmp/wiggum-loop.log 2>&1 &
```

**Important**: Use `nohup` to keep the loop running if your session disconnects.

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
| `TIMEOUT` | 1800 | Per-target timeout in seconds (30 min) |
| `STALE_TIMEOUT` | 300 | Watchdog: kill agent if log stale for N seconds (5 min) |
| `DISCOURAGE_SUBAGENTS` | (empty) | Set non-empty to discourage subagent use |

## Loop Features

### EXIT trap
On any exit (success or failure), the loop logs to `wiggum/logs/loop-exit.log`
with the exit code, line number, and failing command. Check this file first when
the loop dies unexpectedly.

### Stale-output watchdog
A per-agent background watchdog monitors the log file. If no output is written
for `STALE_TIMEOUT` seconds (default 300 = 5 min), the watchdog kills the agent.
The loop marks the target as failed and moves on to the next one. This prevents
hung agents from blocking the entire pipeline.

### Prompt template includes
Prompts support `{{PLACEHOLDER}}` syntax for file includes. A placeholder like
`{{EHI_SCOPE_REFERENCE}}` is replaced with the contents of
`wiggum/prompts/ehi-scope-reference.md` (key lowercased, underscores to hyphens).
This lets shared content (like the EHI scope definition) be reused across prompts.

## Monitoring

**Live log (agent output + loop messages):**
```bash
tail -f /tmp/wiggum-loop.log
```

**Current target's per-phase log:**
```bash
tail -f results/<slug>/phase1-log.txt
```

**Count completed:**
```bash
echo "Phase 1: $(find results -name 'sources.json' | wc -l)"
echo "Phase 2: $(find results -name 'files.json' | wc -l)"
```

**Recent completions from git log:**
```bash
git log --oneline --since="1 hour ago" -- 'results/*/sources.json' 'results/*/files.json'
```

**Check if loop is running:**
```bash
ps aux | grep -E 'loop\.sh|claude.*dangerous' | grep -v grep
```

**Check exit log for failures:**
```bash
cat wiggum/logs/loop-exit.log
```

## Killing and Restarting

**Kill everything:**
```bash
pkill -f 'wiggum/loop.sh'
sleep 1
pkill -f 'claude -p --dangerously'
```

**Wait for current target to finish, then restart** (graceful):
Watch for the git commit line in the loop log, kill the loop after it appears,
then restart with `--resume`.

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

## How the Pipeline Works

1. `loop.sh` reads a target list (e.g., `work/phases/phase-1-comprehensive-ehrs.json`)
2. For each target, copies `work/target-metadata/NNNN.json` → `results/<slug>/chpl-metadata.json`
3. Renders the phase prompt template with target details and file includes
4. Agent runs in background; watchdog monitors log file for staleness
5. Agent output goes to both `results/<slug>/phase{N}-log.txt` and stdout
6. Each agent phase produces its completion marker (`sources.json` or `files.json`)
7. The loop git-commits and pushes after each successful target completion
8. If an agent exceeds `TIMEOUT` seconds or stalls for `STALE_TIMEOUT`, it is killed
   and the loop moves on

## Abstraction Pipeline (Post-Collection)

After collection, each product's evidence is abstracted into structured JSON:

```bash
./scripts/wrap-codex-yolo-single-product.sh \
  --dir <results-slug> \
  --product "<Product Name>" \
  --output abstraction/<slug>/<product>.json
```

The wrapper:
- Inlines the TS interface into the prompt
- Pipes prompt via stdin to `codex exec` (avoids shell arg truncation)
- Tells Codex to validate with `ajv` against `ehi-abstraction.schema.json`
- Post-validates the output itself as a safety net

## i3 Desktop Setup

Chrome windows launched by the chrome-devtools-mcp plugin route to workspace 0:
```
for_window [instance="(?i)chrome-devtools-mcp"] move to workspace number 0
```
The MCP Chrome profile is at `~/.cache/chrome-devtools-mcp/chrome-profile`.

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
