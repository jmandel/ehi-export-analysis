# Greenway Prime Suite EHI Export — Enrichment

## Run Commands

```bash
bun run extract-data-dictionary.ts
bun run extract-xml-reference.ts
```

## Input Boundary

- `extract-data-dictionary.ts` parses `../PrimeSuiteEHIExport_Data_Dictionary.html` (1.7 MB)
- `extract-xml-reference.ts` parses `../PrimeSuiteEHIExport_Document_Reference.html` (2.5 MB)

## Output Files

| File | Description |
|------|-------------|
| `data-dictionary.json` | All 1026 tables with columns, data types, nullable flags, and descriptions |
| `extraction-stats.json` | Parsing statistics and any failures for the data dictionary |
| `xml-reference.json` | All 19 document type sections with text content and embedded tables |
| `xml-reference-stats.json` | Parsing statistics for the XML reference |

## Known Parsing Limitations

- The XML reference document contains large base64-encoded inline images (diagram examples). These are replaced with `[image]` placeholders in the extracted text content.
- The XML reference's first table lists generic document type names without numeric IDs. The proprietary document format types (1005, 1016, etc.) are documented in heading-based sections rather than a single lookup table.
- Text content in `xml-reference.json` sections is truncated to 2000 characters per section to keep the output manageable.
