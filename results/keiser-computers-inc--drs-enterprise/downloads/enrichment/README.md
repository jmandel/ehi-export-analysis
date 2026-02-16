# Enrichment: Drs Enterprise EHI Export Schema

## Run command

```bash
cd downloads/enrichment
bun run extract-export-schema.ts
```

## Input boundary

- `../Export_data.pdf` — the single 10-page EHI Export Documentation PDF from Keiser Computers

## Output files

- `export-schema.json` — Complete structured extraction of the export documentation including:
  - Export format and standard (C-CDA 2.1 / USCDv1)
  - Directory structure for exported data
  - 7 exported file types with descriptions
  - 7 XML entities with 71 total fields (name, type, description, optional flag)
  - 2 enumerators with 32 total values (convert_type, TFieldType)
  - XML examples for each entity
  - Fax export structure and files

## Known parsing limitations

- The PDF is a well-structured Word-generated document, so field tables were manually transcribed rather than parsed from pdftotext output (which loses table structure). All data was verified against the PDF visual rendering.
- The C-CDA content itself (account_ccda.xml) is documented by reference to the HL7 C-CDA 2.1 standard rather than with field-level detail in this vendor document. The enrichment captures only the vendor's proprietary XML sidecar formats.
