# EHI Export Analysis: NovoMedici, LLC

**Product**: NovoClinical v1.0
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.02.05.3015.Novo.01.01.1.220131 (CHPL ID 10805)

## 1. Product Context

NovoClinical is a cloud-based, all-in-one ambulatory EHR and practice management system built by NovoMedici, LLC, a small vendor (~5–9 employees) in Ogden, Utah. It targets small to mid-sized ambulatory practices across multiple specialties (general practice, cardiology, GI, OB/GYN, pediatrics, dermatology). The product integrates:

- **Clinical documentation**: charting with customizable templates, problem lists, medication lists, allergy lists, implantable device lists, vital signs, immunizations, lab/imaging orders and results, clinical notes with voice recognition
- **E-Prescribing**: electronic prescribing integrated with external networks
- **Billing & RCM**: medical billing/coding, UB-04, claim scrubbing, DME billing, payment processing, statement generation, credit card integration — billing is a core marketed feature ("Medical Billing Software for Small Business")
- **Practice management**: scheduling, patient registration, check-in, referrals
- **Patient portal**: secure messaging, visit summaries, lab results, appointment requests, e-signatures
- **Telemedicine**: virtual visit capabilities
- **Chronic care management**: monitoring for chronic conditions
- **Communications**: built-in e-fax, text messaging, alerts, task management, Direct messaging

This product stores data across clinical, billing, scheduling, communications, and patient engagement domains. A genuine (b)(10) export should cover all of these.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/Novoclinical-Data-Export-Format.pdf` | Single-page PDF (129 KB, created 2023-10-07). Contains 3 sentences describing export format (C-CDA + CSV), navigation instructions, and a screenshot of the export UI. | **Primary artifact** — but extremely thin. No data dictionary, no field definitions, no schema. |
| `downloads/screenshot-meaningful-use-page.png` | Screenshot of vendor's Meaningful Use / mandatory disclosures page at novomedici.com/meaningful-use/. Confirms the same PDF is linked as "EMR Data Export." | **Confirmatory** — verified no additional EHI export documentation exists on the vendor's site. |
| `product-research.md` | Prior research on NovoClinical's features and capabilities. | **Context** — established baseline of what the product stores. |
| `ehi-export-report.md` | Prior agent's analysis of collected artifacts. | **Orientation** — findings verified against source artifacts. |

The PDF is the sole substantive artifact. It contains no data dictionary, no schema, no sample data, and no field-level documentation of any kind.

## 3. Export Mechanics

- **Format**: ZIP file containing C-CDA XML document(s) and CSV file(s)
- **Mechanism**: UI-based — clinic administrators navigate to Communication > Data Export
- **Single-patient vs bulk**: Both supported. The interface (visible in the PDF screenshot) offers individual patient export or group export of "all or multiple patients." Filters include doctor, frequency (monthly), date range, and patient search.
- **Access constraints**: Available to clinic administrators (role-restricted)
- **Fees**: Not mentioned in the documentation

The export interface screenshot shows tabs for "Data Export" and "Create New," with fields for Doctor (default: "All Doctors"), Frequency ("MONTHLY"), date/time range for appointments, and an "Add Patient" search box. Buttons are "Create New" and "Reset."

## 4. Export Content: What's In It

The documentation names exactly two export components with no further detail:

1. **C-CDA document** — "Each patient will have a C-CDA document in the exported data." No specification of which C-CDA document type (CCD, Referral Note, etc.), which HL7 template versions, or which sections are populated.

2. **CSV files** — "Comma separated value, used for patient demography, Appointments." No column definitions, no delimiter specification, no encoding details, no sample data.

There is **no data dictionary**. Zero fields are documented. Zero types are specified. Zero value sets are defined. Zero relationships are described.

### Vendor's own content organization

The vendor organizes the export into two named components:

| Entity/Component | Fields Documented | Descriptions | Types | Category (vendor's) |
|---|---|---|---|---|
| C-CDA Document | 0 | 0 | No | Clinical (unspecified sections) |
| Patient Demography CSV | 0 | 0 | No | Demographics |
| Appointments CSV | 0 | 0 | No | Scheduling |

**Total documented entities: 3. Total documented fields: 0.**

A developer receiving this export would need to reverse-engineer the file formats entirely from actual export files. The C-CDA could be parsed using standard C-CDA libraries, but the CSV files have no specification at all.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes three export components spanning two categories:

1. **Clinical data via C-CDA**: C-CDA is a standard that *can* include problems, medications, allergies, immunizations, vitals, procedures, lab results, encounters, and clinical notes. However, the vendor does not specify which C-CDA sections their implementation populates. At best, this covers standard clinical summary data — the same data that would be in a (g)(10) FHIR API or a transitions-of-care C-CDA. At worst, it could be a minimal CCD with only a few sections populated.

2. **Demographics and appointments via CSV**: Basic patient demographics and scheduling data. Without column definitions, the depth is unknown.

The export has **no coverage** of billing, prescribing history, patient portal data, telemedicine records, chronic care management data, communications, referrals, documents/attachments, or insurance/coverage data — all of which the product stores.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | "Patient Demography" CSV mentioned, but no fields defined | Product stores demographics; CSV exists but content unknown |
| Encounters / visits | ⚠️ Partial | C-CDA may include encounter sections; Appointments CSV exists | Appointments exported as CSV; clinical encounter detail depends on unspecified C-CDA sections |
| Problems / conditions | ⚠️ Partial | C-CDA may include problem list | Depends on C-CDA sections (unspecified) |
| Medications / prescriptions | ⚠️ Partial | C-CDA may include medication list | C-CDA would cover medication list; e-prescribing history likely not included |
| Allergies | ⚠️ Partial | C-CDA may include allergy list | Depends on C-CDA sections (unspecified) |
| Immunizations | ⚠️ Partial | C-CDA may include immunizations | Depends on C-CDA sections (unspecified) |
| Vitals | ⚠️ Partial | C-CDA may include vital signs | Depends on C-CDA sections (unspecified) |
| Lab results | ⚠️ Partial | C-CDA may include lab results | Depends on C-CDA sections (unspecified) |
| Imaging / diagnostic reports | ⚠️ Partial | C-CDA may include some imaging results | Product integrates RIS/PACS; C-CDA unlikely to carry full imaging data |
| Procedures | ⚠️ Partial | C-CDA may include procedures | Depends on C-CDA sections (unspecified) |
| Clinical notes / documents | ⚠️ Partial | C-CDA may include notes sections | Product has extensive charting/templates; C-CDA unlikely to carry all note types |
| Care plans / goals | ⚠️ Partial | C-CDA may include care plan section | Product has CCM module; coverage unknown |
| Orders / referrals | ❌ Not covered | No mention in export documentation | Product supports orders and referrals; not addressed in export |
| Insurance / coverage | ❌ Not covered | No mention in export documentation | Product manages patient eligibility and insurance; significant gap |
| Claims / billing | ❌ Not covered | No mention in export documentation | Product has full billing/RCM (claims, coding, UB-04, DME billing); **major gap** |
| Payments | ❌ Not covered | No mention in export documentation | Product processes payments and generates statements; significant gap |
| Consents / directives | ❌ Not covered | No mention in export documentation | Product has e-signature for documents; not addressed |
| Patient communications | ❌ Not covered | No mention in export documentation | Product has portal messaging, e-fax, text messaging, Direct messaging; significant gap |
| Specialty-specific data | ❌ Not covered | No mention in export documentation | Product supports multiple specialties with customizable templates; not addressed |

**Summary**: 0 domains are definitively covered with field-level evidence. 10 domains receive only *possible* partial coverage via an unspecified C-CDA implementation. 8 domains that the product stores are completely absent from the export documentation. The most significant gap is **billing/RCM** — a core marketed feature of NovoClinical with no representation in the export.

## 6. Documentation Quality

The documentation quality is **extremely poor** — among the worst possible while still technically existing:

- **No data dictionary**: Not a single field is named, typed, or described anywhere
- **No schema**: No machine-readable format specification for either the C-CDA or CSV components
- **No sample data**: No example exports provided
- **No value sets**: No coded value documentation
- **No relationships**: No description of how files relate to each other
- **No C-CDA section specification**: The vendor says "C-CDA" but doesn't say which document type, template, or sections
- **No CSV column specification**: The vendor says "CSV" but doesn't list a single column name

A developer **could not** build an import from this documentation. The entire documentation is 3 sentences of prose plus a UI screenshot. The C-CDA component could be reverse-engineered using standard C-CDA parsers on an actual export file, but the CSV files would require complete reverse-engineering.

The documentation has not been updated since its creation on October 7, 2023.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation is too thin to assess actual field-level coverage, but even taking the vendor's description at face value, the export covers only C-CDA clinical summary data plus basic demographics and appointments. This is a fraction of what NovoClinical stores. The product's entire billing/RCM module — a core feature prominently marketed — is absent. Patient portal data, communications, telemedicine records, chronic care management data, referrals, insurance/coverage, and specialty-specific clinical data are all unaddressed. Even the clinical data covered by C-CDA is of unknown depth because the vendor doesn't specify which C-CDA sections are populated.

**Axis 2 — Export approach: Repackaged existing export**

This export is clearly a repackaged version of NovoClinical's existing clinical exchange capabilities. The C-CDA component is the same Consolidated Clinical Document Architecture used for transitions of care under (b)(1)–(b)(3), which the product is also certified for. The CSV files for demographics and appointments add minimal value beyond what's already in the C-CDA. There is no product-specific data dictionary, no mapping beyond standard C-CDA templates, and no coverage of billing, operational, or specialty data. The export format, content scope, and documentation all point to the vendor relabeling their existing clinical document exchange as a (b)(10) export.

### Key Findings

1. **The entire EHI export documentation is a single 1-page PDF with 3 sentences of substance.** It names two formats (C-CDA, CSV) and provides navigation instructions. Zero fields are documented anywhere. (`downloads/Novoclinical-Data-Export-Format.pdf`, 129 KB, 1 page)

2. **The export is a repackaged C-CDA clinical exchange plus minimal CSV files.** C-CDA is the same standard used for transitions of care — this is not a purpose-built EHI export. The CSV files add only demographics and appointments with no column definitions.

3. **Billing/RCM data — a core product feature — is entirely absent.** NovoClinical is marketed as integrated billing software with claims, coding, UB-04, DME billing, payment processing, and statement generation. None of this appears in the export.

4. **No field-level documentation exists for any component.** A recipient cannot know what data is in the C-CDA (which sections?), what columns are in the CSV files, or how the files relate. Complete reverse-engineering from actual export files would be required.

5. **At least 8 data domains the product stores are completely unaddressed**: billing/claims, payments, insurance/coverage, patient communications, referrals/orders, consents, telemedicine records, and specialty-specific data.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Repackaged existing export
Export format:   C-CDA XML + CSV, delivered as ZIP
Entities:        3 (named components; 0 field-level detail)
Fields:          0 (no fields documented)
Descriptions:    N/A (no fields to describe)
Sample data:     No
Bulk export:     Yes (multi-patient export supported via UI)
Domains covered: 0 of 17 confirmed; up to 10 of 17 possible via unspecified C-CDA
```

### Bottom Line

NovoClinical's (b)(10) EHI export is a repackaged C-CDA clinical summary with two undocumented CSV files for demographics and appointments, described in a single-page PDF with zero field-level documentation. A patient or provider would receive a clinical summary comparable to a transitions-of-care document, but would not get their billing records, communications, portal messages, insurance details, or any of the other data that NovoClinical stores about them. The single biggest gap is the complete absence of billing/RCM data from a product whose billing capabilities are a core selling point.
