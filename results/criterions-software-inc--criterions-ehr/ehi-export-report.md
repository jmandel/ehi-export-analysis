# Criterions Software Inc — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://criterions.com/cures-disclosures-2022/
- CHPL IDs: 10171
- Product: Criterions EHR v4.0
- Developer: Criterions Software Inc

## Navigation Journal

The registered URL returns HTTP 200 directly. It is a WordPress page (Divi theme) hosted behind Cloudflare on WP Engine.

```bash
curl -sI -L "https://criterions.com/cures-disclosures-2022/" -H 'User-Agent: Mozilla/5.0'
# HTTP/2 200, content-type: text/html; charset=UTF-8
```

The page is titled "Certifications & Documentation" and contains exactly three button-links:

1. **"2022 CURES Disclosure"** → `https://criterions.com/wp-content/uploads/2022/08/2022-CURES-DISCLOSURES.pdf`
2. **"Patient EHI Data Export"** → `https://criterions.com/wp-content/uploads/2024/05/Patient-EHI-Data-Export-Overview.pdf`
3. **"Mandatory Disclosure 2022"** → `https://criterions.com/wp-content/uploads/2022/12/MandatoryDisclosure2022.pdf`

All three are direct PDF downloads. No accordions, no JavaScript rendering needed — the buttons are plain `<a>` tags with `target="_blank"`.

```bash
curl -sL "https://criterions.com/wp-content/uploads/2024/05/Patient-EHI-Data-Export-Overview.pdf" -H 'User-Agent: Mozilla/5.0' -o Patient-EHI-Data-Export-Overview.pdf
curl -sL "https://criterions.com/wp-content/uploads/2022/08/2022-CURES-DISCLOSURES.pdf" -H 'User-Agent: Mozilla/5.0' -o 2022-CURES-DISCLOSURES.pdf
curl -sL "https://criterions.com/wp-content/uploads/2022/12/MandatoryDisclosure2022.pdf" -H 'User-Agent: Mozilla/5.0' -o MandatoryDisclosure2022.pdf
```

All three files verified as actual PDF documents.

## What Was Found

### Patient EHI Data Export Overview (1 page)

This is the primary EHI export documentation. It is a single-page PDF titled "Patient EHI Data Export Overview and Instructions." The document states:

> "Your Patient Electronic Health Information (EHI) files are all sent via 'Email/Print of your Chart' along with the option to Download the CCDA file through our Criterions Electronic Health Records System. Your emailed or printed chart will include your chart information that was stored by the practice."

The document then explains what a CCDA file is and lists 22 clinical data categories included in the CCDA export:

1. Allergies
2. Assessment
3. Consult Note
4. Diagnostic Imaging Study
5. Encounters
6. Functional Status
7. Goals
8. Health Concern
9. History and Physical
10. Immunizations
11. Laboratory Report Narrative
12. Medical Equipment
13. Medications
14. Mental Status
15. Plan of Care
16. Problem List
17. Procedures
18. Progress Note
19. Reason for Referral
20. Results
21. Social History
22. Vital Signs

The export mechanism is described as "Email/Print of your Chart" plus a CCDA download option. The document is patient-facing — it instructs patients on how to read CCDA files rather than providing technical details about the export format.

### 2022 CURES Disclosures (1 page)

This single-page document has two sections:

1. **Multi-Factor Authentication** — describes MFA implementation
2. **EHI** — states: "The Criterions EHR allows customers to export industry-standard patient information in XML format using CCDA architecture and our Email/Print Chart functionality. Exports can be performed without intervention from programming or Criterions Software, Inc and without charge for individual patients, groups of patients, or automated scheduled export."

### Mandatory Disclosure 2022 (9 pages)

A comprehensive mandatory disclosure table listing all certified capabilities, descriptions, and costs. The relevant entry is:

- **§170.315(b)(10) Electronic Health Information export**: appears as a row header on page 5, but the description column for this row is blank — the page layout collapses it into the surrounding (b)(6) Data export section, which says: "Allow a practice to create individual and group exports of PHI without programming intervention."
- **170.315(b)(6) Data export**: "This functionality enables a user to electronically create a set of export summaries for all patients in C-CDA format that represents the most current clinical information about each patient. It includes clinical data defined in the Common Clinical Data Set, the reason for referral, and the referring or transitioning provider's name and office contact information."

## Export Coverage Assessment

### Data Domain Coverage

The export documentation describes a **C-CDA-based clinical summary export** that covers 22 clinical data categories. Comparing this against what Criterions EHR actually stores (per the product research):

**Clearly covered (clinical data):**
- Allergies, medications, problem lists, immunizations, vital signs — core clinical data
- Encounters, procedures, results/labs — encounter-level data
- Social history, functional status, mental status — social/behavioral data
- Medical equipment (implantable devices)
- Goals, plan of care, assessments
- Progress notes, H&P, consult notes — clinical documentation

**Clearly missing:**
- **Billing/financial data** — insurance, claims, superbills, A/R, payment history, denial tracking, patient payment plans. The product has a full practice management/billing module. None of this appears in the export.
- **Scheduling data** — appointment calendars, appointment history, recurring appointments, reminders. No mention.
- **Patient portal data** — intake forms, secure messages, uploaded documents/IDs, online payment records. No mention.
- **Prescription management data** — e-prescribing transaction history, controlled substance tracking, refill requests, pharmacy information. While "Medications" is listed, the Surescripts/NewCrop integration data (fulfillment tracking, dispensing records, EPCS audit trails) is absent.
- **Administrative data** — user accounts, audit logs, role-based access records. While the system has audit logging (certified for (d)(2)), audit data is not in the export.
- **Document management** — folders, annotations, digital signatures. No mention.
- **Reporting data** — CQM calculations, MIPS data, practice analytics. No mention.
- **Public health submissions** — immunization registry submissions, cancer case reports. No mention.
- **Referral management records** — while "Reason for Referral" is in the CCDA, the referral management workflow data is likely not captured.

### Export Format & Standards

The export is **C-CDA (Consolidated Clinical Document Architecture)** — an XML-based standard. This is a well-recognized clinical document standard, but it is fundamentally a **clinical summary format**, not a comprehensive data export format.

C-CDA was designed for transitions of care and patient summaries. It has well-defined sections for clinical data but no native support for:
- Billing/claims data
- Scheduling data
- Administrative/audit data
- Practice management data
- Portal interaction data

This is a classic case of **using the (g)(10)/(b)(1) clinical summary as the (b)(10) export**. The C-CDA export covers the "Common Clinical Data Set" (now USCDI) but not "all electronic health information" as required by 170.315(b)(10). The product stores extensive billing, scheduling, administrative, and portal data that cannot be represented in C-CDA format.

The 2022 CURES Disclosures document even says the export uses "industry-standard patient information in XML format using CCDA architecture" — acknowledging it's a standards-based clinical summary, not a comprehensive data dump.

### Documentation Quality

The documentation is **minimal**:

- The EHI export overview is a single page, patient-facing, explaining what a CCDA is
- There is no data dictionary — no table/field definitions, no schema documentation
- There are no worked examples or sample export files
- There is no technical documentation describing the CCDA's specific mapping, extensions, or constraints
- There is no description of how the "Email/Print Chart" functionality works technically
- A developer could not implement an import based on this documentation alone — they would need to rely entirely on the C-CDA standard specification and hope Criterions follows it faithfully

The documentation reads as a compliance checkbox rather than a genuine effort to document the export mechanism. It appears designed for patients ("How to read your CCDA") rather than for technical interoperability.

### Structure & Completeness

- **Granularity**: The documentation lists 22 section names but provides no field-level detail, data types, value sets, or constraints
- **Relationships**: No documentation of entity relationships
- **Coded fields**: No documentation of code systems used beyond mentioning ICD-9/10, SNOMED, RxNorm in the mandatory disclosure
- **Versioning**: The EHI export PDF was uploaded May 2024; the CURES disclosures are from August 2022. The mandatory disclosure is from December 2022. No version history or changelog.
- **Sample data**: None provided

### Overall Assessment

Criterions has produced the minimum viable documentation for (b)(10) compliance: a statement that patients can export their chart as a CCDA, plus a list of what sections the CCDA contains. This approach has several fundamental problems:

1. **It's not actually a (b)(10) export** — it's a C-CDA clinical summary that covers roughly the same data as the (g)(10) FHIR API and (b)(1) transitions of care. The extensive billing, scheduling, administrative, and portal data stored by the product is entirely absent.

2. **The documentation provides no technical detail** — there's no data dictionary, no schema, no mapping documentation. The one-page patient-facing overview is the entirety of the technical documentation.

3. **The export mechanism is described vaguely** — "Email/Print of your Chart" plus CCDA download. There's no documentation of batch export capabilities, automation, or how the "automated scheduled export" mentioned in the CURES disclosure actually works.

This is consistent with a small vendor (7-12 employees) that has treated (b)(10) as a repackaging of their existing C-CDA/transitions of care capability rather than building a genuine comprehensive data export.

## Access Summary
- Final URL (after redirects): https://criterions.com/cures-disclosures-2022/
- Status: found
- Required browser: no
- Navigation complexity: direct_link (three buttons on a single page)
- Anti-bot issues: none (Cloudflare present but no blocking)

## Obstacles & Dead Ends

None. The page loaded cleanly, all three PDF links worked, and the files downloaded without issues. The simplicity of the page (three buttons, three PDFs) made collection straightforward. The challenge is not access — it's that there simply isn't much documentation to collect.
