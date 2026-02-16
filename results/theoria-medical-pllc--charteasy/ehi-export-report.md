# Theoria Medical, PLLC — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://theoriamedical.com/ehr-certificate
- CHPL ID: 11542
- Product: ChartEasy™ v1.5
- Certification Date: 2024-12-04

## Navigation Journal

### Step 1: Probe the registered URL
```bash
curl -sI -L "https://theoriamedical.com/ehr-certificate" -H 'User-Agent: Mozilla/5.0'
```
Returned HTTP 200 with `Content-Type: text/html; charset=utf-8`, powered by Next.js. No redirects.

### Step 2: Download and examine the page
```bash
curl -sL "https://theoriamedical.com/ehr-certificate" -H 'User-Agent: Mozilla/5.0' -o ehr-certificate-page.html
```
16,621 bytes. Static HTML rendered by Next.js. The page contains:
- ONC Certification overview text
- Certification details (developer, date, product, CHPL number)
- Tab buttons showing 34 certification criteria and 10 CQMs
- Real-World Testing Plans and Reports (6 PDF links, all regulatory filings)
- **EHI Export (b)(10) section** — a text-only attestation statement
- Intervention Risk Management section (about predictive models)

### Step 3: Search for downloadable documentation
```bash
grep -oiE 'href="[^"]*\.(pdf|zip|xlsx|xls|csv|json|doc|docx|yaml|yml)[^"]*"' /tmp/theoria-page.html
```
Found 6 PDF links — all are Real-World Testing Plans/Reports, not EHI export documentation:
- `TheorialMedical_Real_World_Test_Plan_CY2023_22Nov2022.pdf`
- `TheorialMedical_Real_World_Test_Plan_CY2024_19Oct2023.pdf`
- `TheoriaMedical_Real_World_Test_Results_CY2023_26Jan2024.pdf`
- `TheoriaMedical_Real_World_Test_Results_CY2024_26Feb2025.pdf`
- `TheorialMedical_Real_World_Test_Plan_CY2025_07Oct2024.pdf`
- `TheoriaMedical_Real_World_Test_Results_CY2025_03Feb2026.pdf`

No EHI export data dictionaries, schemas, format specs, or downloadable export documentation found.

### Step 4: Extract the (b)(10) statement
The full text of the EHI export section:

> **Support for EHI Export in Accordance with ONC Health IT Certification Criterion 170.315(b)(10)**
>
> Theoria Medical hereby attests and confirms its commitment to enhancing patient access to their Electronic Health Information (EHI). Our Electronic Health Record system, ChartEasy™, is designed in alignment with the ONC Health IT Certification criterion 170.315(b)(10) pertaining to EHI Export.
>
> Patients can readily export their EHI in the following ways:
>
> 1. Direct Patient Access via ChartEasy Patient Portal: Theoria offers patients direct access to their EHI via the ChartEasy Patient Portal. This portal is designed to be user-friendly and secure, ensuring that patients can conveniently retrieve their information whenever needed. Records may be exported as both PDF and CCDA format.
>
> Web: https://patient-portal.charteasy.com/
> iOS App: https://apps.apple.com/us/app/charteasy-patient-portal/id1564972475
>
> 2. Request to Theoria Medical Records Team: In instances where further assistance or specific record retrieval is required, patients may forward their request to Theoria's dedicated medical records team. Please send all such inquiries to: records@theoriamedical.com. Records may be exported as both PDF and CCDA format.
>
> Theoria Medical takes pride in its unwavering dedication to patient privacy, security, and transparency. We continue to strive for excellence and adherence to standards that benefit both healthcare professionals and patients.

### Step 5: Check the patient portal
```bash
curl -sI "https://patient-portal.charteasy.com/" -H 'User-Agent: Mozilla/5.0'
```
Returned HTTP 200. The portal is a Flutter web application (v2.0.8) requiring login. The landing page describes four features:
1. Access Chronic Care Management Plan
2. View Lab and Imaging Results
3. View Medication Lists
4. **Download and Transmit your records** — "complete and full access to your personal records while also being able to allow any other authorized representatives you choose to have access to your records, or simply use the portal to transmit your information to whomever you want, including other healthcare providers."

No public documentation about export format, CCDA structure, or data dictionary is accessible without logging in.

### Step 6: Check the iOS App Store listing
The ChartEasy Patient Portal iOS app (v2.0.7, released December 15, 2025) describes:
- View, download, and transmit health records
- Real-time access to lab results and vital signs
- Current medication lists
- CCM care plans
- Signed encounter records (added in v2.0.4)
- Ability to share records with authorized representatives and other providers

No additional detail about export format or data dictionary.

### Step 7: Check the developer portal
The search results reference a FHIR API developer portal at `developer.charteasy.com`.
```bash
curl -sI -L "https://developer.charteasy.com/" -H 'User-Agent: Mozilla/5.0' --max-time 15
```
Connection timed out (curl exit code 28). The site appears to be down or unreachable. No Wayback Machine captures exist for this domain. This portal is for the (g)(10) FHIR API, not the (b)(10) EHI export, but I investigated it in case it contained relevant documentation.

### Step 8: Search for alternative documentation locations
- Probed common paths on theoriamedical.com: `/ehi`, `/ehi-export`, `/interoperability`, `/fhir`, `/api`, `/developer`, `/onc`, `/b10` — all returned 404.
- Checked sitemap.xml — returned 404.
- Probed for undiscovered PDFs at `/pdf/ehi*.pdf`, `/pdf/ChartEasy*.pdf`, `/pdf/data-dictionary*.pdf`, `/pdf/export*.pdf` — all 404.
- Checked Compliance & Privacy page (`/compliance`) — contains only compliance program info, privacy policies, and Transparency in Coverage links. No EHI export documentation.
- Google searches for `"charteasy" EHI export data dictionary` — returned no results beyond the same certification page.

### Step 9: Took screenshots
- Full-page screenshot of the EHR certificate page
- Screenshot of the patient portal login page

## What Was Found

**The EHI export "documentation" consists entirely of a brief text attestation on the ONC certification page.** There is no data dictionary, no schema, no format specification, no API documentation, no sample data, and no downloadable artifacts of any kind.

The attestation states that the EHI export mechanism is:
1. **Patient Portal self-service** — patients log in to the ChartEasy Patient Portal and can download records in PDF and CCDA format
2. **Records request by email** — patients email records@theoriamedical.com and receive records in PDF and CCDA format

That is the entirety of what is documented. There is:
- **No data dictionary** describing what fields or tables are included in the export
- **No CCDA implementation guide or profile** describing which CCDA sections, entries, or templates are used
- **No sample exports** showing what the PDF or CCDA outputs look like
- **No schema files** (XSD, JSON Schema, OpenAPI, etc.)
- **No description of what "EHI" means** in their context — i.e., which data domains from ChartEasy are included in the export
- **No documentation of the export process** beyond "log in to the portal" or "email us"

## Export Coverage Assessment

### Data Domain Coverage

Based on the product research, ChartEasy stores:
- Patient demographics (from facility EHR integrations)
- ADT records (admission/discharge/transfer)
- Physician progress notes and encounter documentation
- Medication lists and reconciliation data
- Vital signs (manual and RPM device data)
- Lab results (from laboratory integrations)
- Diagnoses
- Implantable device information
- Clinical decision support alerts / ProphEasy RTH predictions
- Care plans (CCM)
- Scheduling data
- Secure messaging data (ChatEasy)
- RPM device readings (heart rate, respiration, SpO2, motion, presence)

The (b)(10) attestation says records are exported as "PDF and CCDA format" but provides **zero documentation about which data domains are included**. Given that the export mechanism is a patient portal that mentions "lab results, vital signs, current medications, CCM plans, and signed encounters," the export likely covers only the patient-portal-visible subset:

**Likely covered (based on portal features):**
- Lab results
- Vital signs
- Current medications
- Signed clinical encounters/progress notes
- CCM care plans

**Likely missing or unknown:**
- ADT records
- Full medication reconciliation history
- RPM device data streams (heart rate, SpO2, respiration, motion)
- ProphEasy clinical decision support predictions
- ChatEasy secure messaging content
- Scheduling data
- Historical diagnoses/problem lists (unclear if in CCDA)
- Implantable device information
- Billing data (if ChartEasy stores any — unclear)
- Integration data received from facility EHRs (demographics, diagnoses, vitals)
- Imaging reports

**It is impossible to assess completeness** because no data dictionary or content specification exists.

### Export Format & Standards

The export is stated to be **PDF and CCDA**. However:
- There is no documentation of which CCDA document type is used (CCD, Discharge Summary, Progress Note, etc.)
- There is no documentation of which CCDA sections and entries are populated
- There is no CCDA implementation guide, profile, or template list
- There is no documentation of what the PDF contains vs. what the CCDA contains
- C-CDA is a reasonable format for clinical summaries but cannot represent all of ChartEasy's data (e.g., RPM device streams, secure messages, scheduling data, CDS predictions)
- A CCDA export alone cannot satisfy (b)(10) requirements if ChartEasy stores data that doesn't map to standard CCDA sections — and it does (RPM data, ProphEasy predictions, ChatEasy messages)

This is a classic (g)(10)/(b)(10) confusion: the patient portal's view/download/transmit capability (which is the (e)(1) certification criterion) is being repackaged as the (b)(10) EHI export. The (e)(1) VDT capability exports a clinical summary; the (b)(10) requirement is to export **all** electronic health information in the designated record set.

### Documentation Quality

**Essentially non-existent.** The documentation consists of a ~150-word attestation statement. There is:
- No data dictionary
- No field-level definitions
- No data type specifications
- No value set documentation
- No sample exports
- No worked examples
- No developer-facing documentation
- No instructions beyond "log into the portal" or "email us"

A developer could not implement an import of this data based on the documentation because there is no documentation of the data format. A patient cannot understand what is included in their export because it is not specified. A regulator cannot verify completeness because there is no data dictionary to evaluate.

### Structure & Completeness

The documentation has no structure at all. It is a single paragraph of prose. There are no tables, no schemas, no field lists. The (b)(10) requirement explicitly calls for "documentation describing the format of the export" to be publicly available. This documentation falls far short of that requirement.

### Critical Assessment

This is one of the weakest (b)(10) documentation implementations possible:

1. **The export mechanism appears to be the patient portal (e)(1) VDT capability relabeled as (b)(10).** The certification page does not describe any separate bulk export or comprehensive EHI export mechanism.

2. **PDF and CCDA cannot cover all EHI** that ChartEasy stores. RPM device data, secure messages, CDS predictions, and scheduling data have no representation in C-CDA.

3. **No documentation of the export format exists.** The (b)(10) criterion requires the developer to "make publicly accessible" documentation "describing the format of the export." A sentence saying "PDF and CCDA format" does not satisfy this requirement.

4. **The developer portal (developer.charteasy.com) is unreachable.** Even if it contained relevant FHIR API documentation, that would be (g)(10) documentation, not (b)(10).

5. **Context:** Theoria Medical is a physician practice that built ChartEasy for internal use, not a traditional EHR vendor. The product was certified very recently (December 2024). This may explain the minimal documentation — the certification was obtained for compliance purposes, and the documentation requirements may not have been fully understood or prioritized.

## Access Summary
- Final URL (after redirects): https://theoriamedical.com/ehr-certificate
- Status: found
- Required browser: no (static HTML via curl, though screenshots confirmed via browser)
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends
- **developer.charteasy.com**: Connection times out. No Wayback Machine captures. Would have been the FHIR API developer portal but is unreachable.
- **Patient portal**: Requires login. No public-facing export documentation.
- **No alternative documentation paths**: Exhaustively probed common paths, searched Google, checked the compliance page. No additional EHI export documentation exists on the public site.
- **No downloadable artifacts**: The only PDFs on the site are Real-World Testing Plans/Reports, which are regulatory filings unrelated to EHI export.
