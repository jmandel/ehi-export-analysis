# EHI Export Analysis: Streamline Healthcare Solutions

**Product**: SmartCare R6
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2855.Smar.R6.01.1.220915 (CHPL ID 10987)

## 1. Product Context

SmartCare is a cloud-based (Azure), single-platform EHR built exclusively for **behavioral health and human services**. Its target market includes community mental health centers (CMHCs), certified community behavioral health clinics (CCBHCs), substance use disorder (SUD) treatment providers, foster care/adoption agencies, intellectual/developmental disabilities (IDD) service providers, and managed behavioral health organizations (MCOs).

The product stores data across these domains:

- **Clinical**: Progress notes, treatment plans, assessments, diagnoses, problem lists, medications (with ePrescribing via Surescripts), allergies, immunizations, vital signs, lab orders/results, and the behavioral health "golden thread" (presenting problems → diagnoses → treatment goals → interventions → progress notes)
- **Behavioral health specialty**: Custom screening tools (PHQ-9, AUDIT, DAST, etc.), substance use disorder treatment records, mental status assessments, functional status tracking
- **Billing/revenue cycle**: Claims (837), remittance advice (835), denial management, reimbursement tracking
- **MCO module**: Provider contracts, credentialing, authorization tracking, utilization management, capitation management, claims adjudication
- **Case management**: Client tracking, document due dates, compliance deadlines, program enrollment/discharge
- **Specialty populations**: Foster care/adoption records, IDD service plans, inpatient/residential (bed management, MAR)
- **Patient portal**: Secure messaging, patient-facing access
- **Telehealth**: Remote service delivery

This breadth is critical context: a genuine (b)(10) export for SmartCare should cover behavioral health clinical data, billing, case management, and specialty populations — not just a standard clinical summary.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/ehi-export-page.html` (130 KB) | Full HTML of the EHI export documentation page from `streamlinehealthcare.com/electronic-health-information-export/`. Contains the entire public-facing export documentation. | **Primary source** |
| `downloads/ehi-export-page-wp-api.json` (15 KB) | WordPress REST API response for the same page. Provides cleaner content and metadata (published 2023-11-16, modified 2023-12-05). | **Useful for parsing** — same content as HTML but without theme markup |
| `downloads/ehi-export-page-full.png` (363 KB) | Full-page screenshot of the documentation page. | **Confirmatory** — visually confirms the page content matches parsed HTML |
| `downloads/ehi-export-page-top.png` (215 KB) | Viewport screenshot of the top of the page. | **Low value** — subset of the full screenshot |

**Notable absence**: There are no downloadable artifacts — no PDFs, no data dictionaries, no sample export files, no schemas, no ZIP archives. The entire documentation is a single web page with approximately 250 words of substantive content and 17 hyperlinks to external HL7 specifications.

## 3. Export Mechanics

- **Format**: C-CDA 2.2 (HL7 Consolidated Clinical Document Architecture) — XML-based patient summary documents
- **Mechanism**: UI-driven export within SmartCare, available to system administrators and permissioned users. Setup instructions are described as available "in the help desk documentation" (customer-only, not public).
- **Single-patient**: Yes — documentation states "export for a single patient"
- **Bulk capability**: Yes — documentation states "or a population at any time"
- **Access constraints**: Limited to system administrators and permissioned SmartCare users
- **Fees**: "No additional cost for Streamline customers"
- **Developer assistance**: Not required ("without developer assistance")

The documentation also states: "EHI Export functionality allows for SmartCare to let patients download their EHI at any time independently." This suggests patients can self-serve through the portal.

## 4. Export Content: What's In It

### No vendor-specific data dictionary

The export documentation provides **zero vendor-specific field-level documentation**. There is no data dictionary, no field list, no type definitions, no value sets, no relationship documentation, no sample data. The entire "Data Included" section consists of 17 bullet-pointed C-CDA section names, each linking to the generic HL7 C-CDA 2.2 StructureDefinition on `build.fhir.org`.

This means the export content is defined entirely by reference to the C-CDA 2.2 standard — there is no indication of what SmartCare-specific data maps into each section, what code systems are used, or whether any vendor extensions exist.

### Vendor's own content organization

The vendor lists 17 C-CDA sections organized by entry constraint:

| C-CDA Section | Entry Constraint | HL7 OID | Domain |
|---|---|---|---|
| Allergies and Intolerances Section | entries required | 2.16.840.1.113883.10.20.22.2.6.1 | Allergies |
| Medications Section | entries required | 2.16.840.1.113883.10.20.22.2.1.1 | Medications |
| Problem Section | entries required | 2.16.840.1.113883.10.20.22.2.5.1 | Problems |
| Procedures Section | entries required | 2.16.840.1.113883.10.20.22.2.7.1 | Procedures |
| Results Section | entries required | 2.16.840.1.113883.10.20.22.2.3.1 | Lab results |
| Immunizations Section | entries required | 2.16.840.1.113883.10.20.22.2.2.1 | Immunizations |
| Vital Signs Section | entries required | 2.16.840.1.113883.10.20.22.2.4.1 | Vitals |
| Advance Directives Section | entries optional | 2.16.840.1.113883.10.20.22.2.21 | Consents/directives |
| Encounters Section | entries optional | 2.16.840.1.113883.10.20.22.2.22 | Encounters |
| Family History Section | — | 2.16.840.1.113883.10.20.22.2.15 | Family history |
| Functional Status Section | — | 2.16.840.1.113883.10.20.22.2.14 | Health status |
| Medical Equipment Section | — | 2.16.840.1.113883.10.20.22.2.23 | Medical devices |
| Payers Section | — | 2.16.840.1.113883.10.20.22.2.18 | Insurance/coverage |
| Plan of Treatment Section | — | 2.16.840.1.113883.10.20.22.2.10 | Care plans |
| Social History Section | — | 2.16.840.1.113883.10.20.22.2.17 | Social history |
| Mental Status Section | — | 2.16.840.1.113883.10.20.22.2.56 | Health status |
| Nutrition Section | — | 2.16.840.1.113883.10.20.22.2.57 | Nutrition |

**Total sections**: 17 (7 entries required, 2 entries optional, 8 unconstrained)
**Vendor-documented fields**: 0
**Fields per C-CDA 2.2 spec**: ~82 standard fields across all 17 sections (but no vendor-specific mapping provided)

These 17 sections are the standard sections found in a C-CDA Continuity of Care Document (CCD) — this is essentially the same clinical summary available through any C-CDA exchange, including standard transitions of care documents.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export is a standard C-CDA patient summary. It covers the same clinical domains as any Continuity of Care Document: allergies, medications, problems, procedures, lab results, immunizations, vital signs, encounters, payers, advance directives, family history, social history, functional/mental status, plan of treatment, medical equipment, and nutrition.

There is **nothing behavioral-health-specific** in this export. For a product whose entire value proposition is behavioral health and human services, the export contains no representation of:
- Treatment plans with the "golden thread" linking
- Behavioral health progress notes
- Screening tools and assessments (PHQ-9, AUDIT, etc.)
- Substance use disorder treatment records
- Case management and client tracking
- Foster care, adoption, or IDD data
- Claims, billing, or revenue cycle data
- MCO module data

The Payers Section provides basic insurance coverage information but not billing/claims data.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA header contains patient demographics; Social History Section covers some social determinants | Standard C-CDA demographics only; no specialty intake data |
| Encounters / visits | ⚠️ Partial | Encounters Section (entries optional) | Basic encounter data only; no behavioral health session details, group therapy, telehealth sessions |
| Problems / conditions / diagnoses | ⚠️ Partial | Problem Section (entries required) | Standard problem list; likely misses behavioral health diagnostic detail, severity tracking, treatment response |
| Medications / prescriptions | ✅ Covered | Medications Section (entries required) | Reasonable for C-CDA; product has ePrescribing via Surescripts |
| Allergies | ✅ Covered | Allergies and Intolerances Section (entries required) | Standard coverage |
| Immunizations | ✅ Covered | Immunizations Section (entries required) | Standard coverage |
| Vitals | ✅ Covered | Vital Signs Section (entries required) | Standard coverage |
| Lab results | ✅ Covered | Results Section (entries required) | Standard coverage |
| Imaging / diagnostic reports | ❌ Not covered | No imaging section in C-CDA export | Product may store some diagnostic reports; unclear if significant for behavioral health |
| Procedures | ✅ Covered | Procedures Section (entries required) | Standard coverage |
| Clinical notes / documents | ❌ Not covered | No clinical notes section in C-CDA export | **Major gap** — progress notes are core to behavioral health; the "golden thread" documentation is the product's central clinical artifact |
| Care plans / goals | ⚠️ Partial | Plan of Treatment Section | Generic plan of treatment; unlikely to capture behavioral health treatment plans with linked goals, interventions, and outcomes |
| Orders / referrals | ❌ Not covered | No orders or referrals section | Product supports order entry and referral tracking |
| Insurance / coverage | ⚠️ Partial | Payers Section | Basic payer/coverage info only; no claims or billing detail |
| Claims / billing | ❌ Not covered | No billing entities | **Major gap** — product has full revenue cycle management (837/835 claims) |
| Payments | ❌ Not covered | No payment entities | Product manages reimbursement and payment processing |
| Consents / directives | ⚠️ Partial | Advance Directives Section (entries optional) | Standard advance directives; may not cover behavioral health consent forms |
| Patient communications / portal messages | ❌ Not covered | No communication entities | Product has patient portal with secure messaging |
| Behavioral health (specialty) | ❌ Not covered | No behavioral health-specific sections | **Critical gap** — this is the product's primary domain; assessments, screening tools, SUD records, case management, golden thread documentation all absent |
| Foster care / IDD (specialty) | ❌ Not covered | No specialty population sections | Product has dedicated modules for foster care/adoption and IDD services |
| MCO management (specialty) | ❌ Not covered | No MCO entities | Product has full MCO module with authorization tracking, utilization management, credentialing |

**Summary**: 6 of 19 applicable domains are covered (standard clinical data only), 5 partially covered, 8 not covered at all. The 8 uncovered domains include the product's core behavioral health functionality, all billing/financial data, and all specialty population data.

## 6. Documentation Quality

The documentation quality is **extremely poor**:

- **No data dictionary**: Zero field-level documentation. The only content is a list of 17 C-CDA section names linking to external HL7 specifications.
- **No vendor-specific mapping**: No indication of how SmartCare's internal data model maps to C-CDA sections. No code systems identified. No vendor extensions documented.
- **No sample data**: No example C-CDA files provided.
- **No machine-readable artifacts**: No schemas, templates, or implementation guides beyond generic C-CDA 2.2 references.
- **No export instructions**: Setup documentation is customer-only ("available to all Streamline customers in the help desk documentation").
- **No screenshots**: The page describes the capability abstractly without showing the export interface.
- **Could a developer build an import?** Not from this documentation. A developer would know the output is C-CDA 2.2 XML, but nothing about SmartCare's specific data mapping, OID assignments, vocabulary choices, or what data actually populates each section. They would have to reverse-engineer the export from sample files (which are not provided).

The page was published 2023-11-16 and last modified 2023-12-05 — it has not been updated in over two years.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub**

SmartCare is a comprehensive behavioral health EHR with billing, MCO management, case management, specialty population tracking (foster care, IDD), and dozens of custom clinical forms and assessments. The C-CDA export covers only standard clinical summary data — the same data available through any C-CDA exchange. It contains no behavioral health-specific content whatsoever, which is particularly damning for a product whose entire purpose is behavioral health. The export covers perhaps 10–15% of what SmartCare stores about patients. The documentation is a single web page with ~250 words.

**Axis 2 — Export approach: Repackaged existing export**

The export is explicitly described as "CCDAs or patient summary documents" — the same C-CDA documents used for transitions of care and clinical exchange. The 17 sections listed are the standard CCD sections. Every link goes to the generic HL7 C-CDA 2.2 specification. There is no vendor-specific data dictionary, no mapping beyond standard C-CDA templates, no coverage of billing, behavioral health, or operational data. This is the vendor's existing C-CDA clinical exchange capability relabeled as (b)(10). The documentation even references "the ONC 2015 Edition certification for Meaningful Use" — framing from the prior regulatory era, not the Cures Act.

### Key Findings

1. **The export is a standard C-CDA patient summary with zero behavioral health content.** For a product built exclusively for behavioral health and human services, the export contains no representation of treatment plans, progress notes, screening tools, assessments, case management, SUD records, or the "golden thread" documentation that is SmartCare's core clinical artifact. This is the single most significant gap.

2. **No data dictionary or vendor-specific documentation exists.** The entire documentation is 17 hyperlinks to external HL7 C-CDA 2.2 specifications. There are zero vendor-documented fields, zero sample files, and zero machine-readable artifacts. (Source: `downloads/ehi-export-page-wp-api.json`)

3. **Billing, MCO, and specialty population data are entirely absent.** SmartCare has full revenue cycle management (837/835), an MCO module (authorization tracking, utilization management, claims adjudication), and specialty modules for foster care, adoption, and IDD — none of which appear in the export.

4. **The documentation page has been static since December 2023.** Published 2023-11-16, last modified 2023-12-05 (per WordPress API metadata). No updates in over two years suggest minimal ongoing investment.

5. **The prior agent's report notes zero customer adoption during Real World Testing (2025 RWT results).** While I did not independently verify this claim (the RWT PDF was not in the downloads), this is consistent with the minimal documentation and repackaged export approach.

### Summary Stats

```
Coverage:        Minimal/stub
Approach:        Repackaged existing export
Export format:   C-CDA 2.2 (XML)
Entities:        17 C-CDA sections (no vendor-specific entities)
Fields:          0 vendor-documented (sections reference generic HL7 spec)
Descriptions:    N/A (no data dictionary)
Sample data:     No
Bulk export:     Yes (claimed)
Domains covered: 6 of 19 applicable domains (standard clinical only)
```

### Bottom Line

SmartCare's EHI export is a standard C-CDA clinical summary relabeled as (b)(10) — it covers basic clinical data (allergies, meds, problems, vitals, labs) but contains nothing specific to behavioral health, which is the product's entire purpose. A patient receiving this export would get a generic clinical summary while their treatment plans, progress notes, behavioral health assessments, billing records, and case management data remain unexported. The biggest gap is the complete absence of behavioral health clinical content in a product that exists solely to serve behavioral health organizations.
