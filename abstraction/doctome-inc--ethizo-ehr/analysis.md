# EHI Export Analysis: DocToMe, Inc.

**Product**: ethizo EHR v2.0
**Analysis date**: 2026-02-15
**CHPL IDs**: 10265 (15.05.05.3060.DOTM.01.00.1.200107)

## 1. Product Context

ethizo EHR is a cloud-based, ONC-certified EHR and practice management platform built by DocToMe, Inc., a very small (~5–9 employees) physician-founded company in Gig Harbor, WA. Despite its size, ethizo has achieved an unusually broad ONC certification covering clinical criteria (a)(1)–(a)(14), transitions of care (b)(1)–(b)(5), CQMs (c)(1)–(c)(4), patient portal (e)(1)–(e)(3), public health reporting (f)(1), (f)(2), (f)(7), FHIR API (g)(10), and direct messaging (h)(1).

The product targets ambulatory practices, FQHCs, and post-acute/long-term care (PALTC) facilities across 20+ specialties. It comprises eight modules:

1. **Certified EHR** — Clinical documentation, CPOE, CDS, lab/radiology orders, scheduling
2. **Practice Management System (PMS)** — Full billing/RCM: claims scrubbing, ERA posting, eligibility verification, copay collection, PCI-compliant payments, revenue KPIs
3. **Patient Portal** — Appointments, messaging, medication tracking, Fitbit integration, questionnaires
4. **Vezo (Telemedicine)** — Virtual visits with chat, scheduling, transit notes
5. **Hybrid eFax** — Fax/email/e-signature document management
6. **IVR** — Automated phone triage and call tracking
7. **CCM (Chronic Care Management)** — Enrollment, care plans, activity tracking, automated billing
8. **RPM (Remote Patient Monitoring)** — Device-agnostic vitals via cellular devices (BP, glucose, CGM, SpO2, weight, temp, HR, ECG)

For EHI export assessment, the key question is whether the export covers not just the CDA-friendly clinical data but also the billing/PMS data, RPM device data, telemedicine records, patient portal messages, and specialty-specific content.

## 2. Artifacts Reviewed

| Artifact | Source | What it is | Informativeness |
|---|---|---|---|
| `EHI-Export-b.10-Documentation-v2.pdf` | [ethizo.com](https://www.ethizo.com/wp-content/uploads/2025/03/EHI-Export-b.10-Documentation-v2.pdf) | 9-page PDF (created 2025-03-01, MS Word). Sole documentation artifact. Contains export process description, CDA data dictionary with XPATH paths and code systems, brief mentions of CSV and document exports. | **Primary source** — most informative |
| `ehi-export-landing-page.png` | [ethizo.com/electronic-health-information-export/](https://www.ethizo.com/electronic-health-information-export/) | Screenshot of landing page. Contains heading and single download link. | Minimal — confirms single-PDF approach |
| FHIR API documentation (live) | [fhir-api.ethizo.com](https://fhir-api.ethizo.com/) | Postman-hosted FHIR R4 API docs. 47 resource-type folders. Standard US Core resources. Base URL: `https://fhir.ethizo.com/api/4.0.0`. | Verified: no billing, scheduling, or custom EHI resources |

No sample data files, no machine-readable schemas (XSD, JSON Schema), no data dictionaries for the CSV exports, and no FHIR Bulk Data documentation for (b)(10) were found. The entire EHI export documentation is a single 9-page PDF.

## 3. Export Mechanics

- **Format**: ZIP file containing: (1) CDA XML (C-CDA R2.1), (2) CSV for demographics/insurance, (3) CSV for appointments, (4) scanned documents (PDF/JPG/PNG)
- **Mechanism**: UI-based. "Share Data" option in the EHR.
  - *Single patient*: Search patient → "Share Data" in left menu → select sections → "Process" → secure link delivered via email/text → download ZIP
  - *Bulk/population*: "Quick Links" → "Share Data" → choose EHI export → select sections → "Process" → secure link → download ZIP of ZIPs
- **Bulk export**: Yes, supported via the bulk pathway. Each patient gets a separate ZIP within a master ZIP.
- **Access constraints**: Secure link delivery with token-based access. No mention of fees.
- **FHIR alternative**: A single sentence mentions FHIR Bulk Data for population-level export per §170.315(b)(10)(ii), with no further documentation.

## 4. Export Content: What's In It

### CDA Data Dictionary

The PDF provides a field-level data dictionary for the CDA (C-CDA R2.1) output. Based on manual verification of the PDF text (see `analysis/cda_dictionary_analysis.json`):

- **24 CDA sections** documented (20 with OID identifiers)
- **82 data elements** across all sections
- **13 unique code systems** referenced: AdministrativeGender, CDC Race & Ethnicity, CPT, CPT-4, CVX, GMDN, HCPCS, ICD-10, LOINC, NCI Thesaurus, NDC, RxNorm, SNOMED
- Each element includes XPATH/Entry paths and OID-based code system references
- **No field descriptions** beyond the element name — names are self-explanatory clinical labels (e.g., "Vaccine," "Dose," "Lot Number") but no definitions or business rules
- **No value set bindings** — code systems are identified but specific allowed values are not specified
- **No relationship/FK documentation** — the CDA structure provides implicit hierarchy (e.g., encounter → diagnosis) but cross-file relationships are undocumented
- **No data types** explicitly stated (types are implied by the CDA standard)

### Vendor's own content organization

The PDF organizes the export into four components:

| Component | Format | Elements/Fields | Documented | Category |
|---|---|---|---|---|
| Clinical Data in CDA Format | C-CDA R2.1 XML | 82 elements across 24 sections | Yes — XPATH paths + code systems | Clinical |
| Patient Demographics and Insurance Details | CSV | Unknown | **No** — zero field documentation | Demographics/Insurance |
| Appointments | CSV | Unknown | **No** — zero field documentation | Scheduling |
| Documents | PDF/JPG/PNG | N/A (file-based) | Organizational structure described | Documents |

#### CDA sections detail

| CDA Section | Elements | Code Systems |
|---|---|---|
| Patient Demographics/Information | 6 | AdministrativeGender, CDC Race & Ethnicity |
| Provider's name and office contact | 3 | — |
| Date and Location of visit | 2 | — |
| Chief Complaint and Reason for visit | 1 | — |
| Encounters | 5 | CPT, SNOMED, ICD-10 |
| Immunizations | 9 | CVX, CPT-4, NCI Thesaurus, SNOMED |
| Instructions | 1 | SNOMED |
| Treatment Plan | 2 | LOINC |
| Social History | 3 | LOINC, SNOMED |
| Problems | 3 | SNOMED, ICD-10 |
| Medications | 5 | RxNorm, NDC |
| Medication Allergies | 4 | RxNorm, SNOMED |
| Laboratory Tests | 4 | LOINC |
| Laboratory Information | 5 | — |
| Laboratory value(s)/result(s) | 5 | LOINC |
| Vitals | 2 | LOINC |
| Goal | 3 | — |
| Procedures | 2 | CPT-4, SNOMED, HCPCS |
| Care team member(s) | 3 | — |
| Reason for Referral | 1 | SNOMED |
| Medical Equipment | 2 | SNOMED, GMDN |
| Mental Status | 4 | SNOMED |
| Functional Status | 4 | SNOMED |
| Health Concern | 3 | SNOMED |
| **Total** | **82** | **13 unique** |

### FHIR API (not part of the primary export)

The FHIR API at fhir-api.ethizo.com documents 47 resource-type folders covering standard US Core R4 resources (Patient, AllergyIntolerance, Condition, Coverage, CarePlan, CareTeam, Device, DiagnosticReport, DocumentReference, Goal, Immunization, MedicationRequest, MedicationDispense, Procedure, ServiceRequest, various Observations, Organization, Practitioner, Provenance, Location, Specimen, RelatedPerson, Encounter). There are **no billing resources** (Claim, ExplanationOfBenefit, Invoice), **no scheduling resources** (Appointment, Schedule), and **no custom or vendor-specific EHI resources**. This is the (g)(10) API, not a dedicated (b)(10) mechanism.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export has four components:

1. **CDA Clinical Data** (strongest): 24 sections covering the standard CDA clinical summary — demographics, encounters, diagnoses, medications, allergies, labs, vitals, immunizations, procedures, care plans, goals, referrals, implantable devices, mental/functional status, and health concerns. This is comprehensive *for a clinical summary* but inherently limited to what CDA can represent.

2. **Demographics/Insurance CSV**: Mentioned but completely undocumented. The PDF says it provides a "comprehensive view of demographics and insurance details" — this could be 5 fields or 50; we cannot tell.

3. **Appointments CSV**: Explicitly limited to "future appointments." No field documentation. Historical visit data would only appear in the CDA encounters section.

4. **Documents**: Scanned/uploaded files organized by patient chart number with category subfolders. This captures the document layer (signed notes, lab reports, radiology, scanned receipts) but as unstructured files, not as structured data.

The export is essentially **a C-CDA clinical summary plus a document dump plus two undocumented CSV files.** There is no native database export.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | CDA: 6 elements (name, sex, DOB, race, ethnicity, language). CSV: "demographics" but zero field documentation. | CDA covers USCDI minimum. CSV likely adds more fields but is undocumented — can't verify. |
| Encounters / visits | ✅ Covered | CDA Encounters section: code, performer, diagnosis, location, date (5 elements; CPT + SNOMED + ICD-10) | Standard encounter summary. Lacks encounter-level notes or detailed visit data. |
| Problems / conditions | ✅ Covered | CDA Problems section: problem, status, active date (3 elements; SNOMED + ICD-10). Also Health Concerns (3 elements). | Adequate for problem list. |
| Medications / prescriptions | ✅ Covered | CDA Medications: medication, directions, start/end date, status (5 elements; RxNorm + NDC) | Covers medication list. Does not specifically address ePrescription records, PDMP query results, or controlled substance prescribing details. |
| Allergies | ✅ Covered | CDA Medication Allergies: substance, reaction, severity, status (4 elements; RxNorm + SNOMED) | Adequate. |
| Immunizations | ✅ Covered | CDA Immunizations: 9 elements including vaccine, route, site, manufacturer, dose, lot number (CVX + CPT-4 + SNOMED) | Thorough for immunizations. |
| Vitals | ⚠️ Partial | CDA Vitals: observation, date (2 elements; LOINC) | Standard vital signs. Does **not** address high-granularity RPM device data (continuous glucose, cellular BP readings, ECG). Product has extensive RPM module — significant gap. |
| Lab results | ✅ Covered | CDA Labs: 3 sub-sections with 14 total elements (test code, lab info, results with reference ranges; LOINC) | Comprehensive lab results coverage. |
| Imaging / diagnostic reports | ⚠️ Partial | Documents folder may contain radiology reports as scanned files. CDA has no dedicated imaging section beyond what's captured as lab/diagnostic. | Unstructured document capture only. No structured radiology data. |
| Procedures | ✅ Covered | CDA Procedures: procedure, date (2 elements; CPT-4 + SNOMED + HCPCS) | Basic procedure list. |
| Clinical notes / documents | ✅ Covered | Documents component: signed progress notes, lab results, radiology reports as PDF/JPG/PNG organized by category subfolders | Document capture is good. Notes are unstructured files, not structured note data. |
| Care plans / goals | ✅ Covered | CDA Treatment Plan (2 elements; LOINC) + Goal (3 elements) + Care team (3 elements) | Basic care plan data. CCM module care plans are not specifically addressed. |
| Orders / referrals | ⚠️ Partial | CDA Reason for Referral (1 element; SNOMED). Treatment Plan includes pending tests and referrals. | Referral reason only — no order details, no order status, no structured referral documents. |
| Insurance / coverage | ⚠️ Partial | CSV: "insurance details" mentioned but **zero field documentation**. FHIR Coverage resource exists in API. | Insurance data likely present in CSV but impossible to assess depth or completeness without field documentation. |
| Claims / billing | ❌ Not covered | **No billing entities anywhere in the export.** No claims, charges, ERA, payment records, or billing transaction data. | **Critical gap.** Product has full PMS with claims scrubbing, ERA posting, eligibility verification, copay collection, PCI payments, revenue KPIs. None exported. |
| Payments | ❌ Not covered | No payment data in export. | Product processes PCI-compliant payments and copay collection. Not exported. |
| Consents / directives | ❌ Not covered | No consent or advance directive data in export. | Unknown whether product stores structured consent data. |
| Patient communications / portal messages | ❌ Not covered | No secure messaging data in export. | Product has patient portal with secure messaging. Not exported. |
| Specialty-specific (PALTC/behavioral health/wound care) | ❌ Not covered | No specialty-specific clinical data beyond standard CDA sections. | Product targets 20+ specialties including behavioral medicine, psychiatry, wound care, geriatrics, palliative care. Specialty assessments and workflows are not represented. |

**Summary**: Of 18 applicable domains, 7 are covered, 5 are partially covered, and 6 are not covered at all.

## 6. Documentation Quality

**Strengths**:
- The CDA data dictionary provides XPATH paths and OID code system identifiers for each element, enabling a developer to parse the CDA output
- Export process instructions are clear with step-by-step descriptions for both single-patient and bulk workflows
- Code systems are properly identified with standard OIDs

**Weaknesses**:
- **CSV exports are completely undocumented** — no field names, data types, value sets, or examples for the demographics/insurance and appointments files. A developer would have to reverse-engineer these from actual exports.
- **No sample data** — no example CDA documents, CSV files, or export ZIPs are provided
- **No machine-readable schemas** — no XSD, JSON Schema, or other parseable artifact
- **No field descriptions** — CDA element names are listed but not defined
- **No relationship documentation** — how the CDA, CSV, and document components relate to each other is unstated
- **FHIR Bulk Data is a single sentence** with zero implementation detail
- **No data types documented** for any export component

A developer could parse the CDA output using the XPATH mappings and standard CDA knowledge, but the CSV files would require trial-and-error, and there is no way to import billing or specialty data because it's not exported at all.

## 7. Overall Assessment

### Classification

**Standard-based projection**

The export is fundamentally a C-CDA clinical summary supplemented with two undocumented CSV files and a document dump. The CDA component covers what C-CDA was designed for — clinical summaries — but cannot and does not represent the product's billing data, specialty workflows, RPM data, telemedicine records, patient portal messages, or CCM activities. The vendor has also pointed to their standard US Core FHIR API as a (b)(10) pathway, but that API contains no billing or specialty resources either. This is a clinical summary repackaged as an EHI export, not a comprehensive native data model export.

### Key Findings

1. **The entire EHI export documentation is a single 9-page PDF.** There are no sample data files, no machine-readable schemas, and no supplementary artifacts. (Source: `files.json`, `EHI-Export-b.10-Documentation-v2.pdf`)

2. **Billing and financial data are completely absent.** The product has a full Practice Management System with claims, ERA posting, eligibility verification, copay collection, PCI payments, and revenue cycle KPIs — none of which appears in the export documentation. This is the most significant EHI gap. (Source: product-research.md for PMS features; PDF for export content)

3. **The CDA data dictionary is reasonably detailed for what it covers** — 24 sections, 82 elements, 13 code systems with XPATH paths and OIDs — but it only covers standard CDA clinical summary content. (Source: `EHI-Export-b.10-Documentation-v2.pdf` pages 4–8; `analysis/cda_dictionary_analysis.json`)

4. **Two CSV export components have zero field documentation.** The demographics/insurance and appointments CSVs are described only as "CSV, comma-separated" with no field names, types, or value sets. (Source: `EHI-Export-b.10-Documentation-v2.pdf` page 8)

5. **Multiple product modules are invisible in the export**: RPM (remote patient monitoring), CCM (chronic care management), Vezo (telemedicine), patient portal messaging, eFax document management, and IVR call data all generate patient-specific data that is not addressed in the export documentation.

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA R2.1 XML + CSV + PDF/JPG/PNG documents
Model type:      Standard projection (CDA), not native database
Entities:        24 CDA sections + 2 undocumented CSV files + document folder
Fields:          82 CDA data elements (CSV fields unknown)
Descriptions:    0% (element names only, no definitions)
Sample data:     No
Bulk export:     Yes
Domains covered: 7 of 18 applicable domains fully covered; 5 partial; 6 missing
```

### Bottom Line

The ethizo EHR export is a C-CDA clinical summary with minimal supplementary CSV files and scanned documents. It covers standard clinical data adequately but completely omits billing/financial data from the product's full Practice Management System, as well as data from RPM, telemedicine, CCM, and patient portal modules. A patient requesting their complete EHI would receive their clinical summary and uploaded documents but would miss all billing records, device-sourced vitals, secure messages, and specialty-specific data. The biggest gap is the total absence of billing and financial data from a product that operates a comprehensive revenue cycle management system.
