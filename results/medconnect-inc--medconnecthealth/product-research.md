# MedConnect, Inc. — Product Research

Researched: 2026-02-16
Developer website: http://medconnecthealth.com

## Overview

MedConnect, Inc. is a small, privately held health IT company headquartered in Montgomery, Alabama. Founded in 2004 by Jimmy Chapman, the company builds and sells MedConnectHealth, a cloud-based integrated EHR and practice management platform aimed at ambulatory physician practices. The company has approximately 11–50 employees (per LinkedIn) and operates out of a single office in Montgomery. MedConnect positions itself as an affordable, physician-designed alternative to larger EHR vendors, with pricing at $349/month per provider.

MedConnect has a close relationship with MediSYS, Inc. (medisysinc.com), which appears to serve as a distribution/support partner — MediSYS's website describes providing "local, expert support, customizations, onsite implementation and continued training since 2006" for MedConnect EHR. Earlier versions of the product (e.g., MedConnect v2.3) appear on MediSYS press releases, suggesting that MediSYS may have originally developed or co-developed the platform, while MedConnect, Inc. is the certified developer entity. The exact corporate relationship is not fully clear from public sources.

The company claims to support over 25 medical specialties with connectivity to over 30 hospitals and labs/diagnostics. Its customer base appears concentrated in Alabama, with notable integrations specific to that state (direct connection to Blue Cross/Blue Shield of Alabama, connection to Alabama's One Health Record HIE). MedConnect was recognized as the first ambulatory EHR vendor to connect to Alabama's One Health Record HIE network. The product is not listed on major review platforms like G2 or Capterra, suggesting a small customer base and limited national presence.

Patient data is hosted at a Tier-4 data center. The product is entirely cloud-based and browser-accessible, requiring no on-premise hardware or software installation.

## Product: MedConnectHealth

CHPL IDs: 9183

### What It Is

MedConnectHealth 3.0 is a cloud-based, integrated healthcare software platform combining EHR, practice management, scheduling, patient portal, patient kiosk, and telehealth into a single product. It is ONC 2015 Edition certified (certified December 12, 2017) across a broad set of criteria spanning clinical documentation, e-prescribing, transitions of care, patient access, clinical quality measures, public health reporting, and FHIR APIs. The certified product number is 15.04.04.1889.MedC.03.00.1.171212.

The SED intended user description is "Outpatient Clinic," indicating it is designed for ambulatory care settings. The product appears to be the vendor's single, integrated offering — there are no separately named or marketed sub-products beyond the modules described below.

### Users & Market

**Target users:** Physicians, clinical staff, billing staff, and practice managers in ambulatory/outpatient settings. Patients interact through the patient portal and kiosk.

**Clinical settings:** Ambulatory clinics and physician group practices. The product supports over 25 specialties (specific specialties not enumerated on the vendor's website). The product appears oriented toward small to mid-size physician practices rather than hospitals or health systems.

**Geographic focus:** Strong Alabama presence, with direct integrations to Blue Cross/Blue Shield of Alabama and the Alabama One Health Record HIE. The extent of out-of-state deployment is unclear.

**Customer scale:** Not disclosed. The small company size (~11–50 employees), absence from major review platforms, and regional focus suggest a relatively small customer base, likely in the hundreds of practices or fewer.

**No notable named customers** are publicly identified on the vendor's website. Bingham Healthcare (in Idaho) appears in search results as having a "MedConnect" patient portal, though this may be a different "MedConnect" product unrelated to this vendor.

### Modules & Functionality

Based on vendor website product pages, the platform includes the following integrated modules:

**EHR / Clinical Documentation:**
- "One-Click" options for patient history, review of systems, and physical exam documentation
- Multiple documentation methods: voice recognition, point-and-click, document scanning, image annotation
- Configurable templates by provider specialty
- Patient chart displaying medications, lab results, problem lists, allergies, vitals, flowsheets, immunizations, and scanned documents
- Financial information visible within the patient chart
- Care plan management with diagnosis documentation accessible to patients
- Patient education resources customizable by clinic, routed to patient portal
- AI-described as "advanced clinical support tools" (details sparse)

**E-Prescribing:**
- Surescripts Certified for electronic prescribing including controlled substances (EPCS)
- Contraindication checking and formulary status verification
- Partnership with DrFirst for e-prescribing functionality

**Orders & Results / Lab Integration:**
- Integrated orders with patient flow
- Automatic lab test triggers based on exam findings
- Interfaces with LabCorp, Quest Diagnostics, and other lab companies
- Lab results populate directly into patient notes
- Connectivity to over 30 hospitals and labs/diagnostics

**Practice Management / Billing:**
- Claims management with charges categorized by Pending Processing, Submission, and Rework
- Electronic and paper claim generation
- Claims transmission via multiple clearinghouses: ClaimMD, Change Healthcare, Trizetto, Navicure, Waystar
- Direct connection to Blue Cross/Blue Shield of Alabama
- Automatic downloading of electronic remittances (ERA/EOB)
- Manual check posting to outstanding charges
- Real-time insurance eligibility checking (individual and batch)
- Financial statements and collection letters with customizable templates
- Revenue reporting with drill-down views of summary and detailed transactions
- Daily, weekly, and monthly report generation

**Scheduling:**
- Multiple or single provider views
- Flexible template configurations
- Color-coded visit types
- Rescheduling and new patient registration from the scheduler
- Insurance eligibility check from the schedule
- Patient balance or copay amount display during scheduling
- Scheduled appointments visible in patient portal
- Appointment reminder emails
- Printable schedule views
- Schedule reporting and analytics

**Patient Portal:**
- View/update medications, allergies, problems, and demographics
- View lab results and clinical summaries
- Request medication refills
- Request and view appointments online
- Send questions or comments to staff
- Online bill pay
- View electronic statements
- Download limited patient records in PDF and XML format
- Electronic forms (registration, consent, wellness visits)
- Virtual check-in for scheduled appointments

**Patient Kiosk / Check-in:**
- Driver's license and insurance card scanning
- Patient check-in at time of appointment
- Display and collect visit copay amount
- Address and contact information updates
- Patient identity verification and lookup

**Telehealth:**
- Integrated video visit capability
- Works with all devices, no download required
- Secure communication

**Clinical Quality & Reporting:**
- Support for 35 clinical quality measures (CQMs) per the mandatory disclosures page
- Population Health and ACO reporting
- Quality/Promoting Interoperability (PI) reporting
- Clinical quality measures span depression screening, diabetes management, cancer screenings, childhood immunizations, and more

**Interoperability & Data Exchange:**
- DIRECT protocol secure messaging
- Connection to Alabama One Health Record HIE
- Electronic faxing through Updox integration
- Alabama Immunization Registry access
- Automated clinical data submission to Blue Cross/Blue Shield of Alabama
- FHIR API access (certified for g(7)–g(10))
- Transitions of care (C-CDA) support (certified for b(1)–b(3))
- Public health reporting including immunization, syndromic surveillance, and cancer registry (certified for f(1), f(2), f(4))

### Data & Content

Based on the vendor's described functionality, MedConnectHealth stores and manages the following categories of data:

**Clinical data:** Patient demographics, problem lists, medications, allergies, immunizations, vitals, lab results (discrete and from interfaced labs), clinical notes/documentation (structured and free-text), review of systems, physical exam findings, care plans, patient education materials delivered, scanned documents and images.

**Orders and results:** Lab orders, diagnostic orders, order results populated from external labs (LabCorp, Quest, etc.).

**Prescriptions:** E-prescribing data including controlled substances, formulary checks, contraindication alerts, prescription history (via Surescripts/DrFirst integration).

**Scheduling data:** Appointments, provider schedules, templates, appointment types, reminder communications.

**Financial/billing data:** Charges, claims (electronic and paper), remittance advice (ERAs), payment postings, patient balances, copay collections, insurance eligibility responses, financial statements, collection letters, revenue reports. Direct claims data flows to BCBS Alabama and multiple clearinghouses.

**Patient portal data:** Patient-submitted messages, medication refill requests, appointment requests, electronic form submissions (registration, consent, wellness), patient-downloaded records, bill pay transactions.

**Kiosk/check-in data:** Scanned driver's licenses, scanned insurance cards, check-in timestamps, copay collection records, demographic updates.

**Telehealth data:** Video visit session records (unclear how much session metadata vs. clinical documentation is retained).

**Quality/reporting data:** Clinical quality measure calculations, PI reporting data, population health analytics.

**Interoperability data:** C-CDA documents (sent/received), DIRECT messages, HIE exchange records, immunization registry submissions, syndromic surveillance submissions, cancer registry submissions.

**Gaps/uncertainties:**
- The website does not describe document management or medical record scanning in detail beyond mentioning "document scanning" and "scanned documents" in the chart.
- The AI features are described vaguely — unclear what data AI tools access or generate.
- Whether the product stores referral management data is not mentioned.
- Fax data routing through Updox is mentioned but the extent of fax archival within MedConnectHealth is unclear.
- The Clinigence partnership (2018 press release) suggested clinical data analytics integration, but details were unavailable.
- No mention of integrated messaging/chat between staff beyond the DIRECT protocol for external exchange.
- Third-party fees apply for Promoting Interoperability, clearinghouse services, lab interfaces, and payment gateway processing, suggesting some data flows are handled by external services rather than stored natively.
