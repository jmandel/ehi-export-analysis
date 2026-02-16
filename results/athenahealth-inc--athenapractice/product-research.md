# athenahealth, Inc. — Product Research

Researched: 2026-02-16
Developer website: https://www.athenahealth.com

## Overview

athenahealth, Inc. is a major U.S. healthcare IT company focused on ambulatory (outpatient) care. The company was founded in 1997 and went public, then was taken private by Veritas Capital and Evergreen Coast Capital for $5.7 billion in February 2019. In 2021, it was acquired again by Hellman & Friedman and Bain Capital for $17 billion, where it remains today as a privately held company. athenahealth is headquartered in Watertown, Massachusetts, with approximately 5,000–10,000 employees.

In 2018, Veritas Capital acquired GE Healthcare's value-based care division (including the Centricity product line) for $1 billion, forming a company called Virence Health. When Veritas subsequently acquired athenahealth, it merged Virence into athenahealth. The former GE Centricity products were rebranded: **Centricity Practice Solution became athenaPractice**, **Centricity EMR became athenaFlow**, and Centricity Business became athenaIDX. These legacy products continue to be supported alongside athenahealth's flagship cloud-native platform, athenaOne.

athenahealth's network includes over 160,000 healthcare providers across more than 10,000 customer organizations, processing approximately $290 billion in annual claims. The platform supports care for more than 20% of the U.S. population. athenahealth holds approximately 7–17% of the ambulatory EHR market share (depending on measurement methodology), making it one of the top ambulatory EHR vendors alongside Epic and eClinicalWorks. Its target users are "ambulatory clinicians and support staff" per CHPL metadata.

## Product: athenaPractice

CHPL ID: 11629

### What It Is

athenaPractice is a fully integrated Electronic Health Record (EHR) and Practice Management (PM) system. It is the rebranded version of **GE Healthcare's Centricity Practice Solution (CPS)**, a well-established on-premise/client-server EHR platform with roots going back decades. Unlike athenahealth's flagship athenaOne (which is fully cloud-native), athenaPractice is architecturally a **Windows-based client-server application** that can be deployed on-premise, with server components including a database server, application server (running JBoss/Service Layer), and data exchange server for integration with external systems.

athenaPractice is certified across a very broad set of ONC criteria (35+ criteria), covering clinical data (a)(1)–(a)(5), (a)(12), (a)(14)–(a)(15); transitions of care (b)(1)–(b)(3), (b)(9), (b)(11); clinical quality measures (c)(1)–(c)(3); patient portal/view-download-transmit (e)(1), (e)(3); public health reporting (f)(1), (f)(2), (f)(5); FHIR/API access (g)(2)–(g)(7), (g)(9)–(g)(10); and direct messaging (h)(1). This breadth indicates the product is a comprehensive clinical+administrative system, not a narrow module.

### Users & Market

athenaPractice serves ambulatory practices of various specialties and sizes, from small independent practices to larger multi-site groups. It is described as focused on "provider efficiency, improving care quality, and bettering financial performance." Because it originated as GE Centricity Practice Solution — one of the most widely deployed ambulatory EHR/PM systems historically — it has a large installed base, though athenahealth has been working to migrate customers toward athenaOne over time. Third-party support firms (Med Tech Solutions, ACES Medical, TrueNorth ITG, Summit Software Technologies, eMedApps) maintain active businesses around athenaPractice, suggesting a significant ongoing user community.

### Modules & Functionality

Based on vendor materials, FHIR API documentation, and third-party sources, athenaPractice includes:

**Clinical / EHR:**
- Clinical documentation (SOAP notes, encounter charting, specialty-specific templates)
- Problem list, medication list, allergy list management
- CPOE (Computerized Provider Order Entry) for medications, labs, imaging
- E-prescribing with drug interaction and allergy alerts (Surescripts integration implied by certification criteria)
- Lab ordering and results management (bidirectional integration with external lab systems)
- Immunization tracking and registry reporting
- Family history recording
- Clinical decision support
- Care plans and care team management
- Consent management
- Device data tracking
- Specimen tracking
- Clinical impressions / assessments
- Media/image management (clinical photos, scanned documents)
- Document management (clinical documents, CCDAs, referral letters)

**Practice Management / Administrative:**
- Appointment scheduling (schedule and slot management)
- Patient registration and demographics
- Insurance/coverage management
- Patient accounting (charges, payments, adjustments, collections)
- Billing statements
- Claims submission and management (claims scrubbing with payer-specific rules)
- Eligibility verification
- Deductible tracking
- Electronic remittance processing
- Revenue cycle management analytics
- Referral management

**Patient Engagement:**
- Patient portal (view records, billing statements, prescriptions, lab results, appointment details)
- Secure messaging between patients and providers
- Automated appointment reminders (SMS, email, portal)

**Interoperability & Reporting:**
- FHIR R4 API access (g)(10) — extensive resource coverage
- C-CDA document generation and consumption for transitions of care
- Direct messaging (h)(1)
- Public health reporting: immunization registries (f)(1), syndromic surveillance (f)(2), electronic case reporting (f)(5)
- Clinical quality measure calculation and reporting (c)(1)–(c)(3), supporting MIPS/Meaningful Use
- Audit logging and provenance tracking

**Data Exchange Infrastructure:**
- Data Transfer Station for integration with external systems
- LinkLogic / Clinical Gateway for HL7 messaging
- Support for standard terminologies: LOINC, SNOMED CT, ICD-9-CM, ICD-10-CM, CPT-4, HCPCS, RxNorm, NDC, CVX

### Data & Content

The FHIR API documentation for athenaPractice reveals the breadth of data the system stores, organized into:

**Clinical data** (28 resource types): AllergyIntolerance, Binary, CarePlan, CareTeam, ClinicalImpression, Condition, Consent, Device, DiagnosticReport, DocumentReference, Encounter, FamilyMemberHistory, Goal, Immunization, Media, MedicationAdministration, MedicationDispense, MedicationRequest, MedicationStatement, Observation, Procedure, ServiceRequest, Specimen, and Provenance.

**Practice management data** (9 resource types): Account, Appointment, Coverage, Patient, Posting, RelatedPerson, Schedule, Slot — all available in athenaPractice.

**Custom/financial data** (9 resource types): Adjustment, BillingStatement, Charge, Claim, Collection, Deductible, Eligibility, PatientInsurance, Payment.

**System/configuration data** (16 resource types): AuditEvent, ConceptMap, CapabilityStatement, Endpoint, List, Location, Medication, NamingSystem, OperationDefinition, Organization, Practitioner, PractitionerRole, Provenance, Subscription, ValueSet.

This confirms the system stores comprehensive clinical records (problems, medications, allergies, immunizations, labs, imaging, procedures, encounters, family history, care plans, goals), administrative data (scheduling, patient demographics, insurance, related persons), and detailed financial/billing data (charges, claims, payments, adjustments, collections, deductibles, eligibility, billing statements).

---

## Product: athenaFlow

CHPL ID: 11663

### What It Is

athenaFlow is the rebranded version of **GE Healthcare's Centricity EMR**, a separate legacy product from the same GE Centricity lineage. While athenaPractice (formerly Centricity Practice Solution) is a combined EHR+PM system, athenaFlow (formerly Centricity EMR) originated as a more **EMR-focused** product. Both are now maintained by athenahealth following the GE/Virence acquisition.

athenaFlow has the same broad set of ONC-certified criteria as athenaPractice (35+ criteria covering clinical, care transitions, clinical quality, patient portal, public health, FHIR, and direct messaging), indicating it too is a comprehensive clinical system.

athenaFlow is also a client-server/on-premise architecture inherited from the GE Centricity platform, not athenahealth's cloud-native athenaOne.

### Users & Market

Like athenaPractice, athenaFlow serves ambulatory practices. Centricity EMR had a significant installed base when acquired from GE, and athenahealth continues to support these customers. The same third-party support ecosystem (Med Tech Solutions, eMedApps, Summit Software Technologies) serves athenaFlow clients. The product supports practices of various sizes and specialties.

### Modules & Functionality

athenaFlow shares nearly all the same functionality as athenaPractice, with one notable difference flagged in the FHIR documentation: **Schedule and Slot resources are unavailable in athenaFlow**, meaning the scheduling module is either absent or implemented differently. This aligns with Centricity EMR's historical focus as a clinical/charting tool that may have relied on separate practice management software for scheduling.

Otherwise, athenaFlow includes the same clinical capabilities:
- Clinical documentation and charting
- Problem, medication, and allergy management
- CPOE for medications, labs, imaging
- E-prescribing
- Lab integration and results management
- Immunization tracking
- Family history
- Care plans and care team management
- Document management
- Patient portal access
- Secure messaging
- FHIR R4 API access
- C-CDA generation and consumption
- Direct messaging
- Public health reporting
- Clinical quality measure support
- Standard terminology support (LOINC, SNOMED CT, ICD-10, CPT, RxNorm, etc.)

athenaFlow also includes practice management and billing resources (Account, Coverage, Patient, Posting, RelatedPerson, and the custom financial resources like Charge, Claim, Payment, etc.), suggesting that even though it originated as an EMR, it has been extended or integrated with billing/PM capabilities — or these may reflect integration with companion products.

### Data & Content

The same FHIR API resource types are available for athenaFlow as for athenaPractice, **except Schedule and Slot** (scheduling resources). This means athenaFlow stores:

- All 28 clinical resource types (same as athenaPractice)
- 7 of 9 practice management resource types (Account, Coverage, Patient, Posting, RelatedPerson — but NOT Schedule and Slot)
- All 9 custom financial resource types (Adjustment, BillingStatement, Charge, Claim, Collection, Deductible, Eligibility, PatientInsurance, Payment)
- All 16 system resource types

The absence of Schedule/Slot suggests athenaFlow may not natively manage appointment scheduling data, or may handle it differently than athenaPractice.

---

## Key Observations for EHI Export Assessment

1. **Two legacy products, one heritage**: Both athenaPractice and athenaFlow are former GE Centricity products (Practice Solution and EMR respectively), now maintained by athenahealth. They share the same FHIR API infrastructure and nearly identical data models.

2. **These are NOT athenaOne**: athenaOne is athenahealth's flagship cloud-native platform (combining athenaClinicals, athenaCollector, athenaCommunicator). athenaPractice and athenaFlow are the legacy on-premise products from the GE acquisition. They have separate architectures but share the same EHI export documentation URL.

3. **Comprehensive data scope**: The FHIR API documentation reveals these products store extensive clinical data (28 resource types), practice management data (scheduling, patients, insurance), and detailed financial/billing data (claims, charges, payments, collections, deductibles, eligibility). Any EHI export should cover all of these domains.

4. **Custom financial resources**: The presence of 9 custom (non-standard FHIR) financial resource types (Adjustment, BillingStatement, Charge, Claim, Collection, Deductible, Eligibility, PatientInsurance, Payment) is notable — this is richer financial data than many EHR FHIR APIs expose, and all of it should be in scope for EHI export.

5. **athenaFlow scheduling gap**: athenaFlow lacks Schedule/Slot resources, which may mean it doesn't store scheduling data or handles it externally.

6. **On-premise architecture**: These are Windows client-server applications, not cloud SaaS. This may affect how EHI export is implemented and accessed.
