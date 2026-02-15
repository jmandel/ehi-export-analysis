# Medplum — Product Research

Researched: 2026-02-15
Developer website: https://www.medplum.com/

## Overview

Medplum is an open-source, FHIR-native healthcare developer platform founded in 2021 by Reshma Khilnani (CEO), Cody Ebberson (CTO), and Rahul Agarwal (COO) — all previously co-founders of MedXT (YC W13), which was acquired by Box. Medplum went through Y Combinator's Summer 2022 batch and is based in San Francisco with a team of approximately 12 people.

Medplum describes itself as a "headless EHR" — an API-first, developer-oriented platform that provides the backend infrastructure (clinical data repository, FHIR API, authentication, automation, UI components) for building custom healthcare applications. It is not a traditional turnkey EHR that practices buy and use out of the box. Instead, it is a platform that healthcare technology companies and provider organizations use to *build* their own EHR, patient portal, care coordination tools, or other clinical applications on top of.

The company claims to facilitate care for over 20 million patients across hundreds of practices. Customers range from startups (Summer Health, Develo) to larger enterprises (Ro Diagnostics, Thirty Madison). The platform is open source under the Apache 2.0 license, with the core codebase available on GitHub (2.1K+ stars, 157 contributors). Medplum offers both a managed cloud service and self-hosted deployment options.

The founding team's stated inspiration is open-source developer infrastructure companies like GitLab, PostHog, and Airbyte — applied to healthcare. Their competitive positioning is as the open-source alternative to proprietary healthcare platforms, targeting developers and engineering teams rather than end-user clinicians directly.

## Product: Medplum

CHPL IDs: 11745

### What It Is

Medplum is a headless EHR platform — a FHIR-compliant clinical data repository with APIs, SDKs, and developer tools for building custom healthcare applications. The certified product (Medplum v5, certified 2025-12-31) encompasses the entire platform.

Unlike traditional EHRs where the vendor provides a complete clinical application, Medplum provides the *infrastructure layer*: a FHIR data store, REST/GraphQL APIs, an authentication system (OAuth2, OpenID Connect, SMART-on-FHIR), server-side automation ("Bots"), a React UI component library, and pre-built integrations. Customers then build their own clinical applications on this foundation.

The certification criteria reflect this platform nature:
- Clinical: (a)(2) CPOE for lab, (a)(5) demographics, (a)(14) implantable device list
- Transitions of care: (b)(1)
- EHI export: (b)(10)
- Clinical quality measures: (c)(1)
- FHIR APIs: (g)(7), (g)(9), (g)(10)
- Security/infrastructure: extensive (d) criteria

Notably absent from certification: e-prescribing criteria, patient portal (e)(1), and public health reporting (f) criteria — though the platform does offer e-prescribing and patient portal capabilities through integrations (DoseSpot for prescribing, custom-built portals via the React component library).

Medplum also provides a "Provider App" — a ready-to-use clinical application built on the platform that serves as both a starting point for customization and a functional EHR for smaller practices.

### Users & Market

**Primary users**: Healthcare technology developers and engineering teams who build clinical applications. The platform also serves end-user clinicians and staff through the applications built on it.

**Target settings**: Extremely broad — the platform is used to build applications for primary care, specialty care (pediatrics, radiology, geriatrics, cardiac care), virtual-first clinics, remote health startups, diagnostics providers, and others.

**Notable customers and use cases** (from case studies):
- **Summer Health**: Pediatric care via SMS with AI-enhanced charting
- **Ro Diagnostics**: Laboratory and diagnostic workflow integration
- **Rad AI**: AI-powered radiology reporting (Medplum earned IHE IRA radiology reporting certification in 2025)
- **Develo**: Pediatric billing solutions
- **Chamber Cardio**: Cardiac care with EHR integrations
- **Flexpa**: Claims and billing interoperability (described Medplum as "the best FHIR server implementation")
- **Tia**: Women's health
- **CDC**: Government use case (listed as a customer on homepage)
- **Thirty Madison**: Multi-condition telehealth

**Scale**: Claims 20M+ patients and hundreds of practices. GitHub shows 2.1K stars, 500K+ Docker downloads, 157 contributors.

**Market position**: Small startup (12 people, YC-backed) positioned as open-source infrastructure for healthcare development. Not competing with Epic/Cerner as a turnkey EHR; competing with proprietary healthcare platforms and custom-built backends.

### Modules & Functionality

Based on Medplum's products page, documentation, and case studies, the platform includes:

**Clinical Data Repository (CDR)**
The core product — a FHIR-native data store that serves as the single source of truth for patient data. Supports all FHIR R4 resource types. Includes time-aware search, event-driven subscriptions/webhooks, and CRUD operations via REST and GraphQL APIs.

**Forms & Assessments**
Patient intake forms, clinical questionnaires, and assessments — built using FHIR Questionnaire resources.

**Scheduling**
Appointment management with customizable workflows. The 2026 roadmap indicates self-scheduling, advanced availability management, facilities scheduling, and resource scheduling are being enhanced — suggesting current scheduling is functional but being expanded.

**E-Prescribing & Medication Management**
Integrated via external partners (DoseSpot is mentioned in documentation). Medplum earned Drummond-certified EPCS (Electronic Prescribing for Controlled Substances) integration compliance. Medication tracking is a documented capability.

**Laboratory Orders & Results**
Lab ordering and results processing integrated with major lab networks (Health Gorilla is mentioned in the docs as an integration partner). CPOE for lab is a certified criterion (a)(2).

**Revenue Cycle & Billing**
Billing and claims management integrations. Case studies confirm billing use cases (Develo for pediatric billing, Flexpa for claims interoperability). The 2026 roadmap lists "high-fidelity revenue cycle solutions" as a focus area, suggesting current billing capabilities are growing.

**Messaging & Communications**
Asynchronous messaging between patients and providers. FHIR Communication resources. Summer Health's SMS-based pediatric care is built on this.

**Care Planning**
Care plan creation and management using FHIR CarePlan resources. Documented in the FHIR modeling section.

**Provider Directory & Administration**
Management of practitioners, organizations, locations, and roles.

**Identity & Access Management (Medplum Auth)**
OAuth2, OpenID Connect, SMART-on-FHIR authentication. User management and role-based access control.

**Automation (Bots)**
Server-side application logic that runs in response to events — used for workflow automation, data transformation, integration triggers.

**Interoperability**
- HL7v2/MLLP interfacing (legacy system integration)
- C-CDA document support
- FHIR APIs (R4)
- FHIRcast for real-time synchronization
- SMART App Launch
- On-premises agent for connecting to local systems

**AI Integration**
MCP (Model Context Protocol) server support introduced in 2025 for building AI copilots, scribes, and other AI-powered tools on top of clinical data.

**React UI Component Library**
Pre-built components for building healthcare UIs — a major differentiator as a developer platform.

### Data & Content

Because Medplum is a FHIR-native platform, it stores data as FHIR R4 resources. The $patient-everything operation (which serves as the EHI export mechanism) returns all resources in the FHIR Patient Compartment plus referenced resources (Organizations, Practitioners, PractitionerRoles, Locations, Medications, Devices).

Based on documented features, integrations, and case studies, the platform manages:

**Clinical data** (directly documented):
- Patient demographics (certified (a)(5))
- Encounters and visit records
- Clinical observations (vitals, lab results)
- Conditions/diagnoses
- Medications and prescriptions (via DoseSpot integration)
- Laboratory orders and results (certified (a)(2), Health Gorilla integration)
- Implantable device records (certified (a)(14))
- Care plans
- Clinical notes/charting (case studies reference AI-enhanced charting)
- Imaging references (Rad AI case study, IHE IRA certification)
- Questionnaire responses (intake forms, assessments)

**Administrative data** (directly documented):
- Scheduling/appointments
- Provider directories (practitioners, organizations, locations)
- User accounts and access logs
- Audit trails

**Financial data** (documented through case studies and integrations):
- Claims and billing data (Develo, Flexpa case studies)
- Revenue cycle data (products page lists "revenue cycle tools")

**Communication data** (directly documented):
- Patient-provider messages
- SMS-based communications (Summer Health case study)

**Key consideration for EHI completeness**: Because Medplum is a *platform*, the actual data stored varies enormously by implementation. A Summer Health deployment stores pediatric chat-based clinical data. A Rad AI deployment stores radiology reports. A Develo deployment stores pediatric billing data. The platform *can* store virtually any FHIR R4 resource type, but what any given deployment *actually* stores depends entirely on how the customer built their application.

The EHI export mechanism ($patient-everything) returns all FHIR resources in the Patient Compartment, which is a well-defined FHIR specification. This is a reasonable approach for a platform whose data model is FHIR itself — the export returns whatever FHIR resources exist for the patient, regardless of what application created them.

**Gaps / Uncertainties**:
- The website doesn't clearly describe whether Binary/document storage (PDFs, scanned documents, images) is supported and included in exports
- Remote patient monitoring data is mentioned in case studies but specifics on how device data is stored are unclear
- The degree to which billing/claims data flows through Medplum's CDR versus external billing systems is unclear — some customers may use Medplum for clinical data while billing data lives elsewhere
- No G2 or Capterra reviews were found for Medplum, likely because it's a developer platform rather than an end-user product that clinicians would review on those sites
