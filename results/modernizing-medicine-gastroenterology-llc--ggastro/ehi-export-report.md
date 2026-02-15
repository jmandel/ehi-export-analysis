# Modernizing Medicine Gastroenterology, LLC — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://www.modmed.com/onc-certification-gi/
- CHPL IDs: 11054
- Product: gGastro v6 (certified 2022-12-07)
- Developer: Modernizing Medicine Gastroenterology, LLC (formerly gMed, Inc.)

## Navigation Journal

1. **Initial probe via curl** returned HTTP 403 (Cloudflare protection):
   ```bash
   curl -sI -L "https://www.modmed.com/onc-certification-gi/" -H 'User-Agent: Mozilla/5.0'
   # Result: HTTP/2 403, Cloudflare challenge page
   ```

2. **Navigated via browser** to `https://www.modmed.com/onc-certification-gi/` — page loaded successfully. No JavaScript SPA complexity; it's a WordPress page with static content.

3. **Found EHI Export Documentation section** directly on the page under an H4 heading "EHI Export Documentation" with two PDF links:
   - "Data Dictionary for ModMed gGastro EHI Export" → `https://www.modmed.com/wp-content/uploads/2025/12/crp-13761-gGastro-EHI-Patient-Export-Specifications.pdf`
   - "Data Dictionary for ModMed gGastro EHI Export Additional" → `https://www.modmed.com/wp-content/uploads/2025/12/crp-13761-gGastro-EHI-Patient-Export-Specifications-Additional.pdf`

4. **Downloaded both PDFs** (curl worked for downloads despite Cloudflare blocking the HTML page):
   ```bash
   curl -sL -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36' \
     -o gGastro-EHI-Patient-Export-Specifications.pdf \
     "https://www.modmed.com/wp-content/uploads/2025/12/crp-13761-gGastro-EHI-Patient-Export-Specifications.pdf"

   curl -sL -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36' \
     -o gGastro-EHI-Patient-Export-Specifications-Additional.pdf \
     "https://www.modmed.com/wp-content/uploads/2025/12/crp-13761-gGastro-EHI-Patient-Export-Specifications-Additional.pdf"
   ```

5. **Verified downloads**: Both confirmed as PDF documents. 14.4 MB (167 pages) and 16.9 MB (551 pages) respectively. Author: Isaac Tobelem. Created: 2025-12-30. Version 6.5.3.20251230.

6. **Page also links to**: Technical API Documentation (https://portal.api.modmed.com/), Intervention Risk Management, Real World Testing Plans/Results, Mandatory Disclosures, and gGastro 6 Certificate. Only the EHI Export Documentation links were downloaded as the others are not EHI-export-specific.

7. **No embedded URLs or attachments** in either PDF. The documents are self-contained.

## What Was Found

### Overview

ModMed has produced an exceptionally thorough EHI export specification for gGastro. The export is a **CSV-based package** containing discrete data from the patient record plus associated documents (MHT, PDF, JPG, etc.). The documentation is organized into five sections:

1. **CSV Files Dictionary** — Field-level specifications for 441 CSV files (tables), covering 4,453 total fields. Each field is documented with column position, name, data type (GUID, Alphanumeric, Numeric, Boolean, Decimal, Date & Time, Score), maximum length, and format/translation references.

2. **Data Schema** — A tree-like hierarchical view showing how all 441 tables relate to each other through foreign key relationships. The tree is rooted at the `Patient` table and shows 574 parent-child relationships. This is critical for reconstructing the full patient record from the exported CSV files.

3. **Translations** — 1,157 value set / lookup tables providing human-readable values for coded fields. These range from small enumerations (e.g., "Active Inactive Criteria": 0=Only Active, 1=Only Inactive, 2=Both) to large GUID-based reference tables (e.g., "Address Type" with GUID codes for Home, Work, Mailing, Billing, etc.).

4. **Patient Documents** — Instructions for reconstructing file paths to patient documents included in the export package. Document types include:
   - **Service Documents**: Encounter notes stored as MHT files, located via `ServiceDocumentVersion` table
   - **Imaging Documents**: Faxes, scans, imports, lab results (JPG, PDF, etc.), located via `ImagingDocument` + `ImagingDocumentPage` tables
   - **Patient Portal Documents**: Statements and published documents, located via `PatientPortalDocument.FilePath`
   - **Letters**: Recall and correspondence documents (MHT), located via `LetterQueueFile` table

5. **Glossary** — 23 term definitions for domain-specific abbreviations (AGA, CAHPS, CPT, GIQuIC, LOINC, etc.).

### The Additional PDF (551 pages)

The second PDF contains only two very large translation tables that were too big for the main document:
- **Occupation** — A comprehensive lookup of GUID-to-occupation-name mappings (appears to be the full SOC/O*NET occupation taxonomy, spanning ~41,000 lines of text)
- **Occupation Industry** — A similar comprehensive GUID-to-industry mapping

These support the `PatientOccupationHistory` table in the main export.

### Export Format

The export is a **flat file (CSV) package** with:
- One CSV file per table/entity (441 files)
- GUID-based primary and foreign keys linking tables together
- A hierarchical relationship tree rooted at `Patient`
- Associated document files organized in a `Documents\` folder structure by year, type, and date
- Translation tables providing human-readable values for all coded fields
- All dates in `MM/dd/yyyy hh:mm:ss.fff tt` format
- Boolean fields as `0 = False / 1 = True`

This is a **genuine (b)(10) export** — it is clearly not a repackaged FHIR API. The export format is a proprietary CSV dump of the application's database schema, covering far more data domains than USCDI/US Core.

## Export Coverage Assessment

### Data Domain Coverage

This is one of the most comprehensive EHI export data dictionaries encountered. Comparing against the product research:

**Clinical data — Fully covered:**
- Patient demographics (30 fields in `Patient`, 36 fields in `Person`, plus `UsaAddress`, `Phone`, `Email`, `EmergencyContact`)
- Diagnoses/conditions (`PatientDiagnosis` with 21 fields, `PatientDiagnosisHistory` with 14 fields, `ServiceDiagnosis`)
- Medications (`Medication` with 41 fields, `MedicationHistory` with 44 fields, `MedicationSnapshot`, `MedicationWarning`, `MedicationDiagnosis`)
- Prescriptions (`Prescription` with 30 fields, `PrescriptionQueue`, `PrescriptionSig`, `PrescriptionWarning`, `PrescriptionFormularyWarning`, `PrescriptionInsurance`, `PrescriptionSample`, renewal requests)
- Allergies (`PatientAllergy` with 24 fields, `PatientAllergyHistory`, `PatientAllergyReview`)
- Immunizations (`PatientImmunization` with 38 fields, `ExportImmunization`, `CvxCodePerPatientImmunization`)
- Lab results (`InterfaceResult` with 53 fields, `InterfaceTest` with 23 fields, `InterfaceTestResult` with 19 fields, `InterfaceSpecimen`, `InterfaceRequisition`)
- Vital signs (`VitalSigns` with 27 fields, `BloodPressure`, `VitalSignsMonitorSession`)
- Clinical observations and physical measurements (`PhysicalMeasurement` with 19 fields)
- Implantable devices (`PatientImplantableDevice` with 25 fields)
- Care plans and goals (via `ServiceDocument`, clinical notes)
- Clinical notes/documents (`ServiceDocument` with 18 fields, `ServiceDocumentVersion`, `ServiceDocumentSection`, `ServiceDocumentSignature`, `ChartNotes`)
- Orders (`Order` with 50 fields, `OrderNotes`, `OrderAUC`)
- Referrals (`ReferringPhysicianPerPatient`, `ServiceReferringPhysician`)
- Family history (`PatientFamilyMember` with 10 fields, `PatientFamilyMemberDiagnosis`)
- Social history (`PatientSocialHistory`, `PatientSmokingStatusHistory`, `PatientTobaccoHistory`, `PatientAlcoholHistory`, `PatientCaffeineHistory`, `PatientDrugHistory`, `PatientExerciseHistory`, `PatientSexualHistory`, `PatientOccupationHistory`)

**GI/Endoscopy-specific clinical data — Fully covered:**
- Endoscopy procedure documentation (`ServiceProcedure` with 14 fields, `ProcedureOverview` with 43 fields, `ProcedureOverviewLandmark`, `ProcedureOverviewSiteReached`, `ProcedureOverviewSitePoorlyVisualized`, `ProcedureOverviewSurgicalSite`, `ProcedureOverviewEusSiteVisualized`)
- Findings (`Finding` with 155 fields — the largest table, reflecting the richness of endoscopic finding documentation; `FindingCode`, `FindingSite`, `FindingSegments`, `FindingImageService`)
- Interventions (`Intervention` with 115 fields — the second largest; `InterventionSite`)
- Anesthesia/sedation (`AdministeredMedication`, `AnesthesiaComplication`, `AsaClass`, `AldreteScore`, `Oxygen`, `IvFluid`, `IvSetup`, `IvDiscontinued`, `InfusionSession`, `InfusionLotExpiration`)
- Nursing documentation (`NursingComplication`, `PainAssessment`, `Npo`, `GeneralWellBeing`)
- Preparation (`Preparation` with 10 fields)
- Time markers (`ServiceTimeMarker`)
- Instruments (`Instrument` with 8 fields)
- Procedure coding (`ProcedureCodingAdvisor`, `ProcedureCodingDiagnosis`, `ProcedureCodingProcedure`, and modifier tables)
- GI-specific disease tracking (`PatientDisease`, `PatientDiseaseIBD` with 14 fields, `PatientMontrealClassification`, `ExtraIntestinalManifestations`)
- GI disease scoring systems (`PatientDiseaseScoringSystem` plus AD8, Full MSI, HBI, MSI, PHQ9 variants)
- AGA registry exports (`AgaExport`, `AgaService`, `AgaServiceDetail`)
- GIQuIC quality export (`GiquicExport` with 149 fields)
- Stress test data (`StressTest` with 19 fields)
- Nuclear perfusion (`NuclearPerfusion`, `NuclearPerfusionInjection`)
- Cardiology procedures (`CardiologyProcedure`)
- Carotid ultrasound (`CarotidUltrasound`, `CarotidUltrasoundMeasurement`)
- Transthoracic echo (`Tte` with 41 fields)

**Billing and financial data — Fully covered:**
- Charges (`BillingCharge` with 25 fields, `BillingChargeBalance`, `BillingChargeTransaction`, modifiers)
- Claims (`BillingClaim` with 16 fields, `BillingClaimEvent`, `BillingClaimSnapshot` with 95 fields, plus charge-level, diagnosis-level, modifier-level, and payment-level snapshot tables)
- EDI claim payments (`BillingEdiClaimPayment` with 22 fields and 15+ related sub-tables for claim adjudication detail)
- Encounters (`BillingEncounter` with 30 fields, `BillingEncounterDiagnosis`)
- Superbills (`BillingSuperbill` with 43 fields, plus diagnosis, procedure, modifier, condition code, e-code, value code, import, and import detail tables)
- Patient balances (`BillingPatientBalance`, `BillingInsuranceBalance`, `BillingChargeBalance`)
- Patient billing information (`BillingPatientBillingInformation` with 15 fields)
- Statements (`BillingPatientStatementHistory` with 43 fields, plus charge and transaction sub-tables)
- Payments/refunds (`BillingPaymentAdjustmentRefund` with 33 fields, electronic refunds, per-patient breakdowns)
- Prepayments (`BillingPatientPrepay` with 21 fields, events)
- Collections (`BillingCollection`, `BillingCollectionEvent`, `BillingCollectionPaymentPlan`)
- Online payments (`BillingOnlinePayment` with 22 fields)
- Cost estimation (`BillingPatientCostEstimation`, events)
- Insurance (`Insurance` with 35 fields, `Eligibility`, `EligibilityInsurance`, `BillingEligibility`, authorizations)
- Credit card processing (`BillingCreditCardProcessingOneTimeKey`, `CreditCardNotificationEvents`)
- Patient episodes (`BillingPatientEpisode`)
- Patient invoices (`BillingPatientInvoice`)
- Patient ledger (`BillingPatientLedger`)

**Patient engagement — Covered:**
- Patient portal (`PatientPortalUser`, `PatientPortalAccessLog`, `PatientPortalDocument`, `PatientPortalMessage`, `PatientPortalMessageAttachment`, `PatientPortalRegistration`, `PatientPortalRos`, `PatientPortalUpdateRequest`, `PatientPortalAlternateUser`, `PatientPortalChallenge`, `PatientPortalDocumentQueue`, `PatientPortalAppointmentUpdate`, `PatientPortalUserPreferences`)
- Kiosk data (`AppointmentKioskSnapshot`, `AppointmentKioskSectionSnapshot`, `PatientKioskDevice`)
- Recalls (`Recall`, `RecallEvent`)
- Patient reminders (`PatientReminder`, `AppointmentReminderCurrentStatus`, `AppointmentReminderEventLog`, `BalanceReminderEventLog`, `BillingBalanceReminderEvent`)

**Practice management — Covered:**
- Appointments (`Appointment` with 38 fields, `AppointmentSet`, `AppointmentHold`, `AppointmentStatusHistory`, `AppointmentWaitDay`, `AppointmentExternal`, `AppointmentAttachment`)
- Tasks (`Task` with 15 fields, `TaskAttachment`, `TaskFile`, `TaskNotes`, `TaskRecipient`, `TasksPerLocation`)
- Faxing (`FaxOutboundQueue`, `FaxOutboundQueueAudit`, `FaxOutboundQueuePage`, `FaxOutboundQueueStaff`)
- Direct messaging (`DirectMailbox`, `DirectMessage`, `DirectMessageAttachment`, `DirectMessageRecipient`)
- Document management (`ImagingDocument` with 38 fields, `ImagingDocumentPage`, `ImagingDocumentNotes`, `ImagingDocumentSignature`, etc.)

**Other covered domains:**
- Quality measures (`AscQualityMeasures`, `MipsReportExecutionAciDetail`, `MipsReportExecutionQualityDetail`)
- Telehealth (`TelehealthPatient`, `TelehealthRoomInvite`, `TelehealthService`)
- Patient advance directives (`PatientAdvancedDirectives`)
- Functional/cognitive status (`FunctionalCognitiveStatus`)
- Patient identifiers (`PatientIdentification`, `PatientIdExternalMapping`, `PatientAccountNumber`)
- Provider-patient relationships (`ProviderPerPatient`, `UserPerPatient`)
- C-CDA documents (`PatientCcdaDocument`, `PatientCcdaDocumentIncorporate`, `ServiceCcdaVersion`)
- ECR documents (`PatientEcrDocument`)
- Syndromic surveillance (`SyndromicSurveillance`)
- Questionnaire responses (`QuestionnaireResponse`)
- Chart bookmarks and captures (`ChartBookmark`, `ChartCapture`)
- Coding advisor data (`CodingAdvisor` with 29 fields, 2021 variant, MDM modes)
- Guideline actions/overrides (`GuidelineAction`, `GuidelineOverride`)
- Standing orders (`PhysicianStandingOrder`, `PhysicianStandingOrderSection`)
- Rounding lists (`RoundingList` with 17 fields, plus notes, billing, diagnosis, and procedure sub-tables)
- Patient data export tracking (`PatientDataExport`, `PatientDataRestrictionResponse`)
- Patient merge history (`PatientMerge`)
- Demographics granularity (race, ethnicity, gender identity, tribal affiliation, disability — `PersonRace`, `PersonRaceGranularity`, `PersonEthnicityGranularity`, `PersonGenderIdentity`, `PersonTribalAffiliation`, `PersonSelfdisclosedDisability`)

**Domains with no apparent gaps**: The export covers essentially every clinical, billing, and patient-facing data domain described in the product research. The Finding table (155 fields) and Intervention table (115 fields) are particularly impressive — they capture the full richness of endoscopic procedure documentation that is the core differentiator of gGastro.

### Export Format & Standards

- **Format**: Proprietary CSV dump — not FHIR, C-CDA, or any other standard format. This is appropriate for a (b)(10) export since the goal is completeness, not standardization.
- **Relationships**: Expressed through GUID-based foreign keys with a documented hierarchical schema tree. A third party can reconstruct the full record by following the relationship tree.
- **Value sets**: All coded fields reference named translation tables with explicit code-to-value mappings.
- **Documents**: Included as actual files (MHT, PDF, JPG, etc.) with documented path construction rules.
- **Suitability**: Excellent. The CSV format with documented relationships and translations provides everything needed to reconstruct a complete patient record. A developer could write an importer based solely on this documentation.

### Documentation Quality

- **Readability**: Excellent. The document is well-organized with clear section divisions. The rendered tables are clean and professionally formatted.
- **Field definitions**: Every field has a column index, name, data type, and (where applicable) maximum length and format/translation reference. This is field-level documentation, not just table-level.
- **Value sets**: Comprehensive. The 1,157 translation tables in the main document plus the two massive occupation/industry tables in the supplemental document cover all coded fields.
- **Relationships**: The data schema tree is a standout feature — it shows the complete hierarchical structure from Patient down to every child table, with the joining field specified.
- **Document reconstruction**: Clear instructions with path templates and examples for each document type.
- **Glossary**: Includes key domain-specific terms.
- **Sample data**: No sample export files are provided, but the documentation is detailed enough that samples are not strictly necessary.
- **Versioning**: The document is versioned (6.5.3.20251230) and recently updated (December 2025).

### Structure & Completeness

- **Granularity**: Field-level. Every field in every table is documented with type, length, and format.
- **Coded fields**: All reference their translation tables by name.
- **Relationships**: Fully documented in the data schema tree.
- **Completeness**: 441 tables, 4,453 fields, 574 relationships, 1,157+ translation tables. This is an exceptionally comprehensive data dictionary.

### Overall Assessment

This is an exemplary EHI export implementation. ModMed has clearly done real (b)(10) work here — this is not a repackaged FHIR API or a compliance checkbox. Key strengths:

1. **True full-record export**: 441 tables covering every aspect of the patient record — clinical, billing, scheduling, documents, portal interactions, and specialty-specific GI data.
2. **GI-specific depth**: The Finding (155 fields) and Intervention (115 fields) tables capture the full richness of endoscopic procedure documentation, including polyp details, sites, instruments, techniques, and complications. The GIQuIC export table (149 fields) shows integration with GI quality registries.
3. **Complete billing coverage**: Over 70 billing-related tables covering charges, claims, EDI payments, statements, collections, and refunds at granular detail.
4. **Document inclusion**: Actual patient documents (notes, scans, faxes, lab results) are included with clear path construction rules.
5. **Relationship documentation**: The hierarchical data schema tree is essential for a third party to reconstruct the patient record from flat CSV files.
6. **Translation completeness**: Over 1,150 value set tables ensure coded fields are interpretable.

The only notable omission is the lack of sample export files — but given the quality of the specification, a developer could implement an importer without them.

## Access Summary
- Final URL (after redirects): https://www.modmed.com/onc-certification-gi/
- Status: found
- Required browser: yes (Cloudflare blocked curl for HTML page; PDFs downloadable via curl with User-Agent)
- Navigation complexity: direct_link (EHI Export Documentation section visible on the main page, no accordion or multi-page navigation)
- Anti-bot issues: Cloudflare protection on HTML page (403 response to curl), but PDF downloads work with User-Agent header

## Obstacles & Dead Ends
- Cloudflare returned HTTP 403 for the main HTML page when accessed via curl. Browser navigation worked without issue. PDF direct download URLs worked via curl with a standard User-Agent header.
- No other obstacles encountered. The documentation was clearly labeled, easily accessible, and comprehensive.
