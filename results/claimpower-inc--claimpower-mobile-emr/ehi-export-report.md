# Claimpower, Inc. — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://www.claimpowerehr.com/curesUpdate/CCDA_Export.PDF
- CHPL IDs: 11209
- Product: Claimpower Mobile EMR v6.1
- Certification Date: 2023-01-09

## Navigation Journal

The registered URL is a direct PDF download. No navigation required.

```bash
curl -sI -L "https://www.claimpowerehr.com/curesUpdate/CCDA_Export.PDF" \
  -H 'User-Agent: Mozilla/5.0'
# HTTP/2 200, Content-Type: application/pdf, 1,063,362 bytes
```

The PDF (9 pages, authored by Rohan Thadani, created 2023-08-28) is titled "Claimpower EMR version 6.1 CCDA Export." Page 1 is an index linking to three sub-documents, each also hosted as separate PDFs:

1. `CCDA_Export_Signle_Patient.PDF` (note the typo "Signle") — 3 pages
2. `CCDA_Multiple_Patients.PDF` — 2 pages
3. `CCDA_Patient_Portal.PDF` — 3 pages

All three sub-PDFs were downloaded successfully:
```bash
curl -sL "https://www.claimpowerehr.com/curesUpdate/CCDA_Export_Signle_Patient.PDF" -o CCDA_Export_Single_Patient.PDF
curl -sL "https://www.claimpowerehr.com/curesUpdate/CCDA_Multiple_Patients.PDF" -o CCDA_Multiple_Patients.PDF
curl -sL "https://www.claimpowerehr.com/curesUpdate/CCDA_Patient_Portal.PDF" -o CCDA_Patient_Portal.PDF
```

The main PDF contains all three sub-documents inline (pages 2–9), so the sub-PDFs are redundant but were downloaded for completeness.

I also checked the parent directory (`/curesUpdate/`) which hosts an API documentation page for their FHIR/scheduling API (tabs for "Introduction", "Access Token", "Get Scheduled Patient List", "Post Scheduled Patient Notes", "Terms & Conditions"). This is their (g)(7)/(g)(10) API documentation, not EHI export documentation, so it was not downloaded.

The mandatory disclosures page (`https://claimpower.com/legal-notice/`) was also checked but contains no additional EHI export documentation or links.

## What Was Found

The documentation consists entirely of **step-by-step screenshot walkthroughs** showing how to export C-CDA documents from the Claimpower Mobile EMR. There are three export paths:

### 1. Single Patient Export (via EMR)
Login → Lookup Medical Records → search patient → click Clinical Document icon → Summary of Care Records → generate CCDA → download ZIP.

### 2. Multiple Patient Export (via EMR Reports)
Login → EMR Reports → Export Patient Medical Records → select patients (or "all patients" checkbox — the screenshot shows 12,217 patients) → Generate ZIP.

### 3. Patient Portal Export
Login via Patient Portal (requires 3-digit client ID, patient name, DOB, and 4-digit password) → View Health Information → Summary of Care Records → download ZIP.

The documentation contains screenshots of the actual UI at each step, showing the Claimpower interface. The screenshots reveal:
- The EMR dashboard with icons for Patient Census, MicroEMR, Billing, Results, Lookup Medical Records, Credits, ePrescribe, Administration, Payroll Registration, Schedules, Centers, Speed Billing, Time Reports, Attach Documents, Settings, and more.
- A "Summary Of Care" view showing patient demographics, document metadata, encounter info, provider info, and contact details in a blue-themed table.
- The multi-patient export interface under "EMR Reports" with a report menu that includes: Rx Billing/Claims Report, Patients Procedures Status, Billing Audit Report, Billing Stats Report, Server Activity, Checked In/Rollback Modes, Record Log, Audit Report, Public Health Surveillance Report, Clinical Quality Measures Report, Automated Physicians Credentials Report, Lab's FHIR Report, **Export Patient Health Records** (highlighted), Immunization Export Report, Daily Office Collection Report, CCM, MIPS Report, 90 Report/Chart Status Report.
- The patient portal with a "View Summary of Care" / "Secure Messaging" / "View Health Information" interface.

The export format is **C-CDA (Consolidated Clinical Document Architecture)**, delivered as a ZIP file. The C-CDA "Summary of Care" document visible in the screenshots includes standard C-CDA header fields: patient demographics, document ID, creation date, performer, author, encounter details, responsible party, personal relationships, contact info, and legal authenticator.

**What is NOT in the documentation:**
- No data dictionary
- No field-level definitions
- No schema or format specification beyond "C-CDA"
- No description of what data elements are included in the export
- No sample files
- No API documentation for the export mechanism
- No description of how data beyond standard C-CDA sections is handled

## Export Coverage Assessment

### Data Domain Coverage

The export documentation describes a **C-CDA Summary of Care** export. C-CDA is a well-defined standard, so the export will include standard clinical summary data: demographics, problems, medications, allergies, immunizations, vital signs, procedures, lab results, and clinical notes — essentially the USCDI/US Core clinical data set.

However, Claimpower is fundamentally a **billing services company with an integrated EMR**. Per the product research, the platform stores extensive data that would NOT be captured in a C-CDA Summary of Care:

**Likely missing from the C-CDA export:**
- **Billing and claims data** — electronic claims (primary/secondary), ERA/EOB records, CPT/ICD-10 codes, denial and appeal records, payment posting, collections activity. This is core to what Claimpower does and constitutes a major part of the designated record set.
- **Practice management data** — scheduling/appointments, insurance eligibility, patient balances, payment records, superbills/encounter forms.
- **Scanned/indexed documents** — paper chart digitization is a listed feature; these documents may not be included in a C-CDA export.
- **Communication records** — secure messages, Direct messages, text messages (patient reminders/recalls), eFax records.
- **Custom clinical data** — any specialty-specific documentation beyond what C-CDA sections support.
- **ePrescribing records** — detailed prescription history beyond what's in the C-CDA medications section.

The screenshots of the multi-patient export are notable: the report menu item is labeled "**Export Patient Health Records**" (not "Export Patient Medical Records" as the text says), and it sits alongside billing-specific reports. But there is no indication in the documentation that the export includes anything beyond the C-CDA clinical summary.

This is a clear case of the **(b)(10) vs (g)(10) confusion**. The vendor has certified for 170.315(b)(10) (EHI export) but the documentation describes only a C-CDA export, which is essentially the same clinical summary used for transitions of care under (b)(1)/(b)(2). C-CDA covers a well-defined subset of clinical data — it does not cover billing, claims, practice management, or other non-clinical data that is part of the designated record set.

For a company whose primary business is billing services, the absence of any billing data from the export is a particularly significant gap.

### Export Format & Standards
- **Format**: C-CDA (Consolidated Clinical Document Architecture), packaged as ZIP files
- **Standard**: HL7 C-CDA is a recognized, widely-implemented standard
- **Appropriateness**: C-CDA is appropriate for clinical summary data but is fundamentally insufficient for a complete EHI export. It cannot represent billing records, claims, scheduling, communication logs, or scanned documents. A product that stores extensive billing and practice management data needs a supplementary export format for non-clinical data.
- **Reconstruction potential**: A third party could reconstruct the clinical summary from the C-CDA, but could not reconstruct the full patient record (billing history, communications, scanned documents, etc.)

### Documentation Quality
- **Very minimal**. The documentation is purely a screenshot walkthrough of the UI workflow for generating exports. There are no technical details.
- **No data dictionary** — no field-level definitions, no description of what C-CDA sections or entries are populated.
- **No format specification** — beyond "C-CDA" there is no description of which C-CDA document type, which sections are included, what coded values are used, or what constraints apply.
- **No sample files** — no example C-CDA documents are provided.
- **No developer documentation** — a developer could not implement an import based solely on this documentation. They would need to obtain a sample export and reverse-engineer the structure.
- **The documentation reads as a compliance checkbox** — created to satisfy the (b)(10) certification requirement with minimal effort. All four PDFs were created on the same date (2023-08-28) by the CEO personally, suggesting they were produced specifically for certification.

### Structure & Completeness
- **Granularity**: Zero technical detail. No field names, data types, value sets, or cardinality information.
- **Relationships**: Not documented.
- **Versioning**: No change history. The PDFs were created 2023-08-28 and have not been updated (server last-modified date is 2025-05-15 but the PDF metadata is unchanged).
- **The most useful artifact** is arguably the screenshots, which at least confirm the export exists and show the basic UI flow.

## Access Summary
- Final URL (after redirects): https://www.claimpowerehr.com/curesUpdate/CCDA_Export.PDF (no redirects)
- Status: found
- Required browser: no
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends
None. The URL worked on the first try, and all linked sub-documents were accessible. The only issue is a typo in one filename ("Signle" instead of "Single").
