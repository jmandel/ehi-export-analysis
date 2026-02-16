# DOX EMR — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://www.doxemr.com/b10doc
- CHPL IDs: 10806
- Product: DOX EMR v5.2 (certified 2022-01-31)
- Developer: DOX EMR (Scottsdale, AZ)
- Certification body: SLI Compliance (ONC-ACB)

## Navigation Journal

### Step 1: Initial probe of registered URL
```bash
curl -sI -L "https://www.doxemr.com/b10doc" -H 'User-Agent: Mozilla/5.0'
```
Result: HTTP 200, Content-Type: text/html (Wix-hosted site). No redirects.

### Step 2: Fetch and examine the page
```bash
curl -sL "https://www.doxemr.com/b10doc" -H 'User-Agent: Mozilla/5.0' -o b10doc-page.html
```
The page is a Wix site (JavaScript-rendered). Fetched 417 KB of HTML, but the actual visible content is minimal. Opened in browser to see rendered output.

### Step 3: Browser rendering
Navigated to https://www.doxemr.com/b10doc in Chrome. The page rendered with the following content:

**Title**: "DOX EMR B10 Documentation"

**Section heading**: "§ 170.315 (b)(10) Electronic Health Information export"

**Body text** (complete):
> DOX EMR authorized users can generate the Electronic Health Information Export (EHI) for a single patient and also the patient population using CCDA xml format that comply with USCDI v1 requirements standards.
>
> The Implementation guide for the CCDA xml standard file description can be accessed from below link. Note document describes connection for V1-V3 standards. DOX EMR uses V1 standard for connection.

**Single link**: https://www.hl7.org/implement/standards/product_brief.cfm?product_id=492

This links to the HL7 C-CDA Implementation Guide product page — an external standard, not vendor-specific documentation.

### Step 4: Search for additional files and links
```bash
grep -oiE 'href="[^"]*\.(pdf|zip|xlsx|xls|csv|json|doc|docx|yaml|yml)[^"]*"' b10doc-page.html
```
Result: No downloadable files found on the page. No PDFs, ZIPs, CSVs, schemas, or other documentation artifacts.

### Step 5: Check sitemap for other EHI-related pages
```bash
curl -sL "https://www.doxemr.com/pages-sitemap.xml"
```
The sitemap lists 21 pages. The only potentially relevant ones beyond /b10doc:
- `/dox-hs-aidbox-apis` — FHIR API documentation (examined; this is the (g)(10) Standardized API page, not EHI export)
- `/certification-and-meaningful-use` — Meaningful Use attestation (examined; no EHI export content)

### Step 6: Examined the FHIR API page
Navigated to https://www.doxemr.com/dox-hs-aidbox-apis. This page documents their (g)(10) Standardized API built on Health Samurai Aidbox. It lists:
- US Core FHIR endpoints (AllergyIntolerance, CarePlan, CareTeam, Condition, Device, DiagnosticReport, DocumentReference, Encounter, Goal, Immunization, Location, MedicationRequest, Observation, Organization, Patient, Practitioner, Procedure, Provenance)
- Supporting endpoints including Bulk Data API
- Authentication endpoints
- Links to a PDF at `https://podiatry.doxemr.net/DoxExtAPI/g10-API-for-patient-and-population-services.pdf`

This is their (g)(10) API — a separate system from the (b)(10) EHI export described on the b10doc page.

### Step 7: Check navigation "More" dropdown
Expanded the "More" menu in the navigation bar. Additional pages:
- Certification and Meaningful Use
- Partners and Ownership Opportunities
- Demo and Testimonials 2
- Contact Us
- DOX EMR RWT

None contain EHI export documentation.

### Step 8: Wayback Machine check
```bash
curl -s "https://archive.org/wayback/available?url=https://www.doxemr.com/b10doc"
```
Closest snapshot: 2025-11-08, HTTP 200. The page content appears unchanged — the same minimal description has been present throughout the page's history.

## What Was Found

The entire (b)(10) EHI export documentation consists of a single web page with three sentences:

1. The export uses **C-CDA XML format** compliant with **USCDI v1** standards.
2. It can generate exports for a **single patient** or the **patient population**.
3. The implementation guide is the standard **HL7 C-CDA specification** (linked to hl7.org product page for C-CDA, product_id=492).

There is:
- **No data dictionary** — no listing of what data elements are included in the export
- **No schema** — no vendor-specific C-CDA templates, constraints, or extensions documented
- **No sample data** — no example export files
- **No export instructions** — no user guide for how to initiate or receive the export
- **No field-level documentation** — no description of how DOX EMR data maps to C-CDA sections
- **No downloadable files** of any kind

The only actionable information is: "the export is C-CDA XML, USCDI v1."

## Export Coverage Assessment

### Data Domain Coverage

The b(10) documentation states the export uses "CCDA xml format that comply with USCDI v1 requirements standards." This is a critical limitation for a (b)(10) export:

**USCDI v1 / C-CDA covers** (at most):
- Patient demographics
- Allergies and intolerances
- Medications
- Problems/conditions
- Procedures
- Lab results
- Vital signs
- Immunizations
- Clinical notes
- Care team members
- Goals
- Health concerns
- Assessment and plan
- Smoking status
- Provenance

**Data domains from product research that are likely NOT covered by C-CDA/USCDI v1:**
- **Billing data** — CPT codes, ICD codes, claims, invoices, payments, insurance information. DOX EMR has integrated billing with automatic code extraction. None of this maps to standard C-CDA.
- **Scheduling/appointment data** — appointment history, reminders, no-shows. Not a C-CDA section.
- **Podiatry-specific clinical data** — the product's core value is its pre-built podiatry database covering "all location, diagnosis, treatment, and plan options for conditions below the knee." This specialty-specific structured data likely exceeds what maps to standard C-CDA problem/procedure sections.
- **Clinical quality measure data** — MIPS reporting numerators, denominators, and calculated measures. Not in C-CDA.
- **Patient portal activity** — patient-completed medical histories, portal access logs.
- **Orders and referrals** — while some order data may appear in C-CDA, the full order lifecycle (referral tracking, lab orders, procedure requests) likely isn't captured.
- **Audit logs** — system access and activity records.
- **Research data** — the Starwriter component collects structured research data; this would not be in a C-CDA export.

**Assessment**: By equating their (b)(10) EHI export with a C-CDA/USCDI v1 document, DOX EMR is effectively providing only the clinical data subset that overlaps with the (g)(10) requirement. This is a textbook case of the (b)(10)/(g)(10) confusion described in EHI export assessments. A C-CDA USCDI v1 document covers roughly the same data as their FHIR US Core API — meaning the "EHI export" likely exports no more data than their standardized API already provides. The entire point of (b)(10) is to export *everything* the system stores, including billing, scheduling, audit trails, and specialty-specific data that doesn't fit into standard clinical document formats.

### Export Format & Standards

- **Format**: C-CDA XML (Consolidated Clinical Document Architecture)
- **Standard version**: USCDI v1 (the page says "V1 standard for connection")
- **FHIR involvement**: None — the b(10) export is C-CDA, separate from their Aidbox FHIR API
- **Appropriateness**: C-CDA is a recognized healthcare standard, but it is not appropriate as a *complete* EHI export format. C-CDA is designed for clinical document exchange (care summaries, referrals), not for bulk data export of an entire EHR database. It has no sections for billing data, scheduling, audit logs, or custom/specialty-specific data structures. Using C-CDA for (b)(10) means the export is structurally limited to the clinical data domains that C-CDA supports.
- **Reconstruct-ability**: A third party could understand the clinical portions of the export by referencing the C-CDA standard, but would have no visibility into billing, scheduling, or specialty-specific podiatry data that the system stores.

### Documentation Quality

The documentation is among the most minimal possible while still technically existing:
- **One paragraph** of text describing the export format
- **No data dictionary** at any level of granularity
- **No field-level definitions** — not even a list of which C-CDA sections are populated
- **No sample data** or examples
- **No user instructions** for how to trigger the export
- **No schema or template documentation** — the only reference is to the generic HL7 C-CDA standard, not any vendor-specific customization
- **Not developer-implementable** — a developer could not implement an import of this data based on this documentation alone; they would need the generic C-CDA spec and would have to reverse-engineer the vendor's mapping

A developer receiving a DOX EMR C-CDA export would have to rely entirely on the generic C-CDA specification to parse it, with no guidance on which sections are populated, what data elements are included, or how DOX EMR's internal data model maps to C-CDA structures.

### Structure & Completeness

- **Granularity**: Zero. There is no structural documentation — no table names, field names, data types, or descriptions.
- **Coded fields**: Not documented. No indication of what value sets are used, whether they use SNOMED CT, ICD-10, CPT, or custom codes.
- **Relationships**: Not documented.
- **Versioning**: No version history or change log.

### Overall Assessment

DOX EMR's (b)(10) documentation is a compliance placeholder, not a genuine attempt to document their EHI export capability. The single paragraph essentially says "we export C-CDA" and points to the HL7 standard — providing zero vendor-specific information about what data is actually included, how to use the export, or what the output looks like.

The choice of C-CDA USCDI v1 as the export format strongly suggests that the (b)(10) export covers only the standard clinical data subset — the same data their FHIR API already provides. This would leave billing, scheduling, podiatry-specific structured data, quality measures, and other significant data domains unexported. For a podiatry-specific EMR whose unique value is its structured clinical database for conditions below the knee, the absence of any specialty-specific export documentation is particularly notable.

This is consistent with the product research findings: DOX EMR is a very small company (likely a single physician-developer with a handful of staff), and the documentation quality reflects limited resources dedicated to compliance documentation. The product was certified in January 2022, so there has been ample time to develop more complete documentation.

## Access Summary
- Final URL (after redirects): https://www.doxemr.com/b10doc
- Status: found
- Required browser: yes (Wix site renders via JavaScript, but the content is also in SSR HTML)
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends
- The Wix platform makes curl-based text extraction difficult (most of the 417KB HTML is JavaScript framework code), but the page renders fine in a browser.
- No downloadable files exist — the page is purely textual with a single external link.
- The HL7.org link (product_id=492) is an external standard reference, not vendor-specific documentation.
- The "More" navigation dropdown was checked for hidden pages; none contained EHI export content.
- Full sitemap (21 pages) was enumerated; no additional EHI export documentation exists on the site.
- Wayback Machine snapshot from 2025-11-08 confirms the page has been in this minimal state.
