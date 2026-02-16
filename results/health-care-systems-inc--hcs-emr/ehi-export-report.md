# Health Care Systems, Inc. — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://www.hcsinc.net/meaningful-use/
- CHPL IDs: 11416
- Product: HCS eMR v10
- Certification date: 2023-12-20

## Navigation Journal

The registered URL (https://www.hcsinc.net/meaningful-use/) returns HTTP 403 Forbidden when accessed via curl with a standard User-Agent header. The entire hcsinc.net domain appears to block non-browser HTTP clients — both the homepage and WordPress upload URLs return the same 403 error page (a styled "403 - Forbidden" HTML page, 75,193 bytes).

However, the page loads normally in a real browser (Chrome). The site appears to use server-side bot detection that blocks curl/programmatic access but allows standard browser traffic.

**Steps taken:**

1. `curl -sI -L "https://www.hcsinc.net/meaningful-use/" -H 'User-Agent: Mozilla/5.0...'` → HTTP 403
2. `curl -sI "https://www.hcsinc.net/"` → HTTP 200 (homepage responds differently to HEAD vs GET for curl, but body is still the 403 page)
3. Navigated to https://www.hcsinc.net/meaningful-use/ in Chrome browser → page loads successfully
4. Took full-page screenshot of the Meaningful Use page (saved as `meaningful-use-page.png`)
5. The page contains three sections: "HCS eMR Real World Testing", "HCS EHI Export", and "ONC Certification"
6. Under "HCS EHI Export", found two links:
   - **"EHI Export Instructions"** → `https://hcsinc.net/wp-content/uploads/2024/12/EHIExportInstructionsHCSeMRv10.pdf`
   - **"EHI Data Dictionary"** → `https://hcsinc.net/wp-content/uploads/2024/12/HCSDataDictionary.csv`
7. Direct curl downloads of these files also returned the 403 page, so files were fetched via JavaScript `fetch()` from the browser's page context on `www.hcsinc.net` (the links point to `hcsinc.net` without www, but the www subdomain serves the same files)
8. PDF verified as valid PDF document (608,872 bytes, 2 pages). CSV verified as proper comma-separated values (253,996 bytes, 4,557 lines).

**Wayback Machine note:** The page was also available at `https://web.archive.org/web/20260215003835/https://www.hcsinc.net/meaningful-use/` and confirmed the same structure and links. The Wayback snapshot was used to identify file URLs before browser-based download.

## What Was Found

### 1. EHI Export Instructions PDF (2 pages, scanned document)

The PDF is a scanned paper document (produced by a Konica Minolta bizhub C364e scanner on 2023-12-19), so text extraction yields nothing — the content is only in the page images.

**Page 1** contains:
- **Product identification**: HCS eMR v10.0
- **Overview**: Describes a real-time export of all patient information stored in the EHR. The export is available without interacting with HCS Support or Developers. It produces a collection of comma-separated value (CSV) files and a readme file containing a hyperlink to the most up-to-date data dictionary. HCS maintains and updates this documentation as part of their release notes process.
- **User Access**: The EHI Export function is configurable but defaults to availability for Corporate Users. The "Corporate User" authorization role is typically assigned to Administrators and Analysts for EHR at the organization. Organizations use Active Directory to maintain access. The functions are built into HCS eMR at no additional charge and are available autonomously.
- **Instructions (Creating the Export)**: Users go to System→EHI Export. The menu/screen is the same Patient Selection tool used elsewhere in the application. Users can select a single patient by Visit Identifier, or a group of patients using various filter parameters. After selecting patient(s), users click "View Patients" to review the list, then "Export Patients" to perform the export.

**Page 2** contains:
- **Screenshot of the export interface**: Shows the "Electronic Health Information Export" screen with extensive filtering options including:
  - Active in Date Range and Patient Set
  - Active in Date Range
  - Active in Patient Set
  - All Currently Active
  - Admit Date Range and Patient Set
  - Admit Date Range
  - Discharge Date Range and Patient Set
  - Discharge Date Range
  - Discharge Date Range and Assigned to Staff
  - Discharge Date Range and Class
  - Not Discharged Date Range and Class
  - Patients with Address in Date Range
  - Patients with Address in Date Range and Prescriber
  - Any Entries in Date Range
  - Patients with Entries in Date Range and Prescriber
  - Patients with Entries in Date Range
- **Instructions (Reading the Export)**: The ZIP file exported to the user's "Downloads" directory contains a CSV file for each table in the HCS database. The data dictionary describes the data type and size of each field, plus a description of how the field is used and how it relates to other tables. The data dictionary is provided in CSV format for machine readability.
- **Key statement**: "The files exported as part of the HCS EHI Export contain all necessary data, including that which is not strictly personal health information, to allow the creation of a complete and fully usable HCS database with only the patient(s) that the users chose to export."
- **Attestation**: Signed by Reubin Felkey (Authorized Representative) on 12/18/2023, stating the documentation is complete with all required elements.

### 2. EHI Data Dictionary CSV (339 tables, 3,878 columns)

The CSV file has five columns: `Table`, `Column`, `Type`, `Size`, `Description`. It documents every table and column in the HCS database that is included in the EHI export. Each table has a header row (with table name and description) followed by its column definitions.

**Structure**: Tables are separated by blank lines. Each table's first row has only the Table and Description fields filled. Subsequent rows define individual columns with their SQL data types (bigint, varchar, int, datetime, decimal, bool, varbinary, etc.), sizes, and human-readable descriptions. Foreign key relationships are documented as "Reference to [TableName]" in the description field.

**Notable tables by domain:**

**Clinical core:**
- `Patient` (37 cols) — demographics, identifiers, SSN, DOB, gender, ethnicity, language, religion, marital status, veteran status, death info
- `PatientVisit` (48 cols) — admission/discharge, visit type, class, bed assignment, attending physician, diagnosis info
- `PatientAllergy` (20 cols) — allergy/intolerance records with severity, reaction, source
- `PatientDevice` (13 cols) — implantable device tracking (UDI)
- `PatientDocument` (16 cols) — clinical documents
- `PatientFamilyHistoryItem` (9 cols) — family history
- `PatientConsent` (23 cols) — consent documentation
- `PatientInsuranceCoverage` (27 cols) — insurance/coverage details

**Clinical observations and assessments:**
- `Observation` (88 cols) — the most detailed observation table with coded values, units, ranges, abnormal flags
- `ObservationGroup` (62 cols) — observation groupings/panels
- `ObservationGroupItem` (71 cols) — individual items within observation groups
- `VisitObservation` (46 cols) — visit-specific observations (vitals, labs, assessments)
- `VisitObservationSet` (58 cols) — observation sets with specimen collection details

**Diagnoses and problems:**
- `VisitDiagnosis` (13 cols) — diagnoses with coding system, rank, type
- `VisitProblem` (19 cols) — problem list with status, classification, evidence, related problems
- `Condition` (31 cols) — detailed condition records

**Medications and pharmacy:**
- `PatientOrder` (143 cols) — the largest table, covering all orders including medications, with extensive detail on dosing, frequency, route, prescriber, status, refills, DAW codes, controlled substance info
- `TherapyAdmin` (45 cols) — medication administration records
- `AdminProduct` (18 cols) — administered product details (dose, lot, manufacturer, expiration)
- `HCS_MedList` (27 cols) — medication list entries
- `MedRecItem` (29 cols) — medication reconciliation items
- `DispensableProduct`, `RoutedProduct`, `PackagedProduct`, `NamedProduct` — full drug product hierarchy

**Billing and financial:**
- `VisitCharge` (60 cols) — charges with CPT/HCPCS codes, revenue codes, diagnosis pointers, amounts, modifiers, NDC, service dates, units, expected reimbursement
- `ChargeClaim` (40 cols) — claim submissions with NCPDP messaging, payer responses, copay info
- `Payment` (12 cols) — payment records
- `PatientClaimResponse` (12 cols) — claim responses
- `CopayProduct`/`CopaySummary` — copay tracking
- `InsuranceCompany` (24 cols) — insurer master data
- `InsuranceContract` (9 cols) — contract details

**Care management:**
- `VisitIntervention` (33 cols) — clinical interventions with goals, objectives, outcomes (treatment plan components)
- `VisitCarePlan` (4 cols) — care plan records
- `VisitCareLevel` (7 cols) — level of care tracking
- `VisitConcern` (8 cols) — patient concerns
- `ConcernItem` (5 cols) — concern details

**Staff and provider:**
- `Staff` (80 cols) — provider/staff records with extensive detail (credentials, NPI, DEA, specialties)
- `StaffPractitionerID`, `StaffSpecialty`, `StaffIDCode` — provider identifiers

**Safety and compliance:**
- `VisitPhysicalLocation` (8 cols) — patient physical location tracking (proximity beacons for safety rounds)
- `NearMiss` (11 cols) — near-miss safety events
- `ClinicalAlert` (21 cols) — clinical alerts

**Other notable tables:**
- `VisitDocument` (19 cols) — visit-specific documents
- `VisitNote` (7 cols) — clinical notes
- `VisitInstruction` (14 cols) — discharge/care instructions
- `VisitImmunizationQuery` (11 cols) — immunization queries
- `VisitTransfer` (11 cols) — patient transfers between units
- `VisitFlag` (5 cols) — patient flags/alerts
- `ConsentDocument` (4 cols) — consent document storage
- `Chat`/`ChatMessage` (messaging)
- `Event`/`EventOccurrence` — scheduling/events

## Export Coverage Assessment

### Data Domain Coverage

This is an exceptionally thorough EHI export. HCS has taken the (b)(10) requirement seriously by exporting **the entire relational database structure** as CSV files — one per table — rather than limiting the export to a standardized clinical subset. The explicit statement in the instructions that the export contains "all necessary data... to allow the creation of a complete and fully usable HCS database" demonstrates genuine understanding of what a full EHI export means.

**Clearly covered domains:**
- **Demographics and patient identity**: Patient table with 37 columns including race, ethnicity, language, religion, marital status, veteran status, SSN, plus separate PatientAddress, PatientAlias, PatientContact, PatientIdentifier, PatientRace tables
- **Clinical encounters/visits**: PatientVisit (48 cols) with admission, discharge, class, attending, location
- **Diagnoses and problem lists**: VisitDiagnosis, VisitProblem, VisitProspectiveProblem, Condition tables
- **Medications**: PatientOrder (143 cols — the most detailed table), full pharmacy product hierarchy (DispensableProduct, RoutedProduct, PackagedProduct, NamedProduct), medication reconciliation (MedRecItem), medication list (HCS_MedList)
- **Medication administration**: TherapyAdmin (45 cols), AdminProduct, AdminVolume, AdminComponent, AdminField — detailed MAR data
- **Allergies**: PatientAllergy (20 cols)
- **Clinical observations/vitals/labs**: Observation (88 cols), ObservationGroup (62 cols), ObservationGroupItem (71 cols), VisitObservation (46 cols), VisitObservationSet (58 cols)
- **Procedures**: VisitProcedure (18 cols)
- **Devices**: PatientDevice (13 cols), DeviceIdentifier
- **Clinical documents**: PatientDocument, VisitDocument, VisitNote
- **Billing/charges**: VisitCharge (60 cols) with CPT, revenue codes, diagnosis pointers, amounts — genuinely detailed financial data
- **Claims**: ChargeClaim (40 cols), PatientClaimResponse, ClaimObservation
- **Insurance/coverage**: PatientInsuranceCoverage (27 cols), InsuranceCompany, InsuranceContract, VisitInsuranceCoverage, VisitInsuranceAuthorization, VisitEligibilityQuery
- **Payments**: Payment (12 cols), CopayProduct, CopaySummary
- **Treatment plans/interventions**: VisitIntervention (33 cols) with goals, objectives, outcomes — critical for behavioral health
- **Care plans**: VisitCarePlan, VisitCareLevel, VisitConcern
- **Consents**: PatientConsent (23 cols), VisitConsent, ConsentDocument
- **Safety data**: VisitPhysicalLocation (patient location tracking), NearMiss
- **Immunizations**: VisitImmunizationQuery, ImmunizationQueryForecast, ImmunizationQueryHistory
- **Discharge instructions**: VisitInstruction (14 cols)
- **Referrals/transfers**: VisitTransfer, VisitServiceLevel
- **Family history**: PatientFamilyHistoryItem
- **Clinical alerts**: ClinicalAlert (21 cols), ClinicalRelationship
- **Pharmacy management**: PBM tables (formulary, coverage, copay), DispenseBatch, product substitution, interaction checking
- **Scheduling/events**: Event, EventOccurrence, EventItem, CalendarDay
- **Staff/provider data**: Staff (80 cols) — provider context needed to interpret clinical records

**Behavioral health-specific coverage:**
While the data dictionary doesn't have tables explicitly named for behavioral health assessments (e.g., no "PHQ9" or "CSSRS" table), the behavioral health assessment data is stored in the **Observation/ObservationGroup/ObservationGroupItem** hierarchy. The Observation table alone has 88 columns and includes coded values, numeric results, text responses, and abnormal flags. The ObservationGroup (62 cols) and ObservationGroupItem (71 cols) tables provide the structure for multi-item assessment instruments. This generic observation model is how behavioral health EMRs typically store their 50+ assessment tools (PHQ-9, C-SSRS, ASAM, etc.) — each assessment is an ObservationGroup with items as ObservationGroupItems. This is a sound approach that exports the assessment data without hard-coding assessment tool names into the schema.

The `VisitIntervention` table (33 cols) with goals, objectives, and outcomes captures treatment plan data critical for behavioral health documentation.

**Potential gaps or areas of ambiguity:**
- **Clinical note full text**: While VisitNote and VisitDocument tables exist, it's unclear whether narrative note content (progress notes, H&P, discharge summaries) is stored as document content or as observations. The `VisitNote.NoteText` (if such a field exists in the 7-column table) or document binary content in `PatientDocument`/`VisitDocument` would contain this. The 7-column VisitNote table may be thin, but clinical notes could be stored as document attachments.
- **Imaging/radiology reports**: No explicit radiology or imaging table, though results likely flow through the Observation/ObservationSet pathway as they would for lab results.
- **Scanned documents and attachments**: `NamedImage` (11 cols) and `PatientDocument` tables exist, but it's unclear whether binary document/image content is included in the CSV export or omitted due to format limitations. The `WorkTask.AttachmentData` field is `varbinary`, suggesting binary data is part of the schema.

### Export Format & Standards

**Format**: The export is a **ZIP file containing CSV files** — one CSV per database table. This is a vendor-proprietary format (not FHIR, C-CDA, or any standard), but it is the most appropriate format for a complete database export of this nature.

**Strengths of this approach**:
- CSV is universally readable and machine-processable
- One-file-per-table preserves the relational structure
- The accompanying data dictionary (also CSV) provides complete metadata
- Foreign key relationships are documented ("Reference to [TableName]") allowing reconstruction of table joins
- Data types and sizes are specified for every column
- A third party could reconstruct the full database from these exports

**Limitations**:
- CSV cannot represent binary data (images, scanned documents) — it's unclear how varbinary columns are handled
- No explicit foreign key constraint definitions beyond the description text
- No value set documentation for coded fields (e.g., what values are valid for ProblemStatus, ActionCode, etc.)
- No sample export files are provided to verify the actual CSV structure

**This is genuinely a (b)(10) export, not a repackaged (g)(10)**. The export contains 339 tables covering the entire database — far beyond any FHIR/USCDI subset. It includes billing, pharmacy management, PBM data, work queues, safety rounding, scheduling, and other operational data tied to patient care. This is exactly what a full EHI export should look like.

### Documentation Quality

**Strengths:**
- The data dictionary is thorough: 339 tables, 3,878 columns, all with data types, sizes, and descriptions
- The data dictionary is in CSV format (machine-readable) — far better than a PDF
- Foreign key relationships are explicitly documented
- The export instructions are clear and actionable
- The attestation statement is specific about what the export includes

**Weaknesses:**
- The export instructions PDF is a **scanned paper document** — not searchable, not accessible, not version-controllable. This is the weakest element.
- No sample export files are provided
- No value set documentation for coded/enumerated fields (what are the valid values for `ProblemStatus`, `OrderStatus`, `ClaimType`, etc.?)
- Descriptions are generic ("Problem Code", "Action Code") — they say what the field is but not always what values it takes
- No explicit ER diagram or relationship diagram showing how tables connect
- No documentation of which tables correspond to which clinical workflows

**Could a developer implement an import?** Mostly yes. The data dictionary provides enough structural information to create a receiving database schema and load the CSV files. The foreign key references allow reconstruction of relationships. However, interpreting coded values and understanding the clinical semantics of the data would require additional knowledge of the HCS data model.

### Structure & Completeness

- **Granularity**: Field-level documentation with table name, column name, SQL data type, size constraint, and plain-English description for every field
- **Relationships**: Foreign keys documented via description ("Reference to [TableName]")
- **Data types**: Full SQL type information (bigint, varchar, int, datetime, decimal, bool, varbinary)
- **Constraints**: Size constraints specified where applicable (e.g., varchar(1000), decimal(15,5))
- **Value sets**: NOT documented — this is the main gap
- **Versioning**: The page states "HCS will update the data dictionary as the database structure evolves with each new version" but no version history is provided. File last-modified date is 2024-12-30.

## Access Summary
- Final URL (after redirects): https://www.hcsinc.net/meaningful-use/ (no redirect, same URL)
- Status: found (but requires browser — curl is blocked)
- Required browser: yes (site blocks curl/programmatic access with 403)
- Navigation complexity: direct_link (EHI section is immediately visible on the page with download links)
- Anti-bot issues: Server returns 403 Forbidden for non-browser HTTP clients. All curl requests (including with realistic User-Agent headers) are blocked. Browser-based access works fine.

## Obstacles & Dead Ends

1. **Anti-bot blocking**: The entire hcsinc.net domain returns 403 Forbidden for curl requests, even with standard User-Agent headers. This blocks both page access and file downloads. The server likely checks for additional browser-specific headers (Accept, Accept-Language, etc.) or uses challenge-response mechanisms. Files had to be downloaded via browser JavaScript `fetch()` calls and saved through browser DevTools network interception.

2. **PDF is a scan**: The EHI Export Instructions PDF was scanned from a paper document rather than created digitally, making text extraction impossible. Content was interpreted from rendered page images.

3. **File URLs use different subdomain**: The links on the page point to `hcsinc.net` (without www), but the site requires `www.hcsinc.net` for browser-context fetches. The non-www domain fails with CORS errors when fetched from the www page context.
