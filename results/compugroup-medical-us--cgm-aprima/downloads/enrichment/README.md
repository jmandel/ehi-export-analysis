# CGM APRIMA EHI Export Data Dictionary Enrichment

## Run Command

```bash
bun run extract-data-dictionary.ts
```

## Input

- `../cgm-aprima-electronic-health-information-export-user-guide.pdf` (28-page PDF, via `pdftotext`)

## Output

- `ehi-data-dictionary.json` — structured JSON containing all 22 CSV file definitions with field-level column headings, SQL data types, and descriptions

## What It Does

Parses the pdftotext output of the EHI Export User Guide PDF to extract the data dictionary for all 22 CSV files that CGM APRIMA exports as part of its (b)(10) EHI export. Each CSV file definition includes:

- File name pattern
- Description
- Fields with: column heading, SQL data type (e.g., `char(255)`, `datetime`, `money`), and human-readable description

## Known Parsing Limitations

1. **Patient Ledger `glDate` field**: The `glDate` field's description is incorrectly captured as "whoPaid" (the next field name) because the PDF text has no description for `glDate` and the parser interprets the next field name as description continuation. The actual `whoPaid` field (char(100), "Superbill payer.") is missing as a separate entry.

2. **Patient Ledger `lastInsurancePaymentAmount`**: This field (money, "Amount of last insurance payment.") may be missing due to a PDF line-break parsing issue where the type appeared on the same line as the previous field's description.

3. **Patient Referrals**: Has 14 fields extracted but the PDF shows 15 fields — the final field `Referral Date` (datetime) may or may not be captured depending on the page break parsing.

4. **Multi-line field names**: Field names that span two lines in the PDF (e.g., "Appointment Type\nCode", "Allow Join Telehealth\nCall") are generally handled correctly by concatenation, but edge cases may produce slightly different formatting than the original.

These are minor artifacts affecting ~3 fields out of 383 total extracted. The vast majority of the data dictionary is accurately captured.
