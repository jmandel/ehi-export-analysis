# DocToMe, Inc. — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://www.ethizo.com/electronic-health-information-export/
- CHPL IDs: 10265 (15.05.05.3060.DOTM.01.00.1.200107)
- Product: ethizo EHR v2.0
- Developer: DocToMe, Inc., 518 33rd Ave CT NW, Gig Harbor, WA

## Navigation Journal

### Step 1: Probe the registered URL
```bash
curl -sI -L "https://www.ethizo.com/electronic-health-information-export/" \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
```
Result: HTTP 200, Content-Type: text/html; charset=UTF-8. WordPress-powered page (PHP/7.4.33). No redirects.

### Step 2: Fetch and examine the page
```bash
curl -sL "https://www.ethizo.com/electronic-health-information-export/" \
  -H 'User-Agent: Mozilla/5.0' -o /tmp/ethizo-ehi.html
```
The page is extremely simple: a heading "EHI Export b.10 Documentation" and a single download link: "Please click here to download the electronic health information documentation" pointing to a PDF.

### Step 3: Search for downloadable files
```bash
grep -oiE 'href="[^"]*\.(pdf|zip|xlsx|xls|csv|json|doc|docx|yaml|yml)[^"]*"' /tmp/ethizo-ehi.html
```
Found one file link:
- `https://www.ethizo.com/wp-content/uploads/2025/03/EHI-Export-b.10-Documentation-v2.pdf`

### Step 4: Download the PDF
```bash
curl -sL "https://www.ethizo.com/wp-content/uploads/2025/03/EHI-Export-b.10-Documentation-v2.pdf" \
  -H 'User-Agent: Mozilla/5.0' \
  -o downloads/EHI-Export-b.10-Documentation-v2.pdf
```
Verified: PDF document, version 1.7, 9 pages, 311,422 bytes. Created 2025-03-01 with Microsoft Word for Microsoft 365.

### Step 5: Examine PDF contents
```bash
pdfinfo downloads/EHI-Export-b.10-Documentation-v2.pdf
pdftotext downloads/EHI-Export-b.10-Documentation-v2.pdf -
pdfdetach -list downloads/EHI-Export-b.10-Documentation-v2.pdf
```
- Title: "§170.315(b)(10) Electronic Health Information Export- Documentation"
- Author: ethizo EHR
- 9 pages, no embedded files, no embedded URLs (beyond standard XML namespace URIs)

### Step 6: Checked FHIR API documentation
The PDF's final line mentions: "FHIR Data Export - ethizo FHIR server can creates a single-patient FHIR resource Document Reference as well as supports FHIR Bulk Data EHI Export for patient population as described in § 170.315(b)(10)(ii)."

Navigated to https://fhir-api.ethizo.com/ (Postman-hosted documentation) to assess whether the FHIR Bulk Data path adds EHI-specific resources beyond US Core. The sidebar lists these FHIR resources: Patient, Allergy Intolerance, Condition (Health Concerns), Condition (Encounter Diagnosis), Coverage, CarePlan, CareTeam, Device, DiagnosticReport (Lab Results), DiagnosticReport (Report and Note Exchange), DocumentReference, Goal, Immunization, Implantable Device Tests, MedicationRequest, MedicationDispense, Procedure, Service Request, various Observations (Smoking Status, Pediatric Weight/Height, Lab Result, Pulse Oximetry, Pediatric Head Circumference, Body Height/Weight/Temp, Clinical Result, Screening Assessment, BMI, Blood Pressure, Heart Rate, Respiratory Rate, Pregnancy Status/Intent, Occupation), Organization, Practitioner, Provenance, Location, Specimen, Related Person, Encounter.

This is a standard US Core FHIR API — there are no billing-specific, scheduling-specific, or custom EHI-specific resources. This confirms the FHIR Bulk Data path is the (g)(10) API reused for (b)(10), not a dedicated EHI export mechanism with broader coverage.

## What Was Found

The EHI export documentation consists of a single 9-page PDF that describes an export mechanism called "Share Data." The export produces a ZIP file containing data in four categories:

### 1. Clinical Data in CDA Format
The primary clinical data export uses **HL7 CDA Release 2 (C-CDA R2.1, August 2015)** as specified in § 170.205(a)(4). The PDF provides a detailed data dictionary mapping for the CCD output with the following sections:

| CCD Section | Code Systems |
|---|---|
| Patient Demographics/Information | AdministrativeGender, CDC Race & Ethnicity |
| Provider's name and office contact | — |
| Date and Location of visit | — |
| Chief Complaint and Reason for visit | — |
| Encounters | CPT, SNOMED, ICD-10 |
| Immunizations | CVX, CPT-4, NCI Thesaurus, SNOMED |
| Instructions (Patient Instructions/Followup) | — |
| Treatment Plan (pending tests, future appts, referrals) | LOINC |
| Social History | LOINC, SNOMED |
| Problems | SNOMED, ICD-10 |
| Medications | RxNorm, NDC |
| Medication Allergies | RxNorm, SNOMED |
| Laboratory Tests & Results | LOINC |
| Vitals | LOINC |
| Goals | — |
| Procedures | CPT-4, SNOMED, HCPCS |
| Care Team Members | — |
| Reason for Referral | SNOMED |
| Medical Equipment (Implanted Devices) | GMDN |
| Mental Status | SNOMED |
| Functional Status | SNOMED |
| Health Concerns | SNOMED |

Each element includes XPATH/Entry paths, OID-based code system identifiers, and code system names.

### 2. Patient Demographics and Insurance Details
Exported as CSV (comma-separated). No field-level documentation is provided — the PDF says only "comprehensive view of demographics and insurance details."

### 3. Appointments
Exported as CSV (comma-separated). No field-level documentation — "comprehensive view of all future appointments details."

### 4. Documents
Scanned documents (PDF, JPG, PNG) organized into per-patient chart number folders with category subfolders (e.g., Lab Reports, Radiology, Scanned Receipts). Includes signed progress notes, lab results, radiology reports, and other uploaded documents.

### 5. FHIR Bulk Data Export (briefly mentioned)
A single sentence at the end of the PDF mentions FHIR DocumentReference for single-patient and FHIR Bulk Data for population-level export per §170.315(b)(10)(ii). No additional documentation for this pathway is provided in the PDF.

### Export Process
- **Single patient**: Log in → search patient → "Share Data" in left menu → select sections → "Process" → receive secure link via email/text → download ZIP
- **Bulk/population**: Log in → "Quick Links" (top right) → "Share Data" → choose EHI export for single or bulk → select sections → "Process" → secure link → download ZIP of ZIPs

## Export Coverage Assessment

### Data Domain Coverage

**Clearly covered (via CDA + CSV + documents):**
- Patient demographics (CDA + CSV)
- Insurance details (CSV — mentioned but no field documentation)
- Problems/diagnoses (CDA, SNOMED + ICD-10)
- Medications (CDA, RxNorm + NDC)
- Allergies (CDA, RxNorm + SNOMED)
- Lab results (CDA, LOINC)
- Vital signs (CDA, LOINC)
- Immunizations (CDA, CVX + CPT-4)
- Procedures (CDA, CPT-4 + SNOMED + HCPCS)
- Encounters (CDA, CPT + SNOMED + ICD-10)
- Goals (CDA)
- Care plans (CDA treatment plan section)
- Care team members (CDA)
- Referrals (CDA)
- Implantable devices (CDA, GMDN)
- Mental/functional status assessments (CDA, SNOMED)
- Health concerns (CDA, SNOMED)
- Social history (CDA, LOINC + SNOMED)
- Clinical notes and documents (as PDF/JPG/PNG files in the ZIP)
- Appointments (CSV — future appointments only, no field documentation)

**Missing or not documented:**
- **Billing data**: The product has a full Practice Management System with claims, ERA posting, CPT macros, eligibility verification, copay collection, payment processing, and revenue cycle KPIs. None of this billing/financial data is mentioned in the export documentation. The insurance CSV covers insurance *details* (likely coverage info), but there is no mention of claims, charges, payments, remittance advice, patient statements, or billing transaction history.
- **ePrescription / PDMP data**: The product has EPCS (electronic prescribing of controlled substances) with PDMP integration. While medications appear in the CDA, PDMP query results and controlled substance prescribing records are not specifically addressed.
- **Secure messages**: The patient portal supports secure messaging between patients and providers. No mention of message export.
- **Telemedicine records**: The Vezo telemedicine platform produces visit records, transit notes, and video call records. Not mentioned in the export.
- **Remote patient monitoring data**: The RPM module captures blood pressure, glucose, CGM, SpO2, weight, temperature, heart rate, and ECG data from connected devices. While vitals appear in the CDA (LOINC), there is no mention of the device-sourced RPM data stream, which likely has higher granularity than manually-entered vitals.
- **Chronic Care Management (CCM) data**: Care plans, enrollment records, activity logs, and automated billing generation for CCM are not specifically mentioned beyond the generic CDA care plan section.
- **Fax documents (Hybrid eFax)**: The product has a document management system merging fax, email, and e-signatures. The "Documents" export section may capture some faxed items if they're filed to patient charts, but the eFax workflow data itself is not addressed.
- **IVR call data**: The IVR system tracks calls and voicemails linked to patient rosters. Not mentioned (though this is borderline — call tracking may not be part of the designated record set).
- **Questionnaire responses**: Patient-generated data from portal questionnaires and smart trackers is not mentioned.
- **Patient-generated device data**: Fitbit/wearable integration data from the patient portal is not mentioned.

### Export Format & Standards

The primary export uses **C-CDA R2.1** for clinical data, which is a recognized standard. This is appropriate for the clinical domains it covers, but C-CDA has inherent limitations:
- It was designed for clinical summaries and transitions of care, not comprehensive EHI export
- It cannot naturally represent billing data, scheduling data, or many specialty-specific data types
- The CDA data dictionary maps only to standard CDA sections — there is no evidence of custom CDA extensions for non-standard data

The supplementary CSV files for demographics/insurance and appointments provide some coverage beyond CDA, but with zero field-level documentation — we don't know what columns exist, their data types, or their value sets.

The document export (PDF/JPG/PNG) captures the scanned/uploaded document layer, which is valuable for completeness but provides no structured data.

The FHIR Bulk Data option mentioned in the last line of the PDF is undocumented as an EHI mechanism. The FHIR API at fhir-api.ethizo.com documents standard US Core resources — there is no evidence of custom FHIR resources for billing, scheduling, or other non-USCDI data.

### Documentation Quality

The documentation is functional but minimal:
- **CDA section mapping is the strongest part** — it provides XPATH paths, OID code systems, and code system names for each data element. A developer could use this to parse the CDA output.
- **CSV formats are undocumented** — the PDF says only that demographics/insurance and appointments are "CSV, comma-separated" with no field definitions, data types, or examples.
- **No sample data or examples** — there are no sample export files, example CDA documents, or CSV extracts.
- **No schema files** — no XSD, JSON Schema, or other machine-readable artifact beyond the PDF.
- **Export instructions are adequate** — the step-by-step process is clear enough for a user to follow.
- **No FHIR Bulk Data documentation** — the mention of FHIR Bulk Data export is a single sentence with no endpoint URLs, authentication details, or resource type listing.

### Structure & Completeness

**Granularity**: The CDA data dictionary goes to the field level with XPATH paths and code systems. This is reasonably detailed for the clinical data it covers. However, the CSV components have zero field-level documentation.

**Value sets**: Code systems are identified by OID (e.g., SNOMED 2.16.840.1.113883.6.96, LOINC 2.16.840.1.113883.6.1) but specific value set bindings within those code systems are not documented.

**Relationships**: The CDA structure provides implicit relationships (e.g., encounter → diagnoses, medication → dosage). Cross-file relationships between the CDA, CSV, and document exports are not documented (e.g., how a document file maps to a CDA encounter).

**Versioning**: The PDF filename says "v2" and was created March 2025. No change history is provided.

### Overall Assessment

Ethizo has made a genuine effort to document a multi-format export (CDA + CSV + documents) that goes somewhat beyond a bare FHIR API. The CDA clinical data dictionary is the most detailed component and covers the standard clinical domains reasonably well. However, the export has significant gaps for a product of this breadth:

1. **The biggest gap is billing/financial data.** For a product with a full Practice Management System — claims, ERA, payments, eligibility, revenue cycle — there is no documented export mechanism for any billing data beyond insurance coverage. This is the most critical EHI gap.

2. **Several product modules are invisible in the export documentation**: telemedicine (Vezo), remote patient monitoring (RPM), chronic care management (CCM), secure messaging, eFax, and IVR. These modules generate patient-specific data that is part of the designated record set.

3. **The CSV components lack any documentation.** Saying a file is "CSV, comma-separated" tells a developer nothing about how to parse or import it.

4. **The FHIR Bulk Data mention appears to be the (g)(10) API repackaged.** The FHIR API documentation at fhir-api.ethizo.com lists only standard US Core resources — no billing, no specialty data, no custom resources. This is the classic (b)(10)/(g)(10) conflation, though here the vendor has at least *also* provided CDA + CSV + documents rather than relying solely on FHIR.

The documentation reads as a compliance-driven effort rather than a comprehensive data portability solution. The CDA mapping shows technical competence, but the gaps in billing, specialty modules, and CSV documentation suggest the export was designed around the clinical summary use case rather than the "everything in the designated record set" requirement of (b)(10).

## Access Summary
- Final URL (after redirects): https://www.ethizo.com/electronic-health-information-export/
- Status: found
- Required browser: no (simple HTML page with direct PDF download link)
- Navigation complexity: direct_link (one click to PDF)
- Anti-bot issues: none

## Obstacles & Dead Ends
- None. The page loaded cleanly, the PDF downloaded without issues.
- The FHIR API site at fhir-api.ethizo.com is Postman-hosted documentation that loads client-side (JavaScript required) but was accessible via browser. It documents the (g)(10) API, not a dedicated (b)(10) mechanism.
- The ONC mandatory disclosures page (ethizo.com/onc-ehr-certified/) was noted as returning HTTP 500 in the product research, but this is not relevant to the EHI export documentation itself.
