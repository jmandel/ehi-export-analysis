# EHI Export Analysis: InPracSys

**Product**: InPracSys EHR  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.05.05.2762.INPS.01.00.1.191206 (CHPL #10194)

## 1. Product Context

InPracSys EHR is a cloud-based, urology-specialty EHR built by Innovative Practice Systems, Inc. (Minneapolis, MN). Founded in 2003 by Dr. Ashu Kataria, the company has ~25 employees and serves a very small customer base (possibly single-digit clinics). The product is certified across 35 ONC criteria including (b)(10).

**Key capabilities relevant to EHI scope:**

- **Clinical charting**: Point-and-click "FastCharting" system with urology-specific templates covering HPI, ROS, exam, assessment/plan, E/M coding. Full encounter documentation in under 30 seconds (per vendor claims).
- **CPOE**: Medication, lab, and diagnostic imaging orders (certified (a)(1)–(a)(3)).
- **Medications & e-prescribing**: Via SureScripts/DoseSpot integration (certified (a)(10), (b)(3)).
- **Clinical data**: Problems, allergies, vitals, immunizations, implantable devices, family history, smoking status, social determinants.
- **Lab results**: Inbound lab interfaces with results.
- **Billing**: Superbill generation, Level 1 coding, professional component anatomical pathology billing. Claims a 99% clean claim rate. Unclear if this is full practice management or supplementary billing.
- **Care Pathways / PRACTICE iQ**: Stepped therapy programs, pre-authorization, drug program qualifications. Described as generating $2,500–$7,500/patient/year.
- **Risk Management**: Urology-specific CDS alerts (stent tracking, missed ultrasounds). Related to separate RiskAssistMD company.
- **Patient Portal**: Records access, messaging, appointments.
- **Clinical notes**: Full encounter documentation (the product's primary differentiator).
- **Urology-specific data**: Urine analysis, bladder scans, TRUS results, cystoscopy workflows.
- **Care coordination**: C-CDA, direct messaging, referrals (certified (b)(1)–(b)(3), (h)(1)).
- **Quality measures**: CQMs/PQRS (certified (c)(1)).

This is a full-featured ambulatory EHR with billing, specialty clinical data, patient portal, and care pathway management. The EHI export should cover all these domains.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `Disclosure-EHR-Inpracsys_NewV6.1.pdf` (192 KB, 3 pages) | Mandatory disclosure letter. Page 3 contains the (b)(10) statement: export produces ZIP files with XML files, links to FHIR page for format details. | **Medium** — confirms export exists, format claim (XML/ZIP), but no data dictionary |
| `fhir-api-documentation-page.html` (691 KB) | FHIR API documentation page linked as "EHI export format." Documents 15 FHIR resource types with field definitions, cardinality, types, and sample JSON. | **Most informative** — primary data dictionary equivalent |
| `FhirServiceBaseBundleV10.json` (4 KB) | FHIR Bundle with Endpoint + 2 Organization resources. Endpoint points to `sfp-proxy23604.azurewebsites.net/fhir`. | **Low** — infrastructure metadata only |
| `screenshot-disclosure-page.png` (259 KB) | Screenshot of disclosure page with embedded PDF viewer. | **Low** — visual confirmation only |
| `screenshot-disclosure-bottom.png` (191 KB) | Screenshot showing download links: "EHI export format" → /fhir, "Service URL Bundle" → JSON file. | **Low** — confirms link structure |
| `screenshot-fhir-page.png` (305 KB) | Screenshot of FHIR API documentation page showing nav and intro. | **Low** — visual confirmation only |

**No sample export data, no machine-readable schemas, no export procedure documentation were provided.**

## 3. Export Mechanics

- **Format**: The disclosure PDF states exports are "downloaded as a zip file containing .xml file(s)." However, the linked "EHI export format" page documents a FHIR JSON REST API, not XML files. This is a contradiction that the documentation does not resolve.
- **Mechanism**: The FHIR API is queried via REST endpoints with OAuth 2 Bearer token authentication. Individual resource types are retrieved per-patient using `?pid=` parameters. It is unclear whether the ZIP/XML export is a separate mechanism or a packaging of the API output.
- **Single-patient vs bulk**: The disclosure states the export supports "a single patient as well as for the patient population." The FHIR API documentation only shows single-patient queries.
- **Access constraints**: OAuth 2 authentication required. No mention of fees specifically for the (b)(10) export.
- **FHIR API base URL**: `fhirips.azurehealthcareapis.com` (Azure Health Data Services). A separate proxy at `sfp-proxy23604.azurewebsites.net/fhir` is referenced in the service bundle.
- **Non-standard serialization**: Sample JSON outputs use C#-style property names (`ValueElement`, `SystemElement`, `CodeElement`, `DisplayElement`, `StatusElement`) rather than standard FHIR JSON. This appears to be a .NET FHIR library's internal object model serialized directly.

## 4. Export Content: What's In It

The FHIR API documentation page is the sole source of information about what the export contains. It documents **15 FHIR resource types** with **328 total fields** across those resources.

- **Fields with descriptions**: 325 of 328 (99.1%)
- **Fields with types**: 301 of 328 (91.8%)
- **Value sets referenced**: Some fields link to standard FHIR/Argonaut value sets by URL, but the actual codes used by InPracSys are not enumerated
- **Relationships**: Only implicit patient references; no explicit foreign key documentation
- **Sample data**: JSON examples embedded in the HTML for each resource type, but these use non-standard serialization

### Vendor's own content organization

The documentation organizes content by FHIR resource type. Each section includes an endpoint URL, request parameters, response field table, and sample JSON.

| Entity/Resource | Fields | Described | Types | USCDI Data Class |
|---|---|---|---|---|
| Patient | 20 | 19 | yes | Patient Demographics |
| Observation (Smoking Status) | 13 | 13 | yes | Health Status Assessments |
| Condition | 31 | 31 | yes | Problems |
| MedicationStatement | 31 | 29 | yes | Medications |
| AllergyIntolerance | 23 | 23 | yes | Allergies & Intolerances |
| DiagnosticReport (Lab Orders) | 7 | 7 | yes | Laboratory |
| Observation (Lab Results) | 22 | 22 | yes | Laboratory |
| Observation (Vital Signs) | 33 | 33 | yes | Vital Signs |
| Procedure | 29 | 29 | yes | Procedures |
| CareTeam | 8 | 8 | yes | Care Team Members |
| Immunization | 36 | 36 | yes | Immunizations |
| Device | 18 | 18 | yes | Medical Devices |
| CarePlan | 7 | 7 | yes | Assessment & Plan of Treatment |
| Goal | 20 | 20 | yes | Goals & Preferences |
| Condition (Health Concerns) | 30 | 30 | yes | Health Status Assessments |
| **Total** | **328** | **325** | | |

Full inventory: `analysis/entity-inventory-full.json`  
Summary statistics: `analysis/entity-inventory-summary.json`

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export covers exactly the USCDI clinical data classes — and nothing else. The 15 documented resource types map cleanly to 10 USCDI data classes:

- **Patient Demographics** (1 entity, 20 fields)
- **Problems** (1 entity, 31 fields)
- **Medications** (1 entity, 31 fields)
- **Allergies & Intolerances** (1 entity, 23 fields)
- **Laboratory** (2 entities, 29 fields — lab orders + results)
- **Vital Signs** (1 entity, 33 fields)
- **Procedures** (1 entity, 29 fields)
- **Care Team Members** (1 entity, 8 fields)
- **Immunizations** (1 entity, 36 fields)
- **Medical Devices** (1 entity, 18 fields)
- **Assessment & Plan of Treatment** (1 entity, 7 fields)
- **Goals & Preferences** (1 entity, 20 fields)
- **Health Status Assessments** (2 entities, 43 fields — smoking status + health concerns)

This is precisely the USCDI / US Core surface. There is no evidence of any data beyond what a standard (g)(10) FHIR API would expose. The resource types, field sets, and overall structure are indistinguishable from a basic US Core implementation.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | Patient (20 fields) | Standard USCDI demographics |
| Encounters / visits | ❌ Not covered | No Encounter resource documented | Product does encounter documentation (FastCharting); significant gap |
| Problems / conditions | ✅ Covered | Condition (31 fields), Health Concerns (30 fields) | Standard USCDI coverage |
| Medications / prescriptions | ✅ Covered | MedicationStatement (31 fields) | Standard USCDI; no e-prescribing history or DoseSpot data |
| Allergies | ✅ Covered | AllergyIntolerance (23 fields) | Standard USCDI coverage |
| Immunizations | ✅ Covered | Immunization (36 fields) | Standard USCDI coverage |
| Vitals | ✅ Covered | Observation/Vitals (33 fields) | Standard USCDI coverage |
| Lab results | ✅ Covered | DiagnosticReport (7 fields), Observation/Labs (22 fields) | Standard USCDI coverage |
| Imaging / diagnostic reports | ❌ Not covered | No imaging resources documented | Product has CPOE for diagnostic imaging (certified (a)(3)); gap |
| Procedures | ✅ Covered | Procedure (29 fields) | Standard USCDI coverage |
| Clinical notes / documents | ❌ Not covered | No DocumentReference or clinical note resources | FastCharting encounter notes are the product's primary differentiator; **major gap** |
| Care plans / goals | ✅ Covered | CarePlan (7 fields), Goal (20 fields) | Standard USCDI; CarePlan is thin (7 fields) |
| Orders / referrals | ❌ Not covered | No ServiceRequest or referral resources | Product has CPOE and is certified for referrals (b)(3); gap |
| Insurance / coverage | ❌ Not covered | No Coverage or insurance resources | Product handles insurance for billing; gap |
| Claims / billing | ❌ Not covered | No billing, superbill, or claims resources | Product has billing module with superbill generation, E/M coding, claims; **major gap** |
| Payments | ❌ Not covered | No payment resources | If product processes payments (unclear); potential gap |
| Consents / directives | ❌ Not covered | No consent resources | N/A — unclear if product stores these |
| Patient communications / portal messages | ❌ Not covered | No communication resources | Product has patient portal with messaging; gap |
| Family health history | ❌ Not covered | No FamilyMemberHistory resource | Certified (a)(12); gap |
| Social determinants | ❌ Not covered | No SDOH resources beyond health concerns | Certified (a)(15); gap |
| Specialty-specific (urology) | ❌ Not covered | No urology-specific data (urine analysis, bladder scans, TRUS, cystoscopy) | Product is built specifically for urology; **major gap** |
| Care Pathways / stepped therapy | ❌ Not covered | No care pathway or pre-authorization resources | PRACTICE iQ is a key feature; gap |

**Summary**: 10 of 21 applicable domains covered, 11 not covered. All covered domains are standard USCDI clinical data. All non-USCDI domains are absent.

## 6. Documentation Quality

**Strengths:**
- Each of the 15 resource types has a structured field table with name, cardinality, type, and description
- 99.1% of fields (325/328) have descriptions
- Sample JSON output is provided for each resource type
- The page is clearly organized with left-nav navigation

**Weaknesses:**
- **No data dictionary for the actual export format** — if the export truly produces XML in a ZIP (as the disclosure PDF claims), there is no documentation of that XML schema
- **Contradiction between PDF and documentation page**: PDF says XML/ZIP, documentation page shows JSON API responses
- **Non-standard FHIR serialization**: Sample JSON uses `ValueElement`, `SystemElement` etc. — a developer expecting standard FHIR JSON would fail to parse this
- **No machine-readable schema files** (no XSD, JSON Schema, OpenAPI, CapabilityStatement)
- **No sample export files** — no downloadable ZIP or example data
- **No export procedure documentation** — no user guide explaining how to trigger the export
- **Stale references**: Value set URLs point to DSTU2/Argonaut-era specifications despite claiming FHIR R4
- **No relationship documentation**: How entities link to each other is implicit only
- **No vendor-specific value sets**: Coded fields reference standard URLs but don't enumerate InPracSys's actual code values

A developer could understand the field structure for the 15 documented resource types, but could not build a reliable import without trial-and-error due to the non-standard serialization and missing schema artifacts.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The export covers only USCDI-scope clinical data — 10 of 21 applicable domains. The 11 missing domains include the product's most distinctive capabilities: urology-specific clinical data (the entire reason this product exists), encounter notes/FastCharting documentation, billing/superbills, care pathway management (PRACTICE iQ), and patient portal communications. The export is clearly a clinical summary, not a designated record set export. For a urology-specialty EHR, omitting all urology-specific data is a particularly stark gap.

**Axis 2 — Export approach: Repackaged existing export**

This is a textbook case. The disclosure page links directly to the FHIR API documentation page as the "EHI export format." The 15 documented resource types map exactly to standard USCDI/US Core data classes. There are no vendor-specific extensions, no billing resources, no specialty data, no custom forms — nothing beyond what the (g)(10) FHIR API would already expose. The documentation references Argonaut/DSTU2-era specifications and DAF profiles, suggesting this API predates the (b)(10) requirement and was simply relabeled. The vendor did not build a purpose-specific EHI export; they pointed at their existing FHIR API and called it (b)(10).

### Key Findings

1. **Classic (g)(10)→(b)(10) relabeling**: The export documentation is the vendor's FHIR API documentation page. The 15 resource types are exactly the standard US Core/USCDI set. No product-specific data dictionary exists beyond this API documentation.

2. **All urology-specific data is absent**: InPracSys EHR is "built by urologists, for urologists" — yet the export contains no urology-specific clinical data (urine analysis, bladder scans, TRUS, cystoscopy, stent tracking). The product's entire specialty identity is missing from the export.

3. **Clinical notes are missing**: The FastCharting module is the product's primary clinical differentiator, but no DocumentReference or clinical note resource is documented in the export. Encounter notes — the core clinical record — are not exported.

4. **Billing data is missing**: The product generates superbills, E/M codes, and claims (citing a 99% clean claim rate), but no billing entities appear in the export.

5. **Format contradiction**: The disclosure PDF says "zip file containing .xml file(s)" but the linked documentation page describes a FHIR JSON REST API with non-standard serialization. It is unclear what the actual export format is.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Repackaged existing export
Export format:   FHIR JSON (non-standard serialization) — possibly XML/ZIP per disclosure PDF
Entities:        15
Fields:          328
Descriptions:    99.1% of fields
Sample data:     No (inline JSON examples only, non-standard format)
Bulk export:     Unclear (PDF claims population-level, API docs show single-patient only)
Domains covered: 10 of 21 applicable domains
```

### Bottom Line

InPracSys has relabeled its (g)(10) FHIR API as its (b)(10) EHI export, covering only standard USCDI clinical data classes. A patient or provider would not get a complete copy of their data: all urology-specific clinical data, encounter notes, billing records, care pathway information, and patient communications are missing. The single biggest gap is the complete absence of the specialty clinical data that defines this product — a urology EHR that exports no urology data.
