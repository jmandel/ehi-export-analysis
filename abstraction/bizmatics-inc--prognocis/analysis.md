# EHI Export Analysis: Bizmatics Inc.

**Product**: PrognoCIS
**Analysis date**: 2026-02-16
**CHPL IDs**: 8856 (Denali 3.1, certified 2017-09-29), 11738 (v4.0, certified 2025-12-24)

## 1. Product Context

PrognoCIS by Bizmatics Inc. is a cloud-based integrated EHR/EMR and practice management platform targeting small-to-mid-sized ambulatory practices across 30+ specialties. It is a single unified product (not a modular suite) encompassing:

- **Clinical documentation**: Customizable templates for 30+ specialties, CPOE, e-prescribing (including EPCS), lab/radiology ordering and results, clinical decision support
- **Practice management**: Scheduling, referral management, pre-authorization tracking, real-time insurance eligibility
- **Medical billing/RCM**: Integrated billing with claim creation, scrubbing, submission, payment posting, AR management, denial tracking, own clearinghouse (Secure Connect)
- **Patient portal**: Secure messaging, intake forms, appointment scheduling, prescription refill requests, lab result viewing
- **Document management**: "Attach Center" for scanned/faxed documents, PrognoFax electronic faxing
- **Telemedicine**: Built-in HIPAA-compliant video conferencing
- **Reporting**: Clinical quality measures, financial analytics, customizable dashboards

This product stores extensive clinical, billing, administrative, and patient engagement data. A complete EHI export should cover all of these domains.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/b-10-EHI-Export_PrognoCIS-Support.pdf` | 26-page PDF, primary EHI export documentation (678 KB). Self-attestation document dated Dec 2023 for version Denali 3.1. Contains workflow instructions, data element checklist (47 types), and field-level data dictionary. | **Most informative** — sole source of export content detail |
| `downloads/b-10-EHI-Export_PrognoCIS-Support.txt` | Plain text extraction via `pdftotext` (890 lines, 45 KB). Clean extraction with minor footer/header noise. | Input for parsing |
| `downloads/macra-page-top.png` | Screenshot of the MACRA compliance page hosting the PDF link (1.0 MB). | Context only |
| `downloads/macra-page-ehi-section.png` | Screenshot of the EHI export section on the MACRA page (1.0 MB). | Context only |
| `downloads/enrichment/data-dictionary.json` | Prior agent's structured JSON extraction of the data dictionary (47 elements, 1180 fields). | Reference; verified against own parse |
| `downloads/enrichment/extract-data-dictionary.ts` | TypeScript script used for prior extraction. | Reference for parsing approach |
| `product-research.md` | Product capabilities research. | Baseline for coverage assessment |

## 3. Export Mechanics

- **Format**: ZIP file containing XLS (Excel) + TXT files for structured data, PDF files for documents/notes, and HTML/XML (C-CDA) for CCD export. One file per data element type.
- **Mechanism**: UI-driven for single patient; vendor-assisted for population export
  - **Single patient**: User with `CuresEHIExport` role searches for patient, selects checkboxes for data types, clicks EXPORT. Background processing with email notification. Download via Settings → Configuration → Download Files → "Cures EHI Export"
  - **Patient population**: Must contact Bizmatics Data Migration Team (`support@bizmaticsinc.com`). Vendor handles extraction depending on "size of data, time and efforts required to manage the server resources."
- **Single-patient vs bulk**: Single patient is self-service; bulk requires vendor assistance (compliance concern per §170.315(b)(10)(ii) which requires population export capability)
- **Access constraints**: Requires `CuresEHIExport` role assignment. No fees mentioned. Population export has vendor dependency.
- **No API**: Export is purely UI-driven; no programmatic/API access documented.

## 4. Export Content: What's In It

The export documentation is a single 26-page PDF containing a data dictionary for **47 data element types** with **1,180 total fields** across **40 entities with discrete field lists**. The remaining 7 entities are document-only exports (PDFs), CCD exports, or report exports without discrete field enumeration.

**Documentation depth is shallow at the field level**: Fields are listed by name only. There are **zero field descriptions**, **zero data type annotations**, **zero value set definitions**, and **no foreign key/relationship documentation**. A developer would need to examine actual export data to understand field semantics, types, and relationships.

### Vendor's own content organization

The vendor organizes the 47 data elements into four categories:

| Category | Entities | Fields | Description |
|---|---|---|---|
| Reference/Provider Data (#1–7) | 7 | 177 | Insurance companies, providers, referring doctors, adjusters, attorneys, employers, guarantors |
| Patient Clinical Data (#8–38) | 31 | 603 | Demographics, insurance, clinical records, documents, encounters, medications, labs, vitals, codes |
| Patient Administrative/Case Data (#39–42) | 4 | 62 | Workers' comp cases, patient notes, alerts, past appointments |
| Billing Data (#43–47) | 5 | 338 | Ledger, claims, charges, patient advances, statements |

**Top entities by field count:**

| Entity | Fields | Category | Export Type |
|---|---|---|---|
| Billing Claims | 185 | Billing Data | Structured data |
| Patient Demographics | 131 | Patient Clinical Data | Structured data |
| Billing Charges | 123 | Billing Data | Structured data |
| Enc Progress Notes | 63 | Patient Clinical Data | Structured data + documents |
| Patient Insurance | 60 | Patient Clinical Data | Structured data |
| Patient Cases | 41 | Patient Administrative/Case Data | Structured data |
| Lab Test Result Values | 38 | Patient Clinical Data | Structured data |
| Adjusters | 33 | Reference/Provider Data | Structured data |
| Procedure Orders | 33 | Patient Clinical Data | Structured data |
| Medics | 31 | Reference/Provider Data | Structured data |
| Consults | 30 | Patient Clinical Data | Structured data |
| Patient Advance | 30 | Billing Data | Structured data |
| Referring Doctor | 28 | Reference/Provider Data | Structured data |
| Employers | 25 | Reference/Provider Data | Structured data |
| Lab Results | 23 | Patient Clinical Data | Structured data |

**Entities without discrete field lists (7):**

| Entity | Export Type | Notes |
|---|---|---|
| Legal Documents (#18) | Document files only | PDFs with file paths |
| Other Documents (#19) | Document files only | PDFs with file paths |
| Enc Attach Docs (#20) | Document files only | PDFs with file paths |
| Old Progress Notes (#21) | Document files only | PDFs with file paths |
| CCD (#28) | CCD export | HTML + XML (C-CDA) |
| Billing Ledger (#43) | Report export | Ledger for run date, billed claims only |
| Statements (#47) | Document files only | Latest patient statement as PDF |

**Notable data points from the documentation:**

- Billing Claims (185 fields) includes claim-level detail: transaction type, batch info, billing/rendering provider, subscriber, insurance sequence, ICD codes, place of service, amounts (bill, insurance, RP, write-off, balance), dates, and more. UB04 data is explicitly excluded.
- Patient Demographics (131 fields) is comprehensive — likely covering far more than USCDI demographics requirements.
- Billing Charges (123 fields) covers line-item billing detail with procedure codes, modifiers, amounts, and posting information.
- Enc Progress Notes (63 fields) includes encounter metadata, multiple doctor roles (attending, rendering, referring, supervisor) with IDs/NPI/taxonomy, plus document attachments.
- Patient Cases (41 fields) covers workers' compensation with injury details, WCAB#, case managers, and approved amounts — genuine specialty/administrative data.
- Messages (#22) has only 5 fields (ID, Date, Subject, Notes, Sender) — very thin and unclear whether this captures patient portal secure messages.
- Only active patient details are exported (deleted encounters can optionally be included).
- Void claims and void charges are not exported.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor organizes exports into four categories. The **Billing Data** category is the strongest signal that this is a genuine EHI export — 338 fields across 5 entities, with Billing Claims alone having 185 fields. This depth goes far beyond any USCDI or C-CDA repackaging.

**Reference/Provider Data** (7 entities, 177 fields): Complete reference data for the entities involved in patient care and billing — insurance companies, providers, adjusters, attorneys, employers, guarantors. These supporting entities are critical for reconstructing the full patient record.

**Patient Clinical Data** (31 entities, 603 fields): Broad clinical coverage including demographics, insurance, vitals, diagnoses, procedures (CPT/HCPC), prescriptions, lab results, radiology results, immunizations, family history, social history, allergies, medications, encounters, progress notes, procedure notes, consults, letters, and health maintenance. Document types (legal docs, other docs, encounter attachments, old progress notes) are exported as PDF files.

**Patient Administrative/Case Data** (4 entities, 62 fields): Workers' comp cases with detailed injury/case management data, patient notes, alerts, and past appointments.

**Billing Data** (5 entities, 338 fields): Claims, charges, patient advances, ledger, and statements. Notably deep and detailed.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | Patient Demographics (131 fields) | Very thorough — 131 fields far exceeds USCDI requirements |
| Encounters / visits | ✅ Covered | Enc Progress Notes (63 fields), Future Appointments (18), Past Appointments (17) | Detailed encounter data with multiple provider roles |
| Problems / conditions / diagnoses | ✅ Covered | Diagnosis Codes (11 fields) | Adequate |
| Medications / prescriptions | ✅ Covered | Current Medication (18 fields), Prescriptions (20 fields) | Covers active meds and Rx history |
| Allergies | ✅ Covered | Allergy (13 fields) | Adequate |
| Immunizations | ✅ Covered | Vaccination (18 fields) | Adequate |
| Vitals | ✅ Covered | Vitals (11 fields), All Vitals (11 fields) | Two separate exports; adequate |
| Lab results | ✅ Covered | Lab Results (23 fields), Lab Test Result Values (38 fields) | Detailed with both summary and discrete values |
| Imaging / diagnostic reports | ✅ Covered | Rad Results (21 fields) | Radiology results included |
| Procedures | ✅ Covered | CPT Codes (10 fields), HCPC Codes (10 fields), Procedure Orders (33 fields), Procedure Notes (3 fields + PDFs) | Multiple procedure-related entities |
| Clinical notes / documents | ✅ Covered | Enc Progress Notes (63 fields + PDFs), Old Progress Notes (PDFs), Legal Documents (PDFs), Other Documents (PDFs), Enc Attach Docs (PDFs), Letters (16 fields + PDFs) | Extensive document export |
| Care plans / goals | ❌ Not covered | No care plan entity | PrognoCIS likely stores care plans; gap |
| Orders / referrals | ⚠️ Partial | Procedure Orders (33 fields), Consults (30 fields) | Orders and consults covered; referral tracking workflows not as a separate entity |
| Insurance / coverage | ✅ Covered | Patient Insurance (60 fields), Insurance Master (22 fields) | Thorough |
| Claims / billing | ✅ Covered | Billing Claims (185 fields), Billing Charges (123 fields), Billing Ledger | Very detailed — strongest non-clinical coverage |
| Payments | ✅ Covered | Patient Advance (30 fields), data within Billing Claims | Patient advances and claim payment data |
| Consents / directives | ⚠️ Partial | Legal Documents (PDFs only, no structured fields) | Documents exported but no structured consent data |
| Patient communications / portal messages | ⚠️ Partial | Messages (5 fields: ID, Date, Subject, Notes, Sender) | Very thin; unclear if this includes patient portal secure messages or just internal messages |
| Specialty-specific (workers' comp) | ✅ Covered | Patient Cases (41 fields with injury details, WCAB#, case managers) | Genuine specialty data |
| Family history | ✅ Covered | Family History (7 fields) | Present but thin |
| Social history | ✅ Covered | Social History (11 fields) | Adequate |
| Health maintenance | ✅ Covered | Health Maintenance (7 fields) | Present but thin |
| Surgery history | ✅ Covered | Surgery (6 fields) | Present but thin |

**Summary**: 17 of 19 applicable domains have at least some coverage. Care plans/goals are absent. Patient communications and consents are thin/partial.

## 6. Documentation Quality

**Overall: Moderate — functional for understanding scope but inadequate for implementation.**

**Strengths:**
- All 47 data element types are enumerated with descriptions of what each covers
- 40 of 47 have explicit field name lists (1,180 total fields)
- Workflow documentation explains how to trigger exports with screenshots/steps
- Notes about data filtering (active patients only, void claims excluded) set expectations
- Role-based access control documented (`CuresEHIExport` role)

**Weaknesses:**
- **No field descriptions**: All 1,180 fields are names only — no explanations of what each field contains
- **No data types**: No indication of string, date, numeric, boolean for any field
- **No value sets**: Coded fields (Status Code, Type, etc.) have no enumerated values
- **No relationships/foreign keys**: No documentation of how entities relate (e.g., how a Billing Claim links to an Encounter)
- **No sample data**: No example export files provided
- **No machine-readable schema**: No XSD, JSON Schema, or DDL
- **Document titled "Self Attestation Document"**: Suggests compliance-driven rather than developer-facing documentation
- **A developer could not build an import from this documentation alone** — they would need actual export data and significant reverse engineering

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

PrognoCIS has built an export that demonstrably covers the breadth of data the product stores. The strongest evidence is the billing domain: Billing Claims (185 fields), Billing Charges (123 fields), and Patient Advance (30 fields) represent deep, detailed billing data far beyond anything in USCDI or standard clinical exchange formats. Additionally, workers' compensation case data (41 fields with injury details, attorneys, adjusters) demonstrates export of specialty/administrative data. The clinical coverage spans 31 data element types covering demographics, encounters, medications, labs, vitals, imaging, immunizations, procedures, clinical documents, and more. Reference data (insurance companies, providers, employers, guarantors) rounds out the record. The only notable gap is care plans/goals, and patient communications are thin — but relative to what this ambulatory EHR stores, the export covers the vast majority of domains.

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly a purpose-built export, not a repackaged clinical exchange. Key evidence:
- The format is XLS/TXT/PDF — not FHIR, not C-CDA (except for the optional CCD element)
- The data dictionary documents 47 internal data element types that map to the product's database structure
- Billing data is front and center (308+ fields across claims, charges, and advances)
- Workers' comp case management data, adjusters, attorneys, and employers are exported
- The documentation makes no reference to USCDI, US Core, or FHIR resources as the organizing principle
- The export includes reference/master data (Insurance Master, Medics, Employers) alongside patient data

### Key Findings

1. **Genuine (b)(10) export with real billing depth**: Billing Claims (185 fields) and Billing Charges (123 fields) are among the most detailed billing exports seen. This is not a USCDI repackaging — the vendor clearly exports from internal database tables.

2. **Broad coverage across 47 data element types**: The export spans clinical, billing, administrative, and reference data with 1,180 total fields. This covers the majority of what an ambulatory EHR stores about patients.

3. **Documentation is breadth-over-depth**: While all 47 data types are enumerated with field names, there are zero field descriptions, zero data types, zero value sets, and zero relationship documentation. A developer cannot build an import from this documentation alone.

4. **Population export requires vendor assistance**: The bulk/population export is handled by Bizmatics' Data Migration Team, creating a dependency that may conflict with the (b)(10) requirement for exports "without subsequent developer assistance."

5. **Patient communications are thin**: The Messages entity has only 5 fields (ID, Date, Subject, Notes, Sender), and it's unclear whether this captures patient portal secure messaging — a gap for a product with a patient portal.

### Summary Stats

    Coverage:        Comprehensive
    Approach:        Purpose-built EHI export
    Export format:   XLS/TXT (structured data), PDF (documents), HTML/XML (CCD)
    Entities:        47
    Fields:          1,180
    Descriptions:    0% (field names only, no descriptions)
    Sample data:     No
    Bulk export:     Vendor-assisted only
    Domains covered: 17 of 19 applicable domains (care plans absent, communications thin)

### Bottom Line

PrognoCIS provides one of the more credible (b)(10) exports in terms of data breadth — 47 data element types including deeply detailed billing (185 claim fields, 123 charge fields) and specialty data (workers' comp cases). However, the documentation quality is poor: 1,180 fields are listed by name only with no descriptions, types, or relationships, making the export usable but not well-documented. The biggest structural concern is that population export requires contacting the vendor's Data Migration Team, potentially undermining the self-service requirement of (b)(10).
