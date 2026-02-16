# Ulrich Medical Concepts — Product Research

Researched: 2026-02-15
Developer website: http://www.ulrichmedicalconcepts.com

## Overview

Ulrich Medical Concepts (UMC) is a small, privately held EHR vendor based in Paducah, Kentucky, founded over two decades ago. The company has approximately 22–26 employees and an estimated annual revenue of ~$1.4M. The developer contact listed on CHPL is Sandra Ulrich. UMC serves ambulatory medical practices across multiple disciplines including primary care, internal medicine, dermatology, OB/GYN, general surgery, urgent care, and therapy practices. Their sole product is Team Chart Concept (TCC), a fully integrated EHR and practice management system. UMC describes TCC as built "by physicians for physicians." The company is a very small niche vendor serving what appears to be a modest customer base of solo practitioners, mid-sized clinics, and some hospital-based groups, primarily in the southeastern United States (Kentucky-area presence is apparent from their cancer registry work with KHIE, the Kentucky Health Information Exchange).

## Product: Team Chart Concept (TCC)

CHPL ID: 10227
Version: 7.1
Certification date: 2019-12-26

### What It Is

Team Chart Concept (TCC) is a fully integrated EHR and practice management suite. It is not a component of a larger product — TCC *is* the product, combining clinical documentation, practice management, billing, scheduling, and document management in a single system. The certified module covers the full product. The name "Team Chart Concept" reflects the philosophy that every staff member (clerical, clinical, nursing, providers) is part of a "team" managing the patient "chart," which encompasses all clinical, financial, and scheduling information.

TCC uses a ribbon-based interface (similar to Microsoft Office) and supports button-based navigation for rapid clinical data access. It can be deployed either on-premise or cloud-hosted.

The product is certified for a broad set of ONC criteria (30+), spanning clinical data (a)(1)–(a)(14), transitions of care (b)(1), FHIR APIs (g)(7)–(g)(10), clinical quality measures (c)(1), and immunization registry reporting (h)(1). This breadth confirms it is a full-featured certified EHR, not a narrow specialty module.

### Users & Market

**Target users**: Medical office personnel including physicians, nurse practitioners, physician assistants, nurses, therapists, administrative/billing staff, and office managers — as stated in the CHPL SED intended user description: "Medical office personnel, including RNs, Providers, Admins and Support staff."

**Clinical settings**: Solo practices, mid-sized ambulatory clinics, urgent care clinics, and hospital-based groups. The FAQ page notes that "smaller practices are fully operational in two to three months," suggesting their typical customer is on the smaller side.

**Specialties**: Primary care, internal medicine, dermatology, OB/GYN, general surgery, urgent care, therapy practices. The system accommodates mixed-discipline environments with educational, mental health, medical, and administrative staff.

**Customer count**: Not disclosed. Given the company's size (~22 employees, ~$1.4M revenue), the customer base is likely quite small — probably dozens to low hundreds of practices rather than thousands.

**Notable deployments**: UMC was noted as the first EHR in the U.S. to establish real-time cancer registry reporting connectivity, demonstrated through work with the Kentucky Health Information Exchange (KHIE).

### Modules & Functionality

TCC is described as a single integrated suite rather than a collection of separate modules. Based on vendor materials, the following functional areas are described:

**Clinical Documentation / EHR**
- Rapid documentation of encounter notes (source: capabilities page)
- Customizable templates for medical and non-medical specialties (source: EHR overview page)
- Full support for dictation, voice recognition, and handwriting recognition (source: features page)
- Health maintenance alerts and reminders (source: features page)
- Risk factor analysis (source: capabilities page)
- Clinical quality measures dashboard with automated reporting (source: capabilities page)
- ICD-10 compliant coding (source: capabilities page)

**Electronic Prescribing**
- Integrated e-prescribing via NewCrop (third-party service; disclosed as a separate cost item — one-time fee plus monthly per-prescriber fee) (source: cost disclosure page)
- Direct connection with pharmacies (source: features page)

**Practice Management & Billing**
- Full HIPAA-compliant billing routines (source: capabilities page)
- Print or electronically file claims (source: practice management page)
- SmartCoder claims scrubbing functionality (source: capabilities page)
- Post payments manually, in batches, or via electronic remittance (source: practice management page)
- Management-by-Exception financial reporting (source: practice management page)
- One-click Financial Summary generation (source: practice management page)
- Collections and productivity tracking reports (source: practice management page)
- Statement printing (source: practice management page)
- Audit of all financial operations (source: practice management page)

**Scheduling**
- Search for next available appointment (source: practice management page)
- Multi-provider, multi-location, multi-equipment scheduling (source: features page)
- Patient reminders and appointment confirmations (source: practice management page)
- In-office patient flow management (source: practice management page)
- Reschedule, cancel, or reassign blocks of appointments (source: practice management page)
- Eligibility checking (source: EHR overview page)
- Download provider schedules to mobile devices for rounds or surgery (source: practice management page)

**Document Management**
- Integrated document management system (source: features page)
- Scanning and drag-and-drop functionality for document ingestion (source: EHR overview page)
- Manages patient charts, office forms, and other documents (source: features page)

**Lab & Diagnostic Interfaces**
- Bi-directional connectivity to lab vendors (source: main website)
- Communication with laboratory facilities (source: features page)
- Multi-facility connectivity including labs, pharmacies, and hospitals (source: capabilities page)

**Interoperability & Data Exchange**
- HL7 messaging (source: interoperability page)
- Clinical Document Architecture (CDA) format support (source: interoperability page)
- Direct Messaging — disclosed as separate cost (one-time setup + monthly per-address fee) (source: cost disclosure page)
- Health information exchange connectivity (demonstrated with KHIE) (source: interoperability page)
- Cancer registry electronic reporting (source: interoperability page, capabilities page)
- FHIR API / Standardized API access — disclosed as separate cost (one-time setup + monthly service fee) (source: cost disclosure page)

**Patient Portal**
- Patient portal integration via Medfusion (third-party; disclosed as separate cost — setup fee + monthly fee) (source: cost disclosure page)
- More recently, partnership with Bridge patient engagement platform for enhanced patient portal capabilities including medical records access, messaging, appointments, notifications/reminders, patient forms, and caregiver/dependent management (source: Bridge partnership announcement)

**Reporting**
- Standard and ad hoc reporting suite (source: features page)
- Graphs using clinical and financial data combinations (source: EHR overview page)
- User-defined records for custom tracking and trending (source: EHR overview page)
- PQRS (quality reporting) capability (source: capabilities page)
- Clinical quality measures dashboard (source: capabilities page)

### Data & Content

Based on the described features and functionality, TCC stores and manages the following categories of data:

**Clinical data**: Patient demographics, encounter notes/visit documentation, health maintenance records, clinical alerts, risk factors, clinical quality measures data, problem lists, medication lists, allergy lists (implied by certified criteria (a)(1)–(a)(8)), vital signs, and clinical templates/forms.

**Prescription data**: E-prescribing records flow through NewCrop (Surescripts-connected) — the cost disclosure explicitly lists NewCrop as a separate billable integration, confirming prescription data is managed.

**Lab and diagnostic data**: Bi-directional lab interfaces mean lab orders and results are stored in the system.

**Financial/billing data**: Claims, payments (manual, batch, and electronic remittance), financial summaries, collections data, billing audits, and statements. The practice management page is quite explicit about financial data management.

**Scheduling data**: Appointments, provider schedules, patient flow tracking, appointment confirmations and reminders.

**Documents**: Scanned documents, office forms, and other document management content.

**Patient portal data**: Messages, forms, and patient-facing records — managed through third-party integrations (Medfusion or Bridge), so the extent to which this data resides in TCC vs. the portal platform is unclear.

**Interoperability records**: CDA documents, Direct messages, HL7 transactions, cancer registry submissions.

**EHI export format**: The cost disclosure page states records can be exported as "PDF or C-CDA format. Records for a patient are exported to one or more PDF/C-CDA files." This is a limited export format that may not cover all data categories (particularly billing/financial data, scheduling data, scanned documents, and portal messages).

---

## Research Gaps & Notes

- **Customer count unknown**: UMC does not disclose how many practices use TCC. The company's small size suggests a modest customer base.
- **No third-party reviews found**: No reviews were found on G2, Capterra, KLAS, or similar platforms. The vendor is likely too small to appear in these databases.
- **Patient portal architecture unclear**: The patient portal is provided by third parties (Medfusion and/or Bridge). It's unclear how much portal data (messages, forms, etc.) is stored within TCC itself vs. solely in the portal platform.
- **Cloud vs. on-premise data differences**: TCC can be deployed either way; data architecture may differ between deployments.
- **No acquisitions or rebranding noted**: UMC appears to have been the same company with the same product name for its entire 20+ year history.
- **Mobile capabilities**: Limited to Windows tablets and downloading schedules to mobile devices — no native mobile app mentioned.
