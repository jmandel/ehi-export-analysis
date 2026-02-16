# Health Innovation Technologies, Inc. — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://www.revolutionehr.com/certification-disclosures/
- CHPL IDs: 9923
- Product: RevolutionEHR v7
- Certification date: 2018-12-31

## Navigation Journal

**Step 1: Initial probe**
```bash
curl -sI -L "https://www.revolutionehr.com/certification-disclosures/" -H 'User-Agent: Mozilla/5.0'
```
Result: 301 redirect from trailing-slash URL to `https://www.revolutionehr.com/certification-disclosures` (no trailing slash), then 200 OK. Served via Cloudflare CDN. Content-Type: text/html.

**Step 2: Fetch and examine the page**
```bash
curl -sL "https://www.revolutionehr.com/certification-disclosures" -H 'User-Agent: Mozilla/5.0' -o certification-disclosures.html
```
The page is a static HTML page (~65KB) built with Webflow. It contains the full ONC certification disclosures for RevolutionEHR v7 in a single page without accordions or hidden sections.

**Step 3: Locate b(10) export documentation**

The page contains a clearly labeled section: **"RevolutionEHR b(10) Export Documentation"** which states:

> Single patient export is available within RevolutionEHR in the Admin module under Patient Management.
> Population export is available upon request by contacting customer support.
> Data dictionary is available by [clicking here](https://4915236.fs1.hubspotusercontent-na1.net/hubfs/4915236/openapiServices.json)

**Step 4: Download the data dictionary**
```bash
curl -sL "https://4915236.fs1.hubspotusercontent-na1.net/hubfs/4915236/openapiServices.json" -o openapiServices.json
```
Result: 46,534 bytes, valid JSON. Confirmed OpenAPI 3.0.1 specification titled "RevolutionEHR Patient Export" describing the EHI export JSON format.

**Step 5: Examine FHIR API documentation links**

The page also links to:
- FHIR API Documentation: `https://revolutionehr.dynamicfhir.com/dhit/basepractice/r4/Home/ApiDocumentation`
- FHIR Endpoints: `https://revolutionehr.dynamicfhir.com/fhir/r4/endpoints`

The FHIR API Documentation link returns a server error ("No data for the practice with PracticeID - 0" — an ASP.NET MVC stack trace). This is the g(10) documentation, not the b(10) export documentation, and is broken.

The FHIR Endpoints link returns a FHIR Bundle of Endpoint resources listing service-based FHIR R4 URLs. This is also g(10) infrastructure, not relevant to the b(10) export.

The page notes that "ConnectEHR +BulkFHIR by Dynamic Health IT, Inc" meets the g(7), g(9), g(10) criteria — confirming the FHIR API is a separate system from the b(10) export.

**Step 6: Screenshot**

Full-page screenshot captured via browser for visual reference.

## What Was Found

RevolutionEHR provides a **proprietary JSON export** as its b(10) EHI export mechanism, documented via an **OpenAPI 3.0.1 specification** file. This is a genuine, purpose-built b(10) export — it is clearly distinct from their FHIR/g(10) API.

### Export Format
- **Format**: Custom JSON
- **Endpoint**: `patient/export` (POST)
- **Root schema**: `Patient` — a single JSON object per patient containing all data domains as nested arrays/objects
- **Not FHIR**: Uses vendor-specific field names and structures (e.g., `odSphere`, `osCylinder` for refraction data; `billTo`/`invoiceDate` for billing)

### Data Dictionary (OpenAPI Spec)
The spec defines **35 schemas** with **279 total fields** and **37 inter-schema relationships**. The root `Patient` schema has 17 top-level properties:

| Property | Type | Description |
|----------|------|-------------|
| exportTimestamp | datetime | When the export was generated |
| demographics | Demographics | Patient identity, address, employment |
| healthGoals | HealthGoal[] | Health goals with status tracking |
| healthConcerns | HealthConcern[] | Health concerns with type and status |
| immunizations | Immunization[] | Immunization records with CVX codes |
| implantableDevices | ImplantableDevice[] | UDI-tracked devices |
| allergies | Allergy[] | Allergies with severity and reactions |
| encounters | Encounter[] | Clinical encounters with nested diagnoses, vitals, refractions, tests, services, family/social history, CDS, and orientation/mood |
| medicalOrders | MedicalOrder[] | Lab orders with LOINC codes and results |
| insurances | Insurance[] | Insurance coverage with payer details |
| invoices | Invoice[] | Billing invoices with line items, payments, and claim history |
| diagnoses | Diagnosis[] | Diagnosis history with ICD codes and eye location |
| familyHealthHistories | FamilyHealthHistory[] | Family conditions with SNOMED codes |
| referrals | Referral[] | Referral tracking with response data |
| contacts | Contact[] | Emergency/responsible party contacts |
| statements | Statement[] | Billing statement history |
| familyMembers | FamilyMember[] | Family account members |

### Noteworthy Domain-Specific Content
The schema includes **optometry-specific data** that goes beyond standard USCDI:
- **Refraction** schema: 19 fields covering OD/OS sphere, cylinder, axis, prism (horizontal/vertical with orientation), intermediate add, near add
- **Test/TestValue**: Generic name/value test structure for diagnostic equipment readings
- **Diagnosis** with `eyeLocation` and `qualifier` fields (optometry-specific)
- **OrientationMood**: Mental/functional status assessment within encounters
- **Invoice/InvoiceItem/Claim/Payment**: Full billing chain from services through claims to payments

## Export Coverage Assessment

### Data Domain Coverage

**Clearly covered domains:**
- Demographics (name, DOB, sex, race, ethnicity, language, address, phone, email, employment)
- Allergies (severity, reactions, treatment)
- Diagnoses/Problem list (ICD codes, eye location, encounter dates)
- Encounters (date, type, location, provider, signed status, diagnoses, vitals, refractions, tests, services, CDS, mental status)
- Vital signs (BP, pulse, height, weight)
- Immunizations (CVX codes, administration details, lot info)
- Medical orders / Lab results (LOINC codes, values, units, interpretation)
- Insurance (company, policy, group, payer ID)
- Billing (invoices, line items with CPT codes/modifiers, pricing, payments, claims with submission tracking)
- Patient statements (billing statements with balances)
- Family health history (SNOMED-coded conditions with family relationships)
- Social history (smoking, tobacco, alcohol)
- Health goals and health concerns
- Care plans (linked to diagnoses)
- Referrals (with tracking, response, and report receipt)
- Implantable devices (UDI)
- Patient contacts and family members
- Refraction data (OD/OS sphere, cylinder, axis, prism, add — optometry core data)
- Diagnostic test results (generic name/value pairs from equipment)

**Domains that appear to be missing or unclear:**
- **Optical dispensing data** — Eyeglass/contact lens prescriptions, frame selections, lens orders, contact lens orders, and order fulfillment. The product research identifies this as a major functional area (optical POS, frame inventory, supplier integrations). No schema in the export covers spectacle prescriptions, contact lens parameters, or optical orders.
- **Medications / Prescriptions** — No `Medication` or `Prescription` schema. The product integrates with RXNT for e-prescribing. It's unclear whether medication lists and prescription history are captured in `MedicalOrder` or are entirely in the external RXNT system and thus excluded.
- **Clinical notes / Narrative documentation** — No field for encounter note text, progress notes, or clinical narrative. The encounter schema captures structured data (diagnoses, vitals, tests, services) but no free-text clinical documentation.
- **Patient portal data** — Patient intake forms (RevIntake/IntakeQ), portal messages, survey responses, self-scheduled appointments
- **Documents and attachments** — No schema for scanned documents, uploaded files, or external records incorporated into the chart
- **Ophthalmic images** — The product includes PACS for retinal photos, OCT images, visual fields, corneal topography. No image or document attachment export is documented.
- **E-prescribing details** — Drug interaction checks, allergy checks (via RXNT)
- **Provider communication** — Direct secure messages (via RevDirect)

### Export Format & Standards
The export uses a **vendor-specific JSON format** with an OpenAPI 3.0.1 specification as its data dictionary. This is **not FHIR**, not C-CDA, and not any recognized standard — but it is a reasonable, purpose-built approach for a b(10) export.

The format is structurally simple: a single nested JSON object per patient, with arrays of domain-specific objects. Relationships are implicit (encounters contain nested diagnoses, services, tests) rather than using foreign keys. The format is self-contained and doesn't require external references to interpret.

The JSON structure would be straightforward for a developer to parse. The lack of coded value sets (fields like `severity`, `status`, `smokingStatus` are plain strings without documented enumerations) makes it harder to programmatically interpret the data, but the structure itself is clear.

**Could a third party reconstruct the patient record from this export?** Partially. The clinical encounter data, billing, demographics, and diagnoses are well-represented. However, the absence of clinical notes, optical dispensing data, and images means significant portions of the optometric record would be missing.

### Documentation Quality
- **Readability**: The OpenAPI spec is a machine-readable, self-documenting format. Good choice.
- **Data dictionary clarity**: Field-level definitions are present for all 279 fields, though most descriptions simply restate the field name (e.g., `city` → "City", `address1` → "Address1"). Only a few have genuinely informative descriptions.
- **Data types**: Fully specified — string, integer, number, boolean, with format annotations (date, date-time, double, int32, int64).
- **Required fields**: Documented per schema (e.g., Allergy requires severity and name; Invoice requires billTo, invoiceDate, status, items, payments).
- **Value sets**: Not documented. Coded fields like severity, status, type, smokingStatus are typed as plain strings with no enum constraints.
- **Examples**: None provided. No sample export files.
- **Developer usability**: A developer could build a parser for this format from the spec alone. They would struggle to interpret the semantics of coded values without sample data.
- **Maintenance signals**: The spec is version "1.0" with no change history. The HubSpot hosting URL suggests it's managed as a static upload rather than generated from the system.

### Structure & Completeness
- **Granularity**: Field-level documentation is present for all schemas, with types and descriptions
- **Coded fields**: Not documented with value sets — this is a significant gap for interoperability
- **Relationships**: Expressed via JSON nesting and `$ref` references in the OpenAPI spec; 37 cross-schema relationships are defined
- **Versioning**: Version "1.0" only; no change history

### (b)(10) vs (g)(10) Assessment

This is a **genuine b(10) export** — not a repackaged FHIR API. Evidence:
1. The export uses a proprietary JSON format, completely separate from their FHIR/g(10) API (powered by Dynamic Health IT's ConnectEHR +BulkFHIR)
2. The data dictionary includes billing data (invoices, claims, payments) and optometry-specific data (refractions, eye-specific diagnoses) that would not be in a USCDI/US Core FHIR export
3. The certification disclosures page clearly separates b(10) documentation from the FHIR API links

However, the export still has notable gaps relative to the full designated record set — particularly optical dispensing, clinical notes, medications, and images. The export covers clinical structured data and billing well, but doesn't reach the "everything the product stores about patients" standard that b(10) requires.

## Access Summary
- Final URL (after redirects): https://www.revolutionehr.com/certification-disclosures
- Status: found
- Required browser: no (all content accessible via curl)
- Navigation complexity: direct_link (data dictionary linked directly from the certification page)
- Anti-bot issues: none (Cloudflare CDN but no challenges)

## Obstacles & Dead Ends
- The FHIR API Documentation link (`revolutionehr.dynamicfhir.com/dhit/basepractice/r4/Home/ApiDocumentation`) returns a 500 server error. This is g(10) documentation, not b(10), so it doesn't affect the EHI export collection, but it's a broken link on their certification disclosures page.
- No additional export documentation (user guide, instructions, screenshots of the export UI) was found beyond the brief text on the certification page and the OpenAPI spec.
