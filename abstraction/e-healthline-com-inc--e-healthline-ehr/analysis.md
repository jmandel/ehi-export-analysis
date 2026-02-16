# EHI Export Analysis: E*HealthLine.com, Inc.

**Product**: CARE© Integrated Hospital Information Management System  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 10833 (15.02.05.1384.EHLC.01.01.0.220217)

## 1. Product Context

CARE© is a full-scope hospital information system (HIS) developed by E*HealthLine.com, Inc., a very small company (~7 employees, ~$5.3M revenue) based in Sacramento, CA. The product targets hospital settings with integrated modules spanning:

- **Core clinical**: ADT, bed management, electronic medical records (CARE Chart), clinical data repository (CARE Clinical Foundation), CPOE with medication ordering and allergy/drug-interaction alerts
- **Departmental**: eLab (full clinical laboratory information system with specimen lifecycle management), eRad (radiology information system with order tracking, transcription, PACS integration), pharmacy
- **Financial/billing**: eBilling (claims, charges, payments, EDI, revenue cycle), SPHINX (financial management — details unknown, product page 404)
- **Other**: Scheduling, material management, inventory control, patient portal, telehealth capabilities

The product holds an unusually broad certification profile (40+ ONC criteria) for a company of its size. Given this is a hospital information system with dedicated billing, lab, radiology, and CPOE modules, a (b)(10) export should cover clinical documentation, lab/radiology detail beyond C-CDA summaries, billing records, order history, and administrative data like demographics and encounters.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/Electronic_Health_Information_Export.pdf` | 10-page PDF (v2.0, Oct 24 2023; file modified Jul 18 2024). User guide for the EHI export function. Describes export mechanism, ZIP file structure (7 components), access controls, and FHR exclusion mechanism. **No data dictionary, no field-level schema, no sample data.** | Primary and only artifact; moderately informative for understanding export mechanics but provides no technical detail about export content |

**Total artifacts: 1 PDF (265 KB, 10 pages)**. This is the entirety of the (b)(10) documentation. No supplementary data dictionaries, schemas, sample files, or technical reference materials were found.

## 3. Export Mechanics

- **Format**: ZIP file (`CDAXMLExport_8.Zip`) containing C-CDA XML + CSV files + CDA XML document folders
- **Mechanism**: Desktop/server UI — "Export Batch CCDA" function accessible from Data Maintenance Menu. Not an API. Output written to a UNC network path (`\\SERVERNAME\BarcodeScans\HL7ExportFiles\CDAexports`)
- **Single-patient**: Yes — select patient by name or MR#, choose provider and clinic
- **Bulk/population**: Yes — select multiple patients by name or MR# range
- **Access constraints**: Requires admin-granted privileges (`[Edit General Database Setup]` + `[Print Documents]` or `[Chart Reviewer]`)
- **Fees**: Not mentioned

## 4. Export Content: What's In It

The PDF describes the export ZIP as containing 7 core components plus 2 optional additions. **There is no data dictionary** — the documentation provides only prose-level descriptions of each file component with no field names, no column headers, no types, no schemas, and no sample data.

### Vendor's own content organization

The export components as described in the PDF (pages 5–6):

| Entity/Component | Format | Fields Documented | Types | Category |
|---|---|---|---|---|
| CCDA | XML (HL7 C-CDA) | 0 (defers to HL7 spec) | N/A | Clinical Summary |
| BillingReport | CSV | 6 (from prose only) | None | Billing |
| demographics | CSV | 4 (from prose only) | None | Demographics |
| Schedule | CSV | 7 (from prose only) | None | Encounters |
| Documents | CDA XML folder | 0 | N/A | Clinical Documents |
| Notes | CDA XML folder | 0 | N/A | Clinical Documents |
| PatientDocumentFiles | CSV mapping | 0 | N/A | Clinical Documents |
| Custom Patient Data Tables | Embedded in CDA | 0 (variable) | N/A | Custom Data |
| Chart Documents | Mixed (TIF, etc.) | 0 | N/A | Clinical Documents |

**Total**: 9 entities/components, 17 fields mentioned in prose (no actual field names, types, or schemas provided).

The "fields" for BillingReport, demographics, and Schedule are inferred entirely from sentences like "The information includes the patient information, transaction dates, charges, claims and the description of transactions made with status" — these are not column headers or a schema.

### Key observations on content

1. **The CCDA component is explicitly USCDI v1**: The PDF states "The system allows exports of HL7 CCDA which complies with United States Core Data for Interoperability (USCDI), Version 1 requirements. The specifications for the CCDA can be obtained from the HL7 website." This is the vendor's existing C-CDA export, not a purpose-built data extraction.

2. **Three supplementary CSV files add some non-USCDI content**: BillingReport (billing transactions), demographics (patient info beyond what C-CDA captures), and Schedule (encounter/appointment history) go beyond a pure C-CDA export.

3. **Document folders include notes and attachments**: The Notes and Documents folders with CDA XML files, plus optional Chart Documents, capture clinical documentation.

4. **Custom Patient Data Tables are included by default**: This is notable — the vendor includes user-created data tables in the CDA export unless explicitly excluded. This could capture specialty or facility-specific data, though the content is entirely opaque.

5. **No detail on what BillingReport actually contains**: The billing CSV is described in one sentence. For a product with a dedicated eBilling module (claims, charges, payments, EDI, revenue cycle), one CSV with ~6 vague prose-described fields is almost certainly a thin representation.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export has three layers:

1. **C-CDA (USCDI v1)**: Standard clinical summary — problems, medications, allergies, labs, vitals, procedures, immunizations, care plans, etc. This is the vendor's existing clinical exchange export repackaged as the core of the (b)(10) export.

2. **Supplementary CSV files**: Three CSV files add demographics, billing transactions, and scheduling data beyond what C-CDA captures. These are the vendor's attempt to go beyond the clinical summary, but the total documented content is ~17 prose-described pseudo-fields across 3 files.

3. **Document collections**: CDA XML folders for notes and documents, plus optional chart documents (scanned images/TIFs), capture clinical documentation.

The strongest element is the inclusion of billing data and scheduling data as separate CSVs — this shows awareness that (b)(10) requires more than clinical summaries. However, the depth of these files is unknowable from the documentation.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | `demographics` CSV (4 prose-described categories: key info, identification, contact, insurance) | CSV exists but no field-level detail; product stores extensive ADT data |
| Encounters / visits | ⚠️ Partial | `Schedule` CSV (7 prose-described fields: date, provider, location, type, workflow, notes, note date) | CSV captures appointment-level data; detailed ADT events (transfers, bed assignments) likely not represented |
| Problems / conditions | ⚠️ Partial | C-CDA (USCDI v1 standard) | Only what C-CDA captures; EHR likely stores richer problem list data |
| Medications / prescriptions | ⚠️ Partial | C-CDA (USCDI v1 standard) | CPOE module stores detailed order data, interaction checks, administration records; C-CDA captures medication lists only |
| Allergies | ⚠️ Partial | C-CDA (USCDI v1 standard) | Standard C-CDA allergy section; CPOE has detailed drug interaction/allergy alert data |
| Immunizations | ⚠️ Partial | C-CDA (USCDI v1 standard) | Standard representation only |
| Vitals | ⚠️ Partial | C-CDA (USCDI v1 standard) | Standard representation only |
| Lab results | ⚠️ Partial | C-CDA (USCDI v1 standard) | eLab module stores full specimen lifecycle (collection, routing, preparation, testing, QA, auto-verification, reflex rules); C-CDA captures results summary only — significant gap |
| Imaging / diagnostic reports | ⚠️ Partial | C-CDA (USCDI v1 standard) | eRad stores orders, exam tracking, film tracking, transcription, reports, PACS image references; C-CDA captures minimal imaging data — significant gap |
| Procedures | ⚠️ Partial | C-CDA (USCDI v1 standard) | Standard representation only |
| Clinical notes / documents | ✅ Covered | `Notes` folder (CDA XML), `Documents` folder (CDA XML), optional `Chart Documents` (TIF/other), `PatientDocumentFiles` mapping CSV | Most thoroughly covered domain; dedicated folders for notes and documents with optional chart document inclusion |
| Care plans / goals | ⚠️ Partial | C-CDA (USCDI v1 standard) | Standard representation only |
| Orders / referrals | ❌ Not covered | No dedicated export component | CPOE is a major module; orders, order sets, and referral details are not represented beyond what's in C-CDA medication/procedure lists |
| Insurance / coverage | ⚠️ Partial | `demographics` CSV mentions "insurance information" | Mentioned in demographics CSV description but no detail on depth |
| Claims / billing | ⚠️ Partial | `BillingReport` CSV (6 prose-described fields: patient info, dates, charges, claims, descriptions, status) | eBilling module handles full revenue cycle (claims editing, EDI, AR, denials); one CSV file with ~6 vague fields is almost certainly a thin representation |
| Payments | ⚠️ Partial | Possibly within `BillingReport` CSV ("financial transactions") | May be included but not specifically documented |
| Consents / directives | ❌ Not covered | No evidence in export | Unknown whether product stores consent data |
| Patient communications | ❌ Not covered | No evidence in export | Product has patient portal; portal messages not mentioned in export |
| Specialty-specific data | ⚠️ Partial | Custom Patient Data Tables included in CDA by default | Opaque — content depends on facility configuration; could cover specialty data or could be minimal |

## 6. Documentation Quality

The documentation is **poor by any standard for a (b)(10) export**:

- **No data dictionary**: Zero field-level documentation. The CSV files are described only in one-sentence prose. A developer receiving this export would have to reverse-engineer every CSV file's columns.
- **No schema or sample data**: No CSV headers, no XML schemas beyond the generic C-CDA spec, no sample export files.
- **No relationships documented**: No description of how entities relate to each other (e.g., how PatientDocumentFiles maps to the Documents folder).
- **CCDA defers entirely to HL7**: The vendor provides zero product-specific documentation about what their C-CDA contains — just a pointer to the generic HL7 specification.
- **10 pages total**: Of which ~4 pages are boilerplate (title page, table of contents, revision history, regulatory attestation text), ~3 pages are step-by-step UI instructions for running the export, and ~3 pages describe the file structure.

A developer could not build an import from this documentation alone. They would need sample data and would have to inspect actual CSV files to understand the columns.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The export goes beyond pure C-CDA by adding three supplementary CSV files (billing, demographics, scheduling) and document folders. This shows the vendor made *some* effort to address (b)(10) beyond their existing clinical exchange. However, the depth is clearly insufficient for a product of this scope:

- A full hospital information system with dedicated eLab, eRad/PACS, CPOE, and eBilling modules should export far more than a C-CDA + 3 CSV files
- Lab data is reduced to C-CDA result summaries (eLab stores full specimen lifecycle data)
- Radiology data is reduced to C-CDA procedure entries (eRad stores orders, exam tracking, film tracking, transcription, PACS references)
- CPOE order data is not separately exported
- Billing data is compressed to one CSV with ~6 vaguely described fields (eBilling handles full revenue cycle management)
- The Custom Patient Data Tables mechanism is the most interesting feature — it could capture additional depth, but it's entirely opaque

**Axis 2 — Export approach: Repackaged existing export with minor additions**

The core of the export is the vendor's existing C-CDA "Export Batch CCDA" function — the documentation explicitly says this function was "updated to comply with 170.315(b)(10)" and the C-CDA complies with "USCDI, Version 1 requirements." The PDF header itself reads "170.315(g)(10)" in the footer (likely a copy-paste from their API documentation), reinforcing that this originated from their clinical exchange capabilities. The three supplementary CSV files and the document folders were additions to make it nominally cover (b)(10), but the overall approach is a C-CDA export with bolt-ons rather than a purpose-built EHI extraction.

### Key Findings

1. **C-CDA core with thin CSV supplements**: The export is fundamentally the vendor's existing C-CDA export with 3 CSV files (billing, demographics, scheduling) and document folders added. The C-CDA covers USCDI v1 clinical data; the CSVs add minimal non-USCDI content. (Source: PDF pages 5-6)

2. **No data dictionary at all**: The entire documentation is a 10-page user guide with zero field-level specifications. CSV files are described in single sentences. The CCDA component defers entirely to the generic HL7 specification. This makes the export nearly impossible to independently evaluate or consume. (Source: PDF, full document)

3. **Major modules unrepresented**: The product's eLab (full lab lifecycle), eRad (radiology workflow + PACS), and CPOE (detailed order entry) modules generate patient data far richer than what a C-CDA summary captures, yet no dedicated export components exist for this data. (Source: product-research.md module descriptions vs. PDF export structure)

4. **Custom Patient Data Tables are a notable feature**: The automatic inclusion of user-created Patient Data Tables in the CDA export (with an opt-out mechanism) is a thoughtful feature that could capture facility-specific and specialty data. However, its content is entirely opaque in the documentation. (Source: PDF page 7-8)

5. **Billing representation is almost certainly thin**: A dedicated eBilling module handling claims editing, EDI, AR management, and denial prevention is reduced to one CSV file described as containing "patient information, transaction dates, charges, claims and the description of transactions made with status." This is likely a basic transaction ledger, not a comprehensive billing export. (Source: PDF page 5 vs. product-research.md eBilling description)

### Summary Stats

```
Coverage:        Partial
Approach:        Repackaged existing export
Export format:   C-CDA XML + CSV + CDA XML documents (ZIP)
Entities:        9 (7 core + 2 optional)
Fields:          17 (prose-described only; no actual field-level schema)
Descriptions:    N/A (no data dictionary exists)
Sample data:     No
Bulk export:     Yes (population-level via MR# range)
Domains covered: ~8 of 18 applicable domains (most partial)
```

### Bottom Line

The CARE© EHI export is a C-CDA clinical exchange export with three supplementary CSV files bolted on to address (b)(10). For a full hospital information system with dedicated lab, radiology, CPOE, and billing modules, the export is clearly incomplete — it reduces rich departmental data to standard clinical summaries and provides no data dictionary whatsoever. A patient receiving this export would get a clinical summary plus a basic billing ledger, but not the detailed lab workflows, radiology records, order histories, or comprehensive billing data that the system stores about them.
