# EHI Export Analysis: Mendelson Kornblum Orthopedic & Spine Specialists

**Product**: OrthoplexEMR V1
**Analysis date**: 2026-02-15
**CHPL IDs**: 15.04.04.3014.Orth.01.00.1.180101

## 1. Product Context

OrthoplexEMR is a custom-built, single-organization EMR developed by Proactive Technology Management exclusively for Mendelson Kornblum Orthopedic & Spine Specialists (MKO), now operating under the Synergy Health Partners (SHP) brand. It is not commercially sold. The practice is a large multi-site orthopedic group in Southeast Michigan with 20+ physicians across outpatient clinics, ambulatory surgery centers, MRI imaging centers, and physical/occupational therapy sites.

**What the product stores (relevant to export completeness):**
- **Clinical data** (confirmed by ONC certifications): demographics, problem lists/diagnoses (using IMO terminology), medications (via MDToolbox integration), allergies, vital signs, encounters, procedures, lab/test results, immunization records, social history, medical equipment/implantable devices, care team info, goals, health concerns, treatment plans, family health history, clinical quality measure data.
- **Likely stored**: clinical notes (20+ physician practice), imaging orders (certified for CPOE imaging; operates MRI centers), surgical/operative records (orthopedic surgery with ASCs), referral data, patient portal messages (certified for (e)(1)/(e)(3)), Direct messaging documents.
- **Uncertain**: billing/claims data (may reside in a separate system), scheduling, PACS integration, PT/OT records.

This is an orthopedic specialty practice — specialty-specific data (orthopedic assessments, surgical implant details, pain management records, functional outcome measures) would be expected in a complete EHI export.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/Healthinformationexport.html` | Single static HTML page (5,200 bytes) containing all EHI export documentation — export instructions, data dictionary, and patient self-service info. Last modified 2023-09-15. | **Primary artifact** — this is the entirety of the vendor's EHI export documentation |
| `downloads/screenshot-ehi-export-page.png` | Full-page browser screenshot of the HTML page (425 KB) | Confirms HTML content renders correctly; confirms no dynamic content missed |
| `chpl-metadata.json` | CHPL certification details — 34 certified criteria including (b)(10) | Establishes baseline of what the product is certified for |
| `product-research.md` | Background research on MKO/OrthoplexEMR | Provides context on product capabilities and data domains |

**Notable**: There are no downloadable files (no PDFs, ZIPs, schemas, sample data, XLSX, or JSON). The entire EHI export documentation consists of a single 5,200-byte HTML page. The live URL (https://orthoplex.mkoss.com/UserContent/Healthinformationexport.html) was verified as still accessible on 2026-02-15, returning HTTP 200 with unchanged content (Last-Modified: 2023-09-15).

## 3. Export Mechanics

- **Format**: C-CDA (Consolidated Clinical Document Architecture), specifically the Continuity of Care Document (CCD) template (HL7 template 2.16.840.1.113883.10.20.22.1.2)
- **Mechanism**: UI-driven within OrthoplexEMR
  - **Single patient**: History → CCDA tab; download as encrypted ZIP, send via secure email, or send via Direct messaging
  - **Population export**: Utilities → CCDA; configurable export job with scheduling (Run Once, Daily, Weekly, Monthly, Yearly), date range, and scope (All Patients or Single Patient). Output placed on shared server (accessible on MKO network or via SynergyHealth VPN)
- **Patient self-service**: Patients log into portal at `portal.mendelsonortho.com` to download "Patient Summary for Transition of Care"
- **Bulk capability**: Yes — the population export supports all patients with scheduling
- **Access constraints**: Provider must have OrthoplexEMR credentials; population export output requires MKO network or VPN access
- **Fees**: Not mentioned

## 4. Export Content: What's In It

The export is a standard C-CDA Continuity of Care Document. The data dictionary on the HTML page lists **18 C-CDA sections** containing **68 structured fields** across 14 sections with enumerated elements. Four sections are either free-form text or explicitly empty.

There are no data types documented, no descriptions beyond field names, no value sets or code systems specified, no cardinality information, no relationships documented, and no sample data provided. The documentation provides only field names grouped by C-CDA section.

### Vendor's own content organization

The vendor organizes content as C-CDA sections. All counts verified by parsing the HTML programmatically (see `analysis/parsed_sections.json`).

| Section | Fields | Descriptions | Types | Notes |
|---|---|---|---|---|
| Demographics | 9 | None | No | Patient name, DOB, sex, race, language, ethnicity (primary/secondary), contact info, patient ID |
| Document | 4 | None | No | Document ID, created date, author, contact info |
| Encounter | 4 | None | No | Encounter ID, date, responsible party, contact info |
| Document Meta | 2 | None | No | Maintainer, contact info |
| Medications | 9 | None | No | Medication, code, type, strength, dose, route, frequency, date started, status |
| Problems | 4 | None | No | Problem code, patient problem, status, date diagnosed |
| Allergies, Adverse Reactions, Alerts | 5 | None | No | Allergy code, substance, medication/agent allergy, reaction, date entered |
| Vital Signs | 10 | None | No | Date/time, height, weight, BP, pulse, temp, resp, pulse ox, O2 % BldC Ox, inhaled O2 conc |
| Care Team Information | 3 | None | No | Name, position, email |
| Immunizations | 0 | N/A | N/A | Explicitly empty: "Immunizations not provided at clinics" |
| Social History (smoking) | 3 | None | No | Smoking code, smoking status, from/to |
| Medical Equipment | 3 | None | No | Description, date/time, status |
| Results (Tests) | 7 | None | No | Code, code system, name, date, result, lab, provider |
| Procedures | 3 | None | No | Description, date/time, status |
| Goals | 0 (free form) | None | No | Free-form text |
| Health Concerns | 0 (free form) | None | No | Free-form text |
| Plan of Treatment | 2 | None | No | Plan of treatment, assessment |
| Reason for referral | 0 (free form) | None | No | Free-form text |

**Totals**: 18 sections, 68 structured fields, 0 fields with descriptions, 0 fields with type information, 0 value sets documented.

The "Structure of Export" section simply links to the generic HL7 C-CDA CCD template specification — no vendor-specific profile, extensions, or implementation guide is provided.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor covers exactly one thing: a standard C-CDA Continuity of Care Document. This is the same document format used for transitions of care under criterion (b)(1), reused as the (b)(10) EHI export.

The 18 sections map directly to standard C-CDA CCD sections. There are no vendor-specific extensions, no additional data beyond what C-CDA CCD natively supports, and no indication that any orthopedic specialty data, clinical notes, imaging, billing, or other non-CCD data is included.

The sections with the most fields are Vital Signs (10 fields) and Demographics/Medications (9 fields each). Several sections — Goals, Health Concerns, Reason for Referral — contain only free-form text with no structured elements. Immunizations is explicitly empty (appropriate for an orthopedic practice). Encounter data is minimal (4 fields: ID, date, responsible party, contact info) with no encounter type, diagnosis, or clinical detail.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Demographics section: 9 fields (name, DOB, sex, race, language, ethnicity, contact info, patient ID) | Basic demographics present but no address breakdown, emergency contacts, or employer info. Adequate for C-CDA level. |
| Encounters / visits | ⚠️ Partial | Encounter section: 4 fields (ID, date, responsible party, contact info) | Minimal — no encounter type, reason for visit, diagnoses, or clinical details. A 20+ physician multi-site practice generates rich encounter data not captured here. |
| Problems / conditions / diagnoses | ⚠️ Partial | Problems section: 4 fields (code, problem, status, date diagnosed) | Problem list is present but represents only active/resolved summary, not the full diagnostic history per encounter. |
| Medications / prescriptions | ✅ Covered | Medications section: 9 fields (medication, code, type, strength, dose, route, frequency, date started, status) | Reasonably detailed for a summary. Prescribing is via MDToolbox; unclear if full Rx history (fills, refills, prior auths) is captured vs. current medication list. |
| Allergies | ✅ Covered | Allergies section: 5 fields | Present with structured elements. |
| Immunizations | N/A | Explicitly empty: "Immunizations not provided at clinics" | Appropriate for orthopedic specialty. |
| Vitals | ✅ Covered | Vital Signs section: 10 fields including oxygen-related measures | Most detailed section. |
| Lab results | ⚠️ Partial | Results (Tests) section: 7 fields | Summary-level lab results. No specimen info, reference ranges, or result interpretation. |
| Imaging / diagnostic reports | ❌ Not covered | No imaging section in export | Product is certified for CPOE imaging orders (a)(4); practice operates MRI centers. Significant gap for an orthopedic practice. |
| Procedures | ⚠️ Partial | Procedures section: 3 fields (description, date/time, status) | Extremely thin — description-level only. An orthopedic surgery practice generates detailed operative notes, implant records, surgical details. This captures none of that richness. |
| Clinical notes / documents | ❌ Not covered | No clinical notes section in export | A 20+ physician orthopedic practice produces extensive clinical documentation (H&P, progress notes, operative reports, consult notes). Major gap. |
| Care plans / goals | ⚠️ Partial | Goals (free form), Health Concerns (free form), Plan of Treatment (2 fields) | Present but entirely free-form text with no structure. |
| Orders / referrals | ⚠️ Partial | Reason for Referral (free form) | Referral reason as free text only. No structured order data. Product is certified for CPOE (a)(1)–(a)(4). |
| Insurance / coverage | ❌ Not covered | No insurance section in export | Unknown whether product stores insurance data. |
| Claims / billing | ❌ Not covered | No billing section in export | Unknown whether billing is in OrthoplexEMR or a separate system; if in the EMR, this is a gap. |
| Payments | ❌ Not covered | No payment data in export | Same uncertainty as billing. |
| Consents / directives | ❌ Not covered | No consent section in export | Unknown if product stores advance directives. |
| Patient communications / portal messages | ❌ Not covered | No portal message section in export | Product is certified for patient portal (e)(1)/(e)(3). If portal messages are stored, this is a gap. |
| Specialty-specific (orthopedics) | ❌ Not covered | No orthopedic-specific data in export | An orthopedic EMR should contain specialty assessments, range-of-motion measurements, surgical implant details, pain scales, functional outcome scores. None present. |

**Summary**: Of 19 assessed domains, 3 are covered (medications, allergies, vitals), 6 are partially covered (demographics, encounters, problems, lab results, procedures, care plans/goals/referrals), 8 are not covered, 1 is N/A (immunizations), and 1 more is partially covered (orders/referrals as free text). The export covers approximately what a standard C-CDA clinical summary provides — core clinical data at a summary level — but misses clinical notes, imaging, specialty data, and potentially billing.

## 6. Documentation Quality

The documentation quality is **minimal**:

- **Format**: A single unstyled HTML page, 5,200 bytes, 162 lines. No CSS, no JavaScript, no images.
- **Data dictionary**: Field names only. Zero descriptions of what any field contains. Zero data types. Zero value sets or code systems (several fields reference "Code" but don't specify ICD-10, SNOMED CT, RxNorm, LOINC, or other systems). Zero cardinality or constraints. Zero relationship documentation.
- **Schema**: The "Structure of Export" links to the generic HL7 C-CDA CCD template — no vendor-specific profile, implementation guide, or mapping documentation.
- **Sample data**: None. No sample C-CDA documents, no example exports, no test data.
- **Machine-readable artifacts**: None.
- **Developer usability**: A developer could not build an import from this documentation alone. They would need to rely on the generic C-CDA specification and reverse-engineer vendor-specific patterns from actual export files (which are not provided).
- **Maintenance**: Last modified September 15, 2023. Product certified January 1, 2018. The documentation appears to be a static compliance artifact that has been touched once since certification.

The export instructions themselves (how to trigger the export) are reasonably clear step-by-step guides. But the data content documentation — what's actually in the export — is bare-minimum field name enumeration with no supporting detail.

## 7. Overall Assessment

### Classification

**Standard-based projection** — The (b)(10) EHI export is a C-CDA Continuity of Care Document, the same document format used for transitions of care. This is a clinical summary standard, not a comprehensive data export format. It covers roughly the same data as a (g)(10) FHIR US Core API or a (b)(1) transitions-of-care document — the standard USCDI clinical domains at a summary level. The vendor has repackaged their existing C-CDA capability as the EHI export rather than building a native data model export.

### Key Findings

1. **The (b)(10) export is a repackaged C-CDA CCD** — identical in scope to a transitions-of-care document. The export format (C-CDA CCD) is structurally incapable of representing many data types an orthopedic EMR stores (imaging, operative notes, specialty assessments, billing). This is the classic "C-CDA repackaging" failure mode.

2. **No orthopedic specialty data is exported.** For a product purpose-built for an orthopedic surgery practice with ASCs and MRI centers, the absence of any specialty-specific content (surgical implant details beyond generic "Medical Equipment," operative reports, orthopedic assessments, imaging) is a significant gap.

3. **Clinical notes are absent.** The export contains no clinical notes section — no progress notes, H&P, operative reports, consult notes, or discharge summaries. For a 20+ physician practice, this omits a major portion of the patient record.

4. **Documentation is bare-minimum.** 68 field names across 18 sections with zero descriptions, zero type information, zero value sets, zero sample data, and zero machine-readable schemas. The entire documentation fits in a 5 KB HTML file.

5. **Population export with scheduling is a positive feature.** The ability to schedule recurring bulk exports (daily/weekly/monthly/yearly) for all patients is more sophisticated than many vendors offer — but the data scope remains limited to the same C-CDA summary regardless of export method.

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA (CCD template 2.16.840.1.113883.10.20.22.1.2)
Model type:      Standard projection (C-CDA)
Entities:        18 C-CDA sections
Fields:          68 structured fields
Descriptions:    0% (0 of 68 fields have descriptions)
Sample data:     No
Bulk export:     Yes (population export with scheduling)
Domains covered: 3 of 17 applicable domains fully; 6 partially
```

### Bottom Line

OrthoplexEMR's (b)(10) export is a standard C-CDA clinical summary repackaged as an EHI export. A patient or provider would receive a transitions-of-care-level summary — basic demographics, medication list, problem list, allergies, and vitals — but would miss clinical notes, imaging, operative/surgical records, orthopedic-specific assessments, and potentially billing data. For an orthopedic surgery EMR, the gap between what the product stores and what the export delivers is substantial.
