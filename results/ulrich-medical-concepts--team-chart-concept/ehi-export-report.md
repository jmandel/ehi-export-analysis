# Ulrich Medical Concepts — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://ulrichmedicalconcepts.com/home/the-ehr/meaningful-use/cost-disclosure-and-transparency/
- CHPL IDs: 10227
- Product: Team Chart Concept (TCC) v7.1
- Certification Date: 2019-12-26

## Navigation Journal

### Step 1: Probe the registered URL
```bash
curl -sI -L "https://ulrichmedicalconcepts.com/home/the-ehr/meaningful-use/cost-disclosure-and-transparency/" \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
```
Result: HTTP 200, `Content-Type: text/html; charset=UTF-8`. WordPress site behind Sucuri/Cloudproxy CDN. Page loaded directly, no redirects.

### Step 2: Fetch and examine the page
```bash
curl -sL "https://ulrichmedicalconcepts.com/home/the-ehr/meaningful-use/cost-disclosure-and-transparency/" \
  -H 'User-Agent: Mozilla/5.0' -o cost-disclosure-and-transparency.html
```
The page is titled "Disclosure and Transparency" — a mandatory ONC compliance/cost disclosure page built with Elementor on WordPress. It contains:
- Certified EHR vendor/product information table
- Clinical Quality Measures list
- Certification Criteria table (all 26+ criteria listed)
- A single footnote about the (b)(10) EHI export
- Cost transparency information
- Application Access API additional information with links to Interoperability Engine docs

### Step 3: Identify the EHI export documentation
The entire (b)(10) EHI export documentation on this page consists of a single footnote attached to the certification criteria listing:

> **§170.315(b)(10) Electronic Health Information (EHI) Export\***
>
> *EHI can be exported in PDF or C-CDA format. Records for a patient are exported to one or more PDF/C-CDA files. The files created by the export are saved to a folder specified by the user.*

That is the complete EHI export documentation. There are no links to a data dictionary, schema, user guide, sample files, or any additional technical documentation about the export.

### Step 4: Check linked resources
The page links to three external resources under "Application Access API Additional Information":
1. **Interoperability Engine Open API Documentation**: https://www.interopengine.com/2021/open-api-documentation.html — This is the FHIR R4 API documentation from EMR Direct. It covers the (g)(10) standardized API, not the (b)(10) EHI export. The documentation describes a read-only RESTful FHIR R4 API with OAuth 2.0 authentication, supporting US Core Implementation Guide resources. No mention of EHI, (b)(10), or bulk data export for all health information.
2. **Interoperability Engine Open API Terms of Use**: https://www.interopengine.com/open-api-terms.html — API terms of service, not relevant to EHI export.
3. **FHIR R4 Endpoints JSON**: https://appstudio.interopengine.com/partner/fhirR4endpoints-umc.json — Returns a nearly empty FHIR Bundle: `{"resourceType":"Bundle","type":"collection","timestamp":"2026-02-07T14:37:24-08:00"}` with no actual endpoint entries. This suggests no UMC customers have active FHIR API integrations.

### Step 5: Explore the broader UMC site
Checked the sitemap (`/wp-sitemap-posts-page-1.xml`) for all pages on the site. Relevant pages checked:

- **/home/the-ehr/interoperability/** — General interoperability marketing content about HIE connectivity, cancer registry reporting, and HIMSS conference participation. No EHI export details.
- **/home/the-ehr/meaningful-use/** — Marketing page about Meaningful Use incentives and cancer registry reporting. No EHI export details.
- **/onc-real-world-testing/** — Links to Real World Testing plan and results PDFs (2022-2025).

### Step 6: Examine Real World Testing documents for EHI export details
The 2025 RWT Plan PDF (https://elearning.ulrichmedicalconcepts.com/RWT/2025_RWT_Plan_Ulrich_Medical_Concepts.pdf) contains the most detail about the EHI export:

**EHI Export Single** (§170.315(b)(10)):
> "This test is completed by selecting a single patient in the Team Chart Concept product as user that has permission to complete a chart export and running the chart export routine to export the patient's chart to PDF and C-CDA file(s). If a PDF is generated the result has been met successfully."

**EHI Export Multiple** (§170.315(b)(10)):
> "This test is completed by retrieving a list of patients in the Team Chart Concept product as user that has permission to complete a chart export and running the chart export routine to export each patient's chart to PDF and C-CDA file(s). If multiple PDFs are generated the result has been met successfully."

**Notable finding**: The 2025 RWT Results Report (4 pages) covers outcomes for API Patient, API Data All, and API Data Category — but **omits the EHI Export Single and EHI Export Multiple outcomes entirely**. The results report only has 3 measures in its outcomes table despite the plan including 12 measures. All three tested measures note: "No customers opted to implement."

### Step 7: Full-page screenshot
Captured a full-page screenshot of the disclosure page using Chrome DevTools.

## What Was Found

The EHI export documentation for Team Chart Concept is extraordinarily minimal. The entire public-facing description of the (b)(10) export consists of a **single sentence footnote** on the vendor's mandatory disclosure page:

> *EHI can be exported in PDF or C-CDA format. Records for a patient are exported to one or more PDF/C-CDA files. The files created by the export are saved to a folder specified by the user.*

From the RWT plan, we learn slightly more: the export is called a "chart export routine" that can be run for a single patient or a list of patients, and it requires a user with "permission to complete a chart export." The success criterion is simply "if a PDF is generated."

There is no:
- Data dictionary or field listing
- Schema definition
- Export format specification beyond "PDF or C-CDA"
- Sample export files
- User guide or instructions
- API specification for the export
- Description of what data is included in the export
- Description of what data is excluded from the export
- Information about C-CDA template conformance or profile
- Documentation of the export's relationship to the FHIR API

The linked Interoperability Engine documentation covers the FHIR R4 API for (g)(10) compliance and is a completely separate mechanism from the (b)(10) export. The FHIR endpoints JSON for UMC customers is empty, suggesting no active FHIR integrations.

## Export Coverage Assessment

### Data Domain Coverage

Based on the product research, Team Chart Concept manages:
- **Clinical data**: Demographics, encounters, problem lists, medications, allergies, immunizations, vitals, health maintenance, implantable devices, clinical decision support, quality measures
- **Order data**: Lab orders/results, medication orders, diagnostic imaging orders
- **Prescribing data**: E-prescriptions (via NewCrop), medication history
- **Practice management**: Scheduling, billing, claims, financial reports, ICD-10 codes
- **Document management**: Scanned documents, office forms, patient chart documents
- **Patient engagement**: Portal interactions, patient communications
- **Interoperability data**: C-CDA documents, HL7 messages, FHIR resources

**Coverage assessment is essentially impossible** because the vendor provides no data dictionary, field listing, or any description of what the export includes. The documentation says "records for a patient are exported" but never defines what constitutes a "record."

**What we can infer:**
- **PDF export**: A PDF rendering of the patient chart likely captures whatever is displayed in the EHR's chart view — probably clinical notes, demographics, medications, problem lists, allergies, vitals, and lab results. However, PDFs are not computable. Billing data, scheduling data, and structured coded data are likely lost or flattened.
- **C-CDA export**: C-CDA documents follow a defined standard (CCD, CCD-A, or referral note templates). If this is the same C-CDA used for Transitions of Care (b)(1), it would cover the USCDI subset: demographics, problems, medications, allergies, immunizations, vital signs, procedures, results, and care team. This would miss billing data, scheduling, custom forms, document attachments, and any specialty-specific data.

**Likely missing domains** (based on typical PDF/C-CDA limitations):
- Billing records and claims data (TCC is an integrated PM system — billing is a core function)
- Scheduling/appointment data
- Custom "User Defined Records" (a TCC feature for ad-hoc reporting)
- Scanned document attachments and digitized historical records
- Lab order details (as distinct from results)
- E-prescribing history from NewCrop integration
- Patient portal interaction data
- Direct messaging correspondence
- Cancer registry submission data
- Health maintenance alerts and reminders

### Export Format & Standards

The export uses two formats:
1. **PDF** — A non-computable, human-readable rendering. Useful for visual review but cannot be programmatically parsed, queried, or imported into another system with any reliability. The PDF format fundamentally cannot satisfy the spirit of (b)(10), which requires export of data in a form that preserves its structure and utility.
2. **C-CDA** — A structured clinical document standard (HL7 CDA R2). While computable, C-CDA is designed for clinical summaries, not comprehensive data export. It covers a subset of clinical data aligned with USCDI/US Core but lacks representations for billing, scheduling, custom forms, and many specialty-specific data types.

Neither format is appropriate for a comprehensive EHI export of all electronic health information stored by an integrated EHR and practice management system. A database dump, CSV export of all tables, or even a FHIR Bulk Data export with custom extensions would be more appropriate.

The RWT plan describes the export success criterion as "if a PDF is generated" — the bar for success is whether a file was created, not whether it contains all EHI.

### Documentation Quality

The documentation quality is **extremely poor** — effectively nonexistent:
- No data dictionary
- No field-level definitions
- No data types, value sets, or constraints
- No worked examples or sample export files
- No user guide for performing the export
- No description of what data is included or excluded
- A developer could not implement an import based on this documentation
- The documentation consists of a single footnote

The RWT plan adds marginal detail (describing the export as a "chart export routine" with user permission requirements and single/multiple patient modes), but this is operational testing documentation, not export format documentation.

This is clearly a compliance checkbox exercise, not a genuine effort to document the EHI export.

### Structure & Completeness

There is no structured documentation to assess. The vendor has:
- **Zero** tables, fields, or columns documented
- **Zero** relationships or entity descriptions
- **Zero** value set or coded field documentation
- **Zero** versioning or change history
- **Zero** schema or format specification

The vendor's certified criteria include (b)(10) since December 2019. Over six years later, the public documentation still consists of a single sentence.

### The (b)(10) vs (g)(10) Situation

In this case, the vendor does **not** conflate (b)(10) with (g)(10) — the EHI export (PDF/C-CDA files saved locally) is clearly distinct from the FHIR API (Interoperability Engine). However, the FHIR API (g)(10) is equally undocumented from UMC's perspective — they rely entirely on EMR Direct's generic Interoperability Engine documentation, and the FHIR endpoints JSON shows zero active customer integrations.

The real issue is that the vendor appears to have done the absolute minimum: a basic "chart export to PDF" function and a C-CDA export (which they likely already had for Transitions of Care (b)(1) compliance), with no thought given to whether these formats actually capture all electronic health information in the designated record set.

## Access Summary
- Final URL (after redirects): https://ulrichmedicalconcepts.com/home/the-ehr/meaningful-use/cost-disclosure-and-transparency/
- Status: found
- Required browser: no (static HTML, works with curl)
- Navigation complexity: direct_link (everything is on the single registered page)
- Anti-bot issues: none (Sucuri/Cloudproxy CDN, but no blocking)

## Obstacles & Dead Ends
- The FHIR endpoints JSON (fhirR4endpoints-umc.json) is effectively empty — a Bundle with no entries
- The 2025 RWT Results Report omits EHI Export outcomes despite the plan including them
- No additional EHI export documentation found anywhere on the UMC site (checked sitemap, interoperability page, meaningful use page, and real-world testing page)
- No downloadable PDFs, ZIPs, or data dictionary files linked from the disclosure page
- The Interoperability Engine API docs are generic EMR Direct documentation, not UMC-specific
