# EHI Export Analysis: Claimpower, Inc.

**Product**: Claimpower Mobile EMR v6.1
**Analysis date**: 2026-02-15
**CHPL ID**: 15.04.04.1238.Clai.06.02.1.230109 (CHPL #11209)

## 1. Product Context

Claimpower Mobile EMR is a cloud-based EHR/EMR from Claimpower, Inc., a small family-run medical billing services company in New Jersey. The EMR is **not sold standalone** — it is bundled free with Claimpower's managed medical billing services for small ambulatory physician practices. This makes Claimpower fundamentally a **billing company that includes an EHR**, not a software vendor that happens to do billing.

The platform stores and manages:
- **Clinical data**: patient demographics, problem lists, medication lists, allergy lists, clinical notes (with Dragon dictation), lab orders/results, prescriptions, immunizations, implantable device lists, family health history, vital signs, procedures
- **Billing/claims data**: electronic claims (primary/secondary), ERA/EOB records, CPT/ICD-10 codes, denial and appeal records, payment posting, collections activity — this is the company's core business
- **Practice management data**: scheduling, insurance eligibility, patient balances, superbills, payment records
- **Communication data**: secure messages, Direct messages, text message reminders, eFax records
- **Scanned documents**: paper chart digitization and indexing

The EMR dashboard screenshots (visible in `CCDA_Export.PDF` pages 2 and 5) confirm icons for Patient Queue, Messages, Notes, ePrescribing, Results, Lookup Medical Records, Charts, Billing, Immunizations, Patient Registration, Scheduling, Census, Speed Billing, EMR Reports, Attach Documents, Settings, RPM, CCM List, and TCM List.

The reports menu (page 5) confirms billing-specific features with items like "Billing Audit Report," "Billing Stats Report," "Daily Office Collection Report," and "Insurance's Eligibility Status." This is a product with significant billing and practice management capabilities beyond clinical documentation.

## 2. Artifacts Reviewed

All artifacts are from `downloads/` in the results directory. Four PDF files were collected, all authored by CEO Rohan Thadani on August 28, 2023:

| Artifact | Size | Pages | Words | What it is |
|---|---|---|---|---|
| `CCDA_Export.PDF` | 1.0 MB | 9 | 252 | **Main document**: index page linking to 3 sub-documents + all 3 inline. Most informative — contains screenshots showing the EMR dashboard, reports menu, clinical document view, C-CDA header, and patient portal. |
| `CCDA_Export_Single_Patient.PDF` | 500 KB | 3 | 102 | Single-patient C-CDA export walkthrough. Redundant with pages 2–4 of the main PDF. |
| `CCDA_Multiple_Patients.PDF` | 265 KB | 2 | 64 | Multi-patient C-CDA export walkthrough. Shows "Export Patient Health Records" with 12,217 patients. Redundant with pages 5–6 of main PDF. |
| `CCDA_Patient_Portal.PDF` | 387 KB | 3 | 84 | Patient portal C-CDA download walkthrough. Redundant with pages 7–9 of main PDF. |

**Totals**: 4 files, 17 pages (9 unique), 502 total words of extracted text. The low word count reflects that these PDFs are almost entirely screenshots with brief step labels. All three sub-documents are duplicates of content already in the main PDF.

**Most informative**: `CCDA_Export.PDF` — the screenshots reveal the EMR's module structure, the reports menu (confirming billing features), the clinical document sections, and the C-CDA header fields. The patient portal screenshot (page 8) shows the 12 health information sections available in the export.

**Least informative**: The three sub-PDFs, which are redundant subsets of the main document.

**What's absent**: No data dictionary, no schema, no sample data, no API documentation for the export, no field definitions, no format specification beyond "C-CDA."

## 3. Export Mechanics

- **Format**: C-CDA (Consolidated Clinical Document Architecture), delivered as ZIP files
- **Mechanism**: UI-based export through the web application, with three paths:
  1. **Single patient** (provider-initiated): Lookup Medical Records → select patient → Clinical Document → Summary of Care Records → Generate CCDA → Download ZIP
  2. **Multi-patient/bulk** (provider-initiated): EMR Reports → Export Patient Health Records → select patients or check "All Patients" → Generate ZIP. The screenshot shows a system with 12,217 patients, confirming bulk capability.
  3. **Patient portal** (patient-initiated): Patient logs into portal (requires 3-digit client ID, first name, last name, DOB, and 4-digit password) → View Health Information → Summary of Care Records → Download ZIP
- **Single-patient vs bulk**: Both supported. Bulk export via the "Export Patient Health Records" report.
- **Access constraints**: No fees mentioned for export. The EMR itself requires an active billing services contract with Claimpower. The patient portal path requires login credentials provided by the practice.

## 4. Export Content: What's In It

### What the export produces

The export generates **C-CDA Summary of Care Records**. There is no data dictionary, no field-level documentation, and no sample files. The only evidence of export content comes from:

1. **C-CDA header fields** visible in screenshots (pages 4 and 9): Patient name, date of birth, race, preferred language, contact info, patient IDs, document ID, document created date, performer, author, encounter ID, encounter dates, encounter location, responsible party, personal relationship, covered by, contact info (repeated for multiple roles), information recipient, legal authenticator.

2. **Patient portal "View Health Information" sections** visible in screenshot (page 8), which correspond to C-CDA sections:

| Section | Source |
|---|---|
| Patient Demographics | Portal screenshot (page 8) |
| Provider Details | Portal screenshot (page 8) |
| Patient Medical Documents | Portal screenshot (page 8) |
| Allergies | Portal screenshot (page 8) |
| Medications | Portal screenshot (page 8) |
| Problems | Portal screenshot (page 8) |
| Procedures | Portal screenshot (page 8) |
| Vital Signs | Portal screenshot (page 8) |
| Encounters | Portal screenshot (page 8) |
| Social History | Portal screenshot (page 8) |
| Family History | Portal screenshot (page 8) |
| Results (Discrete) | Portal screenshot (page 8) |

These 12 sections are standard C-CDA Summary of Care content, covering the USCDI clinical data set but nothing beyond it.

3. **Problem list data** partially visible in clinical document screenshot (page 3): Shows conditions like "Elevated C-reactive protein CRP," "Acute pericarditis" with SNOMED codes, dates, and status — confirming coded problem list entries.

### What is NOT in the export

There is no evidence — in any artifact — of the following data being included in the export:
- Billing records, claims, charge data, CPT/ICD codes beyond the problem list
- ERA/EOB records, payment posting, collections
- Insurance/coverage details beyond what C-CDA header captures
- Practice management data (scheduling, superbills, eligibility)
- Scanned/indexed documents
- Secure messages, Direct messages, text messages, eFax records
- ePrescribing history beyond the C-CDA medications section
- Custom clinical forms, specialty-specific assessments
- Any data in a non-C-CDA format

### Vendor's own content organization

The vendor does not provide a data dictionary or organize content into categories. The only categorization is the 12 sections visible in the patient portal screenshot. The export is a single C-CDA document per patient containing those standard sections — there is no vendor-specific layering or additional data beyond the standard.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor provides a C-CDA Summary of Care export. The 12 sections visible in the patient portal (Demographics, Provider Details, Medical Documents, Allergies, Medications, Problems, Procedures, Vital Signs, Encounters, Social History, Family History, Results) represent standard C-CDA clinical summary content.

There is no indication of any vendor-specific extensions, custom sections, or supplementary data formats. The export is strictly a standard C-CDA clinical summary — the same document type used for transitions of care under criteria (b)(1)/(b)(2). The vendor appears to be repurposing their transitions-of-care C-CDA export for the (b)(10) EHI export requirement.

The vendor's reports menu (page 5) reveals 19 report types including 4 billing-related reports, confirming substantial billing and practice management data exists in the system that is not part of the export.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | "Patient Demographics" section visible in portal; C-CDA header shows name, DOB, race, language, contact info, patient IDs | Standard C-CDA demographics — adequate for basic info |
| Encounters / visits | ⚠️ Partial | "Encounters" section in portal; C-CDA header shows encounter ID, dates, location | C-CDA encounter data is typically thin (date, type, location) vs. full encounter documentation |
| Problems / conditions | ✅ Covered | "Problems" section in portal; screenshot shows coded problem list with SNOMED codes, dates, status | Standard C-CDA problem list |
| Medications / prescriptions | ⚠️ Partial | "Medications" section in portal; ePrescribing is an add-on feature ($25/prescriber/month) | C-CDA captures medication list but likely misses detailed Rx history, prescription fills, refill data from ePrescribing integration |
| Allergies | ✅ Covered | "Allergies" section in portal; clinical document screenshot shows "No Current Medications" section adjacent to allergies | Standard C-CDA allergy section |
| Immunizations | ⚠️ Partial | Not listed as a separate section in portal screenshot, but product is certified for (f)(1) immunization registry | Product stores immunization data (has "Immunizations" icon on dashboard and "Immunization Export Report" in reports menu); unclear if included in C-CDA export sections |
| Vitals | ✅ Covered | "Vital Signs" section in portal | Standard C-CDA vital signs |
| Lab results | ✅ Covered | "Results (Discrete)" section in portal; product has lab integration | Standard C-CDA results section |
| Procedures | ✅ Covered | "Procedures" section in portal | Standard C-CDA procedures |
| Clinical notes / documents | ⚠️ Partial | "Patient Medical Documents" section in portal; clinical document view shows tabs for SUMMARY, PROGRESS NOTE, COMM LOG, CONSENTS, FLAG, LAB REQUISITION, SCREENING | C-CDA may include some note content, but the product's full note types (progress notes, consent forms, screening tools, etc.) likely exceed what a C-CDA Summary of Care captures |
| Care plans / goals | ❌ Not covered | No evidence in any artifact | Product supports CCM and TCM (dashboard icons visible), which involve care plans; this is a gap |
| Orders / referrals | ❌ Not covered | No evidence in any artifact | Product is certified for CPOE (a)(1); order data likely exists but is not in C-CDA export |
| Insurance / coverage | ❌ Not covered | No insurance entities in export beyond minimal C-CDA header | Product has "Insurance's Eligibility Status" report; checks real-time eligibility; stores insurance data; significant gap |
| Claims / billing | ❌ Not covered | No billing data in export | **Critical gap.** Claimpower is primarily a billing company. They process daily claims, ERA/EOBs, denials, appeals, and collections. The reports menu includes "Billing Audit Report," "Billing Stats Report," and "Daily Office Collection Report." This is core designated-record-set data that is entirely absent from the export. |
| Payments | ❌ Not covered | No payment data in export | Product collects patient payments and posts ERA payments; not in export |
| Patient communications | ❌ Not covered | No communication data in export | Product supports secure messaging, Direct messaging, text messaging; portal screenshot shows "Secure Messaging" option; not in export |
| Imaging / diagnostic reports | ❌ Not covered | No imaging data in export | No evidence product stores imaging, so may be N/A |
| Consents / directives | ❌ Not covered | Clinical document view shows "CONSENTS" tab (page 3 screenshot), suggesting consent documents are stored | Product stores consent documents; not in export |
| Specialty-specific data | N/A | No specialty modules identified | Product serves "all specialties" per billing services but no specialty-specific EHR modules identified |

**Summary**: Of approximately 15 applicable domains, 5 are covered (Demographics, Problems, Allergies, Vitals, Lab results), 4 are partially covered (Encounters, Medications, Immunizations, Clinical notes), and 6 are not covered (Care plans, Orders, Insurance, Claims/billing, Payments, Communications, Consents). The most significant gap is **billing and claims data** — the core of Claimpower's business — which is entirely absent from the export.

## 6. Documentation Quality

The documentation quality is **extremely poor**:

- **No data dictionary**: zero field-level definitions anywhere in the 17 pages of documentation
- **No schema or format specification**: the documentation says "C-CDA" but provides no detail about which CDA document type, which template IDs, which sections are populated, what coded vocabularies are used, or what constraints apply
- **No sample data**: no example C-CDA documents are provided
- **No API documentation for export**: the bulk export is UI-only with no programmatic access documented
- **No developer guidance**: a developer could not implement an import based on these documents. They would need to obtain a sample export and reverse-engineer the structure
- **No change history**: all documents created on a single day (Aug 28, 2023) with no evidence of updates
- **Content is almost entirely screenshots**: 502 total extracted words across 17 pages. The text consists only of brief step labels like "Click on Summary of Care Records"

The documentation reads as a **compliance checkbox** created for certification with minimal effort. All four PDFs were authored by the CEO personally on the same day, suggesting they were produced specifically to satisfy the (b)(10) certification requirement.

The only technically useful information comes from the screenshots themselves, which at least confirm the export exists, show the UI workflow, and reveal the 12 C-CDA sections and the EMR's module structure.

A developer working with this export would need to:
1. Actually perform an export to obtain a sample C-CDA file
2. Parse the C-CDA to determine sections, coded values, and structure
3. Reference the C-CDA R2.1 standard for structural documentation
4. Reverse-engineer any vendor-specific content or extensions

## 7. Overall Assessment

### Classification

**Standard-based projection.** The (b)(10) EHI export is a C-CDA Summary of Care document — the same standard clinical summary used for transitions of care under criteria (b)(1)/(b)(2). This covers standard clinical data (demographics, problems, meds, allergies, vitals, labs, procedures) but fundamentally cannot represent the billing, claims, practice management, communications, and other non-clinical data that constitutes a large portion of Claimpower's designated record set.

### Key Findings

1. **The export is a C-CDA repackaging, not a genuine EHI export.** The vendor's (b)(10) documentation is titled "CCDA Export" and describes exporting C-CDA Summary of Care Records — the same clinical summary format used for care transitions. This covers ~20-30% of the data the product stores about patients.

2. **Billing and claims data — the company's core business — is entirely absent.** Claimpower is fundamentally a billing services company. They process daily electronic claims, ERA/EOBs, denials, appeals, and collections. The EMR reports menu (visible in screenshots) includes billing-specific reports confirming this data exists. None of it is in the export.

3. **Documentation is a 502-word screenshot walkthrough with zero technical content.** Across 4 PDFs and 17 pages, there is no data dictionary, no field definitions, no schema, no sample data, and no format specification. The documents show how to click through the UI to generate a ZIP file — nothing more.

4. **Practice management, communications, and scanned documents are also missing.** The product stores scheduling, insurance eligibility, patient balances, secure messages, Direct messages, text messages, and scanned/indexed paper documents. None appear in the export.

5. **Bulk export is supported.** The multi-patient export path ("Export Patient Health Records" under EMR Reports) supports selecting all patients (screenshot shows 12,217), which at least satisfies the mechanical requirement for population-level export.

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA (Summary of Care Records), delivered as ZIP
Model type:      Standard projection (HL7 C-CDA R2.1)
Entities:        N/A (no data dictionary; 12 C-CDA sections visible)
Fields:          N/A (no field-level documentation)
Descriptions:    N/A (no data dictionary)
Sample data:     No
Bulk export:     Yes (via "Export Patient Health Records" report)
Domains covered: 5 of 15 applicable domains fully covered; 4 partial
```

### Bottom Line

Claimpower's EHI export is a C-CDA clinical summary being called a (b)(10) export — a classic case of repurposing the transitions-of-care document for the "all EHI" requirement. For a company whose primary business is medical billing, the complete absence of billing, claims, and payment data from the export is a critical gap. A patient or provider receiving this export would get a standard clinical summary but would be missing the majority of their designated record set, particularly all financial and billing records.
