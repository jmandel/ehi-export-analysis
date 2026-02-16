# EHI Export Analysis: Streamline Healthcare Solutions

**Product**: SmartCare R6
**Analysis date**: 2026-02-15
**CHPL IDs**: 15.04.04.2855.Smar.R6.01.1.220915 (CHPL ID 10987)

## 1. Product Context

SmartCare is a comprehensive, cloud-based (Azure) EHR built exclusively for **behavioral health and human services**. It serves community mental health centers, CCBHCs, substance use disorder treatment providers, foster care/adoption agencies, IDD service providers, and managed behavioral health organizations. The product is a single integrated platform covering:

- **Clinical care management**: Progress notes, treatment plans, assessments, care plans, the "golden thread" linking presenting problems → diagnoses → goals → interventions → progress notes — the core clinical workflow for behavioral health.
- **Behavioral health specialty data**: Custom screening tools (PHQ-9, AUDIT, etc.), substance use disorder records, IDD habilitation records, foster care/adoption tracking.
- **Revenue cycle management**: Claims processing (837), denial management, reimbursement tracking, billing.
- **MCO module**: Provider contracts, credentialing, claims adjudication, authorization tracking, utilization management, capitation management, 835 remittance advice.
- **Inpatient/residential**: Bed management, medication administration records.
- **ePrescribing**: Surescripts integration, prescription management.
- **Patient portal**: Secure messaging, patient engagement.
- **Primary care integration**: Orders, lab results, flow sheets, referral tracking.
- **Business intelligence**: Data warehouse, reporting dashboards.

This is relevant because the (b)(10) requirement demands export of **all** EHI the product stores — not just standard clinical summary data. For a behavioral health EHR, the specialty-specific clinical data (treatment plans, assessments, screening tools, golden thread documentation) and billing data represent the majority of what the product stores about patients.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/ehi-export-page.html` (130,589 bytes) | Full HTML of the EHI export documentation page from `streamlinehealthcare.com/electronic-health-information-export/` | **Primary artifact** — contains the entirety of vendor's EHI export documentation |
| `downloads/ehi-export-page-wp-api.json` (15,215 bytes) | WordPress REST API JSON for the page; cleaner content, confirms publish date (2023-11-16) and last modified (2023-12-05) | Useful for structured parsing; confirms page metadata |
| `downloads/ehi-export-page-full.png` (363,450 bytes) | Full-page screenshot of EHI export page | Visual confirmation of page layout |
| `downloads/ehi-export-page-top.png` (215,019 bytes) | Viewport screenshot of page top | Minor — shows page header |
| 2025 RWT Results PDF (from live site, 21 pages) | Real World Testing results (Jan 2026) covering 90-day period ending Aug 2025 | **Critical** — confirms 0 customer usage of EHI export |
| 2025 RWT Test Plan PDF (from live site) | Test plan for 2025 RWT cycle | Confirms b(10) test methodology |
| 2024 RWT Results PDF (from live site) | 2024 Real World Testing results | Notes: b(10) not measured in 2024; b(6) Data Export also showed 0 usage |
| Live EHI export page (verified 2026-02-15) | Current state of the EHI export documentation page | Confirmed identical to downloaded version — no updates since Dec 2023 |

**Most informative**: `ehi-export-page-wp-api.json` (the actual export documentation) and the 2025 RWT Results PDF. **Least informative**: The screenshots, which add nothing beyond what's in the HTML/JSON.

There are **no downloadable files** — no data dictionary, no sample exports, no schema documentation, no PDF documentation. The entire EHI export documentation consists of a single web page with 326 words of substantive content.

## 3. Export Mechanics

- **Format**: C-CDA 2.2 (Consolidated Clinical Document Architecture) — XML-based patient summary documents
- **Mechanism**: UI-based ("without developer assistance"); detailed instructions available only through customer help desk documentation (not public)
- **Single-patient**: Yes — claimed on the documentation page
- **Bulk/population export**: Yes — claimed on the documentation page ("export of all electronic health information of the patient population")
- **Access constraints**: Limited to system administrators and permissioned SmartCare users
- **Fees**: No additional cost for Streamline customers
- **Actual usage**: Per 2025 RWT Results, **0 export files were created** across all customer environments during the 90-day evaluation period. The report states: "While the functionality has been fully implemented, tested, and successfully demonstrated, there has been no customer adoption to date." The 2024 RWT (which measured b(6) Data Export, a related criterion) also reported 0 usage.

## 4. Export Content: What's In It

The export produces C-CDA 2.2 documents containing **17 standard C-CDA sections**. The documentation lists these sections by name with links to the generic HL7 C-CDA 2.2 StructureDefinitions on `build.fhir.org`. There is **no vendor-specific field-level documentation** — no data dictionary, no field descriptions, no type information, no value sets, no relationships, no sample data.

### Vendor's own content organization

The vendor organizes the 17 sections into three groups:

**Entries Required (7 sections):**

| Section | Fields | Described | Types | Category |
|---|---|---|---|---|
| Allergies and Intolerances Section | N/A | N/A | N/A | Entries Required |
| Medications Section | N/A | N/A | N/A | Entries Required |
| Problem Section | N/A | N/A | N/A | Entries Required |
| Procedures Section | N/A | N/A | N/A | Entries Required |
| Results Section | N/A | N/A | N/A | Entries Required |
| Immunizations Section | N/A | N/A | N/A | Entries Required |
| Vital Signs Section | N/A | N/A | N/A | Entries Required |

**Entries Optional (2 sections):**

| Section | Fields | Described | Types | Category |
|---|---|---|---|---|
| Advance Directives Section | N/A | N/A | N/A | Entries Optional |
| Encounters Section | N/A | N/A | N/A | Entries Optional |

**Other Sections (8 sections):**

| Section | Fields | Described | Types | Category |
|---|---|---|---|---|
| Family History Section | N/A | N/A | N/A | Other |
| Functional Status Section | N/A | N/A | N/A | Other |
| Medical Equipment Section | N/A | N/A | N/A | Other |
| Payers Section | N/A | N/A | N/A | Other |
| Plan of Treatment Section | N/A | N/A | N/A | Other |
| Social History Section | N/A | N/A | N/A | Other |
| Mental Status Section | N/A | N/A | N/A | Other |
| Nutrition Section | N/A | N/A | N/A | Other |

All field counts are "N/A" because the vendor provides **zero field-level documentation**. The only documentation is the section names and links to the generic HL7 C-CDA 2.2 specification. There is no indication of what SmartCare-specific data maps into each section, what code systems are used, what extensions (if any) exist, or what the actual export looks like.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's documentation describes a standard C-CDA patient summary document. The 17 sections are the standard sections from the HL7 C-CDA 2.2 specification — there is nothing specific to SmartCare, behavioral health, or any specialty domain. This is the same set of sections that would appear in a Continuity of Care Document (CCD) generated for clinical data exchange between providers.

The documentation makes no mention of:
- Any behavioral health-specific content
- Treatment plans or progress notes beyond what's in standard C-CDA
- Custom assessments or screening tools
- Billing or claims data
- MCO module data
- Substance use disorder-specific data
- Foster care or IDD data
- Any vendor extensions to the C-CDA standard

The "Mental Status Section" and "Functional Status Section" are standard C-CDA sections, not behavioral health-specific extensions. They are generic sections defined by HL7, not SmartCare customizations.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA header contains patient demographics per standard, but no section-level detail documented | C-CDA includes basic demographics in the header; depth unknown without sample data |
| Encounters / visits | ⚠️ Partial | Encounters Section (entries optional) | Marked as "entries optional" — unclear what encounter detail is included |
| Problems / conditions / diagnoses | ✅ Covered | Problem Section (entries required) | Standard C-CDA coverage; behavioral health diagnoses may or may not be fully represented |
| Medications / prescriptions | ✅ Covered | Medications Section (entries required) | Standard coverage; ePrescribing history depth unknown |
| Allergies | ✅ Covered | Allergies and Intolerances Section (entries required) | Standard C-CDA coverage |
| Immunizations | ✅ Covered | Immunizations Section (entries required) | Standard C-CDA coverage |
| Vitals | ✅ Covered | Vital Signs Section (entries required) | Standard C-CDA coverage |
| Lab results | ✅ Covered | Results Section (entries required) | Standard C-CDA coverage |
| Imaging / diagnostic reports | ❌ Not covered | No imaging-specific section | Product has primary care integration with order entry; imaging results gap if product stores them |
| Procedures | ✅ Covered | Procedures Section (entries required) | Standard C-CDA coverage |
| Clinical notes / documents | ❌ Not covered | No notes section in the export | **Major gap**: SmartCare's core value is clinical documentation — progress notes, treatment plans, assessments, the "golden thread" documentation. None of this appears in the export. |
| Care plans / goals | ⚠️ Partial | Plan of Treatment Section | Standard C-CDA section; unlikely to capture SmartCare's structured treatment plans |
| Orders / referrals | ❌ Not covered | No orders section | Product has order entry and referral tracking |
| Insurance / coverage | ⚠️ Partial | Payers Section | Standard C-CDA payer information; unlikely to capture full insurance/enrollment detail |
| Claims / billing | ❌ Not covered | No billing data in C-CDA | **Major gap**: SmartCare has full revenue cycle management (837 claims, denial management). None exported. |
| Payments | ❌ Not covered | No payment data in C-CDA | Product handles reimbursement tracking |
| Consents / directives | ⚠️ Partial | Advance Directives Section (entries optional) | Standard section; marked as optional |
| Patient communications / portal messages | ❌ Not covered | No communication data in C-CDA | Product has patient portal with secure messaging |
| Specialty: Behavioral health assessments | ❌ Not covered | No behavioral health-specific content | **Critical gap**: SmartCare is a behavioral health EHR. Custom screening tools (PHQ-9, AUDIT, etc.), behavioral health assessments, and structured clinical forms are the product's core data and are entirely absent from the export. |
| Specialty: Substance use disorder | ❌ Not covered | No SUD-specific content | Product serves SUD treatment providers; SUD records absent |
| Specialty: Foster care / adoption | ❌ Not covered | No foster care content | Product serves foster care agencies; this data is absent |
| Specialty: IDD services | ❌ Not covered | No IDD-specific content | Product serves IDD providers; habilitation records absent |
| Specialty: MCO administration | ❌ Not covered | No MCO data in C-CDA | Product has full MCO module (authorization, utilization management, capitation). Entirely absent. |

**Summary**: Of 22 assessed domains, 6 are covered (standard C-CDA clinical data), 5 are partially covered, and **11 are not covered** — including the product's core specialty domains (behavioral health, SUD, foster care, IDD) and billing/MCO administration.

## 6. Documentation Quality

The EHI export documentation is **extremely thin**:

- **Total substantive content**: 326 words on a single web page (verified via `analysis/ehi-page-analysis.json`)
- **Data dictionary**: None
- **Field-level documentation**: None — not a single field name, type, or description
- **Schema/profile documentation**: None — only links to generic HL7 C-CDA 2.2 StructureDefinitions (17 links to `build.fhir.org`)
- **Sample data**: None
- **Machine-readable artifacts**: None
- **Export instructions**: Not public — "available to all Streamline customers in the help desk documentation"
- **Value sets / code systems**: Not documented (product research mentions SNOMED CT, LOINC, RxNorm, ICD-10-CM, but the export documentation does not)
- **Relationships**: N/A (C-CDA is a document, not a relational model)

**Could a developer build an import from this documentation?** No. A developer would learn only that the export is "a C-CDA" with 17 standard sections. They would have no information about SmartCare-specific data mapping, OID assignments, vocabulary choices, extensions, or how behavioral health data is (or isn't) represented. The documentation is functionally equivalent to saying "we export C-CDA" with no further detail.

## 7. Overall Assessment

### Classification

**Standard-based projection** — The export is a C-CDA 2.2 patient summary document. It is not the vendor's native data model but a projection of a small subset of SmartCare data into the HL7 C-CDA standard. This is the same type of document already available through clinical data exchange (transitions of care) and provides clinical summary coverage but entirely misses the vendor-specific behavioral health, billing, MCO, and specialty data that constitutes the majority of what SmartCare stores about patients.

### Key Findings

1. **The export is a standard C-CDA patient summary, not an EHI export.** The 17 sections listed are the standard C-CDA 2.2 sections — the same content available through transitions of care (b)(1). This covers standard clinical summary data (allergies, meds, problems, labs, vitals, immunizations) but omits everything that makes SmartCare a behavioral health EHR. There is no data dictionary, no field-level documentation, and no evidence of vendor-specific extensions.

2. **Zero customer adoption.** The 2025 RWT Results (January 2026, 21 pages) report that during the 90-day evaluation period across all customer environments, 0 export files were created, 0 on-demand executions occurred, and 0 population exports were generated. The 2024 RWT (which measured the related b(6) Data Export criterion) also reported 0 usage. This feature has never been used by any customer.

3. **The product's core data domains are entirely absent from the export.** SmartCare is purpose-built for behavioral health with treatment plans, progress notes, screening tools, golden thread documentation, SUD records, foster care tracking, IDD services, and MCO administration. None of these appear in the C-CDA export. The export covers approximately 6 of 22 applicable data domains assessed.

4. **Documentation is among the thinnest possible.** The entire EHI export documentation is 326 words on a single web page. There are zero data dictionary entries, zero field descriptions, zero sample files, and zero machine-readable schemas. Setup instructions are behind a customer login wall.

5. **No updates since December 2023.** The documentation page was published November 16, 2023 and last modified December 5, 2023. The live page (verified February 15, 2026) is identical to the downloaded version — no updates in over two years.

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA 2.2 (XML)
Model type:      Standard projection (HL7 C-CDA)
Entities:        17 C-CDA sections (no native entities)
Fields:          N/A (no field-level documentation)
Descriptions:    N/A (0% — no fields documented)
Sample data:     No
Bulk export:     Yes (claimed, but 0 usage)
Domains covered: 6 of 22 applicable domains (+ 5 partial)
```

### Bottom Line

SmartCare's EHI export is a standard C-CDA patient summary repackaged as a (b)(10) export. For a behavioral health EHR whose core value is specialty clinical documentation (treatment plans, assessments, screening tools, progress notes) and integrated billing/MCO administration, a C-CDA export covers a small fraction of the patient's designated record set. The single biggest gap is the complete absence of behavioral health-specific clinical data — the very reason this product exists.
