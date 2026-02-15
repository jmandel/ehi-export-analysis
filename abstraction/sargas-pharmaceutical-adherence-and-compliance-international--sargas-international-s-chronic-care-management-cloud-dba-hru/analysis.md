# EHI Export Analysis: Sargas Pharmaceutical Adherence and Compliance International

**Product**: Sargas International's Chronic Care Management Cloud dba hru2day  
**Analysis date**: 2026-02-15  
**CHPL ID**: 15.05.05.2306.SPAC.01.00.0.211014 (internal ID 10702)

## 1. Product Context

Sargas International (SPAC International) is a small, niche vendor based in Bakersfield, CA, specializing in **chronic care management (CCM), remote patient monitoring (RPM), and medication therapy monitoring (MTM)**. The product — branded "hru2day" — is **not a full EHR** but a modular platform that supplements a practice's existing EHR with CCM/RPM/MTM-specific capabilities. It achieved ONC HIT **Modular** EHR certification (version 21.9, certified 2021-10-14).

The platform's core data includes:
- **Care plans**: comprehensive, addressing physical, mental, cognitive, psychosocial, functional, and environmental domains
- **Care coordination logs**: documenting 20+ minutes/month of CCM services (200,000+ interactions logged per the vendor's website)
- **RPM device data**: glucose, blood pressure, heart rate, oxygen saturation, weight from FDA-approved home monitoring devices
- **Medication adherence records**: the company's founding use case — tracking adherence, reminders, and side effects (originally for oncology patients)
- **Demographics, problem lists, medication lists, allergies**: standard clinical data
- **Billing-relevant time tracking**: linked to CPT codes for CCM (99490 etc.), PCM (99424–99427), and RPM
- **Patient consent records**, secure messages, referral and care transition records

The product operates a 24/7 clinical call center as part of its managed-service model — SPAC staff perform care management on behalf of contracting physician practices. The platform serves ~200 practices and ~20,000 patients.

For EHI export assessment, the key question is whether the export captures the **specialized data that differentiates this product** — care plans, care coordination logs, RPM telemetry, medication adherence tracking, and CCM time documentation — or only the clinical summary data (demographics, problems, medications, allergies) that any C-CDA would contain.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `SPAC-Export.pdf` (380 KB, 1 page) | The entire EHI export documentation. Six sentences stating the export is a ZIP containing C-CDA XMLs (per encounter) and PDF attachments. No data dictionary, no field-level detail, no sample data. | **Primary artifact** — but extremely thin |
| `screenshot-certification-page.png` (236 KB) | Screenshot of vendor's "Certified EHR Technology" page. Certification boilerplate and link to mandatory disclosures. | Not informative for EHI export assessment |

Only two artifacts were collected. The PDF is the sole source of information about the EHI export. No data dictionary, schema, sample data, or API documentation exists in any reviewed artifact.

## 3. Export Mechanics

- **Format**: ZIP file containing per-encounter C-CDA XML documents (in nested ZIP archives) and PDF files from the patient's chart
- **Standard**: C-CDA (Consolidated Clinical Document Architecture)
- **Mechanism**: Not documented. The PDF does not describe how to initiate an export — no UI instructions, no API endpoint, no description of who can perform it.
- **Single-patient vs bulk**: Not documented. The language ("the patient EHI export") implies single-patient.
- **Access constraints or fees**: Not documented in the export documentation. The mandatory disclosures page (per the screenshot) links to a separate document that may address pricing but was not collected as an artifact.

## 4. Export Content: What's In It

The documentation provides **no field-level or section-level detail** about what the export contains. The entire description is:

> "The patient EHI export contains data from the patient's chart. [...] The export file itself is a zip file. It contains zip files of C-CDAs and PDF files attached to the patient's chart (machine readable PDF). Information for each patient encounter is available C-CDA format in zip archive."

### What can be inferred

Since the export is stated to be C-CDA documents, the content is constrained by what C-CDA supports. Standard C-CDA sections would typically include:
- Demographics
- Problems / conditions
- Medications
- Allergies
- Encounters
- Procedures
- Results (if any)
- Care Plan (if populated)
- Vital signs (if populated)

However, **no documentation confirms which C-CDA sections are actually populated**, whether vendor extensions are used, or what level of detail is included. There is no sample C-CDA file to inspect.

The PDF attachments mentioned could contain any documents from the patient chart, but no inventory or description of what types of PDFs are included is provided.

### Vendor's own content organization

The vendor provides **no content organization**. There is no data dictionary, no entity listing, no table of fields, and no categorization of data domains. The sole claim is "data from the patient's chart" in C-CDA and PDF format.

| Entity/Table | Fields | Described | Types | Category (vendor's) |
|---|---|---|---|---|
| *None documented* | N/A | N/A | N/A | N/A |

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's documentation describes exactly **zero** data entities, fields, or sections. The only content claim is that the export contains "data from the patient's chart" in C-CDA format (per encounter) plus PDF attachments.

Since no data dictionary, sample data, or section-level documentation exists, it is impossible to verify what the export actually includes. The use of C-CDA as the export format imposes structural limitations: C-CDA is a clinical document standard designed for health information exchange of summary clinical data. It has well-defined sections for demographics, problems, medications, allergies, encounters, procedures, results, and vital signs — but **it is not designed to represent**:
- Care coordination activity logs
- RPM device time-series data
- Medication adherence tracking
- CCM/PCM/RPM service time documentation
- Call center interaction records

These are the core data types that differentiate hru2day from a standard clinical summary.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA standard section (if populated) — but no documentation confirms | Product stores demographics; C-CDA likely includes basic demographics but coverage unverifiable |
| Encounters / visits | ⚠️ Partial | C-CDA generated per encounter — but no section-level detail | Product logs encounters; C-CDA should reference encounters but completeness unknown |
| Problems / conditions | ⚠️ Partial | C-CDA standard section (if populated) | Core to CCM (chronic conditions); C-CDA likely includes problems but no confirmation |
| Medications / prescriptions | ⚠️ Partial | C-CDA standard section (if populated) | Product maintains medication lists; likely in C-CDA but unverifiable |
| Allergies | ⚠️ Partial | C-CDA standard section (if populated) | Product stores allergies; likely in C-CDA but unverifiable |
| Immunizations | N/A | No evidence | Product does not appear to store immunization data |
| Vitals | ⚠️ Partial | C-CDA vital signs section (if populated) | RPM device data (glucose, BP, HR, SpO2, weight) is core to this product; C-CDA vitals section cannot represent time-series device telemetry — **significant likely gap** |
| Lab results | ❌ Not covered | No evidence | Product is certified for CPOE for labs (a)(2), implying orders are placed, but no evidence lab results are stored or exported |
| Imaging / diagnostic reports | ❌ Not covered | No evidence | Product is certified for CPOE for imaging (a)(3), but no evidence imaging results are stored |
| Procedures | ⚠️ Partial | C-CDA standard section (if populated) | Unclear what procedures the product documents |
| Clinical notes / documents | ⚠️ Partial | PDF attachments from patient chart included in export | PDFs described but no detail on types or completeness |
| Care plans / goals | ⚠️ Partial | C-CDA has a Care Plan section | Care plans are the **core product capability** (comprehensive, multi-domain); C-CDA's Care Plan section is unlikely to capture the full structured richness — **significant likely gap** |
| Orders / referrals | ⚠️ Partial | No specific evidence | Product supports referrals and care transitions but no export documentation |
| Insurance / coverage | ❌ Not covered | No evidence | Product likely stores insurance info for CCM billing; C-CDA does not support this — **gap** |
| Claims / billing | ❌ Not covered | No evidence | Product tracks CCM/PCM/RPM service time linked to CPT codes; this is billing-relevant EHI with no C-CDA analog — **significant gap** |
| Payments | N/A | No evidence | Product does not appear to process payments directly |
| Consents / directives | ❌ Not covered | No evidence | Product requires patient consent for CCM enrollment; no evidence this is in the export — **gap** |
| Patient communications / portal messages | ❌ Not covered | No evidence | Product supports secure messaging and call center interactions (200,000+ logged); no C-CDA representation — **significant gap** |
| Specialty: Medication adherence tracking | ❌ Not covered | No evidence | This is the company's **founding specialty** (Drug Adherence® for oncology); adherence records, side effect reports, reminders — no C-CDA analog — **significant gap** |
| Specialty: RPM device telemetry | ❌ Not covered | No evidence | Time-series data from glucose monitors, BP cuffs, pulse oximeters, scales; C-CDA cannot represent this — **significant gap** |
| Specialty: Care coordination logs | ❌ Not covered | No evidence | Logs documenting 20+ min/month of CCM services; core to product purpose and billing justification; no C-CDA analog — **significant gap** |

All "⚠️ Partial" ratings reflect that C-CDA *could* contain these sections but no documentation confirms they are populated. Without sample data or a section-level description, these cannot be upgraded to "✅ Covered."

## 6. Documentation Quality

The export documentation is **critically deficient**:

- **Data dictionary**: None
- **Field definitions**: None
- **C-CDA section listing**: None — not even which standard C-CDA sections are populated
- **Sample data**: None
- **Machine-readable schema**: None
- **Export instructions**: None — no description of how to initiate, who can request, what parameters exist
- **PDF organization**: None — no description of what types of PDFs are included or how they're structured in the ZIP

A developer given this document could not build an import. They would know only: "it's a ZIP with C-CDAs and PDFs inside." They could parse C-CDA XML generically, but would have no vendor-specific guidance on what to expect, what sections are populated, what extensions might be used, or what the PDFs contain.

The documentation consists of 6 sentences on a single page, 3 of which are definitions of commonly known file formats (ZIP, PDF, C-CDA). The substantive content is 3 sentences. This reads as a minimal compliance artifact — the absolute minimum text needed to claim (b)(10) documentation exists.

## 7. Overall Assessment

### Classification

**Minimal/stub**

The documentation is too thin to assess what is actually exported. The 6-sentence PDF provides no data dictionary, no field-level detail, no sample data, and no export instructions. The choice of C-CDA as the sole structured export format is fundamentally mismatched with the product's core data — a chronic care management platform's most important data (care coordination logs, RPM device telemetry, medication adherence tracking, CCM time documentation) has no C-CDA representation. Even if the C-CDA export contains well-populated clinical sections, the majority of the product's distinctive data likely cannot be expressed in C-CDA format.

### Key Findings

1. **The entire EHI export documentation is 6 sentences on 1 page** (`SPAC-Export.pdf`, 380 KB). Three of those sentences define common file formats (ZIP, PDF, C-CDA). The substantive content is 3 sentences. No data dictionary, field definitions, sample data, schema, or export instructions exist.

2. **C-CDA is structurally inadequate for this product's core data.** hru2day is a chronic care management / RPM / medication adherence platform. Its most distinctive and voluminous data — care coordination logs (200,000+ interactions), RPM device telemetry (glucose, BP, HR, SpO2, weight time-series), medication adherence tracking, and CCM/PCM/RPM service time documentation — cannot be represented in C-CDA format. The export likely captures only the clinical summary layer (demographics, problems, meds, allergies) while missing the bulk of the product's actual data.

3. **No way to verify coverage.** Without sample data, a C-CDA section listing, or any field-level documentation, it is impossible to confirm what the export actually includes. Every domain assessment is necessarily speculative.

4. **Billing-relevant EHI is almost certainly absent.** The product tracks service time linked to CPT codes (99490, 99437, 99487, etc.) for Medicare CCM/PCM/RPM billing. This time tracking data is billing-relevant EHI that has no C-CDA analog and is not mentioned in the export documentation.

5. **The PDF attachments are an unknown wildcard.** The export includes "PDF files attached to the patient's chart (machine readable PDF)" — but no description of what these contain. They could potentially include care plans, consent forms, or other documents, but this is speculative.

### Summary Stats

```
Classification:  Minimal/stub
Export format:   C-CDA XML + PDF (in ZIP archive)
Model type:      Standard projection (C-CDA)
Entities:        N/A (no data dictionary)
Fields:          N/A (no data dictionary)
Descriptions:    N/A
Sample data:     No
Bulk export:     Unclear
Domains covered: 0 of 15 confirmed; up to 7 of 15 possible (if C-CDA sections populated)
```

### Bottom Line

This is one of the thinnest EHI export implementations possible. A 6-sentence PDF with no data dictionary, combined with a C-CDA-based export format that is fundamentally mismatched with the product's core data domains (care coordination, RPM telemetry, medication adherence), means that a patient would almost certainly receive only a fraction of their data. The product's most valuable and distinctive information — care management logs, device monitoring readings, adherence tracking, and billing documentation — likely has no path into the export at all.
