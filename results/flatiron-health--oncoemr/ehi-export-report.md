# Flatiron Health / OneOncology — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://flatiron.com/certification
- CHPL IDs: 11115 (OncoEMR v2.8), 11640 (OneOncology HIE Integration v1)
- Developer: Flatiron Health, OneOncology, LLC

## Navigation Journal

**Step 1: Probe the registered URL**
```bash
curl -sI -L "https://flatiron.com/certification" -H 'User-Agent: Mozilla/5.0'
```
Result: HTTP 200, Content-Type: text/html; charset=UTF-8. Page is served via Cloudflare + HubSpot CMS. No redirects.

**Step 2: Fetch and examine the page**
```bash
curl -sL "https://flatiron.com/certification" -H 'User-Agent: Mozilla/5.0' -o certification-page.html
```
The page is titled "OncoEMR® ONC Certification" and lists all certified criteria for OncoEMR v2.8 (CHPL ID 15.04.04.3010.Onco.28.02.1.221221, certified December 21, 2022). It is a single static page (117KB HTML, HubSpot-hosted) with no accordions, tabs, or JavaScript-required content for the EHI section.

**Step 3: Identify EHI-relevant content**
The page includes a section headed "EHI Export Documentation:" with a single link:
```html
<p>EHI Export documentation can be found <a href="https://flatiron.com/certification/ehi-data-dictionary?hsLang=en">here</a>.</p>
```
Searched for all downloadable file links:
```bash
grep -oiE 'href="[^"]*\.(pdf|zip|xlsx|csv|json).*?"' certification-page.html
```
Found PDF links for: compliance certificate, risk management practices, and RWT plans/results (2022-2025). None of these are EHI export documentation.

Also found:
- Flatiron API documentation link: https://flatiron.my.site.com/FHIR/s/ (FHIR API portal — this is g(10), not b(10))
- API Terms of Use: https://flatiron.my.site.com/FHIR/s/article/API-Terms-of-Use

**Step 4: Download the EHI data dictionary**
```bash
curl -sL "https://flatiron.com/certification/ehi-data-dictionary?hsLang=en" -H 'User-Agent: Mozilla/5.0' -o ehi-data-dictionary.pdf
```
The URL serves a PDF directly (no HTML wrapper). Verified: `file ehi-data-dictionary.pdf` → "PDF document, version 1.4, 63 page(s)". Size: 400,903 bytes. Title: "EHI data dictionary v1.0", Creator: "Google Sheets".

**Step 5: Check for OneOncology HIE Integration documentation**
Searched the certification page HTML for "OneOncology", "HIE", and "11640". No matches. The page is exclusively about OncoEMR (CHPL ID 11115). The OneOncology HIE Integration product (CHPL ID 11640, certified May 2025) has no separate documentation section on this page, nor any link to separate documentation.

**Step 6: Examine the PDF for embedded links or attachments**
```bash
pdftotext ehi-data-dictionary.pdf - | rg -No 'https?://[^[:space:]>)"]+' | sort -u
```
Found only one URL: `https://terminology.hl7.org/5.5.0` — a reference to HL7 terminology, not actionable EHI documentation.

**Step 7: Browser verification**
Navigated to https://flatiron.com/certification in Chrome. Confirmed the rendered page matches the HTML content. Scrolled to the EHI section and took screenshots. No hidden content, no JavaScript-rendered sections beyond what's in the source HTML.

## What Was Found

The EHI export documentation consists of a single 63-page PDF data dictionary ("EHI data dictionary v1.0", last modified 9/9/2025) that documents the complete schema of the OncoEMR EHI export. The documentation is substantive and well-structured.

### Export Format
- **Single Patient Export**: CSV files (machine-readable)
- **Population Export**: Parquet files (machine-readable)
- **Additional files**: XML, JPEG, PNG, TIFF, or PDF formats for human-readable content (encounter summaries, faxes, imaging results, scanned clinical documents)

### Access Method
- Single Patient: Self-serviceable via the OncoEMR UI
- Population: Requested via OncoEMR UI, downloaded via UI or SFTP depending on export size

### Data Dictionary Structure
The PDF is a table with five columns:
1. **TableName** — the export table/file name
2. **ColumnName** — field name within the table
3. **Type** — SQL Server data type (varchar, datetime, int, bit, etc.)
4. **Nullable** — TRUE/FALSE
5. **Description** — plain-English description of the field

After enrichment parsing: **125 distinct tables** containing **2,689 columns** across 23 data domain categories. Nearly all tables (121 of 125) have a Table Description entry. Each table also has a `PARTITION_NAMESPACE` column indicating which OncoEMR secure environment the practice is hosted on.

### Key Tables by Data Domain

| Domain | Tables | Examples |
|--------|--------|----------|
| Demographics | 8 | Demographics_History (82 cols), Address_History, Contact_History, PhoneNumber_History, EmailAddress_History |
| Diagnoses & Staging | 5 | Diagnosis_History (33 cols), Diagnosis_Staging_History, Diagnosis_Factors_History, Staging_History |
| Medications & Orders | 18 | Medication_History (58 cols), Order_History (70 cols), Order_Details_History (45 cols), DoseCalculationHistory (45 cols), Inventory_Dispense_History |
| Labs & Results | 3 | Lab_Result_History (28 cols), Test_History (31 cols), Test_AOE_History |
| Clinical Notes & Documents | 14 | Document_History (44 cols), Visit_Note_Assessment_And_Plan, Data_History, DataNew_History |
| Billing & Financial | 6 | Charge_History, Invoice_History (42 cols), Transaction_History (49 cols), Claim_Adjustment_History |
| Insurance & Eligibility | 10 | Patient_Insurance_History (189 cols!), Insurance_Authorization_History, Patient_Guarantor_History, Patient_Eligibility_History |
| Encounters | 10 | Encounter (17 cols), EncounterParticipant, EncounterLocation, EncounterDiagnosticReport |
| Allergies | 2 | Allergy_History (28 cols), Allergy_Reaction_History |
| Immunizations | 3 | Immunization_History (60 cols), Immunization_Registry_History, Immunization_Eval_Forecast_History |
| Vital Signs | 1 | Vital_Sign_History (20 cols) |
| Family History | 5 | FamilyHist_History, FamilyHist_Person_History, FamilyHist_Observation_History, FamilyHist_Relative_History |
| Care Plans & Goals | 4 | Care_Plan_History, Care_Plan_Item_History, Care_Plan_Text_History, PatientGoals |
| Treatment & Pathways | 6 | Treatment_Current_History, Treatment_Previous_History, Pathways_History, RegimenConcordance |
| Questionnaires | 3 | QuestionnaireResponse, QuestionnaireResponseAnswer, QuestionnaireResponseInterpretation |
| Care Team | 3 | CareTeam, CareTeamParticipant, CareTeamProvenance |
| Appointments | 3 | Appointment_History, Appointment_Detail_History |
| Imaging | 1 | Image_History |
| Messaging & Tasks | 9 | Message_History, Tasks, TaskMessages, Reminder_History |
| Devices | 1 | ImplantableDevice_History |
| Prescriptions | 1 | Preferred_Pharmacy_History |

## Export Coverage Assessment

### Data Domain Coverage

This is a genuinely comprehensive EHI export that goes well beyond the USCDI/US Core minimum. It is a real (b)(10) implementation — a database-level export of the patient record, not a repackaged FHIR API.

**Clearly covered domains:**
- **Demographics**: Extensive — 82 columns including DOB, gender, race, ethnicity, language, marital status, deceased status, tribal affiliation, birth order, and more
- **Diagnoses & Staging**: Full oncology diagnosis model with AJCC staging factors, staging history, and migration logs
- **Medications & Orders**: Very thorough — covers medication history, order lifecycle (creation, changes, collection, delivery, signoff), dose calculations, drug interaction rules, and inventory dispensing
- **Billing & Financial**: Charges, invoices, transactions, claim adjustments, insurer credits — a substantial billing record set
- **Insurance**: Exceptionally detailed — Patient_Insurance_History alone has 189 columns covering primary/secondary payer details, authorization tracking, eligibility, guarantors, and PBM (pharmacy benefit manager) data
- **Lab Results & Tests**: Lab result history with ask-at-order-entry (AOE) data
- **Clinical Notes & Documents**: Document history, visit note assessments, document signoff workflows
- **Allergies, Immunizations, Vital Signs, Family History**: All covered with full detail
- **Care Plans & Goals**: Patient goals and care plan items
- **Treatment Pathways**: Oncology-specific — treatment current/previous history, pathways results, regimen concordance
- **Encounters**: Full encounter model with participants, locations, diagnostic reports, external encounters
- **Questionnaire Responses**: Structured assessment data with answers and interpretations
- **Patient Assistance**: PatientAssistanceActivityDetail — drug assistance program tracking
- **E-Prescribing**: SureScripts message history, preferred pharmacy history
- **Imaging**: Image history for stored clinical images

**Domains with limited or absent documentation:**
- **Clinical trial data**: OncoTrials is described in product marketing as a key module, but no trial-specific tables appear in the export. There is no mention of clinical trial enrollment, screening, or CTMS data
- **Patient portal data**: CareSpace portal data (secure messages from patients, appointment requests via portal, bill payment records) does not appear to have dedicated tables in the export. The Message_History and Patient_Request_History tables may partially cover this
- **Cancer registry submissions**: While OncoEMR certifies for cancer registry transmission (f)(4), and there's a CancerRegistry-related reference in Immunization fields, no dedicated cancer registry submission/response tables are visible
- **OncoAnalytics data**: No analytics or aggregated reporting tables are in the export, which is appropriate — analytics/aggregates are not EHI

**Notable oncology-specific coverage:**
- DoseCalculationHistory (45 cols) — detailed chemotherapy dosing calculations
- Diagnosis_Staging_History — AJCC cancer staging
- Treatment_Current_History / Treatment_Previous_History — oncology treatment records
- Pathways_History / Pathways_Results_History — clinical pathway tracking
- RegimenConcordance / RegimenConcordanceFactors — regimen adherence monitoring
- Patient_LifetimeDoses_History — cumulative drug dosing (critical for oncology)

### Export Format & Standards

The export format is well-chosen for the data:
- **CSV** for single-patient exports (universal readability)
- **Parquet** for population exports (efficient columnar format for large datasets)
- **Additional files** in native formats (XML, JPEG, PNG, TIFF, PDF) for human-readable clinical documents

This is **not** a FHIR-based export. It's a direct database export in tabular format, which is exactly what (b)(10) should look like for a system of this complexity. The data types are SQL Server types (varchar, datetime, int, bit, float, etc.), reflecting the underlying database schema.

The Flatiron FHIR API (linked separately on the certification page at https://flatiron.my.site.com/FHIR/s/) is their (g)(10) implementation — a separate system from the EHI export. The vendor correctly maintains this separation.

**Could a third party reconstruct the patient record?** Mostly yes. The export includes:
- Clear table and column naming conventions
- Field-level descriptions for nearly every column
- Data type and nullable information
- Cross-references between tables (e.g., sPatientID, sRowID, sGroupID patterns)
- Table-level descriptions explaining what each table stores

However, some aspects could make reconstruction challenging:
- Foreign key relationships are documented implicitly through naming conventions and descriptions rather than a formal schema
- Value sets for coded fields (e.g., sAllergyType: "The vast majority of these values are Drug. NULL is the second biggest value set.") are sometimes described narratively rather than enumerated
- The PARTITION_NAMESPACE field and multi-tenant architecture add complexity

### Documentation Quality

**Strengths:**
- Comprehensive: 125 tables, 2689 columns — this covers the full breadth of an oncology EHR
- Field-level descriptions for nearly every column (only 5 of 2689 missing)
- Clear data types and nullable specifications
- Table-level descriptions explaining the purpose of each table
- Deprecated fields are clearly marked ("Deprecated: Data table is longer in use for recording new patient data")
- Practical format — originated from Google Sheets, exported as PDF
- Last modified date (9/9/2025) shows active maintenance

**Weaknesses:**
- PDF format only — no machine-readable version (CSV, JSON, or XSD) is provided by the vendor. We created the enrichment JSON as a downstream artifact
- No formal schema or DDL
- No entity-relationship diagram
- No sample data or example export files
- No worked examples showing what a complete export looks like
- Foreign key relationships are implicit, not explicit
- Value sets for coded fields are mostly not enumerated
- No documentation of the export file naming conventions or directory structure
- No documentation of how the Parquet population export differs structurally from the CSV single-patient export
- No versioning or change log beyond the single "Last Modified" date

### Structure & Completeness

The documentation is at the **field level** — it goes well beyond just listing table names. Each column has:
- Name
- SQL Server data type (with precision, e.g., varchar(25), varchar(50))
- Nullable flag
- Description (typically 1-3 sentences)

What's missing:
- **Primary/foreign key designations**: Only implicitly documented through descriptions (e.g., "sPatientID" is described as a unique patient identifier)
- **Enumerated value sets**: Most coded fields describe possible values narratively rather than listing them
- **Cardinality**: No documentation of one-to-many or many-to-many relationships
- **Indexes or constraints**: Not documented
- **Change history**: Single "Last Modified" date, no record of what changed

### OneOncology HIE Integration (CHPL ID 11640)

The certification page at https://flatiron.com/certification covers only OncoEMR (CHPL ID 11115). The OneOncology HIE Integration product (CHPL ID 11640, certified May 2025 for b(10) only) has **no documentation** on this page and is not mentioned anywhere in the page content.

This is a notable gap. The CHPL listing registers the same URL (https://flatiron.com/certification) as the mandatory disclosure page for both products, but the page only documents OncoEMR's export. The OneOncology HIE Integration — which may have a different data scope and export format as a health information exchange integration layer — has no publicly visible EHI export documentation.

## Access Summary
- Final URL (after redirects): https://flatiron.com/certification
- Status: found
- Required browser: no (PDF downloads work via curl)
- Navigation complexity: one_click (single link from certification page to data dictionary PDF)
- Anti-bot issues: none (Cloudflare present but not blocking; standard User-Agent sufficient)

## Obstacles & Dead Ends

- **No obstacles** encountered for the OncoEMR documentation. The page loaded cleanly, the PDF link worked directly, and the PDF contained real structured data.
- **OneOncology HIE Integration gap**: No documentation found for CHPL ID 11640. The product is certified for (b)(10) but has no corresponding EHI export documentation at the registered URL.
- The FHIR API documentation (https://flatiron.my.site.com/FHIR/s/) was not downloaded because it documents the (g)(10) standardized API, not the (b)(10) EHI export. The two systems are correctly maintained as separate by Flatiron.
