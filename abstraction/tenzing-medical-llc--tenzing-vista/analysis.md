# EHI Export Analysis: Tenzing Medical LLC

**Product**: Tenzing VistA  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.02.05.2936.TENZ.01.01.1.220120 (CHPL ID 10799)

## 1. Product Context

Tenzing VistA is an adaptation of the U.S. Department of Veterans Affairs' open-source VistA EHR, customized for community hospital use by Tenzing Medical LLC. The company is tightly coupled with Oroville Hospital, a 133-bed non-profit acute care facility in Northern California — likely its sole customer. The product runs on a FOSS Linux/YottaDB stack with the CPRS clinical interface.

**Clinical data the product stores:** Patient demographics, problem lists, medications (inpatient and outpatient, including ePrescribing via Surescripts), allergies, vital signs, lab results (interfaced with Sunquest lab system covering chemistry, microbiology, pathology, blood bank, cytology), radiology/imaging orders and results, clinical notes (progress notes, discharge summaries), CPOE orders, consult tracking, surgical records, dietary/nutrition orders, immunizations, clinical images and scanned documents (VistA Imaging), encounter/visit data, and scheduling/appointment data.

**Custom applications:** Real-time patient dashboard, pediatric growth charts, flow sheets (anesthesia, obstetrical, infusion center), centralized bed control, and a custom scheduling GUI.

**Billing/financial:** VistA includes an Integrated Billing module, but Oroville Hospital uses McKesson Series as a separate billing system. Whether billing data resides in VistA, Series, or both is unclear from product research.

**Patient portal:** Bridge Patient Portal (previously HealtheMe).

This product is a full-scope hospital EHR with both inpatient and ambulatory capabilities, meaning a complete EHI export should cover clinical, pharmacy, billing, and administrative patient data.

## 2. Artifacts Reviewed

| Artifact | Source | Description | Informativeness |
|---|---|---|---|
| `TenzingEHIFormatInfo.pdf` | http://tenzingmedical.com/TenzingEHIFormatInfo.pdf (registered (b)(10) URL) | 3-page PDF (102,594 bytes, created 2023-11-14). Lists 29 C-CDA sections exported by VistA and 4 McKesson Series data sections. Section-level documentation only — no field-level detail. | **Primary artifact** — defines what the export contains |
| `ElectronicHealthInformationExport.pdf` | http://tenzingmedical.com/ElectronicHealthInformationExport.pdf | 4-page PDF (114,026 bytes, created 2023-07-10). User guide for running exports via two VistA menu options. Includes screenshots of terminal interface and Taskman scheduling parameters. | **Moderate** — explains export mechanics but no data content |

Total documentation: **2 PDFs, 7 pages combined**. No data dictionary, no sample data, no schema artifacts, no JSON/XML/XLSX files.

## 3. Export Mechanics

The export uses a **dual-system approach**:

**Tenzing VistA (clinical data):**
- **Format:** C-CDA R2.1 XML (USCDI v2)
- **Mechanism:** Two VistA menu options:
  - `VGTM EHI EXPORT` — interactive, runs at user's console. User selects hospital locations, encounter scope (latest/specific/date range), and export destination path.
  - `VGTM AUTO CCDA EXPORT` — scheduled batch via VistA's Taskman. Supports recurring exports (e.g., monthly) with configurable date ranges, location filters, and output paths. Task parameters use a pipe-delimited format: `M56|S3|shares/dataexport` (date range | location | path).
- **Granularity:** One XML document per patient. User selects which C-CDA sections to include.
- **Bulk export:** Yes — batch selection of multiple patients is supported, and scheduled recurring exports are available.
- **Access:** Users need `VGTM DP-EHI EXPORT` security key for interactive export; `#` Fileman Access and `XUTM SCHEDULE` menu option for scheduled exports. No developer assistance required (`ElectronicHealthInformationExport.pdf`, p. 4).
- **Fees:** Not mentioned.

**McKesson Series (billing/financial data):**
- **Format:** "Structured delimited format" — delimiter, encoding, and schema are not specified.
- **Mechanism:** Not described beyond "Users can export Series data by individual patients or by batch selection."
- **Bulk export:** Yes — batch selection with date ranges supported.
- **No operational documentation** for the Series export was provided (no screenshots, no menu paths, no user guide).

## 4. Export Content: What's In It

The documentation provides **section-level enumeration only** — no field-level detail for either system. There are no sample data files, no machine-readable schemas, and no data dictionary beyond section names and one-line descriptions.

### VistA C-CDA Sections (29 sections)

The format specification (`TenzingEHIFormatInfo.pdf`) lists 29 C-CDA sections, each identified by an HL7 template ID (or XPath for Care Team). 28 sections have template IDs; Discharge Diagnosis is listed without one.

| Section | Template ID | Description |
|---|---|---|
| Care Team | XPath: /ClinicalDocument/.../performer | Ordering providers, clinical care team |
| Problems | 2.16.840.1.113883.10.20.22.2.5.1 | Clinical problem list |
| Vitals | 2.16.840.1.113883.10.20.22.2.4.1 | Vital signs (blood pressure, heart rate, pulse, blood ox, etc.) |
| Medications | 2.16.840.1.113883.10.20.22.2.1.1 | Active and pertinent medication history |
| Admission Medications | 2.16.840.1.113883.10.20.22.2.44 | Medications administered during an inpatient stay |
| Ambulatory Medications | 2.16.840.1.113883.10.20.22.2.38 | Medications administered during a clinical visit |
| Discharge Medications | 2.16.840.1.113883.10.20.22.2.11.1 | Medications ordered upon discharge |
| Allergies and Intolerances | 2.16.840.1.113883.10.20.22.2.6.1 | Active and pertinent allergy list |
| Social History / Smoking Status | 2.16.840.1.113883.10.20.22.2.17 | Relevant social history and smoking status |
| Assessments | 2.16.840.1.113883.10.20.22.2.8 | Impressions/diagnoses guiding treatment |
| Encounter Diagnosis | 2.16.840.1.113883.10.20.22.2.22.1 | Diagnoses at close of visit w/ location and timeframes |
| Procedures | 2.16.840.1.113883.10.20.22.2.7.1 | Interventional, surgical, diagnostic, and therapeutic procedures |
| Diagnostic Results | 2.16.840.1.113883.10.20.22.2.3.1 | Laboratory, radiological, and procedural results |
| Plan of Treatment | 2.16.840.1.113883.10.20.22.2.10 | Pending orders, interventions, encounters, services |
| Immunizations | 2.16.840.1.113883.10.20.22.2.2.1 | Current and pertinent immunization history |
| Reason For Referral | 1.3.6.1.4.1.19376.1.5.3.1.3.1 | Notes related to outside referrals |
| Chief Complaint | 2.16.840.1.113883.10.20.22.2.13 | Patient's own description of complaint |
| Admit Diagnosis | 2.16.840.1.113883.10.20.22.2.43 | Diagnosis at time of inpatient admission |
| Discharge Diagnosis | *(not listed)* | Diagnosis at time of inpatient discharge |
| Instructions | 2.16.840.1.113883.10.20.22.2.45 | Provider notes directed to the patient |
| Functional Status | 2.16.840.1.113883.10.20.22.2.14 | Observations/assessments of physical abilities |
| Mental Status | 2.16.840.1.113883.10.20.22.2.56 | Psychological and mental competency evaluations |
| Notes | 2.16.840.1.113883.10.20.22.2.65 | Free text based clinical documentation |
| Discharge Instructions | 2.16.840.1.113883.10.20.22.2.41 | Instruction at discharge |
| Medical Equipment | 2.16.840.1.113883.10.20.22.2.23 | Implanted and external medical devices |
| Health Concerns | 2.16.840.1.113883.10.20.22.2.58 | SDOH-related conditions |
| Goals | 2.16.840.1.113883.10.20.22.2.60 | Outcome/condition to be achieved in patient care |
| Payers/Insurance | 2.16.840.1.113883.10.20.22.2.18 | Insurance and payer information |
| Family History | 2.16.840.1.113883.10.20.22.2.15 | Genetic relatives' health risks/factors |

These are standard C-CDA sections. No vendor-specific extensions or custom sections are documented. The data elements within each section follow the C-CDA R2.1 specification — a developer would need to consult the HL7 standard to know what fields exist within each section.

### McKesson Series Sections (4 sections)

| Section | Path | Description |
|---|---|---|
| Patient | /Patient | Patient demographics |
| Payer/Insurance | /Patient/Payer | Insurance, payer information |
| Enrollment/Account Information | /Patient/Account | Enrollment, account information |
| Billing History | /Patient/Billing | Billing history, adjudication, etc. |

The Series export is described at an extremely high level — 4 section names with single-sentence descriptions. No fields, no schema, no delimiter specification, no sample data. A recipient could not parse or import this data from the documentation alone.

### Documentation gaps

- **Field count:** N/A — no field-level documentation exists for either system. The number of individual data fields exported is unknown.
- **Types:** Not documented (C-CDA types are implicit from the standard; Series types are completely undocumented).
- **Relationships:** Not documented — no explanation of how VistA clinical data relates to Series billing data for the same patient.
- **Value sets/code systems:** Not documented — C-CDA sections would use standard terminologies (SNOMED CT, LOINC, RxNorm, etc.) but the specific value sets are not specified.
- **Sample data:** None provided.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor organizes their export into two systems with distinct content:

**Tenzing VistA (29 C-CDA sections):** Covers a broad range of clinical data. The 29 sections extend well beyond a minimal USCDI export — notable inclusions are Mental Status, Functional Status, Health Concerns (SDOH), Medical Equipment, multiple medication contexts (admission/ambulatory/discharge), Notes (free-text clinical documentation), Family History, and Goals. This represents a thorough C-CDA clinical export within the constraints of what C-CDA can express.

However, all content is constrained to what C-CDA R2.1 sections can represent. VistA's internal FileMan database stores data in hundreds of files with complex cross-references that don't map cleanly to C-CDA's ~29 standardized sections. The export is a *projection* of VistA's rich data model into a clinical document standard, not a native database export.

**McKesson Series (4 sections):** The billing export addresses a domain most C-CDA-only vendors miss entirely. However, the documentation is so thin (4 section names, no field definitions) that it's impossible to assess depth. "Billing history, adjudication, etc." could mean detailed claim line items or could mean high-level account summaries — the documentation doesn't say.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA header elements; Series `/Patient` section | C-CDA carries basic demographics in the header. Series has a separate Patient section. No field-level detail to confirm completeness. |
| Encounters / visits | ⚠️ Partial | Encounter Diagnosis section includes "visit location and timeframes" | Encounter context is embedded in section data, not a standalone export. ADT details (admission/discharge/transfer tracking) not explicitly covered. |
| Problems / conditions / diagnoses | ✅ Covered | Problems, Assessments, Encounter Diagnosis, Admit Diagnosis, Discharge Diagnosis (5 sections) | Well-represented across multiple diagnostic contexts. |
| Medications / prescriptions | ✅ Covered | Medications, Admission Medications, Ambulatory Medications, Discharge Medications (4 sections) | Strong — separate sections for each medication context. However, pharmacy-specific data (controlled substance tracking, ePrescribing transmission details, formulary decisions) may not be captured in standard C-CDA medication sections. |
| Allergies | ✅ Covered | Allergies and Intolerances section | Standard C-CDA coverage. |
| Immunizations | ✅ Covered | Immunizations section | Standard C-CDA coverage. |
| Vitals | ✅ Covered | Vitals section | Standard C-CDA coverage. |
| Lab results | ⚠️ Partial | Diagnostic Results section ("laboratory, radiological, and procedural results") | C-CDA can carry lab results, but VistA interfaces with Sunquest for a full-service lab (chemistry, microbiology, pathology, blood bank, cytology). Unclear whether granular Sunquest-sourced results are fully captured in C-CDA or just summaries. |
| Imaging / diagnostic reports | ⚠️ Partial | Diagnostic Results section; VistA Imaging not mentioned | Radiological results are mentioned in Diagnostic Results, but VistA Imaging (clinical images, scanned documents) is not addressed. Images and scanned documents in the patient record are EHI. |
| Procedures | ✅ Covered | Procedures section | Covers "interventional, surgical, diagnostic, and therapeutic procedures." Operative notes and detailed surgical records may be partially captured via Notes section. |
| Clinical notes / documents | ✅ Covered | Notes section (free text clinical documentation), plus Assessments, Instructions, Chief Complaint, Reason For Referral | The Notes section (template 2.16.840.1.113883.10.20.22.2.65) covers free-text documentation. |
| Care plans / goals | ✅ Covered | Plan of Treatment, Goals, Health Concerns sections | Good coverage across care planning domains. |
| Orders / referrals | ⚠️ Partial | Plan of Treatment ("pending orders, interventions, encounters, services"), Reason For Referral | Orders are partially covered via Plan of Treatment. However, VistA's CPOE generates detailed order data (medication orders, lab orders, radiology orders, diet orders, consults) that C-CDA may not fully represent. |
| Insurance / coverage | ✅ Covered | Payers/Insurance (VistA C-CDA), Payer/Insurance (Series) | Covered in both systems. |
| Claims / billing | ⚠️ Partial | Series Billing History ("/Patient/Billing — billing history, adjudication, etc."), Series Enrollment/Account Information | Billing is explicitly addressed via Series, which is better than most vendors. However, zero field-level documentation means actual coverage depth is unverifiable. |
| Payments | ⚠️ Partial | Series introductory text mentions "payment" as a Series data type | Payment is mentioned in the overview text ("patient account, billing, payment, adjudication, and payer information") but has no dedicated section. May be included in Billing History. |
| Consents / directives | ❌ Not covered | No section for advance directives or consent documents | VistA stores advance directives; this is a gap. |
| Patient communications / portal messages | ❌ Not covered | No section for patient portal messages | Product uses Bridge Patient Portal. Portal message data is not addressed. |
| Specialty-specific (custom VistA applications) | ❌ Not covered | No mention of custom app data | Product has custom flow sheets (anesthesia, obstetrical, infusion center), pediatric growth charts, and other custom apps. Data from these custom modules is not addressed in the C-CDA export. |

## 6. Documentation Quality

**Overall quality: Thin.** Two PDFs totaling 7 pages for a dual-system export spanning clinical and financial data.

**Strengths:**
- C-CDA template IDs provided for 28 of 29 sections — a developer with C-CDA expertise can identify the expected data elements from the HL7 standard
- Clear, practical user guide with VistA terminal screenshots for running exports
- Both interactive and scheduled batch export mechanisms are documented with parameter syntax
- Security/access requirements are documented

**Weaknesses:**
- **No field-level documentation whatsoever** — the documentation lists section names but not the data elements within each section
- **No sample export files** — no example C-CDA XML or Series delimited files
- **No machine-readable schema** — no XSD, Schematron, JSON Schema, or any parseable artifact
- **McKesson Series export is barely documented** — 4 section names with one-line descriptions; no field definitions, no delimiter specification, no encoding, no operational instructions
- **No value set or terminology documentation** — which code systems (SNOMED, LOINC, RxNorm, ICD-10) are used in which sections is not specified
- **No relationship documentation** — how a patient's VistA clinical record connects to their Series billing record is not explained
- **No documentation of what VistA data is excluded** — VistA's FileMan database has hundreds of files; which ones are not represented in the C-CDA export is not addressed

**Could a developer build an import?** For the VistA C-CDA portion, a developer with C-CDA parsing experience could build a generic C-CDA importer using the template IDs. However, they'd be importing standard C-CDA, not Tenzing-specific data — any vendor extensions or VistA-specific data elements would be invisible. For the Series portion, a developer could not build an importer from the documentation alone — the format is completely unspecified.

## 7. Overall Assessment

### Classification

**Standard-based projection**

The clinical export is a C-CDA R2.1 projection of VistA's native FileMan database. C-CDA is a document standard designed for clinical care coordination summaries, not a comprehensive database export format. While the 29 sections represent broader-than-average C-CDA coverage, they inherently flatten VistA's rich hierarchical data model (hundreds of FileMan files with complex cross-references) into ~29 standardized document sections. The billing export from McKesson Series is too poorly documented to assess independently.

This is not a native database export — it's a clinical summary standard being used as the (b)(10) export vehicle. The approach is architecturally better than many vendors (dual-system, broad C-CDA section selection, batch capability), but it remains a projection rather than a comprehensive native export.

### Key Findings

1. **Dual-system approach is architecturally sound but under-documented.** Tenzing explicitly addresses billing data via McKesson Series alongside VistA clinical data — a design that recognizes EHI includes financial records. Most C-CDA-only vendors miss this entirely. However, the Series export has essentially zero technical documentation (4 section names, no fields, no schema).

2. **29 C-CDA sections represent broad clinical coverage within C-CDA's constraints.** The inclusion of Mental Status, Functional Status, Health Concerns (SDOH), Medical Equipment, Goals, and multiple medication contexts goes well beyond a minimal USCDI export. (`TenzingEHIFormatInfo.pdf`, pp. 1-3)

3. **No field-level documentation exists.** The entire export documentation consists of section names and one-line descriptions — no individual data elements, no types, no value sets, no relationships. Total field count: unknown. (`TenzingEHIFormatInfo.pdf`)

4. **Custom VistA data is not addressed.** Tenzing/Oroville Hospital has custom applications (anesthesia flow sheets, obstetrical flow sheets, pediatric growth charts, infusion center data) that generate patient-specific clinical data stored in VistA. None of this data is mentioned in the export documentation — it presumably cannot be represented in standard C-CDA sections.

5. **VistA Imaging data is absent.** The product includes VistA Imaging for clinical images and scanned documents, which are part of the designated record set. No export mechanism for images is documented.

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA R2.1 XML (clinical) + proprietary delimited format (billing)
Model type:      Standard projection (C-CDA) + proprietary (Series)
Entities:        33 sections (29 VistA C-CDA + 4 McKesson Series)
Fields:          N/A (no field-level documentation)
Descriptions:    100% of sections have one-line descriptions; 0% field-level
Sample data:     No
Bulk export:     Yes (both interactive batch and scheduled recurring)
Domains covered: 9 of 16 applicable domains fully or partially covered
```

### Bottom Line

Tenzing VistA's EHI export is a C-CDA clinical summary plus a minimally documented billing system export — better than many small vendors (it acknowledges billing data exists and provides batch export capability), but still a standard-based projection rather than a native database export. The biggest gap is the complete absence of field-level documentation: with 7 pages total and zero field definitions, a recipient cannot fully understand, validate, or import the exported data without independent knowledge of C-CDA and reverse-engineering of the Series format.
