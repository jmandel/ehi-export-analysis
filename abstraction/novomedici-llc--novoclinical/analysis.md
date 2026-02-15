# EHI Export Analysis: NovoMedici, LLC

**Product**: NovoClinical v1.0
**Analysis date**: 2026-02-15
**CHPL ID**: 10805 (15.02.05.3015.Novo.01.01.1.220131)

## 1. Product Context

NovoClinical is a cloud-based ambulatory EHR and practice management system developed by NovoMedici, LLC, a small vendor (~5–9 employees) based in Ogden, Utah. The product targets small to mid-sized medical practices and is marketed as an all-in-one platform combining clinical documentation, billing/RCM, scheduling, e-prescribing, patient portal, telemedicine, and chronic care management.

**Data domains the product stores** (based on product research and vendor feature pages):
- **Clinical**: charting with customizable templates, problem lists, medication lists, allergy lists, implantable device lists, clinical notes, vital signs, lab orders/results, imaging (via RIS/PACS integration), immunizations
- **Prescribing**: e-prescriptions, medication history
- **Billing/RCM**: claims, billing codes (ICD-10, UB-04), payment records, DME billing, statements, credit card payments, claim scrubbing
- **Scheduling**: appointments, patient check-in, reminders
- **Patient portal**: secure messaging, patient-entered demographics/history, e-signed documents
- **Telemedicine**: virtual visit records
- **Chronic care management**: care plans, monitoring data
- **Communication**: e-fax, text messaging, direct messaging
- **Public health reporting**: immunization registries, syndromic surveillance, cancer case reports

The product's own navigation bar (visible in the export PDF screenshot) confirms modules for: Appointment, Doc. And Notes, Patient, Communication, Coding, Accounting, Reports, Admin, Inventory, Su Admin. This breadth of functionality establishes a high baseline for what a complete EHI export should cover.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `Novoclinical-Data-Export-Format.pdf` (129 KB, 1 page) | The entire EHI export documentation. Contains 3 sentences describing C-CDA + CSV export formats, navigation instructions, and one screenshot of the export UI. Created 2023-10-07 with Microsoft Word. | **Primary artifact** — but extremely thin |
| `screenshot-meaningful-use-page.png` (193 KB) | Screenshot of vendor's Meaningful Use / mandatory disclosures page. Lists links to regulatory disclosures, API docs, and API terms of use. Footer links to "EMR Data Export" (same PDF). | Low — confirms no additional EHI export documentation exists on the vendor site |

**Additional verification performed**:
- The vendor's Meaningful Use page (https://www.novomedici.com/meaningful-use/) was fetched live and confirmed accessible. It contains links to mandatory disclosures, application access, patient selection, and API terms — no additional EHI export documentation.
- The footer "EMR Data Export" link (https://www.novomedici.com/emr-data-export/) returns HTTP 404.
- The PDF URL (S3) was verified accessible (HTTP 200, Last-Modified: 2023-10-08).
- No additional EHI-related documentation was found on the vendor's website.

## 3. Export Mechanics

- **Format**: ZIP file containing C-CDA XML documents and CSV files
- **Mechanism**: UI-based. Clinic administrators navigate to Communication > Data Export within NovoClinical
- **Patient scope**: Supports both single-patient export and group/bulk export of multiple or all patients
- **Controls**: The export UI allows filtering by doctor, frequency (monthly), date range, and specific patient selection
- **Access constraints**: Available to clinic administrators (role-restricted)
- **Fees**: Not documented in the export PDF; mandatory disclosures document not examined for fee information

## 4. Export Content: What's In It

The export documentation describes exactly two components:

### 4a. C-CDA Documents
> "Each patient will have a C-CDA document in the exported data."

This is the entirety of the C-CDA specification. The documentation does not specify:
- Which C-CDA document type (CCD, Continuity of Care Document, Discharge Summary, etc.)
- Which C-CDA template version or implementation guide
- Which sections are populated (problems, medications, allergies, procedures, results, etc.)
- Whether any vendor-specific extensions are included
- What data elements map to which C-CDA fields

A standard C-CDA clinical summary would typically cover: demographics, problems, medications, allergies, procedures, results, vital signs, immunizations, and possibly clinical notes. However, without specification, the actual content is unknown.

### 4b. CSV Files
> "CSV – Comma separated value, used for patient demography, Appointments."

Two data domains are explicitly mentioned for CSV export:
1. **Patient demography** — no column definitions, no field count, no sample data
2. **Appointments** — no column definitions, no field count, no sample data

The documentation provides zero field-level detail for either CSV file. Column names, data types, delimiters, encoding, date formats, and value sets are all undocumented.

### What's NOT in the export (based on the documentation)

The following modules visible in NovoClinical's own navigation bar (per the screenshot in the PDF) have **no mention** in the export documentation:
- **Coding** — billing codes, ICD-10, CPT
- **Accounting** — financial records, payments, claims
- **Doc. And Notes** — clinical documents beyond what C-CDA may contain
- **Communication** — secure messages, faxes, direct messages
- **Inventory** — medical supplies/equipment tracking
- **Reports** — generated reports

### Vendor's own content organization

The vendor does not provide a data dictionary, so there is no entity/table/field structure to present. The entire documented export is:

| Component | Format | Documented Scope | Fields Documented | Descriptions |
|---|---|---|---|---|
| Patient clinical data | C-CDA XML | "a C-CDA document" per patient | 0 | None |
| Patient demography | CSV | "patient demography" | 0 | None |
| Appointments | CSV | "Appointments" | 0 | None |

**Total documented entities: 3 (at the format level only)**
**Total documented fields: 0**
**Fields with descriptions: 0**

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export documentation describes exactly three categories of data:

1. **C-CDA clinical data**: One C-CDA document per patient. No specifics on what clinical data is included. If this is a standard CCD, it would cover a clinical summary (problems, medications, allergies, results, vitals, immunizations, procedures) but not billing, custom forms, or detailed notes.

2. **Demographics (CSV)**: Patient demographic information. No field definitions.

3. **Appointments (CSV)**: Appointment/scheduling data. No field definitions.

The documentation is so thin that it's impossible to precisely assess depth in any category. The C-CDA component could contain anywhere from a minimal clinical summary to a reasonably complete clinical record, but there's no way to know from the documentation alone.

What is clear: billing, coding, accounting, communications, documents/notes (beyond C-CDA), and other modules visible in the product's own UI are entirely absent from the export documentation.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | CSV for "patient demography" mentioned; 0 fields documented | Product stores demographics; CSV export exists but completely undocumented |
| Encounters / visits | ⚠️ Partial | Appointments CSV mentioned; C-CDA may contain encounter data | Appointment data exported as CSV; clinical encounter detail depends on C-CDA content (unspecified) |
| Problems / conditions | ⚠️ Partial | Likely in C-CDA if standard sections populated | No explicit confirmation; depends entirely on C-CDA implementation |
| Medications / prescriptions | ⚠️ Partial | Likely in C-CDA if standard sections populated | E-prescribing is a product feature; C-CDA may carry medication lists but not full Rx history |
| Allergies | ⚠️ Partial | Likely in C-CDA if standard sections populated | No explicit confirmation |
| Immunizations | ⚠️ Partial | Likely in C-CDA if standard sections populated | Product certified for immunization reporting (f)(1); C-CDA may include |
| Vitals | ⚠️ Partial | Likely in C-CDA if standard sections populated | No explicit confirmation |
| Lab results | ⚠️ Partial | Likely in C-CDA if standard results section populated | No explicit confirmation |
| Imaging / diagnostic reports | ⚠️ Partial | May be in C-CDA if results section populated | Product integrates with RIS/PACS; unclear if imaging data is in export |
| Procedures | ⚠️ Partial | Likely in C-CDA if standard sections populated | No explicit confirmation |
| Clinical notes / documents | ⚠️ Partial | May be in C-CDA notes section; "Doc. And Notes" module exists in product | Product has dedicated Doc. And Notes module; C-CDA may carry some notes but unlikely to capture all |
| Care plans / goals | ❌ Not covered | No mention in export documentation | Product has Chronic Care Management module; no CCM data in export |
| Orders / referrals | ❌ Not covered | No mention in export documentation | Product supports referrals and order tracking; not in export |
| Insurance / coverage | ❌ Not covered | No mention in export documentation | Product handles patient eligibility verification; not in export |
| Claims / billing | ❌ Not covered | No mention in export documentation | Product has full billing/RCM module (claims, coding, UB-04, DME); **significant gap** |
| Payments | ❌ Not covered | No mention in export documentation | Product processes payments and credit cards; not in export |
| Consents / directives | ❌ Not covered | No mention in export documentation | Patient portal has e-signature for documents; not in export |
| Patient communications / portal messages | ❌ Not covered | No mention in export documentation | Product has secure messaging, patient portal; not in export |

**Note on "Partial" ratings**: Many clinical domains are rated ⚠️ Partial rather than ✅ Covered because the documentation never confirms what C-CDA sections are populated. A C-CDA *could* contain these data elements, but the vendor provides zero specifics. The export may be better than documented, but the documentation itself provides no assurance.

**Key gaps**:
- **Billing/RCM** is the most significant gap. NovoClinical is marketed as "Medical Billing Software for Small Business" with claims, coding, UB-04, DME billing, payment processing, and accounting. None of this appears in the export.
- **Clinical notes** beyond C-CDA summaries. The product has a dedicated "Doc. And Notes" module, suggesting rich clinical documentation that likely exceeds what a standard C-CDA captures.
- **Patient communications and portal data** — secure messages, patient-entered data, e-signed documents.
- **Chronic care management** — care plans, monitoring data for chronic conditions.

## 6. Documentation Quality

The documentation quality is **extremely poor** — among the worst possible while still technically having documentation.

**What exists**:
- A single-page PDF (3 sentences + 1 screenshot)
- Confirmation that the export produces a ZIP file with C-CDA and CSV components
- Navigation instructions for triggering the export

**What's entirely missing**:
- ❌ Data dictionary (none)
- ❌ Field definitions for CSV files (zero fields documented)
- ❌ C-CDA section/template specification (none)
- ❌ Schema or format specification (none)
- ❌ Sample data files (none)
- ❌ Value sets or code system documentation (none)
- ❌ Relationship documentation between C-CDA and CSV files (none)
- ❌ Machine-readable artifacts of any kind (none)

**Could a developer build an import from this documentation?** No. A developer receiving this documentation would know only that they'll receive a ZIP containing "a C-CDA" and "CSV files for demographics and appointments." They would have to reverse-engineer every aspect of the actual data format from the export files themselves. The documentation provides essentially zero technical guidance.

## 7. Overall Assessment

### Classification

**Minimal/stub**: The documentation is a single page that names two file formats (C-CDA and CSV) with no field-level detail. The export appears to cover only a clinical summary (C-CDA) plus basic demographics and appointments (CSV), omitting billing, coding, accounting, communications, care management, and other data domains that the product stores. This is a compliance checkbox, not a genuine effort to enable EHI portability.

### Key Findings

1. **The entire EHI export documentation is 3 sentences on a single page.** The PDF (`Novoclinical-Data-Export-Format.pdf`, 1 page, created 2023-10-07) contains no data dictionary, no field definitions, no schemas, no sample data — zero technical detail beyond naming C-CDA and CSV as formats.

2. **Billing and financial data — a core product capability — is completely absent from the export.** NovoClinical is marketed as billing software and has dedicated Coding and Accounting modules visible in the export screenshot's own navigation bar. None of this data is addressed in the export documentation.

3. **The export is a C-CDA repackaging plus two minimal CSV files.** This is the classic (b)(10) failure mode: the vendor points to their existing C-CDA clinical summary and calls it EHI export. C-CDA covers only a standard clinical summary — not the full designated record set.

4. **Zero fields are documented across all export components.** Neither the C-CDA content nor the CSV columns are specified at any level of detail. A recipient has no way to know what data to expect without generating an actual export and reverse-engineering it.

5. **The product's own UI reveals the gap.** The screenshot embedded in the export PDF shows navigation modules (Coding, Accounting, Doc. And Notes, Communication, Inventory) whose data is entirely unaddressed by the export — the vendor's own artifact inadvertently documents the incompleteness.

### Summary Stats

```
Classification:  Minimal/stub
Export format:   C-CDA XML + CSV, delivered as ZIP
Model type:      Standard projection (C-CDA) + minimal CSV
Entities:        3 (C-CDA document, demographics CSV, appointments CSV)
Fields:          0 documented
Descriptions:    N/A (no fields documented)
Sample data:     No
Bulk export:     Yes (group export of multiple/all patients)
Domains covered: 2 of 15 applicable domains confirmed; ~8 more possible via unspecified C-CDA content
```

### Bottom Line

NovoClinical's EHI export is a minimal compliance stub: a C-CDA clinical summary plus two undocumented CSV files covering demographics and appointments. The product stores extensive billing, coding, accounting, communications, and care management data — none of which appears in the export. A patient or provider requesting their complete health information would receive, at best, a clinical summary covering a fraction of what NovoClinical stores about them, with no documentation to help them understand even that fraction.
