# Glenwood Systems LLC — Product Research

Researched: 2026-02-16
Developer website: http://www.glenwoodsystems.com

## Overview

Glenwood Systems LLC is a privately held healthcare IT company headquartered in Waterbury, Connecticut. Founded in 1998 (now 27+ years in operation), the company provides EHR, practice management, revenue cycle management, and related services to ambulatory medical practices, surgical centers, and hospitals across the U.S. The company reports approximately $17.3 million in revenue and 162 employees (per Dun & Bradstreet/ZoomInfo). Their website claims "hundreds of satisfied clients," though no precise customer count is published.

Glenwood Systems offers a suite of products under the "Glace" brand: GlaceEMR (the certified EHR), GlaceRCM (revenue cycle management/billing services), GlaceOffice (practice administration tools), GlaceScribe (AI-powered transcription using Amazon HealthScribe), GlaceGrow (digital marketing for patient acquisition), GlacePhoneSmart (automated phone/task handling), and GlaceBillSmart (AI billing automation). The company primarily targets small-to-mid-size ambulatory practices and positions itself as an all-in-one solution combining clinical, billing, and administrative functions.

## Product: GlaceEMR

CHPL ID: 9559

### What It Is

GlaceEMR is a cloud-based, ONC-certified electronic health records system that combines clinical documentation with practice management capabilities. It is certified as a Complete EHR (per the CHPL product number prefix 15.04.04) with extensive certification across 40+ criteria spanning clinical data (a)(1)-(5), (a)(12), (a)(14)-(15); transitions of care (b)(1)-(3), (b)(7)-(9); patient portal (e)(1), (e)(3); public health reporting (f)(1)-(2), (f)(4)-(5), (f)(7); CQMs (c)(1)-(4); and FHIR API access (g)(7), (g)(9)-(10). The intended users are "Outpatient Clinic" staff per the CHPL metadata.

GlaceEMR is the core clinical module, but it is part of the larger Glace product ecosystem. The certified module appears to encompass both the clinical EHR and integrated practice management/billing functionality — the transparency disclosure describes it as including "clinical documentation, eRX, patient portal, hosting, and maintenance" in the base package, with billing/RCM services available as add-ons (GlacePremium and GlaceComplete tiers). The product is offered in multiple service tiers: GlaceBasic, GlacePremium, GlacePremium+, GlaceComplete, and GlaceEnterprise.

### Users & Market

GlaceEMR targets ambulatory outpatient practices across multiple specialties. The vendor's marketing specifically calls out podiatry, psychiatry/behavioral health, internal medicine, urgent care, cardiology, neurology, ophthalmology, rheumatology, and general surgery. The behavioral health module is particularly detailed, suggesting it's an important vertical. The vendor also mentions serving surgical centers and hospitals, though the primary market appears to be ambulatory practices.

End users include physicians (MDs/DOs), nurse practitioners, practice managers, office managers, and billing staff. The system has a patient portal for patient-facing access as well. The product is cloud-based, accessible across devices including a smartphone app for mobile access.

No specific customer counts are published, but the vendor claims "hundreds of satisfied clients" and 24+ years of operation. Pricing starts at $54/month per provider for the base EMR, scaling up to $1,000/month for GlaceBasic, with GlacePremium/GlaceComplete tiers using a revenue-sharing model (percentage of collected revenue or monthly minimum, whichever is greater).

### Modules & Functionality

Based on vendor materials, product pages, the transparency disclosure, and third-party review sites, GlaceEMR includes the following modules and capabilities:

**Clinical Documentation**
- Hundreds of pre-built specialty-specific templates (customizable)
- AI-integrated documentation assistance including scribing, dictation-to-form, auto-coding, and document generation (powered in part by Amazon HealthScribe via GlaceScribe)
- Custom templates, pre-filled reusable templates, shortcuts, and order-sets
- Clinical decision support with data summarization and analytics

**Scheduling**
- Integrated appointment scheduler managing clinical slots across multiple resources
- Multi-channel appointment reminder system (reduces no-shows)
- Group therapy scheduler (behavioral health)
- Telehealth appointment scheduling

**E-Prescribing**
- Electronic prescriptions via SureScripts integration
- EPCS (Electronic Prescribing of Controlled Substances) with two-way authentication and biometric verification
- PMP (Prescription Drug Monitoring Program) support
- Pharmacy refill request handling
- Multum Lexi-Data integration for drug data

**Patient Portal**
- Two-way patient-provider communication/messaging
- Appointment scheduling
- Prescription refill requests
- Lab results viewing
- Contactless check-in and KIOSK functionality

**Lab Integration**
- "Glenwood standard lab interface program" for lab order/result exchange
- Medical device interfaces
- Integration with partner healthcare entities

**Billing & Practice Management**
- Integrated billing and coding module for electronic claims submission
- ICD-10 and ICD-9 code support
- Two-way data flow between clinical and billing modules ("cleaner billing claim submission information for improved claim collection results")
- Charge capture integrated with clinical documentation
- Patient balance collection (eBills, text reminders, patient portal, kiosk terminals)
- Eligibility verification

**Revenue Cycle Management (add-on tiers)**
- GlacePremium and GlaceComplete offer full RCM billing services
- GlaceRCM handles charge capture through claim resolution
- Denial management with pattern-learning software
- A/R tracking and management
- Analytics and transparent reporting dashboards
- Accepts charges from GlaceEMR, third-party EMRs, mobile devices, and rounding software

**Telehealth**
- Comprehensive telemedicine module from scheduling through billing
- Video call/conferencing functionality
- Virtual receptionist

**Behavioral Health (specialty module)**
- Group therapy management and scheduling
- Mental Status Exam, Advanced Treatment Plan, screening templates
- PHQ-9, BIMS, Mini Mental Status Exam, suicidal assessment protocols
- DSM-5 assessments
- Addiction management templates
- Treatment plan and goal tracking with objective benchmarks
- Case manager resource allocation analysis

**Quality Reporting & Compliance**
- MIPS/MACRA capture and dashboard
- PCMH and ACO program support
- Meaningful Use attestation support
- Clinical quality measure (CQM) reporting
- Care Coordination Management (CCM) module
- Remote Patient Monitoring (RPM) module
- Public health reporting (immunization registries, syndromic surveillance, cancer/specialized registries)

**Practice Administration (via GlaceOffice add-on)**
- HR management, recruiting, credentialing
- Payroll administration, bookkeeping (AP/AR/reconciliation)
- Payment gateway for patient payments
- Email and fax routing/tracking
- Internet and telephony systems
- HIPAA and security audits

### Data & Content

Based on the features and modules described across vendor materials and reviews, GlaceEMR stores and manages the following categories of data:

**Clinical data**: Patient demographics, clinical encounter documentation (via specialty templates), problem lists, medication lists, allergy lists, vital signs, clinical notes, assessments (including behavioral health screening instruments like PHQ-9, BIMS, Mini Mental Status Exam), treatment plans with goals and progress tracking, immunization records, growth charts.

**Orders and results**: Lab orders and results (via lab interface program), medication orders/prescriptions (via SureScripts e-prescribing), PDMP data, pharmacy refill requests.

**Scheduling data**: Appointment records, provider schedules, resource allocation, group therapy schedules, appointment reminders and no-show tracking.

**Messaging and communication**: Patient portal messages (two-way), secure messaging, patient engagement communications, appointment reminders.

**Billing and financial data**: Claims/charge data, ICD-10/ICD-9 codes, CPT codes (implied by charge capture and auto-coding), insurance eligibility data, accounts receivable, patient balances, denial records, payment records. The extent of billing data stored within GlaceEMR itself vs. the add-on GlaceRCM service is somewhat unclear — the base product includes billing/coding for claims submission, while the GlacePremium/GlaceComplete tiers add full RCM services.

**Documents**: Clinical documents, care coordination documents (CCDs for transitions of care, given (b)(1)-(3) certification), fax records (via GlaceOffice integration).

**Quality/reporting data**: CQM data, MIPS/MACRA performance metrics, public health reporting data (immunizations, syndromic surveillance, cancer registries — per (f)(1),(2),(4),(5),(7) certification).

**Telehealth data**: Telehealth visit records and video conferencing session data.

**Audit/system data**: Authentication and access logs (per (d) criteria certification), data integrity records.

**What's less clear**: The boundary between GlaceEMR and GlaceOffice/GlaceRCM for administrative and financial data. The vendor describes GlaceOffice as handling HR, payroll, bookkeeping, and credentialing — whether that data resides in the same system as GlaceEMR or is separately managed is not explicitly stated. Similarly, GlaceRCM accepts charges from "third-party EMRs" as well, suggesting it may be a somewhat independent service, but it also deeply integrates with GlaceEMR.

---

## Broader Product Ecosystem

Glenwood Systems markets several companion products alongside GlaceEMR:

- **GlaceRCM**: Full revenue cycle management service. Can work with GlaceEMR or third-party EMRs. Manages the complete billing lifecycle from eligibility verification through denial management and patient collections.
- **GlaceOffice**: Practice administration suite covering HR, credentialing, payroll, bookkeeping, payment processing, and IT infrastructure management.
- **GlaceScribe**: AI transcription/scribe service powered by Amazon HealthScribe, integrated into GlaceEMR.
- **GlaceGrow**: Digital marketing services for patient acquisition (SEO, social media, reputation management).
- **GlacePhoneSmart**: Automated phone answering and routine task handling.
- **GlaceBillSmart**: AI automation for billing tasks, denials, and A/R management.

These products appear to be marketed as separate add-ons/services rather than components of the certified health IT module, though GlaceRCM and GlaceScribe integrate deeply with GlaceEMR. For EHI export purposes, the key question is what data resides within the GlaceEMR system boundary vs. in these companion services.

## User Sentiment

Third-party reviews on emrsystems.net, FindEMR, and other sites show mixed reception (roughly 3/5 overall). Users praise the system's template library, customizability, integrated workflows, and ease of record access. Criticisms focus on system slowness during peak hours, an outdated-looking interface, occasional freezing, and inconsistent customer support responsiveness. Multiple reviews describe the system as comprehensive but sometimes clunky.
