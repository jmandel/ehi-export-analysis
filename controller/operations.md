# EHI Export Analysis — Ops Runbook

## Quick Start: Run the Collection Loop

```bash
# 1. Build family targets using bottom-up methodology
#    (first time, or after editing url-group-merges.json)
bun run scripts/build-phase-families.ts

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
| `work/phases/phase-1-comprehensive-ehrs.json` | CPOE + FHIR API (g)(10) — full EHRs | 218 |
| `work/phases/phase-2-cpoe-no-fhir.json` | CPOE without FHIR API | 107 |
| `work/phases/phase-3-other.json` | Everything else | 212 |
| `work/family-targets.json` | All families combined | 537 |

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

### Family generation (bottom-up methodology)

```
chpl-data/all-active-listings.json    696 CHPL product listings
        ↓  Step 1: each product = own family
        ↓  Step 2: merge by (developer, product_name, url) — version dedup
        ↓  Step 3: apply work/url-group-merges.json — content-verified merges
        ↓  scripts/build-phase-families.ts
work/family-targets.json              535 per-family targets
work/phases/phase-{N}-{slug}.json     per-phase target lists
```

**Step 1**: Every CHPL product matching a phase's criteria starts as its own family.
**Step 2**: Products with the same developer + product name + EHI URL are merged
(this is just version deduplication — "Product X v1" and "Product X v2" become one).
**Step 3**: Products sharing a developer + URL but with *different* product names
are candidates for merging. `url-group-merges.json` encodes decisions made by
actually reading EHI documentation at each URL to determine whether products
share an EHI approach (merge) or have distinct approaches (keep separate).

Key files:
- `scripts/naming.ts` — shared slugify + resultDirName (single source of truth)
- `work/url-group-merges.json` — merge/no-merge rules with rationale
- `scripts/build-phase-families.ts` — generates family targets
- `scripts/migrate-family-names.sh` — one-time migration of old dir names

### Collection and analysis pipeline

```
work/phases/phase-1-comprehensive-ehrs.json
        ↓  wiggum/loop.ts  (or scripts/run-research.sh + run-download.sh)
results/<vendor>--<family>/
  chpl-metadata.json       CHPL data filtered to this family
  product-research.md      Phase 1 output (+ sources.json marker)
  downloads/               Phase 2 downloads (+ files.json marker)
  ehi-export-report.md     Phase 2 coverage report
        ↓  scripts/run-fixup.sh  (if issues found — patches results, cascades)
        ↓  scripts/run-all-analyses.sh  (or run-split-analysis.sh for multi-product vendors)
abstraction/<vendor>--<family>/
  analysis.md              Deep analysis document
  metadata.json            Traceability (developer, CHPL products, timestamps)
  analysis/                Scripts and intermediate data
        ↓  scripts/run-all-summaries.sh
  summary.json             Structured JSON per ehi-summary-schema.ts
```

### Directory naming

All dirs use `<vendor-slug>--<family-slug>`. The slugification and dir-name
logic live in `scripts/naming.ts` (single source of truth, used by both
`build-phase-families.ts` and `wiggum/loop.ts`). Family names come from the
bottom-up methodology: each product's CHPL name is the default family name,
modified by merge rules in `url-group-merges.json` where products share an
EHI approach.

### Target ordering

Targets are sorted by CHPL product count descending (big vendors first in the
list). Use `--reverse` to process small single-product vendors first, deferring
complex multi-product vendors (Epic, MEDITECH, etc.) to the end.

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

# 3. Build family targets using bottom-up methodology
bun run scripts/build-phase-families.ts
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

# 3. Review url-group-merges.json for any new multi-product vendors
#    sharing a URL. Investigate content to decide merge vs. keep separate.

# 4. Regenerate family targets
bun run scripts/build-phase-families.ts

# 5. Run the loop with --resume (skips already-collected families)
```

The pipeline is additive: `--resume` skips any family that already has completion
markers, so only new/changed families get processed.

## Standalone Per-Vendor Scripts

Each pipeline stage has a standalone script for one-off runs, reruns, and
debugging. These use the same prompts and LLM backends as the batch tools
but work on a single vendor at a time.

### Script inventory

| Script | Stage | Inputs | Outputs |
|--------|-------|--------|---------|
| `scripts/run-research.sh` | Phase 1 (research) | `chpl-metadata.json` | `product-research.md`, `sources.json` |
| `scripts/run-download.sh` | Phase 2 (download) | `chpl-metadata.json`, `product-research.md` | `downloads/`, `files.json`, `ehi-export-report.md` |
| `scripts/run-analysis.sh` | Analysis | everything in `results/<slug>/` | `abstraction/<slug>/analysis.md`, `analysis/` |
| `scripts/run-summary.sh` | Summary | `analysis.md` | `summary.json` |
| `scripts/run-fixup.sh` | Fixup (autonomous) | `results/<slug>/` + issue/hint | patched results + cascaded downstream |
| `scripts/run-split-analysis.sh` | Split analysis | shared `results/` + split config | per-split `abstraction/<slug>/analysis.md` |

### Common options (all standalone scripts)

| Flag | Description |
|------|-------------|
| `--dir <slug>` | Directory name under `results/` (e.g. `vendor--product`) |
| `--backend <b>` | LLM backend: `copilot`, `codex` (default: copilot) |
| `--model <m>` | Model override (default: `claude-opus-4.6-fast` for copilot) |
| `--prompt <file>` | Custom prompt file (research + download only) |
| `-h, --help` | Show usage |

### One-off rerun of a single stage

```bash
# Redo research for one vendor
./scripts/run-research.sh --dir ezemrx-inc--ezemrx

# Redo download for one vendor
./scripts/run-download.sh --dir ezemrx-inc--ezemrx

# Redo analysis (remove old output first)
rm -f abstraction/ezemrx-inc--ezemrx/analysis.md
./scripts/run-analysis.sh --dir ezemrx-inc--ezemrx

# Use a custom prompt for research/download
./scripts/run-research.sh --dir vendor--product --prompt my-custom-prompt.md
```

### Relationship to the loop

The loop (`wiggum/loop.ts`) handles batch iteration (target ordering, `--resume`,
`--reverse`, git commits, watchdog/timeout). The standalone scripts handle
single-vendor execution. The loop uses its own built-in LLM dispatch (supports
`claude`, `shelley`, `gemini`, `copilot` backends); the standalone scripts use
`copilot` or `codex` backends and follow the same pattern as `run-analysis.sh`.

Both use the same prompt templates (`wiggum/prompts/1-research.md`,
`wiggum/prompts/2-download.md`) and template variable system.

## Fixup Workflow (Ad-Hoc Corrections)

When a collection run missed something or got something wrong, the fixup agent
diagnoses the problem, fixes it at the right pipeline stage, and cascades
downstream automatically.

### When to use fixup

- Download agent missed an artifact (e.g., PDF embedded in a viewer widget)
- Research is incomplete or wrong
- Downloaded file is corrupt or wrong content
- Any issue where the `results/` dir needs patching before re-analysis

### Running a fixup

```bash
# From a GitHub issue (reads title + body as the fixup hint)
./scripts/run-fixup.sh --dir ezemrx-inc--ezemrx --issue 1

# From an inline description
./scripts/run-fixup.sh --dir ezemrx-inc--ezemrx \
  --hint "The EHI page has a PDF embedded in an iframe viewer widget. The download agent noted an empty viewer but didn't extract the PDF URL. The PDF is the actual data dictionary."
```

### What the fixup agent does

The agent is fully autonomous. It:

1. **Reads** `controller/operations.md` to understand the pipeline
2. **Reads** the issue/hint and all existing results to diagnose the problem
3. **Determines the root-cause stage** (research? download? analysis?)
4. **Fixes at that stage** — e.g., fetches the missed PDF, updates `files.json`
5. **Cascades downstream** by running the standalone scripts:
   - If it fixed downloads → runs `run-analysis.sh` → `run-summary.sh`
   - If it fixed research → runs `run-download.sh` → `run-analysis.sh` → `run-summary.sh`
6. **Writes `fixup-log.md`** documenting diagnosis, changes, and cascade results

The prompt is at `wiggum/prompts/fixup.md`. Template variables include
`{{ROOT_DIR}}` and `{{DIR_SLUG}}` so the agent can invoke scripts by path.

### GitHub issue convention

- Use a `fixup` label on issues that need automated repair
- Issue body should mention the vendor slug or dashboard URL
- The `--issue` flag reads the issue via `gh issue view`

### Safety

The script archives `downloads/` to `downloads.pre-fixup/` before the agent
starts (first fixup only — won't overwrite an existing archive). The agent
is instructed not to modify the archive.

## Split Analysis (Multi-Product-Line Vendors)

Some vendors have one EHI documentation URL that covers multiple distinct
product lines with different export configurations. The normal pipeline
treats them as one family, but the analysis is better when split per
product line.

### The problem (MEDITECH example)

MEDITECH has 16 CHPL-certified products sharing one URL. That page documents
2 export "Configurations":
- **Config 1** (HIM/SCN/PHM-based): eChart + FHIR + C-CDA — covers Expanse,
  6.1x acute, older platforms in acute mode
- **Config 2** (MRI/DR-based): CSV + FHIR + C-CDA — covers older platforms,
  6.0 ambulatory

A monolithic analysis covering all 16 products and both configs is confusing.
Better to split into platform lines (Expanse, 6.x, CS/MAGIC) with focused
analyses.

### How split analysis works

Two things happen:

**1. Merge rules split** — edit `work/url-group-merges.json` (hand-authored)
to split one family into multiple:

```json
{
  "families": [
    { "name": "MEDITECH Expanse", "products": ["MEDITECH Expanse 2.2 Core HCIS", ...] },
    { "name": "MEDITECH 6.x", "products": ["MEDITECH 6.1 Electronic Health Record Core HCIS", ...] },
    { "name": "MEDITECH CS/MAGIC", "products": ["MEDITECH Client/Server ...", ...] }
  ]
}
```

Then regenerate targets: `bun run scripts/build-phase-families.ts`

**2. Split config** — create `work/splits/<vendor>.json` defining how to run
separate abstractions from shared downloads:

```json
{
  "source_dir": "medical-information-technology-inc-meditech--meditech-ehr",
  "splits": [
    {
      "slug": "medical-information-technology-inc-meditech--meditech-expanse",
      "focus": "MEDITECH Expanse platform (Config 1: eChart/FHIR/C-CDA)",
      "products": ["MEDITECH Expanse 2.2 Core HCIS", ...],
      "relevant_artifacts": ["ehiexportconfig1.html", "csacuteandambehiexportdrsolutionmerged.pdf"]
    }
  ]
}
```

### Running split analysis

```bash
# Dry run — see what would execute
./scripts/run-split-analysis.sh --split-config work/splits/meditech.json --dry-run

# Run all splits
./scripts/run-split-analysis.sh --split-config work/splits/meditech.json

# Force redo existing splits
./scripts/run-split-analysis.sh --split-config work/splits/meditech.json --force

# Then run summaries for the new split dirs
./scripts/run-all-summaries.sh --filter "medical-information-technology-inc-meditech--meditech-*" --force
```

### What the script does for each split

1. Creates `abstraction/<split-slug>/`
2. Symlinks `downloads/`, `*.md`, `*.json` from the shared source results dir
3. Writes `metadata.json` with split-specific traceability
4. Appends a **split context addendum** to the analysis prompt:
   - Which products to focus on
   - Which artifacts in `downloads/` are most relevant
   - Instruction to evaluate coverage against these specific products
5. Runs the analysis agent in the split output dir

### Options for `run-split-analysis.sh`

| Flag | Description |
|------|-------------|
| `--split-config <file>` | Split config JSON (required) |
| `--backend <b>` | LLM backend (default: copilot) |
| `--model <m>` | Model override |
| `--force` | Remove existing `analysis.md` and re-run |
| `--dry-run` | Print what would happen without executing |

### When to use splits

- Multiple product lines share one EHI documentation URL
- The documentation has configs/sections that apply to different products
- One monolithic analysis would be confusing or unfair to individual products

### What's hand-authored vs generated

| Artifact | Hand-authored? | Notes |
|---|---|---|
| `work/url-group-merges.json` | ✅ Yes | Merge/split rules with rationale |
| `work/splits/*.json` | ✅ Yes | Split configs for multi-product analysis |
| `work/family-targets.json` | ❌ Generated | From `build-phase-families.ts` |
| `work/phases/*.json` | ❌ Generated | From `build-phase-families.ts` |
| `results/*/` | ❌ Generated | From wiggum loop or standalone scripts |
| `abstraction/*/` | ❌ Generated | From analysis/split-analysis scripts |

Hand-authored files are fair game for manual editing. Generated files should
be regenerated from their sources (don't hand-edit `family-targets.json` —
edit `url-group-merges.json` and rerun `build-phase-families.ts`).
