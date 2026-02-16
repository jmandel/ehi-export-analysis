# Enrichment: PracticeStudio EHI Export Documentation

## Run Command

```bash
cd /home/jmandel/hobby/ehi-export-analysis/results/microfour-inc--practicestudio/downloads/enrichment
bun run extract-fhir-docs.ts
```

## Input Boundary

- `../ExportProcess.html` — the registered (b)(10) EHI export page
- `../Interoperability.html` — interoperability education page listing CCD sections
- `../fhir-api-docs/*.html` — 17 FHIR API documentation pages (g)(10) API docs)

## Output Files

- `fhir-docs-extracted.json` — structured extraction containing:
  - Export process content (the single paragraph describing CCD-based mass export)
  - CCD sections list (16 sections documented)
  - FHIR resource documentation (17 resources with parameters, endpoints, examples)
  - Coverage/accounting metrics

## Known Parsing Limitations

- FHIR doc pages use JavaScript-rendered content; some sections may only be
  partially captured from the server-rendered HTML
- Parameter table extraction is heuristic and may miss complex table layouts
- The export process page has extremely minimal content (one paragraph)
