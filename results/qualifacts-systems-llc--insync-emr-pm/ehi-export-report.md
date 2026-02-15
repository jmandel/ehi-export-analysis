# Qualifacts Systems, LLC — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://documentation.qualifacts.com/ehi-export/platform/insync/insync-ehi-export.html
- CHPL IDs: 10858
- Product: Insync EMR/PM, Version 10
- Certification date: 2022-03-14

## Navigation Journal

1. **Initial probe**: `curl -sI -L "https://documentation.qualifacts.com/ehi-export/platform/insync/insync-ehi-export.html" -H 'User-Agent: Mozilla/5.0'` returned HTTP 200 with `Content-Type: text/html; charset=utf-8`. Page is served behind Cloudflare but no challenge was presented. Final URL is the same as the registered URL (no redirects).

2. **Fetched page**: `curl -sL "https://documentation.qualifacts.com/ehi-export/platform/insync/insync-ehi-export.html" -H 'User-Agent: Mozilla/5.0' -o insync-ehi-export.html`. The page is a Sphinx-generated static HTML doc (Sphinx 7.0.1, Docutils 0.18.1). 9,900 bytes. It contains four sections: Single Patient Export, Patient Population Export, Accessing the EHI Export, and Technical Documentation (with File Types and Data Dictionary subsections).

3. **Identified downloadable artifacts**:
   - Data Dictionary: `https://documentation.qualifacts.com/ehi-export/_downloads/InSync_EHI_Export_Data_Dictionary.xls` (linked from the "Data Dictionary" section)
   - Terms of Use PDF: `https://documentation.qualifacts.com/ehi-export/_downloads/Qualifacts_EHI_Export_Terms_of_Use_SEP_2024.pdf` (linked from the Patient Population Export section)

4. **Downloaded Data Dictionary**: `curl -sL "https://documentation.qualifacts.com/ehi-export/_downloads/InSync_EHI_Export_Data_Dictionary.xls" -H 'User-Agent: Mozilla/5.0' -o InSync_EHI_Export_Data_Dictionary.xls`. Verified with `file` command: "Composite Document File V2 Document" (genuine XLS). 1,562,112 bytes. Author: subrata.choudhury, last saved by Rob Sipe, last saved 2025-11-17.

5. **Downloaded Terms of Use**: `curl -sL "https://documentation.qualifacts.com/ehi-export/_downloads/Qualifacts_EHI_Export_Terms_of_Use_SEP_2024.pdf" -H 'User-Agent: Mozilla/5.0' -o Qualifacts_EHI_Export_Terms_of_Use_SEP_2024.pdf`. Verified: PDF document, version 1.7, 3 pages. 148,904 bytes.

6. **Checked parent index page**: `curl -sL "https://documentation.qualifacts.com/ehi-export/index.html"`. This is the Qualifacts Systems EHI Exports hub page linking to three platforms (CareLogic, Credible, InSync). No additional InSync-specific resources were found beyond the platform-specific page.

7. **Enrichment**: Created a Bun TypeScript script to extract the XLS data dictionary into queryable JSON. Script parses all 84 sheets (81 data sections after skipping 3 metadata sheets), extracts 960 fields with full metadata. Zero parse failures. Output: `data-dictionary.json` (241 KB) and `extraction-stats.json` (15 KB).

## What Was Found

### Export Mechanism

InSync provides two EHI export modes:

1. **Single Patient Export**: Initiated by designated agency staff within the InSync application upon patient/authorized representative request. Produces a ZIP file containing a Newline Delimited JSON file and a "Supported File" folder for attachments.

2. **Patient Population Export**: Requested by submitting a ticket through the Qualifacts Care Center. Qualifacts staff initiates the process. Produces a ZIP containing one JSON file per patient, with all attachments in a shared "Supported File" folder. May take up to 30 calendar days to complete. Only one can be requested at a time, and requesting requires acceptance of the Qualifacts EHI Export Terms of Use.

Both exports are accessed through the requester's To Do list within InSync. Download links expire after 30 calendar days.

### Export Format

The export format is **Newline Delimited JSON** (NDJSON) — a vendor-defined flat JSON structure, not FHIR. This is a genuine (b)(10) export format, not a repackaging of the (g)(10) FHIR API. The documentation explicitly separates EHI export from FHIR API access (the parent page links to their FHIR API documentation separately).

Attachments (documents, images) are exported as physical files in a "Supported File" folder, linked to the patient JSON via the `DownloadedFilePath` field in the "Documents / Images" array. The page includes a JSON example showing this structure:

```json
"Documents / Images": [
    {
        "FileDescription": "Patient's Insurance Card",
        "FolderName": "Insurance Card",
        "FileType": "jpg",
        "FileCreationDate": "2023-09-06T05:21:39.97",
        "DownloadedFilePath": "~/Supported File/12345_Front_98765.jpg"
    }
]
```

### Data Dictionary

The data dictionary is the primary technical documentation artifact. It is an XLS file with 84 sheets:

- **3 metadata sheets**: Confidential Notice, INDEX (table of contents with category/module classification), Changelogs (7 versions from initial release through Sprint 69/USCDI v3.1, last updated November 2025)
- **81 data section sheets**, each documenting the fields exported for a specific data domain

Each data section sheet contains:
- A description of the section
- A field-level table with columns: Row #, Name of the Column, Data Type, Nullable, Used For (description), Remarks

The 81 sections cover **960 total fields**. Field data types include String, INT, Date, DateTime, and Boolean. The "Used For" column provides brief English descriptions. The "Remarks" column is sparsely populated.

### Changelog History

| Version | Date | Description |
|---------|------|-------------|
| 1 | 2023-09-13 | Initial Release |
| 2 | 2023-10-11 | Second release with new sections |
| 3 | 2023-10-15 | Third release with new sections |
| 4 | 2024-07-30 | Sprint 36 — new fields added |
| 5 | 2025-01-24 | Sprint 49 — Fractional Units in Patient Program |
| 6 | 2025-06-27 | Sprint 60 — Out-of-Pocket Payments in Collection Information |
| 7 | 2025-10-31 | Sprint 69 — changes related to USCDI v3.1 |

The dictionary file metadata confirms last save date of 2025-11-17.

## Export Coverage Assessment

### Data Domain Coverage

The InSync EHI export data dictionary demonstrates **remarkably broad coverage** across clinical and billing domains, which is notable for a (b)(10) compliance effort. Here is a domain-by-domain assessment, referencing the product research:

**Well-covered clinical domains:**
- **Patient demographics** (64 fields) — comprehensive, including SSN, race, ethnicity, preferred language, communication preferences, emergency contacts
- **Allergies** (11 fields) — includes RXCUI, SNOMED codes, severity, reactions
- **Problems/Diagnoses** (8 fields) — ICD codes, onset/resolved dates
- **Medications** (12 fields) — includes RXCUI, prescribing details, sig instructions
- **Immunizations** (18 fields) — CVX codes, manufacturer, lot numbers
- **Vital signs** (43 fields) — very detailed, including BMI, blood pressure, pulse ox, pain scale
- **Clinical notes** (13 fields) — encounter notes with provider, date, type
- **Lab results / Clinical tests** (12 fields) — LOINC codes, values, units, reference ranges
- **Procedures** (10 fields) — CPT/HCPCS codes, modifiers
- **Goals** (11 fields) — treatment goals with target dates and status
- **Care team members** (8 fields) — providers, therapists
- **Referrals** (6 fields) — referral tracking
- **Family health history** (15 fields) — conditions by family member
- **Medical devices** (14 fields) — implant details with UDI

**Well-covered billing/financial domains:**
- **Claims** (18 fields) — claim numbers, payers, submission dates, transmission types
- **Billing codes assigned** (3 fields) — CPT code linkage
- **Billing statements and summaries** (6 fields)
- **Charges, refunds, deductibles** (6 fields) — payment details
- **Collection information** (3 fields) — copay collection
- **Denials** (4 fields) — claim denials
- **Explanation of benefits** (8 fields) — ERA/payer remittance
- **Health insurance information** (46 fields) — very detailed payer coverage
- **Eligibility information** (6 fields)
- **Prior authorizations** (21 fields) — authorization tracking
- **Price estimates** (17 fields) — patient cost estimates
- **Financial assistance** (16 fields) — sliding fee scale
- **List of prices/charges** (2 fields)

**Specialty and behavioral health domains:**
- **Psychiatric history** (7 fields) — directly relevant to InSync's behavioral health focus
- **Behavioral data** (4 fields)
- **Substance abuse** (5 fields) — consumption details
- **Assessments and treatment plans** (7 fields) — treatment planning data
- **Social history** (13 fields for consumption, 2 for elements)
- **Smoking status** (8 fields)

**OB/GYN and specialty clinical data:**
- **Pregnancy information** (13 fields)
- **Newborn delivery** (26 fields)
- **Gynecological history** (18 fields)
- **Past pregnancy data** (19 fields)
- **Medical history (Ob/Gyn)** (13 fields)
- **Pregnancy intent** (2 fields), **Pregnancy status** (5 fields)

**Additional domains:**
- **Documents/images** (5 fields) — with physical file export
- **Additional/clinical forms** (4 fields) — custom forms
- **Custom fields** (2 fields) — demographic custom fields
- **Consents** (6 fields) — TPO, HIE, medication consents
- **Encounter information** (21 fields)
- **Patient relationships** (22 fields) — delegates, emergency contacts
- **Patient education** (6 fields)
- **Health concerns/reason for visit** (9 fields)
- **Functional status** (8 fields)
- **Patient summary and plan** (21 fields)
- **Diagnostic imaging** (20 fields)
- **Care setting histories**: Inpatient Hospice (7), Ambulatory Hospice (6), Palliative Care (6), Long Term Care (5)
- **Work information** (17 fields)
- **Surgical history** (9 fields)
- **Genetic history** (12 fields)
- **Medical history** (7 fields)
- **Nutrition and diet** (6 fields)
- **ROS** (8 fields), **Physical Exam** (7 fields), **Chief Complaints/HPI** (11 fields)
- **Health maintenance** (6 fields)
- **Referring diagnosis** (6 fields)
- **Patient pharmacy** (15 fields)
- **Program** (29 fields), **Case management** (40 fields)
- **Census data** (10 fields)
- **Organization** (20 fields), **Facility data** (8 fields), **Provider** (9 fields)
- **Credentialing records** (8 fields)
- **HL7 ADT notifications** (2 fields)
- **Provenance** (3 fields) — EHI export request tracking
- **Recorded sex or gender** (4 fields)
- **Review of results** (7 fields), **Special alerts for care handoffs** (10 fields)
- **Event logs** (12 fields) — audit trail (note: this is included in the export even though audit logs are not strictly EHI)

**Potentially missing or underrepresented domains:**

Based on the product research, InSync stores data for several features that are not clearly represented in separate data dictionary sections:

- **ePrescribing / EPCS data**: Medication prescriptions are in the Medications section, but specific ePrescribing transaction details (PDMP queries, controlled substance prescription records, pharmacy transmission status) are not explicitly broken out. Some of this may be captured in the Medications fields.
- **eMAR (electronic medication administration records)**: Not explicitly called out as a separate section, though it may be included within Medications or Clinical notes.
- **Telehealth session metadata**: No dedicated section for telehealth session records (video session details, session duration, participant info). These may be captured as encounter subtypes.
- **Secure messaging**: Patient portal secure messages are not explicitly listed as an exported data domain.
- **Patient portal activity**: Portal-specific data (login history, form submissions via portal) is not represented.
- **HL7 interface data**: Only "HL7 ADT notifications" (2 fields) is present — this is a narrow view of the interface capabilities.

These gaps are relatively minor and characteristic of a product that exports from its database rather than cherry-picking USCDI elements. Most of these data types may be subsumed within the broad sections (e.g., telehealth encounters within Encounter information, secure messages within Clinical notes or Documents).

### Export Format & Standards

The export uses a **vendor-defined flat JSON format** — not FHIR, C-CDA, or any recognized standard. This is appropriate for a (b)(10) export because:

1. The format is clearly designed to export the full breadth of InSync's data model, not just USCDI elements.
2. The field names are descriptive and self-documenting (e.g., `PatientFirstName`, `ClaimNumber`, `AllergiesRXCUI`).
3. The data dictionary provides adequate field-level documentation for a developer to parse the export.
4. Clinical codes (ICD, CPT, LOINC, RXCUI, SNOMED, CVX) are preserved in their standard coded forms.

The format is NOT standardized interoperability-ready (no FHIR, no C-CDA), which means a receiving system would need to build a custom import. However, this is expected for (b)(10) and is arguably more complete than a FHIR-only export would be.

There is no JSON Schema, OpenAPI spec, or other machine-readable format specification beyond the XLS data dictionary itself.

### Documentation Quality

**Strengths:**
- The data dictionary is extensive (81 sections, 960 fields) and covers both EMR and PM modules.
- Each field has a name, data type, nullable flag, and brief description.
- The INDEX sheet provides category/module classification for each section.
- The changelog shows active maintenance (7 versions over 2+ years, most recently November 2025 with USCDI v3.1 updates).
- The export page clearly separates single-patient vs. population export workflows.
- The JSON example for document/attachment linking is helpful.

**Weaknesses:**
- **No sample export file** — no example JSON showing a complete patient record. Only one JSON snippet for the Documents/Images array.
- **No JSON schema** — the data dictionary is in XLS format only. No machine-readable schema (JSON Schema, XSD, etc.).
- **Field descriptions are minimal** — the "Used For" column often just restates the column name (e.g., `PatientFirstName` → "Patient First Name").
- **No value sets documented** — coded fields (e.g., `AllergiesSeverityCode`, `PatientGender`, `TransmissionType`) do not specify the allowed values or code systems.
- **No relationship documentation** — the export appears to be a flat JSON structure per patient, but how the 81 sections relate to each other (e.g., which encounters link to which claims) is not specified.
- **No cardinality information** — which sections are arrays vs. single values is not documented (though the JSON example implies arrays).
- **The "Remarks" column is almost entirely empty** across all 960 fields.

### Structure & Completeness

The field-level documentation is at a **moderate** level of granularity:
- Field names: yes
- Data types: yes (String, INT, Date, DateTime, Boolean)
- Nullable: yes
- Brief descriptions: yes (though often tautological)
- Value sets/enumerations: no
- Relationships/foreign keys: no
- Cardinality: no
- Examples: no (except one JSON snippet)

A developer receiving an InSync EHI export could identify and parse the fields but would need to reverse-engineer the structure, relationships, and coded values from actual export data.

### Overall Assessment

This is a **genuinely strong (b)(10) implementation** that exports across the full breadth of InSync's clinical and billing data model using a vendor-native JSON format. It is clearly not a repackaging of the (g)(10) FHIR API — the export covers 81 distinct data domains including billing, insurance, financial assistance, case management, and specialty-specific clinical data that would not appear in a USCDI/US Core export.

The primary limitation is **documentation quality rather than export scope**. The data dictionary covers the right breadth of data but lacks the depth (value sets, relationships, examples, machine-readable schema) that would make it fully self-describing. A developer working with this export would need access to sample data to fill in the gaps.

The export is actively maintained (last updated November 2025 with USCDI v3.1 changes) and has evolved through 7 versions since its September 2023 initial release. The 30-day timeline for population exports and the Terms of Use requirement for population exports are notable operational constraints but not documentation gaps.

## Access Summary
- Final URL (after redirects): https://documentation.qualifacts.com/ehi-export/platform/insync/insync-ehi-export.html
- Status: found
- Required browser: no
- Navigation complexity: direct_link (one click to data dictionary download)
- Anti-bot issues: Cloudflare present but no challenge served; standard User-Agent header sufficient

## Obstacles & Dead Ends
- None. The documentation URL resolved directly, all linked artifacts downloaded without issues, and no authentication or bot challenges were encountered.
