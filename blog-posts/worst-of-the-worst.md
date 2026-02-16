# Five Ways EHR Vendors Fail at EHI Export Documentation

Under the [21st Century Cures Act](https://www.congress.gov/bill/114th-congress/house-bill/34/text/pl), certified health IT must be able to export **all** of a patient's electronic health information — not just a clinical summary, but everything the system stores electronically from the [Designated Record Set](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.501): billing, insurance, specialty clinical data, and anything else used to make decisions about their care. The export must be in a computable, machine-readable format — ONC has [clarified](https://www.healthit.gov/wp-content/uploads/2023/02/b10_EHI_Export_Factsheet_FINAL.pdf) that converting structured data to unstructured PDF doesn't count. And vendors must document exactly what gets exported and how, under [§170.315(b)(10)](https://www.healthit.gov/test-method/electronic-health-information-export).

Hundreds of EHR products have now certified to this requirement. But certification doesn't guarantee quality. I built an [automated analysis system](https://jmandel-bot.github.io/ehi-export-analysis/#about) that retrieves every vendor's official (b)(10) documentation from the ONC [Certified Health IT Product List (CHPL)](https://chpl.healthit.gov/), downloads whatever they've published, and scores it on coverage, documentation quality, data structure, and usability.

Of the 129 product families analyzed so far, **39 received an F** — indicating that the documentation is either missing, too sparse to evaluate, or describes an export limited to standard summary formats that fall short of the full EHI requirement. Here are five that illustrate distinct failure modes.

---

## 1. Link rot

**Dexter Solutions — eZDocs v5.5**
CHPL [#11432](https://chpl.healthit.gov/#/listing/11432) · [Registered EHI documentation URL](https://dexter-solutions.com/certification)

Dexter Solutions' CHPL-registered documentation URL redirects to their marketing homepage. The certification page that once existed has been deleted — the vendor rebuilt their Wix site and simply dropped it.

Wayback Machine archives confirm the page previously existed, but even the archived version listed the older §170.315(b)(6) "Data Export" criterion — not the Cures Act (b)(10) EHI Export requirement. No EHI export documentation is available from any public source.

**What this means for patients:** If you request your records from an eZDocs-powered practice, there is no publicly available documentation describing what you'll receive, in what format, or whether it includes your full record. The vendor certified to a federal requirement and then removed the evidence.

## 2. 62 words and a link to the C-CDA spec

**DOX EMR — DOX EMR v5.2**
CHPL [#10806](https://chpl.healthit.gov/#/listing/10806) · [Registered EHI documentation URL](https://www.doxemr.com/b10doc)

The entire (b)(10) documentation page contains 62 words:

> DOX EMR authorized users can generate the Electronic Health Information Export (EHI) for a single patient and also the patient population using CCDA xml format that comply with USCDI v1 requirements standards. The Implementation guide for the CCDA xml standard file description can be accessed from below link.

The "below link" points to the [generic HL7 C-CDA specification](https://www.hl7.org/implement/standards/product_brief.cfm?product_id=492) — a standard that DOX EMR did not author and that says nothing about what DOX EMR specifically exports.

There is no data dictionary. No schema. No sample data. No field mapping. No export instructions. I checked all 21 pages on the site, the Wayback Machine, and web search — this is all that exists.

DOX EMR [markets itself](https://www.doxemr.com/) as a podiatry-focused EHR with specialty-specific clinical workflows. C-CDA is a general-purpose clinical summary standard with no templates for podiatry-specific data. By declaring the export is "C-CDA XML" with no further detail and providing no sample files, the documentation raises an obvious question: how does specialty clinical content that has no C-CDA representation make it into the export? Without sample data, there's no way to tell.

**What this means for patients:** The export format is C-CDA — the same format used for standard health information exchange. Any data that doesn't fit C-CDA's predefined sections would need custom handling that the documentation doesn't describe, and the lack of sample files makes it impossible to verify from the outside.

## 3. A working export with no documentation

**Office Practicum — Office Practicum**
CHPL [#11049](https://chpl.healthit.gov/#/listing/11049) · [Registered EHI documentation URL](https://www.officepracticum.com/op/population-health/onc-certification#onccert)

Office Practicum is a pediatric EHR that, according to its [2025 Real World Testing results](https://www.officepracticum.com/op/population-health/onc-certification#onccert), has processed 2,861 single-patient exports and 20 bulk exports. The export mechanism is genuinely promising: a pre-built SQL query against the product's database, outputting CSV files — which means the export could potentially include the *full* native data model.

But the documentation is approximately 100 words, a significant portion of which is a generic textbook definition of the CSV file format:

> A comma-separated values (CSV) file is a delimited text file that uses a comma to separate values. Each line of the file is a data record…

What tables are exported? What columns? What data types? What clinical domains are covered? The documentation doesn't say. A recipient of an Office Practicum EHI export would receive CSV files with no way to know what they contain.

**What this means for patients:** Your data may actually *be* in the export — the SQL-to-CSV mechanism suggests it could be comprehensive. But nobody can verify that, because there's zero documentation of the export contents.

## 4. Five pages of screenshots, zero pages of schema

**Zoobook Systems — Zoobook EHR 2.0**
CHPL [#9268](https://chpl.healthit.gov/#/listing/9268) · [Registered EHI documentation URL](https://app.zoobooksystems.com/EHIexportDocumentation)

Zoobook is a behavioral health EHR — a domain where the Designated Record Set includes sensitive clinical data like psychosocial evaluations, counseling notes, substance use assessments, and psychiatric treatment plans. The export system appears to cover up to 172 modules, with an administrative interface for selecting which modules to include.

The documentation is a 5-page PDF. Every page is annotated screenshots of the export UI: where to click, what filters to set, how to download the result. It explains the *process* of generating an export in detail.

What it never explains is what comes *out*. There is no description of the exported file format. No schema. No field definitions. No list of the 172 modules or what data each contains. A recipient of a Zoobook export would receive files with no publicly available documentation to interpret them.

**What this means for patients:** The export system itself may be reasonably complete — 172 modules suggests broad coverage. But without a data dictionary or format specification, the exported data is effectively opaque. A new provider receiving your records via EHI export would have no way to parse or import them.

## 5. Three sentences in a footnote

**CorrecTek — Spark**
CHPL [#10274](https://chpl.healthit.gov/#/listing/10274) · [Registered EHI documentation URL](https://www.correctek.com/cost-disclosure-and-transparency/)

CorrecTek [describes Spark](https://www.correctek.com/) as a correctional healthcare EHR covering medical, mental health, dental, and nursing workflows. Their own website and eLearning portal reference modules for intake screening, medication administration, and multiple clinical roles — suggesting a broad clinical data footprint.

The entire EHI export documentation is an asterisk footnote at the bottom of the mandatory disclosures page:

> *EHI can be exported in PDF or C-CDA format. Records for a patient are exported to one or more PDF/C-CDA files. The files created by the export are saved to a folder specified by the user.*

Three sentences. I checked all 83 pages on the CorrecTek website, the eLearning portal (which has modules for 10+ user roles), and web search results. No additional EHI export documentation exists anywhere.

C-CDA has no templates for correctional health workflows like intake screenings, behavioral health assessments, or dental charts. And PDF is not a computable format — ONC has explicitly stated that converting structured data to PDF does not satisfy the (b)(10) requirement. The documentation doesn't explain how the product's advertised clinical breadth is represented in either export format.

**What this means for patients:** Based on the vendor's own description of Spark's capabilities, there's a significant gap between the clinical domains the product covers and what PDF or C-CDA can structurally represent — and the documentation doesn't address it.

---

## What these have in common

These five vendors illustrate a spectrum, but they share a common thread: the (b)(10) certification was treated as a checkbox rather than a patient-facing capability. None provide sample export files, which means there's no way to independently verify what the export actually contains. The Cures Act requires that EHI be available "without special effort." For these products, the published documentation doesn't demonstrate that the export delivers on the underlying promise — that patients can get **all** of their data in a usable form.

The [full dashboard](https://jmandel-bot.github.io/ehi-export-analysis/) covers 129 product families so far, with analysis of the remaining ~90 phase-1 targets in progress. The [methodology](https://jmandel-bot.github.io/ehi-export-analysis/#about) and [all source data](https://github.com/jmandel-bot/ehi-export-analysis) are open.

*Analysis by [Josh Mandel, MD](https://www.linkedin.com/in/joshuamandel/). Assessments are AI-assisted and independently verified against source documentation. [Report errors or corrections.](https://github.com/jmandel-bot/ehi-export-analysis/issues/new)*
