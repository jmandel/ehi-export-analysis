# EHI Export Analysis: EndoSoft, LLC

**Product**: EndoVault 3.2
**Analysis date**: 2026-02-16
**CHPL IDs**: 10854 (15.02.05.2721.ENDV.01.01.1.220310)

## 1. Product Context

EndoVault is an ONC-certified, multi-specialty EHR designed for **procedure-based specialties**, with its origin and core strength in **gastroenterology/endoscopy**. Developed by EndoSoft, LLC (founded 1995, headquartered in Schenectady, NY), the product serves over 100,000 clinical users worldwide across 100+ hospitals in 40+ countries. It runs on Microsoft SQL Server and Interbase databases.

EndoVault's data footprint spans multiple domains relevant to EHI export assessment:

- **Procedure documentation**: Detailed endoscopy reports with HD image capture (up to 4K, BMP/JPEG/TIF/DICOM formats), video recording (AVI), specialty-specific findings (polyp characteristics, cecal intubation, bowel prep scores, adenoma detection), and instrument tracking
- **Clinical data**: Patient demographics, medical history, allergies, medications, problem lists, diagnoses, vital signs (auto-captured from monitors), progress notes, consult reports
- **Electronic Nursing Record (ENR)**: Intra-procedure nursing documentation—sedation scores, IV assessments, medication administration during procedures, pain scales, adverse events, consciousness levels, discharge status
- **Oncology modules**: Cancer staging (TNM, ICD-O-3), chemotherapy management (dose calculations, cycle tracking), radiation therapy, adverse reaction histories, tumor board records
- **Pathology**: Requisitions and results, tissue sample tracking
- **Image management/PACS**: Integrated DICOM-compliant PACS with vendor-neutral scope support
- **E-prescribing**: Surescripts-certified electronic prescriptions
- **CPOE**: Orders for medications, labs, imaging
- **Patient portal**: Questionnaires, messaging, lab results access
- **Billing**: Time-and-material billing is tracked internally (items used, room utilization), but full claims/revenue cycle appears handled via interfaces to external billing systems
- **Scheduling & recall**: Multi-provider scheduling, recall management for follow-up procedures
- **Reporting**: 150+ prebuilt reports, registry submissions (GIQuIC, AGA, MIPS/MACRA)

This product stores far more specialty-specific clinical data than a typical ambulatory EHR. The export should cover endoscopy procedure documentation, imaging, nursing records, and oncology data in addition to standard clinical summaries.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `ephi-page.html` (85 KB) | Main EHI export page at www.endosoft.com/ephi/. Lists 23 C-CDA sections, describes two export methods (C-CDA and FHIR bulk). Brief — ~300 words of content. | **Medium** — establishes what vendor claims but no technical depth |
| `170.315-g10-Standardized-API-FHIR-2.pdf` (1.3 MB, 138 pages) | FHIR API documentation PDF dated 2022-11-25. Covers authorization, 18 FHIR resource types with individual API endpoints (pages 5–119), Bulk Data Access (pages 120–132), API resource table, rate limits, terms of service. | **Primary artifact** — most detailed technical documentation available |
| `fhir-page.html` (84 KB) | FHIR API landing page at www.endosoft.com/fhir/. Brief description of SMART on FHIR service with link to the PDF. | **Low** — just a pointer to the PDF |
| `endovault_ehr_disclosure_onc_2015-10_15_25.xlsx` (23 KB) | ONC cost disclosure spreadsheet. 57 rows listing all certified capabilities with "X" marks. Confirms b(10) certification with no additional costs listed. | **Low** — confirms certification, no export detail |
| `ephi-page-full.png` (761 KB) | Full-page screenshot of the EHI export page | **Verification** — confirms HTML content |
| `fhir-page-full.png` (666 KB) | Full-page screenshot of the FHIR API page | **Verification** — confirms HTML content |

**Most informative**: The 138-page FHIR API PDF is the only artifact with technical depth. The ePHI page provides the export overview. Together, these two artifacts constitute the entire (b)(10) documentation.

## 3. Export Mechanics

EndoVault documents two export methods:

### Method 1: Single/Multi-Patient C-CDA Export
- **Format**: C-CDA 2.1 XML files with CDA.xsl stylesheet
- **Mechanism**: UI-based export (end-user selects data sections)
- **Scope**: Single or multiple patients
- **Documentation**: Only the brief description on the `/ephi/` page — no technical specification, no sample files, no schema documentation

### Method 2: Bulk EHI Export via FHIR API
- **Format**: NDJSON (FHIR R4)
- **Mechanism**: RESTful API GET requests to static NDJSON file endpoints
- **Base URL**: `https://fhirapi.endosoft.com/bulk/`
- **Authorization**: OAuth 2.0 Bearer token (SMART on FHIR)
- **Scope**: All patients (bulk)
- **Rate limit**: 60 requests per time period (default quota per API doc p. 135)

The bulk FHIR API uses simple static file downloads (e.g., `GET /bulk/allergyintolerance-bulkfile.ndjson`), not the standard FHIR Bulk Data Export kick-off/status/download workflow.

**Access constraints**: Requires OAuth 2.0 registration with EndoSoft to obtain client credentials. No additional fees are listed in the cost disclosure spreadsheet.

**Critical broken link**: The EHI export page at `/ephi/` links to `https://old.endosoft.com/fhir/#_Toc120735483` for bulk export details. This link returns **HTTP 502 Bad Gateway** (verified 2026-02-16). The working equivalent is at `https://www.endosoft.com/fhir/`. A user following the documented path for bulk EHI export would reach a dead end.

## 4. Export Content: What's In It

### FHIR API Export (Bulk Data)

The bulk export provides 18 FHIR R4 resource types as NDJSON files. The Patient resource is available only through the individual API (not in bulk). All resources conform to standard US Core profiles with no vendor-specific extensions or custom profiles.

From the 138-page PDF, I extracted sample JSON responses for each resource type and parsed 739 unique field paths across all 19 resource types (see `analysis/full-entity-inventory.json` for the complete extraction).

### C-CDA Export

The C-CDA export lists 23 selectable sections:
Allergies, Encounter, Immunizations, Medications, Plan of treatment, Referral reason, Active problems, Reason for visit, Implants, Health concerns, Procedures, Functional status, Results, Social history, Vitals, Goals, Discharge instructions, Assessments, Cognitive status, Media, Diagnostic Report, Documents, Service Request.

No further documentation exists for the C-CDA export — no sample files, no section-level field definitions, no mapping to EndoVault's internal data model.

### Vendor's own content organization

The PDF organizes FHIR resources into four categories matching the US Core profile structure:

| Resource | Fields | Category (PDF) | Bulk Endpoint | Samples in PDF |
|---|---|---|---|---|
| Patient | 52 | Individual | No (individual API only) | 1 |
| Practitioner | 29 | Individual | Yes | 3 |
| RelatedPerson | 35 | Individual | Yes | 2 |
| Organization | 24 | Entities | Yes | 3 |
| Encounter | 63 | Management | Yes | 2 |
| AllergyIntolerance | 38 | Clinical | Yes | 2 |
| Condition | 46 | Clinical | Yes | 3 |
| Procedure | 13 | Clinical | Yes | 3 |
| DiagnosticReport | 38 | Clinical | Yes | 3 |
| Observation | 78 | Clinical | Yes | 18 |
| MedicationRequest | 56 | Clinical | Yes | 2 |
| Immunization | 69 | Clinical | Yes | 2 |
| CarePlan | 18 | Clinical | Yes | 2 |
| CareTeam | 25 | Clinical | Yes | 2 |
| Goal | 18 | Clinical | Yes | 2 |
| ServiceRequest | 33 | Clinical | Yes | 2 |
| DocumentReference | 48 | Clinical | Yes | 1 |
| Device | 33 | Clinical | Yes | 1 |
| Provenance | 23 | Security | Yes | 27 |
| **Total** | **739** | | | |

The Observation resource has 19 subcategories documented across 59 pages of the PDF (pages 45–103), covering: Laboratory Results, SDOH Assessments, Respiratory Rate, Social History, Heart Rate, Body Temperature, Pediatric Weight for Height, Pulse Oximetry, Smoking Status, Sexual Orientation, Head Circumference, Body Height, BMI, Blood Pressure, Imaging Result, Clinical Test Result, Pediatric BMI for Age, Pediatric Head Occipital-frontal Circumference Percentile, Body Weight.

These are standard US Core Observation profiles — they represent **standard vital signs, labs, and social determinants**, not EndoVault's specialty data.

**Field counts note**: The 739 fields represent unique JSON paths extracted from sample responses in the PDF. These are standard FHIR R4 element paths (e.g., `identifier[].type.coding[].system`), not EndoVault-specific fields. No vendor-specific field names, custom extensions, or proprietary data elements appear anywhere in the export documentation.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export covers standard USCDI/US Core clinical data:

- **Clinical** (13 resources, 559 fields): The largest category. Covers allergies, conditions/diagnoses, procedures, observations (vitals/labs/social history), medications, immunizations, care plans, care teams, goals, service requests, documents, diagnostic reports, and devices. This maps precisely to the USCDI v1/v2 data classes required by (g)(10).
- **Individual** (3 resources, 116 fields): Patient demographics, practitioners, related persons (next of kin).
- **Management** (1 resource, 63 fields): Encounters/visits with class, type, period, discharge disposition, location, and participant details.
- **Entities** (1 resource, 24 fields): Healthcare organizations.
- **Security** (1 resource, 23 fields): Provenance tracking.

The export is a competent implementation of the **US Core / USCDI clinical data set**. It covers the same data elements required for the (g)(10) Standardized API certification — and nothing more.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | Patient (52 fields): name, DOB, gender, address, telecom, language, marital status, extensions for race/ethnicity | Adequate for standard demographics |
| Encounters / visits | ✅ Covered | Encounter (63 fields): class, type, period, participants, locations, discharge disposition | Covers visit-level data |
| Problems / conditions | ✅ Covered | Condition (46 fields): code (SNOMED/ICD-10), category, clinical status, onset, verification status | Standard problem list coverage |
| Medications / prescriptions | ✅ Covered | MedicationRequest (56 fields): medication codes, dosage instructions, status, intent, requester | Standard medication orders; not e-prescribing transaction details |
| Allergies | ✅ Covered | AllergyIntolerance (38 fields): code, category, criticality, reactions, clinical status | Standard allergy coverage |
| Immunizations | ✅ Covered | Immunization (69 fields): vaccine code, date, status, site, route, lot number, performer | Standard immunization records |
| Vitals | ✅ Covered | Observation (78 fields, 19 subcategories): BP, heart rate, respiratory rate, temperature, height, weight, BMI, pulse ox, head circumference, pediatric measures | Standard vital signs |
| Lab results | ✅ Covered | Observation (laboratory category) + DiagnosticReport (38 fields) | Standard lab results |
| Imaging / diagnostic reports | ⚠️ Partial | DiagnosticReport covers reports; Observation has "Imaging Result" subcategory. However, **no actual images/DICOM data** are exported — only text-based reports | Product stores HD endoscopy images/video (BMP, JPEG, TIF, DICOM, AVI) as its core data type; these are completely absent from the export |
| Procedures | ⚠️ Partial | Procedure (13 fields): code, status, performed date/time. Only basic procedure records | Product stores rich endoscopy procedure documentation with specialty findings (polyp characteristics, bowel prep scores, cecal intubation, adenoma detection) — none of this specialty data is in the export |
| Clinical notes / documents | ⚠️ Partial | DocumentReference (48 fields): category, type, content, author, date | May reference notes but no evidence of specialty procedure reports with detailed findings |
| Care plans / goals | ✅ Covered | CarePlan (18 fields) + Goal (18 fields) | Standard care plan data |
| Orders / referrals | ✅ Covered | ServiceRequest (33 fields): code, category, status, requester, subject | Standard order/referral data |
| Insurance / coverage | ❌ Not covered | No Coverage or InsurancePlan resource | Product stores patient insurance data for billing interfaces; gap |
| Claims / billing | ❌ Not covered | No Claim, ExplanationOfBenefit, or billing-related resource | Product tracks time-and-material billing (items used, room utilization); gap |
| Payments | ❌ Not covered | No payment-related resources | N/A — full billing handled by external systems |
| Consents / directives | ❌ Not covered | No Consent resource | Product manages electronic signatures for consent and procedure sign-offs; gap |
| Patient communications / portal | ❌ Not covered | No Communication resource | Product has patient portal with messaging and questionnaires; gap |
| Specialty: Endoscopy imaging/video | ❌ Not covered | No Media resource in FHIR export (C-CDA lists "Media" section but no documentation of content) | **Critical gap** — endoscopy image capture is the product's core feature and raison d'être; HD images and video are central to the patient record |
| Specialty: Endoscopy findings | ❌ Not covered | No specialty data elements for polyp characteristics, bowel prep quality, cecal intubation, adenoma detection rates | **Critical gap** — these are the most clinically significant data elements the product stores |
| Specialty: Oncology | ❌ Not covered | No cancer staging, chemotherapy, radiation therapy, or tumor board resources | Product has dedicated oncology modules (TNM staging, chemo dose calculations, radiation ordering); significant gap |
| Specialty: Nursing (ENR) | ❌ Not covered | No procedural nursing resources for sedation scores, IV assessments, medication administration during procedures, pain/consciousness scales | Product has extensive ENR module; gap |
| Specialty: Pathology | ❌ Not covered | No pathology requisition or specialized result resources beyond generic DiagnosticReport | Product has pathology module; gap |

## 6. Documentation Quality

**Data dictionary**: None. There is no field-level data dictionary for the export. The FHIR API PDF provides sample JSON responses for each resource type, which implicitly show the data structure, but these are standard FHIR R4 structures. There is no EndoVault-specific mapping documentation showing which internal database fields map to which FHIR elements, or what EndoVault-specific data is lost in the projection to FHIR.

**Field descriptions**: None provided beyond standard FHIR element names. The PDF includes brief prose descriptions of each resource type (1–3 sentences each) but no field-level documentation.

**Types**: Implicit from FHIR R4 specification only. No EndoVault-specific type documentation.

**Value sets**: Standard FHIR/US Core value sets (SNOMED, LOINC, ICD-10) are referenced via code system URIs in sample data. No EndoVault-specific coded value documentation.

**Relationships**: FHIR references between resources are visible in sample JSON (e.g., Encounter referenced from Condition, Patient referenced from all resources). No entity-relationship diagram.

**Sample data**: Each resource type has 1–27 sample JSON responses in the PDF. These use synthetic data (test patient "Shepherd Meredith Lynn" / "HL7CONN1", EndoVault Medical Center). Sample data is adequate for understanding the FHIR resource structure but does not demonstrate EndoVault-specific data.

**Machine-readable artifacts**: None. No JSON schemas, no OpenAPI specifications, no downloadable sample NDJSON files. The only technical artifact is the PDF.

**Developer implementability**: A FHIR-experienced developer could implement an import of the standard clinical data elements. However, they would receive only a US Core clinical summary — not the product's specialty data. The C-CDA export is essentially undocumented beyond the section list.

## 7. Overall Assessment

### Classification

**Standard-based projection**

The EndoVault EHI export is the (g)(10) Standardized API repackaged as the (b)(10) export. The evidence is unambiguous:

1. The PDF is titled "170.315-g10-Standardized-API-FHIR-2.pdf" — it is explicitly the g(10) documentation
2. The 18 bulk data resource types map precisely to the US Core resource types required by g(10)
3. There are zero vendor-specific FHIR profiles, extensions, or custom resource types
4. The resource table (PDF p. 134) lists 16 API resources — exactly the US Core set
5. No specialty data (endoscopy findings, oncology staging, nursing records) appears anywhere
6. The EHI page simply points users to this same FHIR API for "Bulk EHI Export"

### Key Findings

1. **Classic (b)(10)/(g)(10) conflation**: The "Bulk EHI Export" is the same FHIR API used for g(10) certification, covering only the USCDI clinical summary (~20% of the product's data model). The product's core differentiating data — endoscopy images/video, specialty procedure findings, oncology records, nursing documentation — is entirely absent.

2. **Endoscopy images and video — the product's raison d'être — have no export path**: EndoVault was built around HD endoscopic image capture and video recording. These are stored in an integrated PACS with DICOM compliance. The export documentation does not address how this data is exported. The C-CDA export lists a "Media" section, but no technical documentation exists for it.

3. **No native data model exposure**: The export is purely a FHIR R4 projection. There is no export of EndoVault's underlying SQL Server/Interbase tables, no CSV/TSV dump, no proprietary format that would capture the full data model. Specialty-specific data structures (polyp findings, bowel prep scores, chemotherapy regimens, sedation records) have no representation in standard FHIR US Core profiles.

4. **Broken documentation link**: The primary path users would follow for bulk EHI export documentation (`old.endosoft.com/fhir/`) returns HTTP 502 Bad Gateway. The working URL (`www.endosoft.com/fhir/`) exists but is not linked from the EHI page. Verified 2026-02-16.

5. **No data dictionary beyond FHIR standard**: There are 0 vendor-specific field descriptions, 0 custom value sets, and 0 EndoVault-to-FHIR mapping documentation. A recipient of this export would have no way to know what EndoVault data was omitted or how EndoVault's internal data model relates to the FHIR resources.

### Summary Stats

    Classification:  Standard-based projection
    Export format:   C-CDA 2.1 XML + FHIR R4 NDJSON
    Model type:      Standard projection (US Core / USCDI)
    Entities:        19 FHIR resource types (18 in bulk, 1 individual-only)
    Fields:          739 (extracted from sample JSON; all standard FHIR paths)
    Descriptions:    0% (no vendor-specific field descriptions)
    Sample data:     Yes (synthetic JSON in PDF, no downloadable samples)
    Bulk export:     Yes (FHIR NDJSON via API)
    Domains covered: 10 of 22 applicable (+ 3 partial)

### Bottom Line

EndoVault's EHI export is a repackaged (g)(10) FHIR API that exports standard clinical summary data but misses the product's most valuable and distinctive data: endoscopy images/video, specialty procedure findings, oncology treatment data, nursing records, and pathology results. A patient or provider requesting their complete health information from an EndoVault system would receive a basic clinical summary but would be missing the detailed endoscopy documentation, HD images, and specialty clinical data that are the primary reason for using this product. The single biggest gap is the absence of any export path for endoscopic imaging — the product's founding and core capability.
