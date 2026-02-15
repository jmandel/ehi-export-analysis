# Careexpand LLC — Product Research

Researched: 2026-02-15
Developer website: https://www.careexpand.com

## Overview

Careexpand LLC is a small health IT company founded in 2016 and headquartered in Plano/Dallas, Texas. The company has approximately 1–10 employees (per ZoomInfo) and a listed team of about 16 people on their website, including CEO Javier Vinals, CTO Pablo Vinals, and Chief Software Strategist Ameya Parab. The company secured initial funding in 2018, launched a beta in 2019, and released a "full-suite version with integrated modules" in 2024. They received ONC certification in April 2025, making them a very recently certified product.

Careexpand positions itself as "the operating system for continuity of care" — a cloud-based SaaS platform integrating EHR, telemedicine, care coordination, and practice management. They market to individual doctors, small clinics, healthcare payers, and large health systems. The website claims 20,000+ registered users, though this likely refers to patient portal registrations rather than clinical users. The platform operates in English and Spanish.

The company is a startup-stage vendor with no presence on major review aggregator sites (G2, Capterra, GetApp). There are no identifiable third-party reviews. No notable customers or case studies were found beyond generic testimonial quotes on the vendor's website. There is no evidence of acquisitions, mergers, or white-labeling. The product appears to be a proprietary, ground-up build.

## Product: Careexpand

CHPL IDs: 11625 (15.04.04.3226.Care.24.00.1.250422)

### What It Is

Careexpand is a cloud-based, all-in-one healthcare platform combining EHR, telemedicine, remote patient monitoring (RPM), care coordination, and practice management. The certified module covers the full platform — it is not a component of a larger product. The product is offered in three pricing tiers that reflect escalating functionality:

1. **Telemedicine Plan** ($49/mo per provider) — Video/phone consultations, basic scheduling
2. **Continuity of Care Plan** ($149/mo per provider) — Adds care coordination, referral management, follow-up protocols
3. **Full Practice Management Plan** ($249/mo per provider) — Adds EHR, e-prescribing, lab orders, billing, reporting, CQMs

An additional Change Healthcare/Optum integration is available for $65/mo per provider for orders.

### Users & Market

**Intended users** (per CHPL): Providers, FNPs, Clinicians.

**Target settings**: Individual doctors, small clinics, multi-provider groups, and (aspirationally) larger health systems and payer organizations. The enterprise page targets health systems, payers, provider networks, and retail/DTC brands — though it's unclear how many enterprise clients they actually serve.

**Market position**: Very small, startup-stage vendor. No identifiable market share data. Not listed on KLAS, G2, Capterra, or other review platforms. The 20,000+ users figure on the website likely includes patient accounts, not just clinical users.

**Clinical settings**: Appears focused on ambulatory/outpatient care, with emphasis on primary care, chronic disease management (diabetes, hypertension), and urgent care. No evidence of inpatient, surgical, behavioral health, or specialty-specific modules.

### Modules & Functionality

Based on vendor website and mandatory disclosures page:

**Electronic Health Records (EHR)**
- Patient demographics management (certified (a)(5))
- Clinical documentation with AI-assisted automated coding and metatags
- Problem lists, medication lists, allergy lists (implied by CCDA/transitions of care certification)
- Implantable device tracking (certified (a)(14))
- CPOE for medications (certified (a)(1))
- Ultra-customizable interface for specialists and family medicine

**E-Prescribing & Lab Orders**
- AI-assisted electronic prescribing
- Pre-configured protocols for common conditions (diabetes, hypertension)
- Lab order integration
- Change Healthcare/Optum integration for orders ($65/mo add-on)

**Telemedicine**
- Video and phone consultations
- Virtual waiting rooms
- Multi-channel messaging
- Patient portal with web/mobile access

**Care Coordination & Continuity of Care**
- Automated referral suggestions based on patient history and physician patterns
- Follow-up protocol recommendations
- Care plan management (certified (b)(11))
- Transitions of care / C-CDA exchange (certified (b)(1))
- Direct messaging for health information exchange (certified (h)(1))

**Remote Patient Monitoring (RPM)**
- Device delivery and configuration (mentioned but specifics not detailed)
- Clinical monitoring and alerts
- Continuous tracking for chronic conditions (diabetes, hypertension, heart disease mentioned)
- Specific devices and metrics not enumerated on the website

**Scheduling & Patient Engagement**
- Unified scheduling and workflow calendar (in-person and remote)
- Automated appointment reminders
- Patient portal with health information access
- Personalized engagement campaigns

**Billing & Reporting**
- Automated billing solutions (mentioned on the doctors use-case page)
- Performance reporting within EHR
- Clinical Quality Measures (CQMs) — certified for (c)(1), with specific CQMs for pediatric weight/nutrition counseling and diabetes HbA1c monitoring
- Value-based care program support

**Integrations & Interoperability**
- FHIR R4 API (certified (g)(10))
- HL7 connectors
- Integration with existing EMR systems (marketed as a feature for enterprise tier)
- Auth0 for authentication
- Change Healthcare / Optum Clinician integration

**Security & Administration**
- HIPAA and SOC 2 compliant infrastructure
- Role-based access control
- Multi-factor authentication
- Audit logging, automatic logoff, encryption (certified (d) criteria)

### Data & Content

Based on certified criteria and vendor descriptions, Careexpand stores and manages the following data:

**Clinical data** (evidenced by certifications and feature descriptions):
- Patient demographics (a)(5)
- Medication orders/CPOE data (a)(1)
- Implantable device lists (a)(14)
- Care plans (b)(11)
- Clinical notes and encounter documentation (described in EHR features)
- Problem lists, medication lists, allergy lists (implied by C-CDA transitions of care (b)(1))
- Lab orders (described in e-prescribing/lab features)
- Prescription data (e-prescribing feature)
- Clinical quality measure data (c)(1)

**Telemedicine/communication data** (described in features):
- Video/phone consultation records
- Multi-channel messages between providers and patients
- Patient portal communications
- Direct messaging (h)(1)

**RPM data** (described in RPM features):
- Remote monitoring device readings (specifics not enumerated — diabetes, hypertension, heart disease mentioned as target conditions)
- Clinical alerts from monitoring

**Administrative data** (described in practice management features):
- Scheduling/appointment data
- Billing data (mentioned but details thin — unclear if full claims/billing is built-in or relies on integrations)
- Referral tracking data
- Workflow/task management data

**Security/audit data** (certified (d) criteria):
- Authentication logs
- Audit trails
- Access logs

**Notable gaps in clarity**:
- The billing capability is mentioned repeatedly but never described in depth. It's unclear whether Careexpand has a full practice management billing system (claims submission, ERA/EOB processing, patient statements) or whether "billing" refers to simpler charge capture that relies on the Change Healthcare/Optum integration for actual claims processing. The $65/mo add-on for Change Healthcare suggests the latter.
- RPM device specifics are not detailed — it's unclear what device types, vitals, or biometric data are actually captured and stored.
- The website does not mention patient documents/imaging storage, faxing, or scanned document management.
- No mention of inventory management, immunization registry reporting, or syndromic surveillance despite some products in this space offering these.
- The distinction between what the platform stores natively vs. what flows through integrations (e.g., Change Healthcare for orders) is unclear.

---
