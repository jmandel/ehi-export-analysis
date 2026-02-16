# Veradigm (Veradigm View / Practice Fusion) — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://veradigm.com/legal/onc-reg-compliance/
- CHPL ID: 11697 (15.04.04.2891.View.01.02.1.250909)
- Certification date: 2025-09-09

## Navigation Journal

1. **Initial probe** — `curl -sI -L "https://veradigm.com/legal/onc-reg-compliance/"` returned HTTP 200 with `text/html` content type (250 KB). The page is a static HTML page served from CloudFront/S3.

2. **Page examination** — The compliance page is a large regulatory hub with sections for multiple Veradigm products: Veradigm EHR, Veradigm View, FollowMyHealth, and ePrescribe. It contains compliance certificates, RWT plans/reports, cost disclosures, MFA documentation, and EHI export documentation.

3. **Found Veradigm View EHI Export section** — Under the "EHI Export Documentation" heading, the "Veradigm View" subsection lists six versioned documentation sets:
   - V6 (published January 12, 2026) — **latest, downloaded**
   - V5 (published November 4, 2025)
   - V4 (published September 17, 2025)
   - V3 (published July 7, 2025)
   - V2 (published July 3, 2025)
   - V1 (published April 1, 2025)

4. **Downloaded V6 index page** — `curl -sL "https://veradigm.com/legal/veradigm-view-ehi-export-documentation/v6/index/"` — 249 KB HTML. The index page describes the export format (TSV) and lists all 87 entity types organized into 8 categories, each linking to a dedicated entity documentation page.

5. **Downloaded all 87 entity pages** — Each page at `/legal/veradigm-view-ehi-export-documentation/v6/{entity-slug}/` contains:
   - An `<h2>` with the TSV filename (e.g., `patient-demographics.tsv`)
   - An `<h4>` with an entity description
   - A table with columns: Field Name, Data type, Field Description

   Each page was downloaded via curl with standard browser User-Agent header. All 87 downloaded successfully, each approximately 232–243 KB (mostly boilerplate site chrome).

6. **Built enrichment script** — Created `extract-entities.ts` (Bun TypeScript) to parse all 87 HTML pages and the index page, producing `entities-catalog.json` (full structured catalog) and `coverage-accounting.json` (parse statistics). All 87 entities parsed successfully with 1,194 total fields extracted.

## What Was Found

### Export Format

Veradigm View exports EHI as **TSV (tab-separated values) files** — one file per entity type, 87 entity types total in V6. The index page states:

> "EHI Export functionality allows health systems to do a manual export of health data for a single patient or entire patient population in a practice. The EHI export contains a patient's electronic health information record available in the EHR in a computable, tab-separated value file format."

This is a genuine **(b)(10) export** — not a repackaged FHIR API. The product exports flat files from its database entities, covering data domains well beyond USCDI/US Core. The export is manual (triggered by the practice) and can cover a single patient or entire practice population.

### Data Dictionary Structure

The V6 documentation provides field-level documentation for all 87 TSV entities:

| Category | Entities | Fields | Key Entities |
|---|---|---|---|
| Clinical | 31 | 376 | encounters (20 fields), encounter-events (31), encounter-procedures (18), encounter-observations (12), conditions (6), diagnoses (14), allergies (20), immunizations (31), healthcare-devices (31), goals (11), health-concerns (11), family-history (10+9), care-team (8), advance-directives (5), clinical-worksheets (9+7), risk-scores (5) |
| Demographics | 10 | 143 | patient-demographics (50), appointments (15), contacts (15), communication-settings (12), gender-identity/sexual-orientation (17), ethnicity (7), race (7), occupation-industry (9) |
| Billing & Insurance | 13 | 286 | superbills (70), insurances (65), superbill-insurances (51), guarantor (22), insurance-eligibilities (12), superbill-procedures (14), superbill-diagnoses (8), restrictions (12) |
| Medications & Prescriptions | 11 | 124 | prescriptions (38), medications (17), drug-alert-overrides (12), immunization-vis-editions (8), pharmacies (10), prescription-transactions (10) |
| Labs | 16 | 187 | lab-orders (25), lab-results (19), lab-result-tests-observations (18), lab-order-items (13), lab-result-item-specimen-data (13) |
| Patient Records | 2 | 27 | documents (12), questionnaire (15) |
| Messaging | 3 | 27 | messages (12), message-recipients (6), message-attachments (9) |
| Referrals | 2 | 24 | referrals (13), referral-recipients (11) |

Each field is documented with:
- **Field Name** — the column name in the TSV file
- **Data type** — e.g., Guid, String, Integer, Boolean, Boolean?, Date, DateTime, Decimal
- **Field Description** — plain English description of what the field contains

### Documentation Quality

The documentation is **well-structured and clearly maintained**. It has gone through 6 versions in 10 months (April 2025 to January 2026), suggesting active development. The entity/field descriptions consistently reference "Practice Fusion EHR" (the product's internal/former name), confirming this maps directly to the product's data model.

Field descriptions are generally informative (e.g., "Unique identifier representing a patient", "Represents the secondary address of the guarantor", "The status code reported by the lab (F=final, C=corrected, etc.)") though some are terse (e.g., a few just name the field without additional context).

The documentation is **publicly accessible** with no authentication required, served as static HTML pages with good URL structure.

## Export Coverage Assessment

### Data Domain Coverage

**Well covered (clearly documented in export):**

- **Demographics** — Comprehensive: 50-field patient record including name variants, DOB, SSN, address, phone, email, language, marital status, plus separate entities for race, ethnicity, gender identity, sexual orientation, tribal affiliation, occupation/industry, financial resources
- **Clinical encounters** — Rich model: encounters with assessments, assessment plans, diagnoses, procedures, observations, events, medications, addendums, and documents
- **Diagnoses & conditions** — Both standalone patient diagnoses (14 fields) and encounter-specific diagnoses (6 fields)
- **Medications & prescriptions** — Full lifecycle: current medications, prescriptions (38 fields including route, strength, frequency, refills, DAW, pharmacy), prescription transactions, drug alert overrides, medication history, medication history consent
- **Allergies** — Detailed: 20 fields per allergy plus separate allergy-reactions entity
- **Immunizations** — 31 fields including VIS edition tracking, registry reporting, transmission history
- **Lab orders & results** — Most detailed domain: 16 entities covering orders (with items, diagnoses, answers, specimens, documents), results (with test observations, observation diagnoses, notes, specimen data, documents)
- **Billing** — Substantial: superbills (70 fields), superbill procedures/diagnoses/modifiers/events/insurances, patient insurances (65 fields), insurance eligibilities, guarantor (22 fields), restrictions, financial resources
- **Family history** — Both family member records (10 fields) and family history diagnoses (9 fields)
- **Patient messaging** — Messages (12 fields) with attachments and recipients
- **Referrals** — Referrals (13 fields) with referral recipients (11 fields)
- **Documents** — Patient documents (12 fields) with encounter documents (8 fields)
- **Care plans/goals** — Goals (11 fields), health concerns (11 fields), advance directives (5 fields), care team (8 fields + care team profiles 7 fields)
- **Clinical worksheets** — Summaries (9 fields) and detail (7 fields) — appears to cover custom clinical forms
- **Smoking status** — Dedicated entity (9 fields)
- **Healthcare devices** — 31 fields including UDI, device identifiers, production identifiers
- **Risk scores** — HCC/RAF risk scores (5 fields)
- **Education** — Patient education records (6 fields)
- **Questionnaires** — Patient questionnaire responses (15 fields)
- **Scheduling** — Appointments (15 fields)

**Not explicitly present but may not be applicable:**

- **Telemedicine visit data** — While Veradigm View supports telemedicine, there's no separate telemedicine entity. Virtual visits may be captured under the general encounters model with appropriate encounter type codes.
- **Patient portal activity** — FollowMyHealth is a separate certified product; its data would be in a separate export.
- **Analytics/reporting aggregates** — Not EHI (operational data).
- **Audit logs** — Not EHI per the scope definition.

### (b)(10) vs (g)(10) Assessment

**This is a genuine (b)(10) export, not a repackaged FHIR API.** Key evidence:

1. **Format is TSV, not FHIR** — The export uses flat TSV files mapped to database entities, not FHIR resources. This is a raw data dump approach that naturally covers whatever the product stores.
2. **87 entity types vs ~20 USCDI resources** — The export covers 87 distinct data entities with 1,194 fields, far exceeding the scope of US Core/USCDI.
3. **Billing data included** — Superbills (70 fields), insurance (65 fields), guarantor, eligibility, restrictions — none of which are part of USCDI or US Core.
4. **Operational data included** — Drug alert overrides, prescription transactions, immunization transmission history, lab order item answers — granular operational data beyond clinical summaries.
5. **Separate FHIR API exists** — The product is separately certified for (g)(10) FHIR API access. The EHI export is clearly a different mechanism.
6. **Dedicated documentation site** — Six versioned releases with entity-level documentation, not a repurposed FHIR API portal.

### Export Format & Standards

- **Format**: TSV (tab-separated values) — a well-understood flat file format
- **Standard**: Not a recognized healthcare standard (not FHIR, C-CDA, or HL7v2). This is a proprietary vendor format, but it's an appropriate choice for a bulk data dump of the entire database.
- **Relationships**: Entities use GUIDs as foreign keys (e.g., `PatientPracticeGuid` links most entities to a patient, `EncounterGuid` links encounter sub-entities). Relationship semantics are implicit from field names rather than formally documented in a schema file.
- **Completeness for reconstruction**: A third party could reasonably reconstruct a patient record from these TSV files by joining on GUID keys. The 87 entity types cover the full data model. However, there are no formal relationship diagrams or foreign key documentation — you'd need to infer joins from field names.

### Documentation Quality

**Strengths:**
- Clean, navigable HTML documentation with consistent structure
- Field-level documentation for all 1,194 fields across 87 entities
- Clear categorization into 8 functional domains
- Six published versions showing active maintenance
- Publicly accessible, no authentication required
- Entity descriptions reference "Practice Fusion EHR" confirming direct mapping to product data model

**Weaknesses:**
- No sample export files or example data
- No formal schema files (no JSON Schema, XSD, or DDL)
- No explicit relationship/foreign key documentation — relationships must be inferred from matching GUID field names
- No documentation of value sets or coded field enumerations (e.g., what values does `EncounterStatus` accept?)
- Some field descriptions are minimal (just restating the field name)
- No export instructions or user guide linked from the documentation pages
- Data types are high-level (String, Guid, Integer, Boolean, Date, DateTime, Decimal) with no length constraints or precision specifications

### Structure & Completeness

- **Granularity**: Field-level with names, types, and descriptions — a solid data dictionary
- **Value sets**: Not documented; coded fields lack enumeration of valid values
- **Relationships**: Implicitly documented through shared GUID field names; no formal ERD
- **Versioning**: Six versions (V1–V6) published between April 2025 and January 2026; changelog not provided but versioned URLs enable comparison
- **Overall**: This is a **good-faith, substantive (b)(10) implementation** that exports the full breadth of the product's data model. The documentation quality is above average for the EHR industry — it provides field-level documentation for all entities in a navigable format, and covers data well beyond USCDI. The main gaps are in supporting artifacts (sample data, formal schemas, relationship documentation, value set enumerations) rather than in the data coverage itself.

## Access Summary
- Final URL: https://veradigm.com/legal/onc-reg-compliance/ (no redirects)
- V6 documentation base: https://veradigm.com/legal/veradigm-view-ehi-export-documentation/v6/index/
- Status: found
- Required browser: no (standard curl with User-Agent header)
- Navigation complexity: one_click (from compliance hub, click into "EHI Export Documentation V6")
- Anti-bot issues: none

## Obstacles & Dead Ends

None. The documentation was straightforward to find and download. All pages loaded successfully with curl. The HTML structure was consistent across all 87 entity pages, enabling reliable automated extraction.
