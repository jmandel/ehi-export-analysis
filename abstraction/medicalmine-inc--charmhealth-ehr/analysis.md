# EHI Export Analysis: MedicalMine Inc. (CharmHealth)

**Product**: CharmHealth EHR v1.2  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.04.04.1948.ChAR.12.00.1.181115 (CHPL #9741)

## 1. Product Context

CharmHealth EHR is a cloud-based, all-in-one healthcare platform from MedicalMine Inc., targeting ambulatory practices — particularly independent clinics, small-to-medium practices, and integrative/functional medicine providers. The platform is hosted on Zoho's infrastructure and has approximately 5,000 licensed physician users.

The product encompasses far more than a clinical EHR:

- **Clinical EHR**: SOAP notes with customizable templates, clinical decision support, flowsheets, image annotation, AI Scribe (ambient clinical documentation)
- **E-Prescribing**: Via Surescripts, including EPCS and drug-herb interaction checking (notable for integrative medicine)
- **Lab Integration**: Pre-built interfaces with LabCorp, Quest, and other labs via HL7
- **Practice Management**: Multi-facility scheduling, patient self-scheduling, iPad kiosk check-in, task management
- **Medical Billing**: SuperBills, CMS 1500, electronic claims submission, ERA processing, real-time eligibility verification
- **Revenue Cycle Management (RCM)**: Claims scrubbing, denial management, A/R follow-up, provider credentialing
- **Patient Portal**: Secure messaging, appointment requests, refill requests, intake forms, PHR with wellness tracking
- **Telehealth**: Integrated audio/video with recording capability, multi-user sessions
- **Secure Messaging (CharmConnect)**: End-to-end encrypted HIPAA-compliant messaging between providers and patients
- **Inventory Management**: Medication/supplement tracking with stock alerts and expiration monitoring
- **Document Management**: Secure storage, e-fax, document scanning
- **App Marketplace (CharmHealthHub)**: Third-party integrations

This breadth is critical for assessment: a (b)(10) export should cover clinical data, billing/claims, patient communications, and specialty-specific data (e.g., integrative medicine content). The certified EHR module (v1.2) is the clinical component, but the broader product stores data across all these domains.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `electronic-health-information-export.html` (10 KB) | Main EHI export landing page. Lists 3 export mechanisms: FHIR R4 API, HL7 CCDA, CSV billing export. Links to all documentation. | **High** — defines the vendor's export scope |
| `fhir-api-documentation.html` (421 KB) | Single-page FHIR R4 API docs. 24 resources, 68 operations, OAuth/SMART auth, Bulk Export API, CCDA API. | **High** — primary technical docs for clinical data |
| `enrichment/fhir-api-extracted.json` (208 KB) | Structured JSON extraction of FHIR API docs (24 resources, 68 operations, all parameters, sample responses). | **High** — machine-readable parse of FHIR docs |
| `billing-reports.html` (51 KB) | Resource center page for billing reports. 7 report categories, 24 individual report types, CSV export documented. | **Medium** — documents billing export scope but no schema |
| `claims.html` (107 KB) | Claims management documentation. 22 workflow sections, 5 claims report types. | **Medium** — explains claims processes, CSV export for reports |
| `analytics.html` (29 KB) | Analytics/reporting docs. 20 report types including Patient Insurance Report. | **Low** — mostly describes reporting features, not export schema |
| `create-encounter.html` (23 KB) | Encounter creation docs with Export section showing PDF/CCDA/Surveillance export from UI. | **Low** — confirms UI export mechanism |
| `export-encounters-as-hl7-messages.html` (85 KB) | HL7 billing message export (DFT-P03, ADT-A03). 2 segment tables, 258 field definitions. | **Medium** — detailed field-level schema for HL7 billing export |
| `export-encounter.jpg` (117 KB) | Screenshot of bulk export menu in encounter list. | **Low** — confirms UI mechanism |
| `export-encounter1.jpg` (115 KB) | Screenshot of per-encounter export dropdown. | **Low** — confirms UI mechanism |
| `screenshot-ehi-export-page.png` (333 KB) | Full-page screenshot of EHI export page. | **Low** — visual confirmation |
| `screenshot-fhir-api-top.png` (198 KB) | Screenshot of FHIR API docs header. | **Low** — visual confirmation |
| `screenshot-bulk-export.png` (200 KB) | Screenshot of Bulk Export section. | **Low** — visual confirmation |

## 3. Export Mechanics

CharmHealth documents a **multi-mechanism export approach** with three distinct channels, explicitly referenced to the 170.315(b)(10) criterion on the EHI export landing page (`electronic-health-information-export.html`):

### Clinical Data: FHIR R4 API
- **Format**: FHIR R4.0.1 JSON (individual) / NDJSON (bulk)
- **Mechanism**: REST API at `https://ehr2.charmtracker.com/api/ehr/v2/fhir`
- **Single-patient**: Per-resource GET/search endpoints with patient parameter
- **Bulk**: `GET /Group/{group_id}/$export` → async NDJSON download (standard FHIR Bulk Data)
- **Authentication**: SMART on FHIR (OAuth 2.0) supporting patient-facing apps, provider-facing apps, backend services (JWT), and API key auth
- **Access constraints**: Requires API registration; no fees documented

### Clinical Summary: HL7 CCDA
- **Format**: HL7 CCDA v2.1 XML
- **Mechanism**: API (`GET /patients/{patient_id}/ccda`) and EHR UI (per-encounter and bulk)
- **Single-patient**: Yes (API with optional date range filtering)
- **Bulk**: Yes (via UI "Export Encounters as HL7 CCDA")

### Billing Data: CSV Reports
- **Format**: CSV
- **Mechanism**: Manual export from EHR UI (report-by-report)
- **Single-patient**: Some reports support patient filtering
- **Bulk**: Yes (practice-wide reports)
- **Access constraints**: Requires EHR login; manual process per report type

### HL7 Billing Messages
- **Format**: HL7 v2 (DFT-P03, ADT-A03)
- **Mechanism**: EHR UI export
- **Purpose**: Encounter data export for external billing systems

There is **no unified "Export All EHI" button**. A complete export requires running the FHIR Bulk Export API for clinical data plus manually generating multiple billing/claims CSV reports from the UI. The billing CSV export is not programmatic — it requires a user to navigate to each report type and click "Export as CSV."

## 4. Export Content: What's In It

### FHIR R4 Resources (Clinical Data)

The FHIR API documents **24 FHIR resource types** with **68 API operations** (list/get/search). 19 of 24 resources reference US Core STU3.1.1 profiles. From sample responses in the documentation, 667 unique field paths are demonstrated across all resources.

There is **no formal data dictionary** — field definitions rely entirely on standard FHIR resource specifications and US Core profiles. No CharmHealth-specific extensions, custom value sets, or vendor-specific field mappings are documented. The documentation consists of API endpoints with search parameters and sample JSON responses, not a field-by-field schema.

| FHIR Resource | Sample Fields | Search Params | US Core Profile | Category |
|---|---|---|---|---|
| Immunization | 58 | 11 | ✅ | Clinical |
| Encounter | 47 | 19 | ✅ | Clinical |
| DocumentReference | 45 | 41 | ✅ | Clinical |
| Patient | 44 | 19 | ✅ | Demographics |
| Observation | 39 | 15 | ✅ | Clinical |
| DiagnosticReport | 38 | 15 | ✅ | Clinical |
| Organization | 37 | 7 | ✅ | Administrative |
| AllergyIntolerance | 34 | 9 | ✅ | Clinical |
| MedicationAdministration | 34 | 11 | ❌ | Clinical |
| Condition | 32 | 15 | ✅ | Clinical |
| Device | 28 | 9 | ✅ | Clinical |
| Appointment | 26 | 13 | ❌ | Administrative |
| FamilyMemberHistory | 24 | 9 | ❌ | Clinical |
| RelatedPerson | 24 | 13 | ❌ | Demographics |
| Practitioner | 22 | 7 | ✅ | Administrative |
| MedicationRequest | 21 | 17 | ✅ | Clinical |
| Goal | 20 | 11 | ✅ | Clinical |
| Procedure | 20 | 13 | ✅ | Clinical |
| Location | 18 | 13 | ✅ | Administrative |
| QuestionnaireResponse | 16 | 11 | ❌ | Clinical |
| CarePlan | 15 | 13 | ✅ | Clinical |
| CareTeam | 14 | 9 | ✅ | Clinical |
| Medication | 11 | 1 | ✅ | Clinical |
| Provenance | 0 | 1 | ✅ | Administrative |

**Note**: "Sample Fields" are unique field paths extracted from sample JSON responses in the documentation. This is the closest approximation to a field count since no formal data dictionary exists. Actual resource instances may contain more or fewer fields depending on data completeness.

### Billing CSV Reports

The billing documentation describes **24 distinct report types** across 7 categories, plus **5 claims report types**. These reports are exportable as CSV from the EHR UI.

**No CSV schema documentation exists.** The billing report pages are user-guide-style help articles describing how to navigate to each report and click "Export as CSV." Column names, data types, and value sets are not documented. A developer would need sample CSV files to reverse-engineer the schema.

| Report Category | Reports | Source |
|---|---|---|
| Invoices & Receipts Reports | 9 reports (Receipts List, Procedures List, Product Sales List, Procedures by Patient, Product Sales By Patient, Receipts by Patient, Receipts By Payment Method, Receipts and Refund Report, Refunds Report) | `billing-reports.html` |
| Provider Collection Reports | 1 report (Payment Collection by Provider) | `billing-reports.html` |
| Products & Tax Reports | 3 reports (Product Sales List, Tax Report (Invoice), Tax Report (Collection)) | `billing-reports.html` |
| Account Receivable Reports | 2 reports (A/R Aging by Patient, A/R Aging by Provider) | `billing-reports.html` |
| Payment Gateway Reports | 3 reports (Patient Card on File, Recurring Profile, Recurring Profile Line Items) | `billing-reports.html` |
| Encounter Summary Reports | 1 report (Encounter Summary Report) | `billing-reports.html` |
| Other Reports | 5 reports (Write-off/Adjustment, Patient Invoice Sent, EOBs List, ERAs List, Electronic Claim Submission) | `billing-reports.html` |
| Claims Reports | 5 reports (Claims List, Claims Aging by Payer, Claims by Patient, Claims by Provider, Claim Procedures List) | `claims.html` |

### HL7 Billing Message Export

The HL7 billing message export provides the most detailed field-level documentation of any export component. Two message types are documented with segment-by-segment field definitions:

- **DFT-P03** (Detailed Financial Transaction): 136 field definitions across 12 segments (MSH, EVN, PID, PV1, PV2, FT1, DG1, GT1, IN1, IN2, OBX, ACC)
- **ADT-A03** (Discharge): 122 field definitions across 11 segments (MSH, EVN, PID, PV1, PV2, DG1, PR1, GT1, IN1, IN2, OBX)

Each field definition includes segment name, field number, description, and comments (e.g., mapping notes). This is the only component with explicit field-level schema documentation.

### Analytics Reports

20 report types are documented in `analytics.html`, including Patient Insurance Report, which is referenced from the EHI export page. These reports cover practice statistics, appointment reports, patient demographics, vaccinations, diagnoses, prescriptions, lab tests, and quality measures. Export capability (CSV) is mentioned for some but not systematically documented.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

CharmHealth organizes its EHI export into two explicit categories:

**Clinical Data (FHIR R4)**: 24 FHIR resources covering standard clinical content — demographics, conditions, medications, allergies, immunizations, labs/vitals, procedures, care plans, goals, encounters, documents, and appointments. This is a standard US Core / (g)(10) API with a few extras (Appointment, FamilyMemberHistory, MedicationAdministration, QuestionnaireResponse, RelatedPerson). The resources follow standard FHIR definitions with no vendor-specific extensions.

**Billing Data (CSV)**: 29 report types across invoices/receipts, claims, insurance, A/R, provider collections, product sales/tax, and encounter summaries. This acknowledges that billing data is separate from clinical FHIR data and needs its own export path. However, this is report-based CSV output, not a structured data export with schema documentation.

The FHIR clinical data is relatively deep for what it covers — US Core plus meaningful additions. The billing CSV reports are broad (29 report types) but completely undocumented in terms of schema.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | FHIR `Patient` (44 fields), `RelatedPerson` (24 fields) | Standard US Core demographic data |
| Encounters / visits | ✅ Covered | FHIR `Encounter` (47 fields), `Appointment` (26 fields) | Good — includes both encounters and appointments |
| Problems / conditions | ✅ Covered | FHIR `Condition` (32 fields) | Standard US Core |
| Medications / prescriptions | ✅ Covered | FHIR `Medication` (11 fields), `MedicationRequest` (21 fields), `MedicationAdministration` (34 fields) | Good — includes administration records beyond just orders |
| Allergies | ✅ Covered | FHIR `AllergyIntolerance` (34 fields) | Standard; unclear if drug-herb interactions (an integrative medicine feature) are captured |
| Immunizations | ✅ Covered | FHIR `Immunization` (58 fields) | Richest resource by field count |
| Vitals | ✅ Covered | FHIR `Observation` (39 fields) | Vitals + lab results share Observation |
| Lab results | ✅ Covered | FHIR `Observation` (39 fields), `DiagnosticReport` (38 fields) | Standard |
| Imaging / diagnostic reports | ⚠️ Partial | FHIR `DiagnosticReport`, `DocumentReference` | Reports covered; unclear if actual images (e.g., annotated clinical images) are included in DocumentReference |
| Procedures | ✅ Covered | FHIR `Procedure` (20 fields) | Standard US Core |
| Clinical notes / documents | ⚠️ Partial | FHIR `DocumentReference` (45 fields), HL7 CCDA | DocumentReference should capture clinical notes; AI Scribe transcriptions unclear |
| Care plans / goals | ✅ Covered | FHIR `CarePlan` (15 fields), `Goal` (20 fields) | Standard US Core |
| Orders / referrals | ⚠️ Partial | FHIR `MedicationRequest` covers med orders; no dedicated ServiceRequest or ReferralRequest resource | Product has referral management; no explicit export path |
| Insurance / coverage | ⚠️ Partial | CSV "Patient Insurance Report" (from analytics), no FHIR Coverage resource | Insurance data available via CSV report but no structured schema |
| Claims / billing | ⚠️ Partial | CSV reports: 5 claims reports + 24 billing reports + HL7 DFT-P03/ADT-A03 messages | Broad report coverage but CSV schema undocumented; HL7 messages have field-level docs |
| Payments | ⚠️ Partial | CSV billing reports (Receipts, Payment Collection, ERA) | Available via CSV but no schema documentation |
| Consents / directives | ❌ Not covered | No FHIR Consent resource; no documented consent export | Product generates telehealth consent documents; gap |
| Patient communications / portal messages | ❌ Not covered | No export mechanism for portal messages, secure messaging (CharmConnect) | Product stores patient-provider messages and portal interactions; significant gap |
| Specialty-specific (integrative/functional medicine) | ❌ Not covered | No evidence of export for drug-herb interactions, supplement protocols, custom template content | Product's primary differentiator is integrative medicine support; no export path for this specialty data |

### Key Coverage Gaps

1. **Patient communications**: CharmConnect (secure messaging) and patient portal messages are a significant data store with no documented export path. These messages are part of the patient's designated record set.

2. **Specialty/integrative medicine data**: CharmHealth's competitive advantage is integrative/functional medicine features — drug-herb interaction databases, supplement protocols, custom clinical templates for specialty workflows. None of this appears in the FHIR export (no vendor extensions) or in any other export mechanism.

3. **Telehealth records**: Session metadata, consent documents, and possibly recorded sessions have no documented export path.

4. **Consent documents**: No FHIR Consent resource; telehealth consent documents are not covered.

5. **Custom form/template content**: QuestionnaireResponse covers intake forms, but custom SOAP note template content and specialty-specific clinical assessments likely lose fidelity when mapped to generic FHIR resources.

## 6. Documentation Quality

### Strengths
- **FHIR API documentation is professional and thorough** for what it covers: 24 resources with clear API URLs, parameter tables, request/response examples, OAuth/SMART authentication flows for multiple client types, Bulk Export API, and CCDA API. A developer with FHIR experience could build an integration.
- **The EHI export landing page clearly links to all relevant documentation**, organizing the export by clinical (FHIR) and billing (CSV) categories with explicit (b)(10) citation.
- **HL7 billing message documentation** includes field-level segment descriptions (258 fields across 2 tables) — the only component with true schema documentation.
- **Screenshots confirm the UI export mechanisms** exist and show the actual export buttons/menus.

### Weaknesses
- **No formal data dictionary for FHIR resources**: Field definitions rely entirely on standard FHIR/US Core profiles. No documentation of which CharmHealth-internal data maps to which FHIR fields, what data is lost in the FHIR projection, or what vendor-specific constraints apply.
- **No CSV schema documentation**: The 29 billing/claims report types are described only in user-guide prose ("click Export as CSV"). No column names, data types, value sets, or relationships are documented. A developer cannot build a billing data import from these docs.
- **No sample export data**: No example NDJSON from bulk export, no example CSV from billing reports, no example CCDA output. A developer has no way to verify expected output format.
- **No documentation of completeness**: No mapping from CharmHealth's internal data model to the export. It is impossible to determine from these docs what data is stored but not exported.
- **No relationships/foreign keys documented**: How billing CSV data links to FHIR clinical data is not explained.

### Developer Usability Assessment
A developer could implement the FHIR API integration (relying on standard FHIR knowledge). They could **not** implement a billing data import without obtaining sample CSV files and reverse-engineering the schema. The documentation is insufficient to build a complete EHI import pipeline.

## 7. Overall Assessment

### Classification

**Standard-based projection** with a billing supplement.

The core clinical export is a standard FHIR R4 / US Core API — the same 24 resources that serve the (g)(10) Standardized API criterion. The FHIR resources contain no vendor-specific extensions, no custom data types, and no evidence of data beyond what US Core profiles define. This is essentially the (g)(10) API relabeled for (b)(10) purposes.

The billing CSV reports supplement the FHIR data with financial information, which is better than many vendors. However, the billing export is a collection of ad-hoc report CSVs with no schema documentation, not a structured data export.

The product stores significantly more data than what the FHIR API + CSV reports cover — patient portal messages, secure messaging, telehealth sessions, integrative medicine specialty data, inventory, custom templates, and AI Scribe content are all absent from the documented export.

### Key Findings

1. **The FHIR clinical export is the (g)(10) API repackaged as (b)(10).** All 24 resources are standard FHIR R4 / US Core with no vendor extensions. The Bulk Export API exports only these 24 resource types. This is not a native data model export — it's a standard projection that likely omits vendor-specific clinical data.

2. **Billing data export is acknowledged but undocumented at the schema level.** CharmHealth deserves credit for explicitly including billing CSV reports in their (b)(10) documentation (many vendors don't). However, 29 report types with no column definitions, no data types, and no sample data does not constitute usable documentation.

3. **Major data domains stored by the product have no export path.** Patient portal messages, CharmConnect secure messaging, telehealth session data, and integrative/functional medicine specialty content — key differentiators of this product — are absent from the export documentation.

4. **The HL7 billing message export (DFT-P03/ADT-A03) is the most schema-rich component**, with 258 field definitions across 2 tables, but this is for interoperability with external billing systems, not a general-purpose EHI export.

5. **No sample data or formal data dictionary exists.** The FHIR docs include sample API responses (which demonstrate field coverage) but no downloadable sample export files. Billing CSV exports have zero schema documentation.

### Summary Stats

```
Classification:  Standard-based projection (FHIR + CSV billing supplement)
Export format:   FHIR R4 JSON/NDJSON + HL7 CCDA v2.1 + CSV + HL7 v2
Model type:      Standard projection (US Core FHIR, not native database)
Entities:        24 FHIR resources + 29 billing CSV report types
Fields:          667 (from FHIR sample responses) + undocumented (CSV)
Descriptions:    0% vendor-specific (relies on standard FHIR definitions)
Sample data:     No (sample API responses in docs, but no downloadable export samples)
Bulk export:     Yes (FHIR Bulk Data API for clinical; manual CSV for billing)
Domains covered: 10 of 16 applicable domains (✅ or ⚠️)
```

### Bottom Line

CharmHealth's EHI export is a FHIR R4 API (essentially the same as their (g)(10) certified API) supplemented with billing CSV reports. The clinical FHIR export covers standard data categories well but omits vendor-specific data — particularly the integrative/functional medicine content that is CharmHealth's primary market differentiator. Patient communications (portal messages, CharmConnect) and telehealth data have no documented export path. The billing CSV reports acknowledge financial data but lack any schema documentation, making them unusable without sample files. The single biggest gap is the absence of specialty clinical data and patient communications that CharmHealth stores but does not export.
