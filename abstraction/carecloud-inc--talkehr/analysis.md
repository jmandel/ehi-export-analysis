# EHI Export Analysis: CareCloud, Inc.

**Product**: talkEHR
**Analysis date**: 2026-02-16
**CHPL IDs**: 9799 (15.04.04.2790.Talk.01.01.1.181217)

## 1. Product Context

talkEHR is a cloud-based ambulatory EHR and practice management platform developed by MTBC (now CareCloud, Inc.), launched in 2017. It is an integrated platform combining:

- **Clinical EHR**: Patient charting with 70+ specialty templates, clinical documentation with voice dictation, problem lists, medications, allergies, immunizations, vitals, lab ordering/results, imaging, clinical decision support, care plans, and referrals.
- **E-Prescribing**: Surescripts integration including controlled substances, refill management, drug interaction alerts (talkRX mobile app).
- **Practice Management**: Appointment scheduling, patient check-in (talkCheckin app), staff scheduling.
- **Medical Billing & RCM**: Insurance claim submission, payment posting, denial management, end-to-end revenue cycle management.
- **Patient Engagement**: Patient portal (talkPHR) with secure messaging, lab results viewing, claims/statements review, demographic self-service, telehealth/video visits.
- **Public Health Reporting**: Immunization registries, syndromic surveillance, cancer/electronic case reporting.
- **Financial Analytics**: PrecisionBI Lite dashboards and KPI reporting.

The product is certified for 45+ ONC criteria. For EHI export completeness, the key question is whether the export covers not just the clinical C-CDA data but also billing/claims, appointment data, patient communications, e-prescribing workflow data, and the full depth of clinical detail beyond what C-CDA standard sections capture.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/talkEHR-b10-EHI-Export-Documentation.pdf` | 12-page PDF (1.1 MB, created 2023-11-14). The sole EHI export documentation artifact. Contains C-CDA field mapping (pp. 6–10), export UI screenshots (pp. 3–5), PDF export descriptions (p. 11), and a brief FHIR mention (p. 12). | **Primary source** — all export detail comes from this document |
| `downloads/cost-and-fees-information.html` | 61 KB HTML page — CareCloud/talkEHR ONC mandatory disclosures page. Lists certified criteria and links to the b(10) PDF. | Low — confirms the PDF is the official documentation |
| `downloads/screenshot-footer-with-b10-link.png` | Screenshot of page footer showing b(10) link location | Minimal — confirms navigation |
| `downloads/screenshot-b10-link-footer.png` | Focused screenshot of b(10) link element | Minimal |
| `product-research.md` | Detailed product research on talkEHR capabilities and modules | **Context source** — establishes what the product stores |
| `ehi-export-report.md` | Prior agent's analysis of the export documentation | Orientation only — verified independently |

## 3. Export Mechanics

**Format**: Dual-format approach:
1. **C-CDA R2.1 XML** — for structured clinical data (HL7 CDA Release 2, Consolidated CDA Templates, DSTU R2.1, August 2015)
2. **PDF** — for demographics/insurance, advance directives, appointments, messages, billing data, and clinical documents

**Mechanism**: UI-driven export within the talkEHR application:
- **Single-patient export**: Navigate to CCDA Report → CCDA Export tab → select patient → Generate → Download XML
- **Bulk patient export**: Navigate to CCDA Report → Data Portability tab → select date range → Export → Downloads as ZIP of XML files
- **PDF exports**: Available via the application's "Reports" section for demographics, insurance, appointments, messages, and claim data
- **FHIR**: Mentioned on page 12 — "talkEHR FHIR server creates a single-patient FHIR resource Document Reference and supports FHIR Bulk Data EHI Export for patient population" — no technical detail provided

**Single-patient**: Yes (C-CDA and PDF)
**Bulk capability**: Yes (C-CDA via Data Portability tab; FHIR Bulk Data claimed but undocumented)
**Access constraints**: Practice administrator controls user access to export. No fees mentioned.

## 4. Export Content: What's In It

The export documentation consists of a single 12-page PDF with no sample data, no machine-readable schemas, and no supplementary technical documentation.

### C-CDA Clinical Data (Pages 6–10)

The documentation maps 82 data elements across 24 C-CDA sections, with XPATHs/template references for 30 fields and code system identifiers for 29 fields. This represents the standard C-CDA CCD document structure — it is **not a product-specific data dictionary** but rather a mapping of talkEHR's clinical data to the C-CDA R2.1 standard.

Code systems referenced: SNOMED CT, ICD-10, RxNorm, NDC, LOINC, CVX, CPT-4, HCPCS, NCI Thesaurus, GMDN, AdministrativeGender, CDC Race & Ethnicity.

### PDF Exports (Page 11)

Six categories of data exported as PDF, each with a single boilerplate sentence and no field-level detail:

| PDF Export Category | Documentation Detail |
|---|---|
| Patient Demographic/Insurance | "comprehensive view of demographics and insurance details" |
| Advance Directive | "comprehensive view of Advance Directive" |
| Appointments | "comprehensive view of appointments" |
| Provider-to-Patient Messages | "comprehensive view of messages" |
| Billing Data (Claim) | "comprehensive view of billing data (CPT, ICD, Modifier)" |
| Documents | "signed progress notes, available lab results, radiology reports, and any other scanned or uploaded document" |

### FHIR Export (Page 12)

One sentence: "talkEHR FHIR server creates a single-patient FHIR resource Document Reference and supports FHIR Bulk Data EHI Export for patient population as described in § 170.315(b)(10)(ii)." No endpoint URLs, no resource types, no profiles, no API documentation.

### Vendor's Own Content Organization

| Entity/Section | Fields | Documented with XPATH | Code Systems | Format | Category |
|---|---|---|---|---|---|
| Patient Demographics/Information | 6 | 6 | 3 | C-CDA XML | Clinical |
| Provider's Name and Contact Info | 3 | 3 | 0 | C-CDA XML | Clinical |
| Date and Location of Visit | 2 | 2 | 0 | C-CDA XML | Clinical |
| Chief Complaint and Reason for Visit | 1 | 0 | 0 | C-CDA XML | Clinical |
| Encounters | 5 | 1 | 2 | C-CDA XML | Clinical |
| Immunizations | 9 | 1 | 3 | C-CDA XML | Clinical |
| Instructions | 1 | 1 | 1 | C-CDA XML | Clinical |
| Treatment Plan | 2 | 1 | 1 | C-CDA XML | Clinical |
| Social History | 3 | 1 | 2 | C-CDA XML | Clinical |
| Problems | 3 | 1 | 1 | C-CDA XML | Clinical |
| Medications | 5 | 1 | 1 | C-CDA XML | Clinical |
| Medication Allergies | 4 | 1 | 3 | C-CDA XML | Clinical |
| Laboratory Tests | 4 | 0 | 1 | C-CDA XML | Clinical |
| Laboratory Information | 5 | 0 | 0 | C-CDA XML | Clinical |
| Laboratory Values/Results | 5 | 1 | 1 | C-CDA XML | Clinical |
| Vitals | 2 | 1 | 1 | C-CDA XML | Clinical |
| Goal | 3 | 1 | 0 | C-CDA XML | Clinical |
| Procedures | 2 | 1 | 1 | C-CDA XML | Clinical |
| Care Team Members | 3 | 1 | 0 | C-CDA XML | Clinical |
| Reason for Referral | 1 | 1 | 1 | C-CDA XML | Clinical |
| Medical Equipment | 2 | 1 | 1 | C-CDA XML | Clinical |
| Mental Status | 4 | 1 | 1 | C-CDA XML | Clinical |
| Functional Status | 4 | 1 | 1 | C-CDA XML | Clinical |
| Health Concern | 3 | 1 | 1 | C-CDA XML | Clinical |
| Patient Demographic/Insurance (PDF) | 1* | 0 | 0 | PDF | Admin |
| Advance Directive (PDF) | 1* | 0 | 0 | PDF | Clinical |
| Appointments (PDF) | 1* | 0 | 0 | PDF | Admin |
| Provider-to-Patient Messages (PDF) | 1* | 0 | 0 | PDF | Communications |
| Billing Data / Claims (PDF) | 4* | 0 | 2 | PDF | Billing |
| Documents (PDF) | 4* | 0 | 0 | PDF | Documents |
| FHIR Data Export | 1* | 0 | 0 | FHIR | Clinical |

\* Indicates fields are nominal placeholders — no actual field-level detail is documented for these categories.

**Totals**: 31 entities, 95 documented data elements (82 in C-CDA with meaningful detail, 13 nominal placeholders for PDF/FHIR exports).

Full inventory: `analysis/entity-inventory-full.json`

## 5. Coverage Assessment

### 5a. What the Vendor Covers (Bottom-Up)

The export has two clearly different tiers of documentation quality:

**Tier 1 — C-CDA Clinical Data (well-documented)**: 24 sections covering standard clinical domains (demographics, encounters, problems, medications, allergies, immunizations, labs, vitals, procedures, goals, care team, referrals, medical equipment, mental/functional status, health concerns, social history). These map directly to C-CDA R2.1 standard sections with XPATHs and code systems. This is the standard clinical summary — exactly what you'd expect from a CCD/C-CDA export. The 82 fields across these sections correspond closely to the USCDI data elements.

**Tier 2 — PDF Exports (barely documented)**: 6 categories covering billing, appointments, messages, demographics/insurance, advance directives, and documents. These get one sentence each. The billing data mentions "CPT, ICD, Modifier" but no other details — no claim amounts, dates of service, payer information, payments, adjustments, or denial data. The vendor acknowledges these data categories exist and claims to export them, but the PDF format renders the data non-machine-readable, and the documentation provides no field-level specification.

**Tier 3 — FHIR (essentially undocumented)**: A single sentence claiming FHIR Bulk Data support for (b)(10)(ii). If this is a real, working FHIR export with multiple resource types beyond DocumentReference, it could change the assessment — but there is zero documentation to evaluate.

### 5b. Standardized Domain Coverage (Top-Down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA: 6 fields (name, sex, DOB, race, ethnicity, language); PDF: "demographics and insurance" (no detail) | C-CDA covers USCDI minimum. PDF likely has more detail but undocumented. Product stores contacts, addresses, employer info — unclear if exported. |
| Encounters / visits | ⚠️ Partial | C-CDA: Encounters section (5 fields — code, performer, diagnosis, location, date) | Standard C-CDA encounter data. Product's PM module has detailed scheduling and visit workflow data not captured here. |
| Problems / conditions | ✅ Covered | C-CDA: Problems (3 fields), Health Concern (3 fields) with SNOMED + ICD-10 | Standard coverage via C-CDA |
| Medications / prescriptions | ⚠️ Partial | C-CDA: Medications (5 fields — medication, directions, dates, status) | Covers medication list but not e-prescribing workflow data (refill requests, pharmacy info, drug interaction alert history, controlled substance details). Product has extensive e-prescribing via Surescripts. |
| Allergies | ✅ Covered | C-CDA: Medication Allergies (4 fields — substance, reaction, severity, status) | Standard coverage via C-CDA |
| Immunizations | ✅ Covered | C-CDA: Immunizations (9 fields) with CVX, CPT-4, SNOMED | Good detail for immunizations |
| Vitals | ✅ Covered | C-CDA: Vitals (2 fields — observation, date/time) with LOINC | Standard coverage |
| Lab results | ✅ Covered | C-CDA: Laboratory Tests (4), Lab Info (5), Lab Results (5) — 14 fields total with LOINC | Good coverage across three related sections |
| Imaging / diagnostic reports | ⚠️ Partial | PDF Documents export mentions "radiology reports" | Radiology reports exported as PDFs; no structured imaging data |
| Procedures | ✅ Covered | C-CDA: Procedures (2 fields) with CPT-4, SNOMED, HCPCS | Standard coverage |
| Clinical notes / documents | ✅ Covered | PDF Documents export: "signed progress notes, lab results, radiology reports, scanned/uploaded documents" | Documents exported as PDFs — appropriate format for unstructured clinical notes |
| Care plans / goals | ✅ Covered | C-CDA: Treatment Plan (2 fields), Goal (3 fields), Instructions (1 field) | Standard C-CDA coverage |
| Orders / referrals | ⚠️ Partial | C-CDA: Reason for Referral (1 field), Treatment Plan (planned observations) | Referral reason captured but not referral workflow details. Order entry data (CPOE) beyond what appears in C-CDA sections is not documented. |
| Insurance / coverage | ⚠️ Partial | PDF: "demographics and insurance details" (no field-level detail) | Product stores payer information for billing. PDF export claimed but completely undocumented — could be comprehensive or minimal. |
| Claims / billing | ⚠️ Partial | PDF: "billing data (CPT, ICD, Modifier)" (3 named elements, no further detail) | Product has full RCM with claim submission, payment posting, denial management. PDF export mentions only codes/modifiers — no amounts, dates, payer responses, payments, adjustments, or denial details documented. Non-machine-readable format. |
| Payments | ❌ Not covered | No mention in export documentation | Product has payment posting capabilities. No evidence of payment data export. |
| Consents / directives | ⚠️ Partial | PDF: "Advance Directive" (no field detail) | Advance directives claimed but undocumented. No mention of general consent forms. |
| Patient communications | ⚠️ Partial | PDF: "Provider-to-Patient Messages" (no field detail) | Messages exported as PDF but no detail on what's included. Patient portal (talkPHR) communications, appointment requests, demographic update requests not mentioned. |
| Medical devices | ✅ Covered | C-CDA: Medical Equipment (2 fields) with SNOMED, GMDN | Standard implantable device coverage |
| Mental/functional status | ✅ Covered | C-CDA: Mental Status (4 fields), Functional Status (4 fields) with SNOMED | Standard C-CDA coverage |
| Family health history | ❌ Not covered | Not present in any documented export section | Product is certified for (a)(12) Family Health History. This is a clear gap — the data exists but is not in the documented export. |
| Social history | ✅ Covered | C-CDA: Social History (3 fields) with LOINC, SNOMED | Standard coverage |

**Summary**: 12 of 22 applicable domains have at least standard coverage. 8 domains are partially covered (mostly due to undocumented PDF exports or missing workflow depth). 2 domains with known product data (payments, family health history) appear absent from the export.

## 6. Documentation Quality

**Overall**: Poor to fair. The documentation is a 12-page Word-to-PDF document that reads as a compliance checkbox rather than a technical specification.

**What's well-documented**: The C-CDA field mapping on pages 6–10 provides useful reference information — XPATHs, template OIDs, and code systems for each data element. However, this is essentially the C-CDA R2.1 standard specification reproduced in a vendor document, not a product-specific data dictionary showing what talkEHR actually stores.

**What requires guesswork**: Everything outside the C-CDA sections. The PDF export categories on page 11 each get a single generic sentence ("comprehensive view of..."). A developer receiving billing data as PDF would have no idea what fields to expect, what date ranges are covered, or how claims relate to encounters. The FHIR mention on page 12 provides zero actionable information.

**Machine-readable artifacts**: None. No sample C-CDA files, no JSON/XML schemas, no sample PDFs, no FHIR capability statement, no API documentation.

**Could a developer build an import?** For C-CDA clinical data: yes, because C-CDA R2.1 is a well-defined standard. For PDF exports: no — the content and structure are undocumented. For FHIR: no — no endpoint, resource type, or profile information provided.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The clinical C-CDA component covers the standard USCDI domains well — this is what any certified EHR's C-CDA export would produce. The PDF exports attempt to go beyond clinical summaries by including billing data, appointments, messages, and documents, which is a positive signal. However:
- The billing export ("CPT, ICD, Modifier" as PDF) is far too thin to represent the full RCM data the product stores (claims, payments, denials, adjustments, EOBs).
- Family health history is missing entirely despite being a certified capability.
- E-prescribing workflow data (refill history, pharmacy details, controlled substance records) is not addressed beyond the basic medication list.
- Payment data appears entirely absent.
- The PDF format for structured data (billing, appointments) means the data is technically exported but practically non-computable.

The vendor clearly *thought* about going beyond C-CDA (the PDF export categories show awareness of non-clinical data), but the execution is shallow — particularly for billing/RCM, which is a major product capability.

**Axis 2 — Export approach: Repackaged existing export with minor additions**

The core of the export is a standard C-CDA R2.1 CCD — this is the same clinical summary format used for transitions of care (b)(1)-(b)(3) and clinical data exchange. The C-CDA mapping on pages 6–10 is essentially the C-CDA specification, not a product-specific EHI export design. The PDF exports for billing, appointments, and messages represent an attempt to go beyond C-CDA, but they are:
1. In a non-machine-readable format (PDF)
2. Completely undocumented at the field level
3. Apparently generated from the existing "Reports" section of the application

This is a C-CDA export relabeled as (b)(10), with PDF report printouts bolted on for non-clinical categories. The FHIR Bulk Data mention appears to be a reference to the existing (g)(10) FHIR API rather than a purpose-built EHI export, given the total absence of documentation.

### Key Findings

1. **C-CDA is the foundation, not purpose-built EHI**: The clinical data export is a standard CCD conforming to C-CDA R2.1 — the same output used for transitions of care. The 82 documented fields across 24 sections correspond to standard C-CDA template sections, not product-specific data. (Source: PDF pp. 6–10, standard referenced: § 170.205(a)(4))

2. **PDF format for structured data is a significant limitation**: Billing claims, appointment schedules, and insurance data are internally structured/coded data exported as non-machine-readable PDFs. This means a recipient can view the data but cannot import it into another system without manual re-entry. (Source: PDF p. 11)

3. **Billing export is far too thin for a product with full RCM**: The billing PDF mentions only "CPT, ICD, Modifier" — no claim amounts, payer information, payment posting, denial details, adjustments, or statements. For a product that advertises "end-to-end Revenue Cycle Management" and "unlimited claim submissions," this is a major gap. (Source: PDF p. 11, product-research.md billing module)

4. **Family health history is a documented gap**: The product is certified for (a)(12) Family Health History, but no export section covers this data. (Source: PDF pp. 6–10 — no Family History section; metadata.json — certified for 170.315 (a)(12))

5. **FHIR export claim is unsubstantiated**: A single sentence on page 12 claims FHIR Bulk Data support for (b)(10)(ii) with zero technical detail. Without documentation, this claim cannot be evaluated. (Source: PDF p. 12)

### Summary Stats

```
Coverage:        Partial
Approach:        Repackaged existing export (C-CDA + PDF report printouts)
Export format:   C-CDA R2.1 XML + PDF + FHIR (claimed, undocumented)
Entities:        31 (24 C-CDA sections, 6 PDF categories, 1 FHIR mention)
Fields:          95 (82 with meaningful C-CDA detail, 13 nominal placeholders)
Descriptions:    ~34% (30 of 82 C-CDA fields have XPATH references; 29 have code systems; PDF/FHIR fields have no detail)
Sample data:     No
Bulk export:     Yes (C-CDA bulk via Data Portability tab; FHIR Bulk claimed)
Domains covered: 12 of 22 applicable (with 8 partially covered, 2 not covered)
```

### Bottom Line

talkEHR's EHI export is a standard C-CDA clinical summary with PDF report printouts attached for billing, appointments, and messages. A patient would get their clinical data in a machine-readable standard format, but their billing records, insurance details, and communications would arrive as non-computable PDFs with no documented structure. The biggest gap is the shallow billing export — for a product whose core value proposition includes "end-to-end Revenue Cycle Management," exporting claims as PDFs with only "CPT, ICD, Modifier" mentioned falls far short of a genuine EHI export of the designated record set.
