# Advanced Data Systems Corporation — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://apps.medicscloud.com/B10_MedicsCloud.html
- CHPL IDs: 10786
- Product: MedicsCloud, Version 11.0
- Certification date: 2022-01-11

## Navigation Journal

1. **Initial probe** — HTTP HEAD request to the registered URL:
   ```
   curl -sI -L "https://apps.medicscloud.com/B10_MedicsCloud.html" -H 'User-Agent: Mozilla/5.0'
   ```
   Returned HTTP 200, Content-Type: text/html, 2346 bytes. No redirects. Server: Microsoft-IIS/10.0. Last-Modified: 2023-12-05.

2. **Fetched and examined the page:**
   ```
   curl -sL "https://apps.medicscloud.com/B10_MedicsCloud.html" -H 'User-Agent: Mozilla/5.0' -o B10_MedicsCloud.html
   ```
   The entire page is a single static HTML document (~2.3 KB) with Bootstrap styling. It contains:
   - A heading: "Advanced Data Systems Corporation"
   - Product identification: "MedicsCloud, Version 11.0"
   - A section titled "§ 170.315 (b)(10) Electronic Health Information export"
   - One paragraph of substantive text
   - Two links to external HL7 standards (CCDA and FHIR US Core STU3.1.1)
   - No download links, no data dictionary, no schema, no API documentation

3. **Opened the page in browser** and took a screenshot confirming the page renders as a simple text page with the paragraph and two links. No interactive elements, accordions, or hidden content.

4. **Checked for additional files on apps.medicscloud.com:**
   - Root (`/`) redirects to `http://www.adsc.com/`
   - No `robots.txt` (404)
   - Probed common paths (`/ehi`, `/b10`, `/export`, `/data-dictionary`, `/docs`, `/documentation`) — all returned 404
   - Checked for PDF version (`/B10_MedicsCloud.pdf`) — 404

5. **Checked the vendor's mandatory disclosures page** at `https://www.adsc.com/icsa-labs-onc-health-it-certification-program-medicscloud`:
   - Lists 170.315(b)(10) in a table of certified criteria
   - No additional EHI export documentation or links beyond the CHPL-registered URL
   - The only CTA is a link to request a live demonstration

6. **Web searches** for "MedicsCloud EHI export documentation data dictionary" and "medicscloud b(10)" returned no relevant results. No supplementary EHI export documentation appears to exist publicly.

7. **Wayback Machine** check: the page has been archived; the content appears unchanged from the current version (same structure and text referencing USCDI v1, CCDA, and FHIR US Core STU3.1.1).

## What Was Found

The entire EHI export documentation consists of a single paragraph:

> "MedicsCloud authorized users can generate the Electronic Health Information Export (EHI) for a single patient and also the patient population in both HL7 CCDA xml format that comply with USCDI v1 requirements standards and HL7 FHIR v 4.0.1 US Core v 3.1.1."

The page then links to:
1. The HL7 C-CDA implementation guide (external standard)
2. The HL7 FHIR US Core STU3.1.1 implementation guide (external standard)

There is no vendor-specific documentation whatsoever. No data dictionary, no field-level mapping, no schema, no API specification, no user guide, no sample data, no screenshots of the export interface.

## Export Coverage Assessment

### Data Domain Coverage

This is a textbook case of the (b)(10) vs (g)(10) conflation. The documentation explicitly states that the EHI export complies with "USCDI v1 requirements standards" using CCDA and FHIR US Core — which are the (g)(10) standardized API formats, not a comprehensive EHI export.

USCDI v1 / US Core STU3.1.1 covers a defined subset of clinical data:
- Patient demographics
- Allergies and intolerances
- Conditions/problems
- Medications/prescriptions
- Lab results/diagnostic reports
- Vital signs
- Procedures
- Immunizations
- Clinical notes (limited set)
- Care plans/goals
- Smoking status

Based on the product research, MedicsCloud stores significantly more data that would be part of the designated record set but is almost certainly **not** covered by a USCDI v1 / CCDA+FHIR US Core export:

- **Billing and claims data** — claims, claim tracking, denial records, EDI transactions, payment history, patient balances. This is core EHI (billing records about individuals) with no representation in CCDA or FHIR US Core STU3.1.1.
- **Specialty-specific clinical data** — the product supports 27+ specialties with user-definable templates. Custom clinical assessments for podiatry, ophthalmology, orthopedics, cardiology, behavioral health, pain management, etc. are unlikely to map cleanly to standard CCDA sections or US Core resources.
- **Practice management data** — scheduling, insurance verification results, insurance discovery data.
- **Patient portal interactions** — questionnaires, appointment requests, portal messages, payment transactions.
- **Remote patient monitoring data** — blood pressure, glucose, oxygen saturation readings from RPM devices.
- **Communication records** — secure messages, text interactions, fax documents.
- **Telemedicine session data** — virtual visit records.
- **Attorney/legal case management data** — personal injury/workers' comp case records.
- **CRM data** — healthcare CRM records.
- **Inventory data** — purchasable product inventory.
- **Documents and images** — scanned records, imported PDFs, fax documents.

The export format (CCDA + FHIR US Core) by definition cannot represent most of these data domains. A CCDA document and US Core FHIR resources are designed for clinical summary exchange, not for exporting the full designated record set of an ambulatory EHR with practice management, billing, and specialty-specific workflows.

### Export Format & Standards

- **CCDA XML**: Standard HL7 C-CDA format — well-defined but limited to clinical summary data
- **FHIR R4 US Core STU3.1.1**: Standard FHIR format — well-defined but limited to USCDI v1 data classes

Both are recognized standards, but neither is appropriate as the sole format for a comprehensive EHI export from a full-featured EHR+PM system. They cover the clinical summary layer but cannot represent billing records, custom specialty assessments, practice management data, or most of the non-clinical data domains this product stores.

The documentation does not describe:
- How billing data is exported (or whether it is)
- How custom/specialty clinical data is exported
- How data that doesn't fit CCDA or FHIR US Core is handled
- Whether there are additional export formats beyond CCDA and FHIR
- How relationships between records are maintained in the export

A third party could reconstruct a clinical summary from this export, but could not reconstruct the full patient record including billing, scheduling, portal interactions, specialty assessments, and other non-clinical data.

### Documentation Quality

The documentation is exceptionally sparse — a single paragraph and two links to external standards. There is:

- **No data dictionary** — no listing of tables, fields, or data elements
- **No field-level mapping** — no documentation of how MedicsCloud-specific data maps to CCDA sections or FHIR resources
- **No schema or profile documentation** — no custom profiles, extensions, or constraints
- **No sample data** — no example export files
- **No user guide** — no instructions for how to perform the export (beyond "authorized users can generate")
- **No API documentation** — no endpoint descriptions, authentication, request/response formats
- **No screenshots** — no visual documentation of the export interface

A developer could not implement an import of this data based on this documentation alone. The only guidance is "it's CCDA and FHIR US Core" — which tells you the standard but nothing about this vendor's specific implementation, data mapping, or export mechanics.

### Structure & Completeness

The documentation has essentially zero structure. There is no:
- Table/entity listing
- Field-level definitions
- Data types or constraints
- Value sets or coded field documentation
- Relationship documentation
- Versioning or change history

This appears to be a minimal compliance checkbox — the absolute minimum documentation needed to have *something* at the CHPL-registered URL. The page was last modified December 5, 2023, which aligns with the December 31, 2023 deadline for EHI export compliance, suggesting it was created close to the deadline.

## Access Summary
- Final URL (after redirects): https://apps.medicscloud.com/B10_MedicsCloud.html
- Status: found
- Required browser: no (static HTML, curl works fine)
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends
- The apps.medicscloud.com domain has no other discoverable documentation (root redirects to adsc.com, no robots.txt, common paths all 404)
- The vendor's main certification page at adsc.com lists (b)(10) as certified but provides no additional documentation
- Web searches for MedicsCloud EHI export documentation returned no results
- The two links on the page point to external HL7 standards documentation, which is not vendor-specific and was not downloaded per instructions
- The HubSpot CTA on the certification page redirects to a demo request form, not documentation
