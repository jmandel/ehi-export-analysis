# EHI Export Analysis: Theoria Medical, PLLC

**Product**: ChartEasy™ v1.5
**Analysis date**: 2026-02-15
**CHPL ID**: 15.04.04.3091.Char.01.01.1.241204 (CHPL listing 11542)

## 1. Product Context

ChartEasy™ is a proprietary, cloud-based EHR built by Theoria Medical, PLLC for internal use by its own clinicians — physicians, nurse practitioners, and physician assistants — who provide attending physician services, medical directorship, telemedicine, chronic care management (CCM), and remote patient monitoring (RPM) at skilled nursing facilities (SNFs) and other senior living communities across 21 states. ChartEasy is **not sold commercially** to external healthcare organizations; it is an internal-use physician EHR that integrates bidirectionally with facility EHR systems (PointClickCare, MatrixCare, American HealthTech).

The product was certified recently (December 4, 2024) with 34 certification criteria and 10 CQMs.

**Data domains ChartEasy stores** (per product documentation and certification profile):
- Patient demographics (received from facility EHR integrations)
- ADT (admission/discharge/transfer) records
- Physician progress notes and encounter documentation
- Medication lists and reconciliation data
- Vital signs (manual and from RPM devices — heart rate, respiration, SpO2, motion)
- Lab results (from laboratory integrations)
- Imaging results (integration with imaging companies mentioned)
- Diagnoses/problem lists
- Implantable device information (certified for (a)(14))
- Clinical decision support alerts and ProphEasy return-to-hospitalization (RTH) predictions
- Care plans (CCM care plans)
- Scheduling data (automated regulatory-compliant visit scheduling)
- Secure messaging data (ChatEasy messages between clinicians and facility staff)
- RPM device data streams

**Billing/claims**: The website does not explicitly describe billing or claims management within ChartEasy, though CPT and HCPCS terminologies are supported. Billing may be handled through a separate system.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/ehr-certificate-page.html` (16,621 bytes) | ONC certification page containing the (b)(10) attestation statement, certification criteria list, and Real-World Testing PDF links. **This is the entirety of the vendor's EHI export documentation.** | **Primary artifact** — the only source of (b)(10) information |
| `downloads/ehr-certificate-page-full.png` (1,075,299 bytes) | Full-page screenshot of the ONC certification page | Confirms HTML content visually; shows certification badges and page layout |
| `downloads/patient-portal-login.png` (364,356 bytes) | Screenshot of the ChartEasy Patient Portal login page (Flutter web app v2.0.8) | Shows portal feature descriptions: CCM plans, lab/imaging results, medications, download/transmit records. Login-walled; no export documentation accessible. |

**Total downloadable artifacts**: 3 files (1 HTML page, 2 screenshots). No PDFs, no data dictionaries, no schemas, no sample data, no machine-readable artifacts of any kind related to EHI export.

The 6 PDF links on the certification page are all Real-World Testing Plans and Reports — regulatory filings unrelated to EHI export:
1. `TheorialMedical_Real_World_Test_Plan_CY2023_22Nov2022.pdf`
2. `TheorialMedical_Real_World_Test_Plan_CY2024_19Oct2023.pdf`
3. `TheoriaMedical_Real_World_Test_Results_CY2023_26Jan2024.pdf`
4. `TheoriaMedical_Real_World_Test_Results_CY2024_26Feb2025.pdf`
5. `TheorialMedical_Real_World_Test_Plan_CY2025_07Oct2024.pdf`
6. `TheoriaMedical_Real_World_Test_Results_CY2025_03Feb2026.pdf`

**Verification of prior report claims**:
- Prior report states developer.charteasy.com times out — **confirmed**: curl returns empty response with no HTTP headers (connection fails).
- Prior report states patient portal returns HTTP 200 — **confirmed**: HTTP 200, Content-Length 3,405 bytes, Flutter web app.
- Prior report states EHR certificate page returns HTTP 200 — **confirmed**: HTTP 200, 16,621 bytes.
- Prior report states the (b)(10) statement is ~150 words — **corrected**: the statement is 213 words (counted programmatically from the extracted text).

## 3. Export Mechanics

- **Format**: PDF and C-CDA (per attestation; no format specification provided)
- **Mechanism**: Two options described:
  1. **Patient Portal self-service**: Patients log in at https://patient-portal.charteasy.com/ (or iOS app) and download records
  2. **Email request**: Patients email records@theoriamedical.com for record retrieval
- **Single-patient vs bulk**: Single-patient only (patient portal is individual-access; email request is per-patient). No bulk export mechanism described.
- **Access constraints**: Patient portal requires authentication. No documentation of provider-initiated bulk export.
- **Fees**: Not mentioned.

The attestation describes only patient-facing access. There is no documentation of an administrative or provider-initiated export mechanism for bulk EHI export as contemplated by (b)(10).

## 4. Export Content: What's In It

**There is no data dictionary, schema, or structured documentation of what the export contains.** The entirety of the vendor's content specification is the phrase "Records may be exported as both PDF and CCDA format."

### What can be inferred

The patient portal login page describes four feature areas:
1. **Access Chronic Care Management Plan** — CCM plans with goals, medications, lab results
2. **View Lab and Imaging Results** — real-time lab and imaging results
3. **View Medication Lists** — active medications
4. **Download and Transmit your records** — "complete and full access to your personal records"

The portal's "download and transmit" capability is the (e)(1) view/download/transmit function, which typically produces a C-CDA clinical summary (CCD or Continuity of Care Document). This is being presented as the (b)(10) EHI export.

### Vendor's own content organization

No content organization exists. The vendor provides zero structured documentation of what is included in the export. There are:
- **0 entities/tables** documented
- **0 fields** documented
- **0 field descriptions**
- **0 type specifications**
- **0 value sets**
- **0 relationship/foreign key definitions**
- **0 sample data files**
- **0 machine-readable schemas**

A complete inventory is saved at `analysis/full-entity-inventory.json` (which is necessarily empty since no data dictionary exists).

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's documentation covers nothing in structured terms. The attestation says exports are in "PDF and CCDA format" but does not specify:
- Which C-CDA document type(s) are used
- Which C-CDA sections are populated
- What data elements appear in the PDF
- Whether the PDF and C-CDA contain the same information
- Which data domains from ChartEasy are included
- Which data domains are excluded and why

Based solely on the patient portal feature descriptions, the export likely includes the patient-portal-visible subset: lab results, vital signs, current medications, CCM care plans, and signed clinical encounters. This appears to be a standard (e)(1) clinical summary, not a comprehensive (b)(10) EHI export.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial (inferred) | No documentation; likely in C-CDA header | ChartEasy receives demographics from facility EHRs; C-CDA typically includes basic demographics but coverage depth is unknown |
| Encounters / visits | ⚠️ Partial (inferred) | Portal mentions "signed encounters" (added v2.0.4) | Progress notes are a core function; C-CDA may include encounter sections but completeness is undocumented |
| Problems / conditions / diagnoses | ⚠️ Partial (inferred) | No documentation; likely in C-CDA if present | ChartEasy manages diagnoses; standard C-CDA includes problem list but vendor-specific coverage unknown |
| Medications / prescriptions | ⚠️ Partial (inferred) | Portal lists "View Medication Lists" | Medication reconciliation is a core feature; C-CDA typically includes medications but reconciliation history unlikely |
| Allergies | ⚠️ Partial (inferred) | No documentation; may be in C-CDA | Standard C-CDA section; unclear if populated |
| Immunizations | ❌ Not covered (inferred) | No evidence | Not a core ChartEasy function for SNF physician workflows; likely N/A |
| Vitals | ⚠️ Partial (inferred) | Portal mentions lab/vital results | ChartEasy stores manual vitals + RPM device data; C-CDA may include vitals but RPM streams almost certainly excluded |
| Lab results | ⚠️ Partial (inferred) | Portal mentions "View Lab and Imaging Results" | Lab integrations are bidirectional; C-CDA likely includes some lab results |
| Imaging / diagnostic reports | ⚠️ Partial (inferred) | Portal mentions "Imaging Results" | Integration with imaging companies mentioned; unclear what's in export |
| Procedures | ❌ Not covered (inferred) | No evidence | May not be a primary ChartEasy function in SNF context |
| Clinical notes / documents | ⚠️ Partial (inferred) | Portal mentions signed encounters | Progress notes are ChartEasy's core function; PDF may include notes but no documentation |
| Care plans / goals | ⚠️ Partial (inferred) | Portal mentions "Access Chronic Care Management Plan" | CCM care plans are a core feature; may appear in C-CDA or PDF |
| Orders / referrals | ❌ Not covered (inferred) | No evidence | CPOE is certified (a)(1); orders data likely exists but no evidence it's exported |
| Insurance / coverage | ❌ Not covered | No evidence | Unclear if ChartEasy stores insurance data |
| Claims / billing | ❌ Not covered | No evidence | Unclear if billing is in ChartEasy or separate system; if in ChartEasy, this is a gap |
| Payments | ❌ Not covered | No evidence | Unclear if ChartEasy handles payments |
| Consents / directives | ❌ Not covered | No evidence | May be managed at facility level, not in ChartEasy |
| Patient communications / portal messages | ❌ Not covered | No evidence | ChatEasy secure messaging exists but no evidence it's in the export |
| RPM device data | ❌ Not covered | No evidence | ChartEasy stores RPM data (heart rate, SpO2, respiration, motion); C-CDA cannot represent continuous device data streams; significant gap if not exported separately |
| Clinical decision support data | ❌ Not covered | No evidence | ProphEasy RTH predictions are stored; no standard format for this data; not in export |

**Important caveat**: Every "Partial (inferred)" rating above is based solely on what standard C-CDA documents typically include, not on any vendor documentation. The vendor provides **zero evidence** of what is actually in the export. The true coverage could be better or worse than inferred.

## 6. Documentation Quality

The export documentation quality is **essentially non-existent**:

- **No data dictionary** of any kind
- **No field-level documentation**
- **No type specifications**
- **No value set or code system documentation**
- **No relationship/foreign key documentation**
- **No sample data or sample exports**
- **No machine-readable schemas** (XSD, JSON Schema, OpenAPI, etc.)
- **No C-CDA implementation guide** specifying which sections/templates are used
- **No description of what "EHI" includes** in the vendor's context

A developer could not build an import from this documentation. A patient cannot understand what is included in their export. A regulator cannot verify completeness. The only actionable information is: "you can get PDF and CCDA from the patient portal or by emailing records@theoriamedical.com."

The (b)(10) criterion requires the developer to "make publicly accessible" documentation "describing the format of the export." A 213-word attestation statement saying "PDF and CCDA format" does not satisfy this requirement in any meaningful sense.

## 7. Overall Assessment

### Classification

**Minimal/stub**: Documentation is too thin to assess what the export actually contains. The export appears to be the (e)(1) patient portal view/download/transmit capability (clinical summary in C-CDA) relabeled as the (b)(10) EHI export, with no documentation of scope or content.

### Key Findings

1. **The (b)(10) "documentation" is a 213-word prose attestation with zero technical content.** There is no data dictionary, no schema, no sample data, no format specification — nothing that describes what data is exported or how it's structured. (`downloads/ehr-certificate-page.html`)

2. **The export mechanism is the patient portal's (e)(1) view/download/transmit capability repackaged as (b)(10).** The attestation points to the same patient portal and the same PDF/C-CDA formats that satisfy the (e)(1) criterion. No separate bulk or comprehensive export mechanism is described.

3. **C-CDA cannot represent all of ChartEasy's data.** ChartEasy stores RPM device data streams (heart rate, respiration, SpO2, motion), ProphEasy clinical decision support predictions, ChatEasy secure messages, medication reconciliation history, and automated scheduling data — none of which map to standard C-CDA sections. A C-CDA export alone cannot be a complete (b)(10) EHI export for this product.

4. **No bulk export capability is documented.** The (b)(10) criterion requires the ability to export a single patient's data and to export data for a population. Only single-patient portal access and individual email requests are described.

5. **Recently certified product with minimal compliance effort.** ChartEasy was certified December 4, 2024, and is an internal-use EHR built by a physician group practice, not a commercial EHR vendor. The (b)(10) documentation appears to reflect the minimum effort to check a certification box rather than a genuine attempt to support comprehensive EHI export.

### Summary Stats

```
Classification:  Minimal/stub
Export format:   PDF and C-CDA (per attestation; no specification)
Model type:      Standard projection (C-CDA clinical summary)
Entities:        0 (no data dictionary)
Fields:          0 (no data dictionary)
Descriptions:    N/A
Sample data:     No
Bulk export:     No (single-patient portal access only)
Domains covered: 0 of 14 confirmed; ~7 of 14 inferred from standard C-CDA content (unverifiable)
```

### Bottom Line

A patient or provider requesting their data from ChartEasy would receive a PDF and/or C-CDA clinical summary via the patient portal or email — essentially the same clinical summary available through the (e)(1) view/download/transmit function. There is no evidence that this constitutes a comprehensive export of all electronic health information stored in ChartEasy. The single biggest gap is the complete absence of any documentation describing what the export contains — making it impossible to assess completeness, let alone build an import or verify that all EHI is included.
