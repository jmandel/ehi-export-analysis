# Comtron Inc. — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://portal.medgenehr.com/Medgenweb/MedgenBackupUtility.pdf
- CHPL IDs: 10986
- Product: Medgen EHR, Version 9
- Certification date: 2022-09-15

## Navigation Journal

The registered URL is a direct PDF download. No navigation was required.

```bash
curl -sI -L "https://portal.medgenehr.com/Medgenweb/MedgenBackupUtility.pdf" \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
```

Response: HTTP/2 200, Content-Type: application/pdf, Content-Length: 2977613. Server is Microsoft-IIS/10.0 with ASP.NET. No redirects.

```bash
curl -sL "https://portal.medgenehr.com/Medgenweb/MedgenBackupUtility.pdf" \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36' \
  -o MedgenBackupUtility.pdf
```

Verified: `file` identifies it as "PDF document, version 1.5, 79 page(s)". Author: Naveen Malla. Created with Microsoft Word 2016 on September 13, 2023.

## What Was Found

The PDF is titled **"Medgen Data Export & Backup Utility Guide v1.0"** (July 2023, 79 pages). It documents a Windows desktop application called "Medgen Backup Utility" (`MedBackup_Utility.exe`) that connects to the Medgen EHR cloud service and exports patient data. The document covers:

### Export Mechanism
The utility is a Windows MSI-installable desktop application. After installation, the user logs in with Medgen EHR credentials, selects a practice/office, and configures backup criteria:
- **All Patients**: exports every patient in the practice
- **By Date/Time Range**: exports patients within a specified date range
- **By Patient ID Code**: exports selected individual patients

The utility supports optional AES encryption of exported files, and can be scheduled for automated backup via Windows Task Scheduler using an `AUTORUN <PRACTICE CODE>` command-line argument.

### Export Format — Two Components

**1. C-CDA XML documents (per patient):** Each patient gets an XML file conforming to C-CDA (Consolidated Clinical Document Architecture). The document extensively describes the C-CDA sections included, with XML template IDs, XPath structure, and USCDI data class mappings for each section:

| C-CDA Section | USCDI Data Class | Key Data Elements |
|---|---|---|
| Allergy Intolerance | Allergies & Intolerance | Drug allergies, reactions |
| CarePlan | CarePlan | Health concerns, interventions, goals |
| CareTeam | Care Team | Member name, identifier, role, location, telecom |
| Problems | Problems | Active/resolved problems, diagnosis dates, resolution dates |
| Medication | Medication | Medications, dose, indication, fill status |
| Immunization | Immunization | Vaccination status, codes |
| Functional Status | Functional Status | Health concerns, functional status, smoking status |
| Cognitive Status | Cognitive Status | Physical, cognitive, intellectual, psychiatric disabilities |
| Result Section Data | Results | Tests, values/results |
| Vital Signs | Vital Signs | BP, heart rate, respiratory rate, temperature, height, weight, pulse ox, O2 concentration |
| Social History | Social History | Name, DOB, birth sex, address, telecom, smoking status |
| Implant or Device | Implant/Device | UDI device data |
| History of Encounter | Encounters | Encounter type, diagnosis, time, location |
| Goals | Goals | Patient goals |
| Procedure | Procedure | Procedures performed |
| Clinical Notes | Clinical Notes | Consultation notes, discharge summaries, procedure notes, progress notes, test reports |

**2. Patient document ZIP files:** Each patient also gets a ZIP file containing scanned/attached documents (lab reports, patient education materials, etc.) with a structured filename pattern: `{docno}_{date}_{idcode}_{firstname}_{lastname}_{dob}_{provider}_{description}.{ext}`

**3. Additional CSV files (pp. 72–77):** The guide documents supplementary CSV exports that go beyond C-CDA. These are described with full column-level data dictionaries:

- **patients.csv** (22 columns): Demographics, address, phone numbers, email, SSN, and primary/secondary insurance details (code, name, policy number)
- **appointments.csv** (12 columns): Appointment date, time, duration, reason, notes, provider, office
- **pharmacy.csv** (7 columns): Patient-pharmacy associations with NCPDPID identifiers
- **comments.csv** (6 columns): Patient comments/alerts with dates and color coding
- **Transactions.csv** (117 columns): Comprehensive billing/financial data including claims, procedure codes with modifiers, charges, payments, deductibles, copays, adjustments, balances (primary/other/patient), up to 12 diagnosis codes, insurance details (primary and secondary with policy/group/dates), action notes, claim status/substatus, provider info, office info, and sales group fields

### Bulk Export Note
The final page states: "For a bulk data export of full patient populations please contact a Medgen support team member: medgensupport@comtronusa.com" — suggesting the utility documented here may handle individual or filtered exports, with population-level bulk export requiring vendor assistance.

## Export Coverage Assessment

### Data Domain Coverage

Comtron's approach is **notably better than average** for a small vendor. Rather than simply pointing to their FHIR API or repackaging a C-CDA export alone, they have created a **hybrid export** that combines C-CDA XML (for standardized clinical data) with supplementary CSV files (for data that doesn't fit neatly into C-CDA).

**Clearly covered domains:**
- **Clinical records**: Problems, medications, allergies, vital signs, immunizations, clinical notes, care plans, care teams, goals, procedures, functional/cognitive status — all via C-CDA
- **Lab/imaging results**: Result Section Data in C-CDA covers lab and imaging observations
- **Encounters**: History of encounters with diagnosis, type, time, location
- **Devices/implants**: UDI device data via C-CDA
- **Patient demographics**: Covered in both C-CDA header and patients.csv (with more detail in CSV including SSN, insurance)
- **Insurance/payer data**: Primary and secondary insurance in patients.csv, plus extensive insurance detail in Transactions.csv
- **Billing/financial data**: Transactions.csv is remarkably comprehensive with 117 columns covering claims, charges, payments, adjustments, diagnosis codes, insurance billing details, and action notes
- **Appointments/scheduling**: appointments.csv covers appointment scheduling data
- **Pharmacy associations**: pharmacy.csv
- **Patient comments/alerts**: comments.csv
- **Patient documents**: Scanned documents exported as ZIP files

**Domains that appear missing or uncovered:**
- **Addiction medicine data**: This is Medgen's signature specialty module — methadone/buprenorphine dispensing records, controlled substance inventory, drug screening panels, dosing records, service plans, incident reports, bio-psychosocial assessments, counselor notes. None of this appears in the export documentation. This is a significant gap given it's a core differentiating feature.
- **OB/GYN specialty data**: Antepartum/postpartum records, pregnancy tracking, EFW calculations, EDD records, ultrasound reports, high-risk care plans, OB questionnaires — none documented in the export.
- **E-prescribing history**: While medications are in C-CDA, the prescription transmission history, controlled substance prescriptions (EPCS), and pharmacy refill requests are not explicitly mentioned.
- **Audit trails**: The vendor website advertises "complete audit trails" but the export documentation doesn't mention audit log export.
- **Internal messaging**: Secure messages between providers, e-fax records — not mentioned.
- **Patient portal data**: Portal access records, patient-provider messages — not mentioned.
- **Document scanning metadata**: While scanned documents are exported as files in ZIPs, the MedScan metadata (scan dates, categories, indexing) is not documented.
- **Referral authorization tracking**: Mentioned as a product feature but absent from export.
- **Quality reporting data**: PQRS/MIPS quality measure data — not mentioned.
- **Public health reporting records**: Immunization registry submissions, syndromic surveillance, cancer case reports — the submissions themselves are not in the export.

### Export Format & Standards

The export uses a **sensible hybrid approach**:

- **C-CDA XML** for standardized clinical data — this is a well-established healthcare interoperability standard. The documentation maps each section to specific C-CDA template IDs and USCDI data classes, showing genuine engagement with the standard rather than superficial compliance.
- **CSV files** for data that doesn't fit C-CDA (billing, scheduling, pharmacy associations, comments). This is pragmatic — CSV is simple, widely parseable, and appropriate for tabular data.
- **Document ZIPs** for attached files (lab reports, patient education, etc.)

The C-CDA portion covers standard USCDI v1 data classes. The CSV portion extends beyond USCDI to include billing, scheduling, and administrative data. A third party could reconstruct a reasonably complete patient clinical and financial record from the combined C-CDA + CSV + documents export, though the absence of specialty module data (addiction medicine, OB/GYN) would leave gaps for practices using those features.

This is **not** a (g)(10) FHIR API repackaged as (b)(10). The Medgen Backup Utility is a distinct, purpose-built export tool with its own documentation, separate from whatever FHIR endpoint serves the (g)(10) requirement.

### Documentation Quality

The documentation is **adequate but unpolished**:

- **Strengths**: Step-by-step installation and configuration instructions with screenshots. CSV data dictionaries have column-level specifications (position, column name, description). C-CDA sections are documented with template IDs and XPath structures. The file naming convention is documented.
- **Weaknesses**: The document mixes generic C-CDA standard education (explaining what C-CDA is, showing XML examples from the standard) with product-specific documentation. Much of the 79 pages is devoted to explaining C-CDA concepts rather than documenting what Medgen specifically exports. The CSV data dictionaries are the most useful product-specific content but only occupy ~6 pages (pp. 72-77). Data types and constraints are not specified for CSV columns. The Transactions.csv "Description" column simply repeats the column name for most fields rather than providing actual descriptions.
- **Missing**: No sample export files. No value set documentation for coded fields. No explanation of how C-CDA and CSV files relate to each other in the export package. No versioning or change history. The "Software Requirements" page (p. 78) lists requirements but the content appears truncated/empty — it says requirements are "needed" but doesn't list them.

A developer could implement a basic import from the C-CDA files (since C-CDA is a well-documented standard), and could parse the CSVs given the column listings. However, they would need to make assumptions about data types, encoding, and edge cases that aren't documented.

### Structure & Completeness

- **C-CDA sections**: Documented at the section and entry level with template IDs. Field-level detail relies on C-CDA standard templates rather than Medgen-specific customizations. No custom extensions or constraints are documented.
- **CSV files**: Column-level documentation with position numbers, column names, and descriptions. Five CSV files are specified. Data types (string, date, numeric) are not explicitly stated though some can be inferred from descriptions (e.g., "MM/DD/YYYY" for dates). No value set documentation for coded fields like insurance codes, claim status, etc.
- **Relationships**: Patient ID (`Id_code`) appears across CSV files, providing the join key. No formal relationship diagram or foreign key documentation.
- **No versioning**: The guide is v1.0 from July 2023 with no change history.

## Access Summary
- Final URL (after redirects): https://portal.medgenehr.com/Medgenweb/MedgenBackupUtility.pdf
- Status: found
- Required browser: no
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends

None. The URL returned the PDF directly with no authentication, redirects, or anti-bot challenges.
