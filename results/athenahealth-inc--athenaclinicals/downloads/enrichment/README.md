# athenahealth EHI Export Documentation — Enrichment

## Run Commands

```bash
cd /home/jmandel/hobby/ehi-export-analysis/results/athenahealth-inc--athenaclinicals/downloads/enrichment
bun run extract-datasets.ts
```

## Input Boundary

Parses all `api-*.json` files in `../` (the downloads directory), excluding
`api-navigation.json` and `api-microsite.json` (structural metadata only).

These files are Contentful freeformPage entries fetched from the athenahealth
Document Portal API at `https://docs.athenahealth.com/v1/api/entries/freeformPage`.

Input files:
- `api-welcome-exports.json` — Overview page
- `api-ambulatory-clinical.json` — Ambulatory Clinical EHI Export page
- `api-ambulatory-collector.json` — Ambulatory Collector EHI Export page
- `api-inpatient-clinical.json` — Inpatient Clinical EHI Export page
- `api-inpatient-collector.json` — Inpatient Collector EHI Export page
- `api-release-notes.json` — Release Notes page

## Output Files

- `datasets.json` — Structured catalog of all export types, datasets, field
  specs, headings, and PDF download URLs
- `coverage.json` — Parsing accounting: files discovered, parsed, failures

## Structure of datasets.json

```
{
  extractionDate, source,
  totalApiFiles, totalExportTypes, totalDatasets, totalInlineSpecs,
  exportTypes: [{
    id, title, urlAlias, category, format,
    downloadPdfUrl,
    datasets: [{ name, specUrl, includesAttachments, source, category }],
    inlineSpecs: [{ datasetName, category, source, inputParameters, outputParameters }],
    headings: [string]
  }]
}
```

## Known Parsing Limitations

- The inpatient clinical page documents its 38 datasets as HTML templates
  in the PDF (not as API endpoint references like ambulatory). The inline
  HTML field specs from that PDF are not extracted by this script — they
  are only in the PDF text.
- Embedded entry content within "accordion" UI components (download buttons)
  is parsed for PDF URLs but not for rendered text content.
- The Contentful rich text structure uses `embedded-entry-block` for some
  tables; the script handles both direct `table` nodes and embedded table
  entries.
