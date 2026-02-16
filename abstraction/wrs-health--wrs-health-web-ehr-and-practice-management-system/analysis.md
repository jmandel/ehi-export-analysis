# EHI Export Analysis: WRS Health

**Product**: WRS Health Web EHR and Practice Management System v7.0
**Analysis date**: 2026-02-16
**CHPL ID**: 15.02.05.2527.WRSH.01.01.1.211214

## 1. Product Context

WRS Health is a cloud-based, all-in-one EHR and practice management platform targeting ambulatory specialty practices across 32+ medical specialties (internal medicine, cardiology, dermatology, OB/GYN, orthopedics, psychiatry, pain management, gastroenterology, etc.). The product integrates:

- **Clinical documentation/charting** with specialty-specific templates (six-tier content system), voice dictation, digital pen input
- **E-prescribing** (Surescripts-certified Gold Solution Provider, including EPCS for controlled substances)
- **Lab ordering and results** with bidirectional connectivity to major labs (LabCorp, Quest)
- **Billing/RCM** with electronic superbills, claim scrubbing, denial management, and optional full-service billing
- **Patient scheduling** with automated reminders, eligibility verification, multi-provider/multi-location support
- **Patient portal** with secure messaging, lab results, refill requests, bill pay
- **Telehealth** with integrated video visits and virtual waiting room
- **Document management** with integrated eFax, scanning/import
- **Referral management** and health maintenance/recall system
- **Reporting/analytics** including MIPS/CQM quality measures

This is a full-featured ambulatory EHR+PM system. A complete EHI export should cover clinical documentation, medications, labs, billing/claims, demographics, insurance, encounters, documents, patient communications, and specialty-specific clinical data.

## 2. Artifacts Reviewed

| Artifact | Type | Size | Description | Informativeness |
|---|---|---|---|---|
| `170.315-b10-EHI-Export.pdf` | PDF | 1.1 MB, 8 pages | The sole EHI export documentation. Describes single/multi-patient export workflow, ZIP file structure with screenshots. Created with Google Docs, dated October 14, 2023, v1.0. | **Primary artifact** — only source of export information |
| `screenshot-certification-page-full.png` | PNG | 1.4 MB | Full-page screenshot of the ONC certification and costs page | Low — confirms the PDF link is the only EHI documentation |
| `screenshot-ehi-section-viewport.png` | PNG | 686 KB | Zoomed screenshot of the EHI Export section on the certification page | Low — confirms a single link to the PDF |
| Certification page (live) | HTML | ~102 KB | `https://www.wrshealth.com/onc-certification-and-costs` — verified live on 2026-02-16, HTTP 200. Contains exactly one link in the EHI section: the PDF. | Confirms no additional documentation exists |
| PDF direct link (live) | PDF | 1.1 MB | `https://www.wrshealth.com/wp-content/uploads/2023/10/170.315-b10-EHI-Export.pdf` — verified live on 2026-02-16, HTTP 200. | Confirms PDF is still accessible |

**No data dictionary, schema file, sample export data, API documentation, or machine-readable artifact was found.** The entire EHI export documentation consists of a single 8-page PDF.

## 3. Export Mechanics

- **Format**: ZIP archive (`ehi_documents.zip`) containing CSV files, a C-CDA XML, HTML encounter notes, and raw document attachments
- **Mechanism**: UI-driven (EHR Admin → search patient → right-click → EHI Export → Request → Download ZIP)
- **Single-patient**: Self-service via EHR Admin by users with Clinical Admin/Admin permissions
- **Multi-patient/bulk**: Not self-service. Requires emailing `accountmanagement@wrshealth.com` to request a population-level export in the same ZIP format
- **Access constraints**: Requires Clinical Admin or Admin permissions in the EHR Admin system
- **Fees**: Not mentioned in the documentation
- **API access**: None — purely UI-based with no programmatic export option

## 4. Export Content: What's In It

### No field-level data dictionary

The PDF provides **file-level descriptions only** — it names each file in the ZIP and gives a 1-2 sentence prose description of its contents. **Zero individual field names, data types, value sets, or relationships are documented anywhere.** There is no data dictionary, no schema, and no sample data.

Total documented fields across all files: **0**. The vendor does not list a single column name for any CSV file.

### Vendor's own content organization

The export contains 9 components organized into the vendor's implicit categories:

| Component | Format | Category (vendor's) | Vendor Description |
|---|---|---|---|
| `BillingReport.csv` | CSV | Billing | Financial transactions: patient info, transaction dates, charges, claims, description, status |
| `CCDA.xml` | XML (C-CDA) | Clinical | Clinical data export, HL7 C-CDA compliant with USCDI v1 |
| `demographics.csv` | CSV | Demographics | Patient key info, identification, contacts, insurance |
| `schedule.csv` | CSV | Scheduling | Encounter records: appointment date, provider, location, type, workflow, notes, note dates |
| `PatientDocumentFiles.csv` | CSV | Index | Mapping file listing documents in the Documents folder |
| `Documents/` | Mixed (PDF, DOCX, XLS, XML, HTML, DAT, JPG, GIF, PNG) | Documents | Supporting documents, attachments, uploaded lab results |
| `Notes/` (HTML files) | HTML + CSS/JS | Clinical Notes | Encounter notes from patient visits, one HTML file per note |
| `Notes/PatientNoteFiles.csv` | CSV | Index | Mapping file listing exported notes |
| `Notes/NOTES.LOG` | Text | Export Metadata | Logs of successfully exported notes and errors |

From the PDF's screenshots (page 8), the following note types are visible in a sample export:
- `VISIT_NOTE_II`
- `ENT_NOTE`
- `DERMATOLOGY_NOTE`
- `INTERNAL_MEDICINE_NOTE`

This confirms the export includes specialty-specific encounter notes, though only as rendered HTML — not as structured data.

### What the C-CDA likely covers

The PDF states the C-CDA complies with USCDI v1, which includes:
- Patient demographics/contact info
- Problems/conditions
- Medications
- Allergies and intolerances
- Immunizations
- Vital signs
- Lab results (some)
- Procedures
- Assessment and plan
- Care team members
- Goals
- Health concerns
- Smoking status
- Unique device identifiers

However, the PDF provides **no detail** about which USCDI data classes are actually populated or how completely. It simply states compliance and refers to the HL7 website for specifications.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor organizes the export into four functional areas:

1. **Billing**: A single CSV (`BillingReport.csv`) with financial transactions. The prose mentions "charges, claims, description of transactions, status" — this sounds like a superbill/charge-level export, but without field names it's impossible to know if it includes claim details, payment records, or denial information.

2. **Demographics/Insurance**: A single CSV (`demographics.csv`) covering "key information, identification details, contact information, insurance information." Scope unknown without field names.

3. **Scheduling/Encounters**: A single CSV (`schedule.csv`) with appointment-level data. The prose mentions 7 data elements: appointment date, provider, location, appointment type, workflow, notes, and note dates.

4. **Clinical**: A C-CDA XML (USCDI v1 subset) plus HTML encounter notes and raw document attachments. The clinical data is split across:
   - Structured clinical data → C-CDA (standard projection, limited to USCDI v1 scope)
   - Narrative clinical notes → HTML files (human-readable, not computable)
   - Documents/labs → raw files (PDFs, images, etc.)

The thinnest area is the CSV files: 3 data files with no documented columns. The C-CDA is a known-quantity standard but limited to the USCDI v1 subset. The richest component may be the Notes folder (which captures the actual encounter documentation), but it's in narrative HTML — not structured data.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | `demographics.csv` (fields unknown); C-CDA demographics section | CSV likely has demographic fields but no documentation to verify completeness |
| Encounters / visits | ⚠️ Partial | `schedule.csv` mentions appointment date, provider, location, type; HTML notes per visit | Schedule data exists but depth unknown; encounter context only in narrative HTML |
| Problems / conditions / diagnoses | ⚠️ Partial | Presumably in C-CDA (USCDI v1 includes problems) | C-CDA should include problem list; no vendor-specific structured export |
| Medications / prescriptions | ⚠️ Partial | Presumably in C-CDA (USCDI v1 includes medications) | C-CDA covers current medications. Product has deep e-prescribing (EPCS, Surescripts, formulary checking) — prescription history, pharmacy data, drug interaction records likely not in export |
| Allergies | ⚠️ Partial | Presumably in C-CDA (USCDI v1 includes allergies) | Standard C-CDA allergies section; product-specific allergy data unknown |
| Immunizations | ⚠️ Partial | Presumably in C-CDA (USCDI v1 includes immunizations) | Standard C-CDA immunizations; health maintenance/recall data not exported |
| Vitals | ⚠️ Partial | Presumably in C-CDA (USCDI v1 includes vital signs) | Standard C-CDA vitals section |
| Lab results | ⚠️ Partial | Presumably in C-CDA; raw lab documents in Documents/ folder | C-CDA has some lab results; uploaded lab PDFs in Documents/. Lab Order Tracking System data (order status, alerts, patient communications) not mentioned |
| Imaging / diagnostic reports | ⚠️ Partial | May be in Documents/ folder as uploaded files | Only if practice uploaded reports; no structured radiology data |
| Procedures | ⚠️ Partial | Presumably in C-CDA (USCDI v1 includes procedures) | Standard C-CDA procedures section |
| Clinical notes / documents | ✅ Covered | HTML encounter notes in Notes/ folder; raw documents in Documents/ folder | Notes exported per visit with specialty-specific types visible. However, notes are narrative HTML — no structured data extraction possible |
| Care plans / goals | ⚠️ Partial | USCDI v1 includes goals and health concerns | Only via C-CDA; product's health maintenance/recall system data not exported |
| Orders / referrals | ❌ Not covered | No referral or order data mentioned in export | Product has referral management and lab order tracking; neither is in the documented export |
| Insurance / coverage | ⚠️ Partial | `demographics.csv` mentions "insurance information" | Some insurance data in demographics CSV, but depth unknown; eligibility verification data not mentioned |
| Claims / billing | ⚠️ Partial | `BillingReport.csv` mentions charges, claims, status | A billing CSV exists, but without field documentation it's impossible to assess depth. Product has claim scrubbing, denial management, electronic superbills — unclear if these details are exported |
| Payments | ❓ Unclear | `BillingReport.csv` may include payments | Mentioned as "financial transactions" but payment-specific fields not confirmed |
| Consents / directives | ❌ Not covered | No mention in export | If product captures advance directives, they're not in the documented export |
| Patient communications / portal messages | ❌ Not covered | No mention in export | Product has patient portal with secure messaging, refill requests, bill pay — none mentioned in export |
| Specialty-specific data | ⚠️ Partial | HTML encounter notes include specialty note types (ENT, dermatology, internal medicine) | Specialty data exists in narrative HTML notes but not as structured/computable data. Product's 32+ specialty templates with structured fields are flattened to HTML |

**Summary**: Of 19 applicable domains, **1 is well-covered** (clinical notes as HTML), **12 are partially covered** (mostly via C-CDA with unknown depth), **3 are not covered**, and **1 is unclear**. The partial coverage is largely speculative — based on what USCDI v1 *should* include, not on verified field-level evidence.

## 6. Documentation Quality

The documentation is **minimal**. The 8-page PDF is a user guide for performing the export, not a technical specification for understanding the exported data.

**What's documented well:**
- How to perform the export (step-by-step with screenshots)
- What files the ZIP contains (file-level inventory with format and brief description)
- File naming conventions (patient name, ID, date, note type)

**What's not documented at all:**
- Column/field names for any CSV file (zero fields listed across all 3 data CSVs)
- Data types, formats, or encodings
- Value sets, code systems, or enumerated values
- Relationships between files (e.g., how BillingReport rows relate to schedule rows)
- What specific USCDI v1 data classes are populated in the C-CDA
- Whether the C-CDA includes any vendor extensions beyond the standard
- Any versioning or change history of the export format

**Could a developer build an import from this documentation?** No. A developer receiving this documentation would know they'll get a ZIP with some CSVs, a C-CDA, HTML files, and attachments — but they would have no idea what columns the CSVs contain, what data types to expect, or how to link records across files. They would need to request an actual export and reverse-engineer the schema. The C-CDA is the only component with an external specification (HL7), but even there, the vendor doesn't document which optional sections are populated.

**Machine-readable artifacts**: None. No JSON Schema, XSD, DDL, OpenAPI spec, CSV header documentation, or sample data files.

## 7. Overall Assessment

### Classification

**Partial native export**

The export goes beyond a pure C-CDA/FHIR repackaging — it includes vendor-specific CSV files for billing, demographics, and scheduling alongside the C-CDA, plus raw encounter notes and documents. This is a genuine (b)(10) effort. However, the documentation is so thin that it's impossible to assess the depth of coverage, and the clinical data is split between a standard C-CDA (limited to USCDI v1) and narrative HTML (not computable). Significant product capabilities — e-prescribing details, lab order tracking, referral management, patient portal data, telehealth records, health maintenance alerts, specialty-specific structured data — are not documented as being in the export.

### Key Findings

1. **Zero field-level documentation across all export files.** The 3 CSV data files (BillingReport, demographics, schedule) have no documented column names, data types, or value sets. This is the single most significant documentation gap — it makes the export opaque to any recipient.

2. **Clinical data relies on C-CDA (USCDI v1) — a known limited subset.** The structured clinical export is a standard C-CDA, which covers ~15 USCDI data classes but misses vendor-specific structured data from 32+ specialty templates, e-prescribing workflows, and lab order tracking.

3. **Encounter notes are exported as narrative HTML, not structured data.** While this captures the clinical narrative, it means specialty-specific structured fields (from the product's six-tier template system) are flattened into uncomputable HTML.

4. **Billing data is present but undocumented.** `BillingReport.csv` exists — this is better than many vendors who omit billing entirely — but without knowing what fields it contains, it's impossible to assess whether it covers charges, claims, payments, denials, or just a subset.

5. **Multiple product capabilities have no documented export coverage**: patient portal messages, telehealth records, referral tracking, health maintenance/recall data, e-prescribing history, and eFax records are not mentioned in the export documentation.

### Summary Stats

```
Classification:  Partial native export
Export format:   Mixed (CSV, C-CDA XML, HTML, raw documents)
Model type:      Hybrid — vendor CSV files + standard C-CDA projection + narrative HTML
Entities:        9 components (3 data CSVs, 1 C-CDA, 2 folders, 2 index CSVs, 1 log)
Fields:          0 documented (no field-level data dictionary)
Descriptions:    N/A (no fields documented)
Sample data:     No
Bulk export:     Yes (via email request to vendor)
Domains covered: 1 of 19 fully, 12 of 19 partially (mostly via C-CDA assumption)
```

### Bottom Line

WRS Health provides a genuine (b)(10) export that bundles billing, demographics, scheduling, clinical summary, encounter notes, and documents — but the documentation is far too thin to assess or use the export meaningfully. With zero documented field names across all CSV files, no sample data, and no schema, a recipient would have to reverse-engineer the entire export structure. The biggest gap is not what's exported but what's knowable: the documentation tells you *what files* you'll get but nothing about *what's in them*.
