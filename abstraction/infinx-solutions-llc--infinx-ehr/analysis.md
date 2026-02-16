# EHI Export Analysis: Infinx Solutions, LLC

**Product**: Infinx EHR (formerly iMedEMR / i3Med)
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2621.iMed.53.02.1.241219 (v5.3), 15.04.04.2621.Infi.54.03.1.260128 (v5.4)

## 1. Product Context

Infinx EHR is a cloud-based ambulatory EHR and practice management system originally built by iMed Software Corp, acquired by i3 Verticals in 2022, and then by Infinx Solutions in May 2025. It is a fully integrated EHR + PM platform targeting ambulatory medical practices of all sizes.

**Key capabilities relevant to EHI export completeness:**
- **Clinical documentation**: Patient charting, SOAP notes, encounter documentation, problem lists, medication lists, allergy lists
- **CPOE**: Medication ordering and diagnostic imaging ordering (certified for (a)(2) and (a)(3))
- **E-prescribing**: Via DrFirst integration
- **Lab management**: Orders and results with Labcorp, Boston Heart, and other integrations
- **Document management**: Scanned letters, reports, X-rays, dictation audio, lab results
- **Billing / RCM**: Integrated billing with electronic superbills, E&M coding, claims processing, insurance eligibility verification, fee schedules, A/R management
- **Scheduling**: Appointment management with reminders
- **Patient portal**: Secure messaging, lab results viewing, document access
- **Specialty features**: OB/pregnancy tracking, anticoagulation (PT/INR) management, prescription monitoring program (PMP), surgical documentation
- **Quality/Population health**: MIPS reporting, clinical quality measures, population health dashboards
- **Family health history**: Certified for (a)(12)
- **Implantable device list**: Certified for (a)(14)

This product has genuine billing and administrative capabilities beyond clinical charting, so a comprehensive (b)(10) export should include billing data, insurance/coverage, and administrative records in addition to clinical data.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/IMED-EHI-Export-Documentation.pdf` | 13-page PDF (92 KB, created 2025-09-04). Primary EHI export documentation with export format spec and data dictionary covering 15 tables and 248 fields. | **Most informative** — sole source of export documentation |
| `downloads/infinx-ehr-certification-page.html` | HTML of the Infinx EHR Certification 5.4 page at infinx.com/ehr-certification/ (1.3 MB). Links to the PDF. | Context only — confirms the PDF link |
| `downloads/infinx-ehr-certification-fullpage.png` | Full-page screenshot of certification page (1.3 MB). | Context only |
| `downloads/infinx-ehr-certification-page.png` | Viewport screenshot of certification page (718 KB). | Context only |
| `downloads/enrichment/data-dictionary.json` | Prior agent's structured parse of the PDF (36 KB). | Reference — used to cross-check my own parse |
| `downloads/enrichment/extract-data-dictionary.ts` | Prior agent's parsing script. | Reference |
| `downloads/enrichment/ehi-export-doc.txt` | Plain text extraction from PDF (16 KB). | Used as cross-reference |

No sample export data, no machine-readable schemas, no user guide for performing the export were available.

## 3. Export Mechanics

- **Format**: ZIP archive containing three types of files:
  - **CSV files** — one per patient data table (15 tables), with header row and comma-separated data
  - **C-CDA XML files** — main `ccda.xml` for clinical data + additional `ccda_[id].xml` for referrals
  - **PDF files** — clinical documents with type-specific prefixes (`SoapDoc_`, `document_`, `Labs_`, `formletter_`, `OB_`)
- **Mechanism**:
  - Single-patient: available via UI (instructions in user guide, not publicly available)
  - Bulk/multi-patient: requires contacting support via a support ticket
- **Access constraints**: Bulk export requires vendor involvement. No documented API endpoint. No mention of fees.

## 4. Export Content: What's In It

The export documentation is a single 13-page PDF (`IMED-EHI-Export-Documentation.pdf`) containing:
- 2 pages of export format overview and file type descriptions
- 1 page of table index with summary descriptions
- 10 pages of field-level data dictionary across 15 tables

### Data dictionary statistics

- **15 tables**, **248 fields** total
- **207 fields** (83.5%) have descriptions
- **132 fields** (53.2%) have data types documented
- **7 fields** have value sets documented
- No foreign key documentation (relationships are implicit via shared GUIDs like `patientid`, `scheduleid`)
- No ER diagram or relationship documentation

### Documentation quality varies significantly by table

Tables with full documentation (description + type for every field): `charges` (21 fields), `healthmaintenance` (10), `patient_advforms` (11), `patient_codes` (14), `patient_forms_data` (6), `patient_guarantor` (22), `patient_pmp` (10), `ptinr` (8), `ptinr_log` (15), `surgerymemo` (8).

Tables with descriptions but no types: `patientinfo` (47 fields — descriptions only), `ob` (8), `patient_letters` (8), `patient_referrals` (12).

Tables with minimal documentation: `schedules` (48 fields — only 7 have descriptions and types; the remaining 41 are bare field names with no description or type).

### Vendor's own content organization

The vendor does not use explicit categories. All 15 tables are presented as "Patient Data Tables" without grouping. Based on content, they organize as:

| Table | Fields | Described | Typed | Functional Area |
|---|---|---|---|---|
| patientinfo | 47 | 47 | 0 | Demographics / Patient Identity |
| charges | 21 | 21 | 21 | Billing |
| healthmaintenance | 10 | 10 | 10 | Preventive Care |
| ob | 8 | 8 | 0 | OB/Pregnancy |
| patient_advforms | 11 | 11 | 11 | Patient Forms |
| patient_codes | 14 | 14 | 14 | Clinical Codes (generic) |
| patient_forms_data | 6 | 6 | 6 | Provider Forms |
| patient_guarantor | 22 | 22 | 22 | Billing / Guarantor |
| patient_letters | 8 | 8 | 0 | Correspondence |
| patient_pmp | 10 | 10 | 10 | Prescription Monitoring |
| patient_referrals | 12 | 12 | 0 | Referrals |
| ptinr | 8 | 8 | 8 | Anticoagulation Tracking |
| ptinr_log | 15 | 15 | 15 | Anticoagulation Results |
| schedules | 48 | 7 | 7 | Appointments / Scheduling |
| surgerymemo | 8 | 8 | 8 | Surgical Documentation |
| **Totals** | **248** | **207** | **132** | |

### Notable table details

**`patientinfo`** (47 fields): Extensive demographics including name, DOB, SSN, addresses (current + previous), multiple phone numbers, emergency contact, email, marital status, gender identity, sexual orientation, birth sex, preferred language, preferred communication method, ethnicity, employer info, injury/accident details, financial class, patient type, and active/inactive status. No data types documented.

**`charges`** (21 fields): CPT charge data with charge code, heading, description, text, units, fee, verification status, case type (New/Pending/Processed), batch number, export status (not exported/set to export/exported), export datetime, billing description, and location GUID.

**`patient_codes`** (14 fields): A generic code storage table linking codes of "various code systems" to patients and schedules. Fields include code, value (JSON array), units, type, description, and linking fields (`link_table`, `link_guid`). Critically, the `type` field's possible values are **not documented** — this table likely holds diagnoses, allergies, medications, vitals, and other coded clinical data, but the documentation doesn't specify which code systems or types are stored.

**`schedules`** (48 fields): Appointment data. Only 7 of 48 fields are documented (scheduleid, patientid, doctorid, ob_pregid, date, time, end). The remaining 41 fields are bare names — many are self-explanatory (`firstname`, `copay`, `cancelled`, `virtual_visit_url`) but some are opaque (`acs_resource_id`, `qsi_visit_no`, `muerror`, `soc_status`).

**`patient_advforms`** and **`patient_forms_data`** (17 fields combined): Two tables for forms — one for patient-facing online forms, one for provider-side forms. Both store responses as JSON arrays (`user_data`, `response`), which could contain rich structured data, but the JSON structure is not documented.

### Non-CSV content

Beyond the 15 CSV tables, the export includes:

- **C-CDA XML** (`ccda.xml`): Standard clinical data (problems, medications, allergies, immunizations, vitals, etc.). No documentation of which C-CDA sections are populated or how vendor-specific data maps to C-CDA.
- **SOAP note PDFs** (`SoapDoc_` prefix): Visit/encounter documentation — likely contains vitals, assessments, and plans in unstructured form.
- **Lab result PDFs** (`Labs_` prefix): Lab results as PDF documents.
- **Chart document PDFs** (`document_` prefix): Scanned or uploaded documents.
- **Letter PDFs** (`formletter_` prefix): Clinic-generated letters.
- **OB visit PDFs** (`OB_` prefix): Pregnancy-related visit documentation.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export has two notable strengths:

1. **Purpose-built CSV tables for non-clinical data**: The `charges` table (CPT billing), `patient_guarantor` (billing demographics), `patient_pmp` (prescription monitoring scores), `ptinr`/`ptinr_log` (anticoagulation tracking), `surgerymemo` (surgical documentation), and `patient_advforms`/`patient_forms_data` (custom forms with JSON responses) represent data that would not appear in a standard C-CDA or FHIR export. This is genuine (b)(10) content.

2. **Hybrid format approach**: The vendor honestly separates structured data (CSV) from clinical summaries (C-CDA) and documents (PDFs), rather than pretending one format covers everything.

However, there are clear thin spots:

- **The `patient_codes` table is a black box**: It's a generic code container whose `type` field values are undocumented. This single table may hold diagnoses, medications, allergies, vitals, and other coded clinical data — but without knowing the type taxonomy, it's impossible to assess coverage of these domains.
- **Core clinical data relies on C-CDA and PDFs**: Medications, allergies, problem lists, vitals, and immunizations have no dedicated CSV tables. They're presumably in the C-CDA XML and/or embedded in SOAP note PDFs, but there's no documentation of C-CDA section coverage.
- **Insurance/coverage data is absent**: Despite the product having insurance eligibility verification and billing capabilities, there's no table for insurance plans, policy numbers, payer details, or coverage dates. The only insurance-related data is a single `financial_class` field in `patientinfo`.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `patientinfo` (47 fields): name, DOB, SSN, addresses, phones, gender identity, sexual orientation, birth sex, ethnicity, language, employer info | Thorough — one of the most detailed tables |
| Encounters / visits | ✅ Covered | `schedules` (48 fields) for appointments; SOAP note PDFs for encounter content | Scheduling data present but poorly documented (41/48 fields undescribed) |
| Problems / conditions | ⚠️ Partial | Likely in `patient_codes` and C-CDA XML; no dedicated table | Unclear — depends on undocumented `patient_codes.type` values |
| Medications / prescriptions | ⚠️ Partial | Likely in `patient_codes` and C-CDA XML; PMP scores in `patient_pmp` | No dedicated medication table despite DrFirst e-prescribing integration |
| Allergies | ⚠️ Partial | Likely in `patient_codes` and C-CDA XML | No dedicated allergy table |
| Immunizations | ⚠️ Partial | Likely in C-CDA XML only | No dedicated table |
| Vitals | ⚠️ Partial | Likely in SOAP note PDFs and C-CDA XML | No dedicated table; structured vitals not explicitly exported |
| Lab results | ⚠️ Partial | `Labs_` PDF files; possibly in C-CDA XML | Lab results exported as PDFs (unstructured), not structured data |
| Imaging / diagnostic reports | ⚠️ Partial | `document_` PDF files may include imaging; C-CDA may include narratives | No dedicated imaging table despite CPOE certification for imaging orders |
| Procedures | ⚠️ Partial | `surgerymemo` (8 fields) for surgical documentation; may be in `patient_codes` | Only surgical procedures; other procedures unclear |
| Clinical notes / documents | ✅ Covered | `SoapDoc_` PDFs, `document_` PDFs, `formletter_` PDFs | Exported as PDF documents — comprehensive but unstructured |
| Care plans / goals | ❌ Not covered | No evidence in export | Product likely supports care plans through charting; gap |
| Orders / referrals | ✅ Covered | `patient_referrals` (12 fields) with associated C-CDA XML files | Referrals covered; other order types (lab, imaging) unclear |
| Insurance / coverage | ❌ Not covered | Only `financial_class` in `patientinfo`; no insurance table | Product does eligibility verification and billing — significant gap |
| Claims / billing | ✅ Covered | `charges` (21 fields): CPT codes, fees, units, batch, export status, descriptions | Charge-level billing data present; no claims-level data (payer responses, remittance) |
| Payments | ⚠️ Partial | `schedules` has `copay`, `balance`, `payment_type`, `payment_type1/2`, `check_num` fields | Payment fields exist but undocumented; no dedicated payments table |
| Consents / directives | ⚠️ Partial | `patient_advforms` may include consent forms (JSON responses) | Depends on form content; no dedicated consent table |
| Patient communications | ❌ Not covered | No portal message or communication table | Product has patient portal with secure messaging — gap |
| Specialty: OB/Pregnancy | ✅ Covered | `ob` table (8 fields) + `OB_` PDF files; `schedules.ob_pregid` links | Dedicated support |
| Specialty: Anticoagulation | ✅ Covered | `ptinr` (8 fields) + `ptinr_log` (15 fields) | Unusually detailed — diagnosis, INR ranges, dosage tracking, test results |
| Specialty: Prescription monitoring | ✅ Covered | `patient_pmp` (10 fields): narcotics/stimulant/sedative/overall scores | Purpose-built table for PMP database integration |
| Family health history | ❌ Not covered | No evidence in export | Certified for (a)(12) — gap |
| Implantable devices | ❌ Not covered | No evidence in export | Certified for (a)(14) — gap |

**Gap summary**: 4 domains not covered at all (insurance, patient communications, family health history, implantable devices) despite the product storing this data. 7 domains have only partial coverage, primarily because core clinical domains (medications, allergies, problems, vitals, immunizations) rely on C-CDA and SOAP PDFs rather than structured CSV tables, and the generic `patient_codes` table is undocumented.

## 6. Documentation Quality

**Strengths:**
- Field-level data dictionary covers 15 tables with descriptions for 83.5% of fields
- Clear export format specification (ZIP → CSV + XML + PDF)
- Specific file naming conventions for PDF types documented
- Value sets documented for a few fields (gender, active/inactive, case type, export status)
- Data types documented for 53.2% of fields (GUIDs, dates, timestamps, integers, text, JSON arrays)

**Weaknesses:**
- **No machine-readable schema**: No XSD, JSON Schema, DDL, or any machine-parseable format. The PDF is the only specification.
- **No sample data**: No example export files provided.
- **`schedules` table is 85% undocumented**: 41 of 48 fields are bare names with no description or type.
- **`patient_codes.type` is the critical gap**: This generic table likely holds the bulk of structured clinical data, but the type taxonomy is not documented. A developer would have no way to distinguish diagnoses from medications from allergies.
- **No relationship documentation**: Tables share GUIDs (patientid, scheduleid) but no foreign key mapping or ER diagram.
- **No C-CDA section documentation**: The C-CDA export is described as "all patient ccda-compatible data" but no specifics on which sections are populated.
- **No JSON structure documentation**: Forms tables store responses as "JSON array" but the JSON schema/structure is not described.
- **No versioning**: The PDF filename suggests original creation around December 2023. The PDF metadata shows it was last generated September 2025, but there's no change log or version number.

**Could a developer build an import?** Partially. The well-documented tables (charges, healthmaintenance, patient_guarantor, etc.) are usable. But the `patient_codes` table would require significant reverse-engineering, the `schedules` table would need trial-and-error, and the C-CDA and form JSON content are undocumented.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The export goes meaningfully beyond USCDI by including billing charges, guarantor demographics, prescription monitoring scores, custom forms with JSON responses, anticoagulation tracking, surgical documentation, and OB/pregnancy data. These are genuine EHI domains that would not appear in a C-CDA or FHIR (g)(10) export.

However, there are real gaps relative to what the product stores:
- **Insurance/coverage**: The product does eligibility verification and billing, but there's no insurance table in the export.
- **Patient portal messages**: The product has secure messaging, but no communication data in the export.
- **Family health history** and **implantable devices**: The product is certified for these ((a)(12), (a)(14)) but they're absent from the export.
- **Core clinical structured data**: Medications, allergies, problem lists, vitals, and immunizations rely on C-CDA and PDFs rather than structured tables. The `patient_codes` table may hold some of this data, but it's undocumented.

The export covers more than USCDI but less than the full designated record set.

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly a purpose-built (b)(10) export, not a repackaged (g)(10) or C-CDA export. The evidence:
1. **15 CSV tables with vendor-specific schema** — these are internal database tables, not a standard projection.
2. **Data domains beyond USCDI**: billing charges, guarantor info, PMP scores, custom forms, anticoagulation tracking, surgical memos.
3. **Hybrid format**: The vendor honestly acknowledges that different data types need different formats (CSV for structured, C-CDA for clinical summaries, PDF for documents).
4. **No references to USCDI, US Core, or (g)(10)** in the documentation — this isn't a relabeled clinical exchange export.

The vendor made a genuine effort to build an EHI-specific export that reflects their internal data model. The effort is incomplete (missing domains, thin documentation in places), but the approach is correct.

### Key Findings

1. **Genuine (b)(10) effort with meaningful non-USCDI content**: The export includes 15 purpose-built CSV tables covering billing (charges, guarantor), specialty clinical data (PT/INR, PMP, OB, surgery), and custom forms — data that would never appear in a C-CDA or FHIR exchange.

2. **The `patient_codes` table is the critical documentation gap**: This generic table likely holds the bulk of structured clinical data (diagnoses, medications, allergies, etc.), but its `type` field values are not documented. This single omission makes it impossible to fully assess clinical data coverage.

3. **41 of 48 `schedules` fields are undocumented**: The appointment/visit table — arguably the richest data table — has only 7 of 48 fields described. Many field names are guessable (`copay`, `firstname`) but others are opaque (`muerror`, `soc_status`, `qsi_visit_no`).

4. **Insurance/coverage data is absent**: Despite the product having integrated billing and eligibility verification, there is no insurance plan, payer, or coverage table in the export. The only insurance-related data point is `patientinfo.financial_class`.

5. **No sample data or machine-readable schema**: The sole documentation is a 13-page PDF. No JSON Schema, XSD, DDL, or sample export files are provided. A receiving system would need to process a real export to understand the actual data structure, especially for the C-CDA sections and JSON form responses.

### Summary Stats

    Coverage:        Partial
    Approach:        Purpose-built EHI export
    Export format:   CSV + C-CDA XML + PDF (ZIP archive)
    Entities:        15 tables (CSV) + C-CDA + PDF documents
    Fields:          248 (across CSV tables)
    Descriptions:    83.5% of fields (207/248)
    Sample data:     No
    Bulk export:     Yes (via support ticket)
    Domains covered: 8 of 19 applicable domains fully covered; 7 partial; 4 not covered

### Bottom Line

Infinx EHR built a genuine (b)(10) export that goes beyond C-CDA/USCDI to include billing, specialty clinical data, and custom forms — a real effort that many vendors don't make. However, the export has meaningful gaps: no insurance/coverage data despite having billing capabilities, core clinical domains (medications, allergies, diagnoses) rely on an undocumented generic `patient_codes` table and C-CDA rather than structured exports, and the single largest table (`schedules`, 48 fields) is 85% undocumented. A patient would get a substantial but incomplete copy of their record.
