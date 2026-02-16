# EHI Export Analysis: Tebra Technologies, Inc.

**Product**: Tebra EHR v5.1
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2777.Tebr.05.03.1.241219 (CHPL #11557)

## 1. Product Context

Tebra EHR (formerly Kareo EHR) is a cloud-based all-in-one practice management and EHR platform built for independent ambulatory practices. It serves 140,000+ providers across specialties including primary care, mental health, pediatrics, dermatology, chiropractic, and podiatry. The platform was formed from the merger of Kareo (clinical + billing) and PatientPop (patient engagement + marketing).

**Data domains the product stores** (relevant to EHI export completeness):

- **Clinical documentation**: SOAP notes with templates/macros, AI Note Assist (ambient AI documentation), problem lists, medication lists, allergy lists, vital signs, assessment/plan, visit summaries, care plans
- **E-prescribing**: Via DrFirst Rcopia — prescription ordering, drug interaction checks, refill tracking
- **Lab orders/results**: Via LabSoft integration with LabCorp and Quest — bidirectional lab interfaces
- **Billing & revenue cycle**: Insurance eligibility verification (2,700+ payers), electronic claims, ERA/EOB auto-posting, denial tracking, patient statements, payment collection, charge capture, A/R tracking
- **Patient portal**: Secure messaging, lab/visit results viewing, bill viewing, online payments, document sharing
- **Scheduling**: Appointment management, online self-scheduling, automated reminders, two-way texting
- **Telehealth**: Built-in HIPAA-certified video visits
- **Patient intake**: Digital intake forms flowing into EHR
- **Practice marketing**: Reputation management, SEO, directory listings (PatientPop lineage — not EHI)

The product has comprehensive billing capabilities integrated alongside clinical charting. This is a critical baseline: a genuine (b)(10) export should cover both clinical AND billing data in computable formats.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `macra_mips_page.html` (173 KB) | Registered EHI documentation URL. Contains a single paragraph (47 words) on EHI Export Functionality. | **Primary source** — but extremely thin |
| `cures_act_request_form_screenshot.png` | Screenshot of OneTrust privacy portal form listing 19 EHI data categories patients can request | **Key evidence** — shows the 19 categories Tebra acknowledges as EHI |
| `cures_act_request_form.html` (131 KB) | HTML of the request form page; actual form loaded via iframe from privacyportal.onetrust.com | Low — form content is dynamically loaded |
| `help_export_patient_clinical_data.html` (65 KB) | Help Center article describing how to run bulk C-CDA exports | **Moderate** — confirms export mechanics but no field detail |
| `help_cures_act_faqs.html` (69 KB) | 21st Century Cures Act FAQ from help center | **Moderate** — reveals ShareFile fulfillment for non-USCDI EHI |
| `2024_test_results.pdf` (373 KB) | RWT Measure #4: 3,931 EHI exports across 790 practices (Apr–Jun 2024) | **Key evidence** — confirms export is C-CDAs + documents |
| `2025_test_plan.pdf` (285 KB) | RWT plan for 2025; Measure #4 targets (b)(10) EHI exports | Low — planning only |
| `2024_test_plan.pdf` (1.4 MB) | RWT plan originally measuring (b)(6), later substituted for (b)(10) | **Moderate** — reveals the (b)(6)→(b)(10) substitution |
| `fhir_api_guide.pdf` (912 KB, ~33 pages) | FHIR R4 API User Guide (May 2025) documenting (g)(10) API with 22 US Core resource types | Low for (b)(10) — this is the (g)(10) API, not EHI export |
| `general_api_docs.pdf` (599 KB) | Older (2023) patient-facing clinical API with 14 JSON endpoints | Low for (b)(10) — separate patient portal API |
| `costs_and_guidance.pdf` (101 KB) | Dec 2022 costs document; references "Kareo EHR" and (b)(6), not (b)(10) | Low — outdated, predates (b)(10) certification |
| `ehi_export_section_screenshot.png` (5 KB) | Screenshot of the EHI Export Functionality heading | Minimal — just shows the section title |
| `2022_test_plan.pdf`, `2022_test_results.pdf`, `2023_test_plan.pdf`, `2023_test_results.pdf` | Pre-(b)(10) certification RWT documents | Not relevant — predate (b)(10) |
| `macra_mips_page_full.png` (2.5 MB) | Full-page screenshot of MACRA/MIPS page | Contextual |
| `certification_section_screenshot.png` (5 KB) | Screenshot of ONC certification heading | Minimal |

## 3. Export Mechanics

**Format(s):**
1. **C-CDA (XML)** — Summary of Care documents for clinical records
2. **PDF** — for claims and billing information (non-computable)
3. **Native format** — uploaded documents in their original format

**Mechanism:**
- **Self-service clinical export**: Practice Settings > Data Management > Export Patient Data. Providers select a date range and provider, then download a zip file of individual .ccda XML files per patient, plus patient documents.
- **Recurring exports**: Can be scheduled monthly (1st of month) or weekly (Mondays).
- **Cures Act Request Form**: Patients can submit a request via OneTrust privacy portal at `https://www.tebra.com/cures-act-request/`, selecting from 19 data categories. Fulfilled via "secure ShareFile service" — this is a manual, vendor-mediated process.

**Single-patient vs bulk**: The self-service export is bulk (date range + provider filter). Individual patient export is available via the Cures Act request form. The RWT data shows most exports covered 10 or fewer patients (single-day ranges).

**Access constraints**: No fees mentioned for the clinical export (included in base EHR price per the Costs and Guidance document). The Cures Act request form process is manual and vendor-mediated, with no documented SLA.

## 4. Export Content: What's In It

### No data dictionary exists

There is **zero field-level documentation** for the (b)(10) export. The entire export documentation on the registered URL is a single paragraph of 47 words:

> "Tebra EHR enables providers to export out EHI for individual patients and their patient population at any time without developer assistance. Export formats include C-CDA documents for clinical records, PDFs for claims and billing information, and also documents in the original native format which they were uploaded."

There is no data dictionary, no schema, no field listing, no sample data, no format specification.

### Vendor's own content organization

The only structured categorization Tebra provides is the 19 categories on the Cures Act Request Form:

| # | Category (Vendor's) | Format | Field Documentation | Notes |
|---|---|---|---|---|
| 1 | Allergies and Intolerances | Unknown | None | USCDI-aligned |
| 2 | Assessment and Plan of Treatment | Unknown | None | USCDI-aligned |
| 3 | Care Team Members | Unknown | None | USCDI-aligned |
| 4 | Clinical Notes | Unknown | None | USCDI-aligned |
| 5 | Immunizations | Unknown | None | USCDI-aligned |
| 6 | Laboratory Tests & Results | Unknown | None | USCDI-aligned |
| 7 | Medications | Unknown | None | USCDI-aligned |
| 8 | Patient Demographics | Unknown | None | USCDI-aligned |
| 9 | Problems | Unknown | None | USCDI-aligned |
| 10 | Procedures | Unknown | None | USCDI-aligned |
| 11 | Patient's Implantable Device(s) | Unknown | None | USCDI-aligned |
| 12 | Vital Signs | Unknown | None | USCDI-aligned |
| 13 | Past Medical History | Unknown | None | May overlap with Problems |
| 14 | Past Surgical History | Unknown | None | May overlap with Procedures |
| 15 | Family History | Unknown | None | Beyond standard USCDI |
| 16 | Social History (e.g., smoking status) | Unknown | None | Partially USCDI (smoking) |
| 17 | OB/Pregnancy History | Unknown | None | Beyond standard USCDI |
| 18 | Account/Insurance Information | Unknown | None | Beyond USCDI — billing domain |
| 19 | Documents | Unknown | None | Uploaded documents |

**Critical gap**: For the self-service export (the one actually used by 790 practices in 3 months), the output is C-CDA files + documents. The C-CDA content follows the standard Summary of Care template — which covers approximately USCDI-scope clinical data. The Cures Act Request Form categories beyond USCDI (Past Medical/Surgical History, Family History, OB/Pregnancy History, Account/Insurance Information) are only available via the manual ShareFile fulfillment process.

### Comparison: Self-service export vs. request form

| Dimension | Self-Service Export | Cures Act Request Form |
|---|---|---|
| Initiation | Provider-initiated via UI | Patient-initiated via web form |
| Format | C-CDA XML + PDF + native docs | Unknown (ShareFile delivery) |
| Content | C-CDA Summary of Care + documents | 19 selectable categories |
| Automation | Fully automated, schedulable | Manual, vendor-mediated |
| Computable | C-CDA yes; PDF no | Unknown |
| Field documentation | None | None |

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

Tebra's EHI export approach has two tiers:

**Tier 1 — Self-service clinical export (the primary mechanism):**
- C-CDA Summary of Care files containing standard clinical data (demographics, problems, medications, allergies, vitals, labs, immunizations, procedures, clinical notes, care team, goals, assessment/plan, implantable devices)
- Patient documents in native upload format
- This is functionally identical to the (b)(6) data portability export and the transitions of care (b)(1) C-CDA — the 2024 test plan explicitly acknowledges substituting the (b)(6) measure for (b)(10)

**Tier 2 — Cures Act Request Form (supplementary):**
- 19 categories selectable via OneTrust privacy portal
- 13 categories align with USCDI/C-CDA content (already in Tier 1)
- 6 categories go beyond USCDI: Past Medical History, Past Surgical History, Family History, OB/Pregnancy History, Account/Insurance Information, Documents
- Fulfilled manually via ShareFile — no self-service, no field documentation, no format specification

**Notable observations:**
- The "Account/Insurance Information" category is the only acknowledgment of billing/financial data in the export
- No categories for: claims, charges, payments, ERA/EOB, denial tracking, superbills, patient statements, A/R — all of which Tebra stores
- No categories for: secure messages, intake forms, appointment history, telehealth records, referrals
- Billing data in the self-service export is described as "PDFs for claims and billing" — rendered PDFs are not computable

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA patient data + request form "Patient Demographics" | C-CDA covers standard demographics; depth of vendor-specific fields unknown |
| Encounters / visits | ⚠️ Partial | C-CDA encounter sections | C-CDA covers encounter summaries; product stores rich encounter workflow data |
| Problems / conditions | ⚠️ Partial | C-CDA problem list + request form "Problems" | Standard C-CDA coverage; EHR likely stores additional metadata (onset context, verification workflows) |
| Medications / prescriptions | ⚠️ Partial | C-CDA medications + request form "Medications" | C-CDA covers active meds; full e-prescribing history via DrFirst/Rcopia unclear |
| Allergies | ⚠️ Partial | C-CDA allergies + request form "Allergies and Intolerances" | Standard coverage |
| Immunizations | ⚠️ Partial | C-CDA immunizations + request form "Immunizations" | Standard coverage |
| Vitals | ⚠️ Partial | C-CDA vital signs + request form "Vital Signs" | Standard coverage |
| Lab results | ⚠️ Partial | C-CDA results + request form "Laboratory Tests & Results" | C-CDA covers results; full order details via LabSoft integration unclear |
| Imaging / diagnostic reports | ⚠️ Partial | C-CDA diagnostic reports section | Product mentions imaging ordering but depth of imaging data is unclear |
| Procedures | ⚠️ Partial | C-CDA procedures + request form "Procedures" + "Past Surgical History" | Standard coverage |
| Clinical notes / documents | ✅ Covered | C-CDA clinical notes + uploaded documents in native format + request form "Clinical Notes" + "Documents" | Best-covered domain; includes AI Note Assist output (as signed notes) and uploaded documents |
| Care plans / goals | ⚠️ Partial | C-CDA care plan sections + request form "Assessment and Plan of Treatment" | Standard C-CDA coverage |
| Orders / referrals | ❌ Not covered | No evidence of order export | Product supports lab ordering, imaging ordering, referrals — none documented in export |
| Insurance / coverage | ⚠️ Partial | Request form "Account/Insurance Information" (Tier 2 only) | Only via manual request; not in self-service export; no field detail |
| Claims / billing | ⚠️ Partial | Self-service: "PDFs for claims and billing" (non-computable) | **Significant gap**: Product has full RCM (claims, ERA/EOB, denials, charge capture) but export is only rendered PDFs — not computable. No structured billing data export documented. |
| Payments | ❌ Not covered | No evidence | Product manages patient payments, payment collection, transaction history — none in export |
| Consents / directives | ❌ Not covered | No evidence | No mention in any export documentation |
| Patient communications / portal messages | ❌ Not covered | No evidence | Product has secure messaging, two-way texting, portal messages — none in export |
| Specialty-specific (OB/GYN) | ⚠️ Partial | Request form "OB/Pregnancy History" (Tier 2 only) | Only via manual request; not in self-service export |
| Family health history | ⚠️ Partial | Request form "Family History" (Tier 2 only) | Only via manual request |

**Summary**: Of 20 applicable domains, 1 is well-covered (clinical notes/documents), 13 are partially covered (mostly via standard C-CDA with no vendor-specific depth), 4 are not covered at all, and 2 are only available via manual request. The product's major capability — billing and revenue cycle management — is covered only by non-computable PDFs, which fails the (b)(10) computable format requirement.

## 6. Documentation Quality

**Overall: Very poor.** The (b)(10) export documentation is among the thinnest possible for a certified product.

- **Data dictionary**: None. Zero tables, zero fields, zero types documented.
- **Schema**: None. No XSD, JSON Schema, or prose field descriptions.
- **Sample data**: None. No examples of exported C-CDA content or billing PDFs.
- **Format specification**: None beyond naming three formats (C-CDA, PDF, native).
- **Export instructions**: The registered URL has no link to the Help Center article that describes how to actually run the export. A user must discover it independently.
- **Machine-readable artifacts**: None.

**Could a developer build an import from this documentation?** No. A developer would have to rely entirely on the C-CDA standard specification (not vendor-documented) and reverse-engineer any vendor-specific content. For billing data (PDF), no programmatic import is possible. For the Cures Act Request Form categories, there is no documentation of what format or fields the ShareFile delivery contains.

**Contrast with (g)(10) documentation**: The FHIR API User Guide (33 pages) documents 22 US Core resource types with field tables, authentication flows, and registration procedures. This shows Tebra is capable of producing documentation — they simply didn't for (b)(10).

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation is too thin to fully assess coverage, but available evidence indicates the export covers only a fraction of what the product stores. The self-service export — the mechanism actually used by practices — is a C-CDA Summary of Care export, which covers roughly USCDI-scope clinical data. Billing data is exported only as non-computable PDFs. The Cures Act Request Form lists 19 categories but provides zero documentation of what those categories contain, how they're formatted, or how they're delivered beyond "ShareFile." Multiple major data domains the product stores (payments, portal messages, intake forms, orders, referrals, detailed billing records) have no evidence of export coverage.

**Axis 2 — Export approach: Repackaged existing export**

Multiple lines of evidence converge on this classification:

1. **The (b)(6)→(b)(10) substitution**: The 2024 RWT plan originally measured (b)(6) "Patient Batch Export" of C-CDAs. The results document explicitly states they "substituted it for the broader 315(b)(10) EHI Export." This is the clearest possible signal that the same C-CDA batch export was relabeled from (b)(6) to (b)(10).

2. **C-CDA Summary of Care as the core**: The self-service export produces the same Summary of Care documents used for transitions of care under (b)(1). The Help Center article title is "Export Patient Clinical Data" — it's a clinical data export, not an "all EHI" export.

3. **No purpose-built export infrastructure**: There is no evidence of any export mechanism built specifically for (b)(10). No new data formats, no database-level export, no field mapping beyond C-CDA standard sections.

4. **The Cures Act Request Form is a compliance addendum**: The OneTrust privacy portal form appears to be a manual supplement to address the gap between C-CDA coverage and the full EHI definition. But it's a manual, vendor-mediated process with no documentation of outputs — not a technical export solution.

### Key Findings

1. **The entire (b)(10) export documentation is 47 words.** One paragraph on the MACRA/MIPS page with no data dictionary, no schema, no sample data, no format specification — the absolute minimum viable disclosure (source: `macra_mips_page.html`).

2. **The (b)(10) export is an explicitly relabeled (b)(6) C-CDA batch export.** The 2024 RWT Results confirm that RWT Measure #4 "previously identified a measure for 315(b)(6) Patient Batch Export, but we have substituted it for the broader 315(b)(10) EHI Export" (source: `2024_test_results.pdf`, RWT Measure #4).

3. **Billing data is exported only as non-computable PDFs.** The product has comprehensive billing/RCM capabilities (claims, ERA/EOB, denials, payments, charge capture), but the export describes billing as "PDFs for claims and billing information." PDF is not a computable format as required by (b)(10) (source: `macra_mips_page.html`).

4. **The Cures Act Request Form supplements the export but is undocumented.** The OneTrust form lists 19 categories patients can request, but there is no documentation of what data each category contains, what format it's delivered in, or when the request is fulfilled (source: `cures_act_request_form_screenshot.png`, `help_cures_act_faqs.html`).

5. **Major product capabilities are absent from the export.** Patient portal messages, intake forms, detailed billing records, payment history, order details, referral workflows, and telehealth records have no evidence of coverage in any export mechanism.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Repackaged existing export
Export format:   C-CDA (XML) + PDF + native documents
Entities:        0 (no data dictionary)
Fields:          0 (no field-level documentation)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (C-CDA batch export by date range/provider)
Domains covered: 1 of 20 well-covered; 13 of 20 partially (via standard C-CDA)
```

### Bottom Line

Tebra's (b)(10) export is a rebranded C-CDA batch export — the same mechanism used for (b)(6) data portability and (b)(1) transitions of care — supplemented by non-computable billing PDFs and a manual vendor-mediated request form. A patient or provider would receive standard clinical summary data but would not get computable billing records, structured payment history, portal messages, or the full depth of clinical data the EHR stores beyond what fits in a C-CDA. The single biggest gap is the absence of computable billing data from a product whose billing and revenue cycle management is a core capability.
