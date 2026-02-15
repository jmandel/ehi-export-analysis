# Ulrich Medical Concepts — Product Research

Researched: 2026-02-15
Developer website: http://www.ulrichmedicalconcepts.com

## Overview

Ulrich Medical Concepts (UMC) is a small, privately held healthcare software company based in Paducah, Kentucky, founded in 1999 by Dr. Dennis Ulrich, a family practice physician who wanted a better alternative to paper records. The company has approximately 22 employees and an estimated annual revenue of ~$1.4M (per ZoomInfo/LeadIQ data). UMC develops and sells Team Chart Concept (TCC), an integrated EHR and practice management system targeted at ambulatory medical practices. They serve solo practitioners, mid-sized clinics, and hospital-based groups across disciplines including primary care, internal medicine, dermatology, OB/GYN, general surgery, urgent care, and therapy practices. The intended users are medical office personnel including RNs, providers, admins, and support staff.

In 2006, UMC created a subsidiary brand called **CorrecTek**, which provides correctional healthcare EHR and eMAR (electronic Medication Administration Record) software for jails, prisons, and juvenile detention centers. CorrecTek has its own product called "Spark" which is separately ONC-certified. CorrecTek appears to be a distinct product line from TCC, though they share the same parent company.

UMC also provides medical billing services — "beginning to end medical billing services" including claims, coding, billing, and financial reporting — suggesting the company functions as both a software vendor and a billing services provider.

UMC is a very small vendor with no presence on major software review platforms (G2, Capterra, Software Advice). There are no publicly available third-party reviews of TCC. The company appears to have a regional customer base, likely concentrated in the southeastern United States given its Kentucky headquarters and its documented integration with the Kentucky Health Information Exchange (KHIE) and the Kentucky Cancer Registry.

## Product: Team Chart Concept (TCC)

CHPL IDs: 10227

### What It Is

Team Chart Concept (TCC) version 7.1 is an integrated EHR and practice management system, certified on December 26, 2019. The vendor describes it as "a full-featured suite, including electronic health records, practice management, high-level clinical data and interoperability." It is designed as a single platform that combines clinical charting and administrative/billing functions. The system is available as either on-premises or cloud-hosted deployment.

TCC is certified for a broad set of 26+ ONC criteria spanning clinical data ((a)(1)-(a)(14)), transitions of care ((b)(1)), EHI export ((b)(10)), FHIR API ((g)(7)-(g)(10)), and public health reporting ((h)(1)). This indicates the certified module is a comprehensive clinical EHR, not a narrow specialty or single-function module.

The vendor positions TCC as "extremely powerful, flexible, and sophisticated" — not a "cookie-cutter EHR" — and notes that significant training (10-15 hours per person, 20 hours for financial staff) and configuration is required to get full value. Implementation takes 2-3 months for small practices.

### Users & Market

TCC serves nurse practitioners and physicians across multiple disciplines: primary care, internal medicine, dermatology, OB/GYN, general surgery, urgent care, and therapy practices. The vendor's FAQ also mentions doctors, medical providers, therapists, nurse practitioners, and physician assistants as target users. The system is designed to "engage everyone in your office, including the clerical staff, clinical practitioners, nurses and even patients."

The vendor serves solo practitioners, mid-sized clinics, and hospital-based groups. No specific customer counts are publicly available. Given the company's size (~22 employees, ~$1.4M revenue), the customer base is likely small — probably dozens to low hundreds of practices rather than thousands.

The vendor has a documented integration with the Kentucky Health Information Exchange (KHIE) and was described as "the nation's first EHR to electronically submit cancer data to a state registry" (Kentucky Cancer Registry), suggesting early adoption and strong ties to Kentucky healthcare infrastructure.

### Modules & Functionality

Based on vendor website pages (TCC Features, Capabilities, and mandatory disclosures), TCC includes the following modules and capabilities:

**Clinical / EHR:**
- Electronic health records with button-based navigation and configurable workflow
- Rapid documentation of encounter notes with customizable clinical templates
- Health maintenance alerts and reminders
- Risk factor analysis
- Implantable device list management
- Decision support interventions (clinical decision support)
- Drug-drug and drug-allergy interaction checking
- Clinical quality measures dashboard with automated tracking (6 CQMs supported)
- Support for dictation, voice recognition, and handwriting recognition input methods
- Multi-user simultaneous chart access

**Prescribing:**
- Electronic prescribing (e-prescribing) — via **NewCrop** (a third-party e-prescribing service by DrFirst), listed as an add-on with per-prescriber monthly fees

**Orders:**
- Computerized provider order entry (CPOE) for medications, laboratory, and diagnostic imaging
- Bi-directional lab connectivity for orders and results
- Interfacing with labs, pharmacies, rehabilitation and post-acute care facilities

**Practice Management & Billing:**
- Appointment scheduling for multiple providers, locations, and equipment
- Integrated billing with "full HIPAA compliant billing routines"
- **SmartCoder** claims scrubbing tool
- ICD-10 ready
- PQRS-capable
- Standard and ad hoc reporting, plus "User Defined Records" for custom reportability

**Document Management:**
- Integrated document management system for patient charts, office forms, and documents
- Historical data scanning and digitization services (offered as a service)

**Patient Engagement:**
- Patient portal — via **Medfusion** (third-party), listed as an add-on with monthly service fees
- Partnership with **Bridge** (BridgeInteract) for enhanced patient engagement, mobile accessibility, and patient communication
- Direct patient communication features

**Interoperability & Data Exchange:**
- Transitions of Care (C-CDA)
- Direct Messaging — listed as an add-on with per-address monthly fees
- Health Information Exchange connectivity (documented KHIE integration)
- HL7 messaging and Clinical Document Architecture (CDA) support
- FHIR API access (Application Access API) — listed as an add-on with monthly service fee
- Multi-facility connectivity with labs, pharmacies, hospitals, imaging centers

**Public Health Reporting:**
- Cancer registry reporting (historically first to Kentucky Cancer Registry)
- Certified for (h)(1) — transmission to public health agencies

**Platform:**
- Windows-based with Windows Tablet support for mobile access
- Ribbon-style interface
- On-premises or cloud-hosted deployment
- Multi-level security: Windows login, TCC login, department-based access controls
- HIPAA compliant with encryption

### Data & Content

Based on the features and modules documented above, TCC manages the following categories of data:

**Clinical data:** Patient demographics, encounter notes, problem lists, medication lists, allergy lists, immunization records, vital signs, health maintenance records, implantable device lists, clinical decision support rules and alerts, clinical quality measure data.

**Order data:** Lab orders and results (bi-directional), medication orders, diagnostic imaging orders. Lab connectivity implies storage of lab results.

**Prescribing data:** E-prescriptions via NewCrop integration, medication history, drug interaction checking data.

**Practice management data:** Appointment schedules (multiple providers/locations/equipment), billing records, claims data (with SmartCoder scrubbing), financial reports, ICD-10 codes, PQRS quality data.

**Document management:** Scanned documents, office forms, patient chart documents, digitized historical records.

**Patient engagement data:** Patient portal interactions (via Medfusion), patient communications (via Bridge integration), direct messaging.

**Interoperability data:** C-CDA documents, HL7 messages, CDA documents, FHIR resources, health information exchange transactions, public health submissions.

**Notable observations on data scope:**
- E-prescribing (NewCrop), patient portal (Medfusion), direct messaging, and FHIR API access are all listed as separate add-ons with additional fees on the mandatory disclosures page. This means they may not be deployed at all customer sites, but the data they generate is part of what TCC can store.
- The vendor also provides medical billing services, so billing data appears to be a core part of the product, not an afterthought.
- The website does not explicitly mention faxing, referral management, or patient messaging/secure messaging as distinct features (beyond the Bridge partnership and patient portal).
- There is no mention of behavioral health-specific features, although therapists are listed as a target user group.
- No mention of imaging storage (PACS) — only imaging orders. The system interfaces with imaging centers but likely does not store images itself.
