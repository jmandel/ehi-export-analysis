# EHI Export Analysis: NovoMedici, LLC

**Product**: NovoClinical v1.0
**Analysis date**: 2026-02-16
**CHPL IDs**: 10805 (15.02.05.3015.Novo.01.01.1.220131)

## 1. Product Context

NovoClinical is a cloud-based, all-in-one ambulatory EHR and practice management system developed by NovoMedici, LLC (Ogden, Utah). It targets small to mid-sized ambulatory medical practices across multiple specialties (general practice, cardiology, gastroenterology, OB/GYN, pediatrics, dermatology, etc.). The product integrates clinical documentation, billing/revenue cycle management, scheduling, e-prescribing, patient portal, telemedicine, and chronic care management into a single platform. It was certified 2022-01-31 against a broad set of ONC criteria including (b)(10) EHI export.

Key data domains the product stores, relevant to export completeness assessment:

- **Clinical**: Charting with customizable templates, problem lists, medication lists, allergy lists, implantable device lists, vitals, lab orders/results, imaging integration (RIS/PACS), immunizations, clinical notes, care plans
- **Prescribing**: E-prescriptions, medication history
- **Billing/RCM**: Claims, billing codes (ICD-10, UB-04), payments, DME billing, statements, accounts receivable, claim scrubbing
- **Scheduling/Administrative**: Appointments, patient check-in, referrals, tasks
- **Patient Portal**: Secure messages, patient-entered demographics/history, e-signed documents
- **Telemedicine**: Virtual visit records
- **Chronic Care Management**: Care plans, monitoring data
- **Communications**: E-fax, text messages, direct messages

The product's navigation bar (visible in the export UI screenshot) confirms modules for: Appointment, Doc. And Notes, Patient, Communication, Coding, Accounting, Reports, Admin, Inventory, Su Admin — indicating a broad feature set well beyond clinical documentation.

## 2. Artifacts Reviewed

| Artifact | Type | Size | Description | Informativeness |
|---|---|---|---|---|
| `Novoclinical-Data-Export-Format.pdf` | PDF, 1 page | 129 KB | The entire EHI export documentation. Contains a title, two bullet points describing C-CDA and CSV formats, navigation instructions (3 sentences total), and a screenshot of the export UI. Created 2023-10-07 with Microsoft Word. | **Primary source; extremely minimal** |
| `screenshot-meaningful-use-page.png` | PNG screenshot | 193 KB | Screenshot of vendor's Meaningful Use page at novomedici.com. Lists links to mandatory disclosures, API terms, and an "EMR Data Export" footer link that points to the same PDF. Confirms no additional EHI export documentation exists on the vendor's site. | Contextual only |

**Verification performed:**
- The PDF URL (`https://s3.amazonaws.com/novoclinical.miscellaneous/Novoclinical+Data+Export+Format.pdf`) returns HTTP 200 as of 2026-02-16 (Last-Modified: 2023-10-08, unchanged).
- The vendor's meaningful use page (`https://www.novomedici.com/meaningful-use/`) is still accessible. The "EMR Data Export" link in the footer still points to the same PDF.
- No dedicated `/emr-data-export/` page exists (returns 404).
- The API documents page contains only FHIR/Smart-on-FHIR API links for (g)(10), not (b)(10) documentation.

## 3. Export Mechanics

- **Format**: ZIP file containing C-CDA XML documents (one per patient) and CSV files (for demographics and appointments)
- **Mechanism**: UI-based. Clinic administrators navigate to Communication > Data Export within NovoClinical.
- **Single-patient vs bulk**: Both. The UI supports specific patient export or group export of all/multiple patients.
- **Selection controls** (visible in screenshot): Doctor filter (dropdown, default "All Doctors"), frequency (dropdown, default "MONTHLY"), date/time picker, appointment date range (FROM/TO), patient search field.
- **Access constraints**: Export is restricted to clinic administrators per the documentation.
- **Fees**: Not mentioned in the export documentation. The vendor's mandatory disclosures document (linked from the meaningful use page) may address this but was not part of the EHI export artifacts.

## 4. Export Content: What's In It

The export documentation describes exactly two data categories in a total of three sentences:

1. **C-CDA (Consolidated Clinical Document Architecture)**: "Each patient will have a C-CDA document in the exported data." No further specification — no document type (CCD vs. Discharge Summary vs. other), no template version, no section list, no details about what clinical data is included.

2. **CSV**: "Comma separated value, used for patient demography, Appointments." No column definitions, no field names, no data types, no encoding specifications, no sample data.

### Vendor's own content organization

The vendor provides no data dictionary, no schema, and no field-level documentation of any kind. The only "organization" is the two format-level bullet points:

| Entity/Category | Format | Fields Documented | Descriptions | Types | Vendor Description |
|---|---|---|---|---|---|
| C-CDA document (per patient) | XML (C-CDA) | 0 | N/A | N/A | "Each patient will have a C-CDA document in the exported data" |
| Patient demography | CSV | 0 | N/A | N/A | "Comma separated value, used for patient demography" |
| Appointments | CSV | 0 | N/A | N/A | "Comma separated value, used for ... Appointments" |

**Total documented entities**: 3 (at format/category level only)
**Total documented fields**: 0
**Fields with descriptions**: 0
**Fields with types**: 0

There is no data dictionary to parse. The complete content of the export documentation has been extracted to `analysis/full-entity-inventory.json` and `analysis/artifact-summary.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's documentation describes two components:

1. **C-CDA documents**: Presumably standard clinical summary content (problems, medications, allergies, lab results, vitals, immunizations, procedures). However, the documentation does not specify which C-CDA sections are populated, so the actual clinical coverage is unknown. C-CDA is a clinical document standard and by design cannot represent billing records, scheduling details, communications, portal messages, or custom clinical forms.

2. **CSV for demographics and appointments**: Two administrative data categories. Without column definitions, the depth of coverage is unknown — "patient demography" could mean 5 fields or 50.

The vendor makes no mention of:
- Billing or financial data of any kind
- Clinical notes or documents beyond what C-CDA might contain
- Prescribing history beyond C-CDA medication sections
- Lab or imaging orders (as distinct from results)
- Patient portal data (messages, patient-entered forms)
- Telemedicine encounter data
- Chronic care management records
- Communication records (fax, SMS, direct messages)
- Insurance/coverage information
- Referrals or care coordination data
- Custom templates or specialty-specific clinical data

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | CSV for "patient demography" — no fields specified | Present but undocumented; depth unknown |
| Encounters / visits | ⚠️ Partial | Appointments CSV; C-CDA may include encounter data | Appointments listed; clinical encounters may be in C-CDA but unspecified |
| Problems / conditions / diagnoses | ⚠️ Partial | Likely in C-CDA (standard section) | No confirmation; depends on C-CDA template used |
| Medications / prescriptions | ⚠️ Partial | Likely in C-CDA (standard section) | No confirmation; e-prescribing history may not be fully captured |
| Allergies | ⚠️ Partial | Likely in C-CDA (standard section) | No confirmation |
| Immunizations | ⚠️ Partial | Likely in C-CDA (standard section) | No confirmation |
| Vitals | ⚠️ Partial | Likely in C-CDA (standard section) | No confirmation |
| Lab results | ⚠️ Partial | Likely in C-CDA (standard section) | No confirmation; lab orders likely missing |
| Imaging / diagnostic reports | ⚠️ Partial | May be in C-CDA | Product integrates RIS/PACS; unclear if imaging data is in export |
| Procedures | ⚠️ Partial | Likely in C-CDA (standard section) | No confirmation |
| Clinical notes / documents | ⚠️ Partial | May be in C-CDA | Product has "Doc. And Notes" module; unclear if notes are fully exported |
| Care plans / goals | ❌ Not covered | No evidence | Product offers chronic care management with care plans; gap |
| Orders / referrals | ❌ Not covered | No evidence | Product supports referrals; gap |
| Insurance / coverage | ❌ Not covered | No evidence | Product does eligibility verification; gap |
| Claims / billing | ❌ Not covered | No evidence | Product has full billing/RCM module (Coding, Accounting visible in nav bar); **significant gap** |
| Payments | ❌ Not covered | No evidence | Product processes payments including credit cards; gap |
| Consents / directives | ❌ Not covered | No evidence | Patient portal supports e-signatures; gap |
| Patient communications / portal messages | ❌ Not covered | No evidence | Product has patient portal with secure messaging; gap |
| Specialty-specific data | ❌ Not covered | No evidence | Product serves multiple specialties with customizable templates; gap |

**Summary**: Of 19 applicable domains, 0 are confirmed covered, 10 are partially covered (assumed via unspecified C-CDA content), and 9 are not covered at all. The documentation is too thin to confirm coverage of even the C-CDA-based domains.

## 6. Documentation Quality

The export documentation is among the most minimal possible for a certified EHR product:

- **Total documentation**: 1 page, 3 sentences of text, 1 screenshot
- **Data dictionary**: None
- **Field definitions**: None for any format
- **Schema or format specification**: None (CSV columns undefined, C-CDA template/sections unspecified)
- **Sample data**: None
- **Value sets or code systems**: None
- **Relationships between files**: Not documented (how C-CDA and CSV files relate is unexplained)
- **Machine-readable artifacts**: None
- **Import guidance**: None

A developer receiving an export from NovoClinical would have to reverse-engineer both the CSV column structure and the C-CDA template usage entirely from the export files themselves. The documentation provides no actionable technical detail beyond "there will be a C-CDA file and CSV files in a ZIP."

## 7. Overall Assessment

### Classification

**Minimal/stub**: The documentation is too thin to meaningfully assess export completeness. The export appears to be a C-CDA clinical summary plus two CSV files for demographics and appointments — a narrow projection covering a small fraction of what NovoClinical stores. There is no data dictionary, no field-level documentation, and no evidence that billing, specialty, portal, or communication data is exported.

### Key Findings

1. **Entire EHI export documentation is 3 sentences on 1 page.** The PDF (`Novoclinical-Data-Export-Format.pdf`, 129 KB, created 2023-10-07) contains a title, two bullet points, navigation instructions, and a screenshot. No data dictionary, schema, or field definitions exist.

2. **Export is C-CDA + two CSV categories, not a native data model export.** The documented export produces C-CDA documents (one per patient) and CSV files for demographics and appointments. This is a standard-based projection covering at most standard clinical summary data plus basic admin fields — not the vendor's native data model.

3. **Billing and RCM data — a core product feature — is entirely absent from the export.** NovoClinical markets itself as "Medical Billing Software for Small Business" and has dedicated Coding and Accounting modules visible in the navigation bar. No billing, claims, payment, or financial data is mentioned in the export documentation.

4. **Zero fields are documented.** Neither the C-CDA content (sections, templates) nor the CSV files (column names, types) are specified at any level of detail. A recipient cannot know what data to expect without performing the export and examining the files.

5. **No additional documentation exists on the vendor's site.** The meaningful use page links only to this same PDF; the API documents page covers (g)(10) FHIR APIs, not (b)(10) EHI export; there is no dedicated EMR data export web page (returns 404).

### Summary Stats

```
Classification:  Minimal/stub
Export format:   C-CDA (XML) + CSV, delivered as ZIP
Model type:      Standard projection (C-CDA) + minimal CSV
Entities:        3 (category-level only: C-CDA doc, demographics CSV, appointments CSV)
Fields:          0 (no field-level documentation)
Descriptions:    N/A (0 fields documented)
Sample data:     No
Bulk export:     Yes (group export of all/multiple patients)
Domains covered: 0 of 19 confirmed; 10 of 19 assumed partial via unspecified C-CDA
```

### Bottom Line

NovoClinical's EHI export documentation is a single-page PDF with three sentences — one of the thinnest (b)(10) submissions possible. The export appears to repackage standard C-CDA clinical summaries and two basic CSV files, omitting billing/RCM data (a core product feature), portal messages, care plans, communications, and specialty-specific data. A patient or provider would receive a narrow clinical summary, not a complete copy of their electronic health information.
