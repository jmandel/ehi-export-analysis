# Prime DataQ Health, LLC — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://static1.squarespace.com/static/692e09ea4112f840c4fb54d8/t/69307ee493279950e0b33148/1764785893013/EHI+Export+Documentation+-+SummitEHR+v1.0.pdf
- CHPL IDs: 11689
- Mandatory disclosures page: https://www.summitehr.com/onc-certification

## Navigation Journal

The registered URL is a direct link to a PDF hosted on Squarespace's static CDN. No navigation was required.

```bash
# Step 1: Probe the URL
curl -sI -L "https://static1.squarespace.com/static/692e09ea4112f840c4fb54d8/t/69307ee493279950e0b33148/1764785893013/EHI+Export+Documentation+-+SummitEHR+v1.0.pdf" -H 'User-Agent: Mozilla/5.0'
# Result: HTTP 200, Content-Type: application/pdf, 377,490 bytes

# Step 2: Download the PDF
curl -sL "https://static1.squarespace.com/static/692e09ea4112f840c4fb54d8/t/69307ee493279950e0b33148/1764785893013/EHI+Export+Documentation+-+SummitEHR+v1.0.pdf" -H 'User-Agent: Mozilla/5.0' -o downloads/EHI-Export-Documentation-SummitEHR-v1.0.pdf
# Verified: `file` confirms PDF document, 4 pages

# Step 3: Check the ONC certification page for additional documentation
curl -sL "https://www.summitehr.com/onc-certification" -H 'User-Agent: Mozilla/5.0' -o /tmp/summitehr-onc.html
# Found 4 PDF links on the page:
#   - Pricing-Disclosures-SummitEHR-v10.pdf (not EHI-related)
#   - Multi-factor-Authentication-Use-Cases-SummitEHR-v10.pdf (not EHI-related)
#   - EHI-Export-Documentation-SummitEHR-v10.pdf (same PDF, short URL alias)
#   - Application-Access-API-Guide-SummitEHR-v10.pdf (g)(9) API guide, not EHI export)
# No additional EHI export documentation found.
```

The certification page has an "EHI Export Documentation" section that provides a brief summary (identical to the PDF's introduction) and links to the same PDF. No additional data dictionaries, schemas, sample files, or supplemental documentation exist.

## What Was Found

The entire EHI export documentation consists of a single 4-page PDF:

**Page 1**: Cover page with DataQ Health logo, title "EHI Export Documentation", product name "SummitEHR (v1.0)".

**Page 2**: Description of the export format:
- Exports are in **TSV (Tab-Separated Values)** format
- The EHI Export feature supports **single-patient** or **full practice population** export
- For bulk/population exports, a **separate TSV file is generated for each resource type**
- Each row in a resource file represents one patient's data
- Includes a brief TSV example showing PatientID, FirstName, LastName, DOB, Gender columns
- Lists programs that can open TSV files (Excel, Google Sheets, Notepad, Python/R)

**Pages 3-4**: A bulleted list of 47 "Supported Resources" — the resource types available for export:

Allergies, Appointment reminders, Appointments, Assessments, Care plans, Cognitive statuses, Diet, Document Details, Encounter built procedures, Encounters, Exam, Family history, Family history diseases, Follow up appointments, Functional statuses, Goals, Immunizations, Implantable devices, Interventions, Lab order diagnosis, Lab Orders, Lab test result notes, Lab test results, Lab tests, Medications, Past medical history, Past surgeries, Patient addresses, Patient care team members, Patient contacts, Patient information, Patient insurances, Patient payments, Patient races, Patient tasks, Patient vitals, PHQ 9 screening, Pregnancy status, Prior authentication, Problems, Progress notes, Related person details, SDOH, Smoking status, Social history, Unsigned documents, Vaping status.

The PDF contains **no embedded URLs**, **no attachments**, and **no links to additional resources**. The PDF metadata shows it was authored by "Abdur Rehman" and created on December 3, 2025, converted from a Word document via "Microsoft: Print To PDF."

## Export Coverage Assessment

### Data Domain Coverage

The 47 resource types listed in the documentation suggest that summitEHR has attempted a genuine (b)(10) export — this is not merely a FHIR (g)(10) repackaging. The resource list goes well beyond USCDI/US Core, including several data types that would not be found in a standard FHIR API:

**Clearly covered domains:**
- **Demographics**: Patient information, Patient addresses, Patient contacts, Patient races
- **Problems/Diagnoses**: Problems
- **Medications**: Medications
- **Allergies**: Allergies
- **Lab data**: Lab Orders, Lab order diagnosis, Lab tests, Lab test results, Lab test result notes
- **Vitals**: Patient vitals
- **Immunizations**: Immunizations
- **Implantable devices**: Implantable devices
- **Family history**: Family history, Family history diseases
- **Clinical notes**: Progress notes, Unsigned documents
- **Care plans**: Care plans, Goals, Interventions
- **Encounters**: Encounters, Encounter built procedures, Exam
- **Social determinants**: SDOH, Social history, Smoking status, Vaping status
- **Behavioral/screening**: PHQ 9 screening, Assessments, Cognitive statuses, Functional statuses
- **Insurance**: Patient insurances
- **Payments**: Patient payments
- **Scheduling**: Appointments, Appointment reminders, Follow up appointments
- **Care team**: Patient care team members, Related person details
- **Other clinical**: Diet, Pregnancy status, Past medical history, Past surgeries, Prior authentication, Document Details, Patient tasks

**Potential gaps or unclear areas:**
- **Prescriptions/e-prescribing data**: "Medications" is listed but there's no separate resource for prescription orders, refill history, pharmacy routing data, or controlled substance prescriptions (EPCS). Given the NewCrop integration for e-prescribing, this data may be in the "Medications" resource, but it's unclear.
- **Billing/claims detail**: "Patient payments" and "Patient insurances" are present, which is encouraging. However, there's no resource for charges, claims, billing codes, or superbills. The product research was unclear on whether summitEHR has integrated billing; if it does, the export may be missing billing detail.
- **Referrals**: No resource for referral orders or referral tracking.
- **Telehealth session data**: The product supports telehealth, but no resource specifically covers telehealth encounters or session records (these may be captured under "Encounters").
- **Patient portal messages / Secure messaging**: Not listed as a resource type, despite the product supporting secure messaging.
- **Direct messages**: Not listed, though the product is certified for Direct messaging (h)(1).
- **Clinical quality measure data**: Not listed as a resource, though the product is certified for CQM (c)(1)-(c)(3).

### Export Format & Standards

The export uses **TSV (Tab-Separated Values)** — a simple, non-standard but highly portable flat-file format. This is a reasonable choice for a (b)(10) export:

- TSV is easy to parse and process with any programming language or spreadsheet tool
- One file per resource type is a clean organizational model
- Each row represents one patient, which is simple but potentially limiting for resources with one-to-many relationships (e.g., a patient with multiple allergies — it's unclear whether multiple allergies produce multiple rows or are concatenated into one row)

**Critical limitation**: There is no documentation whatsoever of the **columns/fields** in each TSV file. The documentation provides a single trivial example (PatientID, FirstName, LastName, DOB, Gender) but does not define:
- What columns appear in each of the 47 resource files
- Data types for each column
- Value sets or coded values
- How relationships between resources are expressed (foreign keys, patient identifiers)
- How multi-valued fields are handled
- Date/time formats
- How null/empty values are represented
- Character encoding

Without field-level documentation, a recipient of the export would have to reverse-engineer the meaning of each column from the data itself. This is a significant gap.

### Documentation Quality

The documentation is **extremely minimal**. At 4 pages (with one being a cover page and one being mostly blank), this is among the thinnest EHI export documentation possible:

- **No data dictionary**: Just a list of 47 resource names with no field definitions
- **No schema**: No TSV header definitions, no JSON schema, no formal specification
- **No sample data**: Only a trivial example of a patient demographics snippet
- **No export instructions**: Only says the feature "lets you manually export" — no screenshots, no step-by-step walkthrough, no explanation of where to find the feature in the UI
- **No worked examples**: No real-world sample export files
- **No versioning/changelog**: Only the v1.0 designation

A developer receiving this export would know they're getting TSV files for 47 resource types, but would have no guidance on interpreting the data beyond column headers in the files themselves.

### Structure & Completeness

- **Granularity**: Resource-name level only. No field-level documentation at all.
- **Coded fields**: Not documented. No value sets specified.
- **Relationships**: Not documented. No description of how to link data across the 47 resource files.
- **Data types**: Not specified.
- **Versioning**: v1.0 only, no change history.

The documentation reads like a compliance checkbox — a minimal document created to satisfy the (b)(10) certification requirement. The list of 47 resources suggests the vendor has thought about which data to include, but the total absence of field-level documentation makes the export effectively opaque to anyone who doesn't already have access to the system.

### Overall Assessment

summitEHR's EHI export approach has a **promising scope** — the 47 resource types cover most of the clinical data domains you'd expect from an ambulatory EHR, plus insurance and payment data. The use of TSV rather than FHIR suggests this is a genuine (b)(10) effort, not a (g)(10) repackaging.

However, the documentation is **critically incomplete**. A list of resource names without field definitions is barely better than no documentation at all. The product was certified very recently (August 2025, with the PDF created December 2025), and this appears to be a v1.0 startup EHR with minimal documentation infrastructure. The quality of the documentation may improve over time, but as it stands, a data recipient would need the actual export files to understand what's in them.

## Access Summary
- Final URL (after redirects): https://static1.squarespace.com/static/692e09ea4112f840c4fb54d8/t/69307ee493279950e0b33148/1764785893013/EHI+Export+Documentation+-+SummitEHR+v1.0.pdf
- Status: found
- Required browser: no
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends
None. The URL resolved directly to a publicly accessible PDF with no authentication, CAPTCHAs, or anti-bot measures. The Squarespace CDN served the file immediately.
