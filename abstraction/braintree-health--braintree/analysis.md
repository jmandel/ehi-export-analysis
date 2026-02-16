# EHI Export Analysis: Braintree Health

**Product**: BRAINTREE (BMW Platform) v10.5.1.1  
**Analysis date**: 2026-02-16  
**CHPL ID**: 15.02.05.1167.BRNT.01.01.1.211119 (ID 10727)

## 1. Product Context

Braintree Health (Corpus Christi, TX) develops the BMW (Braintree Medical Workflow) Platform — an integrated EHR suite designed primarily for outpatient procedure centers, ambulatory surgery centers, vascular access centers, and specialty clinics (interventional radiology, pain management, orthopedics). The platform is distinguished by deep integration of **medical imaging (PACS/RIS)**, **inventory management**, and **procedure-oriented clinical workflow** — pre-op, intra-op, and post-op documentation with real-time CPT auto-encoding during procedures.

Key modules relevant to EHI scope:
- **EMR/Clinical**: Demographics, problems, medications, allergies, vitals, labs, clinical notes, procedure documentation, nursing assessments, e-prescribing
- **BT PACS/RIS**: DICOM image management, radiology reports, study tracking
- **Billing**: Integrated billing with auto-CPT encoding, charges, receivables, payment cycles
- **BT Inventory**: Per-procedure supply consumption tracking (operational, not EHI)
- **BT Scheduler**: Appointment scheduling (administrative, not core EHI)
- **Patient Portal**: Patient access, referral portal for physicians
- **Public Health**: Immunization registries, syndromic surveillance, lab reporting, cancer case reporting

The product is certified for 49 ONC criteria including (b)(10) EHI export. This is a small niche vendor — no customer counts or third-party reviews exist publicly.

**Baseline expectation**: A genuine (b)(10) export should cover clinical documentation (pre-op/intra-op/post-op), imaging, medications, allergies, labs, vitals, billing/charges, consent forms, and procedure-specific data. The imaging (DICOM) export is particularly important given this product's core market.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|----------|-------------|-----------------|
| `certification-page.html` (71 KB) | Full ONC certification disclosure page; contains the entire b(10) section as 6 inline bullet points | **Primary source** — this is the only b(10) documentation |
| `ehi-export-section-screenshot.png` (245 KB) | Screenshot of the b(10) section | Confirms HTML extraction is accurate |
| `Braintree-FHIR-API-Documentation-1.pdf` (804 KB, 76 pages) | g(10) FHIR API docs: SMART on FHIR launch, OAuth2, 15 FHIR resource types with sample JSON | **Context only** — shows what the g(10) API covers (standard US Core); b(10) is separate |
| `Braintree-fhir-doc.pdf` (166 KB, 1 page) | FHIR server endpoint URLs (test + production) | Minimal — g(10) infrastructure only |
| `transparency.htm` (10 KB) | Cost disclosure spreadsheet (Excel-exported HTML) | Not relevant to EHI export |
| `certification-page-full.png` (938 KB) | Full-page screenshot of certification page | Confirms page structure |

**No data dictionary, schema, sample export, or user guide exists for the b(10) export.** The entire b(10) documentation is 6 bullet points of inline text on the certification page.

## 3. Export Mechanics

- **Format(s)**: Mixed — CCDA XML (demographics), HTML (consent forms), PDF ("computable format" — clinical and billing reports), DICOM (medical images), original upload format (attachments)
- **Mechanism**: Not described. No documentation on how to trigger the export (UI button, API call, or vendor-assisted).
- **Single-patient vs bulk**: Not specified.
- **Access constraints or fees**: Not documented.
- **Process**: Completely undocumented. No user guide, no workflow description, no screenshots.

The only description of the export mechanism is the format listing. There is no information about who can initiate an export, what parameters are available, how long it takes, or how the output is delivered.

## 4. Export Content: What's In It

### No data dictionary exists

There is **no data dictionary, no schema, no field-level documentation, and no sample data**. The entire b(10) documentation consists of six bullet points describing output formats at the highest possible level:

1. "While certain EHI, such as images, documents, reports are exported in human-readable html/pdf format where applicable."
2. "The patient demographics are exported in CCDA xml format."
3. "The consents form of the patient are exported in HTML format."
4. "The clinical and billing report and encounter documentation of the patient is exported in PDF format. The PDF provided are in computable format."
5. "The patient attachments are exported in the original format as uploaded into EMR."
6. "The patient images are exported into DICOM format."

### Vendor's own content organization

| Entity/Category | Fields | Described | Types | Format | Category (vendor's) |
|---|---|---|---|---|---|
| Patient demographics | N/A | N/A | N/A | CCDA XML | Demographics |
| Consent forms | N/A | N/A | N/A | HTML | Consents |
| Clinical and billing reports / encounter documentation | N/A | N/A | N/A | PDF | Clinical / Billing |
| Patient attachments | N/A | N/A | N/A | Original format | Attachments |
| Patient images | N/A | N/A | N/A | DICOM | Imaging |
| Images, documents, reports (general) | N/A | N/A | N/A | HTML/PDF | Documents / Reports |

**Total documented entities**: 6 high-level categories (no entity/table-level detail)  
**Total documented fields**: 0  
**Fields with descriptions**: 0  

This is not a data dictionary — it is a format listing. No field names, data types, value sets, relationships, or granularity of any kind is provided.

### What the g(10) FHIR API covers (for comparison)

The g(10) API documentation (76-page PDF) covers 15 FHIR resource types, all standard US Core / USCDI v1:

Patient, AllergyIntolerance, CarePlan, CareTeam, Condition (Problems/Health Concerns), Device (Implantable), DiagnosticReport/Clinical Notes/DocumentReference, Observation (Lab Results), Goal, Immunization, Medication/MedicationRequest, Observation (Smoking Status), Procedure, Provenance, Observation (Vital Signs)

Notably, the b(10) export does **not** reference FHIR at all — it uses CCDA, HTML, PDF, and DICOM. This separation from g(10) is appropriate for a procedure-center product, but the b(10) documentation is orders of magnitude less detailed than the g(10) docs.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes 6 broad output categories with no field-level detail:

1. **Demographics** (CCDA XML): Presumably standard C-CDA demographics. No detail on which fields.
2. **Consent forms** (HTML): Patient consent documents. No detail on structure.
3. **Clinical and billing reports / encounter documentation** (PDF): This is the broadest and vaguest category. "Clinical and billing report and encounter documentation" could conceivably include most patient data, but the PDF format limits machine-readability. The vendor claims PDFs are in "computable format" — this term is unexplained and ambiguous (could mean tagged PDF, PDF/A, or PDFs with embedded structured data).
4. **Attachments** (original format): Patient-uploaded documents preserved as-is.
5. **Medical images** (DICOM): Appropriate for this imaging-heavy product. DICOM is the correct standard.
6. **General documents/reports** (HTML/PDF): Catch-all for other human-readable content.

The **strongest signal** is the DICOM image export — this is domain-appropriate and uses the correct standard. The **weakest signal** is the "clinical and billing report" category, which is too vague to assess.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | "Patient demographics exported in CCDA xml format" — no field detail | Product stores demographics; CCDA likely covers basics but no detail on completeness |
| Encounters / visits | ⚠️ Partial | "Encounter documentation" mentioned as part of PDF export | Product has rich pre-op/intra-op/post-op workflows; unclear if all are captured |
| Problems / conditions | ❌ Not covered | Not mentioned in b(10) documentation | Product stores problem lists (certified for (a)(6)); gap — only available via g(10) FHIR |
| Medications / prescriptions | ❌ Not covered | Not mentioned in b(10) documentation | Product has e-prescribing (certified for (a)(1)); gap |
| Allergies | ❌ Not covered | Not mentioned in b(10) documentation | Product stores allergies (certified for (a)(8)); gap |
| Immunizations | ❌ Not covered | Not mentioned in b(10) documentation | Product stores immunizations (certified for (f)(1)); gap |
| Vitals | ❌ Not covered | Not mentioned in b(10) documentation | Product captures vitals from monitors; gap |
| Lab results | ❌ Not covered | Not mentioned in b(10) documentation | Product handles lab orders/results (CPOE certified); gap |
| Imaging / diagnostic reports | ✅ Covered | "Patient images are exported into DICOM format" | Appropriate for this imaging-centric product |
| Procedures | ⚠️ Partial | May be included in "encounter documentation" PDFs | Product's core workflow is procedure documentation; unclear coverage |
| Clinical notes / documents | ⚠️ Partial | "Clinical report... exported in PDF format" + "documents... in html/pdf" | Likely includes notes but no detail on scope |
| Care plans / goals | ❌ Not covered | Not mentioned in b(10) documentation | Product certified for care plans; gap |
| Orders / referrals | ❌ Not covered | Not mentioned in b(10) documentation | Product has CPOE; gap |
| Insurance / coverage | ❌ Not covered | Not mentioned in b(10) documentation | Product stores insurance info; gap |
| Claims / billing | ⚠️ Partial | "Billing report" mentioned as part of PDF export | Product has integrated billing with auto-CPT; "billing report" is vague — could be a summary PDF rather than structured charge data |
| Payments | ❌ Not covered | Not mentioned in b(10) documentation | Product tracks receivables/payment cycles; gap |
| Consents / directives | ✅ Covered | "Consents form... exported in HTML format" | Explicitly mentioned |
| Patient communications / portal | ❌ Not covered | Not mentioned | Unclear if product stores portal messages |
| Specialty-specific (vascular/procedural) | ⚠️ Partial | May be in "encounter documentation" PDFs | Product's core strength is procedural workflows; unclear if specialty-specific data structures are captured vs. generic PDFs |

**Summary**: Of 19 applicable domains, 2 are clearly covered (imaging, consents), 5 are partially/vaguely covered (demographics, encounters, procedures, clinical notes, billing), and 12 have no evidence of coverage. Many core clinical domains available through the g(10) FHIR API (problems, medications, allergies, vitals, labs, immunizations) are not mentioned in the b(10) export at all.

## 6. Documentation Quality

The b(10) export documentation quality is **extremely poor**:

- **No data dictionary**: Zero field-level documentation. No tables, columns, types, or relationships.
- **No schema**: No machine-readable format definition of any kind.
- **No sample data**: No example export files or screenshots of export output.
- **No user guide**: No instructions on how to trigger or configure an export.
- **No process documentation**: No description of who can request an export, what parameters exist, or how output is delivered.
- **Unexplained claims**: The term "computable format" for PDFs is used but never defined.
- **Grammatically awkward**: Several bullet points are incomplete sentences (e.g., "While certain EHI, such as images, documents, reports are exported in human-readable html/pdf format where applicable" — the "while" clause has no main clause).

A developer tasked with importing data from this export would have **nothing to work with**. They would need to receive an actual export to reverse-engineer the structure. The documentation provides no basis for building an import pipeline, validating exported data, or even understanding what to expect in the output.

**Contrast with g(10)**: The g(10) FHIR API has a 76-page PDF with endpoint documentation, authentication flows, and sample JSON for each resource type. The b(10) documentation is 6 bullet points — roughly 100 words total.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation is far too thin to assess actual coverage. Only 6 high-level format descriptions are provided with no field-level detail. Many core clinical domains (problems, medications, allergies, vitals, labs, immunizations, care plans, orders) are not mentioned at all in the b(10) documentation despite being available through the g(10) FHIR API. The vague "clinical and billing report and encounter documentation" PDF category could theoretically contain substantial data, but without any specification, this is unknowable. The DICOM image export is the only clearly specified, domain-appropriate element.

**Axis 2 — Export approach: Unclear/undetermined**

The b(10) export uses different formats (CCDA, HTML, PDF, DICOM) than the g(10) FHIR API, which suggests the vendor made *some* effort to create a distinct export rather than simply repackaging g(10). The mention of "billing report" and "consent forms" goes beyond USCDI scope, which is a positive signal. However, the documentation is so sparse that it's impossible to determine whether this is a genuinely purpose-built comprehensive export or just a collection of existing print/export functions relabeled for compliance. The lack of any data dictionary, schema, or field-level documentation makes it impossible to distinguish between a thoughtful EHI export and a minimal compliance checkbox.

### Key Findings

1. **The entire b(10) documentation is 6 bullet points (~100 words) with zero field-level detail.** No data dictionary, schema, sample data, or user guide exists. This is among the thinnest EHI export documentation possible while still acknowledging the requirement.

2. **DICOM image export is appropriate and a genuine strength.** For a product centered on outpatient procedure centers and imaging (PACS/RIS), exporting medical images in DICOM format is the correct technical choice and goes beyond what USCDI/FHIR covers.

3. **Multiple core clinical domains are unmentioned.** Problems, medications, allergies, vitals, labs, immunizations, care plans, and orders — all available through the vendor's own g(10) FHIR API — have no stated coverage in the b(10) export.

4. **The "clinical and billing report" PDF is a black box.** This single vague category could contain substantial patient data, but "computable format" PDF is unexplained and inherently limited for data portability. Without field-level documentation, it's impossible to assess what it actually contains.

5. **The b(10) export is distinct from g(10)**, which is a positive signal — the vendor did not simply relabel their FHIR API. However, the documentation gap between g(10) (76-page PDF) and b(10) (6 bullet points) is stark.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Unclear/undetermined
Export format:   Mixed (CCDA XML, HTML, PDF, DICOM, original)
Entities:        6 high-level categories (no entity/table detail)
Fields:          N/A (no field-level documentation)
Descriptions:    N/A
Sample data:     No
Bulk export:     Unclear
Domains covered: 2 of 19 clearly; 5 of 19 partially/vaguely
```

### Bottom Line

Braintree Health's b(10) EHI export documentation is a stub — 6 bullet points describing output formats with no data dictionary, no field-level detail, and no process documentation. While the DICOM image export is technically appropriate for this imaging-centric product, a patient or developer receiving this export would have no way to know what data is included, what fields to expect, or how to programmatically process the output. The single biggest gap is the complete absence of documentation — the export may be adequate, but the documentation makes it impossible to verify.
