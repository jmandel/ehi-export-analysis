# EHI Export Analysis: Prime DataQ Health, LLC

**Product**: summitEHR  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.04.04.3236.Davi.01.00.1.250827 (CHPL ID 11689)

## 1. Product Context

summitEHR is a recently certified (August 2025, v1.0) ambulatory EHR developed by Prime DataQ Health, LLC — a small, privately held Dallas-based healthcare IT company — in a joint venture with Summus Health Care, a North Texas multi-specialty healthcare organization. The product targets internal medicine, endocrinology, cardiology, behavioral health, and primary care practices.

**Certified capabilities (34 ONC criteria):**
- Clinical documentation with smart templates, voice charting, auto-coding
- CPOE for medications, labs, diagnostic imaging — (a)(1), (a)(12)
- Electronic prescribing via NewCrop integration (including EPCS)
- Patient demographics, problem lists, medication lists, allergy lists — (a)(2)–(a)(5)
- Transitions of care via C-CDA — (b)(1)–(b)(3)
- Patient portal with view/download/transmit — (e)(1)
- FHIR APIs — (g)(7), (g)(9), (g)(10)
- Direct messaging via EMR Direct — (h)(1)
- Clinical quality measure reporting — (c)(1)–(c)(3)
- Implantable device list — (a)(14)
- Social/psychological/behavioral data — (a)(15)
- Integrated scheduling, secure messaging, telehealth
- Analytics dashboards for quality metrics and financial performance

**Billing/PM status**: Unclear. The website mentions "financial performance dashboards" and "auto-coding assistance" but does not explicitly describe integrated billing, claims management, or revenue cycle features. It is uncertain whether summitEHR includes billing or if billing is handled externally.

**Baseline expectation**: The export should cover patient demographics, problems, medications, allergies, immunizations, vitals, labs, clinical notes, encounters, procedures, e-prescribing data, care plans, assessments, social history, family history, implantable devices, insurance information, and — if the product stores it — billing/claims data and patient communications.

## 2. Artifacts Reviewed

| Artifact | Description | Informative? |
|---|---|---|
| `downloads/EHI-Export-Documentation-SummitEHR-v1.0.pdf` | 4-page PDF (377 KB). Cover page + TSV format description + list of 47 supported resource types. Created Dec 3, 2025 by "Abdur Rehman" via Microsoft Print to PDF. No field-level data dictionary, no schema, no sample data. | **Primary and only artifact.** Provides resource list but zero field-level detail. |

Only one artifact exists. There is no data dictionary, no schema file, no sample export data, and no supplementary documentation beyond this PDF.

## 3. Export Mechanics

- **Format**: TSV (Tab-Separated Values) — one file per resource type
- **Mechanism**: Manual UI-based export ("EHI Export feature lets you manually export")
- **Scope**: Single-patient or full practice population (bulk)
- **Bulk structure**: Separate TSV file per resource type; each row contains data for one patient
- **Access constraints**: No fees or constraints described; documentation implies the feature is accessible to authorized users within the application
- **No API-based export**: No programmatic/automated export mechanism described

The documentation includes a trivial TSV example showing `PatientID`, `FirstName`, `LastName`, `DOB`, `Gender` columns — but this is just a format illustration, not actual export content documentation.

## 4. Export Content: What's In It

### What we know

The PDF lists **47 resource types** available for export. This is the complete extent of the documentation — resource names only, with no field-level details whatsoever.

**No data dictionary exists.** The documentation provides:
- ❌ No column/field definitions for any resource
- ❌ No data types
- ❌ No field descriptions
- ❌ No value sets or coded values
- ❌ No relationships or foreign keys between resources
- ❌ No handling of multi-valued fields
- ❌ No date/time format specifications
- ❌ No null/empty value conventions
- ❌ No sample export files
- ❌ No machine-readable schema

### Vendor's own content organization

The vendor does not organize resources into categories; they are presented as a flat bulleted list. I have categorized them by clinical domain for analysis purposes:

| Resource Name | Domain (analyst-assigned) |
|---|---|
| Allergies | Allergies |
| Appointment reminders | Encounters / Visits |
| Appointments | Encounters / Visits |
| Assessments | Assessments / Screening |
| Care plans | Care Plans / Goals |
| Cognitive statuses | Assessments / Screening |
| Diet | Diet / Nutrition |
| Document Details | Clinical Notes / Documents |
| Encounter built procedures | Encounters / Visits |
| Encounters | Encounters / Visits |
| Exam | Encounters / Visits |
| Family history | Family History |
| Family history diseases | Family History |
| Follow up appointments | Encounters / Visits |
| Functional statuses | Assessments / Screening |
| Goals | Care Plans / Goals |
| Immunizations | Immunizations |
| Implantable devices | Implantable Devices |
| Interventions | Care Plans / Goals |
| Lab order diagnosis | Lab Results |
| Lab Orders | Lab Results |
| Lab test result notes | Lab Results |
| Lab test results | Lab Results |
| Lab tests | Lab Results |
| Medications | Medications / Prescriptions |
| Past medical history | Problems / Conditions |
| Past surgeries | Procedures |
| Patient addresses | Demographics |
| Patient care team members | Care Team |
| Patient contacts | Demographics |
| Patient information | Demographics |
| Patient insurances | Insurance / Coverage |
| Patient payments | Payments |
| Patient races | Demographics |
| Patient tasks | Tasks / Workflow |
| Patient vitals | Vitals |
| PHQ 9 screening | Assessments / Screening |
| Pregnancy status | Social / Behavioral |
| Prior authentication | Prior Authorization |
| Problems | Problems / Conditions |
| Progress notes | Clinical Notes / Documents |
| Related person details | Demographics |
| SDOH | Social / Behavioral |
| Smoking status | Social / Behavioral |
| Social history | Social / Behavioral |
| Unsigned documents | Clinical Notes / Documents |
| Vaping status | Social / Behavioral |

**Domain summary (47 resources across 21 domains):**

| Domain | Count | Resources |
|---|---|---|
| Encounters / Visits | 6 | Appointments, Appointment reminders, Encounters, Encounter built procedures, Exam, Follow up appointments |
| Demographics | 5 | Patient information, Patient addresses, Patient contacts, Patient races, Related person details |
| Lab Results | 5 | Lab Orders, Lab order diagnosis, Lab tests, Lab test results, Lab test result notes |
| Social / Behavioral | 5 | SDOH, Social history, Smoking status, Vaping status, Pregnancy status |
| Assessments / Screening | 4 | Assessments, PHQ 9 screening, Cognitive statuses, Functional statuses |
| Care Plans / Goals | 3 | Care plans, Goals, Interventions |
| Clinical Notes / Documents | 3 | Progress notes, Unsigned documents, Document Details |
| Family History | 2 | Family history, Family history diseases |
| Problems / Conditions | 2 | Problems, Past medical history |
| Allergies | 1 | Allergies |
| Care Team | 1 | Patient care team members |
| Diet / Nutrition | 1 | Diet |
| Immunizations | 1 | Immunizations |
| Implantable Devices | 1 | Implantable devices |
| Insurance / Coverage | 1 | Patient insurances |
| Medications / Prescriptions | 1 | Medications |
| Payments | 1 | Patient payments |
| Prior Authorization | 1 | Prior authentication |
| Procedures | 1 | Past surgeries |
| Tasks / Workflow | 1 | Patient tasks |
| Vitals | 1 | Patient vitals |

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The 47 resource names suggest broad coverage of clinical data domains typical of an ambulatory EHR:

**Strengths:**
- **Lab data** is the most granular area, with 5 separate resources splitting orders, tests, results, result notes, and order diagnoses — this suggests a structured internal data model being exported rather than a flat summary.
- **Social/behavioral data** is well-represented: SDOH, social history, smoking status, vaping status, and pregnancy status each get a dedicated resource. This goes beyond USCDI minimums.
- **Screening/assessments** include PHQ-9, cognitive statuses, and functional statuses — specialty-relevant data beyond standard clinical summaries.
- **Insurance and payments** are present (`Patient insurances`, `Patient payments`), which goes beyond USCDI.
- **Prior authentication** (likely prior authorization) suggests some billing/administrative workflow data.

**Weaknesses:**
- Without field-level documentation, it is impossible to assess depth. A resource named "Medications" could contain 5 fields or 50; there is no way to know.
- The flat bulleted list has no categorization or relationship information. How "Lab Orders" relates to "Lab test results" is undocumented.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | Patient information, Patient addresses, Patient contacts, Patient races, Related person details (5 resources) | Appears thorough; multiple resources suggest detailed demographic capture |
| Encounters / visits | ✅ Covered | Encounters, Encounter built procedures, Exam, Appointments, Appointment reminders, Follow up appointments (6 resources) | Well-represented |
| Problems / conditions / diagnoses | ✅ Covered | Problems, Past medical history (2 resources) | Present |
| Medications / prescriptions | ⚠️ Partial | Medications (1 resource) | Only one resource; unclear if e-prescribing details from NewCrop (prescription orders, refill history, pharmacy routing, EPCS data) are included or only medication lists |
| Allergies | ✅ Covered | Allergies (1 resource) | Present |
| Immunizations | ✅ Covered | Immunizations (1 resource) | Present |
| Vitals | ✅ Covered | Patient vitals (1 resource) | Present |
| Lab results | ✅ Covered | Lab Orders, Lab order diagnosis, Lab tests, Lab test results, Lab test result notes (5 resources) | Well-structured with multiple related resources |
| Imaging / diagnostic reports | ❌ Not covered | No imaging-specific resource listed | Product is certified for CPOE for diagnostic imaging (a)(12); imaging orders/results may be absent from export |
| Procedures | ✅ Covered | Past surgeries, Encounter built procedures (2 resources) | Present |
| Clinical notes / documents | ✅ Covered | Progress notes, Unsigned documents, Document Details (3 resources) | Present; "Unsigned documents" is a useful detail |
| Care plans / goals | ✅ Covered | Care plans, Goals, Interventions (3 resources) | Present |
| Orders / referrals | ⚠️ Partial | Lab Orders present; no general order or referral resource | Product supports CPOE; non-lab orders and referrals may be missing |
| Insurance / coverage | ✅ Covered | Patient insurances (1 resource) | Present |
| Claims / billing | ⚠️ Partial | Patient payments (1 resource); no claims, charges, superbills, or billing codes | If the product has billing capabilities (unclear), this is thin. "Patient payments" alone does not constitute billing data coverage |
| Payments | ⚠️ Partial | Patient payments (1 resource) | Present but cannot assess depth |
| Consents / directives | ❌ Not covered | No consent or advance directive resource | May not be a significant gap if product doesn't store these |
| Patient communications / portal messages | ❌ Not covered | No messaging or communication resource | Product supports secure messaging and patient portal; this is a gap |
| Specialty-specific (endocrinology, cardiology, behavioral health) | ⚠️ Partial | PHQ-9 screening (behavioral health); no endocrinology or cardiology-specific resources | Product targets these specialties; only behavioral screening is represented |

**Summary**: 12 of 18 applicable domains show at least nominal coverage. 4 domains show partial coverage. 2 domains with expected data (imaging, patient communications) show no coverage. Without field-level documentation, "coverage" here means only that a resource name exists — depth is entirely unverifiable.

## 6. Documentation Quality

The documentation quality is **critically poor**:

- **4 pages total** (1 cover, 1 format description, 2 resource list)
- **No data dictionary**: Zero field-level documentation for any of the 47 resources
- **No schema**: No TSV header definitions, no JSON schema, no formal specification
- **No sample data**: Only a trivial format illustration (PatientID, FirstName, LastName, DOB, Gender)
- **No relationships**: No documentation of how resources relate to each other
- **No export instructions**: No UI walkthrough, no screenshots, no step-by-step guide
- **No versioning beyond "v1.0"**: No changelog

**Could a developer use this?** No. A developer receiving this export would get a set of TSV files with column headers and data, but would have to reverse-engineer the meaning of every column, the data types, the coded values, and the relationships between files. The documentation provides the file names but nothing about their content.

**Machine-readable artifacts**: None. No schema files, no sample data files, no API documentation related to export.

The documentation was created on December 3, 2025 — roughly 3 months after the August 2025 certification date — and appears to be a minimal compliance artifact.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The 47 resource names span a reasonably broad set of clinical domains and go beyond USCDI by including insurance, payments, prior authorization, detailed lab structure, and behavioral screening data. However, there are notable gaps in domains the product is known to support: diagnostic imaging (product is certified for imaging CPOE), patient communications (product has secure messaging and a patient portal), and potentially e-prescribing details (product integrates NewCrop). Furthermore, without field-level documentation, it is impossible to verify that the resources are genuinely deep rather than superficial. The resource _names_ suggest reasonable coverage; the complete absence of field documentation prevents confirmation.

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly not a repackaged FHIR or C-CDA export. The TSV-based format with 47 product-specific resource names (e.g., "Encounter built procedures," "Lab test result notes," "PHQ 9 screening," "Vaping status," "Prior authentication") reflects the vendor's internal data model, not a standards-based clinical exchange projection. Resources like "Patient payments," "Patient insurances," "Unsigned documents," and "Patient tasks" go beyond what any standard clinical exchange format would include. The vendor built a purpose-specific export for (b)(10), even though they documented it poorly.

### Key Findings

1. **Purpose-built but almost entirely undocumented**: The 47 TSV resource types represent a genuine (b)(10) effort — the vendor exported their internal data model rather than repackaging C-CDA or FHIR. But the documentation is among the thinnest possible: resource names only, no field definitions, no schema, no sample data.

2. **Impossible to verify depth**: Without a single field name documented, the actual content of each resource file is completely opaque from the documentation alone. A resource named "Medications" could contain comprehensive prescription data or just a drug name list.

3. **Resource scope goes meaningfully beyond USCDI**: Resources like Patient payments, Patient insurances, Prior authentication, PHQ-9 screening, SDOH, Vaping status, Cognitive statuses, Functional statuses, and Patient tasks are not part of USCDI/US Core clinical exchange.

4. **Notable gaps in portal/messaging and imaging**: Despite product support for secure messaging, patient portal, and diagnostic imaging ordering, no corresponding export resources exist for communications or imaging data.

5. **Very new product, minimal maturity**: Certified August 2025, documentation created December 2025, version 1.0. This is a startup EHR with no independent reviews or market presence. Documentation quality may improve but is currently insufficient for practical use.

### Summary Stats

```
Coverage:        Partial
Approach:        Purpose-built EHI export
Export format:   TSV (Tab-Separated Values)
Entities:        47
Fields:          N/A (no field-level documentation)
Descriptions:    N/A (0% — no fields documented at all)
Sample data:     No
Bulk export:     Yes (full practice population)
Domains covered: 12 of 18 applicable domains (4 additional partial)
```

### Bottom Line

summitEHR built a genuine purpose-specific EHI export with 47 TSV resource types that go beyond USCDI, covering insurance, payments, behavioral screening, and other non-standard domains. However, the documentation is critically deficient — a flat list of resource names with zero field-level detail makes the export effectively opaque to anyone without access to the actual data files. A patient or provider would receive TSV files they'd have to interpret entirely from column headers, with no guidance on data types, coded values, or relationships.
