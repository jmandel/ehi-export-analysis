# MD Charts, LLC — Product Research

Researched: 2026-02-14
Developer website: https://mdchartsehr.com/ (redirected from https://mdcharts.net/)

## Overview

MD Charts, LLC is a small, privately held EHR vendor founded in 2002 and headquartered in Great Neck, New York. The company has 11–50 employees and was founded by Aaron Wachspress (CTO), who has 35+ years in healthcare and software development and previously founded Universal EHR Solutions. The product, "Physician's Solution," was designed in partnership with physicians and is marketed under several specialty-branded names (DermCharts, KidsCharts, OBGYNCharts). MD Charts is best known for dermatology — the SED intended user description is "Dermatology" — and ranks #2 in "Top 12 Dermatology EMRs" on Software Advice (4.8 stars). However, the platform serves multiple ambulatory specialties including OB-GYN, pediatrics, cardiology, urology, hematology/oncology, internal medicine, gastroenterology, and pulmonology. The company claims a senior analyst has overseen 150+ EHR implementations, suggesting a customer base in the low hundreds of practices. The product scales from solo providers to multi-office, multi-specialty practices.

## Product: Physician's Solution

CHPL ID: 11214

### What It Is

Physician's Solution is an all-in-one cloud-based EHR, practice management, and revenue cycle management platform for ambulatory practices. It is a "Complete EHR" certification (not a modular certification), meaning the certified product encompasses all clinical, administrative, and financial functionality described below. The product is sold under specialty-branded names (DermCharts for dermatology, KidsCharts for pediatrics, OBGYNCharts for OB-GYN) but these appear to be the same platform with specialty-specific templates and workflows, not separate products.

The certification is broad: 37 criteria including clinical documentation (a)(1)–(a)(5), drug interaction checks (a)(4), demographics (a)(5), clinical decision support (a)(14), transitions of care (b)(1)–(b)(2), patient portal (e)(1), (e)(3), public health reporting (f)(1)–(f)(2), (f)(5)–(f)(7), immunization registry (f)(1), syndromic surveillance (f)(2), electronic case reporting (f)(5), and FHIR APIs (g)(10).

### Users & Market

- **Primary users**: Physicians, medical assistants, front desk staff, and billers in ambulatory practices
- **Settings**: Solo practices through multi-site, multi-specialty groups
- **Specialties**: Dermatology (primary focus), OB-GYN, pediatrics, cardiology, urology, hematology/oncology, internal medicine, gastroenterology, pulmonology
- **Customer base**: Approximately 150+ implementations per the company's senior business analyst bio; no precise customer count published
- **Geography**: US-based practices
- **User feedback**: A long-term user (9+ years) described the program as "user friendly for providers, MAs, front desk and billers" and noted "providers actually see more patients a day due to the ease of use and customization" (Software Advice)

### Modules & Functionality

Based on vendor website, feature pages, and third-party listings:

**Clinical EHR**
- Ultra-customizable templates for specialty-specific documentation (100+ templates)
- E-prescribing to 50,000+ pharmacies (noted on DermCharts page)
- Lab integration: uni- and bi-directional interfaces with 20+ laboratories including LabCorp, Quest, and BioReference (EHR page)
- Lab orders and results tracking with embedded PDF support
- Clinical decision support (certified for (a)(14))
- Drug-drug and drug-allergy interaction checks (certified for (a)(4))
- Problem lists, medication lists, medication allergy lists (certified for (a)(1)–(a)(3))
- CPOE for medications, labs, and diagnostic imaging (certified for (a)(1)–(a)(3))
- Patient demographics management (certified for (a)(5))
- Implantable device tracking (certified for (a)(14))
- Immunization tracking and growth charts (noted for pediatric specialty — KidsCharts)
- MIPS data collection and reporting ("MIPs Made Easy℠")
- Telehealth integration — launched directly from patient chart, patients join via text/email link with no app required

**Dermatology-Specific (DermCharts)**
- BiopsyMapping™: visualizes multiple biopsy results on a single page
- InstaPath℠: time-stamped biopsy tracking with body-part location mapping and diagnosis recording
- Instant image upload and management — providers import patient images directly into charts and send to laboratories
- Lesion documentation and tracking
- Dermatology-specific order sets and pre-configured protocols
- Skin condition, biopsy report, and treatment plan documentation
- Automated coding suggestions with dermatology-specific ICD-10 support

**Practice Management**
- Appointment scheduling with online booking and patient self-scheduling
- Patient reminders via text and email
- Electronic patient intake forms (patients complete from mobile phones prior to arrival)
- Insurance eligibility verification (real-time)
- Patient account ledger management
- Advanced inventory control module
- 300+ built-in reports plus custom report builder
- SwiftDat™ real-time practice dashboards

**Revenue Cycle Management / Billing**
- Integrated charge capture (Peak Charge Capture™)
- Smart Super Bill℠ — custom dashboards for procedure tracking and billing accuracy
- Claims scrubbing with 3M+ CCI edits, 99% first-pass acceptance rate claimed
- C-Track™ — real-time claims tracking panel across all payers
- Electronic claim submissions with built-in clearinghouse
- Payment posting
- Denial appeal management
- A/R tracking with customizable reminders and bills
- Text-to-pay and online payment processing (MDCPay™)
- Collections management
- Gross vs. net revenue reporting, claim adjustment tracking

**Patient Engagement / Portal**
- Patient portal (certified for (e)(1) view-download-transmit and (e)(3) patient education)
- Electronic patient intake and demographics
- Patient-controlled information sharing
- Educational materials sharing
- Appointment scheduling and reminders
- Test results access
- Remote check-in functionality
- QR code-enabled chart updates
- Health Records ID card — physical card for instant secure access to critical medical information

**Data Exchange / Interoperability**
- Transitions of care via C-CDA (certified for (b)(1) and (b)(2))
- FHIR API access (certified for (g)(10))
- Public health reporting: immunization registries (f)(1), syndromic surveillance (f)(2), electronic case reporting (f)(5), transmission to cancer registries (f)(6), transmission to public health agencies (f)(7)
- AutoConsult Letters™ for provider communications
- National Emergency database integration
- Human-voiced IVR system

**Security & Infrastructure**
- Cloud-hosted (accessible from anywhere)
- HIPAA compliant with encryption
- Audit logging and access controls (certified for (d) criteria)

### Data & Content

Based on the features and certifications described above, the product stores and manages:

- **Patient demographics and registration data** — name, DOB, contact info, insurance, intake forms
- **Clinical notes and encounter documentation** — customizable templates per specialty, visit notes
- **Problem lists, diagnoses, and conditions** — ICD-10 coded
- **Medication lists and prescriptions** — including e-prescribing data transmitted to pharmacies via Surescripts (implied by the 50,000+ pharmacy integration)
- **Medication allergies and adverse reactions**
- **Lab orders and results** — bidirectional with LabCorp, Quest, BioReference, and 20+ other labs
- **Clinical images and photographs** — particularly for dermatology; stored within the chart with body-part mapping
- **Biopsy tracking data** — BiopsyMapping™ and InstaPath℠ with timestamps, body locations, diagnoses, and pathology results
- **Immunization records** — including registry reporting
- **Growth charts** — for pediatrics
- **Appointment schedules and booking data**
- **Billing and claims data** — charges, claims, scrubbing results, payment posting, denials, A/R aging
- **Insurance eligibility and verification data**
- **Patient account ledgers and payment history**
- **Patient portal messages and communications** — implied by patient portal and engagement features
- **Referral and consult letters** — AutoConsult Letters™
- **MIPS/quality measure data**
- **Audit logs and access records**
- **Telehealth session records** — sessions launched from chart
- **Inventory data** — via advanced inventory control module
- **Custom reports and analytics data**

The vendor website does not explicitly mention separate document scanning/storage beyond clinical images, though the DermCharts page references sending images to laboratories. The mandatory disclosures URL (https://mraemr.com:47102/api/mandatory_disclosure.asp) was unreachable at the time of research (ECONNREFUSED), so no additional product details could be obtained from that source.
