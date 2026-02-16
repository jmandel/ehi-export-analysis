# EHI Export Analysis: Eyefinity, Inc.

**Product**: EHR powered by EMA in Eyefinity Encompass
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2900.Eyef.07.17.1.221219

## 1. Product Context

EHR powered by EMA in Eyefinity Encompass is a cloud-based electronic health records system for eye care (optometry and ophthalmology) practices. The product is a white-labeled/customized version of Modernizing Medicine's (ModMed) EMA platform, integrated with Eyefinity's own Practice Management system. Together, under the "Eyefinity Encompass" brand, they form an all-in-one platform serving over 7,000 independent optometry practices and 20,000+ offices.

**Clinical capabilities**: Eye exam documentation with customizable templates, adaptive learning engine, comprehensive ocular exam fields (refraction, contact lens parameters, visual acuity), iPad-native charting, problem/medication/allergy lists, immunizations, lab ordering/results, e-prescribing, diagnostic equipment integration (OCT, visual fields), pathology tracking, CPOE.

**Practice management capabilities**: Appointment scheduling, insurance eligibility verification (including VSP-specific), claims management and billing, ERA/remittance, optical lab orders, inventory management, patient statements, accounts receivable.

**Patient engagement**: Secure messaging (IntraMail), patient portal, telehealth, electronic consent forms, appointment reminders, two-way texting.

**Key for export assessment**: The certified product spans both clinical EHR (via ModMed EMA) and practice management (via Eyefinity PM). A complete EHI export should cover clinical documentation, eye-care-specific measurements, billing/financial records, prescriptions, and patient communications. The EHI documentation URL points to ModMed's domain, meaning the export documentation covers the EMA engine's data model.

## 2. Artifacts Reviewed

| Artifact | Description | Informational Value |
|---|---|---|
| `Data-Dictionary-for-ModMed-EMA-EHI-Export4.pdf` (684 KB, 131 pages) | Full data dictionary for the ModMed EMA EHI Export. Defines 197 database tables across 16 groupings with ~4,670 columns. Includes intro section with export format, folder structure, and tracking conventions. | **Primary artifact** — sole source of export documentation |
| `Data-Dictionary-for-ModMed-EMA-EHI-Export4.txt` (123 KB) | Plain-text extraction via `pdftotext` | Used for parsing |
| `Data-Dictionary-layout.txt` (511 KB) | Layout-preserved text extraction via `pdftotext -layout` | Used for column position verification |
| `enrichment/data-dictionary.json` (174 KB) | Prior structured parse: 197 tables, 4,784 columns (pre-cleaning) | Cross-reference for parsing |
| `enrichment/coverage-summary.json` (26 KB) | Prior summary statistics | Cross-reference |

The PDF is the sole artifact. No sample data files, no JSON/XML schema, no separate API documentation. The analysis is entirely based on parsing this 131-page PDF data dictionary.

## 3. Export Mechanics

- **Format**: Pipe-delimited CSV files (one per database table) inside a ZIP file (`ehi_export.zip`), plus an attachments folder containing human-readable files (XML, JPEG, PNG, TIFF, JSON, PDF) for imaging results, scanned documents, lab attachments, and prescription attachments.
- **Folder structure**: `ehi_export/xxxx_data_extract/` for structured data; `ehi_export/attachments/` for media/documents.
- **Mechanism**: Described as an export capability within the product. The documentation says "ModMed enables Customers in the ambulatory setting to easily export demographic and billing information pertaining to patient records."
- **Scope**: Can be exported for a single patient or for multiple (all) patients.
- **Access constraints**: No mention of fees. The data dictionary itself includes a confidentiality notice but also acknowledges that "nothing herein shall be construed to prohibit or restrict any communication that is protected by 45 C.F.R. § 170.403."

## 4. Export Content: What's In It

The data dictionary documents **197 database tables** with approximately **4,670 columns** organized into **16 populated groupings**. Three additional groupings are declared but have no table entries (Lookup, MIPS, Medical Lookup).

The documentation provides:
- **Table names**: Yes — all 197 tables named (snake_case)
- **Table descriptions**: Yes — 196 of 197 tables have prose descriptions explaining purpose and cardinality
- **Column names**: Yes — all ~4,670 columns named (snake_case)
- **Column descriptions**: **No** — only table-level descriptions; individual columns are listed by name only
- **Data types**: **No** — mentioned in the introduction ("Field Length column of the Data Dictionary sheet") but not present in the actual entries
- **Value sets/codes**: **No** — coded fields not documented
- **Relationships/foreign keys**: **Implicit only** — inferred from naming conventions (e.g., `patient_id`, `visit_id`, `bill_id`)
- **Longitudinal tracking flags**: Yes — Y/N/L/S for each table indicating historical tracking behavior

### Vendor's own content organization

The vendor organizes tables into 16 groupings (plus 3 declared-but-empty). Below is a summary by grouping with representative tables:

| Grouping | Tables | Fields | Top Tables (by field count) |
|---|---|---|---|
| Ophth Pretesting | 25 | 1,213 | wearing_contacts (110), contacts_trial (107), binocular (107), rgp_contacts_trial (104), wearing_rgp_contacts (103) |
| PM Financials | 38 | 1,182 | bill (130), production_summary (110), accounts_receivable (102), charges (100), payments_posted (54) |
| Patient | 31 | 697 | patient (177), insurance_policy (136), family_history (44), patient_case_contact (34), immunization (26) |
| eLab | 19 | 234 | result_log (26), order_log (24), elab_result (22), lab_result (20), lab_request (17) |
| Prescription | 4 | 229 | glasses_rx (105), contacts_rx (78), rx (45) |
| Appointment | 10 | 207 | appointment (92), appointment_log (26), appointment_attachment (26) |
| Visit | 16 | 186 | visit (40), visit_follow_up (19), vitals (18), visit_quality_measure (18) |
| Pathology | 8 | 146 | cancer_log (54), pathology_log (36), cancer_log_visit (27) |
| Inventory | 5 | 119 | package_item_sale_utilization (40), package_item_sale (33), package_sale (30) |
| Document Management | 5 | 106 | file_attachment (29), fax_outbound (28), fax_management (26) |
| Diagnosis | 9 | 86 | diagnosis (17), diagnosis_referral_correspondence_id (16), diagnosis_body_location (12) |
| Office Flow | 7 | 78 | task (44), task_note (7), task_staff_assignee (6) |
| CC/HPI | 6 | 68 | hpi_response (17), hpi_response_metadata (17), hpi_follow_up (15) |
| Practice | 7 | 63 | referral_source_link (18), consent_form_patient (9), protocol_log (8) |
| Procedure | 3 | 30 | procedure_metadata (12), procedure_mips_quality (10), procedure_body_location (8) |
| Exam | 4 | 26 | exam_element_metadata (10), exam_element (8), exam_set (6) |

The full inventory of all 197 tables and their fields is in `analysis/entity-inventory-full.json`.

**Declared but empty groupings** (no table entries in the data dictionary):
- **Lookup**: "Static lookup tables for medical and industry codes"
- **MIPS**: "MIPS scores, including overall scores and measure-specific scores"
- **Medical Lookup**: "Static lookup tables for medical content (CC/HPI, Exam, Diagnosis, Procedure, Pathology Log)"

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export is remarkably broad for a specialty EHR, covering both clinical and financial data in depth:

**Strongest areas:**
- **Ophthalmology/optometry pretesting** (25 tables, 1,213 fields): Exceptionally deep specialty clinical data — refraction, visual acuity, keratometry, binocular vision, cover test, color vision, diagnostic drops, contact lens fitting (soft, RGP/hybrid), endothelial counts, pachymetry, central retinal thickness, RNFL thickness, amsler grid, IOP, visual field, duction. Tables like `wearing_contacts` (110 fields), `contacts_trial` (107 fields), and `binocular` (107 fields) reflect the full granularity of eye care measurement sets.
- **Practice management financials** (38 tables, 1,182 fields): Full billing lifecycle — bills, charges, payments (posted and unposted), claims, claim submissions, payer adjustments, accounts receivable, refunds, patient statements, pre-collections, production summaries, billing quotes, transfer of funds. The `bill` table alone has 130 fields.
- **Patient demographics & clinical history** (31 tables, 697 fields): The `patient` table (177 fields) includes demographics, contact info, employment, smoking/social history, health care proxy/advance directives, portal status, and more. Supplemented by insurance_policy (136 fields), guarantor, medical_history, surgical_history, family_history, problem_list, medication, allergy, immunization tables.
- **Prescriptions** (4 tables, 229 fields): Eyeglass Rx (105 fields), contact lens Rx (78 fields), medication Rx (45 fields) — deep specialty-specific prescription data far beyond what any standard clinical exchange would include.

**Moderate areas:**
- **Lab results** (19 tables, 234 fields): Comprehensive electronic lab order/result workflow.
- **Appointments** (10 tables, 207 fields): Full appointment data with waitlists, reminders, authorization, insurance policy linkage.
- **Pathology** (8 tables, 146 fields): Biopsy/pathology specimens, results, notifications, cancer log with visit linkage.
- **Diagnoses** (9 tables, 86 fields): DDX/ADX, body locations, morphology, measurements, referral correspondence.
- **Documents** (5 tables, 106 fields): File attachments, fax management (inbound/outbound).

**Thinner areas:**
- **Procedures** (3 tables, 30 fields): Only procedure metadata, MIPS quality, and body locations. No detailed operative/surgical records, though this is appropriate for an ambulatory eye care product.
- **Exam** (4 tables, 26 fields): Exam elements and metadata — the detailed exam content may be captured in the HPI and diagnosis tables instead.
- **Visit** (16 tables, 186 fields): Visit records, vitals, follow-ups, quality measures, review of systems, chart notes. Reasonable for ambulatory encounters.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `patient` (177 fields): name, DOB, sex, gender identity, sexual orientation, pronouns, race/ethnicity, language, marital status, employment, contacts, addresses (home + seasonal) | Thorough — includes fields well beyond USCDI |
| Encounters / visits | ✅ Covered | `visit` (40 fields), `visit_follow_up` (19), `vitals` (18), `visit_quality_measure` (18), `chart_note` (26), `chart_note_signature` (7) | Solid ambulatory visit model |
| Problems / conditions | ✅ Covered | `problem_list` (17 fields), `diagnosis` (17), `diagnosis_ddx` (5), `diagnosis_adx` (7), `diagnosis_body_location` (12) | Comprehensive with DDX/ADX support |
| Medications / prescriptions | ✅ Covered | `medication` (23 fields), `rx` (45 fields, medication Rx), `glasses_rx` (105), `contacts_rx` (78), `rgp_contacts_rx` | Deep — includes both medication and optical Rx |
| Allergies | ✅ Covered | `allergy` table + `allergy_nkda`/`allergy_other` fields on patient | Present |
| Immunizations | ✅ Covered | `immunization` (26 fields) + registry fields on patient | Present with registry integration |
| Vitals | ✅ Covered | `vitals` (18 fields) | Present |
| Lab results | ✅ Covered | 19 eLab tables: `order_log`, `result_log`, `elab_result`, `lab_result`, `lab_request`, etc. | Comprehensive lab workflow |
| Imaging / diagnostic reports | ✅ Covered | Attachments folder for imaging results + diagnostic equipment integration tables; `file_attachment` (29 fields) | Images in native formats + structured data |
| Procedures | ✅ Covered | `procedure_metadata` (12), `procedure_body_location` (8), `final_bill_procedure`, `original_bill_procedure` | Adequate for ambulatory eye care |
| Clinical notes / documents | ✅ Covered | `chart_note` (26), `chart_note_signature` (7), `file_attachment` (29), `fax_management` (26) | Notes + attachments + faxes |
| Care plans / goals | ⚠️ Partial | `visit_follow_up` (19), `hpi_follow_up` (15) — follow-up plans exist but no explicit care plan entity | No dedicated care plan table; follow-ups partially cover this |
| Orders / referrals | ✅ Covered | `order_log` (24), `order_log_detail`, `referral_source_link` (18), `visit_referral`, `diagnosis_referral` (8) | Orders + referral tracking |
| Insurance / coverage | ✅ Covered | `insurance_policy` (136 fields), `insurance_group_policy` (17), `appointment_insurance_policy`, `bill_insurance` | Exceptionally detailed — 136-field insurance table |
| Claims / billing | ✅ Covered | 38 PM Financials tables: `bill` (130), `charges` (100), `claim` (32), `claim_submission` (18), `claim_payer`, `claim_log`, etc. | Deep billing lifecycle coverage |
| Payments | ✅ Covered | `payments_posted` (54), `payments_received` (15), `patient_payments_unposted`, `refunds`, `transfer_funds`, `bill_cash` | Comprehensive payment tracking |
| Consents / directives | ✅ Covered | `consent_form_patient` (9 fields), `health_care_proxy` and `living_will` fields on patient | Consent forms + advance directives |
| Patient communications | ✅ Covered | `intra_mail` (12), `intra_mail_recipient` (10) — secure messaging | IntraMail messaging present |
| Specialty-specific (eye care) | ✅ Covered | 25 Ophth Pretesting tables (1,213 fields): refraction, visual acuity, keratometry, binocular vision, cover test, color vision, contact lens fitting, pachymetry, OCT measurements, visual field, IOP, amsler grid, diagnostic drops | **Exceptionally deep** — genuine specialty data |

**Gap Analysis Summary**: The export covers nearly every applicable domain. The only notable gap is the absence of a formal care plan entity, though follow-up plans partially fill this role. The three empty groupings (Lookup, MIPS, Medical Lookup) are a documentation gap rather than a data gap — the lookup tables would enable interpretation of coded values but their absence doesn't mean patient data is missing.

## 6. Documentation Quality

**Strengths:**
- **Substantial scope**: 131 pages documenting 197 tables and ~4,670 columns is a serious documentation effort.
- **Table-level descriptions**: Nearly every table (196/197) has a prose description explaining what it stores, its cardinality (e.g., "one row per visit," "zero or more per patient"), and relationships to other data.
- **Longitudinal tracking flags**: Each table's temporal behavior (Y/N/L/S) is documented, telling recipients whether they're getting historical data or current snapshots.
- **Export format documentation**: Clear description of the ZIP structure, pipe-delimited CSV format, and attachments folder.
- **UTC convention**: Explicitly documented that timestamps use UTC unless fields have `_ld` suffix.

**Weaknesses:**
- **No field-level descriptions**: 0 of ~4,670 columns have individual descriptions. A field like `financial_category_id` on the patient table has no explanation of what it means or what values it takes.
- **No data types**: The introduction mentions a "Field Length column" but the actual entries don't include types or lengths.
- **No value sets**: Coded fields (e.g., `status`, `type`, `category` columns) have no documented allowed values. Combined with the missing Lookup/Medical Lookup tables, many coded values would be opaque to a recipient.
- **No relationship documentation**: Foreign keys must be inferred from column naming conventions (e.g., `patient_id` → `patient` table).
- **No sample data**: No example export files or worked examples.
- **Missing groupings**: The Lookup, MIPS, and Medical Lookup groupings are declared but contain no table definitions. Without lookup tables, a recipient cannot interpret coded values in the export.

**Could a developer build an import?** Partially. The table/column structure is clear enough to load the pipe-delimited CSVs into a database. However, interpreting the data would require significant reverse-engineering — foreign key relationships, coded values, and field semantics would all need to be inferred. The documentation is sufficient for loading but insufficient for understanding.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

This export demonstrably covers the breadth of data domains the product stores. For an eye care EHR/PM system, the critical data categories are: (1) clinical eye exam data — covered with exceptional depth via 25 Ophth Pretesting tables and 1,213 fields; (2) billing and financial data — covered with 38 PM Financials tables and 1,182 fields spanning the full billing lifecycle; (3) prescriptions — covered with specialty-specific detail (eyeglass Rx at 105 fields, contact lens Rx at 78 fields); (4) demographics and clinical history — covered thoroughly via a 177-field patient table and 30 supplementary tables; (5) lab results, imaging, documents, messaging — all covered. The export goes far beyond USCDI in both depth (177 fields for demographics vs. ~15 in US Core Patient) and breadth (billing, eye-care pretesting, pathology, inventory, fax management). The only notable absence is a formal care plan entity.

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly a purpose-built EHI export, not a repackaged clinical exchange. The telltale signs: (1) the export uses a native database dump format (pipe-delimited CSVs of internal database tables), not C-CDA or FHIR; (2) table names reflect the internal database schema (e.g., `wearing_rgp_contacts`, `bill_insurance_timely_filing`, `payer_adjustments_rarc`) — not standardized clinical exchange resources; (3) the export includes 38 PM Financials tables and 25 Ophth Pretesting tables that would never appear in a FHIR or C-CDA clinical exchange; (4) the data dictionary is titled "Data Dictionary for ModMed EMA EHI Export" — it's explicitly built for this purpose; (5) the export includes attachments in native formats (JPEG, PNG, TIFF, PDF) alongside the structured data.

### Key Findings

1. **Genuinely deep specialty clinical data**: The 25 Ophth Pretesting tables with 1,213 fields represent one of the most thorough specialty-specific clinical data exports observed. Tables like `contacts_trial` (107 fields), `binocular` (107 fields), and `wearing_contacts` (110 fields) capture the full granularity of eye care measurements — data that has no representation in USCDI or standard clinical exchange formats.

2. **Full billing lifecycle coverage**: 38 PM Financials tables (1,182 fields) covering bills, charges, payments, claims, claim submissions, payer adjustments, accounts receivable, refunds, patient statements, pre-collections, and production summaries. This is among the more comprehensive billing data exports seen in EHI documentation.

3. **Field-level documentation gap**: While table-level documentation is solid (196/197 tables described), none of the ~4,670 individual columns have descriptions, data types, or value set documentation. Combined with the three empty Lookup/MIPS/Medical Lookup groupings, many coded values would be uninterpretable without reverse-engineering.

4. **Shared ModMed EMA data dictionary**: The export documentation is hosted on `modmed.com` and titled "ModMed EMA EHI Export" — it serves multiple ModMed-powered products, not just Eyefinity. This means the PM tables may or may not reflect Eyefinity's specific PM capabilities (e.g., VSP-specific claims integration). The documentation notes "PM tables will be empty for practices not using PM."

5. **No sample data or lookup tables**: The absence of sample export files and lookup/reference tables means a data recipient would face significant interpretation challenges despite the structural completeness.

### Summary Stats

    Coverage:        Comprehensive
    Approach:        Purpose-built EHI export
    Export format:   Pipe-delimited CSV (one file per table) + native format attachments, in ZIP
    Entities:        197 tables (across 16 groupings; 3 additional groupings declared but empty)
    Fields:          ~4,670
    Descriptions:    0% of fields (table-level descriptions: 99.5%)
    Sample data:     No
    Bulk export:     Yes (single or multiple/all patients)
    Domains covered: 17 of 18 applicable domains (care plans partial)

### Bottom Line

This is a strong (b)(10) export. A patient or provider would receive a comprehensive copy of their data spanning clinical eye care measurements, billing records, prescriptions, lab results, demographics, and more — all in a machine-readable format. The biggest weakness is documentation depth at the field level: the ~4,670 columns have names but no descriptions, types, or value sets, meaning a recipient can load the data but would struggle to fully interpret coded values without the missing lookup tables.
