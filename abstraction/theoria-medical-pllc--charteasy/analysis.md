# EHI Export Analysis: Theoria Medical, PLLC

**Product**: ChartEasy™ v1.5
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.3091.Char.01.01.1.241204 (CHPL ID 11542)

## 1. Product Context

ChartEasy™ is a proprietary, cloud-based EHR built by Theoria Medical for its own clinicians — physicians, NPs, and PAs who provide attending physician services at skilled nursing facilities (SNFs), assisted living, and other senior living communities across 21 states. It is **not sold to external customers**; the facilities where Theoria clinicians work use their own EHRs (PointClickCare, MatrixCare), and ChartEasy integrates bidirectionally with them.

**Clinical data ChartEasy stores** (per product documentation and research):
- Patient demographics (received from facility EHR integrations)
- ADT (admission/discharge/transfer) records
- Physician progress notes and encounter documentation
- Medication lists and reconciliation data
- Vital signs (manual entry and RPM device data — heart rate, respiration, SpO2, motion)
- Lab results (from laboratory integrations)
- Diagnoses / problem lists
- Implantable device information
- Care plans (chronic care management)
- Clinical decision support data (ProphEasy RTH risk predictions)
- Remote patient monitoring (RPM) device streams
- Secure clinical messages (ChatEasy platform)
- Scheduling data (regulatory-required SNF visit frequencies)

**Unclear from public documentation:**
- Whether ChartEasy handles billing/claims internally or through a separate system. CPT and HCPCS terminologies are listed as supported, but no billing module is explicitly described.
- Whether e-prescribing is handled within ChartEasy.

The product was certified in December 2024 with 34 criteria and 10 CQMs. It is certified for (b)(10) EHI Export, (g)(10) FHIR API, (e)(1) VDT, and (b)(1) Transitions of Care.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/ehr-certificate-page.html` (16,621 bytes) | The ONC certification page containing the entire (b)(10) attestation — a ~214-word statement. Lists 34 certification criteria, 10 CQMs, and links to 6 Real-World Testing PDFs. | **Primary source** — contains the only (b)(10) documentation |
| `downloads/ehr-certificate-page-full.png` (1.05 MB) | Full-page screenshot of the certification page | Confirms HTML content visually |
| `downloads/patient-portal-login.png` (364 KB) | Screenshot of ChartEasy Patient Portal login page | Confirms portal exists; shows feature list including "Download and Transmit your records" |

**No additional artifacts exist.** There is no data dictionary, no schema, no sample data, no format specification, no API documentation for (b)(10). The 6 PDFs linked from the certification page are all Real-World Testing Plans and Reports — regulatory filings unrelated to EHI export content.

## 3. Export Mechanics

- **Format**: PDF and C-CDA
- **Mechanism**: Two options documented:
  1. **Self-service via ChartEasy Patient Portal** — patients log in at `patient-portal.charteasy.com` (web) or the iOS app and download records
  2. **Request via email** — patients email `records@theoriamedical.com` for record retrieval
- **Single-patient vs bulk**: Single-patient only (patient portal is per-patient; email requests are per-patient). No bulk export mechanism is documented.
- **Access constraints**: Portal requires patient login; email requests go through the medical records team. No documentation of fees or turnaround times.

This mechanism is functionally identical to the (e)(1) View, Download, and Transmit capability — the patient portal's standard clinical summary export relabeled as (b)(10).

## 4. Export Content: What's In It

### No data dictionary exists

There is **zero** structured documentation of what the export contains. The (b)(10) attestation states only:

> "Records may be exported as both PDF and CCDA format."

No further specification is provided:
- No list of data domains, entities, tables, or fields
- No C-CDA implementation guide specifying which document type, sections, or entries are used
- No description of what the PDF contains vs. what the C-CDA contains
- No sample exports
- No machine-readable schema

### Vendor's own content organization

There is no vendor-provided content organization. The only content clues come from the patient portal's feature list (visible on the login page screenshot):
- Lab and imaging results
- Medication lists
- Chronic care management plans
- Signed clinical encounters (added in app v2.0.4)
- "Download and Transmit your records"

No entity/field table can be constructed because no data dictionary exists.

| Entity/Table | Fields | Described | Types | Category |
|---|---|---|---|---|
| *(none documented)* | — | — | — | — |

**Total entities documented: 0. Total fields documented: 0.**

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor provides no structured documentation of export content. The only evidence of what might be in the export comes from:

1. **The attestation statement**: says "PDF and CCDA format" with no content specification
2. **The patient portal feature list**: mentions lab results, medications, vital signs, care plans, and signed encounters
3. **The export format (C-CDA)**: standard C-CDA documents typically cover demographics, problems, medications, allergies, immunizations, vitals, lab results, procedures, and clinical notes — but without an implementation guide, we cannot confirm which sections are populated

The vendor provides zero categories, zero domain descriptions, and zero field-level detail. It is impossible to perform a rigorous bottom-up assessment.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Likely in C-CDA header; no field-level confirmation | ChartEasy stores demographics from facility integrations; C-CDA likely includes basic demographics |
| Encounters / visits | ⚠️ Partial | Portal lists "signed clinical encounters"; likely in C-CDA | Product stores encounter documentation; probably partially covered via C-CDA Encounters section |
| Problems / conditions | ⚠️ Partial | Likely in C-CDA if standard sections populated | Product stores diagnoses; no confirmation of coverage |
| Medications / prescriptions | ⚠️ Partial | Portal lists "medication lists"; likely in C-CDA | Product stores medication reconciliation data; basic med list probable, full reconciliation history unclear |
| Allergies | ⚠️ Partial | Standard C-CDA section; no confirmation | Product likely stores allergies; probably in C-CDA |
| Immunizations | ⚠️ Partial | Standard C-CDA section; no confirmation | May or may not be relevant for SNF/LTC population |
| Vitals | ⚠️ Partial | Portal mentions "vital signs"; likely in C-CDA | Product stores both manual vitals and RPM data; C-CDA probably covers manual vitals only |
| Lab results | ⚠️ Partial | Portal explicitly lists "lab and imaging results" | Product integrates with labs; likely in C-CDA Results section |
| Imaging / diagnostic reports | ⚠️ Partial | Portal mentions "imaging results" | Product integrates with imaging companies; coverage unknown |
| Procedures | ⚠️ Partial | Standard C-CDA section; no confirmation | Unclear what procedures a SNF-focused physician EHR tracks |
| Clinical notes / documents | ⚠️ Partial | Portal lists "signed encounters"; could be in C-CDA or PDF | Product's core function is physician progress notes; probably included |
| Care plans / goals | ⚠️ Partial | Portal lists "CCM care plans" | Product stores CCM care plans; may be in C-CDA Plan of Care section |
| Orders / referrals | ❌ Not covered | No evidence | Product is CPOE-certified; order data likely stored but not documented in export |
| Insurance / coverage | ❌ Not covered | No evidence | Unknown if ChartEasy stores insurance data |
| Claims / billing | ❌ Not covered | No evidence | Unclear if ChartEasy handles billing; CPT/HCPCS supported but no billing module described |
| Payments | N/A | No evidence | No billing module documented |
| Consents / directives | ❌ Not covered | No evidence | SNF settings involve advance directives; unclear if stored in ChartEasy |
| Patient communications | ❌ Not covered | No evidence | ChatEasy secure messaging data is stored; not mentioned in export |
| Specialty-specific (SNF/LTC) | ❌ Not covered | No evidence | RPM device data, ProphEasy risk predictions, GDR workflows — none documented in export |

**Critical gaps:**

1. **RPM device data** — heart rate, respiration, SpO2, motion data from continuous monitoring devices. This is patient-specific clinical data used for care decisions. No evidence it is in the export.
2. **Secure messaging (ChatEasy)** — clinical communications between Theoria clinicians and facility nursing staff about patient care. Part of the patient record. No evidence in the export.
3. **CDS predictions (ProphEasy)** — return-to-hospitalization risk predictions used for clinical decision-making. No evidence in the export.
4. **Orders** — ChartEasy is CPOE-certified, so it stores order data. No evidence orders are in the export.

**Fundamental limitation**: Because no data dictionary exists, all coverage assessments above are speculative, based on what standard C-CDA documents typically contain and what the patient portal feature list mentions. The actual export could contain more or less than estimated.

## 6. Documentation Quality

The (b)(10) documentation is **essentially non-existent**:

- **Data dictionary**: None
- **Field-level definitions**: None
- **Data type specifications**: None
- **Value set documentation**: None
- **C-CDA implementation guide**: None (no specification of document type, sections, entries, or templates)
- **Sample exports**: None
- **Machine-readable schemas**: None
- **Developer-facing documentation**: None
- **Export process documentation**: Two sentences — "log in to the portal" or "email us"

A developer could not build an import from this documentation. A patient cannot understand what is included in their export. A regulator cannot verify completeness.

The 170.315(b)(10) criterion requires the developer to "make publicly accessible" documentation "describing the format of the export." A ~214-word attestation statement saying "PDF and CCDA format" does not satisfy this requirement in any meaningful way.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

Documentation is too thin to assess coverage. The ~214-word attestation provides no content specification whatsoever. The export mechanism (patient portal PDF/C-CDA download) strongly suggests this is a clinical summary limited to USCDI-scope data at best. ChartEasy stores significant data domains beyond what C-CDA can represent — RPM device streams, secure clinical messaging, CDS risk predictions, CPOE orders — and none of these are addressed in the documentation or plausibly captured by a standard C-CDA export. Even for domains C-CDA could cover, there is no way to confirm coverage without a data dictionary or sample data.

**Axis 2 — Export approach: Repackaged existing export**

The (b)(10) documentation describes the same mechanism as the (e)(1) View, Download, and Transmit certification criterion: patients access the patient portal and download records in PDF and C-CDA format. The portal's feature list (lab results, medications, vitals, care plans, signed encounters) matches a standard clinical summary, not a comprehensive EHI export. The email request option (`records@theoriamedical.com`) is a standard medical records request process, not a purpose-built export mechanism. There is no evidence of any purpose-built export that covers data beyond the clinical exchange surface.

### Key Findings

1. **No data dictionary or structured documentation exists.** The entire (b)(10) documentation is a ~214-word attestation statement on the ONC certification page (`downloads/ehr-certificate-page.html`). Zero entities, zero fields, zero schemas are documented.

2. **The export is the patient portal's VDT capability relabeled as (b)(10).** The attestation describes the same PDF/C-CDA download mechanism used for (e)(1) View, Download, and Transmit. No separate or expanded export exists.

3. **C-CDA cannot represent all EHI that ChartEasy stores.** RPM device data (heart rate, SpO2, respiration streams), ChatEasy secure messages, ProphEasy risk predictions, and CPOE order details have no standard C-CDA representation. These domains are unaddressed.

4. **The developer portal (developer.charteasy.com) was unreachable** during collection. Even if accessible, it would serve (g)(10) FHIR API documentation, not (b)(10) EHI export documentation.

5. **Context matters**: Theoria Medical is a physician group that built ChartEasy for internal use, certified in December 2024. This is not a commercial EHR vendor with a documentation team — but the (b)(10) requirement applies equally regardless of the developer's size or business model.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Repackaged existing export
Export format:   PDF, C-CDA
Entities:        N/A (no data dictionary)
Fields:          N/A
Descriptions:    N/A
Sample data:     No
Bulk export:     No
Domains covered: 0 of 14 confirmed (up to ~10 speculative via C-CDA, unverifiable)
```

### Bottom Line

A patient requesting their records from ChartEasy would receive a clinical summary PDF and/or C-CDA document via the patient portal — likely covering basic demographics, medications, vitals, labs, and encounter notes. However, ChartEasy stores significant additional data (RPM device streams, secure clinical messages, CDS risk predictions, order details) that has no pathway into this export and no documentation describing its inclusion or exclusion. The single biggest gap is the **complete absence of documentation** — without a data dictionary, it is impossible to evaluate what the export actually contains, and the vendor has not met the (b)(10) requirement to publicly describe the export format.
