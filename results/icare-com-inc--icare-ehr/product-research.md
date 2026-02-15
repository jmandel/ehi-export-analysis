# iCare.com, Inc. — Product Research

Researched: 2026-02-14
Developer website: http://www.icare.com

## Overview

iCare.com, Inc. is a small, privately held health IT company based in Fort Lauderdale, Florida, founded in 2011 by Jim Riley (CEO), Ted Schneider (CTO), and Don Cook (CMO). The company builds and sells iCare, a cloud-native enterprise EHR platform marketed to hospitals, clinics, and physician practices. iCare positions itself as a modern, lower-cost alternative to legacy EHR systems — at its HIMSS15 debut, it claimed to be "the industry's first new enterprise EHR in 16 years." The company has not raised outside funding (per Crunchbase/Tracxn). LinkedIn lists 51–200 employees, though only about 11 profiles are associated with the company, suggesting the actual headcount is on the smaller end.

iCare serves a broad range of healthcare settings: single hospitals, multi-hospital organizations, integrated delivery systems (U.S.), NHS trusts (U.K.), private hospital chains, government health agencies, and ambulatory clinics. The CHPL certification SED description lists intended users as "Inpatient, Ambulatory, and Behavioral." However, specific named customers or detailed case studies are not publicly available on the vendor's website or in third-party sources. The product has very few reviews on major software review platforms (3 reviews on SoftwareFinder, zero on Capterra, zero on SourceForge, zero on Slashdot), making it difficult to gauge real-world adoption at scale.

The company achieved Complete Inpatient Meaningful Use Stage 2 Certification in January 2015 (via Drummond Group ONC-ACB), which it described as an industry first for an enterprise cloud EHR. Pricing is subscription-based with tiers ranging from Free (Basic) to $175/month (Acute Care), with per-user monthly pricing.

## Product: iCare EHR

CHPL IDs: 10314

### What It Is

iCare EHR is a fully integrated, cloud-native electronic health record platform designed for both inpatient (acute care/hospital) and outpatient (ambulatory) settings. The vendor describes it as a single platform that consolidates clinical, administrative, and financial operations. The certified module (iCare EHR Version 2) appears to be the entire product — there is no evidence of separate branded products or distinct platform variants. The CHPL certification covers a broad set of criteria across clinical data (a)(1)–(a)(5), (a)(12), (a)(14); care transitions (b)(1)–(b)(3); patient portal (e)(1); public health reporting (f)(2)–(f)(3); FHIR APIs (g)(7)–(g)(10); and direct messaging (h)(1).

The system is cloud-hosted (single-tenant SaaS), accessible via any browser on any device, with a mobile iOS application. iCare emphasizes modern architecture with "built-in big data capability" and open APIs for integration.

### Users & Market

**Target users:** Physicians, clinicians, nurses, healthcare administrators, billing staff, and patients (via portal). The SED intended user description says "Inpatient, Ambulatory, and Behavioral."

**Target settings:** Hospitals (small to large), multi-hospital systems, ambulatory clinics, physician practices, and government health agencies. The vendor also mentions NHS trusts in the U.K. and private hospital chains internationally.

**Market position:** Small vendor in the enterprise EHR space. No publicly known major hospital deployments. Very limited third-party review presence. The few reviews that exist (SoftwareFinder: 3 reviews, 5-star aggregate) are positive but sparse. No KLAS ratings or G2 reviews were found. The product appears to be early-stage or niche despite being certified since 2015.

**Notable claims:** "One of the fastest growing EHR providers in the industry" (from LinkedIn), though no revenue, customer count, or growth metrics are publicly disclosed.

### Modules & Functionality

Based on vendor website product pages, third-party directory listings, and the CHPL certification criteria, iCare EHR includes the following modules and capabilities:

**Clinical Documentation:**
- Patient charting with customizable templates, macros, and forms
- Clinical notes (visit notes, histories, physical exams, care plans)
- Dictation support for voice-based documentation
- Problem lists, medication lists, allergy lists (implied by (a)(1)–(a)(5) certification)
- Clinical decision support (implied by (a)(9) not being certified, but (a)(2)–(a)(5) drug-drug interaction checking is certified via e-prescribing)
- Computerized provider order entry — CPOE for medications (a)(1) and labs (a)(2)–(a)(3)
- Demographics recording (a)(5)

**E-Prescribing:**
- Electronic prescribing including controlled substances (EPCS)
- Real-time prescription tracking
- Drug interaction checks and formulary information
- Comprehensive medication database with dosages, interactions, contraindications
- Surescripts integration implied by e-prescribing certification

**Scheduling:**
- Appointment, procedure, and surgery scheduling
- Calendar views with patient preference accommodation
- Resource scheduling to reduce no-shows
- Patient self-service scheduling via portal

**Patient Portal:**
- Secure patient access to health summaries, test results, and schedules
- Online appointment scheduling
- Bill payment capabilities
- Secure messaging with the clinic
- Mobile-responsive portal access
- View, download, and transmit health information (e)(1) certified

**Revenue Cycle Management (RCM):**
- Insurance verification
- Billing and claims management
- Payment tracking and accounts receivable
- Denial management
- Medical coding (E/M coding)
- Financial reporting and analytics
- Described as a separate product page on icare.com but integrated into the platform

**Integrations & Interoperability:**
- API integrations with pharmacy, lab, imaging, and payer systems
- Named integrations: Change Healthcare, CareDox
- PACS integration for radiology image viewing
- Lab results integration directly into patient records
- Radiology results integration
- FHIR API access (g)(10) certified
- Direct messaging (h)(1) certified
- Transitions of care / C-CDA support (b)(1)–(b)(3) certified

**Public Health Reporting:**
- Syndromic surveillance reporting (f)(2) certified
- Electronic reportable laboratory results (f)(3) certified

**Administrative:**
- Document management — attachment and organization of charts, forms, lab results, images, correspondence
- Role-based user permissions
- Customizable dashboards and workflows (administrator-configurable without developer support)
- Reporting and analytics

**Other noted features (from directory listings):**
- Telehealth integration
- HIPAA compliance
- Mobile apps (iPhone, iPad, Android mentioned on SourceForge)
- Speech recognition integration
- 24/7 customer support

### Data & Content

Based on the certified criteria and described features, iCare EHR manages the following categories of data:

**Clinical data:** Patient demographics, problem lists, medication lists, allergy/intolerance lists, clinical notes and visit documentation, vital signs, immunization records, lab orders and results, radiology/imaging orders and results, care plans, clinical decision support alerts.

**Medication data:** Prescription records, medication histories, drug interaction data, controlled substance prescriptions (EPCS), formulary data. E-prescribing certification confirms this data flows through the system.

**Scheduling data:** Appointments, procedures, surgeries, calendar/resource schedules, patient preferences, no-show tracking.

**Financial/billing data:** Insurance information, claims, payments, denials, accounts receivable, billing codes (E/M). The RCM module is described as integrated, so this data lives within the platform.

**Patient portal data:** Patient-generated messages, self-service appointment requests, form submissions, payment records.

**Documents and media:** Attached charts, forms, images, correspondence, radiology images (via PACS integration), photos, and other digital media stored in what the vendor describes as a "centralized vault."

**Public health data:** Syndromic surveillance data, electronic reportable lab results.

**Interoperability data:** C-CDA documents for transitions of care, Direct messages, FHIR resources.

**Gaps and uncertainties:**
- The SED description mentions "Behavioral" as an intended user setting, but no behavioral health-specific modules or features are described anywhere on the vendor website or in third-party sources. It's unclear whether this means the general EHR is used in behavioral health settings or whether there are behavioral health-specific workflows (e.g., treatment plans, group therapy notes, substance abuse screening).
- No mention of specific inpatient workflows like nursing documentation, medication administration records (MAR), bed management, or operating room management, despite the acute care certification. The vendor markets hospital use but detailed inpatient module descriptions are absent.
- No mention of population health, quality reporting (beyond public health), or analytics beyond basic reporting.
- The mandatory disclosures URL field in the CHPL metadata is empty, which is unusual — this is a required ONC disclosure.
- The vendor website is heavily JavaScript-rendered (Divi/WordPress), making it difficult to extract actual content — many product pages returned only CSS/JS framework code with no readable content, so there may be additional feature details not captured here.
