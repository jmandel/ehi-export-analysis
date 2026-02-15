# EHI Export Analysis: Patient First

**Product**: PAS (Version 2015.0.0.1)
**Analysis date**: 2026-02-15
**CHPL ID**: 15.04.04.2140.PAS1.15.02.1.221212 (CHPL #11065)

## 1. Product Context

Patient First Corporation operates ~79 urgent care / primary care walk-in clinics across Virginia, Maryland, Pennsylvania, and New Jersey. PAS is their **self-developed, internal-only EHR system** — not sold or licensed externally. It is a full EHR covering clinical documentation, CPOE (medications, labs, imaging), e-prescribing (via Surescripts), on-site lab and x-ray, on-site medication dispensing, patient portal, billing, quality reporting, public health reporting, and a FHIR API. It is certified for 30+ ONC criteria.

Key data domains PAS stores, relevant to export completeness:
- **Clinical**: encounter notes, problem lists, medications, allergies, vitals, immunizations, lab orders/results, imaging orders, procedures, family history, implantable devices, clinical decision support interactions
- **E-Prescribing**: ~479,000 prescriptions/quarter across 4 states
- **Imaging**: on-site digital x-ray at every location
- **Billing/Financial**: charges, claims, payments, statements, balances (patients can view/pay via portal)
- **Occupational Health**: DOT physicals, workers' comp, drug testing, employer portal
- **Documents**: scanned insurance cards, photo IDs, consult/referral documents
- **Patient Portal**: secure messaging, lab results, visit history, billing
- **Public Health**: immunization registry submissions, syndromic surveillance

The product handles ~1.9M e-prescriptions, ~716K C-CDAs, ~240K portal logins, and ~3.3M syndromic surveillance messages per year (Q1 2025, annualized). This is a high-volume system with broad functionality for an urgent care chain.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `mandatory-disclosure-page.html` (530 KB) | Full WordPress page with all mandatory disclosures. The EHI Export section is one paragraph + a 7-row HTML table. Verified against live site on 2026-02-15 — content identical. | **Primary source** — this IS the entire EHI export documentation |
| `mandatory-disclosure-page-api.json` (26 KB) | WordPress REST API JSON of same page. Cleaner for parsing; same content. | Duplicate of above, useful for scripting |
| `PatientFirst_Real_World_Test_Results_CY2025.pdf` (23 pages, 227 KB) | CY 2025 RWT report dated Feb 2, 2026. RWT Measure #3 covers b(10). | **Key secondary source** — reveals the b(10) metric is labeled "Number of C-CDA Batch Exports Sent" |
| `screenshot-ehi-export-section.png` (213 KB) | Browser screenshot of the EHI Export section showing the paragraph and 7-row table | Confirms visual layout; matches parsed content |
| `screenshot-page-top.png` (252 KB) | Screenshot of page header with certification details | Minimal additional value |

**No data dictionary, schema files, sample exports, or API documentation exist.** The entire EHI export documentation is ~150 words of prose and a 7-row × 4-column table.

## 3. Export Mechanics

- **Format**: Compressed ZIP archive containing files organized into 7 folders by category
- **Mechanism**: Manual, one-time export initiated within the EHR ("EHI Export functionality allows health systems to do a manual one-time export of health data")
- **Scope**: Single-patient export (the description says "a patient's record")
- **Bulk capability**: The RWT measure description mentions "bulk patient exports" alongside individual requests, but no separate bulk mechanism is documented
- **Access constraints/fees**: Not documented. The export appears to be an internal tool operated by Patient First staff — there is no self-service patient export described
- **Volume**: 31 exports in Q1 2025 (20 VA, 6 MD, 5 PA, 0 NJ), annualized ~124/year across ~79 clinics — very low utilization

**Notable RWT finding**: The b(10) testing metric in the CY 2025 RWT report (p. 13) is labeled **"Number of C-CDA Batch Exports Sent"** despite being associated with criterion 315(b)(10). The measurement description says "tracking and counting how many patients requested and received EHI exports of their health information by the EHR Module as well as number of bulk patient exports." The mismatch between the metric label ("C-CDA Batch Exports") and the intended scope (full EHI export) raises a question about whether the b(10) export is truly multi-format as documented, or primarily C-CDA-based in practice.

## 4. Export Content: What's In It

The export contains 7 categories of data in a multi-format ZIP archive. There is **no data dictionary, no field-level documentation, no schema, and no sample data** for any category. Documentation exists only at the category level.

### Vendor's own content organization

| Category | Description (vendor's) | Folder | Format | Field-Level Docs | Schema |
|---|---|---|---|---|---|
| Medical Records | Medical records in industry-standard C-CDA format | `CCDA` | XML (C-CDA) | No | No (standard C-CDA, but no template/profile specified) |
| X-Rays | X-Ray images | `Xray` | DCM (DICOM) | No | No (DICOM is self-describing) |
| Scanned Images | Insurance Cards, Photo ID, etc. | `Scan/{type}` (e.g., `InsCard`, `PhotoID`) | JPG, PNG | No | N/A (images) |
| Consults | Documents from referrals | `ConsultNotes` | PDF | No | N/A (documents) |
| Messages | Secure Messages sent to and from the patient | `DirectSecureMessages` | EML | No | No |
| Forms | Various forms, such as Drug Screen results | `Forms` | PDF | No | N/A (documents) |
| Financials | Billing and Claim information | `BillingClaim` | JSON | No | No |

**Total entities/tables**: 7 top-level categories. No sub-entity or field-level breakdown is provided for any category.

**Total fields**: Unknown — no field-level documentation exists. The C-CDA format has a known structure (per the HL7 C-CDA standard), and DICOM is self-describing, but the JSON financial format and EML message structure are completely undocumented.

**Key observations**:
1. **Medical Records (C-CDA)**: The clinical data backbone. C-CDA is a well-defined standard, so a recipient familiar with C-CDA can parse this. However, no implementation guide, template IDs, C-CDA version, or custom extensions are documented. It is unknown which C-CDA sections are populated — a C-CDA can range from a bare-minimum clinical summary to a comprehensive document.
2. **Financials (JSON)**: The only structured computable format besides C-CDA. No schema, no field names, no sample data — a recipient would need to reverse-engineer the JSON structure. This is the most significant documentation gap: billing data in an undocumented proprietary format.
3. **Documents (PDF, JPG, PNG)**: Three of the 7 categories are non-computable document formats. These preserve originals but cannot be programmatically parsed for structured data.
4. **DICOM**: A strong choice for x-ray export — DICOM is the native medical imaging standard and is self-describing with metadata headers.
5. **EML**: Standard email format for messages, reasonable for preserving message content.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor organizes the export into 7 categories. The richest structured data is in two categories:

- **Medical Records (C-CDA)**: Contains the clinical data — problems, medications, allergies, vitals, procedures, lab results, immunizations, etc. However, C-CDA is a clinical summary standard; it captures a subset of what an EHR stores natively. Discrete data like individual lab order details, clinical decision support alerts, detailed encounter metadata, and custom clinical forms are typically lost in C-CDA translation.
- **Financials (JSON)**: Contains billing and claims data in a computable format. This is notable — many vendors omit billing entirely from b(10) exports. However, the complete absence of documentation for this JSON format significantly reduces its utility.

The remaining 5 categories are document/image-level exports:
- **X-Rays (DICOM)**: Excellent inclusion for an urgent care chain with on-site imaging.
- **Scanned Images**: Administrative documents (insurance cards, photo IDs).
- **Consults (PDF)**: Referral documents — important for continuity of care.
- **Messages (EML)**: Patient-provider secure messages.
- **Forms (PDF)**: Miscellaneous forms including drug screen results.

The export is **broader than typical C-CDA-only exports** and shows awareness that EHI goes beyond clinical summaries. The inclusion of billing, imaging, messages, and scanned documents reflects genuine effort. However, all non-C-CDA structured data is undocumented.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA includes demographics section; scanned photo IDs in `Scan/PhotoID` | C-CDA demographics is limited to USCDI elements. Registration details, extended contact info, and insurance plan details beyond scanned card images likely not fully captured |
| Encounters / visits | ⚠️ Partial | C-CDA documents encounters but as summaries; visit history available in portal | C-CDA flattens encounter data. PAS tracks visits across ~79 locations — encounter-level metadata (site, provider, visit type, timestamps) may lose granularity |
| Problems / conditions / diagnoses | ⚠️ Partial | C-CDA problem list section | Covered via C-CDA standard sections, but limited to what the C-CDA template includes |
| Medications / prescriptions | ⚠️ Partial | C-CDA medications section | C-CDA includes medication lists. However, PAS processes ~479K e-prescriptions/quarter — the full prescription transaction records (Surescripts messages, dispensing records from on-site medication dispensing) are unlikely to be captured in C-CDA |
| Allergies | ⚠️ Partial | C-CDA allergies section | Standard C-CDA coverage |
| Immunizations | ⚠️ Partial | C-CDA immunizations section | Standard C-CDA coverage; ~16K immunization registry messages/quarter suggest significant immunization activity |
| Vitals | ⚠️ Partial | C-CDA vital signs section | Standard C-CDA coverage |
| Lab results | ⚠️ Partial | C-CDA results section | C-CDA includes results but PAS runs on-site CLIA labs at every location — discrete lab order data, order-level metadata, and full result panels may lose detail in C-CDA translation |
| Imaging / diagnostic reports | ✅ Covered | `Xray` folder with DICOM files | Strong coverage — DICOM is the native imaging format. Includes the actual images, not just reports |
| Procedures | ⚠️ Partial | C-CDA procedures section | Standard C-CDA coverage |
| Clinical notes / documents | ⚠️ Partial | C-CDA may include notes sections; `ConsultNotes` (PDF) for referral documents; `Forms` (PDF) for miscellaneous forms | C-CDA may include some notes. Consults and forms are exported as PDFs (non-computable). Full progress notes, H&P documents, and encounter-specific notes from ~79 clinics are not explicitly documented as included |
| Care plans / goals | ⚠️ Partial | C-CDA may include care plan section if populated | Unclear — depends on C-CDA template used |
| Orders / referrals | ⚠️ Partial | `ConsultNotes` includes referral documents (PDF) | Referral documents are exported but as PDFs. Structured order data (lab orders, imaging orders, CPOE records) is not explicitly documented |
| Insurance / coverage | ⚠️ Partial | Scanned insurance cards in `Scan/InsCard`; financial JSON may contain coverage data | Insurance card images are included but structured insurance/coverage data depends on undocumented JSON format |
| Claims / billing | ⚠️ Partial | `BillingClaim` folder with JSON files | Billing data IS included — a notable positive. However, the JSON format is completely undocumented. No schema, no field names, no sample data. Impossible to assess depth without seeing actual data |
| Payments | ❓ Unclear | May be in financial JSON | Patients can view/pay balances via portal, so PAS stores payment data. Whether payments are in the billing JSON is unknown |
| Consents / directives | ❌ Not covered | No evidence in export categories | Not explicitly listed; may be in C-CDA or Forms but not documented |
| Patient communications / portal messages | ✅ Covered | `DirectSecureMessages` folder with EML files | Secure messages between patient and provider are exported in standard email format |
| Specialty: Occupational Health | ⚠️ Partial | Drug screen results mentioned in Forms (PDF) | Patient First does DOT physicals, workers' comp, and drug testing. Drug screen results are in Forms as PDF, but structured occupational health data (DOT exam records, workers' comp case details, employer-specific records) is not documented |

**Summary**: Of 19 applicable domains, 2 are clearly covered (imaging, portal messages), 14 are partially covered (primarily via C-CDA which provides some coverage but loses native granularity), 1 is not covered (consents), and 2 are unclear (payments, occupational health details). The C-CDA backbone provides baseline clinical coverage but acts as a lossy filter on PAS's native data model.

## 6. Documentation Quality

The EHI export documentation is **minimal**. The entire specification consists of:
- 2 sentences of prose describing the export concept (~50 words)
- 1 sentence about the ZIP format
- A 7-row × 4-column HTML table listing category, description, folder name, and file format

**What's missing**:
- **No data dictionary**: Zero field-level documentation for any export category
- **No JSON schema**: The financial/billing JSON format is entirely undocumented — no field names, types, or structure
- **No C-CDA implementation guide**: No C-CDA version, template IDs, profile, or section inventory specified
- **No sample data**: No example export files of any kind
- **No user/admin guide**: No instructions for requesting, generating, or receiving an export
- **No relationship documentation**: No entity relationships, foreign keys, or cross-references between categories
- **No value sets or code systems**: No documentation of coded values used in any format

**Could a developer build an import from this documentation?** No. A developer could parse the C-CDA using standard C-CDA libraries (if they assume a standard C-CDA profile), view the DICOM images with standard DICOM tools, and read the EML messages with email clients. But the billing JSON would be impenetrable without reverse-engineering, and there would be no way to know what clinical data is in the C-CDA vs. what was lost in translation from PAS's native model.

The documentation quality is below what b(10) compliance requires for meaningful data portability. The export itself may contain useful data, but the documentation provides almost no guidance for interpreting it.

## 7. Overall Assessment

### Classification

**Standard-based projection** with ancillary native files.

The core clinical data is projected through C-CDA — a standard clinical summary format that captures a subset of the native EHR data model. The 6 additional categories (DICOM images, scanned documents, consult PDFs, secure messages, forms, and billing JSON) supplement the C-CDA with data types that C-CDA cannot represent, which is commendable. However, the clinical data backbone remains a C-CDA projection, not a native database export. There is no evidence that PAS's internal tables, custom fields, or proprietary data structures are exported in their native form (except possibly the billing JSON, which is undocumented).

### Key Findings

1. **Multi-format export goes beyond typical C-CDA repackaging**: The 7-category ZIP with DICOM images, billing JSON, secure messages (EML), and scanned documents is broader than most vendors' b(10) exports. Patient First shows awareness that EHI extends beyond clinical summaries. (Source: `mandatory-disclosure-page.html`, EHI Export section)

2. **Billing data included but completely undocumented**: The `BillingClaim` JSON is one of the most important categories — billing is a major gap for most vendors. However, with zero documentation (no schema, no field names, no sample data), a recipient cannot interpret the data. (Source: EHI Export table, "Financials" row)

3. **Clinical data funneled through C-CDA loses native granularity**: PAS is a full EHR with CPOE, on-site labs, e-prescribing, and on-site medication dispensing. C-CDA captures clinical summaries but not the full richness of the native data model — order details, CDS interactions, discrete lab panels, prescription transaction records, and encounter-level metadata are likely compressed or lost. (Source: C-CDA is listed as "industry-standard C-CDA format" with no extensions documented)

4. **RWT metric mislabeled, raising questions about export fidelity**: The b(10) Real World Testing metric is labeled "Number of C-CDA Batch Exports Sent" rather than "Number of EHI Exports Run," suggesting the export may be more C-CDA-centric in practice than the 7-category documentation implies. (Source: `PatientFirst_Real_World_Test_Results_CY2025.pdf`, p. 13)

5. **Documentation is a stub — 7 rows, no field-level detail**: The entire export documentation is a single HTML paragraph and table. No data dictionary, no schemas, no sample data, no user guide. This is among the thinnest b(10) documentation of any certified product. (Source: `mandatory-disclosure-page.html`)

### Summary Stats

```
Classification:  Standard-based projection (with ancillary native files)
Export format:   Multi-format ZIP (C-CDA XML, DICOM, JSON, EML, PDF, JPG/PNG)
Model type:      Standard projection (C-CDA) + native ancillary formats
Entities:        7 categories (no sub-entity breakdown)
Fields:          N/A (no field-level documentation)
Descriptions:    N/A (no field-level documentation)
Sample data:     No
Bulk export:     Unclear (mentioned in RWT but not documented)
Domains covered: 2 of 19 fully, 14 of 19 partially (via C-CDA)
```

### Bottom Line

Patient First's EHI export is better than a pure C-CDA repackaging — the inclusion of DICOM images, billing JSON, secure messages, and scanned documents shows genuine effort to export beyond clinical summaries. However, the clinical data backbone is still C-CDA (a lossy standard projection), the billing JSON is completely undocumented, and the total documentation is just 7 table rows with no field-level detail. A patient receiving this export would get their x-rays and messages but would have no way to interpret the billing data, and would receive only a C-CDA summary rather than the full granularity of their clinical record as stored in PAS.
