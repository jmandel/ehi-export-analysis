# EHI Export Analysis: EndoSoft, LLC

**Product**: EndoVault 3.2
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.02.05.2721.ENDV.01.01.1.220310

## 1. Product Context

EndoVault is an ONC-certified, multi-specialty EHR designed primarily for **procedure-based specialties**, with its core strength in **gastroenterology/endoscopy**. Originally built around endoscopic procedure documentation and image capture, it has expanded to support oncology, pulmonology, pain management, general surgery, orthopedics, OB/GYN, ENT, urology, pathology, ophthalmology, dermatology, and cardiology. The vendor claims 100,000+ clinical users across 100+ hospitals in 40+ countries.

Key data domains the product stores include:

- **Core clinical**: Demographics, encounters, problems, medications, allergies, immunizations, vitals, lab results, clinical notes, care plans, goals
- **Procedure documentation**: Detailed procedure reports with findings (polyp characteristics, cecal intubation, bowel prep quality), intra-procedure nursing data (sedation scores, IV access), post-procedure observations
- **Images & video**: HD still images (BMP, JPEG, TIF, DICOM) and video recordings (AVI, up to 4K) from endoscopic procedures — this is a core differentiator
- **Electronic Nursing Record (ENR)**: Automatic vital sign capture from monitors, medication administration during procedures, patient tracking across rooms
- **Oncology-specific**: Cancer staging (TNM, ICD-O-3), chemotherapy management (dose calculations, cycle tracking, MAR), radiation therapy ordering, adverse reaction tracking, tumor board coordination
- **Pathology**: Requisitions and results, tissue sample tracking
- **E-prescribing**: Surescripts-certified
- **CPOE**: Medication, lab, and imaging orders
- **Scheduling & recalls**: Multi-provider, multi-facility appointment scheduling
- **Inventory & scope tracking**: RFID/barcode-based equipment tracking
- **Time-and-material billing**: Items used per procedure, room utilization (full claims/revenue cycle handled externally via interfaces)
- **Patient portal**: Questionnaires, lab results, messaging
- **Quality measures**: GIQuIC, AGA, MIPS/MACRA registry data, adenoma detection rates

This is a specialty-rich product with significant data beyond standard USCDI clinical summaries.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/ephi-page.html` (85 KB) | Main EHI export page at endosoft.com/ephi/. Lists 23 export data sections and two export methods (C-CDA and FHIR bulk). | **High** — primary documentation of (b)(10) scope |
| `downloads/170.315-g10-Standardized-API-FHIR-2.pdf` (1.3 MB, 138 pages) | FHIR API documentation dated 2022-11-25. Covers OAuth 2.0, 16 individual patient API endpoints, and 18 bulk data NDJSON endpoints. This is the (g)(10) standardized API documentation, referenced as the bulk EHI export mechanism. | **High** — shows exact FHIR resources available |
| `downloads/fhir-page.html` (84 KB) | FHIR API landing page at endosoft.com/fhir/. Links to the FHIR API PDF. | Low — just a landing page |
| `downloads/endovault_ehr_disclosure_onc_2015-10_15_25.xlsx` (23 KB) | EHR cost disclosure spreadsheet. Lists (b)(10) "Electronic Health Information Export" with no additional costs noted. | Low — confirms (b)(10) certification, no content detail |
| `downloads/ephi-page-full.png` (761 KB) | Full-page screenshot of the EHI export page. | Low — visual confirmation of HTML content |
| `downloads/fhir-page-full.png` (666 KB) | Full-page screenshot of the FHIR page. | Low — visual confirmation |

## 3. Export Mechanics

- **Format(s)**:
  - **C-CDA 2.1 XML** for single/multi-patient export (produces `*.xml` data + `CDA.xsl` stylesheet)
  - **FHIR R4 NDJSON** for bulk EHI export (18 resource-type-specific NDJSON files via HTTP GET)

- **Mechanism**:
  - Single/multi-patient: UI-based export within EndoVault (user selects sections to export)
  - Bulk: FHIR API endpoints at `<base bulk url>/<resource>-bulkfile.ndjson`, authenticated via Bearer token

- **Single-patient vs bulk**: Both supported. Single/multi-patient via C-CDA, bulk via FHIR API.

- **Access constraints**: OAuth 2.0 / Bearer token required. API rate limit of 60 requests/minute (adjustable). Client applications must register with EndoSoft.

- **Fees**: No additional costs listed in the cost disclosure spreadsheet for (b)(10).

## 4. Export Content: What's In It

### No product-specific data dictionary

EndoVault provides **no product-specific data dictionary, field documentation, or schema** for its EHI export. The only documentation is:

1. The EHI page listing 23 C-CDA section names (one-word or short-phrase labels with no field-level detail)
2. The 138-page FHIR API PDF, which is a **(g)(10) standardized API document** with sample JSON responses for standard US Core FHIR resources

There are no:
- Field-level descriptions beyond FHIR resource definitions
- Product-specific field mappings (e.g., "EndoVault's bowel prep score maps to Observation.valueCodeableConcept")
- Vendor extensions or custom FHIR profiles
- Relationship documentation between EndoVault's internal data model and the export
- Value sets or code systems specific to EndoVault
- Sample export data files

### C-CDA export sections (23)

The EHI page lists these sections available for single/multi-patient C-CDA export:

| # | Section | USCDI Mapping |
|---|---|---|
| 1 | Allergies | Allergies & Intolerances |
| 2 | Encounter | Encounters |
| 3 | Immunizations | Immunizations |
| 4 | Medications | Medications |
| 5 | Plan of treatment | Assessment & Plan of Treatment |
| 6 | Referral reason | Orders / Referrals |
| 7 | Active problems | Problems |
| 8 | Reason for visit | Encounters |
| 9 | Implants | Medical Devices |
| 10 | Health concerns | Health Status Assessments |
| 11 | Procedures | Procedures |
| 12 | Functional status | Health Status Assessments |
| 13 | Results | Laboratory / Clinical Tests |
| 14 | Social history | Health Status Assessments |
| 15 | Vitals | Vital Signs |
| 16 | Goals | Goals & Preferences |
| 17 | Discharge instructions | Clinical Notes |
| 18 | Assessments | Health Status Assessments |
| 19 | Cognitive status | Health Status Assessments |
| 20 | Media | Clinical Notes / Documents |
| 21 | Diagnostic Report | Diagnostic Imaging |
| 22 | Documents | Clinical Notes / Documents |
| 23 | Service Request | Orders / Referrals |

These are standard C-CDA 2.1 sections — none are EndoVault-specific.

### FHIR Bulk Data resources (18)

The bulk export exposes 18 FHIR resource types as NDJSON files:

| # | Resource Type | FHIR Profile | USCDI Domain |
|---|---|---|---|
| 1 | AllergyIntolerance | US Core AllergyIntolerance | Allergies & Intolerances |
| 2 | CarePlan | US Core CarePlan | Assessment & Plan of Treatment |
| 3 | CareTeam | US Core CareTeam | Care Team Members |
| 4 | Condition | US Core Condition | Problems / Diagnoses |
| 5 | Device | US Core Implantable Device | Medical Devices |
| 6 | DiagnosticReport | US Core DiagnosticReport | Diagnostic Imaging / Lab |
| 7 | DocumentReference | US Core DocumentReference | Clinical Notes / Documents |
| 8 | Encounter | US Core Encounter | Encounters |
| 9 | Goal | US Core Goal | Goals & Preferences |
| 10 | Immunization | US Core Immunization | Immunizations |
| 11 | MedicationRequest | US Core MedicationRequest | Medications |
| 12 | Observation | US Core Observation | Vitals / Labs / Clinical Tests |
| 13 | Organization | FHIR R4 Organization | Facility Information |
| 14 | Patient | US Core Patient | Demographics |
| 15 | Practitioner | US Core Practitioner | Care Team Members |
| 16 | Procedure | US Core Procedure | Procedures |
| 17 | Provenance | US Core Provenance | Provenance |
| 18 | RelatedPerson | US Core RelatedPerson | Care Team Members |
| — | ServiceRequest | US Core ServiceRequest | Orders / Referrals |

Note: Patient is listed in the individual API resources table (Table 4-1) but not explicitly shown as a separate bulk endpoint in the Bulk Data section. ServiceRequest has a bulk endpoint but is listed at the very end (page 132).

**All sample responses in the PDF use standard US Core profiles with no vendor extensions observed.** The sample data shows generic test patients (e.g., "Shepherd Meredith Lynn", "HL7CONN1") with standard coded values.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's EHI export documentation organizes content into exactly two mechanisms:

1. **C-CDA export**: 23 named sections corresponding to standard C-CDA 2.1 document sections. No field-level documentation. The vendor simply lists section names — the user must know C-CDA to understand what's in each section.

2. **FHIR Bulk Data export**: 18 FHIR R4 resource types matching the standard US Core / (g)(10) profile set. Each resource has a static NDJSON endpoint with one sample response shown in the PDF.

Both export mechanisms cover **exactly the same clinical domains** — the USCDI data set. There is no indication that either mechanism exports data beyond what's required for (g)(10) standardized API certification. The vendor does not describe any supplementary export, database dump, or additional data files.

The vendor's own documentation on the EHI page says: *"EHI – Electronic protected health information (ePHI) Export functionality allows EndoVault to do an export of health data for one or more patients. EndoVault supports the data export in CCD/C-CDA and ndjson formats."* This describes the existing (g)(10) and transitions-of-care mechanisms, not a purpose-built EHI export.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | Patient resource (bulk), C-CDA header | Standard US Core Patient fields only |
| Encounters / visits | ✅ Covered | Encounter resource (bulk), C-CDA Encounter section | Standard encounter data |
| Problems / conditions | ✅ Covered | Condition resource (bulk), Active problems section | Standard US Core Condition |
| Medications / prescriptions | ✅ Covered | MedicationRequest (bulk), Medications section | Standard; no MAR for chemo/procedures |
| Allergies | ✅ Covered | AllergyIntolerance (bulk), Allergies section | Standard |
| Immunizations | ✅ Covered | Immunization (bulk), Immunizations section | Standard |
| Vitals | ✅ Covered | Observation (bulk), Vitals section | Standard US Core vital signs |
| Lab results | ✅ Covered | Observation/DiagnosticReport (bulk), Results section | Standard |
| Imaging / diagnostic reports | ⚠️ Partial | DiagnosticReport (bulk), Diagnostic Report section | Standard FHIR DiagnosticReport only — **no endoscopy images or video** (a core product capability) |
| Procedures | ⚠️ Partial | Procedure resource (bulk), Procedures section | Only standard FHIR Procedure — **no detailed endoscopy procedure documentation** (findings, bowel prep scores, polyp characteristics, cecal intubation, intra-procedure nursing data) |
| Clinical notes / documents | ⚠️ Partial | DocumentReference (bulk), Documents/Media/Discharge instructions sections | Standard document references; unclear if procedure reports with embedded images are included |
| Care plans / goals | ✅ Covered | CarePlan, Goal (bulk), Plan of treatment/Goals sections | Standard |
| Orders / referrals | ✅ Covered | ServiceRequest (bulk), Service Request/Referral reason sections | Standard |
| Insurance / coverage | ❌ Not covered | No Coverage resource in bulk or C-CDA | Product stores insurance via interfaces; gap if patient-level coverage data exists |
| Claims / billing | ❌ Not covered | No billing entities or Claim resources | Product tracks time-and-material billing within ENR module — **significant gap** |
| Payments | ❌ Not covered | No payment data in export | N/A if billing is external |
| Consents / directives | ❌ Not covered | No Consent resource | Product captures electronic signatures for consent and procedure sign-offs |
| Patient communications / portal messages | ❌ Not covered | No Communication resource | Product has patient portal with messaging |
| Specialty-specific: Endoscopy | ❌ Not covered | No endoscopy-specific data (images, video, scope tracking, findings detail) | **Major gap** — this is the product's core domain |
| Specialty-specific: Oncology | ❌ Not covered | No oncology-specific data (staging, chemo regimens, radiation, tumor board) | Product has extensive oncology modules |
| Specialty-specific: Pathology | ❌ Not covered | No pathology-specific data beyond DiagnosticReport | Product has pathology requisition/results module |
| Specialty-specific: ENR | ❌ Not covered | No ENR data (intra-procedure vitals, sedation, patient tracking) | Product has dedicated ENR module |

**Domains covered**: 10 of 21 applicable domains (all USCDI-aligned)
**Domains missing**: 11 domains, including the product's core specialty (endoscopy)

## 6. Documentation Quality

**Overall quality: Poor.**

- **No data dictionary**: There is no product-specific data dictionary, schema, or field documentation for the EHI export. A developer receiving this export would need to understand C-CDA 2.1 and FHIR R4 / US Core specifications independently — the vendor provides no mapping or guide.

- **No sample export files**: The PDF contains individual sample JSON responses for each FHIR resource type, but these are embedded in a 138-page API document, not provided as standalone sample export files.

- **No field-level documentation**: The 23 C-CDA section names are listed without any description of what fields or coded values each section contains. The FHIR resources rely entirely on the generic US Core profile definitions.

- **No machine-readable schema**: No JSON Schema, FHIR StructureDefinitions, or other machine-readable artifacts are provided.

- **The FHIR API PDF is a (g)(10) document**: The 138-page PDF is titled "API Definition," dated 2022-11-25, and covers OAuth 2.0 authorization, individual patient API endpoints, and bulk data access. It is clearly the vendor's (g)(10) Standardized API documentation, not a purpose-built (b)(10) EHI export guide. The document makes no mention of "(b)(10)", "EHI", "designated record set", or "electronic health information export."

- **Could a developer build an import?** Only for the standard USCDI data set, and only if they already know C-CDA and FHIR. There is nothing EndoVault-specific to guide a developer in understanding the product's data model or specialty-specific content.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The export covers only standard USCDI clinical domains through standard C-CDA 2.1 and US Core FHIR resources. EndoVault is a procedure-focused EHR whose core value proposition is endoscopy documentation, image/video capture, and specialty clinical workflows (oncology chemotherapy management, ENR, pathology). None of this specialty data — which represents the majority of what makes EndoVault's data unique — is present in the export. The export covers approximately the same clinical summary data that any US Core-compliant EHR would expose through its (g)(10) API, missing the product's entire specialty data layer.

**Axis 2 — Export approach: Repackaged existing export**

The evidence is clear:
1. The EHI export page describes C-CDA and FHIR bulk as the two export methods — these are the vendor's existing (b)(1) transitions of care and (g)(10) standardized API mechanisms.
2. The FHIR API PDF is explicitly the (g)(10) document (titled "API Definition," no mention of (b)(10) or EHI).
3. The 18 bulk FHIR resource types exactly match the standard US Core (g)(10) resource set.
4. No vendor extensions, no custom FHIR profiles, no product-specific data dictionary.
5. The EHI page itself links to the FHIR page with "More information can be found here" — directly pointing users to the (g)(10) documentation.
6. The 23 C-CDA sections are standard C-CDA 2.1 sections, not EndoVault-specific.

### Key Findings

1. **Export is the (g)(10) API relabeled as (b)(10).** The bulk EHI export documentation points directly to the same FHIR Bulk Data endpoints documented in the (g)(10) API PDF. There is no additional export mechanism, data dictionary, or product-specific documentation.

2. **No endoscopy data in the export.** EndoVault's core capability — endoscopic procedure documentation with HD image/video capture, findings documentation, bowel prep scores, polyp detection — has zero representation in the export. This is the product's primary clinical domain.

3. **No oncology, pathology, or ENR data.** Three major clinical modules (oncology staging/chemotherapy, pathology requisitions/results, electronic nursing record) are absent from the export.

4. **No data dictionary exists.** The vendor provides no product-specific field documentation. The only documentation is a list of 23 C-CDA section names and the standard (g)(10) FHIR API specification.

5. **No billing or operational data.** Time-and-material billing tracked in the ENR module, scheduling data, inventory/scope tracking, and patient portal communications are all absent.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Repackaged existing export
Export format:   C-CDA 2.1 XML, FHIR R4 NDJSON
Entities:        18 FHIR resource types + 23 C-CDA sections (all standard, no vendor-specific)
Fields:          N/A (no product-specific data dictionary)
Descriptions:    N/A
Sample data:     No standalone samples (inline examples in API PDF only)
Bulk export:     Yes (FHIR Bulk Data API)
Domains covered: 10 of 21 applicable domains
```

### Bottom Line

EndoVault's (b)(10) EHI export is its existing (g)(10) FHIR API and C-CDA transitions-of-care export relabeled. A patient receiving this export would get a standard USCDI clinical summary but would be missing the product's most valuable and distinctive data: endoscopy procedure documentation with images and video, oncology staging and chemotherapy records, pathology results, intra-procedure nursing documentation, and time-and-material billing data. The single biggest gap is the complete absence of endoscopy-specific data — the core clinical domain EndoVault was built to serve.
