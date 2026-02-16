# EHI Export Analysis: Claimpower, Inc.

**Product**: Claimpower Mobile EMR v6.1
**Analysis date**: 2026-02-16
**CHPL IDs**: 11209 (15.04.04.1238.Clai.06.02.1.230109)

## 1. Product Context

Claimpower, Inc. is a small, family-run healthcare IT company based in Glen Rock, NJ, founded in 1992. Its **core business is managed medical billing services** for small ambulatory physician practices. The company bundles a proprietary cloud-based EHR/EMR (Claimpower Mobile EMR) free of charge to practices that use its billing services — the EMR is not offered as a standalone product.

The product serves small and solo physician practices across multiple specialties. Based on the vendor's own feature descriptions and ONC certifications, the platform stores:

- **Clinical data**: Patient demographics, problem lists, medication lists, allergy lists, clinical notes (with Dragon dictation), lab orders/results, prescriptions, family health history, implantable device lists, immunization records, C-CDA documents, clinical quality measure data
- **Practice management data**: Patient scheduling, insurance eligibility, patient balances, payment records, superbills/encounter forms, scanned/indexed documents
- **Billing/claims data**: Electronic claims (primary/secondary), ERA/EOB records, CPT/ICD-10 codes, denial and appeal records, payment posting, collections activity
- **Communication data**: Secure messages (provider-to-provider, provider-to-patient), Direct messages, text messages, eFax records

The billing data is particularly important context: Claimpower is **primarily a billing company** with an EHR, not the reverse. Billing and claims data constitute a substantial portion of the patient-level data the platform manages.

## 2. Artifacts Reviewed

| Artifact | Pages | Size | Description | Informative? |
|---|---|---|---|---|
| `CCDA_Export.PDF` | 9 | 1,063,362 bytes | Main document: title/index page (p1) + all three sub-documents inline (pp 2–9). Screenshot walkthroughs of three C-CDA export paths. | **Most informative** — contains all content from the sub-documents plus the index |
| `CCDA_Export_Single_Patient.PDF` | 3 | 511,961 bytes | Single patient C-CDA export walkthrough. Subset of main PDF (pp 2–4). | Redundant with main PDF |
| `CCDA_Multiple_Patients.PDF` | 2 | 271,425 bytes | Multiple patient C-CDA export walkthrough. Subset of main PDF (pp 5–6). | Redundant with main PDF |
| `CCDA_Patient_Portal.PDF` | 3 | 396,625 bytes | Patient portal C-CDA export walkthrough. Subset of main PDF (pp 7–9). | Redundant with main PDF |

**Total**: 4 PDF files, 17 pages combined (9 unique pages). All authored by Rohan Thadani (CEO) on 2023-08-28 using Microsoft Word for Microsoft 365. The three sub-PDFs are exact duplicates of content in the main PDF.

All four artifacts are **screenshot walkthroughs** showing how to click through the UI to generate a C-CDA export. There is no data dictionary, no field-level documentation, no schema, and no sample data in any artifact.

## 3. Export Mechanics

- **Format**: C-CDA (Consolidated Clinical Document Architecture) XML, packaged as a ZIP file
- **Mechanism**: Web UI — three paths available:
  1. **Single patient**: Login → Lookup Medical Records → search patient → Clinical Document → Summary of Care Records → Generate (CCDA radio button) → Download ZIP
  2. **Bulk/multi-patient**: Login → EMR Reports → Export Patient Health Records → select specific patients or "All Patients" checkbox → Generate ZIP. The screenshot shows a system with **12,217 patients**, confirming bulk capability.
  3. **Patient portal (self-service)**: Patient logs in with 3-digit client ID, name, DOB, and 4-digit password → View Health Information → Summary of Care Records → Download ZIP
- **Single-patient**: Yes (paths 1 and 3)
- **Bulk export**: Yes (path 2 — "All Patients" option visible)
- **Access constraints**: Paths 1 and 2 require provider login; path 3 requires patient portal credentials
- **Fees**: Not documented

## 4. Export Content: What's In It

The export is a **C-CDA Summary of Care** document. There is no data dictionary, no field-level documentation, and no sample data provided. All evidence about export content comes from screenshots of the UI.

### What the screenshots reveal

**C-CDA header fields** (visible in Summary of Care screenshots on pages 4 and 9): The document header includes 23 fields: Patient name, date of birth, race, ethnicity, preferred language, contact info (address, phone), patient IDs (MRN, insurance IDs), document ID (OID), document creation date, performer, author, author contact info, encounter ID, encounter dates, encounter location, responsible party, responsible party contact, personal relationship, personal relationship contact, covered by (insurance/payer), covered by contact, information recipient, and legal authenticator with timestamp.

**Patient portal "View Health Information" sections** (visible in screenshot on page 8): The patient portal displays 12 expandable sections that represent the C-CDA clinical content:

| Section | Category |
|---|---|
| Patient Demographics | Demographics |
| Provider Details | Administrative |
| Patient Medical Documents | Documents |
| Allergies | Clinical |
| Medications | Clinical |
| Problems | Clinical |
| Procedures | Clinical |
| Vital Signs | Clinical |
| Encounters | Clinical |
| Social History | Clinical |
| Family History | Clinical |
| Results (Discrete) | Clinical |

**Clinical document tabs** (visible in single-patient screenshot on page 3): The patient chart has tabs for SUMMARY, E.PROGRESS NOTE, COMM LOG, CONSULTS, FLAG, LAB REQUISITION, and SCREENING — but the export only generates from "Summary of Care Records," not from these other data views.

**Health Documents menu** (visible on page 3): The export dialog offers three document types — Summary of Care Records, Clinical Summary, and Visit Summary — with format options "Referral Note" or "CCDA" (radio buttons). The CCDA option is what produces the export.

### Vendor's own content organization

The vendor provides no data dictionary or entity/field documentation. The only content organization visible is the 12 C-CDA sections listed above, which are standard C-CDA sections — not a vendor-specific data model. No field counts, types, descriptions, or value sets are documented anywhere.

**There are zero entities/tables and zero fields documented.** The entire documentation consists of UI navigation instructions.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export documentation describes exactly one thing: a C-CDA Summary of Care document. The 12 sections visible in the patient portal correspond to standard C-CDA clinical summary sections. This is the same content typically used for transitions of care under 170.315(b)(1)/(b)(2) — it is not a purpose-built EHI export.

The C-CDA standard covers a well-defined subset of clinical data. It does **not** include billing records, claims, practice management data, scanned documents, secure messages, or other non-clinical data that is part of the designated record set.

Notably, the EMR Reports menu (visible on page 5) lists 19 report types including "Billing Sent Report," "Billing Stats Report," "Insurance Liability Status," and "Daily Office Collection Report" — confirming the platform stores billing and financial data. However, the EHI export function ("Export Patient Health Records") produces only C-CDA documents, not billing or practice management data.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA header: patient name, DOB, race, ethnicity, language, address, phone. Patient portal: "Patient Demographics" section. | Standard C-CDA demographics — likely covers basics but may miss vendor-specific fields |
| Encounters / visits | ⚠️ Partial | C-CDA header: encounter ID, dates, location. Patient portal: "Encounters" section. | C-CDA encounter summary only; product stores scheduling/appointment data not in C-CDA |
| Problems / conditions | ✅ Covered | Patient portal: "Problems" section visible; problem list visible in clinical view screenshot | Standard C-CDA problem list |
| Medications / prescriptions | ⚠️ Partial | Patient portal: "Medications" section. Clinical view shows "No Current Medications" for test patient. | C-CDA medication list; product has ePrescribing ($25/month) — detailed Rx history may not be fully captured in C-CDA |
| Allergies | ✅ Covered | Patient portal: "Allergies" section. Clinical view shows allergy list with codes. | Standard C-CDA allergy section |
| Immunizations | ❌ Not covered | Not listed among the 12 patient portal sections. Product is certified for immunization registry reporting (f)(1). | Product stores immunization data (per certification); absence from visible C-CDA sections is a gap |
| Vitals | ✅ Covered | Patient portal: "Vital Signs" section | Standard C-CDA vitals |
| Lab results | ✅ Covered | Patient portal: "Results (Discrete)" section. EMR has "LAB REQUISITION" tab and lab integration features. | C-CDA results section; may not capture full lab order details |
| Procedures | ✅ Covered | Patient portal: "Procedures" section | Standard C-CDA procedures |
| Clinical notes / documents | ⚠️ Partial | Patient portal: "Patient Medical Documents" section. EMR has tabs for E.PROGRESS NOTE, CONSULTS. | C-CDA may include some notes, but product stores progress notes, consult notes, comm logs — unclear if all are in the C-CDA |
| Care plans / goals | ❌ Not covered | Not visible in any section. Product offers CCM/TCM support. | Product has CCM List and TCM List features; care plan data likely not in C-CDA export |
| Family history | ✅ Covered | Patient portal: "Family History" section. Product certified for (a)(12) family health history. | Standard C-CDA family history |
| Social history | ✅ Covered | Patient portal: "Social History" section | Standard C-CDA social history |
| Insurance / coverage | ⚠️ Partial | C-CDA header: "Covered by" field with payer info. Patient search shows insurance type (e.g., "Aetna HMO", "Aetna PPO"). | C-CDA header has basic coverage info; product stores detailed eligibility data — mostly not in C-CDA |
| Claims / billing | ❌ Not covered | No billing entities in export. Reports menu confirms billing data exists: "Billing Sent Report," "Billing Stats Report." | **Major gap.** Claimpower is primarily a billing company. Claims, ERA/EOB, CPT/ICD codes, denials, payment posting — none in C-CDA. |
| Payments | ❌ Not covered | No payment data in export. Product has "Daily Office Collection Report" and payment collection features. | Product stores payment records; not in C-CDA export |
| Orders / referrals | ⚠️ Partial | EMR has "LAB REQUISITION" tab and CPOE certification (a)(1). C-CDA may include some order info. | Product has CPOE; order details beyond what C-CDA captures are likely missing |
| Consents / directives | ❌ Not covered | No evidence in export | Uncertain if product stores advance directives |
| Patient communications | ❌ Not covered | Not in C-CDA. Product has secure messaging, Direct messaging, text messaging ($0.10/text). | Product stores secure messages and text messages; not in C-CDA export |
| Scanned documents | ❌ Not covered | Not in C-CDA. Product offers document scanning/indexing ($0.10/page). | Product stores scanned paper charts; not in C-CDA export |

**Summary**: 7 of 20 domains are covered (standard C-CDA clinical sections), 6 are partially covered, and 7 are not covered at all. The most significant gaps are **billing/claims data** (core to Claimpower's business), **payments**, **patient communications**, and **scanned documents** — all of which the product demonstrably stores.

## 6. Documentation Quality

The documentation quality is **extremely poor** — among the lowest possible for a certified product:

- **No data dictionary**: Zero entities, zero fields documented
- **No schema or format specification**: The only format information is "C-CDA" — no indication of which C-CDA document type (CCD, CDA, etc.), which template IDs, which sections are populated, or what coded value sets are used
- **No sample data**: No example C-CDA files provided
- **No API documentation** for the export mechanism (there is a separate FHIR API page at `/curesUpdate/` but it covers scheduling, not EHI export)
- **No technical content whatsoever**: All 9 unique pages are screenshot walkthroughs with brief step-by-step instructions ("Click on Lookup Medical Records," "Click on Summary of Care Records")
- **Total text content**: 1,859 characters across 9 pages (the main PDF) — the rest is screenshots

A developer could not build an import from this documentation. They would need to obtain a sample C-CDA export and reverse-engineer its structure. Even then, they would only have the clinical summary — no documentation exists for how to obtain billing, practice management, or communication data.

The documentation appears to be a **compliance checkbox** created specifically for ONC certification. All four PDFs were authored by the CEO (Rohan Thadani) on the same date (August 28, 2023) using Microsoft Word, suggesting they were produced in a single session to satisfy the (b)(10) requirement.

## 7. Overall Assessment

### Classification

**Standard-based projection**

The export is a C-CDA Summary of Care document — the same standard clinical summary used for transitions of care. There is no native data model export, no vendor-specific data format, and no coverage of data domains beyond what C-CDA supports. The vendor has effectively repurposed its (b)(1)/(b)(2) transitions-of-care capability as its (b)(10) EHI export.

### Key Findings

1. **C-CDA repackaging as EHI export**: The vendor's "(b)(10) EHI export" is simply its existing C-CDA Summary of Care export. The documentation title is literally "Claimpower EMR version 6.1 **CCDA Export**." This is a textbook case of the common failure mode where vendors point to their transitions-of-care C-CDA and call it an EHI export. (`CCDA_Export.PDF`, page 1)

2. **Billing data entirely absent despite being the vendor's core business**: Claimpower is fundamentally a billing services company — its billing features (claims, ERA/EOB, CPT/ICD coding, denials, payment posting) are the primary value proposition. The EMR Reports menu (visible in `CCDA_Export.PDF`, page 5) confirms billing reports exist ("Billing Sent Report," "Billing Stats Report," "Insurance Liability Status," "Daily Office Collection Report"). None of this data is in the C-CDA export.

3. **Zero technical documentation**: Across all 4 PDFs (17 pages), there is no data dictionary, no field definitions, no schema, no sample data, and no format specification beyond "C-CDA." The entire documentation is screenshot walkthroughs of the UI. Total extractable text: 1,859 characters in the main PDF.

4. **Bulk export capability exists**: The multi-patient export path (EMR Reports → Export Patient Health Records) shows an "All Patients" checkbox with 12,217 patients, confirming the system supports bulk C-CDA export — but only for C-CDA clinical data. (`CCDA_Export.PDF`, page 6)

5. **Multiple data domains demonstrably stored but not exported**: Screenshots reveal the EMR stores data in areas including scheduling, billing, lab requisitions, communication logs, consult notes, CCM/TCM tracking, and scanned documents — none of which are addressed by the C-CDA export.

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA XML (ZIP archive)
Model type:      Standard projection (C-CDA Summary of Care)
Entities:        0 (no data dictionary)
Fields:          0 (no field documentation)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (multi-patient C-CDA, up to all patients)
Domains covered: 7 of 20 applicable domains (7 partial, 7 not covered)
```

### Bottom Line

A patient or provider requesting their complete health record from Claimpower would receive a C-CDA clinical summary — the same document used for transitions of care — containing standard clinical data (problems, medications, allergies, vitals, labs, procedures, social/family history). They would **not** receive billing records, claims history, payment data, secure messages, scanned documents, or any of the extensive practice management and billing data that constitutes Claimpower's core offering. For a company whose primary business is medical billing, the complete absence of billing data from the EHI export is the single most significant gap.
