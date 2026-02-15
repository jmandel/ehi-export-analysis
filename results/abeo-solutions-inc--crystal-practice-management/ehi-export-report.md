# Abeo Solutions, Inc — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://www.crystalpm.com/21stCenturyCuresActB10AllDataExportUserDocumentation2.pdf
- CHPL IDs: 10996
- Product: Crystal Practice Management v6.0
- Certification date: 2022-10-04

## Navigation Journal

The registered URL is a direct PDF download. No navigation required.

```bash
# Probe URL
curl -sI -L "https://www.crystalpm.com/21stCenturyCuresActB10AllDataExportUserDocumentation2.pdf" \
  -H 'User-Agent: Mozilla/5.0'
# Returns HTTP/2 200, Content-Type: application/pdf, Content-Length: 2680793

# Download
curl -sL "https://www.crystalpm.com/21stCenturyCuresActB10AllDataExportUserDocumentation2.pdf" \
  -H 'User-Agent: Mozilla/5.0' \
  -o downloads/21stCenturyCuresActB10AllDataExportUserDocumentation2.pdf

# Verify
file downloads/21stCenturyCuresActB10AllDataExportUserDocumentation2.pdf
# PDF document, version 1.7, 921 page(s)
```

The filename suggests this is version 2 of the documentation. A check for version 1 at the same path without the "2" suffix returned HTTP 404.

## What Was Found

A single, massive 921-page PDF titled **"CrystalPM 21st Century Cures Act B.10 All Patient Data Export Documentation"**. Created October 12, 2023 using Microsoft Word 2021, authored by "Erik."

### Export Format

The export produces **CSV files** — one per database table. Some columns containing serialized complex objects use "CSV + Binary Deserialization," meaning the raw column contains XML data that has been further serialized to binary; the export process deserializes these back to their structured form. The overview states:

> "This feature is meticulously designed to facilitate the secure and efficient export of all patient data strictly in CSV file formats, ensuring the optimal utility and interoperability of health information."

### Document Structure

The PDF is essentially a **complete database data dictionary** for the Crystal PM system. For each of the 55 distinct database tables included in the export, it provides:

1. **Table description** — a paragraph explaining the table's purpose
2. **Column-level documentation** in tabular format with four columns:
   - **Column Name** — the database field name
   - **Data Type** — MySQL data types (int, varchar, char, date, datetime, bigint, longblob, tinyint, etc.)
   - **Description** — a prose description of what the column stores
   - **Extraction Method** — either "CSV" for simple columns or "CSV + Binary Deserialization" for serialized blob columns

3. **Serialized type documentation** — for tables with XML-serialized blob columns (particularly `ehr_file` and `mcs`), the PDF additionally documents the object model types and their member fields. This includes .NET-style type names like `VisualAcuityFieldDataModel`, `RefractionMeasurementFieldDataModel`, `TargetSiteType`, `DataCategoryType`, etc.

### Tables Documented (55 distinct tables)

**Patient & Demographics:**
- `patients` — core patient demographics, contact info, financial balances, insurance

**Clinical/EHR Data (via `ehr_file` table, with 20+ sub-types):**
- Lab Orders, Lab Results, Lab Result CCR
- Immunizations
- Medication Orders, Medication History, Formulary
- Drug Allergies, Drug Allergy History, Drug Interactions, Drug F9
- Problems (internal and external), Medications (external), Drug Allergies (external)
- Observations, Procedures, Smoking Status, Implantable Devices
- Interventions, Diagnostic Studies, Devices
- Clinical Notes (`clinical_note`)
- **Eye Care Data** — with detailed VisualAcuityFieldDataModel and RefractionMeasurementFieldDataModel type documentation

**Prescriptions & Medication:**
- `mcrx` — MedComp RX (prescription data)
- `mcs` — MedComp (medication collection data with XML serialization)
- `mcs_log` — MedComp Log

**Billing & Financial:**
- `invoice` — patient invoices
- `inv_trans_items` — invoice transaction line items
- `trans_pay` — transaction payments
- `trans_data` — transaction data
- `hcfa_print` — HCFA (CMS-1500) claim print records
- `hcfa_data` — HCFA claim data
- `rslip` — routing slips

**Insurance (VSP-specific):**
- `vsp_claims`, `vsp_claim_response`, `vsp_claim_services`
- `vsp_authorizations`, `vsp_auth_services`, `vsp_auth_servicegrid`
- `vsp_eligibility`, `vsp_eligibility_benefits`, `vsp_eligibility_services`
- `frame_for_vsp` — frame data for VSP claims

**Optical & Inventory:**
- `framepage` — frame page data
- `fp_log` — frame page log
- `cl_log` — contact lens log
- `contorders` — contact lens orders
- `inv_log` — inventory log
- `clrx_notes` — contact lens RX notes
- `sprx_notes` — spectacle RX notes

**Scheduling & Appointments:**
- `appts` — appointments
- `appt_waitlist` — appointment waitlist
- `appt_log` — appointment log

**Patient Engagement & Communication:**
- `recall` — patient recall records
- `reminders` — reminders
- `rem_log` — reminder log
- `directmail_message` — direct mail messages
- `pat_markets` — marketing records
- `comments` — patient comments

**Documents & Images:**
- `med_image_info` — medical image metadata
- `med_image_data` — medical image binary data
- `pat_file` — patient file metadata
- `pat_file_data` — patient file binary data
- `pat_photo_info` — patient photo metadata
- `pat_photo_data` — patient photo binary data
- `pat_photos` — patient photos
- `pat_ins_card` — patient insurance card metadata
- `ins_card_info` — insurance card info
- `ins_card_data` — insurance card binary data

**Administrative:**
- `alerts` — patient alerts
- `hippadisc` — HIPAA disclosure log
- `authlogs` — authorization logs
- `mu_measures` — Meaningful Use measures
- `order_groups` — order groups
- `result_groups` — result groups
- `pro_refrl` — professional referrals

## Export Coverage Assessment

### Data Domain Coverage

This is an impressive (b)(10) implementation for a small vendor. The export clearly attempts to dump the **entire database** — not just clinical data, and not just USCDI elements. Specific coverage:

**Well-covered domains:**
- **Patient demographics** — comprehensive, including family relationships, communication preferences, financial balances
- **Clinical records** — the `ehr_file` table (with 20+ sub-types) covers lab orders/results, medications, allergies, problems, procedures, observations, immunizations, smoking status, implantable devices, interventions, diagnostic studies
- **Eye care-specific data** — visual acuity measurements, refraction measurements with full serialized data model documentation including TargetSiteType, DataCategoryType — this is genuinely specialty-specific data that goes beyond USCDI
- **Billing/financial** — invoices, transactions, payments, HCFA/CMS-1500 claims, routing slips
- **Vision insurance (VSP)** — claims, authorizations, eligibility, benefits — very detailed vision plan billing data
- **Optical/inventory** — contact lens orders and logs, frame data, spectacle RX notes, inventory logs
- **Scheduling** — appointments, waitlists, appointment logs
- **Documents and images** — medical images, patient files, patient photos, insurance cards — all with both metadata and binary data
- **Patient engagement** — recall, reminders, marketing, direct messages, comments
- **Administrative** — HIPAA disclosures, authorization logs, alerts, referrals

**Potentially missing or unclear:**
- **User/employee data** — the `empid` foreign key appears in many tables, but there's no `employees` table in the export. Staff information that contextualizes who did what is absent.
- **Scheduling configuration** — room assignments, multi-location setup, scheduling templates are not in the export
- **System configuration** — custom templates (the 300+ EHR templates), form definitions, custom procedures, ICD/CPT code mappings
- **Kiosk data** — check-in data, form submissions from Crystal Kiosk
- **Text messaging logs** — Crystal Communicator SMS logs don't appear as a distinct table (may be in `reminders` or `directmail_message`)
- **Audit trails** — beyond `authlogs`, there's no general audit log of user actions
- **Fee schedules** — no fee schedule table despite billing functionality
- **Practice analytics/reports** — saved reports or analytics data

### Export Format & Standards

- **Format**: CSV files — one per database table — with binary deserialization for complex serialized columns
- **Standard**: This is a **proprietary database dump**, not FHIR, C-CDA, or any standard format. This is entirely appropriate for (b)(10) — a CSV dump of the full database is exactly the right approach for exporting "all electronic health information"
- **Relationships**: Foreign keys are documented implicitly (e.g., `acctid` in every table links to `patients.acctid`, `empid` references employees), but there's no formal relationship diagram or ERD
- **Serialized data**: Some columns contain XML-serialized .NET objects that are binary-encoded in the database. The export deserializes these. The document goes to the trouble of documenting the object model types and their members (e.g., `VisualAcuityFieldDataModel`, `RefractionMeasurementFieldDataModel`), which is unusually thorough
- **Could a third party reconstruct records?** Mostly yes. The column descriptions are sufficient to understand most data. The serialized types for eye care data are well-documented. The main gap is understanding the coded values — many integer columns (e.g., `type` in `ehr_file`) represent categories but the valid values and their meanings aren't always enumerated

### Documentation Quality

- **Readability**: The document is long (921 pages) but well-structured. Each table follows the same four-column format (Column Name, Data Type, Description, Extraction Method)
- **Data dictionary**: Yes — this IS a data dictionary. Every column in every exported table has a name, data type, and prose description
- **Data types**: MySQL data types are specified (int, varchar, char, date, datetime, bigint, longblob, tinyint)
- **Value sets**: Mostly not documented. Integer type columns (e.g., `type` field in `ehr_file`) are described as "category or classification" but the valid values aren't listed
- **Examples**: No sample export files or example records are provided
- **Developer usability**: A developer could build an import system from this documentation, though they'd need to discover coded value meanings through the data itself
- **Maintenance**: The PDF was created October 2023, and the naming convention ("Documentation2") suggests it's a revision of an earlier version. It appears to be a genuine maintenance effort

### Structure & Completeness

- **Granularity**: Field-level — every column has a name, type, and description. This is among the more granular data dictionaries we've seen
- **Coded fields**: Weakly documented. The descriptions mention that a field "represents a category" but don't enumerate the possible values
- **Relationships**: Implied through column descriptions (e.g., "The acctid column is a unique identifier for a patient in the 'patients' table") but no formal foreign key documentation or entity relationship diagram
- **Serialized types**: Impressively documented. The .NET object models for eye care data (visual acuity, refraction measurements) are broken down to their member fields with types and descriptions
- **Versioning**: The filename suggests version 2. No changelog within the document

### Overall Assessment

This is a **genuinely strong (b)(10) implementation** from a small vendor. Crystal PM has taken the right approach: rather than repurposing their FHIR API (which would only cover USCDI clinical data), they're exporting CSV dumps of their actual database tables — 55 of them — covering clinical data, billing, insurance, optical inventory, scheduling, documents, images, and eye care-specific measurements.

The standout feature is the documentation of serialized data types for eye care data. Many vendors would simply export a binary blob and leave the consumer to figure it out; Crystal PM documents the VisualAcuityFieldDataModel and RefractionMeasurementFieldDataModel down to their individual member fields.

The main weaknesses are: (1) no enumeration of coded values for integer type fields, (2) no sample data or examples, (3) no formal relationship documentation (ERD), and (4) some operational tables (employees, system configuration, scheduling setup) appear to be excluded. But for a 12-35 person company, the 921-page data dictionary is a serious effort that far exceeds what many larger vendors provide.

## Access Summary
- Final URL (after redirects): https://www.crystalpm.com/21stCenturyCuresActB10AllDataExportUserDocumentation2.pdf
- Status: found
- Required browser: no
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends
- Version 1 of the PDF (same URL without "2" suffix) returns HTTP 404
- No other obstacles encountered; direct PDF download worked cleanly
