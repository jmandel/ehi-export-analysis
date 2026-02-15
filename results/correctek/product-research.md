# CorrecTek — Product Research

Researched: 2026-02-15
Developer website: http://www.correctek.com

## Overview

CorrecTek is a niche EHR vendor based in Paducah, Kentucky, founded in 2006 and specializing in electronic health records for **correctional healthcare, juvenile detention, and behavioral health** settings. The company's tagline is "EHR Your Way," emphasizing customizability. They serve over 120 organizations across 30+ U.S. states and territories, with over 200 correctional institutions reportedly using their platform. CorrecTek claims a 99% customer satisfaction rate and over 20 years of experience in the correctional health IT space.

CorrecTek is a small, privately held company (headquartered at 2929 Broadway, Paducah, KY 42001). Based on ZoomInfo data, competitors include AltaPoint Data Systems, FoxFire Systems Group, ChartLogic, and The Joxel Group — all relatively small vendors. The company's president is Dan Jarrett. CorrecTek sells directly and also works with healthcare vendors who provide correctional healthcare services (e.g., companies that contract to run medical operations within jails/prisons). They specifically note a "Corizon vs CorrecTek" comparison page, suggesting they compete directly with Corizon Health (a major correctional healthcare provider with its own EHR).

The product is offered as either a one-time purchase or a lease option. Hosting options include cloud-hosted (managed by Kalleo Technologies, their preferred option), hybrid (on-premise but Kalleo-managed), or self-hosted (on-premise, self-managed).

## Product: Spark

CHPL ID: 10274

### What It Is

Spark is CorrecTek's single EHR platform — it is the entire product, not a component of something larger. It is ONC-certified (version 7.1, certified 2020-01-14) and purpose-built for complex care environments, primarily correctional facilities (jails and prisons), juvenile detention centers, behavioral health programs, and other specialized residential treatment settings. The certified module IS the product. Spark is also EPCS-certified for electronic prescribing of controlled substances.

The CHPL certification is broad, covering 30+ criteria across clinical data (a)(1)-(a)(14), transitions of care (b)(1), EHI export (b)(10), bulk data (b)(11), clinical quality measures (c)(1), FHIR API (g)(7)+(g)(10), direct messaging (h)(1), and security/privacy criteria. This certification profile indicates a full-featured EHR, not just a narrow module.

### Users & Market

**Intended users** (per CHPL): "Medical office personnel, including RNs, Providers, Admins and Support staff." In practice, given the correctional setting, this includes:
- **Nurses and medical staff** performing intake screenings, sick call, medication administration, and chronic care management
- **Physicians/providers** documenting encounters, ordering labs/imaging, prescribing medications
- **Behavioral/mental health clinicians** documenting behavioral health encounters (the correctional page explicitly mentions behavioral health records in the unified chart)
- **Dental providers** (dental records are mentioned as part of the unified patient chart)
- **Billing/administrative staff** managing claims, eligibility checks, and payment reconciliation
- **Facility administrators** using reporting and analytics tools for compliance oversight

Customer base is overwhelmingly in **correctional and juvenile detention settings**: county jails, state prisons, juvenile detention centers, and residential treatment programs. The system supports compliance with correctional healthcare accreditation bodies including NCCHC (National Commission on Correctional Health Care), ACA (American Correctional Association), and AJA (American Jail Association).

### Modules & Functionality

**Charting & Clinical Documentation** (vendor Spark product page, correctional solutions page):
- Structured clinical documentation with customizable forms, templates, and workflows
- Emphasis on quick data entry through structured inputs and direct selections rather than manual typing
- Configurable patient intake workflows
- Audit-ready documentation to support compliance

**Unified Health Record** (correctional and juvenile pages):
- Integrates medical, dental, and behavioral health records into a single unified patient chart
- Centralizes all patient data in one location

**Medication Management** (correctional page, interfaces page):
- Electronic Medication Administration Record (eMAR) for accurate medication tracking
- EPCS-certified e-prescribing (including controlled substances)
- E-prescribing via NewCrop (required for Meaningful Use users, per mandatory disclosures page)
- Bidirectional pharmacy interfaces supporting medication orders, renewals, refills, drug substitutions, and barcoding
- SureScripts integration for querying 12-month prescription history

**Computerized Provider Order Entry (CPOE)** (per CHPL criteria (a)(1)-(a)(3)):
- Medication orders
- Laboratory orders (sent directly to lab vendors, results received back into Spark)
- Imaging/radiology orders (sent to radiology vendors, interpretations and optional low-res images returned)

**Drug Interaction Checking** (mandatory disclosures page, CHPL criteria (a)(4)):
- Clinical decision support for drug interactions

**Integrated Billing** (Spark product page):
- Full billing cycle management within Spark — no external billing system needed
- Eligibility checks (real-time coverage verification)
- Automatic code assignment (billing codes applied automatically during documentation)
- Claim submission (Medicare, Medicaid, private insurance)
- ERA (Electronic Remittance Advice) posting — automated payment and adjustment application
- Specific support for Medicaid 1115 waiver programs (common in correctional healthcare where states use waivers to bill Medicaid for inmate healthcare)
- Charges feed interface that automates billing through commissary vendors

**Sick Call Management** (interfaces page):
- Inmate sick call requests captured through phones, kiosks, or tablets are sent to Spark
- Optional confirmation and status updates back to inmates

**Reporting & Analytics** (Spark product page, solutions page):
- Built-in reporting engine with hundreds of prebuilt report templates
- Reports across clinical, compliance, cost, and operational domains
- Automated reports for detailed analysis
- Optional CBI (CorrecTek Business Intelligence) Dashboard add-on powered by Microsoft Power BI for visual dashboards, drill-down analysis, and trend monitoring

**Scheduling & Workflow** (various pages):
- Scheduling through structured inputs
- Task optimization through automation of redundant tasks

**Compliance & Risk Management** (correctional page):
- Configurable workflows aligned with NCCHC, ACA, AJA accreditation requirements
- Detailed documentation for compliance and liability reduction
- Role-based access controls
- Comprehensive audit trail tracking all user activity

**Juvenile-Specific Features** (juvenile solutions page):
- Release planning (coordination with case managers for resident release)
- Medication compliance tracking
- Patient portal for guardian access to resident records and consent
- Immunization registry verification and updates for state compliance
- Automated age-based preventative care (wellness checks)
- Resident tracking interfaces

**Interoperability & Data Exchange** (interfaces page):
- C-CDA and PDF export (per mandatory disclosures)
- FHIR API access via "Interoperability Engine" (likely EMR Direct, per mandatory disclosures)
- Carequality network participation for nationwide health record sharing
- Health Information Exchange (HIE) — sending/receiving patient records with regional and state exchanges
- Direct messaging (h)(1) certification
- US Marshals documentation support for federal detainees
- Hospital interface for receiving lab results, transcriptions, and medical service records
- Immunization and cancer registry reporting to state systems
- AI/analytical tools interface (Spark does not include built-in clinical analysis; it interfaces with external AI tools)

**Patient Portal** (interfaces page, juvenile page):
- Integrates a portal allowing patients or family members to communicate electronically with healthcare providers

**Hosting & Deployment**:
- Cloud-hosted (Kalleo Technologies, recommended), hybrid, or self-hosted options

### Data & Content

Based on the features and interfaces described above, Spark stores and manages the following data:

**Clinical data**: Patient demographics, photos, facility locations, admission/discharge times (received from tracking/OMS/JMS systems). Medical records including encounter documentation, clinical notes, problem lists, medication lists, allergy/intolerance records, immunization records, vital signs, and clinical assessments. The (a)(1)-(a)(14) certification confirms CPOE data, drug interaction data, demographics, clinical decision support data, implantable device lists, and clinical quality measure data.

**Behavioral health and dental records**: Explicitly mentioned as integrated into the unified patient chart alongside medical records.

**Medication data**: eMAR records, e-prescribing history (including controlled substances via EPCS), medication orders/renewals/refills, drug substitution records, barcoding data, and 12-month SureScripts prescription history queries.

**Orders and results**: Lab orders and results (bidirectional with lab vendors), radiology orders and interpretations (with optional images), medication orders.

**Billing and financial data**: Claims data (Medicare, Medicaid, private), eligibility verification records, billing codes (auto-assigned from documentation), ERA/payment posting data, charges feed data, Medicaid 1115 waiver claims.

**Sick call requests**: Inmate-initiated requests via phones/kiosks/tablets with confirmation and status tracking.

**Tracking/custody data**: Patient demographic information, photos, locations within the facility, and admission/discharge events received from offender management/jail management systems (OMS/JMS).

**Compliance and audit data**: Comprehensive audit trail of all system activity, compliance reporting data aligned with NCCHC/ACA/AJA standards.

**Reporting data**: Hundreds of prebuilt report outputs across clinical, compliance, cost, and operational domains. CBI Dashboard analytics data (if add-on is used).

**Interoperability records**: C-CDA documents, FHIR resources, health information exchange records (Carequality, HIE), US Marshals documentation, hospital records (lab results, transcriptions).

**Portal data**: Patient/guardian communications and consent records (juvenile settings).

**Notable**: The website does not mention appointment scheduling in detail beyond brief references to "scheduling" as a structured input. It's unclear how robust the scheduling module is. The system is not described as having a robust patient-facing portal in the correctional context (inmates typically don't have direct portal access), though guardian portal access is mentioned for juvenile settings.

---
