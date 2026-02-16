# eClinicalWorks, LLC — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://ehi.eclinicalworks.com/ehiexport/tableindex.html
- CHPL IDs: 11299 (v12.0.2, certified 2023-06-13), 11456 (v12.0.3, certified 2024-03-22)

## Navigation Journal

1. **Initial probe**: `curl -sI -L "https://ehi.eclinicalworks.com/ehiexport/tableindex.html" -H 'User-Agent: Mozilla/5.0'` — returned HTTP 200, Content-Type: text/html, 133,604 bytes. No redirects.

2. **Page examination**: The page is a static HTML page titled "EHI Export Schema" with:
   - A descriptive header explaining eClinicalWorks' (b)(10) certification
   - An alphabetical list of 1,466 database table names, each linking to a detail page at `tables/{tablename}.html`
   - A link to eClinicalWorks' Mandatory Disclosures at www.eclinicalworks.com/resources/certified-ehr-technology

3. **Table page structure**: Each table detail page (e.g., `tables/allergies.html`) contains:
   - Table name
   - Table description (human-readable explanation of what the table stores)
   - Column listing with: column name, data type, and description for each column

4. **No downloadable files found**: `grep -oiE 'href="[^"]*\.(pdf|zip|xlsx|csv|json)"' /tmp/ecw-tableindex.html` returned nothing. The entire documentation is presented as HTML pages — no PDFs, ZIPs, or structured export files are offered.

5. **Bulk download**: All 1,466 table pages were downloaded using parallel curl requests:
   ```bash
   grep -oiE 'href="tables/[^"]*"' tableindex.html | sed 's/href="//;s/"//' | \
     xargs -P 20 -I{} curl -sL --max-time 20 \
       "https://ehi.eclinicalworks.com/ehiexport/{}" -H "User-Agent: Mozilla/5.0" -o "{}"
   ```

6. **Two HTML formats identified**: The majority of files use CSS-class-based styling. Eleven files (all `ip_rh_*` prefixed, related to inpatient/hospital features) use an inline-style format with slightly malformed HTML. Both formats were parsed successfully.

7. **No additional documentation found**: No API docs, sample data, schema files (XSD, JSON Schema), or user guides for performing the export were linked from the documentation site.

## What Was Found

### Export Format
The documentation is a **database schema data dictionary** describing 1,466 tables and 19,819 columns that comprise the EHI export. The export appears to be a direct database export — tables with foreign key relationships between them. The format is not FHIR, C-CDA, or any health data standard; it is a proprietary relational database schema.

### Data Dictionary Quality
Each table has:
- A **table name** (database table name, e.g., `allergies`, `billingdata`, `enc`)
- A **table description** explaining what data the table stores (present for all 1,466 tables)
- **Column definitions** with name, SQL data type (int, varchar, datetime, etc.), and a human-readable description

Column descriptions frequently reference foreign keys to other tables (e.g., "This column refers to the UID column in the user table"), providing relationship documentation.

### Scope — This Is a Real (b)(10) Export
This is a genuine (b)(10) EHI export, not a repackaged FHIR API. Key evidence:
- **1,466 tables** covering the full breadth of eClinicalWorks' database schema
- Includes billing, claims, payments, insurance, and revenue cycle data (171+ tables)
- Includes specialty-specific clinical data: behavioral health (28 tables), vision/ophthalmology (52 tables), dental (20 tables), OB/GYN (15 tables), cardiology (3 tables)
- Includes operational/administrative data beyond what FHIR/USCDI covers
- No mention of FHIR, US Core, or USCDI anywhere in the documentation
- Export is a database-level dump, not a standardized API

## Export Coverage Assessment

### Data Domain Coverage

The schema covers an exceptionally broad range of data domains:

| Domain | Tables | Assessment |
|--------|--------|------------|
| Patient Demographics | ~155 | ✅ Comprehensive — user, patient contact, address, insurance info |
| Clinical Encounters | ~140 | ✅ Extensive — enc table with 100+ columns, encounter types, providers |
| Medications/Prescriptions | ~139 | ✅ Deep — prescriptions, ePrescribing, medication history, compound Rx |
| Clinical Notes/Documents | ~185 | ✅ Very thorough — progress notes, letters, templates, addenda |
| Billing/Claims/Payments | ~171 | ✅ Comprehensive — claims, charge posting, payments, refunds, ERA |
| Lab Results | ~70 | ✅ Well covered — lab orders, results, specimens, panels |
| Allergies | ~41 | ✅ Detailed — allergies, reactions, formulations, extract billing |
| Vision/Ophthalmology | ~52 | ✅ Specialty-specific — visual acuity, refraction, slit lamp, tonometry |
| Inpatient/Hospital | ~39 | ✅ Present — discharge, orders, staging, medication orders |
| Care Plans/Goals | ~29 | ✅ Covered — care plans, goals, assessments |
| Behavioral Health | ~28 | ✅ Specialty-specific — BH encounters, billing data, addendums |
| Scheduling/Appointments | ~27 | ✅ Covered — appointments, waitlists |
| Immunizations | ~24 | ✅ Covered — immunization records, registries |
| Insurance | ~23 | ✅ Covered — insurance, eligibility, X12 transactions |
| Referrals | ~21 | ✅ Covered — referral tracking |
| Dental | ~20 | ✅ Specialty-specific — dental charts, procedures |
| Vitals | ~20 | ✅ Covered — vital signs, vital logs |
| OB/GYN | ~15 | ✅ Specialty-specific — obstetric/gynecologic history |
| Messages/Communication | ~12 | ✅ Covered — messages, inbox, telephone logs |
| Cardiology | ~3 | ⚠️ Minimal — only a few cardiology-specific tables |
| Imaging/Radiology | ~1 | ⚠️ Limited — imaging appears underrepresented relative to product capabilities |

**Approximately 251 additional tables** (~17%) fall outside these categories, covering areas like: ACO programs, flowsheets, questionnaires, structured history elements, warfarin management, growth charts, telehealth, chronic care management, and more.

**Notable strengths**: The export includes billing and revenue cycle data (171 tables), specialty-specific clinical data for multiple specialties, and patient engagement data — all areas frequently missing from EHI exports that are merely repackaged FHIR APIs.

**Potential gaps**: Telehealth visit records, remote patient monitoring data, and PRISMA interoperability records are not obviously represented, though they may be captured within encounter or document tables. The documentation does not explicitly address how documents, images, and attachments (scanned faxes, PDFs) are exported.

### Export Format & Standards
- **Format**: Proprietary relational database dump — SQL table structures with no standardized encoding
- **Not FHIR**: No mention of FHIR resources, profiles, or standardized APIs
- **Relationships**: Documented via foreign key references in column descriptions (e.g., "refers to the UID column in the user table"), but no formal ERD or relationship schema is provided
- **Data types**: Standard SQL types (int, varchar, datetime, smallint, char, text, tinyint, decimal, etc.)
- **Appropriateness**: A database dump is actually well-suited for a comprehensive EHI export. Unlike FHIR (which would struggle to represent 1,466 tables of proprietary clinical and billing data), a database export preserves the full breadth and depth of stored data.

### Documentation Quality
- **Strengths**:
  - Every table has a description
  - Every column has a data type and description
  - Foreign key relationships are described in column descriptions
  - The documentation is well-organized and navigable (alphabetical index → table detail pages)
  - 1,466 tables with 19,819 columns is an extensive data dictionary

- **Weaknesses**:
  - No formal ERD or entity-relationship diagram
  - No value set documentation (coded fields like `allergytype` say "Example: Allergy, Side Effects..." but don't provide exhaustive code lists)
  - No sample data or example export files
  - No user guide for actually performing the export
  - No export file format specification (is the export CSV? SQL dump? JSON? The documentation describes the schema but not the export file format)
  - Some column descriptions are vague or duplicated (e.g., two columns in the allergies table have the identical description "This column stores the order in which allergies are displayed")
  - No versioning or change history

### Structure & Completeness
- **Granularity**: Field-level — table name, description, column name, data type, description for every column
- **Value sets**: Partially documented — some coded fields mention examples but don't provide complete code lists
- **Relationships**: Documented informally via text references (e.g., "refers to encounterid column in the enc table")
- **No schema files**: No DDL, XSD, JSON Schema, or other machine-readable schema beyond the HTML pages
- **No API documentation**: The export mechanism (how a user triggers the export, what format the output takes) is not documented on this site

## Access Summary
- Final URL (after redirects): https://ehi.eclinicalworks.com/ehiexport/tableindex.html
- Status: found
- Required browser: no (static HTML, no JavaScript required)
- Navigation complexity: direct_link (index page links directly to all table pages)
- Anti-bot issues: none

## Obstacles & Dead Ends
- No obstacles encountered. All pages loaded reliably with standard curl requests.
- Two different HTML formats exist among the 1,466 table pages, requiring dual-format parsing in the enrichment script, but both are static HTML.
- The Mandatory Disclosures link (www.eclinicalworks.com/resources/certified-ehr-technology) was not followed as it leads to general certification information, not EHI export documentation.
