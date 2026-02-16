# EHI Export Analysis: ChartPath, LLC

**Product**: ChartPath v1.29  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.04.04.2996.Char.12.01.1.191227 (CHPL ID 10258)

## 1. Product Context

ChartPath is a cloud-based EHR purpose-built for **physician practices that round on patients in long-term and post-acute care (LTPAC) facilities** — primarily skilled nursing facilities (SNFs) and assisted living facilities (ALFs). It is not the facility's EHR; it is the visiting physician group's charting and billing system. The company (now part of LivTech) reports 250+ practices and 4,000+ users as of late 2022.

**Key data domains the product stores:**
- **Clinical encounter documentation**: Single-page encounter notes from facility rounding, with pull-forward from prior visits. This is the core workflow.
- **Patient demographics**: Including multi-facility census management (patients tracked across multiple LTPAC facilities).
- **Medications**: Certified for e-prescribing (a)(2), including drug-drug and drug-allergy checking (a)(5).
- **Problem/diagnosis lists**: ICD-10 coded diagnoses for encounter documentation and CQM reporting.
- **Screening/assessment scores**: Structured tools for anxiety, dementia staging, depression, caregiver burden — specialty-specific to LTPAC populations. GUIDE Model (CMS dementia care) assessments.
- **Billing/RCM data**: Smart CPT coding, RVU tracking, claims, and reimbursement. ChartPath RCM and RCM Pro products launched in 2021.
- **Implantable device data**: Certified for (a)(14).
- **Orders**: Mentioned in integration documentation with PointClickCare.
- **Allergies**: Implied by drug-allergy checking certification.
- **C-CDA documents**: Certified for transitions of care (b)(1), (b)(2).
- **FHIR API data**: Certified for (g)(10) with a 55-page FHIR API document covering standard US Core resources.

A complete (b)(10) export should cover all of these domains, particularly the billing/RCM data and specialty screening assessments that go beyond what C-CDA and FHIR US Core capture.

## 2. Artifacts Reviewed

| Artifact | Size | Description | Informativeness |
|---|---|---|---|
| `downloads/ehiexport-page.html` | 15,298 bytes | The sole EHI export documentation page. 144 words of substantive content describing export as ZIP of PDFs/C-CDAs/attachments. | **Primary source** — but extremely thin |
| `downloads/ehiexport-page-screenshot.png` | 293,816 bytes | Full-page screenshot confirming the page renders as a simple landing page with no interactive elements or hidden content. | Confirmatory |
| `downloads/2015-cehrt-page.html` | 148,806 bytes | Mandatory disclosures / 2015 CEHRT page. Contains buttons linking to certification documents. The "EHI Export" button links back to the same ehiexport page. | Context — confirms no additional EHI documentation exists on the vendor site |
| `downloads/2015-cehrt-screenshot.png` | 555,179 bytes | Screenshot of CEHRT page showing document download buttons. | Confirmatory |

**No data dictionary, schema, sample data, or field-level documentation was found in any artifact.** The prior report's claim that this is "among the most minimal EHI export documentation encountered" is independently verified.

## 3. Export Mechanics

- **Format**: ZIP archive containing:
  - Sub-ZIP of per-encounter **PDF** documents
  - Sub-ZIP of per-encounter **C-CDA** documents
  - A **face sheet** document with patient demographics
  - Sub-ZIP of **attached files** in their original format
- **Mechanism**: Not documented. No UI instructions, API specification, or workflow description is provided. The (e)(3) certification (patient health information export on request) suggests it may be a UI-driven process, but this is not stated.
- **Single-patient vs bulk**: Not specified. The documentation says "the patient EHI export" (singular), suggesting single-patient export.
- **Access constraints or fees**: Not documented.

## 4. Export Content: What's In It

### No data dictionary exists

The EHI export documentation contains **zero** entities, tables, fields, or structured data definitions. The entire documentation is 144 words across 9 paragraphs, of which 3 paragraphs merely define file format acronyms (ZIP, PDF, C-CDA).

The substantive content reduces to:
1. The export is a ZIP file
2. Each encounter is available as PDF and C-CDA
3. Demographics are in a "face sheet" and in encounter documents
4. Attached files are included

### Vendor's own content organization

There is no vendor-provided content organization. The vendor does not enumerate entities, tables, categories, or fields.

| Entity/Table | Fields | Described | Types | Category (vendor's) |
|---|---|---|---|---|
| *(none documented)* | — | — | — | — |

### Inferred export content

Based on the described format (C-CDA + PDF per encounter), the export likely contains whatever data ChartPath puts into its C-CDA encounter documents. Standard C-CDA sections would include: demographics, problems, medications, allergies, vitals, procedures, results, and encounter information. However, **ChartPath does not document which C-CDA sections or templates it populates**, making it impossible to verify coverage. Their separate 55-page FHIR API document (for (g)(10)) lists standard US Core resources (Patient, AllergyIntolerance, CarePlan, CareTeam, Problems, Implantable Device, DiagnosticReport, DocumentReference, Laboratory Results, Goal, Immunization, Medication, Smoking Status, Procedure, Provenance, Vital Signs, Encounter, CCDA summary), but this is the (g)(10) API, not the (b)(10) export.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor provides no categories, modules, or organizational structure for the export content. The only information is that the export produces encounter-level PDFs and C-CDAs plus a demographics face sheet and attachments.

**There is no way to assess depth or breadth from the documentation alone.** The vendor has not documented:
- What C-CDA sections are populated
- What data elements appear in encounter PDFs
- Whether any structured data beyond C-CDA content is exported
- Whether billing, screening scores, or other non-clinical data appears anywhere in the export

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | "Face sheet" mentioned; demographics said to be in PDFs and C-CDAs | Present in some form, but no field-level detail. Multi-facility census data likely not captured in C-CDA. |
| Encounters / visits | ⚠️ Partial | Per-encounter PDFs and C-CDAs produced | Encounter documents exist, but no detail on what structured data is captured vs. just narrative text. |
| Problems / conditions | ⚠️ Partial | Likely in C-CDA if standard sections populated | Unverifiable — C-CDA template details not documented. |
| Medications / prescriptions | ⚠️ Partial | Likely in C-CDA if standard sections populated | Unverifiable. Product has e-prescribing (a)(2); prescription history may or may not appear in full. |
| Allergies | ⚠️ Partial | Likely in C-CDA if standard sections populated | Unverifiable. Product certified for drug-allergy checking (a)(5). |
| Immunizations | ⚠️ Partial | Likely in C-CDA if standard sections populated | Unverifiable. Less relevant for LTPAC specialty but product is certified. |
| Vitals | ⚠️ Partial | Likely in C-CDA if standard sections populated | Unverifiable. |
| Lab results | ⚠️ Partial | May appear in C-CDA if received via HIE/integration | Product may not natively manage labs (not certified for (a)(3) CPOE for labs). |
| Procedures | ⚠️ Partial | Likely in C-CDA if standard sections populated | Unverifiable. |
| Clinical notes / documents | ⚠️ Partial | PDFs of encounter notes included | PDF notes are human-readable but not computable. C-CDA encounter documents provide some structure. |
| Care plans / goals | ⚠️ Partial | May be in C-CDA; product has CarePlan in FHIR API | Unverifiable. |
| Orders / referrals | ❌ Not covered | No mention in export documentation | Product stores orders (per PointClickCare integration docs). Not addressed. |
| Insurance / coverage | ❌ Not covered | No mention in export documentation | Product stores insurance data for billing. Not addressed. |
| Claims / billing | ❌ Not covered | No mention in export documentation | **Significant gap.** ChartPath has full RCM module (ChartPath RCM, RCM Pro) with CPT coding, RVU tracking, claims, and reimbursements. None of this appears in the export. |
| Payments | ❌ Not covered | No mention in export documentation | Related to billing gap above. |
| Screening/assessments (specialty) | ❌ Not covered | No mention of structured assessment data | **Significant gap.** ChartPath stores structured screening scores for anxiety, dementia staging, depression, caregiver burden, and GUIDE Model assessments. These LTPAC-specific assessments are core to the product's value proposition and would not appear in standard C-CDA sections. |
| Implantable devices | ❌ Not covered | Not mentioned; product certified for (a)(14) | May be in C-CDA but undocumented. |
| Patient communications | N/A | Product has no patient portal | No (e)(1) certification; not a gap. |
| Imaging / diagnostic reports | N/A | Product does not appear to manage imaging | No imaging capabilities identified. |
| Consents / directives | ❌ Not covered | No mention | May be stored as attachments; unclear. |

**Summary**: Of 17 applicable domains, **zero are verifiably covered** at field level. At best, ~10 clinical domains are **partially** covered by inference from C-CDA inclusion. At least 5 domains where the product stores data (billing/claims, insurance, screening assessments, orders, implantable devices) have **no evidence of coverage**.

## 6. Documentation Quality

The EHI export documentation is essentially non-functional:

- **Can a developer use it?** No. A developer receiving this documentation would know only that the export is "a ZIP with PDFs and C-CDAs." They would have no field definitions, no schema, no C-CDA template specifications, and no sample data to work with. They would need to reverse-engineer an actual export.
- **What's well-documented?** The container format (ZIP) and the high-level file types (PDF, C-CDA, attachments). That's it.
- **What requires guesswork?** Everything else: which C-CDA sections are populated, what data elements appear in encounter documents, whether any structured data beyond C-CDA content is exported, how to initiate the export, whether it can be automated.
- **Machine-readable artifacts?** None. No schemas, no sample data, no JSON/XML definitions.
- **Three of the nine paragraphs** (33% of content) are spent defining common file format acronyms (ZIP, PDF, C-CDA) that any technical audience would already know.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation is far too thin to assess what the export actually contains. The described format — per-encounter C-CDAs and PDFs — suggests at best a **clinical encounter document export**, which would cover standard C-CDA sections (demographics, problems, medications, allergies, vitals) but would miss billing/RCM data, structured screening assessments, implantable device lists, orders, and census management data. ChartPath's core differentiator is LTPAC-specific functionality (dementia staging, caregiver burden assessments, multi-facility census management, RCM for SNF/ALF rounding) — none of which is addressed in the export documentation. Even if the C-CDA documents are well-populated, the format inherently cannot capture the structured billing and specialty assessment data that constitutes a significant portion of ChartPath's designated record set.

**Axis 2 — Export approach: Repackaged existing export**

The export is described as per-encounter C-CDA documents plus PDFs — this is essentially the same clinical document exchange capability required for transitions of care (b)(1)/(b)(2) certification, bundled into a ZIP with attached files. There is no evidence of a purpose-built export that goes beyond existing clinical document exchange to capture billing, specialty assessments, or other non-USCDI data. The vendor maintains a separate 55-page FHIR API document for (g)(10) and treats the (b)(10) export as a thin wrapper around encounter document generation.

### Key Findings

1. **Documentation is among the thinnest possible**: 144 words, zero field definitions, zero entities, zero schemas. Three paragraphs define ZIP, PDF, and C-CDA. This is a compliance stub, not usable documentation.

2. **Billing/RCM data is completely absent**: ChartPath has a full revenue cycle management product (ChartPath RCM, RCM Pro with CPT coding, RVU tracking, claims, reimbursements), but the export documentation makes no mention of any billing data. This is a significant gap in the designated record set.

3. **Specialty screening assessments are not addressed**: ChartPath's LTPAC-specific structured assessments (dementia staging, caregiver burden, anxiety/depression screening, GUIDE Model data) — core to its value proposition — appear nowhere in the export documentation. Standard C-CDA sections cannot fully represent these structured, scored instruments.

4. **Export format is document-centric, not data-centric**: Per-encounter PDFs and C-CDAs produce human-readable documents but not structured, queryable data. A developer receiving this export would get narrative clinical notes, not a computable dataset. This is clinical document exchange rebranded as EHI export.

5. **No way to verify actual export content**: Without sample data, C-CDA template documentation, or field definitions, it is impossible to determine from the documentation alone what the export actually produces. The vendor could be exporting more than documented — but the documentation provides no evidence of this.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Repackaged existing export
Export format:   ZIP containing PDFs, C-CDAs, and attachments
Entities:        N/A (no data dictionary)
Fields:          N/A
Descriptions:    N/A
Sample data:     No
Bulk export:     Unclear
Domains covered: 0 of 17 verifiably; ~10 of 17 plausibly partial via C-CDA inference
```

### Bottom Line

ChartPath's EHI export documentation is a 144-word landing page that describes a ZIP of encounter PDFs and C-CDAs — effectively repackaging its existing clinical document exchange as a (b)(10) export. A patient or provider would receive encounter documents but likely miss billing/RCM data, structured LTPAC-specific assessments, and other non-clinical data that constitutes a meaningful portion of ChartPath's designated record set. The single biggest gap is the complete absence of documentation — without a data dictionary, schema, or sample data, there is no way to verify what the export actually produces or to import it into another system.
