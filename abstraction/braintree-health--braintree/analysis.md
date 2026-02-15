# EHI Export Analysis: Braintree Health

**Product**: BRAINTREE (BMW Platform) v10.5.1.1
**Analysis date**: 2026-02-15
**CHPL ID**: 15.02.05.1167.BRNT.01.01.1.211119 (CHPL #10727)

## 1. Product Context

Braintree Health develops the BMW (Braintree Medical Workflow) Platform, an integrated EHR/practice management suite designed primarily for **outpatient procedure centers, ambulatory surgery centers, vascular access centers, and interventional radiology clinics**. The company, headquartered in Corpus Christi, TX, also operates under "NephroPACS," reflecting its origins in nephrology/vascular access imaging.

The product is distinguished from typical ambulatory EHRs by its deep integration of:

- **Medical imaging (BT PACS/RIS)**: DICOM image acquisition, archiving, viewing, and routing; radiology information management
- **Procedure-oriented clinical workflow**: Pre-operative, intra-operative, and post-operative documentation with point-and-click workflows
- **Integrated billing**: CPT codes auto-generated during procedures as nursing staff document procedural steps; same-day billing completion
- **Inventory management (BT Inventory)**: Per-procedure supply consumption tracking, stock levels, purchase orders
- **Scheduling (BT Scheduler)**: Multi-provider, multi-facility appointment scheduling
- **Patient portal and referral portal**: Patient access to records; referring physician access to DICOM images and reports

The product stores clinical data (demographics, encounters, vitals, medications, prescriptions, allergies, problems, labs, notes, imaging), billing data (CPT codes, charges, insurance, claims), procedure-specific documentation, medical images (DICOM), consent forms, and patient attachments. This breadth sets the baseline for assessing export completeness.

Braintree is certified for 49 ONC criteria including (b)(10) EHI export, (g)(10) FHIR API, clinical documentation criteria (a)(1)–(a)(15), patient portal (e)(1)–(e)(3), and public health reporting (f)(1)–(f)(7).

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `certification-page.html` (71 KB) | Full HTML of the ONC certification disclosure page; contains the b(10) section inline (6 bullet points) | **Primary source** — the only b(10) documentation |
| `ehi-export-section-screenshot.png` (245 KB) | Screenshot of the b(10) section on the certification page | Confirms HTML content visually |
| `certification-page-full.png` (938 KB) | Full-page screenshot of the certification disclosure page | Context for page layout |
| `Braintree-FHIR-API-Documentation-1.pdf` (804 KB, 76 pages) | FHIR API documentation for g(10); covers SMART on FHIR, OAuth2, and 15 FHIR resource types | **Not b(10)** — useful for understanding what clinical data the system exposes via FHIR |
| `Braintree-fhir-doc.pdf` (166 KB, 1 page) | FHIR server endpoint URLs (test and production) | Minimal; just 4 URLs |
| `transparency.htm` (10 KB) | Excel-exported HTML frameset for cost disclosures | Not relevant to EHI export |

**Live site verification** (2026-02-15): The certification page at `https://www.braintreehealth.com/braintree-onc-certification-btree/` was confirmed accessible and unchanged from the collected artifact. The b(10) section content is identical. There are **zero** EHI-export-specific downloadable files among the 12 linked documents on the page — all links are for FHIR API docs (2), Real World Testing plans/results (6), administrative documents (2), or cost transparency (1).

## 3. Export Mechanics

- **Format**: Mixed — C-CDA XML (demographics), PDF (clinical and billing reports), HTML (consent forms), DICOM (medical images), original format (attachments)
- **Mechanism**: Not described. No instructions on how to trigger the export (UI button, API call, vendor-assisted, etc.)
- **Single-patient vs bulk**: Not specified. The language references "the patient" (singular), suggesting single-patient export
- **Access constraints**: Not described. No mention of who can perform exports, timelines, or costs
- **Separate from g(10)**: The b(10) export is presented as a distinct section from the FHIR API, using non-FHIR formats. This is appropriate — the vendor does not simply point to their FHIR API for b(10)

## 4. Export Content: What's In It

### What the documentation says

The entire b(10) documentation is **114 words** — an introductory paragraph and 6 bullet points on the certification page. There is:

- **No data dictionary** — zero tables, fields, schemas, or column definitions
- **No sample export files** — no examples of actual export output
- **No user guide** — no instructions on performing the export
- **No schema or machine-readable specification**
- **No enumeration of specific data elements**
- **No description of relationships between exported files**

### Vendor's own content organization

The vendor describes 6 categories of exported data, each with a format but no field-level detail:

| Data Category (vendor's language) | Format | Fields Documented | Types | Descriptions |
|---|---|---|---|---|
| General EHI (images, documents, reports) | HTML/PDF | 0 | No | "human-readable html/pdf format where applicable" |
| Patient demographics | C-CDA XML | 0 | No | No detail beyond "CCDA xml format" |
| Consent forms | HTML | 0 | No | No detail |
| Clinical and billing reports, encounter documentation | PDF | 0 | No | "computable format" — meaning unexplained |
| Patient attachments | Original format | 0 | No | "as uploaded into EMR" |
| Patient images | DICOM | 0 | No | Medical imaging standard |

**Total entities documented: 0.** **Total fields documented: 0.** The vendor provides no field-level documentation whatsoever. The documentation operates entirely at the level of "category → format" with no indication of what specific data elements are included in each category.

### The "computable format" claim

The vendor states that clinical and billing PDFs are "in computable format." This likely refers to tagged/structured PDFs (PDF/A or PDF with embedded structured data), but the claim is not explained. Without sample output, it is impossible to verify whether these PDFs contain machine-parseable structured data or are simply visually formatted documents.

### What the FHIR API (g(10)) covers for comparison

The FHIR API documentation (76 pages) covers 15 FHIR resource types — all standard US Core / USCDI v1:

1. Patient
2. AllergyIntolerance
3. CarePlan
4. CareTeam
5. Condition (Problems / Health Concerns)
6. Device (Implantable)
7. DiagnosticReport / Clinical Notes / DocumentReference
8. Goal
9. Immunization
10. Laboratory Result Observation
11. Medication / MedicationRequest
12. Observation (Smoking Status)
13. Observation (Vital Signs)
14. Procedure
15. Provenance

These are standard clinical data elements. The FHIR API does **not** cover billing, imaging (DICOM), inventory, procedure-specific workflow data, or specialty clinical data — which is expected, as these don't map to FHIR US Core. The b(10) export is the appropriate mechanism for this broader data, but its documentation doesn't enumerate what's included.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes 6 high-level categories with no depth. The broadest category — "clinical and billing report and encounter documentation" — could conceivably cover most patient data, but without enumeration it is impossible to verify.

**Strongest category**: Patient images (DICOM) — this is the correct standard for imaging data, and imaging is central to this product's use case.

**Thinnest categories**: All others. "Patient demographics in CCDA" provides no detail on which C-CDA sections or demographic fields. "Consent forms in HTML" names a format but not what consent data is captured. "Clinical and billing report" is a catch-all with zero specificity.

The absence of any mention of medications, allergies, labs, vitals, immunizations, problem lists, or care plans in the b(10) section is notable — these are core clinical data domains that the product stores and exposes via its FHIR API. They may be subsumed under "clinical and billing report and encounter documentation" PDFs, but this is speculation.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | "Patient demographics exported in CCDA xml format" — no field enumeration | Product stores demographics; C-CDA is a reasonable format but scope unknown |
| Encounters / visits | ⚠️ Partial | "Encounter documentation exported in PDF format" — no detail | Product manages pre-op/intra-op/post-op encounters; export scope unclear |
| Problems / conditions | ❌ Not explicitly covered | Not mentioned in b(10); available via FHIR API | Product stores problem lists; gap unless included in PDF reports |
| Medications / prescriptions | ❌ Not explicitly covered | Not mentioned in b(10); available via FHIR API | Product does e-prescribing; gap unless included in PDF reports |
| Allergies | ❌ Not explicitly covered | Not mentioned in b(10); available via FHIR API | Product stores allergies; gap unless included in PDF reports |
| Immunizations | ❌ Not explicitly covered | Not mentioned in b(10); available via FHIR API | Product stores immunizations (certified for (f)(1)); gap unless in PDF reports |
| Vitals | ❌ Not explicitly covered | Not mentioned in b(10); available via FHIR API | Product captures vitals from monitors; gap unless included in PDF reports |
| Lab results | ❌ Not explicitly covered | Not mentioned in b(10); available via FHIR API | Product handles lab orders/results (CPOE certified); gap unless in PDF reports |
| Imaging / diagnostic reports | ✅ Covered | "Patient images exported into DICOM format"; also "reports in html/pdf" | Appropriate format for this imaging-centric product |
| Procedures | ⚠️ Partial | May be included in "encounter documentation" PDFs | Product's core is procedure documentation; critical if missing |
| Clinical notes / documents | ⚠️ Partial | "Clinical report and encounter documentation in PDF format" | Likely covered but no specifics on what note types |
| Care plans / goals | ❌ Not explicitly covered | Not mentioned in b(10); available via FHIR API | Product certified for CarePlan via FHIR; gap unless in PDF reports |
| Orders / referrals | ❌ Not explicitly covered | Not mentioned | Product supports CPOE and referrals; gap |
| Insurance / coverage | ⚠️ Partial | May be in "billing report" PDF | Product stores insurance info; unclear if exported |
| Claims / billing | ⚠️ Partial | "Billing report" mentioned in PDF export | Product auto-generates CPT codes; unclear what billing detail is in the PDF |
| Payments | ❌ Not explicitly covered | Not mentioned | Product tracks receivables/payment cycles; gap if applicable |
| Consents / directives | ✅ Covered | "Consent forms exported in HTML format" | Explicitly listed |
| Patient communications / portal messages | ❌ Not explicitly covered | Not mentioned | Product has patient portal; gap if messages are stored |
| Specialty-specific (vascular access, interventional radiology) | ❌ Not explicitly covered | Not mentioned | Core specialty of the product (access flow history, vascular data); significant gap if missing |

**Summary**: Only 2 of 18 applicable domains are clearly covered (imaging, consents). 5 domains have partial/ambiguous coverage. 11 domains have no explicit mention in the export documentation. Many of these may be subsumed under the vague "clinical and billing report" PDF category, but without a data dictionary or sample data, this cannot be verified.

## 6. Documentation Quality

The b(10) export documentation is **extremely poor** — among the thinnest possible:

- **114 total words** for the entire b(10) section
- **Zero fields documented** — not a single specific data element is named
- **Zero downloadable artifacts** specific to EHI export (no data dictionary, no schema, no sample data, no user guide)
- **No export process description** — a developer or patient has no instructions on how to actually obtain the export
- **No relationship documentation** — no description of how exported files relate to each other
- **No value sets or code systems** referenced
- **No versioning or change history**

The only semi-technical claim is that PDFs are "in computable format," which is unexplained.

**Could a developer build an import from this documentation?** No. A developer would need to receive an actual export, reverse-engineer its structure, and hope it doesn't change. The documentation provides no basis for building import logic.

**Contrast with g(10) documentation**: The FHIR API documentation is 76 pages with detailed request/response examples, endpoint URLs, and resource schemas. The b(10) documentation is 6 bullet points with no supporting materials. This stark difference (76 pages vs. ~10 lines) suggests the vendor invested in FHIR API compliance but treated b(10) as a checkbox.

## 7. Overall Assessment

### Classification

**Minimal/stub** — Documentation is too thin to assess what the export actually covers. The 6 bullet points describe export formats at a high level but provide zero field-level documentation, no data dictionary, no sample data, no export instructions, and no schema. It is impossible to determine whether the export covers "all electronic health information" or just a fraction of what the product stores.

### Key Findings

1. **The entire b(10) export documentation is 114 words (6 bullet points) with zero downloadable artifacts.** No data dictionary, no sample data, no schema, no export instructions exist. Among the 12 downloadable files on the certification page, zero are related to EHI export. (Source: `certification-page.html`, verified against live site 2026-02-15)

2. **The b(10) export is correctly separated from the FHIR API.** The vendor uses C-CDA, PDF, HTML, and DICOM for b(10) rather than pointing to the FHIR API. This suggests some intent to provide a broader export, but the documentation is too thin to verify. (Source: `certification-page.html`)

3. **Core clinical domains (medications, allergies, labs, vitals, immunizations, problems) are not mentioned in the b(10) documentation** despite being available via the FHIR API and stored by the product. They may be included in "clinical report" PDFs but this is unverifiable. (Source: `certification-page.html`, `Braintree-FHIR-API-Documentation-1.pdf`)

4. **Medical imaging export in DICOM format is a genuine strength** for this imaging-centric product (vascular access, interventional radiology, ambulatory surgery). DICOM is the correct standard. (Source: `certification-page.html`)

5. **PDF as the primary structured data format is a significant portability limitation.** Even if PDFs are "computable" (meaning unclear), PDF is inherently difficult for downstream systems to programmatically ingest and reconstruct as structured data. (Source: `certification-page.html`)

### Summary Stats

```
Classification:  Minimal/stub
Export format:   Mixed (C-CDA XML, PDF, HTML, DICOM, original)
Model type:      Unknown — no data model documented
Entities:        N/A (no data dictionary)
Fields:          N/A (zero fields documented)
Descriptions:    N/A
Sample data:     No
Bulk export:     Unclear
Domains covered: 2 of 18 applicable domains clearly covered; 5 partial/ambiguous
```

### Bottom Line

Braintree Health's b(10) export documentation is a stub — 6 bullet points describing output formats with no data dictionary, no field-level detail, no sample data, and no export instructions. For a product that stores procedure-specific clinical workflows, medical imaging, billing with auto-CPT encoding, and specialty data across vascular access and ambulatory surgery settings, this documentation is wholly inadequate to assess whether the export meets the "all EHI" requirement. The single clear strength is DICOM export for medical images, which is the correct format for this imaging-centric product.
