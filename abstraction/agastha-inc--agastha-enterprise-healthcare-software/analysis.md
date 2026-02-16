# EHI Export Analysis: Agastha, Inc.

**Product**: Agastha Enterprise Healthcare Software
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.1056.Agas.20.01.1.221228 (v20.1), 15.04.04.1056.Agas.25.02.1.250325 (v25.1)

## 1. Product Context

Agastha Enterprise Healthcare Software is an integrated, cloud-based healthcare platform developed by Agastha, Inc., a small (~18 employees) Charlotte, NC-based company. The product combines **EHR, practice management, pharmacy management, laboratory information system (LIS), billing/claims, patient portal, e-prescribing (including EPCS), and telehealth** into a single platform. It targets ambulatory practices, multi-specialty clinics, hospitals, pharmacies, and laboratories, serving specialties including primary care, internal medicine, oncology, neurology, dermatology, emergency medicine, mental health, and pediatrics.

For assessing export completeness, the key product capabilities that should be represented in a genuine (b)(10) export include:
- **Clinical EHR data**: encounters, problems, medications, allergies, labs, vitals, immunizations, procedures, clinical notes, care plans
- **Billing & claims**: invoicing, insurance claim submission, eligibility verification, revenue cycle management, payments
- **Pharmacy management**: medication inventory, procurement, stock tracking, pharmacy sales/billing
- **Laboratory (LIS)**: lab orders, specimen tracking, barcode data, device connectivity, result management
- **E-prescribing**: prescription transmission records, EPCS records, controlled substance prescribing details
- **Patient portal**: secure messaging between patients and providers, portal interactions
- **Telehealth**: virtual visit records, remote monitoring data
- **Practice management**: scheduling, patient registration, document management
- **Custom/specialty data**: oncology-specific assessments, neurology data, mental health records

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/Agastha-B10-Documentation.pdf` (586 KB, 7 pages) | Primary (b)(10) EHI export documentation. Lists 21 FHIR R4 resources, shows UI screenshots, provides resource-level descriptions copied from FHIR spec. | **Primary source** — but very thin. No field-level detail. |
| `downloads/dataExport.html` (5 KB) | EHI export landing page. Version history (v1.0, 2023-04-10), links to PDF and FHIR API docs. | **Minimal** — just a linking page. |
| `downloads/apiR4.html` (215 KB) | FHIR R4 API documentation for (g)(10). Documents 23 FHIR resources with API endpoints, query parameters, and sample JSON responses. | **Supplementary** — reveals 4 additional resources (Appointment, ChargeItem, Coverage, FamilyMemberHistory) not listed in B10 PDF. |

No sample data files, no JSON schemas, no data dictionary, no FHIR profiles, no XLSX/CSV artifacts were provided.

## 3. Export Mechanics

- **Format**: FHIR R4 JSON (4.0.1) conforming to US Core IG STU V3.1.1 for 21 listed resources; "standard JSON format" for unspecified additional resources
- **Standards**: HL7 FHIR R4, US Core STU V3.1.1, HL7 FHIR Bulk Data Export
- **Mechanism**: UI-based — "Data Portability/Export" screen with role-based access
- **Scope options**:
  - Single patient export (with Date of Service filter: Date Range / Previous Month / None)
  - Group of patients (comma-separated account IDs)
  - Patient population (all patients)
- **Bulk capability**: Yes — supports group and population-level export
- **Access constraints**: Requires "assigned roles" / "clinical users with assigned rights"
- **Fees**: Not mentioned in documentation

## 4. Export Content: What's In It

### Field-level documentation

**There is no field-level documentation.** The B10 PDF provides only resource-level names and descriptions copied verbatim from the FHIR R4 specification. No Agastha-specific field mappings, no custom extensions, no value sets, no data types beyond what FHIR standard defines, no relationships beyond FHIR references.

### Vendor's own content organization

The vendor does not organize their export into categories. The documentation simply lists 21 FHIR resource types. The descriptions are generic FHIR spec definitions, not product-specific mappings.

| Entity (FHIR Resource) | Fields | Described | Types | In B10 PDF | In (g)(10) API |
|---|---|---|---|---|---|
| AllergyIntolerance | N/A | N/A | N/A | ✅ | ✅ |
| Appointment | N/A | N/A | N/A | ❌ | ✅ |
| CarePlan | N/A | N/A | N/A | ✅ | ✅ |
| CareTeam | N/A | N/A | N/A | ✅ | ✅ |
| ChargeItem | N/A | N/A | N/A | ❌ | ✅ |
| Condition | N/A | N/A | N/A | ✅ | ✅ |
| Coverage | N/A | N/A | N/A | ❌ | ✅ |
| Device | N/A | N/A | N/A | ✅ | ✅ |
| DiagnosticReport | N/A | N/A | N/A | ✅ | ✅ |
| DocumentReference | N/A | N/A | N/A | ✅ | ✅ |
| Encounter | N/A | N/A | N/A | ✅ | ✅ |
| FamilyMemberHistory | N/A | N/A | N/A | ❌ | ✅ |
| Goal | N/A | N/A | N/A | ✅ | ✅ |
| Immunization | N/A | N/A | N/A | ✅ | ✅ |
| Location | N/A | N/A | N/A | ✅ | ❌ |
| Medication | N/A | N/A | N/A | ✅ | ❌ |
| MedicationRequest | N/A | N/A | N/A | ✅ | ✅ |
| Observation | N/A | N/A | N/A | ✅ | ✅ |
| Organization | N/A | N/A | N/A | ✅ | ✅ |
| Patient | N/A | N/A | N/A | ✅ | ✅ |
| Practitioner | N/A | N/A | N/A | ✅ | ✅ |
| Procedure | N/A | N/A | N/A | ✅ | ✅ |
| Provenance | N/A | N/A | N/A | ✅ | ✅ |
| RelatedPerson | N/A | N/A | N/A | ✅ | ✅ |
| ServiceRequest | N/A | N/A | N/A | ✅ | ✅ |

All fields are marked N/A because no field-level documentation exists — only resource-level names with FHIR spec descriptions.

### The "other resources" claim

The B10 PDF contains a critical sentence: *"All the other resources are currently exported using the standard JSON format."* This implies the export includes data beyond the 21 FHIR resources, but **zero documentation** exists for what those other resources are, what format they take, what fields they contain, or what data domains they represent. This claim is unverifiable from the provided documentation.

### apiR4.html discrepancies

The (g)(10) FHIR API documentation (`apiR4.html`) documents **23 FHIR resources** — 4 more than the B10 PDF lists:
- **Appointment** — scheduling data
- **ChargeItem** — billing/charge data
- **Coverage** — insurance coverage data
- **FamilyMemberHistory** — family health history

Conversely, the B10 PDF lists **Location** and **Medication** as resources, which don't have dedicated tabs in apiR4.html. The B10 PDF was written for version 20.1 (October 2023) while the newer certification is version 25.1 (March 2025), suggesting the documentation is outdated and the actual export may differ from what's documented.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's documentation is a flat list of 21 standard FHIR R4 / US Core resources. There are no vendor-defined categories, no product-specific groupings, and no indication of depth within each resource. The resources listed are precisely the US Core resource set — the standard clinical data exchange surface.

The vendor makes no claim about export breadth beyond these 21 resources, except the vague "all the other resources are currently exported using the standard JSON format" statement. The vendor does not identify which product modules or data domains map to the export.

The (g)(10) API documentation adds ChargeItem and Coverage, suggesting the FHIR API surface includes some financial data, but these are not mentioned in the (b)(10) documentation.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | `Patient`, `RelatedPerson` in B10; no field-level detail | Product does registration/demographics; coverage at resource level only, no custom fields documented |
| Encounters / visits | ⚠️ Partial | `Encounter` in B10; `Appointment` in API only | Resource listed but no field-level detail; Appointment not in B10 docs |
| Problems / conditions | ⚠️ Partial | `Condition` in B10 | Resource listed, no field detail |
| Medications / prescriptions | ⚠️ Partial | `Medication`, `MedicationRequest` in B10 | Basic prescription data; no MAR, no EPCS-specific fields documented |
| Allergies | ⚠️ Partial | `AllergyIntolerance` in B10 | Resource listed, no field detail |
| Immunizations | ⚠️ Partial | `Immunization` in B10 | Resource listed, no field detail |
| Vitals | ⚠️ Partial | `Observation` in B10 (covers vitals per US Core) | No specificity about vital sign profiles or custom measurements |
| Lab results | ⚠️ Partial | `Observation`, `DiagnosticReport` in B10 | Standard lab results may be covered; LIS-specific data (specimen tracking, barcodes, device connectivity) not documented |
| Imaging / diagnostic reports | ⚠️ Partial | `DiagnosticReport` in B10 | Resource listed, no field detail |
| Procedures | ⚠️ Partial | `Procedure` in B10 | Resource listed, no field detail |
| Clinical notes / documents | ⚠️ Partial | `DocumentReference` in B10 | Resource listed; unclear which note types or documents are included |
| Care plans / goals | ⚠️ Partial | `CarePlan`, `Goal`, `CareTeam` in B10 | Resources listed, no field detail |
| Orders / referrals | ⚠️ Partial | `ServiceRequest` in B10 | Resource listed, no field detail |
| Insurance / coverage | ❌ Not covered | Not in B10 PDF; `Coverage` in apiR4.html only | Product has insurance verification; Coverage in (g)(10) API but NOT documented for (b)(10) export — significant gap |
| Claims / billing | ❌ Not covered | Not in B10 PDF; `ChargeItem` in apiR4.html only | Product has full billing/claims/revenue cycle module; no Claim, ClaimResponse, ExplanationOfBenefit anywhere; ChargeItem only in (g)(10) API — **major gap** |
| Payments | ❌ Not covered | No payment-related resources documented | Product processes payments via portal and billing module — gap |
| Consents / directives | ❌ Not covered | No Consent resource documented | No evidence of consent data in export |
| Patient communications / portal messages | ❌ Not covered | No Communication resource documented | Product has patient portal with secure messaging — gap |
| Specialty-specific (oncology, neurology, mental health) | ❌ Not covered | No specialty-specific resources or extensions documented | Product serves oncology, neurology, mental health; no specialty assessments or data structures in export — gap |
| Family health history | ❌ Not covered | Not in B10 PDF; `FamilyMemberHistory` in apiR4.html only | In API but not B10 documentation |
| Pharmacy management | ❌ Not covered | No pharmacy-specific resources | Product has full pharmacy management module (inventory, procurement, sales) — **major gap** |
| E-prescribing details | ❌ Not covered | `MedicationRequest` covers basic prescriptions only | EPCS records, controlled substance details, transmission logs not documented — gap |
| Telehealth | ❌ Not covered | No telehealth-specific resources | Product has telehealth module — gap |

## 6. Documentation Quality

The documentation quality is **poor**:

- **No data dictionary**: Zero field-level definitions exist. The 21 resource descriptions are verbatim copies from the FHIR R4 specification — they describe generic FHIR, not how Agastha maps its data to FHIR elements.
- **No schemas or profiles**: No JSON Schema, no FHIR StructureDefinitions, no custom profiles, no CapabilityStatement for the export.
- **No sample data**: No example export files, no sample JSON structures showing what the actual output looks like.
- **No mapping documentation**: No description of how internal Agastha data maps to FHIR resources and elements.
- **No documentation of "other resources"**: The PDF claims additional data is exported in "standard JSON format" but provides absolutely no documentation of what that data is.
- **Outdated**: The B10 PDF is version 20.1 (October 2023) but the current certification is version 25.1 (March 2025). The documentation has not been updated in over 2 years.
- **Helpful UI screenshots**: The export interface screenshots showing single/group/population export options with date filters are useful for end users finding the feature.
- **Version mismatch with API docs**: The apiR4.html documents 4 resources not in the B10 PDF (Appointment, ChargeItem, Coverage, FamilyMemberHistory), suggesting the documentation is out of sync.

A developer receiving this export would know the 21 FHIR resources conform to US Core R4 and could use standard FHIR tooling. However, they would have no guidance on Agastha-specific mappings, extensions, or the undocumented "other resources" in "standard JSON format."

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation lists exactly the US Core / USCDI resource set — the regulatory floor for clinical exchange. The product stores substantial data beyond this: billing/claims/revenue cycle, pharmacy management (inventory, procurement, sales), laboratory management (specimen tracking, barcodes), patient portal communications, telehealth records, e-prescribing details, and specialty-specific clinical assessments for oncology, neurology, and mental health. None of these domains appear in the documented export.

The "all other resources exported in standard JSON format" claim *might* mean the export is broader than documented, but without any documentation of what those resources are, this cannot be verified. The documentation itself covers only USCDI-scope clinical data.

**Axis 2 — Export approach: Repackaged existing export**

The 21 FHIR resources listed in the B10 PDF are precisely the US Core resource set. The documentation references FHIR R4, US Core IG STU V3.1.1, and HL7 FHIR Bulk Data — all (g)(10) standards. The resource descriptions are copied verbatim from the FHIR specification with no product-specific mappings. The (g)(10) API documentation (`apiR4.html`) documents essentially the same resources (plus 4 more). The export UI appears to be a "Data Portability/Export" wrapper around the existing FHIR Bulk Data capability.

The telltale signs are clear: standard FHIR resources, standard specs referenced, generic descriptions, no product-specific data dictionary, no billing/operational data, and the API docs overlap almost entirely with the B10 resource list. This is a (g)(10) FHIR API repackaged as (b)(10).

### Key Findings

1. **Repackaged (g)(10) FHIR export**: The 21 FHIR resources listed are the standard US Core / USCDI set. The resource descriptions are copied from the FHIR spec. The (g)(10) API (`apiR4.html`) documents essentially the same resources. No evidence of a purpose-built EHI export.

2. **Zero field-level documentation**: No data dictionary exists anywhere in the provided artifacts. Only resource-level names and generic FHIR descriptions are provided. A third party cannot understand what specific data elements are exported.

3. **Major domains missing**: Despite the product having billing/claims, pharmacy management, LIS, patient portal, telehealth, and specialty clinical modules, none of these domains appear in the (b)(10) export documentation. This represents a significant gap between what the product stores and what the export documents.

4. **Unsubstantiated "other resources" claim**: The PDF states "All the other resources are currently exported using the standard JSON format" but provides absolutely no documentation of what those resources are. This is either an undocumented broader export or a misleading statement.

5. **Outdated documentation**: The B10 PDF is from October 2023 (v20.1) while the current certification is v25.1 (March 2025). The apiR4.html documents 4 resources not in the B10 PDF, suggesting the documentation hasn't kept pace with the product.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Repackaged existing export
Export format:   FHIR R4 JSON + unspecified "standard JSON"
Entities:        21 (documented in B10 PDF); 25 across all docs
Fields:          N/A (no field-level documentation)
Descriptions:    0% (resource descriptions are generic FHIR spec copies)
Sample data:     No
Bulk export:     Yes (single, group, population)
Domains covered: ~8 of 19 applicable domains (all partial — USCDI clinical only)
```

### Bottom Line

A patient or provider requesting their data from Agastha would receive a standard FHIR clinical summary — the same data available via the (g)(10) API — covering basic clinical domains (problems, meds, labs, vitals, notes). They would **not** receive their billing records, pharmacy data, secure messages, specialty-specific assessments, or any of the substantial non-clinical data the product stores. The single biggest gap is the complete absence of documented billing/claims export from a product that has a full revenue cycle management module. The documentation is a 7-page PDF with no data dictionary, making this one of the thinnest (b)(10) documentation packages possible.
