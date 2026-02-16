# PrognoCIS EHI Export — Enrichment

## Run command

```bash
cd enrichment && bun run extract-data-dictionary.ts
```

Prerequisite: the text extraction must exist at `../b-10-EHI-Export_PrognoCIS-Support.txt`
(produced by `pdftotext ../b-10-EHI-Export_PrognoCIS-Support.pdf ../b-10-EHI-Export_PrognoCIS-Support.txt`).

## Input boundary

- **Source PDF**: `b-10-EHI-Export_PrognoCIS-Support.pdf` (26 pages, 678 KB)
- **Text extraction**: `b-10-EHI-Export_PrognoCIS-Support.txt` (pdftotext output)
- Only one file is parsed — this is the sole EHI export documentation artifact.

## Output files

- `data-dictionary.json` — Complete structured extraction of 47 data element
  types, their field lists, descriptions, file attachment info, and notes.

## Known parsing limitations

- 4 of 47 sections have no enumerated field list in the source PDF:
  - **Enc Attach Docs (20)**: Only describes file attachments, no discrete fields.
  - **CCD (28)**: Says "This contains the CCD details" with no field enumeration.
  - **Billing Ledger (43)**: Says "Exports the Ledger for Run Date" with no fields.
  - **Statements (47)**: Describes file output (PDF statements) but no discrete fields.
- Some field names may be slightly merged where the PDF text wraps
  mid-field-name (e.g., "Address Tel\nOffice1" becomes "Address Tel Office1").
- The PDF has page breaks that split field lists mid-sentence; these are cleaned
  but some footer residue may remain in descriptions.
