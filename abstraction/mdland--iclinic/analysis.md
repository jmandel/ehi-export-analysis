# EHI Export Analysis: MDLand International Corp

**Product**: iClinic v12.3
**Analysis date**: 2026-02-16
**CHPL IDs**: 9814 (15.04.04.1828.iCli.12.00.1.181221)

## 1. Product Context

iClinic is a comprehensive, cloud-based ambulatory EHR and practice management system developed by MDLand International Corp, a small company (~75 employees) headquartered in Great Neck, New York. The product targets outpatient physician practices of all sizes, from solo practitioners to large physician organizations (MSOs, IPAs, ACOs). Notable customers include Northwell Health, NYC Health + Hospitals, and SOMOS Community Care, suggesting a concentration in the New York metro area.

iClinic is a unified platform that combines:

- **Clinical documentation**: encounter notes, customizable templates, problem lists, vitals, clinical decision support
- **E-prescribing**: integrated prescribing including EPCS for controlled substances via Surescripts
- **Lab & imaging interfacing**: lab ordering, results, abnormal result notifications, trend tracking
- **Billing & practice management**: electronic claim submission, claim status tracking, payment posting, eligibility checking, denied/rejected claim management
- **Scheduling**: multi-provider web-based appointment scheduling
- **Document management**: scanning, uploading, centralized repository
- **Patient portal (iClinicHealth)**: mobile app with medical history, lab results, medication refill requests, appointment booking, secure messaging
- **Telehealth**: HIPAA-compliant video visits integrated within the EHR
- **Care management**: CCM, RPM, TCM, CoCM, PCM programs with enrollment, care plans, time tracking
- **Public health reporting**: immunization registries, syndromic surveillance, cancer registry, electronic case reporting

This is a full-featured ambulatory EHR with integrated billing — the CHPL certification covers 37 criteria including (b)(10) EHI export, (g)(10) FHIR API, transitions of care, patient portal, and clinical quality measures. The breadth of stored data is substantial: demographics, clinical records, medications, allergies, labs, imaging, immunizations, documents, scheduling, billing/claims, portal messages, telehealth records, care management data, and public health reports.

## 2. Artifacts Reviewed

| Artifact | Type | Size | Description | Informativeness |
|---|---|---|---|---|
| `ehiexport.pdf` | PDF, 2 pages | 250 KB | The entire EHI export documentation. A user guide describing how to trigger the export, the output format (XML in password-protected ZIP), and scope options. Contains two UI screenshots. **No data dictionary, no schema, no field definitions, no sample data.** | **Low** — answers "how to trigger" but not "what's in it" |
| `ehiexport-page1.png` | PNG | 231 KB | Rendered image of PDF page 1 (regulatory text and instructions) | Redundant with PDF |
| `ehiexport-page2.png` | PNG | 275 KB | Rendered image of PDF page 2 (UI screenshots showing the Patient Data Export interface with batch records from 2020–2023) | Redundant with PDF |

**URL verification (2026-02-16)**: The registered EHI documentation URL (`https://mdland.net/iClinicEHR/ehiexport/`) returns HTTP 302 redirecting to `/static/docs/ehiexport.pdf`, which returns HTTP 200 with `Content-Type: application/pdf`. The URL is accessible and serves the same 250,123-byte PDF.

Only one substantive artifact exists. The PDF is the entirety of MDLand's public EHI export documentation.

## 3. Export Mechanics

Based on the PDF (`ehiexport.pdf`, pages 1–2):

- **Format**: XML files in a password-protected ZIP archive. The PDF references the W3C XML standard (`https://www.w3.org/TR/xml/`) as the format specification, but provides no vendor-specific XML schema, DTD, XSD, or structural documentation.
- **Mechanism**: UI-driven with server-side processing by MDLand IT. The workflow is:
  1. Log in as an authorized user
  2. Navigate to Settings → Advanced → Patient Data Export
  3. Select export scope and click Submit
  4. Wait for MDLand IT to complete processing (10 minutes to several hours)
  5. Receive an iClinic inbox message with the ZIP password
  6. Download the ZIP file and extract the XML
- **Single-patient vs bulk**: Both supported. Export scope options visible in the UI screenshot (page 2) are:
  - All Patients (include Active, Inactive, and Deceased)
  - All Active Patients
  - Patient with Encounter
  - Patient with DOB
  - Specify Patient (single patient)
- **Access constraints**: Export is restricted to authorized users via privilege settings under "Advanced Settings." The feature is located at Settings → Advanced (ADM Only) → Patient Data Export, suggesting it requires administrator-level access.
- **Vendor involvement**: Step 3 explicitly states "After MDLand IT completes the processing" — the vendor's IT team is involved in generating the export file. This raises questions about whether the export can truly be executed "without subsequent developer assistance to operate" as required by §170.315(b)(10), though "developer assistance" and "IT processing" may be distinguished.
- **Fees**: Not mentioned in the documentation.

**Notable observations from the page 2 screenshots**:
- The Settings sidebar shows categories: General, EMR, VBP Setting, Patient Portal, Billing/Account, Schedule, Follow Up, ePrescription, Lab, Other Settings, Advanced (ADM Only). Under Advanced: Privilege, Security Log, Audit Report, User List, My Account, MD Network, **Patient Data Export**, Capitation Provider Setup, E-Payment. This confirms the export is an admin-only feature.
- The batch list shows 3 historical exports: Batch 1001 (11/12/2020, "All Active Patients", Finished), Batch 1006 (07/27/2023, "All Active Patients", Finished), Batch 1007 (11/30/2023, "Specify Patient", Downloaded). This confirms the feature has been operational since at least 2020.

## 4. Export Content: What's In It

### What the documentation tells us

**Nothing.** The PDF documentation contains zero information about the content or structure of the exported XML. Specifically, the documentation provides:

- **0** entity/table names
- **0** field/element names
- **0** data type definitions
- **0** field descriptions
- **0** relationship/foreign key definitions
- **0** value set/code system specifications
- **0** sample data files
- **0** XML schema definitions (XSD, DTD, RelaxNG)
- **0** namespace definitions

The only content-related claim is the regulatory assertion that the export includes "all of a single patient's electronic health information stored at the time of certification by the product." This is a regulatory compliance statement, not a technical specification.

### What we can infer (but cannot verify)

The reference to "XML format" and the involvement of "MDLand IT" in processing suggests this may be a server-side database extraction rendered as XML — potentially a comprehensive dump of the patient record. However, without any schema, data dictionary, or sample output, this is speculation. The XML could contain anything from a full native database model to a minimal subset of clinical data.

### Vendor's own content organization

No content organization is documented. The vendor provides no tables, entities, categories, or field listings of any kind. The following table is therefore empty:

| Entity/Table | Fields | Described | Types | Category (vendor's) |
|---|---|---|---|---|
| *(none documented)* | — | — | — | — |

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's documentation provides **no information** about what data domains are included in the export. There are no categories, no modules, no sections, no entity listings. The entire documentation is a 2-page user guide for triggering the export process.

The only structural evidence comes from the Settings sidebar visible in the page 2 screenshot, which shows iClinic modules (EMR, VBP Setting, Patient Portal, Billing/Account, Schedule, Follow Up, ePrescription, Lab, Other Settings, Advanced). These are product navigation categories, not export content categories — there is no documentation linking any of these modules to specific data in the export.

### 5b. Standardized domain coverage (top-down)

Without any data dictionary, schema, sample data, or content documentation, coverage cannot be assessed from the artifacts. Every domain below is marked as "Unknown" because the documentation provides no evidence either way.

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ❓ Unknown | No documentation of exported fields | Product stores demographics (registration, photos, ID scans, insurance); cannot verify export inclusion |
| Encounters / visits | ❓ Unknown | No documentation | Product stores encounter notes via customizable templates; cannot verify |
| Problems / conditions / diagnoses | ❓ Unknown | No documentation | Product has problem lists (certified (a)(5)); cannot verify |
| Medications / prescriptions | ❓ Unknown | No documentation | Product has e-prescribing including EPCS; cannot verify |
| Allergies | ❓ Unknown | No documentation | Product has allergy lists (certified (a)(4)); cannot verify |
| Immunizations | ❓ Unknown | No documentation | Product reports to immunization registries (certified (f)(1)); cannot verify |
| Vitals | ❓ Unknown | No documentation | Product records vitals; cannot verify |
| Lab results | ❓ Unknown | No documentation | Product interfaces with labs, stores results with trending; cannot verify |
| Imaging / diagnostic reports | ❓ Unknown | No documentation | Product interfaces with radiology/imaging centers; cannot verify |
| Procedures | ❓ Unknown | No documentation | Ambulatory procedures expected; cannot verify |
| Clinical notes / documents | ❓ Unknown | No documentation | Product has customizable clinical templates, document management; cannot verify |
| Care plans / goals | ❓ Unknown | No documentation | Product has CCM/RPM/TCM care management with care plans; cannot verify |
| Orders / referrals | ❓ Unknown | No documentation | Product supports lab ordering; referral tracking unclear; cannot verify |
| Insurance / coverage | ❓ Unknown | No documentation | Product stores insurance info, does eligibility checking; cannot verify |
| Claims / billing | ❓ Unknown | No documentation | Product has integrated billing with claim submission, payment posting; cannot verify |
| Payments | ❓ Unknown | No documentation | Product has electronic payment posting, E-Payment module visible in UI; cannot verify |
| Patient communications / portal messages | ❓ Unknown | No documentation | Product has patient portal (iClinicHealth) with secure messaging; cannot verify |
| Specialty-specific | N/A | No documentation | Product is general ambulatory, no specialty-specific modules identified |

**Summary**: 0 of 17 applicable domains can be confirmed as covered or not covered. The documentation is entirely silent on export content.

## 6. Documentation Quality

The EHI export documentation is a **2-page PDF user guide** that answers one question: "How do I trigger an export?" It does not answer:

- What data is in the export?
- How is the data structured?
- What XML elements and attributes are used?
- How are relationships between data represented?
- What encoding or namespaces are used?
- What value sets or code systems apply to coded fields?

**Could a developer build an import from this documentation?** No. A developer receiving this export would have a password-protected ZIP containing XML in an undocumented proprietary format. They would need to reverse-engineer the XML structure entirely from the raw data. The only "format specification" provided is a link to the generic W3C XML standard, which describes XML syntax but nothing about MDLand's specific data model.

**Machine-readable artifacts**: None. No XSD, DTD, RelaxNG, JSON schema, sample XML, or any other machine-readable format specification exists in the public documentation.

**Documentation currency**: The PDF was created on 2023-12-01 (per PDF metadata, author: Catherine Cai, created in Microsoft Word for Microsoft 365). The product was certified 2018-12-21. The document has not been updated since creation.

**Comparison to (b)(10) requirements**: The regulation requires the export format's "publicly accessible hyperlink" to be included with the exported files. MDLand provides a link to the W3C XML specification — this technically satisfies the letter of the requirement but provides no practical value, as it tells the recipient nothing about the proprietary XML structure.

## 7. Overall Assessment

### Classification

**Minimal/stub**: The documentation is too thin to assess what is actually exported. The entire public EHI export documentation is a 2-page user guide with zero information about export content, structure, or schema. There is no data dictionary, no field definitions, no sample data, and no XML schema. It is impossible to determine from the available artifacts whether the export covers a comprehensive set of EHI or a minimal subset.

### Key Findings

1. **No data dictionary or schema exists in the public documentation.** The entire EHI export documentation is a 2-page PDF (`ehiexport.pdf`, 250 KB, created 2023-12-01) that describes only how to trigger the export, not what it contains. Zero entities, zero fields, zero data types are documented.

2. **The export format is proprietary, undocumented XML.** Patient data is exported as XML in a password-protected ZIP. The only format reference is the generic W3C XML specification (`https://www.w3.org/TR/xml/`), which describes XML syntax but nothing about MDLand's data model. No XSD, DTD, or sample XML is provided.

3. **Vendor IT involvement in export processing.** Step 3 of the export workflow states "After MDLand IT completes the processing" — suggesting the vendor's IT team must process each export request. This is a potential concern for the (b)(10) requirement that users be able to export "without subsequent developer assistance."

4. **The export mechanism itself appears functional.** The UI screenshots show the Patient Data Export interface with historical batch records dating back to November 2020, confirming the feature has been operational. Both single-patient and population-level exports are supported with multiple filtering options.

5. **iClinic stores data across many domains that cannot be verified in the export.** The product includes clinical documentation, e-prescribing, lab interfacing, integrated billing, scheduling, patient portal, telehealth, and care management. None of these domains are confirmed or denied in the export documentation.

### Summary Stats

```
Classification:  Minimal/stub
Export format:   XML (proprietary, undocumented) in password-protected ZIP
Model type:      Unknown (no schema or data dictionary to determine)
Entities:        N/A (no data dictionary)
Fields:          N/A (no data dictionary)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (population-level export supported)
Domains covered: 0 of 17 applicable domains verifiable
```

### Bottom Line

MDLand's EHI export documentation is among the thinnest possible while still technically existing as a public URL. A patient or developer receiving this export would get a password-protected ZIP of proprietary XML with no schema, no field documentation, and no way to understand the data without reverse-engineering it. The single biggest gap is the complete absence of any content documentation — it is impossible to assess whether the export is comprehensive or minimal because the vendor has documented nothing about what the export actually contains.
