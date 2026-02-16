# EHI Export Analysis: Physicians EMR, LLC

**Product**: IPClinical v2.1
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.05.05.2163.PEMR.01.00.1.200123

## 1. Product Context

IPClinical is a cloud-based EHR and practice management platform developed by Physicians EMR, LLC, a small Florida-based company founded by cardiologist Dr. Wasim Ahmar. The product targets small-to-mid-size ambulatory practices across specialties including cardiology, spine care, primary care, and diagnostic centers. The company has minimal public visibility (no G2/Capterra/KLAS reviews).

**Data domains the product stores** (based on product research and feature pages):

- **Clinical**: Patient demographics, clinical notes, encounter documentation, medical history, medications/e-prescribing, lab results, imaging results, treatment plans, problems/conditions, allergies, immunizations, vitals, CPOE orders, clinical quality measures
- **Billing/RCM**: Insurance eligibility verification, charge capture, claim submission, rejection/denial management, payment posting, accounts receivable, authorization/pre-approvals
- **Scheduling**: Appointment scheduling, reminders, cancellation lists
- **Documents**: PDF/image document management, fax management, scanned records, medical transcription
- **Patient engagement**: Patient portal with view/download/transmit
- **Specialty**: Remote patient monitoring, cardiac device home monitoring
- **Administrative**: Task management, provider credentialing (outsourced service)

The product is broadly certified across 47 ONC criteria, including (b)(10) EHI export, (g)(10) FHIR API, and a full suite of clinical criteria.

## 2. Artifacts Reviewed

| Artifact | Size | Description | Informativeness |
|---|---|---|---|
| `b_10_Electronic_Health_Information_export.pdf` | 2 pages (467 KB) | The primary (b)(10) EHI export documentation. Page 1 is a cover page; page 2 describes three export formats (C-CDA, FHIR, Excel/PDF) in a single page of prose. Created Nov 23, 2023 by Ahmed Tariq. | **Low** — no data dictionary, no field definitions, no sample data, no export instructions |
| `IPClinical_g10_API_Documentation.pdf` | 121 pages (784 KB) | The (g)(10) FHIR API documentation. Covers SMART on FHIR authentication, Bulk Data export, and all US Core FHIR resources with sample requests/responses and search parameters. Created May 24, 2023. | **Medium** — thorough FHIR API spec but strictly limited to US Core / USCDI scope |
| `IPClinical-api-documentation.pdf` | 8 pages (270 KB) | Older proprietary API documentation (IPClinical API v5.0). Describes OAuth2 auth, patient search, and data retrieval as C-CDA XML. Lists USCDI v1 data classes. Created Mar 26, 2024 (copyright 2021). | **Low** — superseded by the g10 doc; returns the same C-CDA data via a proprietary endpoint |

**Total**: 3 PDFs, 131 pages combined. No data dictionary, no database schema, no sample export files, no JSON/XML schemas for non-FHIR exports.

## 3. Export Mechanics

The (b)(10) documentation describes three export formats:

1. **C-CDA**: Single patient and patient population export of USCDI v1 data. References three C-CDA specifications (CDA R2 IHE Health Story Consolidation DSTU 1.1, C-CDA R2.1, C-CDA R2.1 Companion Guide R2). No vendor-specific mapping or examples provided.

2. **FHIR**: Single patient and patient population export via FHIR US Core STU V3.1.1 and FHIR Bulk Data Access V1.0.1. The 121-page g10 doc provides the technical specification. The CapabilityStatement lists 21 FHIR resource types. Supports group-export, patient-export, and system-level export operations. FHIR endpoint: `https://staging.pemr.com:93/api`.

3. **Excel/PDF**: Described in a single paragraph with no technical detail:
   - Patient Documents (lab results, radiology reports, scanned/imported/faxed documents) → PDF
   - Scheduling & Appointments → Excel and PDF
   - Billing & Financial information → "most" in Excel, "some" in PDF
   - Imaging Result Reports → FHIR

**Mechanism**: The b10 document does not describe the actual export mechanism (UI button, API call, admin action). The FHIR exports are clearly API-based. The Excel/PDF exports are undocumented — it's unclear whether they are generated from a UI, requested through support, or created ad-hoc.

**Access constraints**: The g10 doc states "IPClinical does not currently charge any fees for the use of the API" but "reserves the right to charge fees for future use." No other access constraints mentioned.

**Single vs. bulk**: Both single patient and patient population export are stated for C-CDA and FHIR. The Excel/PDF exports are not described in these terms.

## 4. Export Content: What's In It

### No data dictionary

There is **no data dictionary** for any export format. The FHIR export is documented via its CapabilityStatement and US Core profiles (which define a standard schema), but there is no vendor-specific field mapping, no documentation of vendor extensions, and no documentation of what native database fields map to which FHIR elements.

The Excel/PDF exports have **zero field-level documentation** — no column names, no data types, no schemas, no sample files.

### FHIR Export Content (g10 documentation)

The g10 documentation covers 21 FHIR resource types in the CapabilityStatement and provides 30 documented sections with sample requests and responses for each. The resources are strictly US Core profiles with no documented vendor extensions.

**FHIR Resource Types in CapabilityStatement (21)**:

| Resource Type | Category | Has Sample Response | Notes |
|---|---|---|---|
| AllergyIntolerance | Clinical | Yes | US Core profile |
| CarePlan | Clinical | Yes | US Core profile |
| CareTeam | Clinical | Yes | US Core profile |
| Condition | Clinical | Yes | US Core profile |
| Device | Clinical | Yes | Implantable devices only |
| DiagnosticReport | Clinical/Lab | Yes | Two sections: notes exchange + lab results |
| DocumentReference | Documents | Yes | Includes Clinical Notes Guidance (10+ pages of samples) |
| Encounter | Clinical | Yes | US Core profile |
| Goal | Clinical | Yes | US Core profile |
| Group | Administrative | No | Listed in CapabilityStatement only (for Bulk Data groups) |
| Immunization | Clinical | Yes | US Core profile |
| Location | Administrative | No | Listed in CapabilityStatement, no dedicated section |
| Medication | Medications | No | Listed in CapabilityStatement, no dedicated section |
| MedicationRequest | Medications | Yes | US Core profile |
| Observation | Vitals/Lab | Yes | 12 sub-sections covering vitals, smoking status, lab results, pediatric measures |
| Organization | Administrative | Yes | US Core profile |
| Patient | Demographics | Yes | US Core profile with race, ethnicity, birthsex extensions |
| Practitioner | Administrative | Yes | US Core profile |
| PractitionerRole | Administrative | No | Listed in CapabilityStatement, no dedicated section |
| Procedure | Clinical | Yes | US Core profile |
| Provenance | Administrative | Yes | US Core profile |

### Vendor's own content organization

The vendor organizes the (b)(10) export into three categories:

| Category (vendor's) | Format | Detail Level | Entities/Fields |
|---|---|---|---|
| Clinical EHI (C-CDA/FHIR) | C-CDA XML, FHIR JSON | Well-documented via standards | 21 FHIR resource types, ~300+ standard FHIR fields across profiles |
| Patient Documents | PDF | One sentence description | No schema; "lab results, radiology reports, scanned/imported/faxed documents" |
| Scheduling & Appointments | Excel, PDF | One sentence description | No schema; zero column definitions |
| Billing & Financial information | Excel (most), PDF (some) | One sentence description | No schema; qualified with "most" — scope unclear |
| Imaging Result Reports | FHIR | References FHIR export | Covered by DiagnosticReport resource |

### Excel/PDF Export Content (b10 documentation)

The Excel/PDF exports are described in exactly one paragraph (82 words) on page 2 of the b10 document. The full text:

> "EHI including other information such as Patient Documents, Scheduling & Appointments and Billing & Financial information can be exported via Excel/PDF file formats. All patient documents including lab results, radiology reports and any other scanned/imported/ faxed documents can be exported in PDF format. Images available under Imaging Result Reports are exported through FHIR format as well. In regards to scheduling and appointments, IPClinical is capable to export that information via both Excel and PDF formats. Lastly, most of the billing and financial information can be exported in Excel format and some of it can also be exported in PDF format."

There are:
- **0** column/field definitions for the Excel exports
- **0** sample export files
- **0** data type specifications
- **0** relationship descriptions
- No explanation of what "most" billing information means

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export strategy is a two-tier approach:

1. **Clinical data (well-specified)**: FHIR US Core / C-CDA covering the standard USCDI v1 data classes — demographics, allergies, conditions, medications, labs, vitals, immunizations, procedures, care plans, goals, encounters, clinical notes, implantable devices, smoking status, provenance. This is documented in 121 pages with sample requests and responses. It covers the standard clinical interoperability scope.

2. **Non-clinical data (unspecified)**: Excel/PDF exports for scheduling, billing, and documents. This is described in a single paragraph with no technical detail whatsoever. The word "most" qualifying billing data is a red flag — it explicitly acknowledges incomplete coverage without specifying what's excluded.

The clinical FHIR/C-CDA layer is the standard US Core projection — it captures clinical summaries but not the vendor's native data model. The Excel/PDF layer theoretically extends coverage to billing and scheduling but is completely undocumented.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | FHIR `Patient` resource with US Core extensions (race, ethnicity, birthsex). Sample response shows name, phone, address, gender, DOB, language, MRN. | Standard USCDI coverage; likely missing some native fields (e.g., employer, emergency contacts in structured form) |
| Encounters / visits | ✅ Covered | FHIR `Encounter` resource | Standard profile only |
| Problems / conditions | ✅ Covered | FHIR `Condition` resource | Standard profile only |
| Medications / prescriptions | ✅ Covered | FHIR `MedicationRequest` resource | Standard profile; e-prescribing details (pharmacy, prior auth) may be lost |
| Allergies | ✅ Covered | FHIR `AllergyIntolerance` resource | Standard profile only |
| Immunizations | ✅ Covered | FHIR `Immunization` resource | Standard profile only |
| Vitals | ✅ Covered | 12 `Observation` sections covering BP, height, weight, temp, heart rate, respiratory rate, pulse oximetry, pediatric growth, smoking status | Thorough vital sign coverage via standard profiles |
| Lab results | ✅ Covered | FHIR `DiagnosticReport` (lab) and `Observation` (lab result) resources | Standard profile only |
| Imaging / diagnostic reports | ⚠️ Partial | FHIR `DiagnosticReport` (notes exchange) covers reports; b10 doc says "Imaging Result Reports are exported through FHIR format." Documents exported as PDF. | Report text likely covered; actual images unclear |
| Procedures | ✅ Covered | FHIR `Procedure` resource | Standard profile only |
| Clinical notes / documents | ✅ Covered | FHIR `DocumentReference` with extensive examples (progress notes, procedure notes). 10+ pages of Clinical Notes Guidance with 7 sample documents. PDF export of documents. | Good coverage through FHIR + PDF export |
| Care plans / goals | ✅ Covered | FHIR `CarePlan` and `Goal` resources | Standard profiles only |
| Orders / referrals | ⚠️ Partial | Product is certified for CPOE (a)(1)-(a)(3) and clinical decision support. No dedicated order/referral resource in the export. MedicationRequest covers medication orders. | Product has CPOE; non-medication orders (lab, imaging, referral) may not be captured in export |
| Insurance / coverage | ⚠️ Partial | b10 doc mentions "Billing & Financial information" exportable in Excel. No dedicated insurance/coverage entity documented. | Product does insurance eligibility verification; no evidence of insurance data structure in export |
| Claims / billing | ⚠️ Partial | b10 doc says "most of the billing and financial information can be exported in Excel format." No field definitions. | Product has comprehensive RCM (charge capture, claim submission, denial management, payment posting, AR). "Most" qualifier explicitly acknowledges gaps. Zero documentation of what's included. |
| Payments | ⚠️ Partial | Subsumed under "billing & financial information" — no specific mention | Product does payment posting and AR; no evidence of structured payment data in export |
| Consents / directives | ❌ Not covered | No mention in any artifact | Unclear if product stores structured consents; possible N/A |
| Patient communications / portal messages | ❌ Not covered | Product has patient portal (certified (e)(1)-(e)(3)); no mention of portal data in export | Product stores portal interactions; not included in export |
| Specialty-specific (cardiology, RPM) | ❌ Not covered | Product website mentions cardiac device monitoring, remote patient monitoring, specialty-specific documentation. No mention in export. | Product is founded by a cardiologist and serves cardiology practices; RPM and cardiac monitoring data appear absent from export |

**Domains covered**: 10 of 17 applicable domains fully covered (all via standard FHIR profiles)
**Domains partially covered**: 5 (billing, insurance, payments, orders, imaging — mentioned but undocumented)
**Domains not covered**: 2 clearly missing (portal communications, specialty/RPM data); consents unclear

## 6. Documentation Quality

**FHIR/C-CDA documentation (g10 doc)**: Adequate for its scope. The 121-page document provides resource-by-resource documentation with search parameters, sample requests, and sample JSON responses for each US Core resource type. The CapabilityStatement is included in full. A developer could build a FHIR US Core client from this documentation. However, this is standard US Core documentation — it describes the standard profiles, not vendor-specific data mappings.

**b10 export documentation**: Very poor. The entire (b)(10)-specific content is a single page of prose (82 words describing the Excel/PDF exports, plus references to C-CDA/FHIR standards). There is:
- No data dictionary for any format
- No field definitions for Excel exports
- No sample export files
- No export instructions or screenshots
- No description of the export mechanism (UI vs. API vs. manual process)
- No information about data volume or completeness guarantees

**Overall**: A developer could reconstruct standard USCDI clinical data from the FHIR API. A developer could **not** understand, validate, or import the billing, scheduling, or document exports — there is literally nothing to build against. The documentation is a compliance artifact, not a technical specification.

**Machine-readable artifacts**: The g10 doc includes a FHIR CapabilityStatement JSON and sample FHIR JSON responses. There are no machine-readable artifacts for the Excel/PDF exports.

## 7. Overall Assessment

### Classification

**Standard-based projection**: The export is primarily the vendor's FHIR US Core / C-CDA implementation relabeled as "(b)(10)." The vendor adds a paragraph mentioning Excel/PDF exports for billing and scheduling, but with zero documentation. The FHIR/C-CDA components cover only the standard USCDI clinical summary scope (~20-30% of what the product stores). The Excel/PDF layer is too undocumented to assess.

### Key Findings

1. **The (b)(10) documentation is a single page.** The entire EHI export specification beyond C-CDA/FHIR references is 82 words describing Excel/PDF exports for billing, scheduling, and documents — with no data dictionary, no field definitions, and no sample data. (`b_10_Electronic_Health_Information_export.pdf`, page 2)

2. **The export is a FHIR/C-CDA repackaging.** The vendor's substantial documentation effort (121 pages) went into the (g)(10) FHIR API, which covers standard US Core resources. The (b)(10) document simply points to this plus a vague mention of Excel/PDF. The FHIR API covers 21 US Core resource types — all standard clinical interoperability data, none of the vendor's native data model.

3. **Billing coverage is explicitly qualified as incomplete.** The b10 document says "most of the billing and financial information can be exported in Excel format" — the word "most" explicitly acknowledges that not all billing data is exportable. For a product with comprehensive RCM features (charge capture, claim submission, denial management, payment posting, AR), this is a significant and self-acknowledged gap.

4. **No native database model is exposed.** The export does not include any vendor-specific tables, custom fields, or internal data structures. Everything is projected through C-CDA/FHIR standards or exported as undocumented Excel/PDF files.

5. **Specialty and RPM data are absent.** The product serves cardiology practices and offers remote patient monitoring and cardiac device monitoring, but none of this data appears in the export documentation.

### Summary Stats

```
Classification:  Standard-based projection
Export format:   FHIR R4 JSON, C-CDA XML, Excel, PDF
Model type:      Standard projection (US Core FHIR + C-CDA) with undocumented Excel/PDF supplement
Entities:        21 FHIR resource types (no native entities documented)
Fields:          ~300+ (standard FHIR profile fields only; Excel/PDF fields unknown)
Descriptions:    N/A (uses standard FHIR profile definitions; no vendor-specific descriptions)
Sample data:     Yes (FHIR sample responses in g10 doc); No (no sample Excel/PDF exports)
Bulk export:     Yes (FHIR Bulk Data Access supported)
Domains covered: 10 of 17 applicable domains (fully, via standard FHIR); 5 partially
```

### Bottom Line

IPClinical's EHI export is a standard FHIR US Core / C-CDA implementation relabeled as "(b)(10)," supplemented by a single paragraph mentioning undocumented Excel/PDF exports for billing and scheduling. A patient or provider would receive a standard clinical summary via FHIR/C-CDA covering demographics, conditions, medications, labs, and notes — but billing records, scheduling data, insurance information, RPM data, and specialty clinical data would either be missing or delivered as undocumented Excel files that no receiving system could interpret without reverse engineering. The single biggest gap is the complete absence of field-level documentation for the non-FHIR exports, making it impossible to assess whether the billing and scheduling data is actually usable.
