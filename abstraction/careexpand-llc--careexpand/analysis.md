# EHI Export Analysis: Careexpand LLC

**Product**: Careexpand  
**Analysis date**: 2026-02-16  
**CHPL ID**: 15.04.04.3226.Care.24.00.1.250422

## 1. Product Context

Careexpand is a cloud-based, all-in-one healthcare platform combining EHR, telemedicine, remote patient monitoring (RPM), care coordination, and practice management. It is built by a small startup (1–10 employees) based in Plano, TX, and received ONC certification in April 2025. The product targets individual doctors, small clinics, and multi-provider groups in ambulatory/outpatient settings, with emphasis on primary care and chronic disease management.

**Relevant capabilities for export completeness assessment:**
- **EHR**: Patient demographics, clinical documentation, problem lists, medication lists, allergy lists, implantable device tracking, CPOE for medications
- **E-prescribing & Lab Orders**: Electronic prescribing, lab order integration via Change Healthcare/Optum
- **Telemedicine**: Video/phone consultations, virtual waiting rooms, multi-channel messaging
- **Care Coordination**: Referral management, follow-up protocols, care plans, transitions of care (C-CDA)
- **Remote Patient Monitoring**: Device readings for chronic conditions (diabetes, hypertension)
- **Practice Management**: Scheduling, billing (described as "automated billing solutions"), CQMs
- **Patient Portal**: Health information access, engagement campaigns, messaging

The billing capability is ambiguous — it may be limited to charge capture with claims flowing through the Change Healthcare/Optum integration ($65/mo add-on), rather than a full billing/claims system. Regardless, the product stores patient-level charge and billing data.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/b10-ehi-export-ccda.html` (68 KB) | BookStack HTML export of the single EHI export documentation page. Contains narrative text, API endpoint details, JSON response examples, and a link to the data dictionary image. No HTML tables with structured data. | **Primary source** — full documentation content |
| `downloads/b10-ehi-export-ccda.md` (11 KB) | BookStack Markdown export of the same page. Readable text version; data dictionary referenced as image link only. | Redundant with HTML; useful for text extraction |
| `downloads/b10-ehi-export-ccda.pdf` (1.3 MB) | PDF export of the documentation page. Data dictionary table is rendered as an embedded image, not extractable as text. 4 pages. | Redundant with HTML |
| `downloads/data-dictionary-table.png` (28 KB) | PNG image of the data dictionary table listing 17 fields. This is the **only** data dictionary provided — it is an image, not structured data. | **Critical artifact** — the entire data dictionary |
| `downloads/page-screenshot-full.png` (645 KB) | Full-page browser screenshot of the BookStack documentation page. | Confirms page layout; no new information |

**Most informative**: `data-dictionary-table.png` and `b10-ehi-export-ccda.html`  
**Least informative**: `page-screenshot-full.png` (redundant screenshot)

## 3. Export Mechanics

- **Format**: C-CDA 2.1 XML (.xml file)
- **Mechanism**: API call — `POST /patient/:idPatient/getPatientCCDAData`
- **Authentication**: JWT Bearer Token (JwtAuthGuard)
- **Single-patient only**: The API endpoint takes a single patient ID as a path parameter. No bulk export mechanism is documented.
- **Access**: Requires authenticated API access; no UI-based "download my data" button is documented
- **Request body**: `PatientCCDADTO` (contents not specified)
- **Response**: JSON wrapper containing `patientData` with `demographics`, `clinicalData`, and `monitors` sub-objects, plus a link to download the C-CDA XML file
- **Fees/constraints**: Not documented

## 4. Export Content: What's In It

The entire export documentation consists of a single API endpoint that produces a C-CDA 2.1 XML document. The data dictionary is provided exclusively as a PNG image (`data-dictionary-table.png`) containing 17 fields.

- **Entities/tables**: 1 (a single C-CDA document per patient)
- **Total fields**: 17
- **Fields with descriptions**: 17/17 (100%)
- **Fields with types**: 17/17 (100%)
- **Relationships/foreign keys**: None documented
- **Value sets/code systems**: None documented (gender noted as "M/F/Other" only)
- **Sample data**: None provided
- **Machine-readable schema**: None — the data dictionary is a PNG image

The documentation states: *"Additional fields may be included depending on the data available for the patient"* — this is the only acknowledgment that the export might contain more than the 17 documented fields, but no detail is given.

### Vendor's own content organization

The vendor does not organize content into categories. All 17 fields are presented in a single flat table:

| Field | Description | Data Type | Required |
|---|---|---|---|
| patient_name | Full name of the patient | String | Yes |
| dob | Date of birth of the patient | Date (YYYY-MM-DD) | Yes |
| gender | Patient's gender | String (M/F/Other) | Yes |
| race | Race of the patient | String | No |
| ethnicity | Ethnicity of the patient | String | No |
| language | Preferred language of communication | String | No |
| address | Patient's home address | String | No |
| phone | Contact number | String | No |
| emergency_contact | Emergency contact name and phone | String | No |
| smoking_status | Patient's smoking habits | String | No |
| problem_list | List of active and past medical problems | Array (Structured) | Yes |
| medications | Active and past medications | Array (Structured) | Yes |
| allergies | Patient allergies | Array (Structured) | No |
| lab_results | Laboratory test results | Array (Structured) | No |
| procedures | Medical procedures performed | Array (Structured) | No |
| encounters | Clinical encounters and visits | Array (Structured) | No |
| vital_signs | Blood pressure, heart rate, temperature, etc. | Array (Structured) | No |

Seven of these fields are typed as "Array (Structured)" but no sub-field documentation is provided — we do not know what elements a problem, medication, allergy, lab result, procedure, encounter, or vital sign record contains. The C-CDA 2.1 standard defines these sections, but the vendor provides no mapping from their internal data model to C-CDA elements, and no indication of which C-CDA optional elements are populated.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor documents a single C-CDA export containing exactly the data domains one would expect from a standard Continuity of Care Document:
- **Demographics** (10 fields): name, DOB, gender, race, ethnicity, language, address, phone, emergency contact, smoking status
- **Clinical summaries** (7 array fields): problems, medications, allergies, labs, procedures, encounters, vitals

This is precisely the content of a standard C-CDA CCD template — the same document used for transitions of care under criterion (b)(1). There is no evidence this export was built specifically for (b)(10). The API endpoint name itself (`getPatientCCDAData`) and the documentation title ("Patient Data via CCDA") confirm this is the vendor's existing C-CDA generation capability rebranded as EHI export.

The documentation has no mention of:
- Any data beyond standard C-CDA sections
- Billing, claims, or financial data
- Care plans, goals, or referrals
- Clinical notes or documents beyond what C-CDA sections carry
- Immunizations (a standard USCDI domain, notably absent)
- Remote patient monitoring data (despite being a key product feature)
- Telemedicine session records
- Patient portal communications
- E-prescribing details beyond the medications list
- Custom forms or specialty assessments
- Any vendor-specific extensions to C-CDA

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | 10 fields (name, DOB, gender, race, ethnicity, language, address, phone, emergency contact, smoking status) | Basic demographics present but thin — no patient ID, no marital status, no preferred pharmacy, no multiple addresses/phones. Smoking status is demographic here but clinically relevant. |
| Encounters / visits | ⚠️ Partial | `encounters` field (Array, no sub-fields documented) | Listed but no detail on what encounter data is included — dates? Types? Providers? Diagnoses? |
| Problems / conditions | ⚠️ Partial | `problem_list` field (Array, no sub-fields documented) | Listed but no sub-field detail. Standard C-CDA problem section likely includes code and description; unknown if onset dates, status, severity are included. |
| Medications / prescriptions | ⚠️ Partial | `medications` field (Array, no sub-fields documented) | Listed but undocumented sub-fields. Product has e-prescribing; unclear if prescription details (dosage, pharmacy, prescriber, refills) are exported. |
| Allergies | ⚠️ Partial | `allergies` field (Array, no sub-fields documented) | Listed, no detail on reaction types, severity, or coded allergens. |
| Immunizations | ❌ Not covered | Not listed in data dictionary | Standard USCDI domain missing. Product may store immunization data (certified for (b)(1) transitions of care which includes immunizations). |
| Vitals | ⚠️ Partial | `vital_signs` field (Array, no sub-fields documented) | Listed with note "blood pressure, heart rate, temperature, etc." but no detail on which vitals or sub-fields. |
| Lab results | ⚠️ Partial | `lab_results` field (Array, no sub-fields documented) | Listed but no detail on what lab data is included — codes, values, units, reference ranges, specimen info? |
| Imaging / diagnostic reports | ❌ Not covered | No mention | Unclear if product stores imaging data; no evidence of imaging in export. |
| Procedures | ⚠️ Partial | `procedures` field (Array, no sub-fields documented) | Listed but undocumented. |
| Clinical notes / documents | ❌ Not covered | No mention | Product has clinical documentation features; no notes section in export. |
| Care plans / goals | ❌ Not covered | No mention | Product is certified for (b)(11) care plans; care plan data not in export. |
| Orders / referrals | ❌ Not covered | No mention | Product has referral management and lab orders; not in export. |
| Insurance / coverage | ❌ Not covered | No mention | Product likely stores insurance information; not in export. |
| Claims / billing | ❌ Not covered | No mention | Product advertises "automated billing solutions"; billing data not in export. |
| Payments | ❌ Not covered | No mention | N/A or gap — billing capability unclear. |
| Consents / directives | ❌ Not covered | No mention | Unknown if product stores advance directives. |
| Patient communications | ❌ Not covered | No mention | Product has patient portal, multi-channel messaging; communications not in export. |
| Telemedicine records | ❌ Not covered | No mention | A core product feature; no telemedicine data in export. |
| Remote patient monitoring | ❌ Not covered | No mention | A core product feature (RPM); response JSON mentions `monitors` array but it's not in the data dictionary. |

**Notable**: The JSON response structure mentions a `monitors` array alongside `demographics` and `clinicalData`, suggesting the API may return RPM data, but this is not documented in the data dictionary and no detail is provided.

## 6. Documentation Quality

The documentation is **minimal and insufficient** for a developer to work with:

- **Data dictionary is an image**: The only structured field listing is a PNG image, not a table, not JSON, not any machine-readable format. A developer cannot programmatically parse or validate against it.
- **No sub-field documentation**: 7 of 17 fields are typed as "Array (Structured)" with zero documentation of their internal structure. For a C-CDA export, this means the vendor is relying entirely on the reader's knowledge of the C-CDA standard — but without specifying which optional C-CDA elements they populate, which code systems they use, or how their internal data maps to CDA entries.
- **No sample data**: No sample C-CDA XML file is provided. A developer cannot see what the output actually looks like.
- **No value sets**: Gender is listed as "M/F/Other" but no other coded fields have value set references.
- **No relationships**: No foreign keys, no entity relationships, no data model documentation.
- **Ambiguous scope**: The note "Additional fields may be included depending on the data available for the patient" hints at undocumented content but provides no specifics.
- **Single page**: The entire (b)(10) documentation is one BookStack page (4 PDF pages), including API mechanics and error codes. The actual data content documentation is a single image.

A developer could not build a reliable import from this documentation alone. They would need to make API calls and reverse-engineer the C-CDA output.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The export documents 17 top-level fields that map exactly to standard C-CDA CCD sections. No sub-field documentation is provided for the 7 clinical array fields. Entire product capabilities are absent from the export: telemedicine sessions, RPM data, care plans (despite (b)(11) certification), clinical notes, orders/referrals, billing, insurance, patient communications, and portal messages. The export covers demographics and a thin clinical summary — roughly the USCDI floor minus immunizations — while the product stores substantially more data across telemedicine, RPM, care coordination, billing, and patient engagement.

**Axis 2 — Export approach: Repackaged existing export**

This is clearly the vendor's existing C-CDA generation capability (used for (b)(1) transitions of care) relabeled as (b)(10) EHI export. Evidence:
1. The API endpoint is named `getPatientCCDAData` — a generic C-CDA endpoint, not an EHI-specific one
2. The data dictionary lists exactly the standard C-CDA CCD sections with no extensions
3. The format is C-CDA 2.1 — the same format used for transitions of care
4. There is no product-specific data dictionary, no mapping beyond standard C-CDA templates, and no coverage of billing, operational, or specialty data
5. The documentation makes no distinction between this export and a standard clinical summary

### Key Findings

1. **The export is a standard C-CDA document relabeled as (b)(10)**: The 17 documented fields map one-to-one to standard C-CDA CCD sections. No vendor-specific extensions, no non-USCDI data, no purpose-built EHI content. The API endpoint name (`getPatientCCDAData`) confirms this is existing functionality.

2. **The data dictionary is a PNG image with no sub-field detail**: The only field-level documentation is an image of a 17-row table. The 7 clinical fields are typed as "Array (Structured)" with zero documentation of their internal structure — no element names, no codes, no value sets.

3. **Major product capabilities are absent from the export**: Telemedicine (video/phone consultations), RPM (device readings), care plans (despite (b)(11) certification), clinical notes, orders, referrals, billing, and patient communications are all product features with no representation in the export.

4. **No sample data or machine-readable artifacts**: No sample C-CDA XML, no JSON schema, no structured data dictionary. Documentation is a single BookStack page.

5. **No bulk export capability**: The API exports one patient at a time via `POST /patient/:idPatient/getPatientCCDAData`. No batch or bulk export mechanism is documented.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Repackaged existing export
Export format:   C-CDA 2.1 XML
Entities:        1 (single C-CDA document)
Fields:          17 (top-level only; sub-fields undocumented)
Descriptions:    100% (17/17 have one-line descriptions)
Sample data:     No
Bulk export:     No
Domains covered: 8 of 17 applicable domains (all partial due to lack of sub-field documentation)
```

### Bottom Line

Careexpand's (b)(10) export is a standard C-CDA clinical summary rebranded as an EHI export. It covers basic demographics and 7 clinical summary sections (problems, medications, allergies, labs, procedures, encounters, vitals) with no sub-field documentation, while omitting entire product capabilities including telemedicine, RPM, care plans, clinical notes, orders, billing, and patient communications. A patient requesting their complete EHI would receive a clinical summary, not a comprehensive record export.
