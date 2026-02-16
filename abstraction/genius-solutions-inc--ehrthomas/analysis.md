# EHI Export Analysis: Genius Solutions Inc.

**Product**: ehrTHOMAS  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.05.05.2737.GENI.01.00.1.180802 (CHPL ID 9585)

## 1. Product Context

ehrTHOMAS is an ONC-certified ambulatory EHR developed by Genius Solutions Inc. (Warren, MI), a small vendor (~51–200 employees) serving primarily **chiropractic, podiatry, PT/OT, and general medicine** practices. The product is paired with **eTHOMAS**, a practice management and billing system. Together they form the "Total Health Office Management Automation System" (THOMAS).

**Data domains the product stores** (per product-research.md and certified criteria):
- **Clinical**: Demographics, problem lists, medication lists, medication allergies, vital signs, immunizations, clinical notes/encounter documentation (via touch-screen templates and WritePad module), lab orders/results (Quest integration), diagnostic imaging attachments, clinical decision support alerts, devices, procedures, care plans
- **Billing/Administrative**: Appointment scheduling, insurance verification, electronic claims, billing/insurance ledgers, patient statements, remittance posting, online payments, inventory, referral tracking, financial reports
- **Patient Portal**: Patient access to clinical records (historically HealthVault-based)
- **E-Prescribing**: Electronic prescribing including EPCS via DrFirst
- **Specialty Content**: DRxContent™ podiatry-specific templates; specialty-specific templates for chiropractic, PT/OT
- **Interoperability**: C-CDA transitions of care, FHIR APIs, HL7 interface

This is a product with meaningful billing/PM capabilities and specialty-specific clinical content that should be reflected in a comprehensive EHI export.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/ehi-export-page.html` (25 KB) | **Primary artifact.** Single HTML page containing all EHI export documentation: introduction, security notes, how-to instructions with screenshots, and XML sample snippets for 8 data domains. References §170.315(b)(10). | **Most informative** — this is the entirety of the vendor's EHI documentation |
| `downloads/EHI_Export1.jpg` (160 KB) | Screenshot of ehrTHOMAS Reports Menu showing the "Electronic Health Information (Export)" button location | Moderately informative — confirms export is a UI feature accessible from Reports menu |
| `downloads/EHI_Export2.jpg` (218 KB) | Screenshot of single-patient export dialog showing Export Folder Path, patient search, and Export button | Moderately informative — confirms single-patient export with file system output |
| `downloads/EHI_Export3.jpg` (177 KB) | Screenshot of all-patients (bulk) export dialog | Moderately informative — confirms bulk export option exists |
| `downloads/screenshot-ehi-export-full-page.png` (1.2 MB) | Full-page browser screenshot of the HTML documentation page | Low informativeness — duplicate of HTML content |

**No data dictionary, schema file, or sample export data files were provided.** The only documentation of export content is the 8 XML sample snippets embedded in the HTML page.

## 3. Export Mechanics

- **Format**: XML files
- **Mechanism**: UI button in the Reports module of ehrTHOMAS. User logs in with "full rights or as system administrator," navigates to Reports → "Electronic Health Information (Export)"
- **Single-patient**: Select "Single Patient" from Export Type dropdown, search by Last Name or Account Number, click Export. Output goes to a local folder path (screenshot shows `C:\Users\...\EHRElectronicHealthInformation\02`)
- **Bulk export**: Select "All Patients (Entire Database)" from Export Type dropdown, click Export. Documentation notes this "may require support from the health IT developer"
- **Access constraints**: Users must have export rights or use system administrator access
- **Fees**: Not mentioned in documentation

## 4. Export Content: What's In It

The entire export documentation consists of XML sample snippets for **8 data domains** with a total of **96 unique fields**. There is **no data dictionary** — no field descriptions, no type definitions (beyond a few `type="date"` XML attributes), no value sets, no foreign key documentation, no cardinality constraints.

The documentation states: "The EHI export file(s) will be in xml format. Each resource will have the following xml data set."

### Vendor's own content organization

The vendor organizes the export into 8 "Datasets" presented as XML sample snippets:

| Entity/Table | Fields | Described | Types Documented | Category (vendor's) |
|---|---|---|---|---|
| Patient | 22 | 0 | 1 (BirthDate) | Patient Dataset |
| Encounter | 10 | 0 | 2 (VisitDate, DischargeDate) | Encounter Dataset |
| Device | 11 | 0 | 3 (ManufactureDate, ExpirationDate, ImplantedDate) | Device Dataset |
| Immunization | 7 | 0 | 1 (DateAdministered) | Immunization Dataset |
| Allergy | 7 | 0 | 1 (RecordedDate) | Allergy Dataset |
| Procedure | 9 | 0 | 3 (RequestedTime, ProcedureStartTime, ProcedureEndTime) | Procedure Dataset |
| Vital | 21 | 0 | 1 (TimeRecorded) | Vital Dataset |
| Condition | 9 | 0 | 0 | Condition Dataset |
| **TOTAL** | **96** | **0** | **12** | |

**Key observations about the XML samples:**
- **No field descriptions at all** — field names are the only documentation. A developer would have to guess at semantics based on element names and sample values.
- **Only 12 of 96 fields have explicit type annotations** (all `type="date"` or `type="time"`). The remaining 84 fields have no type information.
- **92 of 96 fields have sample values**, which provide some implicit documentation.
- **The samples appear to show USCDI-aligned clinical data only.** The 8 entities map directly to standard USCDI data classes: Patient → Demographics, Encounter → Encounters, Condition → Problems, etc.
- **Notable data quality issues in samples**: The Encounter sample shows "1234567897" as the value for LastName, FirstName, MidInitial, and TaxonomyCode (copy-paste of NPI into all fields). The Condition sample shows what appears to be a GUID (`f1f0bd65-a248-4930-b981-2531ed4fcd93`) in the ICD10Code field rather than an actual ICD-10 code.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export covers exactly **8 clinical data domains**, all of which align with standard USCDI data classes:

1. **Patient** (22 fields) — Basic demographics including name, DOB, gender, contact info, address, race, ethnicity, language, marital status. No insurance information, no emergency contacts, no preferred pharmacy.
2. **Encounter** (10 fields) — Visit date, discharge date, performing doctor (NPI, name, taxonomy). Very thin — no encounter type, no reason for visit, no facility information.
3. **Device** (11 fields) — UDI data: manufacture date, expiration, lot/serial numbers, device identifier, SNOMED code. Reasonable for devices.
4. **Immunization** (7 fields) — CVX code, lot number, date administered. No site, route, manufacturer, or administering provider.
5. **Allergy** (7 fields) — SNOMED code, clinical status, reaction, recorded date. No severity, no onset, no category.
6. **Procedure** (9 fields) — CPT code, description, status, start/end times. No performing provider, no body site, no notes.
7. **Vital** (21 fields) — Temperature, BP, pulse, respiration, SpO2, FiO2, height, weight, BMI. The richest entity; includes units. But no head circumference, no smoking status, no pain scale.
8. **Condition** (9 fields) — ICD-10 code, clinical status, verification status, onset date, comment. Reasonably structured.

**Entirely absent**: Medications/prescriptions, lab results, clinical notes/documents, care plans, goals, orders/referrals, insurance/coverage, billing/claims, payments, patient communications, specialty-specific data (chiropractic, podiatry, PT/OT templates), imaging reports, family history, social history.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | `Patient` entity (22 fields): name, DOB, gender, address, race, ethnicity, language, marital status | Missing: insurance info, emergency contacts, preferred pharmacy. Covers basics but thin |
| Encounters / visits | ⚠️ Partial | `Encounter` entity (10 fields): dates, performing doctor | Very thin — no encounter type, reason, facility, diagnosis linkage |
| Problems / conditions | ✅ Covered | `Condition` entity (9 fields): ICD-10, status, verification, onset | Adequate for basic problem list |
| Medications / prescriptions | ❌ Not covered | No medication entity | **Significant gap** — product has e-prescribing (EPCS via DrFirst), medication lists, drug interaction checking |
| Allergies | ✅ Covered | `Allergy` entity (7 fields): SNOMED, status, reaction | Basic but present |
| Immunizations | ✅ Covered | `Immunization` entity (7 fields): CVX, lot, date | Basic but present |
| Vitals | ✅ Covered | `Vital` entity (21 fields): temp, BP, HR, RR, SpO2, FiO2, height, weight, BMI | Most complete entity in the export |
| Lab results | ❌ Not covered | No lab entity | **Significant gap** — product supports lab orders/results with Quest integration |
| Imaging / diagnostic reports | ❌ Not covered | No imaging entity | Product supports imaging attachments via WritePad |
| Procedures | ✅ Covered | `Procedure` entity (9 fields): CPT, status, times | Basic but present |
| Clinical notes / documents | ❌ Not covered | No notes entity | **Significant gap** — product's core workflow involves touch-screen documentation and WritePad templates |
| Care plans / goals | ❌ Not covered | No care plan entity | Product is certified for care plans (b)(9) |
| Orders / referrals | ❌ Not covered | No orders entity | Product supports CPOE for meds and labs ((a)(1)–(a)(3)), referral tracking |
| Insurance / coverage | ❌ Not covered | No insurance entity | **Significant gap** — eTHOMAS handles insurance verification, insurance ledgers |
| Claims / billing | ❌ Not covered | No billing entity | **Significant gap** — eTHOMAS handles claims, billing, superbills, remittance posting |
| Payments | ❌ Not covered | No payments entity | eTHOMAS handles patient statements, online payments |
| Consents / directives | ❌ Not covered | No consent entity | N/A — no evidence product stores consent documents specifically |
| Patient communications | ❌ Not covered | No communications entity | Product has patient portal; no evidence of messaging |
| Devices | ✅ Covered | `Device` entity (11 fields): UDI data | Adequate |
| Specialty-specific (chiro/podiatry/PT) | ❌ Not covered | No specialty entities | **Significant gap** — DRxContent™ podiatry templates, chiropractic documentation, PT/OT assessments are core product features |
| Family health history | ❌ Not covered | No family history entity | N/A — unclear if product stores this beyond what's in notes |

**Summary**: 6 of ~15 applicable domains have any coverage; 9 applicable domains are completely absent. The export covers only core USCDI clinical data classes and entirely omits medications, labs, notes, billing, insurance, and specialty-specific data.

## 6. Documentation Quality

The documentation quality is **very poor**:

- **No data dictionary exists.** The only documentation of export content is XML sample snippets showing example data for each entity. There are no field descriptions, no type specifications (beyond a few date attributes), no value set definitions, no cardinality information, no foreign key documentation.
- **No machine-readable schema** — no XSD, no JSON Schema, no DTD.
- **No sample export files** — only embedded XML snippets that may or may not represent the actual export format faithfully.
- **Field semantics must be guessed** from element names and sample values. Some are clear (FirstName, BirthDate) but others are ambiguous (KeyId, Status, Comment).
- **Data quality issues in samples** suggest insufficient review: the Encounter sample has "1234567897" as the value for every doctor field (name, NPI, taxonomy all identical), and the Condition ICD10Code field contains a GUID rather than an actual ICD-10 code.
- **A developer could not build a reliable import** from this documentation alone. The XML structure is inferable from samples, but without a schema or field descriptions, interpretation would require significant guesswork.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub**

The export covers only 8 data entities with 96 total fields, all mapping directly to basic USCDI clinical data classes. It entirely omits medications (despite the product having e-prescribing), lab results (despite Quest integration), clinical notes (despite touch-screen documentation being the core workflow), and all billing/insurance data (despite eTHOMAS being a full PM system). The 8 exported entities represent a small fraction of what ehrTHOMAS/eTHOMAS stores about patients. The documentation is a single HTML page with XML snippets — no data dictionary, no schema, no sample files.

**Axis 2 — Export approach: Repackaged existing export / Unclear**

The 8 entities exported (Patient, Encounter, Device, Immunization, Allergy, Procedure, Vital, Condition) map almost exactly to USCDI data classes and look like a minimal clinical data projection rather than a purpose-built EHI export. The absence of medications — a core USCDI element the product is certified for — is particularly telling; even as a repackaged clinical export, it's incomplete. There is no evidence of any export coverage beyond what would be available through the product's existing (g)(10) FHIR API or C-CDA transitions of care. The custom XML format suggests some purpose-built work occurred, but the narrowness of coverage (8 entities, no billing, no notes, no meds) indicates this was a compliance checkbox rather than a genuine effort to export all EHI.

### Key Findings

1. **Only 8 data entities with 96 fields are documented** — this is among the thinnest EHI export documentations possible. The entire documentation fits on a single HTML page with XML snippets (`downloads/ehi-export-page.html`).

2. **Zero field descriptions** — none of the 96 fields have any documentation beyond their XML element name. No types (beyond 12 date attributes), no value sets, no relationships documented.

3. **Medications are completely absent** despite the product being certified for CPOE, e-prescribing (including EPCS), and drug interaction checking. This is a gap even relative to USCDI, not just relative to the full designated record set.

4. **All billing, insurance, and PM data is excluded** despite eTHOMAS being a full practice management system with claims, billing ledgers, insurance verification, patient statements, and payments. This represents the largest category of missing EHI.

5. **Specialty-specific clinical content is absent** — DRxContent™ podiatry templates, chiropractic-specific documentation, and PT/OT assessments are core product differentiators but appear nowhere in the export.

### Summary Stats

    Coverage:        Minimal/stub
    Approach:        Repackaged existing export
    Export format:   XML (proprietary schema)
    Entities:        8
    Fields:          96
    Descriptions:    0% (0 of 96 fields described)
    Sample data:     Embedded XML snippets only (no standalone sample files)
    Bulk export:     Yes (all-patients option available)
    Domains covered: 6 of 15 applicable domains (and most only partially)

### Bottom Line

A patient or provider would receive a very incomplete copy of their data from this export. The export covers basic demographics, vitals, conditions, allergies, immunizations, procedures, devices, and encounters — but entirely omits medications, lab results, clinical notes, billing records, insurance information, and all specialty-specific data. The documentation is a single HTML page with no data dictionary, making the export both narrow in coverage and poorly documented. This appears to be a minimal compliance effort rather than a genuine attempt to export all electronic health information.
