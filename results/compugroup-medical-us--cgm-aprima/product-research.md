# CompuGroup Medical US — Product Research

Researched: 2026-02-15
Developer website: https://www.cgm.com/us

## Overview

CompuGroup Medical SE & Co. KGaA (CGM) is a large German healthcare IT company headquartered in Koblenz, Germany. Founded in 1987, CGM develops software for medical practices, pharmacies, labs, and hospitals across 20 countries, with products used in 60 countries and more than 1.6 million users worldwide. The company reported EUR 1,154 million revenue in FY2024 with approximately 8,700 employees. In June 2025, CGM was delisted from the Frankfurt Stock Exchange after CVC Capital Partners acquired ~27.78% of shares; the Gotthardt founding family retains ~50.12% majority ownership.

CGM's US operations are headquartered in Austin, Texas and were built primarily through the December 2020 acquisition of eMDs, Inc. for USD 240 million — one of the largest acquisitions in CGM's history. eMDs itself had acquired Aprima Medical Software in January 2019. The Aprima product originated as iMedica Corporation, founded in 1998 in Carrollton, Texas and renamed to Aprima in 2009 after a legal name dispute. So the product lineage is: iMedica (1998) → Aprima Medical Software (2009) → eMDs/Aprima (2019) → CGM APRIMA (2020). The @emds.com contact email domain on the CHPL listing reflects this history. CGM positions itself as a top-4 provider in the US ambulatory information systems market. The US product portfolio includes CGM APRIMA, CGM eMDs, ARIA RCM, CGM LYTEC, CGM MEDISOFT, CGM LABDAQ, and eMEDIX (clearinghouse).

## Product: CGM APRIMA

CHPL ID: 11167
CHPL Product Number: 15.04.04.2700.Apri.19.01.1.221228
Version: v19 (latest release v19.4, early 2025)
Certification Date: 2022-12-28
Certification Body: Drummond Group

### What It Is

CGM APRIMA is a comprehensive ambulatory EHR and practice management system described as a "market-leading, award-winning EHR" with a "smart, free-flowing interface" that uses adaptive learning technology. The certified module covers clinical documentation, practice management/billing, e-prescribing, patient portal, quality reporting, public health reporting, and FHIR API access — essentially the full ambulatory product. It is very broadly certified across 40+ ONC criteria spanning clinical data, care transitions, patient access, public health, FHIR APIs, quality measures, and security.

The product is deployed as cloud-hosted (CGM-managed servers), on-premise, or via mobile app (CGM APRIMA NOW for iOS/Android). It supports offline capability with auto-sync.

CGM APRIMA is complemented by several companion products/add-ons that are marketed as part of the broader ecosystem: CGM AMBI (ambient AI), CGM PRESCRIBE (e-prescribing), CGM CONNECTION (patient communication), CGM MEASURES (quality reporting), CGM PAY (payment processing), CGM INDEX.AI (document workflow automation), and ARIA RCM Services (outsourced revenue cycle management — 2024-2026 KLAS Best in KLAS winner). It's unclear whether all of these are modules within the certified product or separately licensed products that integrate with it; several (AMBI, ARIA RCM) appear to be add-on/optional services.

### Users & Market

The vendor's product page claims over 65,000 users across 1,000+ providers. At the time of the eMDs acquisition by CGM (2020), eMDs served 60,000+ providers across all its products, so the CGM APRIMA-specific user base is a subset. The product serves 70+ medical specialties, explicitly including primary care, internal medicine, family medicine, pediatrics, dermatology, pain management, OBGYN, immunology, orthopedics, and surgical specialties. Practice types range from solo practitioners to multi-physician groups (up to 60+ doctors). KLAS evaluates CGM APRIMA separately in a "Small Practices" (1-10 physicians) segment, suggesting significant penetration in smaller practices.

Settings include ambulatory care offices, FQHCs/CHCs, Rural Health Clinics, Patient-Centered Medical Homes, home-based primary care, and palliative care. This is purely an ambulatory system — not a hospital/inpatient product.

Third-party reviews are mixed. Capterra shows 2.9/5 from 56 reviews; Software Finder shows 3.3/5 from 70 reviews (56% positive, 26% negative). Positive themes include ease of customization for individual providers, efficient billing, and good specialty support. Negative themes include outdated UI, inconsistent support quality, and system interruptions. The companion ARIA RCM service has won three consecutive KLAS Best in KLAS awards (2024-2026), though the EHR itself has not.

### Modules & Functionality

Based on the vendor product page, specialty pages, reseller materials, and third-party reviews, CGM APRIMA includes the following capabilities:

**Clinical Documentation / EHR:**
- Adaptive learning technology that adjusts to provider workflows
- Multiple input methods: voice recognition, point-and-click, typing, inking/handwriting
- Structured data capture with customizable templates for 70+ specialties
- Clinical decision support with care gap alerts
- Offline capability with auto-sync when reconnected
- Optional CGM AMBI ambient AI integration (listens to patient encounter, suggests diagnoses, orders, and billing codes)

**E-Prescribing (CGM PRESCRIBE):**
- Multiple Surescripts White Coat Award winner
- Electronic prior authorization (ePA)
- EPCS (Electronic Prescribing for Controlled Substances)
- PDMP (Prescription Drug Monitoring Program) integration
- Automatic pharmacy downloads
- Instant e-prescriptions

**Scheduling:**
- Integrated appointment scheduling with customizable calendars

**Practice Management / Billing:**
- Integrated practice management module
- Claims management and submission
- Revenue cycle tools and code accuracy assistance
- eMEDIX clearinghouse integration for real-time eligibility verification, ERA posting, and claim scrubbing
- Optional ARIA RCM outsourced revenue cycle management
- Optional CGM PAY payment processing via Easy Pay partnership

**Patient Portal:**
- Bilingual portal (English/Spanish) on desktop and mobile
- Health record access for patients
- Appointment requests
- Prescription refill requests
- Secure messaging between patients and providers
- Lab result viewing
- Premium Patient Portal option mentioned in v19.4 release

**Patient Communication (CGM CONNECTION):**
- Text, email, and phone-based patient communication
- Appointment reminders
- Marketing communications

**Telehealth:**
- Remote patient monitoring
- Virtual visits (Patient Connect for CGM APRIMA)

**Lab Ordering:**
- Electronic lab orders integrated with diagnosis and billing workflows

**Quality Reporting (CGM MEASURES):**
- MIPS quality reporting dashboard
- 60+ clinical quality measures
- Real-time tracking with drill-down to individual chart notes

**FQHC/CHC-Specific Features:**
- Sliding fee scale management
- Encounter-based billing
- UDS and UDS+ reporting (built-in, no add-on required)
- UB04 billing
- G-code billing under PPS
- Multi-source funding support
- Group therapy documentation

**Document Workflow (CGM INDEX.AI):**
- AI-enabled document workflow automation

**Reporting & Analytics:**
- Customizable performance dashboards
- v19.4 added 8 new report types including PM claims, care management, CQM/interoperability, SDOH assessment, and demographics reports

**Interoperability:**
- FHIR R4 API (certified g(10))
- Health Information Exchange (HIE) support
- Direct messaging
- Carequality and CommonWell network connections
- Surescripts integration for prescriptions

**Public Health Reporting:**
- Immunization registry reporting (f)(1)
- Syndromic surveillance (f)(2)
- Cancer case reporting (f)(4)
- Electronic case reporting (eCR) — added in v19.4

**Mobile Access (CGM APRIMA NOW):**
- iOS and Android app providing full EHR access from tablet or smartphone

### Data & Content

Based on the documented features and modules, CGM APRIMA stores and manages a broad range of clinical and administrative data:

**Clinical data** (strongly supported by (a)(1)-(a)(5), (a)(12), (a)(14) certification and product feature descriptions): patient demographics, problem lists, medication lists, medication allergy lists, clinical notes/encounter documentation (including free-text and structured data via adaptive templates), vital signs, lab orders and results, imaging orders, procedures, diagnoses/assessments, care plans, clinical decision support alerts, and care gap tracking. The ambient AI (AMBI) integration suggests encounter audio may also be captured or referenced.

**Prescription data** (supported by e-prescribing module and Surescripts integration): prescription history, medication orders, pharmacy information, prior authorization records, PDMP query results, controlled substance prescribing records.

**Scheduling data** (supported by integrated scheduling): appointments, provider schedules/calendars.

**Billing and financial data** (supported by integrated PM module and eMEDIX clearinghouse integration): insurance/payer information, claims data, eligibility verification results, ERA/remittance data, payment records, coding data (CPT, ICD, HCPCS). For FQHCs: sliding fee scale data, encounter-based billing records, multi-source funding allocations, UDS reporting data.

**Patient portal data** (supported by (e)(1) certification and portal features): patient-entered information, secure messages between patients and providers, appointment requests, prescription refill requests, portal access logs.

**Communication data** (supported by CGM CONNECTION): appointment reminder logs, text/email/phone communication records with patients.

**Quality and reporting data** (supported by (c)(1)-(c)(3) certification and CGM MEASURES): CQM measure calculations, quality performance data, MIPS submissions. SDOH assessment data is mentioned in the v19.4 reporting additions.

**Public health reporting data** (supported by (f)(1)-(f)(5) certification): immunization records, syndromic surveillance data, cancer case reports, electronic case reports.

**Document management** (supported by CGM INDEX.AI and general EHR functionality): scanned documents, imported documents, faxes, and associated metadata.

**Telehealth data** (supported by virtual visit and RPM features): telehealth encounter records, remote patient monitoring data.

The vendor website does not explicitly discuss data retention policies, database architecture, or comprehensive data dictionaries. The mandatory disclosures URL points to the same product marketing page rather than a separate compliance/transparency page, which limits visibility into technical data specifications.
