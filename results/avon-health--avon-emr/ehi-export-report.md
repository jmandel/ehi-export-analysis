# Avon Health — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://avonhealth.com/meaningful-use
- CHPL IDs: 11636 (15.04.04.3227.Avon.01.00.1.250514)
- Certification Date: May 14, 2025

## Navigation Journal

1. **Probed registered URL** with curl:
   ```bash
   curl -sI -L "https://avonhealth.com/meaningful-use" -H 'User-Agent: Mozilla/5.0'
   ```
   Result: HTTP 200, `text/html; charset=utf-8`, 62,091 bytes. Next.js app hosted on Vercel.

2. **Examined page content.** The page is the "Avon Health ONC Certification" page listing all certified criteria, costs, MFA details, SVAP notices, and two links at the bottom:
   - "EHI Export Documentation" → `https://guides.avonhealth.com/docs/ehi-export`
   - "API Documentation" → `https://docs.avonhealth.com`

3. **Searched for downloadable files** on both the certification page and EHI export page:
   ```bash
   grep -oiE 'href="[^"]*\.(pdf|zip|xlsx|xls|csv|json|doc|docx|yaml|yml)[^"]*"' /tmp/avon-page.html
   grep -oiE 'href="[^"]*\.(pdf|zip|xlsx|xls|csv|json|doc|docx|yaml|yml)[^"]*"' /tmp/ehi-export-page.html
   ```
   Result: No downloadable files found on either page.

4. **Fetched and saved EHI export documentation page:**
   ```bash
   curl -sL "https://guides.avonhealth.com/docs/ehi-export" -H 'User-Agent: Mozilla/5.0' -o downloads/ehi-export.html
   ```
   Result: 52,873 bytes of HTML (Next.js SSG page with embedded structured JSON content).

5. **Took full-page screenshots** of both the certification page and the EHI export documentation page in a browser.

6. **Checked API documentation site** at `https://docs.avonhealth.com`. This is a separate REST API reference site with detailed resource documentation (Patient, Allergy, Condition, Medication, etc.). However, the EHI export documentation does not reference the API as its export mechanism — the export produces a ZIP file with CSVs, PDFs, and PNGs. The API documentation is for the (g)(10) FHIR API and general REST API, not for the (b)(10) export.

## What Was Found

The EHI export documentation lives at a single page on the Avon Health guides site: `https://guides.avonhealth.com/docs/ehi-export`. The page describes:

### Export Mechanism
- **Single patient export**: An admin navigates to a patient's profile and clicks the "Export EHI" button.
- **Patient population export**: Must be requested from the Avon Support team via email to support@avonhealth.com with subject line "Patient Population b10 Export Request". This is handled manually as it depends on data size and server resources.

### Export Format
The export produces a **.zip file** containing:
- **CSV files** — structured data
- **PDF documents** — clinical documents
- **PNG images** — uploaded images
- **Dedicated folder per patient** (for population exports, named `<FirstName><LastName>_<MRN>`)

The contents of each patient directory in a population export mirror those of the individual patient export.

### Data Categories
The documentation lists data categories organized as:

**Demographics**: Name, Date of birth, Sex, Race and ethnicity, Language preferences, Addresses

**Clinical Information**: Allergies and adverse reactions, Medications (including prescription history and active medications), Problem list (diagnoses), Immunizations, Family history, Vital signs, Procedures, Surgical history, Lab results, Imaging results, Clinical notes (progress notes, H&P, discharge summaries), Care plans

**Administrative and Billing Information**: Appointments, Insurance details, Insurance claims, Payment history

**Other Documents**: Forms, Uploaded documents (PDFs) and images (PNGs)

### What Is NOT Provided
- No data dictionary with field-level definitions, data types, or column descriptions
- No sample export files or example CSVs
- No schema files (no XSD, JSON Schema, OpenAPI spec, DDL)
- No documentation of the CSV file structure (column names, data types, relationships between files)
- No documentation of how many CSV files are generated or what each one contains
- No documentation of coded values or value sets used in the export
- No screenshots of the export interface or example output

## Export Coverage Assessment

### Data Domain Coverage

Comparing against the product research, which identifies Avon EMR as a comprehensive ambulatory EMR with clinical, scheduling, messaging, billing, patient engagement, and AI features:

**Clearly covered domains:**
- Demographics (name, DOB, sex, race/ethnicity, language, addresses)
- Problem lists / diagnoses
- Medications and prescription history
- Allergies and adverse reactions
- Immunizations
- Family history
- Vital signs
- Procedures and surgical history
- Lab results
- Imaging results
- Clinical notes (progress notes, H&P, discharge summaries)
- Care plans
- Insurance details and claims
- Payment history
- Appointments
- Forms (patient-submitted intake forms, etc.)
- Uploaded documents and images

**Domains mentioned in product research but absent or ambiguous in export documentation:**
- **Messaging data** — The product has in-app messaging, 2-way SMS, and internal notes. These are not mentioned in the export.
- **Prescriptions (e-prescribing details)** — "Medications, including prescription history" is listed, but it's unclear whether this includes full e-prescribing transaction data (pharmacy, fill status, etc.) or just the medication list.
- **Superbills** — The product has a superbills feature with procedure and diagnosis codes. Not mentioned in export.
- **Invoices** — The product generates invoices. Not explicitly mentioned in export.
- **Eligibility checks** — Insurance eligibility data. Not mentioned.
- **Revenue cycle management data** — The product integrates RCM. Not mentioned beyond "insurance claims" and "payment history."
- **Courses** — Patient education content. Not mentioned.
- **Tasks** — Clinical task assignments. Not mentioned.
- **Fax records** — E-faxing is a product feature. Not mentioned.
- **Custom fields and custom objects** — The product supports custom fields/objects for extensibility. Not mentioned.
- **AI Scribe transcriptions** — The product generates AI-powered visit note drafts. Not mentioned whether transcriptions or AI-generated content are included.
- **Implantable device list** — Certified under (a)(14) but not listed in export categories.
- **Clinical decision support data** — Certified under (a)(2). Not mentioned.
- **Smoking status** — A standard clinical data element. Not mentioned.

The export claims to cover "all electronic health information (EHI) that is part of the designated record set," which is promising language. However, the documentation only lists broad categories without field-level detail, making it impossible to verify what's actually included. Notably, several patient-facing data domains (messaging, superbills, invoices, custom data) are absent from the listed categories.

### Export Format & Standards

The export uses a **vendor-proprietary format**: a ZIP file containing CSV files, PDFs, and PNGs. This is not a recognized standard (not FHIR, C-CDA, or any other interoperability format), but it's a reasonable approach for a (b)(10) export — CSVs are human-readable and machine-processable, and including original documents as PDFs/PNGs preserves fidelity.

However, the documentation provides **no detail on the CSV structure**. Without knowing:
- How many CSV files are generated
- What columns each CSV contains
- What data types and formats are used
- How relationships between entities are expressed (e.g., linking a lab result to a visit)
- What coded values are used

...a third party could not reliably reconstruct the patient record from the export. They would receive a ZIP file and have to reverse-engineer the CSV structure.

### Documentation Quality

The documentation is **minimal**. It occupies a single web page with approximately 300 words of substantive content. It correctly explains what EHI is, describes two export types (single patient and population), and lists data categories at a high level.

However, it lacks:
- **Field-level documentation**: No data dictionary, no column definitions, no data types
- **Worked examples**: No sample export files or example records
- **Schema documentation**: No formal specification of the CSV file format
- **Export interface documentation**: No screenshots or step-by-step guide
- **Value set documentation**: No description of coded fields or their permissible values
- **Relationship documentation**: No description of how CSV files relate to each other

A developer could not implement an import of this data based solely on the documentation. They would need access to an actual export file to understand the structure.

### Structure & Completeness

The documentation provides **category-level granularity only** — it tells you that "Lab results" are included but not what fields a lab result record contains. This is the minimum viable documentation for a (b)(10) export: it confirms the vendor has thought about what data to include, but it doesn't provide the technical detail needed to understand or use the export.

There is no versioning or change history. The documentation appears to be a single static page created for certification purposes.

### Overall Assessment

Avon Health is an early-stage startup (certified May 2025) that has created genuine (b)(10) export documentation — this is not a repackaged FHIR API or a (g)(10)/(b)(10) conflation. The export is clearly a distinct mechanism (ZIP with CSVs) separate from their REST/FHIR API. The documentation correctly defines EHI scope and lists reasonable data categories.

However, the documentation is thin. The absence of a data dictionary, schema, or sample export means the documentation functions as a high-level description of what the export includes, not a technical specification of how it works. For a recently certified startup, this is not unusual, but it represents a significant gap for anyone trying to understand or import the exported data.

The population export requiring manual email request to the support team (rather than a self-service mechanism) is notable — it suggests the export infrastructure is not yet fully automated.

## Access Summary
- Final URL (after redirects): https://avonhealth.com/meaningful-use
- EHI Export Documentation URL: https://guides.avonhealth.com/docs/ehi-export
- Status: found
- Required browser: no (content fully accessible via curl; Next.js SSG with content in HTML)
- Navigation complexity: one_click (certification page links directly to EHI export docs)
- Anti-bot issues: none

## Obstacles & Dead Ends
None. The URL was live, the documentation page loaded cleanly, and all content was accessible without JavaScript rendering (the Next.js page uses SSG with all content embedded in the HTML source).
