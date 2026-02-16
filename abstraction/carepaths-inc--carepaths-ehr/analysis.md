# EHI Export Analysis: Carepaths Inc

**Product**: CarePaths EHR  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.04.04.2982.Care.19.00.1.210408 (CHPL ID 10607)

## 1. Product Context

CarePaths EHR is a cloud-based, all-in-one behavioral health EHR and practice management platform targeting solo and small-group behavioral health practices (psychiatrists, psychologists, therapists, counselors, social workers, addiction specialists). Priced at $49/month per clinician, it serves a niche market.

Key data domains the product stores, relevant to EHI export assessment:

- **Clinical documentation**: Intake assessments, progress notes, treatment plans, custom clinical forms (via forms maker), diagnoses, treatment goals
- **Measurement-based care / outcomes**: Standardized assessment instruments (PHQ-9, GAD-7, OQ-45, 20+ others), longitudinal outcomes tracking with graphing
- **Billing and accounting**: Automated charge posting from notes, X12 claims generation, electronic remittance processing, patient accounting (charges, payments, adjustments, invoices/statements), CPT coding, credit card payment processing
- **Insurance**: Eligibility verification, coverage lookups
- **Medications**: E-prescribing via DrFirst/Rcopia integration
- **Scheduling**: Calendar management, appointment reminders, patient self-scheduling
- **Communications**: Secure messaging between patient and therapist, appointment reminders
- **Teletherapy**: Built-in HIPAA-compliant video sessions, AI session summaries
- **Patient portal data**: Document viewing/signing, online payments, assessment completions
- **Demographics**: Patient demographics (certified for (a)(5))
- **Family health history**: Certified for (a)(12)

This is a behavioral-health-specific product with integrated practice management and billing. A complete EHI export should cover clinical documents, structured assessment/outcomes data, billing/accounting records, insurance info, medications, messaging, and demographics.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/b10-export-format.html` (93 KB) | The complete B.10 EHI Export documentation page from CarePaths website. Contains ~234 words of content describing export mechanism and listing 7 file categories. | **Primary source** — this is the entirety of the vendor's EHI export documentation |
| `downloads/b10-export-page-full.png` (383 KB) | Full-page screenshot of the documentation page, confirming the HTML content is complete and matches | Confirmatory |
| `downloads/b10-export-page-screenshot.png` (199 KB) | Viewport screenshot of the top portion of the documentation page | Confirmatory |
| `product-research.md` | Detailed research on CarePaths EHR features, modules, and data storage | Essential for establishing baseline of what the product stores |
| `chpl-metadata.json` | CHPL certification details including certified criteria | Confirms (b)(10) certification and other criteria |

**No data dictionary, schema, sample data files, or other technical documentation exists.** The entire export documentation is a single webpage with approximately 234 words.

## 3. Export Mechanics

- **Format**: ZIP file per patient containing mixed file types (XML, PDF, TXT, original uploads)
- **Mechanism**: Admin UI — users with "record management permissions" access the export from an "exports dropdown on the patient management overview"
- **Single-patient**: Yes, select individual patients
- **Bulk capability**: Yes, but with caveats — "For full patient population exports, please contact support or schedule the export for outside business hours. Running bulk exports can be resource heavy, and doing so during the day may affect ehr functionality."
- **Delivery**: Exported files are presented to the admin user through the internal messaging system and can be downloaded directly
- **Access constraints**: Requires admin user with record management permissions
- **Fees**: Not mentioned

## 4. Export Content: What's In It

The export documentation lists 7 file categories with no field-level detail whatsoever. There is no data dictionary, no schema, no sample data, and no field-level documentation of any kind.

### Vendor's own content organization

The vendor organizes the export as a list of files included in the ZIP:

| # | File Category | Format | Naming Scheme | Notes |
|---|---|---|---|---|
| 1 | CCD (Continuity of Care Document) | XML | `cda_PATIENT_NAME.xml` | Standard C-CDA clinical summary; 1 per patient |
| 2 | Accounting Statement | PDF | `PATIENT_ID_Statements_asOfDate.pdf` | Patient's accounting transactions; 1 per patient |
| 3 | Messaging History | TXT | `PATIENT_ID_Message_History_asOfDate.txt` | Messages sent/received by patient; 1 per patient |
| 4 | Patient Charts | PDF | `PATIENT_ID_Chart_Year.pdf` | Completed service documents grouped by year; multiple per patient |
| 5 | Audit Logs | Unspecified | Unspecified | Changes made to patient chart/account |
| 6 | Appointment History | Unspecified | Unspecified | Appointment history and statuses |
| 7 | Uploaded Documents/Images | Original format | Original filename | Uploads from patient's EHR facesheet |

**Critical observations:**

1. **No structured data export**: The only structured data format is the CCD XML, which is a standard C-CDA clinical summary. Everything else is either rendered as PDF/TXT (losing structure) or passed through as original uploads.

2. **Accounting is a PDF statement, not structured data**: The billing/accounting data is exported as a PDF "Accounting Statement" — a rendered document, not structured transaction data. Individual charges, payments, adjustments, claim details, CPT codes, payer information, and remittance data cannot be programmatically extracted from a PDF statement.

3. **Clinical charts are PDFs**: The patient's clinical documentation (progress notes, treatment plans, intake assessments) is exported as rendered PDF charts grouped by year. The structured data within these documents (diagnoses, treatment goals, assessment scores, form field values) is lost.

4. **No field-level documentation**: Zero fields are documented. No types, no descriptions, no relationships, no value sets.

5. **Two categories lack format/naming details**: Audit Logs and Appointment History don't specify format or naming scheme.

(See `analysis/entity-inventory-full.json` for the complete machine-readable extraction.)

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes 7 file categories spanning clinical data (CCD + chart PDFs), accounting (PDF statement), communications (messaging TXT), audit logs, scheduling (appointment history), and attachments. On the surface, this touches several domains. However, the critical issue is that almost all data is rendered into non-structured formats (PDF, TXT), meaning the underlying structured data is lost.

The CCD XML is the only machine-readable clinical data, and it is a standard C-CDA clinical summary — not a product-specific export. A CCD covers USCDI-scope data (demographics, problems, medications, allergies, vital signs, immunizations, procedures, lab results) but does not include behavioral-health-specific data like standardized assessment scores (PHQ-9, GAD-7), treatment plan details, outcomes tracking, or custom form data.

The "Patient Charts" PDFs likely contain the richest clinical content (progress notes, treatment plans, intake assessments), but as rendered PDFs, they are not structured data. A patient could read them, but a developer or downstream system cannot programmatically extract diagnoses, assessment scores, or treatment goals.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | CCD XML contains standard demographics | CCD covers basics; product stores more (certified for (a)(5)); no field-level detail available |
| Encounters / visits | ⚠️ Partial | Appointment History (unspecified format); service documents in chart PDFs | Appointment history exists but format unknown; encounter details buried in PDF charts, not structured |
| Problems / conditions / diagnoses | ⚠️ Partial | CCD XML contains problem list | Only standard CCD problem list; behavioral health diagnoses in progress notes are in PDF only |
| Medications / prescriptions | ⚠️ Partial | CCD XML contains medication list | CCD covers active medications; e-prescribing detail (DrFirst integration data) unclear |
| Allergies | ⚠️ Partial | CCD XML typically includes allergies section | Standard CCD section only |
| Immunizations | ⚠️ Partial | CCD XML may include immunizations | Less relevant for behavioral health; likely minimal |
| Vitals | ⚠️ Partial | CCD XML typically includes vitals | Standard CCD section only |
| Lab results | ⚠️ Partial | CCD XML may include lab results | Product has CPOE for labs (a)(2)/(a)(3); CCD may include results but detail unclear |
| Imaging / diagnostic reports | ❌ Not covered | No specific export component | Product may order imaging but this is not central to behavioral health |
| Procedures | ⚠️ Partial | CCD XML typically includes procedures | Standard CCD section only |
| Clinical notes / documents | ⚠️ Partial | Patient Charts PDFs contain rendered notes | Notes exist but as rendered PDFs, not structured data; behavioral health notes (progress notes, treatment plans, intake assessments) lose all structure |
| Care plans / goals | ⚠️ Partial | May appear in CCD and/or chart PDFs | Treatment plans are core to behavioral health; exported only as PDF, not structured |
| Orders / referrals | ❌ Not covered | No specific export component | Product supports CPOE; no structured order data in export |
| Insurance / coverage | ❌ Not covered | No specific export component | Product stores insurance info and does eligibility verification; not in export |
| Claims / billing | ⚠️ Partial | Accounting Statement PDF | Product has full billing (X12 claims, remittance, charge posting); exported only as a rendered PDF statement, not structured transaction data. **Significant gap** — the structured billing data (claims, CPT codes, payer info, remittance, adjustments) is lost |
| Payments | ⚠️ Partial | Accounting Statement PDF | Payment records rendered in PDF; not machine-readable |
| Consents / directives | ❌ Not covered | No specific export component | May be in uploaded documents if scanned |
| Patient communications / portal messages | ✅ Covered | Messaging History TXT file | Messaging history explicitly included, though as plain text |
| Specialty-specific (behavioral health) | ❌ Not covered | No specific export component | **Major gap**: Product's core differentiator is measurement-based care (PHQ-9, GAD-7, OQ-45, 20+ standardized instruments), outcomes tracking, longitudinal assessment graphs, and custom clinical forms. None of this structured assessment/outcomes data appears in the export. The CCD does not carry instrument-specific assessment scores, and the chart PDFs may render some results but not as structured data |

## 6. Documentation Quality

The export documentation is **extremely thin** — a single webpage with approximately 234 words. It provides:

- ✅ A description of how to access the export (admin UI, exports dropdown)
- ✅ A list of 7 file categories included in the export
- ✅ File naming schemes for 4 of 7 categories
- ❌ No data dictionary
- ❌ No field-level documentation of any kind
- ❌ No schema or structural documentation for the CCD content
- ❌ No sample data
- ❌ No documentation of what's in the CCD beyond "Continuity of Care Document"
- ❌ No documentation of what fields appear in the Accounting Statement PDF
- ❌ No documentation of the format or structure of Audit Logs or Appointment History
- ❌ No machine-readable artifacts

**Developer usability**: A developer could not build an import from this documentation. They would know they'll receive a ZIP with some PDFs, a CCD XML, and a TXT file, but would have no idea what fields or data elements to expect in any of them. They would need to reverse-engineer the CCD structure from the C-CDA standard and hope the PDFs are consistent enough to parse.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

While the export technically touches several domains (clinical via CCD, billing via PDF statement, messaging via TXT, appointments, audit logs, and attachments), the coverage is fundamentally shallow. The product's most distinctive data — structured behavioral health assessments (PHQ-9, GAD-7, OQ-45, 20+ instruments), longitudinal outcomes tracking, custom clinical forms, treatment plan details, insurance/eligibility data, and structured billing/claims data — is either absent or buried in rendered PDFs where it cannot be programmatically accessed. The only structured clinical data is a standard CCD, which covers USCDI-scope data but none of the behavioral-health-specific content that is this product's core value. The absence of any data dictionary or field-level documentation makes it impossible to verify what's actually in the export beyond these high-level file categories.

**Axis 2 — Export approach: Repackaged existing export**

The export is assembled from pre-existing document generation capabilities: the CCD is the standard clinical summary the product already generates for transitions of care (certified for (b)(1) and (e)(1)), the accounting statement is a standard financial report, the chart PDFs are the same rendered charts users can view/print in the UI, and messaging history is a text dump. No purpose-built structured data export was created for (b)(10). The telltale signs: the CCD is explicitly labeled as a "Continuity of Care Document" (a transitions-of-care artifact), there is no product-specific data dictionary, and financial/clinical data is rendered into PDFs rather than exported as structured data. This is a collection of existing document outputs bundled into a ZIP and labeled as EHI export.

### Key Findings

1. **No structured data export beyond CCD**: The only machine-readable clinical data is a standard C-CDA document. All other clinical and financial data is rendered as PDF or TXT, losing all structure. A patient receiving this export would get readable documents but no data they could import into another system.

2. **Behavioral health assessment data not exported**: CarePaths' core differentiator — measurement-based care with 20+ standardized instruments, longitudinal outcomes tracking, and custom forms — has no representation in the export. This structured assessment data (PHQ-9 scores over time, GAD-7 trajectories, etc.) is the most valuable behavioral health data the product stores, and it is absent.

3. **Billing data exported as PDF, not structured data**: Despite the product having full billing capabilities (X12 claims, electronic remittance, charge posting, CPT coding), the export includes only a rendered accounting statement PDF. Individual claims, CPT codes, payer information, remittance details, and payment records are not available as structured data.

4. **Documentation is a 234-word webpage with zero field-level detail**: No data dictionary, no schema, no sample data, no field documentation of any kind. This is among the thinnest (b)(10) documentation possible while still having a dedicated page.

5. **Insurance and eligibility data missing entirely**: The product stores insurance information and performs eligibility verification, but neither appears in the export file list.

### Summary Stats

    Coverage:        Minimal/stub/unclear
    Approach:        Repackaged existing export
    Export format:   Mixed (CCD XML, PDF, TXT, original uploads)
    Entities:        7 file categories (no structured entities)
    Fields:          0 documented
    Descriptions:    N/A (no fields documented)
    Sample data:     No
    Bulk export:     Yes (with vendor support contact required)
    Domains covered: 1-2 of 14 applicable domains (only messaging fully; all others partial or missing)

### Bottom Line

A patient receiving this export would get a standard clinical summary (CCD), some rendered PDF documents, and a messaging history text file — readable but not importable into another system. The product's most valuable data — structured behavioral health assessments, outcomes tracking, treatment plan details, and billing/claims records — is either absent from the export or trapped in rendered PDFs. This is a compliance checkbox, not a genuine effort to export all electronic health information.
