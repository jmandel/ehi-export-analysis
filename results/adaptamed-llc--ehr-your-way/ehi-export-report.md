# Adaptamed, LLC — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://ehryourway.com/electronic-health-information-export/
- CHPL IDs: 10757
- Product: EHR Your Way v9.2.0.0
- Developer: Adaptamed, LLC
- Certification date: 2021-12-20

## Navigation Journal

1. Probed the registered URL with `curl -sI -L`:
   - HTTP/2 200, Content-Type: text/html; charset=UTF-8
   - Server: Apache, PHP 8.3.30
   - No redirects; URL resolves directly.

2. Downloaded the full page:
   ```bash
   curl -sL 'https://ehryourway.com/electronic-health-information-export/' \
     -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36' \
     -o ehi-export-page.html
   ```
   Result: 214,711 bytes HTML. WordPress-powered site with WP Rocket optimization.

3. Searched for downloadable files (PDF, ZIP, CSV, JSON, etc.) — **none found**. The page contains only inline HTML content and a data table; no downloadable artifacts are linked.

4. Searched for links containing EHI/export/data dictionary keywords — found only self-references back to this page and links to the FHIR API page and clinical documentation page.

5. Checked the certification page (`/certification/`) — it contains a brief mention: "170.315(b)(10) Electronic Health Information Export: Our documentation for single patient and bulk patient EHI export capabilities can be found here" with a link back to the EHI export page. No additional documentation there.

6. Checked the FHIR API page (`/standardized-api-for-patient-population-services-fhir-r4-smart-on-fhir-bulk-fhir/`) — this is the (g)(10) standardized API documentation, separate from the (b)(10) EHI export. Contains no EHI-specific content.

7. Opened the page in a browser, took screenshots (top, middle, full-page) to verify the rendered content matches the HTML extraction.

8. Extracted the C-CDA data dictionary table (69 rows, 28 sections) into structured JSON using a Bun TypeScript enrichment script.

## What Was Found

The EHI export documentation lives on a single HTML page at the registered URL. There are no downloadable files (no PDFs, ZIPs, schemas, or sample data). All documentation is inline on the page.

### Export Format

The export produces **C-CDA (Consolidated Clinical Document Architecture) XML** documents based on the HL7 Implementation Guide for CDA Release 2: Consolidated CDA Templates for Clinical Notes, DSTU Release 2.1 (August 2015). Additionally, human-readable PDF versions are included. All files are packaged in a **ZIP archive**.

### Export Modes

Two workflows are described:

1. **Single Patient Export**: Navigate to patient's chart → CCDA folder → Data Export. Users can select a date range and choose which clinical sections to include. An Attachments tab allows selecting scanned clinical and administrative documents for inclusion as PDFs.

2. **Bulk Export**: Navigate to Dashboard → CCDA Export folder → Data Export dropdown. Filter by date range and provider, select patients from the list, queue them for export. Produces individual ZIP files per patient.

### Access Controls

Export is limited to users with export privileges granted by a practice administrator.

### Data Dictionary

The page includes a table mapping 69 data elements across 28 C-CDA sections. The sections documented are:

| Section | # Elements |
|---------|-----------|
| Demographics | 13 |
| Reason for Visit | 1 |
| Encounter | 2 |
| Medication Allergies | 6 |
| Medication Information | 2 |
| Problem or Conditions | 2 |
| Results | 1 |
| Social History | 3 |
| Vitals | 2 |
| Immunizations | 4 |
| Procedures | 2 |
| Assessment | 1 |
| Reason for Referral | 1 |
| Plan of Treatment | 2 |
| Functional Status | 2 |
| Mental Status | 2 |
| Medical Equipment | 2 |
| Goals | 2 |
| Health Concerns | 2 |
| Care Team | 1 |
| History and Physical Exam Note | 2 |
| Progress Notes | 2 |
| Procedure Notes | 2 |
| Laboratory Notes | 2 |
| Consultation Notes | 2 |
| Discharge Summary | 2 |
| Imaging Narrative | 2 |
| Pathology Report | 2 |

Each row specifies Section Name, Data Element, Entry/XPath, and Code System (OID). The table documents the C-CDA template IDs and code system OIDs used for each section.

## Export Coverage Assessment

### Data Domain Coverage

EHR Your Way is a behavioral health-focused EHR serving psychiatrists, therapists, counselors, and substance abuse clinicians. The product research identified these major data domains:

**Clearly covered in the export (via C-CDA sections):**
- Demographics (name, DOB, race, ethnicity, sex, language)
- Encounters and encounter diagnoses
- Medication allergies (substance, reaction, severity, status)
- Medications (prescriptions)
- Problems/conditions (with ICD-10 and SNOMED codes)
- Lab results (Results section)
- Social history (smoking status)
- Vital signs
- Immunizations
- Procedures
- Assessment and plan of treatment
- Functional and mental status
- Goals and health concerns
- Care team information
- Clinical notes — 8 note types: H&P, progress, procedure, lab, consultation, discharge summary, imaging narrative, pathology report
- Reason for visit and referral
- Medical equipment

**Not mentioned or clearly absent from the export:**
- **Billing and financial data** — The product includes integrated billing (CMS 1500, UB-04, claims, ERA/835, payment posting, denial management). None of this appears in the export. C-CDA is a clinical document standard with no billing sections.
- **Behavioral health assessments** — The product's key differentiator is 50+ validated behavioral health assessments (PHQ-9, GAD-7, etc.) with automated scoring and trending. These are not represented in any C-CDA section. The Mental Status section may capture some observations, but discrete scored assessment data (individual question responses, total scores, trending) would not be faithfully represented in a standard C-CDA mental status observation.
- **Treatment plans with outcome tracking** — The product emphasizes treatment planning with outcome measurement. The Plan of Treatment section is documented but the depth of treatment plan data (goals, objectives, interventions, progress tracking) that the product stores likely exceeds what a standard C-CDA plan section can express.
- **Custom forms** — The product allows replication of paper forms as electronic versions for state compliance. These custom form data are not represented in C-CDA.
- **Substance abuse treatment data** — As a substance abuse treatment EHR, the product presumably stores substance use histories, treatment protocols, PDMP query results, and program-specific data (IOP schedules, group therapy rosters, etc.). None of this has a clear C-CDA mapping.
- **Scanned documents and attachments** — The single-patient export documentation mentions an Attachments tab for including scanned documents as PDFs. This is a partial solution — documents are included but only as flat PDFs, not as structured data.
- **Patient portal data** — Intake forms, patient messages, and portal activity are not mentioned.
- **Prescription Drug Monitoring Program (PDMP) data** — The product integrates PDMP checking; these records are not in the export.
- **Insurance/enrollment information** — Not in C-CDA.
- **CRM data** — Customer relationship management data mentioned in product features is absent.

### Export Format & Standards

The export uses **C-CDA Release 2.1**, a well-established clinical document standard. This is a legitimate, computable format for clinical data exchange. The documentation references specific template IDs and code system OIDs, demonstrating actual implementation knowledge.

However, **C-CDA is fundamentally a clinical summary format** — it was designed for transitions of care, not for comprehensive data export. It excels at representing the clinical data domains listed in the "covered" section above, but it has no provisions for:
- Billing records
- Discrete behavioral health assessment scores
- Custom form data
- Substance abuse program-specific data
- Practice management data

This is a textbook example of the **(b)(10) vs (g)(10) confusion**. The C-CDA export covers the same clinical summary data that would satisfy (g)(10) or transitions of care requirements, but it falls well short of "all electronic health information" as required by (b)(10). For a behavioral health EHR, the gap is especially significant because the product's core value proposition — behavioral health assessments, substance abuse tracking, treatment outcome measurement — lives outside what C-CDA can express.

A third party receiving this export would get a reasonable clinical summary (demographics, medications, problems, notes) but would miss the specialized behavioral health data that differentiates this product and that clinicians rely on for treatment decisions.

### Documentation Quality

The documentation is **readable and clear** in describing how to perform the export (step-by-step workflows for single and bulk export). The C-CDA data dictionary table provides section-level granularity with template IDs and code systems.

However, the documentation has significant gaps:
- **No sample export files** are provided — no example C-CDA XML, no sample ZIP
- **No field-level definitions** beyond section/element names — no data types, cardinality, or constraints
- **No value set documentation** — code system OIDs are listed but specific value sets are not enumerated
- **No relationship documentation** — how sections relate to each other
- **No documentation of the PDF format** — what the human-readable version contains
- **No description of what "clinical sections" are selectable** in the single-patient export (it says users can "choose which clinical sections to include" but doesn't enumerate them beyond the table)
- **No explanation of what happens with data that doesn't fit C-CDA** — the documentation doesn't acknowledge any limitations

The contact email (support@ehryourway.com) is provided for questions.

### Structure & Completeness

The data dictionary has **section-level and element-level granularity** (69 elements across 28 sections). Each entry includes:
- Section name
- Data element name
- Entry/XPath reference or C-CDA template ID
- Code system OID

What's missing:
- Data types for each element
- Cardinality (required vs. optional)
- Value set bindings (only OIDs, not the enumerated values)
- Field-level descriptions or business definitions
- No versioning or change history (though the page was last modified 2026-01-25)

## Overall Assessment

EHR Your Way has taken a **good-faith but insufficient approach** to (b)(10) EHI export. They have built a real export mechanism with a documented C-CDA format, two export workflows (single and bulk), and a data dictionary. The documentation is well-organized and clearly written.

The fundamental problem is that **C-CDA cannot express the full breadth of data this behavioral health EHR stores**. The export covers standard clinical data domains (demographics, medications, problems, notes, vitals, immunizations, etc.) but misses the product's core differentiating content: 50+ behavioral health assessments, substance abuse treatment protocols, outcome tracking data, billing records, custom forms, and PDMP data.

This is particularly significant because EHR Your Way is explicitly designed for behavioral health — a specialty where the most clinically important data (validated assessment scores, treatment progress, substance use histories) is exactly the data that falls outside C-CDA's standard sections.

The inclusion of scanned documents/attachments as PDFs in the export is a partial mitigation — if clinicians have scanned paper forms or external documents into the system, those flat files would be included. But structured data from electronic assessments, billing, and custom forms would not be.

## Access Summary
- Final URL (after redirects): https://ehryourway.com/electronic-health-information-export/
- Status: found
- Required browser: no (content is in static HTML, though site uses WP Rocket lazy loading)
- Navigation complexity: direct_link
- Anti-bot issues: none (standard User-Agent header sufficient)

## Obstacles & Dead Ends
- No downloadable files (PDF, ZIP, CSV, etc.) are linked from the page — all documentation is inline HTML only.
- The FHIR API page is a separate (g)(10) documentation page, not relevant to the (b)(10) EHI export.
- The certification page links back to the EHI export page with no additional content.
- No sample export files, schemas, or machine-readable artifacts are provided by the vendor.
