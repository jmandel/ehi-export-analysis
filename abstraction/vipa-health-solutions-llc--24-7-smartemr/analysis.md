# EHI Export Analysis: VIPA Health Solutions, LLC

**Product**: 24/7 smartEMR v7.2
**Analysis date**: 2026-02-16
**CHPL ID**: 11079 (15.04.04.2916.smar.07.02.1.221216)

## 1. Product Context

24/7 smartEMR is a cloud-hosted, web-based EMR and practice management system developed by VIPA Health Solutions, LLC (Miami, FL, ~11 employees). It targets physician offices and ambulatory clinics across a broad range of specialties — internal medicine, cardiology, dermatology, pediatrics, orthopedics, family medicine, and more. The product is marketed as a combined EMR + billing system.

**Key data domains the product stores** (based on product research, CHPL certification, and FHIR API documentation):

- **Clinical core**: Patient demographics, encounters, diagnoses/problem lists, medications (e-prescribing via Surescripts), allergies, immunizations, vitals, lab results (LabCorp/Quest integration), procedures, clinical notes, care plans, goals, care teams
- **Billing/revenue cycle**: CMS-compliant Superbill generation, electronic claims submission, insurance eligibility verification, E/M coding, fee schedules — described as the product's "best-known feature"
- **Documents**: Scanned/uploaded documents (lab reports, radiology, receipts), signed encounter notes
- **Scheduling**: Appointment management
- **Patient portal**: Patient-facing view/download/transmit
- **Specialty-specific**: Marketed as "specialty-specific" with customizable templates
- **Reporting**: Clinical quality measures (14 CQMs certified), public health reporting (immunization registry, syndromic surveillance)

The product is certified for 37 ONC criteria including (b)(10) EHI export, (g)(10) FHIR API, transitions of care, e-prescribing, and CQM reporting. This is a full-featured ambulatory EMR+PM system, and a compliant (b)(10) export should cover clinical, billing, and specialty data.

## 2. Artifacts Reviewed

All artifacts are hosted on `smartemr.readme.io` (ReadMe.io platform). No downloadable files (PDFs, ZIPs, schemas, sample data) are available anywhere on the site.

| # | Artifact | Source | Description | Informativeness |
|---|---|---|---|---|
| 1 | `electronic-health-information-export-b10.html` (92 KB) | [EHI Export page](https://smartemr.readme.io/docs/electronic-health-information-export-b10) | The sole EHI export documentation page. ~287 words of prose describing CDA export + document repository export. **No data dictionary, no schema, no sample data.** | ⭐ Primary — but extremely thin |
| 2 | `screenshot-ehi-export-page-full.png` (279 KB) | Screenshot | Full-page screenshot confirming page content and sidebar structure | Corroborative |
| 3 | `patient-demographics.html` (123 KB) | [Patient Demographic](https://smartemr.readme.io/docs/patient-demographics) | Data *import* specification: 30 fields with types, descriptions, max lengths | ⭐⭐ Most detailed data model |
| 4 | `insurance-information.html` (106 KB) | [Insurance Import](https://smartemr.readme.io/docs/insurance-information) | Import spec: 6 fields for insurance payer directory | Moderate |
| 5 | `cpt-and-fee-schedule.html` (100 KB) | [CPT and Fee Schedule](https://smartemr.readme.io/docs/cpt-and-fee-schedule) | Import spec: 2 fields (code + amount) | Minimal |
| 6 | `service-location.html` (104 KB) | [Service Location](https://smartemr.readme.io/docs/service-location) | Import spec: 10 fields including NPI, CLIA, Medicare | Moderate |
| 7 | `referring-physician.html` (100 KB) | [Referring Physician](https://smartemr.readme.io/docs/referring-physician) | Import spec: 3 fields (name, NPI) | Minimal |
| 8 | `scheduler-appointments.html` (103 KB) | [Appointments](https://smartemr.readme.io/docs/scheduler-appointments) | Import spec: 6 fields for appointments | Moderate |
| 9 | `document-upload.html` (110 KB) | [Document Upload](https://smartemr.readme.io/docs/document-upload) | Import spec: 12 fields for document uploads with category/subcategory | Moderate |
| 10 | `problem-list.html` (105 KB) | [Problem List](https://smartemr.readme.io/docs/problem-list) | Import spec: 5 fields (ICD-10-CM coded) | Moderate |
| 11 | `patient-allergies.html` (114 KB) | [Allergy & Intolerance](https://smartemr.readme.io/docs/patient-allergies) | Import spec: 11 fields with RxNorm/SNOMED CT standards | ⭐⭐ Best clinical data model |
| 12 | `immunization-records.html` (84 KB) | [Immunization Records](https://smartemr.readme.io/docs/immunization-records) | **Empty page** — exists in sidebar but contains no content | None |
| 13 | `enrichment/smartemr-data-models.json` (34 KB) | Prior agent extraction | Pre-parsed data models from import pages | Corroborative |
| 14 | `enrichment/smartemr-ehi-export.json` (2 KB) | Prior agent extraction | Structured extraction of EHI export page | Corroborative |

**Critical observation**: Artifacts 3–12 are all **data import** specifications (for onboarding/migration), not export documentation. They reveal what the product stores but tell us nothing about what the EHI export outputs. The only actual export documentation is artifact 1, which contains ~287 words and no field-level detail.

I verified the live EHI export page (fetched 2026-02-16) and confirmed it is identical to the downloaded artifact — no updates since collection.

## 3. Export Mechanics

The EHI export has two components:

### CDA Clinical Data Export
- **Format**: HL7 CDA (Clinical Document Architecture)
- **Mechanism**: UI-based — Admin Panel → Export Options → Patient Data → Create a backup/export
- **Single-patient**: Select individual patient(s), click "Create"
- **Bulk/population**: Click "Select All" patients, click "Create"
- **Options**: One-time or recurring schedule; filter by Date of Service
- **CDA spec**: Links to [HL7 CDA product page](https://www.hl7.org/implement/standards/product_brief.cfm?product_id=7) but does not specify which CDA template, implementation guide, or version is used (no C-CDA template OIDs, no conformance claims)

### Document Repository Export
- **Format**: PDF, JPG, PNG files (original scanned/uploaded documents)
- **Mechanism**: Admin Panel → Export Options → Patient Document Data (b10)
- **Organization**: Files sorted into patient chart ID folders with category subfolders (Lab Reports, Radiology, Scanned Receipts, etc.)
- **Selection**: Single patient or all patients; creates a "Portable" package

**Access**: UI-only, admin access required. No API or programmatic export documented.
**Fees**: Not mentioned.

## 4. Export Content: What's In It

### The EHI Export Page Itself

The entire EHI export documentation consists of **287 words** on a single page. It describes the two export mechanisms above but provides:

- **No data dictionary** for the CDA output
- **No specification of CDA sections or templates** included
- **No field mappings** between smartEMR internal data and CDA elements
- **No sample CDA files** or example output
- **No schema files** (XSD, JSON Schema, etc.)
- **No technical specifications** (encoding, naming conventions, file structure)

The documentation says "each unique patient encounter is meticulously documented within a CDA file" but never specifies what data elements are in those CDA files.

### Data Import Specifications (Indirect Evidence)

While the EHI export has no data dictionary, the vendor's **data import** pages (on the same ReadMe.io site) provide field-level specifications for 9 data entities. These document what the product *accepts* during data migration, which is an indirect indicator of what it stores — though they do not document what the export produces.

**Summary of import specifications** (from `analysis/full-entity-inventory.json`):

| Entity | Fields | Described | Typed | Required | Code Systems | Category |
|---|---|---|---|---|---|---|
| Patient Demographic (PM) | 30 | 30 | 30 | 5 | — | DATA IMPORT |
| Insurance Import (PM) | 6 | 6 | 6 | 1 | — | DATA IMPORT |
| CPT and Fee Schedule | 2 | 2 | 2 | 2 | CPT/HCPCS | DATA IMPORT |
| Service Location (PM) | 10 | 10 | 10 | 6 | NPI | DATA IMPORT |
| Referring Physician | 3 | 3 | 3 | 3 | NPI | DATA IMPORT |
| Appointments | 6 | 6 | 6 | 5 | — | DATA IMPORT |
| Document Upload | 12 | 12 | 12 | 7 | — | CLINICAL DATA IMPORT |
| Problem List | 5 | 5 | 5 | 5 | ICD-10-CM | CLINICAL DATA IMPORT |
| Allergy & Intolerance | 11 | 11 | 0* | 7 | RxNorm, SNOMED CT | CLINICAL DATA IMPORT |
| **Totals** | **85** | **85 (100%)** | **74 (87%)** | **41** | 5 systems | |

\* Allergy page uses a "Standard" column instead of "Data Type" column, referencing RxNorm/SNOMED CT but not SQL types.

Two additional entities exist as pages but have no content:
- **Electronic Health Information Export**: The EHI export page itself — 0 fields, only prose
- **Immunization Records**: Empty page in sidebar — 0 fields, no content at all

### What We Know vs. What We Don't

**We know the export produces:**
1. CDA files (one per encounter + consolidated per patient)
2. Document files (PDF/JPG/PNG) organized by patient and category

**We do not know:**
- Which CDA sections are included (CCDA? Custom CDA? Which templates?)
- Whether the CDA contains structured data or just narrative text
- Which of the 85+ data fields documented in import specs appear in the CDA output
- Whether billing data (Superbills, claims, charges) is included anywhere
- Whether medication/prescription data from Surescripts integration is included
- Whether lab results beyond uploaded documents are included as structured data
- Whether any data beyond what's available via the FHIR API (g)(10) is included

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's EHI export documentation describes exactly two categories of exported content:

1. **CDA clinical encounter data** — described only as "each unique patient encounter...documented within a CDA file." No further detail on sections, templates, or data elements. CDA is a clinical document standard well-suited for encounter summaries and US Core-equivalent clinical data, but it has no standard sections for billing, claims, or administrative data.

2. **Document repository** — scanned/uploaded files (signed notes, lab results, radiology reports, receipts) in original formats. Organized by patient chart ID and document category. This is a file dump, not structured data.

The import specifications on the same site document 9 data entities across two categories:
- **DATA IMPORT** (6 entities, 57 fields): Demographics, insurance payers, CPT codes, locations, referring physicians, appointments — a mix of clinical and administrative reference data
- **CLINICAL DATA IMPORT** (3 entities, 28 fields): Documents, problem lists, allergies — core clinical data with standard terminology (ICD-10-CM, RxNorm, SNOMED CT)

However, these import specs do not document what the export produces. They demonstrate the vendor *can* write field-level documentation (the import pages are well-structured with types, descriptions, max lengths, and validation rules) but *chose not to* for the export.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | CDA files likely contain patient demographics; import spec shows 30 fields | CDA probably includes basic demographics but unclear if all 30 fields (including insurance info) are exported |
| Encounters / visits | ⚠️ Partial | CDA files are per-encounter; document repository contains signed notes | Encounter structure exists but no detail on what encounter data is included |
| Problems / conditions / diagnoses | ⚠️ Partial | Likely in CDA if using C-CDA templates; import spec shows ICD-10-CM coded | Probably included in CDA sections but unconfirmed |
| Medications / prescriptions | ⚠️ Partial | Likely in CDA if using C-CDA templates | Product has Surescripts e-prescribing; unclear if prescription history is in CDA |
| Allergies | ⚠️ Partial | Likely in CDA; import spec shows RxNorm/SNOMED coded model | Probably included but unconfirmed |
| Immunizations | ⚠️ Partial | Likely in CDA; import page exists but is empty | Product is certified for immunization registry reporting (f)(1); data exists but export coverage unknown |
| Vitals | ⚠️ Partial | Likely in CDA if using C-CDA templates | FHIR API exposes Observation resources; probably in CDA but unconfirmed |
| Lab results | ⚠️ Partial | Document repository includes uploaded lab reports (PDF/image); may be in CDA | Structured lab data coverage unclear; uploaded lab documents are exported |
| Imaging / diagnostic reports | ⚠️ Partial | Document repository includes radiology reports | Image files exported; structured radiology data unclear |
| Procedures | ⚠️ Partial | Likely in CDA; FHIR API exposes Procedure resources | Unconfirmed in CDA output |
| Clinical notes / documents | ⚠️ Partial | Document repository exports signed encounter notes | Exported as original files (PDF/JPG/PNG), not structured data |
| Care plans / goals | ⚠️ Partial | FHIR API exposes CarePlan and Goal resources | Unclear if included in CDA export |
| Orders / referrals | ⚠️ Partial | Referring physician data in import specs (3 fields); no order-specific export | Import spec only covers provider reference data, not actual referral records |
| Insurance / coverage | ⚠️ Partial | Import specs document insurance data (6 payer fields, 12 patient insurance fields) | Product stores insurance data; unclear if CDA includes it |
| Claims / billing | ❌ Not covered | No mention of billing data, Superbills, claims, charges, or payments in export | **Significant gap**: Product's "best-known feature" is Superbill generation and electronic claims. No billing data in export documentation. |
| Payments | ❌ Not covered | No mention of payment records | Product does claims and billing; payments likely stored but not exported |
| Consents / directives | ❌ Not covered | No mention | May not be stored as structured data |
| Patient communications / portal messages | ❌ Not covered | No mention | Product has patient portal (e)(1) certified; portal data not in export |
| Specialty-specific data | ❌ Not covered | No mention of specialty templates or custom forms | Product marketed for 10+ specialties with "specialty-specific" features; none documented in export |

**Note on coverage ratings**: Nearly every clinical domain is rated "⚠️ Partial" rather than "✅ Covered" because the vendor never specifies which CDA sections are in the export. The CDA format *can* contain most clinical data, but without knowing the template or sections used, we cannot confirm coverage. The vendor's documentation makes it impossible to distinguish between "exports everything" and "exports a minimal clinical summary."

## 6. Documentation Quality

**Overall quality: Very poor.** The EHI export documentation is among the thinnest possible — a single page with ~287 words, no technical detail, and no field-level documentation.

### What's well-documented
- The UI navigation paths to trigger exports (Admin Panel → Export Options → ...)
- The two-component structure (CDA + document repository)
- Export selection options (single patient, all patients, date filtering, scheduling)

### What requires guesswork
- Everything about CDA content: sections, templates, coded entries, data elements
- Whether billing/claims data is included anywhere
- Whether structured data beyond standard C-CDA sections is exported
- File naming conventions, directory structure for CDA files
- Error handling, export size limits, performance characteristics

### Machine-readable artifacts
- **None.** No schemas (XSD, JSON Schema), no sample CDA files, no sample exports, no data dictionaries for the export output.

### Developer usability
A developer attempting to build an import for this export would have essentially no useful technical information. They would need to obtain a sample export and reverse-engineer the CDA structure entirely. The irony is that the import pages on the same site demonstrate the vendor's ability to write clear, structured field-level documentation — they simply didn't do it for the export.

### Asymmetry between import and export documentation
The import specifications document 85 fields across 9 entities with:
- 100% of fields having descriptions
- 87% having SQL data types with max lengths
- Validation rules and coded terminology references
- Two-table format (summary + detail) per entity

The export documentation has none of this. This asymmetry is striking and suggests the export documentation was a compliance checkbox rather than a genuine effort to document the export output.

## 7. Overall Assessment

### Classification

**Standard-based projection**

The export uses HL7 CDA (Clinical Document Architecture), a standardized clinical document format. While CDA can be comprehensive for clinical data, it is inherently a clinical document standard — it has no standard representation for billing claims, Superbills, fee schedules, or revenue cycle data. The vendor's billing system (described as the product's "best-known feature") is entirely absent from the export documentation. The document repository component adds file-level export of uploaded documents but no structured data.

The choice of CDA as the sole structured export format, combined with the absence of any native database model export, strongly suggests this export covers clinical encounter data only — the same scope as what's available via the (g)(10) FHIR API, just in a different format. This is a projection of clinical data into a standard format, not a comprehensive export of all electronic health information.

### Key Findings

1. **Export documentation is extremely thin** (~287 words, no data dictionary, no sample data, no schema) — despite the same site hosting well-structured import documentation with 85 fields, types, descriptions, and validation rules across 9 entities.

2. **Billing data is entirely absent.** The product's "best-known feature" — CMS-compliant Superbill generation, electronic claims, and revenue cycle management — has zero representation in the export documentation. CDA format has no standard sections for billing/claims data.

3. **CDA format without template specification is unverifiable.** The vendor says it exports CDA files but never specifies the CDA template, sections, or data elements. This makes it impossible to verify what clinical data is actually exported vs. what's omitted.

4. **Specialty-specific data not addressed.** The product is marketed for 10+ medical specialties with "specialty-specific" customization, but the export documentation makes no mention of specialty templates or custom clinical data.

5. **The import vs. export documentation gap is revealing.** The vendor invested in detailed import specs (for onboarding new customers) but not export specs (for patients/providers leaving). This pattern is consistent with treating (b)(10) as a compliance checkbox.

### Summary Stats

```
Classification:  Standard-based projection
Export format:   HL7 CDA + document files (PDF/JPG/PNG)
Model type:      Standard projection (CDA)
Entities:        N/A (no data dictionary for export output)
Fields:          N/A (CDA sections unspecified)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (all-patients option available)
Domains covered: 0 of 16 confirmed; ~10 of 16 probable via CDA (unverifiable)
```

### Bottom Line

A patient or provider requesting their complete health information from 24/7 smartEMR would receive CDA encounter files and a folder of scanned documents, but almost certainly not their billing records, claims, Superbills, or specialty-specific clinical data. The export documentation is too thin to verify what's actually included, but the choice of CDA as the sole format — a clinical document standard with no billing representation — combined with the total absence of billing data from the documentation, indicates this is a clinical data export, not a comprehensive EHI export. The biggest gap is billing/revenue cycle data in a product where billing is a core feature.
