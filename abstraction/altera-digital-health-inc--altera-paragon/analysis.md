# EHI Export Analysis: Altera Digital Health

**Product**: Paragon® Denali (v1) / Paragon® EHR (v25)
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.3123.Para.01.10.1.250130 (Denali), 15.04.04.3123.Para.25.10.1.260202 (EHR)

## 1. Product Context

Paragon is a comprehensive, integrated hospital EHR platform developed by Altera Digital Health (formerly part of Allscripts) that targets community, rural, and critical access hospitals. Both CHPL listings (Denali = cloud-native SaaS, EHR = traditional deployment) share identical certified criteria and represent the same product platform at different deployment stages.

Paragon stores data across the following core domains, all relevant to (b)(10) completeness:

- **Clinical**: Patient demographics, problem lists, medication lists, allergies, clinical notes/documentation (including AI-transcribed ambient notes), vital signs, assessments, care plans, CPOE orders, CDS alerts, immunizations, family history
- **Ancillary services**: Pharmacy management (dispensing, drug interaction alerts), laboratory (orders, specimens, results, QC), radiology (procedures, film tracking)
- **Surgical/OR**: Perioperative charting, OR scheduling, supply tracking, charge capture
- **Emergency department**: Visit records, coded clinical data
- **Revenue cycle/financial**: Patient registration, billing/accounting, claims management (PreBill editing), collections, insurance, scheduling
- **Patient portal**: CarePath portal — health records, lab results, clinical summaries, provider messaging
- **Public health**: Immunization reporting, syndromic surveillance, case reporting, cancer registry

Key question: Does the export cover the breadth of clinical *and* financial/revenue cycle data Paragon stores?

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/paragon-25-1/CapabilityStatement.json` (460 KB) | FHIR R4 CapabilityStatement documenting 48 resource types with standard elements and custom extensions. Dated 2026-02-12. **Primary data dictionary.** | ⭐ High |
| `downloads/paragon-25-1/Extension-Details.xlsx` (64 KB) | Excel spreadsheet with 826 rows documenting custom Paragon-specific FHIR extensions across 33 resource types, each with name and natural-language definition | ⭐ High |
| `downloads/compliance-page.html` (204 KB) | Altera's ONC regulatory compliance webpage with EHI export links and brief usage instructions | Medium |
| `downloads/paragon-ehr-25-1-denali-1.zip` (84 KB) | ZIP containing the above two files | N/A (container) |
| `downloads/paragon-24-1/CapabilityStatement.json` (460 KB) | Previous version (24.1) — identical file size suggests no changes | Low |
| `downloads/paragon-24-1/Extension-Details.xlsx` (64 KB) | Previous version extension details | Low |
| `downloads/capabilitystatement.json` (394 KB) | Archived Paragon 23.2 version (Bundle format, older structure) | Low |
| `downloads/extension-details.xlsx` (64 KB) | Archived Paragon 23.2 extension details | Low |
| `downloads/enrichment/` | Prior agent's extraction scripts and outputs — used for reference but independently verified | Reference |

No sample data files, user guides, screenshots, or StructureDefinition resources were provided.

## 3. Export Mechanics

- **Format**: FHIR R4 JSON (NDJSON), per CapabilityStatement `format: ["json"]`
- **Mechanism**: FHIR server with `search-type` interaction on all resources, searchable by `patient` and `_lastUpdated` parameters. The CapabilityStatement references a development server URL (`pqsambmainc9.cloud.mdrxdev.com`), suggesting a FHIR Bulk Data-style API endpoint.
- **Single-patient vs bulk**: Search params include `patient`, indicating single-patient capability. Bulk export capability is not explicitly documented but FHIR Bulk Data patterns are implied by the NDJSON format.
- **Access constraints**: No export instructions, user guide, or step-by-step process documented. The compliance page says only: "Open the 'Paragon Capability Statement' file on your local machine to look at all the fields that are captured for modules under each categories."
- **Fees**: Not mentioned.

## 4. Export Content: What's In It

### Data dictionary structure

The EHI export documentation consists of a FHIR R4 CapabilityStatement (the schema) plus an Extension Details spreadsheet (definitions for custom extensions). Together they define:

- **48 FHIR resource types** (entities)
- **1,425 total fields** across all resources
  - 589 standard FHIR elements (names only, no types/descriptions)
  - 836 custom Paragon extensions (826 with natural-language definitions from XLSX, 10 CS-only without definitions)
- **58.0% of fields have descriptions** (all 826 XLSX-matched extensions; standard elements have no descriptions)
- **Data types**: Not documented for any field
- **Value sets**: Not documented
- **Relationships/foreign keys**: Not documented (implicit via FHIR references)
- **3 resource types have zero fields**: ChargeItemDefinition, PaymentNotice, Person (declared but empty)

### Vendor's own content organization

The CapabilityStatement does not organize resources into explicit categories. The following categorization is derived from FHIR resource type semantics and the extension content:

| Entity (FHIR Resource) | Standard Fields | Custom Extensions | Total Fields | Category |
|---|---|---|---|---|
| Claim | 20 | 172 | 192 | Billing |
| Coverage | 12 | 130 | 142 | Billing |
| Patient | 15 | 64 | 79 | Demographics |
| MedicationRequest | 27 | 49 | 76 | Medications |
| Encounter | 19 | 51 | 70 | Encounters |
| PaymentReconciliation | 11 | 58 | 69 | Billing |
| DocumentReference | 15 | 41 | 56 | Documents |
| Observation | 18 | 38 | 56 | Diagnostics |
| MedicationAdministration | 13 | 36 | 49 | Medications |
| ServiceRequest | 27 | 20 | 47 | Orders |
| ChargeItem | 18 | 18 | 36 | Billing |
| Device | 19 | 17 | 36 | Infrastructure |
| Consent | 12 | 21 | 33 | Clinical |
| Immunization | 18 | 13 | 31 | Immunizations |
| Communication | 9 | 17 | 26 | Orders |
| CommunicationRequest | 17 | 6 | 23 | Orders |
| Location | 9 | 14 | 23 | Infrastructure |
| Appointment | 20 | 2 | 22 | Encounters |
| GuidanceResponse | 10 | 9 | 19 | Clinical |
| MedicationStatement | 14 | 5 | 19 | Medications |

*(Full inventory of all 48 resources in `analysis/entity-inventory-full.json`)*

### Category breakdown

| Category | Entities | Total Fields | Custom Extensions |
|---|---|---|---|
| Billing | 9 | 475 | 379 |
| Medications | 6 | 184 | 99 |
| Clinical | 11 | 181 | 50 |
| Infrastructure | 6 | 103 | 42 |
| Encounters | 3 | 100 | 53 |
| Orders | 3 | 96 | 43 |
| Demographics | 3 | 96 | 69 |
| Diagnostics | 4 | 91 | 43 |
| Documents | 2 | 68 | 45 |
| Immunizations | 1 | 31 | 13 |
| **Total** | **48** | **1,425** | **836** |

### Notable extension examples

**Billing depth** (strongest signal of purpose-built export):
- Claim: 172 custom extensions including billing status, agent, diagnosis codes, modifiers, referring physician, patient/person/long notes, attending physician, claim edits, HCPCS codes, revenue codes, DRG, insurance plan details
- Coverage: 130 extensions including visit category, payor verification, priority, reimbursement type/method, copay, deductible, authorization numbers, group plan, subscriber details
- PaymentReconciliation: 58 extensions including payment details, adjustment codes, remittance info

**Clinical depth**:
- Patient: 64 extensions (Organ Donor, Veteran, VIP, race, ethnicity, SSN, language, religion, etc.)
- Encounter: 51 extensions (age at admission, financial class, medical record number, arrived by, admission class, attending/admitting/consulting physicians, discharge disposition)
- MedicationRequest: 49 extensions (Rx number, prescriber, dose type, verified by, sign off reason, pharmacy details)
- MedicationAdministration: 36 extensions (MAR data — detailed administration records)
- DocumentReference: 41 extensions (document metadata beyond standard FHIR)

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export's strongest signal is its **billing/financial depth**: 9 billing-related FHIR resources with 475 fields (379 custom extensions). The Claim resource alone has 172 custom extensions — this is not something that appears in a (g)(10) or C-CDA export. Coverage (130 extensions) and PaymentReconciliation (58 extensions) similarly represent deep, product-specific financial data mapping.

Clinical coverage is broad (22 clinical resource types across conditions, medications, observations, procedures, immunizations, care plans, documents, etc.) but relies more heavily on standard FHIR elements with moderate custom extension density (50 custom extensions across 11 clinical entities). This is appropriate — standard FHIR clinical elements are reasonably comprehensive for clinical data.

The inclusion of Communication and CommunicationRequest (23 total extensions) suggests patient messaging/communication data is partially captured. Consent (21 extensions) is unusually detailed. GuidanceResponse (9 extensions including location, user, action taken) captures CDS alert history.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient` (79 fields, 64 custom), `RelatedPerson` (17 fields), `Person` (0 fields) | Deep — organ donor, veteran, VIP, religion, etc. beyond USCDI |
| Encounters / visits | ✅ Covered | `Encounter` (70 fields, 51 custom), `Appointment` (22 fields) | Deep — financial class, arrival mode, admission class, discharge disposition |
| Problems / conditions | ✅ Covered | `Condition` (16 fields, 1 custom) | Adequate via standard FHIR; minimal custom extensions |
| Medications / prescriptions | ✅ Covered | `MedicationRequest` (76 fields), `MedicationAdministration` (49 fields), `MedicationDispense` (18), `MedicationStatement` (19), `Medication` (4) | Deep — Rx numbers, prescriber detail, MAR data, dose types |
| Allergies | ✅ Covered | `AllergyIntolerance` (15 fields, 2 custom) | Standard coverage with Rx-verification extensions |
| Immunizations | ✅ Covered | `Immunization` (31 fields, 13 custom) | Solid with custom extensions |
| Vitals | ✅ Covered | `Observation` (56 fields, 38 custom) | Vitals are a subset of Observation; good custom depth |
| Lab results | ✅ Covered | `Observation` (56 fields), `DiagnosticReport` (18 fields), `Specimen` (13 fields) | Reasonable — hold status extensions on DiagnosticReport |
| Imaging / diagnostic reports | ⚠️ Partial | `ImagingStudy` (4 fields, 0 custom) | Thin — only 4 standard fields, no custom extensions. Paragon has radiology workflow (film tracking, department data) not captured. |
| Procedures | ✅ Covered | `Procedure` (14 fields, 2 custom) | Basic coverage; only 2 custom extensions seems light for OR/surgical module |
| Clinical notes / documents | ✅ Covered | `DocumentReference` (56 fields, 41 custom), `Media` (12 fields) | Deep — 41 custom extensions for document metadata |
| Care plans / goals | ✅ Covered | `CarePlan` (18 fields), `CareTeam` (11 fields), `Goal` (10 fields) | Standard coverage, no custom extensions |
| Orders / referrals | ✅ Covered | `ServiceRequest` (47 fields, 20 custom), `NutritionOrder` (18 fields) | Good — includes hold status, custom order metadata |
| Insurance / coverage | ✅ Covered | `Coverage` (142 fields, 130 custom), `CoverageEligibilityRequest` (15), `CoverageEligibilityResponse` (12) | Exceptionally deep — 130 custom extensions |
| Claims / billing | ✅ Covered | `Claim` (192 fields, 172 custom), `ChargeItem` (36 fields), `Account` (9 fields) | Exceptionally deep — strongest domain in the export |
| Payments | ✅ Covered | `PaymentReconciliation` (69 fields, 58 custom), `PaymentNotice` (0 fields) | Deep reconciliation; PaymentNotice is empty placeholder |
| Consents / directives | ✅ Covered | `Consent` (33 fields, 21 custom) | Unusually detailed for an EHI export |
| Patient communications | ⚠️ Partial | `Communication` (26 fields, 17 custom), `CommunicationRequest` (23 fields) | Present but unclear if this captures CarePath portal messages specifically |
| Specialty — ED | ❌ Not covered | No ED-specific resources or extensions | Paragon has an ED module; no ED-specific data visible |
| Specialty — OR/Surgical | ⚠️ Partial | `Procedure` (2 custom extensions) | Paragon has OR module with perioperative charting, supply tracking, charge capture — only 2 custom extensions on Procedure seems light |
| Specialty — Pharmacy workflow | ⚠️ Partial | Medication resources present but no dispensing cabinet or drug interaction history detail | Pharmacy module workflow (verification, alerts history) not clearly captured |

## 6. Documentation Quality

**Moderate quality — functional but incomplete.**

**Strengths:**
- Machine-readable FHIR CapabilityStatement provides structured schema
- 826 of 836 custom extensions have natural-language definitions
- Documentation is versioned (23.2 → 24.1 → 25.1) showing active maintenance
- Export format (FHIR R4) is well-chosen and interoperable

**Weaknesses:**
- **No export instructions**: No user guide, screenshots, or step-by-step process for triggering an export
- **No data types**: Neither standard elements nor custom extensions specify data types, cardinality, or constraints
- **No value sets**: Coded fields don't document valid values or code systems
- **No StructureDefinitions**: Custom extensions exist only in a spreadsheet, not as formal FHIR StructureDefinition resources
- **No sample data**: No example FHIR resources or sample export files
- **No relationship documentation**: How resources reference each other is not explicitly mapped
- **Standard element descriptions absent**: 589 standard fields have names only — a developer would need to consult hl7.org/fhir for element definitions
- **10 extensions in CS without XLSX definitions**: DiagnosticReport (Hold Notes, Hold Status), DocumentReference (Hold Status), GuidanceResponse (location, user name, user id, action taken), MedicationRequest (patient allergy), Observation (Hold Status), ServiceRequest (Hold Status)

**Could a developer build an import?** Partially. A developer familiar with FHIR R4 could understand the resource structure and standard elements. The custom extension names and definitions provide semantic meaning. However, without data types, value sets, or sample data, implementation would require trial-and-error with actual export output.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

The export demonstrably covers the breadth of data domains Paragon stores. The strongest evidence is the billing/financial depth: 9 billing resources with 475 fields and 379 custom extensions (Claim alone has 172). This is data that simply does not appear in a (g)(10) FHIR API or C-CDA export. Combined with 22 clinical resource types, 6 medication resources (including MAR), detailed encounter data (51 custom extensions), insurance/coverage (130 custom extensions), consent records, documents, devices, communications, and care planning — the export addresses most major domains the product handles.

Minor gaps exist in specialty areas (ED-specific data, OR/surgical workflow detail, radiology workflow), but these represent depth within covered domains rather than entire missing categories. The product's ERP modules (fiscal management, supply chain, HR) are absent, but these may be separate products outside the certified EHR scope.

**Axis 2 — Export approach: Purpose-built EHI export**

This is unambiguously a purpose-built export. The 836 custom Paragon-specific FHIR extensions — including 172 on Claim, 130 on Coverage, 58 on PaymentReconciliation — represent substantial engineering work to map Paragon's internal data model into FHIR R4. A repackaged (g)(10) export would not include billing resources at all, let alone 475 fields of billing detail with custom extensions. The CapabilityStatement is titled "Paragon EHI Export FHIR R4 Implementation" and is clearly separate from the product's (g)(10) FHIR API. The export uses FHIR R4 as the format, but the mapping goes far beyond any standard profile set — it's a product-specific data model expressed in FHIR.

### Key Findings

1. **Deep billing/financial coverage is the standout feature.** 475 fields across 9 billing resources with 379 custom extensions — Claim (172 extensions), Coverage (130), PaymentReconciliation (58) — demonstrate genuine engagement with (b)(10) requirements. This is data no (g)(10) API would ever surface.

2. **836 custom FHIR extensions across 33 resource types** represent substantial engineering effort to map Paragon's internal data model. All 826 XLSX-documented extensions include natural-language definitions.

3. **48 FHIR resource types span clinical, financial, administrative, and infrastructure domains.** The resource set goes well beyond USCDI's ~26 resource types, including billing, payments, consents, communications, and CDS history.

4. **Documentation quality is the main weakness.** No data types, no value sets, no sample data, no export instructions, no StructureDefinitions. A developer could understand *what* is exported but would struggle to build a robust import without actual export data to inspect.

5. **Some specialty module depth is thin.** Procedure (2 custom extensions) and ImagingStudy (0 extensions) don't reflect the depth of Paragon's OR and radiology modules. ED-specific data is absent despite the product having an ED module.

### Summary Stats

```
Coverage:        Comprehensive
Approach:        Purpose-built EHI export
Export format:   FHIR R4 JSON (NDJSON)
Entities:        48 FHIR resource types
Fields:          1,425 (589 standard + 836 custom)
Descriptions:    58.0% (826/1,425 — all custom extensions described; standard elements not)
Sample data:     No
Bulk export:     Unclear (single-patient search confirmed; bulk not documented)
Domains covered: 15 of 19 applicable domains (4 partial/missing in specialty areas)
```

### Bottom Line

Paragon's EHI export is a genuinely purpose-built effort that maps the product's internal data model into 48 FHIR R4 resource types with 836 custom extensions. Its billing/financial depth (475 fields, 379 custom) is among the strongest signals of authentic (b)(10) engagement. The main weaknesses are documentation gaps (no types, no sample data, no export instructions) and thin coverage of specialty modules (OR, ED, radiology workflow). A patient or provider would get a substantially complete copy of their clinical, billing, and insurance data, though specialty department workflow details may be underrepresented.
