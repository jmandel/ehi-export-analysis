# EHI Export Analysis: CareCloud, Inc.

**Product**: talkEHR
**Analysis date**: 2026-02-15
**CHPL IDs**: 15.04.04.2790.Talk.01.01.1.181217 (CHPL #9799)

## 1. Product Context

talkEHR is a cloud-based EHR and practice management platform developed by CareCloud, Inc. (formerly MTBC). Launched in 2017, it targets small to mid-sized ambulatory practices across 70+ specialties. It is an integrated platform combining:

- **EHR/Clinical documentation**: Charting with specialty-specific templates, voice dictation, clinical decision support, AI-powered diagnosis predictions
- **CPOE**: Medication, laboratory, and diagnostic imaging ordering
- **E-Prescribing**: Surescripts-integrated prescribing including controlled substances (EPCS)
- **Practice management**: Appointment scheduling, patient check-in, staff scheduling
- **Medical billing / RCM**: Insurance claim submission, payment posting, denial management, revenue cycle tools
- **Patient engagement**: Patient portal (talkPHR) with secure messaging, lab results, appointment scheduling, telehealth
- **Financial analytics**: PrecisionBI Lite dashboards and reporting
- **Public health reporting**: Immunization registries, syndromic surveillance, cancer/electronic case reporting

This breadth means a complete EHI export should cover clinical data (notes, meds, labs, vitals, problems, allergies, immunizations, procedures), billing/claims data, insurance/coverage, patient communications, prescriptions, care plans, referrals, and documents. The product is certified for 47 ONC criteria including (b)(10).

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `talkEHR-b10-EHI-Export-Documentation.pdf` (1.1 MB, 12 pages) | Primary (b)(10) documentation. Describes export formats, C-CDA sections with XPATHs and code systems, non-CCD export categories. Created 2023-11-14 in Microsoft Word 2013. | **Most informative** — the sole substantive export documentation |
| `cost-and-fees-information.html` (61 KB) | ONC mandatory disclosures page from talkehr.com. Lists all 47 certified criteria, states "no additional fee." Footer links to the b(10) PDF. | Moderately informative — confirms b(10) certification and PDF link |
| `screenshot-footer-with-b10-link.png` (229 KB) | Screenshot of the talkehr.com cost-and-fees page footer showing the "§170.315(b)(10) Electronic Health Information export - Documentation" link under "Legal & Compliance" | Low — confirms link location only |
| `screenshot-b10-link-footer.png` (3 KB) | Small crop of page footer ("by CareCloud") | Minimal value |

**No sample data, data dictionary, machine-readable schema, or sample export files were provided.** The entire export documentation consists of a single 12-page PDF.

## 3. Export Mechanics

The PDF describes three export pathways:

1. **C-CDA Single Patient Export**: Navigate to CCDA Report → CCDA Export Tab → select patient → Generate → Download XML. Produces a single C-CDA XML document.

2. **C-CDA Bulk Patient Export**: Navigate to CCDA Report → Data Portability Tab → select date range → Export. Downloads a ZIP file of C-CDA XMLs for the patient population.

3. **Non-CCD data via Reports**: Within the application's Reports section, users can export appointments, patient demographics, insurance details, patient messages, and claim data in PDF format.

4. **FHIR**: The document states talkEHR's "FHIR server creates a single-patient FHIR resource Document Reference and supports FHIR Bulk Data EHI Export for patient population as described in §170.315(b)(10)(ii)." No further detail is provided about the FHIR export's scope or content.

**Access**: Practice administrators grant export access to users. Users can perform exports "at any time without developer assistance." No fees mentioned (consistent with "no additional fee" on the mandatory disclosures page).

**Bulk capability**: Yes — both C-CDA bulk (ZIP of XMLs by date range) and FHIR Bulk Data are mentioned.

## 4. Export Content: What's In It

### Clinical data (C-CDA)

The export's clinical component is a standard C-CDA document conforming to §170.205(a)(4) (HL7 CDA R2, C-CDA 2.1 DSTU, August 2015). The PDF documents **24 C-CDA sections** containing **82 data elements** total. Each element lists an XPATH/entry path and, where applicable, a code system OID and name.

This is a standard C-CDA clinical summary — not a native data model export. The sections and elements map directly to the C-CDA 2.1 specification with no vendor-specific extensions documented.

### Non-CCD data (PDF exports)

Six additional categories are exported as PDF files, described in a single page (page 11) of the documentation with one sentence each and **zero field-level detail**:

| Category | Format | Documentation Detail |
|---|---|---|
| Patient Demographic/Insurance | PDF | "comprehensive view of demographics and insurance details" |
| Advance Directive | PDF | "comprehensive view of Advance Directive" |
| Appointments | PDF | "comprehensive view of appointments" |
| Provider-to-Patient Messages | PDF | "comprehensive view of messages" |
| Billing Data (Claim) | PDF | "comprehensive view of billing data (CPT, ICD, Modifier)" |
| Documents | PDF | "signed progress notes, available lab results, radiology reports, and any other scanned or uploaded document" |

The billing data mention of "CPT, ICD, Modifier" is the only hint at field-level content for any of these categories.

### Vendor's own content organization

The PDF organizes content into two groups: C-CDA clinical data and non-CCD supplementary data. Below are the C-CDA sections:

| Section | Data Elements | Code Systems | Category |
|---|---|---|---|
| Patient Demographics/Information | 6 | AdministrativeGender, Race & Ethnicity CDC | Clinical (C-CDA) |
| Provider's name and office contact | 3 | — | Clinical (C-CDA) |
| Date and Location of visit | 2 | — | Clinical (C-CDA) |
| Chief Complaint and Reason for visit | 1 | — | Clinical (C-CDA) |
| Encounters | 5 | CPT, SNOMED, ICD10 | Clinical (C-CDA) |
| Immunizations | 9 | CVX, CPT-4, NCI, SNOMED | Clinical (C-CDA) |
| Instructions | 1 | SNOMED | Clinical (C-CDA) |
| Treatment Plan | 2 | LOINC | Clinical (C-CDA) |
| Social History | 3 | LOINC, SNOMED | Clinical (C-CDA) |
| Problems | 3 | SNOMED, ICD10 | Clinical (C-CDA) |
| Medications | 5 | RxNorm, NDC | Clinical (C-CDA) |
| Medication Allergies | 4 | RxNorm, SNOMED | Clinical (C-CDA) |
| Laboratory Tests | 4 | LOINC | Clinical (C-CDA) |
| Laboratory Information | 5 | — | Clinical (C-CDA) |
| Laboratory value(s)/result(s) | 5 | LOINC | Clinical (C-CDA) |
| Vitals | 2 | LOINC | Clinical (C-CDA) |
| Goal | 3 | — | Clinical (C-CDA) |
| Procedures | 2 | CPT-4, SNOMED, HCPCS | Clinical (C-CDA) |
| Care team member(s) | 3 | — | Clinical (C-CDA) |
| Reason for Referral | 1 | SNOMED | Clinical (C-CDA) |
| Medical Equipment | 2 | SNOMED | Clinical (C-CDA) |
| Mental Status | 4 | SNOMED | Clinical (C-CDA) |
| Functional Status | 4 | SNOMED | Clinical (C-CDA) |
| Health Concern | 3 | SNOMED | Clinical (C-CDA) |

**Totals**: 24 C-CDA sections, 82 data elements, 6 non-CCD PDF export categories.

No field descriptions are provided — only element names, XPATHs, and code system references. No relationships, value sets, or sample data are documented.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export has two tiers of documentation quality:

**Tier 1 — C-CDA clinical data (well-structured but standard-only)**: 24 sections covering demographics, encounters, problems, medications, allergies, immunizations, labs, vitals, procedures, care plans, goals, mental/functional status, referrals, medical equipment, health concerns, and social history. This maps directly to the C-CDA 2.1 specification. It is thorough for the standard clinical summary but contains nothing vendor-specific — no custom templates, no specialty-specific data elements, no EHR-internal identifiers.

**Tier 2 — Non-CCD supplementary data (mentioned but undocumented)**: The vendor acknowledges that billing data, appointments, demographics/insurance, advance directives, provider-to-patient messages, and documents exist beyond C-CDA. These are exported as PDFs. However, the documentation is a single sentence per category with no field-level detail. The billing export mentions "CPT, ICD, Modifier" but nothing about charges, payers, claim status, payment amounts, or denial information. The PDF format makes this data essentially non-machine-readable.

**FHIR export (mentioned, not documented)**: The two-sentence FHIR section provides no detail about which resources are included, scope, or content beyond what C-CDA already covers.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA: 6 fields (name, sex, DOB, race, ethnicity, language). PDF: "demographics" (no detail). | C-CDA covers basic USCDI demographics. Address, phone, email, emergency contacts, preferred pharmacy not documented in C-CDA. PDF may contain more but is undocumented. |
| Encounters / visits | ⚠️ Partial | C-CDA: Encounters section (5 elements — code, performer, diagnosis, location, date). | Standard C-CDA encounter summary. No visit-level detail (chief complaint linked to encounter, duration, billing-level detail). |
| Problems / conditions | ✅ Covered | C-CDA: Problems section (problem, status, active date) with SNOMED + ICD10. | Standard C-CDA problem list. |
| Medications / prescriptions | ⚠️ Partial | C-CDA: Medications section (medication, directions, start/end date, status) with RxNorm/NDC. | Covers medication list but not e-prescribing transaction details (pharmacy, fill history, refill requests, controlled substance records) which the product stores via Surescripts. |
| Allergies | ✅ Covered | C-CDA: Medication Allergies (substance, reaction, severity, status) with RxNorm/SNOMED. | Standard allergy documentation. |
| Immunizations | ✅ Covered | C-CDA: Immunizations (9 elements including vaccine, route, site, manufacturer, lot number). | One of the better-documented sections. |
| Vitals | ⚠️ Partial | C-CDA: Vitals (observation, date/time) — only 2 elements. | Minimal — doesn't enumerate specific vital types (BP, HR, temp, weight, height, BMI, etc.) though they'd be coded via LOINC. |
| Lab results | ✅ Covered | C-CDA: Three lab sections (14 elements total) covering test info, lab info, and results with LOINC coding. | Reasonably detailed for C-CDA. |
| Imaging / diagnostic reports | ❌ Not covered | No imaging section in C-CDA. Documents PDF export mentions "radiology reports" but no detail. | Product supports diagnostic imaging ordering (certified for (a)(3) CPOE-DI). Radiology reports may be in the Documents PDF export but are not structured. |
| Procedures | ✅ Covered | C-CDA: Procedures (procedure, date) with CPT-4/SNOMED/HCPCS. | Standard C-CDA procedure list. |
| Clinical notes / documents | ⚠️ Partial | Documents exported as PDFs: "signed progress notes, available lab results, radiology reports, and any other scanned or uploaded document." | Notes are exported but as PDFs — not structured/searchable. No detail on note types, templates, or how specialty-specific charting data (70+ templates) is represented. |
| Care plans / goals | ✅ Covered | C-CDA: Treatment Plan (2 elements), Goal (3 elements), Health Concern (3 elements). | Standard C-CDA care plan sections. |
| Orders / referrals | ⚠️ Partial | C-CDA: Reason for Referral (1 element). Treatment Plan mentions "Future scheduled tests, Referrals to other providers." | Referral reasons are captured but order details (lab orders, imaging orders, order status) are not separately documented. |
| Insurance / coverage | ⚠️ Partial | PDF: "Patient Demographic/Insurance" export — no field-level detail. | Product stores insurance information. Exported as PDF but zero documentation of what fields are included. |
| Claims / billing | ⚠️ Partial | PDF: "Billing Data (Claim)" with mention of "CPT, ICD, Modifier." | Product has full RCM/billing capabilities. PDF export mentions only CPT/ICD/Modifier — no charges, payments, claim status, payer, dates of service, or denial information documented. PDF format is non-machine-readable. |
| Payments | ❌ Not covered | No payment data mentioned in any export. | Product handles payment posting. Not documented in export. |
| Consents / directives | ⚠️ Partial | PDF: "Advance Directive" — one sentence, no detail. | Advance directives mentioned but zero field-level documentation. |
| Patient communications | ⚠️ Partial | PDF: "Provider-to-Patient Messages" — one sentence, no detail. | Product has secure messaging via talkPHR portal. Exported as PDF but zero field-level documentation. |
| Specialty-specific data | ❌ Not covered | No specialty-specific data elements in export documentation. | Product advertises 70+ specialty-specific templates (cardiology, dermatology, pediatrics, etc.). None of this custom clinical data appears in the export — C-CDA contains only standard sections. This is a significant gap. |

## 6. Documentation Quality

**Overall quality: Poor.** The documentation is a 12-page PDF with significant weaknesses:

- **No data dictionary**: There is no entity/table/field-level documentation of the export's data model. The C-CDA section lists XPATHs and code systems but this is just restating the C-CDA standard, not documenting vendor-specific content.

- **No field descriptions**: The 82 C-CDA data elements are listed by name and XPATH only — no descriptions, no value constraints, no examples.

- **No relationships or keys**: No documentation of how exported data relates across components (e.g., how a C-CDA links to a billing PDF for the same encounter).

- **No sample data**: No sample C-CDA, sample PDFs, or example output of any kind.

- **No machine-readable artifacts**: No JSON schemas, no XML schemas beyond the C-CDA standard reference, no FHIR capability statements.

- **Non-CCD data is essentially undocumented**: Six categories totaling six sentences. A developer receiving these PDF exports would have no documentation to work from.

- **FHIR export is mentioned but not documented**: Two sentences state FHIR Bulk Data is supported but provide no information about scope, resources, or content.

**Could a developer build an import from this documentation alone?** For the C-CDA portion, yes — but only because C-CDA is a well-known standard, not because this documentation adds value. For the PDF exports and FHIR export, no — there is insufficient documentation to understand what data is included or how it's structured.

## 7. Overall Assessment

### Classification

**Standard-based projection**

The core of this export is a C-CDA clinical summary — a standard projection of clinical data into the HL7 CDA format. The supplementary PDF exports attempt to address data beyond C-CDA's scope (billing, appointments, messages) but are in a non-machine-readable format (PDF) with essentially zero documentation. The FHIR Bulk Data export is mentioned but not described. There is no evidence of a native data model export.

### Key Findings

1. **The export is fundamentally C-CDA repackaged as (b)(10).** The 5-page table of C-CDA sections (pages 6–10) is the documentation's centerpiece, but it merely restates the C-CDA 2.1 standard. This covers standard clinical summary data but not the vendor's full data model.

2. **Non-CCD data is exported as non-machine-readable PDFs with no documentation.** Billing, appointments, insurance, messages, and documents are exported as PDFs — six categories described in six sentences on a single page (page 11). No field-level detail, no schema, no structure.

3. **Specialty-specific clinical data is entirely absent.** Despite advertising 70+ specialty-specific templates, none of this custom clinical data appears in the export documentation. The C-CDA contains only standard sections.

4. **No sample data or machine-readable schemas exist.** The entire export documentation is a single 12-page Word-to-PDF document. No JSON schemas, no sample exports, no FHIR capability statements.

5. **Billing/RCM data coverage is superficial.** The product offers full revenue cycle management including claim submission, payment posting, and denial management, but the export's billing component is a PDF mentioning only "CPT, ICD, Modifier" — no charges, payments, claim status, or payer details are documented.

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA XML + PDF (supplementary) + FHIR (mentioned, undocumented)
Model type:      Standard projection (C-CDA 2.1)
Entities:        24 C-CDA sections + 6 PDF export categories = 30 total
Fields:          82 (C-CDA data elements only; PDF categories have 0 documented fields)
Descriptions:    0% (element names and XPATHs only, no descriptions)
Sample data:     No
Bulk export:     Yes (C-CDA ZIP by date range + FHIR Bulk Data mentioned)
Domains covered: 7 of 17 applicable domains adequately; 8 partial; 2 not covered
```

### Bottom Line

This is a C-CDA clinical summary repackaged as a (b)(10) export, supplemented by undocumented PDF exports for non-clinical data. A patient or provider would receive a standard clinical summary in XML plus a collection of PDFs with billing, insurance, appointment, and messaging data — but the PDF format renders that data non-machine-readable, and the complete absence of documentation for those components means no one can verify completeness. The single biggest gap is the total absence of the vendor's native data model: 70+ specialty templates, detailed billing/RCM data, e-prescribing records, and practice management data are either missing or buried in undocumented PDFs.
