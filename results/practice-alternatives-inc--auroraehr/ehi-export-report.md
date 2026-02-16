# Practice Alternatives, Inc. — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://www.practice-alt.com/AuroraEHR_b10_EHI_Export_Documentation.pdf
- CHPL IDs: 11128
- Product: AuroraEHR v2.1
- Certification date: 2022-12-27

## Navigation Journal

The registered URL is a direct PDF download. No navigation was required.

```bash
# Probe URL
curl -sI -L "https://www.practice-alt.com/AuroraEHR_b10_EHI_Export_Documentation.pdf" \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
# → HTTP/2 200, Content-Type: application/pdf, Content-Length: 718676

# Download
curl -sL "https://www.practice-alt.com/AuroraEHR_b10_EHI_Export_Documentation.pdf" \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36' \
  -o downloads/AuroraEHR_b10_EHI_Export_Documentation.pdf
# Verified: PDF document, version 1.4, 39 pages, 718,676 bytes
```

No embedded URLs, no attachments, no links to additional documentation within the PDF. The PDF was created 2023-11-30 using PDF24 and last modified 2024-12-22.

## What Was Found

AuroraEHR provides a **39-page PDF** that is a genuine, dedicated (b)(10) EHI export documentation — not a repackaged FHIR API guide. This is a proper EHI export feature built into the desktop application.

### Export Mechanism

- **Access path**: AuroraEHR > Data Export
- **Single-patient export**: Privileged users (Administrator, Billing Manager, Clinical Manager, Front Office Manager) select patients from a browse list, choose data categories, and export. Up to 10 patients per export run.
- **Population export**: Available by request to gvti@practice-alt.com; uses the same format.
- **Output format**: A ZIP file placed on the user's desktop, named `[userid]-dataExport-[practice code]-[datetime].zip`.

### Export Structure

The ZIP contains per-patient subfolders, each with CSV files and PDF reports. Additionally, three subfolders (Documents, Scans, Reports) hold actual files (PDFs, images, etc.) when the Documents/Scans/Reports category is selected.

The screenshot on page 5 shows the actual file listing inside an export:
- `AccountNotes.csv`, `Allergies.csv`, `Appointments.csv`, `ClinicalInstructions.csv`, `ClinicalNotes.csv`, `ClinicalProgressNotes.csv`, `Documents.csv`, `Immunizations.csv`, `Reports.csv`, `ReviewOfSystems.csv`, `Scans.csv`
- `ImagingOrders.pdf`, `LabOrders.pdf`, `PathologyOrders.pdf`, `TherapyOrders.pdf`
- `Documents/`, `Reports/`, `Scans/` subfolders with actual files

### Data Categories Available for Export

The user can select from these categories on the export screen:

| Category | Format | Contents |
|----------|--------|----------|
| **Account Data** | PDF (report) | Demographics, contacts, employment, services, associated providers/lawyers, billing info (balances, statements), clinical info (diagnoses, injury history, disability), overrides, audit details, emergency contact, account contacts, payors, employers, charges/payments |
| **Charges/Payments** | 3 CSVs | `Charges.csv` (service dates, CPT codes, diagnoses, amounts, balances, modifiers, claim numbers), `Payments.csv` (deposits, remit types, financial class, payor), `ChargeTransactions.csv` (billing audit trail) |
| **Notes/Instructions** | 3 CSVs | `AccountNotes.csv` (billing, medical, family, surgery notes), `ClinicalInstructions.csv`, `ClinicalProgressNotes.csv` (signed progress notes, amendments, orders) |
| **Appointments** | CSV | Date, time, duration, reason, provider, location, kept/fail status, remarks |
| **Documents/Scans/Reports** | 3 CSVs + files | `Documents.csv` (medical reports, referral documents, patient instructions) with actual PDF files; `Scans.csv` (imported images/files in original format); `Reports.csv` (external clinical reports, summaries of care) with actual files |
| **Clinical Alerts** | CSV | Medically significant alerts, patient preferences, non-medical notes |
| **Allergies** | CSV | Allergen, onset, reaction, SNOMED code, severity, RXNORM code, status |
| **Immunizations** | CSV | Vaccine name/code, status, lot number, manufacturer, route, site, units, administered by/date/time, refusal reason |
| **Medications** | PDF (report) | Medication name, dose, duration, start/stop dates, refills, last fill date |
| **Problems/Diagnoses** | CSV | SNOMED code, ICD-10 code, description, onset date, resolved date, status (active/inactive/resolved/chronic) |
| **Review of Systems** | CSV | ROS text per appointment |
| **Social/Family/Surgical History** | 3 CSVs | `SocialHistory.csv` (pregnancy, LMP, IVDA, alcohol, abuse, smoking status with SNOMED), `FamilyHistory.csv` (condition, code, code system, affected family member), `SurgicalHistory.csv` (procedure code, code system, description) |
| **Orders: Tests and Results** | 4 PDFs | `ImagingOrders.pdf`, `LabOrders.pdf`, `PathologyOrders.pdf`, `TherapyOrders.pdf` — order number, instructions, date, test names, LOINC/CPT codes |
| **Vital Signs** | CSV | BP (systolic/diastolic/site/side), blood sugar, heart rate, height, weight, BMI, O2 saturation, supplemental O2, pain scale, respiratory rate, temperature, shoe size |
| **Additional Clinical Data** | Multiple CSVs | `ImplantedDevices.csv` (UDI, manufacturer, model, serial, placement details, MRI safety), `PatientEducation.csv`, `PostAppointment.csv` (post-encounter follow-up), `PostOp.csv` (detailed post-op measures — Aldrete-style scoring for activity, respiration, consciousness, O2 saturation, vascular assessments), `PreOp.csv` (pre-op baseline measures), `PreopProcedureNotes.csv` (consent, access sites, anxiety reduction, catheter placement, antibiotics), `ProviderOrders.csv` (puncture sites, discharge disposition, referrals, functional/cognitive status, medication administration, heparin dosing), `SurgicalChecklist.csv`, `SutureInfo.csv` |

### Field-Level Documentation Quality

Each CSV and PDF report is documented with a table listing every column/field, a description of what it contains, and for coded fields, the complete list of possible values (e.g., allergy severity levels, immunization statuses, smoking status SNOMED codes, appointment kept/fail values, charge statuses, transport methods, etc.). Data types are implicit from descriptions (e.g., "Formatted MM/dd/yyyy", "Numeric value", "Yes or no"). Relationships between entities are expressed via `Account#` and `Accession#` (appointment ID) foreign keys that appear consistently across all CSVs.

## Export Coverage Assessment

### Data Domain Coverage

**Clearly covered — with field-level documentation:**
- **Demographics & contacts** — full account data including name, DOB, SSN, address, ethnicity, language, employment, emergency contacts, account contacts
- **Insurance/payors** — all account payors exported
- **Billing & financial data** — charges (CPT codes, diagnosis codes, amounts, balances, modifiers, claims), payments (deposit dates, financial class, remit types, payor details), charge transactions (audit trail). This is a major strength — many vendors omit billing entirely
- **Clinical notes** — account notes (billing, medical, surgery, family), clinical instructions, progress notes with amendment tracking and signature verification
- **Medications** — full medication list with dosing, duration, refills
- **Allergies** — coded (RXNORM, SNOMED) with severity and status
- **Immunizations** — comprehensive with vaccine codes, lot numbers, manufacturer, route, site, refusal reasons
- **Problems/Diagnoses** — dual-coded (SNOMED + ICD-10) with onset/resolved dates and status
- **Vital signs** — extensive (BP with site/side, height, weight, BMI, O2 sat, pain scale, respiratory rate, temperature, blood sugar)
- **Lab/imaging/pathology/therapy orders** — with LOINC and CPT codes
- **Documents, scans, and external reports** — actual files exported, not just metadata
- **Implanted devices** — full UDI data, manufacturer, model, serial, MRI safety
- **Social/family/surgical history** — structured and coded
- **Review of systems** — text per appointment
- **Pre-op and post-op data** — remarkably detailed (Aldrete scoring, vascular assessments, consent, catheter placement, heparin dosing, sutures, surgical checklists)
- **Appointments** — date, time, duration, reason, provider, location, kept/fail status
- **Patient education** — material given, with URLs and timestamps
- **Provider orders** — including discharge disposition, referrals, functional/cognitive status
- **Clinical alerts** — medically significant flags and patient preferences

**Potentially absent or unclear:**
- **E-prescribing data**: Medications are exported as a report (PDF), but there's no mention of prescription transmission records, pharmacy details, or Surescripts data. The product research notes e-prescribing capability is unclear.
- **Lab results**: Orders are exported (with LOINC codes), but **result values** are not explicitly documented. The `LabOrders.pdf` documents order number, instructions, date, test name, and LOINC code — but there's no mention of result values, reference ranges, or interpretations. This is a significant gap if the system stores discrete lab results. External lab reports received may be captured in the Reports category as imported files.
- **Care plans**: The product research mentions "care plans and patient education materials" as a feature. Patient education is exported, but there's no explicit care plan category or CSV.
- **Patient portal communications**: The research notes a patient portal with secure messaging. No portal communication data appears in the export categories.
- **Consent records**: The iPad app supports consent signing. While `PreopProcedureNotes.csv` has "Verbal Consent Obtained From," there's no general consent document export beyond what might be captured in the Scans/Documents folders.

### Export Format & Standards

The export uses a **pragmatic, vendor-native format**: a ZIP archive containing CSV files for structured data, PDF reports for certain categories (medications, orders), and original-format files for documents/scans/reports. This is not FHIR, not C-CDA, not a standardized format — and that's appropriate for (b)(10).

**Strengths of this format:**
- CSV is universally readable and requires no special tooling
- The Account# and Accession# keys provide clear relationships between files
- Actual documents (PDFs, images) are exported in their original format, not degraded
- The format captures the full granularity of the data, not a summary

**Weaknesses:**
- No formal schema (no XSD, JSON Schema, or DDL). The documentation is the schema.
- Medications and orders are exported as PDFs rather than structured CSV, reducing machine-readability. The text indicates these are searchable PDFs, but structured data would be preferable.
- No explicit encoding specification (presumably UTF-8, but not stated)
- No version header or metadata file in the export itself

### Documentation Quality

This is **above-average documentation** for a small vendor:

- **Clear, navigable structure**: 39 pages organized by export category, each with a table of field names and descriptions
- **Field-level definitions**: Every CSV column and PDF searchable field is documented with an explanation
- **Value sets**: Coded fields include complete enumeration of possible values (e.g., all 16 immunization status values, all 12 immunization administration sites, all smoking status codes with SNOMED)
- **Screenshots**: The document includes actual screenshots of the export UI, the export completion dialog, and the file structure of an exported ZIP
- **Format specifications**: Date and time formats are explicitly stated for most fields (e.g., "Formatted MM/dd/yyyy", "Formatted hh:mm:ss am")
- **Operational guidance**: Clear instructions on who can perform exports, how to filter patients, the 10-patient limit, and how to request population exports
- **Audit note**: The document notes that exports are individually audited per patient

**What could be improved:**
- No sample export files or worked examples
- Data types are implicit rather than explicit (no "integer", "string", "date" type column)
- No cardinality information (can a patient have multiple rows in Allergies.csv? Yes, implied but not stated)
- The "[add screenshot of windows explorer showing directories and files of an export]" placeholder on page 4 suggests the document was partially auto-generated, though the screenshot does appear on page 5

### Structure & Completeness

- **Granularity**: Field-level documentation with descriptions and possible values — this is good for a PDF-based spec
- **Coded fields**: Value sets are documented inline, though not as separate machine-readable artifacts
- **Relationships**: Account# (patient) and Accession# (appointment) serve as foreign keys across all CSVs. The Exported File Path fields in Documents/Scans/Reports CSVs link metadata rows to actual files
- **Versioning**: No version history or changelog in the document. PDF metadata shows creation 2023-11-30, last modified 2024-12-22

### (b)(10) vs (g)(10) Assessment

This is a **genuine (b)(10) export** — not a repackaged FHIR API. The evidence:
- The export format is vendor-native (ZIP/CSV/PDF), not FHIR
- It includes billing data (charges, payments, charge transactions) which goes well beyond USCDI/US Core
- It includes specialty clinical data (pre-op/post-op assessments, surgical checklists, vascular assessments, heparin dosing) that have no standard FHIR mapping
- The export is performed through the desktop application, not via an API
- There is no mention of FHIR resources, US Core profiles, or Bulk Data endpoints anywhere in the document

This vendor has done real (b)(10) work. The export covers a broad range of clinical and financial data domains with field-level detail that goes far beyond what a FHIR-only approach would capture.

### Overall Assessment

AuroraEHR's EHI export documentation is **substantive and well-executed for a small regional vendor**. The documentation clearly describes a purpose-built export feature that covers the vast majority of data domains the product stores. The combination of structured CSV data, PDF reports, and actual file export (documents, scans, external reports) provides a comprehensive patient record.

The most notable gap is the apparent absence of discrete lab/imaging result values — the export includes orders but may rely on imported external report files (in the Reports category) rather than structured result data. This may reflect the product's architecture (a small ambulatory EHR that receives results as documents from external labs rather than storing discrete values). The absence of care plans and patient portal communications as explicit export categories is a minor gap.

The billing data coverage is a particular strength. Many vendors — including much larger ones — fail to include charges, payments, and financial data in their (b)(10) exports. AuroraEHR exports three separate CSVs with detailed billing and payment records.

The level of specialty clinical detail (pre-op/post-op assessments, surgical checklists, suture info, vascular assessments) is impressive and reflects real investment in capturing the product's full data scope, not just checking a compliance box.

## Access Summary
- Final URL (after redirects): https://www.practice-alt.com/AuroraEHR_b10_EHI_Export_Documentation.pdf
- Status: found
- Required browser: no
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends
None. The URL was a clean, direct PDF download with no authentication, redirects, or anti-bot measures.
