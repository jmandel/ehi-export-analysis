# EHI Export Analysis: PracticeSuite, Inc.

**Product**: PracticeSuite (also certified as FreeChiro — same platform)
**Analysis date**: 2026-02-16
**CHPL IDs**: 10788 (PracticeSuite), 10789 (FreeChiro)

## 1. Product Context

PracticeSuite is a cloud-based, integrated medical practice management and EHR platform serving independent physician practices, billing companies, and multi-specialty groups. The company claims 92,000+ medical professionals on the platform and processes over $10 billion in claims annually. The product supports 25+ clinical specialties and 150+ billing specialties.

Key data domains the product stores:

- **Clinical data**: Demographics, medical history, family health history, diagnoses/problem lists, medications, allergies, lab orders/results, imaging orders, encounter notes, treatment plans, vital signs, implantable device info, clinical decision support alerts
- **E-prescribing**: Prescriptions via NewCropRx integration, prior authorizations, PDMP data
- **Billing/financial**: Insurance info, eligibility verification, charges, claims (submitted/denied/corrected), payments, collections, patient statements, financial reports
- **Scheduling**: Appointments, provider schedules, patient check-in, patient flow
- **Patient portal**: Messages/chat, appointment requests, prescription refill requests, intake forms, satisfaction surveys (via HelloHealth integration)
- **Telehealth**: Video/phone consultation records
- **Documents**: e-Faxes, referral documents, C-CDA documents, scanned records
- **Custom templates**: 30+ customizable EMR templates across specialties

This is a comprehensive ambulatory EHR+PM platform. An adequate (b)(10) export should cover clinical, billing, scheduling, portal, and document data.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `ehi-export-page.html` (159 KB) | Main EHI export documentation page. WordPress page with step-by-step export instructions and 12 embedded screenshots. Created 2023-11-14, last modified 2024-05-20. | **Primary source** — contains all export documentation |
| `k3-report-page.html` (161 KB) | K3 Patient Clinical Analysis Report documentation. Describes the report used for EHI export, including search filters, export options, and custom visit summary setup. | **Supplementary** — adds detail on K3 report capabilities |
| `page-screenshot-full.png` (1.3 MB) | Full-page browser screenshot of EHI export page | Confirms HTML content visually |
| `singlepatsearch.png` (158 KB) | Single patient search interface screenshot | Reveals ~36 vital sign search parameters |
| `patpopulationsrch.png` (132 KB) | Patient population search interface | Shows filter categories: Diagnosis, Medication, Facesheet, CPT Code, Lab Order, Lab Result, Radiology, vitals |
| `ccdadownloadzip.png` (85 KB) | Contents of downloaded C-CDA ZIP | Shows cda.xsl (128 KB) + one patient XML (253 KB) |
| `docdownloadzip.png` (148 KB) | Contents of downloaded documents ZIP | Shows per-patient folder with multiple document files |
| `k3-images/K3OutputList.png` (36 KB) | K3 report results showing 20 output columns | Shows MR#, demographics, insurance, DOS fields |
| `k3-images/K3CustomVisitSummary.png` (81 KB) | Sample Custom Visit Summary Report | **Most informative** — shows 17 structured sections including demographics, encounter details, chief complaint, history, meds, vitals, diagnosis, plan |
| 12 additional PNG screenshots | UI screenshots of export buttons, ZIP contents, user access config, search interfaces | Confirmatory — demonstrate workflow |

**No data dictionary, schema, sample data, or machine-readable specification of any kind was found.** All 22 artifacts are either HTML instruction pages (2) or PNG screenshots (20). There are no PDFs, CSVs, JSONs, XMLs, XLSXs, or any structured data artifacts.

## 3. Export Mechanics

- **Format**: C-CDA XML (one file per patient in a ZIP archive) + separate ZIP of documents in their original formats
- **Mechanism**: UI-based. Users navigate to Report Central → K3 Patient Clinical Analysis Report, search for patient(s), then click "Download C-CDA" or "Download Documents" buttons.
- **Single-patient**: Search by patient name or MR#, then download
- **Bulk/population**: Search by health parameters (diagnoses, medications, vitals, CPT codes, lab orders/results, radiology, facesheet parameters), then download for all matching patients
- **Access control**: Restricted to users with Report Central menu privileges
- **Additional export**: A "Download Visit Summary" option generates a PDF-format Custom Visit Summary Report per encounter
- **API access**: None documented. Export is exclusively through the UI.
- **Fees**: No fees mentioned for the export functionality itself

**Key limitation**: The population export requires search criteria — there is no documented way to simply export *all* patients at once without specifying filter parameters.

## 4. Export Content: What's In It

### No data dictionary

PracticeSuite provides **zero field-level documentation** of the export. There is no data dictionary, no schema, no field listing, no type information, no relationship documentation, no value set specification. The entire documentation consists of workflow instructions ("click here, then click here") with screenshots.

The only specification of export content is the phrase "full CCDA Summary" — repeated multiple times but never elaborated. The C-CDA version/template is not specified. The C-CDA sections populated are not listed.

### What the C-CDA likely contains (inferred)

Based on standard C-CDA sections and the Custom Visit Summary screenshot (which shows what PracticeSuite can render per encounter), the C-CDA export likely includes:

- Patient demographics (name, DOB, age, gender, location)
- Encounter information (provider, date, encounter type, telehealth type)
- Chief complaint
- Past medical history
- Allergies
- Medication list
- Vital signs (temperature, heart rate, respiratory rate, blood pressure, pain scale, pulse ox, height)
- Assessment/diagnosis (ICD-10 codes visible: G43.909, R11.0)
- Plan / recommended action

However, **none of this is documented by the vendor** — it is inferred from the Custom Visit Summary screenshot (`k3-images/K3CustomVisitSummary.png`) and general C-CDA capabilities.

### Custom Visit Summary sections (from screenshot)

The Custom Visit Summary Report (`K3CustomVisitSummary.png`) shows 17 structured sections:

| Section | Content observed in screenshot |
|---|---|
| Patient Demographics | Name, DOB, Age, Gender, Location |
| Documentation Demographics | Provider, DOS, Enc Sheet Type, Canned Sheet Type |
| Encounter Demographics | Start Time, Encounter Type, Tele Health Type, Transaction Service, Participant Roster, SHS Eng Level |
| Chief Complaint | Free text |
| Past Medical History | Notes, significant conditions |
| Allergies | Medication allergies, food, environmental, animals/insects |
| MED LIST | Medication list |
| Vital Signs | Temperature, Heart Rate, Respiratory Rate, Blood Pressure, Pain, Pulse Ox, Height |
| Assessment/Diagnosis | ICD-10 codes |
| Plan / Recommended Action | Medications School Administered, Medications Over The Counter, Medications Prescription, Actions Instructions, Follow Up Care, Communication Visit Summary, Patient Education, Student Disposition |
| Special Situation | Free text |
| Escalation and Emergency | Free text |
| Provider Signature | Physician, Nurse Practitioner, Registered Nurse |
| Care Coordinator Signature | Free text |
| Custom Visit Summary | Status (Created and Sent) |
| Authorization for Med Administration - RX | Status |
| CareTeam Communication 1 | Status |

### Documents export

The documents ZIP contains patient documents in their original file formats (PDF, images, etc.), organized into per-patient subfolders. File naming follows `<FileName>_<Category>[file]`. No documentation specifies what document types or categories exist.

### K3 Report output columns

The K3 results list (`K3OutputList.png`) shows these 20 columns for each patient:

MR#, PC Ref#, LName, FName, Gender, DOB, Age, Address, Home Ph., Work Ph., Pref. Means of Contact, Race, Ethnicity, Lan. Spoken, Last Seen, PR. Ins., SE. Ins., TE. Ins., DOS, Time

This data is displayed in the UI but it is unclear whether these fields are included in the C-CDA export or only visible in the report interface.

### Vendor's own content organization

PracticeSuite does not organize its export into named entities, tables, or categories. The vendor describes exactly two export components:

| Export Component | Format | Content (vendor's description) |
|---|---|---|
| C-CDA Download | XML in ZIP | "Full CCDA Summary" (no further detail) |
| Documents Download | Original formats in ZIP | "All available documents" associated with patient(s) |
| Custom Visit Summary (supplemental) | PDF report | Per-encounter summary with 17 sections (see above) |

There is no data dictionary to enumerate entities or fields. The export is not table-based — it is a document-based export (C-CDA XML + raw documents).

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

PracticeSuite's EHI export provides two things:

1. **C-CDA clinical summaries** — standard clinical document format covering demographics, problems, medications, allergies, vitals, encounters, and potentially procedures/results/immunizations (unconfirmed, as the vendor never specifies which C-CDA sections are populated). C-CDA is inherently a clinical summary standard; it cannot represent billing, scheduling, portal communications, or specialty-specific structured data.

2. **Raw documents** — all files attached to a patient record in their original format. This captures uploaded PDFs, scanned documents, images, etc., but does not capture structured data stored in database fields.

The vendor also offers a Custom Visit Summary PDF report with 17 sections, but this appears to be a printed report format rather than a structured data export.

The export is **extremely thin from a documentation perspective**. The only substantive content description is "full CCDA Summary" — three words. There is no field-level detail, no section inventory, no code system specification, and no sample data.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA standard demographics section (inferred); K3 output shows name, DOB, gender, race, ethnicity, language, address, phone | C-CDA carries basic demographics but depth is unverified; vendor never confirms specific fields |
| Encounters / visits | ⚠️ Partial | Custom Visit Summary shows encounter info; C-CDA should include encounters section | Likely present in C-CDA but undocumented |
| Problems / conditions / diagnoses | ⚠️ Partial | ICD-10 codes visible in Visit Summary screenshot; C-CDA has Problems section | Likely in C-CDA but unconfirmed |
| Medications / prescriptions | ⚠️ Partial | "MED LIST" in Visit Summary; C-CDA has Medications section | Basic medication list likely present; detailed e-prescribing data from NewCropRx (prior auths, PDMP, refill history) almost certainly missing |
| Allergies | ⚠️ Partial | Allergies section in Visit Summary; C-CDA has Allergies section | Likely present in C-CDA |
| Immunizations | ⚠️ Partial | Not visible in screenshots; C-CDA can include Immunizations section | Product is certified for immunization registry reporting (f)(1); data exists but export coverage unconfirmed |
| Vitals | ⚠️ Partial | Vital signs in Visit Summary screenshot; ~36 vital types in search interface | Likely in C-CDA; extensive vital sign types suggest rich vitals data |
| Lab results | ⚠️ Partial | Lab Order and Lab Result search filters exist in K3; C-CDA has Results section | Product integrates with Labcorp/Quest; lab data exists but C-CDA coverage depth unknown |
| Imaging / diagnostic reports | ⚠️ Partial | Radiology search filter in K3; C-CDA can include Diagnostic Results | Imaging orders likely referenced but actual images only via documents export |
| Procedures | ⚠️ Partial | CPT Code search filter in K3; C-CDA has Procedures section | CPT-coded procedures likely in C-CDA |
| Clinical notes / documents | ⚠️ Partial | Documents export provides attached files in original format; C-CDA may include Notes section | Attached documents covered; structured note content via C-CDA uncertain |
| Care plans / goals | ⚠️ Partial | "Plan / Recommended Action" in Visit Summary; C-CDA can include Care Plan | Possibly in C-CDA |
| Orders / referrals | ⚠️ Partial | Lab Order search filter exists | E-prescribing orders, lab orders, referrals may be partially in C-CDA |
| Insurance / coverage | ❌ Not covered | K3 output list shows PR. Ins., SE. Ins., TE. Ins. column headers, but these are in the report UI — not in the C-CDA | Product stores detailed insurance/eligibility data; C-CDA has no standard section for insurance details. **Significant gap.** |
| Claims / billing | ❌ Not covered | No billing data in C-CDA format; no billing entities in export | Product processes $10B+ in claims annually — charges, claims, denials, corrections, payments. **Major gap.** |
| Payments | ❌ Not covered | No payment data in export | Product handles patient payments, credit card processing, collections. **Gap.** |
| Consents / directives | ❌ Not covered | Not mentioned in documentation | If consent forms exist as uploaded documents, they may be in the documents export |
| Patient communications / portal messages | ❌ Not covered | No portal data mentioned; HelloHealth integration data not addressed | Product has patient chat, broadcast messaging, appointment requests, satisfaction surveys. **Gap.** |

**Summary**: Every clinical domain receives a "Partial" rating because C-CDA *can* carry standard clinical data, but the vendor never confirms which sections are actually populated. Non-clinical domains (billing, insurance, payments, portal) are completely absent from the export format.

## 6. Documentation Quality

**Overall quality: Very poor.**

- **Can a developer understand and use the export?** A developer would know to expect C-CDA XML and could parse it with standard C-CDA libraries. However, PracticeSuite provides zero vendor-specific documentation: no C-CDA profile, no section inventory, no extension documentation, no value set specification. A developer would have to reverse-engineer the export from actual files.

- **What's well-documented**: The UI workflow (how to navigate menus, click buttons, download ZIPs) is clearly described with annotated screenshots. File naming conventions are documented.

- **What requires guesswork**: Everything about the actual data content — which C-CDA sections are populated, what fields are included, what coded vocabularies are used, what data types are employed, what relationships exist between data elements.

- **Machine-readable artifacts**: None. No schema, no sample C-CDA, no JSON/XML specification, no data dictionary in any format.

- **Maintenance**: Page created November 2023, last updated May 2024. Appears to be a one-time compliance deliverable.

- **The documentation answers "how do I click the button?" but not "what data will I get?"**

## 7. Overall Assessment

### Classification

**Standard-based projection.** PracticeSuite's (b)(10) export is their existing C-CDA generation capability repackaged as an EHI export. The C-CDA format covers a subset of clinical summary data but structurally cannot represent billing records, insurance details, scheduling data, patient portal communications, or specialty-specific structured data that PracticeSuite stores.

### Key Findings

1. **C-CDA repackaging as (b)(10)**: The export is exclusively C-CDA XML documents plus raw attached files. This is a textbook case of a vendor repurposing an existing clinical summary capability to meet the (b)(10) requirement. C-CDA was designed for care transitions between providers, not for comprehensive data export. (Source: `ehi-export-page.html`, which repeatedly describes "CCDA format" as the sole structured export.)

2. **No data dictionary whatsoever**: Among the thinnest documentation reviewed. The entire export content specification is the three-word phrase "full CCDA Summary." No field listing, no section inventory, no schema, no sample data. Zero of the 22 downloaded artifacts contain structured data specifications — they are all HTML pages (2) and PNG screenshots (20). (Source: `files.json`, `artifact-summary.json`)

3. **Billing data completely absent**: PracticeSuite is fundamentally a practice management and billing platform processing $10B+ in claims annually. The C-CDA format has no mechanism to carry charges, claims, payments, insurance details, eligibility verification, or collections data. This represents the single largest gap between what the product stores and what the export provides. (Source: `product-research.md` for product capabilities; `ehi-export-page.html` for export format)

4. **Patient portal and engagement data absent**: PracticeSuite's HelloHealth-powered patient portal stores messages, chat transcripts, appointment requests, prescription refill requests, intake forms, and satisfaction surveys. None of this appears in the C-CDA export, and the documentation makes no mention of it. (Source: `product-research.md`)

5. **Population export requires search criteria**: The documentation describes population export using search filters (diagnosis, medication, vitals, etc.) but does not document a way to export *all* patients without specifying filter parameters. This may mean a true bulk "all patients" export requires workarounds. (Source: `ehi-export-page.html`, `patpopulationsrch.png`)

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA XML + original-format documents
Model type:      Standard projection (C-CDA)
Entities:        N/A (no data dictionary; export is C-CDA documents, not tables)
Fields:          N/A
Descriptions:    N/A
Sample data:     No
Bulk export:     Partial (population export requires search filters)
Domains covered: 0 confirmed, ~10 likely partial (via C-CDA), of 17 applicable domains
```

### Bottom Line

PracticeSuite's EHI export is a C-CDA clinical summary repackaged as a (b)(10) compliance measure, with no data dictionary and no documentation of what the export actually contains beyond "full CCDA Summary." A patient or provider would receive a standard clinical summary and their uploaded documents, but would **not** receive their billing records, insurance details, portal messages, or any structured data beyond what C-CDA can carry — despite PracticeSuite storing all of this data. The biggest gap is billing: a platform processing $10B+ in annual claims exports zero billing data.
