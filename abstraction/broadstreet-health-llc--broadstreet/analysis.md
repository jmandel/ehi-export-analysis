# EHI Export Analysis: BroadStreet Health LLC

**Product**: BroadStreet, Version 1
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.05.05.3161.BRDS.01.00.1.231222 (CHPL ID 11410)

## 1. Product Context

BroadStreet is an ONC-certified EHR developed by BroadStreet Health LLC (a subsidiary or DBA of Arsana Health / WashSense Inc.) for **post-acute and community-based healthcare settings** — specifically skilled nursing facilities (SNFs), assisted living facilities, residential care facilities, and home-based care. The company is extremely small (1–10 employees), based in Springfield, Vermont, and appears to be an early-stage startup with minimal market presence.

**What the product should store (based on certified criteria and product research):**
- **Patient demographics** (a)(5)
- **Medication orders** via CPOE (a)(1) and medication lists
- **Laboratory orders** via CPOE (a)(2) and lab results
- **Diagnostic imaging orders** via CPOE (a)(3)
- **Problem lists / conditions**
- **Allergies**
- **Immunizations**
- **Family health history** (a)(12)
- **Implantable device records** (a)(14)
- **Social, psychological, and behavioral data** (a)(15)
- **Care plans** (b)(11)
- **Clinical notes** (implied by charting and CQM capabilities)
- **Clinical quality measure data** — depression screening, BMI, tobacco, falls, dementia, kidney health
- **C-CDA documents** for transitions of care (b)(1)
- **Patient-generated health data** (e)(3)

**What's unclear / likely absent in the product:**
- **Billing/claims**: No billing-related certification criteria. Product research found no evidence of billing functionality. Billing is likely handled externally.
- **Scheduling**: Not mentioned in any documentation.
- **Nursing assessments (MDS/OASIS)**: Not documented despite post-acute focus where MDS is a core SNF workflow.
- **eMAR (medication administration records)**: Not documented, though expected for post-acute care.

## 2. Artifacts Reviewed

| Artifact | File | Size | Description | Informativeness |
|---|---|---|---|---|
| EHI Export page (rendered HTML) | `ehi-export-page-rendered.html` | 9,698 bytes | Full content of the EHI Export documentation page after JS hydration. **Primary artifact.** | ⭐ Most informative |
| EHI Export page screenshot | `ehi-export-page.png` | 674 KB | Full-page screenshot confirming rendered HTML content matches | Confirmatory |
| FHIR Resources page screenshot | `fhir-resources-page.png` | 127 KB | Screenshot of (g)(10) FHIR API resource listing — 12 clinical + 11 reference resources | Moderately informative |
| Raw HTML (pre-JS) | `ehi-export-page-raw.html` | 4,194 bytes | SvelteKit app shell; confirms site requires JS to render | Minor |
| 2025 RWT Plan | `BST-2025-RWT-Plan.pdf` | 184 KB, 15 pages | Real World Testing plan with Test Case 4 for (b)(10). Describes testing methodology but not export content. | Moderately informative |

**No data dictionary, schema, sample data, or machine-readable artifacts were found.** The five artifacts above are the complete set.

## 3. Export Mechanics

- **Format(s)**: Three formats are described: CDA 2.1 (XML), FHIR R4 (JSON/XML bundles), and BroadStreet Notes (HTML).
- **Mechanism**: Not documented. No instructions exist for how to trigger an export, what UI buttons to use, or what API calls to make. The RWT Plan mentions "export requests" tracked via logs, and the (b)(10) test case references both individual and population-level exports, but gives no procedural detail.
- **Single-patient vs bulk**: The RWT Plan states testing covers "both individual and population-level EHI exports," suggesting both are supported. No further detail.
- **Access constraints or fees**: Not documented. No mention of fees for EHI export specifically. Direct secure messaging (h)(1) requires an annual subscription to EMR Direct, but this is separate.

## 4. Export Content: What's In It

### What the documentation actually provides

The EHI export documentation page (`ehi-export-page-rendered.html`) is almost entirely **generic descriptions of the CDA and FHIR standards**, with minimal BroadStreet-specific content. There is **no data dictionary, no schema, no field-level documentation for the CDA or FHIR exports**, and no sample data.

**CDA 2.1**: The page describes what CDA is (headers, bodies, sections, entries) in textbook terms. The only BroadStreet-specific statement is: *"Our system exports patient data in the form of CDA documents that adhere to the CDA 2.1 standard."* No BroadStreet-specific templates, section lists, profiles, or implementation detail is provided.

**FHIR R4**: The page lists 15 FHIR resource types with one-line generic descriptions (e.g., *"Patient: Information about an individual receiving care"*). These are standard FHIR definitions, not vendor-specific field documentation. The only BroadStreet-specific statement is: *"When exporting data in FHIR format, our system provides a bundle of FHIR resources."*

**BroadStreet Notes (HTML)**: This is the only section with BroadStreet-specific field-level documentation — 22 fields across 10 subsections describing the structure of exported clinical notes.

### Vendor's own content organization

#### FHIR R4 Resources (listed on EHI Export page)

15 resources are listed on the EHI Export page. Separately, the FHIR API Resources page (screenshot: `fhir-resources-page.png`) lists 23 resources. There is notable divergence:

| Resource | On EHI Export Page | On FHIR API Page | Category (vendor's) |
|---|---|---|---|
| AllergyIntolerance | ✅ | ✅ | Clinical Information |
| Appointment | ✅ | ❌ | (EHI page only) |
| CarePlan | ✅ | ✅ | Clinical Information |
| CareTeam | ❌ | ✅ | Clinical Information |
| Condition | ✅ | ✅ | Clinical Information |
| Device | ✅ | ✅ | Resources and References |
| DiagnosticReport | ✅ | ✅ | Clinical Information |
| DocumentReference | ❌ | ✅ | Resources and References |
| Encounter | ✅ | ✅ | Clinical Information |
| Goal | ❌ | ✅ | Clinical Information |
| Immunization | ✅ | ✅ | Clinical Information |
| Location | ❌ | ✅ | Resources and References |
| Medication | ✅ | ✅ | Clinical Information |
| MedicationRequest | ✅ | ✅ | Clinical Information |
| Observation | ✅ | ✅ | Clinical Information |
| Organization | ✅ | ✅ | Resources and References |
| Patient | ✅ | ✅ | Resources and References |
| Practitioner | ✅ | ✅ | Resources and References |
| PractitionerRole | ❌ | ✅ | Resources and References |
| Procedure | ✅ | ✅ | Clinical Information |
| Provenance | ❌ | ✅ | Resources and References |
| QuestionnaireResponse | ❌ | ✅ | Resources and References |
| RelatedPerson | ❌ | ✅ | Resources and References |
| ServiceRequest | ❌ | ✅ | Resources and References |

The FHIR resource list on the EHI Export page is essentially the **standard US Core resource set** — the same resources available through any (g)(10) FHIR API. No vendor-specific FHIR profiles, extensions, or custom resources are documented.

#### BroadStreet Notes (HTML) — Field-level detail

| Section | Field | Description |
|---|---|---|
| Physician Information | Physician Name | The name of the physician who provided the service |
| Physician Information | Sent by | The individual who sent the documentation |
| Physician Information | Date | The timestamp when the documentation was sent |
| Visit and Patient Details | Date of Service | The date when the service was provided |
| Visit and Patient Details | Type | The type of service provided (e.g., H&P) |
| Visit and Patient Details | Patient Name | The full name of the patient |
| Visit and Patient Details | Date of Birth | The birthdate of the patient |
| Visit and Patient Details | Gender | The gender of the patient |
| Visit and Patient Details | Advance Directive Code | Any code related to advance directives |
| Medical Concerns | Allergies | Any known allergies |
| Medical Concerns | Primary Concern | The main reason for the patient's visit |
| Social History | Smoking Status | The patient's smoking habits |
| Treatment Review | *(unstructured)* | Past and ongoing treatments |
| Vital Examination | Blood Pressure | Systolic/Diastolic measurement |
| Vital Examination | Pulse | Heart rate in beats per minute |
| Vital Examination | Weight | Patient's weight |
| Assessment Plan | Diagnosis Code | The ICD code for the diagnosis |
| Assessment Plan | Assessment | Physician's findings and recommendations |
| Visit Details | Next Appointment | Next scheduled appointment date and physician |
| Visit Details | Reason for Next Visit | Purpose for upcoming visit |
| Additional Notes | *(unstructured)* | Physician remarks |
| Signature | Electronically Signed By | Who signed the document electronically |

**Total: 22 fields across 10 sections. All 20 named fields have descriptions. No data types, constraints, value sets, or examples are provided.**

#### CDA 2.1

No BroadStreet-specific documentation. Only generic CDA standard descriptions.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor documents three export formats but provides almost no detail about what data each format actually contains:

1. **CDA 2.1**: No specific section or template documentation. Impossible to assess what clinical data is included.
2. **FHIR R4**: Lists 15 standard FHIR resources — the standard US Core clinical data classes. No field-level detail, no extensions, no vendor-specific content. This appears to be a repackaging of the (g)(10) FHIR API.
3. **BroadStreet Notes (HTML)**: The only vendor-specific export format. Documents a clinical note structure with 22 fields covering physician info, patient demographics, allergies, vitals, diagnoses, and assessment plans. This is a single-note format, not a comprehensive patient record export.

The documentation is thinnest in the areas that should be richest — the CDA and FHIR sections provide no BroadStreet-specific detail whatsoever. The Notes section is the only area with field-level documentation, but it describes just one document type (a clinical note), not a comprehensive data export.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | FHIR Patient resource listed (no field detail); Notes HTML has Patient Name, DOB, Gender | Basic demographics present via FHIR Patient + Notes; depth unknown without field-level FHIR documentation |
| Encounters / visits | ⚠️ Partial | FHIR Encounter resource listed; Notes HTML has Date of Service, Type | Resource listed but no field detail |
| Problems / conditions / diagnoses | ⚠️ Partial | FHIR Condition resource listed; Notes has Diagnosis Code (ICD) | Resource listed; Notes has ICD code |
| Medications / prescriptions | ⚠️ Partial | FHIR Medication + MedicationRequest listed | Resource listed but no field detail. eMAR (medication administration records) not mentioned — significant for post-acute care |
| Allergies | ⚠️ Partial | FHIR AllergyIntolerance listed; Notes has Allergies field | Mentioned in both formats but no detail on allergy structure |
| Immunizations | ⚠️ Partial | FHIR Immunization listed | Resource listed, no detail |
| Vitals | ⚠️ Partial | FHIR Observation listed; Notes has BP, Pulse, Weight | Notes covers 3 vital signs; FHIR Observation presumably covers more |
| Lab results | ⚠️ Partial | FHIR Observation + DiagnosticReport listed | Resources listed; product is certified for lab CPOE (a)(2) |
| Imaging / diagnostic reports | ⚠️ Partial | FHIR DiagnosticReport listed | Resource listed; certified for imaging CPOE (a)(3) |
| Procedures | ⚠️ Partial | FHIR Procedure listed | Resource listed, no detail |
| Clinical notes / documents | ⚠️ Partial | BroadStreet Notes (HTML) — 22 fields documented | Only export format with vendor-specific detail; covers a single note type |
| Care plans / goals | ⚠️ Partial | FHIR CarePlan listed; Goal on API page only | Certified for (b)(11) care plans |
| Orders / referrals | ❌ Not covered | Not on EHI Export page; ServiceRequest on API page only | Certified for CPOE (a)(1-3); no order export documented on EHI page |
| Insurance / coverage | ❌ Not covered | No evidence in any artifact | Product likely doesn't handle insurance internally — N/A if confirmed |
| Claims / billing | ❌ Not covered | No evidence in any artifact | No billing certification criteria; likely N/A |
| Payments | ❌ Not covered | No evidence | Likely N/A |
| Consents / directives | ⚠️ Partial | Notes HTML has Advance Directive Code | Single field only |
| Patient communications / portal messages | ❌ Not covered | No evidence | Product has patient portal (e)(1); messages may exist but not documented |
| Specialty-specific (post-acute/SNF) | ❌ Not covered | No nursing assessments (MDS), no eMAR, no infection surveillance data, no fall risk assessments, no cognitive assessments | **Significant gap.** The product targets SNFs and assisted living. MDS assessments, eMAR, fall risk screening, and dementia cognitive assessments are core workflows. None appear in the export documentation. |

**Key coverage finding:** Every domain listed as "⚠️ Partial" earns that rating because the only evidence is a FHIR resource name with a generic one-line description — there is no way to verify what data actually populates those resources. The coverage could be reasonable or it could be very thin; the documentation simply doesn't say.

## 6. Documentation Quality

**Rating: Very poor.**

- **No data dictionary**: No table/field definitions exist for the CDA or FHIR exports. The Notes HTML section has field names and descriptions, but no types, constraints, value sets, or relationships.
- **No export instructions**: No UI screenshots, no step-by-step guide, no API documentation for triggering an export.
- **No sample data**: No example export files, sample bundles, or test data of any kind.
- **No machine-readable schemas**: No JSON Schema, FHIR StructureDefinitions, XSD, or OpenAPI specs.
- **No value set documentation**: The only coded field mentioned (Diagnosis Code = "ICD code") has no further specification.
- **No relationship documentation**: How entities relate to each other across the three export formats is not described.
- **Generic standard descriptions**: ~75% of the EHI Export page is textbook descriptions of the CDA and FHIR standards that could apply to any EHR system — not BroadStreet-specific documentation.

**Could a developer build an import from this documentation alone?** No. A developer would know the export comes in CDA, FHIR, and HTML formats, and would have a 22-field structure for clinical notes, but would have no specification of what's in the CDA documents, which FHIR profiles are used, what extensions exist, how data is bundled, or how to actually request an export.

## 7. Overall Assessment

### Classification

**Standard-based projection.** The EHI export documentation describes a CDA 2.1 + FHIR R4 export that maps closely to the standard US Core / USCDI data classes — the same clinical summary data available through the (g)(10) FHIR API. The only vendor-specific addition is an HTML clinical note format with 22 fields. There is no evidence of a native data model export, no export of post-acute specialty data (MDS assessments, eMAR, fall risk, cognitive assessments), and no data dictionary.

### Key Findings

1. **The (b)(10) export appears to be the (g)(10) FHIR API repackaged.** The FHIR resource list on the EHI Export page (15 resources) is a subset of the FHIR API page (23 resources), and the resource descriptions are generic FHIR definitions. No evidence exists that the EHI export provides any data beyond what the standard FHIR API serves. (Sources: `ehi-export-page-rendered.html`, `fhir-resources-page.png`)

2. **Documentation is almost entirely generic standard descriptions, not vendor-specific.** Approximately 75% of the EHI Export page describes what CDA and FHIR *are* (structured documents, granular resources, web standards) rather than what BroadStreet *exports*. (Source: `ehi-export-page-rendered.html`)

3. **Post-acute specialty data is absent from the export documentation.** For a product targeting SNFs and assisted living, the export documentation contains no mention of MDS assessments, medication administration records (eMAR), fall risk screenings, cognitive assessments, or infection surveillance data — all core workflows in post-acute care. (Source: product-research.md cross-referenced with `ehi-export-page-rendered.html`)

4. **The only BroadStreet-specific content is the HTML Notes structure — 22 fields describing a single clinical note type.** While this is genuine vendor-specific documentation, it covers only one document format, not a comprehensive patient record export. (Source: `ehi-export-page-rendered.html`)

5. **The RWT Plan confirms the export exists and is tested in production**, but the (b)(10) test case describes tracking export frequency and completion times — not validating export completeness or content coverage. (Source: `BST-2025-RWT-Plan.pdf`, p. 10, Test Case 4)

### Summary Stats

```
Classification:  Standard-based projection
Export format:   CDA 2.1 (XML) + FHIR R4 (JSON) + HTML (Notes)
Model type:      Standard projection (US Core / CDA), not native database
Entities:        24 FHIR resources + 1 CDA document type + 1 HTML note type = 26 total
Fields:          22 (only for HTML Notes; 0 field-level detail for FHIR/CDA)
Descriptions:    100% of 22 Notes fields have descriptions; 0% for FHIR/CDA (no field-level docs)
Sample data:     No
Bulk export:     Yes (per RWT Plan: "population-level EHI exports")
Domains covered: 0 of 13 fully covered; 11 of 13 partially (resource name only); 2 N/A
```

### Bottom Line

BroadStreet's EHI export documentation is a compliance checkbox, not a genuine data portability effort. The export appears to repackage the standard (g)(10) FHIR API as the (b)(10) EHI export, covering only the USCDI clinical summary data — a small fraction of what a post-acute EHR stores. The single biggest gap is the complete absence of post-acute specialty data (MDS assessments, eMAR, fall risk, cognitive assessments) from the export documentation, despite these being core workflows for the product's target market.
