# IHS RPMS EHI Schema Enrichment

## Run Command

```bash
cd downloads/enrichment
bun run extract-schema.ts
```

## Input Boundary

Parses all `BREH_OIT_*.txt` JSON schema files from the parent `downloads/` directory:
- `BREH_OIT_20230607.txt` (5.6 MB, 296 files)
- `BREH_OIT_20240703.txt` (5.7 MB, 298 files)
- `BREH_OIT_20250714.txt` (5.8 MB, 301 files)

## Output Files

| File | Description |
|------|-------------|
| `schema-summary.json` | Overview of all 3 schema versions with metadata, file counts, field counts |
| `files-catalog.json` | Complete catalog of all 301 patient files/tables from latest schema, with all 8,415 field definitions including types, constraints, pointer references, and value sets |
| `pointer-files.json` | All 548 reference/lookup tables with their field references |
| `field-types.json` | Field type distribution across the schema with sample fields per type |
| `schema-diff.json` | Version-to-version diffs showing added files and field count changes |
| `coverage-stats.json` | Parsing accounting (files discovered/parsed/failed) plus domain categorization of all 301 files |

## Known Parsing Limitations

- The script extracts top-level field definitions from each file's `"0"` entry. Deeply nested subfile structures (multiples within multiples) are flagged with `hasSubfields: true` but their internal fields are not recursively enumerated.
- The `WORD PROCESSING` vs `WORD-PROCESSING` type distinction reflects inconsistency in the source schema — both are preserved as-is.
- Domain categorization in `coverage-stats.json` uses keyword heuristics and may miscategorize edge cases (e.g., "Clinical - Other" is a catch-all for files that don't match pharmacy, lab, behavioral health, dental, or immunization patterns).
