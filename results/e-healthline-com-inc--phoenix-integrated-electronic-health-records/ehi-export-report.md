# E*HealthLine.com, Inc. — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: http://ehealthline.com/dev/pdf/Electronic%20Health%20Information%20Export.pdf
- CHPL IDs: 10832
- Product: Phoenix© Integrated Electronic Health Records v10.0.0
- Certification date: 2022-02-17

## Navigation Journal

The registered URL is a direct PDF download. No navigation was required.

```bash
# Probe URL — returns 200 with Content-Type: application/pdf, 265,837 bytes
curl -sI -L "http://ehealthline.com/dev/pdf/Electronic%20Health%20Information%20Export.pdf" \
  -H 'User-Agent: Mozilla/5.0'

# Download
curl -sL "http://ehealthline.com/dev/pdf/Electronic%20Health%20Information%20Export.pdf" \
  -H 'User-Agent: Mozilla/5.0' \
  -o downloads/Electronic_Health_Information_Export.pdf

# Verify: PDF document, version 1.4, 10 pages
file downloads/Electronic_Health_Information_Export.pdf
```

Additional checks performed:
- Directory listing at `http://ehealthline.com/dev/pdf/` returns 403 Forbidden (no browsable index)
- Vendor homepage (`http://ehealthline.com/`) has no links to EHI export documentation beyond the registered PDF URL
- Homepage links to interoperability products (ExChange, HIE) but none to EHI export or data dictionaries
- Transparency Disclosures PDF exists at the registered mandatory disclosures URL but is a regulatory filing, not export documentation
- No embedded URLs, attachments, or linked data files inside the PDF itself (confirmed via pdfdetach and text extraction)
- No screenshots of the export UI are embedded in the PDF — it is entirely text-based

## What Was Found

The registered URL provides a single 10-page PDF titled "170.315(b)(10) Electronic Health Information Export" (version 2.0, dated October 24, 2023). The document was created from a Word document via Acrobat Distiller. Notably, the footer on every page reads "170.315(g)(10) — Standardized API For Patient and Population services" — a clear copy-paste error from a different document template, though the body content is genuinely about (b)(10).

### Export Mechanism

The export is performed through the "Export Batch CCDA" option in the application's Data Maintenance Menu. The system supports:

1. **Single Patient Export**: User selects a provider, clinic, and patient (by name search or MR#), then clicks "Start Export." Options to include chart documents and sticky notes on TIF docs.
2. **Patient Population Export**: Same interface but allows selection of multiple patients or an MR# range.

Both exports produce a ZIP file saved to a network path (`\\SERVERNAME\BarcodeScans\HL7ExportFiles\CDAexports`), containing a file named `CDAXMLExport_8.Zip`.

### Export Format

The ZIP contains the following files/folders:

| Component | Format | Description |
|-----------|--------|-------------|
| **CCDA** | XML (HL7 C-CDA) | Clinical data compliant with USCDI v1 — standard C-CDA document |
| **BillingReport** | CSV | Financial transactions: patient info, dates, charges, claims, descriptions, status |
| **demographics** | CSV | Patient key info, ID details, contact info, insurance info |
| **Schedule** | CSV | Encounter records: appointment date, provider, location, type, workflow, notes, note dates |
| **Documents** | CDA XML folder | Supporting documents and attachments |
| **Notes** | CDA XML folder | All notes from previous medical visits/encounters |
| **PatientDocumentFiles** | CSV | Mapping file listing document attachments in the "Documents" folder |

### Access Control

EHI export is restricted to users with specific security role privileges: the admin user must grant `[Edit General Database Setup]` plus either `[Print Documents]` or `[Chart Reviewer]`.

### Custom Patient Data Tables

The system includes a mechanism for custom (user-created) Patient Data Tables. By default, all custom tables are included in the CDA export. Administrators can exclude specific tables from the Formal Health Record (FHR) via a "General Table Setup" option, which removes them from the export. This is a notable feature — it means the system can export custom/specialty data beyond standard USCDI, but also allows selective exclusion.

## Export Coverage Assessment

### Data Domain Coverage

**Clearly covered:**
- **Demographics** — dedicated CSV with patient info, identification, contact, insurance
- **Clinical data (USCDI v1)** — via C-CDA XML: problems, medications, allergies, lab results, procedures, vital signs, immunizations, care plans (standard C-CDA sections)
- **Billing** — dedicated CSV with transaction dates, charges, claims, descriptions, status
- **Encounters/Schedule** — dedicated CSV with appointment history, provider, location, type, workflow
- **Clinical notes** — dedicated folder with all notes from visits/encounters in CDA XML format
- **Documents/attachments** — dedicated folder with supporting documents, plus a CSV index file
- **Custom Patient Data Tables** — included in CDA export by default (configurable exclusion)

**Likely covered but not explicitly documented in detail:**
- **Prescriptions/medications** — would be in the C-CDA (standard section), but no separate export beyond C-CDA
- **Lab results** — mentioned in the file description text ("lab results") and would be in C-CDA
- **Procedures** — mentioned in file description text and in C-CDA
- **Allergies** — mentioned in file description text and in C-CDA
- **Images** — mentioned in file description text; unclear if actual image files (DICOM, etc.) are exported or just references

**Potentially missing or ambiguous:**
- **Prescribing detail** — the product includes E*Prescription (electronic prescribing with formulary checking, PDMP). Prescription data would be in the C-CDA medications section, but e-prescribing transaction details, pharmacy selection, formulary responses may not be captured
- **Patient portal messages** — the Patient Portal module supports messaging, file sharing, patient-entered health information. No mention of portal data in the export
- **Oncology-specific data** — the vendor offers an oncology variant (Phoenix Oncology EHR). Oncology-specific templates, protocols, and assessments may be captured via custom Patient Data Tables if configured, but this is not explicitly documented
- **Behavioral health data** — vendor lists a behavioral health variant. Same ambiguity as oncology
- **Imaging data** — the vendor has radiology (eRad/PACS) products. Whether actual images vs. references/reports are included is unclear
- **Care coordination data** — transitions of care, referrals. Some would be in C-CDA but detailed referral tracking may not be captured
- **Public health reporting data** — immunization data would be in C-CDA; syndromic surveillance, cancer registry submissions, and other public health data feeds may not be included in the patient-level export

### Export Format & Standards

The export uses a **hybrid approach**:
- **HL7 C-CDA XML** for clinical data (compliant with USCDI v1)
- **CSV files** for demographics, billing, schedule, and document mapping
- **CDA XML** for notes and supporting documents
- **ZIP packaging** for the complete export

This is a reasonable approach for (b)(10) — the vendor goes beyond just USCDI by including billing (CSV), scheduling (CSV), and document attachments alongside the standard C-CDA. The CSV files capture data domains that C-CDA does not naturally represent well (billing transactions, scheduling).

However, the reliance on C-CDA for the clinical core means the clinical export is limited to whatever the C-CDA template supports. USCDI v1 covers a defined subset — problems, medications, allergies, procedures, labs, vitals, immunizations, care plans, goals, assessments, clinical notes, and some social determinants. Specialty-specific data (oncology protocols, behavioral health assessments) would only appear if the custom Patient Data Tables mechanism injects them into the CDA.

The format is **not self-describing** — there is no schema definition, data dictionary with field names, or sample files provided. A recipient of the export would need to understand C-CDA to parse the XML, and would need to reverse-engineer the CSV column structure from the actual files.

### Documentation Quality

**Weak overall.** The documentation is a 10-page PDF that reads more like a user guide for performing the export than a technical specification of the export format. Key deficiencies:

- **No data dictionary**: There are no field-level definitions for any of the CSV files. We know BillingReport contains "patient information, transaction dates, charges, claims and the description of transactions," but we don't know the column names, data types, or possible values.
- **No CSV schema**: Column headers, delimiters, encoding, date formats, and null representations are not specified.
- **No sample data**: No example export files or sample records are provided.
- **No C-CDA profile documentation**: The C-CDA is described only as "USCDI v1 compliant." There is no documentation of custom sections, extensions, or how vendor-specific data (like custom Patient Data Tables) is encoded within the CDA.
- **No relationship documentation**: How the CSV files relate to each other (e.g., how BillingReport rows connect to encounters in Schedule) is not described.
- **Incomplete sentences**: The document has several truncated references — step 14 for single patient export says "For additional details on the export format and default paths," but the sentence ends with a comma and no link or continuation.

A developer attempting to import this data would be unable to write a parser based solely on this documentation. They would need an actual sample export to reverse-engineer the structure.

### Structure & Completeness

- **Granularity**: File-level only. The documentation names 7 components of the ZIP export but does not specify fields/columns for any of them.
- **Value sets**: Not documented. No coding systems, code lists, or enumerated values.
- **Relationships**: Not documented. No foreign keys or cross-references between CSV files.
- **Versioning**: Document has a revision history (v1.0 and v2.0, both October 2023), but no versioning of the export format itself.
- **Completeness indicators**: The document mentions "all the EHI" but never enumerates what "all" means in terms of specific data elements. The claim is aspirational rather than demonstrable.

### Overall Assessment

E*HealthLine has made a genuine attempt at (b)(10) compliance that goes beyond simply repackaging their (g)(10) FHIR API. The export includes billing data (CSV), scheduling data (CSV), clinical notes (separate from the C-CDA summary), and document attachments — none of which would be covered by a pure USCDI/FHIR approach. The custom Patient Data Tables inclusion mechanism shows awareness that specialty-specific data exists beyond USCDI.

However, the documentation is a **compliance checkbox** rather than a useful technical specification. It tells you *how to click the export button* but not *what the export contains at a field level*. The absence of any data dictionary, CSV schema, sample files, or C-CDA profile documentation makes it impossible to assess whether the export truly captures "all EHI" without obtaining an actual export and examining it. The truncated sentences and g(10) footer suggest the document was written hastily.

The vendor's overall web presence — poorly maintained site, injected spam on some pages, limited independent validation — is consistent with this documentation quality. The product was certified in February 2022 with b(10) documentation dated October 2023, suggesting the export documentation was added retroactively.

## Access Summary
- Final URL (after redirects): http://ehealthline.com/dev/pdf/Electronic%20Health%20Information%20Export.pdf
- Status: found
- Required browser: no
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends
- No obstacles encountered. The PDF downloaded cleanly on the first attempt.
- The PDF directory listing (`/dev/pdf/`) returns 403, so no other files could be discovered there.
- The vendor homepage has no navigation path to EHI export documentation; the registered URL is the only way to reach it.
- The PDF footer references "(g)(10)" throughout, which is a copy-paste error from a different document template.
- Steps 14 (single patient) and 15 (population) in the PDF say "For additional details on the export format and default paths," but trail off with no URL or reference — suggesting additional documentation may exist but is not publicly linked.
