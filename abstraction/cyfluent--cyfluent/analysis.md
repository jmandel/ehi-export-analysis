# EHI Export Analysis: Cyfluent

**Product**: Cyfluent (CyCHART EHR + CyMED Practice Management)
**Analysis date**: 2026-02-16
**CHPL IDs**: 10072 (Version 3.2, certified 2019-08-13), 11546 (Version 3.3, certified 2024-12-11)

## 1. Product Context

Cyfluent is a comprehensive, cloud-native outpatient EHR and practice management platform developed by Planned Systems International (PSI). It serves 150+ clinical practices across the U.S. and is the system of record for HRSA's National Hansen's Disease (Leprosy) Program. The company has ~11 employees and targets solo/small ambulatory practices plus federal health programs.

The platform is modular, comprising:

- **CyCHART (EHR)**: Full clinical charting — demographics, allergies, prescriptions (including EPCS), problems, vitals, encounters, lab orders/results, procedures, CPOE, care plans, immunizations, clinical notes, custom forms (DDO/Dynamic Data Objects), OB/GYN, vision, pain management, body measurements, family/social history, advance directives, and telehealth.
- **CyMED/CyfluentPM (Practice Management)**: Billing, claims (via their own EHNAC-accredited clearinghouse CyCLAIMS), scheduling, insurance verification, charge ledger, A/R management, electronic remittance.
- **Occupational Health Module**: Work-related injuries/illnesses, OSHA compliance, hearing exams, workplace medical records.
- **Health Services Management**: Medical evacuation, travel clearance, travel immunization, mental health/substance abuse evaluations.
- **Pharmacy Fulfillment**: Inventory, shipping, barcode tracking.
- **CyPHR/CyPORTAL (Patient Portal)**: Patient-facing records, secure messaging.
- **CySCRIPT (e-Prescribing)**: Integrated prescription management.

Supports 8 medical specialties (cardiology, ophthalmology, podiatry, pulmonology, and others) plus general/family/urgent care. For EHI completeness, the export should cover clinical, billing, specialty, custom form, and patient-generated data.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `b10-EHI-Attestation-Information.docx` (45 KB) | One-page attestation + export instructions. Specifies C-CDA 2.2 as export format. Dated 2023-11-07, references version 3.2.00.3. | Low — confirms export mechanism but provides no data content detail |
| `Cyfluent-Service-Based-URL-Endpoints.docx` (14 KB) | Lists 7 FHIR API facility endpoints and links to SwaggerHub docs. | Low — FHIR API reference, not specific to b(10) |
| `ProviderPortalApi-3.3-swagger.json` (25 KB) | OpenAPI/Swagger 2.0 spec for the Provider Portal API v3.3. Four sections: FHIR, Security, oData, REST. | Medium — documents the oData and REST pathways including C-CDA pull and file retrieval |
| `OdataMetadata.xml` (796 KB) | Full OData EDMX schema for the `CfChartOpModel` namespace: **296 entity types, 3,162 properties, 876 navigation properties, 438 associations**. | **Most informative** — effectively a complete machine-readable data dictionary of the product's native data model |
| `OdataService.xml` (30 KB) | OData service document listing all 296 entity set collection endpoints. | Low — confirms entity set availability |
| `Desktop.zip` (69 KB) | Contains OdataMetadata.xml and OdataService.xml. | Container only |
| `API.zip` / `API-source/` (24 MB) | C# API client with NuGet packages, OData service references, and `Program.cs` demonstrating CDA extraction workflow. The ConnectedReference.cs (131,657 lines) defines **337 entity classes** — 41 more than the OData XML. | **High** — shows the actual extraction logic and reveals schema evolution |
| `API-source/oData Example/Program.cs` (26 KB) | Working C# code that: (1) logs in via API, (2) queries patients via oData, (3) pulls C-CDA per patient, (4) also queries individual data tables (allergies, problems, meds, vitals, prescriptions, social history, care plans, goals, devices, etc.) via oData. | High — demonstrates both C-CDA and oData extraction pathways |
| `cures-directory-listing.html` (2 KB) | IIS directory listing of the CURES documentation folder. | Low — navigation aid |
| `cyfluent-onc-certified-page-full.png` (791 KB) | Screenshot of ONC Certified page with b(10) attestation text. | Low — visual confirmation |
| `swaggerhub-api-docs.png` (207 KB) | Screenshot of SwaggerHub API documentation. | Low — visual confirmation |
| `enrichment/odata-schema.json` (982 KB) | Pre-parsed OData schema in JSON (from prior agent's enrichment script). | Medium — cross-referenced against our independent parse |

## 3. Export Mechanics

**Certified b(10) mechanism**: C-CDA 2.2 export via two pathways:

- **Single Patient**: Patient chart → scroll bar shortcut → "Export Patient Data to CCD" → downloads CDA-format XML file.
- **Bulk Export**: Utilities → Files → CDA Extract Configuration → set date range → "Extract now" → downloads CDA-format files for all patients with encounters in range.

**Format**: C-CDA 2.2 (Consolidated Clinical Document Architecture), XML. The vendor points to the HL7 C-CDA 2.2 specification (`https://build.fhir.org/ig/HL7/cda-ccda-2.2/`) as the format documentation.

**Access**: UI-driven (both single and bulk). Requires authorized Cyfluent user credentials with appropriate role-based privileges. No developer assistance required per the attestation.

**Additional pathway (not the certified b(10) mechanism)**: The vendor's oData API (`oData.svc`) provides programmatic CRUD access to all 296 entity types in the native data model. The Swagger documentation and API client code demonstrate this. However, the b(10) attestation document specifically designates the C-CDA export as the EHI export mechanism.

**Fees**: Not mentioned in any artifact.

## 4. Export Content: What's In It

### The certified export (C-CDA 2.2)

The C-CDA export content is documented only indirectly, via a comment block in `Program.cs` (lines ~230-250) listing the USCDI v1 data elements the CDA includes:

- Patient Name, Sex, Date of Birth, Race, Ethnicity, Preferred Language
- Smoking Status
- Problems
- Medications
- Medication Allergies
- Laboratory Tests and Values/Results
- Vital Signs
- Procedures
- Care Team Member(s)
- Immunizations
- Unique Device Identifier(s) for Implantable Devices
- Assessment and Plan of Treatment
- Goals
- Health Concerns

This is the **USCDI v1** data set — the same clinical summary data required for FHIR API certification under §170.315(g)(10). No vendor-specific extensions beyond the standard C-CDA sections are documented.

There is **no data dictionary specific to the C-CDA export**, no mapping from internal fields to C-CDA templates, and no sample C-CDA files.

### The native data model (via oData API)

The OData EDMX metadata (`OdataMetadata.xml`) documents the full native data model with 296 entity types. Our independent parse (`analysis/full-entity-inventory.json`) confirms:

- **296 entity types**
- **3,162 properties** (fields)
- **876 navigation properties** (relationships)
- **438 associations** (foreign key relationships with referential constraints)
- **0 field descriptions** (OData EDMX provides typed field names but no human-readable descriptions or business logic annotations)
- **1,586 non-nullable properties** (50.2% of all properties)

The newer C# ConnectedReference (from `API.zip`, dated ~2018) defines **337 entity classes** — 41 additional entities beyond the 2017 OData XML, including care plan entities (PatientCarePlan, PatientCarePlanGoal, etc.), immunization details (CodeCVX, ImmunizationForecast, etc.), implantable device tracking, GenderIdentity, SexualOrientation, and address history.

### Vendor's own content organization

The OData schema organizes entities under the `CfChartOpModel` namespace. Based on naming conventions and entity relationships, entities fall into these categories:

| Category | Entities | Properties | Nav Props | Description |
|---|---|---|---|---|
| facility-config | 64 | 617 | 228 | Facility settings, exam templates, insurance providers, code configurations |
| encounter | 43 | 525 | 134 | Encounter documentation, exams, HPI, chief complaints, diagnoses, OB/GYN, pain, DSM, prescriptions, education |
| code-sets | 36 | 231 | 59 | Standard code tables (ICD, CPT, LOINC, SNOMED, allergies, medications, diets, etc.) |
| patient | 34 | 557 | 135 | Demographics, allergies, prescriptions, problems, vitals, insurance, family/social history, body measurements, vision, advance directives, notes, blood glucose, pulse oximetry, OB/GYN, pain |
| other | 33 | 387 | 48 | Mixed: body measurement norms, PQRI/MU measures, company, lab, procedure modifiers |
| orders/actions | 25 | 248 | 81 | Lab/procedure orders, results, result values, administered medications, order types/priorities/statuses |
| application | 23 | 218 | 65 | Files, faxes, audit logs, users/roles, security, interface data queue, form definitions |
| clinical-templates | 9 | 110 | 33 | DDO (Dynamic Data Objects) custom forms, HPI templates, widgets |
| reporting | 9 | 81 | 5 | Report queue, patient report summaries |
| geography | 5 | 27 | 10 | City, state, county, country, ZIP |
| location | 4 | 44 | 13 | Multi-location support |
| scanning | 4 | 47 | 19 | Document scanning sessions, pages, segments, pre-documents |
| eligibility | 3 | 11 | 4 | Insurance eligibility requests/responses |
| human-resources | 2 | 29 | 36 | Provider/staff records |
| messaging | 2 | 30 | 6 | Secure messages and attachments |

**Largest/most important entities (by property count):**

| Entity | Props | Nav Props | Category | Notes |
|---|---|---|---|---|
| PqriMeasure | 135 | 4 | other | Quality reporting measures |
| Facility | 76 | 86 | facility-config | Master facility configuration |
| Patient | 71 | 57 | patient | Core patient demographics + 57 navigation links |
| ActionItem | 49 | 16 | orders/actions | Orders (labs, procedures, referrals) with full lifecycle |
| PatientPrescription | 45 | 5 | patient | Prescription records (drug, directions, quantity, refills, pharmacy, status) |
| PatientInsurance | 44 | 5 | patient | Insurance coverage details |
| Encounter | 43 | 51 | encounter | Visit record with 51 navigation links to sub-components |
| PatientAudit | 35 | 3 | patient | Patient record audit trail |
| EncounterPersistenceCache | 32 | 1 | encounter | Encounter state caching |
| ApplicationFile | 29 | 14 | application | Document/file storage records |
| EncounterAudit | 27 | 3 | encounter | Encounter audit trail |
| EncounterChiefComplaint | 26 | 3 | encounter | Chief complaint documentation |
| PatientSocialHistory | 26 | 2 | patient | Social history including smoking status |
| HumanResource | 26 | 35 | human-resources | Provider/staff records |
| PatientContact | 24 | 1 | patient | Patient contact information |
| Lab | 24 | 6 | other | Lab entity configuration |
| ActionItemResult | 23 | 7 | orders/actions | Order results with documents, review status |
| PatientProblem | 23 | 4 | patient | Problem list with onset, resolution, severity, chronicity |
| SecureMessage | 23 | 3 | messaging | Patient-provider secure messaging |
| EncounterPregnancy | 22 | 1 | encounter | Pregnancy tracking |

The full inventory of all 296 entities with every property is in `analysis/full-entity-inventory.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

**The certified b(10) export (C-CDA 2.2)** covers only the USCDI v1 clinical summary: demographics, problems, medications, allergies, labs, vitals, procedures, immunizations, care plans/goals, implantable devices, and health concerns. This is the standard C-CDA clinical document content — a clinical transitions-of-care summary, not a comprehensive EHI export.

**The native data model (exposed via oData but NOT the certified export)** is genuinely comprehensive. The `patient` category alone has 34 entities with 557 properties covering demographics (71 fields on Patient), prescriptions (45 fields), insurance (44 fields), allergies (19 fields), problems (23 fields), vitals (15 fields), social history (26 fields), contacts (24 fields), body measurements, vision, OB/GYN, advance directives, pain history, blood glucose, pulse oximetry, diet, ethnicity, race, and family history.

The `encounter` category has 43 entities with 525 properties covering the full encounter documentation model: chief complaints, HPI, exams (with nested sections, items, groups), diagnoses, prescriptions, education, pain descriptions, OB/GYN, pregnancy, DSM assessments, risk factors, incoming referrals, associated providers, and custom form (DDO) data.

The `orders/actions` category has 25 entities with 248 properties covering the complete order lifecycle: actionable items, orders, results, result values, administered medications, code associations (CPT, ICD, SNOMED, LOINC), and the interface data queue for billing integration.

The `messaging` category has 2 entities (23 + 7 = 30 properties) for secure patient-provider messaging.

The `scanning` category has 4 entities (47 properties) for scanned document storage.

However, notable gaps exist even in the native model relative to the product's advertised capabilities:
- **No explicit billing/claims entities** — The oData schema has `PatientInsurance` (44 fields) and `PatientEligibilityRequest`/`Response`, plus an `ApplicationInterfaceDataQueue` for billing interface handoff. But there are no dedicated claims, charges, payments, A/R, or charge ledger entities. The Swagger documentation mentions using the `ApplicationInterfaceDataQueue` for billing clients to pull encounter data with billable codes. This suggests billing may be in a separate system/database.
- **No occupational health entities** — Despite the product advertising an occupational health module.
- **No pharmacy fulfillment entities** — Despite the product advertising pharmacy shipping/inventory.
- **No health services management entities** — Despite advertising medical evacuation, travel clearance, and mental health modules.

These specialized modules may exist in separate databases or may be accessed through different APIs not represented in the OData metadata.

### 5b. Standardized domain coverage (top-down)

Assessment of the **certified C-CDA export** (what patients actually get via the b(10) mechanism):

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA includes name, sex, DOB, race, ethnicity, language | C-CDA covers basic demographics. The native model has 71 fields on Patient (contacts, identifiers, account numbers, etc.) — most are lost in C-CDA. |
| Encounters / visits | ⚠️ Partial | C-CDA documents encounters implicitly via clinical content | The native model has 43 encounter entities with 525 properties (HPI, chief complaints, exam sections with nested items/groups, pain, OB/GYN, pregnancy, DSM, risk factors). C-CDA captures only a summary. |
| Problems / conditions | ✅ Covered | C-CDA "Problems" section | Likely includes active problem list, though depth of chronicity/priority metadata from the native 23-field PatientProblem is unknown. |
| Medications / prescriptions | ✅ Covered | C-CDA "Medications" section | The native PatientPrescription has 45 fields (drug, directions, quantity, days supply, refills, pharmacy, prescriber, notes, controlled substance status, etc.). C-CDA captures the medication list but likely loses prescribing workflow details. |
| Allergies | ✅ Covered | C-CDA "Medication Allergies" section | Native model has PatientAllergy (19 fields) + PatientAllergyReaction (13 fields). C-CDA likely captures the core allergy info. |
| Immunizations | ✅ Covered | C-CDA "Immunizations" section | Basic immunization records included. The newer schema adds CodeCVX, ImmunizationForecast, and other vaccine-specific entities. |
| Vitals | ✅ Covered | C-CDA "Vital Signs" section | Native PatientVital has 15 fields. C-CDA captures standard vitals. |
| Lab results | ✅ Covered | C-CDA "Laboratory Tests and Values/Results" | Native ActionItemResult (23 fields) + ActionItemResultValue (17 fields) provide detailed results. C-CDA captures standard lab values. |
| Imaging / diagnostic reports | ❌ Not covered | No imaging data in C-CDA export | Product supports DICOM and document storage (ApplicationFile with 29 fields). Not exported via C-CDA. |
| Procedures | ✅ Covered | C-CDA "Procedures" section | Basic procedure records included. |
| Clinical notes / documents | ⚠️ Partial | C-CDA captures Assessment/Plan of Treatment | Native model has PatientNote (12 fields), encounter documentation (43 entities), scanned documents (4 entities/47 fields). C-CDA captures only structured clinical summaries. |
| Care plans / goals | ✅ Covered | C-CDA "Goals" and "Health Concerns" sections | The newer schema (2018 ConnectedReference) adds PatientCarePlan with sub-entities for goals, observations, interventions, health concerns, and evaluation/outcomes. |
| Orders / referrals | ❌ Not covered | No orders in C-CDA export | Native ActionItem (49 fields) covers full order lifecycle. Not exported via C-CDA. |
| Insurance / coverage | ❌ Not covered | No insurance data in C-CDA export | Native PatientInsurance has 44 fields. Not in C-CDA. Significant gap — product stores detailed insurance data. |
| Claims / billing | ❌ Not covered | No billing data in C-CDA export | Product has CyMED/CyCLAIMS billing modules with charge ledger, claims, remittance. No billing entities visible in the oData schema either — may be in a separate system. |
| Payments | ❌ Not covered | No payment data in C-CDA export | Product handles payments through billing module. Not exported. |
| Consents / directives | ❌ Not covered | Not in C-CDA export | Native PatientAdvanceDirective has 9 fields. Not in C-CDA. |
| Patient communications | ❌ Not covered | No messaging data in C-CDA export | Native SecureMessage has 23 fields + SecureMessageAttachment has 7 fields. Not exported. |
| Custom forms (DDO) | ❌ Not covered | No custom form data in C-CDA export | Product has a custom forms builder (9 DDO entities, 110 properties). Not representable in C-CDA. |
| Specialty data (OB/GYN) | ❌ Not covered | No OB/GYN data in C-CDA export | PatientObGyn (18 fields), EncounterObGyn (20 fields), EncounterPregnancy (22 fields) — not in C-CDA. |
| Specialty data (pain mgmt) | ❌ Not covered | No pain data in C-CDA export | PatientPainHistory (20 fields), EncounterPainDescription (12 fields), EncounterPainFollowUp (10 fields) — not in C-CDA. |
| Specialty data (vision) | ❌ Not covered | No vision data in C-CDA export | PatientVision (9 fields) — not in C-CDA. |
| Scanned documents | ❌ Not covered | No scanned docs in C-CDA export | ScanPage/ScanPredocument/ScanSegment/ScanSession (47 fields total). Not exported. |

**Summary**: Of ~20 applicable domains, the C-CDA export covers **7 fully** and **3 partially**. **10+ domains** with data in the native model are completely absent from the certified export.

## 6. Documentation Quality

**For the certified C-CDA export**: Documentation is **minimal**. The b(10) attestation document (`b10-EHI-Attestation-Information.docx`) is a single page with step-by-step UI instructions and a link to the external C-CDA 2.2 specification. It provides no:
- Data dictionary or mapping from internal fields to C-CDA sections
- List of which C-CDA templates/sections are populated
- Sample export files
- Information about what data is or isn't included
- Vendor-specific extensions or customizations

A developer could not determine what data is in the export from this documentation alone. They would need to perform an actual export and reverse-engineer the content.

**For the oData API (not the certified export)**: Documentation is **strong technically but lacks semantic context**:
- The OData EDMX metadata XML is a complete, machine-readable schema with entity types, typed properties (Edm.String, Edm.DateTime, Edm.Boolean, etc.), nullability, max lengths, and fully documented relationships via 438 associations with referential constraints.
- The Swagger spec documents API endpoints with request/response examples.
- The C# API client (`API.zip`) provides runnable code demonstrating the full extraction workflow.
- However, **zero fields have human-readable descriptions**. Property names are the only clue to semantics (e.g., `PatientPrescription.DrugName`, `Encounter.EncounterStartDateTime`). No value sets, no business rules, no documentation of what values mean.
- The OData metadata XML dates from 2017. The C# ConnectedReference from 2018 has 41 additional entities. The current production schema (v3.3) likely has more.

## 7. Overall Assessment

### Classification

**Standard-based projection.** The certified b(10) export is a C-CDA 2.2 clinical summary — a standard clinical document format repackaged as the EHI export. It covers the USCDI v1 data elements (the same content required for FHIR API access under g(10)) and misses the majority of what the product stores. While the vendor has an oData API that exposes the full 296-entity native data model, this is not the certified b(10) export mechanism and requires API credentials and custom development to use.

### Key Findings

1. **The certified b(10) export is C-CDA 2.2 — a clinical summary, not a comprehensive EHI export.** The attestation document (`b10-EHI-Attestation-Information.docx`) and Program.cs comments confirm the export covers only USCDI v1 data elements: demographics, problems, medications, allergies, labs, vitals, procedures, immunizations, care plans, goals, and implantable devices. This is the same content available through the FHIR API.

2. **The vendor's native data model is far richer than what the export delivers.** The OData EDMX schema (`OdataMetadata.xml`) documents 296 entity types with 3,162 properties — including 34 patient entities (557 properties), 43 encounter entities (525 properties), 25 orders/actions entities (248 properties), custom form templates (DDO), secure messaging, scanned documents, and insurance data. The C-CDA export captures perhaps 10-15% of this.

3. **The oData API technically provides access to the full data model, but it is not the b(10) mechanism.** The Swagger documentation describes the oData endpoint as "database CRUD operations" for general-purpose use. It could theoretically serve as a comprehensive export, but the vendor has explicitly designated C-CDA as the b(10) export format in their attestation.

4. **Billing data appears absent even from the native oData schema.** Despite the product having CyMED/CyCLAIMS billing modules (charge ledger, claims, electronic remittance, A/R), the OData schema has no dedicated billing, claims, charge, or payment entities. The `ApplicationInterfaceDataQueue` serves as a billing interface handoff point, suggesting billing may live in a separate database. This is a gap even in the best-case oData scenario.

5. **Documentation quality is split.** The OData schema is an excellent machine-readable artifact (typed properties, relationships, nullability, max lengths for all 3,162 fields), but the C-CDA export documentation is a single page with no content specification. There are no field descriptions anywhere, no sample data, and no vendor-specific mapping guide.

### Summary Stats

    Classification:  Standard-based projection
    Export format:   C-CDA 2.2 (XML)
    Model type:      Standard projection (C-CDA clinical document)
    Entities:        296 in native model (OData schema); ~14 C-CDA sections in actual export
    Fields:          3,162 in native model; ~100-150 in C-CDA export (estimated)
    Descriptions:    0% (no field descriptions in any artifact)
    Sample data:     No
    Bulk export:     Yes (date-range-based CDA extraction)
    Domains covered: 7-10 of 20 applicable domains (clinical summary only; no billing, insurance, custom forms, specialty, messaging, documents, orders)

### Bottom Line

The Cyfluent b(10) export is a C-CDA 2.2 clinical summary that covers approximately the USCDI v1 data set — the same content already available through the FHIR API. This is a textbook case of C-CDA/FHIR repackaging as "(b)(10)." The product stores far more data across 296+ native entities (encounter details, custom forms, insurance, pain management, OB/GYN, secure messages, scanned documents, orders) that is completely absent from the export. The single biggest gap is the absence of the rich encounter documentation (43 entities, 525 properties) and insurance/billing data from a product that operates its own claims clearinghouse.
