# Bizmatics Inc. — Product Research

Researched: 2026-02-16
Developer website: https://prognocis.com/

## Overview

Bizmatics Inc. is a healthcare software company founded in 2001 and headquartered in Silicon Valley (San Jose, CA area). The company develops PrognoCIS, a cloud-based EHR, practice management, and medical billing platform for ambulatory/outpatient clinical practices. In February 2021, Bizmatics was acquired by Harris Computer Company, itself an operating group of Constellation Software Inc. (TSX: CSU), a major Canadian vertical market software acquirer. Post-acquisition, Bizmatics continues to operate as "PrognoCIS by Bizmatics, A Harris Computer Company."

PrognoCIS targets small-to-mid-sized medical practices, including solo practitioners, multi-provider clinics, and multi-specialty groups. The company claims over 23 years of experience in the EMR industry and supports 30+ clinical specialties with customizable templates and workflows. Specialties highlighted on the vendor website include family medicine, internal medicine, cardiology, dermatology, psychiatry, OB-GYN, pediatrics, podiatry, gastroenterology, occupational medicine, pain management, and orthopedics. Review sites show an overall satisfaction rating around 82% (565 reviews on one platform) and 4/5 stars (92 reviews on another). The product has been ranked in the top 10 by KLAS at some point. Pricing starts at approximately $280/month per provider.

## Product: PrognoCIS

CHPL IDs: 8856 (version Denali 3.1, certified 2017-09-29), 11738 (version 4.0, certified 2025-12-24)

### What It Is

PrognoCIS is an integrated cloud-based EHR/EMR and practice management platform. It is a single, unified product — not a modular suite where components are sold separately. The certified product encompasses electronic health records, practice management, medical billing/revenue cycle management, e-prescribing, patient portal, telemedicine, document management, and reporting/analytics. The SED intended user description is "Outpatient Clinic."

Both CHPL listings share identical certified criteria (37 criteria spanning clinical, care coordination, patient portal, public health, and FHIR API categories), indicating this is the same product at two different version levels rather than two distinct products.

### Users & Market

- **Target users**: Physicians, nurses/clinical staff, billing staff, practice managers, and patients (via portal)
- **Clinical settings**: Ambulatory/outpatient clinics — solo practices, small-to-mid-size groups, multi-specialty practices
- **Specialties**: 30+ including family medicine, internal medicine, cardiology, dermatology, psychiatry, OB-GYN, pediatrics, podiatry, gastroenterology, occupational medicine, pain management, orthopedics, surgery
- **Deployment**: Cloud-based (SaaS), accessible from Windows, Mac, Linux, iOS, and Android devices
- **Market position**: Mid-market ambulatory EHR. Now part of Harris Computer/Constellation Software's portfolio of healthcare acquisitions. Harris also acquired Benchmark Solutions (another EHR/PM/RCM company), suggesting a roll-up strategy in this segment.
- Specific customer counts were not found on the vendor website, but the product appears to have a meaningful installed base given 23+ years in market and hundreds of user reviews across multiple platforms.

### Modules & Functionality

Based on vendor website pages, feature descriptions, third-party review sites, and search results:

**Electronic Health Records / Clinical Documentation**
- Customizable templates for 30+ specialties with pre-built and user-modifiable templates
- Smart phrases and template database for streamlined charting
- Voice recognition for physician dictation
- PrognoAI-Scribe (AI-powered ambient documentation): listens to provider-patient conversation, generates draft notes for provider review and approval
- Clinical decision support
- Problem lists, medication lists, allergy lists
- Vital signs recording
- Growth charts (pediatrics noted specifically)

**Computerized Provider Order Entry (CPOE)**
- Lab ordering with electronic results receipt
- Radiology ordering with electronic results
- Medication ordering
- Seamless integrations with labs, radiology companies, and vaccine registries
- Results review and reporting

**E-Prescribing**
- Surescripts-certified e-prescribing
- EPCS (Electronic Prescribing of Controlled Substances) with IdenTrust two-factor authentication
- RxHub integration for prescription benefit information (eligibility, formulary, lower-cost alternatives)
- RxChange and CancelRx support for pharmacy-provider communication
- Complete medication history access

**Practice Management / Scheduling**
- Appointment scheduling with automated text reminders
- Provider scheduling and resource management
- Pre-authorization tracking
- Real-time insurance eligibility verification
- Referral management with preregistration, insurance verification, messaging, document attachment, notes, and referral tracking

**Medical Billing / Revenue Cycle Management**
- Integrated billing module (not a separate product)
- Automated claim creation — claims auto-generated at encounter close with billing codes auto-populated from services provided
- Claim scrubbing and verification
- Electronic claim submission
- Own clearinghouse (Secure Connect) plus connections to external clearinghouses (Trizetto, Waystar, Jopari)
- Automated payment posting and reconciliation
- AR (accounts receivable) management
- Denial tracking and management
- Automated prior authorization — pre-fills required info from orders, links authorization to billing claim
- Revenue reports and financial analytics

**Patient Portal**
- Patient access to medical records
- Intake form completion
- Online appointment scheduling
- Secure messaging with providers
- Prescription refill requests
- Lab result viewing
- Account management and billing
- Patient education materials (implied by ONC e(1) certification)

**Telemedicine**
- HIPAA-compliant video conferencing (built-in, called PrognoCIS Telemedicine)
- Available as standalone or integrated with EHR
- Supports hybrid care models
- Telehealth-specific billing support

**Document Management**
- "Attach Center" for attaching, organizing, and managing faxed and scanned files
- Supports images, lab results, patient forms attached directly to patient charts
- PrognoFax — electronic faxing service (send faxes without hardware)
- Document scanning and storage

**Reporting & Analytics**
- Customizable dashboards
- Performance reports
- Key performance indicator tracking
- Patient outcome monitoring
- Clinical quality measure (CQM) reporting (certified for c(1)–c(4))
- Various EMR and billing reports

**Public Health Reporting**
- Immunization registry reporting (certified f(1))
- Syndromic surveillance (certified f(2))
- Electronic case reporting (certified f(5))
- Public health registry/specialized registry reporting (certified f(7))

**Interoperability**
- HL7 and FHIR (g(10)) support
- Transitions of care / C-CDA document exchange (b(1), b(2), b(3))
- Direct messaging (h(1))
- API access for third-party app integration
- Lab and radiology interface integrations
- Machine interfaces for medical devices

**E-Signature**
- Built-in digital signature for documentation and medical bills

### Data & Content

Based on the features and modules described above, PrognoCIS stores and manages the following categories of data:

**Clinical Data** (well-documented):
- Patient demographics and registration information
- Clinical encounter notes / progress notes (customizable templates)
- Problem lists, diagnoses (ICD codes)
- Medication lists and prescription history
- Allergy lists
- Vital signs and measurements
- Lab orders and results
- Radiology/imaging orders and results
- Immunization records
- Clinical decision support alerts and interactions
- Growth charts and specialty-specific clinical data

**Orders and Prescriptions** (well-documented):
- CPOE orders (lab, radiology, medications)
- E-prescriptions including controlled substances
- Prescription benefit/formulary data via Surescripts
- Prior authorization requests and responses

**Billing and Financial Data** (well-documented):
- Insurance/payer information and eligibility data
- CPT/billing codes associated with encounters
- Claims data (generated, submitted, adjudicated)
- Payment records and posting
- Accounts receivable records
- Denial records and appeal tracking
- Financial reports

**Patient Portal/Engagement Data** (documented):
- Patient portal accounts and access logs
- Secure messages between patients and providers
- Patient-completed intake forms
- Appointment requests and scheduling data
- Prescription refill requests

**Documents and Media** (documented):
- Scanned documents attached to charts
- Faxed documents (inbound and outbound via PrognoFax)
- Images attached to patient records
- E-signatures on documents

**Scheduling and Administrative Data** (documented):
- Appointment schedules
- Provider schedules
- Referral records and tracking
- Pre-authorization records

**Public Health/Reporting Data** (documented via certification):
- Immunization registry submissions
- Syndromic surveillance reports
- Electronic case reports

**Audit and System Data** (implied by certification):
- Audit trails and access logs (certified d(2), d(3))
- User accounts and authentication records
- System configuration data

**Areas of uncertainty**:
- The vendor website is heavily JavaScript-rendered, making it difficult to extract detailed feature content (many pages returned only framework code). The feature detail above comes primarily from search result snippets, third-party review sites, and a few pages that rendered successfully.
- Specific details about what structured data fields exist in the clinical documentation (beyond what's implied by ONC certification criteria) are not available from public sources.
- The depth of the document management system (version history, document types, retention policies) is unclear from available materials.
- Whether PrognoCIS stores discrete imaging files (DICOM) or just radiology orders/results is unclear — likely the latter, with imaging stored in separate PACS systems.
- The AI/PrognoAI features (ambient scribe) presumably generate and store draft notes, but how these are persisted vs. finalized notes is not documented publicly.

---
