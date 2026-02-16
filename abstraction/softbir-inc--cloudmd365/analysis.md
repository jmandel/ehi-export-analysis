# EHI Export Analysis: Softbir, Inc.

**Product**: CloudMD365
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.3067.Clou.01.00.1.200122

## 1. Product Context

CloudMD365 is an ONC-certified EHR product from Softbir, Inc., a small (~20-employee) healthcare software company in Indianapolis, IN. The product name now redirects to "DocIndy" (docindy.com) and appears closely related to the "iVisitDoc" EMR platform (ivisitdoc.com).

Based on product research, CloudMD365/iVisitDoc is **primarily a behavioral health and telehealth-oriented EHR** with the following capabilities relevant to EHI scope:

- **Clinical documentation**: Progress notes (SOAP/DAP formats), therapy session notes, assessment forms, outcome measures, treatment plans with ICD-10 and DSM-5 coding
- **Behavioral health specialty**: Pre-admission workflows, patient occupancy tracking across locations, utilization review, rounds/security checks, homework planners, aftercare management, discharge planning
- **Medication management**: eMAR (eMARneek module) with barcode scanning, medication lists, e-prescribing
- **Lab integration**: CPOE for labs with 90+ testing partners (certified for (a)(1) lab CPOE)
- **Diagnostic imaging**: Certified for CPOE diagnostic imaging (a)(1)
- **Care coordination**: Appointment calendar, utilization review, care plans (certified for (b)(11))
- **Billing**: Integrated billing including CCM/TCM Medicare billing codes (99490, 99487, 99489)
- **Telehealth**: Video and messaging-based consultations, dermatology image consultations
- **Communication**: HIPAA-compliant messaging, patient surveys, electronic signatures
- **RPM**: Remote patient monitoring for chronic conditions

This sets a high bar for export completeness — the product manages clinical, behavioral health specialty, medication administration, billing, telehealth, and communication data.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `CloudMD365-EHI-Export-Documentation.pdf` (157 KB, 7 pages) | The sole EHI export documentation artifact. A Google Docs-generated PDF containing: introduction, file format description, extraction process steps, and a data dictionary covering 6 entities + 2 sub-objects with 41 total fields. | **Primary and only source** — all export assessment derives from this single document. |

Only one artifact was collected. There are no sample data files, no machine-readable schemas, no supplementary HTML pages, and no additional documentation beyond this 7-page PDF.

## 3. Export Mechanics

- **Format**: Custom JSON (proprietary structure, not FHIR or C-CDA despite the document's claim of adherence to "HL7 FHIR")
- **Mechanism**: Admin UI — navigate to Admin > Export Patient Health Data, select patients, set date range, click Export, download file
- **Single-patient vs bulk**: Patient-selection based — admin selects specific patients for export. Date range filter applies to encounters. Not a full bulk export mechanism.
- **Access constraints**: Requires authorized credentials with admin-level access permissions
- **Fees**: Not mentioned in documentation

The document states the EHI file "adheres to standards like HL7 FHIR to ensure interoperability." However, the sample JSON and field definitions use a completely custom/proprietary structure with no FHIR resource types, no FHIR references, and no standard coding system bindings beyond ICD-10. The FHIR claim is boilerplate, not descriptive of the actual format.

## 4. Export Content: What's In It

The PDF documents **6 top-level entities and 2 sub-objects** with a total of **41 fields**. Every field has a name, data type, and short description. No value sets, foreign keys, nullability constraints, or sample data are provided.

### Vendor's own content organization

The vendor organizes data into 6 sections plus 2 reusable sub-objects:

| Entity/Table | Fields | Described | Types | Category (vendor's) |
|---|---|---|---|---|
| Patient Demographics | 7 | 7 | yes | Patient Demographics |
| Address (sub-object) | 6 | 6 | yes | Patient Demographics |
| Health Summary | 3 | 3 | yes | Health Summary |
| Problem (sub-object) | 2 | 2 | yes | Health Summary / Encounters |
| Medications | 5 | 5 | yes | Medications |
| Allergy | 3 | 3 | yes | Allergies |
| Encounter | 10 | 10 | yes | Encounters |
| RPM Data | 5 | 5 | yes | RPM Data |
| **Total** | **41** | **41** | **yes** | — |

**Field-level detail is minimal but consistent**: every field has a name, a data type (String, GUID, DateTime, Float, Object, Array of X), and a one-sentence description. No field has a value set definition (e.g., what values `gender` can take), no foreign key relationships are documented (e.g., encounter → patient link), and no cardinality or nullability information is provided.

**Notable structural issues**:
- The `medication` field is typed as "Array of Object" but the sub-fields (`dosage`, `frequency`, `start_date`, `end_date`) are listed flat alongside it, creating ambiguity about whether they are properties of the medication object or siblings.
- No explicit relationship connects encounters to patients (the export appears to be patient-scoped, so the relationship is implicit).
- The `Problem` sub-object is reused across Health Summary and Encounters, which is the only cross-entity structure documented.

**Sample JSON**: A minimal 8-line fragment showing a patient object with `id`, `name` (first/last), `dob`, and `gender`. This does not illustrate the full export structure (e.g., no encounters, medications, or nested arrays are shown).

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export covers 6 clinical data categories:

1. **Patient Demographics** (13 fields including address sub-object): Name, DOB, gender, address, phone numbers, email. Missing: race, ethnicity, language, marital status, emergency contacts, insurance information.

2. **Health Summary** (5 fields including Problem sub-object): Chronic conditions and diagnoses with ICD-10 codes, family history as string array. Missing: surgical history, social history.

3. **Medications** (5 fields): Medication name, dosage, frequency, start/end dates. Missing: prescriber, pharmacy, NDC/RxNorm codes, route, status, refill information.

4. **Allergies** (3 fields): Allergy name, type, reaction. Missing: severity, onset date, status, verification status.

5. **Encounters** (10 fields): The richest entity — date, chief complaint, diagnosis with ICD-10, treatment summary, care plan goals/actions/follow-up, provider ID/name, notes. Missing: encounter type (in-person vs telehealth), visit duration, facility, billing codes, structured vitals.

6. **RPM Data** (5 fields): Recording time, data type, attribute type, value, unit. This is a product-specific addition reflecting the RPM capability.

The export is essentially a **clinical summary** — roughly equivalent to the data in a C-CDA CCD, but in a proprietary JSON format without standard terminology bindings.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | `Patient Demographics` (7 fields) + `Address` (6 fields) — name, DOB, gender, address, phone, email | Missing race, ethnicity, language, marital status, emergency contacts |
| Encounters / visits | ⚠️ Partial | `Encounter` (10 fields) — date, complaint, diagnosis, treatment, care plan, provider, notes | No encounter type, no structured vitals, no visit duration |
| Problems / conditions / diagnoses | ✅ Covered | `Health Summary` chronic_conditions + diagnosis fields, both as `Array of Problem` with ICD-10 codes; also `Encounter.diagnosis` | Reasonable for a summary |
| Medications / prescriptions | ⚠️ Partial | `Medications` (5 fields) — name, dosage, frequency, dates | Missing prescriber, pharmacy, NDC/RxNorm, route, status |
| Allergies | ⚠️ Partial | `Allergy` (3 fields) — name, type, reaction | Missing severity, onset, status |
| Immunizations | ❌ Not covered | No immunization entity | Product likely stores immunization data via clinical workflows; gap |
| Vitals | ⚠️ Partial | RPM Data captures remote monitoring vitals (BP, glucose, HR) | In-clinic vitals not separately documented; RPM-only |
| Lab results | ❌ Not covered | No lab results entity | Product is certified for lab CPOE (a)(1) and has lab interface with 90+ partners; **significant gap** |
| Imaging / diagnostic reports | ❌ Not covered | No imaging entity | Product is certified for diagnostic imaging CPOE (a)(1); gap |
| Procedures | ❌ Not covered | No procedures entity | Unclear how much procedure data the product stores |
| Clinical notes / documents | ⚠️ Partial | `Encounter.notes` (single String field) | Product supports SOAP/DAP therapy notes, progress notes, assessments — none of this structured note content is exported as distinct entities |
| Care plans / goals | ⚠️ Partial | `Encounter.care_plan_goals`, `care_plan_actions`, `care_plan_followup` | Embedded in encounters rather than standalone; product is certified for care plans (b)(11) |
| Orders / referrals | ❌ Not covered | No orders entity | Product supports CPOE for meds, labs, imaging (a)(1); gap |
| Insurance / coverage | ❌ Not covered | No insurance entity | Product does benefits verification and billing; **significant gap** |
| Claims / billing | ❌ Not covered | No billing entities | Product has integrated billing and CCM/TCM Medicare billing; **significant gap** |
| Payments | ❌ Not covered | No payment entities | Product does billing; gap |
| Consents / directives | ❌ Not covered | No consent entities | Product captures electronic signatures (patient/guardian); gap |
| Patient communications / portal messages | ❌ Not covered | No messaging entities | Product has HIPAA-compliant messaging and telehealth; gap |
| Specialty: behavioral health | ❌ Not covered | No behavioral health-specific entities | Product's **core specialty** — therapy notes (SOAP/DAP), DSM-5 coding, treatment plans, assessments, outcome measures, homework planners, utilization review, pre-admission workflows, rounds/security checks. **None** of this appears in the export. **Most significant gap.** |
| Specialty: eMAR (medication administration) | ❌ Not covered | No eMAR entities | eMARneek module tracks medication administration with barcode verification; gap |

**Summary**: 1 domain covered, 6 partial, 11 not covered out of 18 applicable domains.

## 6. Documentation Quality

**Clarity**: The documentation is clearly written and well-formatted. The 5-step extraction process is straightforward. Field definitions are consistent in structure (name, type, description).

**Completeness**: Very thin. At 7 pages and 41 fields, this is among the smallest EHI data dictionaries possible for a certified EHR. Key gaps:
- No value set definitions for any coded field (e.g., valid values for `gender`, `type` of allergy, `data_type` for RPM)
- No relationship documentation (how entities relate to each other or to patients)
- No nullability or cardinality information
- Only one JSON sample showing 4 demographic fields — no complete patient export example
- No machine-readable schema (JSON Schema, OpenAPI)
- No error handling or edge case documentation
- Misleading FHIR claim — the format is not FHIR in any way

**Usability**: A developer could build a basic parser from this documentation but would face significant ambiguity around nested structures (especially the `medication` field), coded value interpretation, and missing data handling. The documentation is insufficient for reliable import without access to sample exports or the vendor.

## 7. Overall Assessment

### Classification

**Minimal/stub**

The export documents 41 fields across 6 entities in a 7-page PDF. This covers a basic clinical summary (demographics, conditions, medications, allergies, encounters, RPM vitals) while omitting the vast majority of data the product stores: behavioral health specialty data (the product's core domain), lab results, imaging, billing, eMAR records, clinical documents, communications, orders, insurance, and consents. The export is a compliance checkbox, not a genuine attempt at comprehensive EHI export.

### Key Findings

1. **The product's core specialty data is entirely absent from the export.** CloudMD365/iVisitDoc is primarily a behavioral health EHR with therapy notes (SOAP/DAP), DSM-5 coding, assessments, treatment plans, outcome measures, homework planners, and utilization review. None of these appear in the export's 6 entities.

2. **Only 41 fields across 6 entities (+ 2 sub-objects) are documented** — one of the thinnest EHI data dictionaries in the CHPL ecosystem. For context, the product is certified for CPOE (medications, labs, imaging), care plans, and has modules for eMAR, billing, and telehealth messaging.

3. **Lab results are not exported despite active lab certification.** The product is certified for lab CPOE (a)(1) with a lab interface supporting 90+ testing partners, yet there is no lab results entity in the export.

4. **Billing data is completely absent.** The product has integrated billing including CCM/TCM Medicare billing, yet no charges, claims, payments, or billing codes appear in the export.

5. **The FHIR claim is inaccurate.** The document states adherence to "HL7 FHIR" but the actual export is a custom JSON format with no FHIR resource types, references, or standard terminology bindings beyond ICD-10.

### Summary Stats

```
Classification:  Minimal/stub
Export format:   Custom JSON (proprietary)
Model type:      Custom projection (not native database, not standard)
Entities:        6 top-level + 2 sub-objects (8 total)
Fields:          41
Descriptions:    100% (41/41 fields have descriptions)
Sample data:     Minimal (4-field JSON fragment only)
Bulk export:     No (patient-selection based with date range filter)
Domains covered: 1 of 18 applicable domains fully covered; 6 partial
```

### Bottom Line

This is a minimal compliance artifact. A patient or provider would receive a basic clinical summary — name, conditions, medications, allergies, encounter notes, and RPM vitals — but would miss the majority of their health information, including all behavioral health specialty data (the product's primary domain), lab results, billing records, medication administration history, clinical documents, and communications. The single biggest gap is the complete absence of behavioral health-specific data from a product whose core value proposition is behavioral health workflows.
