# EHI Export Analysis: ezCaretech Co., Ltd.

**Product**: BESTCare 2.0B
**Analysis date**: 2026-02-15
**CHPL IDs**: 15.04.04.2610.BEST.02.00.1.180423 (CHPL ID 9665)

## 1. Product Context

BESTCare is a comprehensive hospital information system (HIS) developed by ezCaretech Co., Ltd., a South Korean healthcare IT company. Originally co-developed with Seoul National University Bundang Hospital (SNUBH), BESTCare is designed for large hospitals and university tertiary medical centers. The system achieved HIMSS EMRAM Stage 7 at SNUBH in 2010.

In the US market, BESTCare is deployed primarily at Aurora Behavioral Healthcare's 14–16 psychiatric hospitals, operating as a behavioral health-specialized EHR variant. The FHIR capability statement explicitly references this deployment ("ezfhirstation-us-core-usa-aurora").

BESTCare is a comprehensive HIS with the following modules relevant to EHI scope:
- **Clinical**: EMR with 3,000+ templates, CPOE (medications, labs, imaging, procedures), CDSS with drug interaction checking (Medi-Span/Lexicomp), closed-loop medication administration (barcode/RFID), nursing documentation, pharmacy, radiology, clinical pathways
- **Administrative**: Billing, patient services/registration, inpatient services/bed management, social services, CRM
- **Behavioral health variant**: Psychiatry-specific workflows, customizable behavioral health documentation forms
- **Analytics**: Clinical data warehouse (CDW) with daily data extraction, 290 clinical quality indicators
- **Integration**: HIE (HL7 V2.X, CDA), FHIR R4 API (US Core)

The product holds 33 ONC certified criteria — one of the broadest certifications possible — including CPOE (medications, labs, imaging), demographics, family history, implantable devices, transitions of care, EHI export, CDS, CQMs, public health reporting (immunizations, syndromic surveillance, case reporting, cancer registry, antimicrobial reporting, health care surveys), and FHIR API access.

Given this breadth, an adequate (b)(10) export should cover clinical documentation across multiple specialties, medication records (including administration), orders, lab results, imaging, billing/financial records, nursing documentation, and behavioral health-specific assessments.

## 2. Artifacts Reviewed

| Artifact | Description | Informative? |
|---|---|---|
| `b.10_EHI_Export.pdf` (24.8 KB, 1 page) | Primary (b)(10) documentation. Describes CSV and Oracle DMP export formats. Contains ~150 words of substantive content. No data dictionary, schema, field definitions, or export instructions. | **Most informative** for understanding vendor's stated (b)(10) approach, but contains almost no technical detail |
| `BESTCare2.0B_Certified_Health_IT_v3.0.pdf` (139 KB, 3 pages) | Lists 33 certified criteria and 13 CQMs. No technical detail about EHI export. Created June 2025. | Low — confirms certification only |
| `fhir-capability-statement.json` (33 KB) | FHIR R4 CapabilityStatement for "ezfhirstation-us-core-usa-aurora". Documents 26 resource types (20 clinical, 6 infrastructure). Dated 2022-02-16. | Moderate — defines FHIR API scope |
| `single-patient-api.html` (1.8 MB) | Single Patient API Guide from ezFHIRStation portal. Documents 20 US Core FHIR R4 profiles plus 12 vital sign sub-profiles with per-resource read/search details. | Moderate — this is (g)(10) documentation, not (b)(10) |
| `multi-patient-api.html` (87 KB) | Multi Patient API Guide. Documents FHIR Bulk Data Export ($export) with NDJSON output at Patient, Group, and System levels. | Moderate — this is (g)(10) documentation, not (b)(10) |
| `base-urls.html` (42 KB) | Service Base URLs for ezFHIRStation portal. Lists Authorization, Single Patient API, Multi Patient API, Application Access, and Inferno test tool endpoints. | Low — endpoint listing only |
| `screenshot-single-patient-api.png` (257 KB) | Screenshot of Single Patient API Guide page | Low — visual confirmation only |
| `screenshot-multi-patient-api.png` (273 KB) | Screenshot of Multi Patient API Guide page | Low — visual confirmation only |
| `screenshot-onc-disclosures-page.png` (171 KB) | Screenshot of ONC mandatory disclosures page | Low — visual confirmation only |
| RWT Results 2025 (fetched separately, not in downloads) | Real World Testing Results Report. Confirms 128 single-patient EHI exports were initiated, 126 completed (98.4% success rate), average 3.5 minutes. Population-level tested in mirrored environment. | Moderate — confirms the export function works but provides no detail on what data is included |
| Mandatory Disclosures Letter (fetched separately) | States "(b)(10) allows to export electronic health information (EHI)" with standard licensing fee language. No technical detail. | Low — cost structure only |

## 3. Export Mechanics

The (b)(10) PDF describes two export mechanisms:

### Native export (CSV / Oracle DMP)
- **Formats**: CSV (comma-separated values) and Oracle DMP (Oracle binary database dump)
- **Single-patient**: "BESTCare2.0B allows a user to export electronic health information (EHI) for a single patient at any time without developer assistance"
- **Multi-patient**: "BESTCare2.0B can export all the data for a patient population in our standardized format"
- **Mechanism**: The PDF implies a UI-driven export ("without developer assistance") but provides no screenshots, workflow description, or step-by-step instructions
- **Maintenance**: "BESTCare2.0B updates all formats on a quarterly schedule unless otherwise indicated by Oracle"
- **Access constraints**: Standard software license fee, implementation fee, and recurring maintenance fee (per mandatory disclosures)

The RWT 2025 results confirm the export is functional: 128 single-patient exports initiated, 126 completed successfully (98.4%), averaging 3.5 minutes. Population-level exports were tested only in a mirrored environment "due to operational constraints on production bulk exports."

### FHIR API (cross-referenced from the PDF)
The PDF's "Section II: API documentation" links to the ezFHIRStation FHIR developer portal at `portal.ezcaretech.com:30112/baseUrls`. This is the (g)(10) Standardized API documentation — standard FHIR R4 US Core with Bulk Data Export. It is a separate system from the CSV/Oracle DMP export.

## 4. Export Content: What's In It

### The core problem: no documentation of export contents

The primary (b)(10) PDF provides **zero information** about what data is included in the CSV or Oracle DMP export files. Specifically, there is:
- No data dictionary
- No table/entity listing
- No field/column definitions
- No schema documentation
- No sample data or example files
- No description of CSV file structure (how many files, what each contains, column headers)
- No description of the Oracle DMP schema (which tables, relationships, data types)
- No instructions for interpreting the exported data

The entire substantive content of the PDF (excluding generic format definitions of CSV and Oracle DMP) amounts to approximately 150 words. The CSV and Oracle DMP descriptions are generic definitions of what these formats are — not documentation of what BESTCare's export files contain.

### FHIR API coverage (for reference — this is (g)(10), not the native export)

The FHIR CapabilityStatement documents 26 resource types. The 20 clinical resource types with search support are:

| Resource Type | Interactions | Search Parameters |
|---|---|---|
| AllergyIntolerance | read, search | clinical-status, patient |
| CarePlan | read, search | category, date, patient, status |
| CareTeam | read, search | patient, status |
| Condition | read, search | category, clinical-status, code, onset-date, patient |
| Device | read, search | patient, type |
| DiagnosticReport | read, search | category, code, date, patient, status |
| DocumentReference | read, search | _id, category, date, patient, period, type |
| Encounter | read, search | _id, class, date, identifier, patient, status, type |
| Goal | read, search | lifecycle-status, patient, target-date |
| Immunization | read, search | date, patient, status |
| Location | read, search | address, address-city, address-postalcode, address-state, name |
| Medication | read, search | — |
| MedicationRequest | read, search | authoredon, encounter, intent, patient, status |
| Observation | read, search | category, code, date, patient, status |
| Organization | read, search | address, name |
| Patient | read, search | _id, birthdate, family, gender, given, identifier, name |
| Practitioner | read, search | _id, identifier, name |
| PractitionerRole | read, search | practitioner, specialty |
| Procedure | read, search | code, date, patient, status |
| Provenance | read | — |

The Single Patient API Guide documents 20 US Core profiles plus 12 vital sign sub-profiles (blood pressure, body height, body weight, body temperature, heart rate, pediatric BMI for age, pediatric head circumference, pediatric weight for height, pulse oximetry, respiratory rate, and a general vital signs profile).

### Vendor's own content organization

There is no vendor-provided content organization for the native export. The vendor does not list tables, entities, categories, or fields anywhere in the (b)(10) documentation. The only content organization available is the FHIR resource type listing above, which covers the (g)(10) API, not the (b)(10) export.

**No entity/field table can be produced** because the vendor provides no data dictionary.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's documentation provides two layers:

1. **Native export (CSV/Oracle DMP)**: Claims to export EHI for single patients and patient populations. Uses the phrase "all the data for a patient population" for multi-patient export. **However, there is zero documentation of what "all the data" includes.** An Oracle DMP could theoretically contain the entire database, but the vendor provides no confirmation or documentation of scope.

2. **FHIR API**: Standard US Core clinical data — 20 resource types covering demographics, conditions, medications, allergies, labs, vital signs, immunizations, encounters, procedures, care plans, goals, implantable devices, clinical notes, and provenance. This is a well-defined but narrow subset (~20% of what a comprehensive HIS like BESTCare stores).

The vendor provides no categories, modules, or groupings for the native export content. The FHIR API covers standard clinical domains but explicitly excludes billing, orders (non-medication), pharmacy administration, nursing documentation, behavioral health-specific content, and all administrative data.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | FHIR Patient resource; native export undocumented | FHIR covers US Core demographics. Native export may include more but is undocumented. Product stores extensive registration data. |
| Encounters / visits | ⚠️ Partial | FHIR Encounter resource; native export undocumented | FHIR Encounter is limited. Product manages full inpatient/outpatient encounters. |
| Problems / conditions / diagnoses | ⚠️ Partial | FHIR Condition resource; native export undocumented | FHIR covers basic problem list. Product has CPOE and clinical pathways with richer diagnostic data. |
| Medications / prescriptions | ⚠️ Partial | FHIR MedicationRequest, Medication resources; native export undocumented | FHIR covers prescriptions. Product has closed-loop medication administration (CLMA), pharmacy dispensing — these are not in FHIR. |
| Allergies | ⚠️ Partial | FHIR AllergyIntolerance resource; native export undocumented | FHIR covers standard allergy data. Product integrates Medi-Span/Lexicomp for drug interaction checking. |
| Immunizations | ⚠️ Partial | FHIR Immunization resource; native export undocumented | FHIR covers standard immunization data. Product is certified for immunization registry reporting. |
| Vitals | ⚠️ Partial | FHIR Observation (12 vital sign profiles); native export undocumented | FHIR covers standard vitals. |
| Lab results | ⚠️ Partial | FHIR DiagnosticReport, Observation resources; native export undocumented | FHIR covers basic lab results. Product has comprehensive CPOE for lab orders. |
| Imaging / diagnostic reports | ⚠️ Partial | FHIR DiagnosticReport for reports/notes; native export undocumented | FHIR covers report text. Product has full radiology module with imaging workflow. |
| Procedures | ⚠️ Partial | FHIR Procedure resource; native export undocumented | Basic procedure records via FHIR. Product manages comprehensive procedural ordering via CPOE. |
| Clinical notes / documents | ⚠️ Partial | FHIR DocumentReference resource; native export undocumented | FHIR supports document references. Product has 3,000+ clinical templates, extensive EMR documentation. |
| Care plans / goals | ⚠️ Partial | FHIR CarePlan, CareTeam, Goal resources; native export undocumented | FHIR covers basic care plan data. Product has 104+ clinical pathways with variance tracking. |
| Orders / referrals | ❌ Not covered | Not in FHIR API; native export undocumented | Product has comprehensive CPOE (medications, labs, imaging, procedures). Only medication orders appear in FHIR. Significant gap if native export doesn't include these. |
| Insurance / coverage | ❌ Not covered | Not in FHIR API; native export undocumented | Product stores insurance/enrollment data. No evidence in any documented export. |
| Claims / billing | ❌ Not covered | Not in FHIR API; native export undocumented | Product has billing module. No evidence in any documented export. |
| Payments | ❌ Not covered | Not in FHIR API; native export undocumented | Product has financial systems. No evidence in any documented export. |
| Consents / directives | ❌ Not covered | Not in FHIR API; native export undocumented | Product supports electronic consent (iPad/PC signature). No evidence in any documented export. |
| Patient communications / portal messages | ❌ Not covered | Not in FHIR API; native export undocumented | Product is certified for patient access. No evidence of portal message export. |
| Specialty-specific (behavioral health) | ❌ Not covered | Not in FHIR API; native export undocumented | Product is deployed at 14 psychiatric hospitals with behavioral health-specific workflows and forms. No evidence of psychiatric assessment export. **This is a significant gap given the US deployment context.** |

**Key assessment caveat**: The native CSV/Oracle DMP export *may* cover many or all of these domains. The problem is that the documentation provides zero evidence either way. All domains are marked based on what can be verified from the available documentation. The "Partial" ratings for clinical domains reflect that the FHIR API provides some coverage but cannot be confirmed as the full (b)(10) export mechanism, and the native export is completely undocumented.

## 6. Documentation Quality

The (b)(10) export documentation quality is **extremely poor**:

- **Data dictionary**: None. Zero tables, entities, fields, or columns are documented.
- **Schema**: None. No machine-readable schema for either CSV or Oracle DMP format.
- **Sample data**: None. No example export files or sample records.
- **Export instructions**: None. No screenshots, workflow description, or step-by-step guide for initiating an export.
- **File structure**: Not described. It is unknown whether the CSV export produces one file or many, what column headers look like, or how relationships between records are expressed.
- **Oracle DMP interpretation**: Not addressed. Oracle DMP is a proprietary binary format requiring Oracle database tools to import. No guidance is provided on how a third party would interpret the dump.
- **Value sets / code systems**: None documented for the native export. The FHIR API uses standard US Core value sets.
- **Relationships**: Not documented. No foreign keys, entity relationships, or data model diagrams.

**Could a developer build an import from this documentation?** No. A developer receiving the (b)(10) PDF would know only that the export files are CSV and Oracle DMP. They would have no knowledge of:
- What data is in the files
- How files are structured or named
- What columns/tables exist
- How to relate records across files/tables
- What codes or identifiers are used

The FHIR API portal (ezFHIRStation) is adequately documented for its purpose as a (g)(10) Standardized API, with per-resource read/search documentation, parameter tables, and response field descriptions. However, this is not (b)(10) documentation — it documents a different regulatory requirement and covers only the US Core clinical subset.

## 7. Overall Assessment

### Classification

**Minimal/stub**

The (b)(10) documentation is a single page with ~150 words of substantive content. It names two export formats (CSV and Oracle DMP) but provides no data dictionary, no schema, no field definitions, no sample data, and no export instructions. The FHIR API documentation linked from the PDF is (g)(10) documentation being cross-referenced, not genuine (b)(10) documentation.

While the underlying export mechanism (CSV + Oracle DMP) *could* be comprehensive — an Oracle database dump is one of the most complete export formats possible — the documentation provides no evidence of what is actually exported. The RWT 2025 results confirm the export function works (128 single-patient exports, 98.4% success rate) but still provide no detail on export contents, stating only that "export files were complete and usable."

### Key Findings

1. **The (b)(10) PDF is essentially empty.** At 1 page and ~150 words of content, it is among the most minimal (b)(10) documentation possible. It defines what CSV and Oracle DMP formats are (generic definitions) but says nothing about what BESTCare exports. (Source: `b.10_EHI_Export.pdf`)

2. **The FHIR API is (g)(10), not (b)(10).** The PDF's "Click Here" link leads to the ezFHIRStation FHIR developer portal, which documents the (g)(10) Standardized API with 26 US Core resource types. This is a textbook case of (g)(10)/(b)(10) conflation. The FHIR API covers only standard clinical data. (Source: `fhir-capability-statement.json`, `single-patient-api.html`, `multi-patient-api.html`)

3. **No data dictionary exists anywhere in the documentation.** Across all 9 artifacts reviewed (PDFs, HTML pages, JSON, screenshots) and supplementary materials (RWT results, mandatory disclosures), there is zero documentation of tables, fields, columns, schemas, or data models for the native export. (Source: comprehensive artifact review)

4. **The Oracle DMP format raises portability concerns.** Oracle DMP is a proprietary binary format that requires Oracle database tools to import. Without schema documentation, a recipient would need to reverse-engineer the database structure. This undermines the practical usability of the export even if the data coverage is comprehensive. (Source: `b.10_EHI_Export.pdf`)

5. **Behavioral health-specific data is unaddressed.** BESTCare is deployed at 14 US psychiatric hospitals (Aurora Behavioral Healthcare) with psychiatry-specific workflows and customizable forms. None of the documentation — not the native export PDF, not the FHIR API — mentions psychiatric assessments, behavioral health forms, or specialty-specific data structures. (Source: `product-research.md`, `fhir-capability-statement.json` naming "usa-aurora")

### Summary Stats

```
Classification:  Minimal/stub
Export format:   CSV, Oracle DMP (native); FHIR R4 NDJSON (API — cross-referenced, not (b)(10))
Model type:      Unknown — native export is undocumented; FHIR API is standard projection
Entities:        0 documented (native export); 20 clinical resource types (FHIR API)
Fields:          0 documented (native export); N/A (FHIR API uses US Core profiles)
Descriptions:    N/A (no data dictionary)
Sample data:     No
Bulk export:     Yes (native multi-patient described; FHIR Bulk Data Export documented)
Domains covered: 0 of 15 verifiable (native export undocumented); ~10 of 15 partially via FHIR API
```

### Bottom Line

A patient or provider receiving this export would get either CSV files or an Oracle database dump with no documentation to interpret the contents. The (b)(10) documentation is a single page that says nothing about what data is exported, making it impossible to assess whether the export is complete. The vendor's FHIR API covers ~20 standard clinical resource types but omits billing, orders, behavioral health-specific data, and administrative records — and it is a separate (g)(10) system being cross-referenced, not the actual (b)(10) export. The single biggest gap is the **complete absence of a data dictionary** — without one, even a technically comprehensive database dump is unusable to a third party.
