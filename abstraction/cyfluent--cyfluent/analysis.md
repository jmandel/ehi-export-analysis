# EHI Export Analysis: Cyfluent

**Product**: Cyfluent EHR (CyCHART, CyMED, CySCRIPT, CyCLAIMS, CyPHR)
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2975.Cyfl.03.00.1.190813 (v3.2), 15.04.04.2975.Cyfl.03.01.1.241211 (v3.3)

## 1. Product Context

Cyfluent is a comprehensive cloud-based outpatient EHR platform developed by Planned Systems International (PSI), primarily serving small ambulatory practices (fewer than 3 physicians) and federal government health programs. The platform encompasses:

- **CyCHART (EHR)**: Full clinical charting with encounters, problems, medications, allergies, labs, vitals, care plans, goals, prescriptions (including EPCS), custom forms builder (DDO — Dynamic Data Objects), OB/GYN workflows, pain management, DSM assessments, vision, body measurements, clinical notes, and document scanning.
- **CyMED/CyfluentPM (Practice Management)**: Appointment scheduling, medical billing, charge ledger, A/R management, electronic claims submission through their own EHNAC-accredited clearinghouse (CyCLAIMS), insurance verification.
- **CySCRIPT (E-Prescribing)**: Electronic prescribing with DEA-certified EPCS.
- **CyPHR (Patient Portal)**: Patient-facing portal with secure messaging and telehealth.
- **Occupational Health**: OSHA-compliant injury/illness tracking, hearing exams, workplace medical records.
- **Health Services Management**: Medical evacuation, travel clearance, travel immunizations.
- **Pharmacy Fulfillment**: Pharmacy inventory, shipping, barcode tracking.

Notable deployment: HRSA's National Hansen's Disease (Leprosy) Program. Supports 8 medical specialties including cardiology, ophthalmology, podiatry, and pulmonology. Serves 150+ clinical practices across 13+ states.

The product stores extensive patient data across clinical, billing, administrative, specialty, and patient-portal domains. A complete EHI export should cover all of these.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `b10-EHI-Attestation-Information.docx` (45KB) | One-page attestation document with export instructions for single-patient and bulk export. References C-CDA 2.2 format. Dated 11/7/2023, version 3.2.00.3. | **Low** — minimal; no data dictionary, no field mapping |
| `OdataMetadata.xml` (796KB) | OData EDMX schema: 296 entity types, 3,162 properties, 876 navigation properties, 438 associations. Namespace: CfChartOpModel. | **High** — effectively a complete database schema / data dictionary |
| `OdataService.xml` (29KB) | OData service document listing all 296 entity set collection endpoints. | Low — confirms entity set availability |
| `ProviderPortalApi-3.3-swagger.json` (24KB) | OpenAPI/Swagger 2.0 spec for Provider Portal API v3.3: FHIR, oData, Security, and REST endpoints. | **Medium** — documents export mechanisms and API structure |
| `API-source/oData Example/Program.cs` (26KB) | C# source code demonstrating CDA extraction: logs in, queries patients via oData, pulls C-CDA per patient, queries individual data tables. | **High** — reveals what the C-CDA export covers (USCDI v1 data set) |
| `Desktop.zip` (69KB) | ZIP containing OdataMetadata.xml and OdataService.xml. | Low — container only |
| `API.zip` (24MB) | Full C# API client solution with NuGet packages and OData service references. | Medium — confirms API capabilities |
| `Cyfluent-Service-Based-URL-Endpoints.docx` (14KB) | FHIR API endpoints for 7 facilities. | Low — FHIR API reference only |
| `cyfluent-onc-certified-page-full.png` (791KB) | Screenshot of ONC certification page. | Low — confirms attestation text |
| `swaggerhub-api-docs.png` (207KB) | Screenshot of SwaggerHub API documentation. | Low — visual reference |
| `cures-directory-listing.html` (1.7KB) | IIS directory listing of CURES documentation folder. | Low — navigation aid |

## 3. Export Mechanics

**Certified (b)(10) export format**: C-CDA 2.2 (Consolidated Clinical Document Architecture)

**Single-patient export**: From patient chart → scroll bar shortcut → "Export Patient Data to CCD" → downloads CDA-format file. No developer assistance required.

**Bulk export**: Utilities → Files → CDA Extract Configuration → set date range → "Extract now" → downloads CDA-format files for all patients in the date range. Available to authorized users.

**API access (not the certified b(10) mechanism)**: Two additional pathways exist but are not described as the (b)(10) export:
- **FHIR v4.0.1 API** at `cyfluentphr.com/fhirapi/{facilityCode}/service-base-url` — Inferno-compliant, supports bulk export. Requires email request for credentials.
- **oData API** at `…/Secure/oData.svc` — Full database CRUD exposing all 296 entity types. Requires login credentials and API access.

**Access constraints**: Export limited to authorized Cyfluent users with role-based access privileges. API access requires credential request via email to support@cyfluent.com.

**Fees**: Not documented in the artifacts reviewed.

## 4. Export Content: What's In It

### The certified (b)(10) C-CDA export

The b10 attestation document (`b10-EHI-Attestation-Information.docx`) specifies C-CDA 2.2 as the export format and points to the HL7 C-CDA 2.2 specification (`https://build.fhir.org/ig/HL7/cda-ccda-2.2/`) as the format documentation. **No product-specific data dictionary or field mapping is provided for the C-CDA export.**

The C# Program.cs source code explicitly lists the data elements in the CDA extract via a comment block:

- Patient Name, Sex, Date of Birth, Race, Ethnicity, Preferred Language
- Smoking Status
- Problems
- Medications
- Medication Allergies
- Laboratory Tests / Laboratory Values/Results
- Vital Signs
- Procedures
- Care Team Members
- Immunizations
- Unique Device Identifiers (Implantable Devices)
- Assessment and Plan of Treatment
- Goals
- Health Concerns

This is the **USCDI v1 data set** — identical to what's required for (g)(10) FHIR API certification.

### The OData schema (full database model)

The OData EDMX metadata (`OdataMetadata.xml`) exposes the full database schema. This is not the (b)(10) export but reveals what data the system actually stores. Key statistics:

- **296 entity types** with **3,162 properties** and **876 navigation properties**
- **438 associations** defining relationships between entities
- **0% field descriptions** — the EDMX format provides field names, data types (Edm.String, Edm.DateTime, Edm.Boolean, Edm.Int32, Edm.Guid, Edm.Decimal, Edm.Binary), max lengths, nullability, and precision, but no human-readable descriptions or value set definitions

### Vendor's own content organization

The OData schema entities can be categorized by prefix/naming convention (see `analysis/entity-inventory-summary.json` for full breakdown):

| Category | Entities | Fields | Category Description |
|---|---|---|---|
| patient | 36 | 569 | Core patient records: demographics (71 fields), prescriptions (45), insurance (44), social history (26), contacts (24), problems (23), allergies (19), OB/GYN (18), medications (17), vitals (15), family history (14), body measurements (13), etc. |
| encounter | 43 | 525 | Encounter documentation: encounter (43 fields), chief complaints (26), pregnancy (22), OB/GYN (20), exams (multi-level: sections → items → groups → group items), diagnoses, prescriptions, DSM assessments, pain descriptions, risk factors, HPI, education, templates |
| orders-results | 25 | 248 | Orders and results: ActionItem (49 fields — lab/procedure orders), ActionItemResult (23 fields), ActionItemResultValue (17 fields), ActionItemResultAdminMedication (11 fields), with CPT/ICD/SNOMED code linkages |
| application | 23 | 218 | System-level entities, some patient-relevant: ApplicationFile (29 fields — stored documents/PDFs), ApplicationInterfaceDataQueue (billing interface), ApplicationFaxFile (faxes) |
| facility-config | 64 | 617 | Facility configuration: races, ethnicities, insurance plans, fee schedules, associates (referral providers), rooms, procedures, medication formulary, appointment types, etc. |
| code-sets | 38 | 240 | Reference/coded terminology: ICD, CPT, LOINC, SNOMED, allergies, medications, diets, advance directives, genders, smoking status, etc. |
| custom-forms | 6 | 71 | Dynamic Data Objects (DDO): DDO, DDOWidget (17 fields), DDOWidgetTemplate (18 fields), DDOInsertable, DDOWidgetUsage, DdoType — custom clinical form definitions and data |
| scanning | 4 | 47 | Document scanning: ScanPage (15 fields), ScanPredocument (12), ScanSegment (9), ScanSession (11) |
| messaging | 2 | 30 | Secure messaging: SecureMessage (23 fields), SecureMessageAttachment (7 fields) |
| eligibility | 3 | 11 | Insurance eligibility requests/responses |
| reporting | 9 | 81 | Report definitions and schedules |
| clinical-templates | 3 | 39 | HPI templates |
| other | 29 | 366 | Misc: PqriMeasure (135 fields), Lab (24), BodyMeasurementNorm (41), MuMeasure (33), etc. |

**Top 10 largest patient-data entities:**

| Entity | Properties | Nav Props | Domain |
|---|---|---|---|
| Patient | 71 | 57 | Demographics, contacts, identifiers |
| ActionItem | 49 | 16 | Orders (labs, procedures, plans) |
| PatientPrescription | 45 | 5 | Prescriptions/medications |
| PatientInsurance | 44 | 5 | Insurance/coverage |
| Encounter | 43 | 51 | Visit documentation |
| PatientAudit | 35 | 3 | Patient record audit trail |
| ApplicationFile | 29 | 14 | Documents/files |
| EncounterAudit | 27 | 3 | Encounter audit trail |
| EncounterChiefComplaint | 26 | 3 | Chief complaints |
| PatientSocialHistory | 26 | 2 | Social/behavioral history |

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The **certified (b)(10) C-CDA export** covers exclusively USCDI v1 clinical data elements — 20 data elements across ~14 C-CDA sections. This is the vendor's existing clinical exchange capability rebranded as the EHI export.

The **OData API** (not the certified export) exposes the full 296-entity database model including deep clinical data (encounter details with exam sections, HPI, chief complaints, pain management, DSM, OB/GYN, pregnancy), orders/results, insurance, prescriptions, custom forms, scanned documents, secure messages, and eligibility data. This would be capable of a comprehensive export, but it is **not what was certified as (b)(10)**.

The gap between the two is enormous:
- C-CDA export: ~14-20 data elements (USCDI scope)
- Full database: 296 entity types with 3,162 properties across clinical, administrative, and specialty domains

### 5b. Standardized domain coverage (top-down)

Assessment is **against the certified C-CDA (b)(10) export**, not the OData API:

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA includes name, sex, DOB, race, ethnicity, preferred language | Product stores 71 fields in Patient entity (contacts, identifiers, assigned physician, account numbers, etc.) — significant depth gap |
| Encounters / visits | ⚠️ Partial | C-CDA includes encounter context for other sections | Product has 43 encounter entity types with 525 fields (exam sections, chief complaints, HPI, pain descriptions, DSM, templates) — massive gap |
| Problems / conditions | ✅ Covered | C-CDA "Problems" section | PatientProblem has 23 fields; C-CDA captures core but not all metadata (e.g., chronicity, priority linkages) |
| Medications / prescriptions | ⚠️ Partial | C-CDA "Medications" section | PatientPrescription has 45 fields, PatientMedication has 17 fields — C-CDA captures subset |
| Allergies | ✅ Covered | C-CDA "Medication Allergies" section | PatientAllergy (19 fields) and PatientAllergyReaction (13 fields) — reasonable coverage |
| Immunizations | ✅ Covered | C-CDA "Immunizations" section | Present in C-CDA extract |
| Vitals | ✅ Covered | C-CDA "Vital Signs" section | PatientVital has 15 fields |
| Lab results | ✅ Covered | C-CDA "Laboratory Tests/Results" section | ActionItemResult (23 fields) and ActionItemResultValue (17 fields) — C-CDA captures core results |
| Imaging / diagnostic reports | ❌ Not covered | No specific imaging section in documented C-CDA export | Product stores ApplicationFile entries for lab/imaging results |
| Procedures | ✅ Covered | C-CDA "Procedures" section | ActionItem (49 fields) covers orders; C-CDA captures basic procedures |
| Clinical notes / documents | ❌ Not covered | C-CDA is itself a document, but does not export encounter PDFs, scanned documents, or free-text notes | Product has ScanPage/ScanPredocument/ScanSegment/ScanSession (47 fields), ApplicationFile (29 fields), PatientNote (12 fields) — significant gap |
| Care plans / goals | ✅ Covered | C-CDA "Assessment and Plan of Treatment," "Goals," "Health Concerns" | Product has PatientCarePlan and sub-entities (observations, interventions, goals, evaluation/outcomes) |
| Orders / referrals | ❌ Not covered | Not listed in C-CDA export elements | ActionItem (49 fields) covers all orders; EncounterIncomingReferral (15 fields) — gap |
| Insurance / coverage | ❌ Not covered | No insurance data in C-CDA export | PatientInsurance has 44 fields, PatientEligibilityRequest (11 fields), PatientEligibilityResponse (6 fields) — significant gap |
| Claims / billing | ❌ Not covered | No billing entities in C-CDA export | Product has CyMED/CyCLAIMS modules; ApplicationInterfaceDataQueue handles billing interface; Swagger notes "pull newly signed encounters with billable codes" — significant gap |
| Payments | ❌ Not covered | No payment data in C-CDA export | Product handles A/R management and electronic remittance — gap |
| Consents / directives | ⚠️ Partial | C-CDA may include advance directives | PatientAdvanceDirective (9 fields) — partial |
| Patient communications / portal messages | ❌ Not covered | No messaging data in C-CDA export | SecureMessage (23 fields), SecureMessageAttachment (7 fields) — gap |
| Custom forms (DDO) | ❌ Not covered | No custom form data in C-CDA export | DDO system (6 entity types, 71 fields) allows custom clinical assessments — gap |
| OB/GYN | ❌ Not covered | Not in C-CDA export elements | PatientObGyn (18 fields), EncounterObGyn (20 fields), EncounterPregnancy (22 fields) — gap |
| Pain management | ❌ Not covered | Not in C-CDA export | PatientPainHistory (20 fields), PatientPainMedicationHistory (6 fields), EncounterPainDescription (12 fields), EncounterPainFollowUp (10 fields) — gap |
| Behavioral/DSM | ❌ Not covered | Not in C-CDA export | EncounterDsm (13 fields) — gap |
| Scanned documents | ❌ Not covered | No scanned document export | 4 scanning entities (47 fields) — gap |
| Specialty-specific (ophthalmology, cardiology, etc.) | ❌ Not covered | Not in C-CDA export | PatientVision (9 fields), PatientBloodGlucose (8 fields), PatientDiabete (7 fields), PatientPulseOximetry (15 fields) — gap |

**Summary**: 7 of 21 applicable domains are covered or partially covered by the C-CDA export. 14 domains with data in the product are not exported.

## 6. Documentation Quality

**The certified (b)(10) export documentation is extremely thin:**
- A one-page Word document with boilerplate attestation text and step-by-step export instructions
- Points to the generic HL7 C-CDA 2.2 specification as the format documentation — no product-specific mapping
- No data dictionary for what's in the C-CDA export
- No documentation of which C-CDA templates are populated or which optional sections are included
- No sample export files
- No machine-readable schema for the C-CDA content

**The OData metadata is excellent but is not positioned as (b)(10) documentation:**
- 296 entity types with full property definitions (names, types, nullability, max lengths, precision)
- 438 associations with referential constraints documenting all relationships
- Machine-readable EDMX format parseable by any OData client
- However: **zero field descriptions** — all fields have names and types but no human-readable descriptions or business definitions
- No value set documentation — coded values exist in the code-set entities (36 of them) but the actual codes/values are data, not schema

**Could a developer build an import from the documentation?**
- From the C-CDA export alone: Partially — C-CDA is a well-documented standard, but without knowing which optional sections/templates Cyfluent populates, a developer would need to reverse-engineer from actual export files.
- From the OData schema: Yes, for schema structure — but without field descriptions, a developer would need to guess the semantics of many fields (e.g., what does `PatientPrescription.PrescriptionStatusName` vs `PatientPrescription.DrugStatusCode` mean?).

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The certified (b)(10) export is a C-CDA 2.2 document containing exactly the USCDI v1 data elements — the same content required for (g)(10) FHIR API certification and C-CDA transitions of care. It covers approximately 7 of 21 applicable data domains. The product stores deep clinical data across 296 entity types (3,162 fields) including billing, insurance, orders, custom forms, OB/GYN, pain management, DSM assessments, secure messaging, scanned documents, and specialty clinical data — none of which are in the C-CDA export.

The OData API *could* expose all this data, and the Swagger documentation even describes billing integration patterns ("pull newly signed encounters with billable codes … use oData to query the ApplicationInterfaceDataQueue"), but this API access is not what's certified as (b)(10). The vendor has the technical capability for a comprehensive export but chose to certify only the clinical summary.

**Axis 2 — Export approach: Repackaged existing export**

The (b)(10) export is transparently the vendor's existing C-CDA/CCD clinical exchange capability relabeled. The telltale signs are clear:
1. The attestation document points to the generic HL7 C-CDA 2.2 specification as the export format — no product-specific data dictionary
2. The export content matches USCDI v1 exactly (as documented in Program.cs comments)
3. The C# extraction utility calls `File.ashx?mode=dataccd` — the same CCD generation endpoint used for clinical exchange
4. The export menu option is literally labeled "Export Patient Data to CCD" — CCD (Continuity of Care Document) is a clinical exchange standard, not an EHI export format
5. No billing, insurance, custom form, specialty, or operational data is included despite the product storing extensive data in these domains

### Key Findings

1. **C-CDA export covers only USCDI v1 — ~7 of 21 applicable data domains.** The certified (b)(10) export is the vendor's existing CCD clinical exchange repackaged. It omits billing/claims, insurance details, custom forms (DDO), OB/GYN data, pain management, DSM assessments, scanned documents, secure messages, and specialty-specific clinical data despite all being stored in the product's 296-entity database.

2. **The OData API exposes the full database model but is not the (b)(10) export.** The EDMX metadata reveals 296 entity types with 3,162 properties — a comprehensive database schema. The Swagger API documentation describes OData access as "database CRUD operations" and shows billing integration patterns. This technical capability exists but was not certified as the EHI export mechanism.

3. **Zero field descriptions in the data dictionary.** While the OData schema has excellent structural documentation (types, nullability, max lengths, 438 associations), none of the 3,162 fields have human-readable descriptions. This limits usability for anyone trying to understand the data semantics.

4. **The attestation document is minimal.** A single page with boilerplate attestation language, export instructions, and a link to the C-CDA spec. No product-specific data dictionary, no field mapping, no sample data.

5. **123 patient-record entities with 1,556 fields are not exported.** The OData schema contains 123 entities classified as directly relevant to patient records (clinical, encounter, orders, scanning, messaging, eligibility, custom forms), totaling 1,556 properties. The C-CDA export covers perhaps 100-150 data elements from a handful of these entities.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Repackaged existing export
Export format:   C-CDA 2.2 (XML)
Entities:        296 in OData schema (not exported via b(10)); ~14-20 C-CDA sections in actual export
Fields:          3,162 in OData schema; ~100-150 in C-CDA export
Descriptions:    0% (EDMX has types but no descriptions)
Sample data:     No
Bulk export:     Yes (via CDA Extract Configuration utility)
Domains covered: 7 of 21 applicable domains
```

### Bottom Line

Cyfluent's (b)(10) export is their existing C-CDA clinical exchange relabeled — it exports USCDI v1 data (demographics, problems, meds, allergies, labs, vitals, procedures, immunizations, care plans, goals) but omits billing/claims, insurance details, custom forms, OB/GYN, pain management, DSM assessments, scanned documents, and secure messages. The irony is that Cyfluent has exceptional technical infrastructure for a comprehensive export — their OData API exposes the full 296-entity database model — but they certified only the clinical summary subset. A patient would get a clinical summary, not their complete health record.
