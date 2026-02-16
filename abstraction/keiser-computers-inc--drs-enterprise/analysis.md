# EHI Export Analysis: Keiser Computers, Inc.

**Product**: Drs Enterprise  
**Analysis date**: 2026-02-16  
**CHPL ID**: 15.04.04.1764.DrsE.12.01.1.221213 (CHPL #11072)

## 1. Product Context

Drs Enterprise is an ambulatory EHR system from a small Fort Lauderdale-based vendor (founded 1985), targeting small to medium-sized medical practices across general and specialty care (orthopedics, ophthalmology, sports medicine, OB/GYN). It is document-centric, built around a customizable patient chart with drag-and-drop filing, QR-code-based document scanning, and rich clinical narrative generation ("Clicktation").

Key data domains the product stores:
- **Clinical documentation**: Progress notes, clinical narratives, customizable templates, problem lists, medication lists, allergy lists
- **Prescriptions**: e-prescribing via SureScripts with drug interaction checking
- **Documents**: Scanned documents, PDFs, Word files, photographs, faxes in customizable folder structures
- **Lab results**: Via HL7 interface in both discrete and scanned formats
- **Charge capture**: Charges posted during visits exported to external billing systems
- **EOB processing**: Explanation of Benefits management
- **Tasks/messages**: Internal workflow tasks, phone messages, secure messaging
- **Forms**: Auto-populated clinical and administrative forms
- **Patient portal**: View/download/transmit capabilities
- **Fax system**: Integrated fax management

**Critical note**: Drs Enterprise does NOT include a full billing/practice management system. It integrates with third-party PM systems (MicroMD, Medisoft, Medical Manager, MedFX, PCN) and exports charge data to them. Core billing, claims, and A/R reside in external systems.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/Export_data.pdf` (10 pages, 1.0 MB) | Primary EHI export documentation PDF dated 2023-11-07. Describes export format, directory structure, XML element definitions for 7 entities, enumerator definitions, and XML examples. | **Most informative** — sole product-specific documentation |
| `downloads/DataExport.html` (8.3 KB) | HTML landing page at drsdoc.com/DataExport. Brief introduction stating C-CDA export format and link to the PDF. | Low — just a pointer to the PDF |
| `downloads/screenshot-DataExport-page.png` (119 KB) | Screenshot of the landing page | Low — confirms page content |
| `downloads/enrichment/export-schema.json` (20 KB) | Machine-readable JSON extraction of the PDF's full schema: 7 XML entities, 71 fields, 2 enumerators, 7 file types | High — structured parse of the PDF, verified against source |
| `downloads/enrichment/extract-export-schema.ts` (17.8 KB) | TypeScript script used to produce the enrichment JSON | Reference — documents parsing methodology |

## 3. Export Mechanics

- **Format**: C-CDA XML (account_ccda.xml) + proprietary XML sidecar files + raw document files (PDF, TIF, RTF, etc.) + patient photo (IMG)
- **Mechanism**: UI-driven export within the application ("options selected during the export")
- **Single-patient vs bulk**: Both supported — documentation states "for a single patient as well as for multiple patients"
- **Directory structure**: Patient data organized in hexadecimal folder hierarchy based on Account ID (4 levels of 2-hex-digit folders, e.g., `00/00/27/0F` for Account ID 9999)
- **Access constraints**: No fees or special access requirements mentioned
- **Error handling**: Errors logged to `errors_<Session_ID>.xml` in an `export_xml` folder
- **Documentation link**: A `Readme.txt` file in the export provides the public URL to the documentation

## 4. Export Content: What's In It

The export consists of two distinct components:

### Component 1: C-CDA (account_ccda.xml)
The vendor states this file contains "the patient's EHI data, such as demographics, problems, medications, allergies, etc. in compliance with the USCDv1 standard." The documentation provides **no product-specific field-level detail** for the C-CDA — it simply references the HL7 C-CDA 2.1 standard and links to the generic HL7 specification documents. This means the C-CDA component exports whatever falls within the standard C-CDA template set (USCDI v1 scope), with no evidence of vendor-specific extensions or customizations.

### Component 2: Proprietary XML sidecars + raw files
The vendor documents 7 XML entities across 71 fields with product-specific metadata for documents, office notes, tasks, structured data lookups, and faxes. All 71 fields have descriptions, types, and optionality documented. Two enumerators define 32 values total.

### Vendor's content organization

| Entity/Table | Fields | Described | Types | Context |
|---|---|---|---|---|
| Document | 15 | 15 | yes | `<Document_ID>_info.xml` — metadata for exported documents |
| office_notes | 13 | 13 | yes | `<Document_ID>_info.xml` — notes linked to documents |
| tasks | 14 | 14 | yes | `account_tasks.xml` — tasks linked to patient account |
| doc_data | 8 | 8 | yes | `<Document_ID>_info.xml` — Drs Data Lookup values (LOINC-coded) |
| loinc_code | 1 | 1 | yes | Nested within doc_data — LOINC code descriptions |
| fax_inbox | 10 | 10 | yes | `Fax_inbox.xml` — inbox fax metadata |
| fax_outbox | 10 | 10 | yes | `Fax_outbox.xml` — outbox fax metadata |

**Additional exported files** (not XML entities but part of the export):
- `account_ccda.xml` — C-CDA clinical data
- `Account_U.img` — patient photograph
- `<Document_ID>.<ext>` — raw document files (PDF, XML, TIF, RTF, etc.)
- `<fax_id>_Fax_Inbox.tif` / `<fax_id>_Fax_Outbox.tif` — fax images

### Summary statistics
- **Total proprietary entities**: 7
- **Total proprietary fields**: 71 (100% with descriptions)
- **Enumerators**: 2 (convert_type: 12 values; TFieldType: 20 values)
- **C-CDA content**: Defers entirely to HL7 C-CDA 2.1 standard (no product-specific documentation)
- **Sample data**: XML examples provided for 5 of 7 entities (no full sample export file)

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export has two layers:

1. **C-CDA layer**: Covers standard USCDI v1 clinical data — demographics, problems, medications, allergies, immunizations, vitals, lab results, procedures, care plans, clinical notes. No product-specific documentation is provided; the vendor simply references the HL7 standard. This layer represents the product's existing clinical exchange capability, not a purpose-built EHI export.

2. **Proprietary XML layer**: Adds document metadata (15 fields per document including folder location, creation/modification tracking, user-defined fields), office notes (13 fields with note text, types, priority), tasks (14 fields with assignment tracking), structured data lookups (8 fields with LOINC coding), and fax metadata (20 fields across inbox/outbox). This layer adds some value beyond the C-CDA by capturing document management and workflow data that doesn't fit in C-CDA.

The proprietary layer is the only evidence of purpose-built export work. However, it covers a narrow slice: primarily document metadata, notes, and tasks. It does not address structured clinical data beyond what C-CDA already carries, nor does it export charge capture data, EOB data, forms, patient portal data, or internal messaging — all of which the product stores.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA standard demographics only; no product-specific field documentation | Product stores demographics; C-CDA covers basics but no evidence of custom fields beyond USCDI |
| Encounters / visits | ⚠️ Partial | C-CDA encounters section | Product stores visits; C-CDA covers standard encounters but depth unclear |
| Problems / conditions | ⚠️ Partial | C-CDA problems section | Standard C-CDA coverage; no product-specific extensions documented |
| Medications / prescriptions | ⚠️ Partial | C-CDA medications section | Product has e-prescribing with SureScripts; C-CDA covers basics; interaction checking data, prescription history depth unclear |
| Allergies | ⚠️ Partial | C-CDA allergies section | Standard C-CDA coverage |
| Immunizations | ⚠️ Partial | C-CDA immunizations section | Standard C-CDA coverage |
| Vitals | ⚠️ Partial | C-CDA vitals + doc_data with LOINC codes | doc_data provides some structured vital values with LOINC coding; better than C-CDA alone |
| Lab results | ⚠️ Partial | C-CDA lab results section | Product has HL7 lab interface storing discrete data; C-CDA may not capture full discrete lab details |
| Imaging / diagnostic reports | ❌ Not covered | No specific evidence | Unclear if product stores imaging reports beyond documents |
| Procedures | ⚠️ Partial | C-CDA procedures section | Standard C-CDA coverage |
| Clinical notes / documents | ✅ Covered | Raw document files exported + Document metadata (15 fields) + office_notes (13 fields) | Strongest area — documents exported as-is with rich metadata and linked notes |
| Care plans / goals | ⚠️ Partial | C-CDA care plan section if present | Standard C-CDA; unclear product depth |
| Orders / referrals | ❌ Not covered | No specific evidence | No export of orders or referral data |
| Insurance / coverage | ❌ Not covered | No insurance entities in export | Product imports insurance data from PM systems; may not store independently |
| Claims / billing | ❌ Not covered | No billing entities in export | Product has charge capture module and EOB Manager — charges/EOBs are NOT exported. However, core billing resides in external PM systems, so this is a **partial gap** (charge capture data is in the product but not exported) |
| Payments | N/A | — | Core payment processing in external PM systems |
| Consents / directives | ❌ Not covered | No consent entities | May be stored as documents (which are exported as raw files) but no structured consent data |
| Patient communications / portal | ❌ Not covered | No messaging or portal data entities | Product has patient portal and secure messaging; not in export |
| Tasks / workflow | ✅ Covered | tasks entity (14 fields) with assignment and completion tracking | Purpose-built — not in C-CDA |
| Fax communications | ✅ Covered | fax_inbox (10 fields) + fax_outbox (10 fields) + raw TIF files | Purpose-built — includes fax images and metadata |

**Domains covered**: 3 of 16 applicable domains with dedicated export entities (documents, tasks, faxes)  
**Domains with C-CDA-only coverage**: 9 domains (demographics through care plans — all via generic C-CDA with no product-specific depth)  
**Domains not covered**: 4 domains (orders/referrals, insurance, claims/billing charge capture, patient portal/messaging)

## 6. Documentation Quality

**Strengths**:
- The proprietary XML sidecar documentation is well-structured: every field has a name, type, description, and optionality flag
- XML examples provided for 5 of 7 entities
- Directory structure and file naming conventions clearly documented
- Two enumerators fully specified with all values

**Weaknesses**:
- The C-CDA component — which carries the bulk of the clinical data — has **zero product-specific documentation**. The vendor simply links to the generic HL7 C-CDA 2.1 spec. A developer would have no way to know which C-CDA sections/templates are actually populated, what extensions (if any) are used, or how the product maps its internal data to C-CDA elements.
- No sample export files provided (only XML snippets within the documentation)
- No machine-readable schema for the proprietary XML — just narrative documentation
- No relationships or foreign keys documented between entities (e.g., how doc_data relates to documents)
- No value sets or code systems beyond the two enumerators
- 10-page document total — thin for a complete EHI export specification

**Could a developer build an import?** Partially. The proprietary XML sidecars are documented well enough to parse. But for the C-CDA component, which carries demographics, problems, medications, allergies, immunizations, vitals, labs, and procedures, a developer would need to rely entirely on the generic C-CDA standard with no product-specific guidance. This is workable (C-CDA is a well-known standard) but provides no insight into what data the product actually exports beyond the standard minimum.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The export covers clinical data via C-CDA (USCDI v1 scope) plus a genuinely useful proprietary layer for documents, tasks, and faxes. However, it omits charge capture data (which the product stores), EOB data (the product has an EOB Manager), patient portal content, and secure messaging — all of which are EHI within the product's designated record set. The C-CDA layer is strictly USCDI v1 with no evidence of extensions or customization. The proprietary XML layer adds real value for document management and workflow data, but covers only 3 non-USCDI domains out of a larger set the product supports.

The product's scope is somewhat bounded by its ambulatory EHR positioning — it doesn't do full billing/PM — which means the gap is less severe than it would be for a full-stack system. But charge capture and EOB data are explicitly within the product's capabilities and are not exported.

**Axis 2 — Export approach: Repackaged existing export (with modest additions)**

The core clinical export is a standard C-CDA — the vendor explicitly says it's "in compliance with the USCDv1 standard" and links only to the generic HL7 spec. This is the product's existing clinical exchange format relabeled as (b)(10). The vendor added proprietary XML sidecars for documents, office notes, tasks, fax metadata, and structured data lookups — this represents genuine (b)(10) work beyond clinical exchange. However, the additions are limited (71 fields across 7 entities) and the C-CDA component has no product-specific depth. The export is primarily a C-CDA repackaging with a thin proprietary supplement.

### Key Findings

1. **C-CDA core with no product-specific documentation**: The clinical data export is a generic C-CDA 2.1 file with zero product-specific field documentation. The vendor links to the HL7 standard spec and says it contains "demographics, problems, medications, allergies, etc." — this is a repackaged clinical exchange export, not a purpose-built EHI export. (Source: Export_data.pdf page 2)

2. **Proprietary XML sidecars add genuine value**: The vendor documents 7 XML entities with 71 fully-described fields covering document metadata, office notes, tasks, structured data lookups (LOINC-coded), and fax metadata. This is purpose-built (b)(10) content that goes beyond C-CDA. (Source: Export_data.pdf pages 4–10)

3. **Charge capture and EOB data not exported**: The product has a charge capture module and EOB Manager, but neither appears in the export documentation. These are patient-specific billing records within the designated record set. (Source: product-research.md vs. Export_data.pdf)

4. **Patient portal and messaging data absent**: The product has a patient portal (certified for (e)(1)) and secure messaging, but the export does not include portal content or message history. (Source: product-research.md vs. Export_data.pdf)

5. **Documentation is thin but honest**: At 10 pages, the documentation is brief but well-structured for what it covers. The vendor is transparent about the C-CDA standard reliance and provides clear documentation for the proprietary components. No sample export data is provided.

### Summary Stats

    Coverage:        Partial
    Approach:        Repackaged existing export (with proprietary XML supplement)
    Export format:   C-CDA XML + proprietary XML + raw document files
    Entities:        7 (proprietary XML only; C-CDA defers to standard)
    Fields:          71 (proprietary) + C-CDA standard fields (undocumented product-specifically)
    Descriptions:    100% of proprietary fields
    Sample data:     No (XML snippets only, no full sample export)
    Bulk export:     Yes (single and multi-patient)
    Domains covered: 3 of 16 applicable domains with dedicated entities; 9 additional via generic C-CDA

### Bottom Line

Drs Enterprise's EHI export is primarily a standard C-CDA clinical summary supplemented by proprietary XML sidecars for document metadata, tasks, and faxes. While the proprietary additions show genuine effort beyond a bare C-CDA relabel, the export omits charge capture data, EOB data, patient portal content, and messaging — all of which the product stores. A patient would receive their clinical summary, stored documents, and task/fax history, but not their complete designated record set.
