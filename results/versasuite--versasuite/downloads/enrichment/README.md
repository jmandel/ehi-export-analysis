# VersaSuite Data Dictionary Enrichment

## Run Command

```bash
cd /home/jmandel/hobby/ehi-export-analysis/results/versasuite--versasuite/downloads/enrichment
bun run extract-data-dictionary.ts
```

## Input Boundary

Parses all `.html` files in `../data-dictionary/` except `index.html`.
Source: https://docs.versasuite.com (96 data dictionary pages + 1 index).

## Output Files

- `data-dictionary.json` — Array of table objects, each containing:
  - `file_name`, `table_name`, `page_title`, `csv_file_name`
  - `prefix` (AP_, AX_, HC_, EM_, FQ_, VE_)
  - `domain_hint` (inferred from prefix/title)
  - `columns[]` with `original_name`, `expanded_name`, `description`
  - `column_count`, `has_patient_id`, `has_encounter_id`, `has_audit_fields`
  - `description_quality` ("good", "mixed", "poor")
- `data-dictionary-summary.json` — Accounting/coverage summary with parse
  stats, distribution counts, and failure details.

## Known Parsing Limitations

- HTML structure is inconsistent across pages (some have `<html>` wrappers,
  some are bare `<h1><table>` fragments). The parser handles both.
- No data types are documented in the source HTML — only column name,
  expanded name, and text description.
- Domain inference is heuristic based on table prefixes and title keywords.
- Some descriptions are AI-generated placeholders ("Provides information
  related to...") which are flagged in quality assessment.
