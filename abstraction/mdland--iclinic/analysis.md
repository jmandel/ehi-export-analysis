# EHI Export Analysis: MDLand

**Product**: iClinic (Professional and Enterprise editions)
**Analysis date**: 2026-02-15
**CHPL IDs**: 15.04.04.1828.iCli.12.00.1.181221 (CHPL ID 9814)

## 1. Product Context

MDLand iClinic is a comprehensive, cloud-based ambulatory EHR and practice management system developed by MDLand International Corp (Great Neck, NY; ~75 employees). Certified December 2018 (v12.3), it serves outpatient physician practices ranging from solo providers to large organizations (MSOs, IPAs, ACOs). Notable customers include Northwell Health, NYC Health + Hospitals, and SOMOS Community Care.

iClinic is a unified platform combining:
- **Clinical EHR**: demographics, encounters, problem lists, medications (including EPCS), allergies, vitals, clinical notes with customizable templates, clinical decision support
- **E-Prescribing**: integrated with Surescripts, EPCS via DUO two-factor authentication
- **Lab & imaging interfacing**: lab ordering, results, trend tracking, abnormal result alerts
- **Billing & practice management**: electronic claims submission, payment posting, eligibility checking, denied claim management, MACRA/MIPS reporting
- **Scheduling**: web-based multi-provider appointment management
- **Document management**: scanning, uploading, file organization
- **Patient portal (iClinicHealth)**: mobile app with records access, messaging, appointment management, medication refill requests, lab result viewing
- **Telehealth**: HIPAA-compliant video visits integrated within the EHR
- **Care management suite**: CCM, RPM, TCM, CoCM, PCM modules with enrollment, care plans, and time tracking
- **Population health**: care gap identification, quality score management

This is a full-featured ambulatory EHR with integrated billing — the (b)(10) export should cover clinical documentation across all these modules, billing/claims data, patient portal communications, care management records, and specialty clinical data.

## 2. Artifacts Reviewed

| Artifact | Description | Informative? |
|---|---|---|
| `ehiexport.pdf` (250,123 bytes, 2 pages) | The **sole** EHI export documentation. A procedural guide describing how to trigger the export (4-step workflow) and the output format (XML in password-protected ZIP). Contains two screenshots of the export UI. Created 2023-12-01 by Catherine Cai in Microsoft Word. | Low — describes mechanics only; zero content documentation |
| `ehiexport-page1.png` / `ehiexport-page2.png` | Rendered images of the PDF pages. Page 2 screenshots reveal the Settings sidebar (showing product modules: EMR, Billing/Account, Schedule, ePrescription, Lab, Patient Portal, etc.) and the Patient Data Export batch list (showing batch IDs from 2020–2023). | Marginally useful — confirms UI location and export scope options |

**No other artifacts exist.** There is no data dictionary, no XML schema, no sample data, no field documentation, no machine-readable artifact of any kind. The entire EHI export documentation consists of a single 2-page PDF.

**URL verification** (2026-02-15): The registered URL `https://mdland.net/iClinicEHR/ehiexport/` returns HTTP 302 redirecting to `/static/docs/ehiexport.pdf`, which returns HTTP 200 with the same 250,123-byte PDF. The URL is live and accessible.

## 3. Export Mechanics

- **Format**: XML files inside a password-protected ZIP archive. The PDF references the generic W3C XML specification (`https://www.w3.org/TR/xml/`) as the format standard — no vendor-specific schema (XSD, DTD, or RelaxNG) is provided or referenced.
- **Mechanism**: UI-driven with vendor-side processing. The user navigates to Settings → Advanced → Patient Data Export, selects an export scope, and clicks Submit. MDLand IT then processes the request server-side (Step 3 of the documented workflow states: "After MDLand IT completes the processing of Patient EHI fata [sic] file generation (it takes 10 minutes to a few hours depending on the data volume)"). The user receives a notification with an unzip password and downloads the file.
- **Single-patient vs bulk**: Both supported. Export scope options are:
  - All Patients (including active, inactive, and deceased)
  - All Active Patients
  - Patient with Encounter
  - Patient with DOB
  - Specify Patient (single patient)
- **Access constraints**: Export is restricted to authorized users via the "Advanced Settings" (ADM Only) menu. The password-protected ZIP adds a second layer. The documentation notes: "One task can be download once, please save the zip file in a safe place."
- **Fees**: Not documented in the PDF.
- **Vendor involvement**: Step 3 explicitly requires MDLand IT to process the export, which raises a question about whether users can truly "execute this capability at any time... without subsequent developer assistance" as required by §170.315(b)(10). The documentation describes this as a normal part of the workflow, not an exception.

## 4. Export Content: What's In It

**There is no documentation of what the export contains.** The PDF makes a single regulatory claim: the export includes "all of a single patient's electronic health information stored at the time of certification." Beyond this assertion, there is:

- **No data dictionary** — zero tables, zero fields documented
- **No XML schema** — no XSD, DTD, RelaxNG, or structure definition of any kind
- **No sample data** — no example XML files to inspect
- **No list of data domains** — no enumeration of what categories of data are included
- **No field-level documentation** — no field names, data types, value sets, constraints, or relationships
- **No entity/relationship documentation** — no description of how data is organized or related

### Vendor's own content organization

The vendor provides **no content organization**. The only insight into the product's data structure comes from the Settings sidebar visible in the Page 2 screenshot, which lists product modules: General, EMR, VBP Setting, Patient Portal, Billing/Account, Schedule, Follow Up, ePrescription, Lab, Other Settings, Advanced. These are UI navigation categories, not data export categories — the documentation does not map any of these to export content.

| Entity/Table | Fields | Described | Types | Category |
|---|---|---|---|---|
| *(none documented)* | — | — | — | — |

**Total entities documented: 0. Total fields documented: 0.**

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor documents **nothing** about export content. The PDF is entirely procedural — it explains how to trigger an export and what format the output is in (XML in ZIP), but provides zero information about what data is actually exported. There are no categories, no modules, no entity lists, and no field descriptions.

The only substantive claim is the regulatory assertion that the export includes "all of a single patient's electronic health information." This claim cannot be verified from the documentation.

### 5b. Standardized domain coverage (top-down)

Because no data dictionary, schema, or sample data exists, coverage cannot be assessed from the artifacts. Every domain below is marked as "unknown" — the export *may* include these domains, but the documentation provides no evidence either way.

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ❓ Unknown | No documentation | Product stores demographics (Section 1); cannot verify inclusion |
| Encounters / visits | ❓ Unknown | No documentation | Product stores encounters; cannot verify |
| Problems / conditions / diagnoses | ❓ Unknown | No documentation | Product stores problem lists; cannot verify |
| Medications / prescriptions | ❓ Unknown | No documentation | Product stores medications and e-prescribing history; cannot verify |
| Allergies | ❓ Unknown | No documentation | Product stores allergies; cannot verify |
| Immunizations | ❓ Unknown | No documentation | Product stores immunization records; cannot verify |
| Vitals | ❓ Unknown | No documentation | Product stores vitals; cannot verify |
| Lab results | ❓ Unknown | No documentation | Product stores lab orders and results; cannot verify |
| Imaging / diagnostic reports | ❓ Unknown | No documentation | Product interfaces with imaging centers; cannot verify |
| Procedures | ❓ Unknown | No documentation | Cannot verify |
| Clinical notes / documents | ❓ Unknown | No documentation | Product stores encounter notes and scanned documents; cannot verify |
| Care plans / goals | ❓ Unknown | No documentation | Product has CCM/RPM/TCM care management modules; cannot verify |
| Orders / referrals | ❓ Unknown | No documentation | Product supports lab ordering; cannot verify |
| Insurance / coverage | ❓ Unknown | No documentation | Product stores insurance information and eligibility; cannot verify |
| Claims / billing | ❓ Unknown | No documentation | Product has integrated billing with claims, payments, eligibility; cannot verify |
| Payments | ❓ Unknown | No documentation | Product supports electronic payment posting; cannot verify |
| Patient communications / portal messages | ❓ Unknown | No documentation | Product has patient portal with secure messaging; cannot verify |

**Note**: The inability to assess coverage is itself the primary finding. For a product with this breadth of functionality — integrated EHR, billing, e-prescribing, care management, patient portal, telehealth — the complete absence of content documentation is a significant compliance gap.

## 6. Documentation Quality

The documentation is **functionally useless for understanding export content**. It answers one question — "how do I trigger an export?" — and fails to answer the questions that matter for (b)(10) compliance:

- **What data is exported?** Not documented.
- **How is it structured?** Not documented beyond "XML."
- **What are the fields and their meanings?** Not documented.
- **How are entities related?** Not documented.
- **What value sets are used?** Not documented.

**Could a developer build an import from this documentation?** No. A developer receiving the XML output would have to reverse-engineer the entire structure. The only format reference is the generic W3C XML specification, which says nothing about the vendor's data model.

**Machine-readable artifacts**: None. No XSD, no JSON Schema, no sample data, no API specification.

**Documentation scope**: 2 pages. For comparison, a well-documented EHI export typically includes dozens to hundreds of pages of data dictionary covering table structures, field definitions, data types, value sets, and relationships. This PDF contains none of that.

The document was created December 1, 2023 (after the original December 2018 certification date) and has not been updated since. It appears to be a minimal compliance document created to satisfy the (b)(10) documentation URL requirement rather than to genuinely support data portability.

## 7. Overall Assessment

### Classification

**Minimal/stub**: The documentation is too thin to assess what is exported. The entire EHI export documentation is a 2-page procedural guide with zero content documentation — no data dictionary, no schema, no sample data, no field definitions. While an export mechanism appears to exist (XML in password-protected ZIP with both single-patient and population scope), the complete absence of structural or content documentation makes it impossible to evaluate whether the export covers all EHI or any subset of it.

### Key Findings

1. **Zero content documentation**: The entire (b)(10) documentation is a 2-page PDF that describes *how to trigger* an export but provides *no information whatsoever* about what the export contains. There are 0 entities, 0 fields, 0 data types, 0 relationships documented. (`ehiexport.pdf`, pages 1–2)

2. **Vendor processing dependency**: Step 3 of the export workflow states that "MDLand IT completes the processing" after the user submits the request, taking "10 minutes to a few hours." This vendor-side processing step raises questions about whether the export truly operates "without subsequent developer assistance" as required by §170.315(b)(10). (`ehiexport.pdf`, page 1)

3. **No schema or sample data**: The only format specification referenced is the generic W3C XML standard (`https://www.w3.org/TR/xml/`). No vendor-specific XML schema (XSD, DTD), sample XML, or structural documentation exists. A recipient of this export would have to reverse-engineer the XML to use it.

4. **Export mechanism does exist**: Despite the documentation gaps, the screenshots confirm that a Patient Data Export feature exists in the product UI under Settings → Advanced, with batch processing, status tracking, and download capability. Batch records from 2020–2023 are visible, suggesting the feature is operational. (`ehiexport.pdf`, page 2 screenshots)

5. **Significant product breadth vs. documentation void**: iClinic is a comprehensive platform (EHR + billing + e-prescribing + care management + patient portal + telehealth). The gap between the product's data breadth and the documentation's completeness (zero) is among the widest possible for a certified product.

### Summary Stats

```
Classification:  Minimal/stub
Export format:   XML (in password-protected ZIP)
Model type:      Unknown (no schema or documentation to determine)
Entities:        0 documented
Fields:          0 documented
Descriptions:    N/A (no fields documented)
Sample data:     No
Bulk export:     Yes (population-level export supported)
Domains covered: 0 of 17 verifiable (export claims "all EHI" but documents none)
```

### Bottom Line

MDLand's EHI export documentation for iClinic is a 2-page procedural PDF that describes how to trigger an XML export but provides absolutely no information about what data the export contains. With zero entities, zero fields, and zero structural documentation, it is impossible to assess whether patients or providers would receive a complete copy of their data. The single biggest gap is the total absence of a data dictionary or schema — without it, the export is a black box that cannot be independently evaluated, imported, or verified for completeness.
