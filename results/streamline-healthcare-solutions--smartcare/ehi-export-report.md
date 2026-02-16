# Streamline Healthcare Solutions — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://streamlinehealthcare.com/electronic-health-information-export/
- CHPL IDs: 10987
- Product: SmartCare R6
- Certification date: 2022-09-15

## Navigation Journal

1. Probed the registered URL with curl:
   ```bash
   curl -sI -L "https://streamlinehealthcare.com/electronic-health-information-export/" -H 'User-Agent: Mozilla/5.0'
   ```
   Result: HTTP 200, Content-Type text/html, WordPress site (Apache).

2. Downloaded the full HTML page:
   ```bash
   curl -sL "https://streamlinehealthcare.com/electronic-health-information-export/" -H 'User-Agent: Mozilla/5.0' -o ehi-export-page.html
   ```

3. Searched for downloadable file links (PDF, ZIP, XLSX, etc.) — found **none**. The page contains only inline text and links to external HL7 C-CDA specification pages on build.fhir.org.

4. Retrieved structured content via WordPress JSON API:
   ```bash
   curl -sL "https://streamlinehealthcare.com/wp-json/wp/v2/pages/13869" -H 'User-Agent: Mozilla/5.0'
   ```
   This confirmed the page was published 2023-11-16 and last modified 2023-12-05.

5. Took full-page screenshot in browser (page loaded successfully after initial timeout).

6. Checked the mandatory disclosures page (https://streamlinehealthcare.com/meaningful-use/) for additional EHI export documentation. Found:
   - A link back to the EHI export page
   - A link to FHIR API documentation at `https://dhfhirpresentation.smartcarenet.com/streamline/basepractice/r4/Home/ApiDocumentation` (this is the (g)(10) FHIR API, separate from the (b)(10) export)
   - Real World Testing documents — checked the 2025 RWT Results (PDF, 21 pages) for b(10) details

7. The 2025 RWT Results PDF confirms that the b(10) EHI export functionality exists but has had **zero customer adoption** during the testing period. No export files were created by any customer.

## What Was Found

The EHI export documentation is a single WordPress page with no downloadable files, no data dictionary, no sample exports, and no schema documentation.

### Export Format
The documentation states that the EHI export produces **C-CDA (Consolidated Clinical Document Architecture)** files — described as "CCDAs or patient summary documents that are XML-based exports meeting the standard defined by HL7." The export format is the HL7 C-CDA 2.2 standard.

### Data Included
The page lists 17 C-CDA sections that are included in the export, each linking to the corresponding HL7 C-CDA 2.2 StructureDefinition on build.fhir.org:

**Entries Required:**
1. Allergies and Intolerances Section
2. Medications Section
3. Problem Section
4. Procedures Section
5. Results Section
6. Immunizations Section
7. Vital Signs Section

**Entries Optional:**
8. Advance Directives Section
9. Encounters Section

**Other Sections:**
10. Family History Section
11. Functional Status Section
12. Medical Equipment Section
13. Payers Section
14. Plan of Treatment Section
15. Social History Section
16. Mental Status Section
17. Nutrition Section

### Export Process
The page claims the export:
- Allows single-patient or population export at any time without developer assistance
- Is limited to system administrators and permissioned SmartCare users
- Creates exports in electronic and computable format
- Detailed setup instructions are "available to all Streamline customers in the help desk documentation" (not publicly accessible)
- No additional cost for Streamline customers

### Real World Testing Findings
The 2025 RWT Results (January 2026) provide critical context:
- **0 export files created** during the 90-day evaluation period
- **0 executions** of the on-demand export
- **No customer usage** of role-based export controls
- **0 computable exports generated**
- **0 patient population exports**
- The report states: "While the functionality has been fully implemented, tested, and successfully demonstrated, there has been no customer adoption to date."

## Export Coverage Assessment

### Data Domain Coverage

This is the most critical finding: **SmartCare's EHI export is a C-CDA patient summary, not a comprehensive EHI export.** The C-CDA format covers a standard clinical summary — essentially the same data as a Continuity of Care Document. This is a narrow subset of what SmartCare stores.

**Clearly missing from the export (based on product research):**

- **Behavioral health-specific data**: Progress notes, treatment plans, assessments, the "golden thread" documentation linking presenting problems to diagnoses to treatment goals to interventions — this is the *core clinical data* for a behavioral health EHR and none of it maps to standard C-CDA sections
- **Custom forms and screening tools**: PHQ-9, AUDIT, DAST, and other behavioral health screening instruments that are fundamental to this type of product
- **Billing and revenue cycle data**: Claims (837), remittance advice (835), billing status, reimbursement records, denial tracking — none of this is in a C-CDA
- **MCO module data**: Provider contracts, credentialing, authorization tracking, utilization management reviews, capitation data — entirely absent
- **Case management data**: Client tracking, document due dates, compliance deadlines, event tracking flags
- **Administrative data**: Scheduling, program enrollment/discharge records, staff assignments, bed management (for inpatient)
- **Care coordination data**: Referral tracking, transitions of care documentation beyond what's in C-CDA
- **Substance use disorder specific data**: SUD treatment records, which may have additional privacy protections (42 CFR Part 2)
- **Foster care/adoption data**: Entirely specific to this vendor's specialty market
- **IDD (Intellectual/Developmental Disabilities) data**: Service plans, habilitation records
- **Audit logs**: System access and usage records
- **Patient portal data**: Messages, portal access records
- **Business intelligence/reporting data**: Data warehouse contents, dashboards
- **Telehealth session data**: Remote service delivery records
- **Electronic signature data**: Signature pad capture records

**What IS covered:**
Standard clinical summary data — allergies, medications, problems, procedures, lab results, immunizations, vital signs, encounters, payers, social history, advance directives, and a few other standard sections. This is approximately what you'd get from the (g)(10) FHIR API or any standard clinical data exchange — it's a patient summary, not "all electronic health information."

**The fundamental mismatch**: SmartCare is a comprehensive behavioral health EHR with billing, MCO management, case management, IDD services, foster care tracking, and dozens of custom clinical forms. A C-CDA export covers perhaps 10-15% of the data the system stores. The export documentation makes no mention of behavioral health-specific data at all — which is the entire purpose of this product.

### Export Format & Standards

- **Format**: C-CDA 2.2 (XML-based)
- **Standard**: HL7 Consolidated Clinical Document Architecture
- **Appropriateness**: C-CDA is a recognized clinical document exchange standard, but it is fundamentally inappropriate as the sole EHI export format for a behavioral health EHR. C-CDA was designed for clinical summaries exchanged between healthcare providers, not for comprehensive data export. A behavioral health EHR stores vast amounts of data (treatment plans, progress notes, custom assessments, billing, case management) that have no C-CDA representation.
- **Third-party reconstruction**: A recipient of this C-CDA export could reconstruct a basic clinical summary of the patient. They could **not** reconstruct the patient's behavioral health treatment record, billing history, case management records, or any of the specialty-specific data that makes SmartCare a behavioral health product.

### Documentation Quality

- **Extremely thin**: The entire documentation is a single web page with approximately 200 words of substantive content
- **No data dictionary**: No field-level documentation of what data elements appear in each C-CDA section, what vocabularies are used, or how SmartCare-specific data maps to C-CDA
- **No schema or profile documentation**: No CDA templates, schematron, or implementation guide beyond linking to the generic HL7 C-CDA 2.2 specs
- **No sample exports**: No example C-CDA files to show what the export actually looks like
- **No export instructions**: The page says instructions are "available to all Streamline customers in the help desk documentation" — this is behind a login wall, making it inaccessible for public review
- **No screenshots of the export interface**: The page describes the capability abstractly but doesn't show it
- **Could a developer implement an import?** Not from this documentation alone. A developer would know "it's a C-CDA" but nothing about SmartCare-specific extensions, OIDs, vocabulary choices, or data mapping decisions.

### Structure & Completeness

- **Granularity**: Section-level only. The documentation lists 17 C-CDA section names with no further detail about fields, data types, constraints, or value sets within those sections.
- **Coded fields**: Not documented. The page doesn't mention what code systems are used for diagnoses, medications, procedures, etc. (the product research mentions SNOMED CT, LOINC, RxNorm, ICD-10-CM, but the export documentation doesn't).
- **Relationships**: Not documented.
- **Versioning**: The page was published November 2023 and last modified December 2023. No change history.

### Overall Assessment

Streamline Healthcare Solutions' EHI export documentation represents a **minimal compliance effort** that does not meaningfully address the (b)(10) requirement. The vendor has taken a standard C-CDA patient summary — essentially the same clinical data already available through their (g)(10) FHIR API — and labeled it as their EHI export.

For a **behavioral health** EHR, this approach is particularly inadequate. The vast majority of data that makes SmartCare useful — behavioral health assessments, treatment plans, progress notes, the "golden thread" documentation, substance use disorder records, case management, billing, MCO administration — has no representation in a C-CDA document. The export is a clinical summary, not a comprehensive data export.

The zero customer adoption reported in the 2025 RWT results, combined with the instruction that setup documentation is only available in the customer help desk (not publicly), suggests this feature exists primarily for certification purposes rather than practical use.

## Access Summary
- Final URL (after redirects): https://streamlinehealthcare.com/electronic-health-information-export/
- Status: found
- Required browser: no (curl works fine; browser used for screenshots)
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends
- No downloadable files on the EHI export page itself — everything is inline text
- Export setup instructions are behind a customer help desk login wall
- The FHIR API documentation (https://dhfhirpresentation.smartcarenet.com/streamline/basepractice/r4/Home/ApiDocumentation) is the (g)(10) API, not the (b)(10) EHI export — these are separate systems
- All links on the EHI export page go to build.fhir.org (external HL7 specs), which are external standards documentation not specific to this vendor
