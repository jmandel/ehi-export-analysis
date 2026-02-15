# EHI Export Analysis: BroadStreet Health LLC

**Product**: BroadStreet, Version 1
**Analysis date**: 2026-02-15
**CHPL ID**: 15.05.05.3161.BRDS.01.00.1.231222

## 1. Product Context

BroadStreet is an ONC-certified EHR developed by BroadStreet Health LLC (closely affiliated with Arsana Health / WashSense Inc.) for **post-acute and community-based healthcare providers**. Its target users include staff at skilled nursing facilities (SNFs), assisted living communities, and other long-term care settings. The company is very early-stage (1–10 employees, based in Cambridge, MA / Springfield, VT) with minimal market presence — no third-party reviews, no customer case studies, and a largely placeholder website.

**Data the product should store** (based on certified criteria and RWT plan):

- Patient demographics, family health history
- Medication orders and lists (CPOE for medications — a)(1))
- Laboratory orders (CPOE — a)(2))
- Diagnostic imaging orders (CPOE — a)(3))
- Problem lists, allergy lists
- Immunization records
- Implantable device records
- Social, psychological, and behavioral data (a)(15))
- Care plans
- Clinical notes (progress notes, H&P — implied by the Notes HTML export format)
- C-CDA documents (transitions of care — b)(1))
- Clinical quality measure data (CQMs for depression, BMI, tobacco, falls, dementia, kidney health)
- Patient-generated health data (e)(3))

**What's notably absent from the product's known capabilities**: billing/claims functionality (not mentioned in any certification criteria or marketing), scheduling as a major module, and detailed nursing assessments (MDS/OASIS — expected for post-acute but not documented). The RWT plan describes testing at "on-site primary care at assisted living facility" and "on-site psychiatric care at skilled nursing facility."

**For EHI completeness assessment**: The baseline expectation is primarily clinical data across the certified criteria domains. Billing is likely handled externally and may be N/A for this product.

## 2. Artifacts Reviewed

| Artifact | File | Size | Description | Informativeness |
|---|---|---|---|---|
| EHI Export page (rendered HTML) | `ehi-export-page-rendered.html` | 9,698 bytes | Full content of the EHI Export documentation page after JS hydration | **Most informative** — the primary (b)(10) documentation |
| EHI Export page (screenshot) | `ehi-export-page.png` | 674 KB | Full-page screenshot confirming rendered content matches extracted HTML | Confirmatory |
| EHI Export page (raw HTML) | `ehi-export-page-raw.html` | 4,194 bytes | Server-rendered SvelteKit shell — just a spinner, no content | Confirms SPA architecture |
| FHIR Resources page (screenshot) | `fhir-resources-page.png` | 127 KB | Screenshot of (g)(10) FHIR API resource index — 12 clinical + 11 reference resources | **Informative** — enables comparison with EHI export FHIR list |
| 2025 Real World Testing Plan | `BST-2025-RWT-Plan.pdf` | 184 KB, 15 pages | RWT plan with Test Case 4 for (b)(10) EHI Export | Moderately informative — confirms testing approach but vague on export content |

**No data dictionary, no sample data files, no schemas, no export format specifications** were found among the artifacts. The entire (b)(10) export documentation consists of a single web page.

## 3. Export Mechanics

- **Format(s)**: Three formats described: CDA 2.1, FHIR R4, and BroadStreet Notes (HTML)
- **Mechanism**: Not documented. No export instructions, no UI screenshots, no API endpoints specific to (b)(10). The RWT plan mentions "export requests" tracked via logs, suggesting a UI-triggered process. The FHIR resources are served from `portal.broadstreetcare.com/api/fhir/` (the (g)(10) API endpoint), and it is unclear whether the "(b)(10) FHIR R4 export" is anything beyond this same API.
- **Single-patient vs bulk**: The RWT plan mentions both "individual and population-level EHI exports" and counts "single-patient exports to EHI." Both capabilities are claimed but not documented.
- **Access constraints/fees**: Not documented. The mandatory disclosures page notes that Direct secure messaging (h)(1) requires an annual subscription via EMR Direct, but no fees for EHI export itself are mentioned.

## 4. Export Content: What's In It

### 4.1 CDA 2.1 Section

The EHI export page provides a **generic textbook description** of the CDA 2.1 standard — what headers and bodies are, that documents are human-readable and machine-processable. There is zero BroadStreet-specific content: no list of CDA sections populated, no template identifiers, no sample documents, no specification of which clinical data is included.

The only BroadStreet-specific statement is: *"Our system exports patient data in the form of CDA documents that adhere to the CDA 2.1 standard."*

Given the (b)(1) Transitions of Care certification with SVAP update to C-CDA R2.1 Companion Guide Release 3, this is very likely the same C-CDA used for transitions of care, not a distinct (b)(10) export.

### 4.2 FHIR R4 Section

The EHI export page lists **15 FHIR resource types** (extracted from `ehi-export-page-rendered.html`, excluding 3 non-resource bullet items about "Granular Data," "Web Standards," and "Extensibility" that describe FHIR features):

| # | FHIR Resource | Description (from page) |
|---|---|---|
| 1 | Patient | Information about an individual receiving care |
| 2 | Observation | Measurements or simple assertions made about a patient |
| 3 | Medication | Details about a medication that can be prescribed |
| 4 | Practitioner | Individual with a formal responsibility in the healthcare process |
| 5 | Encounter | Interaction between a patient and the healthcare provider |
| 6 | Procedure | Clinical activity or intervention performed on or for a patient |
| 7 | Condition | Clinical condition, problem, or diagnosis |
| 8 | Immunization | Record of an immunization given to a patient |
| 9 | AllergyIntolerance | Adverse reaction or allergy a patient has to substances |
| 10 | MedicationRequest | Request for a medication to be administered or dispensed |
| 11 | CarePlan | Plan or protocol to manage a patient's specific health concerns |
| 12 | Device | Medical device used on or for a patient |
| 13 | DiagnosticReport | Findings and interpretation of diagnostic tests |
| 14 | Appointment | Scheduled interaction between patient and healthcare provider |
| 15 | Organization | Organization involved in the care of a patient |

**Comparison with (g)(10) FHIR API** (from `fhir-resources-page.png`):

The (g)(10) API serves **23 resources** (12 clinical + 11 reference). The EHI export page lists 15. The overlap is 14 resources. Key differences:

- **On EHI page but NOT in (g)(10) API**: Appointment (1 resource)
- **In (g)(10) API but NOT on EHI page**: CareTeam, DocumentReference, Goal, Location, PractitionerRole, Provenance, QuestionnaireResponse, RelatedPerson, ServiceRequest (9 resources)

The EHI export page's FHIR list is a **subset** of the standard US Core resource set plus Appointment. The descriptions are generic FHIR standard text (e.g., "Information about an individual receiving care") — identical to what HL7 publishes — with no vendor-specific content, no extensions, no custom profiles.

### 4.3 BroadStreet Notes (HTML) Section

This is the **only vendor-specific export documentation**. It describes the structure of clinical notes exported as HTML documents. Parsed from the rendered page, it contains **10 sections with 20 named fields**:

| Section | Fields | Field Names |
|---|---|---|
| Physician Information | 3 | Physician Name, Sent by, Date |
| Visit and Patient Details | 6 | Date of Service, Type, Patient Name, Date of Birth, Gender, Advance Directive Code |
| Medical Concerns | 2 | Allergies, Primary Concern |
| Social History | 1 | Smoking Status |
| Treatment Review | 0 | *(described as "typically include past and ongoing treatments")* |
| Vital Examination | 3 | Blood Pressure, Pulse, Weight |
| Assessment Plan | 2 | Diagnosis Code, Assessment |
| Visit Details | 2 | Next Appointment, Reason for Next Visit |
| Additional Notes | 0 | *(described as "any additional remarks")* |
| Signature | 1 | Electronically Signed By |

**Documentation quality for Notes fields**: Each field has a name and a one-sentence natural-language description. No data types, no constraints, no value sets (except "ICD code" for Diagnosis Code), no examples, no sample HTML output.

### Vendor's Own Content Organization

The vendor organizes the EHI export page into three top-level sections:

| Export Format | Items Documented | Field-Level Detail | BroadStreet-Specific |
|---|---|---|---|
| CDA 2.1 | 5 generic bullet items | None | 1 sentence |
| FHIR R4 | 15 resource types | None (resource-level only) | 1 sentence |
| BroadStreet Notes (HTML) | 10 sections, 20 fields | Yes (name + description) | Yes |

**Total across all formats**: 15 FHIR resource types (resource-level only, no fields) + 20 named fields in Notes HTML = effectively 20 documented fields total, plus generic standard descriptions.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's EHI export documentation describes three output formats that together cover a narrow range of clinical data:

1. **CDA 2.1**: Completely unspecified. No BroadStreet-specific content. Likely just the C-CDA used for transitions of care (b)(1).

2. **FHIR R4**: Lists 15 standard FHIR resource types — a subset of the US Core set. These correspond to USCDI data classes (demographics, conditions, medications, allergies, immunizations, vitals/labs via Observation, procedures, encounters, care plans, devices, diagnostic reports). No vendor-specific extensions, custom resources, or data beyond USCDI. This appears to be the same data served by the (g)(10) API.

3. **BroadStreet Notes (HTML)**: The only genuinely vendor-specific component. Documents clinical notes with 20 fields covering physician info, patient demographics, allergies, vitals, diagnoses, and assessment plans. This represents a single document type — a clinical encounter note — not a comprehensive export.

**Thinnest areas**: CDA section (no specifics at all), FHIR section (generic standard descriptions only). **Richest area**: Notes HTML (20 fields with descriptions, though still very basic).

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | FHIR `Patient` resource listed; Notes HTML has Patient Name, DOB, Gender | Resource-level only; no field detail for FHIR Patient; Notes covers ~3 demographic fields |
| Encounters / visits | ⚠️ Partial | FHIR `Encounter` listed; Notes HTML has Date of Service, Type | No encounter detail beyond resource name |
| Problems / conditions / diagnoses | ⚠️ Partial | FHIR `Condition` listed; Notes HTML has Diagnosis Code (ICD) | Resource-level only |
| Medications / prescriptions | ⚠️ Partial | FHIR `Medication`, `MedicationRequest` listed | Resource-level only; no eMAR documentation |
| Allergies | ⚠️ Partial | FHIR `AllergyIntolerance` listed; Notes HTML has Allergies field | Resource-level only |
| Immunizations | ⚠️ Partial | FHIR `Immunization` listed | Resource-level only |
| Vitals | ⚠️ Partial | FHIR `Observation` listed; Notes HTML has BP, Pulse, Weight | 3 vitals in Notes; Observation is generic |
| Lab results | ⚠️ Partial | FHIR `Observation`, `DiagnosticReport` listed | Product has CPOE for labs (a)(2); resource-level only |
| Imaging / diagnostic reports | ⚠️ Partial | FHIR `DiagnosticReport` listed | Product has CPOE for imaging (a)(3); resource-level only |
| Procedures | ⚠️ Partial | FHIR `Procedure` listed | Resource-level only |
| Clinical notes / documents | ⚠️ Partial | BroadStreet Notes (HTML) with 20 fields | Only documents a single note type (encounter note). No mention of other note types |
| Care plans / goals | ⚠️ Partial | FHIR `CarePlan` listed | Certified for (b)(11) care plan; resource-level only. Goal not listed on EHI page (though in g(10) API) |
| Orders / referrals | ❌ Not covered | Not mentioned in EHI export documentation | CPOE criteria (a)(1-3) confirmed; ServiceRequest in (g)(10) but not on EHI page |
| Insurance / coverage | ❌ Not covered | No mention | Likely N/A — no evidence product manages insurance data |
| Claims / billing | ❌ Not covered | No mention | Likely N/A — no billing module documented anywhere |
| Payments | ❌ Not covered | No mention | Likely N/A — no payment functionality documented |
| Consents / directives | ⚠️ Partial | Notes HTML has "Advance Directive Code" field | Single field only |
| Patient communications / portal messages | ❌ Not covered | No mention | Product certified for patient VDT (e)(1) and PGHD (e)(3), suggesting patient portal exists; portal messages not in export |
| Specialty-specific (post-acute / long-term care) | ❌ Not covered | No mention of MDS assessments, nursing assessments, eMAR, fall risk tools, cognitive assessments, or other post-acute-specific data | **Significant gap**. Product is specifically designed for post-acute care. CQMs include falls screening (CMS139), dementia cognitive assessment (CMS149), depression screening (CMS2) — the underlying clinical data for these assessments is not documented in the export |
| Family health history | ❌ Not covered | Not listed in FHIR resources or Notes HTML | Certified for (a)(12) family health history; absent from export documentation |
| Social/behavioral data | ⚠️ Partial | Notes HTML: Smoking Status (1 field) | Certified for (a)(15) social, psychological, behavioral data; only smoking status documented |
| Implantable devices | ⚠️ Partial | FHIR `Device` listed | Certified for (a)(14); resource-level only |

**Summary**: Every domain marked "⚠️ Partial" is partial primarily because the documentation only identifies resource/entity names without field-level detail — making it impossible to assess actual depth of coverage. The most concerning gaps are:

1. **Post-acute specialty data** (MDS, nursing assessments, eMAR, fall risk, cognitive assessments) — entirely absent despite being the product's core market
2. **Family health history** — certified but missing from export
3. **Orders/referrals** — CPOE certified but not in EHI export documentation
4. **Patient portal communications** — portal exists but no export documentation

## 6. Documentation Quality

**Overall: Very poor.** The EHI export documentation is a single web page with approximately 1,500 words, most of which are generic descriptions of the CDA and FHIR standards copied from or paraphrasing HL7 specification text.

**What's present**:
- Three export format names (CDA 2.1, FHIR R4, BroadStreet Notes HTML)
- A list of 15 FHIR resource types with one-line standard descriptions
- 20 field names for clinical notes with one-sentence descriptions
- Links to external HL7 CDA and FHIR R4 documentation

**What's absent**:
- ❌ No data dictionary (no table/field definitions beyond the 20 Notes fields)
- ❌ No schema or format specification (no JSON Schema, XSD, or other machine-readable artifact)
- ❌ No sample data or example export files
- ❌ No export instructions (how to trigger, what UI to use, what files are produced)
- ❌ No field data types or constraints
- ❌ No relationship documentation
- ❌ No value set or terminology documentation (only "ICD code" mentioned once)
- ❌ No indication of export file packaging (ZIP? individual files? bundle?)
- ❌ No documentation distinguishing (b)(10) from (g)(10) — the FHIR content appears identical

**Could a developer build an import from this documentation?** No. The documentation does not specify file formats, field schemas, bundle structures, or data types. A developer would not know what files to expect, what format they're in, or how to parse them. The Notes HTML section provides field names but no HTML structure specification. The FHIR section provides resource type names but no profiles, extensions, or search parameters specific to (b)(10).

## 7. Overall Assessment

### Classification

**Minimal/stub**: The documentation is too thin to verify what the export actually contains. What is documented amounts to (1) a generic restatement of the CDA and FHIR standards, (2) a list of 15 standard FHIR resource types that appear identical to the (g)(10) API, and (3) a simple 20-field clinical note structure. No data dictionary, no schemas, no sample data, no export instructions.

### Key Findings

1. **The (b)(10) export appears to be the (g)(10) FHIR API repackaged.** The FHIR resource list on the EHI export page is a subset (15 of 23) of the (g)(10) US Core resources. No vendor-specific extensions or additional data beyond USCDI are documented. The documentation does not explain how (b)(10) differs from (g)(10).

2. **Post-acute specialty data is entirely absent from the export documentation.** Despite being built for skilled nursing and assisted living facilities, there is no mention of MDS assessments, nursing assessments, eMAR, fall risk screening data, cognitive assessments, or other post-acute clinical workflows in the export.

3. **The only vendor-specific documentation is a 20-field clinical note structure.** The BroadStreet Notes (HTML) section is the sole artifact that describes BroadStreet-specific data, but it covers only a single encounter note type with basic fields (demographics, vitals, diagnoses, assessment).

4. **No machine-readable artifacts exist.** No schemas, no sample data, no format specifications. The entire (b)(10) documentation is a single ~1,500-word web page.

5. **The RWT plan confirms testing but is vague on content.** Test Case 4 describes tracking export "frequency and completion times" and verifying "compatibility with external systems" but does not specify what data is exported or what domains are covered.

### Summary Stats

```
Classification:  Minimal/stub
Export format:   CDA 2.1, FHIR R4, HTML (clinical notes)
Model type:      Standard projection (FHIR/CDA) + proprietary note format
Entities:        15 FHIR resource types + 1 note type (no native data model)
Fields:          20 (Notes HTML only; FHIR fields not documented)
Descriptions:    100% of 20 Notes fields have descriptions; 0% have types
Sample data:     No
Bulk export:     Claimed (RWT plan mentions population-level); not documented
Domains covered: 0 of 15 fully covered; 12 of 15 partially (resource-name-only)
```

### Bottom Line

BroadStreet's EHI export documentation is a minimal compliance stub — a single web page that mostly restates the CDA and FHIR standards with no vendor-specific detail. A patient or provider requesting their complete health data would receive, at best, a standard USCDI clinical summary via FHIR/C-CDA, missing specialty post-acute care data (nursing assessments, medication administration records, cognitive/behavioral assessments) that is the product's core value proposition. The biggest gap is the complete absence of post-acute-specific clinical data from the export documentation, combined with no data dictionary or schema to verify what's actually included.
