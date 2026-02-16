# EHI Export Analysis: TriMed Technologies

**Product**: TriMed Complete  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.05.05.3103.TRIC.01.00.1.190820  

## 1. Product Context

TriMed Complete (formerly e-Medsys) is an integrated cloud-based EHR and practice management platform from TriMed Technologies, a small vendor (~50 employees, ~$1.7M revenue) targeting independent ambulatory practices from solo providers to 400+ provider groups. The product has a notable specialty focus on pediatrics but also serves cardiology, family medicine, mental health, urgent care, and multi-specialty groups.

The product is an all-in-one platform that bundles:

- **EHR/Clinical**: Charting, problem lists, medications, allergies, vitals, immunizations, lab orders/results, clinical notes with specialty templates (pediatric growth tracking, well-child visits), clinical decision support, AI-powered ambient documentation (Amazon HealthScribe)
- **Practice Management**: Scheduling, patient registration, eligibility verification, authorization tracking, patient recall
- **Billing/RCM**: Claims management, insurance billing, EDI transactions, payment processing, collections, consolidated family balances
- **E-Prescribing**: Integrated e-Rx via Surescripts including EPCS for controlled substances
- **Patient Engagement**: Patient portal (messaging, records, billing, appointments), digital check-in, electronic forms, telemedicine
- **Document Management**: Centralized storage, AI-powered OCR for scanned documents
- **Interoperability**: FHIR R4 API (g)(10), C-CDA export, Direct messaging, HL7, immunization registry connectivity

This breadth of functionality means a genuine (b)(10) export should cover clinical data, billing/claims, scheduling metadata, patient communications, scanned documents, e-prescribing history, and specialty-specific data (e.g., pediatric growth charts).

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `ehrdisclosurev10.html` (111 KB) | Mandatory disclosure page — contains a single sentence about EHI export | ⭐ Low — the entire (b)(10) documentation is one sentence |
| `patientapi-homepage.html` (212 KB) | SOAP Patient Data API v1.3 docs — 10 methods, request/response params, hidden SQL queries | ⭐⭐⭐ High — most detailed technical documentation |
| `PatientAPI-WSDL.xml` (31 KB) | WSDL definition for 10 SOAP methods with XML Schema types | ⭐⭐ Medium — machine-readable API contract |
| `fhir-capability-statement.json` (38 KB) | FHIR R4 CapabilityStatement: 26 resources, US Core v6.1.0, Bulk Data support | ⭐⭐ Medium — shows FHIR (g)(10) scope |
| `swagger-api-spec.json` (80 KB) | OpenAPI 3.0.4 spec: 92 endpoints, 47 resource paths (schemas empty `{}`) | ⭐ Low — schemas are empty objects, limiting value |
| `FHIR-Documentation.pdf` (290 KB, 54 pages) | Sample FHIR JSON responses for 19 resource types | ⭐⭐ Medium — shows data shape but no field documentation |
| `fhirapi-page.html` (116 KB) | FHIR API overview page with auth docs and developer portal links | ⭐ Low — overview only |
| `smart-configuration.json` (1.4 KB) | SMART on FHIR OAuth2 configuration | ⭐ Low — infrastructure |
| `xml-samples/GetPatientData.xml` (37 KB) | Complete C-CDA sample with 15 clinical sections | ⭐⭐⭐ High — demonstrates actual export content |
| `xml-samples/*.xml` (8 additional files, 680 B–14 KB) | Individual C-CDA samples per data type | ⭐⭐ Medium — confirms per-type API output |
| `enrichment/database-schema-from-sql.json` (5.2 KB) | 18 Oracle database tables extracted from hidden SQL in Patient API docs | ⭐⭐⭐ High — reveals internal data model |
| `enrichment/patient-api-methods.json` (46 KB) | Detailed extraction of all 10 SOAP methods with 204 total parameters | ⭐⭐⭐ High — most complete field-level data |
| `enrichment/ccda-sections.json` (10 KB) | Parsed C-CDA section structure from all sample XML files | ⭐⭐ Medium |
| `patientapi-images/*.png` (6 images) | Postman screenshots showing request/response examples | ⭐ Low — visual confirmation only |

## 3. Export Mechanics

**Format**: C-CDA XML (via SOAP API) and FHIR R4 JSON (via REST API)

**Mechanism**: Two API-based approaches:
1. **SOAP Patient Data API** (v1.3) at `https://svcs-ccd.trimed.cloud/PatientAPI.asmx` — returns C-CDA documents. This is what the mandatory disclosure page references ("exported in XML format in CCDA architecture"). Requires practice-generated authentication keys.
2. **FHIR R4 API** at `https://fhir.trimed.cloud` — standard US Core (g)(10) API with Bulk Data support (`/Patient/$export`, `/Group/{id}/$export`).

**Single-patient vs bulk**: The SOAP API is single-patient only (requires `lPatientID`). The FHIR API supports both individual queries and bulk export.

**Access constraints**: Both APIs require authentication. The SOAP API uses practice-generated secret keys. The FHIR API uses SMART on FHIR OAuth2. No mention of fees for the export itself (pricing is $589/month per MD, $389/month per mid-level, all-inclusive).

**Triggering**: There is no documented UI-based "export my data" button. The disclosure page provides no export instructions. A technical integrator or practice administrator must use the API directly.

## 4. Export Content: What's In It

### No data dictionary exists

TriMed provides **no formal data dictionary** for their (b)(10) export. The mandatory disclosure page contains a single sentence: *"Electronic patient health information may be exported in XML format in CCDA architecture."* There is no schema document, no field listing, no mapping between internal data and export format.

What does exist is API documentation — request/response parameter tables for the SOAP API and sample responses for both APIs. This is technical API documentation, not an EHI data dictionary.

### SOAP Patient Data API — what it exports

The `GetPatientData` method accepts 34 request parameters (including 25+ boolean flags) and returns a C-CDA document with up to 42 documented response fields across these clinical domains:

| Response Domain | Fields | Example Fields |
|---|---|---|
| Encounters | 5 | Encounter type, Provider/Care Team, Location, Date, Diagnosis |
| Allergies | 5 | Allergy Name, Reaction, Severity, Timing, Concern Status |
| Problem List | 4 | Problem Name, SNOMED code, Status, Onset Date |
| Medications | 5 | Medication, Strength, Route, Dose/Frequency, Timing |
| Immunizations | 6 | Vaccine, Date, Status, Manufacturer, Lot Number, Note |
| Lab Results | 7 | LOINC code, Description, Value, Units, Flag, Range, Date |
| Vitals | 3 | Vitals Name, Timing, Value and Units |

Additional boolean flags control inclusion of: advance directives, note data, procedures, care team members, UDI (medical devices), assessment/plan, goals, health concerns, smoking status, confidential items, and demographics (name, DOB, gender, race, ethnicity, preferred language).

8 individual methods provide the same data by domain: `GetPatientAllergy`, `GetPatientProblemList`, `GetPatientMedication`, `GetPatientImmunization`, `GetPatientLabResult`, `GetPatientEncounter`, `GetPatientEncompassingEncounter`, `GetPatientVitals`.

### C-CDA Sample Content (GetPatientData.xml)

The comprehensive sample C-CDA contains 15 sections:

| C-CDA Section | LOINC | Entries |
|---|---|---|
| Encounters | — | 2 |
| Allergies and Adverse Reactions | 48765-2 | 2 |
| Conditions or Problems | — | 2 |
| Medications | — | 3 |
| Immunizations | — | 5 |
| Reason For Visit / Chief Complaint | — | 0 |
| Functional and Cognitive Status | — | 0 |
| Instructions | — | 0 |
| Reason for Referral | — | 0 |
| Procedures | — | 0 |
| Medical Devices | — | 0 |
| Assessment and Plan of Treatment | — | 0 |
| Diagnostic Results | — | 1 |
| Social History | — | 2 |
| Vital Signs | — | 1 |

### FHIR API — what it exposes

The FHIR CapabilityStatement declares 26 resource types, all conforming to US Core v6.1.0 profiles:

AllergyIntolerance, CarePlan, CareTeam, Condition, Coverage, Device, DiagnosticReport, DocumentReference, Encounter, Goal, Group, Immunization, Location, Medication, MedicationDispense, MedicationRequest, Observation, Organization, Patient, Practitioner, PractitionerRole, Procedure, Provenance, RelatedPerson, ServiceRequest, Specimen

The Swagger spec reveals additional resource paths not in the CapabilityStatement: `Consent`, `FamilyMemberHistory`, `Media`, `QuestionnaireResponse`, `CodeSystem`, `Bundle` — bringing the total to ~32 clinical resource types across 92 endpoints.

The FHIR Documentation PDF provides sample JSON responses for 19 resource types but no field-level documentation beyond what US Core requires.

### Internal Database (from hidden SQL)

The Patient API documentation contains hidden "Internal Use Only" sections with SQL queries revealing 18 Oracle database tables (prefixed `pr1_` from the e-Medsys heritage) with 111 columns total:

| Table | Columns | Purpose |
|---|---|---|
| PR1_View_Patient | 7 | Patient demographics |
| pr1_allergies | 8 | Allergy records |
| pr1_problem_list | 9 | Problem list / diagnoses |
| pr1_patient_drug | 12 | Medications |
| pr1_patient_immunization | 10 | Immunizations |
| pr1_lab_result_req | 7 | Lab order headers |
| pr1_lab_result_set | 3 | Lab result sets (panels) |
| pr1_lab_result_item | 5 | Lab result items |
| pr1_lab_result_value | 8 | Lab result values |
| pr1_lab_company_lookup | 7 | Lab facility reference |
| pr1_patient_note | 6 | Clinical notes |
| pr1_patient_note_control | 5 | Note structured data (vitals) |
| pr1_view_doctor | 5 | Provider reference |
| pr1_view_department | 7 | Department reference |
| pr1_template | 2 | Note template definitions |
| pr1_template_field | 3 | Template field definitions |
| pr1_lookups | 3 | Reference value lookup |
| pr1_view_all_diagnosis | 3 | Diagnosis code reference |

These 18 tables represent only the subset used by the Patient Data API queries. The full TriMed Complete database — with billing, scheduling, portal messaging, document management, e-prescribing, and practice management modules — almost certainly has hundreds of additional tables not exposed through either API.

### Vendor's own content organization

The vendor does not organize their documentation by data domain. The closest to a structured inventory is the SOAP API's boolean flags and C-CDA sections:

| Entity/Resource | Fields | Described | Types | Category |
|---|---|---|---|---|
| SOAP:LookupPatientId | 9 | 9 | yes | SOAP Patient Data API |
| SOAP:GetPatientData | 76 (34 req + 42 resp) | 76 | yes | SOAP Patient Data API |
| SOAP:GetPatientAllergy | 14 | 14 | yes | SOAP Patient Data API |
| SOAP:GetPatientProblemList | 14 | 14 | yes | SOAP Patient Data API |
| SOAP:GetPatientMedication | 14 | 14 | yes | SOAP Patient Data API |
| SOAP:GetPatientImmunization | 14 | 14 | yes | SOAP Patient Data API |
| SOAP:GetPatientLabResult | 14 | 14 | yes | SOAP Patient Data API |
| SOAP:GetPatientEncounter | 14 | 14 | yes | SOAP Patient Data API |
| SOAP:GetPatientEncompassingEncounter | 14 | 14 | yes | SOAP Patient Data API |
| SOAP:GetPatientVitals | 14 | 14 | yes | SOAP Patient Data API |
| FHIR resources (26 types) | 74 search params | 0 | partial | FHIR API (g)(10) |
| DB tables (18) | 111 columns | 0 | no | Oracle Database (internal) |

**Total across all sources**: 69 entities, 389 fields, 192 (49.4%) with descriptions.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export covers **standard clinical data as defined by C-CDA and USCDI**. The SOAP Patient Data API is the more detailed mechanism, providing configurable boolean flags for 25+ clinical data categories. The FHIR API covers the standard 26 US Core resource types.

**Richest areas**: Lab results (4 related database tables, 7 response fields with LOINC coding), medications (12 database columns, 5 response fields), immunizations (10 database columns, 6 response fields including manufacturer and lot number).

**Thinnest areas**: Demographics are limited to name, DOB, gender, race, ethnicity, preferred language. Encounters are documented with 5 fields (type, provider, location, date, diagnosis). Vitals have only 3 response fields.

**Completely absent**: There is no billing, scheduling, patient portal, document management, e-prescribing, or specialty-specific (e.g., pediatric growth charts) data in either API.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | GetPatientData boolean flags (name, DOB, gender, race, ethnicity, language); FHIR Patient resource | Basic demographics only. No guarantor, emergency contacts, or family account linkage data — product stores all of these. |
| Encounters / visits | ✅ Covered | GetPatientEncounter, GetPatientEncompassingEncounter; C-CDA Encounters section; FHIR Encounter | Encounter type, provider, location, date, diagnosis documented |
| Problems / conditions | ✅ Covered | GetPatientProblemList; C-CDA Conditions section; FHIR Condition | SNOMED-coded problems with status and dates |
| Medications / prescriptions | ⚠️ Partial | GetPatientMedication; C-CDA Medications section; FHIR MedicationRequest | Active medication list exported. No e-prescribing transaction history (Surescripts EPCS records, prescription fills, refill tracking). Product has full e-Rx integration. |
| Allergies | ✅ Covered | GetPatientAllergy; C-CDA Allergies section; FHIR AllergyIntolerance | Allergy name, reaction, severity, status, dates |
| Immunizations | ✅ Covered | GetPatientImmunization; C-CDA Immunizations section; FHIR Immunization | Vaccine, date, status, manufacturer, lot number |
| Vitals | ✅ Covered | GetPatientVitals; C-CDA Vital Signs section; FHIR Observation | Name, date, value with units |
| Lab results | ✅ Covered | GetPatientLabResult; C-CDA Diagnostic Results; FHIR DiagnosticReport, Observation | LOINC-coded with value, units, flag, range |
| Imaging / diagnostic reports | ⚠️ Partial | FHIR DiagnosticReport present; C-CDA has Diagnostic Results | Combined with labs; unclear if imaging-specific reports are included |
| Procedures | ✅ Covered | GetPatientData `bProcedure` flag; C-CDA Procedures section; FHIR Procedure | Present via boolean flag, but thin — no sample data in C-CDA |
| Clinical notes / documents | ⚠️ Partial | GetPatientData `bNoteData` flag; FHIR DocumentReference; DB: pr1_patient_note | Note data flag exists but only returns structured note metadata (note_datetime, template_id, doctor, department). No full-text note content visible in samples. |
| Care plans / goals | ✅ Covered | GetPatientData `bAssessmentPlan`, `bGoals`, `bHealthConcerns`; FHIR CarePlan, Goal | C-CDA Assessment and Plan section; FHIR CarePlan with text |
| Orders / referrals | ⚠️ Partial | FHIR ServiceRequest present; C-CDA Reason for Referral section | Section exists but empty in sample. Product has referral/authorization tracking not reflected here. |
| Insurance / coverage | ⚠️ Partial | FHIR Coverage resource in CapabilityStatement | No SOAP API method for insurance. FHIR Coverage resource exists but no documentation of what fields it populates from TriMed's insurance management module. |
| Claims / billing | ❌ Not covered | No billing entities in any API | **Major gap.** Product has full billing/RCM module (claims management, EDI, collections, payment processing). None of this is in the export. |
| Payments | ❌ Not covered | No payment data in any API | Product processes payments and has consolidated family balances. Not exported. |
| Consents / directives | ⚠️ Partial | GetPatientData `bAdvDirectives` flag; Swagger shows Consent resource | Advance directives flag exists. Swagger has Consent endpoints not in CapabilityStatement. |
| Patient communications / portal | ❌ Not covered | No portal message or communication entities | Product has patient portal with messaging, appointment requests, form submissions. None exported. |
| Specialty-specific (pediatrics) | ❌ Not covered | No pediatric-specific entities (growth charts, well-child visit data, developmental milestones) | **Significant gap.** Vendor markets product as "pediatric-specific by design" with growth tracking, well-child workflows, consolidated family accounts. None of this specialty data is in the export. |
| Scanned documents / images | ❌ Not covered | No document storage or image export | Product has document management with OCR. Not exported. |

## 6. Documentation Quality

**Overall: Poor to inadequate for (b)(10) purposes.**

The mandatory disclosure page's entire (b)(10) documentation is a single sentence: *"Electronic patient health information may be exported in XML format in CCDA architecture. TriMed Complete regularly updates the CCDA format to meet the current HL7 Clinical Document Architecture standards as set forth at: https://www.hl7.org/implement/standards/"*

This tells a user nothing about: how to trigger an export, what data is included, what data is excluded, what format the output takes beyond "C-CDA XML," or how to interpret the results.

**What does exist**: The SOAP Patient Data API documentation is functional API documentation with parameter tables, sample requests/responses, response codes, and authentication instructions. The FHIR API has a CapabilityStatement, Swagger spec, and sample response PDF. These are adequate for a developer integrating with the API, but they are not (b)(10) export documentation.

**What's missing**:
- No data dictionary mapping internal data to export fields
- No schema documentation (field types, constraints, value sets beyond references to SNOMED/LOINC/CVX)
- No relationships or foreign keys documented (though visible in hidden SQL)
- No export user guide for practice administrators
- No documentation of what's excluded from the export or why
- No sample export data in a downloadable format (samples are embedded in docs)
- The Swagger spec has empty `{}` schema objects, providing no machine-readable field definitions

**Could a developer build an import from this documentation?** For the clinical data in C-CDA: yes, if they know C-CDA. For anything beyond standard C-CDA sections: no. For billing, documents, specialty data: the documentation provides no information because that data isn't exported.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The export covers standard clinical data mapped to C-CDA sections — essentially the same data available through any C-CDA export or USCDI-compliant API. The 15 C-CDA sections and 26 FHIR resource types represent the regulatory floor for clinical exchange, not the designated record set. Critically, this product is an all-in-one EHR+PM+Billing platform, and the export contains **zero** billing data, **zero** practice management data, **zero** patient portal data, **zero** document management data, and **zero** specialty-specific data despite the product storing all of these. The (b)(10) documentation is a single sentence pointing to C-CDA standards with no product-specific content.

**Axis 2 — Export approach: Repackaged existing export**

The evidence is clear: TriMed's (b)(10) export is their existing C-CDA clinical exchange capability (and FHIR (g)(10) API) relabeled. The telltale signs:

1. The disclosure page references "XML format in CCDA architecture" and links to the generic HL7 CDA standard — no product-specific data dictionary or mapping.
2. The SOAP Patient Data API produces standard C-CDA documents with standard CDA sections. The 25+ boolean flags map 1:1 to standard C-CDA sections (allergies, problems, medications, etc.) — exactly what a C-CDA clinical exchange API would provide.
3. The FHIR API is explicitly a (g)(10) US Core implementation (CapabilityStatement instantiates `us-core-server`).
4. No billing, scheduling, document, portal, or specialty data is exposed — these are the domains that distinguish a genuine EHI export from a clinical summary.
5. The hidden SQL queries show the API reads from clinical tables only (allergies, problem lists, medications, labs, notes, vitals) — no billing or PM tables.

### Key Findings

1. **The (b)(10) "documentation" is a single sentence.** The mandatory disclosure page at the registered URL provides exactly one sentence about EHI export, with no data dictionary, no field documentation, no export instructions, and a link to the generic HL7 CDA standard rather than any product-specific documentation.

2. **The export is standard C-CDA/FHIR clinical exchange, not a purpose-built EHI export.** The SOAP API returns C-CDA documents with standard clinical sections. The FHIR API is a standard (g)(10) US Core implementation. Neither contains any data beyond what these standards define.

3. **Billing/RCM data is completely absent despite being a core product capability.** TriMed Complete bundles claims management, insurance billing, EDI, payment processing, and collections. None of this appears in any export API. This is perhaps the largest single gap.

4. **Pediatric specialty data is missing from a product marketed as "pediatric-specific by design."** Growth tracking, well-child visit workflows, consolidated family accounts, developmental milestones — the product's key differentiators — are not represented in the export.

5. **The hidden SQL reveals only 18 of what are likely hundreds of internal tables.** The `pr1_`-prefixed tables visible in the API documentation are exclusively clinical tables. The billing, scheduling, portal, document management, and practice management tables are not exposed through any documented mechanism.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Repackaged existing export
Export format:   C-CDA XML (SOAP API), FHIR R4 JSON (REST API)
Entities:        69 (26 FHIR resources + 10 SOAP methods + 15 C-CDA sections + 18 DB tables)
Fields:          389 (across all sources)
Descriptions:    49.4% (192 of 389 — concentrated in SOAP API params)
Sample data:     Yes (C-CDA XML samples and FHIR JSON samples in PDF)
Bulk export:     Yes (FHIR Bulk Data endpoints)
Domains covered: 8 of 19 applicable domains (clinical only)
```

### Bottom Line

TriMed Complete's (b)(10) export is its existing C-CDA and FHIR clinical exchange relabeled — it covers standard clinical domains (allergies, problems, medications, labs, vitals, immunizations, encounters) but omits billing/RCM, patient portal communications, scanned documents, e-prescribing history, and the pediatric specialty data that defines the product's market position. The (b)(10) documentation is a single sentence with no data dictionary. A patient receiving this export would get a clinical summary but would be missing their billing records, portal messages, scanned documents, and specialty clinical data.
