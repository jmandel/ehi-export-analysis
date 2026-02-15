# CursaHealth LLC — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://cursahealth.com/document/B10-Electronic-Health-information-Export.pdf
- CHPL IDs: 11735
- Product: CursaHealth EHR v2.0
- Certification date: 2025-12-29

## Navigation Journal

The registered URL is a direct PDF download. No navigation required.

```bash
# Probe the URL
curl -sI -L "https://cursahealth.com/document/B10-Electronic-Health-information-Export.pdf" \
  -H 'User-Agent: Mozilla/5.0'
# Returns: HTTP/1.1 200 OK, Content-Type: application/pdf, Content-Length: 466927

# Download the PDF
curl -sL "https://cursahealth.com/document/B10-Electronic-Health-information-Export.pdf" \
  -H 'User-Agent: Mozilla/5.0' \
  -o downloads/B10-Electronic-Health-information-Export.pdf
```

The PDF (4 pages, created 2025-08-14 by Nouman Zafar using Microsoft Word) references a FHIR Documentation page as part of the export mechanism:

```bash
# Download the referenced FHIR documentation
curl -sL "https://cursahealth.com/document/FHIR-Documentation.html" \
  -H 'User-Agent: Mozilla/5.0' \
  -o downloads/FHIR-Documentation.html
```

The ONC certification page at `https://cursahealth.com/onc-ehr-certification` was also checked — it links back to the same PDF for the (b)(10) criterion and to the same FHIR documentation page. No additional EHI export documentation was found.

## What Was Found

The EHI export documentation is a **4-page PDF** that describes three export mechanisms and three non-FHIR data categories. Specifically:

### Export Mechanisms

1. **CCD/C-CDA documents** — Bulk export of HL7 C-CDA XML files complying with USCDI v1. The document references standard C-CDA specifications (CDA R2, Consolidated CDA Templates R2.1) but provides no vendor-specific schema, field mapping, or data dictionary for what data elements are included in the C-CDAs.

2. **FHIR Bulk Data Access** — References the (g)(10) FHIR API at `https://fhirapi.cursahealth.com/api`. Points to a separate FHIR Documentation page which documents 29 US Core resource types: AllergyIntolerance, BMI For Age Observation, CarePlan, CareTeam, Condition, Device, DiagnosticReport, DocumentReference, Encounter, Goal, Head Circumference, Immunization, Laboratory Result, Location, MedicationRequest, Blood Pressure, Body Height, Body Temperature, Body Weight, Heart Rate, Respiratory Rate, Organization, Patient, Practitioner, Procedure, Provenance, Pulse Oximetry, Smoking Status, and Weight For Height. These are all standard US Core STU 3.1.1 profiles.

3. **Non-FHIR supplemental exports** — Three additional data categories exported outside of C-CDA/FHIR:
   - **Patient Demographics & Insurance** — Excel format. Described as "a comprehensive view of demographics and insurance details."
   - **Appointments** — Excel format. Described as "a comprehensive view of all appointment details."
   - **Documents** (scanned/imported) — Original files (PDF, JPG, PNG) organized by patient chart number in categorized subfolders (Lab Reports, Radiology, Scanned Receipts, etc.).

### Documentation Characteristics

- **No data dictionary**: There are no field-level definitions, column names, data types, or value sets for any export format. The Excel files for demographics/insurance and appointments have no schema documentation — just a one-sentence description each.
- **No sample data**: No example export files, sample records, or test data.
- **No schema files**: No XSD, JSON Schema, OpenAPI spec, DDL, or any machine-readable schema.
- **No export instructions**: No screenshots or step-by-step instructions for how a user initiates the export.
- **No format specification**: The document does not define what columns/fields appear in the Excel exports, what sections appear in the C-CDAs beyond "USCDI v1," or how the folder structure for documents is precisely organized.

## Export Coverage Assessment

### Data Domain Coverage

Based on the product research, CursaHealth EHR stores clinical encounters, demographics, medications, allergies, problems/diagnoses, vitals, immunizations, lab results, imaging orders, family health history, social/behavioral data, implantable devices, billing/claims data, scheduling/appointments, care plans, patient portal messages, transitions of care documents, quality measure data, and transcription records.

**Clearly covered** (via C-CDA + FHIR + Excel/documents):
- Patient demographics and insurance (Excel export + FHIR Patient)
- Allergies (C-CDA + FHIR AllergyIntolerance)
- Medications (C-CDA + FHIR MedicationRequest)
- Problems/diagnoses (C-CDA + FHIR Condition)
- Vital signs (C-CDA + FHIR Observation vitals)
- Immunizations (C-CDA + FHIR Immunization)
- Lab results (C-CDA + FHIR DiagnosticReport/Laboratory Result)
- Procedures (C-CDA + FHIR Procedure)
- Care plans/goals (C-CDA + FHIR CarePlan/Goal)
- Care team (FHIR CareTeam)
- Encounters (FHIR Encounter)
- Implantable devices (FHIR Device)
- Appointments (Excel export)
- Scanned/imported documents (original files in patient folders)
- Signed progress notes, lab results, radiology reports (via document export)

**Likely missing or undocumented**:
- **Billing and claims data** — The product offers medical billing, claims processing, A/R management, and coding. None of the three export mechanisms mention billing data, charges, claims, payments, or insurance claims. This is a significant gap for a product that integrates billing.
- **Patient portal messages** — Secure messaging between providers and patients is a feature. No mention in the export.
- **Family health history** — Certified under (a)(12) but not mentioned in the export documentation. May be in the C-CDA but not confirmed.
- **Social/psychological/behavioral data** — Certified under (a)(15). Not explicitly mentioned. May be partially covered by C-CDA social history section.
- **Transcription records** — Listed as a product feature. Not mentioned in export.
- **Clinical decision support alerts** — Patient-specific alerts and reminders. Not mentioned.
- **Quality measure data** — Certified under (c)(1)-(c)(3). Not mentioned in export.
- **Specialty-specific clinical data** — Mental health assessments, OB/GYN-specific records, pediatric-specific data beyond growth charts. Not mentioned.

### Export Format & Standards

The export uses a **hybrid approach**: C-CDA XML for clinical summaries, FHIR R4 Bulk Data for US Core resources, Excel for demographics/insurance and appointments, and original document files.

This is a classic **(g)(10) repackaging** situation. The FHIR component is explicitly the (g)(10) API — the documentation says "Please refer 170.315(g)(10) FHIR-Documentation.html for the API Specifications." The FHIR resources are all standard US Core STU 3.1.1 profiles with no vendor-specific extensions or non-USCDI data.

The vendor has made a reasonable effort to go **beyond** pure FHIR/C-CDA by adding Excel exports for demographics/insurance and appointments, and raw document file exports. However, the total scope still falls well short of "all electronic health information" — particularly billing data, which is a core data domain for a product that markets itself as an all-in-one EHR + billing platform.

A third party could reconstruct a basic clinical summary from this export, but not a complete patient record. The Excel exports have no documented schema, making import/interpretation unreliable. The C-CDA content is limited to USCDI v1.

### Documentation Quality

**Very poor.** The entire EHI export documentation is 4 pages, of which page 1 is a cover page and page 2 is a table of contents. The substantive content is roughly 1.5 pages of text with no field definitions, no column listings, no data types, no examples, and no screenshots.

- No data dictionary whatsoever
- No field-level definitions for any format
- No value sets or coded field documentation
- No sample files or worked examples
- No export instructions (how does a user trigger the export? Single patient vs. multi-patient?)
- No format specification for the Excel files
- No documentation of what C-CDA sections/entries are included

A developer could not implement an import of this data based solely on this documentation. They would need to request a sample export and reverse-engineer the format.

### Structure & Completeness

The documentation is at the **format-name level** only — "Excel format" and "C-CDA XML" with no further detail. There is no field-level documentation, no entity-relationship information, no data type specifications, and no versioning or change history. The FHIR documentation page provides slightly more detail (US Core resource types and API endpoints) but this is standard (g)(10) documentation, not (b)(10)-specific.

## Overall Assessment

CursaHealth's EHI export documentation is **minimal and incomplete**. The vendor has made a basic attempt to go beyond pure FHIR/C-CDA by including Excel exports and raw document files, which shows some awareness that (b)(10) requires more than (g)(10). However:

1. The export appears to cover clinical data reasonably well through C-CDA + FHIR but **omits billing data entirely** — a critical gap for a product that integrates billing as a core feature.
2. The documentation is **too sparse to be actionable** — no data dictionary, no schemas, no examples.
3. The FHIR component is explicitly the (g)(10) API repackaged, covering only US Core/USCDI resources.
4. The product was certified very recently (2025-12-29), which may partially explain the documentation immaturity.

This reads as a compliance checkbox exercise rather than a genuine effort to enable complete EHI portability.

## Access Summary
- Final URL (after redirects): https://cursahealth.com/document/B10-Electronic-Health-information-Export.pdf
- Status: found
- Required browser: no
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends
None. The URL returned a direct PDF download with no issues. The referenced FHIR documentation page was also directly accessible as static HTML.
