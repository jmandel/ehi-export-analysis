# EHI Export Analysis: Claimpower, Inc.

**Product**: Claimpower Mobile EMR v6.1
**Analysis date**: 2026-02-15
**CHPL ID**: 15.04.04.1238.Clai.06.02.1.230109 (internal ID 11209)

## 1. Product Context

Claimpower, Inc. is a small, family-run healthcare IT company based in Glen Rock, New Jersey, founded in 1992. Its **primary business is managed medical billing services** for small physician practices — the EHR is bundled free with billing services and is not sold standalone. The company serves "hundreds of doctors" in small practices across multiple specialties.

The Claimpower Mobile EMR is a cloud-based, mobile-friendly system certified under ONC's 2015 Edition Cures Update. The platform integrates:

- **Clinical documentation**: Problem lists, medication lists, allergy lists, clinical notes with Dragon dictation, lab integration, ePrescribing, family health history, immunizations, implantable device list
- **Practice management**: Patient scheduling, real-time eligibility checking, patient balances, payment collection, customizable superbills, document scanning/indexing
- **Billing services** (managed by Claimpower staff): Daily electronic claims submission, claim scrubbing, CPT/ICD-10 coding, ERA/EOB posting, denial management, collections
- **Patient engagement**: Patient portal with secure messaging, text messaging for recalls
- **Quality reporting**: MIPS submission, CQM reporting, CCM and TCM support

The billing and practice management data are particularly relevant for EHI assessment because billing is Claimpower's core business — a (b)(10) export that omits billing data from a billing-first company represents a major gap.

## 2. Artifacts Reviewed

| Artifact | Size | Pages | Description | Informativeness |
|---|---|---|---|---|
| `CCDA_Export.PDF` | 1,063,362 bytes | 9 | Main document: index page + all three sub-documents inline. Contains all screenshots. | **Primary artifact** — only source of technical detail |
| `CCDA_Export_Single_Patient.PDF` | 511,961 bytes | 3 | Single-patient C-CDA export walkthrough (7 steps with screenshots) | Redundant — subset of main PDF |
| `CCDA_Multiple_Patients.PDF` | 271,425 bytes | 2 | Multi-patient export walkthrough (4 steps). Shows patient list of 12,217 patients. | Redundant — subset of main PDF |
| `CCDA_Patient_Portal.PDF` | 396,625 bytes | 3 | Patient portal export walkthrough (6 steps with screenshots) | Redundant — subset of main PDF |

**Total**: 4 PDF files, 2,243,373 bytes, 17 pages. All authored by Rohan Thadani (CEO) on **2023-08-28** using Microsoft Word. Extractable text totals only **3,462 characters across all 4 files** — the documents are almost entirely screenshots with minimal text.

The main PDF (`CCDA_Export.PDF`) is the only artifact that matters; the three sub-PDFs are exact subsets. There are **no data dictionaries, no schemas, no sample export files, no field definitions, no API documentation**.

## 3. Export Mechanics

- **Format**: C-CDA (Consolidated Clinical Document Architecture) XML, packaged as ZIP files
- **Mechanism**: UI-based — three paths available:
  1. **Single patient** (via EMR): Lookup Medical Records → select patient → Clinical Document → Summary of Care Records → Generate CCDA → Download ZIP
  2. **Multiple patients / bulk** (via EMR Reports): EMR Reports → Export Patient Health Records → select patients (or "All Patients" checkbox — screenshot shows 12,217 patients) → Generate ZIP
  3. **Patient self-service** (via Patient Portal): Patient Portal login → View Health Information → Summary of Care Records → Download ZIP
- **Single-patient**: Yes, via paths 1 and 3
- **Bulk**: Yes, via path 2 (supports selecting all patients)
- **Access constraints**: EMR export requires staff login. Patient portal requires 3-digit client ID, patient name, DOB, and 4-digit password.
- **Fees**: Not mentioned in documentation. EMR is bundled with billing services (no additional cost for core EMR per mandatory disclosures).

## 4. Export Content: What's In It

### Format and Structure

The export is a **C-CDA "Summary of Care" document** — a standardized clinical summary. This is the same document type used for transitions of care under 170.315(b)(1)/(b)(2), now being reused for the (b)(10) EHI export requirement.

### What's Visible in the Export

The documentation contains no data dictionary, no field lists, and no sample files. The only evidence of export content comes from **two screenshots** showing the C-CDA Summary of Care rendered in the Claimpower viewer:

**Screenshot 1** (page 4, single-patient path): Shows C-CDA header fields in a blue table:
- Patient name, date of birth, sex, preferred language
- Contact info (address, phone)
- Document ID, document creation date
- Performer, author, authenticator
- Encounter ID, encounter dates, encounter location
- Responsible party, personal relationships
- Contact info for provider
- Legal authenticator with signature timestamp

**Screenshot 2** (page 8, patient portal "View Health Information"): Shows expandable sections:
1. Patient Demographics
2. Provider Details
3. Patient Medical Documents
4. Allergies
5. Medications
6. Problems
7. Procedures
8. Vital Signs
9. Encounters
10. Social History
11. Family History
12. Results (Discrete)

These are **standard C-CDA sections** — essentially the USCDI/US Core clinical data set. There are **12 sections visible**, which aligns with a typical C-CDA Summary of Care Record.

### What's NOT in the Export

There is **no evidence** that the export contains any data beyond the standard C-CDA sections listed above. The following data domains — all stored by the product — are absent:

- **Billing/claims data**: No claims, CPT/ICD codes, ERA/EOB records, denial/appeal data
- **Payment records**: No patient payments, credit card transactions, balances
- **Insurance/eligibility data**: No insurance plan info (despite being visible in patient search — e.g., "Aetna HMO", "Aetna PPO")
- **Scanned/attached documents**: No digitized paper charts, uploaded images
- **Secure messages**: No provider-to-patient or provider-to-provider messages
- **Orders/referrals**: No CPOE orders beyond what's implied in the encounter
- **Care plans**: No CCM/TCM care plan data
- **Scheduling/appointment data**: Not in C-CDA
- **Superbills/encounter forms**: Not representable in C-CDA

### No Data Dictionary

There are zero field-level definitions anywhere in the documentation. No table names, no column names, no data types, no value sets, no foreign keys, no cardinality constraints. The documentation is purely a screenshot-based UI walkthrough.

## 5. Coverage Assessment

| Domain | Product Stores? | Export Coverage | Evidence |
|---|---|---|---|
| Demographics | Yes | **Covered** | C-CDA Patient Demographics section visible (page 8) |
| Problems / Diagnoses | Yes | **Covered** | C-CDA Problems section visible; ICD codes in screenshot (page 3) |
| Allergies | Yes | **Covered** | C-CDA Allergies section visible (page 8) |
| Vital Signs | Yes | **Covered** | C-CDA Vital Signs section visible (page 8) |
| Procedures | Yes | **Covered** | C-CDA Procedures section visible (page 8) |
| Family Health History | Yes | **Covered** | C-CDA Family History section visible (page 8) |
| Social History | Yes | **Covered** | C-CDA Social History section visible (page 8) |
| Medications / Prescriptions | Yes | **Partially covered** | C-CDA Medications section present, but detailed Rx data (refill history, pharmacy info, prior auth) likely absent |
| Lab Results | Yes | **Partially covered** | C-CDA Results (Discrete) section present, but structured lab data beyond C-CDA may exist (Labs Filed Report in menu) |
| Clinical Notes / Documents | Yes | **Partially covered** | C-CDA Patient Medical Documents section present, but rich dictated notes and custom templates unlikely to be fully represented |
| Encounters / Visits | Yes | **Partially covered** | C-CDA Encounters section present, but likely summary-level only |
| Immunizations | Yes | **Uncertain** | Not visible in portal section list; separate Immunization Export Report exists in EMR Reports menu |
| Implantable Devices | Yes | **Uncertain** | Certified for (a)(14) but no evidence in C-CDA export sections |
| Care Plans / Goals | Yes | **Not covered** | CCM/TCM are separate modules; no care plan section in C-CDA export |
| Insurance / Coverage | Yes | **Not covered** | Insurance data visible in patient search but not in C-CDA |
| Claims / Billing | Yes | **Not covered** | Core business; multiple billing reports visible in menu (Billing Sent, Billing Stats, Daily Office Collection); none in C-CDA |
| Payments | Yes | **Not covered** | Patient Payments is a website feature; ERA/EOB posting is core workflow; not in C-CDA |
| Patient Communications | Yes | **Not covered** | Secure Messaging visible in portal (page 8); not in C-CDA |
| Scanned / Attached Documents | Yes | **Not covered** | Attach Documents icon on dashboard; document indexing is a paid feature; not in C-CDA |
| Orders / Referrals | Yes | **Not covered** | CPOE certified under (a)(1); not in C-CDA Summary of Care |

**Summary**: Of 20 EHI-relevant data domains the product stores, **7 are covered** (35%), **4 are partially covered** (20%), **7 are not covered** (35%), and **2 are uncertain** (10%). The combined covered + partially covered rate is **55%**.

The most significant gap is **billing and claims data** — the company's primary business. A billing-services company whose EHI export contains zero billing data is a serious (b)(10) compliance concern.

## 6. Documentation Quality

The documentation quality is **extremely poor**:

- **No data dictionary**: Zero field-level documentation. No table names, column names, data types, value sets, or relationships.
- **No schema**: No machine-readable format specification. The only format information is "C-CDA."
- **No sample files**: No example C-CDA documents are provided.
- **No API documentation**: The export is UI-only; there is no programmatic access method described.
- **Content**: 17 pages across 4 PDFs, but the documents are almost entirely **screenshots** with brief step-by-step captions. The extractable text across all 4 files totals only **3,462 characters** — less than a single page of prose.
- **Authorship**: All 4 PDFs were created on the **same day** (2023-08-28) by the CEO (Rohan Thadani) using Microsoft Word, suggesting they were produced specifically for certification with minimal effort.
- **Technical depth**: Zero. The documentation tells you which buttons to click, not what data comes out.
- **Developer usability**: A developer receiving this export would have to reverse-engineer the C-CDA structure entirely from the raw XML. The documentation provides no guidance on what sections are populated, what coded values are used, or how to interpret the data.
- **Typo in URL**: The single-patient PDF filename is misspelled as "CCDA_Export_**Signle**_Patient.PDF"

## 7. Overall Assessment

### Classification

**Standard-based projection** — The (b)(10) EHI export is a C-CDA Summary of Care document, which is a standard clinical summary format. This is functionally identical to the transitions-of-care export required under (b)(1)/(b)(2). It covers standard clinical data domains (demographics, problems, meds, allergies, vitals, procedures, results) but completely omits the vendor's native data model, billing/claims data, practice management data, communications, and scanned documents.

### Key Findings

1. **The export is a C-CDA repackaging, not a genuine EHI export.** The vendor's (b)(10) documentation describes the exact same C-CDA Summary of Care export used for transitions of care. The document title is literally "CCDA Export" — not "EHI Export" or "Electronic Health Information Export." This covers roughly 12 standard clinical sections but misses entire data domains.

2. **Billing data — the company's core business — is completely absent.** Claimpower is fundamentally a billing services company. Their EMR dashboard shows Billing, Speed Billing, and billing-related reports (Billing Sent Report, Billing Stats Report, Daily Office Collection Report). Yet the export contains zero billing, claims, payment, or insurance data. For a billing-first company, this is the single largest gap.

3. **Documentation is a compliance checkbox, not a technical resource.** The entire documentation is 4 screenshot-walkthrough PDFs totaling 3,462 characters of extractable text, created in a single day by the CEO. There is no data dictionary, no schema, no sample data, no field definitions. A developer or patient receiving this export would have no documentation to interpret it.

4. **7 of 20 data domains (35%) are not covered at all.** Beyond billing, the export also omits insurance/coverage data, patient communications, scanned documents, care plans, and orders/referrals — all data types the product demonstrably stores.

5. **Bulk export capability exists but is clinically limited.** The multi-patient export path (EMR Reports → Export Patient Health Records) supports selecting all patients (screenshot shows 12,217 patients), which is positive for the (b)(10) bulk requirement. However, the exported content per patient is the same limited C-CDA Summary of Care.

### Bottom Line

A patient or provider would receive a **clinical summary** from this export — demographics, problem list, meds, allergies, vitals, procedures, and lab results in standard C-CDA format. They would **not** receive their billing history, claims, payments, insurance data, secure messages, scanned documents, care plans, or orders — all of which Claimpower stores and which constitute a significant portion of the designated record set. For a company whose primary business is billing, the complete absence of billing data from the EHI export is a particularly notable gap.
