# eMedPractice LLC — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://emedpractice.com/electronic-health-information-export/
- CHPL IDs: 10787
- Product: eMedicalPractice v2.0
- Certification date: 2022-01-12

## Navigation Journal

### Step 1: Initial probe of registered URL

```bash
curl -sI -L "https://emedpractice.com/electronic-health-information-export/" \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
```

Result: HTTP 200 OK, Content-Type: text/html; charset=UTF-8. WordPress site (Elementor page builder). The response headers included a `Link` header pointing to the WP JSON API endpoint: `https://emedpractice.com/wp-json/wp/v2/pages/17436`.

### Step 2: Fetch the page and extract content

```bash
curl -sL "https://emedpractice.com/electronic-health-information-export/" \
  -H 'User-Agent: Mozilla/5.0' -o ehi-export-page.html
```

Also fetched the cleaner WP JSON API version:

```bash
curl -sL "https://emedpractice.com/wp-json/wp/v2/pages/17436" \
  -H 'User-Agent: Mozilla/5.0' -o ehi-export-page-api.json
```

The JSON API response contains the full rendered HTML content without the surrounding WordPress theme chrome, making it much easier to parse.

### Step 3: Identified documentation links

The main EHI export page contained one internal documentation link:

- **Data dictionary**: `https://emedpractice.com/electronic-health-information-data-dictionary-tables` — linked from the text "Patients Details Data CSV fields definition"
- **External standard**: `https://www.hl7.org/implement/standards/` — reference to C-CDA specification (not downloaded per instructions)
- **Demo scheduling**: `https://go.emedpractice.com/` — marketing, not relevant

No PDF, ZIP, CSV, JSON, or other downloadable files were linked from either page.

### Step 4: Fetched the data dictionary page

```bash
curl -sL "https://emedpractice.com/electronic-health-information-data-dictionary-tables/" \
  -H 'User-Agent: Mozilla/5.0' -o ehi-data-dictionary-tables.html

curl -sL "https://emedpractice.com/wp-json/wp/v2/pages?slug=electronic-health-information-data-dictionary-tables" \
  -H 'User-Agent: Mozilla/5.0' -o ehi-data-dictionary-tables-api.json
```

### Step 5: Checked the mandatory disclosures / certification page

```bash
curl -sL "https://emedpractice.com/wp-json/wp/v2/pages?slug=ehr-certification-and-costs" \
  -H 'User-Agent: Mozilla/5.0'
```

Extracted all links from the page content. The only EHI-related link was back to the main EHI export page. No additional documentation resources were found.

### Step 6: Browser screenshots

Navigated to both pages in Chrome and took full-page screenshots to capture the rendered layout, including the table schemas.

### Step 7: Notable finding — commented-out Section 4

The main EHI export page HTML contains a commented-out section (HTML `<!-- -->` comment) that was previously visible:

> **4. Documents (Scanned Documents like PDF, JPG, PNG File Formats)**
>
> This includes signed progress notes, available lab results, radiology reports, and any other scanned or uploaded document in the patient's record.
>
> **Organizational Structure**: All these documents are sorted and indexed within the respective patient chart number folders. If there are specific categories or types for these documents (e.g., Lab Reports, Radiology, Scanned Receipts, etc.), they will reside in their respective category subfolder within the primary patient folder.

This section describes document export capability that was apparently part of the EHI export at some point but was hidden from the live page. The numbering jumps from Section 2 to the Notes section, skipping 3 and 4 entirely in the visible content.

## What Was Found

The EHI export documentation consists of two WordPress pages built with Elementor:

### Main EHI Export Page

The page describes a two-component export:

**1. Clinical Data in CDA Format (C-CDA):**
- Each individual patient encounter is represented as a CDA document
- A consolidated CDA file aggregates all encounters for a patient
- CDA files are organized in a directory structure by patient chart number
- Claims to include "all data elements defined in USCDI v3, in addition to other EHI the system stores"
- Format is XML following the C-CDA specification

**2. Patient Details Data (CSV):**
- Comma-separated file with demographics, insurance details, and appointments
- Documented in a linked data dictionary page with table schemas

**[Commented out] 4. Documents:**
- Scanned documents (PDF, JPG, PNG) including signed progress notes, lab results, radiology reports
- Organized by patient chart number with category subfolders

Additionally, the page notes that within the application's Reports section, clients can export appointments, patient demographics, and insurance details in CSV format.

### Data Dictionary Page

The data dictionary page (created December 2025, updated December 2025) provides column-level schemas for three tables:

**Patients Table Schema** (19 columns): ChartNo (int, PK), FirstName, MiddleName, LastName, Gender, DateOfBirth, Address1, Address2, City, State, Zip, Phone, Fax, Email, ReferredPhysician (int, FK), status, MaritalStatus, Race, Ethnicity.

**Insurance Table Schema** (29 columns): ChartNo (int, FK), plus primary and secondary insurance information — InsuranceName, InsuredPolicyNo, PatientRel, InsuredLastName, InsuredFirstName, InsuredGroupNo, Copay (float), InsuredDOB, address fields (InsAddL1/L2/City/State/Zip/Phone), and mirror fields for secondary insurance (InsuranceName2, InsuredPolicyNo2, etc.).

**Appointments Table Schema** (13 columns): ChartNo (int), FirstName, LastName, DOB, Email, Phone, Reason, AppointmentDate, AppointmentTime, FacilityName (int), SchedulerName (int), AppointmentType (int), AppointmentStatus (int).

Each column specifies: Column Name, Data Type, Default value, and Not Null constraint.

## Export Coverage Assessment

### Data Domain Coverage

Based on the product research, eMedicalPractice stores a comprehensive set of clinical, billing, scheduling, prescribing, lab, telehealth, and communication data. Here is how the documented export maps against those domains:

**Clearly covered (via C-CDA):**
- Demographics (also in CSV)
- Diagnoses / problem lists
- Medications / prescriptions
- Allergies
- Lab results / diagnostic reports
- Vital signs
- Immunizations
- Clinical notes (encounter documentation)
- Care plans / goals / referrals (if captured in C-CDA sections)

The page claims the C-CDA export includes "all data elements defined in USCDI v3, in addition to other EHI the system stores." This is a strong claim, but C-CDA has inherent limitations for representing all data types.

**Partially covered:**
- Insurance information — documented in the CSV data dictionary (primary and secondary insurance)
- Appointments — documented in the CSV data dictionary
- Patient demographics — documented in both CSV and C-CDA

**Notably absent or unclear:**
- **Billing data** — The product has integrated billing, RCM, claims creation/submission, clearinghouse, EOB auto-posting, patient statements, payment processing. None of this is mentioned in the export documentation. The CSV data dictionary only covers demographics, insurance, and appointments — not charges, claims, payments, or financial transactions.
- **E-prescribing data** — Prescription history, pharmacy communications, EPCS records. While some medication data would appear in C-CDA, detailed prescribing workflows (refill requests, pharmacy responses, EPCS audit trails) would not.
- **Scanned documents and attachments** — The commented-out Section 4 described this capability, but it's currently hidden from the live documentation. It's unclear whether the functionality still exists and just isn't documented, or whether it was removed.
- **Lab orders** (as distinct from results) — The product has bidirectional lab integration; order data may not be fully captured in C-CDA.
- **Clinical decision support alerts/history** — Not mentioned.
- **Patient portal data** — Messages, requests, patient-submitted documents.
- **Telehealth session data** — Virtual visit records, session metadata.
- **Communication records** — Secure Direct messages, faxes, email communications.
- **Quality/MIPS reporting data** — Quality measure submissions, though these are arguably not patient-level clinical data.
- **Prior authorization records** — Part of the billing workflow.
- **Custom/specialty clinical data** — The product markets to 9+ specialties and offers customizable templates. Specialty-specific clinical data (dermatology assessments, behavioral health screenings, etc.) may or may not fit within C-CDA constraints.

### Export Format & Standards

The export uses a dual-format approach:

1. **C-CDA (XML)** — A recognized HL7 standard for clinical document exchange. Appropriate for clinical summaries but has well-known limitations:
   - C-CDA is fundamentally a clinical document standard, not a data export format
   - It handles standard clinical data well (problems, meds, allergies, labs, vitals, immunizations)
   - It does not naturally represent billing data, claims, financial transactions, or scheduling
   - Custom/specialty data must be shoehorned into generic sections
   - The claim of including "all data elements defined in USCDI v3, in addition to other EHI" is notable but hard to verify without seeing actual export files

2. **CSV** — For demographics, insurance, and appointments. This is a straightforward tabular format, but it only covers 3 tables totaling 61 columns. For a product with integrated EHR, billing, scheduling, prescriptions, labs, and more, this is a very small data dictionary.

**Could a third party reconstruct the patient record from this export?** Partially. The C-CDA would provide a clinical summary, and the CSV would add demographic/insurance/appointment details. But billing records, detailed prescribing history, documents/images, portal communications, and specialty-specific data would be missing or significantly truncated.

### Documentation Quality

**Readability**: The documentation is clean, well-formatted, and easy to navigate. The WordPress/Elementor pages render nicely and are organized with clear headings.

**Data dictionary**: Present but minimal. Three tables with column name, data type, default, and nullability. No field-level descriptions, no value set definitions (e.g., what values can `status`, `MaritalStatus`, `Race`, `Ethnicity`, `AppointmentType`, `AppointmentStatus` take?). Integer columns like `FacilityName`, `SchedulerName`, `AppointmentType`, and `AppointmentStatus` appear to be foreign keys or coded values, but no reference tables or code lists are provided.

**No sample data**: No example export files, sample C-CDA documents, or sample CSV files are provided.

**No export instructions**: The documentation describes the export format but does not explain how a user initiates an export. There's a mention that CSV exports are available in the Reports section, but no step-by-step user guide.

**Developer implementability**: A developer could not build a reliable import from this documentation alone. The C-CDA portion relies on the standard specification, but without seeing actual output files or knowing which C-CDA sections/templates are used, there's significant ambiguity. The CSV portion lacks value set definitions for coded fields.

### Structure & Completeness

- **Granularity**: Table names, column names, data types, nullability constraints. No descriptions, no cardinality, no relationships documented explicitly (ChartNo is clearly a join key, but this isn't stated).
- **Coded fields**: Not documented. Multiple integer fields (FacilityName, SchedulerName, AppointmentType, AppointmentStatus) and string fields (status, MaritalStatus, Race, Ethnicity, Gender) appear to be coded values with no value sets provided.
- **Relationships**: The ChartNo field appears in all three tables and is presumably the patient identifier / foreign key, but relationships are not formally documented.
- **Versioning**: No version numbers or change history. The data dictionary page was created December 5, 2025 and last modified December 6, 2025. The main export page was created September 19, 2023 and last modified December 5, 2025.
- **Data type error**: The Insurance table has `InsuredDOB` typed as "datet" (apparent typo for "date").

### Overall Assessment

eMedPractice has made a partial effort at documenting their EHI export. They correctly identify it as a 170.315(b)(10) requirement and describe a dual C-CDA + CSV approach that goes beyond simply pointing to their FHIR API. The C-CDA component is appropriate for clinical data, and the CSV data dictionary for demographics/insurance/appointments shows an attempt to export structured non-clinical data.

However, there are significant gaps:

1. **Billing data is entirely absent** from the export documentation, despite the product having integrated billing, claims, RCM, clearinghouse, and payment processing. This is a major gap — billing records are squarely within the designated record set.

2. **The data dictionary is thin** — only 3 tables covering demographics, insurance, and appointments. A comprehensive ambulatory EHR would have dozens of entity types for encounters, orders, results, notes, prescriptions, documents, and more.

3. **The commented-out document export section** raises questions about whether capability was removed or just hidden from documentation.

4. **No sample data or detailed export instructions** make it difficult to verify the completeness claims.

5. **The C-CDA "includes all EHI" claim** is aspirational but hard to substantiate. C-CDA is not designed to carry billing data, scheduling details, or many other non-clinical data types that fall within the EHI scope.

The documentation reads more like a compliance statement than a technical specification. It signals awareness of the requirement but doesn't provide the depth needed for a third party to fully understand or validate the export's completeness.

## Access Summary
- Final URL (after redirects): https://emedpractice.com/electronic-health-information-export/
- Status: found
- Required browser: no (content accessible via curl and WP JSON API)
- Navigation complexity: one_click (main page links to data dictionary)
- Anti-bot issues: none

## Obstacles & Dead Ends

- No downloadable files (PDF, ZIP, CSV, etc.) were found on either page — all documentation is inline HTML
- The WordPress JSON API was accessible and provided cleaner content than parsing the full HTML pages
- No login walls, anti-bot measures, or Cloudflare challenges were encountered
- The commented-out Section 4 about documents was only discoverable by examining the HTML source
