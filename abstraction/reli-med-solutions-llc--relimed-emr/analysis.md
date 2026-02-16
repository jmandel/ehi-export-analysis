# EHI Export Analysis: ReLi Med Solutions, LLC

**Product**: ReLiMed EMR (Version 7.3)
**Analysis date**: 2026-02-16
**CHPL IDs**: 11024 (15.04.04.2990.ReLi.07.01.1.221118)

## 1. Product Context

ReLiMed EMR is a cloud-based, integrated electronic medical records and practice management system built by ReLi Med Solutions, LLC (Cary, NC; ~50 employees). It targets small to mid-size ambulatory practices — family medicine, internal medicine, pediatrics, urgent care, psychiatry/behavioral health, and FQHCs/CHCs.

The product is a single integrated platform covering:

- **Clinical documentation**: Customizable charting templates across multiple specialties, clinical decision support, health guidelines
- **E-prescribing**: CPOE for medications (certified (a)(1))
- **Lab integration**: Electronic lab ordering/results (Quest Diagnostics and others)
- **Scheduling**: Appointment scheduling, self-scheduling, kiosk check-in, automated reminders
- **Billing/claims (Practice Management)**: Integrated superbill auto-population, charge entry, multi-level claim scrubbing, automated posting, AR management, split billing for FQHCs
- **Revenue Cycle Management**: Full-service RCM offering alongside software
- **Patient portal**: Secure messaging, appointment requests, self-registration, online payments
- **Telemedicine**: Secure video visits with documentation
- **FQHC features**: UDS reporting, sliding fee schedules, specialized coding rules
- **Reporting**: UDS, quality measures, population health, productivity, revenue cycle
- **Interoperability**: HIE interfaces, immunization registry reporting, Direct messaging, FHIR API (g)(7)/(g)(9)/(g)(10))

For EHI export completeness, the baseline expectation includes: demographics, encounters, medications, allergies, diagnoses, immunizations, vitals, lab results, clinical notes, documents, billing/claims/charges/payments, insurance, referrals, patient portal messages, and specialty-specific clinical data (behavioral health, pediatrics, women's health).

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `Patient_Export_Data_File_Format.pdf` | 4-page PDF (189,921 bytes). The sole substantive documentation artifact. Lists export mechanisms, 18 XLSX worksheet names, and 8 per-patient file types. No field-level data dictionary. Created Oct 18, 2023 by Lisa Davies (COO). | **Primary** — contains all technical content |
| `kb-article-410.html` | HappyFox KB article page (37,441 bytes). Body text is a single sentence: "Please see attached file for Explanation of the File Format for a Single Patient Export and All Patients Export." Tags confirm (b)(10) scope. Last updated Aug 08, 2024. 2,347 views. | **Minimal** — wrapper only |
| `kb-article-410-screenshot.png` | Browser screenshot of the KB article page (110,515 bytes). | **Minimal** — visual confirmation only |

The PDF is the only artifact with substantive export documentation. There are no data dictionaries, schemas, sample data files, or additional technical documents. The KB article was verified as still accessible on 2026-02-16 with unchanged content.

## 3. Export Mechanics

ReLiMed provides two export paths:

### Single Patient Export
- **Format**: PDF (non-structured, rendered document)
- **Mechanism**: Self-service via UI: Patient Chart → Patient Export menu
- **Privilege required**: "Medical Record Request" user privilege
- **Capability**: Single-patient only
- **Output options**: Save, Print, or Fax
- **Selectable categories** (9): Encounters, Active Medications, Chronic Problems, Allergies, Documents, eLab Results, Patient Forms, CCD, Claims
- **Filters**: Date range (From/To), export options for Insurance, Medical History, Restricted encounter/document types

### All Patient (Bulk) Export
- **Format**: Password-protected ZIP containing XLSX workbook + per-patient document folders
- **Mechanism**: Vendor-assisted — must contact ReLi Med support team to request
- **Capability**: All patients in the system
- **Delivery**: SFTP download with dual-password security (separate SFTP and ZIP passwords)
- **Access constraints**: Not self-service; requires coordination with vendor; files have an expiration date
- **Fees**: Not documented in the export documentation (no mention of cost)

## 4. Export Content: What's In It

### Documentation limitations

**There is no field-level data dictionary.** The documentation lists only worksheet names and per-patient file types with one-sentence descriptions. No column names, data types, value sets, relationships, or sample data are documented anywhere in the 4-page PDF or KB article.

### XLSX Workbook (`patient-data-export.xlsx`)

The workbook contains 18 worksheets. The documentation provides only the worksheet name and a brief phrase describing its content. Zero fields are documented.

### Vendor's own content organization

| Entity (Worksheet/File) | Fields | Described | Types | Category |
|---|---|---|---|---|
| Locations | unknown | N/A | N/A | Practice/Reference |
| License Providers | unknown | N/A | N/A | Practice/Reference |
| Referring Providers | unknown | N/A | N/A | Practice/Reference |
| Master Insurances | unknown | N/A | N/A | Practice/Reference |
| Resources/staff members | unknown | N/A | N/A | Practice/Reference |
| Patient Employers | unknown | N/A | N/A | Patient Administrative |
| Patient Demographics | unknown | N/A | N/A | Patient Administrative |
| Patient Guarantors | unknown | N/A | N/A | Patient Administrative |
| Patient Contacts | unknown | N/A | N/A | Patient Administrative |
| Patient Pharmacies | unknown | N/A | N/A | Patient Administrative |
| Patient Insurances | unknown | N/A | N/A | Insurance |
| Past Appointments | unknown | N/A | N/A | Scheduling |
| Patient Notes | unknown | N/A | N/A | Clinical |
| Patient Alerts (Billing etc.) | unknown | N/A | N/A | Administrative |
| Patient Medications | unknown | N/A | N/A | Clinical |
| Patient Allergies | unknown | N/A | N/A | Clinical |
| Patient Diagnosis | unknown | N/A | N/A | Clinical |
| Future Appointments | unknown | N/A | N/A | Scheduling |

All 18 worksheets have zero documented fields — the documentation provides no column names, types, or descriptions for any worksheet.

### Per-patient files (Medical Records folder)

8 file types are generated per patient:

| File Pattern | Format | Description |
|---|---|---|
| `CCD.xml` | XML (C-CDA) | For viewing/importing in supported EMR systems |
| `CCD.html` | HTML | Human-readable CCD rendering |
| `Demographics_*_MedicalHistory.pdf` | PDF | Demographic and insurance snapshot |
| `MedicalHx_*_MedicalHistory.pdf` | PDF | Active meds, chronic problems, active allergies |
| `Encounter_<date>_<time>_<type>.pdf` | PDF | Encounter summaries (one per encounter) |
| `Document_<type>_<name>.pdf` | PDF | Uploaded chart documents |
| `LabResult_<date>_<time>_<guid>.pdf` | PDF | E-lab results |
| `Form_<date>_<time>_<type>_<name>.rtf` | RTF | Custom user forms |

### Screenshot evidence (single-patient export UI)

The PDF includes a screenshot of the single-patient export dialog showing a test patient (MR# 1596). The encounter list reveals encounter types used by the system: "Billing Only," "Follow Up," "Assessment/Testing," "Initial Evaluation FTF 60 min," and "No Show - Charge." Encounters have columns for Documentation count (A/S), Date, Type, Status (Open/Closed), and Provider — but none of this structural information is documented as part of the export format specification.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor organizes the bulk export into two components:

**XLSX workbook (18 worksheets)** covering:
- **Practice/Reference data** (5 worksheets): Locations, License Providers, Referring Providers, Master Insurances, Resources/staff members
- **Patient Administrative** (5 worksheets): Patient Employers, Patient Demographics, Patient Guarantors, Patient Contacts, Patient Pharmacies
- **Insurance** (1 worksheet): Patient Insurances
- **Scheduling** (2 worksheets): Past Appointments, Future Appointments
- **Clinical** (4 worksheets): Patient Notes, Patient Medications, Patient Allergies, Patient Diagnosis
- **Administrative** (1 worksheet): Patient Alerts (Billing etc.)

**Per-patient document files** (8 types) providing rendered clinical documents: CCD, demographics/insurance summary, medical history summary, encounter notes, uploaded documents, lab results, and custom forms.

The worksheets provide structured tabular data for the core administrative and basic clinical domains (demographics, medications, allergies, diagnoses, notes). The document files provide rendered (non-structured) versions of encounter details, lab results, and uploaded documents.

**Notably thin or missing from the bulk export:**
- No Claims/Billing worksheet (despite Claims being a selectable category in the single-patient export)
- No Immunizations worksheet
- No Vitals worksheet
- No Procedures worksheet
- No Referrals worksheet
- No Patient Portal/Messaging worksheet
- No structured lab results (only PDF renderings)
- No structured encounter data (only PDF renderings)

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | `Patient Demographics` worksheet (fields unknown); `Demographics_*_MedicalHistory.pdf` per patient | Worksheet exists but no field-level documentation; presumably covers basic demographics |
| Encounters / visits | ⚠️ Partial | `Encounter_<date>_<time>_<type>.pdf` per patient; `Past Appointments`, `Future Appointments` worksheets | Encounter content exported only as rendered PDFs — not structured/queryable data. Appointment worksheets may contain scheduling data but no clinical encounter detail. |
| Problems / conditions / diagnoses | ⚠️ Partial | `Patient Diagnosis` worksheet; chronic problems in `MedicalHx_*_MedicalHistory.pdf` | Worksheet exists but field coverage unknown without documentation |
| Medications / prescriptions | ⚠️ Partial | `Patient Medications` worksheet; active meds in `MedicalHx_*_MedicalHistory.pdf` | Worksheet exists but field coverage unknown; e-prescribing history not specifically mentioned |
| Allergies | ⚠️ Partial | `Patient Allergies` worksheet; active allergies in `MedicalHx_*_MedicalHistory.pdf` | Worksheet exists but field coverage unknown |
| Immunizations | ❌ Not covered | No immunization worksheet or file type in export | Product is certified for immunization registry reporting (f)(1)/(f)(2); immunization data exists in the system. **Significant gap.** |
| Vitals | ❌ Not covered | No vitals worksheet or file type in export | Vitals are likely captured during encounters. May be embedded in encounter PDFs but not as structured data. **Gap.** |
| Lab results | ⚠️ Partial | `LabResult_<date>_<time>_<guid>.pdf` per patient | Lab results exported only as rendered PDFs — not as structured data (no HL7, no discrete values). Cannot be programmatically processed. |
| Imaging / diagnostic reports | ❌ Not covered | No imaging-specific content | Product doesn't appear to have imaging capabilities beyond document storage. **N/A or minor gap.** |
| Procedures | ❌ Not covered | No procedures worksheet or file type | Procedures are likely documented in encounter notes (PDFs). No structured procedure data. **Gap.** |
| Clinical notes / documents | ✅ Covered | `Patient Notes` worksheet; `Encounter_*.pdf`; `Document_*.pdf`; `Form_*.rtf` per patient | Notes worksheet provides structured data; encounter/document/form files provide rendered content. Reasonable coverage, though encounter PDFs are non-structured. |
| Care plans / goals | ❌ Not covered | No care plan content in export | If the product supports care plans, this is a gap. Limited evidence the product has formal care plan functionality. **Likely N/A.** |
| Orders / referrals | ❌ Not covered | No orders or referrals worksheet or file type | Product has referral tracking feature. **Gap for referrals.** |
| Insurance / coverage | ✅ Covered | `Master Insurances` worksheet; `Patient Insurances` worksheet; insurance info in `Demographics_*_MedicalHistory.pdf` | Two worksheets plus per-patient rendering. Reasonable coverage. |
| Claims / billing | ❌ Not covered | No claims worksheet in bulk export | The single-patient export UI shows "Claims" as a selectable category, but the bulk XLSX has no Claims worksheet. Product prominently features integrated billing, claim scrubbing, and RCM. **Major gap.** |
| Payments | ❌ Not covered | No payments data in export | Product handles payment posting and AR management. **Gap.** |
| Consents / directives | ❌ Not covered | No consent-specific content | May be captured as uploaded documents (`Document_*.pdf`). **Minor gap or N/A.** |
| Patient communications / portal messages | ❌ Not covered | No messaging or portal content in export | Product has HIPAA-compliant secure messaging through patient portal. **Gap.** |
| Specialty-specific (behavioral health, pediatrics, women's health) | ⚠️ Partial | `Form_*.rtf` for custom forms; encounter PDFs may contain specialty templates | Specialty clinical data likely embedded in encounter PDFs and custom forms but not exported as structured data. Product specifically markets specialty templates for FQHCs. **Gap for structured specialty data.** |

**Summary**: Of 18 applicable domains, 2 are covered, 6 are partially covered, 8 are not covered, and 2 are N/A or uncertain.

## 6. Documentation Quality

The export documentation is **severely inadequate**:

- **Total documentation**: One 4-page PDF plus a one-sentence KB article wrapper
- **Data dictionary**: None. Zero fields are documented across all 18 worksheets.
- **Column names**: Not listed for any worksheet
- **Data types**: Not documented
- **Value sets / code systems**: Not documented
- **Relationships / foreign keys**: Not documented (e.g., how Patient Medications links to Patient Demographics)
- **Sample data**: None provided
- **Machine-readable schema**: None (no JSON schema, XSD, or similar)
- **Version history**: None

**Could a developer build an import from this documentation?** No. The documentation tells you that a worksheet called "Patient Medications" exists but provides no information about what columns it contains, what format medication names/codes take, whether NDC or RxNorm codes are included, how medications link to patients, or what values appear in status fields. A developer would need to reverse-engineer the entire column structure from an actual export file.

**What's well-documented**: The export *process* (how to access the export, how to download from SFTP, password handling) is described clearly. The *content* is not.

**What requires guesswork**: Everything about the actual data structure — column names, data types, relationships, value sets, coded terminology. The worksheet names give a general sense of content domains, but nothing more.

## 7. Overall Assessment

### Classification

**Partial native export** — The bulk export uses a proprietary format (XLSX workbook + per-patient document files) that appears to draw from the native data model, covering a reasonable number of domains. However, the export has significant coverage gaps (no billing/claims despite being an integrated PM system, no immunizations, no vitals, no structured encounter data) and the documentation is so thin that it's impossible to fully assess what's actually in the export without obtaining an actual data file.

### Key Findings

1. **No field-level documentation exists.** The entire export specification is a 4-page PDF listing 18 worksheet names and 8 per-patient file types with one-sentence descriptions each. Zero column names, types, or descriptions are provided for any worksheet. This is among the thinnest EHI export documentation possible — it documents the *existence* of export containers but not their *contents*. (Source: `Patient_Export_Data_File_Format.pdf`, all 4 pages)

2. **Billing/claims data is absent from the bulk export despite being a core product capability.** The single-patient export UI shows "Claims" as a selectable category, but the bulk export's XLSX workbook has no Claims, Charges, Payments, or Billing worksheet. For a product that prominently features integrated billing, claim scrubbing, automated posting, and full RCM services, this is a significant EHI gap. (Source: comparison of single-patient UI screenshot on PDF page 1 vs. bulk export worksheet list on pages 2-3)

3. **Clinical encounter content is exported only as rendered PDFs, not structured data.** Encounter notes, lab results, and medical history summaries are provided as PDF/RTF files — readable by humans but not programmatically processable. The XLSX workbook contains structured worksheets for medications, allergies, diagnoses, and notes, but not for encounter detail, vitals, or lab values. (Source: Medical Records file type list, PDF pages 3-4)

4. **Bulk export is not self-service.** Practices must contact ReLi Med's support team to request the export, which is then delivered via a password-protected ZIP on an SFTP server with an expiration date. This creates a vendor-dependency barrier for data access. (Source: "All Patient Export" section, PDF page 2)

5. **Several clinical domains present in the product are missing from the export.** Immunizations (certified for registry reporting), vitals, procedures, referrals (product has referral tracking), and patient portal messages (product has secure messaging) have no corresponding worksheets or file types in the export documentation. (Source: comparison of product features from `product-research.md` vs. export content in PDF)

### Summary Stats

```
Classification:  Partial native export
Export format:   XLSX + PDF/RTF/XML (mixed)
Model type:      Native database (XLSX worksheets), partially rendered documents (PDFs)
Entities:        18 worksheets + 8 per-patient file types
Fields:          N/A (no field-level documentation)
Descriptions:    N/A (0% — no fields documented)
Sample data:     No
Bulk export:     Yes (vendor-assisted, not self-service)
Domains covered: 2 of 18 fully, 6 partially (of ~18 applicable domains)
```

### Bottom Line

ReLiMed EMR has built a genuine (b)(10) export mechanism — not just a FHIR/C-CDA repackaging — that covers some core clinical and administrative domains through an XLSX workbook and per-patient document files. However, the documentation is among the thinnest we've seen: zero fields documented across 18 worksheets, no sample data, no schema. Combined with missing billing/claims data (despite integrated PM capabilities), no structured encounter or lab data, and vendor-gated bulk access, a patient or provider receiving this export would get a partial picture of their data with no documentation to interpret the structured portions and no way to programmatically process the rendered clinical documents.
