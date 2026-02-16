# EHI Export Analysis: Streamline Healthcare Solutions

**Product**: SmartCare R6
**Analysis date**: 2026-02-16
**CHPL IDs**: 10987 (15.04.04.2855.Smar.R6.01.1.220915)

## 1. Product Context

SmartCare is a comprehensive, cloud-based (Azure) EHR built exclusively for **behavioral health and human services**. Developed by Streamline Healthcare Solutions (~400 employees, ~$60M revenue), it targets community mental health centers, CCBHCs, substance use disorder treatment providers, foster care/adoption agencies, IDD service providers, and managed behavioral health organizations.

The product is a single integrated platform covering:

- **Clinical care**: Progress notes, treatment plans, assessments, care plans, outcome tracking, "golden thread" documentation (linking presenting problems → diagnoses → treatment goals → interventions → progress notes — a core behavioral health compliance requirement)
- **Inpatient/residential**: Medication administration records, bed management
- **Primary care integration**: Scheduling, orders, flow sheets, referral tracking, ePrescribing via Surescripts
- **Revenue cycle management**: Claims processing (837), remittance (835), denial management, claim scrubbing
- **MCO module**: Provider contract/rate management, electronic claims adjudication, authorization tracking, utilization management, capitated arrangements
- **Specialty services**: IDD, foster care/adoption, substance use disorder
- **Patient portal, telehealth, mobile access, business intelligence**

This product context is critical: SmartCare stores deep behavioral health clinical data (custom assessments, screening tools like PHQ-9/AUDIT/DAST, treatment plans, progress notes), extensive billing/claims data, MCO administration data, and specialty-specific records for IDD, foster care, and SUD populations. A compliant (b)(10) export should cover these domains.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `ehi-export-page.html` (130 KB) | Full HTML of the EHI export documentation page from `streamlinehealthcare.com/electronic-health-information-export/`. Contains all substantive content: ~326 words of prose plus a list of 17 C-CDA section names with links to HL7 specs. | **Primary source** — this is the entirety of the vendor's (b)(10) documentation |
| `ehi-export-page-wp-api.json` (15 KB) | WordPress REST API response for the same page. Confirms publication date (2023-11-16) and last modification (2023-12-05). Contains the same content in cleaner form. | **Useful** — confirmed page dates and provided cleaner HTML for parsing |
| `ehi-export-page-full.png` (363 KB) | Full-page screenshot showing the complete EHI export page. Visually confirms the page fits on a single screen with no hidden content. | **Confirmatory** — verified no content missed by HTML extraction |
| `ehi-export-page-top.png` (215 KB) | Viewport screenshot of the page header area. | **Minimal value** — subset of the full screenshot |

**No downloadable files exist** — no PDFs, no data dictionaries, no sample data, no schemas, no ZIP files. The entire (b)(10) documentation is a single web page. The live URL (verified 2026-02-16) returns identical content to the downloaded artifact.

## 3. Export Mechanics

- **Format**: C-CDA 2.2 (HL7 Consolidated Clinical Document Architecture) — XML-based patient summary documents
- **Mechanism**: UI-based; the page states export is available "without developer assistance." Detailed setup instructions are "available to all Streamline customers in the help desk documentation" (not publicly accessible).
- **Single-patient vs bulk**: Both — the page claims support for "a single patient or a population at any time"
- **Access constraints**: "Limited to system administrators and SmartCare users as permissioned by the Streamline customer's roles and permissions"
- **Fees**: "No additional cost for Streamline customers"

The page explicitly describes the export files as "CCDAs or patient summary documents" — the vendor uses the term "patient summary" themselves, which accurately describes the scope of C-CDA but is a narrow interpretation of "all electronic health information."

## 4. Export Content: What's In It

The export consists of C-CDA 2.2 documents containing 17 standard sections. There is **no data dictionary**, **no field-level documentation**, **no sample data**, and **no schema** beyond links to the generic HL7 C-CDA 2.2 StructureDefinitions.

The vendor provides zero information about:
- What specific data elements populate each section
- What code systems are used (though the product supports SNOMED CT, LOINC, RxNorm, ICD-10-CM per their marketing materials)
- Whether any vendor-specific extensions or custom sections are included
- How SmartCare-internal data maps to C-CDA structures

### Vendor's own content organization

The vendor organizes the export into 17 C-CDA sections, categorized by entry requirement:

| C-CDA Section | Entry Requirement | HL7 OID |
|---|---|---|
| Allergies and Intolerances Section | Entries required | 2.16.840.1.113883.10.20.22.2.6.1 |
| Medications Section | Entries required | 2.16.840.1.113883.10.20.22.2.1.1 |
| Problem Section | Entries required | 2.16.840.1.113883.10.20.22.2.5.1 |
| Procedures Section | Entries required | 2.16.840.1.113883.10.20.22.2.7.1 |
| Results Section | Entries required | 2.16.840.1.113883.10.20.22.2.3.1 |
| Immunizations Section | Entries required | 2.16.840.1.113883.10.20.22.2.2.1 |
| Vital Signs Section | Entries required | 2.16.840.1.113883.10.20.22.2.4.1 |
| Advance Directives Section | Entries optional | 2.16.840.1.113883.10.20.22.2.21 |
| Encounters Section | Entries optional | 2.16.840.1.113883.10.20.22.2.22 |
| Family History Section | Not specified | 2.16.840.1.113883.10.20.22.2.15 |
| Functional Status Section | Not specified | 2.16.840.1.113883.10.20.22.2.14 |
| Medical Equipment Section | Not specified | 2.16.840.1.113883.10.20.22.2.23 |
| Payers Section | Not specified | 2.16.840.1.113883.10.20.22.2.18 |
| Plan of Treatment Section | Not specified | 2.16.840.1.113883.10.20.22.2.10 |
| Social History Section | Not specified | 2.16.840.1.113883.10.20.22.2.17 |
| Mental Status Section | Not specified | 2.16.840.1.113883.10.20.22.2.56 |
| Nutrition Section | Not specified | 2.16.840.1.113883.10.20.22.2.57 |

**Summary**: 17 sections total — 7 with entries required, 2 with entries optional, 8 with unspecified entry requirements. All links point to the generic HL7 C-CDA 2.2 specification on `build.fhir.org`; no vendor-specific documentation, templates, or implementation guides are provided.

These 17 sections are the standard sections of a C-CDA Continuity of Care Document (CCD). This is not a custom or extended export — it is the standard clinical summary document format.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export covers exactly what a standard C-CDA patient summary covers: a clinical snapshot suitable for care transitions between providers. The 17 sections map to standard clinical summary data — allergies, medications, problems, procedures, lab results, immunizations, vitals, encounters, payers, social history, advance directives, functional status, mental status, nutrition, family history, plan of treatment, and medical equipment.

The vendor provides **no categories of their own** — they simply list the C-CDA section names. There is no indication of vendor-specific extensions, additional sections, or supplementary data beyond the standard C-CDA format.

Notably, the Mental Status Section and Nutrition Section (both added in C-CDA 2.1) are included, which could theoretically carry some behavioral health-relevant data. However, without sample data or field-level documentation, there is no way to assess whether these sections are meaningfully populated with SmartCare's behavioral health data or are simply empty/minimal.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA header includes patient demographics, but no dedicated section with full demographic detail | C-CDA carries basic demographics (name, DOB, gender, address) in the header; likely misses SmartCare's full enrollment, program, and contact data |
| Encounters / visits | ⚠️ Partial | Encounters Section (entries optional) | Present but entries are optional; depth of encounter data (visit types, durations, behavioral health service codes) unknown |
| Problems / conditions / diagnoses | ✅ Covered | Problem Section (entries required) | Standard C-CDA coverage; whether behavioral health diagnoses are fully represented is unknown |
| Medications / prescriptions | ✅ Covered | Medications Section (entries required) | Standard C-CDA coverage; SmartCare has Surescripts ePrescribing integration — prescription history depth unclear |
| Allergies | ✅ Covered | Allergies and Intolerances Section (entries required) | Standard C-CDA coverage |
| Immunizations | ✅ Covered | Immunizations Section (entries required) | Standard C-CDA coverage |
| Vitals | ✅ Covered | Vital Signs Section (entries required) | Standard C-CDA coverage |
| Lab results | ✅ Covered | Results Section (entries required) | Standard C-CDA coverage |
| Imaging / diagnostic reports | ❌ Not covered | No imaging or diagnostic report section in the 17 listed sections | SmartCare does not appear to be an imaging-focused product, but if diagnostic reports exist, they are not exported; likely **N/A** for most deployments |
| Procedures | ✅ Covered | Procedures Section (entries required) | Standard C-CDA coverage |
| Clinical notes / documents | ❌ Not covered | No Notes Section in the 17 listed sections | **Major gap.** SmartCare's core value proposition is clinical documentation — progress notes, H&P, treatment plan narratives, behavioral health session notes. None of this appears in the export. C-CDA can carry clinical notes, but no Notes Section is listed. |
| Care plans / goals | ⚠️ Partial | Plan of Treatment Section | Only "plan of treatment" — the vendor's rich treatment planning with golden thread documentation, outcome tracking, and care plan features are unlikely to be fully represented in this single C-CDA section |
| Orders / referrals | ❌ Not covered | No orders or referrals section listed | SmartCare supports order entry and referral tracking; not represented in the export |
| Insurance / coverage | ⚠️ Partial | Payers Section | C-CDA Payers Section carries basic insurance information; unlikely to capture SmartCare's full enrollment, authorization, and managed care data |
| Claims / billing | ❌ Not covered | No billing/claims entities in export | **Major gap.** SmartCare has a full revenue cycle management module with claims (837), remittance (835), denial management — none exportable |
| Payments | ❌ Not covered | No payment data in export | SmartCare processes payments and tracks reimbursements; not exported |
| Consents / directives | ⚠️ Partial | Advance Directives Section (entries optional) | Only advance directives; broader consent management not represented |
| Patient communications / portal messages | ❌ Not covered | No portal/communication section | SmartCare has a patient portal with secure messaging; not exported |
| Specialty: Behavioral health assessments | ❌ Not covered | No section for behavioral health screening tools, assessments, or custom forms | **Critical gap.** This is a behavioral health EHR; PHQ-9, AUDIT, DAST, custom intake forms, screening instruments — the core clinical data for this product type — have no C-CDA representation |
| Specialty: Substance use disorder | ❌ Not covered | No SUD-specific data in export | SmartCare serves SUD treatment providers; treatment records, 42 CFR Part 2 data not exported |
| Specialty: Foster care / adoption | ❌ Not covered | No foster care data in export | SmartCare serves foster care agencies; case records not exported |
| Specialty: IDD services | ❌ Not covered | No IDD service data in export | SmartCare serves IDD providers; service plans, habilitation records not exported |
| Specialty: MCO administration | ❌ Not covered | No MCO data in export | SmartCare has an entire MCO module (provider contracts, authorization tracking, utilization management); none exported |

**Summary**: Of 22 assessed domains (including 5 specialty domains relevant to this product), 7 are covered via standard C-CDA sections, 4 have partial coverage, and 11 are not covered at all. The missing domains include the product's most distinctive and data-rich capabilities: behavioral health assessments, treatment plans with golden thread documentation, billing/claims, MCO administration, SUD records, foster care records, and IDD service data.

## 6. Documentation Quality

The documentation quality is **extremely poor**:

- **Total substantive content**: ~326 words on a single web page (published 2023-11-16, last modified 2023-12-05)
- **Data dictionary**: None
- **Field-level documentation**: None — not even a list of data elements within each C-CDA section
- **Schema/profile documentation**: None — only links to the generic HL7 C-CDA 2.2 StructureDefinitions, which are the external standard, not vendor-specific documentation
- **Sample data**: None
- **Machine-readable artifacts**: None (no schemas, no example files, no downloadable content of any kind)
- **Export instructions**: Referenced but locked behind customer help desk ("available to all Streamline customers in the help desk documentation")
- **Screenshots**: None

**Could a developer build an import from this documentation?** No. A developer would know only that the export is "a C-CDA" with 17 possible sections. They would have no information about SmartCare-specific OIDs, vocabulary choices, template usage, extension patterns, or data mapping decisions. They would need to obtain an actual export file and reverse-engineer it.

The documentation essentially says: "We export C-CDA files. Here are the standard C-CDA section definitions." This is the equivalent of saying "we export JSON" and linking to json.org.

## 7. Overall Assessment

### Classification

**Standard-based projection** — The EHI export is a standard C-CDA 2.2 patient summary document with no evidence of vendor-specific extensions or additional data beyond what the C-CDA standard defines. This is a clinical summary format being presented as a comprehensive EHI export.

### Key Findings

1. **The export is a standard C-CDA clinical summary, not a comprehensive EHI export.** The vendor explicitly describes the files as "CCDAs or patient summary documents" — a patient summary covers a narrow slice of what this behavioral health EHR stores. The 17 listed sections are the standard CCD sections with no vendor extensions. (`ehi-export-page-wp-api.json`, content field)

2. **The product's most distinctive data is entirely absent from the export.** SmartCare is purpose-built for behavioral health — its core value is treatment plans, progress notes, custom assessments (PHQ-9, AUDIT, etc.), golden thread documentation, SUD records, foster care tracking, and IDD service plans. None of these have any representation in a C-CDA document. The export omits the very data that differentiates this product from a general-purpose EHR.

3. **Billing and MCO data is completely missing.** SmartCare includes full revenue cycle management (837/835 claims processing, denial management) and an MCO module (provider contracts, authorization tracking, utilization management, capitated arrangements). None of this is in the C-CDA export.

4. **Documentation is near-empty.** The entire (b)(10) documentation is ~326 words with zero downloadable artifacts, no data dictionary, no sample data, no schema, and no field-level documentation. Setup instructions are locked behind a customer help desk login.

5. **The export appears to be a repackaging of existing clinical summary capability.** C-CDA generation is a standard EHR function used for care transitions (certified under criterion (b)(1)). Using the same C-CDA output as the (b)(10) EHI export adds no incremental data access — patients and providers get no data beyond what was already available through standard clinical document exchange.

### Summary Stats

```
Classification:  Standard-based projection (C-CDA repackaging)
Export format:   C-CDA 2.2 (XML)
Model type:      Standard projection (not native database)
Entities:        17 C-CDA sections (standard, no vendor extensions)
Fields:          N/A (no field-level documentation provided)
Descriptions:    N/A (no data dictionary)
Sample data:     No
Bulk export:     Yes (single-patient and population claimed)
Domains covered: 7 of 22 applicable domains (with 4 additional partial)
```

### Bottom Line

SmartCare's EHI export is a textbook example of C-CDA repackaging: the vendor takes its existing clinical summary document — already available for care transitions — and labels it as the (b)(10) EHI export. For a **behavioral health** EHR, this is particularly inadequate because the vast majority of the product's valuable data (behavioral health assessments, treatment plans, progress notes, billing, MCO administration, SUD/foster care/IDD specialty records) has no representation in a C-CDA document. A patient requesting their complete health information from SmartCare would receive a generic clinical summary while their behavioral health treatment history, billing records, and specialty-specific data remain inaccessible.
