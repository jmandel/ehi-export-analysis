# DigiDMS, Inc. — Product Research

Researched: 2026-02-15
Developer website: https://digidms.com/

## Overview

DigiDMS, Inc. is a small, privately held healthcare IT company headquartered in Union/Linden, New Jersey. The company describes itself as "an integrated Medical Information Management Company" offering ONC-certified Electronic Health Records (EHR), Medical Billing, and Transcription Services. DigiDMS positions itself as a "Virtual Secretary" for hospitals, clinics, and independent doctors.

The company is small — reportedly 32+ domestic employees and 175+ overseas staff. They claim to have transformed "300+ medical offices nationwide into efficiency engines" over a six-year period. DigiDMS operates primarily in the eastern United States (NJ, NY, PA, CT, NC, VA, FL, IN, IL, TX, TN) and is expanding nationally. The product is cloud-based and accessible from mobile devices (iOS and Android apps available). The company's contact (from CHPL metadata) is Pratik Yardi.

Note: The vendor's main website (digidms.com) appears to be heavily JavaScript-rendered and was not accessible via standard web scraping or even a browser session during research — it timed out and rendered blank. Most product information was gathered from third-party listings, the myPersonalChart patient portal help pages, SlideShare webinar presentations, and directory sites (Medigy, Cardiovascular Buyers Guide, FindEMR).

## Product: DigiDMS

CHPL ID: 11549 (DigiDMS v25.0, certified 2024-12-12)

### What It Is

DigiDMS is a Complete EHR certified for the ambulatory/outpatient setting. The CHPL metadata indicates certification across a broad set of criteria — clinical data (a)(1)–(a)(5), (a)(12), (a)(14)–(a)(15); transitions of care (b)(1)–(b)(3); patient portal (e)(1); clinical quality measures (c)(1)–(c)(4); public health reporting (f)(1), (f)(2), (f)(4), (f)(5); FHIR APIs (g)(7), (g)(9), (g)(10); and direct messaging (h)(1). This is a comprehensive ambulatory EHR certification covering clinical, portal, public health, and API capabilities.

The product is an integrated EHR + Practice Management + Billing system. It is not a specialty-specific system — it targets general ambulatory practices including physician offices, dental offices, physical therapy clinics, and various medical specialties. The SED intended user description from CHPL is simply "Outpatient Clinic."

### Users & Market

DigiDMS targets small to medium healthcare organizations:
- Physician practices (primary care and specialties)
- Dental offices
- Physical therapy clinics
- Independent practitioners
- Small clinics and hospitals

The company claims 300+ medical offices as customers. This is a small vendor by healthcare IT standards. The company has offices in New Jersey, Texas, and North Carolina. Their listing in the Cardiovascular Buyers Guide suggests some presence in cardiology practices, though they are not cardiology-specific.

End users include physicians, clinical staff, billing staff, and patients (via the patient portal).

### Modules & Functionality

Based on vendor materials, third-party listings, webinar presentations, and the patient portal help documentation, DigiDMS includes the following modules and capabilities:

**EHR / Clinical:**
- Electronic Medical Records (clinical documentation/charting)
- Problem lists (active health problems)
- Medication management (active medications list)
- Allergy documentation
- Vital signs recording and charting
- Immunization records
- Lab results viewing and management
- Diagnostic test results
- Procedures documentation
- Clinical notes and encounter documentation
- Online prescriptions / e-prescribing
- Clinical decision support (mentioned in Medigy profile; also implied by (a)(2) CPOE and (a)(14) implantable device list certifications)
- Implantable device tracking (certified for (a)(14))
- Social, psychological, and behavioral data (certified for (a)(15))
- Drug-drug and drug-allergy interaction checks (certified for (a)(4))
- Demographics recording (certified for (a)(5))

**Practice Management / Billing:**
- Appointment scheduling (integrated into EHR)
- Patient demographics and insurance information
- Claim scrubbing technology (featured in a dedicated webinar)
- HCFA form generation (CMS-1500 billing forms)
- ICD-10 coding support
- Batch eligibility checks
- Auto-generation of claims
- Revenue cycle management
- Billing modules with invoices, insurance forms, and payment records

**Patient Portal (myPersonalChart):**
- Secure patient-provider messaging (inbox, reply, forward, create new messages)
- View active problems/diagnoses
- View medications
- View allergies
- View lab results and diagnostics
- View immunization records
- View vital signs with charts
- View clinical documents
- View insurance and demographic information
- Appointment scheduling, cancellation, and rescheduling
- Medication refill requests
- Referral requests
- Patient check-in (from home or clinic waiting area)
- Export health summary in CCD (Continuity of Care Document) format
- Import external CCD files
- Share chart with authorized users
- Patient education materials access
- Mobile app (iOS and Android)

**Transitions of Care:**
- CCD/CCDA generation and exchange (certified for (b)(1)–(b)(3))
- Direct messaging (certified for (h)(1))

**Public Health Reporting:**
- Immunization registry reporting (certified for (f)(1))
- Syndromic surveillance (certified for (f)(2))
- Cancer case reporting (certified for (f)(4))
- Electronic case reporting (certified for (f)(5))

**Document Management:**
- Centralized document repository for all file types
- OCR capabilities for scanning and indexing paper documents
- Version control
- Granular access controls and permissions
- Digital signatures
- Metadata tagging
- Customizable folder structures
- Document sharing, comments, and annotations

**Transcription Services:**
- DigiDMS historically offered medical transcription services, though more recent sources suggest it integrates with third-party transcription providers rather than providing this natively.

**API Access:**
- FHIR-based API access (certified for (g)(7), (g)(9), (g)(10))

### Data & Content

Based on the evidence gathered, DigiDMS stores and manages the following categories of data:

**Clinical data** (confirmed via patient portal help documentation and certification criteria): Patient demographics, problem lists, active medications, allergies, vital signs, immunization records, lab results, diagnostic test results, procedures, clinical notes/encounter documentation, clinical summaries, implantable device information, social/psychological/behavioral data, and patient education materials.

**Billing and financial data** (confirmed via webinar on claim scrubbing and multiple third-party descriptions): Insurance information, claims data, HCFA/CMS-1500 forms, ICD-10 codes, eligibility verification data, invoices, insurance forms, and payment records.

**Scheduling data** (confirmed via patient portal help and third-party descriptions): Appointment records, scheduling history, and check-in data.

**Communication data** (confirmed via patient portal help and webinar): Secure messages between patients and providers, clinical document sharing, referral requests, and medication refill requests.

**Document management data** (confirmed via multiple sources): Scanned documents, digital signatures, uploaded files of various types, and document metadata/annotations.

**Transition of care data** (implied by certification): CCD/CCDA documents, direct messages to other providers.

**Public health reporting data** (implied by certification): Immunization registry submissions, syndromic surveillance data, cancer case reports, electronic case reports.

**Gaps in research:** The vendor website was inaccessible during research, so detailed feature pages could not be reviewed. Information about specific clinical workflows (e.g., order entry details, clinical decision support rule sets, quality measure reporting specifics) is thin. No user reviews with substantive detail about the product's clinical functionality were found. The product's exact approach to lab ordering (vs. just results viewing) is unclear from available sources — though CPOE certification (a)(1) implies order entry capability.
