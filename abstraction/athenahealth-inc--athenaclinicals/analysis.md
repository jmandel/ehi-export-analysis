# EHI Export Analysis: athenahealth, Inc.

**Product**: athenaClinicals for Hospitals and Health Systems
**Analysis date**: 2026-02-16
**CHPL IDs**: 11613 (athenaClinicals for Hospitals and Health Systems, certified 2025-03-21), 11714 (athenaClinicals ambulatory, certified 2025-10-28)

## 1. Product Context

athenahealth's **athenaOne** is a fully integrated, cloud-based platform combining EHR (athenaClinicals), billing/practice management (athenaCollector), and patient engagement (athenaCommunicator). It serves 170,000+ providers across ~6,800 organizations. The platform supports 60+ medical specialties.

The **athenaClinicals for Hospitals and Health Systems** product (CHPL 11613) extends the ambulatory platform with inpatient capabilities derived from the 2015 acquisitions of RazorInsights and webOMR. It targets critical access and community hospitals, typically under 100 beds.

**Data the product stores (relevant to export completeness):**
- **Clinical data**: Demographics, encounters, conditions/diagnoses, medications (active/historical/denied/procedure), allergies, labs, imaging, vitals, immunizations, procedures (including surgical with roles/times/checklists), clinical notes (SOAP, H&P, discharge summaries, consult notes), care plans, goals, family/social/medical/surgical history, OB/GYN data, eye care, cancer cases, physical therapy episodes, screening questionnaires, devices, clinical decision support alerts
- **Billing/financial**: Claims (details, transactions, notes, attachments), payments, patient insurance, billing statements, outstanding balances, payment plans, referral authorizations, appointments, charges
- **Patient engagement**: Secure messaging (via athenaCommunicator), appointment reminders, digital intake forms, telehealth records
- **Hospital-specific**: ED documentation (triage, assessment, course, provider notes), nursing documentation (admission, notes, tasks, care plan), flowsheets (vitals, ADLs, I&O, airways, drains, lines, measurements), discharge planning, medication administration records (MAR), orders, transfer orders, respiratory/therapy tasks

## 2. Artifacts Reviewed

| Artifact | Description | Size/Scope | Informativeness |
|---|---|---|---|
| `downloads/enrichment/datasets.json` | Structured catalog of all 133 datasets extracted from Contentful API | 46 KB, 133 datasets across 4 export modules | **Most informative** — definitive dataset list |
| `downloads/inpatient-clinical-ehi-export.pdf` | Data dictionary for inpatient clinical export | 37 pages, 38 datasets with HTML template specs | **Most informative** — only artifact with field-level specifications |
| `downloads/ambulatory-clinical-ehi-export.pdf` | Data dictionary for ambulatory clinical export | 10 pages, 64 datasets listed with external API spec links | Moderately informative — dataset list + 2 inline field specs |
| `downloads/ambulatory-collector-ehi-export.pdf` | Data dictionary for ambulatory collector (billing) export | 7 pages, 15 datasets with external API spec links | Moderately informative — dataset list + attachment specs |
| `downloads/inpatient-collector-ehi-export.pdf` | Data dictionary for inpatient collector (billing) export | 7 pages, 16 datasets with external API spec links | Moderately informative — same as ambulatory collector + 1 extra dataset |
| `downloads/api-ambulatory-clinical.json` | Contentful API response for ambulatory clinical page | 78 KB | Informative — structured rich text with dataset list |
| `downloads/api-ambulatory-collector.json` | Contentful API response for ambulatory collector page | 45 KB | Informative — structured rich text with dataset list |
| `downloads/api-inpatient-clinical.json` | Contentful API response for inpatient clinical page | 52 KB | Informative — structured rich text with dataset list |
| `downloads/api-inpatient-collector.json` | Contentful API response for inpatient collector page | 44 KB | Informative — structured rich text with dataset list |
| `downloads/api-welcome-exports.json` | Welcome page content describing export use cases | 15 KB | Context — describes single/multi/bulk export modes |
| `downloads/api-release-notes.json` | Release notes page content | 785 bytes | Uninformative — empty placeholder ("set to be released within 2023") |
| Screenshots (7 files) | Browser screenshots of the documentation portal | ~1.5 MB total | Supplementary — confirm page layouts |

**PDF metadata**: All four PDFs were created on September 22, 2023. Total documentation: 61 pages.

## 3. Export Mechanics

**Format:**
- **Ambulatory Clinical**: Newline Delimited JSON (NDJSON). Each dataset is a `.json` file. Supporting documents (encounter summaries, imaging results, scanned documents) are included as XML, JPEG, PNG, TIFF, or PDF files.
- **Ambulatory Collector**: NDJSON with supporting image/PDF files for insurance cards, claim attachments.
- **Inpatient Clinical**: HTML files viewable in a browser. If the customer also has ambulatory departments, structured NDJSON (same as ambulatory clinical) is also provided.
- **Inpatient Collector**: NDJSON (same format as ambulatory collector), plus a "Visits and Charge Details" dataset.

**Mechanism**: UI-initiated export within athenaOne. Three use cases documented:
1. **Single patient** — individual patient export
2. **Multi-patient** — selected patients
3. **Bulk/all-patient** — all patients in the practice (for practice detachment/termination)

**Access constraints**: No fees mentioned. Export appears to be a standard feature available to customers. Documentation is publicly accessible (no authentication required).

**Patient identifiers**: Each NDJSON line includes FIRSTNAME, LASTNAME, DOB, SSN, ATHENA PATIENT ID, ENTERPRISE ID, MOBILE PHONE, HOME PHONE, and ADDRESS for patient matching across datasets.

## 4. Export Content: What's In It

### Overview

The export is organized into **four modules** covering two care settings (ambulatory, inpatient) and two data domains (clinical, billing/collector):

| Module | Datasets | Format | Attachments |
|---|---|---|---|
| Ambulatory Clinical | 64 | NDJSON | 15 datasets include attachments |
| Ambulatory Collector | 15 | NDJSON | 4 datasets include attachments |
| Inpatient Clinical | 38 | HTML | Documents embedded as images |
| Inpatient Collector | 16 | NDJSON | 4 datasets include attachments |
| **Total** | **133** | | **23 with attachments** |

### Data dictionary detail

Field-level documentation varies significantly by module:

- **Ambulatory Clinical (64 datasets)**: Field specifications are **by external reference** — each dataset links to either athenahealth's proprietary REST API documentation (`docs.athenahealth.com/api/api-ref/...`) or FHIR R4 resource documentation (`docs.athenahealth.com/api/fhir-r4/...`). Two datasets have inline field specs: **Care Plan Events** (13 fields: 2 input + 11 output, all with types and descriptions) and **Eye Care Specific Measurements** (5 sections per encounter). 10 of the 64 datasets reference FHIR R4 resources; the remaining 54 reference athena's proprietary API.

- **Ambulatory Collector (15 datasets)**: Same by-reference approach as ambulatory clinical. Each dataset links to athena's API docs. Two inline specs for attachment handling (Referral Authorization Attachments, Claim Attachments).

- **Inpatient Clinical (38 datasets)**: **Most detailed** — the 37-page PDF provides HTML template-level field specifications for all 38 datasets. These describe the HTML structure, field names, types, and descriptions. My parser extracted 165 fields across the 38 datasets (see `analysis/inpatient-clinical-fields.json`). The most field-rich datasets: Patient Demographics (12 fields), Admission H&P (17 fields/sections), Admission Order (14 fields), Lab Results (12 fields), Medication Administration Record (8 fields).

- **Inpatient Collector (16 datasets)**: Same as ambulatory collector (15 datasets) plus "Visits and Charge Details."

### Specification standards breakdown

| Standard | Dataset Count | Description |
|---|---|---|
| athena REST API | 84 | References to proprietary API docs |
| Inline documentation | 39 | Field specs in PDF (mostly inpatient clinical) |
| FHIR R4 | 10 | References to FHIR R4 resource docs |

**FHIR R4 datasets** (ambulatory only): Care Plan, Care Team Members, Devices or Medical Equipment, Encounters, Goals, Health Concerns (Conditions & Problems), Immunizations, Medications (MedicationRequest), Observations, Procedures.

### Vendor's own content organization

The vendor organizes exports by care setting and data domain. Below are representative datasets by module:

**Ambulatory Clinical (64 datasets)** — key datasets by domain:

| Dataset | Spec Standard | Attachments | Domain |
|---|---|---|---|
| Allergies | athena REST API | No | Allergies |
| Assessment and Plan | athena REST API | No | Conditions |
| Cancer Cases | athena REST API | No | Specialty |
| Care Plan | FHIR R4 | No | Care Plans |
| Care Plan Events | Inline (13 fields) | No | Care Plans |
| Chief Complaint | athena REST API | No | Encounters |
| Clinical Documents | athena REST API | Yes | Documents |
| Encounter Documents | athena REST API | Yes | Documents |
| Encounters | FHIR R4 | No | Encounters |
| Eye Care Specific Measurements | Inline (5 sections) | No | Specialty |
| Family History | athena REST API | No | History |
| Health Concerns – Conditions & Problems | FHIR R4 | No | Conditions |
| Imaging Results | athena REST API | Yes | Lab/Imaging |
| Immunizations | FHIR R4 | No | Immunizations |
| Lab Results | athena REST API | Yes | Lab/Imaging |
| Medications | FHIR R4 | No | Medications |
| OB Episodes | athena REST API | No | Specialty |
| Observations (incl. Vital Measurements) | FHIR R4 | No | Vitals |
| Orders – Labs, Imaging, Consult & Procedures | athena REST API | Yes | Orders |
| Procedures | FHIR R4 | No | Procedures |
| Screening | athena REST API | No | Vitals |
| Social History | athena REST API | No | History |
| Surgical Orders | athena REST API | No | Procedures |
| Vitals | athena REST API | No | Vitals |

**Ambulatory Collector (15 datasets):**

| Dataset | Spec Standard | Attachments | Domain |
|---|---|---|---|
| Appointments | athena REST API | No | Billing |
| Appointment Ticklers & Reminders | athena REST API | No | Billing |
| Claim Attachments | athena REST API | Yes | Billing |
| Claim Details | athena REST API | No | Billing |
| Claim Notes | athena REST API | No | Billing |
| Claim Transactions | athena REST API | No | Billing |
| Demographics | athena REST API | No | Demographics |
| Patient - Billing Statements and Summaries | athena REST API | Yes | Billing |
| Payment History (incl. Patient Refunds) | athena REST API | No | Billing |
| Patient Insurance | athena REST API | Yes | Insurance |
| Patient Outstanding Balance & Patient Unapplied | athena REST API | No | Billing |
| Payment Plans | athena REST API | No | Billing |
| Pre-payment Plans | athena REST API | No | Billing |
| Referral/Auth | athena REST API | Yes | Orders |
| Return to Office | athena REST API | No | Billing |

**Inpatient Clinical (38 datasets)** — with parsed field counts from the 37-page PDF:

| Dataset | Fields Parsed | Domain |
|---|---|---|
| Patient Demographics information | 12 | Demographics |
| Admission H&P | 17 | Clinical Notes |
| Admission Order | 14 | Orders |
| Consult Notes | 5 | Clinical Notes |
| Discharge Summary | 7 | Clinical Notes |
| Lab Results | 12 | Lab/Imaging |
| Imaging Results | 5 | Lab/Imaging |
| Medication Administration Record | 8 | Medications |
| Nursing Care Plan | 4 | Care Plans |
| Orders | 6 | Orders |
| Flowsheet Vitals | 4 | Vitals |
| Flowsheet ADL/ADLs | 4 each | Vitals |
| Flowsheet Intake & Output | 4 | Vitals |
| Transfer Orders | 6 | Orders |
| ED Course / ED Provider Notes / ED Triage Notes | 0–2 | Clinical Notes |
| Discharge Planning Audit/Notes | 4 each | Clinical Notes |

**Inpatient Collector (16 datasets):** Same as ambulatory collector (15 datasets) plus **Visits and Charge Details** (referencing hospital-systems-visit API).

The full entity inventory with all 133 datasets and their parsed fields is in `analysis/full-entity-inventory.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export is organized into four modules, and coverage is genuinely broad:

**Clinical documentation (64 ambulatory + 38 inpatient datasets):** This is the richest area. The ambulatory clinical export covers the full breadth of outpatient clinical data — encounters, notes, conditions, medications, allergies, labs, imaging, vitals, immunizations, procedures (with detailed surgical documentation including roles, times, timeout checklists, pre-sedation assessments, and vitals), screening questionnaires, care plans/goals, and documents. It also includes specialty-specific data: OB/GYN (episodes, history, perinatal), eye care measurements, cancer cases, and physical therapy episodes.

The inpatient clinical export adds hospital-specific sections not found in ambulatory: ED documentation (5 note types), nursing documentation (admission notes, notes, care plans, tasks), 9 different flowsheet types (vitals, ADLs, airways, drains, head-to-toe, intake & output, lines, measurements), medication administration records, discharge planning (audit, notes, instructions, summary), respiratory/therapy tasks, surgical pre-op notes, transfer orders, and orders.

**Billing/financial (15 ambulatory + 16 inpatient datasets):** Claims data is thoroughly covered — claim details, transactions, notes, and attachments. Payment history (including refunds), patient insurance (with card images), billing statements and summaries, outstanding balances, payment plans, and pre-payment plans are all separate datasets. Referral/auth data and appointments (with ticklers/reminders) round out the billing module. The inpatient collector adds "Visits and Charge Details" for hospital-specific billing.

**Thinnest areas:** The collector (billing) datasets are well-enumerated but field-level documentation is entirely by external reference — there are no inline field specs in the billing PDFs beyond the attachment handling specs. Demographics are covered but only as a single dataset referencing the Patient API.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Demographics` (collector), `Patient Demographics information` (inpatient clinical, 12 parsed fields) | Thorough — includes name, address, phone, SSN, DOB, sex, ethnicity, race, language, marital status |
| Encounters / visits | ✅ Covered | `Encounters` (FHIR R4), `Encounter Summary`, `Encounter Documents`, `Encounter Phone Call Checklists` (ambulatory); inpatient has implicit encounters via Admission H&P, ED notes, Discharge Summary | Thorough |
| Problems / conditions / diagnoses | ✅ Covered | `Health Concerns – Conditions & Problems` (FHIR R4), `Assessment and Plan`, `Chief Complaint`; inpatient: diagnoses in Admission H&P, ED assessments | Thorough |
| Medications / prescriptions | ✅ Covered | `Medications` (FHIR R4, includes Procedure Medications, Denied Medications, Prescribed Vaccines), `Prescription Documents`; inpatient: `Medication Administration Record` (8 fields), home medications in Admission H&P | Thorough — covers active, historical, denied, procedure, and administered meds |
| Allergies | ✅ Covered | `Allergies` (ambulatory), allergies sections in inpatient H&P, ED assessments, Discharge Summary | Thorough |
| Immunizations | ✅ Covered | `Immunizations` (FHIR R4) | Covered |
| Vitals | ✅ Covered | `Vitals`, `Observations` (FHIR R4, includes vital measurements); inpatient: `Flowsheet Vitals` + 8 other flowsheet types, `Procedure Vitals` | Thorough — especially rich for inpatient with 9 flowsheet types |
| Lab results | ✅ Covered | `Lab Results`, `Interpretations` (ambulatory); `Lab Results` (inpatient, 12 parsed fields including analyte, value, abnormal flag, ref range, units, note columns) | Thorough |
| Imaging / diagnostic reports | ✅ Covered | `Imaging Results` (ambulatory, with attachments); `Imaging Results` (inpatient, 5 parsed fields) | Thorough |
| Procedures | ✅ Covered | `Procedures` (FHIR R4), `Procedures Documentation`, `Procedure Roles`, `Procedure Times`, `Procedure Timeout Checklist`, `Procedure Vitals`, `Pre-sedation Assessment`; `Surgical Orders`, `Surgical Results`, `Surgery Action Notes`; inpatient: `Surgical Pre-Op Notes` | Exceptionally thorough — 12+ procedure-related datasets |
| Clinical notes / documents | ✅ Covered | `Admin Documents`, `Clinical Documents`, `Encounter Documents`, `Letters`, `Medical Record Documents`, `Office Notes`, `Other CCDAs`; inpatient: `Admission H&P`, `Consult Notes`, `Discharge Summary`, `ED Course/Provider/Triage/Nursing Notes`, `Hospital Notes`, `Nursing Notes`, `Discharge Planning Notes` | Exceptionally thorough — 20+ note/document types |
| Care plans / goals | ✅ Covered | `Care Plan` (FHIR R4), `Care Plan Events` (13 fields), `Goals` (FHIR R4); inpatient: `Nursing Care Plan` | Thorough |
| Orders / referrals | ✅ Covered | `Orders – Labs, Imaging, Consult & Procedures`, `DME Orders`; inpatient: `Admission Order`, `Orders`, `Transfer Orders`; collector: `Referral/Auth` | Thorough |
| Insurance / coverage | ✅ Covered | `Patient Insurance` (with card image attachments) | Covered |
| Claims / billing | ✅ Covered | `Claim Details`, `Claim Transactions`, `Claim Notes`, `Claim Attachments` | Thorough — 4 separate claim-related datasets |
| Payments | ✅ Covered | `Payment History` (includes Patient Refunds), `Payment Plans`, `Pre-payment Plans`, `Patient Outstanding Balance & Patient Unapplied` | Thorough — 4 payment-related datasets |
| Consents / directives | ⚠️ Partial | No dedicated consent dataset. Consent data may be captured within Clinical Documents or digital intake forms, but no explicit export is documented | Product likely stores consent (via athenaCommunicator digital intake); absence from explicit dataset list is a minor gap |
| Patient communications / portal messages | ❌ Not covered | No dataset for secure messages, portal activity, or patient-provider communications | Product stores secure messages (athenaCommunicator); their absence is a gap for data that could inform care decisions |
| Specialty-specific | ✅ Covered | `Cancer Cases`, `Eye Care Specific Measurements`, `OB Episodes`, `OB Episode Summary`, `OB History`, `GYN History`, `Perinatal History`, `PT Episode`, `Screening` | Thorough — 9 specialty-specific datasets |

**Domains not applicable:**
- Telehealth transcripts: The product has telehealth capabilities, but transcripts are more operational than part of the designated record set, unless they are incorporated into clinical notes.

## 6. Documentation Quality

**Strengths:**
- **Dedicated documentation portal** at `docs.athenahealth.com/athenaone-dataexports/` with clear navigation (still live and accessible as of analysis date)
- **Four separate well-organized modules** with consistent structure
- **133 named datasets** — one of the most granular dataset inventories among EHR vendors
- **61 pages of PDF documentation** across four data dictionaries, all downloadable
- **Inpatient clinical PDF (37 pages)** provides HTML template-level field specifications for all 38 hospital datasets — this is unusually detailed
- **Clear file format and folder structure documentation** for all three export use cases (single, multi, bulk)
- **Patient reconciliation guidance** — explains how to match patients across datasets using identifiers
- **Publicly accessible** — no authentication required to view documentation or download PDFs
- **Structured API data** — the underlying Contentful API that powers the documentation portal is publicly accessible, enabling programmatic extraction of the full dataset catalog

**Weaknesses:**
- **Field-level documentation for ambulatory datasets is by external reference** — developers must follow 84+ individual API documentation links to find field definitions. These API docs are a separate system and could change independently
- **No machine-readable schema** — no JSON Schema, OpenAPI spec, or similar for the export format
- **No sample data files** — no example exports are provided
- **PDFs are dated September 22, 2023** — over 2 years old at time of analysis, while certifications are from 2025. No evidence of updates
- **Release Notes page is empty** — still says "set to be released within 2023," suggesting documentation is not actively maintained
- **Inpatient clinical format (HTML) lacks formal schema** — documented at the template level but the HTML structure could vary; harder to import programmatically than NDJSON
- **No relationship/foreign key documentation** — while reconciliation instructions exist, there's no formal entity-relationship model
- **No value set documentation** for ambulatory datasets (though inpatient demographics documents Marital Status values)

**Developer usability assessment:** A developer could build an import for the ambulatory NDJSON data by following the API documentation links, but it would require visiting 84+ separate API doc pages. The inpatient HTML format would require HTML parsing with assumptions about structure. The billing datasets would be importable but field definitions require API doc lookups. Overall, this is functional but labor-intensive documentation.

## 7. Overall Assessment

### Classification

**Comprehensive native export**

This is a genuine, purpose-built EHI export that goes well beyond FHIR or C-CDA repackaging. The 133 datasets across four modules cover clinical, billing, specialty, and hospital-specific data domains using athenahealth's native data model (with 10 FHIR R4 datasets as a small subset). The export addresses both ambulatory and inpatient settings with dedicated documentation for each.

### Key Findings

1. **Genuinely broad coverage**: 133 datasets across 4 modules is one of the largest EHI export dataset inventories among certified EHR vendors. The export covers clinical, billing, specialty, and hospital-specific data — this is not a clinical summary repackaged as (b)(10).

2. **Strong billing coverage**: The collector (billing) modules include 15–16 datasets covering claims, payments, insurance, billing statements, payment plans, referrals, and appointments. Many vendors omit billing entirely from their EHI export.

3. **Exceptional specialty and procedural depth**: 9 specialty-specific datasets (OB/GYN, eye care, cancer, PT, screening) and 12+ procedure-related datasets (roles, times, checklists, vitals, pre-sedation). This level of clinical granularity is uncommon.

4. **Documentation is structurally good but relies on external references**: The 37-page inpatient PDF with HTML template specs is excellent, but ambulatory field-level documentation is entirely by reference to 84+ separate API doc pages. There are no machine-readable schemas, no sample data, and no change history. The PDFs haven't been updated since September 2023.

5. **Patient communications gap**: Secure messages from athenaCommunicator are not in the export. Given that patient-provider messages can inform care decisions, this is a notable gap in an otherwise comprehensive export.

### Summary Stats

```
Classification:  Comprehensive native export
Export format:   NDJSON (ambulatory + inpatient collector), HTML (inpatient clinical)
Model type:      Hybrid — native database model with 10 FHIR R4 datasets
Entities:        133 datasets across 4 modules (114 unique names)
Fields:          183 parsed from PDFs (inpatient clinical + 2 inline specs); ambulatory fields documented by external API reference
Descriptions:    171 of 183 parsed fields have descriptions (93%); ambulatory field descriptions available via API docs (not parsed)
Sample data:     No
Bulk export:     Yes (single, multi, and bulk/all-patient modes)
Domains covered: 16 of 18 applicable domains
```

### Bottom Line

athenahealth's EHI export is one of the more comprehensive implementations among certified EHR vendors, with 133 datasets covering clinical, billing, specialty, and hospital-specific data across both ambulatory and inpatient settings. The single biggest gap is the absence of patient portal messages/secure communications from athenaCommunicator. The biggest documentation weakness is the reliance on 84+ external API doc links for ambulatory field definitions, with no machine-readable schemas or sample data, and PDFs that haven't been updated in over two years.
