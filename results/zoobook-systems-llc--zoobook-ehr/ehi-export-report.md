# Zoobook Systems LLC — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://app.zoobooksystems.com/EHIexportDocumentation
- CHPL IDs: 9268
- Product: Zoobook EHR 2.0
- Developer: Zoobook Systems LLC

## Navigation Journal

The registered URL returns the documentation directly as a PDF download with no navigation required:

```bash
curl -sI -L "https://app.zoobooksystems.com/EHIexportDocumentation" \
  -H 'User-Agent: Mozilla/5.0'
# Returns: HTTP/2 200, Content-Type: application/pdf, Content-Length: 389047
```

Downloaded:
```bash
curl -sL "https://app.zoobooksystems.com/EHIexportDocumentation" \
  -H 'User-Agent: Mozilla/5.0' \
  -o downloads/EHIexportDocumentation.pdf
```

Verified: `file` confirms it is a 5-page PDF document (version 1.7), created 2023-11-28 in Microsoft Word 2016. Author field is "ACER" (likely the computer name).

Also checked the vendor's disclosures page at `https://zoobooksystems.com/disclosures/` — it references the (b)(10) criterion and includes real-world testing metrics for EHI export (target 98% error-free exports, ≤2 minute completion time, role-based access controls) but does not link to any additional downloadable export documentation or data dictionary. The disclosures page has a separate `/api-documentation/` link for the (g)(10) FHIR API, which is a different system from the EHI export.

## What Was Found

The documentation is a 5-page PDF titled "§170.315(b)(10) Electronic Health Information Export Documentation." It is a user guide with annotated screenshots that walks through the export process. It does **not** contain a data dictionary, schema definition, or export format specification.

### Export Process (as documented)

1. **Settings > EHI Export**: The user navigates to the Settings menu and selects the "EHI Export" item.

2. **Filter parameters**: The export interface has three filter fields:
   - **Date Range**: Filters records by creation or modification date
   - **Clients**: Select which clients' data to export
   - **Modules**: Select which system modules to include in the export

3. **Generate**: Clicking "Generate" creates an export record that can be retrieved either via a **Download Button** or a **Public URL** (for sharing with authorized recipients).

4. **Export record listing columns**: Client ID, Full Name, Module Name, URL (public download link), Start Date, End Date, Created By, Expiration Date, and a Download Button.

### Business Rules & Module Selection

The document shows an "EHI Export Business Rules" section where administrators can configure which modules are included/excluded from the export. A screenshot shows a module picker with **172 modules** selected. The visible module names include:
- Client Notes To File (unchecked — excluded)
- PHI Disclosure Log
- CPST Note
- Counseling Monthly Individual Progress Report
- Comprehensive Psychosocial Evaluation
- Pre-Admission Documents

This is significant: the system has a per-module export selection mechanism with 172 modules available, and administrators can selectively exclude modules from the export. The documentation does not enumerate all 172 modules or describe what data each contains.

### Access Control

The final section shows Module Management settings where administrators can control which user roles have access to the EHI Export function. The screenshot shows roles including: Administrative Staff, Administrator, Assistant Clinical Director, Billers, Clerical, Client, Counselor, Director, Driver, Hr Staff, Intake, Intern/Trainee, Manager, Medical Staff, Provisional User, Receptionist, Sample Collector, Super Administrator, Supervisor, Support.

## Export Coverage Assessment

### Data Domain Coverage

The documentation reveals that Zoobook's EHI export operates at the **module level** — users can select from 172 internal system modules to include in the export. This is architecturally promising for (b)(10) compliance, as it suggests the export can cover the full breadth of the system's data rather than just a clinical subset. However, the documentation provides **zero detail about what data is actually in each module or what the export format looks like**.

Based on the product research, Zoobook EHR stores data across many domains:

**Potentially covered** (if the right modules are selected):
- Clinical documentation (progress notes, assessments, treatment plans) — likely among the 172 modules given visible names like "CPST Note", "Counseling Monthly Individual Progress Report", "Comprehensive Psychosocial Evaluation"
- Patient demographics and intake data — "Pre-Admission Documents" visible
- PHI disclosures — "PHI Disclosure Log" visible

**Unknown — not visible or described**:
- Medication data and e-prescribing records
- Lab orders and results
- Scheduling and attendance data
- Billing and claims data
- Referral tracking
- Bed management data
- HR/staff data and payroll
- Communication records (secure messages, faxes, telehealth)
- Quality measure data
- Audit logs
- State reporting data (NJSAMS)
- Decision support intervention data

These domains may well be among the 172 modules, but there is no way to tell from the documentation. The 172-module figure is encouraging — it suggests granularity — but without a module listing or data dictionary, a recipient of the export would have no idea what they're getting.

**Critical gap**: The documentation does not describe the export **format** at all. Is it CSV? JSON? PDF? A zip of files? Database dump? The column definitions describe the export record *listing* (the UI table showing completed exports), not the exported data itself. A user reading this documentation would know how to click buttons to generate an export but would have no idea what the output looks like, how to parse it, or what fields it contains.

### Export Format & Standards

**Unknown.** The documentation does not specify:
- What file format the export produces
- How the data is structured within the export
- Whether relationships between entities are preserved
- Whether coded values include their value sets
- Whether the export is a single file or a collection of files

The mention of "Public URL" and "Download Button" for each export record suggests the output is a single downloadable file per export, but the format is not stated. The disclosures page mentions "validation of format, structure, and completeness" for exported files but does not name the format.

This is a fundamental gap. Without format documentation, a third party cannot programmatically import or interpret the exported data.

### Documentation Quality

**Poor.** The documentation is:
- A 5-page user guide showing how to click through the export UI
- Contains annotated screenshots of the application interface
- Describes filter parameters and UI columns at a surface level
- Does **not** include a data dictionary, field definitions, data types, or format specification
- Does **not** include sample data or example exports
- Does **not** describe the structure of the exported file(s)
- Could not be used by a developer to implement an import

The documentation reads as a compliance checkbox — "we have an EHI export and here are screenshots of it" — rather than technical documentation that would allow a recipient to understand, parse, or use the exported data.

### Structure & Completeness

- **Module-level granularity only**: The documentation identifies that 172 modules exist but does not list them or describe their contents
- **No field-level documentation**: No table names, field names, data types, or descriptions of what's in the export
- **No value sets or coded fields documented**
- **No relationship documentation**: No description of how entities relate across modules
- **No versioning or change history**
- **No sample data or worked examples**

### Overall Assessment

Zoobook appears to have built a functional EHI export mechanism — the ability to export by date range, client, and module with 172 modules available is architecturally sound for (b)(10) compliance. The module-based approach could genuinely cover "all electronic health information" if all relevant modules are included. However, the documentation fails to describe what the export produces. A recipient would receive a file (of unknown format) containing data (of unknown structure) from selected modules (of unknown content). The documentation is a UI walkthrough, not a technical specification. For a behavioral health EHR storing sensitive mental health, addiction treatment, and medication-assisted treatment data, the lack of a data dictionary or format specification is a significant deficiency.

## Access Summary
- Final URL (after redirects): https://app.zoobooksystems.com/EHIexportDocumentation
- Status: found
- Required browser: no
- Navigation complexity: direct_link (PDF served directly at registered URL)
- Anti-bot issues: none

## Obstacles & Dead Ends

None. The URL worked on the first try and returned a PDF directly. No redirects, no JavaScript, no authentication required. The simplicity of access is not the issue — the issue is the thinness of what's documented.
