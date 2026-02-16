# EHI Export Analysis: CloudCraft, LLC

**Product**: CloudCraft Software v9.0  
**Analysis date**: 2026-02-15  
**CHPL IDs**: 15.04.04.3071.Clou.09.01.1.221227 (CHPL ID 11150)

## 1. Product Context

CloudCraft Software is a cloud-hosted, web-based EHR system developed by NAIA Corporation (Birmingham, AL). It is marketed as an "all-in-one solution for electronic health records, practice management, billing, and human resources." The only confirmed deployment is Goshen Medical Center, a Federally Qualified Health Center (FQHC) with 38 service locations in eastern North Carolina. The presence of a sliding fee schedule module (for income-based discount management) confirms FQHC-oriented functionality.

**Data the product is expected to store:**

- **Clinical data**: Demographics, problem lists, medication lists, allergy lists, clinical notes, orders (medication, lab, imaging via CPOE), vital signs, immunizations, procedures, family health history, implantable devices, care plans, clinical decision support data
- **Documents**: Scanned paper records, digital faxes, images (JPEG, GIF, TIF), Word documents
- **Internal correspondence**: Tasks, notes
- **Billing data**: Explicitly listed as one of four core modules; specifics unknown but expected to include charges, claims, and payments
- **Practice management data**: Scheduling and encounter management (implied by "practice management" module branding)
- **Sliding fee/financial data**: Patient income-based discount calculations (FQHC requirement)
- **Public health reporting data**: Immunization registry, electronic case reporting, syndromic surveillance

The product holds a broad ONC certification covering 36 criteria, including (b)(10) EHI export. Certified 2022-12-27.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `B10.html` (6,525 bytes) | **The sole substantive artifact.** Single static HTML page constituting the entire EHI export documentation. Contains two sections (Provider Export, Patient Export Requests), a 5-step workflow diagram, and 5 bullet items listing exported data types. | **Primary** — only source of export information |
| `B10-page-screenshot.png` (150 KB) | Full-page browser screenshot of the rendered B10.html page | Low — confirms visual layout |
| `certification-index-screenshot.png` (262 KB) | Screenshot of the CloudCraft certification site landing page | Low — confirms B10.html is not linked from the certification site navigation |
| `Images/img1.gif` through `img5.gif`, `img2.png`, `arrow1.png`, `CloudCraft.png` | Workflow diagram icons, arrow graphic, logo | Low — decorative assets |
| `styles.css` (34 KB) | CSS stylesheet for B10.html | None — styling only |

**No data dictionary, schema, sample data, API documentation, or downloadable files of any kind were found.** The B10.html page confirmed still live (HTTP 200) as of 2026-02-15 with `Last-Modified: 2023-12-14`, served from S3 via CloudFront. Content unchanged since collection.

## 3. Export Mechanics

- **Format**: C-CDA USCDI v3 (structured clinical data) plus raw document files (PDF, JPEG, GIF, TIF, DOC/DOCX) and unspecified format for "internal correspondence"
- **Provider Export Mechanism**: Admin Console → bulk download. The page describes a 5-step workflow: (1) patient(s) submit requests, (2) admin accesses "Bulk Download" from Admin Console, (3) selects patients, (4) selects secure download location, (5) gives provider secure access. This is a UI-driven process with no API described.
- **Patient Export Mechanism**: FHIR R4 DocumentReference resource. No endpoint URLs, authentication details, or parameters are provided. Mentions "MyLinks, Apple Health, etc." as FHIR App Connections.
- **Single-patient vs bulk**: The provider pathway describes bulk export ("all primary care provider patient data" for selected patients). The patient pathway implies single-patient via FHIR apps.
- **Access constraints**: Not documented. The workflow mentions "secure" access but provides no technical details.
- **Fees**: Not mentioned.

The page describes the export as a "one-time bulk export" — the meaning of "one-time" is ambiguous (one-time per request? per patient? irrevocable?).

## 4. Export Content: What's In It

### No data dictionary exists

CloudCraft provides **zero** entity/table/field-level documentation. There are no table definitions, no column listings, no data types, no value sets, no relationships, no sample data, and no schema files. The entire export content specification consists of 5 bullet items repeated in both sections:

1. C-CDA USCDI v3
2. PDF documents, including scanned paper and digital records of faxes
3. Image files (JPEG, GIF, TIF)
4. Word documents
5. Internal correspondence such as tasks, notes

### Vendor's own content organization

The vendor does not organize content into categories beyond these 5 bullet points. There is nothing to tabulate at the entity/field level.

| Data Category (vendor's) | Format | Entities | Fields | Described |
|---|---|---|---|---|
| C-CDA USCDI v3 | C-CDA XML | N/A (standard) | N/A | Deferred to C-CDA standard |
| PDF documents | PDF | 0 | 0 | Name only |
| Image files | JPEG, GIF, TIF | 0 | 0 | Name only |
| Word documents | DOC/DOCX | 0 | 0 | Name only |
| Internal correspondence | Unknown | 0 | 0 | Name only |

**Total documented entities: 0. Total documented fields: 0.**

The C-CDA USCDI v3 reference implicitly defers all structured clinical data documentation to the HL7 C-CDA standard. No vendor-specific customizations, extensions, or field mappings are described.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes two pathways delivering the same 5 categories of data:

1. **C-CDA USCDI v3**: This is a well-defined clinical document standard that, when fully implemented, covers demographics, problems, medications, allergies, lab results, vitals, immunizations, procedures, clinical notes, care plans, goals, implantable devices, and family health history. However, C-CDA is a clinical *summary* format — it does not cover billing, practice management, or vendor-specific internal data structures.

2. **Document attachments** (PDF, images, Word): Raw files associated with patient records. This is appropriate for document-type data but tells us nothing about the structured data underneath.

3. **Internal correspondence** (tasks, notes): Mentioned but with no detail on format, structure, or what constitutes a "task" or "note" in this context.

The export is essentially a C-CDA document package with attached files. There is no indication of a native database export.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Implied via C-CDA USCDI v3 | C-CDA covers basic demographics; depth unknown without vendor documentation |
| Encounters / visits | ⚠️ Partial | Implied via C-CDA USCDI v3 | C-CDA has encounter sections but CloudCraft PM data likely exceeds this |
| Problems / conditions | ⚠️ Partial | Implied via C-CDA USCDI v3 | Standard USCDI data class |
| Medications / prescriptions | ⚠️ Partial | Implied via C-CDA USCDI v3 | Standard USCDI data class; no e-prescribing certification so scope unclear |
| Allergies | ⚠️ Partial | Implied via C-CDA USCDI v3 | Standard USCDI data class |
| Immunizations | ⚠️ Partial | Implied via C-CDA USCDI v3 | Standard USCDI data class |
| Vitals | ⚠️ Partial | Implied via C-CDA USCDI v3 | Standard USCDI data class |
| Lab results | ⚠️ Partial | Implied via C-CDA USCDI v3 | Standard USCDI data class |
| Imaging / diagnostic reports | ⚠️ Partial | Implied via C-CDA USCDI v3 + image files | Image files may include diagnostic images; CPOE for imaging is certified |
| Procedures | ⚠️ Partial | Implied via C-CDA USCDI v3 | Standard USCDI data class |
| Clinical notes / documents | ⚠️ Partial | C-CDA notes + PDF/Word/image attachments | Scanned records and faxes are included; structured note data limited to C-CDA |
| Care plans / goals | ⚠️ Partial | Implied via C-CDA USCDI v3 | Standard USCDI data class |
| Orders / referrals | ⚠️ Partial | Implied via C-CDA USCDI v3 | CPOE certified for meds, labs, imaging; order detail beyond C-CDA unknown |
| Insurance / coverage | ❌ Not covered | No mention in export documentation | Product has "billing" as a core module; insurance data is EHI — **gap** |
| Claims / billing | ❌ Not covered | No mention in export documentation | Product advertises billing as a core module; billing records are squarely within the designated record set — **significant gap** |
| Payments | ❌ Not covered | No mention in export documentation | If product processes payments, this is EHI — **gap** |
| Consents / directives | ❌ Not covered | No mention in export documentation | May be captured in scanned documents but no structured export |
| Patient communications / portal messages | ❌ Not covered | No mention in export documentation | Patient portal exists (ehrpatientportal.naiacorp.net) — **possible gap** |
| Sliding fee / FQHC financial data | ❌ Not covered | No mention in export documentation | Sliding fee module exists; income-based discounts are part of patient financial records — **gap** |
| Internal correspondence | ✅ Covered | Explicitly listed: "tasks, notes" | Format and completeness unknown |

**All clinical domains are rated ⚠️ Partial** because the vendor provides no documentation of what specific data they include in their C-CDA USCDI v3 implementation. The clinical data may be well-represented or may be a skeletal C-CDA — there is no way to assess from the documentation provided.

**Key gaps**: Billing, insurance, payments, and FQHC-specific financial data (sliding fee) are entirely absent from the export, despite billing being one of CloudCraft's four advertised core modules.

## 6. Documentation Quality

**Extremely poor.** The entire EHI export documentation consists of 150 words of visible prose on a single HTML page. Specific deficiencies:

- **No data dictionary**: Zero entity/table/field-level documentation. No column names, no data types, no constraints.
- **No schema files**: No XSD, JSON Schema, OpenAPI spec, or any machine-readable format definition.
- **No API documentation**: The FHIR section mentions DocumentReference but provides no endpoint URLs, authentication requirements, query parameters, or response examples.
- **No sample data**: No example C-CDA documents, no sample export packages, no illustrative files.
- **No user guide**: The 5-icon workflow provides the highest-level overview only. No screenshots, no step-by-step instructions, no explanations of options.
- **No versioning or changelog**: Page last modified 2023-12-14; no indication of version tracking.
- **Typo present**: "including meme document types" (line 45 of B10.html) — should be "MIME."

A developer receiving this export would need to rely entirely on knowledge of C-CDA and FHIR standards. The documentation provides no insight into what CloudCraft-specific data is in the export, how it's structured, or how to interpret it.

**Could a developer build an import from this documentation?** Only for the C-CDA portion, and only by treating it as a generic C-CDA import (using the HL7 standard, not CloudCraft-specific guidance). For the document attachments, a developer would know to expect PDF/image/Word files but nothing about naming conventions, metadata, or organization. For "internal correspondence," a developer would have no idea what to expect.

## 7. Overall Assessment

### Classification

**Minimal/stub.** The documentation is a single 150-word HTML page listing 5 categories of exported data with no field-level detail, no schema, no sample data, and no API specification. The export itself appears to be a C-CDA clinical summary repackaged as the (b)(10) export, supplemented with raw document files. There is no evidence of a native database model export.

### Key Findings

1. **The export is a C-CDA repackaging, not a comprehensive EHI export.** By describing the structured clinical data component as "C-CDA USCDI v3," CloudCraft implicitly limits the export to what C-CDA can represent — approximately the same data as the (g)(10) Standardized API. This is a clinical summary, not "all electronic health information." (`B10.html`, line 76)

2. **Billing data is entirely absent despite being a core product module.** CloudCraft advertises billing as one of its four core modules (EHR, practice management, billing, HR). Billing records — charges, claims, payments, adjustments — are squarely within the HIPAA designated record set but are not mentioned anywhere in the export documentation. (`product-research.md`, lines 60–68; `B10.html` — billing not mentioned)

3. **Zero field-level documentation exists.** There is no data dictionary, no schema, no entity definitions, and no field listings. The export content specification consists of exactly 5 bullet items. This makes the export essentially opaque — a recipient cannot know what data they're getting without inspecting the actual files. (`B10.html`, lines 75–81, 95–101)

4. **The documentation is 150 words total**, making it among the most minimal EHI export documentation possible. It meets the bare minimum of having a publicly accessible page at the registered CHPL URL but provides no actionable technical detail. (Verified via `parse_b10.py`: `visible_word_count: 150`)

5. **Document attachments and internal correspondence provide some coverage beyond C-CDA.** The inclusion of PDF, image, and Word documents plus "internal correspondence such as tasks, notes" goes slightly beyond a pure C-CDA export. However, without documentation of structure or format, this is marginal added value. (`B10.html`, lines 77–81)

### Summary Stats

```
Classification:  Minimal/stub
Export format:   C-CDA XML + raw document files (PDF, JPEG, GIF, TIF, DOC/DOCX)
Model type:      Standard projection (C-CDA USCDI v3)
Entities:        0 (no data dictionary)
Fields:          0 (no data dictionary)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (admin console workflow described)
Domains covered: 1 of 15+ applicable domains confirmed; ~12 partial via C-CDA inference
```

### Bottom Line

CloudCraft's (b)(10) EHI export is a C-CDA clinical summary repackaged with document attachments — not a comprehensive export of all electronic health information. With billing explicitly absent despite being a core product module, zero field-level documentation, and only 150 words of total prose, this is a compliance checkbox rather than a genuine effort to enable patient data portability. The single biggest gap is the complete absence of billing, insurance, and financial data from a product that advertises billing as a core capability.
