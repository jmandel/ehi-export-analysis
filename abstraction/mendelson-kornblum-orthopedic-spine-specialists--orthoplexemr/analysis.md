# EHI Export Analysis: Mendelson Kornblum Orthopedic & Spine Specialists

**Product**: OrthoplexEMR V1
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.3014.Orth.01.00.1.180101 (CHPL ID 9349)

## 1. Product Context

OrthoplexEMR is a custom-built, single-organization EMR developed by Proactive Technology Management exclusively for Mendelson Kornblum Orthopedic & Spine Specialists (MKO) / Synergy Health Partners (SHP). It is not a commercially sold product. The practice is a large multi-site orthopedic group in Southeast Michigan with 20+ physicians across multiple locations, including outpatient clinics, ambulatory surgery centers, MRI imaging centers, and physical/occupational therapy sites.

The EMR is certified across a broad set of ONC criteria covering clinical documentation (CPOE, demographics, vitals, problem list, allergies, medications, family health history, implantable devices), care transitions (C-CDA), patient portal, public health reporting, clinical quality measures, and FHIR APIs. Key dependencies include MDToolbox (e-prescribing), EMRDirect (Direct messaging), and e-IMO (clinical terminology).

**What the export should cover** (based on the product's orthopedic specialty context):
- Standard clinical domains (demographics, encounters, meds, allergies, vitals, problems, procedures, labs)
- Clinical notes (progress notes, H&P, operative notes, consult notes — critical for a surgical practice)
- Imaging orders and results (practice operates MRI centers)
- Surgical/operative records and implant details
- Orthopedic-specific assessments (range of motion, functional outcomes, pain scales)
- Patient portal messages and patient-submitted data
- Family health history (certified under (a)(12))
- Billing data (unclear if OrthoplexEMR handles billing or if a separate system is used)

## 2. Artifacts Reviewed

| Artifact | Description | Informational Value |
|----------|-------------|---------------------|
| `downloads/Healthinformationexport.html` (5,200 bytes) | Single static HTML page containing the entirety of the EHI export documentation: export instructions and a minimal data dictionary listing 18 C-CDA sections with field names | **Primary source** — this is all that exists |
| `downloads/screenshot-ehi-export-page.png` (426 KB) | Full-page browser screenshot of the HTML documentation page | Confirms visual rendering matches HTML source |

No PDFs, schemas, sample data files, ZIP archives, or any other artifacts exist. The entire EHI export documentation is a single 5,200-byte HTML file. Last-Modified date: September 15, 2023.

## 3. Export Mechanics

- **Format**: C-CDA (Continuity of Care Document, template 2.16.840.1.113883.10.20.22.1.2)
- **Mechanism**: UI-driven within the OrthoplexEMR application
  - **Single patient**: Provider navigates to History → CCDA for a specific patient. Options to download ZIP, send via secure email, or send via Direct messaging.
  - **Population export**: Provider navigates to Utilities → CCDA, creates a named export job with configurable frequency (once/daily/weekly/monthly/yearly), date range, and scope (all patients or single). Output placed on a shared server accessible within MKO network or via VPN.
  - **Patient self-service**: Patients log into `portal.mendelsonortho.com` and download a "Patient Summary for Transition of Care."
- **Bulk capability**: Yes — the population export supports all-patient batch export.
- **Access constraints**: Population export requires MKO network or VPN access to retrieve files from shared server.
- **Fees**: Not documented.

## 4. Export Content: What's In It

The export is a standard C-CDA Continuity of Care Document. The documentation page provides a section-and-field listing for 18 C-CDA sections containing a total of 68 enumerated fields. No fields have descriptions, types, value sets, or any metadata beyond a bare name.

The "Structure of Export" section links to the generic HL7 C-CDA CCD template specification rather than providing any vendor-specific documentation.

### Vendor's own content organization

The vendor lists 18 sections using C-CDA section names. Parsed from `downloads/Healthinformationexport.html` (see `analysis/entity-inventory-full.json`):

| Section | Fields | Described | Types | Notes |
|---------|--------|-----------|-------|-------|
| Demographics | 9 | 0 | no | First Name, Last Name, DOB, Sex, Race, Preferred Language, Ethnicity (primary/secondary), Contact Info, Patient ID |
| Document | 4 | 0 | no | Document ID, Created Date, Author, Contact Info |
| Encounter | 4 | 0 | no | Encounter ID, Encounter Date, Responsible Party, Contact Info |
| Document Meta | 2 | 0 | no | Maintained by, Contact Info |
| Medications | 9 | 0 | no | Medication, Code, Type, Strength, Dose, Route, Frequency, Date Started, Status |
| Problems | 4 | 0 | no | Problem Code, Patient Problem, Status, Date Diagnosed |
| Allergies, Adverse Reactions, Alerts | 5 | 0 | no | Allergy Code, Substance, Medication/Agent Allergy, Reaction, Date Entered |
| Vital Signs | 10 | 0 | no | Date/Time, Height, Weight, Blood Pressure, Pulse, Temp, Resp, Pulse Ox, O2 % BldC Ox, Inhaled Ox Conc |
| Care Team Information | 3 | 0 | no | Name, Position, Email |
| Immunizations | 0 | 0 | no | "Empty (Immunizations not provided at clinics)" |
| Social History (smoking) | 3 | 0 | no | Smoking Code, Smoking Status, from/to |
| Medical Equipment | 3 | 0 | no | Description, Date and Time, Status |
| Results (Tests) | 7 | 0 | no | Code, Code System, Name, Date, Result, Lab, Provider |
| Procedures | 3 | 0 | no | Description, Date and Time, Status |
| Goals | 0 | 0 | no | Free form |
| Health Concerns | 0 | 0 | no | Free form |
| Plan of Treatment | 2 | 0 | no | Plan of Treatment, Assessment |
| Reason for Referral | 0 | 0 | no | Free form |

**Summary statistics**:
- 18 sections total (14 with enumerated fields, 4 free-form/empty)
- 68 fields total
- 0 fields with descriptions (0%)
- 0 fields with data types documented
- 0 value sets or code systems specified (despite several "Code" fields)
- No foreign keys or relationships documented (relying entirely on the C-CDA standard to define structure)
- No sample data provided

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor provides a **standard C-CDA patient summary** — the same document type used for transitions of care. The 18 sections map directly to standard C-CDA CCD sections with no vendor-specific extensions or additions.

The coverage is thin even within the C-CDA sections that are present:
- **Demographics**: 9 fields — basic demographics only, missing address components, phone, email as separate fields
- **Medications**: 9 fields — reasonable for a C-CDA medication list
- **Vital Signs**: 10 fields — includes orthopedically relevant measurements (none specialty-specific though)
- **Results (Tests)**: 7 fields — basic lab result representation
- **Encounters**: 4 fields — ID, date, responsible party, contact info only; no encounter type, location, diagnoses, or disposition
- **Goals, Health Concerns, Reason for Referral**: Free-form text with no structure
- **Immunizations**: Explicitly empty (reasonable for orthopedic specialty)

There are no sections beyond standard C-CDA CCD content. No billing data, no clinical notes, no imaging, no surgical records, no specialty-specific data.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|--------|----------|-----------------|--------------|
| Demographics | ⚠️ Partial | Demographics section (9 fields, name-only) | Basic fields present but minimal detail; no address breakdown, no contact details beyond generic "Contact Info" |
| Encounters / visits | ⚠️ Partial | Encounter section (4 fields) | Only ID, date, responsible party, contact info. Missing encounter type, location, diagnoses, reason, disposition |
| Problems / conditions / diagnoses | ⚠️ Partial | Problems section (4 fields) | Problem code, name, status, date diagnosed. No onset details, severity, verification status, linked encounters |
| Medications / prescriptions | ⚠️ Partial | Medications section (9 fields) | Reasonable field list but no prescriber, pharmacy, refill info. MDToolbox integration data not included |
| Allergies | ✅ Covered | Allergies section (5 fields) | Basic allergy data present |
| Immunizations | N/A | Explicitly empty | Vendor states "Immunizations not provided at clinics" — reasonable for orthopedic specialty |
| Vitals | ✅ Covered | Vital Signs section (10 fields) | Good coverage including pulse oximetry |
| Lab results | ⚠️ Partial | Results (Tests) section (7 fields) | Basic result representation; no reference ranges, specimen info, order context |
| Imaging / diagnostic reports | ❌ Not covered | No imaging section | Product serves orthopedic practice with MRI centers; imaging orders certified under (a)(4). Significant gap |
| Procedures | ⚠️ Partial | Procedures section (3 fields) | Description, date, status only. For a surgical practice, this is extremely thin — no operative details, surgeon, approach, implants used, laterality |
| Clinical notes / documents | ❌ Not covered | No notes/documents section | A 20+ physician surgical practice generates extensive clinical notes. Major gap |
| Care plans / goals | ⚠️ Partial | Goals, Health Concerns, Plan of Treatment sections | All free-form text with no structure |
| Orders / referrals | ⚠️ Partial | Reason for Referral section (free form) | Free text only; no structured order data |
| Insurance / coverage | ❌ Not covered | No insurance section | Unknown if OrthoplexEMR stores insurance data |
| Claims / billing | ❌ Not covered | No billing sections | Unknown if OrthoplexEMR handles billing or uses separate system |
| Payments | ❌ Not covered | No payment sections | Same uncertainty as billing |
| Consents / directives | ❌ Not covered | No consent section | Likely stored for surgical practice |
| Patient communications / portal messages | ❌ Not covered | No communications section | Product is certified for patient portal (e)(1)/(e)(3); portal messages not exported |
| Specialty-specific (orthopedic) | ❌ Not covered | No specialty data sections | No orthopedic assessments, range of motion, functional outcomes, pain scales, implant tracking beyond basic Medical Equipment (3 fields) |
| Family health history | ❌ Not covered | Not in export sections | Certified under (a)(12) but missing from export |
| Social history | ⚠️ Partial | Social History section (3 fields) | Smoking status only; no alcohol, drug use, occupation, exercise |
| Medical devices / implants | ⚠️ Partial | Medical Equipment section (3 fields) | Description, date, status only. Certified for (a)(14) implantable devices, but export has minimal detail |

## 6. Documentation Quality

The documentation quality is **extremely minimal**:

- **Data dictionary**: Field names listed only — no descriptions, no data types, no cardinalities, no value sets, no code system specifications. Several fields reference "Code" (Problem Code, Allergy Code, Smoking Code) but don't specify which code systems (ICD-10? SNOMED? RxNorm?) are used, despite the product using e-IMO for clinical terminology.
- **Schema or sample data**: None. No sample C-CDA documents, no XML schemas, no example outputs.
- **Export structure reference**: Links to the generic HL7 C-CDA CCD template rather than providing product-specific mapping documentation.
- **Developer usability**: A developer could not build an import from this documentation. They would need the generic C-CDA specification plus actual export files to reverse-engineer vendor-specific patterns.
- **Machine-readable artifacts**: None. The documentation is a single unstyled HTML page.
- **Maintenance**: Page last modified September 15, 2023; product certified in 2018. Appears to be a static compliance artifact.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

This export covers only the standard C-CDA CCD sections — precisely what you'd get from a transitions-of-care document. For an orthopedic surgery practice with imaging centers, ambulatory surgery centers, PT/OT, and a patient portal, the C-CDA summary misses fundamental data domains. Clinical notes are absent despite a 20+ physician surgical practice. Imaging data is absent despite the practice operating MRI centers. Surgical/operative details are absent despite the practice performing orthopedic surgeries. Family health history, certified under (a)(12), is not in the export. Patient portal messages, certified under (e)(1)/(e)(3), are not in the export. No specialty-specific orthopedic data is included. Even within the sections that are present, field coverage is minimal (e.g., Procedures has only 3 fields: description, date, status).

**Axis 2 — Export approach: Repackaged existing export**

This is unambiguously a repackaged existing export. The vendor's (b)(10) EHI export is their existing C-CDA document generation capability — the same Continuity of Care Document used for transitions of care under (b)(1). Multiple signals confirm this:
1. The export format is explicitly C-CDA CCD (template 2.16.840.1.113883.10.20.22.1.2) — a clinical summary standard, not a bulk data format.
2. The "Structure of Export" section links to the generic HL7 C-CDA template spec rather than vendor-specific documentation.
3. The patient self-service download is described as a "Patient Summary for Transition of Care" — using transitions-of-care language for what should be an EHI export.
4. The 18 sections map exactly to standard C-CDA CCD sections with no extensions or additions.
5. No data domains beyond the C-CDA clinical summary are represented.

### Key Findings

1. **The (b)(10) export is the vendor's existing C-CDA transition-of-care document rebranded.** The documentation, format, sections, and even patient-facing language ("Patient Summary for Transition of Care") all point to the same C-CDA CCD capability used for (b)(1) transitions of care. No purpose-built EHI export exists.

2. **The entire EHI export documentation is a single 5,200-byte HTML file** with 18 C-CDA sections and 68 field names. No descriptions, types, value sets, sample data, or schemas are provided. This is among the thinnest export documentation possible.

3. **Critical data domains are entirely absent** for an orthopedic surgical practice: clinical notes, imaging orders/results, operative/surgical records, orthopedic-specific assessments, family health history (despite (a)(12) certification), and patient portal messages (despite (e)(1)/(e)(3) certification).

4. **The documentation is honest in one respect**: the Immunizations section candidly states "Empty (Immunizations not provided at clinics)" — an appropriate exclusion for an orthopedic practice. This suggests the vendor thought about what they export, making the omission of clinical notes and surgical records more notable.

5. **The product's custom, single-organization nature** provides context but not justification. OrthoplexEMR serves only MKO/SHP and was built by a small IT firm. The minimal documentation effort is understandable given no commercial customer base, but the (b)(10) requirement applies equally to custom and commercial products.

### Summary Stats

    Coverage:        Minimal/stub/unclear
    Approach:        Repackaged existing export
    Export format:   C-CDA (Continuity of Care Document)
    Entities:        18 sections
    Fields:          68
    Descriptions:    0% (0 of 68 fields have descriptions)
    Sample data:     No
    Bulk export:     Yes (population export with scheduling)
    Domains covered: 2 of 15 applicable domains fully covered (Allergies, Vitals); 8 partial; 5 not covered

### Bottom Line

OrthoplexEMR's (b)(10) export is a repackaged C-CDA transition-of-care document with no purpose-built EHI export capability. For an orthopedic surgery practice with imaging centers, ambulatory surgery centers, and a patient portal, the export misses critical data domains including clinical notes, imaging, surgical records, and specialty-specific assessments. A patient receiving this export would get a clinical summary, not their complete health record.
