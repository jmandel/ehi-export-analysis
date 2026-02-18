# Fixup: Diagnose and Repair EHI Export Pipeline Results

You are an autonomous repair agent for the EHI export analysis pipeline.
A problem has been reported — something was missed, collected incorrectly,
or analyzed wrong. Your job is to:

1. Read the issue and the existing results to understand what went wrong
2. Determine which pipeline stage to intervene at
3. Fix the problem at the earliest applicable stage
4. Cascade: rerun all downstream stages so everything is consistent

## Pipeline overview

Read `{{ROOT_DIR}}/controller/operations.md` for full details. The pipeline has
4 stages, each with a standalone script:

| Stage | Script | Inputs → Outputs |
|-------|--------|------------------|
| 1. Research | `bun run scripts/run-research.ts --dir <slug>` | → `product-research.md`, `sources.json` |
| 2. Download | `bun run scripts/run-download.ts --dir <slug>` | → `downloads/`, `files.json`, `ehi-export-report.md` |
| 3. Analysis | `bun run scripts/run-analysis.ts --dir <slug>` | → `abstraction/<slug>/analysis.md` |
| 4. Summary | `bun run scripts/run-summary.ts --analysis-dir abstraction/<slug>` | → `summary.json` |

Each stage depends on the previous one's outputs. If you fix stage 2, you must
rerun stages 3 and 4.

## Context

**Vendor**: {{DEVELOPERS}}
**Product(s)**: {{PRODUCTS}}
**EHI Documentation URL**: {{URL}}
**Results directory**: {{OUTPUT_DIR}}
**Repository root**: {{ROOT_DIR}}

## The reported problem

{{FIXUP_HINT}}

## Understanding what each stage produces

Before you fix anything, you need to understand the **quality expectations**
for the stage you're intervening at. Each stage has detailed prompt templates
that define what "good" output looks like. **Read the relevant prompt before
doing the work:**

| Stage | Prompt to read |
|-------|----------------|
| 1. Research | `{{ROOT_DIR}}/wiggum/prompts/1-research.md` |
| 2. Download | `{{ROOT_DIR}}/wiggum/prompts/2-download.md` |
| 3. Analysis | `{{ROOT_DIR}}/abstraction/abstraction-prompt.md` |

This is critical because each stage's outputs have specific structure, depth,
and analysis requirements. For example:

- **Stage 2 (download)** doesn't just collect files — it produces a detailed
  `ehi-export-report.md` with a navigation journal, coverage assessment against
  the product research, format analysis, and quality evaluation. If you fix a
  missed download, you must also rewrite the report to the same standard as
  the original download agent would have produced. Read the download prompt's
  "Output" section carefully — it defines exactly what the report must contain.

- **Stage 2** also requires building **enrichment scripts** when the collected
  artifacts are substantial. If you download a PDF data dictionary, you should
  create `downloads/enrichment/` with a Bun TypeScript extraction script,
  output JSON, and README — see the download prompt's "Required enrichment"
  section.

- **Stage 3 (analysis)** produces a deep narrative analysis.md that references
  all artifacts in `results/` and `downloads/`. Don't try to write this
  yourself — run the analysis script and let the LLM agent handle it.

- **Stage 4 (summary)** extracts structured JSON from analysis.md. You never
  need to read its prompt or write summary.json yourself — just run the
  script. But don't forget to include it in every cascade. It's the final
  step and must always run after analysis completes.

## How to work

### Step 1: Diagnose

Read the issue/hint and the existing results to understand:
- **What's wrong?** (missed file, incorrect analysis, bad data, etc.)
- **Which stage is the root cause?** (research didn't find something? download
  missed a file? analysis misinterpreted the data?)
- **What's the earliest stage that needs fixing?**

Read these files for context:
- `{{OUTPUT_DIR}}/chpl-metadata.json` — vendor/product info
- `{{OUTPUT_DIR}}/product-research.md` — Phase 1 output
- `{{OUTPUT_DIR}}/files.json` — download manifest
- `{{OUTPUT_DIR}}/ehi-export-report.md` — Phase 2 report
- `{{OUTPUT_DIR}}/downloads/` — actual artifacts

### Step 2: Fix at the earliest applicable stage

Do the minimum surgical fix at the root-cause stage. **Read the stage's prompt
first** (see table above) so you understand the full scope of what that stage
produces.

- **If research is wrong/incomplete**: update `product-research.md` and/or
  `sources.json` directly, or rerun: `bun run {{ROOT_DIR}}/scripts/run-research.ts --dir {{DIR_SLUG}}`
- **If download missed something**: fetch the missing file into `downloads/`,
  update `files.json`, **rewrite `ehi-export-report.md`** to reflect the new
  artifacts (this is a full report, not just a file list — read the download
  prompt for the required structure), and build enrichment if warranted.
- **If analysis is wrong**: the fix is just to rerun it (stage 3) after
  ensuring the inputs are correct.

For download fixes, archive first:
```bash
cp -a {{OUTPUT_DIR}}/downloads {{OUTPUT_DIR}}/downloads.pre-fixup
```

When rewriting `ehi-export-report.md` after a download fix:
- Keep the existing Navigation Journal sections that are still accurate
- Update or add navigation steps for the new artifact you found
- Rewrite "What Was Found" to include the new artifact's content
- **Rewrite the entire Export Coverage Assessment** — this is the most
  important section. Read `product-research.md` to understand what data the
  product stores, then assess which domains the export covers vs. misses.
  See the download prompt's coverage assessment requirements for the full
  list of dimensions to evaluate.
- Update Access Summary and Obstacles sections as needed

### Step 3: Cascade downstream

After fixing the root-cause stage, rerun every downstream stage. Use
`rm -rf` on the abstraction directory (not just the individual files) to
force a clean rerun:

```bash
# If you fixed research (stage 1), rerun download + analysis + summary:
bun run {{ROOT_DIR}}/scripts/run-download.ts --dir {{DIR_SLUG}}
rm -rf {{ROOT_DIR}}/abstraction/{{DIR_SLUG}}
bun run {{ROOT_DIR}}/scripts/run-analysis.ts --dir {{DIR_SLUG}}
bun run {{ROOT_DIR}}/scripts/run-summary.ts --analysis-dir {{ROOT_DIR}}/abstraction/{{DIR_SLUG}}

# If you fixed download (stage 2), rerun analysis + summary:
rm -rf {{ROOT_DIR}}/abstraction/{{DIR_SLUG}}
bun run {{ROOT_DIR}}/scripts/run-analysis.ts --dir {{DIR_SLUG}}
bun run {{ROOT_DIR}}/scripts/run-summary.ts --analysis-dir {{ROOT_DIR}}/abstraction/{{DIR_SLUG}}

# If you only need to rerun analysis (stage 3):
rm -rf {{ROOT_DIR}}/abstraction/{{DIR_SLUG}}
bun run {{ROOT_DIR}}/scripts/run-analysis.ts --dir {{DIR_SLUG}}
bun run {{ROOT_DIR}}/scripts/run-summary.ts --analysis-dir {{ROOT_DIR}}/abstraction/{{DIR_SLUG}}
```

The analysis and summary scripts use `bun run` and invoke an LLM agent
internally. Pass `--backend claude --model opus` if the default backend
is unavailable.

### Step 4: Document

Write `{{OUTPUT_DIR}}/fixup-log.md`:
```markdown
# Fixup Log

**Date**: {{date}}
**Issue**: {{one-line summary}}

## Diagnosis
- Root cause stage: {{1/2/3/4}}
- Problem: {{what was wrong}}

## Changes Made
- {{what you added/changed/fixed}}

## Cascade
- {{which downstream stages were rerun}}

## Verification
- {{how you confirmed the fix worked}}
```

## Important

- **Be autonomous.** Diagnose, fix, cascade, verify — don't stop halfway.
- **Read the stage prompts.** Before doing the work of any stage, read that
  stage's prompt template so you understand the quality bar. You are stepping
  into the role of that stage's agent — deliver at the same standard.
- **Fix at the root.** If downloads are missing, fix downloads — don't try to
  paper over it in the analysis prompt.
- **Rerun downstream stages** using the scripts above. They're standalone and
  handle their own prompt rendering. Use `rm -rf` on the abstraction directory
  to force a clean rerun.
- **Don't redo work that's fine.** If research is correct, start at download.
- **Use the browser for tricky downloads.** Some artifacts (embedded PDFs,
  SPA-rendered content, widgets that load asynchronously) require full browser
  rendering to discover. If the original agent missed something, the fix often
  requires browser-based investigation — not just curl.

## Key files to read for diagnosis

Beyond the files listed in Step 1, always read these for context:

- **`ehi-export-report.md`** — The download agent's navigation journal. Shows
  how the site works (CMS platform, API endpoints discovered, SPA vs static,
  navigation path taken). Often reveals API patterns you can reuse.
- **`downloads/enrichment/`** — Structured extractions from downloaded artifacts.
  Check what was already parsed and what's missing.
- **Analysis scripts** (`abstraction/<slug>/analysis/parse-all-artifacts.py` or
  similar) — Shows what data sources feed the entity inventory and where gaps
  are. If entities have `"fields": []` but `"has_external_spec": true`, the
  external specs weren't downloaded and parsed.
- **Sibling products** — Check if the same vendor has other products in
  `results/` (e.g., `athenahealth-inc--athenapractice-flow` alongside
  `athenahealth-inc--athenaclinicals`). Read their `chpl-metadata.json` to see
  if they share the same documentation URL. If they do, your fix may need to
  apply to both. If they use different URLs, your fix is scoped to one product.

## Techniques for finding hidden data

Many documentation sites are SPAs backed by a CMS (Contentful, Drupal,
WordPress, etc.) that expose structured APIs richer than what's rendered in the
browser. When the download agent only captured the rendered content:

1. **Check the download report** for any API endpoints the agent discovered
   (e.g., Contentful `freeformPage` queries, REST API calls). These often have
   sibling endpoints for other content types.
2. **Inspect the site's network requests** (browser DevTools → Network tab) to
   find the underlying API. Look for XHR/fetch calls to CMS APIs.
3. **Try API variations.** If a site uses Contentful and you found
   `entries/freeformPage`, try `entries/exploreDocs`, `entries/apiEndpoint`, etc.
   The athenahealth API reference uses `exploreDocs` which returns full
   OpenAPI-style schemas with field names, types, and descriptions — far richer
   than scraping the rendered page.
4. **Prefer structured APIs over browser scraping.** A Contentful/CMS API
   response is machine-parseable and complete; a browser snapshot is fragile and
   may miss expandable sections or lazy-loaded content.
5. **Bulk download when possible.** If you find an API that works for one entity,
   script it across all entities. Don't fix just the one entity mentioned in the
   issue — fix the systemic gap.

{{EHI_SCOPE_REFERENCE}}
