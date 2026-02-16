# EHI Export Analysis: TenEleven Group

**Product**: electronic Clinical Record (eCR™) v2.4
**Analysis date**: 2026-02-15
**CHPL ID**: 11200 (15.04.04.2861.Elec.24.01.1.221231)

## 1. Product Context

electronic Clinical Record (eCR) is a comprehensive **behavioral health EHR and practice management system** developed by TenEleven Group, now part of Ensora Health (formerly Therapy Brands, acquired by KKR in 2021). The product targets behavioral health agencies (10+ users) providing mental health, substance use treatment, and human services. It is certified under (b)(10) along with 40+ other ONC criteria.

**Data domains the product stores** (per vendor materials, press releases, and the Ensora Health knowledge base):

- **Clinical**: Patient demographics, visit history, treatment plans, progress notes, clinical assessments, goals/objectives, diagnoses (DSM-5), custom clinical forms (FormLab), medical necessity documentation ("Golden Thread")
- **Medications**: E-prescribing, medication administration records (MAR), MAT dosing schedules, medication adherence, tapering plans, dispensing records with photo verification
- **Lab**: Electronic lab ordering and results
- **Billing/RCM**: Electronic claims (primary/secondary), batch claim submission, ERA/EOB processing, payment records, credit card transactions, patient statements, daily billing reports
- **Scheduling**: Client appointments, calendar management
- **Bed management**: Bed assignments, occupancy records, resident status tracking (inpatient/residential settings)
- **Patient portal**: Patient-facing records access
- **Intake/referral**: Referral intake through admission, discharge, aftercare
- **Specialty**: MAT (medication-assisted treatment) with DEA/CMS compliance; FormLab for customizable behavioral health forms; CCBHC support; state system integrations (NJ PDMP, NJ SAMS)

This is a broad product covering clinical documentation, prescribing, billing, and behavioral health specialty workflows. A complete (b)(10) export should cover all of these domains.

## 2. Artifacts Reviewed

| Artifact | Type | Size | What It Tells | Informativeness |
|---|---|---|---|---|
| `PDF-for-Website-on-Formats-2.pdf` | PDF, 1 page | 116 KB | Two export formats exist: JSON (single patient, USCDI v1 + "other applicable data") and .bak (SQL Server backup for population). This is the **entire** EHI export documentation. | **Low** — 72 words of substance, no schema, no data dictionary |
| `screenshot-ehi-export-section.png` | PNG screenshot | 174 KB | Shows the EHI Export section on the ONC disclosure page, confirming two export modes and that population export requires a Salesforce support ticket | Medium — confirms process constraints |
| `screenshot-onc-page-top.png` | PNG screenshot | 157 KB | Confirms developer info, product version 2.4, certification date 12/31/2022, additional software: eRx, Inpriva, Dynamic Health IT | Low — metadata only |
| `screenshot-fhir-api-docs.png` | PNG screenshot | 287 KB | Shows the FHIR API docs page branding ("Dynamic FHIR" by Therapy Brands). This is (g)(10) API documentation, not (b)(10) export documentation. | Low for (b)(10) assessment |
| ONC disclosure page (live) | Web page | — | Verified live 2026-02-15; content matches screenshots. Confirms two export types, variability disclaimer, File Formats link, and FHIR Endpoints section (separate from EHI Export). | Medium |
| FHIR API documentation (live) | Web page | ~150 KB | Verified live 2026-02-15. Extensive (g)(10) docs: 29 FHIR resource type entries covering USCDI v1 data classes. Explicitly states API is limited to USCDI data. Not (b)(10) documentation. | Low for (b)(10) |

**Most informative artifact**: The PDF (`PDF-for-Website-on-Formats-2.pdf`) is the only (b)(10)-specific documentation, but it contains minimal information. The FHIR API documentation is detailed but explicitly covers (g)(10), not (b)(10).

**No data dictionary, schema, sample data, or field-level documentation of any kind exists for the (b)(10) export.**

## 3. Export Mechanics

**Single Patient Export**:
- **Format**: JSON
- **Content**: "USCDI v1 data as well as other applicable data" (per the PDF)
- **Mechanism**: Self-service ("without developer assistance"), presumably via UI button
- **Documentation of how to initiate**: None provided
- **JSON structure/schema**: Not documented. It's unclear whether this is FHIR JSON, proprietary JSON, or something else. The phrase "other applicable data" beyond USCDI is entirely unexplained.

**Patient Population Export**:
- **Format**: `.bak` file (Microsoft SQL Server database backup)
- **Content**: "A full SQL Server database backup of all data for an agency"
- **Mechanism**: Vendor-assisted — submit a support ticket via Salesforce
- **Self-service**: No
- **Schema documentation**: None
- **Requirements**: Recipient needs Microsoft SQL Server to restore the backup

**Access constraints**: Population export requires contacting the vendor. No mention of fees for the export itself, though the attestation disclosure page lists costs for setup and maintenance generally.

## 4. Export Content: What's In It

### What is documented

The entire (b)(10) documentation consists of 72 words across two bullet points in a 1-page PDF (created 2023-11-30, authored by Catherine Baker in Microsoft Word):

1. **Single Patient JSON**: "The data includes USCDI v1 data as well as other applicable data." No definition of what "other applicable data" means. No schema, no field list, no sample output.

2. **Population .bak file**: "This is a full SQL Server database backup of all data for an agency that can be restored." No table list, no entity-relationship diagram, no field definitions, no guidance on interpreting the database.

### What we can infer

**Single patient export** likely covers the USCDI v1 data classes visible in the (g)(10) FHIR API:
- Patient Demographics
- Problem List (Condition)
- Procedures
- Smoking Status (Observation)
- Vital Signs (Observation)
- Laboratory Results (Observation) and Laboratory Tests (DiagnosticReport)
- Goals
- Immunizations
- Assessment/Plan (CarePlan)
- Care Team (CareTeam)
- Health Concerns (Condition)
- Medications (MedicationRequest)
- Allergies (AllergyIntolerance)
- Implantable Devices (Device)
- Clinical Notes via DocumentReference: Consultation Notes, Discharge Summaries, H&P Notes, Procedure Notes, Progress Notes
- Diagnostic Reports: Cardiology, Pathology, Radiology

The phrase "other applicable data" could mean anything — there is no documentation to determine its scope.

**Population export** (.bak) should theoretically contain the entire SQL Server database: all clinical data, billing records, custom forms (FormLab), MAT dosing data, bed management records, scheduling, and every other table in the system. A SQL Server backup is by definition complete — it's the database itself. However, without any schema documentation, a recipient would need to reverse-engineer the entire database to understand it.

### Vendor's own content organization

The vendor provides **no content organization** for the EHI export. There is no data dictionary, no table listing, no categorization of exported data. The only categorization comes from the FHIR API documentation (which is (g)(10), not (b)(10)), where data is organized by USCDI v1 data classes:

| USCDI Category (from FHIR API) | FHIR Resource | Notes |
|---|---|---|
| Patient Demographics | Patient | US Core profiled |
| Problem List | Condition | category=problem-list-item |
| Health Concerns | Condition | category=health-concern |
| Procedures | Procedure | US Core profiled |
| Smoking Status | Observation | code=72166-2 |
| Vital Signs | Observation | category=vital-signs |
| Laboratory Results | Observation | category=laboratory |
| Laboratory Tests | DiagnosticReport | category=laboratory |
| Goals | Goal | US Core profiled |
| Immunizations | Immunization | US Core profiled |
| Assessment/Plan | CarePlan | category=assess-plan |
| Care Team Members | CareTeam | US Core profiled |
| Medications | MedicationRequest | US Core profiled |
| Allergies | AllergyIntolerance | US Core profiled |
| Implantable Devices | Device | US Core profiled |
| Clinical Notes | DocumentReference | 5 note types |
| Diagnostic Reports | DiagnosticReport | Cardiology, Pathology, Radiology |
| Encounters | Encounter | US Core profiled |
| Practitioner | Practitioner | Supporting resource |
| PractitionerRole | PractitionerRole | Supporting resource |
| Location | Location | Supporting resource |
| Organization | Organization | Supporting resource |

This table documents the **FHIR (g)(10) API**, not the (b)(10) export. The (b)(10) export has no equivalent documentation.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor provides almost no information about (b)(10) export content. The only substantive claims are:

1. **Single patient JSON** includes "USCDI v1 data as well as other applicable data" — the USCDI v1 portion can be inferred from the FHIR API mapping (17 USCDI data classes mapped to ~22 FHIR resource types). The "other applicable data" is undefined.

2. **Population .bak file** is a "full SQL Server database backup of all data for an agency" — this should include everything in the database, but without a schema, the specific content is unknown.

The FHIR API documentation (which is (g)(10) only) is the richest data available, but it explicitly states: "Available data via the API interface is limited by the data defined by the USCDI." This confirms USCDI is a subset, not the full dataset.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Single patient JSON claims USCDI v1 (includes Patient). Population .bak should contain all demographics. No field-level documentation for either. | Likely present but undocumented |
| Encounters / visits | ⚠️ Partial | FHIR API supports Encounter. Single patient JSON may include via USCDI. Population .bak should contain all encounters. | Likely present but undocumented |
| Problems / conditions / diagnoses | ⚠️ Partial | FHIR API supports Condition (problem-list-item, health-concern). DSM-5 diagnoses are core to the product. Population .bak should contain all. | DSM-5 specific diagnoses may differ from SNOMED-only USCDI mapping; undocumented |
| Medications / prescriptions | ⚠️ Partial | FHIR API supports MedicationRequest. E-prescribing is a core feature. Population .bak should contain all. | USCDI covers prescriptions but likely misses MAT-specific dosing, tapering plans, dispensing records |
| Allergies | ⚠️ Partial | FHIR API supports AllergyIntolerance. Population .bak should contain all. | Likely present but undocumented |
| Immunizations | ⚠️ Partial | FHIR API supports Immunization. Population .bak should contain all. | Likely present but undocumented |
| Vitals | ⚠️ Partial | FHIR API supports Observation (vital-signs). Population .bak should contain all. | Likely present but undocumented |
| Lab results | ⚠️ Partial | FHIR API supports Observation (laboratory) and DiagnosticReport. Population .bak should contain all. | Likely present but undocumented |
| Imaging / diagnostic reports | ⚠️ Partial | FHIR API supports DiagnosticReport (Cardiology, Pathology, Radiology). Population .bak should contain all. | Likely present but undocumented |
| Procedures | ⚠️ Partial | FHIR API supports Procedure. Population .bak should contain all. | Likely present but undocumented |
| Clinical notes / documents | ⚠️ Partial | FHIR API supports DocumentReference (5 note types). Population .bak should contain all notes. | Behavioral health progress notes, FormLab custom forms may not be covered by USCDI note types |
| Care plans / goals | ⚠️ Partial | FHIR API supports CarePlan and Goal. Population .bak should contain all. Treatment planning is core to eCR. | Behavioral health treatment plans may be richer than USCDI CarePlan representation |
| Orders / referrals | ⚠️ Partial | Product supports intake/referral management. Population .bak should contain referral data. Single patient JSON coverage unknown. | Undocumented |
| Insurance / coverage | ❌ Not documented | No insurance entities mentioned in any (b)(10) documentation. Product does billing, so insurance data exists. Population .bak should contain it. | **Significant gap in documentation** — product clearly stores insurance data for billing |
| Claims / billing | ❌ Not documented | No billing entities mentioned in any (b)(10) documentation. Product has full RCM including claims, ERA/EOB, payments. Population .bak should contain all billing data. | **Significant gap in documentation** — product's billing module is a major feature |
| Payments | ❌ Not documented | No payment entities mentioned. Product supports credit card processing, patient statements. Population .bak should contain payment data. | **Significant gap in documentation** |
| Consents / directives | ❌ Not documented | No consent entities mentioned. Behavioral health settings typically require extensive consent documentation. | Unknown if product stores consents; undocumented |
| Patient communications / portal | ❌ Not documented | Product has a patient portal certified under (e)(1). Population .bak should contain portal data. | Undocumented |
| Specialty: MAT (Medication-Assisted Treatment) | ❌ Not documented | MAT is a key differentiator: dosing schedules, tapering plans, dispensing records with photo verification. No mention in (b)(10) documentation. Population .bak should contain all MAT data. | **Major gap in documentation** — MAT is a core product feature |
| Specialty: Behavioral health assessments (FormLab) | ❌ Not documented | FormLab allows custom clinical forms. No mention in (b)(10) documentation. Population .bak should contain all custom form data. | **Major gap in documentation** — custom forms are a key feature |
| Specialty: Bed management | ❌ Not documented | Product supports inpatient/residential bed management. No mention in (b)(10) documentation. Population .bak should contain bed data. | Undocumented |

**Key observation**: The .bak population export theoretically covers all domains (it's the entire database), but the complete lack of documentation means we cannot verify what's actually in it. For the single patient JSON export, only USCDI v1 data is documented; everything behavioral health-specific (MAT, FormLab, billing, bed management) is unaddressed.

## 6. Documentation Quality

**Documentation is near-zero.** The entire (b)(10) export documentation is:
- 1 paragraph on the ONC disclosure page (two numbered items, ~80 words)
- 1 one-page PDF with two bullet points (~72 words of substance)

**What's missing**:
- ❌ Data dictionary or schema for either export format
- ❌ Field-level definitions
- ❌ Table/entity descriptions for the .bak database
- ❌ Sample data or example JSON output
- ❌ Instructions for performing the single patient export
- ❌ Instructions for restoring or interpreting the .bak file
- ❌ Documentation of what "other applicable data" beyond USCDI means
- ❌ Value sets, code systems, or coded field documentation
- ❌ Relationships between tables
- ❌ Any behavioral health-specific export documentation
- ❌ Machine-readable schemas

**Could a developer use this?** No. A developer receiving either a JSON file or a .bak file would have no documentation to guide parsing, interpretation, or import. The JSON format isn't even specified (FHIR JSON? proprietary JSON?). The .bak file requires SQL Server and reverse-engineering of an unknown schema.

The FHIR (g)(10) API documentation, by contrast, is reasonably detailed (29 resource type entries with search parameters, URL syntax, and sample responses). But this explicitly covers a different criterion and is limited to USCDI data.

## 7. Overall Assessment

### Classification

**Minimal/stub** — Documentation is too thin to meaningfully assess what the export contains. The population export (.bak) may be technically complete (a full database backup necessarily contains everything), but with zero schema documentation, the completeness is theoretical rather than practical. The single patient JSON export is ambiguously described and undocumented.

### Key Findings

1. **The entire (b)(10) documentation is 72 words on a single PDF page** (`PDF-for-Website-on-Formats-2.pdf`, created 2023-11-30). No data dictionary, no schema, no field definitions, no sample data exist for either export format.

2. **The population export (.bak) is a SQL Server database backup** — theoretically the most complete possible export (it's the entire database), but it requires proprietary Microsoft software to restore and has zero schema documentation. A recipient would need to reverse-engineer the entire database.

3. **The single patient JSON export's scope is ambiguous** — it claims "USCDI v1 data as well as other applicable data" but does not define what "other applicable data" means. The JSON structure/schema is not documented; it's unclear whether it's FHIR JSON or a proprietary format.

4. **No behavioral health-specific data is documented in the export** — despite MAT, FormLab custom forms, bed management, and behavioral health billing being core product features. These are genuine EHI domains for this product.

5. **The population export requires a vendor-mediated support ticket via Salesforce** — it cannot be self-initiated. The single patient export is described as self-service but no instructions are provided for how to perform it.

### Summary Stats

```
Classification:  Minimal/stub
Export format:   JSON (single patient), .bak/SQL Server backup (population)
Model type:      Unknown (single patient); native database dump (population)
Entities:        N/A (no data dictionary)
Fields:          N/A (no data dictionary)
Descriptions:    N/A (no data dictionary)
Sample data:     No
Bulk export:     Yes (population .bak via support ticket)
Domains covered: Unable to verify — documentation covers only USCDI v1; .bak theoretically covers all but is undocumented
```

### Bottom Line

TenEleven/Ensora Health's (b)(10) export documentation is among the thinnest possible while still technically existing. The population export (.bak) is an honest approach — a full SQL Server backup genuinely contains everything — but without any schema documentation, a recipient cannot practically interpret the data. A patient or provider would get a database file they cannot read and a JSON file of unknown structure. The single biggest gap is the complete absence of any documentation: no data dictionary, no schema, no field definitions, and no explanation of what the product's behavioral health-specific data (MAT dosing, custom forms, billing) looks like in the export.
