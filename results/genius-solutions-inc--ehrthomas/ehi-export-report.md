# Genius Solutions Inc. — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: http://www.media.geniussolutions.com/ehrTHOMAS/ehrWebApi/Help/html/ElectronicHealthInformationExport.html
- CHPL ID: 9585
- Product: ehrTHOMAS Version 3
- Certification date: 2018-08-02

## Navigation Journal

### Step 1: Probe the registered URL
```bash
curl -sI -L "http://www.media.geniussolutions.com/ehrTHOMAS/ehrWebApi/Help/html/ElectronicHealthInformationExport.html" -H 'User-Agent: Mozilla/5.0'
```
Returned HTTP 200 OK, Content-Type: text/html, Content-Length: 25139 bytes. Last-Modified: 2024-04-18. The page is a static HTML file served from Apache on the vendor's media subdomain.

### Step 2: Download the page and its embedded assets
```bash
curl -sL "http://www.media.geniussolutions.com/ehrTHOMAS/ehrWebApi/Help/html/ElectronicHealthInformationExport.html" -H 'User-Agent: Mozilla/5.0' -o ehi-export-page.html
curl -sL "http://www.media.geniussolutions.com/ehrTHOMAS/ehrWebApi/Help/icons/EHI_Export1.jpg" -o EHI_Export1.jpg
curl -sL "http://www.media.geniussolutions.com/ehrTHOMAS/ehrWebApi/Help/icons/EHI_Export2.jpg" -o EHI_Export2.jpg
curl -sL "http://www.media.geniussolutions.com/ehrTHOMAS/ehrWebApi/Help/icons/EHI_Export3.jpg" -o EHI_Export3.jpg
```
All three screenshots are genuine JPEG images (verified with `file` command).

### Step 3: Explore the broader help site
The page is part of a Sandcastle-generated help site at `http://www.media.geniussolutions.com/ehrTHOMAS/ehrWebApi/Help/`. Directory listing is forbidden (403). The master navigation layout (`_masterLayout.html`) reveals the site primarily documents the §170.315(g)(10) FHIR Standardized API with pages for individual FHIR resources (AllergyIntolerance, CarePlan, CareTeam, Condition, etc.). The EHI export page is a standalone b(10) page that sits outside the g(10) navigation tree.

Probed for additional EHI-related files: schema files (.xsd), PDFs, data dictionaries, additional screenshots — all returned 404. No downloadable schema, data dictionary, or structured format files exist at the site.

### Step 4: Check mandatory disclosures page
The ONC transparency disclosures page at `https://www.geniussolutions.com/ehrthomas2015ed-onctransparency` (Wix-hosted) links to the same EHI export URL. No additional EHI export documents are linked.

### Step 5: Browser rendering and screenshot
Loaded the page in Chrome. The page renders cleanly as a single scrollable document with no JavaScript-dependent content beyond a footer fragment. Took a full-page screenshot.

## What Was Found

The EHI export documentation consists of a **single HTML page** containing:

1. **Introduction** — States that the Health IT Module can perform an EHI export "in a computable format" for a single patient at any time, and has an option to export all patients (which "may require support from the health IT developer"). Explicitly references §170.315(b)(10).

2. **How-to instructions** — Three annotated screenshots showing:
   - **Screenshot 1**: The Reports Menu in ehrTHOMAS, with the "Electronic Health Information (Export)" button highlighted (circled with "2"), accessed via the "Reports" button in the bottom toolbar (circled with "1").
   - **Screenshot 2**: The "Export: Electronic Health Information" dialog for single-patient export. Shows: Export Folder Path (`C:\Users\RashidM\Documents\EHRElectronicHealthInformation\02`), Export Type dropdown set to "Single Patient", patient search by Last Name or Account Number, patient selection list, and Export/Cancel buttons.
   - **Screenshot 3**: The same dialog for "All Patients (Entire Database)" export — just the Export Type dropdown and Export button.

3. **XML sample data** — The page documents the export format through XML sample snippets for **8 data domains**:
   - **Patient Dataset**: Demographics — KeyId, AccountNumber, SSN, Name (First/Last/Suffix), BirthDate, Gender, Phone/WorkPhone/CellPhone, Email, MothersMaidenName, Address (Line1/Line2/City/State/ZipCode), Race, Language, Ethnicity, MaritalStatus
   - **Encounter Dataset**: KeyId, PatientId, Status, VisitDate, DischargeDate, PerformingDoctor (NPI, LastName, FirstName, MidInitial, TaxonomyCode)
   - **Device Dataset**: KeyId, PatientId, ManufactureDate, ExpirationDate, LotNumber, SerialNumber, DeviceIdentifier, CarrierHRF, Snomed, DeviceDescription, ImplantedDate
   - **Immunization Dataset**: KeyId, PatientId, EncounterId, LotNumber, CVXCode, ShortDescription, DateAdministered
   - **Allergy Dataset**: KeyId, PatientId, ClinicalStatus, Reaction, RecordedDate, SNOMED, AllergyDescription
   - **Procedure Dataset**: KeyId, PatientId, EncounterId, Status, CPTCode, Description, RequestedTime, ProcedureStartTime, ProcedureEndTime
   - **Vital Dataset**: PatientId, EncounterId, BodyTemperature (Value/Unit/Location), BloodPressure (Systolic/Diastolic), Pulse, Respiration, SpO2, FiO2, Height, Weight, BMI, TimeRecorded
   - **Condition Dataset**: KeyId, PatientId, EncounterId, ClinicalStatus, VerificationStatus, OnSetDate, Comment, ICD10Code, ICD10Description

The export format is **proprietary XML** — not FHIR, not C-CDA, not any recognized standard. The XML elements are straightforward flat structures using vendor-specific element names.

## Export Coverage Assessment

### Data Domain Coverage

The documentation describes 8 XML datasets. Compared against what ehrTHOMAS/eTHOMAS is known to store (from product research), the coverage picture is:

**Clearly covered (8 domains):**
- Patient demographics
- Encounters
- Implantable devices (UDI data)
- Immunizations
- Allergies
- Procedures (with CPT codes)
- Vital signs (comprehensive: temp, BP, pulse, respiration, SpO2, FiO2, height, weight, BMI)
- Conditions/diagnoses (with ICD-10)

**Clearly missing or not mentioned:**
- **Medications and prescriptions** — ehrTHOMAS is certified for CPOE for medications ((a)(1)), e-prescribing ((b)(3)), and integrates with DrFirst for EPCS. The export documentation has no Medication dataset. This is a significant gap — medication lists are core clinical data.
- **Lab orders and results** — ehrTHOMAS is certified for CPOE-Lab ((a)(2)) and integrates with Quest Diagnostics via HL7. No lab data appears in the export.
- **Clinical notes / encounter documentation** — ehrTHOMAS uses touch-screen templates and the WritePad module for clinical documentation. No clinical notes/narrative text appears in the export.
- **Billing records** — The eTHOMAS practice management system handles claims, billing ledgers, patient statements, and payments. None of this appears in the export. For a b(10) export, billing data in the designated record set should be included.
- **Care plans** — ehrTHOMAS is certified for (b)(9) Care Plan. Not in the export.
- **Insurance/enrollment information** — eTHOMAS handles insurance verification and claims. Not in the export.
- **Documents and images** — WritePad can attach x-rays, lab reports, and pictures. No document/attachment export is documented.
- **Referral data** — eTHOMAS has referral tracking. Not in the export.
- **Patient correspondence** — Managed in eTHOMAS. Not in the export.
- **Smoking status / social history** — ehrTHOMAS has a SmokingStatusObservation in its FHIR API but this doesn't appear in the b(10) export.
- **Goals** — Listed in the FHIR API navigation. Not in the b(10) export.

**Assessment**: The export covers roughly the same clinical summary data you'd find in a USCDI patient summary, minus medications and lab results. This appears to be a narrow clinical subset, not a comprehensive export of "all electronic health information." The complete absence of medications is especially notable for a product with e-prescribing capabilities. The absence of billing data, clinical notes, and specialty-specific content (podiatry DRxContent, chiropractic templates) means the export falls well short of the b(10) "designated record set" requirement.

### Export Format & Standards

- **Format**: Proprietary XML with vendor-defined element names
- **Standard**: None — not FHIR, not C-CDA, not HL7 v2, not any recognized healthcare data standard
- **Schema**: No XSD, DTD, or formal schema is provided. The format is documented only through XML sample snippets embedded in the HTML page.
- **Relationships**: Data entities are linked via KeyId/PatientId/EncounterId integer references. These relationships are implicit in the samples but not formally documented.
- **Reconstruction potential**: A third party could parse the XML with reasonable effort for the 8 covered domains, but the lack of a formal schema means parsing relies on inference from samples. Coded fields use standard code systems (ICD-10, CPT, CVX, SNOMED) which is good, but there's no formal mapping or value set documentation.
- **Anomalies in sample data**: The Encounter sample shows all PerformingDoctor fields (LastName, FirstName, MidInitial, TaxonomyCode) populated with the NPI value "1234567897" — likely a redaction artifact but it obscures the actual field semantics. Condition ICD10Code fields contain GUIDs rather than ICD-10 codes, which is puzzling and may indicate an internal key rather than the actual code.

### Documentation Quality

- **Readability**: The page is clean and readable with clear section headings and annotated screenshots.
- **Data dictionary**: None. There is no field-level documentation — no data types, no descriptions, no constraints, no cardinality information. The only documentation of the XML format is the sample snippets themselves.
- **Value sets**: Not documented. Coded fields (Gender, ClinicalStatus, VerificationStatus, Status) show sample values but no enumeration of valid values.
- **Examples**: The XML snippets serve as examples with realistic-looking sample data, but they're the *only* format specification — they are both the documentation and the schema definition.
- **Developer implementability**: A developer could write a basic parser from these samples, but would have to make assumptions about every aspect not shown (optional vs. required fields, maximum lengths, handling of null/empty values, character encoding).
- **Maintenance**: The page was last modified 2024-04-18, for a product certified 2018-08-02. The footer reads "©2022 Genius Solutions." The documentation appears to be periodically updated but not comprehensive.

### Structure & Completeness

- **Granularity**: Table/entity level with field names shown in XML samples. No explicit data types, though `type="date"` and `type="time"` attributes appear on some elements. No cardinality documentation.
- **Coded fields**: Use recognizable code systems (ICD-10, CPT, CVX, SNOMED) but the valid value sets are not enumerated.
- **Relationships**: Implicit through ID references (PatientId, EncounterId) but not formally documented.
- **Versioning**: No version number on the EHI export documentation. The page title says "§170.315(b)(10)" but no version identifier.

### Overall Assessment

This is a minimal compliance effort. Genius Solutions has built a dedicated b(10) EHI export function with a proper UI (Reports > Electronic Health Information Export, with single-patient and full-database options) that produces proprietary XML files. The documentation provides enough XML samples to understand the basic structure of each dataset.

However, the export covers only 8 clinical data categories and **omits major data domains** that ehrTHOMAS/eTHOMAS stores: medications, lab results, clinical notes, billing records, insurance data, care plans, referrals, documents/images, and specialty-specific content. The absence of medications is the most striking gap — you cannot meaningfully reconstruct a patient record without medication data.

The documentation has no formal schema, no data dictionary, no value set documentation, and no description of the overall file structure (e.g., is the export one XML file per patient? One file per resource type? A single combined file?). These omissions make it impossible for a third party to build a reliable import without access to actual export files.

This represents a common pattern among smaller vendors: a genuine attempt to build a b(10) export that produces XML, but scoped to roughly the same clinical summary data available through their g(10) FHIR API, missing the broader "all EHI" scope that the regulation requires.

## Access Summary
- Final URL: http://www.media.geniussolutions.com/ehrTHOMAS/ehrWebApi/Help/html/ElectronicHealthInformationExport.html (no redirect)
- Status: found
- Required browser: no (static HTML, all content in page source)
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends
- Directory listing is forbidden (403) on the help site, so exhaustive file discovery was not possible
- Probed for additional files (XSD schemas, PDFs, data dictionaries, additional screenshots) — all returned 404
- The site navigation (`_masterLayout.html`) only lists g(10) FHIR API pages; the b(10) EHI export page is standalone and not included in the nav
- The mandatory disclosures page on geniussolutions.com (Wix-hosted) links to the same EHI export page with no additional documents
- No downloadable XML schema, sample export file, or data dictionary document exists at the site
