# EHI Export Analysis: Inmediata Health Group, LLC

**Product**: SecureEMR+  
**Analysis date**: 2025-07-16  
**CHPL ID**: 15.04.04.2769.Secu.04.02.1.260116 (listing #11753)

## 1. Product Context

SecureEMR+ is a cloud-based ambulatory EHR built on the PrognoCIS platform (by Bizmatics, Inc.) and localized for the Puerto Rico market by Inmediata Health Group, LLC. It is bundled with Inmediata's practice management/billing module (SecureClaim) and clearinghouse (SecureTrack), giving the product suite end-to-end clinical, billing, and claims capabilities. Inmediata processes approximately 85% of medical claims in Puerto Rico.

The product serves outpatient clinics across 300+ specialties with capabilities including:
- **Clinical**: charting, e-prescribing, lab/imaging ordering, clinical notes, patient portal, CCD generation
- **Billing/PM**: charge capture, claim submission, payment posting, statements, patient advance tracking (via SecureClaim integration)
- **Clearinghouse**: real-time eligibility, claim adjudication, ERA/EOB processing (via SecureTrack)

For a complete EHI export, the product should cover patient demographics, encounters, clinical data across all specialties, medications, labs, imaging, notes, billing/claims data, and insurance information.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `ehi-export-prognocis-self-attestation.pdf` (16 pages, 1.18 MB) | The **sole artifact** — a user guide for SecureEMR+'s EHI export feature. Covers export workflow (single and multi-patient), lists all 47 exportable worksheets, shows 3 field-level examples, and describes the audit trail. | **Primary** — this is the only documentation available |
| `product-research.md` | Prior research on the vendor/product, establishing product capabilities and data domains | Context only |
| `ehi-export-report.md` | Prior agent's analysis of the export documentation | Orientation; contained count errors (stated 43 worksheets, actual is 47) |
| `chpl-metadata.json` | CHPL certification details | Metadata only |
| `files.json` | Manifest of downloaded artifacts | Confirms only 1 artifact was available |

**Note**: The prior report (`ehi-export-report.md`) stated "43+ exportable worksheets" (38 standard + 5 billing). My independent count from the PDF's worksheet list (page 11) yields **42 standard + 5 billing-conditional = 47 total worksheets**.

## 3. Export Mechanics

- **Format**: ZIP file containing `.xls` (spreadsheet), `.txt` (parallel text), and `.pdf` (attached documents) files. One XLS file per worksheet. CCD exports include `.html` and `.xml` files.
- **Mechanism**:
  - *Single patient*: Self-service via UI. Users with `CuresEHIExport` role can export without password or developer assistance. Background generation with email notification. Download from Settings > Configuration > Clinic > Download Files.
  - *All/multiple patients*: Requires Inmediata Data Migration Team involvement. Admin users must enter a password. Contact via servicioalcliente@inmediata.com or techsupport@inmediata.com. Also supports SQL file export format.
- **Bulk capability**: Yes, but only with vendor assistance — a notable (b)(10) concern since the regulation requires export "without subsequent developer assistance to operate."
- **Configuration**: Users can configure which worksheets and fields to export via the Configure Export Fields popup. Fields can be hidden, renamed, and resequenced.
- **Access constraints**: Population-level export requires vendor team coordination; single-patient export is self-service.

## 4. Export Content: What's In It

The export comprises **47 worksheets** (42 standard, 5 billing-conditional) covering clinical and administrative data. However, **field-level documentation is almost entirely absent**.

### Field Documentation Status

| Metric | Count |
|---|---|
| Total worksheets | 47 |
| Worksheets with documented fields | 4 (8.5%) |
| Worksheets with NO field documentation | 43 (91.5%) |
| Total documented fields (across all worksheets) | 42 |
| Fields with descriptions | 39 (92.9% of documented) |
| Fields without descriptions | 3 (Insurance Master partial screenshot) |

Only **3 worksheets** have complete field lists in the documentation:
- **Allergy**: 12 fields (Last name, First name, Middle name, Chart no, Account no, Birth date, Allergy, Reaction, Type, Int Name, Status, Rxnorm)
- **Letters**: 16 fields (includes FILE column for document attachments)
- **CCD**: 11 fields (includes HTML and XML columns for CCD documents)

The **Insurance Master** worksheet shows 3 database column names (IM_ID, IM_NAME, IM_PAYER_ID) partially visible in a Configure Export Fields screenshot on page 10, but the full field list is not provided.

For the remaining **43 worksheets**, only the worksheet name is documented — there is no information about what fields they contain, what data types are used, how they relate to each other, or what values they accept.

### Vendor's Own Content Organization

Based on the worksheet names and functional grouping visible in the PDF:

| Entity/Worksheet | Fields | Documented | Types | Category |
|---|---|---|---|---|
| Insurance Master | 3 (partial) | Partially (screenshot) | No | Reference |
| Medics | Unknown | No | No | Reference |
| Referring Provider | Unknown | No | No | Reference |
| Adjusters | Unknown | No | No | Reference |
| Attorneys | Unknown | No | No | Reference |
| Employers | Unknown | No | No | Reference |
| Guarantor | Unknown | No | No | Demographics |
| Patient Demographics | Unknown | No | No | Demographics |
| Patient Insurance | Unknown | No | No | Insurance |
| Vaccination | Unknown | No | No | Clinical |
| Health Maintenance | Unknown | No | No | Clinical |
| Family History | Unknown | No | No | Clinical |
| Past Medical Hist | Unknown | No | No | Clinical |
| Surgery | Unknown | No | No | Clinical |
| **Allergy** | **12** | **Yes** | **No** | Clinical |
| Current Medication | Unknown | No | No | Clinical |
| Social History | Unknown | No | No | Clinical |
| Legal Documents | Unknown | No | No | Documents |
| Other Documents | Unknown | No | No | Documents |
| Enc Attach Docs | Unknown | No | No | Documents |
| Old Progress Notes | Unknown | No | No | Clinical |
| Messages | Unknown | No | No | Communication |
| Future Appointments | Unknown | No | No | Scheduling |
| Vitals | Unknown | No | No | Clinical |
| Diagnosis Codes | Unknown | No | No | Clinical |
| CPT Codes | Unknown | No | No | Coding |
| HCPC Codes | Unknown | No | No | Coding |
| **CCD** | **11** | **Yes** | **No** | Clinical |
| Prescriptions | Unknown | No | No | Clinical |
| Lab Results | Unknown | No | No | Clinical |
| Rad Results | Unknown | No | No | Clinical |
| Procedure Orders | Unknown | No | No | Clinical |
| Consults | Unknown | No | No | Clinical |
| Enc Progress Notes | Unknown | No | No | Clinical |
| Procedure Notes | Unknown | No | No | Clinical |
| **Letters** | **16** | **Yes** | **No** | Communication |
| All Vitals | Unknown | No | No | Clinical |
| Lab Test Result Values | Unknown | No | No | Clinical |
| Patient Cases | Unknown | No | No | Clinical |
| Patient Notes | Unknown | No | No | Clinical |
| Patient Alert | Unknown | No | No | Clinical |
| Past Appointments | Unknown | No | No | Scheduling |
| *Billing Ledger* | Unknown | No | No | Billing* |
| *Billing Claims* | Unknown | No | No | Billing* |
| *Billing Charges* | Unknown | No | No | Billing* |
| *Patient Advance* | Unknown | No | No | Billing* |
| *Statements* | Unknown | No | No | Billing* |

*\* Billing worksheets are conditional — only available "when Billing is turned on for the clinic."*

The complete entity inventory is available at [`analysis/full-entity-inventory.json`](analysis/full-entity-inventory.json).

### Export File Structure

From the PDF (pages 13–14), the exported ZIP contains:
- **Per-patient folders** (e.g., `APC02734/`, `CHART01/`) containing attached documents (PDFs)
- **XLS files**: one per worksheet, with patient identifier columns (Last name, First name, Middle name, Chart no, Account no, Birth date) as common prefixes
- **TXT files**: parallel text-format exports
- **PDF files**: document attachments referenced via a `FILE` column in the XLS
- Worksheets with document attachments (Lab Results, Rad Results, Letters, etc.) include a `FILE` column pointing to the physical file path within the ZIP

## 5. Coverage Assessment

### 5a. What the Vendor Covers (Bottom-Up)

The 47 worksheets span a reasonably broad set of clinical and administrative data categories:

| Category | Worksheets | Documented Fields |
|---|---|---|
| Demographics | 3 (Patient Demographics, Guarantor, Employers) | 0 |
| Insurance / Coverage | 2 (Insurance Master, Patient Insurance) | 3 (partial) |
| Provider / Reference | 4 (Medics, Referring Provider, Adjusters, Attorneys) | 0 |
| Clinical - History | 4 (Family History, Past Medical Hist, Surgery, Social History) | 0 |
| Clinical - Allergies | 1 (Allergy) | 12 |
| Clinical - Medications | 2 (Current Medication, Prescriptions) | 0 |
| Clinical - Immunizations | 2 (Vaccination, Health Maintenance) | 0 |
| Clinical - Vitals | 2 (Vitals, All Vitals) | 0 |
| Clinical - Labs | 2 (Lab Results, Lab Test Result Values) | 0 |
| Clinical - Imaging | 1 (Rad Results) | 0 |
| Clinical - Procedures | 2 (Procedure Orders, Procedure Notes) | 0 |
| Clinical - Notes | 4 (Old/Enc Progress Notes, Patient Notes, Patient Alert) | 0 |
| Clinical - Diagnoses | 1 (Diagnosis Codes) | 0 |
| Clinical - Codes | 2 (CPT Codes, HCPC Codes) | 0 |
| Clinical - Care Coordination | 3 (Consults, Letters, Messages) | 16 |
| Clinical - Documents | 4 (Legal Documents, Other Documents, Enc Attach Docs, CCD) | 11 |
| Scheduling | 2 (Future Appointments, Past Appointments) | 0 |
| Patient Management | 1 (Patient Cases) | 0 |
| Billing | 5 (Billing Ledger/Claims/Charges, Patient Advance, Statements) | 0 |

The worksheet names suggest broad domain coverage, but with only 42 total documented fields across 4 of 47 worksheets, **it is impossible to independently verify what data is actually exported**. The worksheet names are suggestive but not evidence.

### 5b. Standardized Domain Coverage (Top-Down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | `Patient Demographics` worksheet exists; no field list available | Worksheet present but field content unverifiable; product stores extensive demographics |
| Encounters / visits | ⚠️ Partial | No dedicated "Encounters" worksheet; encounter data may be embedded in `Enc Progress Notes`, `Enc Attach Docs` | Unclear whether encounter metadata (dates, providers, types) is captured vs. just encounter notes |
| Problems / conditions / diagnoses | ⚠️ Partial | `Diagnosis Codes` worksheet exists | Worksheet present but field content unverifiable |
| Medications / prescriptions | ⚠️ Partial | `Current Medication`, `Prescriptions` worksheets exist | Worksheet present but field content unverifiable |
| Allergies | ✅ Covered | `Allergy` worksheet with 12 documented fields including Allergy, Reaction, Type, Rxnorm | Best-documented worksheet; appears clinically complete |
| Immunizations | ⚠️ Partial | `Vaccination`, `Health Maintenance` worksheets exist | Worksheet present but field content unverifiable |
| Vitals | ⚠️ Partial | `Vitals`, `All Vitals` worksheets exist | Two worksheets suggests separate encounter vs. longitudinal views; field content unverifiable |
| Lab results | ⚠️ Partial | `Lab Results`, `Lab Test Result Values` worksheets exist; document attachments supported | Worksheet present but field content unverifiable |
| Imaging / diagnostic reports | ⚠️ Partial | `Rad Results` worksheet exists; document attachments supported | Worksheet present but field content unverifiable |
| Procedures | ⚠️ Partial | `Procedure Orders`, `Procedure Notes`, `Surgery` worksheets exist | Worksheet present but field content unverifiable |
| Clinical notes / documents | ⚠️ Partial | `Old Progress Notes`, `Enc Progress Notes`, `Patient Notes`, `Letters`, plus document attachment worksheets | Multiple worksheets suggest broad notes coverage; Letters has 16 documented fields |
| Care plans / goals | ❌ Not covered | No worksheet for care plans or goals | Product likely stores care plan data as an EHR; this is a gap |
| Orders / referrals | ⚠️ Partial | `Procedure Orders`, `Consults` worksheets exist | Worksheet present but field content unverifiable |
| Insurance / coverage | ⚠️ Partial | `Insurance Master`, `Patient Insurance` worksheets exist; Insurance Master shows database column names | Worksheets present; minimal field visibility |
| Claims / billing | ⚠️ Partial | `Billing Ledger`, `Billing Claims`, `Billing Charges`, `Patient Advance`, `Statements` — but **conditional on billing being enabled** | 5 billing worksheets exist but are not available to all clinics; field content completely undocumented |
| Payments | ⚠️ Partial | May be within `Billing Ledger` or `Patient Advance` | Unclear; no field documentation |
| Consents / directives | ⚠️ Partial | `Legal Documents` worksheet exists | May cover consents; field content unverifiable |
| Patient communications / portal messages | ⚠️ Partial | `Messages` worksheet exists | Worksheet present but field content unverifiable |
| Specialty-specific data | ❌ Not covered | No specialty-specific worksheets despite serving 300+ specialties | Product claims to support many specialties; no specialty-specific export content visible |

**Key coverage observations**:
- Nearly every domain gets a "⚠️ Partial" rating because worksheets with relevant names exist, but the absence of field-level documentation makes it impossible to confirm the depth or completeness of any domain's coverage.
- **Billing is conditional**: the 5 billing worksheets only appear "when Billing is turned on for the clinic," meaning some installations may export with no billing data at all.
- **No specialty-specific content**: despite the product supporting 300+ specialties, there are no worksheets for specialty-specific data (e.g., behavioral health assessments, dermatology charts, ophthalmology measurements).
- **No care plans**: no worksheet for care plans, goals, or treatment plans.

## 6. Documentation Quality

The export documentation consists of a single 16-page PDF that functions as a **user guide** rather than a **data dictionary**. It explains *how to use* the export feature but almost entirely omits *what is exported*.

**What's documented well:**
- Export workflow is clearly described with screenshots for both single-patient and population-level exports
- The worksheet list is complete (47 names)
- The Configure Export Fields UI demonstrates that field-level customization is available
- File structure within the ZIP is explained with examples
- Audit trail functionality is documented

**What's missing or inadequate:**
- **No data dictionary**: Only 3 of 47 worksheets have field lists (Allergy: 12 fields, Letters: 16 fields, CCD: 11 fields). The remaining 44 worksheets have zero field documentation.
- **No data types**: Even for the 3 documented worksheets, no data types are specified
- **No relationships/foreign keys**: No documentation of how worksheets relate to each other
- **No value sets or code systems**: No enumerated values, no reference to standard terminologies (except the Rxnorm field name in Allergy)
- **No sample data**: No example exports or sample records
- **No machine-readable schema**: No JSON schema, no XSD, no CSV headers file
- **No record counts or volume guidance**: No indication of typical export sizes

A developer attempting to build an import from this documentation alone would know the names of 47 worksheets but would have field-level information for only 3 of them (covering 39 fields). For the remaining 44 worksheets, they would have to reverse-engineer the structure from actual export files.

## 7. Overall Assessment

### Classification

**Partial native export**: The export appears to use the product's native data model (47 worksheet categories covering clinical, billing, and administrative data) rather than projecting into a standard like C-CDA or FHIR. This is structurally the right approach. However, the documentation is so thin — only 42 fields documented across 4 of 47 worksheets — that it's impossible to independently verify export completeness. The worksheets suggest broad coverage, but the documentation provides almost no evidence of depth.

### Key Findings

1. **Near-zero field-level documentation is the critical weakness.** Only 3 of 47 worksheets (Allergy, Letters, CCD) have complete field lists, totaling just 39 described fields. The remaining 44 worksheets are documented by name only. This makes the export essentially unverifiable from the documentation alone. (Source: PDF pages 13–14 vs. full worksheet list on page 11)

2. **The export is genuinely native, not a C-CDA/FHIR repackaging.** The 47 worksheet categories (e.g., Billing Ledger, Patient Cases, Insurance Master, Adjusters, Attorneys) clearly represent internal data structures, not a clinical summary projection. CCD is one of 47 worksheets, not the entire export. (Source: PDF page 11)

3. **Billing data is conditional.** The 5 billing worksheets (Billing Ledger, Billing Claims, Billing Charges, Patient Advance, Statements) only appear "when Billing is turned on for the clinic." Since SecureEMR+ is deeply integrated with SecureClaim for billing, this conditionality may exclude billing data from many exports. (Source: PDF page 11)

4. **Population-level export requires vendor assistance**, which may conflict with the (b)(10) requirement that export operate "without subsequent developer assistance." Single-patient export is fully self-service. (Source: PDF pages 3, 7)

5. **No specialty-specific content** despite the product serving 300+ specialties. The 47 worksheets cover general clinical and administrative domains but include nothing specialty-specific (e.g., no behavioral health assessments, no ophthalmology measurements, no dental charts). (Source: PDF page 11 vs. product-research.md)

### Summary Stats

```
Classification:  Partial native export
Export format:   XLS + TXT + PDF (in ZIP), with CCD as HTML+XML
Model type:      Native database (worksheet per entity)
Entities:        47 worksheets (42 standard + 5 billing-conditional)
Fields:          42 documented (across 4 worksheets); unknown for remaining 43
Descriptions:    39 of 42 documented fields (92.9%); 0% for 43 undocumented worksheets
Sample data:     No
Bulk export:     Yes (vendor-assisted only)
Domains covered: 1 confirmed, 15 of 17 partially evidenced (worksheet names only), 2 gaps
```

### Bottom Line

SecureEMR+ takes the right structural approach — exporting native data across 47 worksheet categories rather than repackaging C-CDA — but its documentation is critically deficient: only 42 fields across 4 worksheets are documented, leaving 91.5% of the export completely opaque. A patient or provider would receive a ZIP of spreadsheet files, but without a data dictionary, understanding or reusing the exported data requires reverse-engineering. The biggest gap is the near-total absence of field-level documentation; the biggest strength is the breadth of the worksheet categories, which suggest genuine "all EHI" intent even if verification is impossible from the available artifacts.
