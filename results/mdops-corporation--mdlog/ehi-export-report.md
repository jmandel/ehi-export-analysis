# MDOps Corporation — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://pcc-demo.mdops.com/api/viewCCDSchema
- CHPL IDs: 10792
- Product: MDLog v5.0
- Certification date: 2022-01-17

## Navigation Journal

### Step 1: Initial probe of registered URL

```bash
curl -sI -L "https://pcc-demo.mdops.com/api/viewCCDSchema" -H 'User-Agent: Mozilla/5.0'
```

Response: HTTP 200, Content-Type: `application/xml;charset=UTF-8`. The URL directly serves an XML Schema Definition (XSD) file — no navigation required.

### Step 2: Download and examine the schema

```bash
curl -sL "https://pcc-demo.mdops.com/api/viewCCDSchema" -H 'User-Agent: Mozilla/5.0' -o ccd-schema.xml
```

The file is 85,354 bytes. The opening comment states:

> Supported EHI export format(s) : XML

The schema is `POCD_MT000040` — the HL7 Clinical Document Architecture (CDA) R2 schema, which is the standard XML schema underlying the Continuity of Care Document (CCD) and C-CDA formats. The schema includes references to three sub-schemas:

- `https://connect-demo.mdops.com/api/viewDatatypeSchema`
- `https://connect-demo.mdops.com/api/viewVOCSchema`
- `https://connect-demo.mdops.com/api/viewNarrativeBlockSchema`

### Step 3: Download sub-schemas

The referenced URLs on `connect-demo.mdops.com` return 404 errors. However, the same endpoints are available on `pcc-demo.mdops.com`:

```bash
curl -sL "https://pcc-demo.mdops.com/api/viewDatatypeSchema" -H 'User-Agent: Mozilla/5.0' -o datatype-schema.xml   # 65,977 bytes
curl -sL "https://pcc-demo.mdops.com/api/viewVOCSchema" -H 'User-Agent: Mozilla/5.0' -o voc-schema.xml             # 84,535 bytes
curl -sL "https://pcc-demo.mdops.com/api/viewNarrativeBlockSchema" -H 'User-Agent: Mozilla/5.0' -o narrative-block-schema.xml  # 24,950 bytes
```

All four files are valid XML schemas.

### Step 4: Check for additional documentation

Checked the mandatory disclosures page at `https://www.mdops.com/certified/`:
- Lists 170.315(b)(10) "Electronic Health Information Export" as a certified criterion
- No link to separate EHI export documentation, data dictionary, or user guide
- Contains links to Real World Testing plans/results (2022–2025), BAA, privacy policy, and agreement PDFs — none are EHI export documentation

Checked the demo site root (`https://pcc-demo.mdops.com/`): redirects to login page.

Checked `connect-demo.mdops.com/`: serves a Patient Portal SPA (Angular app) requiring authentication.

Probed additional paths on pcc-demo.mdops.com (`/api`, `/api/export`, `/api/ehi`, `/api/fhir`, `/api/metadata`, `/docs`, `/api-docs`, `/swagger`) — all return 404 or redirect to login.

Checked `www.mdops.com/ehi/`, `/interoperability/`, `/export/` — all 404.

No additional EHI export documentation was found beyond the XSD schema files.

## What Was Found

MDOps provides their EHI export documentation as a single API endpoint that serves the CCD (Continuity of Care Document) XML Schema. The schema is the standard HL7 CDA R2 schema (`POCD_MT000040`) with a vendor-added comment indicating that the supported EHI export format is XML.

The schema set consists of four files:
1. **CCD Schema** (`ccd-schema.xml`) — 88 complex types defining the clinical document structure including ClinicalDocument, Patient, Section, Observation, Procedure, SubstanceAdministration, Supply, Encounter, Act, Organizer, etc.
2. **Datatype Schema** (`datatype-schema.xml`) — 62 complex/simple types for HL7 v3 data types (coded values, identifiers, timestamps, addresses, etc.)
3. **Vocabulary Schema** (`voc-schema.xml`) — 183 simple types defining enumerated value sets for coded fields (act codes, role codes, entity types, etc.)
4. **Narrative Block Schema** (`narrative-block-schema.xml`) — Structured types for CDA narrative text (tables, lists, paragraphs, rendered content)

The schema contains 150 complex types, 183 simple types, 880 element definitions, and 657 enumeration values total.

**No vendor-specific data dictionary, export instructions, field mapping documentation, or sample export files were provided.** The entire EHI export documentation consists of the standard HL7 CDA R2 schema without any MDLog-specific customizations, profiles, or documentation about which CDA sections are populated, what data maps to which sections, or how to perform the export.

## Export Coverage Assessment

### Data Domain Coverage

The CCD schema is a general-purpose clinical document format that *could* accommodate many data domains, but MDOps provides no documentation about which CDA sections their export actually populates. Based on the product research, MDLog stores:

**Potentially covered by CCD format (if properly populated):**
- Clinical notes (the core of MDLog — dictated encounter notes, progress notes)
- Patient demographics
- Medications and e-prescribing data
- Lab orders and results
- Care plans
- Implantable device list
- Allergies (if tracked)
- Diagnoses/problem lists

**Likely missing or inadequately represented in a CCD export:**
- **Billing/charge data** — CCD has no standard mechanism for charge capture, claims, or billing records. MDLog includes a billing portal for charge capture at point of care. No documentation addresses how billing data is exported.
- **Clinical quality measure data** — MDLog captures CQM data for reporting. No documentation addresses its inclusion in the export.
- **Chronic Care Management (CCM) encounter data** — CCM includes time-based billing documentation with built-in timers. The CCD format does not natively represent this workflow data.
- **Wound care assessments** — Specialty-specific structured data that may not map cleanly to standard CCD sections.
- **Patient portal messages** — Secure messaging between patients and providers is part of the patient record.
- **Voice dictation metadata** — The raw dictation and speech recognition data underlying the clinical notes.

**Cannot assess without more documentation:**
- Which CCD sections (e.g., Problems, Medications, Results, Procedures, Encounters) the export actually populates
- Whether the export produces a single CCD per patient or per encounter
- Whether external data imported from PointClickCare/MatrixCare integrations is included in the export

### Export Format & Standards

The export uses **XML conforming to the HL7 CDA R2 standard** (specifically the CCD/C-CDA profile family). This is a recognized healthcare interoperability standard — the same format used for transitions of care under 170.315(b)(1).

However, there is a significant concern: **MDOps appears to be reusing their C-CDA/transitions-of-care capability as their EHI export.** The registered URL is literally `viewCCDSchema` — CCD being the clinical summary document. A CCD is designed for care transitions (a clinical summary), not for exporting **all** electronic health information. This is analogous to the (b)(10) vs. (g)(10) confusion described in the task guidance, but with C-CDA instead of FHIR:

- A CCD/C-CDA document covers USCDI-equivalent clinical data domains (problems, medications, allergies, labs, vitals, procedures, etc.)
- It does **not** cover billing, charge capture, specialty assessments, messaging, or operational data that MDLog stores
- The schema provided is the **unmodified standard HL7 CDA R2 schema** — there are no MDLog-specific extensions, profiles, or templates documented

A third party receiving this export would get a standard C-CDA clinical document, which is useful but likely represents only a clinical summary subset of the full designated record set.

### Documentation Quality

**Very poor.** The entire EHI export documentation consists of a bare XML schema file served from an API endpoint, with no:
- Export instructions or user guide
- Data dictionary mapping MDLog fields to CDA elements
- Description of which CDA sections are populated
- Sample export file
- Explanation of how to trigger the export
- Field-level definitions specific to MDLog's data model
- Value set documentation beyond the standard HL7 vocabulary

A developer could not implement an import of this data based solely on this documentation. They would know the XML *could* conform to CDA R2, but would have no idea what data to expect, which sections are present, or what template IDs are used.

### Structure & Completeness

The schema itself is well-structured (it's a widely-used standard), but it provides no vendor-specific information:
- **No field-level documentation** specific to MDLog
- **No value set documentation** beyond standard HL7 enumerations
- **No relationship documentation** between MDLog's data model and CDA elements
- **No versioning or change history** for the export format
- **No cardinality constraints** beyond what CDA R2 defines

The documentation is essentially a compliance checkbox — pointing to a standard schema without any documentation about how MDLog uses it.

## Access Summary
- Final URL (after redirects): https://pcc-demo.mdops.com/api/viewCCDSchema
- Status: found
- Required browser: no
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends

1. **Sub-schema cross-reference broken**: The CCD schema references three sub-schemas on `connect-demo.mdops.com`, but those endpoints return 404. The same schemas are available on `pcc-demo.mdops.com`. This means the schema set is internally inconsistent — the `schemaLocation` attributes point to non-existent URLs.

2. **Demo site requires authentication**: Both `pcc-demo.mdops.com` (root) and `connect-demo.mdops.com` (patient portal) require login, so no sample data or export interface could be examined.

3. **No additional EHI documentation found**: The certified page, main website, and demo site provide no supplementary EHI export documentation beyond the schema endpoint.
