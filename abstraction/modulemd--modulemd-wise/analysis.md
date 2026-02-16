# EHI Export Analysis: ModuleMD

**Product**: ModuleMD WISE™  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.04.04.2980.Modu.10.01.1.221219 (CHPL ID 11092)

## 1. Product Context

ModuleMD WISE is an integrated cloud-based EHR + Practice Management + Revenue Cycle Management platform designed for specialty ambulatory practices, with a flagship focus on **allergy & immunology**. It also serves pulmonology, ENT/otolaryngology, internal medicine, and infusion center practices. The company manages 10M+ medical records across 300+ practice locations.

**Key data domains the product stores** (per vendor materials):

- **Core clinical**: Demographics, problem lists, medications, allergies, vitals, immunizations, lab results (Quest/LabCorp integration), clinical notes with specialty templates, care plans
- **Allergy-specific (flagship)**: Skin test orders/results with wheal/flare measurements, allergen panels, extract/vial compounding (lot numbers, allergen compositions, Beyond Use Dates), immunotherapy treatment plans and dosage schedules, injection administration records with questionnaires, USP 797 compliance data, SkinSight AI image analysis
- **Pulmonary**: Spirometry results and trending, Asthma Control Test scores, sleep study questionnaires, PFT results, DICOM imaging references
- **Practice management**: Scheduling, eligibility verification, referrals, insurance coverage, custom forms, digital signatures
- **Revenue cycle / billing**: Claims management and submission, auto-charging from clinical data, patient payments, claim scrubbing, financial reports
- **Infusion center**: Infusion session records, biologic/medication administration, insurance pre-authorization
- **Patient portal (Hale Hub)**: Messages, appointment requests, refill requests, demographic updates, lab results access, payments
- **e-Prescribing**: Via DrFirst Rcopia4 integration
- **Inventory** (InDrA add-on): Stock levels, dispensing records, expiration tracking

This is a comprehensive ambulatory specialty platform — far more than a basic charting tool. An adequate (b)(10) export should cover clinical, billing, specialty allergy/immunotherapy, practice management, and patient communication data.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/B10-Data-Export-Process-Flow-Document_compressed.pdf` (448 KB, 9 pages) | Process flow document with 14 annotated screenshots showing how to use the Data Export feature. Created 2023-11-20 by Rajesh Dandu using Microsoft Word 2016. Documents the UI workflow for requesting, processing, and downloading exports. Contains **zero** field definitions, schema documentation, or content specification. | **Low** — documents the export *process* but says nothing about export *content* |

**No other artifacts exist.** There is no data dictionary, no schema, no sample data, no API documentation, no supplementary files. The entire (b)(10) documentation is this single 9-page process guide.

## 3. Export Mechanics

- **Format**: C-CDA XML (ClinicalSummary documents)
- **Mechanism**: UI-based (Administration → Practice Setup → Data Export → +New Export)
- **Patient selection**: Single patient (by name or account number), multiple patients, or "Select All Patients" — so both single-patient and bulk export are supported
- **Processing**: Asynchronous — a backend program runs daily to process export requests through 3 stages (New → InProgress → Completed)
- **Delivery**: Cloud-hosted download URL with expiry date; download link visible only to the requestor
- **Patient portal access**: Individual patients can also download their own C-CDA files via Patient Portal → Documents
- **Encryption**: Optional password-based encryption for exported files
- **File Type dropdown**: Visible in screenshots (page 4) but its options are never documented — it's unclear whether alternatives to C-CDA exist
- **Access constraints**: Requires administrative access (Practice Setup); no API-based export documented
- **Fees**: Not documented in the PDF

**Output structure**: ZIP archive organized by patient folder, each containing a C-CDA ClinicalSummary XML file. File naming pattern: `{PatientID}-{date}_ClinicalSummary` (e.g., `QAT-1-11142023_ClinicalSummary`).

**Notable observation from page 7**: The browser Downloads sidebar in one screenshot shows files beyond the export ZIPs, including `Patients Referred through message.xlsx` and `BilledStatements_4768_10-11 23_14.52.pdf`. These appear to be incidental browser downloads rather than part of the (b)(10) export, as the document text explicitly describes the export output as "C-CDA in XML files" organized by patient folder. However, this introduces a small ambiguity about whether additional file types might be included under certain "File Type" dropdown selections.

## 4. Export Content: What's In It

### No Data Dictionary Provided

ModuleMD provides **zero** field-level documentation for their EHI export. There is:
- No data dictionary
- No schema documentation
- No C-CDA template specifications or profile constraints
- No description of which C-CDA sections are included
- No sample export files
- No field names, types, descriptions, value sets, or relationships

The only evidence of export content comes from:
1. The file naming convention `*_ClinicalSummary` (pages 8–9), indicating C-CDA ClinicalSummary/CCD documents
2. The document's opening statement referencing "Consolidated-Clinical Document Architecture (C-CDA) document(s)" as an example format

### Vendor's Own Content Organization

The vendor provides no content organization. The document describes only the export *process*. There are no entities, tables, fields, or categories documented.

| Entity/Table | Fields | Described | Types | Category (vendor's) |
|---|---|---|---|---|
| *(none documented)* | 0 | 0 | N/A | N/A |

### Inferred Content (from C-CDA ClinicalSummary format)

Based solely on the C-CDA ClinicalSummary format, the export *likely* includes standard CCD sections (allergies, medications, problems, procedures, results, vital signs, immunizations, etc.), but **none of this is confirmed by the vendor's documentation**. A C-CDA ClinicalSummary is a standardized clinical summary — it covers a fixed set of clinical domains defined by the HL7 C-CDA specification, not the full breadth of data the EHR stores.

## 5. Coverage Assessment

### 5a. What the Vendor Covers (Bottom-Up)

The vendor covers exactly **nothing** in their documentation — they document a process for clicking buttons, not what data gets exported. The export appears to produce standard C-CDA ClinicalSummary documents, which by definition cover only the clinical summary domains defined in the CCD template.

Based on the C-CDA ClinicalSummary format, the export would typically include: allergies, medications, problems, procedures, results, vital signs, immunizations, social history, plan of treatment, encounters, goals, health concerns, functional/mental status, and family history. These are standard USCDI-scope clinical data elements.

**Critically absent** from any C-CDA ClinicalSummary — and therefore almost certainly missing from this export:
- All allergy/immunology specialty data (skin tests, immunotherapy, vial compounding, USP 797 compliance)
- All billing and revenue cycle data
- All practice management data
- All infusion center records
- Detailed prescription data beyond medication lists
- Patient portal messages and communications
- Custom forms and questionnaires
- Inventory/dispensing records
- AI-generated content (dictation, coding suggestions, skin test analysis)

### 5b. Standardized Domain Coverage (Top-Down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA patient header (inferred) | C-CDA includes basic demographics; likely misses full administrative details |
| Encounters / visits | ⚠️ Partial | C-CDA Encounters section (inferred) | C-CDA encounter summaries are thin; product stores rich visit documentation |
| Problems / conditions | ⚠️ Partial | C-CDA Problem List section (inferred) | Standard problem list; likely lacks severity history, verification workflows |
| Medications / prescriptions | ⚠️ Partial | C-CDA Medications section (inferred) | Medication list only; full e-prescribing history via DrFirst likely absent |
| Allergies | ⚠️ Partial | C-CDA Allergies section (inferred) | Basic allergy list; almost certainly lacks detailed skin test results, wheal/flare measurements, immunotherapy records — the product's core specialty data |
| Immunizations | ⚠️ Partial | C-CDA Immunizations section (inferred) | Standard immunization records |
| Vitals | ⚠️ Partial | C-CDA Vital Signs section (inferred) | Basic vitals; pulmonary trending (spirometry, ACT scores) likely absent |
| Lab results | ⚠️ Partial | C-CDA Results section (inferred) | Standard lab results; detailed Quest/LabCorp integration data may be truncated |
| Imaging / diagnostic reports | ⚠️ Partial | C-CDA may include some diagnostic results | DICOM/PACS references, PFT reports likely absent |
| Procedures | ⚠️ Partial | C-CDA Procedures section (inferred) | Basic procedure list; detailed ENT/allergy procedure documentation likely missing |
| Clinical notes / documents | ⚠️ Partial | C-CDA may embed some notes | Full specialty-specific templates, JOSH AI dictation transcripts likely absent |
| Care plans / goals | ⚠️ Partial | C-CDA Plan of Treatment, Goals sections (inferred) | Basic care plan data |
| Orders / referrals | ⚠️ Partial | C-CDA may include Reason for Referral section | Detailed referral workflows, order sets likely absent |
| Insurance / coverage | ❌ Not covered | No evidence in C-CDA format | Product manages insurance/eligibility; **significant gap** |
| Claims / billing | ❌ Not covered | No evidence in C-CDA format | Product has full RCM with claims, charges, payments; **significant gap** |
| Payments | ❌ Not covered | No evidence in C-CDA format | Product processes patient payments; **significant gap** |
| Consents / directives | ❌ Not covered | No evidence | Product has digital signatures and custom forms |
| Patient communications | ❌ Not covered | No evidence in C-CDA format | Product has portal messaging, secure messaging; **gap** |
| Specialty: Allergy/Immunotherapy | ❌ Not covered | No evidence in C-CDA format | Product's **core differentiator** — skin tests, immunotherapy management, vial compounding, USP 797 compliance; **most significant gap** |
| Specialty: Pulmonology | ❌ Not covered | No evidence in C-CDA format | Spirometry, ACT scores, sleep studies; **significant gap** |
| Specialty: Infusion Center | ❌ Not covered | No evidence in C-CDA format | Infusion session records, biologic administration; **gap** |

**Summary**: Of 21 applicable domains, 0 are confirmed covered, ~12 are partially covered (inferred from C-CDA format), and 9 are not covered. The most damaging gaps are in the product's core specialty domains (allergy testing, immunotherapy) and billing/RCM — precisely the data that distinguishes this product and that C-CDA cannot represent.

## 6. Documentation Quality

The documentation is among the weakest possible for a (b)(10) EHI export:

- **Can a developer understand and use the export?** No. A developer would receive C-CDA XML files and would need to reverse-engineer the content entirely from the files themselves. There is no description of which C-CDA sections are populated, what data elements are included, whether vendor extensions are used, or how specialty data (if any) is represented.
- **What's well-documented?** Only the UI workflow for requesting and downloading exports — where to click, what the status stages look like, who can see the download link.
- **What requires guesswork?** Everything about the export's *content*: what data is included, what format details apply, what C-CDA templates are used, what the "File Type" dropdown options are.
- **Machine-readable artifacts?** None — no schemas, no sample data, no template specifications.
- **Could an import be built from this documentation?** No. The documentation provides zero information about data structure or content.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation is too thin to confirm what the export actually contains, but all evidence points to a standard C-CDA ClinicalSummary — which covers at most USCDI-scope clinical data. For a specialty allergy/immunology EHR with integrated billing, practice management, and rich specialty workflows, a C-CDA ClinicalSummary represents a small fraction of the designated record set. The product's most valuable and distinctive data — skin test results with wheal/flare measurements, immunotherapy treatment protocols, vial compounding records, infusion session data — has no C-CDA representation and is almost certainly absent from the export. Billing, claims, and payments are definitively absent from any C-CDA export.

**Axis 2 — Export approach: Repackaged existing export**

This is a textbook case of repackaging. The export produces C-CDA ClinicalSummary XML files — the same document type generated for transitions of care under criterion (b)(1). The file naming convention (`*_ClinicalSummary`) matches transition-of-care documents. The document references C-CDA as the export format in its opening sentence. There is no evidence of any purpose-built (b)(10) capability: no product-specific data dictionary, no coverage of billing or specialty data, no mapping beyond the standard C-CDA template. The vendor appears to have pointed their existing C-CDA generation at a "Data Export" screen and called it (b)(10).

### Key Findings

1. **The entire EHI export documentation is a 9-page process guide with zero content specification.** No data dictionary, no schema, no field definitions, no sample data — the document only shows how to click through the export UI. This is the bare minimum possible documentation.

2. **The export produces C-CDA ClinicalSummary XML files — the same format used for transitions of care.** File naming (`*_ClinicalSummary`) and the document's own description confirm this. This is a standard clinical summary, not a comprehensive EHI export.

3. **The product's core specialty data is almost certainly not exported.** ModuleMD WISE's primary value is its deep allergy/immunology workflow (skin tests, immunotherapy, vial compounding, USP 797 compliance) — none of which has a C-CDA representation. This is the single largest gap: the product's most distinctive data is precisely what the export format cannot carry.

4. **Billing and revenue cycle data are definitively absent.** The product includes full RCM (claims, charges, payments, auto-charging), but C-CDA is a clinical document format that does not carry financial data.

5. **An undocumented "File Type" dropdown exists** (visible on page 4), raising a faint possibility that alternative export formats exist. However, the document never describes these options, and all screenshots show C-CDA XML output.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Repackaged existing export
Export format:   C-CDA XML (ClinicalSummary)
Entities:        N/A (no data dictionary)
Fields:          N/A (no data dictionary)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (Select All Patients option)
Domains covered: ~12 of 21 applicable domains partially (inferred from C-CDA format); 0 confirmed
```

### Bottom Line

A patient or provider would receive a standard C-CDA clinical summary — essentially the same document available through transitions of care — and nothing more. For a specialty allergy/immunology EHR with integrated billing and rich specialty workflows, this means the most clinically distinctive data (skin test results, immunotherapy protocols, vial compounding records) and all financial data would be missing. The biggest gap is not just incomplete coverage, but the complete absence of documentation: no one — including a developer, a patient, or a regulator — can determine what this export actually contains without examining the output files directly.
