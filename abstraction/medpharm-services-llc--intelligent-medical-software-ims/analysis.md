# EHI Export Analysis: MedPharm Services LLC (Meditab)

**Product**: Intelligent Medical Software (IMS)
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.99.04.2804.Inte.SP.01.1.181113 (ID 9739)

## 1. Product Context

Intelligent Medical Software (IMS) is a **Complete EHR** by MedPharm Services LLC (an affiliate of Meditab Software, Inc.) for ambulatory/outpatient settings. It is an all-in-one platform combining EHR, practice management, medical billing/RCM, e-prescribing, patient portal, telemedicine, and reporting on a single Sybase SQL Anywhere database. The product is certified for 43 ONC criteria including 170.315(b)(10).

IMS serves small-to-medium practices (2–5 physicians is the sweet spot) and FQHCs, with approximately 41,000 healthcare professionals at 1,600+ clinics. Its primary differentiator is **deep specialty customization across 40+ medical specialties** — including allergy, cardiology, dermatology, fertility, ophthalmology, oncology, pain management, behavioral health, dental, and many others — each with dedicated templates and modules.

**Key data domains IMS stores:**
- **Clinical records**: Demographics, medical history, problem lists, medication lists, allergies, vital signs, clinical notes (specialty-specific templates for 40+ specialties), immunizations, care plans, referrals
- **Orders and results**: E-prescriptions (including EPCS), lab orders/results (90+ lab interfaces), diagnostic orders, prior authorizations
- **Billing and financial**: Claims creation through denial management, superbills, patient statements, insurance information, payment records, managed care write-offs, RCM data
- **Patient engagement**: Portal activity, secure messages, medication refill requests, telemedicine/televisit sessions, kiosk check-in records
- **Quality/reporting**: MIPS/MACRA, HEDIS, UDS, HCC coding, CQM data
- **Public health**: Immunization registry submissions, syndromic surveillance, cancer registry reporting

This broad scope — clinical, billing, specialty, and patient engagement — establishes the baseline for assessing export completeness.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/ehi-export-page.png` (730 KB) | Full-page screenshot of the EHI export page at `https://www.meditab.com/company/ehi-export`. Shows 170.315(b)(10) heading, C-CDA section list, and FHIR format reference. | **High** — primary evidence for what the vendor claims the export contains |
| `downloads/ehi-export-page.html` (326 KB) | Raw HTML of the EHI export page. Duda SPA — no static text content; must be rendered. | **Low** — unreadable without browser rendering |
| `downloads/fhir-specifications-top.png` (167 KB) | Viewport screenshot of the FHIR specifications page showing navigation with resource types and beginning of AllergyIntolerance documentation. | **Medium** — confirms resource list and documentation style |
| `downloads/fhir-specifications.html` (3.3 MB) | Raw HTML of the FHIR API specifications page. Duda SPA with 125 tables. | **Low** — requires browser rendering |
| `downloads/enrichment/fhir-resources.json` (34 KB) | Browser-extracted, deduplicated FHIR resource definitions: 16 resources, 131 fields, 47 search parameters. | **High** — machine-readable content of the FHIR specs page |
| `downloads/enrichment/extraction-stats.json` (2 KB) | Extraction statistics confirming 16 resources and field counts. | **Medium** — validates extraction completeness |
| `downloads/enrichment/fhir-resources-browser-extract.json` (30 KB) | Raw browser extraction data before deduplication. | **Low** — superseded by fhir-resources.json |
| `downloads/enrichment/extract-fhir-specs.ts` (5 KB) | Extraction script used to process browser data. | **Low** — methodology documentation |

**No downloadable data dictionary, PDF, schema, sample export, or ZIP file was found.** All documentation exists only as rendered web pages.

## 3. Export Mechanics

**Format(s):**
- HL7 C-CDA XML files compliant with USCDI v1
- FHIR R4 (v4.0.1) via Bulk Data export (STU 1.0.1), conforming to US Core STU 3.1.1

**Mechanism:** The EHI export page states IMS enables export "for an individual patient and the broader patient population in different export formats." The page does not describe a specific UI workflow, API endpoint, or step-by-step process. The FHIR portion explicitly refers users to their 170.315(g)(10) Standardized API documentation — indicating it is the same FHIR Bulk Data endpoint certified under g(10), repackaged as the b(10) export.

**Single-patient vs bulk:** Both implied ("individual patient and the broader patient population").

**Access constraints or fees:** Not documented on the EHI export page. Meditab's mandatory disclosures (per CHPL) list separate fees for FHIR API access, patient API access, and other modules, but the export page does not address cost.

## 4. Export Content: What's In It

The export documentation describes two output formats, both based on healthcare interoperability standards rather than the IMS native data model.

### C-CDA Sections (19 total)

The EHI export page lists 19 C-CDA sections. These are listed by name only — there is no field-level documentation, no sample C-CDA documents, and no CDA template OID references. The sections are:

1. Assessment
2. Clinical Notes
3. Durable Medical Equipment
4. Encounters
5. Family History
6. Functional Status
7. Goals
8. Health Concerns
9. Immunization
10. Laboratory Values/Results
11. Medications
12. Medication Allergies
13. Payer
14. Plan of Treatment
15. Problems
16. Procedures
17. Reason for Referral
18. Smoking Status and Tobacco Use
19. Vital Signs

*Source: EHI export page screenshot (`ehi-export-page.png`); 12 sections directly visible, 7 obscured by cookie consent banner but confirmed from the prior browser accessibility snapshot. See `analysis/ccda-sections.json`.*

### FHIR Resources (16 documented, possibly 17)

The FHIR specifications page documents 16 standard US Core resource types with field-level detail. The navigation menu in the screenshot also shows "Document Reference" as a 17th resource, but no content section for DocumentReference was captured in the browser extraction.

| Resource | Fields | Search Params | Key Data |
|---|---|---|---|
| Patient | 13 | 5 | Demographics, identifiers, address, contact, language |
| MedicationRequest | 12 | 4 | Medication orders, prescriptions, dosage |
| Immunization | 11 | 2 | Vaccine records, status, dates |
| Device | 11 | 2 | UDI, device identifiers, type |
| Encounter | 10 | 3 | Visit type, status, period, participants |
| DiagnosticReport | 10 | 5 | Lab/imaging reports, status, category |
| Condition | 8 | 2 | Diagnoses, problems, clinical status |
| Goal | 7 | 2 | Care goals, lifecycle status |
| Organization | 7 | 3 | Practice/facility info |
| CarePlan | 7 | 3 | Care plan text, status, category |
| Observation | 7 | 5 | Vitals, lab values, social history |
| AllergyIntolerance | 6 | 2 | Allergen, reaction, clinical status |
| CareTeam | 6 | 3 | Care team members, status |
| Practitioner | 6 | 3 | Provider identifiers, name, specialty |
| Procedure | 6 | 3 | Procedure codes, status, dates |
| Provenance | 4 | 0 | Author, timestamp, target |
| **TOTAL** | **131** | **47** | |

*Source: `downloads/enrichment/fhir-resources.json`; full inventory at `analysis/full-entity-inventory.json`.*

All 131 fields have descriptions (100%) and data types (100%). Each resource documents read and search interactions with request/response structure and standard HTTP response codes. The documentation is standard US Core — there are **no IMS-specific extensions, custom profiles, or vendor-proprietary resource types**.

### Vendor's own content organization

The vendor does not organize data into custom categories. The export is structured entirely around two interoperability standards:

| Standard | Entities | Fields | Documentation Level |
|---|---|---|---|
| C-CDA XML | 19 sections | N/A (section names only) | Section names listed; no field-level detail |
| FHIR R4 US Core | 16 resources | 131 | Field name, data type, description, required/optional |

**No native database entities, no vendor-specific tables, no proprietary data model is documented or exported.** The export is entirely a projection into standard healthcare data interchange formats.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's EHI export documentation covers exactly two things:

1. **C-CDA XML** — 19 standard C-CDA sections corresponding to USCDI v1 data classes. These represent the clinical summary data typically exchanged for care transitions. No field-level detail is provided beyond section names.

2. **FHIR R4 US Core** — 16 standard FHIR resources (131 fields) with field-level documentation. This is explicitly their g(10) Standardized API — the export page states: "For detailed specifications, please refer to 170.315(g)(10) for the Standardized API for patient and population services."

Both formats cover the same narrow slice of data: standard clinical content defined by US Core / USCDI v1. The C-CDA and FHIR documentation overlap substantially (e.g., both cover medications, allergies, conditions, procedures, vitals). Together, they represent **one coverage footprint** across two serialization formats.

The strongest area is standard clinical data: demographics, problems, medications, allergies, vitals, labs, encounters, immunizations, and procedures are all present. The coverage of payer/insurance information via C-CDA's "Payer" section is a small step beyond pure clinical data, but it captures only the insurance plan — not claims, charges, or payments.

**Nothing in the export documentation addresses** the vendor's native data model, billing system, specialty modules, e-prescribing details, patient portal data, quality reporting data, or any of the other data domains IMS stores.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | FHIR `Patient` (13 fields), C-CDA sections | Standard demographics covered |
| Encounters / visits | ✅ Covered | FHIR `Encounter` (10 fields), C-CDA "Encounters" | Standard encounter data; no scheduling or visit workflow detail |
| Problems / conditions / diagnoses | ✅ Covered | FHIR `Condition` (8 fields), C-CDA "Problems", "Health Concerns", "Assessment" | Standard problem list |
| Medications / prescriptions | ⚠️ Partial | FHIR `MedicationRequest` (12 fields), C-CDA "Medications" | Basic prescription data present. However, IMS has deep e-prescribing (EPCS, CoverMyMeds prior auth, Hub-Rx prescription flow). Export shows only standard MedicationRequest — no PDMP data, no prior auth status, no prescription fill history |
| Allergies | ✅ Covered | FHIR `AllergyIntolerance` (6 fields), C-CDA "Medication Allergies" | Standard allergy data |
| Immunizations | ✅ Covered | FHIR `Immunization` (11 fields), C-CDA "Immunization" | Standard immunization records |
| Vitals | ✅ Covered | FHIR `Observation` (7 fields), C-CDA "Vital Signs" | Standard vital signs |
| Lab results | ✅ Covered | FHIR `DiagnosticReport` (10 fields), `Observation`, C-CDA "Laboratory Values/Results" | Standard lab results; IMS interfaces with 90+ labs but export shows only standard representations |
| Imaging / diagnostic reports | ⚠️ Partial | FHIR `DiagnosticReport` category includes "Imaging" | DiagnosticReport can represent imaging reports but no dedicated imaging/DICOM export |
| Procedures | ✅ Covered | FHIR `Procedure` (6 fields), C-CDA "Procedures" | Standard procedure data |
| Clinical notes / documents | ⚠️ Partial | C-CDA "Clinical Notes" section; FHIR nav shows "Document Reference" (not in extracted data) | C-CDA section name listed but no detail. IMS has specialty-specific templates for 40+ specialties — none of that specialty-specific structure is visible in the export |
| Care plans / goals | ✅ Covered | FHIR `CarePlan` (7 fields), `Goal` (7 fields), `CareTeam` (6 fields), C-CDA "Goals", "Plan of Treatment" | Standard care plan data |
| Orders / referrals | ⚠️ Partial | C-CDA "Reason for Referral", "Durable Medical Equipment" | Section names only; IMS has referral tracking and authorization management but no detailed export data |
| Insurance / coverage | ⚠️ Partial | C-CDA "Payer" section | Payer section listed but no field-level detail. Only captures insurance plan info, not enrollment or coverage details |
| Claims / billing | ❌ Not covered | No billing entities in export | **Significant gap.** IMS has integrated billing including claims creation, scrubbing, submission, denial management, superbills, payment posting, and full RCM. None of this appears in the export. Users describe IMS as "a biller's dream." |
| Payments | ❌ Not covered | No payment entities in export | **Significant gap.** IMS processes credit card, online, phone, and in-person payments. No payment data in export. |
| Consents / directives | ❌ Not covered | No consent entities in export | Product likely stores consent data but it does not appear in the export |
| Patient communications / portal messages | ❌ Not covered | No messaging or portal entities in export | **Gap.** IMS has secure messaging, patient portal (IMS Care), automated SMS/email (InTouch), and telemedicine (Televisit). None exported. |
| Specialty-specific data | ❌ Not covered | No specialty data in export | **Major gap.** IMS's primary value proposition is 40+ specialty modules (CosmetiSuite, FertilityEHR, dental, behavioral health, oncology, etc.) with custom templates and assessments. No specialty-specific data appears in the export — only generic US Core clinical resources. |

**Summary**: 8 of 18 applicable domains are covered, 5 are partially covered, and 5 are not covered at all. The missing domains represent the majority of IMS's unique value: billing/RCM, specialty clinical data, patient engagement, and payments.

## 6. Documentation Quality

**Overall quality: Poor.**

- **No data dictionary.** There is no documentation of the IMS database schema, no mapping between IMS internal data and the export, and no vendor-proprietary field definitions.
- **No export instructions.** The EHI export page does not explain how to actually perform an export — no UI screenshots, no step-by-step guide, no API documentation specific to b(10).
- **No sample data.** No example C-CDA documents, no sample FHIR bundles, no test export files.
- **No machine-readable schemas.** No XSD for C-CDA templates, no OpenAPI spec, no FHIR ImplementationGuide or StructureDefinition.
- **C-CDA documentation is section-name-only.** The 19 C-CDA sections are listed without any field-level detail, template references, or content descriptions. A developer cannot know what data populates these sections.
- **FHIR documentation is standard US Core.** The 16 resources with 131 fields are moderately well-documented (descriptions and types for all fields), but this is boilerplate US Core documentation — it tells you the shape of standard FHIR resources, not what IMS-specific data fills them.
- **No vendor-specific content.** There are no IMS-specific extensions, no custom profiles, no proprietary resource types, and no documentation explaining how IMS's rich internal data model maps to the standard resources.
- **g(10)/b(10) conflation.** The FHIR documentation explicitly refers users to their g(10) certification. This is the standard FHIR API repackaged as the EHI export — the vendor is not distinguishing between API access for apps and complete data export.

**Could a developer build an import from this documentation?** Only for standard C-CDA and FHIR consumption. A developer could parse the C-CDA documents and FHIR resources using standard tooling. However, they would have no way to know:
- What data is missing from the export
- How IMS-specific data (specialty templates, billing, e-prescribing) maps to these standards
- Whether the export captures all patient data or just a clinical summary subset
- How to obtain non-standard data

## 7. Overall Assessment

### Classification

**Standard-based projection.** The EHI export is IMS's existing C-CDA generation and FHIR Bulk Data API (certified under g(10)) presented as the b(10) EHI export. It covers standard clinical data classes but does not export the native IMS data model or address data domains beyond US Core / USCDI v1.

### Key Findings

1. **Classic g(10)/b(10) conflation.** The vendor's own EHI export page directs users to "170.315(g)(10) for the Standardized API" for FHIR specifications. The FHIR Bulk Data export is the g(10) API endpoint rebranded as the b(10) export — not a separate, comprehensive data export mechanism. *(Source: `ehi-export-page.png`, FHIR Format section)*

2. **No billing or revenue cycle data in the export.** IMS has integrated billing, claims management, superbills, payment processing, and full RCM — data that is part of the designated record set. None of this appears in the export documentation. *(Source: `product-research.md` §Billing; `ehi-export-page.png` shows no billing sections)*

3. **No specialty-specific clinical data.** IMS's primary differentiator is 40+ specialty modules with dedicated templates and assessments. The export contains only generic US Core resources — no specialty-specific data, custom forms, or assessment tools are documented. *(Source: `fhir-resources.json` shows only standard US Core resources)*

4. **Extremely thin C-CDA documentation.** 19 C-CDA sections are listed by name only — no field-level detail, no template references, no sample documents. It is impossible to assess what data actually populates these sections. *(Source: `ehi-export-page.png`)*

5. **No native database export.** IMS runs on Sybase SQL Anywhere. Despite having a single unified database for all clinical, billing, and administrative data, the vendor does not document or offer any native database-level export. The export is entirely filtered through standard projections (C-CDA, FHIR). *(Source: all artifacts reviewed — no database schema, no table documentation, no CSV/TSV/SQL dump format mentioned)*

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA XML + FHIR R4 (Bulk Data)
Model type:      Standard projection (US Core / USCDI v1)
Entities:        16 FHIR resources + 19 C-CDA sections (overlapping)
Fields:          131 (FHIR only; C-CDA sections have no field-level documentation)
Descriptions:    100% of FHIR fields have descriptions; 0% of C-CDA sections
Sample data:     No
Bulk export:     Yes (FHIR Bulk Data STU 1.0.1)
Domains covered: 8 of 18 applicable domains fully covered; 5 partial
```

### Bottom Line

IMS's EHI export is a repackaging of its standard C-CDA and FHIR g(10) API — it covers the clinical data classes defined by USCDI v1 but misses the majority of data IMS stores, including billing/RCM, 40+ specialty modules, e-prescribing details, patient portal data, and payment records. The single biggest gap is the complete absence of billing data from a product whose integrated billing is a core selling point. A patient or provider requesting their complete health information would receive a clinical summary, not the full record.
