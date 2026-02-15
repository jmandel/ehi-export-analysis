# Medi-EHR Enrichment

## Run Commands

```bash
cd results/medi-ehr-llc/downloads/enrichment
bun run extract-api-docs.ts
```

## Input Boundary

- `../API_Document.html` — Pre-rendered Swagger UI page from Medi-EHR's developer portal (https://proda.mediemr.net:8443/i/mediemr/API_Document.html)

## Output Files

- `api-docs.json` — Structured extraction of all API endpoints, parameters, response formats, and error codes

## Known Parsing Limitations

- The API document HTML is a pre-rendered (static) Swagger UI page, not a live Swagger spec. There is no underlying OpenAPI JSON/YAML spec available.
- The error table uses Oracle APEX-style HTML classes; the regex accounts for these.
- The `mediehrgetpatientdata.php` endpoint block in the HTML reuses the `id` from `mediehrrotatetokens.php` (copy-paste artifact), so the deduplication logic uses path + summary as key.
- The USERNAME parameter appears twice in the `mediehrgetpatientdata.php` endpoint (a copy-paste error in the source docs); both instances are preserved in the extraction.
