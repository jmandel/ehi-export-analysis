# EHI Export Analysis: TronsHealth LLC

**Product**: TronsHealth  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.05.05.3209.TRON.00.00.1.241213

## 1. Product Context

TronsHealth is a cloud-based ambulatory EHR and practice management system from TronsHealth LLC (Austin, TX), a startup subsidiary of Tronsit Solutions LLC. It received its first ONC certification on December 13, 2024 (version 1.0) and has no publicly known customer base.

The product is positioned as an integrated platform covering:
- **EHR**: Clinical documentation with customizable templates, clinical decision support, e-prescribing, vital signs capture via medical device integration, secure messaging
- **Practice Management**: Appointment scheduling, real-time insurance eligibility verification, billing and claims management, financial analytics
- **Patient Engagement**: Patient portal (access to records, lab results, Rx refills), secure messaging, appointment reminders, digital check-in
- **Credentialing**: Provider credentialing, NPI enrollment, CAQH management

Target users are ambulatory physicians, nurse practitioners, surgeons, clinicians, and administrative staff. The certified criteria include CPOE for medications (a)(1), demographics (a)(5), implantable device list (a)(14), transitions of care (b)(1), and FHIR API (g)(10).

For a complete (b)(10) EHI export, we would expect coverage of: patient demographics, encounters, clinical notes, medications, allergies, diagnoses, immunizations, vitals, lab results, imaging, appointments, insurance, billing/claims, payments, patient communications, documents, and potentially referrals, care plans, and orders.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/170.315b10-Electronic-Health-Information-Export-EHI.pdf` | 27-page PDF: overview, export instructions with screenshots, data dictionary for 16 entities. 739 KB. **Primary artifact.** | **High** — contains the entire export documentation |
| `downloads/enrichment/data-dictionary.json` | Prior agent's JSON extraction of the data dictionary (16 entities, 401 fields) | Medium — used for cross-validation only |
| `downloads/enrichment/extraction-stats.json` | Statistics from prior extraction | Low — verified against my own extraction |
| `product-research.md` | Product capabilities research | Medium — establishes baseline for coverage assessment |

Only one substantive artifact exists: the PDF. There are no sample data files, no machine-readable schemas, no additional documentation.

## 3. Export Mechanics

- **Format**: CSV files bundled in a ZIP archive
- **Mechanism**: Web UI — dedicated "Electronic Health Information Export" menu item in the side navigation. Admin/authorized users click through to select a patient or all patients, then download a ZIP.
- **Single-patient**: Yes — select individual patient from a popup list
- **Bulk export**: Yes — "Click here to download all Patient's Health Information" option, requires practice-level permissions
- **Access constraints**: Restricted to authorized/admin-level users. Practice-level permissions required for bulk export.
- **Fees**: Not mentioned

The PDF includes 8 screenshots showing the export workflow (login → dashboard → side menu → EHI export screen → patient selection → export download), demonstrating a purpose-built UI feature.

## 4. Export Content: What's In It

The data dictionary documents **16 entities** with **401 total fields**. The TOC lists 18 sections, but the PDF is truncated — sections 3.15 (Provider Note) and 3.18 (Encounter) are referenced in the TOC (at pages 27 and 32 respectively) but absent from the 27-page document. The filename `§170.315b10-Electronic-Health-Information-Export-EHI.docx.pdf` suggests a Word-to-PDF conversion that truncated the output.

All 401 fields have data types documented. 400 of 401 fields (99.8%) have descriptions. The one undescribed field is `Type` (varchar) in Patient – Consent. Descriptions are brief but functional — they explain the field's purpose, not just restate the field name.

Data types are SQL-like: varchar (234 fields), datetime (57), long (54), boolean (36), int (10), nvarchar (3), decimal (3), plus list (1), bool (1), string (1), file (1).

Relationships are implicit through ID fields (PatientID, AppointmentID, PracticeID, etc.) but not formally documented. Lookup IDs (e.g., `SuffixLookupID`, `GenderLookupId`, `StatusLookupID`) reference undocumented lookup tables — the actual values are not provided.

### Vendor's own content organization

| Entity | Section | Fields | Described | Types | Category |
|---|---|---|---|---|---|
| Patient – Demographics | 3.1 | 52 | 52 | yes | Demographics |
| Patient – Medications | 3.2 | 28 | 28 | yes | Clinical |
| Patient – Allergies | 3.3 | 25 | 25 | yes | Clinical |
| Patient – Appointments | 3.4 | 43 | 43 | yes | Scheduling |
| Patient – Complaints | 3.5 | 18 | 18 | yes | Clinical |
| Patient – Diagnosis | 3.6 | 15 | 15 | yes | Clinical |
| Patient – Documents & Images | 3.7 | 1 | 1 | yes | Documents |
| Patient – Immunization | 3.8 | 13 | 13 | yes | Clinical |
| Patient – Insurances | 3.9 | 32 | 32 | yes | Insurance |
| Patient – Contact | 3.10 | 22 | 22 | yes | Demographics |
| Patient – Consent | 3.11 | 27 | 26 | yes | Administrative |
| Patient – Education | 3.12 | 12 | 12 | yes | Demographics |
| Patient – Patient Notes | 3.13 | 16 | 16 | yes | Administrative |
| Patient – Payments | 3.14 | 33 | 33 | yes | Billing |
| Patient – Provider Note | 3.15 | — | — | — | **MISSING (truncated)** |
| Patient – Social History | 3.16 | 16 | 16 | yes | Clinical |
| Patient – Vitals | 3.17 | 48 | 48 | yes | Clinical |
| Patient – Encounter | 3.18 | — | — | — | **MISSING (truncated)** |

The full field-level inventory is in `analysis/entity-inventory-full.json` (all 401 fields with names, types, and descriptions).

**Notable entities by depth:**

- **Demographics (52 fields)**: Comprehensive — includes names, DOB, SSN, multiple address types, race, ethnicity, preferred language, gender identity, sexual orientation, marital status, employer info, and audit fields.
- **Vitals (48 fields)**: Extensive — covers height, weight, BMI, BP (systolic/diastolic), pulse, respiration, temperature, O2 saturation, blood type, pain severity, urine output, plus measurement metadata (cuff size, cuff location, BP position, measurement units/times).
- **Appointments (43 fields)**: Detailed scheduling — includes status, check-in/out times, copay, insurance references, provider, facility, room, reason, and audit fields.
- **Payments (33 fields)**: Covers patient-side payments — credit card, check, and cash transactions; wallet balance; transaction references; refund tracking. Does NOT include insurance claims or charge/CPT details.
- **Insurances (32 fields)**: Insurance coverage info — member ID, payer ID, group number, policy dates, eligibility status, copay, insured party demographics. Does NOT include claims adjudication or EOBs.
- **Documents & Images (1 field)**: Simply exports files in native format (PNG, JPEG, JPG). No metadata fields (document type, date, author, etc.).

**Standard coding systems referenced**: ICD-10, ICD-9, SNOMED, RxNorm, NDC, ICPC-2.

**Audit fields**: Most entities include CreatedBy, CreatedOn, ModifiedBy, ModifiedOn, IsDeleted, and UUID — indicating soft-delete tracking.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor organizes data around patient-centric entities. The export covers a reasonable breadth for a small ambulatory EHR — 16 documented entities spanning demographics, clinical observations, medications, scheduling, insurance, and payments. The richest areas are demographics (52 fields), vitals (48 fields), and appointments (43 fields).

Notable strengths:
- **Payments entity** (33 fields) goes beyond USCDI by exporting patient financial transactions, which most clinical exchange exports don't include
- **Insurance entity** (32 fields) captures detailed coverage information including eligibility status
- **Appointments** (43 fields) includes scheduling data not typically in clinical summaries
- **Consent** (27 fields) captures consent records with custodian party details
- Standard clinical codes (ICD-10, SNOMED, RxNorm, NDC) are referenced throughout

Notable weaknesses:
- **Provider Note and Encounter sections are missing** due to PDF truncation — these are arguably the two most important clinical entities
- **No lab results entity** — the product's patient portal references lab results, but no lab/diagnostic entity is in the export
- **No orders entity** — the product is certified for CPOE (a)(1) but orders aren't separately documented
- **No implantable device entity** — certified for (a)(14) but not in the data dictionary
- **No secure messaging entity** — product offers secure provider-patient messaging
- **Documents & Images** is paper-thin (1 field) — exports files but no metadata

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient – Demographics` (52 fields), `Patient – Contact` (22 fields), `Patient – Education` (12 fields) | Thorough — includes race, ethnicity, language, gender identity, sexual orientation |
| Encounters / visits | ❌ Not covered | Section 3.18 listed in TOC but missing from document | **Significant gap** — encounters are core clinical data; PDF truncation is the likely cause |
| Problems / conditions / diagnoses | ✅ Covered | `Patient – Diagnosis` (15 fields) with ICD-10, ICD-9, SNOMED coding | Adequate — includes verification status and appointment linkage |
| Medications / prescriptions | ✅ Covered | `Patient – Medications` (28 fields) with NDC, RxNorm, brand/generic names, sig, route | Adequate for ambulatory e-prescribing |
| Allergies | ✅ Covered | `Patient – Allergies` (25 fields) with RxNorm, NDC, severity, criticality | Good depth |
| Immunizations | ✅ Covered | `Patient – Immunization` (13 fields) with vaccine code, amount, route | Adequate |
| Vitals | ✅ Covered | `Patient – Vitals` (48 fields) covering BP, HR, RR, temp, O2 sat, BMI, pain, blood type | Thorough |
| Lab results | ❌ Not covered | No lab/diagnostic entity in the export | **Gap** — patient portal references lab results, so the product likely stores them |
| Imaging / diagnostic reports | ❌ Not covered | No imaging entity | **Possible gap** — uncertain if product stores imaging data |
| Procedures | ❌ Not covered | No procedures entity | **Possible gap** — product targets surgeons per SED description |
| Clinical notes / documents | ⚠️ Partial | `Patient – Documents & Images` (1 field, files only). Section 3.15 Provider Note in TOC but missing | **Significant gap** — provider notes are core clinical documentation; truncation issue |
| Care plans / goals | ❌ Not covered | No care plan entity | N/A — unclear if product has care plan functionality |
| Orders / referrals | ❌ Not covered | No orders entity despite CPOE (a)(1) certification | **Gap** — medication orders certified but not in export |
| Insurance / coverage | ✅ Covered | `Patient – Insurances` (32 fields) with member ID, payer, policy dates, eligibility | Good depth |
| Claims / billing | ⚠️ Partial | `Patient – Payments` (33 fields) covers patient payments only | **Gap** — product has billing/claims management; no claim submissions, CPT codes, charge amounts, or ERA/EOBs in export |
| Payments | ✅ Covered | `Patient – Payments` (33 fields) — credit card, check, cash, wallet, refunds | Good for patient-side payments |
| Consents / directives | ✅ Covered | `Patient – Consent` (27 fields) with status, validity, custodian | Adequate |
| Patient communications / portal messages | ❌ Not covered | No messaging entity | **Gap** — product offers secure messaging and patient portal |
| Specialty-specific data | ❌ Not covered | No specialty-specific entities | N/A — product appears general ambulatory, not specialty-focused |
| Social history | ⚠️ Partial | `Patient – Social History` (16 fields) — tobacco use only | Limited — only covers tobacco; no alcohol, drugs, SDOH |
| Chief complaints | ✅ Covered | `Patient – Complaints` (18 fields) with SNOMED/ICPC-2 codes | Adequate |
| Implantable devices | ❌ Not covered | No entity despite (a)(14) certification | **Gap** — certified but not exported |

**Summary**: 10 of 19 applicable domains covered, 3 partially covered, 6 not covered. Of the 6 not covered, at least 4 represent genuine gaps (encounters, lab results, provider notes, patient communications) relative to what the product stores.

## 6. Documentation Quality

**Strengths:**
- Field-level data dictionary with name, type, and description for nearly every field (400/401)
- Step-by-step export instructions with 8 UI screenshots
- Clear statement of export format (CSV in ZIP) and access controls
- References standard coding systems (ICD-10, SNOMED, RxNorm, NDC)

**Weaknesses:**
- **Truncated document** — the two most important clinical sections (Provider Note, Encounter) are missing. This is a documentation failure, regardless of whether the export actually includes them.
- **No sample data files** — no example CSVs showing actual export output
- **No lookup table definitions** — many fields reference lookup IDs (e.g., `GenderLookupId`, `StatusLookupID`, `SeverityOfPainLookupName`) without documenting what values they resolve to
- **No CSV format specification** — delimiter, quoting, encoding, date formats are unspecified
- **No ZIP structure documentation** — folder hierarchy and file naming conventions unknown
- **No relationship documentation** — foreign keys are implicit through naming but not formally defined
- **No value set documentation** — coded fields reference standards but don't enumerate allowed values
- **No machine-readable schema** — only the PDF

**Could a developer import this data?** Partially. Field names and types are clear, but a developer would need to reverse-engineer lookup tables, guess CSV formatting, and would have no provider note or encounter data to work with. The documentation is a reasonable starting point but insufficient for reliable automated import.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The export covers a meaningful set of patient data domains — demographics, medications, allergies, diagnoses, immunizations, vitals, insurance, payments, appointments, consents, and social history. This goes beyond a pure USCDI clinical summary by including payments (33 fields), insurance (32 fields), appointments (43 fields), and consents (27 fields). However, there are significant gaps relative to what the product stores:

1. **Provider notes and encounters** are listed in the TOC but missing from the truncated PDF — these are core clinical documentation
2. **Lab results** are absent despite the patient portal referencing them
3. **Claims/billing detail** is absent despite the product having billing/claims management — only patient-side payments are exported
4. **Implantable devices** are absent despite (a)(14) certification
5. **Patient communications** (secure messages, portal activity) are absent

The truncation issue is particularly damaging: if Provider Note and Encounter were present, the export's clinical coverage would be substantially better. But as documented, the export has genuine clinical and billing gaps.

**Axis 2 — Export approach: Purpose-built EHI export**

This is genuinely a purpose-built (b)(10) export, not a repackaged clinical exchange. Evidence:
- Dedicated UI feature ("Electronic Health Information Export" in the side menu)
- CSV/ZIP format distinct from the product's C-CDA (b)(1) and FHIR (g)(10) exports
- Includes non-USCDI data: patient payments, appointments, consents, insurance details, education records
- Field-level data dictionary mapping to internal database tables, not standard FHIR/C-CDA structures
- Export covers data domains (payments, scheduling, consent) that would never appear in a C-CDA or FHIR Bulk Data export

The vendor built something specifically for (b)(10), even if the result is incomplete.

### Key Findings

1. **Purpose-built but truncated**: TronsHealth built a genuine (b)(10) CSV export with a dedicated UI and a 401-field data dictionary — but the documentation PDF is truncated, cutting off Provider Note (3.15) and Encounter (3.18) sections. The filename `§170.315b10-Electronic-Health-Information-Export-EHI.docx.pdf` suggests a Word-to-PDF conversion error.

2. **Decent non-clinical coverage**: The export includes patient payments (33 fields), insurance (32 fields), appointments (43 fields), and consents (27 fields) — domains that repackaged clinical exports typically omit. This signals genuine (b)(10) effort.

3. **Missing lab results**: No laboratory or diagnostic results entity exists in the data dictionary, despite the patient portal referencing lab results. For an EHR product, this is a notable gap.

4. **Claims/billing detail absent**: The product advertises billing and claims management, but the export only captures patient-side payments — no claim submissions, CPT/procedure codes, charge amounts, or ERA/EOB data.

5. **Documentation has no sample data or machine-readable schema**: The single PDF contains everything. No example CSVs, no JSON schema, no lookup table definitions. A developer would need significant reverse-engineering effort.

### Summary Stats

    Coverage:        Partial
    Approach:        Purpose-built EHI export
    Export format:   CSV files in ZIP archive
    Entities:        16 documented (18 intended; 2 missing due to truncation)
    Fields:          401
    Descriptions:    99.8% (400/401 fields)
    Sample data:     No
    Bulk export:     Yes (all patients, requires practice-level permissions)
    Domains covered: 10 of 19 applicable domains (+ 3 partial)

### Bottom Line

TronsHealth made a genuine effort at (b)(10) with a purpose-built CSV export covering 16 patient data entities, but the documentation is undermined by a truncated PDF that cuts off provider notes and encounters — arguably the two most important clinical entities. Combined with missing lab results, incomplete billing data, and no sample files, the export delivers partial coverage. A patient would get demographics, medications, allergies, diagnoses, vitals, insurance, and payments, but would be missing their clinical notes, lab results, encounter history, and any claims/billing detail.
