# Doc-tor.com — Product Research

Researched: 2026-02-15
Developer website: https://www.doc-tor.com/

## Overview

Doc-tor.com is a small healthcare IT vendor founded in 2000 in Allendale, New Jersey, by a team of physicians and IT professionals. The company positions itself as a pioneer in cloud-based practice management, claiming to have launched the first cloud-based practice management product in 2000 and the first fully integrated PM and EHR product in 2004. In February 2020, Doc-tor.com was acquired by Harris Healthcare (a division of Constellation Software Inc.'s Harris Computer operating group). Post-acquisition, Doc-tor.com sits alongside Amazing Charts, Harris CareTracker, digiChart, Clinix, MEDfx, and Pulse within Harris Healthcare's ambulatory care portfolio. Harris follows a "Software for Life" / "never sells" philosophy — acquired products are maintained indefinitely. The developer contact email in CHPL metadata is `@harriscomputer.com`, confirming the current corporate parent.

At the time of acquisition, Doc-tor.com served over 550 medical practices and more than 2,200 medical professionals, primarily in the New York, New Jersey, and Pennsylvania region. The RCM arm had processed over $1.7 billion in medical billings. The company is small by industry standards — a regional ambulatory EHR vendor now operating under a large conglomerate. Key technology partners mentioned include IBM, Microsoft, Oracle, Nuance, and Dragon (speech recognition).

## Product: Picasso

CHPL ID: 11652

### What It Is

Picasso is a 100% cloud-based, fully integrated ambulatory EHR and practice management suite marketed as an "All In One Medical Suite." It is not a module or component — Picasso is the entire product, encompassing EHR, practice management, revenue cycle management, and a patient portal ("Community"). The certified module (Picasso version 8.2, certified June 4, 2025) covers the full product.

The product has broad ONC certification across 37 criteria, including:
- Clinical data: (a)(1) CPOE-Meds, (a)(2) CPOE-Labs, (a)(3) CPOE-Imaging, (a)(4) Drug-drug/drug-allergy interaction checks, (a)(5) Demographics, (a)(12) Family health history, (a)(14) Implantable device list
- Transitions of care: (b)(1) Transitions of care, (b)(2) Clinical information reconciliation, (b)(3) Electronic prescribing
- Patient portal: (e)(1) View, download, transmit
- Public health: (f)(1) Immunization registry reporting, (f)(7) Health care surveys
- Clinical quality: (c)(1)-(c)(3) CQMs
- APIs: (g)(7), (g)(9), (g)(10) FHIR-based API access
- EHI export: (b)(10)

### Users & Market

Picasso targets three customer segments: independent physician practices, clinically integrated networks, and billing service companies. It also claims to serve federally qualified community health centers (FQHCs). The vendor describes supporting practices ranging from solo practitioners to healthcare enterprises. At the time of the Harris acquisition (2020), the product served 550+ practices and 2,200+ clinicians, concentrated in the NY/NJ/PA region. No updated customer counts are available post-acquisition.

Day-to-day users include physicians (clinical charting), front-desk staff (scheduling, registration, eligibility checks), billing staff (claims, payments, RCM), and patients (via the Community portal). The SED intended user description in CHPL is simply "Ambulatory."

No specific specialty focus was found — the vendor markets it as general ambulatory, though it claims over 1,000 specialty-specific templates for clinical documentation.

### Modules & Functionality

The Picasso suite consists of four integrated components:

**1. Picasso EHR (Electronic Health Records)**
- Clinical documentation via multiple methods: tab-based point-and-click, voice dictation (Nuance/Dragon integration), visual body diagrams, or combinations
- Over 1,000 specialty templates; smart templates customizable without programming
- Simultaneous real-time multi-user charting in the same patient record (push technology — no refresh needed)
- Lab results with discrete data and charting capability
- Document management / electronic storage
- "Microsoft Office look and feel" interface design
- Cloud+ feature: read-only patient record access during connectivity outages
- Optical Medical Record (OMR) functionality (mentioned on homepage but not elaborated)

From the certified criteria, the product must also support:
- CPOE for medications, lab orders, and imaging orders (a)(1)-(a)(3)
- Drug-drug and drug-allergy interaction checking (a)(4)
- Patient demographics recording (a)(5)
- Family health history (a)(12)
- Implantable device list (a)(14)
- Electronic prescribing via NewCrop (b)(3) — confirmed on the mandatory disclosures page, which lists "NewCrop Core" as integrated third-party software
- Clinical information reconciliation — medication, allergy, and problem list reconciliation (b)(2)
- Transitions of care / C-CDA creation and receipt (b)(1)
- Immunization registry reporting (f)(1)
- Clinical quality measure calculation and reporting (c)(1)-(c)(3) — specifically references CMS measure 131v7 and Healthmonics Registry participation

**2. Picasso Practice Management**
- Scheduling: customizable appointment booking, real-time check-in, automated appointment reminders
- Patient registration: demographics and insurance data capture
- Eligibility verification: automated insurance coverage and benefits checking during registration
- Charge posting with CPT/HCPCS code management
- Claims management: automatic clean claim generation, claim submission, claim scrubbing
- Payment posting and reconciliation with automated matching to open charges
- Patient payment plan management
- KPI dashboards with real-time metrics (collections, aging reports, denial rates, co-pays collected, AR per payer)
- Scheduled report delivery
- Multi-location and multi-provider support with enterprise-wide resource tracking

**3. Picasso Community (Patient Portal)**
- Secure multi-directional messaging between patients and providers
- View medication history and complete medical records
- Receive clinical summaries
- Schedule and request appointments
- Patient-entered health information
- Online bill payment
- Patient education materials
- 24/7 access via computer or mobile device

**4. Revenue Cycle Management (RCM)**
- Offered both as software and as a managed service
- Claims creation, submission, payment posting, and reporting
- Denial management and remediation
- Daily appointment tracking and patient balance updates
- Point-of-service collection optimization
- Real-time financial analytics dashboard (cash flow, denials, AR)
- HIPAA-compliant financial data handling

**Third-party integrations noted on the mandatory disclosures page:**
- NewCrop Core (e-prescribing)
- Clinical Exchange (clinical information exchange)
- NLM AccessGUDID API (implantable device data)

### Data & Content

Based on the vendor's described features and certified criteria, Picasso stores or manages the following categories of data:

**Clinical data:** Patient demographics, encounter/visit notes, medication lists, allergy lists, problem lists, family health history, implantable device lists, lab orders and results (with discrete data), imaging orders, medication orders, vital signs (implied by CQM reporting), immunization records (implied by immunization registry reporting (f)(1)), clinical summaries, clinical quality measure data.

**Documents:** Clinical documents (C-CDAs for transitions of care), scanned/electronic documents (document management feature), encounter notes via multiple input methods.

**Prescriptions:** Electronic prescriptions via NewCrop integration; drug-drug and drug-allergy interaction checking implies structured medication and allergy data.

**Administrative/practice management data:** Appointment schedules, patient registration/demographics, insurance information, eligibility verification data, CPT/HCPCS charge data, claims (submitted, denied, paid), payment records, patient balances and payment plans, accounts receivable data, KPI/reporting data.

**Patient portal data:** Patient-entered health information, secure messages between patients and providers, appointment requests, clinical summaries shared with patients.

**Financial/billing data:** The RCM component processes $1.7B+ in billings (historically), storing claims, payments, denials, collection data, and financial analytics.

**What's unclear:** The vendor website is relatively light on detail about specific clinical data fields beyond what can be inferred from certified criteria. There's no mention of referral management, care plans, or clinical decision support beyond drug interaction checking. The "Optical Medical Record (OMR)" capability is mentioned once without elaboration — it's unclear what additional data this involves. The website doesn't discuss imaging storage (PACS), just imaging orders. No mention of behavioral health, substance abuse, or sensitive data handling. No mention of audit logs or system administration data in user-facing materials (though these would exist for certification compliance).
