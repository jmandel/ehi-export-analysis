# EHI Export Analysis: ezCaretech Co., Ltd.

**Product**: BESTCare 2.0B  
**Analysis date**: 2026-02-16  
**CHPL ID**: 15.04.04.2610.BEST.02.00.1.180423

## 1. Product Context

BESTCare is a comprehensive hospital information system (HIS) developed by ezCaretech Co., Ltd., a South Korean healthcare IT company. Originally co-developed with Seoul National University Bundang Hospital (SNUBH), BESTCare is designed for large tertiary/university hospitals and covers clinical, administrative, and operational functions across the entire hospital.

The product's US deployment is primarily at Aurora Behavioral Healthcare (14 psychiatric hospitals), where a behavioral health variant is used. The FHIR server's capability statement (`fhir-capability-statement.json`) confirms this, naming itself `ezfhirstation-us-core-usa-aurora`.

**Relevant to export completeness**, BESTCare stores:
- **Clinical data**: EMR documentation (3,000+ templates), CPOE orders (medications, labs, imaging, procedures), medication administration records (closed-loop with barcode/RFID), lab results, radiology, vitals, allergies, immunizations, clinical decision support alerts, clinical pathways
- **Administrative data**: Billing and financial records, patient registration/scheduling, inpatient census/bed management, social services records, CRM data
- **Specialty data**: Behavioral health-specific workflows and documentation (for Aurora deployment)
- **Integration data**: Transitions of care documents, HIE exchange records, FHIR API resources

This is a comprehensive HIS with billing, pharmacy, nursing, radiology, and administrative modules — all of which generate patient-level data that should be included in a (b)(10) EHI export.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `b.10_EHI_Export.pdf` (1 page, 25KB) | Primary (b)(10) documentation. Describes CSV and Oracle DMP export formats. **Contains zero field-level documentation** — no data dictionary, no schema, no sample data. | **Most important** — this is the vendor's entire (b)(10) documentation |
| `BESTCare2.0B_Certified_Health_IT_v3.0.pdf` (3 pages, 139KB) | Certified Health IT summary listing 33 certified criteria and 13 CQMs. No technical detail about EHI export. | Low — confirms certification only |
| `fhir-capability-statement.json` (33KB) | FHIR R4 CapabilityStatement from ezFHIRStation. 26 resource types, standard US Core set. | Moderate — documents the (g)(10) API that the (b)(10) PDF links to |
| `single-patient-api.html` (1.8MB) | Single Patient API documentation. US Core profiles with must-have/must-support fields for 22 profiles. | Moderate — documents (g)(10) API fields, not (b)(10)-specific content |
| `multi-patient-api.html` (87KB) | Multi Patient (Bulk Data) API documentation for FHIR $export. Standard Bulk Data spec. | Low — standard (g)(10) Bulk Data, linked from (b)(10) PDF |
| `base-urls.html` (42KB) | Service base URLs for FHIR endpoints. | Low — infrastructure only |
| Screenshots (3 files, ~700KB total) | Screenshots of the ONC disclosures page, single-patient API, and multi-patient API. | Low — visual confirmation of other artifacts |

## 3. Export Mechanics

The (b)(10) PDF (`b.10_EHI_Export.pdf`) describes two export capabilities:

1. **Single Patient Export**: Users can export EHI for a single patient "at any time without developer assistance" in CSV or Oracle DMP formats.
2. **Multi-Patient Export**: The system "can export all the data for a patient population" in the same formats.
3. **Formats**:
   - **CSV**: Standard comma-separated values files. No schema or field documentation provided.
   - **Oracle DMP**: Binary Oracle database dump file. No documentation of what tables or fields are included.
4. **API**: The PDF contains a "Click Here" link to the FHIR API portal, which is the standard (g)(10) FHIR Bulk Data API documentation.

**Access mechanism**: Unclear from documentation. The PDF implies a UI-based export but provides no screenshots, workflow descriptions, or instructions.

**Fees/constraints**: Not documented.

**Critical gap**: The PDF mentions CSV and Oracle DMP formats but provides **absolutely no documentation** about what data is included in these exports — no table names, no field names, no record types, no schema, no sample data. The only structured documentation linked is the standard FHIR (g)(10) API.

## 4. Export Content: What's In It

### What the (b)(10) documentation describes

The 1-page PDF describes two export formats (CSV and Oracle DMP) but provides **zero** detail about what data is exported. The entire substantive content of the PDF is:

> "BESTCare2.0B allows a user to export electronic health information (EHI) for a single patient at any time without developer assistance using the following standardized file formats..."

There is no data dictionary, no schema, no field listing, no table listing, no sample data, and no description of what clinical or administrative domains are covered by the CSV or Oracle DMP exports.

### What the linked FHIR API documentation describes

The PDF links to the ezFHIRStation FHIR portal, which documents a standard US Core (g)(10) API with 26 resource types and 22 US Core profiles. This is the vendor's clinical exchange API, not a purpose-built (b)(10) export.

### Vendor's own content organization

Since there is no data dictionary, the only structured content available is from the FHIR CapabilityStatement:

| Resource Type | Fields Documented | Category |
|---|---|---|
| AllergyIntolerance | 5 | US Core / USCDI |
| CarePlan | 6 | US Core / USCDI |
| CareTeam | 8 | US Core / USCDI |
| Condition | 5 | US Core / USCDI |
| Device | 12 | US Core / USCDI |
| DiagnosticReport | 9 | US Core / USCDI |
| DocumentReference | 10 | US Core / USCDI |
| Encounter | 10 | US Core / USCDI |
| Goal | 4 | US Core / USCDI |
| Immunization | 5 | US Core / USCDI |
| Location | 6 | US Core / USCDI |
| Medication | 2 | US Core / USCDI |
| MedicationRequest | 11 | US Core / USCDI |
| Observation | 3 | US Core / USCDI |
| Organization | 6 | US Core / USCDI |
| Patient | 10 | US Core / USCDI |
| Practitioner | 3 | US Core / USCDI |
| Procedure | 5 | US Core / USCDI |
| Provenance | 5 | US Core / USCDI |
| Binary | 0 | Infrastructure |
| CodeSystem | 0 | Infrastructure |
| Endpoint | 0 | Infrastructure |
| Group | 0 | Infrastructure |
| OperationDefinition | 0 | Infrastructure |
| PractitionerRole | 0 | Infrastructure |
| ValueSet | 0 | Infrastructure |

**Total**: 26 resource types, 125 fields documented (all standard US Core must-have/must-support elements). No vendor-specific extensions, no product-specific mapping beyond standard profiles.

The complete entity inventory is in `analysis/entity-inventory-full.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's (b)(10) documentation is effectively **undocumented**. The 1-page PDF mentions CSV and Oracle DMP formats but provides no detail about content.

The only structured documentation is the FHIR (g)(10) API, which covers standard US Core resources — the exact same set required for clinical data exchange under (g)(10). There are no vendor-specific extensions, no additional FHIR resources beyond US Core, and no mapping documentation that would suggest the FHIR API has been extended for (b)(10) purposes.

The CSV and Oracle DMP formats mentioned in the PDF could theoretically contain comprehensive data from BESTCare's internal Oracle database, but **there is no documentation to verify this claim**. The vendor provides no schema, field listing, sample data, or any other evidence of what these exports contain.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | FHIR Patient resource (10 US Core fields) | Product stores extensive registration data; only USCDI-minimum fields documented |
| Encounters / visits | ⚠️ Partial | FHIR Encounter (10 fields) | Product supports inpatient, outpatient, and ED workflows; only standard FHIR fields documented |
| Problems / conditions | ⚠️ Partial | FHIR Condition (5 fields) | Standard US Core only |
| Medications / prescriptions | ⚠️ Partial | FHIR Medication + MedicationRequest (13 fields) | Product has closed-loop medication admin (CLMA) with barcode/RFID — MAR data not documented |
| Allergies | ⚠️ Partial | FHIR AllergyIntolerance (5 fields) | Standard US Core only |
| Immunizations | ⚠️ Partial | FHIR Immunization (5 fields) | Standard US Core only |
| Vitals | ⚠️ Partial | FHIR Observation (3 fields) | Standard US Core vital signs profiles |
| Lab results | ⚠️ Partial | FHIR DiagnosticReport + Observation | Standard US Core laboratory profiles |
| Imaging / diagnostic reports | ⚠️ Partial | FHIR DiagnosticReport (9 fields) | Product has radiology module; only standard FHIR profiles documented |
| Procedures | ⚠️ Partial | FHIR Procedure (5 fields) | Standard US Core only |
| Clinical notes / documents | ⚠️ Partial | FHIR DocumentReference (10 fields) | Product has 3,000+ templates; only standard DocumentReference documented |
| Care plans / goals | ⚠️ Partial | FHIR CarePlan + Goal (10 fields) | Standard US Core only |
| Orders / referrals | ❌ Not covered | No ServiceRequest in FHIR API; CPOE orders not documented | Product has full CPOE — significant gap |
| Insurance / coverage | ❌ Not covered | No Coverage resource in FHIR API | Product handles insurance/billing — gap |
| Claims / billing | ❌ Not covered | No billing entities documented | Product has billing module — **significant gap** |
| Payments | ❌ Not covered | No payment entities documented | Product handles billing — gap |
| Consents / directives | ❌ Not covered | No consent entities documented | Product supports electronic consent (iPad/PC signatures) — gap |
| Patient communications | ❌ Not covered | No communication entities documented | Unknown if product has patient portal |
| Specialty-specific (behavioral health) | ❌ Not covered | No behavioral health-specific entities | US deployment is specifically for psychiatric hospitals — **major gap** |
| Social services | ❌ Not covered | No social services entities documented | Product has social services module — gap |
| Medication administration records | ❌ Not covered | No MedicationAdministration resource | Product has closed-loop medication admin — gap |
| Clinical decision support alerts | ❌ Not covered | No CDS alert data documented | Product has CDSS module — gap |
| Clinical pathways | ❌ Not covered | No pathway data documented | Product supports 104+ clinical pathways — gap |

## 6. Documentation Quality

The (b)(10) export documentation is **extremely poor**:

- **No data dictionary**: There is no listing of tables, fields, data types, relationships, value sets, or any structural description of the export content.
- **No sample data**: No example CSV files, no sample Oracle DMP contents, no sample FHIR responses beyond standard spec examples.
- **No machine-readable schema**: No JSON schema, no XSD, no DDL, no CSV headers.
- **No export instructions**: No screenshots, no workflow description, no step-by-step guide for performing the export.
- **Entire documentation is 1 page**: The PDF is a single A4 page with ~100 words of substantive content. It defines what CSV and Oracle DMP formats are in generic terms (not specific to BESTCare), then links to the standard FHIR API.

A developer could not build an import from this documentation. A patient or provider receiving an Oracle DMP file would have no way to interpret it without Oracle database tools and reverse-engineering effort. A patient receiving CSV files would have no schema to understand the fields.

The linked FHIR API documentation is standard US Core — adequate for FHIR developers but not specific to (b)(10) and containing no vendor-specific content.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The (b)(10) documentation is too thin to assess what the export actually contains. The 1-page PDF mentions CSV and Oracle DMP formats but provides zero detail about content. It is possible that the Oracle DMP contains a comprehensive database dump, but there is absolutely no documentation to verify this. The only documented content is the standard FHIR (g)(10) API with 26 US Core resource types and 125 standard fields — this is the USCDI floor, covering perhaps 20% of what BESTCare stores. Critical domains that BESTCare is known to handle (billing, behavioral health-specific data, medication administration records, CPOE orders, clinical pathways, social services) have no documented presence in any export.

**Axis 2 — Export approach: Unclear/undetermined**

The vendor describes two potentially distinct export mechanisms: (1) CSV and Oracle DMP exports, which *could* be purpose-built database extracts but are entirely undocumented, and (2) the FHIR API, which is clearly the repackaged (g)(10) clinical exchange. The Oracle DMP format suggests a database-level export, which is a signal of purpose-built (b)(10) — but without any schema documentation, field listing, or sample data, it's impossible to confirm whether this is a comprehensive EHI export or a selective dump. The documentation fails to make this determination possible.

### Key Findings

1. **The entire (b)(10) documentation is a 1-page PDF with ~100 words of substance** (`b.10_EHI_Export.pdf`). It describes CSV and Oracle DMP formats generically, with no product-specific data dictionary, schema, or field documentation whatsoever.

2. **The FHIR API linked from the (b)(10) PDF is the standard (g)(10) US Core API**, covering 26 resource types and 125 standard fields. The server name (`ezfhirstation-us-core-usa-aurora`) confirms this is the clinical exchange API, not a (b)(10)-specific extension.

3. **No evidence of billing, behavioral health, or operational data in any export**. BESTCare's billing module, behavioral health workflows (critical for the Aurora deployment), medication administration records, CPOE order details, clinical pathways, and social services records are entirely absent from all documentation.

4. **The Oracle DMP format is a potentially positive signal that remains unsubstantiated**. A binary Oracle dump could contain comprehensive EHI, but without any documentation of what tables/fields are included, this cannot be verified. A patient receiving a .DMP file would need Oracle database tools to read it.

5. **No sample data exists**. There are no example exports, no sample CSV files, no demonstration of what a patient would actually receive.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Unclear/undetermined
Export format:   CSV, Oracle DMP, FHIR R4 (linked)
Entities:        26 (FHIR resources only — no native data dictionary)
Fields:          125 (US Core must-have/must-support only)
Descriptions:    0% (no product-specific field descriptions)
Sample data:     No
Bulk export:     Yes (multi-patient mentioned in PDF)
Domains covered: ~9 of 19 applicable domains (all partial, via standard FHIR only)
```

### Bottom Line

BESTCare's (b)(10) documentation is among the thinnest possible — a single page stating that CSV and Oracle DMP exports exist, with no data dictionary, no schema, and no evidence of what data is actually exported. The linked FHIR API is the standard (g)(10) clinical exchange covering USCDI only. For a comprehensive HIS with billing, behavioral health, pharmacy, and administrative modules, the documented export coverage is negligible. The biggest gap is the complete absence of documentation — it is impossible for a patient, provider, or developer to determine what they would receive from this export without actually performing one.
