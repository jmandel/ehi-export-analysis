# EHI Export Analysis: Infinx Solutions, LLC

**Product**: Infinx EHR (formerly iMedEMR / i3Med)
**Analysis date**: 2026-02-16
**CHPL IDs**: 11554 (v5.3, certified 2024-12-19), 11759 (v5.4, certified 2026-01-28)

## 1. Product Context

Infinx EHR is a cloud-based ambulatory EHR and practice management system originally built by iMed Software Corp, acquired by i3 Verticals in 2022, then by Infinx Solutions in May 2025. It serves ambulatory/outpatient practices with integrated clinical documentation, billing/RCM, scheduling, e-prescribing (via DrFirst), lab management, and a patient portal.

Key data domains the product stores, based on its certified criteria and documented features:
- **Patient demographics** (certified (a)(5)) including online registration
- **Clinical documentation**: encounter notes (SOAP), problem lists, medication lists, allergies
- **CPOE**: medication orders (a)(2), diagnostic imaging orders (a)(3)
- **E-prescribing** via DrFirst integration
- **Lab ordering and results** with Labcorp, Boston Heart, CGM LABDAQ integrations
- **Family health history** (certified (a)(12))
- **Implantable device list** (certified (a)(14))
- **Document management**: scanned letters, reports, X-rays, dictation
- **Scheduling and registration**
- **Billing/RCM**: superbills, CPT charges, claims, eligibility, fee schedules
- **Patient portal**: secure messaging, lab results viewing
- **Clinical quality measures** and MIPS reporting
- **Transitions of care**: C-CDA exchange via Direct Messaging

This baseline establishes what a complete EHI export should cover.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `IMED-EHI-Export-Documentation.pdf` | Primary EHI export documentation. 13 pages, 92,684 bytes. Contains export format specification, instructions, and a data dictionary with 15 tables and 248 fields. | **Most informative** — the sole substantive artifact |
| `enrichment/data-dictionary.json` | Structured JSON extraction of the PDF data dictionary by a prior agent's TypeScript parser. 35,944 bytes. 15 tables, 248 fields. | Useful secondary source; verified against PDF |
| `enrichment/ehi-export-doc.txt` | Plain text extraction from the PDF via pdftotext. 15,949 bytes. | Used for independent verification |
| `infinx-ehr-certification-page.html` | HTML of the Infinx EHR Certification 5.4 page. 1.3 MB. | Confirmed only one EHI document linked |
| `infinx-ehr-certification-fullpage.png` | Full-page screenshot of certification page. 1.3 MB. | Visual confirmation of page content |
| `enrichment/extract-data-dictionary.ts` | TypeScript script used to parse the PDF text into JSON. 30,817 bytes. | Shows how the enrichment JSON was produced |

The entire EHI export documentation consists of a single 13-page PDF. No sample data files, no machine-readable schemas (JSON Schema, XSD, DDL), and no separate user guide for the export process were provided publicly.

## 3. Export Mechanics

- **Format**: ZIP file containing CSV files (one per table), C-CDA XML files, and PDF files
- **Mechanism**:
  - Single-patient export: available through the user guide (instructions not publicly documented)
  - Bulk/multi-patient export: requires contacting support via a support ticket
- **Access constraints**: User guide not publicly available; bulk export requires vendor involvement
- **Fees**: Not documented

The ZIP export contains three file types:
1. **CSV files** — one per patient data table (15 tables), with header row and comma-separated values
2. **XML files** — `ccda.xml` for C-CDA clinical data, plus `ccda_[id].xml` for referral documents
3. **PDF files** — prefixed by type: `SoapDoc_` (SOAP notes), `document_` (scanned/uploaded documents), `Labs_` (lab results), `formletter_` (clinic letters), `OB_` (pregnancy visit data)

## 4. Export Content: What's In It

The export documentation defines **15 CSV tables with 248 total fields**, plus C-CDA XML and PDF attachments. This was independently verified against the PDF text (`IMED-EHI-Export-Documentation.pdf`, 13 pages).

### Documentation depth

| Metric | Count | Percentage |
|---|---|---|
| Total entities (tables) | 15 | — |
| Total fields | 248 | — |
| Fields with descriptions | 207 | 83.5% |
| Fields without descriptions | 41 | 16.5% |
| Fields with data types (Schema) | 132 | 53.2% |
| Fields with value sets documented | 11 | 4.4% |
| Foreign key relationships documented | 0 | 0% |

**Note**: The prior report claimed 42 fields for the `schedules` table and 46 for `patientinfo`. Independent verification shows **48 fields** for `schedules` and **47 fields** for `patientinfo`.

### Documentation gaps
- **No formal foreign key documentation.** Tables share GUIDs (`patientid`, `scheduleid`) but relationships are implicit. The only explicit cross-reference is `patient_referrals.ccda_id` → `ccda_[id].xml` filename.
- **No machine-readable schema.** The PDF is the only specification — no XSD, JSON Schema, or SQL DDL.
- **No sample data files** are provided.
- **41 undocumented fields** — all in the `schedules` table, which has 48 fields but only 7 with descriptions. These bare field names (e.g., `copay`, `balance`, `payment_type`, `virtual_visit_url`, `waitlist`) are mostly self-explanatory but lack formal documentation.

### Vendor's own content organization

The vendor organizes data into 15 patient-level tables. Tables that have a Schema column in the PDF are marked; tables without Schema have field names and descriptions only.

| Entity/Table | Fields | Described | Typed | Value Sets | Has Schema Column |
|---|---|---|---|---|---|
| patientinfo | 47 | 47 | 0 | 2 | No |
| charges | 21 | 21 | 21 | 3 | Yes |
| healthmaintenance | 10 | 10 | 10 | 1 | Yes |
| ob | 8 | 8 | 0 | 0 | No |
| patient_advforms | 11 | 11 | 11 | 2 | Yes |
| patient_codes | 14 | 14 | 14 | 0 | Yes |
| patient_forms_data | 6 | 6 | 6 | 0 | Yes |
| patient_guarantor | 22 | 22 | 22 | 1 | Yes |
| patient_letters | 8 | 8 | 0 | 0 | No |
| patient_pmp | 10 | 10 | 10 | 0 | Yes |
| patient_referrals | 12 | 12 | 0 | 0 | No |
| ptinr | 8 | 8 | 8 | 1 | Yes |
| ptinr_log | 15 | 15 | 15 | 1 | Yes |
| schedules | 48 | 7 | 7 | 0 | Yes (partial) |
| surgerymemo | 8 | 8 | 8 | 0 | Yes |
| **TOTAL** | **248** | **207** | **132** | **11** | — |

The full field-level inventory is in `analysis/full-entity-inventory.json` (248 field objects).

### C-CDA and PDF components

Beyond the 15 CSV tables, the export includes:
- **C-CDA XML** (`ccda.xml`): Standard clinical summary with problems, medications, allergies, immunizations, vitals, and other C-CDA sections. No vendor-specific extensions are documented.
- **SOAP note PDFs** (`SoapDoc_`): Visit encounter documentation — likely contain vitals, assessments, diagnoses, and treatment plans in unstructured form.
- **Lab result PDFs** (`Labs_`): Lab results as rendered PDF documents.
- **Document PDFs** (`document_`): Scanned or uploaded chart documents.
- **Letter PDFs** (`formletter_`): Clinic-generated correspondence.
- **OB visit PDFs** (`OB_`): Pregnancy-related visit documentation.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export uses a hybrid approach: structured CSV tables for vendor-specific data that doesn't fit C-CDA, C-CDA XML for standard clinical data, and PDF files for unstructured clinical documents.

**Strongest coverage (dedicated CSV tables):**
- **Demographics** (`patientinfo`, 47 fields): Comprehensive — name, DOB, SSN, address, phone, email, gender identity, sexual orientation, birth sex, ethnicity, language, employer, injury/accident details, financial class, provider assignments.
- **Billing charges** (`charges`, 21 fields): CPT charges with fees, units, batch numbers, export status, billing descriptions.
- **Guarantor information** (`patient_guarantor`, 22 fields): Full guarantor demographics including employer information — supports billing workflows.
- **Appointments/scheduling** (`schedules`, 48 fields): Large table covering dates, times, providers, locations, copays, balances, payment types, virtual visit info. However, 41 of 48 fields are undocumented.
- **Patient forms** (`patient_advforms`, 11 fields; `patient_forms_data`, 6 fields): Online patient forms and provider-side forms with responses stored as JSON arrays.

**Specialty/niche coverage:**
- **Anticoagulation tracking** (`ptinr`, 8 fields; `ptinr_log`, 15 fields): PT/INR monitoring with diagnosis, ranges, dosing, and result logs. Genuinely specialized data.
- **Prescription monitoring** (`patient_pmp`, 10 fields): PMP database results with narcotic/stimulant/sedative scores.
- **Surgical documentation** (`surgerymemo`, 8 fields): Custom/optional surgical memos. The documentation notes "Most clinics will have blank table."
- **OB/pregnancy data** (`ob`, 8 fields): Pregnancy visit tracking with associated PDFs.

**Thinnest coverage:**
- **Clinical codes** (`patient_codes`, 14 fields): A generic code container for "codes of various code systems." The `type` field presumably differentiates diagnoses, medications, allergies, etc., but its possible values are **not documented**. This is the most important underdocumented table — it may contain structured diagnoses, problems, and other coded clinical data, but the documentation doesn't specify.
- **Health maintenance** (`healthmaintenance`, 10 fields): Preventive care tracking for recurring tests.
- **Letters and referrals** (`patient_letters`, 8 fields; `patient_referrals`, 12 fields): Cross-references to associated PDF/C-CDA files.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `patientinfo` (47 fields) — extensive demographics, contacts, employer, injury info | Thorough |
| Encounters / visits | ✅ Covered | `schedules` (48 fields) + `SoapDoc_` PDFs for visit content | Appointment data is structured; clinical encounter content is in unstructured PDFs |
| Problems / conditions / diagnoses | ⚠️ Partial | Likely in `patient_codes` (type field undocumented) + C-CDA `ccda.xml` | No dedicated diagnosis table. `patient_codes` may contain ICD codes but this isn't explicitly documented. C-CDA covers standard problem list. |
| Medications / prescriptions | ⚠️ Partial | Likely in C-CDA only; no dedicated medication CSV table | Product has DrFirst e-prescribing integration and is certified for medication CPOE. No structured medication export table — significant gap given the product's capabilities. |
| Allergies | ⚠️ Partial | Likely in C-CDA only; no dedicated allergy CSV table | No structured allergy export. C-CDA covers standard allergy section. |
| Immunizations | ⚠️ Partial | Likely in C-CDA only | No structured immunization export. C-CDA covers standard immunization section. |
| Vitals | ⚠️ Partial | Likely in C-CDA and/or SOAP note PDFs | No structured vitals table. |
| Lab results | ⚠️ Partial | `Labs_` PDF files + likely in C-CDA | Lab results exported as rendered PDFs, not structured data. `healthmaintenance` tracks scheduled tests but not results. |
| Imaging / diagnostic reports | ⚠️ Partial | Possibly in `document_` PDFs | Product is certified for CPOE diagnostic imaging (a)(3) but no dedicated imaging table. |
| Procedures | ⚠️ Partial | `surgerymemo` (8 fields, custom/optional) + `charges` has CPT codes | Surgical memos exist but are a custom feature. CPT charges capture procedures billed. |
| Clinical notes / documents | ✅ Covered | `SoapDoc_` PDFs (visit SOAP notes), `document_` PDFs (scanned/uploaded documents), `formletter_` PDFs | Comprehensive PDF export of clinical documents, though all unstructured |
| Care plans / goals | ❌ Not covered | No evidence in export | Product likely stores care plans; not exported |
| Orders / referrals | ✅ Covered | `patient_referrals` (12 fields) with C-CDA cross-references | Referrals well-covered; medication/imaging orders not separately exported |
| Insurance / coverage | ❌ Not covered | Only `financial_class` (1 field in `patientinfo`) | Product collects insurance information during registration; no insurance/coverage table exported. `patient_guarantor` covers the guarantor but not insurance plans/policies. Significant gap. |
| Claims / billing | ✅ Covered | `charges` (21 fields) — CPT charges with fees, units, batch numbers | Charge-level billing data exported. No claims-level or payment-posting data. |
| Payments | ⚠️ Partial | `schedules` has `copay`, `balance`, `payment_type` fields (undocumented) | Payment-related fields exist in schedules but are undocumented. No dedicated payment table. |
| Consents / directives | ❌ Not covered | No evidence in export | Unknown if product stores advance directives |
| Patient communications / portal messages | ❌ Not covered | No portal message table | Product has a patient portal with secure messaging; messages not exported |
| Specialty-specific (OB/pregnancy) | ✅ Covered | `ob` (8 fields) + `OB_` PDFs | Pregnancy visit tracking with associated documents |
| Specialty-specific (anticoagulation) | ✅ Covered | `ptinr` (8 fields) + `ptinr_log` (15 fields) | Comprehensive PT/INR monitoring data |
| Specialty-specific (prescription monitoring) | ✅ Covered | `patient_pmp` (10 fields) | PMP database scores and results |
| Family health history | ❌ Not covered | No evidence in export | Product is certified for (a)(12) family health history; not exported as structured data. May be in C-CDA. |
| Implantable device list | ❌ Not covered | No evidence in export | Product is certified for (a)(14) implantable device list; not exported as structured data. May be in C-CDA. |

**Domains covered**: 8 of 19 applicable domains have dedicated structured export
**Domains partially covered** (C-CDA/PDF only): 7 domains
**Domains not covered**: 4 domains (insurance/coverage, care plans, portal messages, consents)

## 6. Documentation Quality

**Strengths:**
- The PDF is well-organized: export format overview → file type descriptions → table index with summaries → field-level data dictionary for each table.
- 207 of 248 fields (83.5%) have human-readable descriptions.
- 11 tables include data type information (Schema column).
- A few coded fields document their value sets (e.g., `chrGender`: 1=male, 2=female; `status`: 0=active, 1=inactive; `caseType`: New/Pending/Processed).

**Weaknesses:**
- **No machine-readable schema.** The entire specification is a single PDF with no XSD, JSON Schema, SQL DDL, or other parseable format.
- **No sample export files.** A developer has no way to validate their import logic without requesting an actual export.
- **Inconsistent documentation depth.** The `schedules` table has 48 fields but only 7 documented — 41 bare field names with no descriptions, types, or value sets. The `patientinfo` table has descriptions for all 47 fields but no data types.
- **Critical underdocumented table.** The `patient_codes` table is a generic code container whose `type` field determines what kind of clinical data is stored (potentially diagnoses, allergies, medications). The possible values of `type` are not documented, making it impossible to know what structured clinical data is actually exported.
- **No relationship documentation.** Tables share GUIDs (`patientid`, `scheduleid`) but there's no entity-relationship diagram, no foreign key mapping, and no documentation of table relationships beyond the single `ccda_id` cross-reference.
- **No versioning.** The filename suggests creation date of 2023-12-19. No version number, changelog, or indication of updates despite the product advancing from v5.1 to v5.4.
- **Stale branding.** The PDF retains "IMED" branding from the iMed Software era despite two ownership changes.

**Could a developer build an import?** Partially. The demographics, billing, and specialty tables (PT/INR, PMP, surgical) are documented well enough to import. The generic `patient_codes` table would require significant trial-and-error. The `schedules` table's 41 undocumented fields would require guesswork. The C-CDA and PDF components follow standards but have no vendor-specific documentation.

## 7. Overall Assessment

### Classification

**Partial native export**

The vendor has created a genuine EHI export that goes beyond just C-CDA/USCDI — it exports 15 CSV tables from what appears to be the native database model, covering billing charges, guarantor demographics, PMP scores, custom forms, PT/INR tracking, and surgical documentation. This is real (b)(10) effort, not a C-CDA repackaging.

However, significant gaps remain: core clinical domains (medications, allergies, diagnoses, vitals, immunizations) rely on the C-CDA XML or are embedded in the underdocumented `patient_codes` table rather than being exported as dedicated structured tables. Insurance/coverage data is absent despite the product collecting it. The documentation, while better than many vendors, has meaningful holes (41 undocumented fields, no foreign keys, no sample data, critical `patient_codes.type` values undocumented).

### Key Findings

1. **Genuine hybrid export approach.** The CSV + C-CDA + PDF format is practical and honest — it exports vendor-specific data (billing, forms, PMP scores) as structured CSV while using C-CDA for standardized clinical data and PDFs for unstructured documents. This is better than vendors who only offer C-CDA or FHIR.

2. **Core clinical data is structurally thin.** Medications, allergies, diagnoses, vitals, and immunizations have no dedicated CSV tables. They are either in the C-CDA XML, in SOAP note PDFs (unstructured), or potentially in the generic `patient_codes` table (underdocumented). This means the structured, queryable portion of the export skews heavily toward demographics and billing rather than clinical data.

3. **The `patient_codes` table is a black box.** This 14-field table stores "codes of various code systems" with an undocumented `type` field. It could contain diagnoses, allergies, medications, or other coded clinical data — but without documented `type` values, it's impossible to assess what structured clinical data is actually exported. This is the single most important documentation gap.

4. **Insurance/coverage is missing.** The product collects insurance information during patient registration and performs eligibility verification, but no insurance/coverage table is exported. The `financial_class` field in `patientinfo` is a single field — not a substitute for policy-level insurance data.

5. **Prior report field counts were inaccurate.** The prior report stated 42 fields for `schedules` (actual: 48) and 46 for `patientinfo` (actual: 47). These discrepancies were verified against the raw PDF text.

### Summary Stats

    Classification:  Partial native export
    Export format:   CSV + C-CDA XML + PDF (in ZIP container)
    Model type:      Hybrid (native CSV tables + standard C-CDA + unstructured PDFs)
    Entities:        15 tables
    Fields:          248
    Descriptions:    83.5% (207/248) — but 41 undocumented fields are all in one table (schedules)
    Sample data:     No
    Bulk export:     Yes (via support ticket)
    Domains covered: 8 of 19 applicable domains with dedicated structured data; 7 more via C-CDA/PDF

### Bottom Line

Infinx EHR's export is a legitimate (b)(10) effort that exports native data beyond C-CDA — particularly strong in demographics, billing, and specialty clinical data (anticoagulation, PMP, OB). However, core clinical domains (medications, allergies, diagnoses, vitals) lack dedicated structured tables, relying instead on C-CDA XML and the underdocumented `patient_codes` catch-all table. The single biggest gap is the missing documentation for `patient_codes.type` values, which would reveal what structured clinical data is actually in the export vs. what is only available in unstructured PDFs and C-CDA.
