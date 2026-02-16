# Canvas Medical, Inc. — Product Research

Researched: 2026-02-16
Developer website: https://canvasmedical.com

## Overview

Canvas Medical, Inc. is a San Francisco-based health technology company founded in 2015 by Andrew Hines. The company builds an API-first, cloud-hosted electronic medical record (EMR) platform designed primarily for outpatient specialty clinics and tech-enabled healthcare organizations. Canvas positions itself as a modern, developer-friendly alternative to legacy EHR systems, with a strong emphasis on customizability through its Python SDK and FHIR API.

Canvas has raised approximately $64.4M in total funding (Series B of $24M led by M13, with participation from Inspired Capital, IA Ventures, Upfront Ventures, Village Global, and others). The company achieved ONC certification in 2022. As of early 2026, Canvas serves 20+ named healthcare organizations across multiple outpatient specialties and was named the 2026 Best in KLAS Ambulatory Specialty EHR. The current CEO is Adam Farren (appointed September 2024); founder Andrew Hines serves as CTO. The company reports its customer base grew 300% following its self-serve platform launch.

## Product: Canvas Medical

CHPL IDs: 10904

### What It Is

Canvas Medical is a comprehensive, cloud-hosted EMR platform certified under ONC's Health IT Certification Program. The certified module ("Canvas Medical 1") covers a broad set of criteria spanning clinical documentation, CPOE, transitions of care, patient portal, public health reporting, and FHIR APIs — 35+ certified criteria in total. This is not a narrow specialty module; it is the full platform.

The platform is API-first and built for extensibility. Canvas exposes its functionality through a FHIR R4 REST API (40 FHIR resources, 21 with write support) and a Python SDK that provides access to 47+ internal data models. The architecture is based on an open-source gRPC plugin runner where developers build "handlers" that respond to over 650 clinical and operational events and produce "effects" that modify data or the UI.

Canvas offers pre-built EMR configurations for specific specialties (primary care, behavioral health, cardiology, weight loss/cardiometabolic, longevity, chronic care management, urgent care/telehealth, sleep medicine, gastroenterology, psychiatry) but the underlying platform is the same product. The specialization comes through configurable plugins and workflows, not separate codebases.

### Users & Market

Canvas targets two overlapping audiences:

1. **Tech-enabled healthcare companies** (digital health startups, virtual-first clinics, value-based care organizations) that want a programmable EMR they can customize deeply via API and SDK. Named customers include Heartbeat Health, Wisp, Vida Health, Prax Health, Orchestra Health, Patina Health, Circulo, Vivante Health, and Isaac Health.

2. **Traditional specialty practices** that want a modern, specialty-specific EMR with pre-built workflows and plugins — no developer required. Canvas offers a "library of prebuilt plugins" for these users.

Day-to-day users include physicians, nurses, community health workers, billing staff, and practice managers. The CHPL SED intended user description is "health care delivery users, not limited to clinicians," confirming it's used by non-clinical staff as well.

Canvas operates exclusively in outpatient/ambulatory settings — no inpatient or hospital functionality is described. Clinical settings include solo practices, multi-site groups, virtual care organizations, and chronic care management programs. Canvas won the 2026 Best in KLAS award specifically in the "Ambulatory Specialty EHR" category, and KLAS users highlighted its adaptability to non-fee-for-service and value-based care models.

### Modules & Functionality

Based on vendor materials, developer documentation, and press coverage, Canvas Medical includes the following functionality:

**Clinical Documentation & Charting**
- Proprietary "Narrative Charting" system (claimed 3x faster with 80% fewer clicks than menu-based EMRs)
- "Commands" — structured chart documentation units that form the building blocks of clinical notes
- Clinical notes/encounters linked to assessments, reason for visit, billing codes
- Protocol engine for clinical decision support (active protocols, protocol overrides/snoozing)
- Banner alerts for patient-level notifications

**Orders & Prescribing**
- CPOE for medications, laboratory, and diagnostic imaging (per ONC certification)
- Drug-drug and drug-allergy interaction checking
- E-prescribing via Surescripts integration (including controlled substances implied by certification criteria)
- Lab ordering and results via Health Gorilla integration
- Referral management

**Patient Records**
- Demographics, family health history, implantable device tracking
- Allergy/intolerance management
- Problem list / conditions
- Medication list (active medications, medication history, medication statements, compound medications, stop medication events)
- Immunization records
- Vitals and observations
- Care plans and care teams
- Patient consents
- Goals

**Scheduling**
- Appointment scheduling with calendar management
- Provider schedules and time slots
- Facility and practice location management

**Billing & Revenue Cycle**
- Integrated billing with claims submission via Claim.MD integration
- Billing line items linked to clinical notes
- Charge Description Master (CDM)
- Payor-specific charges
- Coverage/insurance management
- Eligibility checking and summaries (copay, coinsurance)
- Payment posting and claim payment tracking
- Support for fee-for-service, value-based, and direct-to-consumer membership payment models
- HCC (Hierarchical Condition Category) coding support
- AI-powered "Claim Coding Agent" for automated code suggestions

**Patient Engagement & Communication**
- Patient portal (view, download, transmit per (e)(1) certification)
- Secure messaging (Message data model for sent/received messages)
- Patient letters/correspondence
- Open-source patient app
- Questionnaires and questionnaire responses

**AI & Automation**
- Hyperscribe: open-source AI clinical documentation copilot (ambient scribe)
- Claim Coding Agent: automated revenue cycle coding
- Parsing Agent: document and lab data processing
- Plugin-based workflow automation (650+ triggerable events)
- Natural language plugin creation via Claude Code integration

**Interoperability & Data Exchange**
- FHIR R4 API with 40 resources
- C-CDA generation and import
- Transitions of care (send/receive)
- Immunization registry reporting ((f)(1))
- Electronic case reporting ((f)(5))
- SMART on FHIR app embedding
- Webhooks
- External event ingestion (ADT feeds)
- Pre-built integrations: Surescripts (e-prescribing), Health Gorilla (labs), Claim.MD (claims)
- Third-party integration clients for AI/ML, cloud storage, email, messaging

**Administrative**
- Staff and user management
- Organization and facility configuration
- Team and care team management
- Task management system
- Business lines (patient groups sharing brands)
- Audit logging (per (d) criteria certification)

### Data & Content

The Canvas Medical SDK documentation provides an unusually transparent view of the platform's internal data model, listing 47+ data objects. Based on this and the FHIR API documentation, the platform stores:

**Clinical data**: Patient demographics, conditions/diagnoses, allergies/intolerances, medications (active, historical, statements, compounds, stop events), immunizations, lab results, imaging results, observations/vitals, procedures, devices/implantables, clinical notes/encounters, assessments, care plans, care teams, goals, clinical protocols, detected issues, diagnostic reports, specimens.

**Orders & prescriptions**: Medication requests, medication dispense records, lab orders, imaging orders, referrals.

**Administrative data**: Appointments, schedules, calendars, patient consents, tasks, staff records, user accounts, organizations, facilities, practice locations, teams, business lines, value sets, service providers.

**Financial data**: Claims, billing line items, charge description master entries, payor-specific charges, coverage/insurance, eligibility summaries, payment postings.

**Communication data**: Messages (sent/received), letters, questionnaires and responses, banner alerts, external events (ADT).

**Documents**: C-CDA documents, uncategorized clinical documents, media/attachments, document references.

**Audit & system data**: Provenance records, application/plugin definitions, common enumeration types.

The breadth of the SDK data model (47 objects covering clinical, financial, administrative, and communication domains) combined with the FHIR API (40 resources) strongly suggests this platform stores a comprehensive set of ambulatory healthcare data — essentially everything needed to run an outpatient practice including clinical care, billing, scheduling, and patient communication.

---
