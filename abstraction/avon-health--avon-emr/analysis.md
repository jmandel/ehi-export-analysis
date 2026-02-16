# EHI Export Analysis: Avon Health

**Product**: Avon EMR  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 11636 (15.04.04.3227.Avon.01.00.1.250514)

## 1. Product Context

Avon EMR is a cloud-based, all-in-one ambulatory EMR and practice management platform from Avon Health, a startup founded in 2021. It targets solo and small-group ambulatory practices across specialties including primary care, behavioral health, women's health, pediatrics, hospice, and geriatrics. The product was ONC-certified in May 2025.

The platform is modular and includes: clinical documentation (visit notes, care plans, clinical notes, AI Scribe), e-prescribing, lab ordering (1000+ labs), imaging orders, scheduling (virtual and in-person), patient engagement (portal, messaging, forms, courses), practice management and billing (eligibility checks, invoicing, superbills, payment collection, revenue cycle management, insurance claims), analytics/reporting, and administration. It also exposes a FHIR API certified under (g)(10).

For a (b)(10) export, we would expect coverage of: demographics, problem lists, medications, allergies, immunizations, family history, vitals, procedures, lab/imaging results, clinical notes, care plans, prescriptions, appointments, insurance/coverage details, claims, payments, superbills, invoices, patient portal messages, forms/intake data, uploaded documents, and patient communications (SMS, in-app messaging).

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/ehi-export.html` (52,873 bytes) | Single HTML page at `guides.avonhealth.com/docs/ehi-export` describing the (b)(10) export mechanism, format, and data categories. **Primary artifact.** | Moderate — describes export mechanics and lists data categories, but provides no field-level detail |
| `downloads/ehi-export-page-screenshot.png` (466 KB) | Screenshot of the EHI export documentation page | Low — confirms HTML content visually |
| `downloads/certification-page-screenshot.png` (664 KB) | Screenshot of the ONC certification page at `avonhealth.com/meaningful-use` | Low — shows certified criteria and links |

Only 3 artifacts were collected. There is no data dictionary, no sample export, no schema, and no additional documentation beyond the single HTML page.

## 3. Export Mechanics

- **Format**: ZIP file containing CSV files, PDF documents, and PNG images
- **Single-patient**: Admin navigates to patient profile → clicks "Export EHI" button
- **Bulk/population**: Must email `support@avonhealth.com` with subject "Patient Population b10 Export Request"; handled manually by Avon Support team based on data size/server resources
- **Population export structure**: One directory per patient named `<FirstName><LastName>_<MRN>`, mirroring individual export contents
- **Access constraints**: Population export requires vendor assistance; no self-service bulk export
- **Fees**: Not documented on the EHI export page

## 4. Export Content: What's In It

The documentation provides only a **high-level category list** with bullet points — not a data dictionary. There are no CSV column names, no data types, no field descriptions, no relationships, no value sets, and no sample data. The 24 items listed are data domain labels (e.g., "Vital signs," "Lab results"), not field/column definitions.

### Vendor's own content organization

The vendor organizes the export into 4 categories with 24 listed items total (parsed from `downloads/ehi-export.html`; see `analysis/entity-inventory-full.json`):

| Category (vendor's) | Items Listed | Fields Described | Types Documented |
|---|---|---|---|
| Demographics | 6 | 0 | No |
| Clinical Information | 12 | 0 | No |
| Administrative and Billing Information | 4 | 0 | No |
| Other Documents | 2 | 0 | No |
| **Total** | **24** | **0** | **No** |

**Demographics items**: Name, Date of birth, Sex, Race and ethnicity, Language preferences, Addresses

**Clinical Information items**: Allergies and adverse reactions, Medications (including prescription history and active medications), Problem list (diagnoses), Immunizations, Family history, Vital signs, Procedures, Surgical history, Lab results, Imaging results, Clinical notes (progress notes, H&P, discharge summaries), Care plans

**Administrative and Billing Information items**: Appointments, Insurance details, Insurance claims, Payment history

**Other Documents items**: Forms, Uploaded documents (PDFs) and images (PNGs)

These are data domain names, not entity/table definitions. There is no information about:
- How many CSV files are generated
- What columns each CSV contains
- Data types or formats for any field
- Relationships between files
- Coded value sets or terminologies used
- Whether any fields map to standard vocabularies (SNOMED, ICD-10, LOINC, RxNorm)

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's documentation lists 4 categories spanning 24 high-level data domains. The categories are broad and plausible for an ambulatory EMR:

- **Demographics** (6 items): Standard patient identifiers — name, DOB, sex, race/ethnicity, language, addresses. No mention of phone numbers, email, emergency contacts, or MRN (though MRN appears in the folder naming convention).
- **Clinical Information** (12 items): Covers the core USCDI clinical domains — allergies, medications, problems, immunizations, family history, vitals, procedures, lab/imaging results, clinical notes, care plans. Also includes surgical history as a separate item. This is the broadest category.
- **Administrative and Billing Information** (4 items): Includes appointments, insurance details, insurance claims, and payment history. This goes beyond USCDI, which is a positive signal.
- **Other Documents** (2 items): Forms and uploaded documents/images.

Without field-level detail, it is impossible to assess the *depth* of coverage within any domain. "Lab results" could mean a single CSV with result values, or it could include order details, specimen info, reference ranges, performing lab identifiers, etc. The documentation doesn't say.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | 6 items listed (name, DOB, sex, race/ethnicity, language, addresses) | Product stores phone, email, emergency contacts, MRN — none explicitly listed. Depth unknown. |
| Encounters / visits | ⚠️ Partial | "Appointments" listed under Admin/Billing | Appointments listed, but no mention of encounter details (visit type, duration, provider, location, diagnoses linked to visit). Product has detailed visit notes. |
| Problems / conditions | ✅ Covered | "Problem list (diagnoses)" listed | Listed but depth unknown (codes? onset dates? status?). |
| Medications / prescriptions | ✅ Covered | "Medications, including prescription history and active medications" listed | Listed but depth unknown. Product has e-prescribing; no mention of Rx details (pharmacy, dosage, refills). |
| Allergies | ✅ Covered | "Allergies and adverse reactions" listed | Depth unknown. |
| Immunizations | ✅ Covered | "Immunizations" listed | Depth unknown. |
| Vitals | ✅ Covered | "Vital signs" listed | Depth unknown. |
| Lab results | ✅ Covered | "Lab results" listed | Depth unknown. Product integrates with 1000+ labs. |
| Imaging / diagnostic reports | ✅ Covered | "Imaging results" listed | Depth unknown. |
| Procedures | ✅ Covered | "Procedures" and "Surgical history" listed | Depth unknown. |
| Clinical notes / documents | ✅ Covered | "Clinical notes (e.g., progress notes, history and physical, discharge summaries)" listed | Likely exported as PDFs in the ZIP. |
| Care plans / goals | ✅ Covered | "Care plans" listed | Depth unknown. |
| Orders / referrals | ❌ Not covered | Not mentioned | Product supports lab orders, imaging orders, referrals. Significant gap. |
| Insurance / coverage | ✅ Covered | "Insurance details" listed | Depth unknown. |
| Claims / billing | ✅ Covered | "Insurance claims" listed | Depth unknown. Product has claims, superbills, invoicing. |
| Payments | ✅ Covered | "Payment history" listed | Depth unknown. |
| Consents / directives | ❌ Not covered | Not mentioned | Product may store consent forms via Forms module. |
| Patient communications | ❌ Not covered | Not mentioned | Product has in-app messaging, 2-way SMS, portal messages — none mentioned in export. Significant gap. |
| Forms / questionnaires | ✅ Covered | "Forms" listed under Other Documents | Listed but depth unknown. |
| Superbills | ❌ Not covered | Not explicitly mentioned | Product has superbill functionality; not listed in export. May be included under "Insurance claims" but unclear. |
| Invoices | ❌ Not covered | Not mentioned | Product has invoicing; not listed in export. |

**Summary**: 14 of 20 applicable domains have at least nominal coverage. 6 domains are missing or not mentioned (orders/referrals, consents, patient communications, superbills, invoices, and encounter details beyond appointments). However, because there's no field-level documentation, every "✅ Covered" domain carries uncertainty — we know the category is listed but not what data actually appears in the CSV files.

## 6. Documentation Quality

The EHI export documentation is **minimal**. It consists of a single web page with approximately 250 words of substantive content (excluding navigation and boilerplate).

**What's provided:**
- Clear description of the export mechanism (single-patient button, population via email)
- Export format (ZIP with CSV/PDF/PNG)
- High-level data categories (4 groups, 24 items)

**What's missing:**
- No data dictionary (field names, types, descriptions)
- No sample export files
- No schema or structural documentation
- No CSV column specifications
- No documentation of how many files are generated
- No relationship/foreign key documentation
- No value set or terminology documentation
- No documentation of coded fields or code systems

**Could a developer build an import from this documentation?** No. A developer would know the export is a ZIP with CSVs, PDFs, and PNGs, but would have no idea what CSV files to expect, what columns they contain, or what format the data takes. They would need a sample export to reverse-engineer the structure.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The vendor *claims* to include clinical, demographic, billing, and document data in the export — which would be broader than a USCDI-only clinical summary. The inclusion of "Insurance claims," "Payment history," and "Insurance details" suggests the vendor has at least considered billing data, which goes beyond a pure clinical exchange export. However, the lack of any field-level documentation makes it impossible to verify the actual depth of coverage. Several product domains are not mentioned (patient communications, superbills, invoices, orders/referrals, encounter details). The documentation is so thin that "Partial" is the most generous defensible classification — the categories listed are plausible but unverifiable.

**Axis 2 — Export approach: Purpose-built EHI export**

The export is clearly purpose-built for (b)(10), not a repackaged C-CDA or FHIR API:
- It uses a custom format (ZIP with CSVs/PDFs/PNGs) rather than C-CDA or FHIR
- The documentation explicitly references §170.315(b)(10)
- It includes billing/administrative categories not present in the vendor's (g)(10) FHIR API
- It has a dedicated UI button and population export workflow
- There is no reference to USCDI, US Core, or C-CDA in the export documentation

The vendor built something for (b)(10), but documented it minimally.

### Key Findings

1. **No data dictionary exists.** The entire EHI export documentation is a single web page listing 24 high-level data domain labels (e.g., "Vital signs," "Lab results") with zero field-level detail — no column names, no data types, no descriptions. This is the most significant deficiency. (`downloads/ehi-export.html`)

2. **The export is purpose-built, not repackaged.** The ZIP-with-CSVs format, dedicated export button, and inclusion of billing categories confirm this is a (b)(10)-specific mechanism, not a relabeled C-CDA or FHIR export.

3. **Billing categories are listed but unverifiable.** "Insurance details," "Insurance claims," and "Payment history" appear in the documentation, suggesting the vendor considered billing data. But without field-level detail or sample data, the actual depth is unknown. Superbills and invoices — distinct product features — are not mentioned.

4. **Patient communications are entirely absent.** The product has in-app messaging, 2-way SMS, and a patient portal with messaging — none of which are mentioned in the export documentation. This is a likely gap given the product's emphasis on patient engagement.

5. **No sample data or schema is provided.** Without any sample export file or structural documentation, neither patients nor developers can evaluate what the export actually contains before requesting one.

### Summary Stats

```
Coverage:        Partial
Approach:        Purpose-built EHI export
Export format:   ZIP (CSV + PDF + PNG)
Entities:        N/A (no data dictionary; 4 high-level categories listed)
Fields:          N/A (24 domain labels listed, not field definitions)
Descriptions:    N/A (0% — no field-level documentation exists)
Sample data:     No
Bulk export:     Yes (vendor-assisted via email request)
Domains covered: 14 of 20 applicable domains nominally listed
```

### Bottom Line

Avon Health built a purpose-specific (b)(10) export that produces a ZIP of CSVs, PDFs, and images, and the documentation claims coverage of clinical, demographic, billing, and document data. However, the documentation is so thin — just 24 bullet-point labels with no field-level detail, no sample data, and no schema — that it is impossible to verify the actual completeness of the export. The single biggest gap is the complete absence of a data dictionary: a patient or developer receiving this export would have to reverse-engineer the CSV structure with no guidance.
