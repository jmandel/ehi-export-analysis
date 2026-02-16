# EHI Export Analysis: TriMed Technologies

**Product**: TriMed Complete (formerly e-Medsys)
**Analysis date**: 2026-02-16
**CHPL ID**: 10076
**CHPL Product Number**: 15.05.05.3103.TRIC.01.00.1.190820

## 1. Product Context

TriMed Complete is an integrated, cloud-based EHR and practice management platform targeting independent ambulatory practices from solo providers to 400+ provider groups. It was originally developed as "e-Medsys" and acquired by TriMed Technologies in 2010. The product has a notable specialty focus on **pediatrics** ("pediatric-specific by design") and also serves cardiology, family medicine, mental health, and multi-specialty practices. It is hosted on AWS.

The platform is an all-in-one system bundling:

- **EHR/Clinical**: Charting with customizable/specialty templates, problem lists, medication lists, allergies, vitals, immunizations, clinical decision support, growth tracking (pediatric), CPOE (meds, labs, imaging), clinical notes, care plans, goals
- **E-Prescribing**: Integrated with Surescripts, including EPCS for controlled substances
- **Practice Management**: Appointment scheduling, patient registration, eligibility verification, authorization/referral tracking, patient recall
- **Billing/RCM**: Claims management, insurance claim processing, electronic billing/EDI, collections, credit posting, consolidated family balances (pediatric), online bill pay
- **Patient Engagement**: Patient portal (records, messaging, appointments, billing), digital check-in, electronic forms, appointment reminders
- **Document Management**: Centralized document storage with AI-powered OCR
- **Telemedicine**: Integrated telemedicine platform
- **AI/Ambient**: Integration with Amazon HealthScribe for ambient clinical documentation

This product stores comprehensive patient data across clinical, administrative, billing, and communication domains. An adequate (b)(10) export should cover clinical records, billing/claims data, prescription history, scanned documents, and patient-generated content.

## 2. Artifacts Reviewed

| Artifact | File | Size | What it told me |
|---|---|---|---|
| **EHI Disclosure page** | `ehrdisclosurev10.html` | 110 KB | Single-sentence EHI export statement: data exported "in XML format in CCDA architecture." No data dictionary, no export instructions. **Least informative.** |
| **Patient Data API docs** | `patientapi-homepage.html` | 212 KB | SOAP API v1.3 documentation with 10 methods, parameter tables, sample requests/responses. Hidden SQL reveals Oracle database tables. **Most informative artifact.** |
| **Patient API WSDL** | `PatientAPI-WSDL.xml` | 31 KB | SOAP WSDL with XML Schema definitions for all 10 methods. Confirms API structure. |
| **Patient API methods (parsed)** | `enrichment/patient-api-methods.json` | 46 KB | Structured extraction: 10 methods, 121 request params, 83 response params. |
| **Database schema (from SQL)** | `enrichment/database-schema-from-sql.json` | 5 KB | 18 Oracle tables, 111 columns, extracted from hidden "Internal Use Only" SQL queries. |
| **C-CDA samples (9 files)** | `xml-samples/*.xml` | 680 B–37 KB | Sample C-CDA responses for each API method. `GetPatientData.xml` (37 KB) is the comprehensive export with 15 clinical sections. |
| **FHIR CapabilityStatement** | `fhir-capability-statement.json` | 38 KB | 26 FHIR R4 resources, US Core v6.1.0, bulk data support declared. |
| **FHIR OpenAPI spec** | `swagger-api-spec.json` | 80 KB | 92 endpoints covering 33 clinical resource types (7 beyond CapabilityStatement). Response schemas are empty `{}` objects. |
| **FHIR Documentation PDF** | `FHIR-Documentation.pdf` | 290 KB, 54 pages | Sample JSON responses for 19 of 26 FHIR resource types. |
| **FHIR API page** | `fhirapi-page.html` | 116 KB | FHIR API overview, authentication, endpoints. Links to developer portal and docs. |
| **SMART configuration** | `smart-configuration.json` | 1.4 KB | OAuth2 endpoints and supported scopes for SMART on FHIR. |
| **Enrichment scripts** | `enrichment/*.ts` | 4–11 KB | Automated extraction scripts (patient API, FHIR API, C-CDA sections). |
| **C-CDA sections (parsed)** | `enrichment/ccda-sections.json` | 10 KB | Template IDs from 9 XML samples (note: undercounts sections due to parsing limitations). |
| **Screenshots** | `*.png` | 225 KB–9.4 MB | Visual documentation of API pages and Postman examples. |

## 3. Export Mechanics

**Format**: C-CDA XML (via SOAP Patient Data API); FHIR R4 JSON (via FHIR API)

**Mechanism**: API-based. Both export paths require programmatic API calls:

1. **SOAP Patient Data API** (the mechanism referenced in the mandatory disclosure): Requires practice-generated authentication keys. Single-patient retrieval via `GetPatientData` (comprehensive) or 8 individual data-type methods. Endpoint: `https://svcs-ccd.trimed.cloud/PatientAPI.asmx`

2. **FHIR R4 API**: SMART on FHIR OAuth2 authentication. Supports per-patient queries and declares bulk data export capability (`/Patient/$export`, `/Group/{id}/$export`). Endpoint: `https://fhir.trimed.cloud`

**Single-patient vs bulk**: The SOAP API is single-patient only (requires `lPatientID`). The FHIR API declares bulk data support via the CapabilityStatement's instantiation of `http://hl7.org/fhir/uv/bulkdata/CapabilityStatement/bulk-data`.

**Access constraints**: Both APIs require authentication. The SOAP API needs a practice-generated secret key. The FHIR API uses OAuth2/SMART. No mention of fees for data export.

**No UI-based export described**: The mandatory disclosure page contains no instructions for triggering an export through the product's UI. The only documented mechanisms are API calls, which require developer integration.

## 4. Export Content: What's In It

### The C-CDA Export (SOAP Patient Data API)

The primary export mechanism produces C-CDA 2.1 documents. The `GetPatientData` method accepts 25 boolean parameters to control which data categories to include, plus date-range filters.

**Response fields documented**: 42 response parameters across 8 data categories (Encounters: 5, Allergies: 5, Problem List: 4, Medications: 5, Immunizations: 6, Lab Results: 7, Vitals: 3, and header/group fields: 7). Of these, **37 unique clinical fields** have descriptions (85.5% description coverage); 5 group headers have no descriptions (they're section labels like "Encounters", "Allergies").

**C-CDA sections in the comprehensive export** (`GetPatientData.xml`, 15 sections):

| Section | LOINC Code | Content |
|---|---|---|
| Encounters | 46240-8 | Type, provider, location, date, diagnosis |
| Allergies and Adverse Reactions | 48765-2 | Name, reaction, severity, date, status |
| Conditions or Problems | 11450-4 | Description, SNOMED code, status, onset date |
| Medications | 10160-0 | Drug name, strength, route, frequency, date |
| Immunizations | 11369-6 | Vaccine, date, status, manufacturer, lot number |
| Reason For Visit - Chief Complaint | 29299-5 | Free text |
| Functional and Cognitive Status | 47420-5 | Status entries |
| Instructions | 69730-0 | Patient instructions |
| Reason for Referral | 42349-1 | Referral text |
| Procedures | 47519-4 | Procedure entries |
| Medical Devices | 46264-8 | UDI information |
| Assessment and Plan of Treatment | 18776-5 | Assessment/plan text |
| Diagnostic Results | 30954-2 | LOINC code, description, value, units, flag, range, date |
| Social History | 29762-2 | Smoking status |
| Vital Signs | 8716-3 | Measurement name, date, value/units |

### Underlying Database Schema (from hidden SQL)

The "Internal Use Only" sections in the Patient API docs reveal an Oracle database with tables prefixed `pr1_` (from the original e-Medsys product). 18 tables with 111 total columns were identified:

| Table | Columns | Used By | Category |
|---|---|---|---|
| PR1_View_Patient | 7 | LookupPatientId | Demographics |
| pr1_allergies | 8 | GetPatientAllergy | Allergies |
| pr1_lookups | 3 | Multiple methods | Reference data |
| pr1_problem_list | 9 | GetPatientProblemList | Problems |
| pr1_view_all_diagnosis | 3 | GetPatientProblemList | Reference data |
| pr1_patient_drug | 12 | GetPatientMedication | Medications |
| pr1_patient_immunization | 10 | GetPatientImmunization | Immunizations |
| pr1_lab_result_req | 7 | GetPatientLabResult | Lab results |
| pr1_lab_result_set | 3 | GetPatientLabResult | Lab results |
| pr1_lab_result_item | 5 | GetPatientLabResult | Lab results |
| pr1_lab_result_value | 8 | GetPatientLabResult | Lab results |
| pr1_lab_company_lookup | 8 | GetPatientLabResult | Reference data |
| pr1_patient_note | 6 | GetPatientEncounter | Notes/encounters |
| pr1_patient_note_control | 5 | GetPatientVitals | Vitals |
| pr1_view_doctor | 5 | GetPatientEncounter | Providers |
| pr1_view_department | 7 | GetPatientEncounter | Locations |
| pr1_template | 2 | GetPatientEncounter | Configuration |
| pr1_template_field | 3 | GetPatientVitals | Configuration |

These 18 tables represent only the tables used by the patient data API's SQL queries. The actual database likely has many more tables for billing, scheduling, documents, patient portal, etc. — none of which are exposed through the export.

### The FHIR API

The FHIR CapabilityStatement declares 26 resources conforming to US Core v6.1.0 / USCDI v3. The OpenAPI spec covers 33 resource types across 92 endpoints (7 additional types beyond the CapabilityStatement: Bundle, CodeSystem, Consent, FamilyMemberHistory, Media, QuestionnaireResponse, ConditionCreate).

The 54-page FHIR Documentation PDF provides sample JSON responses for 19 of the 26 CapabilityStatement resources (missing: Coverage, MedicationDispense, DocumentReference, Medication, RelatedPerson, ServiceRequest, Specimen).

**Note**: The FHIR API is the product's g(10) Standardized API, not specifically a b(10) EHI export mechanism. The mandatory disclosure page references only the C-CDA export.

### Vendor's own content organization

The vendor organizes export content by API method. Each method corresponds to a clinical data category:

| API Method / Entity | Response Fields | Fields with Descriptions | Types | Category |
|---|---|---|---|---|
| LookupPatientId | 1 | 1 (100%) | Yes | Demographics |
| GetPatientData (comprehensive) | 42 | 37 (88%) | All string | Comprehensive Clinical |
| GetPatientAllergy | 5 | 5 (100%) | All string | Allergies |
| GetPatientProblemList | 4 | 4 (100%) | All string | Problems/Conditions |
| GetPatientMedication | 5 | 5 (100%) | All string | Medications |
| GetPatientImmunization | 6 | 6 (100%) | All string | Immunizations |
| GetPatientLabResult | 7 | 7 (100%) | All string | Lab Results |
| GetPatientEncounter | 5 | 5 (100%) | All string | Encounters |
| GetPatientEncompassingEncounter | 5 | 0 (0%) | All string | Encounters |
| GetPatientVitals | 3 | 3 (100%) | All string | Vitals |

**Notable**: GetPatientEncompassingEncounter has 5 response fields but **zero descriptions** — the only method with completely undocumented responses.

Full inventory saved to: `analysis/full-entity-inventory.json`

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export covers **standard clinical summary data** organized around 8 data categories, all delivered as C-CDA XML:

1. **Demographics** (via LookupPatientId and GetPatientData boolean flags): Name, DOB, gender, race, ethnicity, preferred language. Limited to basic demographics — no address, phone, insurance, emergency contacts, or guarantor info in the documented response fields.

2. **Allergies** (GetPatientAllergy): Name, reaction, severity, timing, status. Reasonably complete for allergy data.

3. **Problems/Conditions** (GetPatientProblemList): Description, SNOMED code, status, onset date. SNOMED-coded.

4. **Medications** (GetPatientMedication): Drug name, strength, route, frequency, prescribed date. Active medications. No medication administration records or e-prescribing history.

5. **Immunizations** (GetPatientImmunization): Vaccine, date, status, manufacturer, lot number, notes. CVX-coded.

6. **Lab Results** (GetPatientLabResult): LOINC code, description, value, units, flag, range, date. Multi-table structure (request/set/item/value) in the database. Well-structured.

7. **Encounters** (GetPatientEncounter, GetPatientEncompassingEncounter): Type, provider, location, date, diagnosis. Encounter data derived from clinical notes (`pr1_patient_note` table).

8. **Vitals** (GetPatientVitals): Measurement name, date, value/units. Stored in the `pr1_patient_note_control` table as structured data within notes.

Additionally, the comprehensive `GetPatientData` method includes C-CDA sections for procedures, medical devices (UDI), assessment/plan, social history, functional status, instructions, and reason for referral — but these appear as embedded C-CDA sections, not as separately documented response fields.

The FHIR API adds Coverage (insurance), DocumentReference, ServiceRequest, MedicationDispense, RelatedPerson, and Specimen beyond the SOAP API. However, the FHIR API is a g(10) API, not specifically the b(10) export mechanism.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | `LookupPatientId` (7 DB columns), GetPatientData boolean flags (name, DOB, gender, race, ethnicity, language) | Only basic demographics. Product stores addresses, phone, emergency contacts, guarantor info, family linkages — not in documented export response fields. |
| Encounters / visits | ✅ Covered | `GetPatientEncounter`, `GetPatientEncompassingEncounter` (5 response fields each), C-CDA Encounters section | Encounter type, provider, location, date, diagnosis covered. |
| Problems / conditions / diagnoses | ✅ Covered | `GetPatientProblemList` (4 fields), SNOMED-coded via `pr1_problem_list` table | Adequate: problem name, code, status, onset date. |
| Medications / prescriptions | ⚠️ Partial | `GetPatientMedication` (5 fields) | Active medications covered. E-prescribing history (EPCS, Surescripts transaction records) not included. No medication administration records. |
| Allergies | ✅ Covered | `GetPatientAllergy` (5 fields) | Name, reaction, severity, timing, status. |
| Immunizations | ✅ Covered | `GetPatientImmunization` (6 fields) | Vaccine, date, status, manufacturer, lot, notes. Well-documented. |
| Vitals | ✅ Covered | `GetPatientVitals` (3 fields), C-CDA Vital Signs section | Name, date, value/units. |
| Lab results | ✅ Covered | `GetPatientLabResult` (7 fields), 4 database tables for lab structure | LOINC-coded, value/units/flag/range. Well-structured. |
| Imaging / diagnostic reports | ⚠️ Partial | C-CDA "Diagnostic Results" section present, no dedicated API method | Results visible in C-CDA but no dedicated imaging report export. Product supports imaging orders (CPOE). |
| Procedures | ✅ Covered | C-CDA "Procedures" section in GetPatientData, `bProcedure` boolean flag | Present as a C-CDA section; no dedicated API method with documented fields. |
| Clinical notes / documents | ⚠️ Partial | `pr1_patient_note` and `pr1_patient_note_control` tables, `bNoteData` flag, encounter methods | Note metadata (datetime, provider, template) exported. Full note text/content is unclear — the API returns C-CDA sections, not raw note content. |
| Care plans / goals | ⚠️ Partial | `bGoals`, `bHealthConcerns`, `bAssessmentPlan` boolean flags; C-CDA Assessment and Plan section | Boolean flags exist but no dedicated response fields documented. FHIR CarePlan/Goal resources available separately. |
| Orders / referrals | ⚠️ Partial | C-CDA "Reason for Referral" section; `bLabTests` flag | Referral reason as free text. Lab orders via result structure. No dedicated orders export. |
| Insurance / coverage | ❌ Not covered | No insurance data in SOAP API response fields | Product stores insurance information (eligibility verification, authorization tracking). FHIR API has Coverage resource but the b(10) C-CDA export does not include insurance. **Significant gap.** |
| Claims / billing | ❌ Not covered | No billing entities in any export mechanism | Product has full billing/RCM: claims management, EDI, collections, consolidated family balances. None exported. **Significant gap.** |
| Payments | ❌ Not covered | No payment data in export | Product processes payments (credit/debit, online bill pay). Not exported. **Significant gap.** |
| Consents / directives | ⚠️ Partial | `bAdvDirectives` boolean flag in GetPatientData; FHIR OpenAPI has Consent endpoint | Advance directives flag exists but no documented response fields. |
| Patient communications / portal messages | ❌ Not covered | No messaging or portal data in export | Product has patient portal with messaging, secure communications, digital check-in. Not exported. **Gap.** |
| Specialty-specific (pediatrics) | ❌ Not covered | No pediatric-specific data elements in export | Product is marketed as "pediatric-specific by design" with growth tracking, well-child visit workflows, vaccine tracking, consolidated family balances. Growth data and pediatric-specific workflows not in export. **Gap given product positioning.** |
| Scanned documents / images | ❌ Not covered | No document export mechanism in SOAP API | Product has document management with AI-powered OCR. FHIR has DocumentReference but not in b(10) export. **Gap.** |

## 6. Documentation Quality

**For the SOAP Patient Data API**: The API documentation is reasonably well-done for what it covers:
- Each method has a clear description, request parameter table (name, type, required, description), and response parameter table
- Sample SOAP request/response XML provided for each method
- Sample C-CDA responses demonstrate actual data structure with realistic synthetic data
- Authentication workflow documented step-by-step with Postman screenshots
- Date filtering capabilities clearly documented
- Response codes documented (1=success, 2=invalid auth, 3=patient not found, etc.)

**Weaknesses**:
- All response field types are documented as "string" — no differentiation for dates, codes, numbers
- No formal data dictionary separate from the API docs
- No ERD or relationship documentation (foreign keys only visible in hidden SQL)
- No value sets documented (references external standards: SNOMED, LOINC, CVX)
- The hidden "Internal Use Only" SQL queries are the most revealing artifact but are not intended for external consumption
- `GetPatientEncompassingEncounter` has 5 response fields with zero descriptions

**For the FHIR API**: Adequate but shallow:
- CapabilityStatement and SMART configuration are machine-readable (good)
- OpenAPI spec exists but response schemas are empty `{}` objects (not useful for understanding data structure)
- 54-page PDF with sample JSON responses for 19 of 26 resource types (helpful but not comprehensive)
- No vendor-specific extensions documented
- No data dictionary mapping FHIR resources to internal database fields

**For the mandatory disclosure page**: The entire EHI export documentation is one sentence: *"Electronic patient health information may be exported in XML format in CCDA architecture."* This provides no actionable information about what data is exported, how to trigger an export, what format the data takes beyond "XML/CCDA," or what data categories are included.

**Could a developer build an import?** A developer could reconstruct clinical summary data from the C-CDA XML output using the sample responses and parameter documentation. However, they would have no way to import billing, documents, portal data, or specialty-specific data because none of these are in the export. The documentation is sufficient for the clinical data it covers but provides no insight into the ~60% of product data that is not exported.

## 7. Overall Assessment

### Classification

**Standard-based projection.** The EHI export is a C-CDA clinical summary repackaged as a (b)(10) export. It covers the same clinical data categories as any C-CDA Continuity of Care Document — demographics, allergies, medications, problems, immunizations, labs, vitals, encounters, and procedures. It does not export the vendor's native data model and omits entire categories of data the product stores (billing, insurance, documents, patient portal data, specialty-specific data, e-prescribing history).

The FHIR API provides a second standard-based projection (US Core / USCDI v3) with slightly broader resource coverage (adding Coverage, DocumentReference, ServiceRequest), but this is the g(10) API, not specifically a (b)(10) export.

### Key Findings

1. **The (b)(10) export is a C-CDA clinical summary, not an "all EHI" export.** The mandatory disclosure page explicitly says data is exported "in XML format in CCDA architecture." The SOAP API produces C-CDA documents covering ~15 clinical sections. This is a standard clinical summary — the same data available through any C-CDA export — not the full designated record set. (Source: `ehrdisclosurev10.html`, `patientapi-homepage.html`)

2. **Billing and financial data are completely absent.** TriMed Complete includes full billing/RCM capabilities (claims management, EDI, collections, consolidated family balances, payment processing), but zero billing entities appear in either the SOAP API or FHIR API export. This is a significant gap given that billing records are explicitly part of the HIPAA designated record set. (Source: `enrichment/patient-api-methods.json` — no billing-related methods; `enrichment/database-schema-from-sql.json` — no billing tables visible)

3. **The product's pediatric specialty focus is not reflected in the export.** TriMed markets itself as a "pediatric-specific by design" EHR with growth tracking, well-child visit workflows, and consolidated family balances. None of these pediatric-specific data elements appear in the export response fields. (Source: comparison of `product-research.md` specialty features vs. `enrichment/patient-api-methods.json` response parameters)

4. **Hidden database schema reveals the gap.** The "Internal Use Only" SQL queries expose 18 Oracle tables with 111 columns — but these are only the tables used by the clinical data API. The absence of any billing, document, scheduling, or patient portal tables in these queries confirms that the export was designed to cover clinical data only. (Source: `enrichment/database-schema-from-sql.json`)

5. **Documentation quality varies dramatically.** The SOAP API documentation is adequate for clinical data retrieval (parameter tables, sample requests/responses, authentication guide). But the mandatory disclosure page — the actual (b)(10) documentation — is a single sentence with no actionable detail. There is no data dictionary, no export user guide, and no documentation of export scope or limitations. (Source: `ehrdisclosurev10.html` vs. `patientapi-homepage.html`)

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA XML (primary), FHIR R4 JSON (secondary/g(10))
Model type:      Standard projection (C-CDA 2.1 / US Core v6.1.0)
Entities:        10 API methods / 15 C-CDA sections / 26 FHIR resources
Fields:          83 response params (SOAP API), 38 unique field names
Descriptions:    85.5% of response fields have descriptions
Sample data:     Yes (9 C-CDA XML samples, 19 FHIR JSON samples in PDF)
Bulk export:     FHIR bulk data declared; SOAP API is single-patient only
Domains covered: 7 of 17 applicable domains fully covered
```

### Bottom Line

TriMed Complete's (b)(10) export is a C-CDA clinical summary — it covers standard clinical data (allergies, medications, problems, immunizations, labs, vitals, encounters, procedures) but omits billing/claims, insurance, scanned documents, patient portal data, and specialty-specific clinical data (pediatric growth charts, well-child workflows). For a product that markets itself as an all-in-one EHR + practice management + billing platform, exporting only the clinical summary portion represents a substantial gap. The biggest missing category is billing/financial data, which is explicitly part of the HIPAA designated record set and is a core feature of this product.
