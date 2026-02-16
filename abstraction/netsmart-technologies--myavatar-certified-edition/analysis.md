# EHI Export Analysis: Netsmart Technologies

**Product**: myAvatar Certified Edition  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 11575 (15.04.04.2816.myAv.05.08.1.241227)

## 1. Product Context

myAvatar is a behavioral health EHR designed for community mental health centers, psychiatric hospitals, substance abuse/addiction treatment programs, methadone clinics, CCBHCs, and residential treatment facilities. It is the flagship behavioral health product from Netsmart Technologies, the dominant vendor in this sector (754,000+ users across product lines).

The product spans clinical documentation (progress notes, treatment plans, clinical assessments), medication management (closed-loop Rx including methadone/MAT, e-prescribing, eMAR), CPOE for labs/medications/diet/seclusion-restraint orders, scheduling, and comprehensive billing/revenue cycle management (CMS-1500, UB-04, 837I/P, 835, eligibility, denial management). Behavioral health-specific capabilities include seclusion/restraint tracking, detoxification management, acuity scoring, 42 CFR Part 2 consent management, group therapy documentation, and deep integration with state behavioral health reporting systems (NY PAS, GA ASO, FL FSR, etc.). The product also connects to myHealthPointe (patient portal), CareConnect (interoperability engine), and the Bells AI ambient documentation assistant.

For EHI export assessment, the baseline expectation includes: clinical records, medication/pharmacy data, billing/financial records, behavioral health-specific documentation, treatment plans, diagnoses, labs/orders, scheduling data, consent management, and state-specific reporting data.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/EHI Export All Tables - September 2023.pdf` | 7,492-page PDF data dictionary documenting 561 unique database tables across 13 schemas. Author: Dru Anne Walz. Created 2023-10-02 via Microsoft Word. 16 MB. | **Primary artifact** — contains the complete data dictionary |
| `downloads/ehi-export-all-tables.txt` | Plain text extraction via `pdftotext` (318,819 lines). Used as input for parsing. | High — machine-parseable text of the PDF |
| `downloads/ehi-all-data-myavatar.html` | HTML of the myAvatar EHI export page at ntst.com. Describes the export mechanism, format, and links to the ZIP download. | Medium — provides export mechanics context |
| `downloads/EHI_Export_All_Tables_myAvatar_September_2023.zip` | ZIP archive containing the PDF. 12.5 MB. | Container only |
| `downloads/ehi-page-screenshot.png` | Browser screenshot of the EHI documentation page. | Low — visual confirmation of page layout |
| `downloads/enrichment/tables.json` | Prior agent's structured extraction of 906 form-table pairs (13 MB). | Reference — used to cross-check my own parse |
| `downloads/enrichment/coverage-summary.json` | Prior agent's aggregate statistics. | Reference — used to validate my counts |

## 3. Export Mechanics

- **Format**: Proprietary delimited file format native to myAvatar. Each database table exports to its own file with a filename matching the table name. The specific delimiter, encoding, escaping rules, null handling, and header format are not specified in the documentation.
- **Mechanism**: Manual one-time export via UI. The EHI page states: "EHI Export functionality allows organizations to do a manual one-time export of health data for one or more patients."
- **Scope**: Single-patient or multi-patient ("one or more patients").
- **Bulk capability**: Not explicitly documented as bulk/batch. Described as "manual one-time export."
- **Access constraints**: No fees or special access mentioned. Export is performed by the organization, not vendor-assisted.
- **Rich content handling**: The page explicitly notes that "some electronic health information might not be available in a table format, such as rich text documents or images. This information is referenced in the extracts created for subsequent export." Binary content is included by reference rather than inline.
- **Distinction from FHIR API**: The page explicitly directs users to the Netsmart Developer Portal for FHIR API documentation and to "Information Sharing" for HL7/web service APIs, clearly separating this EHI export from their (g)(10) FHIR API.

## 4. Export Content: What's In It

### Data dictionary scope

The PDF documents **561 unique database tables** across **13 database schemas**, exposed through **217 distinct UI forms** (906 form-table pairs, since one table may appear under multiple forms). After deduplication across forms, there are **33,474 unique columns** (the prior enrichment's count of 71,903 columns reflects counting each column every time the same table appears under a different form).

- **Columns with descriptions**: 26,047 (77.8%)
- **Columns without descriptions**: 7,427 (22.2%)
- **Columns with max_length specified**: 28,229 (84.3%)
- **Column types documented**: Yes — varchar, integer, numeric, date, time, timestamp

Each table entry includes: form name (UI context), fully-qualified table name (schema.table), table description, and per-column detail (name, type, max length, description). A glossary explains common field patterns (PATID, FACILITY, EPISODE_NUMBER, JOIN_TO/LINK_TO relationships, ss_ fields for site-specific data, data_entry_* audit fields).

No machine-readable schema (DDL, XSD, JSON Schema) is provided. No sample data or sample export files are included. No value set enumerations are provided — coded fields use a pattern of `xxx_CODE` + `xxx_value` pairs, but valid values are not listed.

### Vendor's own content organization

The data dictionary is organized by **form** (UI screen), not by domain. Tables are prefixed by schema. The 13 schemas reflect the product's architecture:

| Schema | Tables | Columns | Purpose |
|---|---|---|---|
| SYSTEM | 437 | 24,311 | Core myAvatar tables (clinical, billing, demographic, scheduling, etc.) |
| STATEFORM | 60 | 4,084 | State-specific behavioral health reporting (NY, GA, FL, CA, MI, IN, KS, LA, OH, WA) |
| OrderEntry | 25 | 1,790 | CPOE and order management |
| CWSTEMP | 8 | 1,993 | Clinical Workstation temporary/pre-filing storage |
| DocR | 7 | 188 | Document routing rules |
| Methadone | 6 | 236 | Methadone/MAT medication management |
| INCIDENT | 5 | 276 | Incident reporting |
| eMAR | 5 | 97 | Electronic medication administration records |
| LAPROV | 3 | 91 | Louisiana provider-specific tables |
| HL7 | 2 | 40 | HL7 integration/external ID mapping |
| CWSOrderEntry | 1 | 225 | Clinical Workstation order entry |
| CWSSF | 1 | 114 | Florida state-specific (CWS) |
| GL | 1 | 29 | General ledger |

### Category breakdown (by data domain)

Tables often span multiple categories. The following shows coverage by domain:

| Category | Tables | Columns | Representative Tables |
|---|---|---|---|
| Demographics & Patient | 168 | 15,288 | `patient_current_demographics` (331 cols), `patient_demographic_history` (342 cols), `client_enrollment`, `episode_history` |
| Billing & Financial | 159 | 10,691 | `billing_tx_charge_detail` (51 cols), `billing_tx_history`, `billing_claim_history_tx_detail`, `billing_835_auto_log`, `file_import_gpbdt_i837` (378 cols) |
| State-Specific Reporting | 63 | 4,236 | `nys_pas44_admit`, `ga_aso_discharge` (425 cols), `florida_fsr_mh_outcomes`, `mich_county_bill_census` |
| Clinical Notes & Documents | 51 | 6,916 | `cw_patient_notes_supp_5` (324 cols), `cw_scratch_notes`, `significant_finding_note`, `service_doc_corrections` |
| Diagnoses | 44 | 5,679 | `client_diagnosis_record`, `client_diagnosis_entry`, `Audit_client_diagnosis_record` |
| Labs & Orders | 43 | 2,794 | `history_client_order` (445 cols), `med_regimen_review_detail` (350 cols), `aoe_answers`, `consent` |
| Scheduling & Appointments | 37 | 2,117 | `AppointmentData`, `appt_data`, `telehealth_appt`, `check_in_clients` |
| Staff & Provider | 25 | 1,482 | `RADplus_audit_teams`, `staff_tx_history` |
| Health History | 22 | 1,240 | `amputations`, `client_condition_preg`, `client_condition_delivery` |
| Medications & Pharmacy | 22 | 1,170 | `history_client_med_order`, `history_client_dispense`, `billing_ncpdp_resp_dtl`, `med_regimen_review_detail` |
| Referral & Transfer | 22 | 641 | `carefabric_referrals`, `referral_consent`, `episode_history` |
| Service Authorization | 19 | 1,436 | `history_provider_auths` (335 cols), `history_fund_auth`, `history_member_auths_2` |
| Behavioral Health Specific | 15 | 567 | `acuity_compile`, `acuity_domain_score`, `incidents_clients`, `incidents_audit` |
| Interoperability | 12 | 284 | `carefabric_fhir_encounter`, `ccd_export_log`, `external_client_id` |
| Bed Management | 10 | 332 | `history_bed_assignment`, `history_patient_movement`, `table_bed` |
| Treatment & Care Plans | 10 | 388 | `Clinical_Pathway_Enrollments`, `tx_disch_summary`, `non_administered_treatment` |
| Consent & Disclosure | 9 | 196 | `RADplus_client_consents`, `audit_consent_for_access`, `disclo_mgmt_req_org` |
| Vitals & Observations | 6 | 284 | `cw_vital_signs`, `cw_observation_details`, `history_client_height_weight` |
| Allergies | 5 | 146 | `cw_client_allergies_review`, `cw_hist_client_allergies`, `cw_client_clinical_info` |
| Immunizations | 4 | 180 | `cw_immunization_history`, `cw_hm_alerts_immunization`, `cw_immunization_cust_def` |
| Other | 75 | 2,783 | `DocR.*` (document routing), `ab_compile*` (activity-based billing compile), `Columbia_Assessment` |

### 20 largest tables

| Table | Columns | Description |
|---|---|---|
| `OrderEntry.history_client_order` | 445 | Every client order stored in Avatar OE |
| `STATEFORM.ga_aso_discharge_rejected` | 437 | Georgia ASO discharge rejected records |
| `STATEFORM.ga_aso_discharge_accepted` | 430 | Georgia ASO discharge accepted records |
| `STATEFORM.ga_aso_discharge` | 425 | Georgia ASO discharge records |
| `STATEFORM.ga_aso_discharge_admin` | 425 | Georgia ASO admin discharge records |
| `SYSTEM.file_import_gpbdt_i837` | 378 | 837 Institutional billing defaults template |
| `OrderEntry.temp_history_client_order` | 366 | Orders queued for printing |
| `OrderEntry.med_regimen_review_detail` | 350 | Medication regimen review data |
| `SYSTEM.file_import_gpbdt_p837` | 343 | 837 Professional billing defaults template |
| `SYSTEM.patient_demographic_history` | 342 | Full patient demographic history |
| `SYSTEM.history_provider_auths` | 335 | Service authorization information |
| `SYSTEM.patient_current_demographics` | 331 | Current patient demographics |
| `CWSTEMP.cw_patient_notes_supp_5` | 325 | Pre-filing storage for progress notes supplement 5 |
| `SYSTEM.cw_patient_not_void_sup_5` | 325 | Voided progress notes supplement 5 |
| `SYSTEM.cw_patient_notes_supp_5` | 324 | Site-specific progress notes supplement 5 |
| `CWSTEMP.cw_patient_notes_supp_4` | 322 | Pre-filing storage for progress notes supplement 4 |
| `SYSTEM.cw_patient_not_void_sup_4` | 322 | Voided progress notes supplement 4 |
| `SYSTEM.cw_patient_notes_supp_4` | 321 | Site-specific progress notes supplement 4 |
| `CWSTEMP.cw_patient_notes_supp_1` | 309 | Pre-filing storage for progress notes supplement 1 |
| `SYSTEM.cw_patient_notes_voided_supp_1` | 309 | Voided progress notes supplement 1 |

The full inventory of all 561 tables and 33,474 columns is available in `analysis/entity-inventory-full.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

Netsmart has documented their **actual database schema**, not a clinical summary projection. The export spans 13 database schemas reflecting different product subsystems:

**Richest domains:**
- **Demographics & Patient** (168 tables, 15,288 columns): The deepest area. `patient_current_demographics` alone has 331 columns. Includes enrollment, episodes, admission/discharge, demographic history, outreach, client merging/purging, and external IDs.
- **Billing & Financial** (159 tables, 10,691 columns): Exceptionally thorough. Covers CMS-1500, UB-04, 837I/P claims processing, 835 remittance, 276/277 claim status, cash posting, charge input, self-pay billing, Medicare pharmacy billing, financial eligibility, payment history, retroactive payor changes, benefit enrollment (834), and general ledger.
- **Clinical Notes & Documents** (51 tables, 6,916 columns): Progress notes (group, individual, ambulatory, inpatient) with 5+ supplement tables each (supp_1 through supp_5, ~300+ columns each), voided notes, co-sign workflows, scratch notes, and significant findings.

**Moderately deep domains:**
- **State-Specific Reporting** (63 tables, 4,236 columns): NY PAS forms (44N, 45N, 46, 47, 125), Georgia ASO, Florida FSR, Michigan county billing, California DCR, Kansas AIMS, Indiana MRO, Louisiana, Ohio BH, and WaMS. This reflects myAvatar's deep integration with state behavioral health systems.
- **Diagnoses** (44 tables, 5,679 columns): Client diagnosis records, audit trails, enrollment diagnoses, problem lists.
- **Labs & Orders** (43 tables, 2,794 columns): CPOE orders (445 columns each), results, specimens, POC results, consent, medication regimen reviews.
- **Service Authorization** (19 tables, 1,436 columns): Funding source, member, and provider authorizations — critical for behavioral health billing workflows.

**Thinner but present:**
- **Treatment & Care Plans** (10 tables, 388 columns): Treatment plan basics, clinical pathway enrollments, discharge summaries. Thinner than expected given the product's emphasis on treatment planning.
- **Vitals & Observations** (6 tables, 284 columns): Basic vital signs and clinical observations.
- **Allergies** (5 tables, 146 columns) and **Immunizations** (4 tables, 180 columns): Present but compact.
- **Behavioral Health Specific** (15 tables, 567 columns): Acuity scoring, incident reporting, seclusion/restraint. Important domain but not as deep as the billing or clinical notes areas.
- **Consent & Disclosure** (9 tables, 196 columns): 42 CFR Part 2 consent management, referral consent, access consent. Essential for behavioral health.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `patient_current_demographics` (331 cols), `patient_demographic_history` (342 cols), 168 total tables in category | Exceptionally thorough |
| Encounters / visits | ✅ Covered | `staff_tx_history`, episode management, admission/discharge tables, `primary_care_visits` | Well covered through service transaction and episode framework |
| Problems / conditions / diagnoses | ✅ Covered | `client_diagnosis_record`, `client_diagnosis_entry`, audit tables, 44 total tables | Thorough including audit trail |
| Medications / prescriptions | ✅ Covered | 22 tables including `history_client_med_order`, `med_regimen_review_detail` (350 cols), Methadone schema (6 tables), NCPDP claim/response | Deep, includes methadone-specific tables |
| Allergies | ✅ Covered | `cw_client_allergies_review`, `cw_hist_client_allergies`, 5 tables | Adequate |
| Immunizations | ✅ Covered | `cw_immunization_history`, `cw_hm_alerts_immunization`, 4 tables | Adequate |
| Vitals | ✅ Covered | `cw_vital_signs`, `cw_vitals_single_row_view`, `cw_observation_details`, 6 tables | Adequate |
| Lab results | ✅ Covered | OrderEntry schema (25 tables), `history_client_order` (445 cols), results and specimen tables | Thorough |
| Imaging / diagnostic reports | ⚠️ Partial | No dedicated imaging tables; imaging results would be in order/result tables | Behavioral health EHR — imaging is minimal. Not a significant gap |
| Procedures | ✅ Covered | Procedure data within order and service transaction tables | Covered via orders framework |
| Clinical notes / documents | ✅ Covered | 51 tables with extensive supplement tables (300+ cols each); group, individual, ambulatory, inpatient notes | Very thorough |
| Care plans / goals | ⚠️ Partial | `Clinical_Pathway_Enrollments`, `tx_disch_summary`, `cw_tp_delete`; 10 tables | Present but thinner than expected given product emphasis on treatment planning |
| Orders / referrals | ✅ Covered | `history_client_order` (445 cols), `carefabric_referrals`, referral consent tables | Thorough |
| Insurance / coverage | ✅ Covered | Benefit enrollment (834), payor tables, eligibility, guarantor data in billing tables | Well covered |
| Claims / billing | ✅ Covered | 159 tables, 10,691 columns. CMS-1500, UB-04, 837I/P, 835, 276/277. | Exceptionally thorough |
| Payments | ✅ Covered | `billing_pay_adj_history`, cash posting tables, payment adjustment history | Well covered |
| Consents / directives | ✅ Covered | 9 tables including 42 CFR Part 2 consent, referral consent, access consent | Appropriate for behavioral health |
| Patient communications / portal messages | ❌ Not covered | No portal message tables visible | myHealthPointe is a separate product with its own EHI export. Reasonable separation |
| Specialty-specific (behavioral health) | ✅ Covered | Acuity scoring (5 tables), incidents (5 tables), seclusion/restraint, detoxification, group therapy documentation, methadone management (6 tables), 42 CFR Part 2 compliance | Core behavioral health workflows are covered |
| Specialty-specific (state reporting) | ✅ Covered | 63 tables across 10+ states (NY, GA, FL, CA, MI, IN, KS, LA, OH, WA) | Uniquely thorough — reflects deep integration with state BH systems |

## 6. Documentation Quality

**Strengths:**
- **Extraordinary scope**: 561 tables, 33,474 unique columns — this is a genuine database schema export, not a summary
- **Good description coverage**: 77.8% of columns have descriptions (26,047 of 33,474)
- **Consistent structure**: Every table has a form name, table name, table description, and per-column detail (name, type, max length, description)
- **Glossary**: Explains common field patterns — PATID (client ID), FACILITY, EPISODE_NUMBER, JOIN_TO/LINK_TO conventions for relationships, ss_ prefix for site-specific fields, data_entry_* audit fields
- **Relationship markers**: JOIN_TO_xxx and LINK_TO_xxx column naming conventions enable data reconstruction

**Weaknesses:**
- **No sample data or example exports**: A developer cannot verify their import works without actual export files
- **No file format specification**: "Computable, delimited file format" is stated but delimiter, encoding, escaping, null handling, and header format are unspecified
- **No machine-readable schema**: The only format is a 7,492-page PDF. No DDL, XSD, or JSON Schema
- **22.2% of columns lack descriptions**: 7,427 columns have names and types but no description
- **No value set enumeration**: Coded fields use `xxx_CODE` + `xxx_value` pattern but valid values are not listed
- **No relationship diagram**: With 561 tables and JOIN_TO/LINK_TO relationships, an ERD would greatly aid comprehension
- **Dated**: Document is from September 2023; the certified product version dates to December 2024. Over a year of potential schema drift
- **No formal nullability or key documentation**: Primary keys, foreign keys, and nullability are not specified

**Overall**: A developer could understand the *structure* and *purpose* of each table from this documentation. They could not, however, build a working import without sample data, format specification, and value set definitions. The documentation is strong on breadth but lacking in implementation-level detail.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

This export demonstrably covers the breadth of data domains myAvatar stores. With 561 unique tables spanning clinical (notes, diagnoses, vitals, labs, medications, allergies, immunizations), financial (159 billing tables including claims, remittance, payments, eligibility), behavioral health-specific (acuity, incidents, seclusion/restraint, methadone management, 42 CFR Part 2 consent), and state reporting (63 tables across 10+ states), this is not a clinical summary rebranded. The export goes far beyond USCDI — the 159 billing tables alone exceed what any standard clinical exchange covers, and the behavioral health-specific and state reporting domains have no representation in USCDI or FHIR US Core.

The only notable domain gap is patient portal messages, but myHealthPointe is a separately certified product with its own EHI export. Treatment/care plan tables are thinner than expected (10 tables vs 159 for billing), but this may reflect how the product structures that data (treatment planning elements may be embedded in clinical notes supplement tables, which are very large).

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly a purpose-built EHI export, not a repackaged FHIR or C-CDA exchange. The evidence:
1. The export uses the product's native database table format, not FHIR resources or C-CDA sections
2. The EHI page explicitly distinguishes this from the FHIR API and HL7 integrations, directing users to different portals for those
3. The export covers 13 database schemas including Methadone, eMAR, INCIDENT, STATEFORM, and GL — domains that have no representation in any clinical exchange standard
4. The 7,492-page data dictionary documents the actual database schema, not a standards-based projection
5. Behavioral health-specific tables (acuity scoring, seclusion/restraint, methadone dispensing) and state-specific reporting tables are uniquely (b)(10) content

### Key Findings

1. **Genuinely comprehensive database-level export**: 561 tables across 13 schemas with 33,474 columns. This is one of the most thorough EHI data dictionaries encountered, reflecting a real effort to export the designated record set, not just clinical summaries.

2. **Exceptional billing coverage**: 159 billing/financial tables with 10,691 columns covering the full revenue cycle (claims, remittance, payments, eligibility, self-pay, payor changes). This alone distinguishes the export from a repackaged clinical exchange.

3. **Deep behavioral health specialization**: Methadone/MAT management schema (6 tables), acuity scoring, incident reporting, seclusion/restraint tracking, 42 CFR Part 2 consent management, and 63 state-specific reporting tables demonstrate domain-appropriate export completeness.

4. **Documentation lacks implementation detail**: No sample data, no file format specification (delimiter, encoding), no machine-readable schema, no value set enumerations. A developer cannot build an import from this documentation alone without obtaining an actual export file first.

5. **Documentation is dated**: The PDF was created October 2023 for a product certified December 2024. Schema may have evolved in the intervening 14+ months.

### Summary Stats

    Coverage:        Comprehensive
    Approach:        Purpose-built EHI export
    Export format:   Proprietary delimited files (one file per table)
    Entities:        561 unique tables (906 form-table pairs)
    Fields:          33,474 unique columns
    Descriptions:    77.8% of fields have descriptions
    Sample data:     No
    Bulk export:     Unclear (described as "manual one-time" for one or more patients)
    Domains covered: 17 of 18 applicable domains (portal messages excluded as separate product)

### Bottom Line

Netsmart has done genuine (b)(10) work with myAvatar. A patient or provider would receive a structurally comprehensive copy of their data spanning clinical, billing, behavioral health, medication, and state-reporting domains — far beyond what any clinical exchange standard covers. The biggest weakness is the lack of implementation documentation (no sample data, no format spec, no machine-readable schema), which means the export data would arrive without sufficient documentation to actually parse it.
