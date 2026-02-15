# Mendelson Kornblum Orthopedic & Spine Specialists — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://orthoplex.mkoss.com/UserContent/Healthinformationexport.html
- CHPL IDs: 9349
- Product: OrthoplexEMR V1
- Developer: Mendelson Kornblum Orthopedic & Spine Specialists (built by Proactive Technology Management)

## Navigation Journal

1. **Initial probe** — HTTP HEAD request to the registered URL:
   ```bash
   curl -sI -L "https://orthoplex.mkoss.com/UserContent/Healthinformationexport.html" -H 'User-Agent: Mozilla/5.0'
   ```
   Result: HTTP 200, `Content-Type: text/html`, 5200 bytes, served by Microsoft-IIS/10.0. Last-Modified: 2023-09-15. No redirects.

2. **Page download**:
   ```bash
   curl -sL "https://orthoplex.mkoss.com/UserContent/Healthinformationexport.html" -H 'User-Agent: Mozilla/5.0' -o downloads/Healthinformationexport.html
   ```
   The page is a simple, unstyled HTML document (no CSS, no JavaScript, no images) containing all the EHI export documentation on a single page.

3. **Link analysis** — The page contains exactly two outbound links:
   - `http://www.hl7.org/ccdasearch/templates/2.16.840.1.113883.10.20.22.1.2.html` — HL7 C-CDA template reference (external standard; not downloaded per instructions)
   - `https://portal.mendelsonortho.com/` — Patient portal login for patient self-service download (login-gated; noted but not downloaded)

4. **Domain root check**:
   ```bash
   curl -sI "https://orthoplex.mkoss.com/" -H 'User-Agent: Mozilla/5.0'
   ```
   Redirects to `/Account/Login` — this is the OrthoplexEMR application login. The EHI export page is a static HTML file served from the `/UserContent/` directory of the application, publicly accessible without authentication.

5. **Mandatory disclosures page** (`https://proactivemgmt.com/disclosure/`) was checked but contains no additional EHI export documentation — it's the Proactive Technology Management company site with standard ONC disclosure information.

6. **Screenshot** taken of the full page in browser.

## What Was Found

The entire EHI export documentation is a **single static HTML page** (5,200 bytes). There are no linked downloadable files (no PDFs, ZIPs, schemas, CSVs, or sample data). The page has not been updated since September 15, 2023.

### Export Mechanism

The export is **C-CDA document generation**. Two export methods are described:

1. **Single Patient Export** — Provider logs into OrthoplexEMR, searches for a patient, navigates to History → CCDA, and can:
   - Download a ZIP file containing the C-CDA document (with optional encryption)
   - Send via secure email
   - Send via Direct messaging (requires a valid Direct mailbox address)

2. **Patient Population Export** — Provider navigates to Utilities → CCDA, creates a named export job with configurable parameters:
   - **Frequency**: Run Once, Daily, Weekly, Monthly, Yearly
   - **Range**: Optional date start/end boundaries
   - **Type**: All Patients or Single Patient
   - Output is placed on a shared server accessible within the MKO network or via SynergyHealth VPN

3. **Patient Self-Service Download** — Patients log into the portal at `portal.mendelsonortho.com` and access "Patient Summary for Transition of Care" to download their own data.

### Data Dictionary

The page lists 16 C-CDA sections with their field elements:

| Section | Fields |
|---------|--------|
| Demographics | First Name, Last Name, DOB, Sex, Race, Preferred Language, Ethnicity (primary/secondary), Contact Info, Patient ID |
| Document | Document ID, Created Date, Author, Contact Info |
| Encounter | Encounter ID, Encounter Date, Responsible Party, Contact Info |
| Document Meta | Maintained by, Contact Info |
| Medications | Medication, Code, Type, Strength, Dose, Route, Frequency, Date Started, Status |
| Problems | Problem Code, Patient Problem, Status, Date Diagnosed |
| Allergies/Adverse Reactions/Alerts | Allergy Code, Substance, Medication/Agent Allergy, Reaction, Date Entered |
| Vital Signs | Date/Time, Height, Weight, Blood Pressure, Pulse, Temp, Resp, Pulse Ox, O2 % BldC Ox, Inhaled Ox Conc |
| Care Team Information | Name, Position, Email |
| Immunizations | Empty (noted: "Immunizations not provided at clinics") |
| Social History (smoking) | Smoking Code, Smoking Status, from/to |
| Medical Equipment | Description, Date and Time, Status |
| Results (Tests) | Code, Code System, Name, Date, Result, Lab, Provider |
| Procedures | Description, Date and Time, Status |
| Goals | (free form) |
| Health Concerns | (free form) |
| Plan of Treatment | Plan of Treatment, Assessment |
| Reason for Referral | (free form) |

The "Structure of Export" section simply links to the HL7 C-CDA Continuity of Care Document template (2.16.840.1.113883.10.20.22.1.2).

## Export Coverage Assessment

### Data Domain Coverage

This export is a **standard C-CDA patient summary** — it covers the clinical data domains one would expect in a Continuity of Care Document, which aligns closely with USCDI / US Core data classes. Based on the product research, here is the coverage picture:

**Clearly covered:**
- Patient demographics
- Problem lists / diagnoses
- Medications
- Allergies and adverse reactions
- Vital signs
- Encounters (ID, date, responsible party only)
- Care team
- Procedures (description-level only)
- Test/lab results
- Social history (smoking status only)
- Medical equipment / implantable devices
- Goals, health concerns, treatment plans (free-form text)
- Referral reasons (free-form text)

**Explicitly absent (noted by vendor):**
- Immunizations — the page states "Immunizations not provided at clinics," which is plausible for an orthopedic specialty practice

**Likely stored but NOT covered by this export:**
- **Clinical notes and documentation** — A 20+ physician orthopedic practice generates extensive clinical notes (history & physical, operative notes, progress notes, consult notes). None are mentioned in the export. This is a major gap.
- **Imaging orders and results** — MKO operates MRI centers; imaging orders are certified under (a)(4). Not in the export.
- **Surgical/operative records** — An orthopedic surgery practice with ambulatory surgery centers. Operative notes, surgical details, implant records beyond the "Medical Equipment" section are not documented.
- **Billing and claims data** — Whether in OrthoplexEMR or a separate system, billing data is not mentioned.
- **Scheduling data** — Appointment history, no-shows, scheduling patterns.
- **Patient portal messages** — Certified for (e)(1) and (e)(3); patient-submitted health information is not in the export.
- **Direct messaging documents** — Documents received via EMRDirect.
- **Family health history** — Certified for (a)(12) but not listed in the export sections.
- **Clinical quality measure data** — Certified for (c)(1)-(c)(3).
- **Audit logs** — No mention.
- **Physical/occupational therapy records** — SHP includes PT/OT services.
- **Custom forms or specialty-specific data** — Orthopedic assessment tools, pain scales, functional outcome measures.

**Assessment**: This is a **C-CDA patient summary, not a comprehensive EHI export**. It covers approximately the same data as a (g)(10) FHIR US Core API would — the standard clinical summary domains. It does not attempt to export "all electronic health information" as required by (b)(10). The export format (C-CDA CCD) is inherently a summary document format, not a bulk data export format. Critical data domains like clinical notes, imaging, surgical records, and billing are absent.

### Export Format & Standards

- **Format**: C-CDA (Consolidated Clinical Document Architecture), specifically the Continuity of Care Document (CCD) template (2.16.840.1.113883.10.20.22.1.2)
- **Standard**: HL7 C-CDA — a recognized healthcare interoperability standard
- **Delivery**: ZIP file download, secure email, or Direct messaging (single patient); shared server file drop (population export)
- **Appropriateness**: C-CDA is appropriate for clinical summary exchange but is **not appropriate as a comprehensive EHI export format**. It cannot represent billing data, audit logs, imaging data, custom forms, or many other data types that an orthopedic EMR stores. A C-CDA CCD is fundamentally a summary — it's the right format for transitions of care, not for "export everything."

The population export feature with scheduling (daily/weekly/monthly/yearly) is a useful operational feature, but the underlying data scope remains the same C-CDA summary regardless of how many patients are exported.

### Documentation Quality

- **Readability**: The page is simple and readable, though unstyled. The instructions are clear step-by-step guides.
- **Data dictionary**: Present but minimal — lists section names and field names only. No data types, no value sets, no cardinality, no constraints, no coding system details beyond the generic "Code" fields.
- **Examples**: None. No sample C-CDA documents, no sample data.
- **Developer usability**: A developer could not implement an import based solely on this documentation. They would need to rely on the generic C-CDA specification and reverse-engineer any vendor-specific patterns from actual export files.
- **Maintenance**: The page was last modified September 15, 2023. The product was certified in 2018. The documentation appears to be a static compliance artifact.

### Structure & Completeness

- **Granularity**: Section-level with field names only. No data types, no descriptions of what each field contains, no cardinality (required vs. optional), no constraints.
- **Coded fields**: Several sections mention "Code" fields (Medication Code, Problem Code, Allergy Code, Smoking Code, Code System) but do not specify which code systems are used (ICD-10, SNOMED CT, RxNorm, etc.) or provide value sets. The product research notes they use e-IMO (Intelligent Medical Objects) for clinical terminology, but this isn't documented.
- **Relationships**: No documentation of how entities relate to each other beyond what's implicit in C-CDA structure.
- **Versioning**: No version history or change tracking.

### Overall Assessment

This is a **minimal compliance documentation effort** from a custom, single-organization EMR. The export itself is a standard C-CDA patient summary — functionally equivalent to a transitions-of-care document rather than a true (b)(10) "all EHI" export. For an orthopedic surgery practice with imaging centers, ASCs, PT/OT, and pain management, the C-CDA summary format misses large swaths of clinically and operationally important data.

The documentation is honest in what it describes (note the candid "Immunizations: Empty" entry), but the scope of what it exports is narrow. The page links to the generic C-CDA CCD template rather than providing vendor-specific profile documentation or sample files.

Given that OrthoplexEMR is a custom in-house system with no commercial customers and development by a small IT firm, the minimal documentation is not surprising but is still notable. The (b)(10) requirement applies regardless of whether a product is commercial or single-organization.

## Access Summary
- Final URL (after redirects): https://orthoplex.mkoss.com/UserContent/Healthinformationexport.html
- Status: found
- Required browser: no (static HTML, no JavaScript required)
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends
- No obstacles encountered. The page loaded directly via curl with no authentication, no JavaScript, and no anti-bot measures.
- The domain root (`orthoplex.mkoss.com`) requires login — it's the EMR application. Only the `/UserContent/` path is publicly accessible.
- The mandatory disclosures site (`proactivemgmt.com/disclosure/`) was checked but contains no additional EHI export documentation.
- No downloadable files (PDF, ZIP, schema, sample data) exist — the entire documentation is the single HTML page.
