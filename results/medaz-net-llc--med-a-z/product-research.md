# MedAZ.Net, LLC — Product Research

Researched: 2026-02-14
Developer website: https://medaz.com

## Overview

MedAZ.Net, LLC is a small EHR and practice management software company based in Hamilton Township, New Jersey. It is a wholly owned subsidiary of KATSI, a global IT company with development centers in the U.S., Canada, Europe, and India. The company was founded around 2002 and claims "350 years of combined software development experience and more than 100 years of clinical experience" across its team. Employee counts from third-party business intelligence sources vary widely (16 to ~200), likely reflecting different counting methodologies and the parent company relationship. Revenue estimates range from $50M–$100M across sources, though these figures should be treated with caution for a company this size.

MedAZ targets physician practices of various sizes, from solo practitioners to multi-physician groups. The product was approved by HITECH Regional Extension Centers in California and New York, and was described as "Doctor's office of the future" by Canada's Infoway. A notable deployment was EBM IPA (an Independent Practice Association in New York City with 100+ physician members) in 2010. The company's go-to-market strategy centers on bundling free EHR and practice management software with their revenue cycle management/billing service, charging a percentage of gross collected receipts.

## Product: Med A-Z Complete

CHPL ID: 11300

### What It Is

Med A-Z Complete is a fully integrated suite combining Electronic Health Records (EHR), Practice Management, and Billing/Revenue Cycle Management in a single product. It is ONC Cures Act certified as of June 16, 2023 (CHPL Product Number 15.05.05.3150.MDAZ.01.00.1.230616). The certified module is the whole product — the three components (internally called "EHR Plus," "Practice Plus," and "Billing Plus") are tightly integrated and sold as a single solution.

The product is certified for both ambulatory and inpatient settings, though its marketing and customer base appear predominantly ambulatory physician practices. Intended users are "Physicians and their support staff" per the CHPL metadata.

The certification covers a broad set of criteria: clinical data management (a)(1)–(a)(5), (a)(12), (a)(14)–(a)(15); clinical information exchange (b)(3); EHI export (b)(10); care coordination (b)(11); clinical quality measures (c)(1)–(c)(4); public health reporting (f)(1)–(f)(2); and FHIR API access (g)(7), (g)(10). This is consistent with a full-featured ambulatory EHR with integrated billing.

### Users & Market

Med A-Z targets physician offices, hospitals, and clinical laboratories per their website. In practice, their customer base appears to be primarily small-to-mid-size ambulatory physician practices. Customer testimonials on the website come from practices in Kentucky and New York. The EBM IPA deployment (2010) brought the product to 100+ physician members of a New York City IPA, suggesting the product is used in multi-physician group settings.

The product is designed for physicians and clinical support staff (nurses, medical assistants) as well as billing/administrative staff. The integrated billing model means the product is also used by practice managers and billing departments.

The company does not appear to have significant market share — no presence on G2 or Capterra was found. A SelectHub listing exists but returned a 403 error. The product appears to be a niche offering for smaller practices attracted to the bundled billing service model.

### Modules & Functionality

The product consists of three integrated modules, based on vendor website, product pages, press releases, and FAQ:

**EHR Plus (Electronic Health Records)**
- Patient demographics and comprehensive clinical records
- Chief complaints, allergies, medications, medical/surgical history, family history, social history
- Review of systems documentation
- Height, weight, BMI tracking against recommended values
- One-click diagnostic templates that auto-populate History of Present Illness, physical exam, and treatment plans
- Auto-copy patient history functionality
- Customizable templates for histories and symptom reviews
- Evidence-based clinical guidelines accessible at point of care
- Disease management prompts based on clinical protocols
- Drug interaction checking: drug-drug, drug-allergy, drug-procedure warnings (monthly updates from certified third-party sources)
- CPOE (Computerized Physician Order Entry) for medications, laboratory orders, and diagnostic imaging
- Electronic prescribing via Surescripts (Gold certified; no additional charge)
- HL7 interfaces with Quest Labs, LabCorp, and regional labs
- HL7 interfaces with pharmacies, PACS imaging systems, hospitals, and other EHRs
- Diagnostic image and medical device input support
- Framingham 10-year cardiovascular risk calculations
- Patient education material tracking/logging
- Under/over-coding detection
- Pending test result reporting
- Clinical quality measure recording, importing, calculation, and reporting (QRDA-1, CCD-A)

**Practice Plus (Practice Management)**
- Patient scheduling tied to resources (flexible scheduling)
- Patient demographics management
- Insurance information management (unlimited insurance plan configuration)
- Real-time office floor plan visualization showing patient location and status (check-in, waiting, exam, testing, checkout)
- Check-in workflows with demographics verification and copay collection
- Rooming capabilities including history, vitals, PFSH, and lab access
- Checkout with copay handling, prescription generation, lab/test orders, follow-up scheduling
- Referral letter preparation
- Multi-location access without additional fees

**Billing Plus (Revenue Cycle Management)**
- Electronic bill transmission to insurers
- Claims scrubbing for errors, medical necessity checks (LMRP edits, CCI compliance)
- ISO 9001 certified billing processes
- HCFA form generation
- Real-time claim status tracking
- Procedure and diagnosis code linking
- Credit card/debit payment processing through partner companies
- Coding ready to print or transmit when patient leaves office
- Clinical, administrative, and financial report compilation

**Additional Services**
- Hosting services (separate fee)
- Direct messaging for clinical information exchange (separate fee)
- Training, maintenance, and support (24/7 phone support; separate fees)
- Chart scanning for data migration (bulk or gradual)
- Free HL7 data transfers; modest fees for non-standard format imports
- FHIR API for single-patient and bulk data exports
- Public health reporting capabilities (immunization, syndromic surveillance)
- Multi-factor authentication via one-time passcodes (text or phone call)
- Role-based access control with customizable user privileges

### Data & Content

Based on vendor documentation, the product stores and manages the following data categories:

**Clinical Data** (per EHR features page, FAQ, and certification info):
- Patient demographics
- Chief complaints, allergies, medication lists (active/inactive)
- Medical history, surgical history, family history, social history
- Review of systems
- Vital signs (height, weight, BMI)
- Physical exam findings
- Diagnosis/problem lists (active/inactive)
- Treatment plans
- Lab orders and results (via HL7 interfaces with Quest, LabCorp, regional labs)
- Diagnostic imaging orders (CPOE)
- Medication orders and prescriptions (via Surescripts e-prescribing)
- Drug interaction alerts and clinical decision support data
- Patient education materials delivered
- Clinical quality measures data
- Cardiovascular risk assessment data (Framingham)

**Administrative/Practice Management Data** (per Practice Management features):
- Appointment/scheduling data
- Patient insurance information
- Copay and payment information
- Referral letters and correspondence
- Patient location/status tracking within office

**Billing & Financial Data** (per Billing features and FAQ):
- Claims and billing records
- Procedure and diagnosis codes (ICD, CPT)
- HCFA forms
- Claim status and tracking data
- Payment processing records
- Revenue cycle analytics

**Exchange/Interoperability Data** (per certification and interoperability pages):
- CCD-A documents (transitions of care)
- QRDA-1 reports (quality measures)
- Public health reports (immunization registries, syndromic surveillance)
- FHIR resources (via g(7) and g(10) APIs)
- Direct messages

**System/Security Data** (per certification info):
- Audit logs
- User access records and authentication data
- Session management data

The vendor website does not explicitly mention a patient portal, though the EBM IPA press release (2010) mentioned a "PHR patient portal" as part of the deployment. The certification includes (e)(3) — patient health information export — but not (e)(1) — patient portal/view-download-transmit. This suggests the product may have limited or no current patient-facing portal functionality, or that it relies on FHIR APIs for patient access. The absence of a strong patient portal is a notable gap compared to typical full EHR suites.

The website does not mention behavioral health-specific features, long-term care, or specialty-specific modules. The product appears to be a general-purpose ambulatory EHR without deep specialty customization, though the one-click diagnostic templates and disease management prompts can be customized per provider.
