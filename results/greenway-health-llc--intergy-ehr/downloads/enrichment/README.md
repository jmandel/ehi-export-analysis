# Intergy EHI Data Dictionary Enrichment

## Run Command

```bash
cd downloads/enrichment
bun run extract-tables.ts
```

## Input Boundary

Parses all `.htm` files in `../viewer/Contracts/` (261 table definition pages)
plus `../viewer/Contracts/include/DBDescriptions.js` for supplemental table
descriptions.

## Output Files

- **tables.json** — Full structured data dictionary with all tables, fields
  (name, datatype, default, null option, comment), parent table relationships,
  and child table relationships.
- **tables-summary.json** — Compact summary with table names, descriptions,
  field counts, relationship counts, and field name lists.
- **coverage-report.json** — Accounting: files discovered, files parsed,
  parse failures, and field count distribution.

## Known Parsing Limitations

- HTML parsing uses regex rather than a DOM parser. This works well for the
  uniform structure of these generated pages but could break if page structure
  varies significantly.
- Default values containing HTML entities beyond the common set (&nbsp; &amp;
  &lt; &gt; &quot;) may not be decoded correctly.
- The "No_Value__N_" default value pattern (used for boolean fields) is
  preserved as-is rather than decoded to "N".
