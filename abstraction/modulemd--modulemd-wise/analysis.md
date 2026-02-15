# EHI Export Analysis: ModuleMD

**Product**: ModuleMD WISE™  
**Analysis date**: 2025-07-17  
**CHPL ID**: 15.04.04.2980.Modu.10.01.1.221219 (internal ID 11092)

## 1. Product Context

ModuleMD WISE™ is a cloud-based, specialty-focused EHR designed primarily for allergy and immunology practices, serving over 300 practice locations with 10+ million patient records. It combines clinical EHR capabilities with practice management and revenue cycle management (RCM) in a single platform.

**Key data domains the product stores:**

- **Clinical (general)**: Demographics, encounters, diagnoses, medications, allergies, immunizations, vitals, lab results, clinical notes, care plans, referrals
- **Allergy/immunology specialty**: Skin testing (prick and intradermal), immunotherapy (vial mixing, injection tracking, dosing schedules), USP 797 compliance tracking, environmental/food allergen panels
- **Pulmonology**: Spirometry testing, PFT results, ATS/ERS compliance data
- **Infusion center**: Infusion management (biologic infusions, chemotherapy), chair scheduling, medication tracking, adverse reaction monitoring
- **Practice management**: Scheduling, patient registration, insurance verification
- **Billing/RCM**: Claims submission, charge capture, payment posting, denial management, accounts receivable, ERA/EOB processing
- **Patient portal**: Secure messaging, document access, appointment requests

The product's navigation tabs (visible in the export PDF screenshots) confirm modules for: General, Billing, Schedule, EMR, Allergy, Meaningful Use, Menu Privileges, and Data Export.

This is a deep specialty EHR with data far beyond what standard clinical summaries can represent. Allergy skin test panels, immunotherapy mixing protocols, spirometry waveforms, and infusion management records are all examples of specialty data that have no C-CDA or FHIR equivalent.

*(Source: `product-research.md`; navigation tabs confirmed on page 6 of the PDF)*

## 2. Artifacts Reviewed

| # | Artifact | Description | Informativeness |
|---|----------|-------------|-----------------|
| 1 | `B10-Data-Export-Process-Flow-Document_compressed.pdf` (448 KB, 9 pages) | The **sole** EHI export documentation artifact. A process flow guide showing UI screenshots of how to request and download an export. No data dictionary, schema, or sample data. | **Primary source** — but extremely thin. Mostly screenshots of the export request workflow. |

**Additional verification performed:**
- Checked the ONC mandatory disclosures page at `https://modulemd.com/onc-certified/` — contains only certification details and fee disclosures. No additional EHI export documentation, data dictionary, or technical specification is linked.
- Confirmed PDF metadata: Author Rajesh Dandu, created 2023-11-20 in Microsoft Word 2016, compressed via iLovePDF, 9 letter-size pages.

No other artifacts exist. There is no data dictionary, no schema file, no sample data export, no API documentation, and no supplementary technical specification. The entire (b)(10) export documentation package is a single 9-page process flow document.

*(Source: `files.json`, PDF metadata via `pdfinfo`)*

## 3. Export Mechanics

The export is initiated through a UI workflow:

- **Access path**: Administration → Practice Setup → Data Export → +New Export
- **Patient selection**: Single patient (by name or account number), multiple patients, or all patients via "Select All Patients" checkbox
- **Configuration options**: Archive Name, File Type (dropdown — **values not enumerated in documentation**), Encryption Key (optional password protection), Comments
- **Processing**: A backend batch program runs daily. Exports go through a 3-step pipeline:
  1. **New** — request submitted
  2. **InProgress** — data generated into folders
  3. **Completed** — data copied from physical server to cloud, download URL generated
- **Delivery**: Download via time-limited URL with expiry date. Download is available **only to the requestor** (other users cannot see the download icon).
- **Patient portal**: Individual patients can also download their C-CDA files from the Patient Portal under Documents.

**Format**: The document confirms C-CDA XML output. Downloaded files are organized as ZIP archives (e.g., `QAT_1.zip`, `QAT_2.zip`, `QAT_3.zip`) containing patient folders with files named like `QAT-1-11142023_ClinicalSummary` — indicating C-CDA Clinical Summary documents.

**Ambiguity about CSV**: Page 1 of the PDF states: *"The documentation for the export format consists of information on the structure and syntax for how the EHI will be exported by the product such as, for example, Consolidated-Clinical Document Architecture (C-CDA) document(s) or data dictionary for comma separated values (csv) file(s)."* This mentions CSV as a possible format, and a "File Type" dropdown is shown on page 4, but its values are never enumerated. The screenshots exclusively show C-CDA XML output. Whether CSV export actually exists or is a planned/template feature is unknown from the documentation.

**Bulk capability**: Yes — "Select All Patients" checkbox enables bulk export of the entire patient population.

**Fees**: The ONC mandatory disclosures page lists license, implementation, and subscription fees but does not mention any specific fee for (b)(10) export.

*(Source: PDF pages 1–8, `https://modulemd.com/onc-certified/`)*

## 4. Export Content: What's In It

### What can be determined

Based on the sole artifact, the confirmed export content is:

- **C-CDA Clinical Summary XML documents**, one per patient, packaged in ZIP archives
- File naming convention: `{PatientID}-{Date}_ClinicalSummary` (e.g., `QAT-1-11142023_ClinicalSummary`, `DevAsthma7-6-11172023_ClinicalSummary`)

A standard C-CDA Clinical Summary (CCD) typically includes:
- Patient demographics
- Problems/conditions
- Medications
- Allergies
- Immunizations
- Vital signs
- Lab results
- Procedures
- Encounters (summary)
- Care plan (if populated)

### What cannot be determined

The documentation provides **zero field-level detail**:

- **No data dictionary** — there is no listing of tables, fields, or data elements
- **No schema** — no XML schema, JSON schema, or data model documentation
- **No sample data** — no example C-CDA files or CSV files are provided
- **No field descriptions** — no explanation of what data elements are included or excluded
- **No relationship documentation** — no foreign keys, no entity-relationship diagrams
- **No value sets** — no code systems, terminology bindings, or enumerated values
- **No mapping to product modules** — no explanation of how the product's clinical, billing, allergy, or specialty data maps to export content

### Vendor's own content organization

The vendor does not organize or categorize the export content in any way. The documentation is purely a process flow for requesting exports. The only content-related information is:

| Evidence Item | Source | What it tells us |
|---|---|---|
| "C-CDA in XML files" | PDF page 7 | Export format is C-CDA XML |
| `_ClinicalSummary` filename suffix | PDF pages 7–8 | Document type is Clinical Summary (CCD) |
| ZIP folder per patient | PDF page 7 | One archive per patient |
| CSV mentioned in intro text | PDF page 1 | CSV may exist but is completely undocumented |
| "File Type" dropdown | PDF page 4 | Suggests multiple format options, but values not shown |

**Entity/table/field counts**: N/A — no data dictionary exists.

*(Source: `analysis/pdf_analysis_output.json`)*

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor provides no categorization of export content. The only confirmed output is C-CDA Clinical Summary XML documents. C-CDA Clinical Summaries are a standardized clinical document format that represents a defined subset of patient data — primarily the "core clinical data" overlap with USCDI.

A C-CDA CCD does **not** include:

- Billing records, claims, charges, payments
- Insurance/coverage details beyond basic payer name
- Specialty-specific clinical data (allergy skin test results, immunotherapy protocols, spirometry waveforms, infusion management records)
- Custom assessment forms
- Detailed encounter notes (full progress notes, H&P, consult notes — may be partially represented as free text sections)
- Imaging reports (may be partially represented)
- Patient portal communications/messages
- Detailed referral records

Given that ModuleMD WISE™ is a specialty allergy/immunology EHR with integrated billing/RCM, the C-CDA export represents a small fraction of the data the product stores about patients.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA patient header (name, DOB, address, contact) | C-CDA provides basic demographics but lacks the full detail the product stores (e.g., employer info, emergency contacts, custom fields) |
| Encounters / visits | ⚠️ Partial | C-CDA Encounters section | Summary-level only; visit details, appointment history likely incomplete |
| Problems / conditions / diagnoses | ⚠️ Partial | C-CDA Problems section | Active problem list likely included; historical diagnoses may be incomplete |
| Medications / prescriptions | ⚠️ Partial | C-CDA Medications section | Active medications likely included; prescription history, e-prescribing details may be thin |
| Allergies | ⚠️ Partial | C-CDA Allergies section | Basic allergy list included but **not** the specialty allergy testing data (skin test panels, intradermal results, environmental/food allergen panels) that is core to this product |
| Immunizations | ⚠️ Partial | C-CDA Immunizations section | Standard immunizations likely included but **not** immunotherapy protocols (vial mixing, injection tracking, dosing schedules) |
| Vitals | ⚠️ Partial | C-CDA Vital Signs section | Basic vitals likely included |
| Lab results | ⚠️ Partial | C-CDA Results section | Standard labs likely included; spirometry/PFT results may not map to C-CDA |
| Imaging / diagnostic reports | ⚠️ Partial | Possibly in C-CDA Results section | Unclear; no evidence of imaging data in export |
| Procedures | ⚠️ Partial | C-CDA Procedures section | Basic procedure list; infusion management details unlikely in C-CDA |
| Clinical notes / documents | ⚠️ Partial | Possibly in C-CDA Notes section | C-CDA may include note text but format/completeness unknown |
| Care plans / goals | ⚠️ Partial | C-CDA Care Plan section (if populated) | Unknown depth |
| Orders / referrals | ⚠️ Partial | Possibly in C-CDA sections | Unknown |
| Insurance / coverage | ❌ Not covered | No evidence of insurance data in C-CDA Clinical Summary | Product stores insurance/coverage data; **gap** |
| Claims / billing | ❌ Not covered | No billing entities in export | Product has full RCM/billing module; **significant gap** |
| Payments | ❌ Not covered | No payment data in export | Product processes payments; **significant gap** |
| Consents / directives | ❌ Not covered | No evidence in export | Unknown if product stores consent data |
| Patient communications / portal messages | ❌ Not covered | No messaging data in export | Product has patient portal with messaging; **gap** |
| Allergy skin testing (specialty) | ❌ Not covered | No skin test data in C-CDA | Core specialty function of product; **major gap** |
| Immunotherapy management (specialty) | ❌ Not covered | No immunotherapy data in C-CDA | Core specialty function of product; **major gap** |
| Spirometry / PFT (specialty) | ❌ Not covered | No spirometry data in C-CDA | Product feature; **gap** |
| Infusion management (specialty) | ❌ Not covered | No infusion data in C-CDA | Product feature; **gap** |

**Summary**: All clinical domains receive "Partial" rather than "Covered" because while C-CDA likely includes basic data for each, the lack of any documentation means we cannot confirm completeness. All specialty and billing domains are clearly not covered by a C-CDA Clinical Summary.

## 6. Documentation Quality

The documentation quality is **extremely poor** for a (b)(10) export:

- **No data dictionary**: Zero documentation of what data elements are in the export
- **No schema**: No machine-readable or human-readable description of the export structure
- **No sample data**: No example files to inspect
- **Process-only documentation**: The 9-page PDF is entirely about *how to request* an export, not *what the export contains*
- **Ambiguous format**: CSV is mentioned but never described; the File Type dropdown is shown but its options are hidden
- **No technical specification**: A developer could not build an import from this documentation. They would know how to click buttons to request an export, but would have no idea what fields, formats, or structure to expect in the output.

The document reads as an internal user guide for the export request workflow, not as technical documentation of the export format and content. It answers "how do I request an export?" but not "what will I get?"

**Could a developer build an import?** No. A developer would receive ZIP files containing C-CDA XML and would need to reverse-engineer the schema from the files themselves. No field mapping, no data dictionary, no relationship documentation exists.

## 7. Overall Assessment

### Classification

**Standard-based projection**

The export is confirmed to be C-CDA Clinical Summary XML documents. This is a standard clinical document format that covers a defined subset of patient data — primarily the clinical summary data that overlaps with USCDI. It is not the vendor's native data model. There is no evidence of native database export, and the C-CDA Clinical Summary format inherently cannot represent the specialty allergy/immunology data, billing/RCM data, or practice management data that is core to what ModuleMD WISE™ stores.

The mention of CSV as a possible format introduces ambiguity — if CSV export exists and includes native database tables, the classification could be different. But with zero documentation of CSV content and all screenshots showing C-CDA, the evidence supports classifying this as a standard-based projection.

### Key Findings

1. **C-CDA Clinical Summary repackaged as (b)(10) export**: The export produces C-CDA XML Clinical Summary documents per patient. This is the same format used for Transitions of Care [(b)(1)] and patient access, not a purpose-built EHI export. The `_ClinicalSummary` filename suffix confirms this. *(PDF pages 7–8)*

2. **Zero data dictionary or field documentation**: The entire (b)(10) documentation is a 9-page process flow PDF with UI screenshots. There is no data dictionary, no schema, no sample data, and no description of what data elements are exported. *(All 9 pages reviewed; `analysis/pdf_analysis_output.json`)*

3. **All specialty data missing from export**: ModuleMD WISE™'s core value proposition — allergy skin testing, immunotherapy management, spirometry, infusion center management — has no representation in a C-CDA Clinical Summary. These are the most important data domains this product uniquely stores, and they are entirely absent from the export. *(Product capabilities per `product-research.md`; C-CDA limitations are inherent to the format)*

4. **Billing/RCM data entirely absent**: The product includes a full billing and revenue cycle management module (claims, payments, ERA/EOB processing), confirmed by the "Billing" tab visible in screenshots. None of this data appears in the C-CDA export. *(PDF page 6 shows Billing tab; no billing content in C-CDA)*

5. **Ambiguous CSV mention never elaborated**: Page 1 references "data dictionary for comma separated values (csv) file(s)" as a possible export format, and a File Type dropdown exists, but neither the dropdown values nor any CSV documentation is provided anywhere. *(PDF pages 1 and 4)*

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA XML (Clinical Summary)
Model type:      Standard projection (C-CDA)
Entities:        N/A (no data dictionary)
Fields:          N/A (no data dictionary)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (Select All Patients option)
Domains covered: 0 of 19 fully covered; ~10 of 19 partially via C-CDA
```

### Bottom Line

ModuleMD WISE™'s (b)(10) export is a C-CDA Clinical Summary repackaged as an EHI export, accompanied by a 9-page process flow guide with no data dictionary or technical documentation. For a specialty allergy/immunology EHR with integrated billing/RCM, this export misses the product's most distinctive and valuable data — allergy skin testing, immunotherapy protocols, spirometry results, infusion management records, and all billing/financial data. A patient or provider receiving this export would get a basic clinical summary but would lose the vast majority of their specialty care records and all financial data.
