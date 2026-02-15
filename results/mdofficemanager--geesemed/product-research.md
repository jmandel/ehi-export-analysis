# MDOfficeManager — Product Research

Researched: 2026-02-15
Developer website: https://mdofficemanager.com

## Overview

MDOfficeManager LLC is a small healthcare IT vendor based in Clarksville, Indiana (founded 1999, revenue below $10M per 360Quadrants). The company provides two tightly integrated products: **GeeseMed EMR** (the electronic health record) and **MDOfficeManager PMS** (practice management system). They also offer revenue cycle management, medical coding, A/R management, medical transcription, and credentialing as services. The company was created by a team of physicians and IT professionals and targets small-to-medium ambulatory care practices and long-term care (LTC) facilities across the US, including skilled nursing facilities (SNF), nursing facilities (NF), and assisted living facilities (ALF), as well as outpatient surgery centers. GeeseMed claims to support 22+ medical specialties. The vendor has minimal presence on major third-party review sites (no reviews on G2, Capterra, or SoftwareAdvice; zero reviews on FindEMR; rated 4.2/5 on ITQlick but with very limited data). 360Quadrants ranks them 97th in the EHR market. This is a very small vendor.

## Product: GeeseMed (with MDOfficeManager PMS)

CHPL IDs: 11586

### What It Is

GeeseMed is a cloud-based, full-featured Electronic Health Record system certified as 2015 Cures Edition compliant (ONC Health IT Module certification from Drummond Group). It is marketed alongside MDOfficeManager PMS (Practice Management System) as an integrated platform — the product pages on the vendor website present them together as "GeeseMed EMR & MDofficeManager PMS." The EHR is web-based (256-bit SSL, accessible from any browser, compatible with Windows and Mac), requiring no local software installation. The certified product number (15.04.09.3013.Gees.07.00.1.250101) covers version 7.1 with a January 2025 certification date. The SED intended user description is "Outpatient & LTC clinic users."

The certification profile is broad, covering: clinical documentation and CPOE (a)(1)-(a)(5), clinical decision support (a)(12), implantable device list (a)(14), transitions of care (b)(1)-(b)(3), EHI export (b)(10), care plan (b)(11), patient portal/VDT (e)(1), public health reporting (f)(1)-(f)(2), and FHIR APIs (g)(7)-(g)(10)). This indicates a full EHR with clinical, interoperability, and patient engagement capabilities.

### Users & Market

GeeseMed targets small-to-medium ambulatory care practices, outpatient surgery centers, and long-term care facilities (SNF, NF, ALF) across the US. The vendor's marketing emphasizes simplicity and efficiency for smaller practices. Testimonials on the website are from small-practice users who praise the customer service and simplicity. No specific customer counts are disclosed; 360Quadrants noted approximately 80 interested buyers/users negotiating, suggesting a very small installed base. The product supports 22+ specialties per vendor claims, though specific specialties are not enumerated beyond the general categories of ambulatory, outpatient surgical, and LTC.

### Modules & Functionality

Based on vendor website materials, the following modules and features are described:

**Clinical Documentation & Charting:**
- Template-based charting with a "powerful knowledgebase template library and macros" (hundreds of macros available)
- Speech recognition software integration for dictation-to-document workflow
- Medical transcription services (offered as a service — physicians dictate, GeeseMed team transcribes and uploads via HL7/DRT/CDA)
- "Five-click data policy" — any data retrievable or enterable within five clicks
- Specialty patient cards for specialized care views
- Problem lists with current diagnoses, active medications, allergy lists
- Discrete Reportable Transcription (DRT), CDA documents, HL7 interfaces for document integration

**Clinical Decision Support & Orders:**
- CPOE for medications, laboratory tests, and imaging orders
- Drug interaction checking (relies on Medispan for drug data)
- Clinical decision support

**E-Prescribing:**
- SureScripts-certified for electronic prescriptions
- Electronic Prescribing of Controlled Substances (EPCS)
- Prescription eligibility checking
- Formulary checks
- Ability to send prescriptions nationwide to any pharmacy

**Laboratory:**
- Certified interfaces with "all major laboratories"
- Electronic lab ordering and results receipt
- Lab results viewable in patient portal

**Practice Management (MDOfficeManager PMS):**
- Appointment scheduling
- Provider dashboard with daily tasks, messages, chart, refill, lab results, alerts/reminders, referrals, appointments
- Task management (e.g., provider can request receptionist to schedule follow-up, lab, or radiology test)
- Prioritized task "donuts" visualization
- To-do lists
- Snapshot views

**Billing & Revenue Cycle Management:**
- Fully integrated billing and EHR — patient information entered clinically passes directly to billing
- Claims processing with focus on low denial rates and high clean claim rates
- Automated billing workflows
- Dashboard analytics for billing reports and practice performance metrics
- Managed billing offered as a service (outsourced RCM)
- Compliance management (payer environment changes, HIPAA, RAC audits)

**Patient Portal:**
- Real-time patient access to medical records, lab results, family/social/medication/surgical histories
- Electronic prescription viewing
- Appointment requests
- Patient engagement features

**Telehealth & Remote Care:**
- Telemedicine with secure video and chat
- Remote patient monitoring
- Automated appointment reminders

**Health Information Exchange:**
- Direct messaging via EMRDirect (relied-upon software per mandatory disclosures)
- Transitions of care (C-CDA exchange)
- HL7, XML integration technologies
- Secure electronic fax
- Secure messaging between providers and staff

**Reporting & Compliance:**
- MIPS/APM compliance support
- ICD-10 coding support
- Quality measurement calculation
- Public health reporting (immunization, syndromic surveillance)
- Data analytics and reporting

**Additional Services (offered alongside the software):**
- Medical coding services
- A/R management
- Credentialing services
- Virtual medical scribe services
- Medical, business, and legal transcription services

### Data & Content

Based on the features described above, GeeseMed stores and manages:

- **Patient demographics and identifiers** (registration, insurance info)
- **Clinical documentation** (encounter notes, transcribed dictations, templates, macros)
- **Problem lists / diagnoses** (ICD-10 coded)
- **Medication lists** (active medications, prescription history)
- **Allergy lists**
- **Family and social history**
- **Surgical history**
- **Laboratory orders and results** (via lab interfaces)
- **Imaging orders** (CPOE for imaging)
- **Prescriptions** (e-Rx via SureScripts, including controlled substances)
- **Drug interaction data** (via Medispan)
- **Appointment/scheduling data**
- **Provider tasks, messages, and alerts/reminders**
- **Referral information**
- **Billing/claims data** (integrated billing with claim processing, denial tracking)
- **Patient portal messages and activity** (appointment requests, record access)
- **Telehealth session data** (video, chat)
- **Remote patient monitoring data**
- **Care plans** (certified for (b)(11) care plan criteria)
- **Implantable device information** (certified for (a)(14))
- **C-CDA documents** (transitions of care)
- **Quality/MIPS reporting data**
- **Public health reports** (immunization, syndromic surveillance)
- **Secure messages** (provider-to-provider, provider-to-staff)
- **Electronic faxes**
- **Audit logs** (required for (d) criteria)

The vendor's reliance on EMRDirect for Direct messaging and Medispan for drug data are the only two relied-upon software components disclosed, suggesting most functionality is built into the GeeseMed platform itself.

**Information gaps:** The website does not detail what LTC-specific data elements are stored (e.g., MDS assessments, ADL tracking) despite marketing to SNF/NF/ALF facilities. The reference to "real-time data exchange with Point Click Care" on the main GeeseMed site suggests integration with that LTC platform but doesn't clarify what data flows between them. Specific imaging data storage (beyond orders) is unclear — the product handles CPOE for imaging but there's no mention of PACS or image storage. The depth of surgical/procedure documentation for outpatient surgery centers is not detailed beyond general charting capabilities.
