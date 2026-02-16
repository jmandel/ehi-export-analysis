# American Medical Solutions, Inc. — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://amsemr.com/services/
- CHPL ID: 10834
- Product: Helios v2.0
- Certification date: 2022-02-17

## Navigation Journal

1. **Initial probe**: `curl -sI -L "https://amsemr.com/services/" -H 'User-Agent: Mozilla/5.0'` — returned HTTP 200, Content-Type: text/html, served by Flywheel/5.1.0 (WordPress hosting). No redirects.

2. **Page examination**: Fetched full page (72,899 bytes). The page is the AMS Services page, a WordPress site with the Enfold theme. It has several sections: "Practice Management System (PPMS)" describing Helios, then a "Certified EHR" section with compliance documentation links displayed in a two-column layout.

3. **Found EHI export link**: In the "Certified EHR" section, the right column lists:
   - Export Documentation → links to `§170.315b10-Electronic-Health-Information-Export-Documentation.pdf`
   - Direct API Documentation → links to interopengine.com (g(10) API, not EHI export)
   - FHIR API Endpoints → links to americanmedicalsolutions.com/heliosmb/modules/public/FHIRAPIEndpoints.aspx
   - Multi-Factor Authentication Use Case Description
   - Transparency & Cost Disclosure

4. **Downloaded the PDF**:
   ```bash
   curl -sL "https://amsemr.com/wp-content/uploads/2023/12/§170.315b10-Electronic-Health-Information-Export-Documentation.pdf" \
     -H 'User-Agent: Mozilla/5.0' \
     -o 170.315b10-EHI-Export-Documentation.pdf
   ```
   Verified: `file` reports "PDF document, version 1.4, 10 page(s)", 172,908 bytes. Text extraction via `pdftotext` works cleanly.

5. **Checked FHIR API Endpoints page**: Fetched `https://www.americanmedicalsolutions.com/heliosmb/modules/public/FHIRAPIEndpoints.aspx` — it's a separate g(10) FHIR R4 endpoint listing page (ASP.NET). The page shows "No records available" in the organization/endpoint table. This is unrelated to the b(10) EHI export and appears to be for the standardized API requirement. Not downloaded.

6. **Took screenshots** of the services page showing the Certified EHR section with the Export Documentation link.

## What Was Found

The sole EHI export documentation is a 10-page PDF titled **"§170.315(b)(10) Electronic Health Information Export Documentation"**, created December 13, 2023, authored by Arturo Sanchez and approved by Anthony Puglisi (CEO).

### Export Mechanism

The export is triggered from the **Encounter Summary toolbar** by users with appropriate permissions (system administrators must grant export access). The user selects which categories of EHI to export. Each selected category generates an independent CSV file named after the section. All CSV files are bundled into a ZIP file for download.

This is a **per-patient, user-initiated CSV export** — not a bulk/batch mechanism and not FHIR-based.

### Data Dictionary

The PDF documents 15 export sections, each with a table showing Column name, DataType, and Notes:

| Section | Fields | Notable Details |
|---------|--------|-----------------|
| 2.1 Patient Demographics | 17 fields | ChartNumber, name, DOB, race, ethnicity, birth sex, language, addresses, phone, email |
| 2.2 Allergies | 6 fields | Substance, reaction, severity, status, non-medication flag |
| 2.3 Vitals | 13 fields | BP, HR, RR, temp, height, weight, pulse ox, O2, BMI percentile, weight-for-length, head circumference |
| 2.4 Care Team | 3 fields | Just Id, FirstName, LastName |
| 2.5 Immunizations | 2 fields | Id and single "Immunizations" varchar |
| 2.6 Procedures | 2 fields | Id and single "Procedures" varchar |
| 2.7 Assessment and Plan of Treatment | 2 fields | Id and single varchar |
| 2.8 Laboratory | 3 fields | Id, Tests, Values/Results |
| 2.9 Provenance | 3 fields | Id, AuthorTimeStamp, AuthorOrganization |
| 2.10 Medications | 2 fields | Id and single "Medications" varchar |
| 2.11 Smoking Status | 2 fields | Id and single varchar |
| 2.12 Clinical Notes | 9 fields | ConsultationNote, DischargeSummary, H&P, ProcedureNote, ProgressNote, ImagingNarrative, LabReportNarrative, PathologyReportNarrative |
| 2.13 Goals | 2 fields | Id and "Patient Goals" varchar |
| 2.14 Health Concerns | 2 fields | Id and "Health Concerns" varchar |
| 2.15 Problems | 2 fields | Id and "Problems" varchar |

## Export Coverage Assessment

### Data Domain Coverage

The 15 export sections map closely to the **USCDI v1 / US Core data classes** — this is essentially the same data scope as a g(10) patient summary, not a comprehensive b(10) EHI export.

**Covered (clinical summary data):**
- Patient demographics
- Allergies
- Vital signs
- Care team members
- Immunizations
- Procedures
- Assessment and plan of treatment
- Laboratory results
- Provenance
- Medications
- Smoking status
- Clinical notes (8 note types)
- Goals
- Health concerns
- Problems

**Not covered — significant gaps based on product capabilities:**
- **Billing/claims data**: Helios includes integrated billing (fee schedules, co-pays, claims submission, patient statements, billing analytics). None of this appears in the export.
- **Scheduling/appointment data**: The product has a multi-physician scheduling system with online patient requests. Not exported.
- **Scanned documents and images**: AMS's core business includes document scanning/imaging. The EHR stores scanned documents. Not exported.
- **E-prescribing history**: The product has EPCS certification. Detailed prescription history (beyond the single "Medications" varchar) is not exported.
- **Lab orders** (as distinct from results): The product has a lab ordering portal. Order details are not exported.
- **Patient portal messages/communications**: The product has a patient portal. Communications are not exported.
- **Inventory data**: The product tracks inventory. Not exported.
- **Audit logs**: Required for d-criteria certification. Not exported.
- **Referrals and transitions of care documents**: CCDAs and care summaries from b(1)/b(2) certification. Not exported.
- **Clinical quality measure data**: Certified for c(1)-c(3). Not exported.
- **Immunization registry submissions**: Certified for f(1). Submission records not exported.
- **Electronic case reporting data**: Certified for f(5). Not exported.
- **Family health history**: Certified for a(12). Not in the export sections.
- **Implantable device records**: Certified for a(14). Not in the export sections.
- **Patient-specific education**: Certified for a(15). Not in the export sections.

This is a textbook example of the b(10)/g(10) confusion. The export sections are essentially a CSV rendering of what would be a C-CDA or FHIR US Core patient summary. The documentation makes no mention of billing, scheduling, documents, or any administrative data — which are core to what this practice management system stores.

### Export Format & Standards

- **Format**: CSV files bundled in a ZIP archive
- **Standard**: No recognized standard. Ad-hoc vendor format.
- **Structure**: Each section is an independent CSV file. No relationships between tables are documented (e.g., there's no way to link a lab result to the encounter it belongs to, or a medication to who prescribed it).
- **Data types**: Only three types used: `long` (for Id), `varchar` (for most text), `numeric`/`decimal`/`DateTime` (for vitals and dates).

The CSV format is reasonable for flat data, but the extreme denormalization (many sections have just Id + a single varchar field) suggests the export may be serializing complex structured data into single text strings. For example, "Medications" is a single varchar — does this contain the drug name, dose, route, frequency, start date, and prescriber all concatenated? Or just the drug name? The documentation doesn't say.

### Documentation Quality

**Poor.** The documentation is minimal:
- Column names and data types are listed, but descriptions are absent for most fields. Only the "Id" column and "ChartNumber" have Notes explaining what they contain.
- No value sets or coded value documentation (what values does "BirthSex" contain? What are the valid Severity levels for allergies?).
- No sample data or example CSV files.
- No explanation of how multi-valued fields are represented (e.g., can a patient have multiple phone numbers? How are they represented?).
- No indication of date/time formats beyond "yyyy/mm/dd" noted for DateofBirth.
- No documentation of how the ZIP file is structured or named.
- A developer attempting to import this data would have to guess at most field semantics and formats.

### Structure & Completeness

- **Granularity**: Minimal. Most sections have only 2 fields (Id + a single varchar). The demographics and vitals sections are the only ones with meaningful field-level granularity.
- **Coded fields**: Not documented with value sets.
- **Relationships**: Not documented. No foreign keys, no encounter references, no temporal linking.
- **Versioning**: Document is version 1.0, approved June 2022. No change history since initial creation.
- **Maintenance**: The PDF was uploaded to the site in December 2023, but the document content dates to June 2022. No updates in nearly 4 years.

### Overall Assessment

This is a **compliance-minimum EHI export documentation**. The vendor has created a basic per-patient CSV export covering the standard USCDI clinical data classes but has not addressed the b(10) requirement to export *all* electronic health information. The product is an integrated EHR and practice management system that stores billing, scheduling, document imaging, and administrative data — none of which is included in the export.

The data dictionary is shallow: most tables have just 2 columns (Id + one varchar), suggesting either the export itself is extremely simplistic (just dumping text labels) or the documentation fails to describe the actual field structure. Either way, a third party would have significant difficulty reconstructing meaningful patient records from this export.

The documentation itself is a single 10-page PDF with no sample data, no value set definitions, no relationship documentation, and no worked examples. It appears to have been written once for certification in 2022 and not updated since.

## Access Summary
- Final URL (after redirects): https://amsemr.com/services/
- Status: found
- Required browser: no (direct PDF download via curl works)
- Navigation complexity: one_click (PDF linked directly from the services page)
- Anti-bot issues: none

## Obstacles & Dead Ends
- None. The page loaded cleanly, the PDF link was directly accessible, and the file downloaded without issues.
- The FHIR API Endpoints page at americanmedicalsolutions.com shows "No records available" — this appears to be a placeholder for the g(10) API endpoint listing that hasn't been populated.
