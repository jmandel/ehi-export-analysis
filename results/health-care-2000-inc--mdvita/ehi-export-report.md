# Health Care 2000, Inc. — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://www.hc2000inc.com/Pages/MDVita_EHR_EHI_DataFormat.pdf
- CHPL IDs: 11000
- Product: MDVita, Version 27
- Certification date: 2022-10-20

## Navigation Journal

The registered URL is a direct PDF download. No navigation required.

```bash
curl -sI -L "https://www.hc2000inc.com/Pages/MDVita_EHR_EHI_DataFormat.pdf" \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
```

Response: HTTP/2 200, Content-Type: application/pdf, Content-Length: 478386 bytes. No redirects. The PDF was downloaded directly:

```bash
curl -sL "https://www.hc2000inc.com/Pages/MDVita_EHR_EHI_DataFormat.pdf" \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36' \
  -o MDVita_EHR_EHI_DataFormat.pdf
```

Verified: `file` confirms "PDF document, version 1.7, 28 page(s)". Author: Luis Martinez. Created with Microsoft Word 2021, dated January 12, 2024. The document itself is dated September 19, 2023 (Guide version 1.2).

## What Was Found

The PDF is a 28-page EHI Export Data Format specification titled "MDVITA Electronic Health Information. Export format" (Guide version 1.2, MDVita version 27). It explicitly states it is written to comply with 170.315(b)(10) and the Information Blocking act.

### Export Format

The export produces three groups of files:

1. **Raw Data** — Apache Parquet format files (e.g., `Patient.parquet`). This is the structured tabular data.
2. **SOAP Notes** — Clinical notes exported as individual PDF files (machine-readable, programmatically generated). An index file (`SOAPNotesIndex.parquet`) maps notes to patients. The naming convention is `CareEventID_MemberID.pdf`.
3. **Documents** — Exported in their original uploaded format (PDF, XML, HTML, CSV, DOC, JPG, etc.). An index file (`DocumentsIndex.parquet`) maps documents to patients. Named by `DocumentID.ext`.

SOAP Notes and Documents are delivered via time-limited Azure Blob Storage URLs (valid 14 days). Reference files (`SOAPNotesReferences_XXX.csv` and `DocumentsReference_XXX.csv`) contain `FileName,FileDownloadURL` columns for automated download.

### Data Files Documented

The PDF provides field-level documentation for **24 Parquet data files** covering:

| # | File | Domain | Fields |
|---|------|--------|--------|
| 1 | Patients | Demographics | 27 fields — MemberID, DOB, gender, name, SSN, address, employer, race, ethnicity, language, transport needs, death info |
| 2 | ProviderNetwork | External providers | 18 fields — PhysID, NPI, taxonomy, name, address, DEA, UPIN, TaxID |
| 3 | ProviderPCPs | In-house providers | 18 fields — same structure as ProviderNetwork but for in-house PCPs |
| 4 | Locations | Service locations | 14 fields — NPI, TaxID, name, address, CLIA number, appointment interval |
| 5 | PatientPlans | Insurance/plans | 21 fields — plan enrollment, insurance company, LOB, copay amounts, effective/term dates |
| 6 | Appointments | Scheduling | 18 fields — date/time, provider, status, transportation details, special needs |
| 7 | SOAPNotesIndex | Clinical notes index | 9 fields — CareEventID, service date, attending physician, subject, comments |
| 8 | Orders | Clinical orders | 11 fields — referrals, tests, lab orders, text instructions, results |
| 9 | ProblemList | Diagnoses | 9 fields — ICD codes (ICD9/ICD10/SNOMED), status (active/inactive/resolved), dates |
| 10 | Allergies | Allergies | 9 fields — name, class (drug/environmental/substance), NDC/SNOMED/UNII codes, status |
| 11 | MedicationList | Medications | 20 fields — brand/generic name, strength, NDC, SIG, route, frequency, dosage |
| 12 | ProcedureList | Procedures | 5 fields — CPT code, dates |
| 13 | DocumentsIndex | Documents index | 12 fields — name, type, binder, service date, parent binder |
| 14 | LabResults | Lab results | 18 fields — ordering provider, SNOMED codes, result values, reference ranges, status |
| 15 | Claims | Claims/encounters | 55+ fields — claim type, billing provider, diagnoses, procedures with charges, modifiers, EPSDT, place of service, NDC drug info |
| 16 | Referrals | Referrals | 35+ fields — referral type/urgency, certification, authorization, service dates, diagnosis codes, clinical notes status |
| 17 | Emails | Internal messages | 11 fields — activity threads, patient association, body, importance |
| 18 | Immunizations | Immunizations | 17 fields — CVX code, vaccine name, manufacturer, lot, administered amount, refusal reason |
| 19 | Vitals | Vital signs | 7 fields — vital name, unit of measure, two value columns |
| 20 | DocumentSignatures | Signature audit | 4 fields — document ID, signed date, user login |
| 21 | ClaimInsurancePayments | Payer payments/EOBs | 23 fields — check info, CPT paid amounts, allowed amounts, copay, deductible, coinsurance, reason codes |
| 22 | MemberCharges | Patient charges | 8 fields — charge amount, date, reason, reversal date |
| 23 | MemberPayments | Patient payments | 12 fields — payment amount, type, check number, e-payment details, reversal |
| 24 | DocumentAnnotations | Document annotations | 5 fields — resolution notes, annotation body, dates |

Each file is documented with column name, data type (Numeric, String, DateTime, Boolean, Date), and a description. Coded fields include possible values (e.g., gender codes, order types, claim types, referral urgency levels, result statuses).

### Key Design Choices

- **Parquet format** is an unusual and technically strong choice — it's a columnar binary format with embedded schema, widely supported by data engineering tools (Python/pandas, R, Spark, DuckDB). It preserves data types natively.
- **Documents delivered by reference** via time-limited Azure Blob URLs is a practical approach for potentially large document sets.
- **Relationships are documented**: The data dictionary consistently cross-references files (e.g., "See Patients data file", "See ProviderPCPs data file") and identifies join keys (MemberID/PatientID, CareEventID, MemberPlanID, PhysID, etc.).
- The document notes that PatientID and MemberID are used "indistinctively" as the same patient account identifier.

## Export Coverage Assessment

### Data Domain Coverage

This is a genuinely comprehensive (b)(10) export that goes well beyond the USCDI clinical core. It covers:

**Clearly covered:**
- Patient demographics (comprehensive — name, DOB, SSN, address, employer, race, ethnicity, language, transport needs, death info)
- Insurance/plan enrollment with copay details and line of business
- Appointments with transportation logistics and special needs
- Clinical notes (SOAP Notes as PDFs + structured index)
- Orders (referrals, tests, labs, text instructions)
- Problem lists with ICD9/ICD10/SNOMED codes and status tracking
- Allergies with NDC/SNOMED/UNII codes
- Medications with full prescription detail (NDC, SIG, route, frequency, dosage)
- Procedures (CPT-coded)
- Lab results with SNOMED-coded observations and reference ranges
- Documents in original format with annotations
- Claims and encounters (extremely detailed — 55+ fields including billing provider info, procedure-level charges, modifiers, place of service, drug NDC, EPSDT)
- Referrals with full authorization/certification detail
- Immunizations with CVX codes and manufacturer info
- Vital signs
- Document signatures (audit trail)
- Insurance payments and EOBs (check-level and procedure-level detail)
- Patient charges and payments (including electronic payment details and reversals)
- Internal emails/messages between MDVita users about patients

**Potentially missing or unclear:**
- **Audit logs** — There is a DocumentSignatures file tracking document review events, but no general system audit log (login events, record access, modifications). The (d) certification criteria require audit logging, so this data exists in the system but may not be included in the export.
- **Clinical decision support alerts/interactions** — Drug-drug and drug-allergy interaction checking is a certified feature, but alert history is not explicitly in the export.
- **Quality measure data** — The product supports CQM tracking and QRDA generation, but quality measure results are not an explicit export file.
- **E-prescribing transaction history** — Medications are exported but specific e-prescribing transmission logs are not mentioned.
- **Patient portal activity** — The product has a patient portal (with third-party component), but portal-specific activity data is not in the export.
- **Scheduling templates/configuration** — While appointments are exported, the scheduling configuration (provider schedules, appointment types) is not.

Overall, the coverage is strong. The export captures the core clinical record, the full billing/financial lifecycle (claims, insurance payments, patient charges, patient payments), referral management, and internal communications. This is clearly a purpose-built (b)(10) export, not a repurposed FHIR API.

### Export Format & Standards

- **Format**: Apache Parquet for structured data, PDF for clinical notes, original format for uploaded documents. CSV reference files for document download URLs.
- **Standard**: Parquet is a well-established open-source columnar storage format (Apache Foundation). It is not a healthcare-specific standard but is a strong technical choice for bulk data export — it preserves data types, is self-describing, and is efficiently queryable.
- **Not FHIR**: This is explicitly a database-level export, not a FHIR-based export. This is appropriate given the breadth of data (billing, referral authorization, internal messaging) that doesn't map cleanly to FHIR resources.
- **Relationships**: Cross-file references are documented through shared identifiers (MemberID, CareEventID, PhysID, MemberPlanID, etc.). A third party could reconstruct the patient record by joining across these files.
- **Terminology**: The export uses standard code systems where applicable — ICD-9/ICD-10/SNOMED for diagnoses, CPT for procedures, NDC for drugs, CVX for vaccines, NPI for providers — while using internal codes for operational fields.

The format is well-suited to the data. A developer with Parquet tooling could load and query this export straightforwardly.

### Documentation Quality

- **Readable and well-organized**: Each data file gets its own numbered section (sections 3–26) with a consistent table format of Column Name, Data Type, and Description.
- **Field-level definitions**: Every column in every file is documented with a name, data type, and description.
- **Coded values documented**: Where fields have enumerated values, the possible values and their meanings are listed (e.g., gender codes, order types, claim types, referral urgency, result statuses, accident codes, bill frequency codes, EPSDT conditions, release of medical records codes, certification types, payment action codes).
- **Cross-references**: Relationships between files are explicitly noted ("See Patients data file", "See ProviderPCPs data file").
- **No sample data**: There are no example Parquet files or sample records included. The Azure Blob URL examples in the document use illustrative but non-functional URLs.
- **No export instructions**: The document directs users to "the MDVita User Guide for instructions how to schedule an EHI export" which is available within the application. The user guide for triggering the export is not publicly available.
- **Versioned**: Guide version 1.2, dated September 2023, for MDVita version 27. The PDF file itself was last modified January 12, 2024.

A developer could implement an import of this data based on this documentation. The Parquet format is self-describing (column names and types are embedded), so the documentation serves as a human-readable reference rather than the sole schema source.

### Structure & Completeness

- **Granularity**: Field-level documentation with column names, data types, and descriptions for all 24 data files.
- **Data types**: Specified for every field (Numeric, String, DateTime, Boolean, Date).
- **Value sets**: Coded fields include enumerated values with descriptions.
- **Relationships**: Join keys and cross-file references are documented.
- **Cardinality**: Not explicitly documented (no mention of required vs. optional fields, or one-to-many relationships), though the structure implies cardinality (e.g., Claims has procedure-level fields suggesting claim-line detail is denormalized into the claim record).
- **No formal schema**: There is no separate machine-readable schema file (e.g., JSON Schema, Avro schema). However, since Parquet files embed their schema, the actual export files would be self-describing.
- **No change history**: The document has a version number (1.2) but no changelog.

## Access Summary
- Final URL (after redirects): https://www.hc2000inc.com/Pages/MDVita_EHR_EHI_DataFormat.pdf
- Status: found
- Required browser: no
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends

None. The registered URL returned the PDF directly with no redirects, no authentication, and no anti-bot measures. This is the cleanest possible access pattern.
