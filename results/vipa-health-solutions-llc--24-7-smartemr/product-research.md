# VIPA Health Solutions, LLC — Product Research

Researched: 2026-02-16
Developer website: http://www.smartemr.com/ (also https://app.smartemr.com/smartemr_dot_com/smartemr_homepage.html)

## Overview

VIPA Health Solutions, LLC is a small, privately held health IT company founded in 2001 and headquartered in Miami, Florida. The company has approximately 11 employees and appears to be self-funded (no recorded venture capital or funding rounds). VIPA Health develops SmartEMR, a web-based electronic medical records and medical billing platform marketed to physician offices and ambulatory practices across a range of specialties. The company also markets related products under the "Smart" brand — SmartEBS (electronic billing system, described as a "5010 compliant Billing and Revenue Cycle Management module") — though limited detail is available on these. A third product name, "SmartMBS," was referenced on the VIPA Health LinkedIn description alongside SmartEMR and SmartEBS, but the smartmbs.com domain is now parked/for sale, suggesting that product may be defunct or absorbed. Revenue estimates from third-party databases (Apollo.io) cite ~$24.6M annually, though this seems high for an 11-person company and should be taken with skepticism.

## Product: 24/7 smartEMR

CHPL ID: 11079

### What It Is

24/7 smartEMR is a cloud-hosted, web-based EMR and practice management system designed for physician offices and ambulatory clinics. The ONC certification (version 7.2, certified December 2022) covers a broad set of 37 criteria spanning clinical data, transitions of care, patient portal, clinical quality measures, public health reporting, and FHIR API access. The SED intended user description is "Physician's Office."

The mandatory disclosures page describes it as "a Web-based electronic medical records solution that enables physicians to record patient encounters and test interpretations quickly and easily." It includes a CMS-compliant Superbill generation module and electronic claims processing. The product is marketed as both an EMR and a billing system in one platform.

SmartEMR is cloud-based and accessible from any device with a web browser, emphasizing "Patient Records Anywhere, Anytime." The vendor also offers a separate SmartEBS billing/RCM module, though it is unclear how tightly integrated this is with the core SmartEMR product or whether the certified product encompasses both.

### Users & Market

SmartEMR targets physician offices, medical clinics, and healthcare practices described as spanning "all types and sizes" across many specialties. Third-party listings (MedicalRecords.com) indicate support for numerous specialties including internal medicine, cardiology, dermatology, pediatrics, orthopedics, family medicine, gastroenterology, ENT, behavioral health, general surgery, and many more. The vendor describes it as "specialty-specific," suggesting customizable templates or workflows per specialty.

The actual installed base is unclear — no customer counts, case studies, or notable deployments were found in public sources. There are virtually no user reviews available: SourceForge shows 0 reviews, FindEMR shows 1 review (5 stars, "Perfectly smooth"), and Capterra has a listing but no accessible review content. This is consistent with a very small vendor serving a limited number of practices. The company is based in Miami, FL, and the contact information on the CHPL certification references a Miami phone number, suggesting a regional focus.

### Modules & Functionality

Based on the vendor's homepage, mandatory disclosures page, third-party review sites, and API documentation, SmartEMR includes the following modules and features:

**Clinical Documentation & EMR Core:**
- Patient encounter recording and documentation
- Test interpretations / diagnostic reports
- Customizable forms and reports
- Voice recognition technology (per SourceForge listing)
- Smart filters for access control

**e-Prescribing:**
- Integrated with Surescripts for electronic prescribing
- Drug database with interaction checking
- Prescription history access

**Lab & Diagnostics:**
- Lab results integration with LabCorp and Quest Diagnostics
- Lab management module
- Advanced interpretations module

**Billing & Revenue Cycle:**
- CMS-compliant Superbill generation (described as the product's best-known feature)
- Electronic claims submission with priority processing
- Insurance claims and billing statement generation
- Patient insurance eligibility verification
- E/M (Evaluation & Management) coding support
- 5010-compliant billing (via SmartEBS module or integrated)

**Patient Portal:**
- Patient portal with patient login access (per homepage)
- Certified for (e)(1) — patient view/download/transmit

**Scheduling & Practice Management:**
- Appointment scheduling / appointment management
- Organization management
- Site monitoring and productivity monitoring

**Telehealth:**
- Integrated telehealth (per SourceForge listing)

**Clinical Quality & Public Health:**
- Clinical quality measure (CQM) reporting — certified for 14 CQMs
- Certified for (c)(1)–(c)(3): clinical quality measures
- Certified for (f)(1): immunization registry reporting
- Certified for (f)(4): syndromic surveillance reporting

**Interoperability & Data Exchange:**
- Electronic exchange of patient records
- Transitions of care — certified for (b)(1)–(b)(3)
- FHIR R4 API with SMART on FHIR launch support
- OAuth 2.0 authentication

**Data Mining & Analytics:**
- Data mining module for inspecting databases and extracting structured data
- Reporting and analytics capabilities
- Statistical analysis and research with clinical data insights

**Communication & Alerts:**
- Alerts and notifications system
- Order management

### Data & Content

Based on the FHIR API documentation (smartemr.readme.io), SmartEMR exposes the following FHIR R4 resources, which indicate the clinical data types stored in the system:

- **Patient** — demographics
- **AllergyIntolerance** — allergy records
- **CarePlan** — care plans
- **CareTeam** — care team assignments
- **Condition** — diagnoses / problem lists
- **Device** — implantable devices
- **DiagnosticReport** — lab/diagnostic reports
- **DocumentReference** — clinical documents
- **Encounter** — visit/encounter records
- **Goal** — patient goals
- **Immunization** — immunization records
- **MedicationRequest** — prescriptions / medication orders
- **Observation** — vitals, lab results, social history, smoking status
- **Organization** — organization data
- **Practitioner** — provider data
- **Procedure** — procedures performed

Beyond the FHIR resources, the product's feature descriptions indicate it also stores:
- **Billing data**: Superbills, insurance claims, billing statements, eligibility verification results, E/M coding
- **Scheduling data**: Appointments
- **Prescription data**: e-prescribing records via Surescripts integration
- **Lab orders and results**: Via LabCorp and Quest integrations
- **Patient portal activity**: Patient-facing views of health records
- **Clinical quality measure data**: CQM calculations and reporting
- **Public health submissions**: Immunization registry and syndromic surveillance data
- **Telehealth session data**: If the integrated telehealth feature stores encounter records

**Gaps in information:**
- The vendor's website is quite sparse and marketing-light. Many feature details come from third-party listing sites rather than vendor documentation.
- The relationship between SmartEMR and SmartEBS (billing module) is unclear — whether SmartEBS is part of the certified product or a separate add-on.
- No information was found about clinical notes/documentation templates, though the product clearly stores encounter documentation.
- No mention of imaging storage (PACS), though the homepage mentions "imaging" integration — likely referring to ordering/results rather than image storage.
- No information about messaging between providers, referral management, or care coordination features beyond what's implied by transitions of care certification.
- The data mining module is mentioned but not well documented — unclear what additional data structures it can access.
