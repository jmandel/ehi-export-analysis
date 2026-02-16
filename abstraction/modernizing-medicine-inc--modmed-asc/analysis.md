# EHI Export Analysis: Modernizing Medicine Inc.

**Product**: ModMed ASC (version 6)
**Analysis date**: 2026-02-15
**CHPL ID**: 15.04.04.2002.mASC.06.11.0.250902 (CHPL #11701)

## 1. Product Context

ModMed ASC is a cloud-based platform purpose-built for ambulatory surgery centers (ASCs), primarily serving ophthalmology and gastroenterology surgery centers. It is built on the gGastro platform and shares the same underlying data model. The product covers:

- **Surgical documentation & charting**: Specialty-specific surgical narrative templates, concurrent charting (nurses, anesthesiologists, physicians), pre/intra/post-operative nursing documentation, anesthesia notes, operative reports, endoscopy report writing
- **Scheduling**: Surgical case scheduling, patient cost estimates
- **Billing & revenue cycle**: Integrated billing (professional, office, ASC, facility charges), insurance eligibility checks, claims scrubbing, ICD-10/CPT coding
- **Quality reporting**: ASC Quality Reporting (ASCQR), GIQuIC, OAS CAHPS
- **Patient engagement**: Patient portal (gPortal), digital check-in kiosks, online intake forms
- **Lab integration**: Electronic lab orders and results
- **Specialty-specific**: GI endoscopy, ophthalmology procedures, cardiology procedures
- **E-prescribing**: Via Surescripts integration

Intended users: MDs, PAs, MAs, Nurses, and Administrators. The product stores clinical, billing, scheduling, quality, and patient engagement data across the full ASC workflow.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `gGastro-EHI-Patient-Export-Specifications-Dec2025.pdf` | Primary data dictionary, 167 pages, v6.5.3.20251230. Contains CSV Files Dictionary (442 entities, 4,453 fields), Data Schema (relationship tree), Translations (value sets), Patient Documents (file reconstruction instructions), Glossary. Found on the gGastro ONC Certification page — newer than the version linked from the ASC page. | **Most informative** — this is the core export specification |
| `gGastro-Patient-Export-Specifications.pdf` | Earlier version of same data dictionary, 168 pages, v6.4.4.20250707. Linked directly from the ASC ONC Certification page. Minor differences from Dec 2025 version. | Informative (superseded by Dec 2025 version) |
| `gGastro-EHI-Patient-Export-Specifications-Additional.pdf` | Supplementary translation/value set document, 551 pages, v6.5.3.20251230. Contains extended reference data for coded fields — starts with a massive Occupation table mapping thousands of SOC codes to job titles, followed by other extended value sets. | Informative — provides complete value sets |
| `ASC-Mandatory-Disclosures.pdf` | 5-page PDF describing certified capabilities, costs, and requirements. Contains key EHI export mechanics: single-patient via UI, bulk via support case (Support@modmed.com), export format is database backup (.bak) with patient visits in .mht format, no fee for standard export. | **Highly informative** for export mechanics |
| `ModMed-ASC-Certification.pdf` | 1-page Drummond Group compliance certificate confirming ModMed ASC 6 certification on 09/02/2025. | Low informativeness (confirms certification) |
| `screenshot-asc-onc-certification-fullpage.png` | Full-page screenshot of ASC ONC Certification page showing "EHI Export Documentation" section with link to "Data Dictionary for ModMed gGastro EHI Export" | Confirms page structure and link |

## 3. Export Mechanics

- **Format**: The export is described in the mandatory disclosures as a "database backup (.bak), with Patient Visits extracted in .mht format and all other files in the format they were stored in Modernizing Medicine." The data dictionary documents the export as a package of **CSV files** — one per entity — plus associated document files (MHT, JPG, PDF).
- **Single-patient export**: Accessible through the ModMed user interface (no vendor assistance required)
- **Bulk/population export**: Must be initiated by opening a support case via email to Support@modmed.com
- **Cost**: No fee for standard single-patient or patient-population EHI export. "Fees may apply for custom EHI reports or other data exports that are not supported by the (b)(10) functionality."
- **Separate from FHIR API**: The FHIR API (documented at portal.api.modmed.com) is a separate §170.315(g)(10) channel providing USCDI-scoped data in FHIR R4 format. The CSV-based EHI export is the (b)(10) mechanism.

## 4. Export Content: What's In It

The export is documented through a comprehensive 167-page data dictionary (v6.5.3.20251230) organized into five sections:

### 4.1 CSV Files Dictionary

**442 entities with 4,453 total fields.** Each field is documented with:
- Column position (ordinal)
- Field name (descriptive PascalCase)
- Data type (99.8% of fields have types specified)
- Maximum length (34.1% of fields — primarily Alphanumeric fields)
- Format/Translation reference (24.7% of fields reference translation tables or specify date/time formats)

Field types distribution:
| Type | Count | % |
|---|---|---|
| GUID (foreign keys/IDs) | 1,362 | 30.6% |
| Alphanumeric | 1,298 | 29.2% |
| Numeric | 642 | 14.4% |
| Boolean | 486 | 10.9% |
| Date & Time | 387 | 8.7% |
| Decimal | 243 | 5.5% |
| Date | 11 | 0.2% |
| XML | 11 | 0.2% |
| Time | 4 | 0.1% |
| Binary | 1 | <0.1% |

**697 fields reference translation tables** — these are coded numeric values that map to human-readable values documented in the Translations section and the 551-page Additional supplement.

**Documentation style note**: Fields do not have prose descriptions. Documentation consists of field name + type + length + translation reference. Field names are descriptive PascalCase (e.g., `PatientFirstName`, `ColonoscopyIndication`, `ScoreRespiration`) which provides reasonable self-documentation. Translation references (e.g., "Service Components Aldrete Activity Score") tell you which value set to use for coded fields.

### 4.2 Data Schema

A hierarchical tree view showing parent-child relationships between all 442 entities, rooted at the Patient entity. Documents 575 relationships with explicit foreign key field names. Example structure:

```
Patient
├── AppointmentSet (PatientId)
│   ├── Appointment (AppointmentSetId)
│   │   ├── BillingEligibility (AppointmentId)
│   │   │   └── Insurance (CurrentBillingEligibilityId)
│   │   │       ├── BillingCharge (InsuranceId)
│   │   │       │   ├── BillingChargeModifier
│   │   │       │   ├── BillingChargeTransaction
│   │   │       │   └── ...
│   │   ├── BillingSuperbill (AppointmentId)
│   │   └── ...
│   └── Recall (AppointmentSetId)
├── Service (PatientId)
│   ├── ServiceDocument (ServiceId)
│   ├── ServiceProcedure (ServiceId)
│   │   ├── Finding (ServiceProcedureId)
│   │   ├── AdministeredMedication (ServiceProcedureId)
│   │   └── ...
│   └── ...
└── ...
```

### 4.3 Translations (Value Sets)

Extensive coded value sets for all Numeric fields that reference translation tables. The main document contains summary translation tables organized by category (Billing, Configuration, Patient, Report, Scheduler, Security, Service Components). The 551-page Additional supplement provides complete extended value sets, including a massive Occupation code table mapping thousands of SOC codes to job titles.

### 4.4 Patient Documents

Instructions for reconstructing file paths for 4 document types:
1. **Service Documents** — clinical documents attached to encounters (MHT format)
2. **Imaging Documents** — inbound faxes, scanned documents, imported documents, lab results with external documents (JPG, PDF, etc.)
3. **Patient Portal Documents** — documents published to patient portal (PDF)
4. **Letters** — recall letters and business correspondence (MHT)

### 4.5 Glossary

Definitions for key domain terms and abbreviations (AGA, CAHPS, CPT, CSV, DOB, GIQuIC, HCPCS, ICD-10, LOINC, MRN, RXNORM, SNOMED, etc.) and product-specific concepts (Service, Order, Translation, etc.).

### Vendor's own content organization

The data dictionary organizes entities alphabetically without explicit domain categories. Based on entity naming patterns and the relationship schema, the 442 entities break down as follows (complete inventory in `analysis/full-entity-inventory.json`):

| Category | Entities | Fields | Notes |
|---|---|---|---|
| Billing & Claims | 122 | 1,211 | Charges, claims, payments, adjustments, EDI transactions, superbills, collections, statements, cost estimation, online payments, auto-posting, ledger |
| Procedures & Services | 93 | 919 | Service records, findings, impressions, anesthesia, Aldrete scores, nursing complications, instruments, infusions, IV management, pain assessments, procedure overview, coding advisors |
| Patient | 44 | 412 | Patient demographics, medical history, family history, social history, consents, allergies, disease scoring, archive, identifiers, external mapping |
| Documents & Notes | 22 | 173 | Service documents, versions, letters, fax queues, general documents, addenda |
| Lab & Results | 19 | 186 | Interface results, requisitions, specimens, test results (manual and automated), lab orders |
| Scheduling | 18 | 142 | Appointments, appointment sets, holds, wait days, reminders, kiosk snapshots, status history, pending cancellations |
| Demographics | 16 | 128 | Person, addresses, phone, email, emergency contacts, employment, occupation, race/ethnicity granularity, gender identity, tribal affiliation, disability |
| Medications | 15 | 295 | Prescriptions, medication history, administered medications, pharmacy, NDC codes, renewal requests, inbound prescription queue |
| Patient Portal | 13 | 100 | Portal messages, documents, appointments, consent, user preferences, account management |
| Imaging | 10 | 85 | Imaging documents, pages, orders, sources, patient associations |
| Cardiology | 9 | 121 | Cardiology procedures, carotid ultrasound, echocardiography (TTE), nuclear perfusion, stress tests, HeartCentrix |
| Orders & Referrals | 8 | 82 | Orders, direct message recipients, general documents per order, imaging per order |
| Administrative | 7 | 52 | Tasks, task files, task notes, task recipients, LDM programs |
| Problems & Diagnoses | 6 | 53 | Patient diagnoses, diagnosis tracking, imaging document diagnoses |
| GI-Specific | 5 | 135 | AGA export/service, GIQuIC exports, extra-intestinal manifestations, follow-up intervals |
| Insurance | 5 | 79 | Insurance records, balances, eligibility per interface |
| Questionnaires & Forms | 5 | 37 | Patient questionnaires, PIF review, functional/cognitive status, guideline actions |
| Chart | 5 | 30 | Chart bookmarks, captures, in-use tracking, last visit |
| Immunizations | 4 | 51 | Patient immunizations, HL7 set values |
| Vitals | 4 | 68 | Vital signs, physical measurements |
| Communications | 4 | 35 | Direct mailbox, messages, syndromic surveillance |
| Quality Measures | 3 | 23 | ASC quality measures, MIPS report details |
| Care Management | 2 | 21 | Recall, recall events |
| Ophthalmology | 2 | 8 | Service procedure ophthalmology, lens data |
| Telehealth | 1 | 7 | Telehealth service records |

**Top 10 largest entities** (representative examples):

| Entity | Fields | Category |
|---|---|---|
| Finding | 155 | Procedures & Services |
| Intervention | 115 | Procedures & Services |
| GiquicExport | 101 | GI-Specific |
| BillingClaimSnapshot | 95 | Billing & Claims |
| InterfaceResult | 53 | Lab & Results |
| Order | 50 | Orders & Referrals |
| PatientOnAntiPlatelet... | 48 | Medications |
| MedicationHistory | 44 | Medications |
| PrescriptionInboundQueue | 44 | Medications |
| BillingPatientStatementHistory | 43 | Billing & Claims |

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export is exceptionally deep in two areas:

1. **Billing & Claims** (122 entities, 1,211 fields): This is by far the largest category, covering the entire revenue cycle — charges, claims, payments, adjustments, EDI transactions, superbills, collections, statements, eligibility, cost estimation, online payments, auto-posting, and patient ledger. The billing data model is deeply normalized with entities like `BillingClaimSnapshot` (95 fields capturing a complete point-in-time claim state), `BillingChargeTransaction`, and a full EDI payment chain (`BillingEdiClaimPayment` → `BillingEdiClaimPaymentClaim` → `BillingEdiClaimPaymentClaimService` etc.).

2. **Procedures & Services** (93 entities, 919 fields): The clinical service model is highly detailed, with the `Finding` entity alone having 155 fields (capturing endoscopic/procedural findings with extraordinary granularity). Includes anesthesia documentation (Aldrete scores, complications), nursing complications, IV management, instruments, infusions, pain assessments, and specialty-specific procedure data.

Other well-covered areas:
- **Patient data** (44 entities, 412 fields): Demographics, medical history, family history, social history, disease scoring
- **Medications** (15 entities, 295 fields): Prescriptions, administration records, medication history with full drug identifiers (NDC, RxNorm)
- **Lab & Results** (19 entities, 186 fields): Interface results, specimens, test results
- **Scheduling** (18 entities, 142 fields): Full appointment lifecycle including kiosk check-in
- **GI-Specific** (5 entities, 135 fields): AGA registry, GIQuIC quality data
- **Cardiology** (9 entities, 121 fields): TTE, carotid ultrasound, nuclear perfusion, stress tests

Thinner areas:
- **Ophthalmology** (2 entities, 8 fields): Only `ServiceProcedureOphthalmology` (1 field — just an Id) and lens data. This is notably thin given that ophthalmology ASCs are a primary market for this product. The ophthalmology-specific clinical detail may reside in the general Service/Finding entities rather than dedicated ophthalmology tables.
- **Telehealth** (1 entity, 7 fields): Minimal
- **Quality Measures** (3 entities, 23 fields): ASC quality measures and MIPS — adequate for the domain

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Person` (36 fields), `UsaAddress`, `Phone`, `Email`, `EmergencyContact`, `Employment`, `Occupation`, ethnicity/race/gender identity granularity entities — 16 entities, 128 fields total | Thorough; includes USCDI v3 demographic elements |
| Encounters / visits | ✅ Covered | `Service` (36 fields), `ServicePhase`, `ProcedureOverview` (43 fields), `Appointment` (38 fields) — encounters modeled as "Services" | Comprehensive encounter model |
| Problems / conditions / diagnoses | ✅ Covered | `PatientDiagnosis`, `PatientDiagnosisPerImagingDocument`, `PatientDiagnosisPerOrder`, `PatientFamilyHistoryDiagnosis`, `PatientDiseaseScoringSystem` — 6 entities, 53 fields | Adequate |
| Medications / prescriptions | ✅ Covered | `Medication` (41 fields), `MedicationHistory` (44 fields), `PrescriptionInboundQueue` (44 fields), `AdministeredMedication` (19 fields), `Pharmacy`, `NdcIdLogEntry` — 15 entities, 295 fields | Deep coverage including administered meds, prescriptions, NDC/RxNorm coding |
| Allergies | ✅ Covered | `PatientAllergy`, `PatientAllergyReaction` — dedicated allergy entities within Patient category | Covered |
| Immunizations | ✅ Covered | `PatientImmunization` (38 fields), `Hl7SetValuePerPatientImmunization` — 4 entities, 51 fields | Thorough |
| Vitals | ✅ Covered | `PatientVitalSigns`, `PatientVitalSignsSmoking`, `PhysicalMeasurement` — 4 entities, 68 fields | Covered |
| Lab results | ✅ Covered | `InterfaceResult` (53 fields), `InterfaceRequisition`, `InterfaceSpecimen`, `InterfaceTest`, `InterfaceTestResult` — 19 entities, 186 fields | Deep lab model |
| Imaging / diagnostic reports | ✅ Covered | `ImagingDocument` (38 fields), `ImagingDocumentPage`, `ImagingDocumentOrder` — 10 entities, 85 fields; plus document reconstruction instructions | Covered |
| Procedures | ✅ Covered | `ServiceProcedure`, `Finding` (155 fields), `Impression`, `ProcedureOverview` (43 fields), `Intervention` (115 fields) — 93 entities, 919 fields | Exceptionally detailed |
| Clinical notes / documents | ✅ Covered | `ServiceDocument`, `ServiceDocumentVersion`, `Addendum`, `ServiceQuickNote` — 22 entities, 173 fields; MHT format documents with file reconstruction paths | Covered; notes exported as MHT files |
| Care plans / goals | ⚠️ Partial | `Recall` and `RecallEvent` entities exist for follow-up scheduling; `GuidelineAction` and `GuidelineOverride` for clinical guidelines. No dedicated care plan entity. | ASCs typically don't generate longitudinal care plans; what exists is appropriate for the setting |
| Orders / referrals | ✅ Covered | `Order` (50 fields), `RefferingPhysicianPerAppointment`, `DirectMessageRecipientPerOrder` — 8 entities, 82 fields | Adequate |
| Insurance / coverage | ✅ Covered | `Insurance` (35 fields), `BillingInsuranceBalance`, `BillingPatientAuthorization`, `BillingEligibility` — 5 entities, 79 fields | Thorough |
| Claims / billing | ✅ Covered | 122 entities, 1,211 fields spanning charges, claims, payments, adjustments, EDI, superbills, collections, statements | Exceptionally deep — the most detailed domain in the export |
| Payments | ✅ Covered | `BillingPaymentAdjustmentRefund` (33 fields), `BillingChargeTransaction`, `BillingOnlinePayment`, `BillingPatientPrepay` | Part of the billing model |
| Consents / directives | ✅ Covered | `PatientConsent`, `PatientPortalConsent` entities | Covered |
| Patient communications / portal messages | ✅ Covered | `PatientPortalMessage`, `PatientPortalMessageAttachment`, `PatientPortalDocument`, `PatientPortalAppointmentUpdate` — 13 entities, 100 fields | Thorough |
| Specialty-specific (GI) | ✅ Covered | `AgaExport`, `AgaService`, `GiquicExport` (101 fields), `ExtraIntestinalManifestations`, `Interval` — detailed GI-specific data | Deep GI coverage with quality registry data |
| Specialty-specific (Ophthalmology) | ⚠️ Partial | `ServiceProcedureOphthalmology` (1 field), `ServiceProcedureLens` — only 2 entities, 8 fields | Thin; ophthalmic procedure details may be captured in generic Finding/Intervention entities rather than dedicated ophthalmology tables |
| Specialty-specific (Cardiology) | ✅ Covered | `CardiologyProcedure`, `Tte` (41 fields), `CarotidUltrasound`, `NuclearPerfusion`, `StressTest` — 9 entities, 121 fields | Solid cardiology sub-model |

## 6. Documentation Quality

**Strengths:**
- **Complete entity and field enumeration**: Every one of 442 entities has every field documented with position, name, type, and where applicable, length and translation reference. This is a full database schema export documentation.
- **Relationship schema**: The Data Schema section provides a complete hierarchical view of all 575 parent-child relationships with explicit foreign key field names, enabling reconstruction of the complete data model.
- **Value sets**: Extensive translation tables in the main document plus a 551-page supplement with complete coded value sets (including SOC occupation codes). The 697 fields that reference translation tables can all be decoded.
- **Document reconstruction**: Clear instructions for rebuilding file paths for all document types (service docs, imaging, portal, letters).
- **Versioned**: Documents are versioned (6.5.3.20251230) indicating active maintenance.

**Limitations:**
- **No prose field descriptions**: Fields have names and types but no textual descriptions explaining what they mean. The PascalCase field names (e.g., `ColonoscopyAbortedPriorToAnesthesia`, `RecommendedColonoscopyIntervalYears`) are largely self-documenting, but more obscure names (e.g., `LdmProgram`, `PifReview`) require domain knowledge.
- **No sample data**: No example CSV files or sample records are provided. A developer would have to work from the schema alone.
- **No explicit primary key documentation**: While GUID `Id` fields are present in most entities and the Data Schema shows foreign keys, primary keys are not formally labeled.
- **Alphabetical rather than domain-organized**: The CSV Files Dictionary lists entities alphabetically rather than by functional domain, making it harder to understand the data model conceptually.

**Overall**: A technically skilled developer with healthcare domain knowledge could build an import from this documentation. The schema is complete and relationships are documented. The main gap is the absence of prose descriptions and sample data.

## 7. Overall Assessment

### Classification

**Comprehensive native export**

This is a genuine native database model export — 442 entities with 4,453 fields covering the complete data model of the gGastro/ModMed ASC platform. The export uses CSV files (one per entity) rather than healthcare-standard formats, with a detailed data dictionary, relationship schema, translation tables, and document reconstruction instructions.

### Key Findings

1. **Genuinely comprehensive scope**: 442 entities and 4,453 fields represent a full database schema export, not a clinical summary or FHIR projection. The billing domain alone has 122 entities and 1,211 fields — this is the vendor's actual data model, not a curated subset.

2. **Exceptionally deep billing coverage**: The 122 billing entities cover the entire revenue cycle from eligibility through claims, payments, EDI transactions, and collections. This level of billing data export is uncommon and demonstrates a real commitment to exporting "all" EHI.

3. **Rich specialty clinical data**: The `Finding` entity (155 fields) and `GiquicExport` (101 fields) capture GI-specific clinical data at a granularity that goes far beyond standard clinical summary formats. Cardiology also has a dedicated 9-entity, 121-field sub-model.

4. **Well-documented relationships**: The Data Schema section provides 575 explicit parent-child relationships, enabling complete data model reconstruction — a significant aid for anyone consuming the export.

5. **Documentation lacks prose descriptions**: While structurally complete, the data dictionary provides field names and types without textual descriptions. Field names are descriptive but some domain expertise is required to interpret them.

### Summary Stats

```
Classification:  Comprehensive native export
Export format:   CSV (one file per entity) + document files (MHT, JPG, PDF)
Model type:      Native database model
Entities:        442
Fields:          4,453
Descriptions:    0% prose descriptions; 99.8% have types; 34.1% have max_length; 15.7% reference translation tables
Sample data:     No
Bulk export:     Yes (via support case to Support@modmed.com)
Domains covered: 17 of 18 applicable domains (care plans partial for ASC context; ophthalmology thin)
```

### Bottom Line

ModMed ASC provides one of the more thorough EHI export specifications available — a 442-entity, 4,453-field native database export with complete relationship documentation and extensive value sets. A patient or provider would get a genuinely comprehensive copy of their data spanning clinical, billing, scheduling, and engagement domains. The main weakness is the absence of prose field descriptions and sample data, but the self-documenting field names and complete translation tables largely compensate.
