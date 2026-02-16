# PracticeSuite, Inc. — Product Research

Researched: 2026-02-16
Developer website: https://www.practicesuite.com

## Overview

PracticeSuite, Inc. is a privately held, cloud-based medical office software company headquartered in Tampa, Florida (originally founded in Silicon Valley/Newark, California in 2004). The company has approximately 200 employees across offices in North America, Asia, and Europe. PracticeSuite claims over 92,000 medical professionals use its platform, processing over $10 billion in claims annually. Other sources cite 41,000 office managers, medical billers, physicians, and RCM companies across 150 billing specialties and over 61 clinical EHR specialties. The company serves independent physician practices, medical billing companies, and multi-specialty groups.

PracticeSuite offers an integrated, cloud-based platform combining practice management, ONC-certified EHR, patient portal, patient engagement tools, telehealth, and revenue cycle management (RCM) services. They also operate **FreeChiro**, a chiropractic-focused brand built on the same underlying PracticeSuite platform, marketed to chiropractors with a free base tier.

## Product: PracticeSuite

CHPL ID: 10788
CHPL Product Number: 15.02.05.2198.PRAS.01.01.1.220113
Version: EHR-18.0.0
Certification Date: 2022-01-13

### What It Is

PracticeSuite is a cloud-based, fully integrated medical practice management and EHR platform. The ONC mandatory disclosures page describes it as "a cloud based full suite of Practice Management, Certified EHR, Portal, Kiosk, and Online Review Management system" offered via monthly subscription. The certified module covers a broad range of criteria: clinical data (a)(1)–(a)(14), transitions of care (b)(1)–(b)(3), patient portal (e)(1), clinical quality measures (c)(1)–(c)(4), public health reporting (f)(1)–(f)(2), and FHIR APIs (g)(7)–(g)(10)) — 40+ criteria total. This is a comprehensive ambulatory EHR certification, not a narrow module.

The platform requires integration with several third-party components for full functionality: NewCropRx (e-prescribing), EMRDirect (direct messaging), and HelloHealth (patient engagement). Additional fees apply for direct messaging and the patient engagement platform.

### Users & Market

PracticeSuite targets independent physician practices, new medical practices, and medical billing companies. It supports 25+ clinical specialties including cardiology, dermatology, orthopedics, psychiatry, and many others. The intended users (per the SED description) are "healthcare providers in private practices." Day-to-day users include physicians, nurses, office managers, medical billers, and patients (via the portal).

The company claims 92,000+ medical professionals on the platform. They sell direct and also offer outsourced revenue cycle management services for practices that want billing handled for them.

### Modules & Functionality

Based on vendor website pages, the mandatory disclosures page, and third-party reviews:

**EHR/Clinical:**
- Single-screen encounter charting with customizable workflows (point-and-click, voice recognition, templates)
- Library of 30+ customizable EMR templates
- Clinical dashboards showing patient data in a consolidated view
- Medical history, diagnoses, medications, lab results, treatment plans
- CPOE for medications, lab orders, and imaging orders (certified for (a)(1)–(a)(3))
- Drug-drug and drug-allergy interaction checking (certified for (a)(4))
- Demographics, family health history recording (certified for (a)(5), (a)(12))
- Clinical decision support (certified for (a)(9))
- Implantable device tracking (certified for (a)(14))
- Task management / electronic to-do lists (signing encounters, authorizing prescriptions, etc.)

**E-Prescribing:**
- Electronic prescriptions sent to pharmacies via NewCropRx
- Access to "the nation's largest and most active e-prescribing network"
- Real-time prior authorizations, prescription benefits, and PDMP data for controlled substances

**Lab Integration:**
- Electronic lab orders and results with major lab providers (Labcorp, Quest Diagnostics)
- Direct submission, assignment, and viewing of lab orders/results

**Practice Management / Scheduling:**
- Resource-based appointment scheduling across multiple providers and locations
- Customizable color-coded appointment types and statuses
- Patient registration
- Insurance eligibility verification (automated and on-demand)
- Patient flow management

**Billing & Revenue Cycle:**
- Charge entry (integrated from EHR or manual)
- Claims dashboard with denied claims tracking and resubmission
- Mass corrections for claim submissions
- Charge validation to reduce denials
- Collections Manager for payment tracking and application
- Integrated credit card processing for patient payments
- Cases designation to separate different payers
- 140+ reports on practice performance and financial metrics (Report Central)
- Drill-down financial reporting, cash-flow-blockage reporting, KPI reporting
- "PULSE MONEY MONITOR" system for revenue leak alerts
- AI-powered claim processing and denial reduction

**Patient Portal & Engagement (powered by HelloHealth):**
- HIPAA-secure patient portal with access to records, labs, and medical records
- Online appointment scheduling
- Digital check-in / kiosk functionality
- Prescription refill requests
- Two-way patient chat (SMS conversations with office staff)
- Broadcast messaging for practice-wide notifications
- Customizable appointment reminders and no-show reengagement
- Patient satisfaction surveys
- ePayments and e-Statements
- Online review/reputation management

**Telehealth:**
- HIPAA-compliant video chat and phone consulting
- Integrated with single-screen charting tool for virtual care documentation

**Data Exchange / Interoperability:**
- Transitions of care / C-CDA document exchange (certified for (b)(1)–(b)(3))
- Clinical information reconciliation
- Direct messaging via EMRDirect
- Electronic referrals
- e-Faxing
- FHIR API access (certified for (g)(7)–(g)(10))
- Immunization registry reporting (certified for (f)(1))
- Syndromic surveillance reporting (certified for (f)(2))

### Data & Content

Based on the features and certifications described above, PracticeSuite stores and manages:

- **Clinical data**: Patient demographics, medical history, family health history, diagnoses/problem lists, medications, allergies, lab orders and results, imaging orders, encounter/visit notes, treatment plans, vital signs, clinical decision support alerts, implantable device information
- **Prescription data**: E-prescriptions (including controlled substances), prior authorization data, PDMP data, prescription refill requests — via NewCropRx integration
- **Billing/financial data**: Insurance information, eligibility verification results, charges, claims (submitted, denied, corrected), payments, collections, patient statements, credit card transactions, financial reports, KPI data
- **Scheduling data**: Appointments, provider schedules, appointment types/statuses, patient check-in data
- **Patient registration**: Demographics, insurance cards, consent forms, intake forms
- **Patient portal data**: Portal messages/chat transcripts, appointment requests, prescription refill requests, patient-completed forms, patient satisfaction survey responses
- **Telehealth data**: Video/phone consultation records, telehealth encounter documentation
- **Documents**: e-Faxes, referral documents, C-CDA transition of care documents
- **Quality measures**: Clinical quality measure data for reporting (certified for CQMs)
- **Public health reporting**: Immunization data, syndromic surveillance data
- **Audit/security**: Access logs, authentication records, audit trails (certified for (d) criteria)

The mandatory disclosures page notes that the system's real-world testing covers interoperability, e-prescribing, quality measures, immunization transmission, and API access — confirming active use of these data categories.

---

## Product: FreeChiro

CHPL ID: 10789
CHPL Product Number: 15.02.05.2198.FREC.01.02.1.220113
Version: EHR-18.0.0
Certification Date: 2022-01-13

### What It Is

FreeChiro is a chiropractic-focused brand of the PracticeSuite platform, marketed separately at freechiro.com. It shares the same underlying software (identical version EHR-18.0.0, identical certification date, and identical certified criteria as PracticeSuite). FreeChiro describes itself as "a Silicon Valley founded Technology Company dedicated to providing the chiropractic community with awesome software and even better support." The key differentiator is branding and pricing: FreeChiro offers a free base-level ONC-certified tier for chiropractors, with a paid tier at $149/month per user for the fully integrated system with practice management, EHR/EMR, and billing.

The same contact phone number ((813) 607-2800 for PracticeSuite, (813) 607-2255 for FreeChiro — both Tampa area codes) and the PracticeSuite Inc. company attribution confirm this is the same company and platform.

### Users & Market

FreeChiro specifically targets chiropractors, though its underlying platform supports 55+ medical specialties. The free tier is a customer acquisition strategy — most chiropractors would need the paid tier for full functionality. A third-party review on ChiroMonkey noted that because the software is designed for 55 specialties, "it fails to meet the specific needs of chiropractors when it comes to reporting." The same review criticized the interface as "poorly designed, non-intuitive and archaic appearing." The ChiroMonkey listing showed 0 user reviews, suggesting limited adoption in the chiropractic community specifically.

### Modules & Functionality

FreeChiro's functionality is essentially identical to PracticeSuite's (see above), as it is the same platform with chiropractic-specific branding. Per the ChiroMonkey listing and other sources, it includes:

- Practice scheduling
- Medical billing and insurance processing
- Electronic health records / EMR with customizable templates
- Patient data management
- Analytics tools
- Mobile-compatible (Android and iOS)

The free tier likely includes a subset of these features, with the full suite available at the paid tier.

### Data & Content

As FreeChiro shares the same platform and certification as PracticeSuite, it stores the same categories of data described above for PracticeSuite. The chiropractic-specific usage would emphasize encounter notes for chiropractic visits, treatment plans, and potentially specialty-specific templates, but the underlying data model and storage capabilities are identical.

---

## Research Gaps & Notes

- **Third-party review coverage is thin**: Capterra returned a 403 error; G2 did not appear in search results for PracticeSuite. The EMRSystems.net review site had only 5 reviews. The product appears to have limited presence on major review aggregators compared to larger EHR vendors.
- **FreeChiro adoption unclear**: Despite being marketed as a free chiropractic EHR, evidence of significant chiropractic market adoption is sparse. The ChiroMonkey listing had zero user reviews.
- **HelloHealth integration depth**: The patient engagement features are "powered by HelloHealth," and the mandatory disclosures page lists HelloHealth as requiring additional fees. It's unclear how tightly integrated HelloHealth data is with the core PracticeSuite database — whether patient chat, surveys, and engagement data are stored in the same system or in a separate HelloHealth database.
- **NewCropRx integration**: E-prescribing data flows through NewCropRx. The extent to which prescription data is replicated back into PracticeSuite's own database vs. remaining in NewCropRx is unclear.
- **Kiosk module**: The mandatory disclosures mention "Kiosk" as part of the suite, but vendor website pages don't describe it in detail. This likely relates to the digital check-in / patient intake workflow.
