# EHI Export Analysis: Mendelson Kornblum Orthopedic & Spine Specialists

**Product**: OrthoplexEMR V1
**Analysis date**: 2026-02-16
**CHPL IDs**: 9349 (15.04.04.3014.Orth.01.00.1.180101)

## 1. Product Context

OrthoplexEMR is a custom-built, single-organization EMR developed by Proactive Technology Management for Mendelson Kornblum Orthopedic & Spine Specialists (MKO), now operating under the Synergy Health Partners (SHP) umbrella. The product is not commercially sold and serves only this one practice group.

MKO/SHP is a large multi-site orthopedic practice in Southeast Michigan with 20+ physicians spanning orthopedic surgery, spine, pain management, podiatry, and physical/occupational therapy. The practice operates outpatient clinics, ambulatory surgery centers, MRI imaging centers, and PT/OT sites.

**Data the product is expected to store** (based on certification criteria and practice context):
- **Core clinical**: Demographics, problems/diagnoses (via IMO terminology), medications (via MDToolbox e-prescribing), allergies, vitals, encounters, procedures, lab results, implantable devices
- **Orthopedic specialty**: Operative notes, surgical records, implant tracking, orthopedic assessments, functional outcome measures, pain scales
- **Notes/documents**: Progress notes, H&P, consult notes, operative reports for a 20+ physician surgical practice
- **Imaging**: Orders and possibly results (certified for CPOE imaging; operates MRI centers)
- **Patient engagement**: Portal messages, patient-submitted health information (certified for (e)(1) and (e)(3))
- **Family health history**: Certified for (a)(12)
- **Care transitions**: C-CDA documents via EMRDirect
- **Billing/claims**: Unclear whether billing is in OrthoplexEMR or a separate system; the practice founder's IT partner has expertise in medical billing systems

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/Healthinformationexport.html` | Single HTML page (5,200 bytes), last modified 2023-09-15. Contains export instructions and a field-level listing of 18 C-CDA sections. **This is the entirety of the vendor's EHI export documentation.** | Primary artifact — only source of export content detail |
| `downloads/screenshot-ehi-export-page.png` | Full-page browser screenshot of the HTML page (426 KB). Confirms rendering matches raw HTML parse. | Confirmatory |
| `files.json` | Manifest confirming only 2 files were collected; no PDFs, schemas, sample data, or additional documentation exist. | Confirms scope |
| `product-research.md` | Background research on the practice and product. | Context for coverage assessment |
| `ehi-export-report.md` | Prior agent's narrative analysis. | Orientation; verified independently |

**Verification notes:**
- The EHI export URL (`https://orthoplex.mkoss.com/UserContent/Healthinformationexport.html`) was confirmed live on 2026-02-16, returning HTTP 200 with identical content (5,200 bytes, Last-Modified: 2023-09-15).
- No additional downloadable files (PDFs, ZIPs, schemas, sample data) are linked from or associated with the page. The prior report's claim that "the entire documentation is the single HTML page" is confirmed.
- The page contains exactly two outbound links: one to the HL7 C-CDA template specification and one to the patient portal login.

## 3. Export Mechanics

- **Format**: C-CDA (Consolidated Clinical Document Architecture), specifically the Continuity of Care Document (CCD) template `2.16.840.1.113883.10.20.22.1.2`
- **Single-patient export**: Provider navigates to patient chart → History → CCDA. Can download as encrypted ZIP, send via secure email, or send via Direct messaging.
- **Bulk/population export**: Provider navigates to Utilities → CCDA, creates a named export job with configurable frequency (once/daily/weekly/monthly/yearly), date range, and scope (all patients or single patient). Output placed on a shared server accessible within the MKO network or via SynergyHealth VPN.
- **Patient self-service**: Patients log into `portal.mendelsonortho.com` to download a "Patient Summary for Transition of Care."
- **Access constraints**: Population export requires MKO network or VPN access. No mention of fees.

## 4. Export Content: What's In It

The export is a standard C-CDA Continuity of Care Document. The documentation lists 18 named sections with 71 total field names. No fields have descriptions, data types, value sets, cardinality, or relationship documentation. Three sections are designated "free form" (Goals, Health Concerns, Reason for referral) and one (Immunizations) is explicitly empty.

There are no sample data files, no machine-readable schemas, and no documentation beyond field names.

### Vendor's own content organization

The vendor organizes the export into C-CDA sections. The complete inventory (extracted via `analysis/parse_ehi_page.py` → `analysis/full-entity-inventory.json`):

| Section (vendor's name) | Fields | Descriptions | Types | Notes |
|---|---|---|---|---|
| Demographics | 9 | 0 | 0 | Patient name, DOB, sex, race, language, ethnicity, contact info, ID |
| Document | 4 | 0 | 0 | C-CDA document metadata |
| Encounter | 4 | 0 | 0 | ID, date, responsible party, contact |
| Document Meta | 2 | 0 | 0 | Maintainer, contact |
| Medications | 9 | 0 | 0 | Medication, code, type, strength, dose, route, frequency, date, status |
| Problems | 4 | 0 | 0 | Code, problem, status, date diagnosed |
| Allergies, Adverse Reactions, Alerts | 5 | 0 | 0 | Code, substance, medication/agent, reaction, date |
| Vital Signs | 10 | 0 | 0 | Standard vitals including pulse ox, O2 measurements |
| Care Team Information | 3 | 0 | 0 | Name, position, email |
| Immunizations | 0 | 0 | 0 | Explicitly empty — "not provided at clinics" |
| Social History (smoking) | 3 | 0 | 0 | Smoking only — no other social history |
| Medical Equipment | 3 | 0 | 0 | Description, date, status |
| Results (Tests) | 7 | 0 | 0 | Code, code system, name, date, result, lab, provider |
| Procedures | 3 | 0 | 0 | Description, date, status |
| Goals | 1 | 0 | 0 | Free-form text |
| Health Concerns | 1 | 0 | 0 | Free-form text |
| Plan of Treatment | 2 | 0 | 0 | Plan, assessment |
| Reason for referral | 1 | 0 | 0 | Free-form text |
| **Totals** | **71** | **0** | **0** | |

**Summary statistics:**
- 18 C-CDA sections
- 71 named fields across all sections
- 0 fields with descriptions (0%)
- 0 fields with data type documentation (0%)
- 0 value sets or code system specifications documented
- 0 relationship/foreign key documentation
- 0 sample data files

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export maps directly to standard C-CDA CCD sections — this is not a native data model export but a projection into a clinical summary standard. The content is organized into the standard CCD sections one would expect from any transitions-of-care document:

- **Structured clinical data** (Demographics, Medications, Problems, Allergies, Vitals, Results, Procedures, Medical Equipment, Care Team, Social History): These sections have named fields but are thin — 3-10 fields each, with no descriptions, types, or code systems specified.
- **Free-form text sections** (Goals, Health Concerns, Plan of Treatment, Reason for referral): Labeled "(free form)" with no field structure.
- **Explicitly absent** (Immunizations): Vendor candidly notes immunizations are not provided at their orthopedic clinics.
- **Document metadata** (Document, Document Meta, Encounter): Standard C-CDA document context, not clinical content.

The total of 71 fields across 18 sections is characteristic of a clinical summary document, not a comprehensive data export. For context, a typical EMR's native database has hundreds to thousands of fields across dozens to hundreds of tables.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Demographics section: 9 fields (name, DOB, sex, race, language, ethnicity, contact, ID) | Basic demographics present but thin for a multi-site practice — no address breakdown, no emergency contacts, no employer info |
| Encounters / visits | ⚠️ Partial | Encounter section: 4 fields (ID, date, responsible party, contact) | Minimal — no encounter type, location, diagnosis, disposition, or duration |
| Problems / conditions | ⚠️ Partial | Problems section: 4 fields (code, problem, status, date) | Present but without specifying code system (ICD-10? SNOMED? IMO?) |
| Medications / prescriptions | ✅ Covered | Medications section: 9 fields including code, type, strength, dose, route, frequency, status | Reasonable for C-CDA; prescribing detail via MDToolbox may not be fully captured |
| Allergies | ✅ Covered | Allergies section: 5 fields | Standard allergy data present |
| Immunizations | N/A | Explicitly empty — vendor states immunizations not provided at clinics | Appropriate for orthopedic specialty |
| Vitals | ✅ Covered | Vital Signs section: 10 fields including standard vitals and O2 measures | Reasonably thorough vital sign set |
| Lab results | ⚠️ Partial | Results (Tests) section: 7 fields | Basic results present; no reference ranges, units, or interpretation flags documented |
| Imaging / diagnostic reports | ❌ Not covered | No imaging section in export | Product is certified for CPOE imaging (a)(4) and practice operates MRI centers; significant gap |
| Procedures | ⚠️ Partial | Procedures section: 3 fields (description, date, status) | Minimally thin for an orthopedic surgery practice — no procedure codes, no surgeon, no operative details |
| Clinical notes / documents | ❌ Not covered | No notes/documents section in export | A 20+ physician surgical practice generates extensive clinical notes; major gap |
| Care plans / goals | ⚠️ Partial | Goals (free form), Health Concerns (free form), Plan of Treatment (2 fields) | Present but only as free-form text; certified for (b)(11) care plan |
| Orders / referrals | ⚠️ Partial | Reason for referral (free form) | Only free-form referral text; no order data |
| Insurance / coverage | ❌ Not covered | No insurance entities in export | Unknown if product stores insurance data; possible gap |
| Claims / billing | ❌ Not covered | No billing entities in export | Unknown if billing is in OrthoplexEMR; possible gap |
| Payments | ❌ Not covered | No payment entities in export | Unknown if payments are in OrthoplexEMR |
| Consents / directives | ❌ Not covered | No consent section in export | Surgical practice likely collects consent data |
| Patient communications / portal messages | ❌ Not covered | No communications section in export | Product is certified for patient portal (e)(1)/(e)(3); gap if portal messages are stored |
| Specialty-specific (orthopedic) | ❌ Not covered | No specialty data in export | Orthopedic assessments, functional outcomes, pain scales, implant details, surgical logs — none present. Medical Equipment section has only 3 generic fields. |
| Family health history | ❌ Not covered | No family history section in export | Certified for (a)(12) family health history; gap |

## 6. Documentation Quality

The documentation is exceptionally thin:

- **Data dictionary**: Present only as a list of field names per C-CDA section. No descriptions, no data types, no cardinality, no constraints, no value sets, no code system identifiers (despite fields named "Code," "Problem Code," "Allergy Code," "Smoking Code").
- **Schema**: The only structural reference is a link to the generic HL7 C-CDA CCD template specification — no vendor-specific profile, no extensions, no implementation guide.
- **Sample data**: None provided.
- **Machine-readable artifacts**: None. The documentation is a single unstyled HTML page.
- **Developer usability**: A developer could not build an import from this documentation alone. They would need to rely on the generic C-CDA specification and reverse-engineer vendor-specific patterns from actual export files, which are not provided.
- **Maintenance**: The page was last modified September 15, 2023. The product was certified January 1, 2018. The documentation appears to be a static compliance artifact that has seen minimal updates.

## 7. Overall Assessment

### Classification

**Standard-based projection**

The export is a standard C-CDA Continuity of Care Document being presented as the (b)(10) EHI export. It covers the clinical summary domains one would expect from any transitions-of-care document (demographics, medications, problems, allergies, vitals, labs, procedures) but does not attempt to export the full breadth of data an orthopedic EMR stores. This is functionally equivalent to the (b)(1) transitions of care export, not a genuine "all EHI" export as required by (b)(10).

### Key Findings

1. **C-CDA repackaging as (b)(10)**: The export is explicitly a C-CDA CCD — the same document format used for transitions of care under (b)(1). The vendor links to the standard HL7 CCD template and describes the same export mechanism (History → CCDA) for both single-patient and population exports. This is a textbook example of repurposing an existing clinical summary as an "all EHI" export.

2. **Critical data domains missing**: For an orthopedic surgery practice with ASCs and MRI centers, the export omits clinical notes, imaging data, operative/surgical records, specialty-specific orthopedic data (assessments, implant details, functional outcomes), family health history (certified under (a)(12)), and patient portal communications (certified under (e)(1)/(e)(3)).

3. **Documentation is minimal**: 71 field names across 18 sections, with zero descriptions, zero type specifications, zero value sets, and zero sample data. The entire documentation is a single 5,200-byte HTML page last updated in 2023.

4. **Bulk export capability exists**: The population export feature with scheduling (daily/weekly/monthly/yearly) and date ranges is a useful operational capability, though the underlying data scope remains the same narrow C-CDA summary.

5. **Vendor candidness on immunizations**: The vendor honestly notes that immunizations are "not provided at clinics," which is appropriate for an orthopedic specialty. However, this candor about one small domain highlights the absence of any acknowledgment of the much larger missing domains.

### Summary Stats

    Classification:  Standard-based projection
    Export format:   C-CDA (CCD template 2.16.840.1.113883.10.20.22.1.2)
    Model type:      Standard projection (C-CDA)
    Entities:        18 C-CDA sections
    Fields:          71
    Descriptions:    0% (0 of 71 fields have descriptions)
    Sample data:     No
    Bulk export:     Yes (population export with scheduling)
    Domains covered: 5 of 17 applicable domains (fully); 6 partial

### Bottom Line

OrthoplexEMR's EHI export is a standard C-CDA clinical summary repackaged as a (b)(10) export. For a multi-site orthopedic surgery practice with 20+ physicians, ambulatory surgery centers, and MRI centers, exporting only 71 fields across standard CCD sections — with no clinical notes, no operative records, no imaging, no specialty orthopedic data, and no documentation beyond field names — represents a significant gap between the regulatory requirement to export "all electronic health information" and what is actually provided. The single biggest gap is the complete absence of clinical notes and surgical records from a surgical specialty practice.
