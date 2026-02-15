# VisionWeb — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://help.youruprise.com/m/72283/l/1745699-data-export
- CHPL IDs: 11069
- Product: Uprise 3.1
- Certification date: 2022-12-13

## Navigation Journal

1. **Initial probe:**
   ```bash
   curl -sI -L "https://help.youruprise.com/m/72283/l/1745699-data-export" -H 'User-Agent: Mozilla/5.0'
   ```
   Result: HTTP 200, Content-Type: text/html. The page is hosted on ScreenSteps (screenstepslive.com) behind Cloudflare. No redirects.

2. **Fetched page HTML:**
   ```bash
   curl -sL "https://help.youruprise.com/m/72283/l/1745699-data-export" -H 'User-Agent: Mozilla/5.0' -o page.html
   ```
   35,826 bytes. The page is a simple ScreenSteps article within the "MIPS Guide" manual, under the chapter "Electronic Health Information (EHI) Export."

3. **Page content:** The page has a brief introductory paragraph about the ONC 170.315(b)(10) EHI Export requirement, then a single downloadable PDF attachment: "Data Export.pdf." Page was last updated April 9, 2024.

4. **Downloaded the PDF:**
   ```bash
   curl -sL "https://media.screensteps.com/attachment_assets/assets/008/241/511/original/Data%20Export.pdf" -o Data_Export.pdf
   ```
   Verified: PDF document, 58 pages, 879,710 bytes. Created by Philip Lu on 2024-02-20 using Microsoft Word for Microsoft 365.

5. **Checked parent section:** Visited `https://help.youruprise.com/m/72283/c/425478` (the "Electronic Health Information (EHI) Export" chapter). It contains only the one "Data Export" article — no additional sub-pages or documents.

6. **Checked sibling pages:** The MIPS Guide manual contains articles on MIPS Overview, Quality Measurements, Promoting Interoperability, Improvement Activities, and MIPS Reports/Data Submission. None of these are relevant to the EHI export data dictionary.

7. **Took browser screenshot** of the live page confirming the layout: breadcrumb navigation, introductory text, and the PDF download link.

## What Was Found

The documentation consists of a single, comprehensive 58-page PDF titled "Data Export" that serves as both a user guide and a data dictionary for the EHI export.

### Export Mechanism
- The export is accessed via the **"Patient Export" section in Practice Management**
- Exports produce a **.zip file** containing multiple files
- The primary data files are in **.csv format** (comma-separated, first line is header)
- Each row after the header represents a piece of patient data
- Additional files include **images and .xml data**, referenced by the CSV files

### Data Dictionary
The PDF documents **76 distinct CSV files** that comprise the export, organized as two-column tables (Data field name | Description). The CSV files cover:

**Clinical Data:**
- AllergyIntolerance.csv — allergy codes, reactions, severity, substances
- CarePlan.csv — care plans with categories and titles
- ClinicalImpression.csv — assessment notes, general notes, medication notes
- Condition.csv — diagnoses with ICD codes, body sites, severity
- ConditionChiefComplaint.csv — chief complaints with timing, signs/symptoms
- ConditionConcern.csv — health concerns
- ConditionFunctionalCognitive.csv — functional/cognitive status
- CommunicationEducation.csv — patient education records
- Goal.csv — clinical goals with lifecycle status
- Images.csv — diagnostic images with OS/OD references, body sites
- Immunizations.csv — immunization records with codes, lots, routes, VFC category
- MedicationRequest.csv — medication prescriptions with dosage, dispense, refills
- ObservationBinocularVision.csv — binocular vision exam data
- ObservationKeratometry.csv — keratometry measurements
- ObservationLabResults.csv — lab results with codes, values, units, reference ranges
- ObservationLifeStyle.csv — lifestyle observations
- ObservationPFSH.csv — past/family/social history
- ObservationPhysicalExam.csv — physical exam findings
- ObservationReviewOfSystem.csv — review of systems
- ObservationVitals.csv — vital signs with codes, values, units

**Optometry-Specific Clinical Data:**
- Prescription.csv — extremely detailed optical prescriptions (spectacle and contact lens Rx with sphere, cylinder, axis, prism, base curve, diameter, addition values for both eyes, keratometry readings, manifest refraction data)
- PrescriptionAddOn.csv — prescription add-on details
- Procedure.csv — procedures with OD/OS-specific reason codes, severity, reliability
- ProcedureDilation.csv — dilation procedures with up to 4 medications, routes, techniques
- ProcedureDilationRemarks.csv — dilation remark codes
- ProcedureIOPs.csv — intraocular pressure measurements
- ProcedureIOPsTargets.csv — IOP targets for OD/OS
- ProcedureOther.csv — other procedures with images
- ProcedureScreening.csv — screening procedures with images
- RefractionAutorefraction.csv — autorefraction data (OD/OS/OU)
- RefractionContactLensRx.csv — highly detailed contact lens refraction data (over 100 fields per eye including product details, over-refractions, observations)
- RefractionCyclopegic.csv — cycloplegic refraction
- RefractionManifest.csv — manifest refraction with lens conditions
- RefractionRetinoscopy.csv — retinoscopy data
- RefractionSpectacleRx.csv — spectacle Rx with lens type, design, material, lab instructions
- RefractionSpectacleRxAddOns.csv — spectacle Rx add-ons
- RefractionWavefront.csv — wavefront refraction data

**Patient Demographics & Administration:**
- Patient.csv — demographics, gender identity, sexual orientation, ethnicity, race, language, employment, HIPAA/financial responsibility dates
- PatientAccount.csv — account balances, charges, payments, write-offs, transfers
- PatientAddress.csv — addresses
- PatientAlert.csv — patient alerts
- PatientDocumentReference.csv — attached documents
- PatientEmail.csv — email addresses
- PatientLinkedAccount.csv — linked/related accounts
- PatientLocation.csv — preferred locations
- PatientNote.csv — patient notes
- PatientPaymentCard.csv — payment card references
- PatientPhoneNumber.csv — phone numbers
- PatientPreference.csv — contact preferences
- Contact.csv — contact records (demographics, addresses)
- ContactLinkedAccount.csv — contact relationships
- Device.csv — UDI devices (carrier, lot, serial, manufacturer)
- Questionnaire.csv — questionnaire responses

**Billing & Financial:**
- Claim.csv — extremely detailed claim records (~80+ fields including billing provider, referring provider, CMS-1500 box fields, accident info, disability dates, prior auth)
- ClaimDiagnosis.csv — claim diagnosis codes (ICD-9/ICD-10)
- ClaimLine.csv — claim line items with place of service, units, prices, modifiers
- ClaimLineCodes.csv — claim line codes with diagnosis pointers
- ClaimNote.csv — claim notes
- ClaimStatus.csv — claim status tracking
- Invoice.csv — invoices with balance, transaction type
- InvoiceLine.csv — invoice line items with pricing, insurance/patient responsibility, modifiers, tax
- InvoiceLineAdjustment.csv — adjustments, discounts, write-offs
- InvoiceLineDiagnosis.csv — invoice line diagnosis codes
- Payment.csv — payments with method, payer, remittance
- PaymentItem.csv — payment application details

**Insurance & Benefits:**
- Benefit.csv — insurance benefits with classification
- BenefitCoverageElectronic.csv — electronic eligibility/coverage responses (~30 fields)
- BenefitCoverageManual.csv — manual benefit coverage entries with enhancements, frequency, allowances
- Policy.csv — insurance policies with member IDs, payer plans
- PolicyNote.csv — policy notes

**Scheduling & Recall:**
- Appointment.csv — appointments with provider, technician, visit reason
- Encounter.csv — encounters with class, service type, participants, recall info
- EncounterProceduresDiagnosis.csv — encounter-level procedures with diagnosis codes
- Recall.csv — patient recall with delivery method, reason

**Orders & Products:**
- RxOrder.csv — extraordinarily detailed optical orders (~120+ fields including frame specs, lens measurements, trace data, shipping, pricing, keratometry, manifest values, personalization)
- Product.csv — product catalog entries (frames, lenses, contact lenses with specifications)
- ServiceRequest.csv — service/lab requests with LOINC codes
- Task.csv — clinical tasks

**Reference/Administrative:**
- Locations.csv — practice locations with addresses, NPI
- Provider.csv — provider records with credentials, DEA, license
- DocumentReference.csv — document references

## Export Coverage Assessment

### Data Domain Coverage

This is an **exceptionally comprehensive** EHI export that goes well beyond what most vendors provide for (b)(10) compliance. The 76 CSV files cover essentially every major data domain that an optometry EHR/PM system would store:

**Clearly covered:**
- Patient demographics (extensive, including SOGI data, race/ethnicity)
- Allergies and adverse reactions
- Conditions/diagnoses (with ICD codes, body sites, chief complaints, concerns, functional/cognitive status)
- Medications/prescriptions (both pharmaceutical and optical Rx — spectacle and contact lens prescriptions with extraordinary detail)
- Lab results
- Vital signs
- Immunizations
- Clinical impressions/notes
- Care plans and goals
- Procedures (including optometry-specific: dilation, IOPs, screening)
- Encounter/visit data
- Documents and images (referenced by file path)
- Billing: claims (with full CMS-1500 field mapping), invoices, payments, adjustments
- Insurance: policies, benefits, electronic and manual coverage determinations
- Optical dispensing: orders with frame/lens specifications, trace data, shipping
- Patient education
- Questionnaire responses
- Scheduling (appointments, recalls)
- Service requests/lab orders
- Patient accounts (financial summaries)
- Device tracking (UDI)

**Specialty-specific clinical data thoroughly covered:**
The optometry-specific data is remarkably detailed. The Prescription.csv has fields for sphere, cylinder, axis, prism, base curve, diameter for both eyes, plus separate fields for spectacle lens type/design/material and contact lens products/fitting parameters. The refraction files (7 different types — autorefraction, contact lens Rx, cycloplegic, manifest, retinoscopy, spectacle Rx, wavefront) capture the full range of optometric examination data. The RxOrder.csv alone has 120+ fields covering frame measurements, lens personalization, trace data, and shipping details. This is exactly the kind of specialty-specific clinical data that distinguishes a genuine (b)(10) export from a repackaged (g)(10) FHIR API.

**Potentially missing or unclear:**
- **Secure messages / patient portal communications** — no dedicated CSV for patient-practice messaging, though PatientNote.csv might capture some of this
- **Telehealth visit data** — no telehealth-specific fields visible, though the product offers telehealth capabilities
- **Clinical quality measure (CQM) data** — no dedicated export file, though CQM data could be derived from clinical observations
- **Referral management** — no dedicated referral CSV, though ServiceRequest.csv and provider references may cover referrals

These gaps are minor. The export covers the vast majority of the designated record set for this product.

### Export Format & Standards

- **Format:** CSV files in a ZIP archive, with supplementary images and XML files
- **Standard:** Vendor-proprietary CSV format, not FHIR or C-CDA. This is entirely appropriate for a (b)(10) export — the format is designed to capture everything the product stores, which a standardized clinical data format like FHIR US Core could not do for this specialty product
- **Field naming:** Uses descriptive field names (e.g., "SphereValueL", "BillingProviderNpi"). Many clinical fields use FHIR-aligned naming conventions (e.g., "AllergyIntolerance", "MedicationRequest", "Condition") suggesting familiarity with FHIR resource types even though the export itself is CSV
- **Code systems:** Clinical codes reference their code systems (CodeSystem, AltCodeSystem fields), supporting ICD-9, ICD-10, LOINC, and other standard terminologies
- **Relationships:** Cross-references use identifiers (e.g., Patient chart number, EncounterID, ClaimID, InvoiceID, PolicyID, PrescriptionID) that link records across CSV files. This is sufficient for reconstructing the patient record, though there's no formal schema document describing the relationships
- **Data reconstruction:** A third party could reconstruct a reasonably complete patient record from these CSV files. The identifier-based cross-referencing (Patient chart number appears in nearly every file) and the consistent pattern of foreign key fields makes the relational structure inferrable

### Documentation Quality

- **Readability:** The data dictionary is well-structured — each CSV file gets a clean two-column table with field names and descriptions
- **Field-level definitions:** Every field in every CSV has at least a brief description. The descriptions are minimal (e.g., "Created date", "Patient chart number") but adequate for understanding what each column contains
- **What's missing from the documentation:**
  - No data types specified (string vs. number vs. date format)
  - No date/datetime format specification (ISO 8601? MM/DD/YYYY?)
  - No value set documentation for coded fields (e.g., what are the valid values for "Status", "Classification", "Category"?)
  - No cardinality information (which fields are required vs. optional)
  - No documentation of relationships between CSV files (e.g., how ClaimLine.ClaimID relates to Claim.ClaimID)
  - No sample data or example export files
  - No schema files (JSON Schema, XSD, etc.)
  - No change history or versioning
- **Developer usability:** A developer could understand the structure and field meanings from this documentation, but would need to examine actual export files to understand data types, date formats, coded value sets, and edge cases. The documentation is significantly better than many vendors but stops short of being a complete integration specification
- **Maintenance:** The PDF was created February 20, 2024, and the ScreenSteps page was last updated April 9, 2024. This suggests active maintenance

### Structure & Completeness

- **Granularity:** Field-level — every column in every CSV is documented with at least a name and description
- **76 CSV files** covering an impressive breadth of data domains
- **Coded fields:** The dictionary notes which fields are codes and which are descriptions (e.g., Code/CodeDisplay/CodeSystem pattern), but does not enumerate the valid values
- **Relationships:** Implied through shared identifiers (Patient chart number, EncounterID, etc.) but not formally documented with an ERD or relationship schema
- **Audit trail fields:** Every CSV includes CreatedDate/CreatedBy/ModifiedDate/ModifiedBy fields, providing change tracking metadata in the export itself

### Overall Assessment

VisionWeb/Uprise has done **genuine (b)(10) work**. This is not a repackaged FHIR API or a clinical summary export — it's a comprehensive database-level export of patient data across all domains the product stores. The 76 CSV files cover clinical data, optometry-specific exam data (with extraordinary detail in refraction and prescription files), billing/claims (with CMS-1500 box-level granularity), insurance benefits/coverage, optical dispensing orders, and administrative data.

The CSV-in-ZIP format is well-suited for this product. Trying to express contact lens fitting parameters, keratometry readings, spectacle lens trace data, and CMS-1500 claim fields in FHIR would lose information or require extensive custom profiling. The vendor chose a format that can faithfully represent everything their product stores.

The documentation quality is solid but not exceptional — field names and brief descriptions for everything, but no data types, value sets, or formal relationship documentation. A developer could work with this export but would need to supplement the documentation with actual data inspection.

This is one of the more thorough (b)(10) implementations encountered, particularly impressive for a specialty (optometry) EHR that stores highly domain-specific clinical data that doesn't map to standard clinical data models.

## Access Summary
- Final URL (after redirects): https://help.youruprise.com/m/72283/l/1745699-data-export
- Status: found
- Required browser: no (PDF downloads directly via curl)
- Navigation complexity: direct_link (single page with one PDF download)
- Anti-bot issues: Cloudflare present but no blocking; standard User-Agent header sufficient

## Obstacles & Dead Ends
None. The URL worked as registered, the page loaded cleanly, and the PDF downloaded without issues. The documentation is publicly accessible without authentication.
