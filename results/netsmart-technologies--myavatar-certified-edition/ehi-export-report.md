# Netsmart Technologies — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://www.ntst.com/lp/certifications
- CHPL IDs: 11575
- Product: myAvatar Certified Edition, Version 5
- Certification date: 2024-12-27
- Certified for 170.315(b)(10): Yes

## Navigation Journal

1. **Probed the registered URL** with curl:
   ```bash
   curl -sI -L "https://www.ntst.com/lp/certifications" -H 'User-Agent: Mozilla/5.0'
   ```
   Returned HTTP 200, Content-Type: text/html. The page is a Netsmart certifications hub covering all their products.

2. **Searched the HTML source** for EHI-related links:
   ```bash
   grep -oiE 'href="[^"]*"' /tmp/ntst-certifications.html | grep -iE 'ehi|export|data.dictionary|b.10|bulk'
   ```
   Found a dedicated EHI section with product-specific links. The certifications page has a heading "EHI (Electronic Health Information) All Data Export" with links to per-product EHI pages.

3. **Navigated to the myAvatar-specific EHI page**:
   ```bash
   curl -sL "https://www.ntst.com/lp/certifications/ehi-all-data-myavatar" -H 'User-Agent: Mozilla/5.0'
   ```
   This is a dedicated page titled "EHI (Electronic Health Information) All Data Export for myAvatar" with explanatory text and a download link.

4. **Downloaded the EHI export documentation ZIP** linked from the page ("CLICK HERE"):
   ```bash
   curl -sL "https://www.ntst.com/-/media/pdfs/certifications/EHI_Export_All_Tables_myAvatar_September_2023.zip" \
     -H 'User-Agent: Mozilla/5.0' \
     -o downloads/EHI_Export_All_Tables_myAvatar_September_2023.zip
   ```
   File is 12.5 MB, verified as valid ZIP archive. Contains a single PDF: "EHI Export All Tables - September 2023.pdf" (16 MB, 7,492 pages).

5. **Extracted and examined the PDF**:
   ```bash
   unzip EHI_Export_All_Tables_myAvatar_September_2023.zip
   pdfinfo "EHI Export All Tables - September 2023.pdf"
   pdftotext "EHI Export All Tables - September 2023.pdf" ehi-export-all-tables.txt
   ```
   Author: Walz, Dru Anne. Created 2023-10-02 with Microsoft Word. 7,492 pages.

6. **Saved the EHI page HTML** and **took a screenshot** via browser for reference.

7. **Built an enrichment script** (`downloads/enrichment/extract-tables.ts`) to parse the pdftotext output into structured JSON. Run with `bun run extract-tables.ts`.

## What Was Found

### The EHI Export Mechanism

The EHI page describes the export as:

> "EHI Export functionality allows organizations to do a **manual one-time export** of health data for one or more patients. This schema is intended for EHI export functionality."

The export produces **computable, delimited files** in a format native to myAvatar. Each database table is exported to its own file with a filename matching the table name. The export covers "both the standard product forms and tables in myAvatar as well as the tables associated to our integrated applications like Flowsheet."

The page notes that "some electronic health information might not be available in a table format, such as rich text documents or images. This information is referenced in the extracts created for subsequent export." This means rich-text clinical notes and images are handled separately (presumably included by reference).

The export content varies by organization based on: (1) software applications in use, (2) software version, (3) documentation/software use practices, and (4) configuration decisions and customizations.

The page also distinguishes this EHI export from their FHIR API and other integration options, explicitly pointing users to the "Netsmart Developer Portal" for FHIR API documentation and "Information Sharing" for HL7/web service APIs. This is a good sign — they understand the EHI export is a different mechanism from their (g)(10) FHIR API.

### The Data Dictionary (PDF)

The ZIP contains a single massive PDF: **"EHI Export All Tables - September 2023.pdf"** (7,492 pages, last updated 2023-09-27).

Structure:
- **Table of Contents** (55 pages) listing all forms and tables
- **Overview** explaining the documentation approach
- **Glossary of Terms** defining common field patterns (PATID, FACILITY, EPISODE_NUMBER, ss_ fields, JOIN_TO/LINK_TO relationships, etc.)
- **Form-by-form and table-by-table documentation** comprising the bulk of the document

Each table entry includes:
- **Form name**: The myAvatar UI form associated with the table
- **Table name**: Fully qualified as schema.table_name (e.g., `SYSTEM.billing_tx_charge_detail`)
- **Table description**: Brief explanation of what the table stores
- **Column definitions**: For each column:
  - Column name
  - Column type (varchar, integer, numeric, date, time, timestamp)
  - Max length (for varchar columns)
  - Description (present for ~81% of columns)

### Parsed Statistics (from enrichment)

| Metric | Value |
|--------|-------|
| Total table entries (form-table pairs) | 906 |
| Unique tables | 561 |
| Unique forms | 217 |
| Total columns across all entries | 71,903 |
| Columns with descriptions | 58,321 (81.1%) |
| Columns with max length specified | 61,215 (85.1%) |

**Schema breakdown** (tables by database schema):

| Schema | Table Entries | Purpose |
|--------|---------------|---------|
| SYSTEM | 746 | Core myAvatar tables |
| STATEFORM | 60 | State-specific behavioral health reporting |
| CWSTEMP | 40 | Clinical Workstation temporary/session tables |
| OrderEntry | 27 | CPOE and order management |
| Methadone | 8 | Methadone/MAT-specific medication management |
| DocR | 7 | Document routing and rules |
| INCIDENT | 5 | Incident reporting |
| eMAR | 5 | Electronic medication administration records |
| LAPROV | 3 | Louisiana provider-specific tables |
| HL7 | 2 | HL7 integration/external ID mapping |
| GL | 1 | General ledger |
| CWSOrderEntry | 1 | Clinical Workstation order entry |
| CWSSF | 1 | Clinical Workstation state-specific (Florida) |

## Export Coverage Assessment

### Data Domain Coverage

This is one of the most comprehensive EHI export data dictionaries encountered. Netsmart has documented the full database schema across all of myAvatar's modules, not just the clinical summary data that would be covered by a FHIR API.

**Domains clearly covered:**

- **Billing/Financial** (159 unique tables): Claims processing (CMS-1500, UB-04, 837I/P), remittance (835), claim status (276/277), cash posting, charge input, self-pay billing, Medicare pharmacy billing, financial eligibility, payment history, ledger transactions, retroactive payor changes, benefit enrollment (834). This is exceptionally thorough billing coverage.

- **Demographics/Patient** (168 unique tables): Client enrollment, admission/discharge records (including outpatient and backdated), episode management, outreach targets, client merging/purging, pre-admission, program transfers, external client IDs, patient account numbers, and demographic updates.

- **Clinical Notes** (49 unique tables): Progress notes (ambulatory, inpatient, group, individual), co-sign/review workflows, voided notes, scratch notes, service documentation corrections, significant findings. The CWS patient notes tables have multiple supplement tables (supp_1 through supp_6) suggesting extensible note content.

- **Medications/Pharmacy** (31 unique tables): Medication orders (including quick orders), eMAR administration records, NCPDP claim submission/response, methadone-specific medication orders (client, recurring, and fixed orders), medication reconciliation, and medication regimen review.

- **Diagnoses** (44 unique tables): Client diagnosis records, enrollment diagnoses, audit trails for diagnosis changes, and problem list entries.

- **Treatment/Care Plans** (61 unique tables): Treatment plans (with goals, level of care, recovery plans, todos), care pathway enrollment, clinical reconciliation, assessment-problem planning, and discharge summaries.

- **Labs/Orders** (43 unique tables): Order entry, results entry, results reconciliation, specimen data, POC results, order consent, and clinical pathway-related orders.

- **Scheduling/Appointments** (37 unique tables): Appointment data, series, waiting room, check-in/check-out, telehealth appointments, overbooking, front desk operations.

- **Vitals/Observations** (6 unique tables): Vital signs (including site-specific configurations), observation details and archives.

- **Allergies** (5 unique tables): Client allergies, clinical info, allergy history, and CCD allergy staging.

- **Immunizations** (4 unique tables): Immunization history, custom definitions, and health maintenance alerts.

- **Behavioral Health-Specific** (15 unique tables): Acuity scoring (compile, domain scores, subdomain scores), incident data, leave management, seclusion/restraint tracking.

- **Service Authorization** (10 unique tables): Funding source authorizations, member authorizations, provider authorizations, MSO service authorizations — critical for behavioral health billing workflows.

- **State-Specific Forms** (61 unique tables): New York PAS reports (44N, 45N, 46, 47, 125), Florida FSR, Georgia ASO, California DCR, Michigan county billing, Indiana MRO, Kansas AIMS, Louisiana provisions, Ohio BH admission, WaMS response files, CIMOR imports. This reflects myAvatar's deep integration with state behavioral health reporting systems.

- **Consent/Disclosure** (9 unique tables): Consent for access, referral consent, disclosure management, internal client consents — important for 42 CFR Part 2 compliance.

- **Bed Management** (10 unique tables): Bed assignment, waiting room, patient movement history.

- **Referral/Transfer** (12 unique tables): CareFabric referrals, internal referrals, program transfers, episode history.

**Data domains with limited or no explicit coverage:**

- **E-prescribing transaction details**: While medication orders are covered, Surescripts transaction-level data (fill history, formulary checks) is not explicitly visible in the table names. This may be captured within the medication order tables or handled by the external Surescripts integration rather than stored natively in myAvatar.

- **Secure messaging content** (patient portal messages): The myHealthPointe portal has its own separate EHI export page, and portal-originated data may not appear in the myAvatar export. This is a reasonable separation given they are separately certified products.

- **Scanned documents and images**: The page explicitly notes these "might not be available in a table format" but are "referenced in the extracts." This means the export includes metadata/references to these documents but the actual binary content may require separate handling.

- **Ambient documentation (Bells AI)**: As a newer AI feature, transcripts or AI-generated note drafts may not be captured in the September 2023 documentation.

### Export Format & Standards

The export uses a **proprietary delimited file format** native to myAvatar — each table exported as its own file. This is **not FHIR, not C-CDA, not a recognized standard interchange format**. It is essentially a database dump in delimited format.

This is actually appropriate for a (b)(10) export from a behavioral health EHR. myAvatar stores far more data (state-specific forms, methadone management, acuity scoring, seclusion/restraint tracking, 42 CFR Part 2 consent management) than could be represented in FHIR US Core or C-CDA. A database-level export preserves all this data without lossy transformation.

The export includes:
- **Relationships between tables** via JOIN_TO and LINK_TO columns (documented in the glossary)
- **Patient identity** via PATID (medical record number/client ID)
- **Episode context** via EPISODE_NUMBER
- **Facility/site context** via FACILITY and SITEID
- **Audit metadata** (data_entry_date, data_entry_by, UTC timestamps, timezone info)
- **Coded values** with both codes and their descriptions (e.g., TYPE_OF_TRANSACTION_CODE + type_of_transaction_value)

A third party could reconstruct the patient record from this export, though they would need to understand the myAvatar data model. The glossary and table descriptions provide a reasonable starting point, but there is no formal schema file (no XSD, JSON Schema, or DDL).

### Documentation Quality

**Strengths:**
- Extraordinarily comprehensive scope — 561 unique tables, 71,903 columns
- The document covers the actual database schema, not a marketing summary
- 81.1% of columns have descriptions, which is good for a document this size
- The glossary explains common field patterns and relationship conventions
- Table descriptions explain the purpose of each table
- Organized by form, which maps to user-facing functionality

**Weaknesses:**
- **No sample data or worked examples**: There are no example export files, sample records, or illustrations of what the delimited output looks like
- **No file format specification**: The page says "computable, delimited file format" but doesn't specify the delimiter, encoding, escaping rules, null handling, or header format
- **No schema files**: No machine-readable schema (DDL, XSD, JSON Schema). The only structured representation is the PDF itself, which required custom extraction
- **~19% of columns lack descriptions**: While 81.1% coverage is good, nearly 13,600 columns have no description
- **Documentation is dated September 2023**: Over 2 years old at time of collection. The product version certified in December 2024 may have additional tables or modified schemas
- **Rich text and images not fully documented**: The export acknowledges these exist but doesn't specify how they're referenced or exported
- **No relationship diagram or ERD**: With 561 tables and JOIN_TO/LINK_TO relationships, a formal relationship diagram would greatly aid comprehension
- **Value set documentation is sparse**: Coded fields reference code/value pairs but the actual allowed values are not enumerated

### Structure & Completeness

**Granularity**: Field-level documentation with column names, data types, max lengths, and descriptions. This is granular enough to understand the structure but lacks cardinality, nullability, primary/foreign key designations, and index information.

**Coded fields**: The pattern of xxx_CODE + xxx_value pairs is documented in the glossary, and descriptions often say "See xxx_CODE for more information." However, the actual valid code values are not enumerated anywhere in the documentation.

**Relationships**: Documented via JOIN_TO_xxx and LINK_TO_xxx column naming conventions. The glossary explains these are used for joins to parent/child documents, but there is no comprehensive relationship map.

**Versioning**: The document is a point-in-time snapshot (September 2023). There is no change history or version comparison.

### Overall Assessment

Netsmart has done genuine (b)(10) work with myAvatar. This is not a repackaged FHIR API or clinical summary — it is a comprehensive database-level export covering clinical, billing, behavioral health-specific, state reporting, medication, scheduling, and administrative data. The 561 unique tables span 13 database schemas, reflecting the product's deep functionality in the behavioral health domain.

The documentation is substantive but dated (September 2023 for a December 2024 certification). The most significant gap is the lack of format specification — knowing the tables and columns is valuable, but without knowing the delimiter, encoding, and output structure, a developer cannot write an import without an actual sample file. The absence of sample data or worked examples compounds this gap.

The export explicitly distinguishes itself from the FHIR API, which demonstrates that Netsmart understands the (b)(10) vs (g)(10) distinction. The breadth of data domains covered — including methadone management, state-specific forms, seclusion/restraint tracking, 42 CFR Part 2 consent management, and complex billing workflows — reflects a genuine effort to export the full designated record set for a behavioral health EHR.

## Access Summary
- Final URL (after redirects): https://www.ntst.com/lp/certifications/ehi-all-data-myavatar
- Status: found
- Required browser: no (all content accessible via curl)
- Navigation complexity: one_click (from main certifications page to product-specific EHI page)
- Anti-bot issues: none (User-Agent header recommended but standard)

## Obstacles & Dead Ends

No significant obstacles. The documentation was straightforward to find and download:
- The main certifications page has a clear EHI section with per-product links
- The myAvatar EHI page has a direct download link ("CLICK HERE")
- The ZIP downloaded cleanly and contained the expected PDF
- No authentication, CAPTCHA, or anti-bot measures encountered
