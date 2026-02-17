# Fixup: Repair EHI Export Collection Results

You are fixing a problem with previously collected EHI export documentation.
A prior collection run missed something or got something wrong. Your job is
to surgically patch the results directory so it's correct, then hand off to
downstream pipeline stages (analysis, summary) that will run on the corrected data.

## Context

**Vendor**: {{DEVELOPERS}}
**Product(s)**: {{PRODUCTS}}
**EHI Documentation URL**: {{URL}}
**Results directory**: {{OUTPUT_DIR}}

## What went wrong

{{FIXUP_HINT}}

## What's already collected

The results directory contains:
- `downloads/` — previously downloaded artifacts
- `files.json` — manifest of downloaded files
- `product-research.md` — product research from Phase 1
- `ehi-export-report.md` — download report from Phase 2
- `sources.json` — URLs visited during research
- `chpl-metadata.json` — CHPL certification data

Read these files to understand what was already collected and what the issue is.

## Your job

1. **Understand the problem** — read the issue description and the existing
   results to understand exactly what's wrong or missing.

2. **Fix it surgically** — do the minimum necessary to correct the results:
   - If a file was missed: download it into `downloads/`
   - If `files.json` needs updating: add the new file entry
   - If `ehi-export-report.md` needs updating: patch the relevant sections
   - Don't redo work that's already correct

3. **Document what you changed** — write `{{OUTPUT_DIR}}/fixup-log.md`:
   ```markdown
   # Fixup Log

   **Date**: {{date}}
   **Issue**: {{brief description}}

   ## Changes Made
   - Added: downloads/filename.pdf (source: URL)
   - Updated: files.json (added entry for new file)
   - Updated: ehi-export-report.md (added section on new artifact)

   ## Verification
   - Confirmed file is valid: `file downloads/filename.pdf` → PDF document
   - File size: X bytes
   ```

4. **Preserve the archive** — the script has already copied `downloads/` to
   `downloads.pre-fixup/` before you started. Don't modify that backup.

## Important

- **Don't redo the full collection.** Only fix what's broken.
- **Keep existing files intact** unless they need correction.
- **Update `files.json`** if you add or modify any files in `downloads/`.
- **Be specific in the fixup log** — someone should be able to verify your fix.
- After you're done, downstream stages (analysis, summary) will rerun on
  the corrected results using their normal prompts.

{{EHI_SCOPE_REFERENCE}}
