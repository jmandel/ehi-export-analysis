# EHI Export Analysis: Kanrad Technologies Inc

**Product**: KanTime Health v1.0
**Analysis date**: 2026-02-16
**CHPL ID**: 11219 (`15.04.04.3096.KanH.01.01.1.230118`)

## 1. Product Context

KanTime Health is a cloud-based enterprise EMR and agency management platform purpose-built for **post-acute care** — specifically home health, hospice, palliative care, pediatric home care, private duty home care, and consumer-directed services. It is a single integrated platform covering clinical, operational, financial, and HR functions. Per vendor marketing, it serves 912,000+ patients and has processed $12.9 billion in claims.

The product stores extensive data across multiple domains relevant to EHI assessment:

- **Clinical**: Patient demographics, clinical assessments (including OASIS for home health, HIS for hospice), plans of care (485s), visit notes, vital signs, medication lists, e-prescribing records (DEA-certified EPCS via Surescripts), drug interaction data (FirstDataBank), physician orders, immunizations, allergies, problems, procedures, care coordination notes, IDT meeting documentation, bereavement records (hospice)
- **Billing/Financial**: Full revenue cycle — charge entry, 837 claims, remittance, accounts receivable, denial management, payer-specific billing rules, secondary payer processing
- **Administrative**: Referral/intake records, scheduling, authorization/eligibility records, EVV data (GPS/telephony)
- **HR/Workforce**: Employee records, credentials, timesheets, payroll, benefits

A genuine (b)(10) export from this product should cover clinical data in depth (home health and hospice-specific assessments, care plans, visit documentation) plus billing/claims data, referral/intake records, and authorization records at minimum.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `EHI_Tool_Documentation.pdf` (1 page, 42 KB) | The registered (b)(10) EHI export documentation. A single-page PDF with 6 sentences total. States clinical data exports as CCDA 2.1 Release 2 (USCDI v1) and billing data exports as CSV/XLSX/PDF. Contains zero field definitions, zero schema, zero sample data. | **Primary (b)(10) doc — extremely thin** |
| `KanTime_Patient_API.pdf` (14 pages, 255 KB) | REST API documentation for retrieving patient clinical data as CCDA XML. Describes authentication, patient search, full CCDA retrieval, and 22 section-specific queries with curl examples and sample responses. | **Useful context** — shows the mechanism for clinical export and enumerates CCDA sections |
| `SmartOnFHIRAPIDoc.pdf` (66 pages, 686 KB) | SMART on FHIR (g)(10) API documentation covering ~24 US Core FHIR resource types. Standard USCDI-scope FHIR API. | **Not (b)(10)** — this is the separate (g)(10) certification |
| `fhir-base-urls-1.json` (4 KB) | FHIR R4 endpoint Bundle listing KanTime FHIR service base URLs. | **Not (b)(10)** — infrastructure for (g)(10) |

The EHI_Tool_Documentation.pdf is the only artifact specifically addressing (b)(10). It is the single thinnest EHI export document I have encountered — literally one page with no data dictionary, no schema, no field definitions, no sample data, and no instructions beyond identifying the two export formats.

## 3. Export Mechanics

- **Clinical data format**: CCDA 2.1 Release 2 (USCDI v1) XML
- **Clinical mechanism**: REST API (`/Patient/patientccda` and `/Patient/patientdata/{section}` endpoints) via the KanTime Patient API. Requires authentication with EHR or Patient Portal credentials. Supports date-range filtering.
- **Billing data format**: CSV, XLSX, or PDF
- **Billing mechanism**: Role-based — users with "billing user role" can "extract patient claims and payments." No API endpoint documented; likely a UI-driven export within the billing module.
- **Single vs bulk**: The EHI documentation states "Single or Multi-Patient EHI Export." The Patient API supports per-patient retrieval by MRN; no bulk export mechanism is documented for clinical data.
- **Access constraints**: Requires authorized EHR user credentials. Clinical export requires "EHI export authorization" role. Billing export requires "billing user role."
- **Fees**: Not mentioned.

## 4. Export Content: What's In It

### Data Dictionary

**There is no data dictionary.** The entire (b)(10) documentation is a single page with no field definitions, no entity descriptions, no types, no relationships, no value sets, and no sample data.

### Clinical Export (CCDA)

The clinical export is a standard CCDA 2.1 document. Based on the Patient API documentation, it contains 22 addressable sections:

| # | CCDA Section | API Name | Category |
|---|---|---|---|
| 1 | Patient Demographics | `demographics` | Demographics |
| 2 | Allergies and Intolerances | `allergies` | Clinical |
| 3 | Assessment | `assessments` | Clinical |
| 4 | Care Team | `careteam` | Clinical |
| 5 | Encounters | `encounters` | Clinical |
| 6 | Functional Status | `functionalstatus` | Clinical |
| 7 | Goals | `goals` | Clinical |
| 8 | Health Concerns | `healthconcerns` | Clinical |
| 9 | Immunizations | `immunizations` | Clinical |
| 10 | Medical Equipment | `medicalequipment` | Clinical |
| 11 | Medications | `medications` | Clinical |
| 12 | Mental Status | `mentalstatus` | Clinical |
| 13 | Plan of Treatment | `planoftreatment` | Clinical |
| 14 | Problem | `problem` | Clinical |
| 15 | Procedures | `procedures` | Clinical |
| 16 | Reason for Referral | `reasonforreferral` | Clinical |
| 17 | Results | `results` | Clinical |
| 18 | Social History | `socialhistory` | Clinical |
| 19 | Vital Signs | `vitalsigns` | Clinical |
| 20 | Consultation Note | `consultationnote` | Clinical Notes |
| 21 | Progress Note | `progressnote` | Clinical Notes |
| 22 | History and Physical Note | `historyandphysicalnote` | Clinical Notes |

These are **standard CCDA sections** — there is no documentation of any vendor-specific extensions, additional data elements beyond the CCDA standard, or mapping of KanTime-specific data (e.g., OASIS assessments, HIS items, hospice-specific workflows) into the CCDA.

The sample CCDA response in the Patient API PDF shows a bare-bones document with standard templateIds (`2.16.840.1.113883.10.20.22.1.1` and `2.16.840.1.113883.10.20.22.1.2`) and an empty `<structuredBody />` element — the sample literally contains no clinical data.

### Billing Export (CSV)

The EHI documentation mentions that "billing user role will facilitate the process for users to extract patient claims and payments in CSV format export." This is the entirety of the billing export documentation:
- **No field definitions** for claims or payments
- **No sample data**
- **No schema**
- **No instructions** on how to perform the export
- It is impossible to determine what fields are included in the CSV export

### Vendor's Content Organization

| Entity/Table | Fields | Described | Types | Category (vendor's) |
|---|---|---|---|---|
| 22 CCDA sections | N/A (standard CCDA) | 0 | No | Clinical |
| Patient Claims (CSV) | N/A | 0 | No | Billing |
| Patient Payments (CSV) | N/A | 0 | No | Billing |

**Total entities**: 24 (22 CCDA sections + 2 billing exports)
**Total fields documented**: 0
**Fields with descriptions**: 0
**Fields with types**: 0

Full inventory saved to `analysis/entity-inventory-full.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes two export components:

1. **Clinical data via CCDA**: 22 standard CCDA sections covering the USCDI v1 clinical data scope. This is functionally identical to their C-CDA transitions-of-care export ((b)(1)/(b)(2)/(b)(3) certification). The documentation explicitly labels it "CCDA 2.1 Release 2 USCDI v1" — this is the standard clinical summary, not a deep export of KanTime's internal data model.

2. **Billing data via CSV**: Claims and payments, available to billing users. The mention of billing data is the one element that distinguishes this from a pure clinical exchange repackaging. However, with zero documentation of what fields are in the CSV, it is impossible to assess depth or completeness.

**Critical gaps vs. what the product stores**:
- **OASIS assessments** (home health's core clinical assessment) — not mentioned anywhere in the EHI documentation; standard CCDA does not have an OASIS section
- **HIS (Hospice Item Set)** data — not mentioned
- **Plans of care / 485 forms** — CCDA has a Plan of Treatment section, but it is unclear whether KanTime's detailed auto-generated 485s are fully represented
- **Visit-level point-of-care documentation** — KanTime's field clinician documentation (detailed visit notes, wound assessments, therapy notes) goes well beyond standard CCDA progress notes
- **Referral/intake records** — "Reason for Referral" is a CCDA section, but KanTime's full intake workflow (lead tracking, eligibility verification, prior authorization) is not covered
- **Authorization and eligibility data** — not mentioned
- **Scheduling data** — not mentioned (though this is borderline EHI)
- **EVV (Electronic Visit Verification) data** — not mentioned
- **E-prescribing details** — CCDA has Medications section but KanTime's DEA-certified EPCS records may contain more detail
- **Bereavement records** (hospice-specific) — not mentioned
- **IDT meeting documentation** — not mentioned

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | CCDA `demographics` section | Standard CCDA patient demographics; KanTime stores additional contact/referral source data not documented |
| Encounters / visits | ⚠️ Partial | CCDA `encounters` section | Standard CCDA encounters; detailed visit-level POC documentation (the core of home health) likely not fully captured in standard CCDA |
| Problems / conditions | ✅ Covered | CCDA `problem` section | Standard CCDA coverage |
| Medications / prescriptions | ⚠️ Partial | CCDA `medications` section | Standard CCDA; KanTime's EPCS and Surescripts medication history may not be fully represented |
| Allergies | ✅ Covered | CCDA `allergies` section | Standard CCDA coverage |
| Immunizations | ✅ Covered | CCDA `immunizations` section | Standard CCDA coverage |
| Vitals | ✅ Covered | CCDA `vitalsigns` section | Standard CCDA coverage |
| Lab results | ⚠️ Partial | CCDA `results` section | Standard CCDA; limited relevance for home health but supported |
| Procedures | ✅ Covered | CCDA `procedures` section | Standard CCDA coverage |
| Clinical notes / documents | ⚠️ Partial | CCDA `consultationnote`, `progressnote`, `historyandphysicalnote` | Only 3 note types; KanTime stores extensive visit documentation that may not map to these standard note types |
| Care plans / goals | ⚠️ Partial | CCDA `planoftreatment`, `goals` sections | Standard CCDA; KanTime's auto-generated 485 plans of care are likely more detailed than standard CCDA representation |
| Orders / referrals | ⚠️ Partial | CCDA `reasonforreferral` section | Referral reason only; no physician order tracking, no order details |
| Insurance / coverage | ❌ Not covered | No insurance/coverage entities in export documentation | Product manages payer information and authorization — significant gap |
| Claims / billing | ⚠️ Partial | "Patient claims" CSV mentioned | Mentioned but completely undocumented; impossible to assess completeness |
| Payments | ⚠️ Partial | "Patient payments" CSV mentioned | Mentioned but completely undocumented; impossible to assess completeness |
| Consents / directives | ❌ Not covered | Not mentioned | Product likely stores consent forms — gap |
| Specialty: OASIS assessments | ❌ Not covered | Not mentioned in export documentation | **Critical gap** — OASIS is the core clinical assessment for Medicare home health; KanTime stores these extensively |
| Specialty: HIS (Hospice Item Set) | ❌ Not covered | Not mentioned in export documentation | **Critical gap** — HIS is the core quality measure for hospice; KanTime stores these |
| Specialty: Bereavement (hospice) | ❌ Not covered | Not mentioned | Product has bereavement management module — gap |
| Specialty: Care plan 485 | ❌ Not covered | CCDA Plan of Treatment may partially cover | Product auto-generates detailed 485 forms; standard CCDA section unlikely to capture full detail |
| Medical devices | ✅ Covered | CCDA `medicalequipment` section | Standard CCDA coverage |
| Functional / mental status | ✅ Covered | CCDA `functionalstatus`, `mentalstatus` sections | Standard CCDA; but KanTime's actual functional assessments are likely far more detailed |

## 6. Documentation Quality

The EHI export documentation quality is **extremely poor** — among the worst possible:

- **Data dictionary**: None. Zero field definitions for any export component.
- **Schema**: None. No machine-readable schema for the CCDA or CSV exports.
- **Sample data**: None. The sample CCDA in the Patient API PDF has an empty `<structuredBody />`.
- **Instructions**: The billing export has no instructions at all. The clinical export relies entirely on the separate Patient API documentation.
- **Value sets / code systems**: None specified beyond the implicit CCDA standard.
- **Relationships / foreign keys**: None documented.

A developer could not build a useful import from this documentation. For the clinical side, a developer would need to know CCDA 2.1 independently and hope that KanTime produces standard-compliant documents. For the billing side, a developer would have no idea what fields to expect — they would need to perform the export and reverse-engineer the CSV structure.

The Patient API documentation (14 pages) is reasonably well-written as API documentation, with working curl examples and sample responses. However, it describes a standard CCDA retrieval API, not a purpose-built EHI export mechanism.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The export documentation is too thin to assess completeness with confidence. The clinical component is explicitly labeled as "CCDA 2.1 Release 2 USCDI v1" — the standard clinical summary scope, which covers perhaps 20-30% of what KanTime stores about patients. The billing component (claims and payments as CSV) is mentioned in one sentence with zero documentation, making it impossible to determine what's actually exported. Critical post-acute care data domains — OASIS assessments, HIS, detailed visit documentation, care plans/485s, authorizations, referral workflows — are entirely unaddressed.

**Axis 2 — Export approach: Repackaged existing export**

The clinical export is explicitly the vendor's existing C-CDA capability rebranded as (b)(10). The EHI document states "Clinical data is exported as CCDA 2.1 Release 2 USCDI v1" — this is the same format and standard used for (b)(1)/(b)(2)/(b)(3) transitions of care. The Patient API used to retrieve the CCDA is the same API documented separately for clinical data exchange. The only element suggesting any (b)(10)-specific effort is the one-sentence mention of billing CSV exports, but with zero documentation this could be an existing report repackaged.

### Key Findings

1. **The EHI documentation is a single page with 6 sentences and zero field definitions** (`EHI_Tool_Documentation.pdf`, 1 page). This is one of the thinnest (b)(10) documents possible — it provides no data dictionary, no schema, no sample data, and no meaningful detail about what is exported.

2. **The clinical export is explicitly standard CCDA (USCDI v1)**, not a purpose-built EHI export. It uses the same Patient API and same format as the vendor's existing clinical exchange. There is no evidence of any KanTime-specific data mapping beyond standard CCDA sections.

3. **Critical post-acute care data domains are absent**: OASIS assessments (home health's core regulatory assessment), HIS data (hospice quality measures), detailed visit-level POC documentation, and care plan 485 forms — the data that makes home health/hospice EHRs distinctive — are not mentioned in the export documentation.

4. **Billing export is mentioned but completely undocumented**: The one-sentence claim that billing users can export claims and payments as CSV is the only element beyond standard clinical exchange, but with zero schema documentation it is not possible to verify this capability or assess its depth.

5. **No sample data, no schema, no data dictionary of any kind** — the documentation provides no machine-readable artifacts and no way to understand what the export actually contains at a field level.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Repackaged existing export
Export format:   CCDA 2.1 XML (clinical) + CSV/XLSX/PDF (billing)
Entities:        24 (22 CCDA sections + 2 billing mentions)
Fields:          N/A (no field-level documentation)
Descriptions:    N/A
Sample data:     No
Bulk export:     Unclear (mentions multi-patient but no details)
Domains covered: ~8 of 19 applicable domains (all via standard CCDA; billing mentioned but undocumented)
```

### Bottom Line

KanTime's (b)(10) EHI export is a standard C-CDA clinical summary relabeled as EHI export, accompanied by a single undocumented sentence about billing CSV exports. A patient or provider would receive a basic clinical summary missing the most important data types in post-acute care — OASIS assessments, hospice item sets, detailed visit documentation, and care plans — with no way to know what's in the billing CSV. The single biggest gap is the complete absence of home health and hospice-specific clinical assessment data (OASIS, HIS), which is the core patient record in this care setting.
