# Enrichment: FHIR Example Extraction from Althea EHI Documentation PDF

## Run Command

```bash
cd downloads/enrichment
bun run extract-fhir-examples.ts
```

## Input

- `../AltheaEHIDocumentation.pdf` — 108-page PDF containing FHIR JSON examples for each exported resource type

## Process

1. Extracts text from PDF using `pdftotext`, stripping form-feed page break characters
2. Locates section headings after the table of contents (using "Below sections list the supported FHIR resources" as content start marker)
3. Extracts JSON blocks from each section via brace-matching parser that handles nested objects, arrays, and string escaping
4. Parses JSON and extracts FHIR resources (handles standalone resources, Bundle entries, and link+resource wrappers)
5. Deduplicates by resourceType + id within each section

## Output Files

- **`fhir-examples.json`** — Array of extracted FHIR resource examples, each with:
  - `section`: The PDF section heading it came from
  - `resourceType`: FHIR resource type
  - `id`: Resource ID (if present)
  - `json`: Full parsed FHIR JSON object
- **`extraction-summary.json`** — Extraction accounting: section counts, resource type counts, and parse failures

## Results

- **52 FHIR examples** extracted across **13 resource types**
- Resource types: Patient (1), AllergyIntolerance (1), CarePlan (1), CareTeam (1), Condition (6), Goal (2), Immunization (4), MedicationRequest (1), Observation (30), Procedure (2), Claim (1), Coverage (1), ExplanationOfBenefit (1)
- 28 sections discovered, 23 produced examples, 5 had parse failures

## Known Parsing Limitations

1. **Implantable Device (Device)**: The UDI carrier HRF string value contains a literal `}` character that spans a line break in the PDF text extraction, breaking JSON structure. The Device example is present in the PDF but cannot be parsed from extracted text.
2. **Diagnostic Report**: Base64-encoded PDF data is explicitly truncated in the source document ("truncated for documentation"), making the JSON structurally incomplete.
3. **Document Reference**: Same issue — base64 data truncated, JSON incomplete. Multiple DocumentReference examples are affected.
4. **Observation Body Temperature**: The PDF section heading exists but contains no JSON example (empty section in the source document).
5. **Observation Body Weight**: Same as Body Temperature — section heading present but no JSON example provided.
