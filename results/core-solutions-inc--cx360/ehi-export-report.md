# Core Solutions Inc — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://www.coresolutionsinc.com/Electronic-Health-Information-Export-Doc
- CHPL IDs: 9168
- Product: Cx360 V7
- Certification date: 2017-12-26 (b)(10) criterion added later

## Navigation Journal

1. **Initial probe** — HTTP HEAD with curl:
   ```bash
   curl -sI -L "https://www.coresolutionsinc.com/Electronic-Health-Information-Export-Doc" \
     -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
   ```
   Response: HTTP 301 redirect to `https://567863.fs1.hubspotusercontent-na1.net/hubfs/567863/Electronic-Health-Information-Export-Doc.pdf`. The redirect target returns HTTP 200 with `Content-Type: application/pdf`, `Content-Length: 2454569`.

2. **Download the PDF**:
   ```bash
   curl -sL "https://567863.fs1.hubspotusercontent-na1.net/hubfs/567863/Electronic-Health-Information-Export-Doc.pdf" \
     -H 'User-Agent: Mozilla/5.0' \
     -o downloads/Electronic-Health-Information-Export-Doc.pdf
   ```
   Verified: `file` reports "PDF document, version 1.7, 12 page(s)".

3. **PDF metadata** — `pdfinfo` shows: Title "Microsoft Word - 170.315(b)(10)Electronic Health Information export Documentation", Author "bbala1", created 2023-12-06. Produced via "Microsoft: Print To PDF". 12 pages, letter size, unencrypted, no attachments (`pdfdetach -list` returns 0), no embedded URLs (`pdfinfo -url` empty).

4. **Text extraction** — `pdftotext` extracted all text. Multi-column table layouts produce garbled output (columns merge, lines wrap mid-word). All 12 pages rendered at 150 DPI via `pdftoppm` for visual verification.

5. **Checked vendor site for additional documentation**:
   - Mandatory disclosures page (`/mandatory-disclosures-2022`): Only link found was a compliance certificate PDF. No additional EHI export documentation, data dictionary, or API docs.
   - Homepage: No links to EHI export, interoperability portal, FHIR API docs, or data dictionary.
   - No additional EHI-specific documentation exists beyond the single PDF.

## What Was Found

The entire EHI export documentation is a single 12-page PDF. It documents the following:

### Export Mechanism
Cx360 V7 implements the (b)(10) EHI export as a **CCD (Continuity of Care Document) export** using the C-CDA standard (§170.205(a)(4) HL7 Implementation Guide for CDA Release 2, Consolidated CDA Templates, DSTU R2.1, August 2015). Two modes are available:

1. **Single Patient Export** — via the "Patient Summary Report Screen." Users select a patient, choose which C-CDA sections to include (15 selectable checkboxes), and click Print/Download. Output is a CCD XML document plus a human-readable Adobe PDF rendering.
2. **Bulk Patient Export** — via the "CCDA Management" utility. Users select multiple patients (by provider or appointment date) and click "Generate CCD." Output is CCD + PDF for each selected patient.
3. **On-demand download** — Images and clinical notes can be downloaded separately as PDF.

### Data Dictionary
Pages 7–12 contain a tabular data dictionary listing 24 CCD sections with 82 data elements. For each element, the documentation provides:
- Data element name
- XPATH/Entry path (C-CDA template ID and entry reference)
- Code System OID
- Code System Name

The 15 selectable C-CDA sections in the UI are: Patient, Encounter, Allergies, Medications, Problems, Diagnosis, Referral, Procedures, Instructions, Functional And Cognitive, Immunizations, Vital Signs, Lab Results, Care Plan, Social History.

The detailed data dictionary covers 24 CDA sections: Patient Demographics/Information, Provider information, Date and Location of visit, Chief Complaint and Reason for visit, Encounters, Immunizations, Instructions, Treatment Plan, Social History, Problems, Medications, Medication Allergies, Laboratory Tests, Laboratory Information, Laboratory values/results, Vitals, Goal, Procedures, Care team members, Reason for Referral, Medical Equipment, Mental Status, Functional Status, and Health Concern.

### Screenshots
The PDF includes 6 screenshots from the Cx360 application:
- Patient home screen showing client demographics (page 3)
- Patient Summary Report screen with Print/Download buttons and C-CDA section checkboxes (page 4)
- Patient Chart Clinical Summary output showing rendered CCD header (page 5)
- Utilities screen showing CCDA Management tool for bulk export (page 6)
- Patient list table for bulk selection (page 6)

## Export Coverage Assessment

### Data Domain Coverage

This is the most critical finding: **the export is fundamentally a C-CDA clinical summary, not a comprehensive EHI export.** The C-CDA/CCD format covers the standard USCDI clinical data classes, but Cx360 is a behavioral health and IDD EHR that stores far more than what C-CDA can represent.

**Domains clearly covered** (via standard C-CDA sections):
- Patient demographics (name, sex, DOB, race, ethnicity, language)
- Provider information
- Encounters (CPT codes, diagnoses, dates)
- Problems/diagnoses (SNOMED, ICD-10)
- Medications (RxNorm, NDC)
- Medication allergies (RxNorm, SNOMED)
- Immunizations (CVX, CPT-4)
- Laboratory tests and results (LOINC)
- Vital signs (LOINC)
- Procedures (CPT-4, SNOMED, HCPCS)
- Social history
- Goals
- Care team members
- Referral reasons
- Medical equipment / implanted devices
- Mental status assessments
- Functional status assessments
- Health concerns
- Instructions / follow-up
- Treatment plan (planned observations)

**Domains clearly absent** — critical data that Cx360 stores but which has no representation in the C-CDA export:

- **Billing records** — claims, charges, payments, accounts receivable, authorization tracking. The product has a full revenue cycle management module. No billing data appears in the export.
- **Behavioral health assessments** — the product's core value proposition includes comprehensive behavioral health assessments (depression, PTSD, anxiety, substance use screening tools, psychiatric history). The C-CDA Mental Status section provides only a generic SNOMED-coded assessment slot, not the structured multi-question instruments the product stores.
- **Treatment plans (detailed)** — Cx360 stores detailed behavioral health treatment plans with trackable goals, interventions, and progress tracking. The C-CDA Treatment Plan section only covers planned observations and dates — not the rich treatment plan structure.
- **Progress notes / clinical notes** — the product stores detailed clinical progress notes linked to treatment goals. The PDF mentions "ability to download Images / Clinical notes on demand" as a separate capability, but this is an on-demand download, not part of the structured CCD export. The relationship between this and the CCD is unclear.
- **IDD-specific data** — person-centered life plans, valued outcomes tracking, DSP task assignments, behavioral tracking data. This is entirely absent from the C-CDA export.
- **Substance use disorder (SUD) data** — addiction history, SUD-specific assessments, MAT tracking. Not present beyond what might fit into generic Social History or Problems sections.
- **Custom forms and configurable assessments** — the product supports configurable clinical forms. No mechanism for exporting form data that doesn't map to standard C-CDA sections.
- **Secure messages** — client-provider communications.
- **Documents and attachments** — clinical documents, external records. Images/notes are available "on demand" as separate PDFs, not as part of the structured export.
- **Electronic visit verification (EVV)** — GPS-stamped visit records from Cx360 GO and DSP Assist.
- **Scheduling/appointment data** — mentioned in the bulk export selection criteria but not exported as structured data.
- **Child and family services data** — foster care records, family engagement records.
- **Insurance/enrollment information** — visible in the UI screenshot (Insurance widget on patient home) but not in the C-CDA export sections.

### Export Format & Standards

The export uses **C-CDA (CCD)** — specifically the HL7 Implementation Guide for CDA Release 2, Consolidated CDA Templates (DSTU R2.1, August 2015). This is a well-defined, widely implemented standard.

However, using C-CDA as the sole (b)(10) export format is problematic for a behavioral health EHR:

- C-CDA was designed to support clinical summary exchange (transitions of care, referrals), not comprehensive record export. It has fixed sections for standard clinical data classes.
- Behavioral health data — which is the entire reason this product exists — has no natural home in C-CDA. Detailed psychiatric assessments, evidence-based screening instruments, IDD life plans, SUD treatment protocols, and custom clinical forms cannot be faithfully represented in C-CDA sections.
- This is effectively the same export that would satisfy the (b)(1) Transitions of Care criterion — a clinical summary, not a complete record dump.
- A third party receiving this export could reconstruct a basic clinical summary of the patient but would lose the vast majority of the behavioral health-specific clinical data that makes Cx360 records valuable.

### Documentation Quality

The documentation is **minimal but clear** for what it covers:

- **Positives**: The data dictionary tables are well-structured, with XPATH paths, OIDs, and code system names for each data element. The screenshots show the actual UI. The standard is clearly referenced.
- **Negatives**: At 12 pages (of which ~5 are screenshots and cover page), this is extremely thin documentation. There are no worked examples, no sample CCD files, no guidance on how to interpret the export, no description of how vendor-specific data maps to C-CDA sections, no documentation of the on-demand clinical notes download, and no error handling or edge case documentation.
- A developer could implement an import of the C-CDA data based on the standard C-CDA IG (which is public), but the vendor-specific documentation adds very little beyond confirming which sections are populated.

### Structure & Completeness

- **Field-level documentation**: Moderate. Each data element has a name, and most have XPATH paths and code system references. However, there are no descriptions, cardinality constraints, or optionality indicators.
- **Value sets**: Code systems are referenced by OID (SNOMED, LOINC, RxNorm, etc.) but no vendor-specific value sets or local code mappings are documented.
- **Relationships**: Not documented beyond the section/element hierarchy.
- **Versioning**: Document is dated 12/2023. No change history.

### Overall Assessment

This is a textbook example of a vendor conflating (b)(10) with (b)(1). The export is a standard C-CDA clinical summary — the same format used for transitions of care. For a general-purpose ambulatory EHR, this might cover most patient data. But for a **behavioral health and IDD-specialized EHR**, the C-CDA format inherently cannot represent the majority of the clinically significant data the product stores.

The missing data isn't obscure — it's the product's core value: behavioral health assessments, treatment plans with goal tracking, IDD life plans, SUD-specific protocols, custom clinical forms, billing records, secure messaging, and mobile documentation. A patient's behavioral health record exported via this mechanism would lose most of its clinical substance.

The documentation quality reflects this mismatch: it's a thin compliance document that describes a standard C-CDA export, not a thoughtful analysis of how to get all of a patient's behavioral health data out of the system.

## Access Summary
- Final URL (after redirects): https://567863.fs1.hubspotusercontent-na1.net/hubfs/567863/Electronic-Health-Information-Export-Doc.pdf
- Status: found
- Required browser: no
- Navigation complexity: direct_link (301 redirect to HubSpot-hosted PDF)
- Anti-bot issues: none

## Obstacles & Dead Ends
- No obstacles encountered. The URL cleanly redirected to a publicly accessible PDF.
- No additional EHI export documentation was found on the vendor's mandatory disclosures page or elsewhere on the site.
- The pdftotext output was garbled for table content due to multi-column layouts; all data was verified from rendered page images.
