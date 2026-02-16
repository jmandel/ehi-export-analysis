# EHI Export Analysis: CursaHealth LLC

**Product**: CursaHealth EHR v2.0
**Analysis date**: 2026-02-15
**CHPL ID**: 15.05.05.3249.CRSA.01.00.1.251229 (ID 11735)

## 1. Product Context

CursaHealth EHR is a cloud-based, all-in-one platform combining electronic health records, practice management, medical billing, patient portal, and transcription services. It targets small-to-medium ambulatory practices across internal medicine, family medicine, OB/GYN, pediatrics, and mental health/psychiatry. The company is small (11–50 employees) and was certified on 2025-12-29 across 37 ONC criteria.

**Data the product should store** (relevant to export completeness):
- **Clinical**: Patient demographics, encounters, problem lists, medications (CPOE for meds/labs/imaging), allergies, immunizations, vitals, lab results (integrations with Quest, Apollo, ConnectDX, etc.), imaging orders, family health history, social/behavioral data, implantable devices, clinical notes, care plans/goals, clinical decision support alerts
- **Billing/PM**: Claims, charges, payments, A/R management, coding, insurance information, appointment scheduling
- **Patient portal**: Secure messaging, patient-facing records, form completion
- **Specialty**: Mental health assessments, OB/GYN-specific records, pediatric growth data
- **Documents**: Scanned/imported documents, transitions of care (C-CDA), transcription records

The product markets itself as an all-inclusive EHR + billing platform (priced at 6% of collections for the full bundle), making billing data a core product feature.

## 2. Artifacts Reviewed

| Artifact | Source | Size | Description | Informativeness |
|---|---|---|---|---|
| `B10-Electronic-Health-information-Export.pdf` | Direct download from cursahealth.com | 466,927 bytes, 4 pages | Primary (b)(10) EHI export documentation. Created 2025-08-14 by Nouman Zafar using Microsoft Word. Pages: 1 = cover, 2 = table of contents, 3–4 = substantive content (~1.5 pages of prose). | **Primary artifact** but very thin |
| `FHIR-Documentation.html` | cursahealth.com/document/FHIR-Documentation.html | 121,094 bytes | (g)(10) FHIR API documentation referenced by the (b)(10) PDF. Documents 29 US Core STU 3.1.1 resource types with GET/POST endpoints, OAuth2 authorization, and client registration. | **Supplementary** — standard FHIR docs, not (b)(10)-specific |

No other artifacts exist. There is no data dictionary, no schema file, no sample data, no XLSX/CSV examples, and no additional documentation pages.

## 3. Export Mechanics

**Format(s)**: Hybrid — C-CDA XML + FHIR R4 JSON (via Bulk Data API) + Excel files + raw document files (PDF/JPG/PNG)

**Mechanism**: The PDF describes both single-patient and multi-patient ("patient population") export, but provides no UI screenshots or step-by-step instructions. The FHIR component uses the (g)(10) Bulk Data Access API at `https://fhirapi.cursahealth.com/api`. The mechanism for the Excel exports and document file exports is not specified.

**Single-patient**: Stated as available "at any time without developer assistance"
**Bulk/multi-patient**: Stated as supported for "a patient population in our standardized format" — no further detail on how this is triggered.

**Access constraints/fees**: Not documented.

## 4. Export Content: What's In It

The export has three structural layers, none with field-level documentation:

### 4a. C-CDA XML Documents

The PDF states the export produces "HL7 CCDA xml files which comply to US Core Data for Interoperability (USCDI), Version 1 requirements." Three HL7 standard references are cited (CDA R2, Consolidated CDA R2.1, C-CDA Companion Guide R2). No vendor-specific documentation is provided — there is no mapping of which C-CDA sections are populated, what coded values are used, or what vendor-specific data might appear. A developer would have to rely entirely on the C-CDA standard specification and reverse-engineer actual export files.

### 4b. FHIR Bulk Data Access (29 US Core Resource Types)

The FHIR documentation page (verified at 121 KB) documents 29 resource types, all standard US Core STU 3.1.1 profiles with zero vendor extensions:

| # | Resource Type | API Operations |
|---|---|---|
| 1 | AllergyIntolerance | Search, Read, _search |
| 2 | BMI For Age Observation | Search, Read, _search |
| 3 | CarePlan | Search, Read, _search |
| 4 | CareTeam | Search, Read, _search |
| 5 | Condition (Health Concerns) | Search, Read, _search |
| 6 | Device | Search, Read, _search |
| 7 | DiagnosticReport | Search, Read, _search |
| 8 | DocumentReference | Search, Read, _search |
| 9 | Encounter | Search |
| 10 | Goal | Search, Read, _search |
| 11 | Head Circumference Observation | Search, Read, _search |
| 12 | Immunization | Search, Read, _search |
| 13 | Laboratory Result Observation | Search, Read, _search |
| 14 | Location | Search |
| 15 | MedicationRequest | Search, Read, _search |
| 16 | Observation – Blood Pressure | Search, Read, _search |
| 17 | Observation – Body Height | Search, Read, _search |
| 18 | Observation – Body Temperature | Search, Read, _search |
| 19 | Observation – Body Weight | Search, Read, _search |
| 20 | Observation – Heart Rate | Search, Read, _search |
| 21 | Observation – Respiratory Rate | Search, Read, _search |
| 22 | Organization | Search |
| 23 | Patient | Search, Read, _search |
| 24 | Practitioner | Search |
| 25 | Procedure | Search, Read, _search |
| 26 | Provenance | Search |
| 27 | Pulse Oximetry Observation | Search, Read, _search |
| 28 | Smoking Status Observation | Search, Read, _search |
| 29 | Weight For Height Observation | Search, Read, _search |

These are exclusively USCDI v1 / US Core STU 3.1.1 resources. The PDF explicitly states: "Please refer 170.315(g)(10) FHIR-Documentation.html for the API Specifications" — confirming this is the (g)(10) API documentation being reused for (b)(10).

### 4c. Supplemental Non-FHIR Exports

Three additional export categories are described in a single sentence each, with no field-level documentation:

| Export Component | Format | Documentation Detail |
|---|---|---|
| Patient Demographics & Insurance | Excel | One sentence: "a comprehensive view of demographics and insurance details structured for clarity and ease of access." No column names, types, or value sets. |
| Appointments | Excel | One sentence: "a comprehensive view of all appointment details, structured for clarity and ease of access." No column names, types, or value sets. |
| Documents (Scanned/Imported) | PDF, JPG, PNG | Signed progress notes, lab results, radiology reports, and other scanned/uploaded documents. Organized by patient chart number in category subfolders (Lab Reports, Radiology, Scanned Receipts, etc.). |

### Vendor's own content organization

The vendor organizes their export into two main sections in the PDF:

**Section "File Formats"** (page 3):
- C-CDA documents (standards-based)
- FHIR Bulk Data Access (standards-based, references (g)(10) API)

**Unnumbered supplemental section** (page 4):
- Patient Demographics & Insurance (Excel)
- Appointments (Excel)
- Documents (original files)

| Entity/Component | Fields | Described | Types | Category (vendor's) |
|---|---|---|---|---|
| C-CDA XML Documents | Unknown | N/A — no vendor-specific mapping | N/A | File Formats |
| FHIR Resources (29 types) | Per US Core profiles | US Core standard only | Per US Core | File Formats |
| Patient Demographics & Insurance | Unknown | 0 | No | Supplemental |
| Appointments | Unknown | 0 | No | Supplemental |
| Documents (Scanned/Imported) | N/A (file export) | Folder structure described | N/A | Supplemental |

**Total entities with vendor-specific field documentation: 0**

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export has two tiers:

1. **Standards-based clinical data** (C-CDA + FHIR): This covers the standard USCDI v1 clinical data set — demographics, allergies, medications, conditions, vitals, immunizations, lab results, procedures, care plans, goals, encounters, diagnostic reports, document references, implantable devices, smoking status, and provenance. This is exactly what the (g)(10) API already provides. There is no evidence of any vendor-specific content beyond the US Core profiles.

2. **Supplemental exports**: The vendor adds three non-FHIR components to go beyond pure (g)(10):
   - Demographics & Insurance in Excel — potentially adds insurance detail not in US Core Patient
   - Appointments in Excel — not available via FHIR
   - Raw document files — provides original scanned/uploaded documents beyond what DocumentReference may contain

The supplemental exports show some awareness that (b)(10) requires more than (g)(10). However, they are completely undocumented at the field level, and the overall scope still has major gaps.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | FHIR Patient resource + Excel "Demographics & Insurance" (undocumented) | FHIR Patient covers basics; Excel may add more but no field list to confirm |
| Encounters / visits | ⚠️ Partial | FHIR Encounter (search only, no read-by-ID) | Basic encounter data via FHIR; likely missing visit-level detail from native model |
| Problems / conditions | ✅ Covered | FHIR Condition, C-CDA Problem List | Standard US Core coverage |
| Medications / prescriptions | ⚠️ Partial | FHIR MedicationRequest, C-CDA Medications | Covers medication orders; no MedicationAdministration or medication history detail. Product lacks e-prescribing certification. |
| Allergies | ✅ Covered | FHIR AllergyIntolerance, C-CDA Allergies | Standard US Core coverage |
| Immunizations | ✅ Covered | FHIR Immunization, C-CDA Immunizations | Standard US Core coverage |
| Vitals | ✅ Covered | FHIR Observations (BP, height, weight, temp, HR, RR, pulse ox, head circumference, BMI-for-age, weight-for-height) | 10 vital sign profiles — thorough for vitals |
| Lab results | ✅ Covered | FHIR Laboratory Result Observation, DiagnosticReport, C-CDA Results | Standard coverage; product has integrations with Quest, Apollo, etc. |
| Imaging / diagnostic reports | ⚠️ Partial | FHIR DiagnosticReport + scanned radiology reports in Documents export | Orders via CPOE (a)(3) certified but no structured imaging order export |
| Procedures | ✅ Covered | FHIR Procedure, C-CDA Procedures | Standard US Core coverage |
| Clinical notes / documents | ✅ Covered | FHIR DocumentReference + Documents export (signed progress notes, lab results, radiology reports as files) | Dual coverage via FHIR and raw files |
| Care plans / goals | ✅ Covered | FHIR CarePlan + Goal | Standard US Core coverage |
| Orders / referrals | ❌ Not covered | No order or referral resources in FHIR export; CPOE certified for (a)(1)–(a)(3) | Product supports CPOE for meds/labs/imaging; orders not in export |
| Insurance / coverage | ⚠️ Partial | Excel "Demographics & Insurance" (undocumented) | Likely present in Excel but no field documentation to confirm depth |
| Claims / billing | ❌ Not covered | No billing entities, claims, charges, or payment data in any export component | **Significant gap** — product markets billing as core feature (6% of collections pricing); A/R management, coding, and claims processing are product features |
| Payments | ❌ Not covered | No payment data in export | Product records payments; this is missing |
| Consents / directives | ❌ Not covered | No consent or advance directive resources | May be in C-CDA if populated, but not explicitly documented |
| Patient communications / portal messages | ❌ Not covered | No messaging or portal communication data in export | Product has secure messaging feature; messages not exported |
| Specialty-specific (mental health) | ❌ Not covered | No mental health assessment or specialty data in export | Product targets psychiatry and mental health; no specialty clinical data exported |
| Specialty-specific (OB/GYN) | ❌ Not covered | No OB/GYN-specific data in export | Product targets OB/GYN; no specialty clinical data exported |
| Specialty-specific (pediatrics) | ⚠️ Partial | FHIR BMI-for-Age, Weight-for-Height, Head Circumference | Growth observations only; no pediatric-specific assessments |
| Family health history | ❌ Not covered | Not in FHIR resources; may be in C-CDA but not documented | Certified under (a)(12); not explicitly in export |
| Social/behavioral data | ⚠️ Partial | FHIR Smoking Status Observation | Only smoking status; product certified under (a)(15) for broader social/behavioral data |

**Summary**: 7 domains covered, 6 partial, 7 not covered out of 20 applicable domains.

## 6. Documentation Quality

**Overall: Very poor.** The entire (b)(10) documentation is 4 PDF pages, of which only ~1.5 pages contain substantive content. There is:

- **No data dictionary** for any export format
- **No field/column definitions** — the Excel exports have zero documentation of what columns they contain
- **No data types** documented
- **No value sets or code systems** specified beyond standard references
- **No relationships or foreign keys** documented
- **No sample data** or example export files
- **No machine-readable schema** (no XSD, JSON Schema, OpenAPI, DDL)
- **No export instructions** — no screenshots, no step-by-step walkthrough
- **No C-CDA section mapping** — just references to the HL7 standard

The FHIR documentation (121 KB HTML) provides more detail but is explicitly the (g)(10) API documentation, not (b)(10)-specific. It documents standard US Core endpoints with no vendor-specific field mapping or extensions.

**Could a developer build an import from this documentation alone?** No. For the C-CDA component, a developer could use standard C-CDA parsers but would have no guidance on vendor-specific content. For the FHIR component, standard US Core clients would work. For the Excel exports, a developer would have to obtain sample files and reverse-engineer the column structure. For the documents export, the folder organization is described in prose but not formally specified.

## 7. Overall Assessment

### Classification

**Standard-based projection** — The export is primarily the (g)(10) FHIR API and C-CDA clinical summaries repackaged as "(b)(10)," supplemented by two undocumented Excel files and raw document files. There is no native data model export. The FHIR component is explicitly referenced as the (g)(10) documentation. The supplemental Excel exports add modest scope (demographics/insurance and appointments) but without field-level documentation they add almost no practical value.

### Key Findings

1. **The FHIR component is explicitly (g)(10) repackaged as (b)(10).** The PDF directly states "Please refer 170.315(g)(10) FHIR-Documentation.html." All 29 resource types are standard US Core STU 3.1.1 profiles with zero vendor extensions. This covers USCDI v1 clinical data but nothing vendor-specific.

2. **Billing data is entirely absent despite being a core product feature.** CursaHealth markets an all-inclusive EHR + billing bundle at 6% of collections, with claims processing, A/R management, and coding review. Not a single billing entity, claim, charge, or payment appears in the export documentation.

3. **Documentation is critically thin** — ~1.5 pages of substantive content across the entire (b)(10) documentation. No data dictionary, no field definitions, no sample data. The two Excel exports are described in a single sentence each with no column names.

4. **Specialty clinical data is absent.** The product targets mental health/psychiatry, OB/GYN, and pediatrics, but no specialty-specific clinical data (assessments, specialty notes, specialty forms) appears in the export.

5. **Patient portal messages are not exported.** The product has secure messaging between providers and patients, but this data is not included in any export component.

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA XML, FHIR R4 JSON, Excel, PDF/JPG/PNG files
Model type:      Standard projection (US Core/C-CDA) + undocumented supplemental
Entities:        29 FHIR resource types + 2 undocumented Excel files + 1 document file export
Fields:          N/A (no field-level documentation for any component)
Descriptions:    N/A (0% vendor-specific field descriptions)
Sample data:     No
Bulk export:     Yes (stated for both single and multi-patient)
Domains covered: 7 of 20 applicable domains fully covered; 6 partial
```

### Bottom Line

CursaHealth's EHI export is a (g)(10) FHIR API and C-CDA clinical summary repackaged as (b)(10), with minor supplemental Excel and document file exports. A patient would get a standard clinical summary (allergies, meds, conditions, vitals, labs, procedures) but would be missing all billing/claims data, specialty clinical assessments (mental health, OB/GYN), patient portal messages, and orders — despite the product storing all of these. The single biggest gap is the complete absence of billing data from a product that markets billing as a core feature.
