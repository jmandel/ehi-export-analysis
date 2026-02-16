# Veradigm — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://veradigm.com/legal/onc-reg-compliance/
- CHPL IDs: 11763
- Product: Veradigm EHR, version 26
- Certification date: 2025-12-31

## Navigation Journal

The registered URL is a static HTML compliance page hosted on AWS S3 via CloudFront. No JavaScript rendering or authentication required.

```bash
curl -sI -L "https://veradigm.com/legal/onc-reg-compliance/" -H 'User-Agent: Mozilla/5.0'
# HTTP 200, Content-Type: text/html, 250KB page
```

The page is a large compliance hub covering multiple Veradigm products. Searching the HTML source for "EHI Export" reveals a dedicated section titled "EHI Export Documentation" with links organized by product:

1. **Veradigm EHR** — one PDF link (v1, Nov 2023)
2. **Veradigm ePrescribe** — one PDF link (v1, Nov 2023)
3. **Veradigm FollowMyHealth** — two PDF links (v1 Nov 2023, v2 Feb 2024)
4. **Veradigm Practice Management** (noted as "non ONC certified") — two PDF links (v1 Dec 2023, v2 May 2024)
5. **Veradigm View** — six HTML doc site versions (v1 Apr 2025 through v6 Jan 2026)

All PDF links were direct downloads from `veradigm.com/img/legal/onc/...` paths:

```bash
curl -sL "https://veradigm.com/img/legal/onc/VeradigmEHR_EHI_Export_output_format_documentation_v1.pdf" -H 'User-Agent: Mozilla/5.0' -o VeradigmEHR_EHI_Export_output_format_documentation_v1.pdf
curl -sL "https://veradigm.com/img/legal/onc/VeradigmePrescribe_EHI_Export_Documentation_v1.pdf" -H 'User-Agent: Mozilla/5.0' -o VeradigmePrescribe_EHI_Export_Documentation_v1.pdf
curl -sL "https://veradigm.com/img/legal/onc/VeradigmFMH_EHI_Export_Data_Guide_v2.pdf" -H 'User-Agent: Mozilla/5.0' -o VeradigmFMH_EHI_Export_Data_Guide_v2.pdf
curl -sL "https://veradigm.com/img/legal/onc/EHIDataExportFile_ReferenceGuide_VeradigmPM_V2.pdf" -H 'User-Agent: Mozilla/5.0' -o EHIDataExportFile_ReferenceGuide_VeradigmPM_V2.pdf
curl -sL "https://veradigm.com/img/legal/onc/EHIDataExportFile_ReferenceGuide_VeradigmPM.pdf" -H 'User-Agent: Mozilla/5.0' -o EHIDataExportFile_ReferenceGuide_VeradigmPM.pdf
```

The FollowMyHealth v1 guide was also available at `https://fhir.followmyhealth.com/documentation/EHIExportDocumentation/v1` (returns a PDF directly despite the URL suggesting an API endpoint).

The Veradigm View documentation is a multi-page HTML site at `veradigm.com/legal/veradigm-view-ehi-export-documentation/v6/...` with 87 entity pages plus an index. Each entity page documents a single TSV file with a table of field definitions (Field Name, Data type, Field Description). Downloaded all 88 HTML files:

```bash
# Index page
curl -sL "https://veradigm.com/legal/veradigm-view-ehi-export-documentation/v6/index/" -H 'User-Agent: Mozilla/5.0' -o index.html
# Entity pages (87 pages, e.g.):
curl -sL "https://veradigm.com/legal/veradigm-view-ehi-export-documentation/v6/patient-demographics/" -H 'User-Agent: Mozilla/5.0' -o patient-demographics.html
# ... (all 87 entity pages downloaded in parallel)
```

The FMH PDF references FHIR extension definitions hosted at `fhir.followmyhealth.com/api/...`. Nine FHIR artifacts (3 StructureDefinitions + 3 CodeSystems + 3 ValueSets) were downloaded from those endpoints.

## What Was Found

Veradigm provides EHI export documentation for **five separate products** from a single compliance page. The ONC certification is specifically for "Veradigm EHR" (CHPL 11763), but the compliance page also documents exports from Practice Management, ePrescribe, FollowMyHealth, and Veradigm View. This reflects Veradigm's product architecture where the EHR is one component of an integrated suite.

### Veradigm EHR Export (89-page PDF, Nov 2023)

The EHR export produces **password-protected ZIP files** containing per-patient sub-ZIPs. Each patient ZIP has four folders:
- **Attachments** — images, documents, voice notes (jpg, gif, tif, png, wav, mp3, pdf, doc, xls, ppt, etc.)
- **Scanned Documents** — TIF files from Input Manager scanning
- **Transcriptions** — RTF files of transcriptions
- **Discrete Data** — JSON files organized by clinical domain

The Discrete Data folder contains **43 JSON files** across these clinical domains:
- **Demographics**: Demographics.json, PatientConsent.json, PatientContacts.json, PatientPhysicians.json
- **History**: HistoryDiagnosis.json, HistoryMedication.json (includes implantable devices)
- **Vitals**: Vitals.json
- **Diagnosis**: Diagnosis.json
- **Medications**: Medications.json, AdminMedications.json, RxOutputSummary.json
- **Procedures**: Procedures.json, ProceduresResult.json
- **Lab Orders**: LabOrders.json, LabResults.json
- **Referrals**: Referrals.json
- **Flowsheet**: FlowsheetDefinitions.json
- **Risk Management**: PatientRiskScore.json
- **Contact**: ContactData.json, ContactNotes.json
- **Encounter**: Encounter.json, EncounterAssessment.json, EncounterPlan.json, HpiData.json, HpiDataNotes.json, ChartAddendum.json
- **Immunization**: ImmunizationRecord.json, ImmunizationAddendum.json, ImmunizationVIS.json
- **Message**: SavedMessages.json, SavedMessageResults.json, SavedWebMessages.json
- **Questionnaire**: QuestionnaireRecords.json, QuestionnaireRecordResult.json, QuestionnaireRecordQuestionAnswer.json
- **Care Plans**: PatientCarePlans.json, PatientCarePlanEncounters.json, PatientGoals.json, PatientGoalBarriers.json, PatientAchieveGoals.json, PatientHealthConcerns.json
- **Additional files**: NoteAndAttachmentDetails.json, ScannedDocuments.json, Transcriptions.json, ChartAttachments.json

Each JSON file maps directly to a named EHR database table with field-level documentation including field names, descriptions, and SQL data types (VARCHAR, Integer, DateTime, etc.). The documentation is a genuine database-level data dictionary.

### Veradigm ePrescribe Export (TSV, Nov 2023)

Exports as **TSV (tab-separated values) files** in ZIP format. Contains 7 files per patient:
- Allergies.tsv, Demographics.tsv, Diagnosis.tsv, Historical Medications.tsv, Insurance.tsv, Prescriptions.tsv, Read Me.txt

Each TSV file is documented with database table names, primary keys, field names, descriptions, and SQL data types.

### Veradigm Practice Management Export (JSON, V2 May 2024)

Exports patient **financial/billing data** as JSON. Documents a claims-oriented JSON structure with:
- Practice and patient identification
- Voucher-level billing data (charges, payments, adjustments, balances)
- Provider, referring provider, responsible party, billing provider
- Claim information fields (prior authorization, condition codes, occurrence codes, value codes)
- Service-level details (procedure codes, descriptions, units, fees, modifiers, diagnoses)
- Payment transactions
- Specialty appendices for ambulance, drug, anesthesia, and dental information

### FollowMyHealth Export (FHIR R4 JSON, V2 Feb 2024)

Exports as a **FHIR R4 Bundle in JSON format** (plus raw documents/images) in a ZIP. Explicitly states: "This is not an implementation of SMART/HL7 Bulk Data Access (Flat FHIR). FollowMyHealth is not currently using any FHIR Profile, such as US Core in this implementation."

Supported FHIR resources: Account, AllergyIntolerance, Appointment, Bundle, Communication, Condition, DiagnosticReport, DocumentReference, Encounter, FamilyMemberHistory, Immunization, Invoice, Medication, MedicationRequest, Observation, Patient, Practitioner, Procedure.

Uses custom FHIR extensions for allergy status, health condition status, procedure status, and family member history. FMH is a Personal Health Record (PHR) that aggregates data from connected source EHRs.

### Veradigm View Export (TSV, V6 Jan 2026)

The most recently updated documentation. Exports as **TSV files** covering **87 entity types** with **1,194 documented fields**. Categories include:
- Demographics (communication settings, contacts, demographics, ethnicity, gender identity, guarantor, occupation, race, tribal affiliation)
- Clinical (advance directives, allergies, conditions, diagnoses, encounters, family history, goals, health concerns, healthcare devices, immunizations, medications, prescriptions, procedures, questionnaires, referrals, restrictions, risk scores, smoking status, vitals/observations)
- Labs (lab orders, order items, order documents, results, result tests/observations, result notes, specimens)
- Billing/Insurance (insurances, insurance eligibilities, superbills, superbill diagnoses, superbill events, superbill insurances, superbill procedures)
- Messaging (messages, message attachments, message recipients)
- Administrative (care teams, facilities, pharmacies, providers, users)

**Important**: The View documentation pages reference "Practice Fusion EHR" in entity descriptions. Veradigm acquired Practice Fusion in 2018 and appears to have rebranded it as "Veradigm View." This is a separate product from Veradigm EHR (formerly Allscripts Professional).

## Export Coverage Assessment

### Data Domain Coverage

**Veradigm EHR** (the certified product, CHPL 11763):

**Clearly covered:**
- Demographics, contacts, consent (comprehensive — 60+ fields)
- Problem lists / diagnoses (active and historical, with ICD/SNOMED coding)
- Medications (active, historical, administered, Rx summaries)
- Vitals
- Lab orders and results
- Procedures and procedure results
- Immunizations (including VIS records and addenda)
- Encounters (with assessment plans, HPI data, addenda)
- Care plans, goals, health concerns
- Referrals
- Flowsheet data (custom clinical worksheets)
- Clinical notes (via Transcriptions, ChartAddendum, encounter notes)
- Documents and attachments (images, scanned docs, voice notes)
- Messages (patient/provider messaging)
- Questionnaires (with question/answer detail)
- Risk management scores
- Implantable device data

**Covered via companion products (PM and ePrescribe):**
- Billing/claims data (via Practice Management export — vouchers, charges, payments, procedure codes, modifiers)
- Insurance information (via ePrescribe export)
- Detailed prescriptions (via ePrescribe export)

**Potentially missing or not clearly documented:**
- **Specialty-specific clinical data**: The product supports "nearly every medical specialty" with preloaded templates. The Flowsheet and Questionnaire tables may contain specialty-specific assessments, but the documentation does not describe what specialty data is captured or how custom forms/templates map to export fields. The export appears to use generic container tables (FlowsheetDefinitions, QuestionnaireRecords) that can hold specialty data, which is good for completeness but makes it hard to verify.
- **Prior authorization records**: ePrescribe has eAUTH, but the EHR export doesn't clearly include PA data. The PM export includes "Prior Authorization Number" as a claim field.
- **Imaging study data**: The Attachments folder includes image files, but there's no specific mention of DICOM or structured radiology data beyond chart attachments.

### Export Format & Standards

The Veradigm EHR uses a **proprietary JSON format** that is a direct database table export. This is a legitimate (b)(10) approach — it doesn't pretend to be FHIR and exports actual database fields with native names and types. Each JSON file maps to a named database table with documented primary keys.

**This is a genuine (b)(10) export, not a repackaged (g)(10) FHIR API.** The export covers data domains well beyond USCDI/US Core — it includes internal database IDs, audit fields, flowsheet data, questionnaire responses, risk scores, scanned documents, and practice-specific metadata that would never appear in a standardized FHIR API.

Relationships between entities are expressed through foreign key fields (PatientID, EncounterId, ContactId, etc.) appearing across tables. A developer could reconstruct the patient record, though the lack of formal relationship documentation adds friction.

### Documentation Quality

**Strong aspects:**
- Field-level documentation with descriptions, data types, and database table names
- Clear folder hierarchy documentation with screenshots
- Password protection and extraction instructions
- 89-page depth for the EHR export alone
- Practice Management appendix with exhaustive claim field listings
- Veradigm View has 87 entity pages with 1,194 fields

**Weaknesses:**
- Only version 1 (Nov 2023) for the EHR — no updates in 2+ years despite ongoing product development
- No sample export files or example JSON/TSV data
- No machine-readable schema files (JSON Schema, XSD, etc.)
- No explicit documentation of relationships between tables (foreign keys implied but not formally specified)
- No value set documentation — fields like PatientMaritalStatus, Race, Ethnicity are VARCHAR(255) with no enumeration of allowed values
- The documentation references "Veradigm EHR 23.4 and higher" but the certified version is 26 — unclear if v1 documentation covers changes in versions 24-26

### Structure & Completeness

Field-level granularity is high — each table has field names, descriptions, and SQL data types. However:
- No cardinality documentation (required vs. optional)
- No value set definitions for coded fields
- No explicit foreign key/relationship documentation
- No change history beyond initial publication
- The Veradigm View documentation (87 entities, 1,194 fields) is more granular than the EHR export (43 JSON files), reflecting different product architectures

### Overall Assessment

Veradigm has done genuine (b)(10) work. The EHR export is a real database-level export with password-protected ZIP files containing the patient's clinical record in JSON format, plus actual documents, images, scanned documents, and transcriptions. This is not a FHIR API repackaging.

The breadth across five products is notable — when a customer uses the full Veradigm suite (EHR + PM + ePrescribe + FMH), the combined exports cover clinical data, billing/claims, prescriptions, and patient portal data. This is more comprehensive than many vendors.

The main gaps are in documentation maintenance (only v1 from Nov 2023 for the core EHR) and missing data quality metadata (no value sets, no cardinality, no sample data). A developer could implement an import from this documentation but would need significant discovery work around coded values and entity relationships.

## Access Summary
- Final URL (after redirects): https://veradigm.com/legal/onc-reg-compliance/
- Status: found
- Required browser: no
- Navigation complexity: one_click (EHI section visible in page source, direct PDF links)
- Anti-bot issues: none

## Obstacles & Dead Ends

None significant. All documentation was publicly accessible without authentication. The only minor issue was the FollowMyHealth v1 URL at `fhir.followmyhealth.com` returning HTTP 405 on HEAD requests but serving the PDF correctly on GET.
