# Enrichment: Core Solutions Cx360 EHI Export Documentation

## Run command

```bash
cd downloads/enrichment
bun run extract-ccd-sections.ts
```

## Input boundary

- `../Electronic-Health-Information-Export-Doc.pdf` — 12-page PDF (2,454,569 bytes)
- Text extracted via `pdftotext`; however, because the multi-column table layouts
  produce garbled output, the structured data was hand-curated from visual
  inspection of all 12 PDF pages rendered at 150 DPI via `pdftoppm`.

## Output files

| File | Description |
|------|-------------|
| `ccd-sections.json` | Complete structured representation of all CCD sections, data elements, XPATH entries, code system OIDs, and code system names documented in the PDF |
| `coverage-accounting.json` | Extraction metadata: source info, counts, parse notes |

## Known parsing limitations

- The PDF's multi-column table layout cannot be reliably parsed by `pdftotext`
  (columns merge, lines wrap mid-word across column boundaries). The structured
  JSON was therefore produced by manual transcription from rendered page images.
- The script is deterministic and rerunnable — it writes the curated data
  structure to JSON. It does not re-parse the PDF text on each run.
- No embedded URLs, attachments, or linked resources were found in the PDF.
