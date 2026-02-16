# EHI Export Analysis: Patient First

**Product**: PAS (Version 2015.0.0.1)
**Analysis date**: 2026-02-16
**CHPL IDs**: 11065 (15.04.04.2140.PAS1.15.02.0.221212)

## 1. Product Context

Patient First is a privately held chain of ~79 urgent care and primary care walk-in medical centers operating across Virginia, Maryland, Pennsylvania, and New Jersey. PAS is their **internally developed, proprietary EHR system** — built and maintained by Patient First's own MIS department, not sold or licensed externally. This is an unusual case: the healthcare provider organization is also the EHR developer.

PAS is a **full EHR system** covering clinical documentation, CPOE (medications, labs, diagnostic imaging), e-prescribing (via Surescripts), drug-drug/drug-allergy interaction checks (Micromedex), clinical decision support, lab integration (on-site CLIA-approved labs at every location), digital x-ray imaging, transitions of care (C-CDA via DataMotion Direct messaging), a proprietary patient portal, quality reporting, public health reporting (immunization registries, syndromic surveillance), and a FHIR API. PAS is certified for 30+ ONC criteria.

**Key data domains PAS stores** (relevant for assessing export completeness):
- **Clinical**: encounter notes, problem lists, medication lists, allergy lists, vitals, family history, immunizations, implantable device records, lab orders/results, imaging orders, procedures, clinical decision support alerts
- **Administrative**: demographics, insurance information, registration data
- **Financial**: billing records, claims, payments, patient statements/balances
- **Documents/Images**: x-ray images (DICOM), scanned insurance cards, photo IDs, consult/referral documents, drug screen result forms
- **Communications**: secure patient-provider messages via portal
- **Specialty**: occupational health (workers' comp, DOT physicals, drug testing, employer portal data)
- **E-prescribing**: ~479,000 prescriptions per quarter across 4 states
- **Telehealth**: integrated telehealth visits

Operational scale (Q1 2025, annualized): ~1.9M e-prescriptions/year, ~716K transition-of-care C-CDAs/year, ~240K patient portal logins/year, ~3.3M syndromic surveillance messages/year, ~124 EHI exports/year, 0 third-party FHIR API applications connected.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `mandatory-disclosure-page.html` (530 KB) | Full HTML of the mandatory disclosures WordPress page. Contains the EHI Export section: 1 paragraph + 7-row table. This is the **entire** EHI export documentation. | **Primary source** — the only substantive EHI export documentation |
| `mandatory-disclosure-page-api.json` (26 KB) | WordPress REST API JSON for the same page. Easier to parse programmatically; content identical to HTML page. Page last modified 2026-02-02. | Useful for parsing; same content as HTML |
| `PatientFirst_Real_World_Test_Results_CY2025.pdf` (23 pages, 227 KB) | CY 2025 Real World Testing Results. RWT Measure #3 (pp. 13–14) covers b(10) EHI exports. Reveals the metric is labeled "Number of C-CDA Batch Exports Sent" despite being the b(10) measure. Shows 31 exports in Q1 2025. | **Important** — provides usage data and reveals C-CDA/EHI conflation |
| `screenshot-ehi-export-section.png` (213 KB) | Browser screenshot of the EHI Export section. Visually confirms the table content matches the parsed HTML. | Corroborative |
| `screenshot-page-top.png` (252 KB) | Screenshot of page header showing certification details. | Minimally informative for export analysis |

**No other artifacts exist.** There are no data dictionaries, JSON schemas, sample export files, C-CDA template specifications, user guides, or API documentation related to the EHI export. The entire documentation is the inline HTML section on the mandatory disclosures page.

**Verified live page** (2026-02-16): The mandatory disclosure page at `https://www.patientfirst.com/mandatory-disclosure-for-ehr` is accessible and the EHI Export section is unchanged from the downloaded copy.

## 3. Export Mechanics

- **Format**: Compressed (ZIP) archive containing files organized into 7 folders by category. Uses multiple file formats: XML (C-CDA), DCM (DICOM), JPG/PNG, PDF, EML, JSON.
- **Mechanism**: Manual one-time export ("EHI Export functionality allows health systems to do a manual one-time export of health data"). No API-based export. No indication of automated or scheduled capabilities.
- **Scope**: Single-patient export. The documentation describes exporting "a patient's record." No mention of bulk or multi-patient export, though the RWT metric references "bulk patient exports" in its description.
- **Access constraints**: Not documented. No mention of fees, turnaround times, or who can request exports.
- **Volume**: 31 exports in Q1 2025 across ~79 clinics (20 VA, 6 MD, 5 PA, 0 NJ). Annualized ~124/year — very low usage.

## 4. Export Content: What's In It

The EHI export documentation provides **category-level descriptions only** — no field-level documentation, no entity/table definitions, no schemas. The entire content description is the 7-row table below.

### Vendor's own content organization

| Category | Description | Folder Name | File Format | Field-Level Docs |
|---|---|---|---|---|
| Medical Records | Medical records in industry-standard C-CDA format | CCDA | XML (C-CDA) | No (C-CDA is an external standard, but no Patient First implementation guide, template list, or extension documentation is provided) |
| X-Rays | X-Ray images | Xray | DCM (DICOM) | No (DICOM is self-describing, but no metadata documentation) |
| Scanned Images | Insurance Cards, Photo ID, etc. | Scan (subfolders: InsCard, PhotoID, etc.) | JPG, PNG, etc. | No |
| Consults | Documents from referrals | ConsultNotes | PDF | No |
| Messages | Secure Messages sent to and from the patient | DirectSecureMessages | EML (Email File Format) | No |
| Forms | Various forms, such as Drug Screen results | Forms | PDF | No |
| Financials | Billing and Claim information | BillingClaim | JSON | **No** — no schema, no field definitions, no sample data |

**Total entities/tables**: 7 high-level categories (not comparable to a data dictionary)
**Total fields**: N/A — no field-level documentation exists for any category
**Fields with descriptions**: N/A
**Types documented**: Only file formats (C-CDA, DICOM, PDF, EML, JSON, image formats)
**Relationships/foreign keys**: N/A
**Value sets/code systems**: N/A
**Sample data**: None provided

### Notable observations

1. **The Financials category is the only computable, vendor-native data**: The "BillingClaim" folder contains JSON — this is the only category where Patient First is exporting structured data in their own format. However, no schema, field definitions, or sample JSON structure are provided. A recipient would have to reverse-engineer the JSON format.

2. **Medical Records rely entirely on C-CDA**: Clinical data is exported in "industry-standard C-CDA format" — meaning the export's clinical coverage is bounded by whatever C-CDA templates Patient First implements. No documentation specifies which C-CDA templates, sections, or entries are included, or whether any vendor extensions are used.

3. **The RWT report labels the b(10) metric as "Number of C-CDA Batch Exports Sent"**: This is significant. The b(10) export is supposed to be a multi-format ZIP (per the disclosure page), but the RWT metric tracks only "C-CDA Batch Exports." This raises the question of whether the actual b(10) export in practice is just a C-CDA batch rather than the full multi-format ZIP described in the documentation. The section description mentions "patients requested and received EHI exports of their health information by the EHR Module as well as number of bulk patient exports," but the metric name specifically says "C-CDA Batch Exports."

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor organizes the export into 7 categories. In their terms:

- **Medical Records (C-CDA)**: The broadest clinical data category, but its depth is unknown because no C-CDA implementation guide or template list is provided. Standard C-CDA would typically include: demographics, problems, medications, allergies, vitals, procedures, results, immunizations, encounters, care plans. But the specific content depends on Patient First's implementation.
- **X-Rays (DICOM)**: Appropriate for an urgent care chain where on-site x-ray is standard at every location. DICOM files are self-describing and include imaging data plus metadata.
- **Scanned Images**: Administrative documents (insurance cards, photo IDs) — relevant as part of the designated record set.
- **Consults (PDF)**: Referral documents in non-computable format.
- **Messages (EML)**: Patient-provider secure messages — a good inclusion often missing from other vendors' exports.
- **Forms (PDF)**: Drug screen results and other clinical forms — in non-computable format.
- **Financials (JSON)**: Billing and claims in computable format — good to include but undocumented.

**Strengths**: The multi-format approach is practical. Including DICOM images, scanned documents, secure messages, and billing data goes beyond what many vendors offer. The export is clearly not just a C-CDA — it attempts to cover non-clinical and non-structured data.

**Weaknesses**: The clinical data appears to be entirely C-CDA-based (a standard projection, not native data model export). Without knowing which C-CDA templates are implemented, it's impossible to assess clinical data completeness. There are no discrete/structured exports of lab results, encounter details, or order records beyond what C-CDA captures. The financial JSON is completely undocumented.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Likely included in C-CDA `recordTarget`; no dedicated demographics export | C-CDA demographics are typically limited (name, DOB, sex, address, language, race/ethnicity). Richer registration data (emergency contacts, employer info, multi-address history) likely not captured. |
| Encounters / visits | ⚠️ Partial | C-CDA may include encounter sections | Patient First handles millions of visits/year. C-CDA encounter documentation varies; no evidence of discrete encounter data export. |
| Problems / conditions / diagnoses | ⚠️ Partial | Expected in C-CDA Problem section | Standard C-CDA coverage; no indication of whether PAS-specific problem data is fully represented. |
| Medications / prescriptions | ⚠️ Partial | Expected in C-CDA Medications section | C-CDA captures medication lists, but ~479K prescriptions/quarter flow through PAS. Actual e-prescribing transaction records (Surescripts messages) and on-site medication dispensing records are unlikely to be in C-CDA. |
| Allergies | ⚠️ Partial | Expected in C-CDA Allergies section | Standard C-CDA coverage. |
| Immunizations | ⚠️ Partial | Expected in C-CDA Immunizations section | Standard C-CDA coverage; PAS sends ~16K immunization messages/quarter to registries. |
| Vitals | ⚠️ Partial | Expected in C-CDA Vital Signs section | Standard C-CDA coverage. |
| Lab results | ⚠️ Partial | Expected in C-CDA Results section | Every Patient First location has an on-site CLIA-approved lab. C-CDA results may lose granularity vs. PAS's internal structured lab data. |
| Imaging / diagnostic reports | ✅ Covered | X-ray images exported as DICOM files in `Xray` folder | DICOM is the native imaging standard. This is a strong point — actual images, not just reports. |
| Procedures | ⚠️ Partial | Expected in C-CDA Procedures section | Standard C-CDA coverage. |
| Clinical notes / documents | ⚠️ Partial | Consult documents (PDF) in `ConsultNotes`; clinical forms (PDF) in `Forms` | Consult notes and forms are exported as PDFs (non-computable). It's unclear whether encounter progress notes, H&P notes, or other clinical narrative is included in the C-CDA or exported separately. |
| Care plans / goals | ⚠️ Partial | May be in C-CDA if implemented | No evidence this is explicitly included. |
| Orders / referrals | ⚠️ Partial | Consult documents suggest referrals exist; orders may be in C-CDA | PAS has CPOE for meds, labs, and imaging — structured order data is likely not fully captured in C-CDA. |
| Insurance / coverage | ⚠️ Partial | Scanned insurance cards in `Scan/InsCard` folder | Insurance cards are images, not structured insurance plan data (payer, group, policy numbers, coverage dates). |
| Claims / billing | ⚠️ Partial | JSON files in `BillingClaim` folder | Claims/billing data is exported in JSON — a computable format. However, no schema or field definitions exist, so the actual content and completeness is unknown. |
| Payments | ❓ Unknown | Not explicitly mentioned; may be in `BillingClaim` JSON | Patient First's portal allows patients to view/pay balances. Payment data may or may not be in the billing JSON. |
| Consents / directives | ❌ Not covered | No mention in export documentation | Unknown whether PAS stores advance directives or consent forms. Not a clear gap for urgent care. |
| Patient communications / portal messages | ✅ Covered | EML files in `DirectSecureMessages` folder | Secure messages to/from the patient. This is a notable inclusion. |
| Occupational health (specialty) | ⚠️ Partial | Drug screen results mentioned as PDF in `Forms` folder | Patient First offers DOT physicals, workers' comp, drug testing, and an employer portal. Drug screen results are included as PDFs, but structured occupational health data (DOT exam results, workers' comp case details, employer billing) is not clearly documented. |

**Summary**: Of 19 applicable domains, 2 are clearly covered (imaging, portal messages), 14 are partially covered (mostly via C-CDA with uncertain depth), 1 is not covered (consents — arguably N/A for urgent care), 1 is unknown (payments), and 1 is partially covered as a specialty domain. The fundamental problem is that clinical data completeness depends entirely on Patient First's C-CDA implementation, which is undocumented.

## 6. Documentation Quality

**Overall**: Minimal. The entire EHI export documentation consists of a single paragraph and a 7-row HTML table on the mandatory disclosures page. There are no supplementary documents.

**What exists**:
- A brief prose description of what the export is (ZIP archive of health data)
- A table mapping 7 export categories to folder names and file formats
- RWT results showing 31 exports in Q1 2025

**What doesn't exist**:
- No data dictionary for any export category
- No JSON schema for the Financials/BillingClaim data
- No C-CDA implementation guide, template list, or section inventory
- No DICOM metadata documentation
- No sample export files
- No user guide for requesting or performing an export
- No API documentation
- No versioning or change history
- No field definitions, value sets, relationships, or cardinality constraints

**Could a developer build an import from this documentation?** No. A developer receiving this export would know the ZIP folder structure and file formats, but would have:
- **For C-CDA**: general knowledge that it's "industry-standard" C-CDA, but no specifics about Patient First's implementation. They'd have to parse and reverse-engineer the XML.
- **For Financials JSON**: no schema at all. Complete reverse-engineering required.
- **For DICOM**: the DICOM standard is self-describing, so images would be interpretable.
- **For PDFs/images**: viewable but not computable.
- **For EML messages**: standard email format, generally interpretable.

## 7. Overall Assessment

### Classification

**Minimal/stub**

The export documentation is too thin to fully assess content completeness. What documentation exists describes a **multi-format collection** (not a native data model export and not purely a standard projection) that covers 7 categories at a high level. However:

1. The clinical data core is C-CDA — a standard-based projection, not a native data model export. This means clinical data coverage is bounded by C-CDA capabilities and Patient First's implementation thereof.
2. No data dictionary, schema, or field-level documentation exists for any category.
3. The RWT metric labeling ("C-CDA Batch Exports Sent" for b(10)) raises questions about whether the actual export in practice matches the multi-format ZIP described in the documentation.
4. Without sample data or schemas, it's impossible to verify whether the export genuinely contains "all EHI" or just a clinical summary with some ancillary files.

### Key Findings

1. **The RWT b(10) metric is labeled "Number of C-CDA Batch Exports Sent"** (RWT PDF, p. 13), despite the disclosure page describing a multi-format ZIP with 7 categories. This conflation raises a significant concern: is the actual b(10) export just a C-CDA batch, or is it the full ZIP? The metric description does mention "EHI exports" and "bulk patient exports," but the metric name specifically says "C-CDA Batch Exports."

2. **Clinical data is entirely C-CDA-based** with no native data model export. The "Medical Records" category exports C-CDA XML — not PAS database tables. This means clinical data is projected through a standard that may lose PAS-specific detail, custom fields, occupational health assessments, and other data that doesn't map cleanly to C-CDA templates.

3. **The Financials (BillingClaim JSON) is completely undocumented.** This is the only computable, vendor-native data export category, yet there is no schema, no field definitions, no sample data. A recipient cannot interpret this data without reverse-engineering.

4. **The documentation is among the thinnest possible** — 1 paragraph and a 7-row table. No data dictionary, no schema, no sample data, no user guide. For a vendor that built their own EHR from scratch, the absence of any documentation about the underlying data model is a missed opportunity.

5. **The multi-format approach is conceptually sound** — including DICOM images, secure messages, scanned documents, and billing JSON alongside clinical C-CDA data goes beyond what many vendors offer. The intent appears genuine, but the execution and documentation fall short.

### Summary Stats

```
Classification:  Minimal/stub
Export format:   Mixed (C-CDA XML, DICOM, PDF, JPG/PNG, EML, JSON) in ZIP
Model type:      Standard projection (C-CDA) + ancillary files
Entities:        7 categories (no entity/table-level granularity)
Fields:          N/A (no field-level documentation)
Descriptions:    N/A
Sample data:     No
Bulk export:     Unclear (documentation says single-patient; RWT mentions "bulk")
Domains covered: 2 of 19 clearly covered; 14 partially (via undocumented C-CDA)
```

### Bottom Line

Patient First's EHI export is conceptually broader than many vendors' — the multi-format ZIP with DICOM images, secure messages, and billing JSON shows genuine effort to go beyond C-CDA. However, the documentation is too thin to assess actual completeness: no data dictionary, no schemas, no sample data, and the RWT report's "C-CDA Batch Exports" labeling raises concerns about whether the full multi-format export is actually delivered in practice. The biggest gap is the complete absence of field-level documentation — especially for the vendor-native billing JSON — which makes the export effectively unusable without significant reverse-engineering.
