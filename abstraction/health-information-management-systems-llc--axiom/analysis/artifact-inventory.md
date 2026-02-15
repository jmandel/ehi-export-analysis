# Artifact Inventory

## Downloaded Files

| File | Size | Description |
|---|---|---|
| Axiom-EHI-Export-Instructions.pdf | 187,728 bytes | 4-page PDF: sole EHI export documentation. Created 2026-01-30 by Khalid Maskari via Microsoft Word. |
| screenshot-ehi-export-page.png | 174,638 bytes | Full-page screenshot of https://axiomehr.com/ehiexport/ showing heading + "Download PDF" button only. |

## PDF Page-by-Page Analysis

### Page 1: Cover page
- HiMS logo, title "170.315 (b)(10) Electronic Health Information Export"
- Company: Health Information Management Systems
- Product: Axiom, Version 7

### Page 2: Single-patient export instructions
- 4 bullet steps: Login → Report page → Enter patient name + parameters → Click BUILD REPORT
- Screenshot of Report Parameters UI with:
  - Start Date / End Date fields
  - Patient ID field (example: 81662)
  - "Form Types" multi-select dropdown showing dynamic forms (alphabetical):
    - Dynamic Form: AccountLogin
    - Dynamic Form: Active Meds Test
    - Dynamic Form: ADAD Test Form
    - Dynamic Form: Adult ADHD Self-Report Scale (ASRS-v1…)
    - Dynamic Form: Adult Brief Pscyhosocial Assessment - Dra…
    - Dynamic Form: Adult Brief Pscyhosocial Assessment - Dra…
    - Dynamic Form: Advance Directive Form
    - Dynamic Form: Agency - Encounter Form Signature
    - Dynamic Form: AKDA
    - Dynamic Form: All Tools Form
    - Dynamic Form: allow fax 1
- 3 additional bullets: review results, select documents, choose "EHI Export" from action dropdown

### Page 3: Export execution screenshots
- "EHI Export(1 patient, 16 forms)" table showing:
  - Patient: KING, TERRY; Patient #: TK10140210; Patient ID: 81662
  - Form types listed with checkboxes:
    - Dynamic Form: 13-17 EPSDT (File Date: 11/23/2023)
    - Dynamic Form: NPP Weekly Progress Report (11/19/2023)
    - Dynamic Form: NPP Weekly Progress Report (11/19/2023)
    - Encounter - CPT Note (11/10/2023)
  - "Choose Action" dropdown with "EHI Export" option
- Success dialog: "The EHI Export for KING, TERRY is generating. We will notify you when the export file is ready"

### Page 4: Export delivery + bulk export
- "EHI Export History" table:
  - Rec: 461053; Patient: KING, TERRY; Form Type: Encounter - CM 3.0; Form Date: 11/26/2023
  - File Name: 1BA97693-8CC0-4C82-A96F-FF42748F15AA.zip; Status: Completed
- Note: file is "compressed and encrypted with a password" sent to employee + patient email
- "Patient Population Data Bulk Export" section (2 sentences):
  - "The request for patient population export will include all population data."
  - "The export file(s) will be compressed to reduce file size."

## Key Observations

1. **No data dictionary** — zero field definitions, table names, schema, or format specs
2. **No sample data** — no example of what's inside the exported ZIP
3. **No format specification** — unknown whether ZIP contains PDFs, CSVs, JSON, FHIR, or other
4. **Form-based export model** — export is scoped to "Form Types" (dynamic forms + encounters), not a database/table export
5. **Visible form types** are behavioral health assessments (ASAM, ADHD, EPSDT, psychosocial assessments) and encounters (CPT Note, CM 3.0)
6. **No evidence of billing, medication, lab, insurance, or demographic data** in the export
7. **Bulk export** is mentioned in 2 sentences with no detail on scope or mechanism
8. **Typos present**: "informaiton" (p2), "cllick" (p2), "compresses" (p4)

## Form Types Visible in Screenshots (complete list)

From the "Form Types" dropdown (page 2):
1. Dynamic Form: AccountLogin
2. Dynamic Form: Active Meds Test
3. Dynamic Form: ADAD Test Form
4. Dynamic Form: Adult ADHD Self-Report Scale (ASRS-v1…)
5. Dynamic Form: Adult Brief Pscyhosocial Assessment - Dra… (appears twice)
6. Dynamic Form: Advance Directive Form
7. Dynamic Form: Agency - Encounter Form Signature
8. Dynamic Form: AKDA
9. Dynamic Form: All Tools Form
10. Dynamic Form: allow fax 1

From the export results list (page 3):
11. Dynamic Form: 13-17 EPSDT
12. Dynamic Form: NPP Weekly Progress Report

From the export history (page 4):
13. Encounter - CPT Note
14. Encounter - CM 3.0

**Note:** The dropdown shows only the first ~12 items of what appears to be a longer list. The prior report incorrectly transcribed "13-17 EPSDT" as "13-17 EPIIDT."
