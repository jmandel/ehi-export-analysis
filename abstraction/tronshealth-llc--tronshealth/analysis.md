# EHI Export Analysis: TronsHealth LLC

**Product**: TronsHealth  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.05.05.3209.TRON.00.00.1.241213  

## 1. Product Context

TronsHealth is a cloud-based ambulatory EHR and practice management system developed by TronsHealth LLC (Austin, TX), a subsidiary of Tronsit Solutions LLC. It received its first ONC certification on December 13, 2024 (version 1.0), making it an extremely new entrant with no publicly known customer base.

The product is positioned as an integrated platform covering:

- **EHR**: Clinical documentation via customizable templates, clinical decision support, e-prescribing, vital signs capture via medical device integration, secure messaging
- **Practice Management**: Appointment scheduling, real-time insurance eligibility verification, billing and claims management, financial analytics
- **Patient Engagement**: Patient portal (medical records, lab results, appointment scheduling, prescription refills), appointment reminders, secure provider-patient messaging, digital check-in
- **Credentialing**: NPI enrollment, provider credentialing, payer verification

Certified criteria include CPOE for medications (a)(1), demographics (a)(5), implantable device list (a)(14), transitions of care (b)(1), EHI export (b)(10), and FHIR API access (g)(10). The target users are ambulatory physicians, nurse practitioners, surgeons, clinicians, and administrative staff.

For EHI export completeness, the baseline expectation includes: patient demographics, clinical documentation (encounters, notes), medications, allergies, diagnoses, immunizations, vitals, lab results, insurance/coverage, billing/claims, patient payments, appointments, secure messages, and any specialty clinical data.

## 2. Artifacts Reviewed

| Artifact | Description | Informative Value |
|---|---|---|
| `170.315b10-Electronic-Health-Information-Export-EHI.pdf` (739 KB, 27 pages) | Primary EHI export documentation: regulatory overview (pp. 4–5), step-by-step export UI instructions with screenshots (pp. 5–9), data dictionary for 16 entities (pp. 9–27). **Truncated** — TOC lists 18 sections but only 16 are present. | **Primary source** — contains the entire data dictionary |
| `enrichment/data-dictionary.json` (72 KB) | Structured JSON extraction of all 16 data dictionary tables from the PDF, with 401 total fields | **Most useful** — machine-readable parse of the PDF tables |
| `enrichment/extraction-stats.json` (1.9 KB) | Entity counts, field counts, missing section list | Useful summary, verified against own analysis |
| `enrichment/extract-data-dictionary.ts` (9.6 KB) | Bun TypeScript extraction script | Context on extraction methodology |

No sample data files, no JSON schemas, no ZIP file examples, and no additional documentation beyond the single PDF were available.

## 3. Export Mechanics

- **Format**: CSV files bundled in a ZIP archive
- **Mechanism**: Web UI — users navigate to a dedicated "Electronic Health Information Export" menu item in the sidebar, select a patient or choose "all patients," and click "Export" to download a ZIP file
- **Single-patient**: Yes — select from a patient list popup
- **Bulk/all-patient**: Yes — "Click here to download all Patient's Health Information" option, requires practice-level permissions
- **Access constraints**: Restricted to authorized/admin-level users; practice-level permissions required for all-patient export
- **Fees**: Not mentioned in documentation

The PDF includes 6 screenshots (Figs 3.1–2.10, with inconsistent numbering) showing the actual TronsHealth UI for the export workflow. The process appears straightforward — approximately 5 clicks from login to download.

## 4. Export Content: What's In It

The data dictionary documents **16 entities with 401 total fields**. The TOC lists 18 entities but 2 are missing from the document (see below). Every field has a data type. 400 of 401 fields (99.8%) have text descriptions — the single exception is `Consent.Type` (varchar), which has a blank description in the PDF.

Descriptions are brief but functional (e.g., "The patient's given name," "A scale or measure used to assess the intensity or severity of a patient's pain"). Data types are generic SQL-like types: varchar (234), datetime (57), long (54), boolean (36), int (10), nvarchar (3), decimal (3), bool (1), list (1), file (1), string (1).

No foreign key relationships are formally documented, though many fields reference IDs from other entities (e.g., `PatientID`, `AppointmentID`, `ProviderNoteID`). No value sets or lookup table definitions are provided — numerous fields ending in "LookupID" or "LookupName" reference undocumented lookup tables. No sample data is provided.

### Vendor's own content organization

All entities follow a "Patient – [Category]" naming convention. Each entity includes standard audit fields: `CreatedBy`, `CreatedOn`, `ModifiedBy`, `ModifiedOn`, `IsDeleted`, `UUID`.

| Entity | Section | Fields | Described | Types | Notes |
|---|---|---|---|---|---|
| Patient – Demographics | 3.1 | 52 | 52 | ✅ | Names, DOB, SSN, address, race, ethnicity, language, gender identity, sexual orientation, alt address, wallet balance |
| Patient – Medications | 3.2 | 28 | 28 | ✅ | NDC, RxNorm codes, brand/generic names, sig, strength, form, route, prescriber |
| Patient – Allergies | 3.3 | 25 | 25 | ✅ | Allergy name/type, RxNorm, NDC, reactions, severity, criticality, verification status |
| Patient – Appointments | 3.4 | 43 | 43 | ✅ | Scheduling details, status, provider, insurance refs, check-in/out times, copay, reason |
| Patient – Complaints | 3.5 | 18 | 18 | ✅ | Chief complaints with SNOMED/ICPC-2 codes, type, duration |
| Patient – Diagnosis | 3.6 | 15 | 15 | ✅ | SNOMED/ICD-10/ICD-9 codes, verification status, linked to appointment |
| Patient – Documents & Images | 3.7 | 1 | 1 | ✅ | Files exported in native format (PNG, JPEG, JPG) — only 1 field (FilePath) |
| Patient – Immunization | 3.8 | 13 | 13 | ✅ | Vaccine code, amount administered, route, dates |
| Patient – Insurances | 3.9 | 32 | 32 | ✅ | Member ID, payer ID, policy dates, eligibility, copay, insured party info |
| Patient – Contact | 3.10 | 22 | 22 | ✅ | Emergency/related contacts with relationship, address, phone |
| Patient – Consent | 3.11 | 27 | 26 | ✅ | Consent type, status, validity period, custodian party, attached documents |
| Patient – Education | 3.12 | 12 | 12 | ✅ | Educational level, disability status |
| Patient – Patient Notes | 3.13 | 16 | 16 | ✅ | Subject, priority, follow-up date, recall, note status (administrative notes) |
| Patient – Payments | 3.14 | 33 | 33 | ✅ | Credit card, check, cash payments; wallet balance; transaction details |
| Patient – Social History | 3.16 | 16 | 16 | ✅ | Tobacco use: status, type, frequency, duration, quit intent |
| Patient – Vitals | 3.17 | 48 | 48 | ✅ | Height, weight, BP, pulse, respiration, temperature, O2 saturation, pain severity, blood type, urine output, and more |
| **Patient – Provider Note** | **3.15** | **—** | **—** | **—** | **MISSING: Listed in TOC (page 27) but absent from PDF** |
| **Patient – Encounter** | **3.18** | **—** | **—** | **—** | **MISSING: Listed in TOC (page 32) but absent from PDF — document only has 27 pages** |

**Totals (documented entities only)**: 16 entities, 401 fields, 400 with descriptions (99.8%), 401 with types (100%).

The full entity inventory with all 401 fields is saved to `analysis/full-entity-inventory.json`.

### Missing sections analysis

The TOC lists section 3.15 "Patient – Provider Note" at page 27 and section 3.18 "Patient – Encounter" at page 32. The document ends at page 27 (which is blank except for the copyright footer). The section numbering is non-sequential (3.14 → 3.16, skipping 3.15; 3.17 → end, with 3.18 expected beyond the document's length). The filename `§170.315b10-Electronic-Health-Information-Export-EHI.docx.pdf` suggests the PDF was converted from a Word document — the conversion likely truncated the output.

These are arguably the two most critical clinical entities. Provider notes contain clinical narratives (progress notes, H&P, etc.), and encounters tie together all clinical data for a visit. Their absence is a significant documentation gap.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export covers 16 patient-centric data entities spanning demographics, clinical, financial, and administrative domains. In the vendor's own organization:

**Richest entities** (most fields):
- Demographics (52 fields) — comprehensive, includes USCDI-required elements like race, ethnicity, language, gender identity, sexual orientation
- Vitals (48 fields) — unusually thorough, includes cuff size, blood type, urine output, resting metabolic rate
- Appointments (43 fields) — detailed scheduling with insurance references and copay

**Clinical data**: Medications (28 fields with NDC/RxNorm), Allergies (25 fields with RxNorm/NDC, severity, criticality), Diagnosis (15 fields with ICD-10/ICD-9/SNOMED), Immunization (13 fields), Complaints (18 fields with SNOMED/ICPC-2), Social History (16 fields — tobacco only), Vitals (48 fields)

**Administrative/financial**: Insurances (32 fields), Payments (33 fields — credit card, check, cash transactions), Appointments (43 fields)

**Other**: Contact (22 fields — emergency/related contacts), Consent (27 fields), Education (12 fields), Patient Notes (16 fields — administrative notes, not clinical notes), Documents & Images (1 field — file path only)

**Thinnest entity**: Documents & Images (1 field — `FilePath`). Files are exported in native format but with no metadata (document type, date, author, description).

**Key limitation**: Social History only covers tobacco use. Other social determinants (alcohol, drug use, housing, employment) are absent.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient – Demographics` (52 fields): names, DOB, SSN, address, race, ethnicity, language, gender identity, sexual orientation, alternate address | Thorough; includes USCDI v1 required elements |
| Encounters / visits | ❌ Not covered | `Patient – Encounter` (section 3.18) listed in TOC but missing from document | **Critical gap** — product stores encounters; truncated PDF omits this section |
| Problems / conditions / diagnoses | ✅ Covered | `Patient – Diagnosis` (15 fields): SNOMED, ICD-10, ICD-9 codes, verification status, appointment linkage | Adequate; covers coded diagnoses |
| Medications / prescriptions | ✅ Covered | `Patient – Medications` (28 fields): NDC, RxNorm, brand/generic names, sig, strength, form, route, prescriber | Good coverage with standard coding |
| Allergies | ✅ Covered | `Patient – Allergies` (25 fields): RxNorm, NDC, reactions, severity, criticality, verification status | Well-documented with standard codes |
| Immunizations | ✅ Covered | `Patient – Immunization` (13 fields): vaccine code, amount, route, dates | Adequate |
| Vitals | ✅ Covered | `Patient – Vitals` (48 fields): height, weight, BP, pulse, respiration, temperature, O2 saturation, pain, blood type, urine output | Unusually thorough |
| Lab results | ❌ Not covered | No lab-related entity in data dictionary | **Significant gap** — patient portal references "lab results," implying the product stores them |
| Imaging / diagnostic reports | ⚠️ Partial | `Patient – Documents & Images` (1 field: file path); native format export of image files | Images exported but no structured metadata; no radiology reports |
| Procedures | ❌ Not covered | No procedures entity | Gap if product tracks procedures beyond what's in encounter notes |
| Clinical notes / documents | ❌ Not covered | `Patient – Provider Note` (section 3.15) listed in TOC but missing from document; `Patient Notes` (section 3.13) is administrative notes, not clinical documentation | **Critical gap** — provider clinical notes are core EHI; truncated PDF omits this section |
| Care plans / goals | ❌ Not covered | No care plan entity | Uncertain if product stores structured care plans |
| Orders / referrals | ❌ Not covered | No orders entity; CPOE (a)(1) certified but no order data in export | Gap — product is certified for CPOE medications |
| Insurance / coverage | ✅ Covered | `Patient – Insurances` (32 fields): member ID, payer ID, policy dates, eligibility, copay, insured party | Good coverage of coverage/enrollment |
| Claims / billing | ⚠️ Partial | `Patient – Payments` (33 fields) covers patient-side payments (credit card, check, cash, wallet) | Missing: CPT/HCPCS codes, claim submissions, ERA/EOB, charge amounts, claim status. Product has billing/claims module |
| Payments | ✅ Covered | `Patient – Payments` (33 fields): transaction details for credit card, check, cash, wallet deposits | Covers patient-facing payment transactions |
| Consents / directives | ✅ Covered | `Patient – Consent` (27 fields): type, status, validity period, custodian party, document attachment | Reasonable consent tracking |
| Patient communications / portal messages | ❌ Not covered | No messaging entity | **Gap** — product has secure messaging between providers and patients |
| Chief complaints | ✅ Covered | `Patient – Complaints` (18 fields): SNOMED/ICPC-2 coded complaints | Coded chief complaints with linkage to appointments |

**Summary**: 9 of 18 applicable domains are covered, 2 partial, 7 not covered. Two of the most critical missing domains (Provider Note and Encounter) appear to be intended for inclusion but were lost to document truncation.

## 6. Documentation Quality

**Strengths:**
- Field-level data dictionary with name, type, and description for nearly every field (400/401)
- Clear step-by-step export instructions with UI screenshots
- Standard coding systems referenced (ICD-10, ICD-9, SNOMED, RxNorm, NDC)
- Every entity includes audit trail fields (CreatedBy, CreatedOn, ModifiedBy, ModifiedOn, IsDeleted, UUID)
- Supports both single-patient and bulk export

**Weaknesses:**
- **Truncated document** — the two most important clinical sections (Provider Note, Encounter) are missing, likely due to a Word-to-PDF conversion error
- No sample data files or example CSV output
- No documentation of ZIP file structure (folder hierarchy, file naming conventions)
- Numerous "LookupID" fields reference undocumented internal lookup tables — a developer cannot interpret these values without the lookup definitions
- No value set documentation for coded fields beyond naming the coding system
- No formal relationship/foreign key documentation (though cross-entity IDs are recognizable)
- No CSV dialect specification (delimiter, quoting, escaping, encoding, date format)
- No versioning or change history

A developer could understand the general shape of the export from this documentation, but could not build a reliable import without: (1) the missing sections, (2) lookup table definitions, and (3) sample data showing actual CSV format. The lookup table issue is particularly problematic — fields like `SuffixLookupID`, `GenderLookupId`, `FrequencyLookupID`, `DisabilityLookupID`, `ConsentTypeLookupID`, `StatusLookupID` are opaque without their value mappings.

## 7. Overall Assessment

### Classification

**Partial native export**: The export uses the vendor's native data model (CSV files from internal tables), which is the right approach for (b)(10). However, the documentation is truncated (missing 2 of 18 entities that were clearly planned), and several important data domains (lab results, claims detail, clinical notes, secure messages, orders) are absent. The 16 documented entities cover demographics, basic clinical data, insurance, and payments, but the gaps are significant relative to what the product stores.

### Key Findings

1. **Truncated PDF is the biggest issue.** The document's TOC lists 18 entities but only 16 are present. The two missing entities — Provider Note (section 3.15) and Encounter (section 3.18) — are arguably the most critical clinical data types. The filename (`*.docx.pdf`) suggests a Word-to-PDF conversion error. This is a documentation failure, not necessarily an export failure — the actual export may include these entities.

2. **Lab results are absent with no explanation.** The patient portal references lab results, and the product is a full ambulatory EHR, yet no lab-related entity appears in the data dictionary or TOC. This appears to be a genuine coverage gap, not a truncation artifact.

3. **Good field-level documentation for what's present.** 400 of 401 fields have descriptions, all have types, and standard coding systems (ICD-10, SNOMED, RxNorm, NDC) are referenced. The data dictionary quality for the documented entities is above average.

4. **Claims/billing depth is thin.** The product has a billing/claims module, but the export only includes patient-side payment transactions (credit card, check, cash). No CPT codes, claim submissions, ERA/EOB data, or charge-level detail appears.

5. **Undocumented lookup tables undermine usability.** Dozens of fields reference "LookupID" values with no value set definitions. Without lookup tables, many fields in the export are uninterpretable.

### Summary Stats

```
Classification:  Partial native export
Export format:   CSV files in ZIP archive
Model type:      Native database tables
Entities:        16 documented (18 in TOC, 2 missing due to truncation)
Fields:          401
Descriptions:    99.8% (400 of 401 fields)
Sample data:     No
Bulk export:     Yes (all patients, requires practice-level permissions)
Domains covered: 9 of 18 applicable domains (+ 2 partial)
```

### Bottom Line

TronsHealth has built a genuine (b)(10) export using native CSV data — not a repackaged FHIR or C-CDA endpoint — which is the right structural approach. However, the truncated PDF removes documentation for the two most important clinical entities (provider notes and encounters), lab results are entirely absent, and claims/billing data is limited to patient payments. A patient receiving this export would get demographics, medications, allergies, diagnoses, vitals, insurance, and payment records, but would likely be missing their clinical notes, encounter history, and lab results — core components of a complete health record.
