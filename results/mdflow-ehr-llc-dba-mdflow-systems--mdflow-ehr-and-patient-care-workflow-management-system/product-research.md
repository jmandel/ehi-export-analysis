# MDFlow EHR, LLC DBA: MDFlow Systems — Product Research

Researched: 2026-02-14
Developer website: https://www.mdflow.com/

## Overview

MDFlow Systems is a small, privately held healthcare IT company based in Miami, Florida (7715 NW 48th Street, Miami, FL 33166), incorporated in 2014 as MDFlow EHR, LLC. The company describes itself as having "over a decade of experience" providing healthcare software and services. MDFlow's primary market is **value-based care provider groups** — particularly staff-model medical groups operating under capitation contracts and sharing risk with health plans in South Florida. Their largest referenced customer, Community Medical Group, operates 18 medical centers with over 70,000 patients using MDFlow.

The company offers three distinct product lines: (1) the MDFlow EHR and Patient Care Workflow Management System (the ONC-certified product), (2) the MDFlow Care Management System (a separate population health/case management platform), and (3) the MDFlow Hospitalist Management System (HMS). The company also offers a telemedicine platform, a mobile app, a non-emergency transportation management system (MDTrans), and HIT consulting services. MDFlow holds HITRUST CSF certification (achieved August 2022). The company's clients include managed care organizations and health plans such as Freedom Health, Optimum Healthcare, Solis Health Plans, and Cano Health, in addition to provider groups.

MDFlow is not listed on G2, Capterra, or KLAS, suggesting a very small market footprint — likely focused on a niche of South Florida managed care/capitated provider groups.

## Product: MDFlow EHR and Patient Care Workflow Management System

CHPL ID: 11459 (15.11.09.3190.MDEP.08.00.1.240402)

### What It Is

The MDFlow EHR is a web-based (cloud/SaaS), ONC-certified electronic health records and patient care workflow management system. It was certified for version 8.0 on April 2, 2024. The product is internet-based, accessible from any computer via secured connection, and positions itself as enabling practices to "go paperless." It is specifically designed for value-based care provider groups, with unique features for staff-model medical groups under capitation contracts.

The certified module appears to be the EHR system itself. The Care Management System and Hospitalist Management System are separate products (the Care Management System is explicitly described as a distinct product line). However, the telemedicine platform is described as "fully integrated into MDFlow EHR and Care Management System."

### Users & Market

**Target users**: Healthcare providers and supporting clinicians (per SED description), physicians, nurses, and clinical staff in ambulatory/primary care settings.

**Clinical settings**: Primarily ambulatory/outpatient. The product targets staff-model medical groups, multi-site practice groups, and value-based care organizations operating under capitation and risk-sharing contracts. The South Florida managed care market appears to be their primary geography.

**Known customers** (from testimonials and news):
- **Community Medical Group** — 18 medical centers, 70,000+ patients (largest referenced customer)
- **Plaza Medical Centers** — referenced in testimonials
- **Health Excel Inc.** — referenced in testimonials
- **Simply Healthcare Plans** — referenced in testimonials
- **Cano Health** — integrated MDFlow into their Population Health Management platform (April 2018 news)

**Market size**: Very small vendor. No presence on major review platforms (G2, Capterra, KLAS). The company appears to serve a niche of South Florida managed care provider groups. The phone number is a direct Miami line (305-648-0028).

### Modules & Functionality

Based on the vendor's mandatory disclosures page, product documentation (DocPlayer archived materials), and the certified criteria list, the EHR includes:

**Clinical Documentation & Charting**
- Electronic capture of patient demographics and medical records
- Clinical decision support (certified: (a)(2))
- Computerized Physician Order Entry (CPOE) for medications (certified: (a)(1))
- Implicit support for clinical notes/encounter documentation (core EHR function)

**Medication Management**
- Electronic prescribing (e-prescribing) with drug interaction checking
- Medication reconciliation
- Formulary compliance checking
- PBM (Pharmaceutical Benefits Management) history — access to patient's previously filled medications from all prescribing physicians (via Surescripts/similar)
- Drug-drug, drug-allergy interaction checking (certified: (a)(5))

**Lab & Diagnostic Integration**
- Automatic retrieval of patient lab test results and incorporation into the patient chart
- Immunization registry submission (certified: (h)(1))

**Scheduling & Patient Flow**
- Appointment scheduling with transportation management
- Mobile app for viewing appointment schedules (iOS/Android, launched August 2017)

**Health Information Exchange**
- Secure health information exchange in HL7, CCD, CCR, CCDA formats
- Transitions of care (certified: (b)(1))
- Direct secure messaging
- FHIR API access (certified: (g)(7), (g)(9), (g)(10))

**Patient Engagement**
- Patient portal (mentioned on mandatory disclosures page)
- Telemedicine consultations (platform fully integrated with EHR since March 2016; sessions recorded and stored in patient's medical record)
- Secure messaging

**Quality Measurement & Risk Adjustment**
- HCC/MRA (Hierarchical Condition Category / Medicare Risk Adjustment) scoring and management
- HCC disease group management
- Star Ratings tracking
- HEDIS measures
- Clinical quality measurement (PQRS & MIPS)
- Medical chart review functionality for risk adjustment

**Reporting & Analytics**
- Data analytics and reporting tools that "turn data into decisions"
- Business intelligence reporting
- Quality measurement tracking

**Document Management**
- Document management capabilities (referenced in the DocPlayer materials)

**Mobile Access**
- MDFlow Mobile App (iOS and Android) — secure access to patient medical records and appointment schedules from smartphones and tablets

### Data & Content

Based on the features described above, the EHR stores or manages:

- **Patient demographics** — explicitly mentioned as a core feature
- **Clinical encounter data / medical records** — core EHR function, explicitly mentioned
- **Medication data** — e-prescribing, medication reconciliation, PBM history, and drug interaction checking all imply medication lists, prescription records, and pharmacy data
- **Lab results** — automatically retrieved and incorporated into patient charts
- **Immunization records** — immunization registry submission (h)(1) certification
- **Appointment/scheduling data** — scheduling is a described feature with mobile access
- **Telemedicine session records** — the vendor explicitly states that telemedicine session information is "recorded and stored in the patient's medical record"
- **Quality/risk adjustment data** — HCC scores, Star Ratings, HEDIS, MIPS/PQRS metrics
- **Health information exchange documents** — CCD, CCR, CCDA, HL7 messages
- **Secure messages** — secure messaging is a listed feature
- **Documents** — document management is referenced

**Unclear / Not mentioned:**
- **Billing and claims data**: The mandatory disclosures page mentions pricing based on practice size and the product promises "revenue enhancement," but the EHR product page does not explicitly describe billing, claims submission, or revenue cycle management as features. The Hospitalist Management System (a separate product) explicitly includes billing and revenue cycle management. It is unclear whether the EHR has built-in billing or whether billing is handled externally or through a separate module.
- **Clinical notes structure**: While encounter documentation is implied, the specific note templates, structured data elements, and clinical note types are not described in available materials.
- **Problem lists / diagnosis data**: While HCC management implies diagnosis coding, explicit problem list functionality is not described on available pages.
- **Allergy data**: Drug-allergy interaction checking (a)(5) certification implies allergy data is stored, but it's not explicitly described as a feature.
- **Vital signs**: Not explicitly mentioned in available materials, though standard for an EHR.
- **Imaging/radiology**: Not mentioned anywhere in the EHR product materials.
- **Referral management**: Not mentioned.
- **Orders beyond medications**: CPOE is listed for medications; unclear if lab orders, imaging orders, or referral orders are managed.

---

## Other MDFlow Products (Not Certified, But Context)

### MDFlow Care Management System
A **separate product** — NCQA Pre-validated, cloud-based population health and case management software. It is member-centric and designed for case and disease management programs (Medicare, Medicaid, SNPs). Features include candidate identification, health risk assessments, care plans, medication management, compliance tracking, data analytics, and integration with lab results, claims/pharmacy data, hospital ADT feeds, and state health information exchanges. Clients include Freedom Health, Optimum Healthcare, Solis Health Plans, and Carisk Partners. This product is delivered as SaaS on Microsoft technology.

### MDFlow Hospitalist Management System (HMS)
A **separate product** — described as "AI-powered," cloud-based, and purpose-built for hospitalist groups. Features include patient intake, charge capture, real-time eligibility verification, provider credentialing, clinical documentation, billing and revenue cycle management, mobile access, and telemedicine. Integrates with hospital ADT feeds and billing systems. This product explicitly includes billing capabilities that are not clearly present in the EHR product.

### MDTrans
Non-emergency medical transportation management system (launched January 2018). Real-time tracking of patients and vehicles with route optimization for dispatchers.

These products are separate from the certified EHR but share the MDFlow ecosystem and suggest the vendor's overall data capabilities extend well beyond the EHR itself.
