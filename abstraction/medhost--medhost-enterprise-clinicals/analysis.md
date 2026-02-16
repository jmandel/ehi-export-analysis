# EHI Export Analysis: MEDHOST

**Product**: MEDHOST Enterprise - Clinicals
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2788.MEDH.CL.10.1.250806

## 1. Product Context

MEDHOST Enterprise - Clinicals is the clinical component of MEDHOST's integrated hospital information system, serving several hundred community and rural hospitals. It is an inpatient-focused EHR running on Microsoft SQL Server, covering:

- **Clinical charting**: physician documentation, nurse charting, care plans, vitals, assessments
- **Emergency department (EDIS)**: triage, patient tracking, ED documentation (separately certified but integrated)
- **Medications**: CPOE, pharmacy, eMAR with barcode scanning, e-prescribing (Surescripts)
- **Diagnostics**: lab and radiology ordering, results, diagnostic reports
- **Perioperative/anesthesia**: surgical scheduling, intra-op charting, anesthesia records, vitals graphing
- **Document management**: routing, access controls, clinical document storage
- **Patient engagement**: YourCare patient portal, condition management, self-check-in

**Financial/billing is a separate certified product** — "MEDHOST Enterprise - Financials" (CHPL# 15.04.04.2788.MEDH.FI.09.0.250606). The Clinicals module does capture charge data (automatic charge capture in EDIS and eMAR) that flows to Financials.

For (b)(10) assessment, the key question is whether the export covers: clinical documentation, medications (including MAR), diagnostics, procedures (including perioperative detail), encounters, demographics, insurance/coverage, charges, and any custom forms — across the Enterprise, EDIS, and YourCare systems.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/MEDHOST-FHIR-Extension-Fields.xlsx` (139 KB) | 45-sheet Excel workbook documenting 699 custom FHIR extension fields across 41 entity sheets / 26 FHIR resource types. Includes field names, types, max lengths, descriptions, and internal database table/column mappings. **Primary technical artifact.** | ⭐⭐⭐ Most informative |
| `downloads/interoperability-page.html` (198 KB) | Full HTML of MEDHOST's interoperability page with EHI Export section describing export mechanics (single-patient and system export, FHIR R4 NDJSON format). | ⭐⭐ Key for mechanics |
| `downloads/ehi-export-section.png` (792 KB) | Screenshot of the EHI Export section on the interoperability page. Confirms text content. | ⭐ Confirmatory |
| `downloads/interoperability-page-top.png` (636 KB) | Screenshot of page header. | ⭐ Context only |
| `downloads/enrichment/extension-fields.json` (291 KB) | Prior agent's JSON parse of the XLSX. Used for cross-validation. | ⭐ Reference |
| `downloads/enrichment/extraction-summary.json` (17 KB) | Prior agent's summary statistics. | ⭐ Reference |

No sample export files, FHIR StructureDefinitions, or user guides were found.

## 3. Export Mechanics

- **Format**: FHIR R4 v4.0.1 NDJSON files, delivered as a compressed ZIP archive per patient
- **Mechanism**:
  - *Single patient*: Patient initiates via YourCare® Universe patient portal, or a facility administrator generates on the patient's behalf. Delivered via secure email link.
  - *System export*: Initiated by facility or MEDHOST administrator. Presumably covers multiple/all patients.
- **Single-patient**: Yes (patient portal or admin-on-behalf)
- **Bulk capability**: Yes (system export)
- **Access constraints**: Patient portal export requires facility to use YourCare® Universe. System export requires administrator access.
- **Fees**: Not documented.

Source: EHI Export section of `downloads/interoperability-page.html`

## 4. Export Content: What's In It

The XLSX documents **extension fields only** — additional fields MEDHOST adds beyond standard FHIR R4 resources. It does not document which standard FHIR fields are populated. The XLSX explicitly states: "MEDHOST utilizes the FHIR R4 v 4.0.1 as a guideline for the structure of electronic health information (EHI). In some cases, MEDHOST adds additional fields to some of these resources to accommodate data fields that are captured in MEDHOST but are not defined in the FHIR R4 standard."

This means the actual export contains standard FHIR R4 fields **plus** these 699 extension fields. The total exported field count is therefore the standard FHIR base fields for each resource type plus the documented extensions.

### Key stats (extension fields only)

- **41 entity sheets** (data-bearing sheets, excluding reference/notes sheets)
- **699 extension fields** total
- **694 fields with descriptions** (99.3%)
- **26 unique FHIR resource types** mapped
- All fields include data type and max length
- Internal database table/column mappings provided for Enterprise and EDIS systems (and some for YourCare)

### Vendor's own content organization

The XLSX is organized by FHIR resource type / clinical concept. Each sheet maps to a specific FHIR resource and clinical context:

| Sheet Name | FHIR Resource | Category | Ext. Fields | Described | % |
|---|---|---|---|---|---|
| **Encounter** | Encounter | Clinical | 102 | 102 | 100% |
| **Procedure** | Procedure | Clinical | 103 | 103 | 100% |
| **Ancillary Order** | ServiceRequest | Orders | 65 | 65 | 100% |
| **Patient** | Patient | Demographics | 59 | 59 | 100% |
| **Observation Labs** | Observation | Diagnostics | 44 | 44 | 100% |
| **Implantable Device** | Device | Clinical | 39 | 39 | 100% |
| **Coverage** | Coverage | Insurance | 30 | 30 | 100% |
| **MedicationRequest-InpatientMed** | MedicationRequest | Medications | 25 | 25 | 100% |
| **Immunization** | Immunization | Clinical | 25 | 25 | 100% |
| **Related Person** | RelatedPerson | Demographics | 19 | 19 | 100% |
| **Appointment** | Appointment | Administrative | 17 | 15 | 88% |
| **PC Orders (Service Request)** | ServiceRequest | Orders | 20 | 20 | 100% |
| **Charge Item** | ChargeItem | Billing | 18 | 18 | 100% |
| **Medication Administration** | MedicationAdministration | Medications | 13 | 13 | 100% |
| **Practitioner** | Practitioner | Administrative | 11 | 11 | 100% |
| **Smoking Status** | Observation | Social History | 10 | 10 | 100% |
| **Observation Sexual Behavior** | Observation | Social History | 9 | 9 | 100% |
| **Condition** | Condition | Clinical | 7 | 5 | 71% |
| **Family Member History** | FamilyMemberHistory | Clinical | 7 | 7 | 100% |
| **MedicationStatement-HomeMed** | MedicationStatement | Medications | 7 | 7 | 100% |
| **Consent** | Consent | Administrative | 6 | 6 | 100% |
| **Diagnostic Report** | DiagnosticReport | Diagnostics | 6 | 6 | 100% |
| **MedicationRequest-Discharge Med** | MedicationRequest | Medications | 5 | 5 | 100% |
| **Detected Issue** | DetectedIssue | CDS | 3 | 3 | 100% |
| **Allergy** | AllergyIntolerance | Clinical | 4 | 4 | 100% |
| **Goal** | Goal | Clinical | 4 | 4 | 100% |
| **MDRO** | Observation | Clinical | 4 | 4 | 100% |
| **Observation Alcohol Use** | Observation | Social History | 4 | 4 | 100% |
| **Observation Drug Use** | Observation | Social History | 4 | 4 | 100% |
| **MedicationRequest-Prescriptions** | MedicationRequest | Medications | 4 | 4 | 100% |
| **Discharge Plan (CarePlan)** | CarePlan | Clinical | 3 | 3 | 100% |
| **Location** | Location | Administrative | 3 | 2 | 67% |
| **Past Procedure** | Procedure | Clinical | 3 | 3 | 100% |
| **Problem** | Problem | Clinical | 3 | 3 | 100% |
| **Condition-Past Medical History** | Condition | Clinical | 2 | 2 | 100% |
| **Observation Education** | Observation | Social History | 2 | 2 | 100% |
| **Observation General Comment** | Observation | Clinical | 2 | 2 | 100% |
| **Observation Marital Status** | Observation | Social History | 2 | 2 | 100% |
| **Observation Occupation** | Observation | Social History | 2 | 2 | 100% |
| **Observation Travel** | Observation | Social History | 2 | 2 | 100% |
| **Question Answer** | QuestionnaireResponse | Clinical | 1 | 1 | 100% |

### Category breakdown

| Category | Entities | Extension Fields |
|---|---|---|
| Clinical | 15 | 307 |
| Orders | 2 | 85 |
| Demographics | 2 | 78 |
| Medications | 5 | 54 |
| Diagnostics | 2 | 50 |
| Administrative | 4 | 39 |
| Social History | 8 | 35 |
| Insurance | 1 | 30 |
| Billing | 1 | 18 |
| Clinical Decision Support | 1 | 3 |

Full inventory: `analysis/entity-inventory-full.json` (699 fields with complete metadata)

### Notable extension field examples

The extensions reveal depth beyond USCDI:

- **Patient** (59 extensions): SSN alpha prefix, religion, congregation/parish code, previous patient number, date of last bill, race/ethnicity detail, language detail, multiple birth flag, patient status codes, VIP indicators
- **Encounter** (102 extensions): confidential flag, legal hold flag, medical service codes, nursing station, admit/discharge/transfer detail, attending/referring/admitting physician detail, financial class, accommodation codes, point of origin, discharge disposition, DRG codes, occurrence codes/dates, condition codes, value codes — many of these are administrative/billing-adjacent
- **Procedure** (103 extensions): procedure type, case number, surgeon/assistant details, anesthesia type, anesthesia start/end times, pre/post-op diagnosis, wound classification, ASA class, implant details, tissue tracking, pathology indicators — deep perioperative detail
- **Observation Labs** (44 extensions): child order number, component name, blood bank fields (unit ID, disposition, crossmatch, ABO/Rh), specimen details, micro sensitivity results
- **ChargeItem** (18 extensions): CPT codes for primary/secondary insurance, charge code, revenue code, quantity, charge amount, modifier codes — genuine billing charge data

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

MEDHOST's export covers **26 FHIR resource types** with vendor-specific extensions, organized across clinical, medication, diagnostic, demographic, insurance, billing, and social history domains.

**Strongest areas:**
- **Encounters** (102 extensions): Extremely deep — includes admit/discharge/transfer detail, financial class, DRG, accommodation, condition codes, value codes. This is well beyond USCDI.
- **Procedures** (103 extensions): Comprehensive perioperative data including anesthesia, implants, tissue tracking, wound classification — addresses the product's surgical workflow capabilities.
- **Orders** (85 extensions across 2 sheets): Ancillary orders and patient care orders with detailed status, scheduling, and result fields.
- **Demographics** (78 extensions across Patient + RelatedPerson): Deep patient data including religion, congregation, SSN details, previous numbers.
- **Medications** (54 extensions across 5 sheets): Covers inpatient meds, discharge meds, prescriptions, home meds, and medication administration — full medication lifecycle.

**Thinnest areas:**
- **QuestionnaireResponse** (1 extension): Minimal — despite the product having custom forms capability.
- **Problem** (3 extensions): Minimal beyond standard FHIR.
- **CarePlan** (3 extensions): Only discharge plan context.
- **Goal** (4 extensions): Minimal beyond standard FHIR.

**Key gap — no clinical notes/documents**: The XLSX documents **no DocumentReference, Composition, or Binary resource**. MEDHOST stores extensive clinical documentation (physician notes, nurse charting, discharge summaries, H&P, consult notes, ED notes). If these are exported as standard FHIR DocumentReference resources with no extensions needed, they wouldn't appear in the extension XLSX — but their absence from the documentation makes it impossible to confirm they're included.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | Patient (59 ext fields), RelatedPerson (19 ext fields) | Deep — includes religion, SSN detail, parish, VIP codes |
| Encounters / visits | ✅ Covered | Encounter (102 ext fields) | Very deep — DRG, financial class, condition/value codes |
| Problems / conditions | ✅ Covered | Condition (7 ext), Condition-Past Medical History (2 ext), Problem (3 ext) | Adequate — standard FHIR Condition plus extensions |
| Medications / prescriptions | ✅ Covered | MedicationRequest (3 variants, 34 ext), MedicationAdmin (13 ext), MedicationStatement (7 ext) | Deep — full lifecycle from prescriptions to administration |
| Allergies | ✅ Covered | AllergyIntolerance (4 ext fields) | Adequate — pharmacy review status, allergy type |
| Immunizations | ✅ Covered | Immunization (25 ext fields) | Thorough |
| Vitals | ⚠️ Partial | No dedicated Observation-Vitals sheet; vitals likely in standard FHIR Observation with no extensions needed | Product stores vitals extensively; no explicit documentation |
| Lab results | ✅ Covered | Observation Labs (44 ext), DiagnosticReport (6 ext) | Deep — includes blood bank, micro sensitivity, specimen detail |
| Imaging / diagnostic reports | ⚠️ Partial | DiagnosticReport (6 ext) covers reports; no ImagingStudy or Media resource | Reports covered; actual images unclear |
| Procedures | ✅ Covered | Procedure (103 ext), Past Procedure (3 ext) | Very deep — perioperative, anesthesia, implants, tissue tracking |
| Clinical notes / documents | ⚠️ Partial | No DocumentReference or Composition resource documented | **Significant uncertainty** — product stores extensive notes; could be exported as standard FHIR resources not needing extensions, but not documented |
| Care plans / goals | ✅ Covered | CarePlan (3 ext), Goal (4 ext) | Thin but present |
| Orders / referrals | ✅ Covered | ServiceRequest (85 ext across 2 sheets — Ancillary Order + PC Orders) | Deep |
| Insurance / coverage | ✅ Covered | Coverage (30 ext fields) | Thorough — plan details, subscriber info, group numbers |
| Claims / billing | ⚠️ Partial | ChargeItem (18 ext fields) — CPT codes, charges, revenue codes, modifiers | Charges present but no full claims/payments. Financial module is separately certified. |
| Payments | ❌ Not covered | No payment-related resources | Financial module is a separate product; likely N/A for Clinicals |
| Consents / directives | ✅ Covered | Consent (6 ext fields) | Present |
| Patient communications | ❌ Not covered | No Communication resource | Product has YourCare portal with messaging; gap if portal messages are part of clinical record |
| Specialty-specific (perioperative) | ✅ Covered | Procedure (103 ext) includes anesthesia type/times, wound class, ASA, implants | Addressed via deep Procedure extensions |
| Specialty-specific (ED) | ⚠️ Partial | EDIS database mappings present in many sheets (EDIS column), but no ED-specific resource | ED data mapped into standard resource extensions rather than dedicated resources |

## 6. Documentation Quality

**Strengths:**
- Field-level documentation is thorough: 99.3% of extension fields have descriptions
- Data types and max lengths documented for all fields
- Internal database table/column mappings provide traceability to source system (Enterprise + EDIS)
- FHIR field types specified for all extension fields

**Weaknesses:**
- **Extensions only** — no documentation of which standard FHIR base fields are populated, or which FHIR resource types are included in the export beyond those with extensions
- **No value sets** — coded fields (religion, VIP codes, discharge disposition, etc.) don't list allowed values
- **No sample data** — no example NDJSON files provided
- **No relationships** — no documentation of how resources reference each other beyond what FHIR R4 provides natively
- **No schema artifacts** — no FHIR StructureDefinitions, CapabilityStatement, or ImplementationGuide
- **No user guide** — no step-by-step instructions for requesting or processing an export
- **No file manifest** — no list of which NDJSON files are generated per patient

**Developer usability**: A developer could understand the extension fields, but would need to independently know FHIR R4 base resources to understand the complete export. There's no way to know from this documentation alone whether DocumentReference, Observation (Vitals), or other standard resources without extensions are included.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The export covers a genuinely broad range of clinical domains with impressive depth — 26 FHIR resource types with 699 extension fields going well beyond USCDI. The Encounter (102 extensions), Procedure (103 extensions), and Order (85 extensions) sheets show deep engagement with the product's internal data model. ChargeItem and Coverage extensions demonstrate billing/insurance data inclusion.

However, there are meaningful gaps relative to what the Clinicals product stores:
- **Clinical notes/documents**: No evidence that DocumentReference, the primary resource for clinical narrative, is exported. For an inpatient EHR with extensive physician and nursing documentation, this is a major gap.
- **Patient communications**: No portal messaging data despite YourCare integration.
- **Full billing**: Only charge-level data (ChargeItem), not claims or payments — though this is partially mitigated by billing being a separate certified product.

The documentation is extensions-only, making it impossible to fully assess coverage of domains that use standard FHIR fields without extensions (vitals, basic notes).

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly a purpose-built (b)(10) export, not a repackaged (g)(10):
1. **699 extension fields** — far beyond what any (g)(10) FHIR API would provide
2. **ChargeItem** with CPT codes, revenue codes, and charge amounts — billing data not in USCDI
3. **Internal database mappings** — the XLSX traces each extension to specific Enterprise/EDIS database columns (e.g., `PATHIST.SSNAL`, `RMBED.NURST`, `mrordir.ordstat`), showing systematic mapping from internal schema to FHIR
4. **102 Encounter extensions** including DRG, financial class, condition codes, value codes — administrative/billing data
5. **103 Procedure extensions** with deep perioperative detail (anesthesia, implants, tissue tracking) — specialty data
6. **Multi-system coverage** — extensions map data from Enterprise, EDIS, and YourCare databases

The vendor built a custom FHIR mapping that reaches deep into their internal database across multiple subsystems. This is genuine (b)(10) effort.

### Key Findings

1. **Purpose-built FHIR export with 699 vendor extensions across 26 resource types** — MEDHOST mapped their internal database columns to FHIR R4 resources with extensions, producing NDJSON files. The database column mappings (`analysis/entity-inventory-full.json`) demonstrate direct tracing from internal SQL Server tables to exported FHIR fields. This is substantive (b)(10) work.

2. **Deep clinical and administrative coverage for key domains** — Encounter (102 extensions), Procedure (103 extensions), and Orders (85 extensions) are exceptionally well-mapped, including perioperative data, DRG codes, financial class, and admission detail that go far beyond USCDI.

3. **Clinical notes/documents are a significant blind spot** — No DocumentReference, Composition, or Binary resource is documented in the XLSX. For an inpatient EHR, clinical notes (H&P, discharge summaries, progress notes, nursing assessments, ED notes) are core EHI. It's possible these are exported as standard FHIR resources needing no extensions, but the documentation doesn't confirm this.

4. **Billing coverage is partial but appropriate** — ChargeItem (18 extensions) includes CPT codes, charges, and revenue codes. Full claims/payment data lives in the separately certified Financials product, so the absence of Claim/ExplanationOfBenefit resources from the Clinicals export is architecturally reasonable.

5. **Documentation quality is uneven** — Extension fields are well-documented (99.3% with descriptions, all with types/lengths and database mappings). But the absence of documentation for base FHIR fields, value sets, sample data, and export file manifests leaves significant gaps in developer usability.

### Summary Stats

```
Coverage:        Partial
Approach:        Purpose-built EHI export
Export format:   FHIR R4 NDJSON (ZIP archive)
Entities:        41 sheets / 26 FHIR resource types
Fields:          699 extension fields (base FHIR fields not documented)
Descriptions:    99.3% of extension fields
Sample data:     No
Bulk export:     Yes (system export)
Domains covered: 14 of 18 applicable domains (vitals, notes, communications, payments uncertain or absent)
```

### Bottom Line

MEDHOST built a genuine purpose-built EHI export that maps 699 internal database fields across Enterprise, EDIS, and YourCare systems into FHIR R4 resources with vendor extensions — this is real (b)(10) work. The export is strong on clinical/administrative data (encounters, procedures, orders, medications, labs) but has a concerning documentation gap around clinical notes and documents, which are core to an inpatient EHR's designated record set. A patient would likely get most of their structured clinical data, but it's unclear whether their narrative documentation (the actual doctor and nurse notes) would be included.
