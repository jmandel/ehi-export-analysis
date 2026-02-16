# SMARTMD Technologies, Inc. — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://www.smartmd.com/compliance/
- CHPL IDs: 11476
- Product: SMARTMD Palliative, Version 6
- Certification Date: 2024-05-31

## Navigation Journal

1. **Initial probe** — `curl -sI -L "https://www.smartmd.com/compliance/" -H 'User-Agent: Mozilla/5.0'` returned HTTP 200. The page is a WordPress site served through Cloudflare.

2. **Fetched page HTML** (170KB). Extracted text and searched for file links:
   ```bash
   curl -sL "https://www.smartmd.com/compliance/" -H 'User-Agent: Mozilla/5.0' -o /tmp/page.html
   grep -oiE 'href="[^"]*\.(pdf|zip|xlsx|xls|csv|json|doc|docx|yaml|yml)[^"]*"' /tmp/page.html
   ```

3. **Found five links** on the compliance page, organized under three headings:

   **National Coordinator for Health Information Technology (ONC):**
   - [ONC Disclosure Statement](https://www.smartmd.com/wp-content/uploads/SMARTMD-ONC-Disclosure-Statement-2024-Leidos-b10.pdf)
   - [B(10) Export Documentation](https://www.smartmd.com/wp-content/uploads/170.315b10-Electronic-Health-Information-Export.pdf)

   **Real World Testing Plans:**
   - SMARTMD Palliative Real World Testing Plan (2025) — not relevant to EHI export, skipped.

   **FHIR Support:**
   - [SMARTMD FHIR API Specifications](https://www.smartmd.com/wp-content/uploads/SMARTMD-FHIR-API-Documentation-v1.pdf)
   - [SMARTMD API (JSON)](https://secure.smartmd.com/downloads/API.json)

4. **Downloaded all four EHI-relevant files** with curl:
   ```bash
   curl -sL -H 'User-Agent: Mozilla/5.0' "https://www.smartmd.com/wp-content/uploads/170.315b10-Electronic-Health-Information-Export.pdf" -o "170.315b10-Electronic-Health-Information-Export.pdf"
   curl -sL -H 'User-Agent: Mozilla/5.0' "https://www.smartmd.com/wp-content/uploads/SMARTMD-ONC-Disclosure-Statement-2024-Leidos-b10.pdf" -o "SMARTMD-ONC-Disclosure-Statement-2024-Leidos-b10.pdf"
   curl -sL -H 'User-Agent: Mozilla/5.0' "https://www.smartmd.com/wp-content/uploads/SMARTMD-FHIR-API-Documentation-v1.pdf" -o "SMARTMD-FHIR-API-Documentation-v1.pdf"
   curl -sL -H 'User-Agent: Mozilla/5.0' "https://secure.smartmd.com/downloads/API.json" -o "API.json"
   ```

5. **Verified all downloads** — `file` confirmed each PDF is a valid PDF document, and the JSON is valid JSON data. No login walls, no redirects.

6. **Took a full-page screenshot** of the compliance page in the browser, confirming the page is a simple static layout with the links listed above. No accordions, no hidden content, no JavaScript-rendered sections beyond the basic page structure.

7. **Checked EHI PDF for embedded URLs and attachments** — no embedded URLs or attachments found. The PDF is self-contained.

## What Was Found

### B(10) Export Documentation (Primary EHI Export Document)

The core EHI export documentation is a 10-page PDF titled "ONC Certification 170.315(b)(10) Electronic Health Information Export, 2024v1." It describes a **per-patient JSON export** mechanism:

**Export mechanism:** Users navigate to the Patients tab, select one or more patients, and tap the "Export" button. The export produces a JSON file **per patient**.

**Data sections documented with field-level detail:**

| Section | Fields Documented | Description |
|---------|-------------------|-------------|
| **Patient** | 13 fields | Demographics: PatientId, PatientName, ChartID, DOB, Case (service line), Address, City, State, Zip, Country, HomePhone, WorkPhone, MobilePhone, Email |
| **KinList** | 10 fields | Caregivers/relatives: PatientId, KinId, FirstName, LastName, MobilePhone, Email, DeceasedFlag, Decisional, Country, RelationshipList |
| **Meds** | 13 fields | Medications: Strength, StrengthUnit, Form, DoseQuantity, StrengthForm, StartDate, EndDate, DoseUnit, Drug, DrugId, DrugInstructions, WrittenAs, Status |
| **Allergies** | 4 fields | Allergen, Reaction, WrittenAs, Status |
| **Problems** | 6 fields | ClinicalSummaryProblemDetailsList: DictionaryCode (ICD-10), Problems (description), ActiveDate, ResolvedDate, ProblemId, isResolved, isPrimaryDx |

**Sample JSON export** is included (pages 7–9), showing a complete patient record with all five sections populated. The sample reveals additional undocumented structures:

- A **CaseList** array containing case/encounter-level data: provider information (ProviderId, ProviderName), patient location details, case descriptions (e.g., "Hospice"), diagnosis codes, insurance lists, external/internal contact lists, and creation timestamps.
- The CaseList section includes a **CaseProvider** sub-object with provider identifiers and names.
- The CaseList includes **InsuranceList**, **ExternalContactList**, and **InternalContactList** arrays (empty in the sample but present in the structure).

These CaseList fields are NOT documented in the field-level tables but ARE present in the sample JSON output.

Each field has a name, data type (string, date, bool, int), and a brief description. Date formats are specified (e.g., "m/d/yyyy" for DOB, ISO 8601 timestamps in the sample data).

### ONC Disclosure Statement

A 2-page PDF listing all certified criteria for SMARTMD Palliative Version 6. Confirms (b)(10) certification. Notes that EMR Direct Interoperability Engine v2023 is relied-upon software for (b)(1) and (h)(1). Updated January 25, 2025.

### FHIR API Documentation

A 58-page PDF documenting the SMART on FHIR API (for g(10) certification). This covers:
- FHIR endpoints (production: https://fhir.smartmd.com:9443/fhir-server/api/v4/)
- SMART on FHIR authentication (OAuth2, symmetric/asymmetric/public client flows)
- FHIR resources: Patient, AllergyIntolerance, CarePlan, CareTeam, Condition, ImplantableDevice, DiagnosticReport/ClinicalNotes/DocumentReference, Laboratory Observations, Goal, Immunization, Medication, SmokingStatus, Procedure, Provenance, VitalSigns, CCDA
- Search operations (Patient, Encounter, Document)

This is the **g(10) standardized API** documentation, NOT the b(10) EHI export. It covers USCDI v1 data classes via FHIR R4. The b(10) export is the separate JSON-based mechanism described in the EHI export PDF.

### API.json

A FHIR R4 Bundle (collection) containing two Endpoint resources and two Organization resources. These are Direct messaging endpoint configurations pointing to a test/certification server (fhirserver.justtest.in), not production endpoints. This appears to be related to the (h)(1) Direct Project criterion rather than the b(10) export.

## Export Coverage Assessment

### Data Domain Coverage

Based on the product research, SMARTMD Palliative stores data across these domains. Here is how the b(10) export covers them:

| Data Domain | Covered in Export? | Notes |
|---|---|---|
| **Patient demographics** | Yes | 13 fields in Patient section |
| **Next of kin / caregivers** | Yes | KinList section with contacts and decisional status |
| **Medications** | Yes | Active medications with drug details, dosing, start/end dates |
| **Allergies** | Yes | Drug/food/environmental allergies with reactions |
| **Problems / Diagnoses** | Yes | ICD-10 coded, with onset/resolution dates, primary dx flag |
| **Provider assignments** | Partial | In CaseList sample but undocumented |
| **Case/service line info** | Partial | In CaseList sample but undocumented |
| **Insurance** | Partial | InsuranceList array present in sample JSON but empty; no field docs |
| **Clinical encounter notes** | **Not documented** | Core product feature — palliative care notes, dictation transcriptions |
| **Palliative assessments (PPS, FAST, ESAS)** | **Not documented** | Specialty-specific structured assessments are a key product feature |
| **Billing / charges / CPT codes** | **Not documented** | Time-based chronic care billing (PCM, TCM, CCM) is a core module |
| **Scheduled appointments** | **Not documented** | Provider scheduling with mobile push |
| **Secure messages** | **Not documented** | HIPAA-compliant team messaging |
| **Scanned documents / images** | **Not documented** | Consent forms, scanned documents |
| **Care plans** | **Not documented** | Implied by palliative workflows and CMS GUIDE model support |
| **Quality measure data (PPS trends, acuity scores)** | **Not documented** | Extracted from notes and plotted as trend graphs |
| **CRM / referral source data** | **Not documented** | May be a separate product (Accelerate CRM) |
| **MIPS/quality reporting data** | **Not documented** | Registry and reporting capability |

**The export covers approximately 5 of 15+ data domains** stored by the product. The documented export is essentially a patient demographic summary with medication, allergy, and problem lists — very similar to what a C-CDA patient summary or USCDI core dataset would include, just in JSON format.

**Critical missing domains for a b(10) export:**

1. **Clinical encounter notes** — This is the product's primary function. Palliative care providers create detailed clinical documentation at every visit. No notes appear in the export.
2. **Palliative care assessments** (PPS, FAST, ESAS) — These are structured, specialty-specific clinical instruments that are central to the product. They track patient trajectory toward hospice. Their absence is a significant gap.
3. **Billing and charge data** — The product has detailed time-based billing with CPT code recommendations. No billing data appears in the export.
4. **Care plans** — Implied by the palliative care workflow and CMS GUIDE model support. Not in the export.
5. **Scanned documents and images** — Consent forms and other documents mentioned in app store listings. Not in the export.

### Export Format & Standards

The export uses a **proprietary JSON format** — not FHIR, not C-CDA, not any recognized healthcare interoperability standard. This is not inherently problematic for b(10); a vendor-specific format is acceptable as long as it includes all EHI. However:

- The JSON structure is flat and simple — good for basic parsing
- Field naming is inconsistent (camelCase mixed with PascalCase)
- Date formats vary within the same export (e.g., "m/d/yyyy" vs ISO 8601 timestamps)
- The export is per-patient, which is appropriate for individual patient requests
- A third party could reconstruct the demographic/medication/allergy/problem data from this export, but NOT the full patient record since clinical notes, assessments, billing, and documents are absent

### Documentation Quality

- **Readable but minimal** — The 10-page PDF is clearly formatted with tables for each section. Field names, types, and descriptions are provided.
- **Sample data included** — A complete JSON example with all sections populated helps developers understand the format.
- **Undocumented structures** — The sample JSON contains a CaseList structure with provider info, location data, insurance, and contacts that is NOT described in the field documentation tables. This means the actual export may be slightly broader than the documentation suggests, but the documentation is incomplete.
- **No schema file** — There is no JSON Schema, no OpenAPI spec, no machine-readable format definition. Only the PDF tables and sample.
- **No value sets** — The documentation doesn't define valid values for fields like "Case" (service line), "Status", or relationship types. The sample shows examples but doesn't enumerate possibilities.
- **No versioning** — Labeled "2024v1" but no changelog or versioning strategy documented.

A developer could implement a basic import of this data, but would need to handle the undocumented CaseList fields and guess at value constraints. The documentation is adequate for a patient summary import but insufficient for reconstructing a full patient record.

### Structure & Completeness

- **Granularity**: Field-level with name, type, and brief description. Better than just listing table names, but lacking constraints, cardinality, and optionality.
- **Coded fields**: ICD-10 codes documented for Problems; RxNorm codes appear in the sample (RxNtCode field) but are not documented in the field tables. No other coded field documentation.
- **Relationships**: Implicit via PatientId linkage across sections. No formal relationship documentation.
- **Cardinality**: Not specified. The sample suggests arrays for KinList, Meds, Allergies, Problems, and CaseList, but min/max counts are not documented.

### Overall Assessment

SMARTMD Palliative has done the minimum to check the b(10) certification box. They have a dedicated EHI export feature (not just repurposed FHIR API), which is good — it demonstrates awareness that b(10) is separate from g(10). The JSON-based per-patient export with field documentation and sample data shows genuine effort.

However, the export covers only the narrowest slice of patient data: demographics, medications, allergies, and problems. This is roughly equivalent to a patient summary — the same data that g(10) already covers through the FHIR API. For a palliative care EHR whose primary value is in its clinical documentation, structured assessments (PPS, FAST, ESAS), and specialty billing, the absence of notes, assessments, billing data, care plans, documents, and messages means the export captures perhaps 20-30% of the EHI the product stores.

The documentation itself is adequate for what it covers but incomplete even for the data it does export (CaseList undocumented). The lack of a machine-readable schema and the absence of value set definitions further limit its utility.

## Access Summary
- Final URL: https://www.smartmd.com/compliance/
- Status: found
- Required browser: no (all content accessible via curl; WordPress static page)
- Navigation complexity: direct_link (two links directly on the compliance page)
- Anti-bot issues: none (Cloudflare present but no blocking)

## Obstacles & Dead Ends
- None. The page was straightforward, all links worked, all downloads were valid. No login walls, no JavaScript-dependent content for the EHI links.
- The API.json file is hosted on a different domain (secure.smartmd.com) but was publicly accessible.
