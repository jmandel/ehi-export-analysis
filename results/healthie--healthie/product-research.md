# Healthie — Product Research

Researched: 2026-02-15
Developer website: https://www.gethealthie.com

## Overview

Healthie is a cloud-based, HIPAA-compliant EHR and practice management platform designed for health and wellness professionals, with a particular focus on virtual-first care delivery. Founded in 2016 by Erica Jain, Cavan Klinsky, and Helen Corrigan, the company has raised $42M in total funding, including a $23M Series B in 2024 led by TCV. Healthie has approximately 135 employees and serves over 25,000 active clinical providers managing more than 10 million patient records and processing over 10 million appointments.

Healthie positions itself as serving the "underdogs of healthcare" — independent practitioners, small group practices, and digital health startups that are typically underserved by legacy EHR vendors. The platform operates across two main go-to-market segments: (1) a direct SaaS product for individual clinicians and group practices, and (2) Healthie+, an API-first infrastructure offering for digital health companies that want to build custom clinical experiences on top of Healthie's backend. Key clinical specialties include behavioral health, nutrition/dietetics, women's health, chronic care management, musculoskeletal care, health coaching, substance use treatment, and longevity medicine. Notable customers include Found (weight management), Klarity Health (psychiatric services), GEM Health (sleep disorders), Isaac Health (dementia care), and Teal Health (women's health).

## Product: Healthie

CHPL IDs: 11055

### What It Is

Healthie is an all-in-one EHR, practice management, and patient engagement platform. The certified product ("Healthie Cures 1," certified 2022-12-07) appears to be the entire platform — there is no indication that the certified module is a subset of a larger product. Healthie is a single, unified cloud-hosted platform with web and mobile (iOS/Android) apps for both providers and patients. The platform is built on Ruby/Postgres with React/React Native frontends, and exposes its full functionality through a GraphQL API.

The certification profile is broad, covering clinical data (a)(3)-(5), (a)(12), (a)(14); transitions of care (b)(1)-(3); patient portal (e)(1); clinical quality measures (c)(1)-(3); FHIR APIs (g)(7)-(10); and health information exchange (h)(1). This suggests a comprehensive clinical system, not a narrow module.

### Users & Market

**Day-to-day users include:**
- Clinicians: nutritionists, dietitians, therapists, psychiatrists, health coaches, nurse practitioners, physicians across multiple specialties
- Practice administrators and billing staff
- Patients/clients (via the patient portal and mobile app)

**Settings served:**
- Solo practitioners and small group practices
- Digital health startups building virtual-first care platforms
- Multi-location wellness groups (e.g., 15+ clinicians)
- Non-profit social services organizations
- Enterprise organizations requiring scalable API infrastructure

**Scale:** 25,000+ active providers, 10M+ patient records, 10M+ appointments. Healthie's API processes approximately 400 million to 1 billion API calls per month across its developer customers.

**Case studies reveal real-world usage:**
- Klarity Health grew from 100 to 400 practices in one year using Healthie, saving $100-250K annually in development costs
- Found used Healthie's scheduling and API infrastructure to scale their weight loss program
- GEM Health used the API-first platform for virtual sleep disorder care
- Big Y (a grocery chain) used Healthie for customer wellness programming with telehealth, food journaling, and metrics tracking

### Modules & Functionality

Based on vendor materials, help documentation, third-party reviews, and case studies, Healthie includes the following functional areas:

**Scheduling & Calendar:**
- Appointment booking with automated follow-ups
- Shared team calendars with color coding (Group plan)
- Recurring appointments and availability management
- Calendar integrations

**Clinical Charting & Documentation:**
- Customizable charting note templates (multiple templates per account)
- Split-screen charting during telehealth video calls
- Chart note sharing with patients
- Group charting notes
- AI Scribe for automated clinical documentation
- CPT and diagnosis code support
- Care plan templates with multimedia support

**Intake & Forms:**
- Customizable intake forms that flow into the EHR
- Electronic forms and document collection
- Custom form building (Essentials plan and above)

**E-Prescribing (via DoseSpot integration):**
- Electronic prescribing (E-Rx) as an add-on
- Electronic Prescribing for Controlled Substances (EPCS) at $20/month on Enterprise plan
- Medication documentation and history
- Prescription Drug Monitoring Program (PDMP) access
- Allergy reconciliation

**Lab Ordering (E-Labs):**
- Integration with lab partners including Rupa Health, Evexia, and Fullscript
- Lab ordering and results management within the platform
- Lab report storage and sharing

**Insurance Billing & Revenue Cycle:**
- Superbills and CMS 1500 claim form generation (Essentials plan+)
- ClaimMD integration for eligibility checks, claims submission, real-time status updates, and ERA processing (Plus plan+, starting $25/month)
- Office Ally integration as alternative clearinghouse
- Patient insurance information capture during onboarding
- Eligibility tracking (visits, co-pays, deductibles)
- Patient invoicing and payment processing
- Support for fee-for-service, value-based care, concierge, and out-of-pocket models
- CMS 1500 reporting
- API access for custom RCM integrations (marketplace partners include Candid Health)

**Telehealth & Video:**
- HIPAA-compliant video sessions integrated with scheduling, charting, and billing
- Group telehealth sessions (Plus plan+)
- Webinar capabilities
- Mobile app support for telehealth

**Patient Portal & Engagement:**
- Secure patient login via web browser and mobile app
- Document viewing and sharing
- Secure messaging (desktop and mobile, HIPAA-compliant)
- Blast messaging and group messaging (Essentials+)
- Health programs with preset enrollment and flexible scheduling (Plus plan+)

**Food & Lifestyle Journaling (unique to Healthie's wellness focus):**
- Photo-based food logging
- Nutrient tracking powered by Edamam's database (900,000+ foods)
- Meal logging with hunger levels, perceived healthiness, mood tracking, and reflections
- Activity/workout logging
- Metrics tracking (weight, height, BMI, body fat, custom metrics)
- Graphed progress tracking over time
- Selfie logging
- Provider-configurable journaling features per client

**Wearable & Device Integrations:**
- Google Fit, Apple Health, and Fitbit sync for automatic metric tracking

**Supplement Management:**
- Fullscript integration for supplement recommendations and ordering within Healthie
- Tracking of recommended and purchased supplements

**Document Management & Fax:**
- E-Fax for sending/receiving faxes (HIPAA-compliant)
- Outbound fax (free on Essentials+), dedicated eFax with inbound/outbound (Plus+)
- Faxing of chart notes, lab reports, and documents to external providers

**Multi-Provider & Team Features:**
- Shared calendars, team member accounts, roles and permissions (Group plan)
- Internal team chat
- Care team collaboration
- Resource sharing across providers

**Reporting & Analytics:**
- Patient population data
- Business forecasting
- Usage statistics
- Customizable dashboards via API/BI tool integration

**API & Developer Infrastructure (Healthie+):**
- Full GraphQL API exposing the entire platform's functionality
- SDKs for custom front-end development
- FHIR API (via Aidbox) for interoperability
- Webhook support
- Data warehouse integration (e.g., Snowflake)
- White-label capabilities for digital health companies

**The Harbor (Integration Marketplace):**
- Built-in integrations (maintained by Healthie)
- Partner integrations via API
- Categories include billing, labs, supplements, communication, wearables

### Data & Content

Based on vendor documentation, the platform stores and manages the following data types:

- **Patient demographics and insurance information** — captured during intake/onboarding
- **Clinical chart notes** — customizable templates, shareable with patients
- **Care plans** — templates with multimedia support, progressive recommendations
- **Intake forms and questionnaires** — custom-built electronic forms
- **Medications and prescriptions** — via DoseSpot integration, including controlled substances
- **Allergy records** — reconciliation capabilities described in feature docs
- **Lab orders and results** — via Rupa Health, Evexia, Fullscript integrations
- **Diagnosis and procedure codes** — CPT and ICD codes for billing
- **Insurance claims data** — CMS 1500 forms, eligibility details, ERAs, claim status
- **Payment and billing records** — invoices, superbills, payment processing
- **Appointment/scheduling data** — bookings, availability, recurring appointments, follow-ups
- **Telehealth session data** — video session records integrated with charting
- **Secure messages** — provider-patient and internal team messaging
- **Patient portal activity** — document sharing, portal access logs
- **Food journals and meal logs** — photos, nutrient data, hunger/mood annotations, reflections
- **Activity/workout logs** — patient-submitted exercise data
- **Biometric metrics** — weight, height, BMI, body fat, custom metrics, with trend graphs
- **Wearable device data** — synced from Fitbit, Google Fit, Apple Health
- **Supplement recommendations and purchase records** — via Fullscript
- **Documents and faxes** — uploaded documents, sent/received faxes
- **Clinical quality measure data** — CMS2 depression screening mentioned specifically
- **Care team assignments** — provider-patient relationships, team collaboration records
- **Patient groups and tags** — organizational metadata
- **Program enrollment data** — health programs with scheduling and engagement tracking
- **Selfie/photo uploads** — patient-submitted images for progress tracking
- **Workflow automation configurations** — administrative automation rules
- **AI Scribe transcriptions** — automated clinical documentation

The breadth of data is notable. Healthie's wellness-specific features (food journaling, nutrient tracking, mood logging, supplement management, wearable sync) represent data categories not typically found in traditional EHRs. These are core to the product's identity and value proposition, particularly for nutrition, health coaching, and wellness practices.

**Gaps/uncertainties:**
- The website does not describe any integrated imaging or radiology module
- No mention of inpatient/hospital workflows — this is clearly an ambulatory/virtual-first product
- It's unclear how much telehealth session content (e.g., recordings, transcripts) is stored versus just session metadata
- The AI Scribe feature implies transcription data is stored, but retention and export details are not clear from marketing materials
- The specific data retained from wearable syncs (raw data vs. summary metrics) is not detailed
