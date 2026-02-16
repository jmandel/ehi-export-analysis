# EHI Export Analysis: CarePaths Inc

**Product**: CarePaths EHR  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.04.04.2982.Care.19.00.1.210408 (CHPL listing ID 10607)

## 1. Product Context

CarePaths EHR is an all-in-one, cloud-based behavioral health EHR and practice management platform built for psychiatrists, psychologists, therapists, counselors, social workers, and addiction specialists. It targets solo practitioners and small-to-mid-size group practices, priced at $49/month per primary clinician. The product combines:

- **Clinical documentation**: Intake assessments, progress notes, treatment plans, case management assessments, custom clinical forms (via a forms maker), and AI-powered session summaries
- **Measurement-based care (MBC)**: The product's core differentiator — automated weekly patient assessments using 20+ standardized instruments (PHQ-9, GAD-7, OQ-45, HAM-A, SCARED, etc.) with longitudinal tracking and graphing
- **Practice management**: Scheduling, appointment reminders, patient self-scheduling
- **Billing and claims**: Automated charge posting, X12 claims generation, electronic remittance processing, credit card payment processing, patient accounting (charges, payments, adjustments, invoices)
- **E-prescribing**: Via DrFirst/Rcopia integration (separate fee)
- **Teletherapy**: Built-in HIPAA-compliant video sessions
- **Patient portal and mobile app** (CarePaths Connect): Secure messaging, assessment completion, appointment booking, document viewing, online payments
- **Reporting**: Clinical, financial, demographic, and quality measure (eCQM/MIPS/MACRA) reporting

For EHI export completeness, the relevant question is whether the export covers clinical documentation, structured assessment/outcomes data, billing records, messaging, and behavioral health–specific data. The MBC assessment data is particularly important — it is CarePaths' distinguishing feature and constitutes clinical records used to make treatment decisions.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/b10-export-format.html` (93,196 bytes, 1,390 lines) | The vendor's complete B.10 EHI export documentation page. Contains ~39 lines of actual prose content describing the export mechanism and listing 7 file categories. The remaining ~1,350 lines are site chrome (navigation, footer, CSS, JS). | **Primary source** — this is the entirety of the export documentation |
| `downloads/b10-export-page-full.png` (383 KB, 1905×2510 px) | Full-page screenshot of the export documentation page | Confirms HTML content; no additional information |
| `downloads/b10-export-page-screenshot.png` (199 KB) | Viewport screenshot of the same page | Confirms HTML content; no additional information |
| `product-research.md` | Prior agent's research on the product's features, modules, and data domains | Useful for establishing what data the product stores (baseline for gap analysis) |
| `ehi-export-report.md` | Prior agent's narrative analysis of the export documentation | Useful for orientation; independently verified against primary HTML source |
| `chpl-metadata.json` | CHPL certification details | Confirms certification criteria and product version |

**Verification notes**: The live URL (https://carepaths.com/features/onc-certification/b10-export-format/) was verified on 2026-02-16 and returned HTTP 200 with identical content size (93,196 bytes). No additional downloadable artifacts, data dictionaries, schemas, or sample exports were found on the vendor's website — the prior report's claim of "no downloadable files" was independently confirmed.

## 3. Export Mechanics

- **Format**: ZIP file per patient containing 7 file categories (CDA XML, PDFs, TXT, and files in unspecified or original formats)
- **Mechanism**: Admin UI — users with "record management permissions" access the export from the "exports dropdown" on the patient management overview, select patients, and receive ZIPs via the internal messaging system
- **Single-patient**: Yes — select individual patients for export
- **Bulk capability**: Technically yes, but constrained — vendor documentation states "For full patient population exports, please contact support or schedule the export for outside business hours. Running bulk exports can be resource heavy, and doing so during the day may affect EHR functionality."
- **Access constraints**: Requires admin role with record management permissions
- **Fees**: Not mentioned in the documentation

## 4. Export Content: What's In It

The export documentation describes 7 file categories per patient ZIP. There is **no data dictionary, no field-level documentation, no schema, and no sample data**. The documentation consists entirely of a brief prose description of each file type.

### No data dictionary exists

- **Total entities documented**: 7 file categories (not database tables/entities)
- **Total fields documented**: 0
- **Fields with descriptions**: 0 (no field-level documentation exists)
- **Types documented**: No
- **Relationships/foreign keys**: No
- **Value sets/code systems**: No
- **Machine-readable schemas**: No
- **Sample data**: No

### Vendor's own content organization

The vendor does not organize the export into data domains or categories. The documentation is a flat numbered list of 7 file types:

| # | File Category | Format | Naming Convention | Structured? | Computable? |
|---|---|---|---|---|---|
| 1 | CCD (Continuity of Care Document) | XML (CDA) | `cda_PATIENT_NAME.xml` | Yes | Yes |
| 2 | Accounting Statement | PDF | `PATIENT_ID_Statements_asOfDate.pdf` | No | No |
| 3 | Messaging History | TXT | `PATIENT_ID_Message_History_asOfDate.txt` | No | No |
| 4 | Patient Charts (completed service documents, grouped by year) | PDF | `PATIENT_ID_Chart_Year.pdf` | No | No |
| 5 | Audit Logs | Unspecified | Unspecified | Unknown | Unknown |
| 6 | Appointment History and Statuses | Unspecified | Unspecified | Unknown | Unknown |
| 7 | Document/Image Uploads | Original format | As uploaded | Varies | Varies |

**Key observations**:

- Only 1 of 7 file categories (CCD) is in a structured, computable format
- 2 of 7 categories don't even specify their file format (Audit Logs, Appointment History)
- 3 of 7 categories are PDFs or TXT — human-readable but not machine-processable
- The CCD (CDA XML) is a clinical summary standard, not a comprehensive data export format. A CCD typically contains demographics, problems, medications, allergies, vitals, procedures, and results — roughly equivalent to USCDI/US Core scope
- The "Patient Charts" PDFs are annual compilations of rendered clinical documents — structured data (diagnosis codes, CPT codes, assessment scores, treatment plan goals) is flattened into non-computable PDF format

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes the export as 7 file categories without organizing them into clinical/billing/administrative domains. In terms of actual coverage:

- **Clinical data**: Covered via two mechanisms — the CCD XML (structured summary of demographics, problems, meds, allergies, vitals) and the Patient Charts PDFs (rendered copies of progress notes, intakes, treatment plans). The CCD provides structured but limited clinical data; the PDFs provide broader clinical documentation but in non-computable form.
- **Billing/financial**: Covered only as a PDF accounting statement — a rendered summary of transactions, not the underlying structured billing data (claims, remittances, CPT codes, payer information).
- **Communications**: Covered as a TXT file of messaging history — preserves message content but likely loses metadata (timestamps, sender/recipient identification, read status).
- **Appointments**: Listed as included but with no format specified.
- **Documents**: Patient-uploaded files are included in original format.
- **Audit logs**: Listed as included but with no format specified. (Note: audit logs are not EHI per the designated record set definition.)

**What is conspicuously absent**:
- **Outcomes/assessment data (MBC)**: CarePaths' core differentiator — PHQ-9, GAD-7, OQ-45, HAM-A, and 20+ other standardized instrument responses collected longitudinally — is not mentioned anywhere in the export documentation. This is clinical data used directly for treatment decisions.
- **Structured billing data**: The underlying X12 claims, electronic remittance records, payer information, CPT/diagnosis code associations, and payment details are not exported as structured data — only a PDF summary is provided.
- **Insurance/coverage information**: Not mentioned.
- **Treatment plan structured data**: Goal status, target dates, interventions, and progress tracking are presumably rendered into the Chart PDFs, losing structure.
- **E-prescribing data**: Medication data from the DrFirst/Rcopia integration is not specifically mentioned.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | CCD XML likely includes demographics per CDA standard, but no documentation of which fields | Product stores demographics (certified for (a)(5)); CCD probably covers basics but completeness is undocumented |
| Encounters / visits | ⚠️ Partial | Patient Charts PDFs contain rendered service documents grouped by year; Appointment History listed (format unspecified) | Encounter data exists in PDFs but not in structured form; appointment data format unknown |
| Problems / conditions / diagnoses | ⚠️ Partial | CCD XML likely includes problem list per CDA standard | Probably covers active problems; completeness of diagnosis history unclear |
| Medications / prescriptions | ⚠️ Partial | CCD XML likely includes medications per CDA standard | E-prescribing data from DrFirst/Rcopia integration may not be fully represented |
| Allergies | ⚠️ Partial | CCD XML likely includes allergies per CDA standard | Typical CDA section; completeness undocumented |
| Immunizations | N/A | Not mentioned | Behavioral health product — immunizations are not a core data domain |
| Vitals | ⚠️ Partial | CCD XML likely includes vitals per CDA standard | Behavioral health context means vitals may be limited |
| Lab results | ⚠️ Partial | CCD XML may include results per CDA standard; product certified for CPOE labs | Limited relevance for behavioral health; if results are stored, CCD may cover them |
| Imaging / diagnostic reports | N/A | Not mentioned | Not a core feature of this behavioral health product |
| Procedures | ⚠️ Partial | CCD XML likely includes procedures per CDA standard | Behavioral health procedures are primarily therapy sessions documented in Chart PDFs |
| Clinical notes / documents | ⚠️ Partial | Patient Charts PDFs contain rendered clinical documents (progress notes, intakes, treatment plans) | Content is present but in non-computable PDF format — structured data is destroyed |
| Care plans / goals | ⚠️ Partial | Treatment plans presumably rendered in Patient Charts PDFs | Structured goal tracking data (status, dates, interventions) is lost in PDF rendering |
| Orders / referrals | ⚠️ Partial | CCD may include orders per CDA standard | Limited relevance for behavioral health |
| Insurance / coverage | ❌ Not covered | No insurance entities mentioned in export | Product stores insurance information and performs eligibility checks; gap |
| Claims / billing | ⚠️ Partial | Accounting Statement PDF covers transactions | PDF summary only — structured claims (X12), remittances, CPT codes, payer details not exported as data. Product generates X12 claims and processes electronic remittances; significant gap |
| Payments | ⚠️ Partial | Accounting Statement PDF may include payments | PDF summary only — structured payment records, credit card transaction details not exported as data |
| Consents / directives | ❌ Not covered | Not mentioned | Product likely captures consent forms; gap if stored |
| Patient communications / portal messages | ⚠️ Partial | Messaging History TXT file | Content preserved but metadata (timestamps, sender, read status) likely lost in TXT format |
| Specialty-specific: Behavioral health assessments (MBC) | ❌ Not covered | **Not mentioned anywhere in export documentation** | **Critical gap.** CarePaths' core feature is measurement-based care with 20+ standardized instruments (PHQ-9, GAD-7, OQ-45, etc.) tracked longitudinally. These assessment responses are clinical records used directly for treatment decisions. Their absence from the export is the single most significant gap. |

**Summary**: Of 15 applicable domains, 0 are fully covered (✅), 11 are partially covered (⚠️), 3 are not covered (❌), and 2 are N/A. The "partial" ratings are generous — they reflect that data may exist somewhere in the CCD or PDFs, but there is no documentation to confirm, and most clinical data is exported in non-computable formats.

## 6. Documentation Quality

The documentation is **extremely minimal** — the entire B.10 export specification is approximately 39 lines of prose on a single web page. It is among the thinnest export documentation possible while still describing anything at all.

**What's missing**:
- No data dictionary at any level of granularity
- No field names, types, descriptions, value sets, or relationships
- No schema or format specification for the CDA XML (which template? which sections? which coded values?)
- No format specification at all for 2 of 7 file categories (Audit Logs, Appointment History)
- No sample export files or worked examples
- No import guidance or integration documentation

**Could a developer build an import from this documentation?** No. A developer receiving this export would need to reverse-engineer the CDA XML structure, parse unspecified audit log and appointment formats, and OCR/manually extract structured data from PDF chart compilations. The behavioral health assessment data — the product's core clinical differentiator — is not even mentioned, so a developer would have no way to know it's missing.

**Machine-readable artifacts**: None. No schemas, no sample data, no JSON/XML format specifications.

## 7. Overall Assessment

### Classification

**Minimal/stub**: The documentation is too thin to fully assess, and the export clearly covers only a fraction of what the product stores. The export appears to be a "print-to-file" approach — rendering structured database records into PDFs and wrapping them with a CDA clinical summary — rather than a genuine structured data export. The most significant clinical data domain (behavioral health assessments/MBC) is entirely absent from the export documentation.

### Key Findings

1. **The product's core clinical feature is missing from the export.** CarePaths' primary differentiator is measurement-based care with 20+ standardized behavioral health instruments (PHQ-9, GAD-7, OQ-45, etc.) tracked longitudinally. These assessment responses — clinical data used directly for treatment decisions — are not mentioned anywhere in the export documentation. This is the single most significant gap. *(Source: `b10-export-format.html` — no mention of assessments, outcomes, or MBC; `product-research.md` documents MBC as core feature)*

2. **Almost all exported data is in non-computable formats.** Of 7 file categories, only the CCD XML is structured and computable. Clinical documentation is rendered into annual PDF compilations, billing is a PDF statement, and messaging is a TXT file. Two categories (Audit Logs, Appointment History) don't even specify their format. *(Source: `b10-export-format.html` file type listing)*

3. **Structured billing data is replaced by a PDF summary.** The product maintains X12 claims, electronic remittances, CPT code associations, and detailed payment records, but the export provides only a rendered PDF accounting statement. *(Source: `b10-export-format.html` — "Accounting Statement listing Patient's accounting transactions" in PDF format)*

4. **Zero field-level documentation exists.** The entire export specification is ~39 lines of prose. No data dictionary, no schema, no sample data, no field names or types. A developer cannot build an import from this documentation. *(Source: `b10-export-format.html` — complete documentation consists of brief descriptions of 7 file categories)*

5. **The CCD provides only clinical-summary-level data.** The CDA/CCD is a standardized clinical summary format covering approximately the same scope as USCDI — demographics, problems, medications, allergies, vitals, procedures, results. It does not cover behavioral health assessments, custom forms, billing details, or specialty-specific data. *(Source: CDA standard scope; vendor provides no documentation of CCD section coverage)*

### Summary Stats

```
Classification:  Minimal/stub
Export format:   Mixed (CDA XML, PDF, TXT, unspecified)
Model type:      Standard projection (CDA) + print-to-file (PDF/TXT)
Entities:        7 file categories (not database entities)
Fields:          0 documented
Descriptions:    N/A (no field-level documentation)
Sample data:     No
Bulk export:     Yes (with constraints — contact support)
Domains covered: 0 of 15 fully; 11 of 15 partially (mostly via non-computable formats)
```

### Bottom Line

A patient or provider would receive a ZIP file containing a clinical summary XML, rendered PDF compilations of their chart and billing statement, a text file of messages, and some metadata files in unspecified formats. The most clinically important data — longitudinal behavioral health assessment scores (PHQ-9, GAD-7, OQ-45, etc.) that drive treatment decisions — appears to be entirely absent. The export's reliance on PDF rendering means that even the data that is included cannot be computationally processed or imported into another system. This is a compliance-checkbox export, not a genuine effort to provide patients with their complete electronic health information in a usable format.
