# iSALUS Healthcare — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://officeemr.knowledgeowl.com/help/ehi-export
- CHPL IDs: 10914
- Product: OfficeEMR v2021
- Certification date: 2022-06-06
- Developer: iSALUS Healthcare (now under EverCommerce / EverHealth division)

## Navigation Journal

### Step 1: Initial probe
```bash
curl -sI -L "https://officeemr.knowledgeowl.com/help/ehi-export" -H 'User-Agent: Mozilla/5.0'
```
HTTP 200, Content-Type: text/html; charset=UTF-8. The URL is live and returns a KnowledgeOwl knowledge base article.

### Step 2: Fetch and examine the page
```bash
curl -sL "https://officeemr.knowledgeowl.com/help/ehi-export" -H 'User-Agent: Mozilla/5.0' -o /tmp/ehi-page.html
```
The page is 1.3MB of HTML. It's a KnowledgeOwl-hosted article titled "EHI Export" with 10 expandable accordion sections and three downloadable ZIP files. Last modified 12/19/2025 8:58 AM EST.

### Step 3: Identified downloadable files
Searched the HTML source for file download links:
```bash
grep -oiE 'href="[^"]*\.(pdf|zip|xlsx|xls|csv|json|doc|docx|yaml|yml)[^"]*"' /tmp/ehi-page.html
```
Found three ZIP files hosted on CloudFront CDN:
1. `officeemr-b10-schema-v1-oct2023.zip` — JSON Schema definitions (80 files)
2. `isalus-ehi-export-data-elements-version1-oct2023.zip` — Excel data dictionary (1 XLSX file)
3. `export-311322-voct2023.zip` — Sample single-patient export (58 JSON data files)

### Step 4: Downloaded all three ZIPs
```bash
curl -sL "https://dyzz9obi78pm5.cloudfront.net/app/image/id/6581f345834514735d5985a7/n/officeemr-b10-schema-v1-oct2023.zip" -o downloads/officeemr-b10-schema-v1-oct2023.zip
curl -sL "https://dyzz9obi78pm5.cloudfront.net/app/image/id/6581f2ad80a15e0a045fe3c2/n/isalus-ehi-export-data-elements-version1-oct2023.zip" -o downloads/isalus-ehi-export-data-elements-version1-oct2023.zip
curl -sL "https://dyzz9obi78pm5.cloudfront.net/app/image/id/65661563c203e87cf17f980d/n/export-311322-voct2023.zip" -o downloads/export-311322-voct2023.zip
```
All verified as valid ZIP archives.

### Step 5: Downloaded PDF export of full page
The KnowledgeOwl platform provides a "Download PDF" button. This generates a 56-page PDF containing all accordion content fully expanded, which serves as the most complete single-document representation of the export documentation.
```bash
curl -sL "https://officeemr.knowledgeowl.com/help/pdfexport/id/6565f0bfbc5664102d34b052" -o downloads/ehi-export-page.pdf
```
Verified: PDF document, 56 pages, 3.98 MB.

### Step 6: Captured screenshots
- Took a full-page screenshot of the main EHI Export page (collapsed accordions)
- Expanded all accordion sections in browser and took a full-page screenshot
- Navigated to the HT1 EHI (B10) Export Updates page and took a screenshot

### Step 7: Checked related pages
- The "HT1 EHI (B10) Export Updates" article (at /help/hti-1-2026-certification-updates#ht1-ehi-b10-export-updates) describes upcoming HTI-1/USCDIv3 additions: Demographics: Tribal Affiliation, Occupation, Industry; Allergies: Verification; Problems: Verification. Marked "COMING SOON: HT1 Release Date is TBD (Q1 2026)".
- Individual export category pages (/help/demographics-export, /help/data-export-claims-export, etc.) are part of a separate "Data Export" (InfoDive) section for a legacy CSV export tool, not the (b)(10) EHI export. These are distinct from the EHI Export documentation.

## What Was Found

### Export Format
The EHI export uses a **proprietary JSON format** — not FHIR, C-CDA, or any other healthcare standard. The export consists of individual JSON files, one per data entity type, following a naming convention of `{entity_name}.json`. Each file contains a JSON array of objects representing records for that patient (single-patient export) or all patients (practice-wide export).

A `readme.json` file is included in every export containing a link back to the publicly accessible format documentation.

### Export Mechanism
- **Single patient export**: Users with the "EHI Export" role can access the EHI Export tool via Reports portal. They search for a patient, request the export, and download a ZIP file once the status changes to "Completed". This is self-service and immediate.
- **All patients (practice) export**: Users with the "EHI Practice Export" role submit a request through the same tool. This triggers a process involving the iSALUS Data Export team. The export is described as being for practices migrating to a new EHR platform. Delivery takes approximately 15 days.

### Downloadable Artifacts
Three outstanding computable artifacts were provided:

1. **JSON Schema files (80 files)**: JSON Schema draft-07 definitions for each export entity. Every field has a property name and type, but all `description` fields are empty strings (`""`). Entity types include clinical data (allergies, vitals, medications, immunizations, lab results, progress notes, etc.) and practice management data (claims, payments, insurance, statements, denials, etc.).

2. **Excel data dictionary (XLSX)**: A single spreadsheet (`iSalus_EHI_ExportDataElements_published_version1_Oct2023_pristine.xlsx`) containing field-level definitions with descriptions.

3. **Sample patient export (58 JSON files)**: A complete export for a test patient (ID 311322), demonstrating the actual export output with realistic test data. This includes claims, appointments, medications, progress notes, template encounters, vitals, lab results, and more.

### Data Dictionary Structure
The PDF documentation organizes the data dictionary into two sections:

**Clinical Data Exports** — including: accident, allergy, allergy_symptom, appointment, care_plan_goal, care_team, case_management, case_management_ckcc_note, chart_share (and related sub-files), chronic_care_management, ckcc_status, comment, communication, communication_recipient, consent, demographics, dialysis_setup, dialysis_visit, education, emergency_contact, epa (electronic prior authorization), extension_encounter, extension_results, goal (and sub-files), health_concern, hie, image_document, image_xref, immunization, immunization_registry, implantable_device, insurance, lab_result, letter, md_revolution_status, medication, optimize_rx, order, order_finding, pharmacy, phone_encounter, portal_message, pregnancy, pregnancy_visit, problem_list, problem_list_note, progress_note, referral_tracking, responsible_party, template_encounter (and sub-files for assessment, exam, history, hpi, order_fulfillment, ros, treatment_plan), vital

**Practice Management Data Exports** — including: claim, claim_procedure, denial, eligibility, fee_schedule (referenced but not in schema ZIP), payment, preschool_billing, price_estimate, price_estimate_line, prior_authorization (and sub-files), sliding_fee, statement

Each entry in the data dictionary provides: Export Name (filename), FIELD (field name), and Description (plain-English description of the field's purpose).

## Export Coverage Assessment

### Data Domain Coverage

iSALUS has done genuine (b)(10) work here. This is **not** a repackaged FHIR/g(10) API — it is a purpose-built JSON export that covers data well beyond the USCDI clinical subset. The coverage is notably broad for a small vendor:

**Clearly covered domains:**
- Patient demographics (comprehensive: name, address, phones, identifiers, race, ethnicity, language, employment, marital status, employer, multiple ID types)
- Insurance and payer information (detailed: 4+ pages of insurance schema fields)
- Responsible parties / guarantors
- Appointments and scheduling
- Allergies and allergy symptoms
- Problem lists with notes
- Medications/prescriptions
- Progress notes
- Template encounters (with granular sub-files for HPI, ROS, exam, history, assessment, treatment plan, order fulfillment)
- Vitals (exceptionally detailed: sitting/standing/supine BP, multiple body measurements, pulse ox details)
- Immunizations and immunization registry data
- Lab results and orders
- Letters and correspondence
- Document metadata (image_document, image_xref) — note: actual document images provided separately as original files (PDF, JPEG, PNG)
- Patient communications and portal messages
- Emergency contacts
- Claims (comprehensive billing data: claim status, charges, balance, aging, providers, payers)
- Claim procedure lines
- Payments
- Denials
- Statements (with aging buckets)
- Prior authorizations (with codes and rendering providers)
- Price estimates
- Fee schedules
- Eligibility verification records
- Consent records
- Care plans and goals
- Care teams
- Health concerns
- Referral tracking
- Phone encounters
- Education records
- Implantable devices
- Chronic care management records
- Dialysis setup and visit data (specialty-specific)
- Case management and CKCC notes (specialty-specific)
- Chart sharing records
- HIE (Health Information Exchange) data
- EPA (Electronic Prior Authorization) records
- Sliding fee schedules
- Preschool billing

**Domains that may be missing or unclear:**
- **Audit logs / access history**: No schema file for system audit trails or user access logs.
- **Telehealth session records**: The AnywhereCare telehealth module is a product feature, but no dedicated telehealth visit entity appears in the export. These may be captured within progress_note or template_encounter.
- **Intelligent Intake (patient intake forms)**: The digital intake module stores patient-submitted forms, but no dedicated schema for intake form data appears.
- **Patient portal activity**: portal_message is covered, but broader portal interaction logs are not explicitly mentioned.
- **Clinical decision support rules/alerts**: These are system configuration data and may not be patient-specific EHI.
- **E-fax records**: Electronic faxing is a product feature but no dedicated fax entity in the export.
- **MIPS/quality measure data**: Referenced as a product feature but no dedicated export entity.
- **RPM (Remote Patient Monitoring)**: The md_revolution_status entity appears related but the coverage is unclear.
- **Custom template data**: Template encounters are well-covered, but whether all custom/specialty-specific template data is fully captured in the generic template_encounter structure is uncertain.

### Export Format & Standards

- **Format**: Proprietary JSON — one file per entity type, each containing a JSON array of record objects.
- **Standard compliance**: This is not FHIR, C-CDA, or any recognized healthcare data standard. It is a vendor-specific flat data model.
- **Relationships**: Entities are linked via `patientId` (present in every file). Some entities have foreign keys to others (e.g., `claimId` in claim_procedure links to claim). However, relationship documentation is limited — the data dictionary describes fields but does not formally document entity relationships or cardinality. The PDF mentions some relationships in passing (e.g., "price_estimate_line.json can be 1-to-many" relative to price_estimate).
- **Appropriateness**: For a practice management + ambulatory EHR system, a flat JSON export is a reasonable approach. The vendor-specific format means a receiving system would need custom import logic, but the data structure is straightforward and self-documenting through the JSON Schema and sample export.
- **Reconstructability**: A third party could reconstruct the patient record from this export. The combination of demographic, clinical, and billing data provides a comprehensive picture. The main challenge would be understanding coded values (e.g., what do specific `claimStatus` values mean?) and reconstructing relationships between template_encounter sub-files.

### Documentation Quality

**Strengths:**
- **Three complementary artifacts**: JSON Schema files provide machine-readable structure, the XLSX provides human-readable field descriptions, and the sample export demonstrates real output. This is unusually thorough for a vendor of this size.
- **Comprehensive data dictionary**: The 56-page PDF includes field-level descriptions for every data element across all export entities. Each field has a plain-English description explaining its purpose.
- **Clear user instructions**: Step-by-step instructions for both single-patient and all-patient exports, including role requirements and process details.
- **Sample data**: A full single-patient sample export with realistic test data across 58 entity files. This is one of the better artifacts — a developer could immediately understand the format.
- **Public accessibility**: All documentation is fully public, no login required, hosted on a well-organized KnowledgeOwl knowledge base.
- **Active maintenance**: Page was last modified 12/19/2025 and HTI-1 updates are already being documented for Q1 2026.

**Weaknesses:**
- **Empty JSON Schema descriptions**: All `description` fields in the JSON Schema files are empty strings. The schema files define structure and types but provide no semantic context. A developer would need the XLSX or PDF to understand what fields mean.
- **No value set documentation**: Coded fields (e.g., `claimStatus`, `gender`, `maritalStatus`, `employmentStatus`, `agingType`) are typed as strings but there is no documentation of valid values, code systems, or enumeration sets.
- **Minimal relationship documentation**: Entity relationships are mostly implicit through shared IDs. No entity-relationship diagram or formal relationship documentation is provided.
- **No versioning/changelog**: The artifacts are labeled "v1-OCT2023" but there's no formal change log documenting what changed between versions.
- **Date format inconsistency**: Some dates appear as "YYYYMMDD" strings (e.g., `birthDate: "19011212"`), others as ISO-like formats (e.g., `authorLogDateUtc: "20150302144846-0400"`). The documentation does not specify date format conventions.

### Structure & Completeness

- **Granularity**: Field-level documentation with descriptions, though no data type detail beyond JSON Schema types (string, number, object, array). Notably, many nullable fields are typed as `"type": "object"` rather than using JSON Schema's nullable patterns — this is technically incorrect but understandable.
- **Entity count**: 80 JSON Schema files covering approximately 70 distinct data entities (excluding readme and sub-entity files).
- **Sample data coverage**: The sample export includes 58 files, which is fewer than the 80 schema files. Entities present in the schema but absent from the sample (e.g., fee_schedule, sliding_fee, statement, eligibility, hie, immunization_registry, implantable_device, chart_share_detail_*, goal sub-files, health_concern, portal_message) may simply have no data for the test patient.
- **Coded values**: Not documented. This is the most significant gap — without value sets, a consumer cannot interpret many fields.
- **Cardinality**: Not formally documented. Implied by the array structure (each file is an array of records).

## Access Summary
- Final URL (after redirects): https://officeemr.knowledgeowl.com/help/ehi-export
- Status: found
- Required browser: no (all content accessible via curl; browser useful for expanding accordions and PDF download)
- Navigation complexity: direct_link (all downloadable artifacts are linked directly from the main page)
- Anti-bot issues: none

## Obstacles & Dead Ends
- The KnowledgeOwl page uses accordion sections that require clicking to expand. However, all content is present in the DOM and the platform offers a PDF export that includes everything expanded.
- The individual export category pages linked in the sidebar (/help/demographics-export, /help/claims-export, etc.) are part of a **separate legacy "Data Export" (InfoDive)** feature, not the (b)(10) EHI export. They document a different, older CSV-based export system. This could be confusing for someone trying to understand the EHI export documentation scope.
- No issues with authentication, bot blocking, or dead links. All resources loaded cleanly.
