# EHI Export Analysis: WEBeDoctor, Inc.

**Product**: WEBeDoctor Physician Office v6.0  
**Analysis date**: 2026-02-16  
**CHPL ID**: 15.99.05.2526.WEBe.06.02.1.260113

## 1. Product Context

WEBeDoctor Physician Office is a cloud-based, integrated EHR and practice management platform for ambulatory physician practices. The company is small (~11 employees, ~$8.5M revenue) and serves several hundred users across multiple specialties. The product is a unified platform ("Unified Desktop") that encompasses:

- **Clinical documentation**: Problem lists, medications, allergies, vitals, lab results, clinical notes (with multiple input methods including AI ambient documentation), immunizations, family health history, implantable devices, care plans
- **Practice management**: Multi-provider scheduling, patient demographics, insurance verification, patient kiosk check-in
- **Medical billing & revenue cycle**: Electronic claims submission, claims tracking, payment posting, coding assistance, EDI, financial reporting, clearinghouse integration (Change Healthcare), dedicated billing services (WEBeBiller)
- **E-prescribing**: Surescripts-connected, controlled substance prescribing, drug interaction checking
- **Lab integration**: LabCorp and Quest Diagnostics ordering and results
- **Patient portal**: Secure messaging, lab results viewing, billing info, appointment requests, prescription refills
- **Telehealth**: HIPAA-compliant virtual visits
- **Remote patient monitoring**: Blood pressure, weight, glucose monitoring
- **Electronic faxing**: Including AI-powered fax matching (WEBeFax.AI)
- **Referral management**: Referral letters and tracking
- **Public health reporting**: Immunization registries and syndromic surveillance

This is a feature-rich ambulatory EHR with substantial billing/PM capabilities. A genuine (b)(10) export should cover clinical data, billing/claims data, patient portal communications, remote monitoring data, and specialty-specific data.

## 2. Artifacts Reviewed

| Artifact | Description | Informative? |
|---|---|---|
| `WEBeDoctor_EHI_Export.pdf` (860 KB, 3 pages) | The sole EHI export documentation. Describes C-CDA 2.1 export with screenshots. Created 2023-10-27. Contains no data dictionary, no field mapping, no schema. | **Primary source** — but nearly empty of technical detail |
| `WEBeDoctor_Mandatory_Disclosures_SLI_01192026_Signed.pdf` (157 KB) | Mandatory cost/certification disclosures. Confirms (b)(10) certification by SLI Compliance on 2026-01-13. Lists all 38 certified criteria. | Context only — confirms certification but no export detail |
| `certification-page-full.png` (490 KB) | Screenshot of https://new.webedoctor.com/certification/ showing the certification page layout with links to documents. | Context only |

**No other artifacts exist.** There is no data dictionary, no schema file, no sample data, no field mapping document, no FHIR capability statement, no export specification beyond the 3-page PDF.

## 3. Export Mechanics

- **Format**: C-CDA 2.1 (XML-based clinical document standard)
- **Mechanism**: UI-driven. Navigate to Hub > EHI Export > One Time. Administrator must first enable EHI Export permission per user via Administration > User Configuration > "Enable EHI Export" button.
- **Single-patient**: Select patient, click Save. C-CDA file appears in Hub > EHI Export > CCDA List > Download.
- **Bulk export**: Check "All Patients" checkbox. Generates a ZIP file of all patient C-CDA files, available from CCDA List > Download. Date range and provider filters available.
- **Access constraints**: Requires admin-granted "EHI Export" permission per user role. Screenshots show roles including physician, biller, nurse, and frontdesk.
- **Fees**: Not stated in the EHI export documentation. The mandatory disclosures PDF lists product costs but does not itemize EHI export fees separately.

The export UI also shows "Scheduled" and "Recurring" tabs (visible in screenshots), suggesting automated/recurring export capability, though these are not described in the documentation text.

## 4. Export Content: What's In It

### What the documentation tells us

The EHI export documentation is 3 pages total:
- **Page 1**: One paragraph stating the export generates C-CDA 2.1 documents, a link to the HL7 C-CDA standard specification, and a screenshot showing user configuration for enabling EHI Export.
- **Page 2**: Screenshots of single-patient export (patient selection, CCDA list with download links). The CCDA List shows columns: Schedule Name, Process Start Date, Process End Date, From Date, To Date, Patient, Process (all show "OneTime"), Status ("Generated"), and View/Download buttons.
- **Page 3**: Screenshot of population-level export with "All Patients" checkbox. Two sentences of instruction.

**The vendor provides zero product-specific documentation about what data is in the export.** The only reference to content is the link to the HL7 C-CDA 2.1 standard specification. There is:
- No data dictionary
- No field mapping (which EHR fields → which C-CDA sections/entries)
- No list of C-CDA sections included
- No description of vendor extensions or custom content
- No sample data file
- No machine-readable schema

### What C-CDA 2.1 typically contains

Since the vendor's only content specification is "C-CDA 2.1," the export is presumably limited to standard C-CDA Continuity of Care Document (CCD) sections. A standard C-CDA CCD typically includes sections for:

| C-CDA Section | Standard LOINC | Domain |
|---|---|---|
| Allergies and Intolerances | 48765-2 | Allergies |
| Medications | 10160-0 | Medications |
| Problem List | 11450-4 | Problems |
| Procedures | 47519-4 | Procedures |
| Results | 30954-2 | Lab results |
| Vital Signs | 8716-3 | Vitals |
| Immunizations | 11369-6 | Immunizations |
| Encounters | 46240-8 | Encounters |
| Plan of Treatment | 18776-5 | Care plans |
| Goals | 61146-7 | Goals |
| Social History | 29762-2 | Demographics |
| Payers | 48768-6 | Insurance (basic) |
| Medical Equipment | 46264-8 | Devices |
| Assessment | 51848-0 | Clinical notes |

**Without sample data or a vendor mapping, it is impossible to determine which of these sections WEBeDoctor actually populates, how completely they are populated, or whether any vendor-specific extensions exist.**

### Vendor's own content organization

There is no vendor-provided content organization. The vendor has not defined entities, tables, fields, or categories. The entire documentation is: "we generate C-CDA 2.1" + link to standard spec + screenshots of the export UI.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes their export in exactly one sentence: *"WEBeDoctor is compliant with §170.315(b)(10) Electronic Health Information Export by generating C-CDA 2.1 electronic documents."*

There are no vendor-defined categories, no content sections, no data domains described. The vendor has effectively delegated all content specification to the HL7 C-CDA 2.1 standard, providing no indication of what product-specific data makes it into the export.

At best, the export covers standard C-CDA clinical summary content — the same data that would be produced for transitions of care under (b)(1). This is USCDI-scope clinical data and represents the existing clinical exchange surface, not a purpose-built EHI export.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA header contains basic demographics | C-CDA includes limited demographics (name, DOB, gender, address). Product stores much more (emergency contacts, preferred language, etc.) |
| Encounters / visits | ⚠️ Partial | C-CDA Encounters section (if populated) | Product stores full encounter records including scheduling, visit types, telehealth sessions. C-CDA captures minimal encounter data |
| Problems / conditions | ⚠️ Partial | C-CDA Problem List section (if populated) | Standard section — likely present but depth unknown without sample data |
| Medications / prescriptions | ⚠️ Partial | C-CDA Medications section (if populated) | Product has robust e-prescribing (WEBeRx, Surescripts). C-CDA captures medication list but not prescribing workflows, refill history, pharmacy communications |
| Allergies | ⚠️ Partial | C-CDA Allergies section (if populated) | Standard section — likely present |
| Immunizations | ⚠️ Partial | C-CDA Immunizations section (if populated) | Standard section — likely present |
| Vitals | ⚠️ Partial | C-CDA Vital Signs section (if populated) | Standard section — likely present |
| Lab results | ⚠️ Partial | C-CDA Results section (if populated) | Product integrates with LabCorp/Quest. C-CDA captures result values but not order details, specimen info, or full result metadata |
| Imaging / diagnostic reports | ❌ Not covered | No evidence in C-CDA standard sections | Product supports CPOE for diagnostic imaging (a)(3). No imaging reports in standard C-CDA |
| Procedures | ⚠️ Partial | C-CDA Procedures section (if populated) | Standard section — basic procedure list only |
| Clinical notes / documents | ⚠️ Partial | C-CDA may include note sections | Product has extensive note capabilities (templates, dictation, AI-generated notes, transcription). C-CDA may include some note content but not the full richness |
| Care plans / goals | ⚠️ Partial | C-CDA Plan of Treatment and Goals sections | Standard sections — basic if present |
| Orders / referrals | ❌ Not covered | No dedicated order/referral sections in standard C-CDA | Product has referral management, CPOE for meds/labs/imaging. Not captured in C-CDA export |
| Insurance / coverage | ⚠️ Partial | C-CDA Payers section (if populated) | Standard C-CDA Payers section is minimal (payer name, ID). Product stores detailed insurance verification data |
| Claims / billing | ❌ Not covered | No billing data in C-CDA | **Major gap.** Product has full billing/RCM: electronic claims, claims tracking, payment posting, coding, EDI, Change Healthcare integration. None of this is in C-CDA |
| Payments | ❌ Not covered | No payment data in C-CDA | Product stores payment records, adjustments, patient statements. Not in C-CDA |
| Consents / directives | ❌ Not covered | No consent section evident | No evidence of consent/directive export |
| Patient communications / portal messages | ❌ Not covered | No messaging data in C-CDA | Product has patient portal with secure messaging, appointment requests, refill requests. None exported |
| Remote patient monitoring | ❌ Not covered | No RPM data in C-CDA | Product has RPM for BP, weight, glucose. Not in C-CDA |
| Specialty-specific data | ❌ Not covered | No specialty sections in C-CDA | Product serves multiple specialties (cardiology, ophthalmology, podiatry, etc.) with customizable templates. None of this specialty data is in C-CDA |

**Summary**: At least 7 applicable domains are completely missing from the export (billing, payments, communications, RPM, imaging reports, orders/referrals, specialty data). The domains marked "Partial" are all speculative based on C-CDA standard sections — without sample data, even their presence cannot be confirmed.

## 6. Documentation Quality

The documentation quality is extremely poor:

- **Can a developer use it?** No. The documentation tells a developer exactly one thing: the export produces C-CDA 2.1 files. There is no product-specific information about what data elements are included, how EHR data maps to C-CDA sections, what coded values are used, or what edge cases exist.
- **Data dictionary**: None provided.
- **Field mapping**: None provided. The vendor links to the HL7 C-CDA 2.1 standard spec and provides no further detail.
- **Sample data**: None provided.
- **Machine-readable artifacts**: None (no schema, no sample XML, no capability statement).
- **Screenshots**: The 3 screenshots show the export UI but reveal nothing about export content.

A developer receiving this export would get XML files conforming to C-CDA 2.1 and would need to parse them using generic C-CDA tooling with no vendor-specific guidance. There would be no way to know whether data was missing, malformed, or incomplete without independent knowledge of the patient's record.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The export is a C-CDA 2.1 document — a clinical summary standard designed for transitions of care, not for comprehensive EHI export. C-CDA covers USCDI-scope clinical data at best, which represents perhaps 20-30% of what WEBeDoctor Physician Office stores. The product has full billing/RCM capabilities (electronic claims, payment posting, EDI, clearinghouse integration), a patient portal with messaging, remote patient monitoring, e-prescribing workflows, referral management, and specialty-specific templates — none of which are captured in C-CDA. The documentation is so thin (3 pages, no data dictionary) that it's impossible to confirm even the clinical data is complete. This is a textbook case of minimal documentation with a narrow export format.

**Axis 2 — Export approach: Repackaged existing export**

This is unambiguously a repackaged existing export. The vendor's (b)(10) export is the same C-CDA generation capability they already have for transitions of care under (b)(1). The telltale signs are all present:
1. The documentation explicitly says "generating C-CDA 2.1 electronic documents" — this is their existing clinical exchange capability.
2. The only content reference is a link to the generic HL7 C-CDA standard spec — no product-specific data dictionary or mapping.
3. The CCDA List UI (visible in screenshots) shows exports labeled "OneTime" alongside what appears to be the same infrastructure used for other C-CDA generation (transitions of care, patient portal VDT).
4. No billing, administrative, portal messaging, RPM, or specialty data — only what C-CDA can carry.
5. The PDF was created in October 2023, suggesting it was produced for certification compliance rather than as documentation of a genuine new capability.

The vendor has taken their existing C-CDA generation (certified under (b)(1) and (g)(6)), added an "EHI Export" menu item, and called it (b)(10). This is the most common failure mode for small EHR vendors.

### Key Findings

1. **The export is simply C-CDA 2.1 — the vendor's existing clinical exchange format rebranded as (b)(10).** The documentation explicitly states this, and there is no evidence of any purpose-built export capability (`WEBeDoctor_EHI_Export.pdf`, page 1).

2. **Zero product-specific documentation exists.** No data dictionary, no field mapping, no schema, no sample data. The entire content specification is a link to the HL7 C-CDA standard. A developer would have no vendor-specific guidance for interpreting the export.

3. **Major data domains are entirely absent.** The product has full billing/RCM capabilities (claims, payments, EDI), a patient portal with secure messaging, remote patient monitoring (BP, glucose, weight), e-prescribing workflows, and referral management — none of which are representable in C-CDA and none of which are addressed in the export documentation.

4. **Even clinical coverage is unverifiable.** Without sample data or a field mapping, it's impossible to confirm which C-CDA sections WEBeDoctor actually populates or how completely. The sections could be richly populated or nearly empty.

5. **The export infrastructure appears functional.** The UI screenshots show a working export system with single-patient and bulk capabilities, date range filtering, scheduled/recurring options, and a download queue — the mechanism works, but the content is limited to C-CDA.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Repackaged existing export
Export format:   C-CDA 2.1 (XML)
Entities:        N/A (no vendor data dictionary; ~18 standard C-CDA sections at most)
Fields:          N/A (no field-level documentation)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (All Patients generates ZIP)
Domains covered: ~6-8 of 19 applicable domains (clinical only, all speculative without sample data)
```

### Bottom Line

WEBeDoctor's (b)(10) export is their existing C-CDA transition-of-care capability relabeled as EHI export, with a 3-page PDF as the sole documentation. A patient or provider would receive a clinical summary in C-CDA format covering basic clinical data (if sections are populated), but would get none of their billing records, portal messages, remote monitoring data, prescription workflows, or specialty-specific clinical data — all of which the product stores and all of which are part of the designated record set. The single biggest gap is the complete absence of billing/financial data from a product with full RCM capabilities.
