# EHI Export Analysis: Claimpower, Inc.

**Product**: Claimpower Mobile EMR  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.04.04.1238.Clai.06.02.1.230109

## 1. Product Context

Claimpower Mobile EMR is a cloud-based, mobile-friendly EHR designed for small ambulatory physician practices, offered by Claimpower, Inc. — a company whose core business is **managed medical billing services**. The EMR is bundled free with billing services and is not sold standalone. This is significant: the company's primary value proposition is billing, not clinical documentation.

The platform stores:
- **Clinical data**: demographics, problem lists, medication lists, allergies, immunizations, lab orders/results, prescriptions, clinical notes (with Dragon dictation), family health history, implantable devices, vital signs, procedures, care plans
- **Practice management data**: patient scheduling, insurance eligibility, patient balances, payments, superbills/encounter forms, scanned documents
- **Billing and claims data**: electronic claims (primary/secondary), ERA/EOB records, CPT/ICD-10 codes, denial/appeal records, payment posting, collections activity — this is the company's core business
- **Communication data**: secure messages (provider-to-provider, provider-to-patient), Direct messages, text messages, eFax records

A complete (b)(10) export from this product should cover all of these domains. The billing data is especially notable given that billing is the company's primary service.

## 2. Artifacts Reviewed

| Artifact | Size | Pages | Description | Informativeness |
|---|---|---|---|---|
| `CCDA_Export.PDF` | 1,063,362 bytes | 9 | Main document: index page + all three sub-walkthroughs inline | **Primary artifact** — but contains only screenshot walkthroughs |
| `CCDA_Export_Single_Patient.PDF` | 511,961 bytes | 3 | Single-patient C-CDA export walkthrough | Low — redundant with main PDF |
| `CCDA_Multiple_Patients.PDF` | 271,425 bytes | 2 | Multi-patient C-CDA export walkthrough | Low — redundant with main PDF |
| `CCDA_Patient_Portal.PDF` | 396,625 bytes | 3 | Patient portal C-CDA export walkthrough | Low — redundant with main PDF |

**Total**: 4 PDFs, 17 pages, 502 words of extractable text combined. All four artifacts are screenshot walkthroughs showing UI navigation steps. The main PDF (`CCDA_Export.PDF`) contains the other three inline, making the sub-documents redundant.

**No data dictionary, no schema, no field definitions, no sample data files were provided.** The analysis script (`analysis/analyze-pdfs.py`) confirmed: zero PDFs contain data dictionary indicators (no "field name," "column," "data type," or "schema" keywords). All four reference C-CDA and consist entirely of step-by-step screenshot instructions.

## 3. Export Mechanics

- **Format**: C-CDA (Consolidated Clinical Document Architecture), delivered as a ZIP file
- **Mechanism**: UI-based — three paths documented:
  1. **Single patient**: Lookup Medical Records → select patient → Clinical Document → Summary of Care Records → Generate → Download ZIP
  2. **Multiple patients**: EMR Reports → Export Patient Medical Records → select patients (or select all; screenshot shows 12,217 patients available) → Generate ZIP
  3. **Patient portal**: Patient Portal login → View Health Information → Summary of Care Records → Download ZIP
- **Single-patient**: Yes (paths 1 and 3)
- **Bulk capability**: Yes (path 2 supports selecting multiple or all patients)
- **Access constraints**: Requires authenticated login to the Claimpower web platform; patient portal path requires patient credentials (3-digit client ID, name, DOB, 4-digit password)
- **Fees**: Not mentioned in the export documentation; mandatory disclosures list the EMR as free with billing services

## 4. Export Content: What's In It

The export documentation provides **no information about what data elements are included in the export**. The documentation consists entirely of UI navigation screenshots showing how to initiate and download a C-CDA export. There is:

- **No data dictionary** — zero entities, zero fields documented
- **No schema** — no machine-readable or human-readable format specification
- **No field definitions** — no names, types, descriptions, value sets, or relationships
- **No sample data** — no example C-CDA files provided
- **No description of C-CDA sections included** — the documentation does not even list which standard C-CDA sections are populated

The title "Summary of Care Records" and the export labeled "CCDA" indicate this is a standard C-CDA Summary of Care document. Based on the C-CDA standard (not vendor documentation), such a document typically includes: patient demographics, problems, medications, allergies, immunizations, vital signs, procedures, lab results, and clinical notes. However, the vendor provides zero confirmation of which sections are populated or to what depth.

### Vendor's own content organization

The vendor provides no content organization. There is no entity/table/field documentation of any kind.

| Entity/Table | Fields | Described | Types | Category |
|---|---|---|---|---|
| *(none documented)* | — | — | — | — |

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's documentation describes exactly one thing: how to navigate the UI to download a C-CDA ZIP file. There are three paths (single patient, multiple patients, patient portal) but all produce the same output format — a C-CDA "Summary of Care Record."

The vendor provides no categorization, no module breakdown, no content description. The entire documentation is 502 words of step instructions like "Step 1 → Click on Lookup Medical Records" accompanied by screenshots.

### 5b. Standardized domain coverage (top-down)

Since no data dictionary or sample data exists, coverage is assessed based on what a standard C-CDA Summary of Care Record would include. Coverage is marked as "Partial" for standard C-CDA sections (since we can infer the standard covers them but cannot verify Claimpower's implementation) and "Not covered" for domains outside C-CDA scope.

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial (inferred) | C-CDA header includes demographics per standard; screenshot shows patient name/DOB/contact fields | Standard C-CDA demographics are basic; product likely stores more |
| Encounters / visits | ⚠️ Partial (inferred) | C-CDA may include encounter context | Cannot verify depth |
| Problems / conditions | ⚠️ Partial (inferred) | Standard C-CDA section | Cannot verify |
| Medications / prescriptions | ⚠️ Partial (inferred) | Standard C-CDA section; product has ePrescribing ($25/mo add-on) | Prescription details beyond C-CDA summary likely missing |
| Allergies | ⚠️ Partial (inferred) | Standard C-CDA section | Cannot verify |
| Immunizations | ⚠️ Partial (inferred) | Standard C-CDA section; product certified for (f)(1) immunization reporting | Cannot verify |
| Vitals | ⚠️ Partial (inferred) | Standard C-CDA section | Cannot verify |
| Lab results | ⚠️ Partial (inferred) | Standard C-CDA section; product has lab integration | Cannot verify |
| Imaging / diagnostic reports | ⚠️ Partial (inferred) | May be in C-CDA if product stores them | Unclear if product stores imaging |
| Procedures | ⚠️ Partial (inferred) | Standard C-CDA section | Cannot verify |
| Clinical notes / documents | ⚠️ Partial (inferred) | C-CDA may include notes section | Product supports Dragon dictation; scanned documents likely excluded |
| Care plans / goals | ⚠️ Partial (inferred) | C-CDA may include care plan section | Cannot verify |
| Orders / referrals | ⚠️ Partial (inferred) | C-CDA may include orders | CPOE-certified; order detail likely limited in C-CDA |
| Insurance / coverage | ❌ Not covered | Not a standard C-CDA section | Product stores insurance/eligibility data; **gap** |
| Claims / billing | ❌ Not covered | Not a standard C-CDA section | **Major gap** — billing is the company's core business; the product stores claims, ERA/EOBs, CPT/ICD codes, denials, appeals, payments, collections |
| Payments | ❌ Not covered | Not a standard C-CDA section | Product stores patient balances and payment records; **gap** |
| Consents / directives | ❌ Not covered | May be in C-CDA Advance Directives section but unverified | Unclear if product stores consents |
| Patient communications | ❌ Not covered | Not a standard C-CDA section | Product has secure messaging, Direct messaging, text messaging; **gap** |
| Specialty-specific data | N/A | — | Product serves multiple specialties but no specialty modules identified |
| Scanned documents | ❌ Not covered | Not a standard C-CDA section | Product supports document scanning/indexing ($0.10/page); **gap** |
| Superbills / encounter forms | ❌ Not covered | Not a standard C-CDA section | Product has customizable superbills; **gap** |

**Summary**: Of ~15 applicable data domains, 0 are confirmed covered with evidence, ~12 are inferred partially from C-CDA standards (without vendor verification), and at least 6 domains representing the product's core business (billing, insurance, payments, communications, scanned documents, superbills) are clearly outside C-CDA scope and therefore missing.

## 6. Documentation Quality

The export documentation is **among the thinnest possible** for a certified product:

- **No data dictionary**: Zero entities, zero fields documented
- **No schema**: No machine-readable or human-readable format specification
- **No sample data**: No example exports provided
- **No section/content listing**: The documentation does not even describe which C-CDA sections are populated
- **No API documentation**: Export is UI-only
- **What exists**: 17 pages of screenshot walkthroughs showing 7–8 UI navigation steps for three export paths, totaling 502 words of text

A developer could not build an import from this documentation. A patient could not understand what data is included in their export. The documentation answers only one question: "How do I click the buttons to download a ZIP file?"

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The export is a standard C-CDA Summary of Care Record — a clinical summary format designed for care transitions, not for comprehensive EHI export. Even assuming every standard C-CDA section is populated (which is unverifiable from the documentation), C-CDA by design covers only USCDI-scope clinical data. This product is primarily a **billing services company** whose platform stores extensive billing, claims, payment, insurance, and practice management data — none of which appears in a C-CDA export. The documentation is too thin to assess even the clinical coverage with any confidence.

**Axis 2 — Export approach: Repackaged existing export**

This is a textbook case of repackaging. The export is literally called "CCDA Export" in the documentation title. The same C-CDA generation used for care transitions (b)(1)/(b)(2) and patient portal access (e)(1) is being presented as the (b)(10) EHI export. The telltale signs are all present:
- The document title is "Claimpower EMR version 6.1 CCDA Export"
- No product-specific data dictionary exists
- No fields beyond the C-CDA standard are documented
- No billing, practice management, or operational data is addressed
- The three export paths (clinical document, EMR reports, patient portal) all produce the same C-CDA output
- The URL is literally `claimpowerehr.com/curesUpdate/CCDA_Export.PDF`

### Key Findings

1. **The entire (b)(10) documentation is 502 words of screenshot walkthroughs** across 17 PDF pages, with zero data dictionary content. No entities, fields, types, descriptions, schemas, or sample data are provided (`analysis/pdf-analysis-output.json`).

2. **The export is a standard C-CDA Summary of Care Record** rebranded as EHI export. This is the same clinical exchange format used for transitions of care and patient portal access — not a purpose-built EHI export.

3. **Billing data — the company's core business — is entirely absent.** Claimpower is primarily a billing services company. The product stores claims, ERA/EOBs, CPT/ICD codes, denials, appeals, payments, and collections data. None of this is in C-CDA.

4. **At least 6 data domains beyond C-CDA scope are missing**: billing/claims, insurance details, payments, patient communications (secure messaging, Direct, text), scanned documents, and superbills — all features the product is known to support.

5. **The bulk export path exists but exports the same limited format.** The "Export Patient Medical Records" function under EMR Reports supports selecting all patients (screenshot shows 12,217), but the output is still C-CDA ZIP files.

### Summary Stats

    Coverage:        Minimal/stub/unclear
    Approach:        Repackaged existing export
    Export format:   C-CDA (Summary of Care Record, ZIP)
    Entities:        N/A (no data dictionary)
    Fields:          N/A (no data dictionary)
    Descriptions:    N/A
    Sample data:     No
    Bulk export:     Yes (multi-patient selection available)
    Domains covered: 0 confirmed of ~15 applicable (up to 12 inferred from C-CDA standard but unverified)

### Bottom Line

Claimpower's (b)(10) export is a standard C-CDA Summary of Care Record with no product-specific documentation — a clinical summary rebranded as EHI export. For a company whose core business is medical billing, the absence of any billing, claims, or payment data from the export is a critical gap. A patient requesting their complete record would receive only a clinical summary, missing the billing, communications, and practice management data that constitutes a substantial portion of their designated record set.
