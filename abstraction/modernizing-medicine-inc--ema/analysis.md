# EHI Export Analysis: Modernizing Medicine Inc.

**Product**: EMA (Electronic Medical Assistant) v7
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2002.EMA6.70.18.1.221129 (CHPL ID 11032)

## 1. Product Context

ModMed EMA is a cloud-based, specialty-specific EHR and practice management platform serving 11 medical specialties (dermatology, ophthalmology, orthopedics, gastroenterology, ENT, OB/GYN, pain management, plastic surgery, podiatry, urology, and allergy/immunology). The company serves 40,000+ providers and was valued at $5.3B in a 2025 acquisition by Clearlake Capital.

EMA is not a generic EHR — it is an all-in-one platform combining:

- **Clinical EHR**: Specialty-specific charting with an Interactive Anatomical Atlas, Virtual Exam Room, AI-powered documentation (ModMed Scribe), and specialty content libraries
- **Practice Management (PM)**: Scheduling, billing, claims management, clearinghouse interfaces, denial tracking
- **Revenue Cycle Management**: Full claims lifecycle from charge capture through patient billing
- **E-Prescribing**: Integrated prescription management including controlled substances
- **Lab Integration**: Electronic lab orders and results from connected clinical, pathology, and genetic labs
- **Ophthalmic Image Management**: DICOM import from diagnostic devices (OCTs, visual fields, corneal topographers, fundus cameras)
- **Pathology Module**: Dermatopathology results tracking
- **Patient Portal (APPatient)**: Secure messaging, appointment scheduling, payment, health data access
- **Inventory Management**: Supply ordering and expense tracking
- **Telehealth**: Virtual visit scheduling and documentation
- **Klara Integration**: Multi-channel patient communication (acquired 2022)

For assessing export completeness, the key question is whether the export covers clinical data across all 11 specialties, the full PM/billing lifecycle, specialty-specific data (particularly ophthalmology pretesting), and patient-facing content — not just a USCDI clinical summary.

## 2. Artifacts Reviewed

| Artifact | Size | Description | Informativeness |
|---|---|---|---|
| `ModMed-EMA-EHI-Export-Data-Dictionary.pdf` | 772 KB, 96 pages | Overview data dictionary — table inventory with ~420 tables across 19 groupings, descriptions, relationships, longitudinal tracking, product/vertical assignments, and 8 value-set appendices | **High** — primary structural reference |
| `ModMed-EMA-Detailed-Data-Dictionary.pdf` | 868 KB, 210 pages | Field-level data dictionary — 5,250 field entries across ~257 tables with column names, descriptions, data types, nullability, field lengths, and value/coding schema references | **High** — definitive field-level detail |
| `onc-certification-page.png` | 755 KB | Screenshot of ModMed's ONC certification page showing the "EHI Export Documentation" section with link to the data dictionary PDF | **Low** — confirms documentation location |
| `enrichment/overview-table-inventory.json` | 217 KB | Pre-extracted JSON of overview table inventory (411 entries) — used as reference but found to have parsing issues | **Medium** — useful but required verification |
| `enrichment/detailed-data-dictionary.json` | 1.66 MB | Pre-extracted JSON of detailed data dictionary (5,250 entries) — had systematic column shift (dataType/nullable misaligned) | **Medium** — required correction |
| `overview-dd-xml.xml` / `detailed-dd-xml.xml` | 666 KB / 3.5 MB | Intermediate pdftohtml XML used by enrichment extraction scripts | **Low** — intermediate artifacts |

The two PDFs (306 pages combined) are the definitive artifacts. No sample data files, no machine-readable schemas (JSON/XML), and no export procedure documentation were provided.

## 3. Export Mechanics

- **Format**: Native relational database model — tables with typed columns. The documentation does not specify the actual file format (CSV, JSON, database dump, etc.), only that data is organized as named tables with defined columns. The detailed DD was originally a Google Sheets spreadsheet (per PDF metadata), suggesting the vendor maintains the dictionary in tabular form.
- **Mechanism**: The ONC certification page has a section labeled "EHI Export Documentation" linking to the data dictionary PDF. No export request procedure, UI workflow, or API endpoint is documented in the public-facing materials. The document references a "training manual" for more detailed usage information, suggesting export initiation is documented internally but not publicly.
- **Single-patient**: Explicitly titled "Single Patient Export" throughout both documents. No mention of bulk export capability.
- **Access constraints**: The data dictionary carries a confidentiality notice: *"This dictionary is the sole property of Modernizing Medicine, Inc. By accessing or using the dictionary you hereby agree to maintain the dictionary and its contents in confidence."*
- **Fees**: Not documented.
- **Notes on PM data**: The overview DD explicitly notes that "Practice Management (PM) tables and columns are included in the dataset and will be empty for practices not using PM," confirming that PM data is part of the export structure even when empty.

## 4. Export Content: What's In It

The export documentation describes a comprehensive native database model with two levels of detail:

**Overview Data Dictionary (96 pages)**:
- ~420 table entries across 19 logical groupings
- Each table has: IDX, grouping, table name, description, relationships (foreign key references), longitudinal tracking indicator (Y/N/L/S), product/vertical assignment, financial priority flag, and refresh frequency
- 8 appendices defining value sets for coded fields (Ophth Usage, Visual Acuity, Fax Status, Patient History, Visit Bill As, Immunization Public, Cancer Log Values, HPI Follow Up)

**Detailed Data Dictionary (210 pages)**:
- 5,250 field entries across ~257 tables
- Each field has: IDX, grouping, table, column name, description, SQL data type, nullable flag, field length, and values/coding schema reference
- 100% of fields have descriptions (verified by parsing)
- 93% of fields have explicit data types (string: 3,348; boolean: 498; double: 468; timestamp: 343; int: 159; date: 67; bigint: 1; ~366 fields where type could not be extracted due to PDF text wrapping)
- ~301 fields reference appendix value sets (e.g., "See Appendix A", "See Appendix B")

**Relationship between the two documents**: The overview DD documents all ~420 tables at the table level (with descriptions and relationships), while the detailed DD provides field-level documentation for 257 of those tables. The ~163 tables in the overview but not in the detailed DD are primarily lookup/reference tables (Medical Lookup: 20, Practice configuration: ~80, Lookup: 7, MIPS: 9) that are static/system tables rather than patient-specific data tables.

### Vendor's own content organization

The vendor organizes the export into 19 groupings. The detailed field-level data dictionary covers 16 of these (excluding Medical Lookup, MIPS, and Lookup which are reference tables). Field counts are from the corrected parse of the detailed data dictionary:

| Grouping | Overview Tables | Detailed Tables | Fields | Key Tables |
|---|---|---|---|---|
| PM Financials | 77 | 41 | 1,818 | `bill` (119), `patient_adjustments` (154), `accounts_receivable` (140), `payments_received` (136), `charges` (110), `production_summary` (121) |
| Patient | 53 | 51 | 1,067 | `patient` (195), `insurance_policy` (149), `patient_flag` (118), `allergy`, `immunization`, `family_history` |
| eLab | 21 | 27 | 380 | `result_log`, `lab_request`, `elab_order`, `lab_result`, `order_log` |
| Prescription | 7 | 4 | 342 | `glasses_rx` (110), `rgp_contacts_rx` (109), `contacts_rx`, `rx` |
| Appointment | 15 | 22 | 268 | `appointment` (97), `appointment_insurance_policy`, `recall`, `appointment_reminder` |
| CC/HPI | 9 | 9 | 228 | `hpi_response_metadata` (131), `hpi_follow_up`, `hpi_option`, `hpi_response` |
| Visit | 17 | 35 | 198 | `visit`, `vitals`, `final_bill_diagnosis`, `visit_follow_up`, `ros`, `outcome` |
| Diagnosis | 13 | 17 | 195 | `diagnosis`, `diagnosis_morphology`, `diagnosis_body_location`, `diagnosis_referral` |
| Ophth Pretesting | 25 | 25* | ~1,200+* | `visual_acuity`, `refraction`, `keratometry`, `binocular`, `pupil`, `cover_test`, `iop`, `visual_field`, `diagnostic_drops` (25 tables) |
| Pathology | 10 | 14 | 123 | `cancer_log`, `pathology_result`, `biopsy_log` |
| Inventory | 20 | 5 | 120 | `product_sales` (145), `package`, `stock`, `cabinet` |
| Office Flow | 12 | 10 | 102 | `task`, `facility_resource_utilization_log`, `task_fax_inbound` |
| Document Management | 7 | 4 | 92 | `fax_outbound`, `fax_inbound`, `fax_management`, `file_attachment` |
| Practice | 88 | 7 | 64 | `referral_contact`, `consent_form_patient`, `staff`, `facility` |
| Procedure | 6 | 6 | 45 | `procedure`, `procedure_metadata`, `procedure_body_location` |
| Exam | 4 | 4 | 27 | `exam_element`, `exam_element_metadata`, `exam_set` |
| Medical Lookup | 20 | — | — | Static medical reference tables (ICD, SNOMED, LOINC, etc.) |
| MIPS | 9 | — | — | Quality measure tracking tables |
| Lookup | 7 | — | — | System lookup tables |

*\*Note: The Ophth Pretesting grouping has 25 tables documented at the overview level with individual table descriptions. The detailed DD documents these across multiple sub-groupings (visual_acuity, refraction, binocular, etc.) but PDF parsing artifacts affected table-to-field attribution for this section. The overview DD documents approximately 1,200+ fields across these 25 tables based on the sub-grouping field counts in the enrichment extraction (visual_acuity: 93, wearing_contacts: 110, contacts_trial: 106, rgp_contacts_trial: 104, wearing_rgp_contacts: 103, color_vision: 89, binocular: 107, refraction: 82, cover_test: 82, wearing_glasses: 90, diagnostic_drops: 61, and others).*

The complete entity inventory with all 5,250 parsed field entries is saved to `analysis/full-entity-inventory.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

ModMed's export is organized into 19 groupings that span clinical, financial, operational, and specialty-specific domains. Key observations:

**PM Financials is the largest category** with 1,818 fields (34.6% of all fields) across 77 tables. This includes bills, charges, payments (received and posted), accounts receivable, patient adjustments, payer adjustments, claims, claim scrubbing, billing quotes, custom codes, production summaries, refunds, unposted charges, and financial categories. This is exceptionally deep — most EHR vendors either exclude billing data from their EHI export entirely or provide only minimal charge data.

**Patient is the second-largest** with 1,067 fields across 53 tables. The `patient` table alone has 195 fields, and `insurance_policy` has 149 fields. This grouping covers demographics, insurance, allergies, immunizations, family history, pregnancy, gynecological history, social history, medical history, surgical history, specialty history, guarantor information, and patient contact data.

**Ophth Pretesting is the signature specialty section** with 25 tables covering ophthalmology-specific diagnostic measurements: visual acuity, refraction, keratometry, binocular testing, pupil exam, motility, cover testing, light reflex, visual fields, intraocular pressure, diagnostic drops (dilation), central retinal thickness, RNFL thickness, pachymetry, endothelial counts, amsler grid, color vision, infant vision, and contact lens trials. Each table has dedicated visual acuity sub-measurements. This is specialty depth rarely seen in EHI exports.

**eLab (380 fields)** covers electronic lab orders, results, and result logs comprehensively. **Prescription (342 fields)** includes separate tables for medication Rx, contact lens Rx, glasses Rx, and RGP contact lens Rx — reflecting the ophthalmology specialty.

**Thinner areas**: Exam (27 fields across 4 tables) and Procedure (45 fields across 6 tables) are relatively thin compared to the product's clinical documentation capabilities, though this may reflect that much clinical documentation is captured through the HPI/Diagnosis workflow rather than separate exam tables.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `patient` (195 fields), `patient_race`, `patient_ethnicity`, `patient_language`, `patient_phone_number`, `patient_address`, `patient_email` | Thorough — 195 fields on the patient table alone |
| Encounters / visits | ✅ Covered | Visit grouping: 17 tables including `visit`, `visit_attending_provider`, `visit_code`, `visit_follow_up` | Solid — covers visit metadata, attending providers, and follow-up |
| Problems / conditions | ✅ Covered | Diagnosis grouping: 13 tables including `diagnosis`, `diagnosis_body_location`, `diagnosis_morphology`, `diagnosis_referral`, `diagnosis_lab` | Deep — includes morphology, body location mapping, and lab linkages |
| Medications / prescriptions | ✅ Covered | Prescription grouping: 7 tables, 342 fields including `rx`, `glasses_rx` (110 fields), `contacts_rx`, `rgp_contacts_rx` (109 fields), `compound_rx` | Very thorough — includes specialty optical prescriptions |
| Allergies | ✅ Covered | `allergy` table in Patient grouping | Present |
| Immunizations | ✅ Covered | `immunization` table in Patient grouping; Appendix F documents immunization value sets | Present with coded values |
| Vitals | ✅ Covered | `vitals` table in Visit grouping | Present |
| Lab results | ✅ Covered | eLab grouping: 21 tables, 380 fields including `result_log`, `lab_result`, `result_log_detail_diagnosis`, `lab_note`, `lab_attachment` | Deep — includes result logs, attachments, and diagnostic linkages |
| Imaging / diagnostic reports | ⚠️ Partial | `file_attachment` in Document Management logs file metadata. Overview DD explicitly states "Physical attachments are excluded." Ophth Pretesting tables capture diagnostic measurement DATA but not the images themselves. | Images (DICOM files) are excluded. Diagnostic measurements are captured. This is a gap for the image-heavy ophthalmology specialty. |
| Procedures | ✅ Covered | Procedure grouping: 6 tables including `procedure`, `procedure_metadata`, `procedure_body_location` | Present |
| Clinical notes / documents | ⚠️ Partial | `chart_note` and `chart_note_signature` in Patient grouping; `chart_segmentation_event` for chart status. Document Management captures fax/file metadata (92 fields). | Chart note metadata is present, but the depth of note content (full text vs. metadata only) is unclear from the dictionary alone. Physical document contents are excluded. |
| Care plans / goals | ⚠️ Partial | `visit_follow_up` and `visit_follow_up_reason` in Visit grouping | Follow-up tracking exists but no dedicated care plan entity |
| Orders / referrals | ✅ Covered | `diagnosis_referral` in Diagnosis; `referral_contact`, `referral_institution` in Practice; lab orders in eLab grouping | Referral and lab order workflows covered |
| Insurance / coverage | ✅ Covered | `insurance_policy` (149 fields), `insurance_company`, `insurance_plan`, `appointment_insurance_policy` in Patient grouping | Exceptionally deep — 149 fields on insurance_policy alone |
| Claims / billing | ✅ Covered | PM Financials: 77 tables, 1,818 fields including `bill` (119 fields), `charges` (110 fields), `claims`, `claim_scrub_result`, `billing_quote` | Most comprehensive billing coverage seen — 34.6% of all fields |
| Payments | ✅ Covered | `payments_received` (136 fields), `payments_posted` (100 fields), `payer_adjustments` (98 fields), `patient_adjustments` (154 fields), `refunds` in PM Financials | Very thorough — separate tables for payments received, posted, adjustments, and refunds |
| Consents / directives | ⚠️ Partial | `consent_form_patient` in Practice grouping | Present but limited detail |
| Patient communications / portal messages | ❌ Not covered | No tables for patient portal messages, patient-initiated communications, or Klara messaging platform data | Product has APPatient portal and Klara messaging — their absence is a gap |
| Specialty-specific (Ophthalmology) | ✅ Covered | 25 Ophth Pretesting tables (~1,200+ fields) covering visual acuity, refraction, keratometry, binocular, pupil, motility, cover test, IOP, visual fields, pachymetry, etc. | Exceptional specialty depth — likely the most detailed specialty export documented |
| Specialty-specific (Other specialties) | ⚠️ Partial | Product/Vertical column in overview assigns tables to specialties (OPHTHALMOLOGY, DERMATOLOGY, etc.). `cancer_log` tables in Pathology grouping serve dermatology. | Ophthalmology and dermatology pathology are well-covered; coverage for other 9 specialties is unclear |
| Inventory | ✅ Covered | Inventory grouping: 20 tables, 120 fields including `product_sales` (145 fields), `package`, `stock` | Rarely seen in EHI exports — notable inclusion |

## 6. Documentation Quality

**Strengths:**
- **Comprehensive scope**: 306 pages across two PDFs documenting ~420 tables and 5,250 fields
- **100% field descriptions**: Every field in the detailed DD has a description — not just a column name
- **Typed and sized**: Data types, nullability, and field lengths documented for all fields
- **Relationship documentation**: Table relationships (foreign keys) documented in the overview DD
- **Value set appendices**: 8 appendices define coded values for fields like visual acuity, fax status, patient history, immunization, cancer log, and HPI follow-up (~301 fields reference appendices)
- **Longitudinal tracking indicators**: Each table indicates whether change history is maintained (Y/N/L/S), enabling a developer to understand data temporality
- **Product/Vertical assignments**: Tables indicate which specialty modules they serve
- **Recently updated**: PDFs dated January 2026 (per URL path)

**Weaknesses:**
- **No export format specification**: The actual file format of the export (CSV, JSON, SQL dump, etc.) is not documented anywhere. A developer receiving the export would need to discover the format empirically.
- **No sample data**: No example exports, sample records, or test datasets are provided. A developer cannot preview what the exported data looks like.
- **No export procedure documentation**: No public instructions on how to request, initiate, or receive an export. The document references an internal "training manual."
- **PDF-only format**: The data dictionary is only available as PDF (originally Google Sheets). No machine-readable schema (JSON Schema, SQL DDL, XML Schema) is provided. Parsing the PDF requires significant effort — both extraction scripts and my own parsing encountered column alignment issues.
- **Confidentiality restriction**: The dictionary carries a confidentiality notice restricting sharing without ModMed's written authorization.
- **Ophth Pretesting documentation gap**: While the overview DD documents all 25 Ophth Pretesting tables with descriptions, the relationship between the detailed DD's sub-groupings (e.g., "Ophth Pretesting visual_acuity", "Ophth Pretesting binocular") and the overview's table names is not always clear due to PDF formatting.

**Could a developer build an import?** Mostly yes, but with significant caveats. The field names, types, descriptions, and relationships provide enough structural information to build a data model. However, the missing export format specification and absence of sample data mean a developer would need access to an actual export to determine file structure, delimiters, encoding, and value formats before writing import logic.

## 7. Overall Assessment

### Classification

**Comprehensive native export**

ModMed EMA's EHI export documentation describes a genuine, broad native data model export with solid documentation. It covers clinical, billing, scheduling, inventory, and specialty-specific domains — well beyond what a clinical summary or FHIR projection would provide. The PM Financials grouping alone (1,818 fields across 77 tables) demonstrates that this is not a repackaged clinical summary.

### Key Findings

1. **Billing data is the deepest domain** — PM Financials accounts for 34.6% of all documented fields (1,818 of 5,250) across 77 tables. This is exceptional; most EHR vendors either exclude billing entirely or provide minimal charge data. Tables like `patient_adjustments` (154 fields), `accounts_receivable` (140 fields), and `payments_received` (136 fields) indicate genuine database-level export.

2. **Ophthalmology specialty data is uniquely comprehensive** — 25 dedicated Ophth Pretesting tables (~1,200+ fields) cover visual acuity, refraction, keratometry, binocular tests, pupil exam, IOP, visual fields, pachymetry, and more. This level of specialty-specific export data is rarely seen and reflects ModMed's ophthalmology market strength.

3. **Documentation quality is high but format is problematic** — 306 pages, 100% field descriptions, typed and sized fields, relationship mapping, and value set appendices. However, the PDF-only format with no machine-readable schema or sample data creates a significant barrier to actually using the export.

4. **Patient portal and messaging data appears absent** — Despite the product having APPatient portal and Klara messaging integration, no tables for patient-initiated messages, portal content, or communication logs are visible in the export. This is a notable gap for a product that explicitly provides patient communication features.

5. **Image content is explicitly excluded** — The overview DD states "Physical attachments are excluded" from the Document Management grouping. For an ophthalmology-focused product that captures DICOM images from OCTs, visual fields, and fundus cameras, the absence of actual image data (vs. measurement data) is a gap, though measurement values from these tests are captured in the Ophth Pretesting tables.

### Summary Stats

```
Classification:  Comprehensive native export
Export format:   Native relational (actual file format unspecified — tables with typed columns)
Model type:      Native database model
Entities:        ~420 tables documented (overview); 257 with field-level detail
Fields:          5,250 (in detailed DD)
Descriptions:    100% of fields have descriptions
Sample data:     No
Bulk export:     No (single-patient only)
Domains covered: 14 of 19 applicable domains (✅ or better)
```

### Bottom Line

ModMed EMA provides one of the more comprehensive EHI export documentations available — a genuine native database export covering clinical workflows, billing/claims, specialty ophthalmology data, lab results, prescriptions, inventory, and scheduling across ~420 tables and 5,250 fields. The single biggest strength is the depth of billing data (1,818 fields) and specialty-specific clinical data. The most significant gaps are the absence of patient portal/messaging data, the exclusion of image file content, and the lack of export format specification or sample data — a developer knows *what* will be exported but not *how* it will be delivered.
