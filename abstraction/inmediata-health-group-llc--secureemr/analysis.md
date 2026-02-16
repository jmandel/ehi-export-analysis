# EHI Export Analysis: Inmediata Health Group LLC

**Product**: SecureEMR+
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2769.Secu.04.02.1.260116

## 1. Product Context

SecureEMR+ is a cloud-based ambulatory EHR built on the PrognoCIS platform (by Bizmatics, Inc.), localized and bundled by Inmediata Health Group LLC for the Puerto Rico market. Inmediata is primarily a healthcare clearinghouse processing ~85% of all medical claims in Puerto Rico. The product combines PrognoCIS's clinical EMR with Inmediata's billing (SecureClaim) and clearinghouse (SecureTrack) tools.

The product serves outpatient/ambulatory practices across 300+ specialties and stores:
- **Clinical data**: demographics, problem lists, medications, allergies, immunizations, vitals, lab/radiology results, clinical notes (specialty-customizable), procedures, surgical history, family/social history, health maintenance, implantable devices, social/behavioral data
- **Billing/claims**: charges, claims, superbills, payments, denial tracking, eligibility, ERA/EOB — deeply integrated given Inmediata's clearinghouse role
- **e-Prescribing**: EPCS-capable, Surescripts integration
- **Documents**: scanned documents, faxes, uploaded files, legal documents
- **Patient portal**: secure messaging, lab results viewing, appointment management
- **Referrals/consults**: referral management and tracking
- **Appointments**: scheduling with reminders
- **Correspondence**: letters, messages

This baseline establishes that a complete (b)(10) export should cover clinical, billing, document, correspondence, and administrative data.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/ehi-export-prognocis-self-attestation.pdf` | 16-page "Electronic Health Information Data Export and User Guide" (Denali 3.1), authored Nov 2023 by Neha Parmar (PrognoCIS/Bizmatics). 1,182,354 bytes. Contains export workflow instructions, UI screenshots, worksheet list, and limited field examples. | **Primary and only artifact.** Provides worksheet-level inventory but minimal field-level detail. |

No other artifacts were collected or available. The vendor's mandatory disclosures page links to this same PDF for (b)(10) documentation. A separate FHIR API document exists for (g)(10) but is not the (b)(10) export.

## 3. Export Mechanics

- **Format**: ZIP file containing XLS spreadsheets (one per data category/worksheet), parallel TXT files, PDF files for attached documents (progress notes, letters, lab results), and HTML/XML files for CCD exports. An SQL export option is also available for admin/bulk exports.
- **Mechanism**:
  - **Single patient**: Self-service via UI. Users with `CuresEHIExport` role navigate to Data Export, select a patient, choose data categories via checkboxes, click EXPORT. Export generates in background; email notification on completion. Downloaded from Settings > Configuration > Clinic > Download Files under "Cures EHI Export" category.
  - **Bulk/population**: Requires Inmediata Data Migration Team involvement ("depends on size of data, time and efforts required to manage server resources"). Users contact servicioalcliente@inmediata.com or techsupport@inmediata.com. Admin users can filter by all patients, selected patients, primary/attending provider, last name range, or SQL file. Encounter date range can be specified.
- **Single-patient vs bulk**: Both supported, but bulk requires vendor assistance.
- **Access constraints**: Single-patient export requires `CuresEHIExport` user role. Bulk export requires admin access plus vendor coordination. No fees mentioned.
- **Configurable fields**: The "Configure Export Fields" feature allows users to select which fields to include/exclude per worksheet, set field titles, hide fields, and set sequence order.

## 4. Export Content: What's In It

The sole documentation artifact is a 16-page PDF that lists 47 exportable worksheets (42 base + 5 conditional billing) but provides field-level detail for only 4 of them.

### Data dictionary assessment

- **Entities/worksheets**: 47 total (42 always available, 5 billing worksheets conditional on billing being enabled)
- **Fields documented**: 52 fields across 4 worksheets (8.5% of worksheets have any field detail)
- **Fields with descriptions**: 13 (Insurance Master only, via Name column)
- **Fields with types**: 0
- **Fields with value sets**: 0
- **Relationships/foreign keys**: Not documented. Patient linkage appears to be via Last name, First name, Middle name, Chart no, and Account no fields (visible in the examples), but not formally specified.

The Configure Export Fields UI (visible in a screenshot on page 10) clearly shows per-worksheet field metadata (Field, Name, Title, Hide, Seqn columns), but this metadata is not published in the documentation beyond one example (Insurance Master).

### Vendor's own content organization

Field-level detail exists for only 4 of 47 worksheets. For the remaining 43, only the worksheet name is documented.

| Entity/Worksheet | Fields | Described | Types | Category |
|---|---|---|---|---|
| Insurance Master | 13 | 13 (Name col) | No | Administrative/Reference |
| Allergy | 12 | 0 | No | Clinical |
| Letters | 16 | 0 | No | Correspondence |
| CCD | 11 | 0 | No | Clinical |
| Medics | — | — | — | Administrative/Reference |
| Referring Provider | — | — | — | Administrative/Reference |
| Adjusters | — | — | — | Administrative/Reference |
| Attorneys | — | — | — | Administrative/Reference |
| Employers | — | — | — | Administrative/Reference |
| Guarantor | — | — | — | Administrative/Reference |
| Patient Demographics | — | — | — | Clinical |
| Patient Insurance | — | — | — | Clinical |
| Vaccination | — | — | — | Clinical |
| Health Maintenance | — | — | — | Clinical |
| Family History | — | — | — | Clinical |
| Past Medical Hist | — | — | — | Clinical |
| Surgery | — | — | — | Clinical |
| Current Medication | — | — | — | Clinical |
| Social History | — | — | — | Clinical |
| Legal Documents | — | — | — | Documents |
| Other Documents | — | — | — | Documents |
| Enc Attach Docs | — | — | — | Documents |
| Old Progress Notes | — | — | — | Clinical |
| Messages | — | — | — | Correspondence |
| Future Appointments | — | — | — | Administrative/Reference |
| Vitals | — | — | — | Clinical |
| Diagnosis Codes | — | — | — | Clinical |
| CPT Codes | — | — | — | Clinical |
| HCPC Codes | — | — | — | Clinical |
| Prescriptions | — | — | — | Clinical |
| Lab Results | — | — | — | Clinical |
| Rad Results | — | — | — | Clinical |
| Procedure Orders | — | — | — | Clinical |
| Consults | — | — | — | Clinical |
| Enc Progress Notes | — | — | — | Clinical |
| Procedure Notes | — | — | — | Clinical |
| All Vitals | — | — | — | Clinical |
| Lab Test Result Values | — | — | — | Clinical |
| Patient Cases | — | — | — | Clinical |
| Patient Notes | — | — | — | Clinical |
| Patient Alert | — | — | — | Clinical |
| Past Appointments | — | — | — | Administrative/Reference |
| Billing Ledger | — | — | — | Billing (conditional) |
| Billing Claims | — | — | — | Billing (conditional) |
| Billing Charges | — | — | — | Billing (conditional) |
| Patient Advance | — | — | — | Billing (conditional) |
| Statements | — | — | — | Billing (conditional) |

("—" = no field-level documentation provided)

Category breakdown:

| Category | Worksheets | With field detail | Known fields |
|---|---|---|---|
| Clinical | 28 | 2 | 23 |
| Administrative/Reference | 9 | 1 | 13 |
| Billing (conditional) | 5 | 0 | 0 |
| Documents | 3 | 0 | 0 |
| Correspondence | 2 | 1 | 16 |
| **Total** | **47** | **4** | **52** |

The full inventory is saved to `analysis/entity-inventory-full.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor organizes their export into 47 worksheets spanning clinical, administrative, document, correspondence, and billing domains. The breadth is notable — this is not a repackaged C-CDA or FHIR export. The worksheet names map to specific EHR data domains:

**Strongest areas (by worksheet count):**
- **Clinical data** (28 worksheets): Demographics, insurance, vitals (two worksheets: Vitals and All Vitals), medications, allergies, immunizations, lab results (with separate Lab Test Result Values), radiology results, diagnoses, procedures (CPT/HCPC codes, Procedure Orders), clinical notes (Enc Progress Notes, Procedure Notes, Old Progress Notes), family/social/surgical history, health maintenance, consults, patient cases/notes/alerts, CCD
- **Administrative/Reference** (9 worksheets): Insurance Master, Medics, Referring Provider, Adjusters, Attorneys, Employers, Guarantor, Future/Past Appointments

**Conditional area:**
- **Billing** (5 worksheets): Billing Ledger, Billing Claims, Billing Charges, Patient Advance, Statements — only available when billing is enabled. Given Inmediata's clearinghouse integration, billing is likely enabled for most customers.

**Thinnest areas:**
- **Documents** (3 worksheets): Legal Documents, Other Documents, Enc Attach Docs — worksheet names listed but no field detail
- **Correspondence** (2 worksheets): Letters (16 fields documented), Messages (no detail)

**Key limitation**: While the worksheet list is broad, the almost complete absence of field-level documentation means we cannot assess the *depth* of any domain. We know there's a "Patient Demographics" worksheet but not whether it has 10 fields or 100.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient Demographics` worksheet | Worksheet exists; field depth unknown |
| Encounters / visits | ⚠️ Partial | No dedicated "Encounters" worksheet; encounter data implied via `Enc Progress Notes`, `Enc Attach Docs`, encounter date range filter | No standalone encounter table; encounter context likely embedded in notes |
| Problems / conditions / diagnoses | ✅ Covered | `Diagnosis Codes` worksheet | Worksheet exists; field depth unknown |
| Medications / prescriptions | ✅ Covered | `Current Medication`, `Prescriptions` worksheets | Two separate worksheets suggest current meds vs prescription history |
| Allergies | ✅ Covered | `Allergy` worksheet (12 fields documented: includes Allergy, Reaction, Type, Int Name, Status, Rxnorm) | One of the better-documented worksheets |
| Immunizations | ✅ Covered | `Vaccination` worksheet | Worksheet exists; field depth unknown |
| Vitals | ✅ Covered | `Vitals`, `All Vitals` worksheets | Two worksheets — likely current vs historical vitals |
| Lab results | ✅ Covered | `Lab Results`, `Lab Test Result Values` worksheets | Two worksheets — results and discrete values |
| Imaging / diagnostic reports | ✅ Covered | `Rad Results` worksheet | Worksheet exists; field depth unknown |
| Procedures | ✅ Covered | `CPT Codes`, `HCPC Codes`, `Procedure Orders`, `Surgery` worksheets | Multiple procedure-related worksheets |
| Clinical notes / documents | ✅ Covered | `Enc Progress Notes`, `Procedure Notes`, `Old Progress Notes` worksheets; documents exported as PDF files | Notes exported as both structured data (XLS) and documents (PDF) |
| Care plans / goals | ❌ Not covered | No care plan or goals worksheet | Product likely stores care plan data (certified for (a)(12) Care Plan); gap |
| Orders / referrals | ✅ Covered | `Procedure Orders`, `Consults` worksheets | Consults likely covers referrals |
| Insurance / coverage | ✅ Covered | `Patient Insurance`, `Insurance Master` (13 fields documented) worksheets | Insurance Master is the only worksheet with name-level field descriptions |
| Claims / billing | ⚠️ Partial | `Billing Ledger`, `Billing Claims`, `Billing Charges`, `Patient Advance`, `Statements` — **conditional on billing being enabled** | 5 billing worksheets exist but are conditional; when billing is enabled, this appears solid. No field detail documented for any billing worksheet. |
| Payments | ⚠️ Partial | `Patient Advance`, `Billing Ledger` (may contain payment data) | Likely covered within billing worksheets, but unclear without field detail |
| Consents / directives | ⚠️ Partial | `Legal Documents` worksheet may include consents | Unclear whether this covers advance directives; no field detail |
| Patient communications / portal messages | ⚠️ Partial | `Messages`, `Letters` worksheets | Messages worksheet exists but unclear if it includes portal messages specifically |
| Specialty-specific data | ❌ Not covered | No specialty-specific worksheets visible | Product supports 300+ specialties with customizable templates; specialty-specific data (custom forms, specialty assessments) not represented as dedicated worksheets |

**Summary**: 12 of 19 domains show dedicated worksheets (✅), 5 show partial evidence (⚠️), and 2 show no coverage (❌). The gaps in care plans and specialty-specific data are notable given the product's certified criteria and multi-specialty market.

## 6. Documentation Quality

**Overall quality: Poor.** The documentation is a 16-page user guide that effectively tells users *how to click buttons* to export data, but does not tell developers *what the exported data contains*.

- **What's documented well**: The export workflow is clearly explained with UI screenshots, role requirements, and step-by-step instructions. The list of 47 worksheet names provides a good high-level inventory of data categories.
- **What's missing**: Field-level documentation for 43 of 47 worksheets. No data types for any field. No value sets or code system definitions. No relationship/foreign key documentation. No sample data files.
- **Machine-readable artifacts**: None. The sole artifact is a PDF with embedded screenshots.
- **Developer usability**: A developer could initiate an export but could not build a reliable import. The field names visible in the one screenshot (e.g., `IM_PAYER_ID`, `IM_ADDRESS_WORKTEL1`) are database column names that require insider knowledge to interpret. The Configure Export Fields UI clearly contains the field metadata needed for a proper data dictionary, but this metadata is not published.
- **Maintenance**: Document dated November 2023 (version Denali 3.1). Current certified version is 4.0 (certified January 2026). The documentation may be stale.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The 47-worksheet inventory is genuinely broad for an ambulatory EHR — far broader than USCDI. It covers clinical data, billing (conditional), documents, correspondence, administrative reference data, and appointments. However, the classification is "Partial" rather than "Comprehensive" because:
1. Billing worksheets are conditional on billing being enabled, creating uncertainty about whether all deployments export billing data
2. No dedicated care plan or goals worksheets despite being certified for care planning
3. No specialty-specific data worksheets despite serving 300+ specialties
4. The near-total absence of field-level documentation means we cannot verify the *depth* of coverage within any domain — a worksheet called "Patient Demographics" could contain 5 fields or 50

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly a purpose-built export, not a repackaged clinical exchange:
- The export produces XLS/TXT tabular data from the product's native data model, not C-CDA or FHIR
- It covers 47 data categories including billing, legal documents, adjusters, attorneys, employers, and guarantors — data that would never appear in a (g)(10) FHIR API or C-CDA
- The `CuresEHIExport` role, "Cures EHI Export" download category, and configurable field selection are purpose-built UI elements
- The CCD worksheet is just one of 47 — it's included alongside the native export, not the entire export
- The SQL export option for bulk exports further indicates this is a native data dump capability

### Key Findings

1. **Purpose-built but poorly documented**: The export itself appears to be a genuine, broad (b)(10) implementation covering 47 data categories from the product's native database — well beyond USCDI. However, the documentation provides field-level detail for only 4 of 47 worksheets (52 fields total), making the export a near-undocumented data dump.

2. **Billing export is conditional**: The 5 billing worksheets (Billing Ledger, Claims, Charges, Patient Advance, Statements) only appear "when Billing is turned on for the clinic." Given Inmediata's core business as a clearinghouse, billing is likely enabled for most customers, but this creates a documentation gap.

3. **Configurable but unpublished field metadata**: The Configure Export Fields UI (visible on page 10) clearly shows per-worksheet field definitions (Field, Name, Title columns), meaning the product stores the data dictionary metadata needed for proper documentation. The vendor chose not to publish it.

4. **Bulk export requires vendor involvement**: Population-level exports require contacting Inmediata's Data Migration Team, which may conflict with the (b)(10) requirement for export "without subsequent developer assistance." Single-patient export is fully self-service.

5. **Documentation is stale**: The PDF references version "Denali 3.1" but the current certified version is 4.0 (certified January 2026). The document was created November 2023.

### Summary Stats

    Coverage:        Partial
    Approach:        Purpose-built EHI export
    Export format:   XLS, TXT, PDF, HTML/XML (CCD), SQL (bulk option) — in ZIP
    Entities:        47 worksheets (42 base + 5 conditional billing)
    Fields:          52 documented (across 4 of 47 worksheets)
    Descriptions:    25% of documented fields (13 of 52; only Insurance Master)
    Sample data:     No
    Bulk export:     Yes (requires vendor assistance)
    Domains covered: 12 of 19 applicable domains fully; 5 partial; 2 not covered

### Bottom Line

SecureEMR+ has built a genuine, purpose-specific EHI export covering 47 data categories from its native database — significantly broader than a repackaged clinical summary. However, the documentation is among the thinnest possible: 47 worksheet names with field-level detail for only 4 of them, no data types, no value sets, no relationships, and no sample data. A patient would receive their data in a computable format, but a developer receiving the export would face substantial reverse-engineering to interpret it. The single biggest gap is the unpublished data dictionary — the product clearly stores the field metadata (visible in UI screenshots) but the vendor did not document it.
