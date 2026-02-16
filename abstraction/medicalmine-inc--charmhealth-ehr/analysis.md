# EHI Export Analysis: MedicalMine Inc. (CharmHealth)

**Product**: CharmHealth EHR  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.04.04.1948.ChAR.12.00.1.181115 (CHPL #9741)

## 1. Product Context

CharmHealth EHR is a cloud-based, all-in-one healthcare platform from MedicalMine Inc., targeting independent and small-to-medium ambulatory practices — particularly in integrative/functional medicine. Approximately 5,000 licensed physicians use the system.

The product is broad: beyond core EHR charting (SOAP notes, customizable templates, flowsheets, clinical decision support), it includes:

- **E-Prescribing** (EPCS, Surescripts, drug-herb interactions)
- **Lab integration** (LabCorp, Quest, HL7 interfaces)
- **Practice management** (scheduling, multi-facility, task management)
- **Medical billing & RCM** (SuperBills, CMS 1500, claims submission, ERA/EOB processing, denial management, A/R aging, provider credentialing)
- **Patient portal** (messaging, appointment requests, refill requests, intake forms, PHR)
- **Telehealth** (integrated audio/video consultations)
- **Secure messaging** (CharmConnect, end-to-end encrypted)
- **Inventory management** (medications, supplements)
- **Document management** (scanning, faxing, storage)
- **AI Scribe** (ambient transcription, auto-generated notes)

This breadth means a genuine (b)(10) export should cover clinical data, billing/claims records, patient communications, custom forms/questionnaires, prescriptions, lab results, documents, and more. The billing/RCM module alone stores charges, claims, ERA/EOB data, payments, denial records, and A/R data — all EHI.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `electronic-health-information-export.html` (10 KB) | Main EHI export landing page. Lists 3 export mechanisms: FHIR API (24 resources), C-CDA, and CSV billing reports. | **High** — establishes the vendor's (b)(10) strategy |
| `fhir-api-documentation.html` (421 KB) | Single-page FHIR R4 API docs covering 24 resources, 68 operations, OAuth, Bulk Export, C-CDA API. | **High** — primary technical documentation |
| `enrichment/fhir-api-extracted.json` (208 KB) | Structured JSON extraction of FHIR API docs (24 resources, 68 operations, parameters, examples). | **High** — machine-readable parse of FHIR docs |
| `billing-reports.html` (51 KB) | Resource center page documenting 24+ billing reports (invoices, receipts, A/R aging, EOBs, etc.) exportable as CSV. | **Medium** — documents billing report types but no field-level dictionary |
| `claims.html` (107 KB) | Claims management documentation (claim generation, submission, ERA processing, denial management, 5+ report types as CSV). | **Medium** — documents claims workflow and report types, no field dictionary |
| `analytics.html` (29 KB) | Analytics page documenting Patient Insurance Report (CSV export). | **Low** — just confirms insurance report exists |
| `create-encounter.html` (23 KB) | Encounter creation docs including C-CDA/PDF export from UI. | **Low** — confirms per-encounter export exists |
| `export-encounter.jpg`, `export-encounter1.jpg` | Screenshots of encounter export UI (PDF, C-CDA, Surveillance Report options). | **Low** — visual confirmation of UI export options |
| `screenshot-ehi-export-page.png`, `screenshot-fhir-api-top.png`, `screenshot-bulk-export.png` | Browser screenshots of documentation pages. | **Low** — visual reference only |

## 3. Export Mechanics

CharmHealth describes three export mechanisms on its EHI documentation page:

### Clinical Data Export (FHIR API)
- **Format**: FHIR R4 JSON (single patient) or NDJSON (bulk)
- **Mechanism**: REST API with OAuth 2.0 / SMART on FHIR authentication
- **Endpoint**: `GET /api/ehr/v2/fhir/{ResourceType}`
- **Single patient**: Per-resource API calls with `patient` search parameter
- **Bulk export**: `GET /Group/{group_id}/$export` → NDJSON files; status polling via `/$export-poll-status`
- **C-CDA**: `GET /patients/{patient_id}/ccda` with optional date range; also available via per-encounter UI export

### Billing Data Export (CSV)
- **Format**: CSV
- **Mechanism**: UI-based report generation and download (no API)
- **Scope**: 24+ billing/claims report types, each independently exported from the Reports section
- **Access**: Requires practice user login; navigate to Billing → Reports or Analytics

### Access Constraints
- FHIR API requires OAuth credentials (client ID/secret via SMART registration)
- Billing CSV exports require interactive UI access — no programmatic/API export for billing data
- No mention of fees for export

## 4. Export Content: What's In It

### FHIR API (Clinical Data)

The FHIR API exposes **24 resource types** with **68 operations** (list, get, search for most resources). **19 of 24** resources reference US Core profiles; 5 use base FHIR R4 definitions (Appointment, FamilyMemberHistory, MedicationAdministration, QuestionnaireResponse, RelatedPerson).

All 24 resources have response examples in the documentation. From parsing these examples, approximately **650 fields** are represented across all resources, though these are standard FHIR elements — there are **no vendor-specific extensions** documented beyond the standard profiles.

The resources map cleanly to USCDI data classes, covering all 21 USCDI resource types. Three resources go beyond the strict USCDI minimum:
- **Appointment** (scheduling data)
- **MedicationAdministration** (MAR records)
- **QuestionnaireResponse** (custom forms/intake)

The FHIR API has **302 total search parameters** across all operations. Documentation quality is good for API usage (endpoints, parameters, examples), but there is **no product-specific data dictionary** — no mapping of which CharmHealth-internal fields map to which FHIR elements, no vendor extensions, no field descriptions beyond the FHIR standard.

### Billing/Claims CSV Reports

The billing documentation describes **29 distinct report types** exportable as CSV:

**Billing Reports (24 types)**:
- Invoices & Receipts: Receipts List, Procedures List, Product Sales List, Procedures by Patient, Product Sales By Patient, Receipts by Patient, Receipts By Payment Method, Receipts and Refund Report, Refunds Report
- Provider Collection: Payment Collection by Provider
- Products & Tax: Product Sales List, Tax Report (Invoice-based), Tax Report (Collection-based)
- A/R: A/R Aging Report by Patient, A/R Aging Report by Provider
- Payment Gateway: Patient Card on File Report, Recurring Profile Report, Recurring Profile Invoice Line Item Report
- Encounter Summary: Encounter Summary Report
- Other: Write-off/Adjustment Report, Patient Invoice Sent Report, EOBs List, ERAs List, Electronic Claim Submission Report

**Claims Reports (5 types)**: Claims List, Claims Aging Report by Payer, Claims by Patient, Claims by Provider, Claim Procedures List

**Analytics Reports (1 type)**: Patient Insurance Report

The billing/claims CSV documentation describes **how to run and export each report** (grouping options, filters, date ranges), but provides **no field-level documentation** — no column names, no data types, no descriptions of what each CSV contains. A developer cannot determine the CSV schema without running the actual reports.

### Vendor's Own Content Organization

| Entity/Resource | Fields (from examples) | Profile | Source | Category |
|---|---|---|---|---|
| Patient | 48 | US Core | FHIR API | Demographics |
| RelatedPerson | 20 | FHIR R4 | FHIR API | Demographics |
| Encounter | 47 | US Core | FHIR API | Encounters |
| Condition | 32 | US Core | FHIR API | Problems/Diagnoses |
| AllergyIntolerance | 34 | US Core | FHIR API | Allergies |
| Medication | 10 | US Core | FHIR API | Medications |
| MedicationRequest | 32 | US Core | FHIR API | Medications |
| MedicationAdministration | 24 | FHIR R4 | FHIR API | Medications |
| Immunization | 58 | US Core | FHIR API | Immunizations |
| Observation | 39 | US Core | FHIR API | Observations/Vitals/Labs |
| DiagnosticReport | 30 | US Core | FHIR API | Diagnostics |
| Procedure | 17 | US Core | FHIR API | Procedures |
| CarePlan | 15 | US Core | FHIR API | Care Plans |
| CareTeam | 14 | US Core | FHIR API | Care Team |
| Goal | 20 | US Core | FHIR API | Goals |
| DocumentReference | 45 | US Core | FHIR API | Documents |
| Device | 28 | US Core | FHIR API | Devices |
| FamilyMemberHistory | 24 | FHIR R4 | FHIR API | Family History |
| Appointment | 26 | FHIR R4 | FHIR API | Scheduling |
| QuestionnaireResponse | 16 | FHIR R4 | FHIR API | Questionnaires/Forms |
| Organization | 20 | US Core | FHIR API | Provider |
| Practitioner | 18 | US Core | FHIR API | Provider |
| Location | 33 | US Core | FHIR API | Provider |
| Provenance | 0* | US Core | FHIR API | Provenance |
| *29 billing/claims/insurance CSV report types* | *undocumented* | N/A | CSV UI | Billing/Claims |

\* Provenance example parsed but extracted 0 unique top-level fields due to array-heavy structure.

Full inventory saved to `analysis/entity-inventory-full.json` (54 entities total).

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

CharmHealth organizes its (b)(10) export into two tiers:

1. **Clinical Data Export** via FHIR API: 24 FHIR R4 resources covering demographics, encounters, problems, medications, allergies, immunizations, vitals, labs, diagnostics, procedures, documents, care plans, goals, care team, family history, appointments, medication administration, questionnaire responses, devices, and provenance. This is a standard USCDI-scope clinical exchange surface — all 19 US Core profiles are present, plus 5 base FHIR resources. There are no vendor extensions, no custom resource types, and no evidence of mapping beyond what (g)(10) already requires.

2. **Billing Data Export** via CSV report downloads: 29 report types covering invoices, receipts, claims, A/R aging, EOBs, ERAs, provider collections, tax reports, and insurance data. This is broader in domain than the FHIR API and addresses billing/RCM data. However, the reports are only available via interactive UI (not API), lack any field-level documentation, and are report-oriented (aggregated/filtered views) rather than raw data exports.

The FHIR clinical tier is well-documented at the API level but is structurally identical to a standard (g)(10) FHIR API — the same 24 resources, the same US Core profiles, the same Bulk Export. The billing CSV tier adds genuine coverage of non-clinical data but is poorly documented and operationally limited (manual UI downloads).

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | FHIR `Patient` (48 fields), `RelatedPerson` (20 fields) | Standard US Core demographics; no evidence of custom demographic fields |
| Encounters / visits | ✅ Covered | FHIR `Encounter` (47 fields), CSV Encounter Summary Report | Good clinical coverage via FHIR; encounter summary CSV adds billing context |
| Problems / conditions | ✅ Covered | FHIR `Condition` (32 fields) | Standard US Core Condition profile |
| Medications / prescriptions | ✅ Covered | FHIR `Medication` (10), `MedicationRequest` (32), `MedicationAdministration` (24) | Includes MAR beyond USCDI minimum |
| Allergies | ✅ Covered | FHIR `AllergyIntolerance` (34 fields) | Standard US Core; drug-herb interaction data from CharmHealth not evident |
| Immunizations | ✅ Covered | FHIR `Immunization` (58 fields) | Well-represented in FHIR |
| Vitals | ✅ Covered | FHIR `Observation` (39 fields, multiple categories) | Standard US Core vital signs profiles |
| Lab results | ✅ Covered | FHIR `Observation`, `DiagnosticReport` (30 fields) | Standard US Core lab profiles |
| Imaging / diagnostic reports | ✅ Covered | FHIR `DiagnosticReport` (30 fields) | Standard US Core |
| Procedures | ✅ Covered | FHIR `Procedure` (17 fields) | Standard US Core |
| Clinical notes / documents | ✅ Covered | FHIR `DocumentReference` (45 fields); C-CDA export per encounter | Standard US Core; C-CDA provides narrative notes |
| Care plans / goals | ✅ Covered | FHIR `CarePlan` (15), `Goal` (20) | Standard US Core |
| Orders / referrals | ⚠️ Partial | FHIR `MedicationRequest` covers med orders; no `ServiceRequest` resource for non-med orders/referrals | Product supports referrals but no FHIR ServiceRequest or referral-specific export |
| Insurance / coverage | ⚠️ Partial | CSV Patient Insurance Report; no FHIR `Coverage` resource | Insurance data only via single CSV report from analytics UI — no structured/API export |
| Claims / billing | ⚠️ Partial | CSV: Claims List, Claims Aging, Claims by Patient/Provider, Claim Procedures List (5 reports) | Reports exist but are UI-only, undocumented fields, aggregated views rather than raw claim records |
| Payments | ⚠️ Partial | CSV: Receipts List, Receipts by Patient, Payment Collection by Provider, etc. (9+ reports) | Same limitations as claims — UI-only, no field documentation |
| Consents / directives | ❌ Not covered | No consent resources in FHIR API; no consent export mentioned | Product generates telehealth consent docs; these appear unexported |
| Patient communications / portal messages | ❌ Not covered | No messaging data in FHIR API or CSV exports | Product has patient portal messaging and CharmConnect secure messaging; significant gap |
| Custom forms / intake | ⚠️ Partial | FHIR `QuestionnaireResponse` (16 fields) | Present but unclear if all custom forms/intake questionnaires are captured |
| Specialty-specific (integrative medicine) | ❌ Not covered | No specialty-specific resources, extensions, or exports | Product markets to integrative/functional medicine with drug-herb interactions, supplement inventory; no evidence these are exported |
| Telehealth records | ❌ Not covered | No telehealth session data in any export | Product includes integrated telehealth; session records not exported |
| Inventory / dispensing | N/A | Not EHI | Inventory management data is operational, not part of designated record set |

## 6. Documentation Quality

**FHIR API Documentation**: Well-structured single-page doc with clear endpoint definitions, parameter tables (name, type, required/optional, description), and response examples for every resource. OAuth/SMART authentication is documented. Bulk Export API is documented with start/status/delete operations. A developer could implement FHIR data retrieval from this documentation.

**What's missing from FHIR docs**: No product-specific data dictionary. No mapping of CharmHealth's internal data model to FHIR elements. No vendor extensions documented. No indication of which fields are CharmHealth-specific vs standard FHIR. No value sets or coded value documentation beyond FHIR standards. No sample bulk export output.

**Billing/Claims CSV Documentation**: Procedural "how-to" documentation (how to run reports, grouping options, filters) but **zero field-level documentation**. No column names, no data types, no descriptions. A developer cannot determine the CSV schema without interacting with the live system. No sample CSV files provided.

**Overall**: The documentation is adequate for a developer to call the FHIR API and download billing CSVs, but insufficient to understand the full scope of exported data or build an import pipeline for the CSV exports. The FHIR portion is standard (g)(10) documentation; the billing portion is user guide material, not a data dictionary.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The clinical data export (FHIR API) covers the full USCDI clinical scope plus a few resources beyond USCDI (Appointment, MedicationAdministration, QuestionnaireResponse). The billing/claims tier adds 29 CSV report types covering invoices, receipts, claims, A/R, EOBs, ERAs, and insurance — this does address billing data, which many vendors omit entirely.

However, significant gaps exist relative to what CharmHealth stores:
- **Patient portal messages and secure messaging** (CharmConnect): a core product feature generating EHI, completely absent from exports
- **Telehealth session records**: product includes integrated video visits, no export
- **Specialty/integrative medicine data**: drug-herb interactions, supplement dispensing records — a key differentiator for CharmHealth, not in exports
- **Referral workflows**: product supports referrals, no ServiceRequest or referral export
- **Consent documents**: telehealth consents and other consent forms not exported

The billing CSV coverage, while broader than many vendors, is structurally weak: reports are aggregated views (grouped by patient/provider/payer), not raw transactional records. A CSV "Claims List" grouped by payer is not the same as exporting individual claim records with all fields.

**Axis 2 — Export approach: Repackaged existing export**

The clinical data export is the vendor's standard FHIR (g)(10) API presented as (b)(10). The evidence is clear:
1. All 19 US Core profiles are present — exactly what (g)(10) requires
2. No vendor-specific FHIR extensions or custom resource types
3. The Bulk Export API is the standard (g)(10) Bulk Data mechanism
4. The documentation page explicitly references the same FHIR API used for (g)(10)
5. No product-specific data dictionary mapping CharmHealth data to FHIR

The billing CSV tier adds genuine non-clinical data, which is a step beyond pure (g)(10) repackaging. But these are existing billing reports that practices already use for operational purposes — they were not purpose-built for (b)(10). The EHI export page simply links to the existing billing Resource Center documentation.

The vendor assembled existing capabilities (FHIR API + billing reports) under a (b)(10) label rather than building a purpose-specific EHI export. There is no evidence of any new development for (b)(10) compliance — no new data dictionary, no new export format, no new API endpoints beyond what (g)(10) and operational billing already provided.

### Key Findings

1. **FHIR API is a standard (g)(10) surface relabeled as (b)(10)**: 24 FHIR resources with 19 US Core profiles, no vendor extensions, no custom mappings — structurally identical to the (g)(10) FHIR API requirement. The EHI export page points directly to the same FHIR API documentation.

2. **Billing CSV reports add breadth but lack depth**: 29 report types covering invoices, claims, A/R, EOBs, and insurance data provide genuine billing coverage that many vendors omit. However, these are UI-only exports with zero field-level documentation — no column names, types, or descriptions are provided anywhere.

3. **Major data domains are completely absent**: Patient portal messages (secure messaging is a core feature), telehealth session data, consent documents, and specialty integrative medicine data (drug-herb interactions, supplement records) have no export path.

4. **No product-specific data dictionary exists**: Neither the FHIR API docs nor the billing CSV docs provide a CharmHealth-specific mapping of internal data to export fields. The FHIR docs reference the standard FHIR specification; the billing docs are user guides, not data dictionaries.

5. **Billing export is operationally limited**: CSV exports require interactive UI access (login → navigate → run report → download). No API for billing data, no bulk billing export, no automation path. This is impractical for a full patient data export.

### Summary Stats

```
Coverage:        Partial
Approach:        Repackaged existing export
Export format:   FHIR R4 JSON, NDJSON (Bulk), HL7 C-CDA, CSV (billing)
Entities:        24 FHIR resources + 29 billing CSV report types (54 total)
Fields:          ~650 (from FHIR examples); billing CSV fields undocumented
Descriptions:    0% (no product-specific field descriptions; FHIR uses standard spec)
Sample data:     Yes (FHIR response examples in API docs); No (no billing CSV samples)
Bulk export:     Yes (FHIR Bulk Export API); No (billing is manual UI only)
Domains covered: 12 of 17 applicable domains (✅ or ⚠️)
```

### Bottom Line

CharmHealth's (b)(10) export is its existing (g)(10) FHIR API plus links to existing billing CSV reports — no purpose-built EHI export was created. A patient would get standard USCDI clinical data via FHIR and could manually download billing reports as CSVs, but would miss portal messages, telehealth records, secure messaging history, and specialty integrative medicine data. The biggest gap is the complete absence of patient communication data (portal messages and CharmConnect) from a product where secure messaging is a core feature.
