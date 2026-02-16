# EHI Export Analysis: Softbir, Inc.

**Product**: CloudMD365
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.3067.Clou.01.00.1.200122

## 1. Product Context

CloudMD365 is a cloud-based EHR developed by Softbir, Inc. (~20 employees, ~$1.8M revenue), a small Indianapolis-based company. The product has been rebranded/merged into the DocIndy/iVisitDoc ecosystem. Based on the iVisitDoc EMR tour and trademark filings, CloudMD365 is described as software for CCM/TCM, DSMT, RPM, eMAR, EHR, and telemedicine.

The product has a strong **behavioral health orientation**: therapy session notes (SOAP/DAP formats), DSM-5 coding, treatment plans, pre-admission workflows, patient occupancy tracking, utilization review, rounds/security checks, homework planners, and aftercare management. It also includes:

- **Medication management** with eMARneek (eMAR module with barcode verification)
- **Lab interface** with 90+ testing partners
- **Electronic prescribing** (eRx)
- **Telehealth** (video and messaging consultations)
- **Billing** (integrated, including CCM/TCM Medicare codes 99490, 99487, 99489)
- **Patient communications** (HIPAA-compliant messaging)
- **Care coordination** (appointment calendar, utilization review, discharge planning)

The certified criteria include (a)(1)–(a)(5) for core clinical CPOE, (b)(10) for EHI export, (b)(11) for care plans, and (g)(10) for standardized FHIR API. Notably absent: (b)(1)–(b)(3) transitions of care, (e)(1) patient portal, (f)(1)–(f)(7) public health reporting — indicating a limited clinical certification scope.

For (b)(10) assessment, the product's data domains include: demographics, problem lists, medications, allergies, encounters, RPM vitals, behavioral health assessments, therapy notes, treatment plans, medication administration records, lab results, billing, insurance/benefits verification, care coordination records, telehealth visit records, and patient communications.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/CloudMD365-EHI-Export-Documentation.pdf` | 7-page PDF (157 KB). The sole EHI export documentation artifact. Contains introduction, file format description, 5-step extraction process, and data dictionary covering 6 main entities with 41 fields (including sub-objects). Produced by Google Docs (Skia/PDF m132). | **Primary source** — this is the only artifact and contains all available information about the export. |

No additional artifacts were found: no sample export files, no machine-readable schemas, no supplementary documentation, no links to additional resources within the PDF.

## 3. Export Mechanics

- **Format**: Custom JSON (proprietary structure, not FHIR despite a claim of "HL7 FHIR" adherence)
- **Mechanism**: Admin UI — Admin > Export Patient Health Data
- **Patient selection**: Select specific patients; date range filter for encounters
- **Single-patient vs bulk**: Appears to support selecting multiple patients, but unclear if this produces one file or multiple
- **Access constraints**: Requires authorized credentials with "necessary permissions to access patient data"
- **Fees**: None mentioned
- **Output**: Downloadable file to local machine or designated storage

The extraction process is a simple 5-step workflow: log in → navigate to Admin > Export → select patients → set date range → click Export → download file.

## 4. Export Content: What's In It

The export documentation defines **8 entities (6 main + 2 sub-objects) with 41 total fields**. Every field has a name, data type, and short description. No value sets, foreign keys, cardinality constraints, or machine-readable schemas are provided.

### Data dictionary statistics (from `analysis/entity-inventory-summary.json`)

- Entities: 8 total (6 main entities, 2 sub-objects)
- Fields: 41 total
- Fields with descriptions: 41 (100%)
- Fields with types: 41 (100%)
- Value sets documented: 0
- Foreign keys documented: 0
- Sample data: Demographics fragment only (4 fields in a JSON snippet)
- Machine-readable schema: No

### Vendor's own content organization

| Entity/Table | Fields | Described | Types | Category |
|---|---|---|---|---|
| Patient Demographics | 7 | 7 | yes | Demographics |
| Address (sub-object) | 6 | 6 | yes | Demographics |
| Health Summary | 3 | 3 | yes | Clinical |
| Problem (sub-object) | 2 | 2 | yes | Clinical |
| Medications | 5 | 5 | yes | Clinical |
| Allergies | 3 | 3 | yes | Clinical |
| Encounters | 10 | 10 | yes | Clinical |
| RPM Data | 5 | 5 | yes | Remote Monitoring |
| **Total** | **41** | **41** | **all** | |

### Category breakdown

| Category | Entities | Fields |
|---|---|---|
| Demographics | 2 | 13 |
| Clinical | 5 | 23 |
| Remote Monitoring | 1 | 5 |

### Notable observations

- The **Encounters** entity is the most detailed (10 fields) and embeds care plan data (goals, actions, follow-up) directly rather than as a separate entity.
- **Medications** has an ambiguous structure: `medication` is typed as "Array of Object" but the description says "Name of the Medication" — unclear whether dosage/frequency/dates are properties of each medication object or separate top-level fields.
- **Health Summary** uses a `Problem` sub-object for diagnoses with ICD-10 codes, but `family_history` is just "Array of String" — no structured coding.
- **Demographics** is missing race, ethnicity, language, marital status, and emergency contacts.
- **Allergies** is missing severity, onset date, and status.
- **Medications** is missing prescriber, pharmacy, NDC/RxNorm codes, route, and status.
- The JSON sample shows only 4 fields (id, name, dob, gender) — not a complete export example.
- The claim of "HL7 FHIR" adherence is contradicted by the actual format: it's a custom JSON with no FHIR resource types, no FHIR references, and no standard terminology bindings beyond ICD-10.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor organizes the export into three implicit categories:

1. **Demographics** (13 fields across 2 entities): Basic patient identification — name, DOB, gender, address, phone numbers, email. Thin but functional for identification purposes.

2. **Clinical** (23 fields across 5 entities): Problem list with ICD-10 coding, medication list with dosage/dates, allergy list with type/reaction, encounter records with diagnosis/treatment/care plan/provider/notes, and family history as unstructured strings. This is roughly equivalent to what a basic C-CDA CCD would contain.

3. **Remote Monitoring** (5 fields, 1 entity): RPM device data with timestamped readings (blood pressure, glucose, heart rate, etc.). This is the one product-specific addition that goes beyond a generic clinical summary.

The clinical section is the most substantial but provides only high-level summaries. Encounters embed care plan data inline rather than as structured, linkable entities. There are no relationships between entities (e.g., which encounter prescribed which medication).

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | `Patient Demographics` (7 fields) + `Address` (6 fields) = 13 fields. Missing race, ethnicity, language, marital status, emergency contacts. | Product certified for (a)(2) demographics; export covers basics but omits several standard demographic elements. |
| Encounters / visits | ⚠️ Partial | `Encounters` (10 fields) — date, complaint, diagnosis, treatment, care plan, provider, notes. | Captures visit summaries but no visit type (in-person vs telehealth), no duration, no facility/location. Product supports telehealth visits; telehealth metadata not distinguished. |
| Problems / conditions | ✅ Covered | `Health Summary` — `chronic_conditions` and `diagnosis` as arrays of Problem objects with ICD-10 codes. | Reasonable for problem list. Missing onset dates, status, severity. |
| Medications / prescriptions | ⚠️ Partial | `Medications` (5 fields) — name, dosage, frequency, start/end dates. | Missing prescriber, pharmacy, NDC/RxNorm, route, status. No distinction between active/historical. |
| Allergies | ⚠️ Partial | `Allergies` (3 fields) — name, type, reaction. | Missing severity, onset, status, verification. |
| Immunizations | ❌ Not covered | No immunization data in export. | Product's immunization capability is unclear (not certified for public health reporting). Likely N/A for this behavioral-health-focused product. |
| Vitals | ⚠️ Partial | `RPM Data` (5 fields) covers remote monitoring vitals. | RPM data is included but in-clinic vitals (if collected during encounters) are not separately structured. |
| Lab results | ❌ Not covered | No lab results entity in export. | Product has lab interface with 90+ partners and is certified for CPOE labs (a)(1). **Significant gap** — lab results are EHI. |
| Imaging / diagnostic reports | ❌ Not covered | No imaging data in export. | Product certified for CPOE diagnostic imaging (a)(1). Gap, though imaging may be limited in a behavioral health product. |
| Procedures | ❌ Not covered | No procedures entity. | May be captured in encounter notes as free text, but no structured procedure data. |
| Clinical notes / documents | ⚠️ Partial | `Encounters.notes` is a single String field per encounter. | Product has extensive note capabilities (SOAP, DAP formats, progress notes, therapy session notes). Export reduces all notes to a single string field per encounter — **major gap** for a behavioral health product where therapy notes are core clinical data. |
| Care plans / goals | ⚠️ Partial | Embedded in `Encounters` as `care_plan_goals`, `care_plan_actions`, `care_plan_followup`. | Product certified for (b)(11) care plans. Care plan data is embedded in encounters rather than standalone. May lose care plan history/versioning. |
| Orders / referrals | ❌ Not covered | No orders entity. | Product has CPOE for medications, labs, imaging. Order data not exported. |
| Insurance / coverage | ❌ Not covered | No insurance data in export. | Product has benefits verification feature. **Gap** — insurance information is EHI. |
| Claims / billing | ❌ Not covered | No billing data in export. | Product has integrated billing including CCM/TCM Medicare codes. **Significant gap** — billing records are EHI. |
| Payments | ❌ Not covered | No payment data. | Unknown billing depth; gap if product stores payment records. |
| Consents / directives | ❌ Not covered | No consent data. | Product captures electronic signatures (patient and guardian). Gap. |
| Patient communications | ❌ Not covered | No messaging or telehealth communication data. | Product has HIPAA-compliant messaging and telehealth. **Gap** — patient communications used in care decisions are EHI. |
| Specialty-specific (Behavioral Health) | ❌ Not covered | No behavioral health-specific entities (therapy session notes, DSM-5 coding, treatment plans, assessments, outcome measures, homework, utilization review). | **Critical gap** — this is the product's core specialty. Behavioral health assessments, treatment plans, session notes in SOAP/DAP format, homework planners, and outcome measures are all part of the designated record set. None appear in the export. |
| Medication Administration (eMAR) | ❌ Not covered | No eMAR data. Export only has prescribed medications, not administration records. | Product has eMARneek module with barcode verification. **Gap** — MAR data is EHI. |

**Summary**: Of ~19 applicable domains, 1 is covered (problems), 6 are partially covered, 11 are not covered, and 1 is likely N/A (immunizations). The export misses the product's core behavioral health specialty data entirely.

## 6. Documentation Quality

**Clarity**: The documentation is well-organized and readable. Tables with field name, data type, and description are consistent across all entities. The 5-step extraction process is clear.

**Completeness**: Very thin. 41 fields across 8 entities in a 7-page PDF. No value sets, no relationship documentation, no error handling, no versioning, no edge cases.

**Accuracy**: The claim of "HL7 FHIR" adherence is misleading — the export is a custom JSON format with no FHIR structure. Only ICD-10 is used as a standard terminology; no SNOMED, LOINC, or RxNorm.

**Machine-readability**: None. No JSON Schema, no OpenAPI spec, no sample export file (only a 4-field fragment). A developer could implement a basic parser but would face ambiguities around nested structures (especially the `medication` field) and coded value interpretation.

**Usability**: A developer could build a basic import from this documentation but would need to guess at value sets, handle the ambiguous medication array structure, and accept that 11+ data domains present in the product are not represented.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub**

The export covers 41 fields across 8 entities — roughly equivalent to a basic clinical summary (demographics, problems, medications, allergies, encounters) plus RPM data. The product stores significantly more: behavioral health specialty data (therapy notes, assessments, treatment plans, DSM-5 coding, outcome measures), medication administration records, lab results, billing, insurance, orders, patient communications, and electronic signatures. The export omits the product's **core differentiator** — its behavioral health functionality — entirely. The RPM Data entity is the only product-specific element that goes beyond what a generic C-CDA CCD would contain.

**Axis 2 — Export approach: Purpose-built EHI export**

Despite its thin coverage, this is technically a purpose-built export mechanism: it uses a custom JSON format (not FHIR, not C-CDA), has its own admin UI pathway (Admin > Export Patient Health Data), and includes RPM Data which is not part of any standard clinical exchange format. It is not a repackaging of the (g)(10) FHIR API or C-CDA exchange. However, the breadth of what it actually exports is comparable to what a USCDI summary would contain, making the "purpose-built" classification somewhat hollow — it's a purpose-built mechanism that exports roughly USCDI-scope data.

### Key Findings

1. **The export misses the product's core specialty data entirely.** CloudMD365/iVisitDoc is primarily a behavioral health EHR, but the export contains zero behavioral health-specific entities — no therapy session notes, no DSM-5 coding structure, no treatment plans, no assessments, no outcome measures, no homework planners. This is the single most significant gap.

2. **Only 41 fields across 8 entities.** This is one of the thinnest data dictionaries in the CHPL ecosystem. For context, the product likely stores hundreds of fields internally given its feature breadth (eMAR, billing, lab interface, care coordination, telehealth).

3. **No lab results despite lab integration.** The product has a lab interface with 90+ testing partners and is certified for CPOE labs, but the export contains no lab results entity.

4. **No billing data despite billing capabilities.** The product has integrated billing including CCM/TCM Medicare billing codes, but the export contains no billing, claims, or payment data.

5. **The FHIR claim is misleading.** The documentation states the export "adheres to standards like HL7 FHIR" but the actual format is custom JSON with no FHIR structure — no resource types, no references, no FHIR-standard terminologies beyond ICD-10.

### Summary Stats

```
Coverage:        Minimal/stub
Approach:        Purpose-built EHI export
Export format:   Custom JSON
Entities:        8 (6 main + 2 sub-objects)
Fields:          41
Descriptions:    100% (all fields have descriptions)
Sample data:     Minimal (4-field JSON fragment)
Bulk export:     Unclear (can select multiple patients)
Domains covered: 7 of 19 applicable (1 full, 6 partial)
```

### Bottom Line

A patient or provider would receive a basic clinical summary — demographics, problem list, medications, allergies, encounter notes, and RPM readings — but would miss the behavioral health specialty data that is the product's primary purpose, plus lab results, billing records, eMAR data, and patient communications. The export covers roughly what a C-CDA CCD would contain, delivered in a custom JSON format, despite the product storing significantly broader data. For a behavioral health EHR, the absence of therapy notes, treatment plans, and assessments is a critical gap in (b)(10) compliance.
