# About This Project

## What is this?

This dashboard presents an independent analysis of how well certified Electronic
Health Record (EHR) systems comply with the
[§170.315(b)(10) "Electronic Health Information export"](https://www.healthit.gov/test-method/electronic-health-information-export)
requirement — the regulation that requires certified health IT to let patients
export **all** of their electronic health information (EHI), not just a clinical
summary.

## What is EHI?

**Electronic Health Information (EHI)** is defined in federal regulation at
[45 CFR 171.102](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-D/part-171/subpart-A/section-171.102)
as electronic protected health information (ePHI) to the extent it would be
included in a
[HIPAA Designated Record Set](https://www.hhs.gov/hipaa/for-professionals/faq/2042/what-personal-health-information-do-individuals/index.html).

The **Designated Record Set** (defined at
[45 CFR 164.501](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.501))
is the group of records that a healthcare provider uses to make decisions about
a patient. It includes:

- **Medical records** — diagnoses, medications, lab results, clinical notes,
  vitals, allergies, immunizations, procedures, care plans, imaging reports,
  and any specialty-specific clinical data the system stores
- **Billing records** — claims, charges, payments, insurance information,
  and payment adjudication records
- **Enrollment and case management records** — anything used in managing a
  patient's care or coverage

Crucially, the Designated Record Set is **broader than a clinical summary**.
Under HIPAA, patients have a
[right of access](https://www.hhs.gov/hipaa/for-professionals/privacy/guidance/access/index.html)
to their full Designated Record Set — not just the subset of data that fits
into standardized exchange formats like C-CDA or FHIR US Core. The ONC's
(b)(10) regulation extends this principle to certified health IT: systems must
be able to export EHI in a computable electronic format.

### What EHI includes (and what it doesn't)

**Included**: All clinical data (across all specialties the system supports),
billing and payment records, patient-provider communications (portal messages,
secure messaging), documents and images in the patient record, insurance and
coverage information, referrals, and any custom or specialty-specific data used
in patient care decisions.

**Not included**: Audit logs, system configuration, quality metrics and
aggregates, provider credentialing records, staff scheduling, workflow queues,
and template definitions. These are operational data, not part of the patient's
record. Psychotherapy notes and litigation compilations are also explicitly
excluded from EHI by statute.

The practical test: *if there's a problem with this data, could it affect a
patient's treatment or the amount they owe?* If yes, it's EHI.

## The regulatory backstory

The [21st Century Cures Act](https://www.congress.gov/bill/114th-congress/house-bill/34/text/pl)
(2016) established that electronic health information should be accessible,
exchangeable, and usable "without special effort" by authorized users, and made
it illegal for health IT developers to engage in
[information blocking](https://www.healthit.gov/topic/information-blocking) —
practices that interfere with, prevent, or materially discourage access to EHI.

ONC's [Cures Act Final Rule](https://www.healthit.gov/regulations/cures-act-final-rule/)
(2020) translated this into a concrete certification requirement:
[§170.315(b)(10)](https://www.healthit.gov/test-method/electronic-health-information-export).
Every certified health IT module must be able to export **all** of the EHI it
manages — not just the data elements in
[USCDI](https://www.healthit.gov/isa/united-states-core-data-interoperability-uscdi)
or the data tied to other certification criteria, but everything the system
stores about patients. And the scope extends beyond the certified module itself:
if a certified module lives inside a larger product, the export must cover EHI
across the whole product, not just the certified slice.

Hundreds of vendors have now certified to (b)(10). But because the regulation
deliberately does not prescribe a standard format — the whole point is to
capture data that *doesn't* fit neatly into existing standards — approaches
vary enormously. Some vendors export their full native database. Others hand
back a C-CDA clinical summary and call it done. The quality, completeness,
and usefulness of these exports differ wildly across the industry.

This project aims to make that variation visible.

## Scope: which products are included?

ONC's [CHPL](https://chpl.healthit.gov/) certifies individual product
*listings* — a specific version of a specific product from a specific
developer. But many listings are just version bumps of the same underlying
system, sharing the same EHI export documentation. For this analysis we group
listings by developer and product name into **product families**: one family
per distinct product line, regardless of how many versions are certified. A
single vendor may have multiple families if it sells separate product lines
(e.g., an ambulatory EHR and an inpatient EHR).

The current analysis focuses on product families certified for both:

- **Computerized Provider Order Entry (CPOE)** —
  [§170.315(a)(1)-(a)(3)](https://www.healthit.gov/test-method/computerized-provider-order-entry-cpoe-medications):
  the ability for providers to enter medication, laboratory, and diagnostic
  imaging orders electronically
- **Standardized FHIR API** —
  [§170.315(g)(10)](https://www.healthit.gov/test-method/standardized-api-patient-and-population-services):
  a patient-facing API using the HL7 FHIR standard

Requiring both criteria selects for **fairly complete EHR systems** — products
that handle clinical ordering and expose modern APIs — rather than
single-purpose modules (e.g., a standalone lab system or a billing-only tool).
This yields approximately **217 product families** (303 certified listings)
out of the roughly **600 product families** (700 listings) certified for
(b)(10) on the
[ONC Certified Health IT Product List (CHPL)](https://chpl.healthit.gov/).
These 217 families cover the EHR systems most patients actually interact with.

Future phases will expand to products certified for CPOE without FHIR (~99
additional families) and remaining certified products (~170 families).

## Methodology

For each product family, the analysis proceeds in three automated phases:

### 1. Collection

An AI agent visits the vendor's
[CHPL-registered EHI export documentation URL](https://chpl.healthit.gov/),
researches the product (what it does, what data it stores, what clinical
specialties it serves), and downloads all available export documentation —
PDFs, HTML pages, data dictionaries, sample files, JSON schemas, screenshots.

### 2. Analysis

A second AI agent reads everything collected and produces a deep,
evidence-backed assessment covering:

- **Export mechanics** — What format? How is it accessed? Single-patient or bulk?
- **Content inventory** — Every entity, table, and field catalogued
- **Coverage assessment** — Which data domains are present vs. missing, evaluated
  against what the product is known to store
- **Documentation quality** — Field descriptions, sample data, machine-readable
  schemas, relationship documentation

When structured data dictionaries exist (HTML tables, PDFs with field listings,
JSON schemas), the agent writes custom parser scripts to extract a complete
machine-readable inventory of every field.

### 3. Summary

A third pass extracts structured scores and classifications into a consistent
JSON format for dashboard display, including the letter grade, export fidelity
classification, and patient messaging coverage.

## What the grades mean

Each product receives a holistic quality score (0–10) mapped to a letter grade,
reflecting a weighted assessment of:

- **Coverage** (~40%) — What fraction of the product's data domains appear in the export, including the full Designated Record Set?
- **Documentation quality** (~25%) — Are fields described? Are there schemas and sample data?
- **Data structure quality** (~20%) — Native data model vs. lossy summary format?
- **Usability** (~15%) — Could a developer build an import from the docs alone?

## Key classifications

**Export fidelity** indicates whether the export shows the vendor's real data
model or launders it through a standardized clinical summary:

- **Native** — Export uses the product's own data structures
- **Summary with supplements** — Core clinical data via C-CDA/FHIR, with
  native-format supplements covering domains the summary can't represent
- **Summary only** — Entirely a clinical summary repackaged as "all EHI"

**Patient messaging** indicates whether patient-provider communications (portal
messages, secure messaging) that the product manages are included in the export.

## Limitations

- **Documentation ≠ implementation.** This project evaluates what vendors
  *document* about their exports, not what the exports actually contain.
  A vendor could document a comprehensive export but implement it poorly,
  or vice versa.
- **AI-generated analysis.** All assessments are produced by AI agents. They
  include verification steps and cross-checks, but may contain errors —
  miscounted fields, missed PDF sections, or incorrect classifications.
- **Point-in-time snapshot.** Vendors update their documentation. Results
  reflect what was available when each vendor was last collected.
- **Phase 1 only.** Currently covers ~217 of ~486 certified product families.

## Source code & data

This is an open-source project. The full dataset — raw documentation, analyses,
parsed inventories, and all source code — is available at
[github.com/jmandel/ehi-export-analysis](https://github.com/jmandel/ehi-export-analysis).

---

## About the author

[Josh Mandel, MD](https://www.linkedin.com/in/joshuamandel/) is a physician
and software engineer. He is Chief Architect for Microsoft Healthcare and
Chief Architect for [SMART Health IT](https://smarthealthit.org), where he
leads the development of
[SMART on FHIR](https://smarthealthit.org/smart-on-fhir/) and
[SMART Health Cards and Links](https://build.fhir.org/ig/HL7/smart-health-cards-and-links/). He is the original creator
of [CDS Hooks](https://cds-hooks.org/). He
holds an S.B. in CS and EE from MIT and an M.D. from Tufts, and is a lecturer
at Harvard Medical School's Department of Biomedical Informatics. He is an
active contributor to [HL7 FHIR](https://hl7.org/fhir/) and the
[Argonaut Project](https://www.fhir.org/argonaut/).
*This bio was drafted by AI and may contain inaccuracies.*
