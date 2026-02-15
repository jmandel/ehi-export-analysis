# Avon Health — Product Research

Researched: 2026-02-15
Developer website: https://www.avonhealth.com

## Overview

Avon Health is a startup founded in 2021, headquartered in New York, NY, by Maitreyee Joshi (CEO, Carnegie Mellon CS graduate, former Product Manager at PathAI). The company builds an "AI-first" all-in-one EMR and practice management platform targeting modern ambulatory care delivery — from solo primary care clinics to virtual care companies. The website claims "100,000+ providers, patients, and high-growth businesses" use the platform, though this metric combines providers, patients, and organizations, so the actual provider count is unclear and likely much smaller. Sequoia Capital is mentioned as a supporter/investor.

Avon Health positions itself as a next-generation, cloud-based, customizable EMR for ambulatory practices across multiple specialties. The company is small — no specific employee count was found, and the product was only ONC-certified in May 2025, suggesting it is relatively early-stage. No reviews were found on Capterra, G2, or KLAS, which is consistent with a young startup that hasn't yet accumulated significant market presence in traditional EHR review channels.

Note: There is an unrelated product called "AvonEHR" (avonehr.com) focused on integrative/functional medicine — this is a completely different company and product.

## Product: Avon EMR

CHPL IDs: 11636 (15.04.04.3227.Avon.01.00.1.250514)

### What It Is

Avon EMR is a cloud-based, all-in-one electronic medical record and practice management platform. It is described as "AI-first by design" and "infinitely customizable" with a modular architecture — modules can be toggled on/off depending on practice needs. The certified module appears to be the entire product (there's no indication of separate uncertified components making up a larger suite). The product is the EMR itself, which includes clinical documentation, practice management, patient engagement, and revenue cycle management all in one platform.

The system is certified for a broad set of ONC criteria: clinical data management (a)(1)-(a)(5), (a)(12), (a)(14); transitions of care (b)(1)-(b)(2); care plan exchange (b)(11); clinical quality measures (c)(1)-(c)(3); patient portal/VDT (e)(1); patient health information export (e)(3); FHIR API (g)(10); and immunization registry reporting (h)(1). This breadth is consistent with a full-featured ambulatory EMR.

### Users & Market

**Target users**: Physicians, physician assistants, nurse practitioners (per SED description), plus practice managers and billing staff based on functionality.

**Clinical settings**: Ambulatory care across multiple specialties — primary care, behavioral health, women's health, chronic care management, pediatrics, specialty care, hospice, and geriatrics. The vendor emphasizes serving both traditional brick-and-mortar practices and virtual/telehealth-first care delivery companies.

**Scale**: Marketed to practices ranging from solo clinics with ~400 patients to virtual care companies with 100,000+ patients. The "100,000+ providers, patients, and high-growth businesses" claim on the homepage is ambiguous and likely includes patient users of the portal.

**Notable customers**: None identified. No case studies or named customers were found on the website or in third-party sources. The vendor website includes testimonials but without identifying specific organizations.

**Market position**: Early-stage startup. No presence on major EHR review platforms (Capterra, G2, KLAS). The recent ONC certification (May 2025) and lack of third-party reviews suggest a company still building its customer base.

### Modules & Functionality

The product is organized into toggleable modules documented on the vendor's guides site (guides.avonhealth.com). Based on the vendor website, documentation, and pricing page, the platform includes:

**Clinical Documentation**
- Visit notes — clinical encounter documentation
- Care plans — treatment planning
- Documents — document storage and management
- AI Scribe — records clinician-patient interactions and auto-generates visit note drafts (Pro/Enterprise tier feature)

**Prescriptions & Medication Management**
- E-prescribing (via integration, listed as pass-through pricing)
- Prescription fulfillment tracking

**Laboratory & Imaging**
- Lab orders — can send to 1000+ labs across the country with parsed results returned into the platform (pass-through pricing)
- Imaging orders
- Mobile phlebotomy scheduling
- At-home test kit management

**Scheduling**
- Virtual and in-person appointments
- One-time or recurring visits
- Individual or group sessions
- Intelligent provider matching (license type, location, availability, time zone)
- Patient self-scheduling
- Automated confirmations and reminders
- Integrated video visits
- Calendar sync with external calendars

**Patient Engagement**
- Patient portal — view medical records, schedule appointments, message care team, complete forms, view educational content
- Caregiver portal
- Messaging — in-app, 2-way SMS, internal notes
- Forms and intake forms with embedded logic
- Courses — patient education content delivery
- SMS and email notifications

**Practice Management & Billing**
- Revenue cycle management (pass-through pricing)
- Eligibility checks / insurance verification (pass-through pricing)
- Invoicing
- Superbills
- E-faxing (pass-through pricing)
- Payment collection

**Analytics & Reporting**
- Real-time dashboards for clinical, operational, and financial metrics
- Filtering by provider, patient, or date
- Drill-down from KPIs to patient-level data
- Export and sharing of reports
- AI Data Analyst for insights generation (Pro/Enterprise tier)
- One certified clinical quality measure (depression screening — PHQ-9/PHQ-A)

**Administration & Configuration**
- Role-based access controls
- Peer groups and triage teams
- Brand settings customization
- Appointment type configuration
- Billing provider and service facility setup
- Task assignment and collaboration

**Integrations & Extensibility**
- FHIR API (g)(10) certified
- Full API access (all tiers)
- Webhooks
- Custom code and custom pages (low-code/no-code extensibility)
- Custom fields
- Automations
- Epic integrations mentioned
- Direct messaging and HIE integrations (Pro/Enterprise tier)
- Uses EMR Direct for clinical messaging
- Uses AccessGUDID for device identification

**Security & Compliance**
- ONC certified
- SOC 2 compliant
- HIPAA/BAA compliant
- PCI compliant
- Multi-factor authentication (email/password + SMS OTP)
- WCAG 2.1 AA accessibility compliance

### Data & Content

Based on the modules and features described above, Avon EMR stores and manages the following categories of data:

**Clinical data** (directly evidenced by certified criteria and feature descriptions):
- Patient demographics (a)(5)
- Problem lists (a)(1) — SNOMED CT
- Medication lists (a)(1)
- Medication allergy lists (a)(1)
- Clinical decision support rules (a)(2)
- Drug-drug and drug-allergy interaction checks (a)(4)
- Visit notes / encounter documentation
- Care plans
- Clinical documents
- Lab orders and parsed lab results (from 1000+ labs)
- Imaging orders and requisitions
- Vital signs
- Immunization records (h)(1) — reports to registries
- Smoking status
- Health information from transitions of care (b)(1)/(b)(2) — C-CDAs
- Clinical quality measure data (c)(1)-(c)(3) — at minimum depression screening (PHQ-9/PHQ-A)

**Prescription data** (evidenced by e-prescribing module):
- Electronic prescriptions
- Prescription fulfillment tracking
- Medication history (implied by e-prescribing integration)

**Scheduling data** (evidenced by scheduling module):
- Appointments (virtual, in-person, recurring, group)
- Provider schedules and availability
- Calendar sync data
- Appointment reminders and confirmations

**Patient engagement data** (evidenced by portal and messaging features):
- Patient portal messages
- In-app messages
- SMS messages (2-way)
- Intake form submissions
- Patient education course progress
- Patient-generated data from forms

**Financial/billing data** (evidenced by RCM and billing features):
- Insurance eligibility information
- Invoices
- Superbills (procedure codes, diagnosis codes)
- Payment records
- Revenue cycle management data

**Administrative data** (evidenced by platform features):
- User accounts and roles
- Audit logs (d)(2)
- Task assignments
- Fax records
- Automation configurations
- Custom field data

**Analytics data** (evidenced by analytics module):
- Dashboard configurations
- Clinical, operational, and financial metrics
- Reporting data

**AI-generated content** (Pro/Enterprise tiers):
- AI Scribe transcriptions and generated note drafts
- AI Data Analyst query results

The pricing model reveals a distinction between core platform features (included in subscription) and transactional services (e-prescribing, lab orders, eligibility checks, e-faxing, RCM) that operate on pass-through pricing. This suggests these integrations flow through third-party services but the data is stored within the Avon EMR platform.

**Gaps/uncertainties**: The vendor website does not mention specific specialty-specific templates or content (e.g., behavioral health assessments, OB/GYN-specific forms) despite listing these as target specialties. It's unclear how deeply the product serves each listed specialty versus being a general-purpose platform. No information was found about data archiving, data retention policies, or the specific database architecture.
