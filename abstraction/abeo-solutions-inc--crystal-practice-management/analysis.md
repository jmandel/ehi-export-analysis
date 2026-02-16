# EHI Export Analysis: Abeo Solutions, Inc

**Product**: Crystal Practice Management v6.0
**Analysis date**: 2026-02-16
**CHPL ID**: 10996 (15.04.04.1030.Crys.06.01.1.221004)

## 1. Product Context

Crystal Practice Management (Crystal PM) is an all-in-one practice management and EHR platform purpose-built for **optometry and ophthalmology** practices. Developed by Abeo Solutions, Inc (a small Austin, TX company with ~12–35 employees), it serves independent and multi-location eye care practices.

The product integrates the following modules, all relevant to assessing export completeness:

- **EHR/Clinical**: 300+ customizable exam templates, eye exam records (refraction, visual acuity, tonometry, slit lamp, fundus), vision therapy, specialty contact lens fitting, diagnostic imaging from 60+ ophthalmic instruments (OCT, visual fields, fundus cameras, autorefractors)
- **Scheduling**: Multi-doctor/multi-location scheduling, waitlists, drag-and-drop calendars
- **Billing & Claims**: Invoice creation, electronic claims submission (Apex, Trizetto, Waystar, VSP), routing slips with diagnosis/CPT tracking, payment posting
- **Vision Insurance (VSP)**: Deep VSP integration for claims, authorizations, and eligibility
- **Optical & Inventory**: Frame and contact lens inventory, RFID support, lab order tracking, barcode scanning
- **E-Prescribing**: Integrated electronic prescribing
- **Patient Engagement**: Patient portal, Crystal Communicator (SMS), Crystal Kiosk (check-in), online forms, secure messaging
- **Direct Messaging**: (h)(1) certified

The designated record set for this product should include: patient demographics, eye exam records (including specialty measurements), medications/prescriptions, allergies, immunizations, problems, procedures, lab results, clinical notes, billing records/invoices/claims, insurance data (especially VSP), optical orders, referrals, images/documents, and patient communications.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/21stCenturyCuresActB10AllDataExportUserDocumentation2.pdf` | 921-page PDF data dictionary. 2.68 MB. Created 2023-10-12 by "Erik" using Microsoft Word 2021. Documents 58 unique database tables (80 entity sections including 23 ehr_file sub-types) exported as CSV files with column-level documentation (name, type, description, extraction method). Also documents 184 serialized .NET type sections with 6,015 member descriptions for complex data stored in binary/XML columns. | **Most informative** — this is the sole artifact and it is exceptionally thorough |
| `product-research.md` | Product research document covering Crystal PM's features and data scope | Useful for baseline |
| `ehi-export-report.md` | Prior agent's analysis of the export documentation | Useful for orientation, verified against primary source |

## 3. Export Mechanics

- **Format**: CSV files — one per database table. Some columns containing serialized .NET objects (stored as XML then binary in the database) are deserialized back to structured form during export. The documentation notes "CSV + Binary Deserialization" or "CSV + XML Deserialization" as extraction methods for these columns.
- **Mechanism**: UI-based ("All Patient Data Export" feature within Crystal PM). The PDF describes it as a user-facing export functionality.
- **Single-patient vs bulk**: The document refers to "all patient data export," suggesting a bulk/full database export rather than single-patient.
- **Access constraints**: No fees or restrictions mentioned. Feature appears built into the product.

## 4. Export Content: What's In It

The export is a **comprehensive database dump** covering 58 unique database tables, presented as 80 documented entity sections (because the `ehr_file` table stores 23 different clinical record sub-types, each documented separately).

### Data Dictionary Statistics

- **Total entity sections**: 80
- **Unique database tables**: 58
- **Total CSV column definitions**: 1,024
- **Total XML sub-field definitions**: 291 (from Custom XML Extraction sections)
- **Total documented fields**: 1,315 (CSV + XML)
- **Fields with descriptions**: 1,315/1,315 (100%)
- **Data types documented**: Yes (MySQL types: int, varchar, char, date, datetime, bigint, longblob, tinyint, text, etc.)
- **Extraction method documented**: Yes (CSV or CSV + Binary/XML Deserialization)
- **Serialized type documentation**: 184 sections documenting .NET object model types with 6,015 member descriptions (for complex clinical data stored in binary columns)
- **Value sets/enumerations**: Partially documented — enum values for specialty types (TargetSiteType: Right/Left/Both; MeasurementType: Distance/Near/Pinhole; StatusType: Uncorrected/Corrected) are explicitly defined; general integer code fields are described but values not enumerated
- **Foreign key relationships**: Implicit — descriptions reference parent tables (e.g., "acctid is the unique patient ID from the 'patients' table") but no formal ERD
- **Sample data**: None provided

### Vendor's Own Content Organization

Based on the vendor's documentation structure:

| Entity/Table | CSV Fields | XML Fields | Total | Category |
|---|---|---|---|---|
| **Patient Demographics** | | | | |
| Patient (`patients`) | 49 | 114 | 163 | Demographics |
| **Clinical - Lab** | | | | |
| Lab Order (`ehr_file`) | 33 | 0 | 33 | Lab |
| Lab Result (`ehr_file`) | 23 | 0 | 23 | Lab |
| Lab Result CCR (`ehr_file`) | 58 | 0 | 58 | Lab |
| **Clinical - Medications** | | | | |
| Medication Order (`ehr_file`) | 15 | 0 | 15 | Medications |
| Formulary (`ehr_file`) | 19 | 0 | 19 | Medications |
| Medication History (`ehr_file`) | 25 | 0 | 25 | Medications |
| Drug Allergy (`ehr_file`) | 16 | 0 | 16 | Medications |
| Drug Allergy History (`ehr_file`) | 16 | 0 | 16 | Medications |
| Drug Interaction (`ehr_file`) | 15 | 0 | 15 | Medications |
| Drug F9 (`ehr_file`) | 15 | 0 | 15 | Medications |
| Medication - External (`ehr_file`) | 28 | 0 | 28 | Medications |
| Drug Allergy - External (`ehr_file`) | 17 | 0 | 17 | Medications |
| **Clinical - Other** | | | | |
| Immunization (`ehr_file`) | 15 | 0 | 15 | Immunizations |
| Observation (`ehr_file`) | 16 | 0 | 16 | Observations |
| Problem (`ehr_file`) | 20 | 0 | 20 | Problems |
| Problem - External (`ehr_file`) | 17 | 0 | 17 | Problems |
| Procedure (`ehr_file`) | 15 | 0 | 15 | Procedures |
| Smoking Status (`ehr_file`) | 15 | 0 | 15 | Social History |
| Implantable Device (`ehr_file`) | 24 | 0 | 24 | Devices |
| Device (`ehr_file`) | 15 | 0 | 15 | Devices |
| Intervention (`ehr_file`) | 15 | 0 | 15 | Interventions |
| Diagnostic Study (`ehr_file`) | 15 | 0 | 15 | Diagnostic Studies |
| Clinical Note (`clinical_note`) | 10 | 0 | 10 | Notes |
| Eye Care Data (`ehr_file`) | 15 | 0 | 15 | Eye Care Specialty |
| **Prescriptions/Medications** | | | | |
| MedComp RX (`mcrx`) | 13 | 0 | 13 | Prescriptions |
| MedComp (`mcs`) | 14 | 28 | 42 | Prescriptions |
| MedComp Log (`mcs_log`) | 12 | 3 | 15 | Prescriptions |
| **Billing & Financial** | | | | |
| Invoice (`invoice`) | 12 | 3 | 15 | Billing |
| Invoice Transaction Item (`inv_trans_items`) | 3 | 0 | 3 | Billing |
| Transaction Payment (`trans_pay`) | 10 | 41 | 51 | Billing |
| Transaction Data (`trans_data`) | 9 | 37 | 46 | Billing |
| HCFA Print (`hcfa_print`) | 8 | 0 | 8 | Billing |
| HCFA Data (`hcfa_data`) | 5 | 28 | 33 | Billing |
| Routing Slip (`rslip`) | 10 | 0 | 10 | Billing |
| **Vision Insurance (VSP)** | | | | |
| VSP Claim (`vsp_claims`) | 86 | 0 | 86 | VSP |
| VSP Authorization (`vsp_authorizations`) | 39 | 0 | 39 | VSP |
| VSP Eligibility (`vsp_eligibility`) | 13 | 0 | 13 | VSP |
| VSP Claim Response (`vsp_claim_response`) | 8 | 0 | 8 | VSP |
| VSP Eligibility Benefit (`vsp_eligibility_benefits`) | 15 | 0 | 15 | VSP |
| VSP Eligibility Service (`vsp_eligibility_services`) | 6 | 0 | 6 | VSP |
| VSP Claim Service (`vsp_claim_services`) | 15 | 0 | 15 | VSP |
| VSP Authorization Service (`vsp_auth_services`) | 6 | 0 | 6 | VSP |
| VSP Authorization Service Grid (`vsp_auth_servicegrid`) | 8 | 0 | 8 | VSP |
| Frame for VSP (`frame_for_vsp`) | 3 | 0 | 3 | VSP |
| **Optical & Inventory** | | | | |
| Frame Page Data (`framepage`) | 9 | 20 | 29 | Optical |
| Frame Page Log (`fp_log`) | 8 | 0 | 8 | Optical |
| Contact Lens Log (`cl_log`) | 8 | 0 | 8 | Optical |
| Contact Lens Order (`contorders`) | 11 | 0 | 11 | Optical |
| Contact Lens RX Notes (`clrx_notes`) | 3 | 0 | 3 | Optical |
| Spectacle RX Notes (`sprx_notes`) | 3 | 0 | 3 | Optical |
| Inventory Log (`inv_log`) | 8 | 0 | 8 | Optical |
| **Scheduling** | | | | |
| Appointment (`appts`) | 26 | 3 | 29 | Scheduling |
| Appointment Waitlist (`appt_waitlist`) | 7 | 0 | 7 | Scheduling |
| Appointment Log (`appt_log`) | 8 | 0 | 8 | Scheduling |
| **Patient Engagement & Communication** | | | | |
| Recall (`recall`) | 4 | 0 | 4 | Engagement |
| Reminder (`reminders`) | 14 | 7 | 21 | Engagement |
| Reminder Log (`rem_log`) | 8 | 0 | 8 | Engagement |
| Comment (`comments`) | 6 | 7 | 13 | Engagement |
| Marketing (`pat_markets`) | 5 | 0 | 5 | Engagement |
| Direct Mail Message (`directmail_message`) | 29 | 0 | 29 | Engagement |
| Kno2 Message (`kno2_message`) | 35 | 0 | 35 | Engagement |
| **Documents & Images** | | | | |
| Patient File (`pat_file`) | 14 | 0 | 14 | Documents |
| Patient File Data (`pat_file_data`) | 2 | 0 | 2 | Documents |
| Medical Image (`med_image_info`) | 10 | 0 | 10 | Documents |
| Medical Image Data (`med_image_data`) | 2 | 0 | 2 | Documents |
| Patient Photo (`pat_photos`) | 2 | 0 | 2 | Documents |
| Patient Photo Info (`pat_photo_info`) | 10 | 0 | 10 | Documents |
| Patient Photo Data (`pat_photo_data`) | 2 | 0 | 2 | Documents |
| Patient Insurance Card (`pat_ins_card`) | 4 | 0 | 4 | Documents |
| Insurance Card Info (`ins_card_info`) | 10 | 0 | 10 | Documents |
| Insurance Card Data (`ins_card_data`) | 2 | 0 | 2 | Documents |
| **Administrative & Compliance** | | | | |
| Alert (`alerts`) | 7 | 0 | 7 | Administrative |
| HIPPA Disclosure (`hippadisc`) | 7 | 0 | 7 | Administrative |
| Authorization Log (`authlogs`) | 4 | 0 | 4 | Administrative |
| Meaningful Use Measure (`mu_measures`) | 5 | 0 | 5 | Administrative |
| Professional Referral (`pro_refrl`) | 19 | 0 | 19 | Administrative |
| Order Group (`order_groups`) | 29 | 0 | 29 | Administrative |
| Result Group (`result_groups`) | 26 | 0 | 26 | Administrative |
| HL7 Record (`hl7_record`) | 18 | 0 | 18 | Administrative |

The full inventory with all field details is in `analysis/entity-inventory-full.json`. Summary statistics are in `analysis/entity-inventory-summary.json`.

### Category Summary

| Category | Entities | CSV Fields | XML Fields | Total Fields |
|---|---|---|---|---|
| Patient Demographics | 1 | 49 | 114 | 163 |
| Clinical - Lab | 3 | 46 | 0 | 46 |
| Clinical - Medications | 9 | 136 | 0 | 136 |
| Clinical - Immunizations | 1 | 15 | 0 | 15 |
| Clinical - Problems | 2 | 31 | 0 | 31 |
| Clinical - Observations | 1 | 16 | 0 | 16 |
| Clinical - Procedures | 1 | 15 | 0 | 15 |
| Clinical - Social History | 1 | 15 | 0 | 15 |
| Clinical - Devices | 2 | 30 | 0 | 30 |
| Clinical - Interventions | 1 | 15 | 0 | 15 |
| Clinical - Diagnostic Studies | 1 | 15 | 0 | 15 |
| Clinical - Notes | 1 | 10 | 0 | 10 |
| Clinical - Eye Care Specialty | 1 | 15 | 0 | 15 |
| Prescriptions/Medications | 3 | 39 | 31 | 70 |
| Billing & Financial | 7 | 48 | 109 | 157 |
| Vision Insurance (VSP) | 10 | 199 | 0 | 199 |
| Optical & Inventory | 7 | 50 | 20 | 70 |
| Scheduling | 3 | 40 | 3 | 43 |
| Patient Engagement & Communication | 7 | 101 | 14 | 115 |
| Documents & Images | 10 | 52 | 0 | 52 |
| Administrative & Compliance | 8 | 87 | 0 | 87 |
| **Total** | **80** | **1,024** | **291** | **1,315** |

**Note on field counts**: The 1,315 CSV + XML fields represent the directly parsed column and XML sub-field definitions. In addition, the PDF documents 184 serialized .NET type sections with 6,015 member descriptions for the complex data stored in binary blob columns (e.g., `ehr_file.data`, `trans_pay.xml`). These members represent the deep clinical data model — for instance, the `StructuredProductType` for medication orders has 52 members, the `LabResult` type has 302 members, `VisualAcuityFieldDataModel` has 60+ members, and `RefractionMeasurementFieldDataModel` has 101 members. Including these, the total documented data points exceeds 7,000.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

Crystal PM's export documentation reveals a database dump that covers virtually every functional module of the product:

**Richest areas:**
- **Vision Insurance (VSP)**: 10 entities, 199 fields — extraordinarily deep coverage of VSP claims, authorizations, eligibility, and associated services. The `vsp_claims` table alone has 86 fields. This is specialty-specific billing data well beyond USCDI.
- **Patient Demographics**: 163 fields (49 CSV + 114 XML) — includes billing-specific demographics, employer, referral source, communication preferences, and financial balances.
- **Billing & Financial**: 7 entities, 157 fields — invoices, transaction payments (51 fields with detailed XML), transaction data (46 fields), HCFA/CMS-1500 claims (33 fields), and routing slips.
- **Medications**: 9 ehr_file sub-types plus 3 MedComp tables = 12 entities, 206 fields — covering medication orders, history, allergies, interactions, formulary, and e-prescribing data. The serialized `StructuredProductType` adds 52 deeply documented members.
- **Patient Engagement**: 7 entities, 115 fields — recall, reminders, direct mail, Kno2 messages, comments, and marketing records.

**Moderate coverage:**
- **Scheduling**: 3 entities, 43 fields — appointments (29 fields including XML), waitlist, and appointment log.
- **Optical & Inventory**: 7 entities, 70 fields — frame pages, contact lens orders/logs, spectacle RX notes, inventory tracking.
- **Documents & Images**: 10 entities, 52 fields — medical images, patient files, patient photos, and insurance cards (all with both metadata and binary data tables).
- **Lab**: 3 entities, 46 fields — plus extensive serialized type documentation (LabResult type: 302 members).

**Thinnest areas:**
- **Clinical Notes**: 1 entity, 10 CSV fields — basic metadata; actual content is in the serialized `ClinicalNote` type (12 members).
- **Eye Care Specialty**: 1 entity, 15 CSV fields — but backed by 60+ members in `VisualAcuityFieldDataModel` and 101 members in `RefractionMeasurementFieldDataModel`.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `patients` (163 fields total), including billing demographics, contacts, employer, SSN, communication preferences, financial balances | Thorough |
| Encounters / visits | ⚠️ Partial | `appts` (29 fields), `appt_log` (8 fields) capture appointment data; `rslip` (routing slips) tracks patient flow through visits. No dedicated encounter/visit table. | Appointments and routing slips serve as encounter proxies. Adequate for this practice type. |
| Problems / conditions / diagnoses | ✅ Covered | `ehr_file` Problem (20 fields), Problem - External (17 fields); `MedRecProblem` serialized type (58 members) | Thorough |
| Medications / prescriptions | ✅ Covered | `ehr_file` Medication Order (15 fields + `StructuredProductType` 52 members), Medication History (25 fields), Medication - External (28 fields); `mcrx` (13 fields), `mcs` (42 fields), `mcs_log` (15 fields) | Very thorough — 12 entities covering orders, history, and e-prescribing |
| Allergies | ✅ Covered | `ehr_file` Drug Allergy (16 fields), Drug Allergy History (16 fields), Drug Allergy - External (17 fields), Drug Interaction (15 fields), Drug F9 (15 fields); `DrugAllergy` type (77 members) | Thorough |
| Immunizations | ✅ Covered | `ehr_file` Immunization (15 fields); `Immunization` serialized type (32 members) | Adequate |
| Vitals | ⚠️ Partial | No dedicated vitals table. Vitals data likely stored within `ehr_file` Observation sub-type (16 fields) or within exam templates. `Observation` serialized type has 139 members. | Product supports vitals via EHR templates; data is likely in observation records but no explicit vitals entity |
| Lab results | ✅ Covered | `ehr_file` Lab Order (33 fields), Lab Result (23 fields), Lab Result CCR (58 fields); `LabResult` type (302 members); `order_groups` (29 fields), `result_groups` (26 fields) | Very thorough |
| Imaging / diagnostic reports | ✅ Covered | `ehr_file` Diagnostic Study (15 fields); `med_image_info` (10 fields), `med_image_data` (2 fields + binary); `MedRecDiagnosticStudy` type (40 members) | Product integrates 60+ ophthalmic devices; imaging data and metadata are exported |
| Procedures | ✅ Covered | `ehr_file` Procedure (15 fields); `MedRecProcedure` type (55 members) | Adequate |
| Clinical notes / documents | ✅ Covered | `clinical_note` (10 fields); `ClinicalNote` type (12 members); `pat_file`/`pat_file_data` for attached documents | Adequate; actual note content is in serialized type |
| Care plans / goals | ⚠️ Partial | `ehr_file` Intervention (15 fields); `MedRecIntervention` type (37 members). No dedicated care plan entity. | Interventions are exported; care plans may not be a core feature of this optometry product |
| Orders / referrals | ✅ Covered | `order_groups` (29 fields); `result_groups` (26 fields); `pro_refrl` (19 fields) | Professional referrals and order/result groups are exported |
| Insurance / coverage | ✅ Covered | `patients` table includes insurance fields; `pat_ins_card`/`ins_card_info`/`ins_card_data` for insurance card images; 10 VSP entities (199 fields total) for vision insurance | Exceptionally thorough for vision insurance |
| Claims / billing | ✅ Covered | `invoice` (15 fields), `inv_trans_items` (3 fields), `trans_pay` (51 fields), `trans_data` (46 fields), `hcfa_print` (8 fields), `hcfa_data` (33 fields), `vsp_claims` (87 fields) | Very thorough — covers CMS-1500 claims, VSP claims, invoices, and payment transactions |
| Payments | ✅ Covered | `trans_pay` (51 fields including 41 XML sub-fields for detailed payment data) | Thorough |
| Consents / directives | ⚠️ Partial | `hippadisc` (7 fields) tracks HIPAA disclosures. No dedicated consent form table. | HIPAA disclosures are tracked; consent forms may be stored as patient files |
| Patient communications / portal messages | ✅ Covered | `directmail_message` (29 fields), `kno2_message` (35 fields), `comments` (13 fields), `reminders` (21 fields), `rem_log` (8 fields) | Thorough — covers direct messages, Kno2 secure messages, and reminders |
| Specialty-specific (Eye Care) | ✅ Covered | `ehr_file` Eye Care Data (15 fields) + `VisualAcuityFieldDataModel` (60+ members including TargetSiteType, MeasurementType, StatusType enums) + `RefractionMeasurementFieldDataModel` (101 members). Also: `framepage` (29 fields), `cl_log`, `contorders`, `clrx_notes`, `sprx_notes` for optical data. `frame_for_vsp` for VSP frame data. | **Exceptionally thorough** — this is the standout feature. Eye care measurement models are documented down to enum values. |

**Summary**: Of 18 applicable domains, 13 are fully covered (✅), 4 are partially covered (⚠️), and 0 are uncovered (❌). The partial coverages (vitals, encounters, care plans, consents) reflect the product's optometry focus — these are not major workflow areas for eye care practices rather than true gaps.

## 6. Documentation Quality

**Strengths:**
- **Comprehensive data dictionary**: Every column in every exported table has a name, MySQL data type, prose description, and extraction method. 100% of 1,315 CSV + XML fields have descriptions.
- **Serialized type documentation**: The documentation of .NET object models for complex data (6,015 members across 184 type sections) is unusually thorough. Most vendors would simply export binary blobs; Crystal PM documents the full object hierarchy including enum values.
- **Specialty data models**: VisualAcuityFieldDataModel and RefractionMeasurementFieldDataModel are documented with clinically meaningful enum values (TargetSiteType: Right/Left/Both; MeasurementType: Distance/Near/Pinhole; StatusType: Uncorrected/Corrected).
- **Clear structure**: Each table section follows a consistent format. The document is well-organized by functional area.

**Weaknesses:**
- **No sample data**: No example CSV files or sample records are provided.
- **No ERD/relationship diagram**: Foreign key relationships are described in prose ("acctid is the unique patient ID from the 'patients' table") but no formal entity-relationship diagram exists.
- **Incomplete value sets**: Integer code fields (e.g., `type`, `recall_type`, `sub_type`) are described as "represents the type of..." but valid values are not enumerated (except for the eye care specialty enums).
- **No machine-readable schema**: The data dictionary is only in PDF format — no JSON schema, SQL DDL, or other machine-readable format.
- **Single monolithic PDF**: At 921 pages, the document is thorough but difficult to navigate programmatically.

**Developer usability**: A developer could build an import system from this documentation. The column names, types, and descriptions provide sufficient context for most tables. The serialized type documentation enables reconstruction of complex clinical data. The main challenge would be discovering coded values for integer fields through the data itself.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

Crystal PM's export covers the full breadth of what this product stores. For an optometry-focused practice management system, the export includes:
- Complete clinical data across 23 ehr_file sub-types (not just USCDI — also eye care specialty data, drug interactions, external records)
- Full billing cycle: invoices, payments, transaction data, CMS-1500 claims, VSP claims
- Deep vision insurance integration (10 VSP entities with 199 fields)
- Optical inventory and ordering data (frames, contact lenses, lab orders)
- Patient engagement data (recalls, reminders, messages, marketing)
- Documents and images with binary data
- Scheduling data with appointment history

This goes well beyond USCDI. The VSP insurance tables alone (199 fields) represent domain-specific billing data that has no USCDI equivalent. The eye care measurement models (visual acuity, refraction) are specialty clinical data unique to this product. The export covers billing, insurance, optical inventory, scheduling, and patient engagement — all non-USCDI domains that this product manages.

**Axis 2 — Export approach: Purpose-built EHI export**

This is unambiguously a purpose-built (b)(10) export. The signals are clear:
1. **Native database dump**: The export uses CSV files mapped to the product's internal MySQL tables, not FHIR or C-CDA
2. **Covers non-clinical domains**: Billing (invoices, payments, HCFA claims), vision insurance (VSP claims/authorizations/eligibility), optical inventory, scheduling, patient engagement — none of these are available through the FHIR (g)(10) API
3. **921-page purpose-written documentation**: A document this size, specifically titled "21st Century Cures Act B.10 All Patient Data Export Documentation," was clearly built for (b)(10) compliance
4. **Binary deserialization**: The export process deserializes complex .NET binary objects from the database rather than simply exporting standard clinical exchange formats
5. **Specialty data models documented**: The VisualAcuityFieldDataModel and RefractionMeasurementFieldDataModel documentation represents eye care-specific data that has no standard exchange format equivalent

### Key Findings

1. **Genuinely comprehensive database export**: 58 unique tables covering clinical, billing, insurance, optical, scheduling, engagement, and document data — this is a real database dump, not a repackaged clinical summary.

2. **Standout specialty data documentation**: The serialized .NET type documentation (6,015 members across 184 type sections) for eye care measurements, medication structures, and lab results goes far beyond what most vendors provide. This enables actual reconstruction of complex clinical data.

3. **Deep vision insurance coverage**: 10 VSP-specific entities with 199 fields (including `vsp_claims` at 86 fields) demonstrate that billing and insurance data — often the biggest gap in (b)(10) exports — is thoroughly exported.

4. **100% field description coverage**: Every one of the 1,315 CSV + XML fields has a prose description. No field is left undocumented.

5. **Missing value set enumerations**: The primary documentation gap is that integer code fields (type codes, status codes, classification codes) are described in prose but their valid values are not listed, requiring discovery through the data itself.

### Summary Stats

```
Coverage:        Comprehensive
Approach:        Purpose-built EHI export
Export format:   CSV (with binary/XML deserialization for complex columns)
Entities:        80 (58 unique tables; 23 ehr_file sub-types)
Fields:          1,315 (CSV + XML) + 6,015 serialized type members = ~7,300 documented data points
Descriptions:    100% (1,315/1,315 CSV+XML fields)
Sample data:     No
Bulk export:     Yes (all patient data)
Domains covered: 13 of 18 fully, 4 partially (17 of 18 at least partially)
```

### Bottom Line

Crystal PM's (b)(10) export is one of the strongest implementations from a small vendor. A patient or provider would get a genuinely complete copy of their data — clinical records, billing, insurance claims, optical orders, prescriptions, images, and eye care-specific measurements — all documented at the field level. The single biggest strength is the depth of specialty data documentation (eye care measurements, serialized clinical objects); the single biggest gap is the absence of enumerated value sets for coded fields.
