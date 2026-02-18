# EHI Export Analysis: athenahealth, Inc.

**Product**: athenaClinicals for Hospitals and Health Systems  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.04.04.2880.Athe.IN.11.1.250321 (Inpatient, certified 2025-03-21); 15.04.04.2880.Athe.AM.12.1.251028 (Ambulatory, certified 2025-10-28)

## 1. Product Context

athenahealth's **athenaOne** platform is a fully integrated, cloud-based EHR + practice management + patient engagement platform. The certified product "athenaClinicals for Hospitals and Health Systems" is the inpatient/hospital EHR component, built from the RazorInsights and webOMR acquisitions (2015), targeting critical access and community hospitals. It integrates with the ambulatory athenaOne platform.

The platform stores:
- **Clinical data**: Encounters, problems, medications, allergies, immunizations, vitals, lab/imaging results, procedures (including surgical), clinical notes (progress, H&P, discharge summaries, consult, ED notes, nursing notes), care plans, goals, devices, screening questionnaires, physical exam findings, HPI, ROS, family/social/surgical history
- **Specialty data**: OB/GYN (episodes, GPAL history, perinatal), eye care measurements, physical therapy episodes, cancer cases, behavioral health
- **Hospital-specific**: Flowsheets (vitals, ADLs, I&O, airways, drains, head-to-toe, lines, measurements), nursing documentation (admission notes, care plans, tasks), MAR, ED documentation (triage, course, provider notes, nursing assessment), discharge planning, surgical pre-op notes, respiratory/therapy tasks, transfer orders
- **Billing/RCM (athenaCollector)**: Claims (details, notes, transactions, attachments), payments, patient insurance, billing statements, payment/pre-payment plans, outstanding balances, referral authorizations, appointments
- **Patient engagement (athenaCommunicator)**: Portal messages, appointment reminders, digital intake forms
- **Documents**: Admin documents, clinical documents, encounter documents, office notes, letters, medical records, prescriptions, DME orders, physician authorizations, surgical orders/results, CCDAs, paper forms

The EHI export documentation explicitly covers **both ambulatory and inpatient** settings, organized into four export types: Ambulatory Clinical, Ambulatory Collector, Inpatient Clinical, and Inpatient Collector.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/api-welcome-exports.json` (15 KB) | Contentful API response for EHI Export overview page. Describes export purpose, use cases, and the four export types. | ⭐ Medium — establishes the export framework |
| `downloads/api-ambulatory-clinical.json` (78 KB) | Contentful API response for Ambulatory Clinical EHI Export. Lists 64 datasets with API spec links; inline specs for Care Plan Events (11 fields) and Eye Care Measurements (5 fields). | ⭐⭐ High — primary dataset catalog |
| `downloads/api-ambulatory-collector.json` (45 KB) | Contentful API response for Ambulatory Collector EHI Export. Lists 15 datasets with API spec links; inline specs for referral auth and claim attachments. | ⭐⭐ High |
| `downloads/api-inpatient-clinical.json` (52 KB) | Contentful API response for Inpatient Clinical EHI Export. Lists 38 datasets (HTML format). | ⭐⭐ High |
| `downloads/api-inpatient-collector.json` (44 KB) | Contentful API response for Inpatient Collector EHI Export. Lists 16 datasets (ambulatory collector + Visits and Charge Details). | ⭐⭐ High |
| `downloads/ambulatory-clinical-ehi-export.pdf` (535 KB, 10 pages) | PDF data dictionary listing 64+ ambulatory clinical datasets with API spec links. Inline field specs for Care Plan Events and Eye Care Measurements. | ⭐⭐ High |
| `downloads/ambulatory-collector-ehi-export.pdf` (495 KB, 7 pages) | PDF data dictionary listing 15 ambulatory billing/demographics datasets. Includes referral auth attachment and claim attachment specs. | ⭐⭐ High |
| `downloads/inpatient-clinical-ehi-export.pdf` (798 KB, 37 pages) | Most detailed artifact. PDF with HTML template specifications for all 38 inpatient clinical datasets. Shows exact HTML structure and field placeholders. | ⭐⭐⭐ Highest |
| `downloads/inpatient-collector-ehi-export.pdf` (497 KB, 7 pages) | PDF data dictionary for 16 inpatient billing/demographics datasets. | ⭐⭐ High |
| `downloads/enrichment/datasets.json` (46 KB) | Structured extraction of 133 datasets across 4 export types, parsed from the API JSON files. | ⭐⭐ High — enables programmatic analysis |
| `downloads/api-navigation.json` (3 KB) | Navigation structure of documentation portal. | ⭐ Low |
| `downloads/api-release-notes.json` (785 B) | Empty release notes page ("set to be released within 2023"). | ⭐ Low — signals documentation maturity concerns |
| `downloads/screenshot-*.png` (6 screenshots) | Screenshots of documentation portal pages. | ⭐ Low — confirms page layouts |

## 3. Export Mechanics

**Format**:
- **Ambulatory (Clinical + Collector)**: Newline Delimited JSON (NDJSON) for structured data, plus supporting files (JPEG, PNG, TIFF, PDF) for documents/attachments
- **Inpatient Clinical**: HTML files (viewable in a browser), including embedded images for imaging results
- **Inpatient Collector**: NDJSON (same as ambulatory collector format)

**Mechanism**: UI-driven export from within athenaOne. Three use cases supported:
- **Single patient export**: Individual patient record
- **Multi-patient export**: Selected set of patients
- **Bulk/all-patient export**: All patients in a practice, provider, medical group, or department

**Bulk export context**: The welcome page states bulk EHI export is enabled "when providers or departments detach from a practice or when practices terminate from athenahealth." Single/multi-patient export is for patient requests, referrals, or authorized auditing.

**File delivery**: ZIP files with hierarchical folder structure. Naming conventions use patient name, DOB, athenahealth IDs. Includes mapping files (JSON) for ID-to-value reconciliation and embedded data dictionaries (PDF).

**Data source**: The ambulatory exports explicitly utilize "athenahealth's standard RESTful FHIR APIs and several proprietary healthcare API endpoints." Each ambulatory dataset links to a specific API endpoint spec on docs.athenahealth.com. The inpatient clinical export uses HTML rendering of chart data rather than API-based extraction.

**Access constraints/fees**: Not documented in the artifacts reviewed.

## 4. Export Content: What's In It

### Data Dictionary Structure

The export documentation provides a **dataset-level catalog** with links to external API specification pages. The key documentation pattern is:

1. **Dataset name** → links to an external API specification page on docs.athenahealth.com
2. For most datasets, the field-level detail is in the **external API spec** (available via the Contentful exploreDocs API)
3. A small number of datasets have **inline field specs** within the PDFs/API JSON files
4. The inpatient clinical datasets use HTML template specs in the PDF data dictionary

From the artifacts (including 55 downloaded API spec pages):
- **133 datasets** listed by the vendor across 4 export types (some shared across ambulatory/inpatient); 138 entity entries in inventory when inline specs creating additional entries are counted
- **117 unique dataset names**
- **94 datasets** have external API specification links (55 proprietary API specs downloaded + 10 FHIR R4)
- **117 entities** have field-level detail (from API specs, inline specs, and PDF parsing)
- **6,809 total fields** documented across all sources
- Of those fields, **97%** have descriptions

The inpatient clinical PDF (37 pages) is the most detailed artifact, providing HTML template specifications that show the exact data structure for each of the 38 inpatient datasets, including field names, types, and value set examples (e.g., Marital Status: "D=Divorced, M=Married, P=Partner, S=Single, U=Unknown, W=Widowed, X=Separated").

### Vendor's Own Content Organization

The vendor organizes the export into four distinct export types:

**Ambulatory Clinical EHI Export (NDJSON) — 64 datasets:**

| Dataset | External Spec | Attachments | Domain |
|---|---|---|---|
| Admin Documents | ✅ | ✅ | Documents |
| Allergies | ✅ | | Clinical |
| Assessment and Plan | ✅ | | Clinical |
| Cancer Cases | ✅ | | Specialty |
| Care Plan | ✅ (FHIR R4) | | Clinical |
| Care Plan Events | Inline (11 fields) | | Clinical |
| Care Team Members | ✅ (FHIR R4) | | Clinical |
| Chief Complaint | ✅ | | Encounter |
| Clinical Documents | ✅ | ✅ | Documents |
| Corrective Lens | ✅ | | Specialty (Eye) |
| Default Clinical Providers – Lab | ✅ | | Reference |
| Default Clinical Providers - Imaging | ✅ | | Reference |
| Default Clinical Providers – Pharmacy | ✅ | | Reference |
| Devices or Medical Equipment | ✅ (FHIR R4) | | Clinical |
| DME Orders | ✅ | ✅ | Orders |
| Encounter Documents | ✅ | ✅ | Documents |
| Encounters | ✅ (FHIR R4) | | Clinical |
| Encounter Phone Call Checklists | ✅ | | Encounter |
| Encounter Summary | ✅ | | Encounter |
| Eye Care Specific Measurements | ✅ + Inline (5 fields) | | Specialty (Eye) |
| Family History | ✅ | | Clinical |
| Goals | ✅ (FHIR R4) | | Clinical |
| GYN History | ✅ | | Specialty (OB/GYN) |
| Health Concerns – Conditions & Problems | ✅ (FHIR R4) | | Clinical |
| History of Present Illness | ✅ | | Encounter |
| Imaging Results | ✅ | ✅ | Results |
| Immunizations | ✅ (FHIR R4) | | Clinical |
| Interpretations | ✅ | | Results |
| Lab Results | ✅ | ✅ | Results |
| Letters | ✅ | ✅ | Documents |
| Letter Action Notes | ✅ | | Documents |
| Medical Record Documents | ✅ | ✅ | Documents |
| Medications | ✅ (FHIR R4) | | Clinical |
| OB Episodes | ✅ | | Specialty (OB/GYN) |
| OB Episode Summary | ✅ | | Specialty (OB/GYN) |
| OB Episode Summary Documents | ✅ | ✅ | Specialty (OB/GYN) |
| OB History | ✅ | | Specialty (OB/GYN) |
| Observations | ✅ (FHIR R4) | | Clinical |
| Office Notes | ✅ | ✅ | Documents |
| Orders – Labs, Imaging, Consult & Procedures | ✅ | ✅ | Orders |
| Other CCDAs | ✅ | ✅ | Documents |
| Past Medical History | ✅ | | Clinical |
| Patient Cases | ✅ (35 fields) | | Patient Communications |
| Perinatal History | ✅ | | Specialty (OB/GYN) |
| Physical Exam | ✅ | | Encounter |
| Physician Authorization | ✅ | ✅ | Documents |
| Prescription Documents | ✅ | ✅ | Documents |
| Procedures | ✅ (FHIR R4) | | Clinical |
| Procedures Documentation | ✅ | | Clinical |
| Procedure Roles | ✅ | | Clinical |
| Procedure Times | ✅ | | Clinical |
| Procedure Timeout Checklist | ✅ | | Clinical |
| Procedure Vitals | ✅ | | Clinical |
| Pre-sedation Assessment | ✅ | | Clinical |
| PT Episode | ✅ | | Specialty (PT) |
| Review of Systems | ✅ | | Encounter |
| Screening | ✅ | | Clinical |
| Social History | ✅ | | Clinical |
| Surgery Action Notes | ✅ | | Procedures |
| Surgical History | ✅ | | Clinical |
| Surgical Orders | ✅ | | Orders |
| Surgical Results | ✅ | ✅ | Procedures |
| Topic of Discussion | ✅ | | Clinical |
| Vitals | ✅ | | Clinical |

**Ambulatory Collector EHI Export (NDJSON) — 15 datasets:**

| Dataset | External Spec | Attachments | Domain |
|---|---|---|---|
| Appointments | ✅ | | Scheduling |
| Appointment Ticklers & Reminders | ✅ | | Patient Communication |
| Claim Attachments | ✅ | ✅ | Billing |
| Claim Details | ✅ | | Billing |
| Claim Notes | ✅ | | Billing |
| Claim Transactions | ✅ | | Billing |
| Demographics | ✅ | | Demographics |
| Patient - Billing Statements & Summaries | ✅ | ✅ | Billing |
| Payment History | ✅ | | Billing |
| Patient Insurance | ✅ | ✅ | Insurance |
| Patient Outstanding Balance & Patient Unapplied | ✅ | | Billing |
| Payment Plans | ✅ | | Billing |
| Pre-payment Plans | ✅ | | Billing |
| Referral/Auth | ✅ | ✅ | Referrals |
| Return to Office | ✅ | | Scheduling |

**Inpatient Clinical EHI Export (HTML) — 38 datasets:**

| Dataset | Fields Parsed (from PDF) | Domain |
|---|---|---|
| Patient Demographics information | 16 fields (name, address, phone, marital status, sex, ethnicity, race, DOB, SSN, language) | Demographics |
| Admin Documents | 1 (image URL template) | Documents |
| Admission H&P | 13 sections (Chief Complaint, Assessment & Plan, Diagnoses, HPI, ROS, Problems, Surgical History, Medications, Allergies, Family History, Social History, Physical Exam, Precautions) | Clinical Notes |
| Admission Order | ~8 fields (date, order details, attribution) | Orders |
| Clinical Documents | 1 (image URL template) | Documents |
| Consult Notes | Structured sections | Clinical Notes |
| Discharge Planning Audit | Structured sections | Discharge |
| Discharge Planning Notes | Structured sections | Discharge |
| Discharge Summary | Structured (visit details, visit summary, labs/imaging, vitals, instructions, allergies, medications) | Clinical Notes |
| ED Course | Structured sections | ED |
| ED Nursing Initial Assessment Notes | Structured sections | ED |
| ED Provider Assessment | Structured sections | ED |
| ED Provider Notes | Structured sections | ED |
| ED Triage Notes | Structured sections | ED |
| Flowsheet ADL–Vitals (9 datasets) | Name/value/datetime measurement pairs | Flowsheets |
| Hospital Notes | Structured sections | Clinical Notes |
| Imaging Results | Document/image references | Results |
| Lab Results | Document/image references | Results |
| Medication Administration Record | ~16 fields (medication, dose, details, actions, administration date/time/action/detail) | Medications |
| Nursing Admission Notes | Structured (visit details, summary, labs, vitals, instructions, allergies, medications) | Nursing |
| Nursing Care Plan | Heading, summary, attribution | Nursing |
| Nursing Notes | Entry-by-entry (entered by, datetime, notes) | Nursing |
| Nursing Tasks | Task date, type, datetime, status, performed by | Tasks |
| Orders | Order type, date, description, entered by/datetime | Orders |
| Paper Forms | Template reference | Documents |
| Patient Discharge Instructions | Structured (visit details, summary, labs, vitals, instructions, allergies, medications) | Discharge |
| Respiratory Tasks | Same structure as Nursing Tasks | Tasks |
| Surgical Pre-Op Notes | Structured (visit details, summary, labs, vitals, allergies, medications) | Procedures |
| Therapy Tasks | Same structure as Nursing Tasks | Tasks |
| Transfer Orders | From/to values, form fields, attribution | Orders |

**Inpatient Collector EHI Export (NDJSON) — 16 datasets:**
Same as Ambulatory Collector (15 datasets) plus **Visits and Charge Details**.

### Key Documentation Pattern

The most important structural observation: **field-level specifications for the ambulatory datasets (64 clinical + 15 collector) reside on external API documentation pages** (docs.athenahealth.com/api/api-ref/...). The PDFs and API JSON files downloaded here provide the dataset catalog and links, but not the full field inventories of each API endpoint. Some datasets reference FHIR R4 resource specs (Care Plan, CareTeam, Condition, Device, Encounter, Goal, Immunization, MedicationRequest, Observation, Procedure), which implies FHIR-formatted output for those datasets.

The inpatient clinical PDF is the exception — it provides complete HTML template specifications showing every field in the output, making it the most detailed artifact for field-level analysis.

The full parsed inventory is in `analysis/entity-inventory-full.json` (138 entity entries, 167 inline-documented fields).

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor organizes exports into two axes: **setting** (Ambulatory vs Inpatient) and **module** (Clinical vs Collector).

**Clinical EHI Export** covers:
- Core clinical data: Allergies, medications, immunizations, vitals, problems/conditions, encounters, procedures, observations, care plans, goals, care team
- Encounter-level detail: Chief complaint, HPI, ROS, physical exam, assessment & plan, encounter summary
- Results: Lab results, imaging results, interpretations
- Notes/Documents: Admin documents, clinical documents, encounter documents, office notes, letters, medical records, CCDAs, hospital notes, consult notes, nursing notes, discharge summaries
- Orders: Lab/imaging/consult/procedure orders, surgical orders, DME orders, admission/transfer orders
- Specialty: OB/GYN (5 datasets), Eye Care (2 datasets), Physical Therapy, Cancer Cases, Screening
- History: Family, social, surgical, past medical, OB/perinatal history
- Hospital-specific (inpatient only): Flowsheets (9 types), ED documentation (5 types), nursing documentation (4 types), MAR, discharge planning, respiratory/therapy tasks
- Procedures: Detailed procedure documentation including roles, times, timeout checklists, pre-sedation assessments, vitals

**Collector EHI Export** covers:
- Demographics (full patient record)
- Insurance (with card images)
- Claims (details, notes, transactions, attachments)
- Payments (history, payment plans, pre-payment plans)
- Billing statements & summaries
- Patient outstanding balances
- Appointments & reminders
- Referral/authorization
- Visits and charge details (inpatient only)

This represents **genuine breadth** — the export covers both clinical and billing/financial data, with specialty-specific datasets and hospital-specific workflows.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | Ambulatory: `Demographics` (API spec); Inpatient: `Patient Demographics information` (16 fields parsed) | Thorough; includes demographics via both Clinical (inpatient) and Collector (ambulatory) |
| Encounters / Visits | ✅ Covered | `Encounters` (FHIR R4), `Appointments`, `Encounter Summary`, `Encounter Phone Call Checklists`; Inpatient: 5 ED datasets, `Hospital Notes`; `Visits and Charge Details` (inpatient collector) | Very comprehensive including ED workflow |
| Problems / Conditions | ✅ Covered | `Health Concerns – Conditions & Problems` (FHIR R4 Condition), `Assessment and Plan` | Covered |
| Medications | ✅ Covered | `Medications` (FHIR R4 MedicationRequest), inpatient `Medication Administration Record` (16 fields) | Strong — includes MAR for inpatient |
| Allergies | ✅ Covered | `Allergies` (API spec) | Covered |
| Immunizations | ✅ Covered | `Immunizations` (FHIR R4) | Covered |
| Vitals | ✅ Covered | `Vitals` (API spec), `Observations` (FHIR R4), `Procedure Vitals`; Inpatient: `Flowsheet Vitals` + 8 other flowsheet types | Very strong — includes procedure vitals and detailed inpatient flowsheets |
| Lab Results | ✅ Covered | `Lab Results` (with attachments), `Interpretations` | Covered |
| Imaging / Diagnostic | ✅ Covered | `Imaging Results` (with attachments) | Covered |
| Procedures | ✅ Covered | `Procedures` (FHIR R4), `Procedures Documentation`, `Procedure Roles`, `Procedure Times`, `Procedure Timeout Checklist`, `Pre-sedation Assessment`, `Surgical Orders`, `Surgical Results`, `Surgery Action Notes`, `Surgical Pre-Op Notes` | Exceptionally thorough — 10 procedure-related datasets |
| Clinical Notes / Documents | ✅ Covered | 19+ document/note datasets including admin, clinical, encounter, office notes, letters, medical records, CCDAs, hospital notes, consult notes, nursing notes, admission H&P, discharge summary, paper forms | Very comprehensive |
| Care Plans / Goals | ✅ Covered | `Care Plan` (FHIR R4), `Care Plan Events` (11 inline fields), `Goals` (FHIR R4), `Topic of Discussion`, `Nursing Care Plan` | Thorough |
| Orders / Referrals | ✅ Covered | `Orders – Labs, Imaging, Consult & Procedures`, `DME Orders`, `Surgical Orders`, `Admission Order`, `Transfer Orders`, `Referral/Auth`, provider defaults | Strong |
| Insurance / Coverage | ✅ Covered | `Patient Insurance` (with card image attachments) | Covered |
| Claims / Billing | ✅ Covered | `Claim Details`, `Claim Notes`, `Claim Transactions`, `Claim Attachments` | Four dedicated claim datasets — genuine billing coverage |
| Payments | ✅ Covered | `Payment History`, `Payment Plans`, `Pre-payment Plans`, `Patient Outstanding Balance & Patient Unapplied`, `Patient - Billing Statements & Summaries` | Five payment-related datasets — thorough |
| Consents / Directives | ⚠️ Partial | No dedicated consent dataset. `Physician Authorization` may cover some authorization aspects | Product stores consent data via FHIR Consent resource (mentioned in product research) but no explicit consent export dataset |
| Patient Communications / Portal Messages | ✅ Covered | `Patient Cases` (35 fields including subject, internalnote, externalnote, patientcaseattachments, phonemessageid, status, priority, assignedto) — per athenahealth, portal messages surface as Patient Case records | Patient Cases is the document type used for clinical phone calls and portal messages routed through the clinical inbox |
| Specialty – OB/GYN | ✅ Covered | `OB Episodes`, `OB Episode Summary`, `OB Episode Summary Documents`, `OB History`, `GYN History`, `Perinatal History` | 6 dedicated OB/GYN datasets — strong |
| Specialty – Eye Care | ✅ Covered | `Eye Care Specific Measurements`, `Corrective Lens` | Covered |
| Specialty – Physical Therapy | ✅ Covered | `PT Episode` | Covered |
| Specialty – Oncology | ✅ Covered | `Cancer Cases` | Basic coverage |
| Screening / Assessments | ✅ Covered | `Screening` (questionnaire-based) | Covered |
| Family History | ✅ Covered | `Family History` | Covered |
| Social History | ✅ Covered | `Social History` | Covered |
| Devices | ✅ Covered | `Devices or Medical Equipment` (FHIR R4) | Covered |
| Flowsheets (Hospital) | ✅ Covered | 9 flowsheet types: ADL, ADLs, Airways, Drains, Head to Toe, Intake & Output, Lines, Measurements, Vitals | Very thorough hospital-specific data |
| ED Documentation | ✅ Covered | `ED Course`, `ED Nursing Initial Assessment`, `ED Provider Assessment`, `ED Provider Notes`, `ED Triage Notes` | 5 dedicated ED datasets — comprehensive |

**Covered domains**: 25 of 26 applicable domains (counting ED and Flowsheets as distinct applicable domains)
**Partially covered**: 1 (Consents)

## 6. Documentation Quality

**Strengths:**
- Clear four-part organization (ambulatory/inpatient × clinical/collector)
- Comprehensive dataset catalog with 133 entries across all export types
- External API specification links for 94 datasets provide detailed field-level documentation; 55 proprietary API specs are available programmatically via the Contentful exploreDocs API with full OpenAPI-style schemas (6,809 fields total)
- Inpatient clinical PDF provides detailed HTML template specs showing exact output structure
- File format and folder structure conventions thoroughly documented with naming conventions and examples for single, multi, and bulk exports
- Inline field specs for specialized datasets (Care Plan Events, Eye Care Measurements) include full input/output parameter definitions with types and descriptions
- Practical reconciliation guidance (patient identifier fields, mapping files, document cross-references)
- Patient Cases dataset includes portal messages (confirmed by athenahealth contact), providing coverage for patient communications

**Weaknesses:**
- **Field-level detail requires API access**: While the 55 proprietary API specs are programmatically accessible via the exploreDocs endpoint, they are not directly linked from the EHI documentation portal — a developer would need to discover the exploreDocs API pattern independently.
- **No consolidated data dictionary**: There is no single artifact listing all fields across all datasets. The documentation is distributed across API spec pages.
- **No sample data provided**: No example NDJSON files or rendered HTML examples are included in the documentation artifacts.
- **No machine-readable schema bundle**: While individual API specs use OpenAPI-style schemas, there is no single bundled OpenAPI document covering all export datasets.
- **Release notes empty**: The release notes page states "This feature is set to be released within 2023" with no actual release notes, suggesting documentation maintenance gaps.
- **Inpatient clinical specs use HTML templates rather than structured field definitions**: While informative, the HTML template format makes it harder to extract a precise field count compared to a tabular data dictionary.
- **Mixed API paradigms**: Some datasets use FHIR R4 resource specs, others use proprietary API specs, creating complexity for data consumers.

**Could a developer build an import?** Yes. The 55 downloaded API spec files provide OpenAPI-style schemas with field names, types, and descriptions for all proprietary API endpoints. Combined with the FHIR R4 specs (standard), the inpatient clinical PDF templates, and the folder structure documentation, a developer has sufficient information to parse all export formats. The Patient Cases dataset (used for portal messages) has 94 fields fully documented.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

This export demonstrably covers the breadth of data domains that athenaOne stores. Key evidence:
- **Clinical + Billing**: The export explicitly separates clinical data (athenaClinicals) from billing/demographics data (athenaCollector), covering both with dedicated datasets. The Collector EHI Export includes 4 claim datasets, 5 payment datasets, insurance, appointments, and referral authorizations — this is not a clinical-only export rebranded as (b)(10).
- **Specialty data**: Dedicated datasets for OB/GYN (6 datasets), Eye Care (2), Physical Therapy (1), Oncology (1), and screening questionnaires.
- **Hospital-specific data**: 9 flowsheet types, 5 ED documentation types, 4 nursing documentation types, MAR, discharge planning — these are clearly purpose-built for the inpatient setting.
- **Procedural depth**: 10 procedure-related datasets covering documentation, roles, times, checklists, pre-sedation assessments, vitals, and surgical workflow.
- **64 ambulatory clinical datasets** is a large number covering granular encounter-level detail (HPI, ROS, physical exam, assessment & plan, chief complaint) beyond summary-level clinical data.
- Minor gap: No explicit consent/advance directive dataset.

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly a purpose-built export, not a repackaged (g)(10) or C-CDA export. Evidence:
- The vendor built a dedicated documentation portal at docs.athenahealth.com/athenaone-dataexports/ specifically for EHI export.
- The export includes **proprietary API endpoints** alongside FHIR R4 resources — datasets like `Care Plan Events`, `Eye Care Measurements`, `Encounter Phone Call Checklists`, `Procedure Timeout Checklist`, and all Collector datasets use athenahealth-specific APIs, not standard FHIR.
- The export covers **billing data** (claims, payments, billing statements) that is not part of any FHIR (g)(10) or C-CDA export.
- The inpatient clinical export uses a completely different format (HTML) from any standard clinical exchange format.
- The export explicitly states it "Utilizes athenahealth's standard RESTful FHIR APIs and several proprietary healthcare API endpoints" — acknowledging it goes beyond standard FHIR.
- The four-export-type structure (ambulatory clinical, ambulatory collector, inpatient clinical, inpatient collector) reflects the product's internal architecture rather than a standards-based projection.

### Key Findings

1. **Genuinely comprehensive coverage**: 133 datasets across 4 export types covering clinical, billing, specialty, and hospital-specific data. This is one of the broader EHI exports reviewed, with dedicated datasets for procedural workflow (10 datasets), OB/GYN (6), ED (5), nursing (4), and flowsheets (9).

2. **Billing coverage is real**: The Collector EHI Export includes Claim Details, Claim Notes, Claim Transactions, Claim Attachments, Payment History, Payment Plans, Pre-payment Plans, Billing Statements, Outstanding Balances, and Insurance — 10+ billing/financial datasets covering the athenaCollector module's scope.

3. **Documentation is programmatically accessible**: While the EHI documentation portal presents dataset names with links to external API spec pages, those specs are available programmatically via the Contentful exploreDocs API endpoint. The 55 proprietary API spec files contain OpenAPI-style schemas with 6,809 fields total, making the documentation functionally complete for import development.

4. **Patient portal messages covered via Patient Cases**: athenahealth confirms that portal messages surface as Patient Cases records — a document type with 94 fields covering subject, notes, attachments, status, priority, and routing metadata. This means the export covers patient communications despite not having a separately named "portal messages" dataset.

4. **Format divergence between settings**: Ambulatory clinical data exports as NDJSON (structured, machine-readable), while inpatient clinical data exports as HTML (human-readable but harder to process programmatically). This suggests the inpatient export may have been built separately from the ambulatory one, consistent with the product's acquisition-based history.

5. **Minor gaps in patient engagement data**: The export lacks explicit datasets for advance directives/consents, despite this being a product capability.

### Summary Stats

```
Coverage:        Comprehensive
Approach:        Purpose-built EHI export
Export format:   NDJSON (ambulatory + inpatient collector), HTML (inpatient clinical)
Entities:        133 vendor-listed datasets (117 unique names across ambulatory/inpatient)
Fields:          6,809 documented across API specs, inline specs, and PDF parsing (97% with descriptions)
Descriptions:    97% of documented fields have descriptions
Sample data:     No
Bulk export:     Yes (single, multi, and bulk/all-patient)
Domains covered: 25 of 26 applicable domains
```

### Bottom Line

athenahealth has built a genuine, purpose-built EHI export that covers clinical, billing, specialty, and hospital-specific data across 133 datasets in both ambulatory and inpatient settings. This is a credible (b)(10) implementation that goes well beyond USCDI/C-CDA repackaging. The API spec pages (accessible via Contentful's exploreDocs endpoint) provide OpenAPI-style schemas with 6,809 fields, making the documentation functionally complete. Patient portal messages are covered via the Patient Cases document type (confirmed by athenahealth). The only notable gap is consent/advance directive data.
