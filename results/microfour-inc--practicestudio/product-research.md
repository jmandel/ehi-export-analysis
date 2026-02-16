# MicroFour, Inc. — Product Research

Researched: 2026-02-16
Developer website: http://www.practicestudio.net

## Overview

MicroFour, Inc. is a small, privately held, family-founded healthcare IT company headquartered in Amarillo, Texas, established in 1989. The company employs approximately 21–31 people and has been developing EHR software for over 25 years. Their flagship product is PracticeStudio, a fully integrated Electronic Health Records (EHR) and Practice Management (PM) system used by medical clinics across all 50 US states. MicroFour also develops RxWriter (their e-prescribing module, Surescripts-certified) and StrataFrame (a proprietary .NET application framework used internally and externally). The company appears to be a small, niche vendor serving primarily small-to-midsize ambulatory practices. They have no known acquisition history or parent company — they remain independently operated. MicroFour was recognized in Healthcare Tech's Top 10 EHR list (2016) and Medical Economics' Top 50 EHR list (2014), suggesting modest industry recognition.

## Product: PracticeStudio

CHPL ID: 9590 (PracticeStudio X20, certified 2018-08-10)

### What It Is

PracticeStudio is a complete, integrated EHR and Practice Management system — not a modular or component product. The certified module encompasses the entire product: there is no separate billing system, scheduling system, or clinical module sold independently. It is marketed as a "Complete Certified EHR" covering both clinical documentation and practice management in a single platform. The product is built on the Microsoft .NET platform using Microsoft SQL Server, and is available in both cloud-hosted and on-premise (server-based) deployment options. It supports touchscreen-based charting on tablets and workstations.

The certification covers a broad set of criteria: clinical data (a)(1)–(a)(5), (a)(12), (a)(14); transitions of care (b)(1)–(b)(3); patient portal (e)(1), (e)(3); clinical quality measures (c)(1)–(c)(4); FHIR/API access (g)(7), (g)(9), (g)(10); and immunization registry reporting (h)(1). This breadth confirms it functions as a full-featured ambulatory EHR.

### Users & Market

PracticeStudio targets small-to-midsize ambulatory medical practices. It serves multiple specialties with pre-built, customizable templates ("Blueprints") including: cardiology, chiropractic, dermatology, family medicine, internal medicine, orthopedics, and urgent care. The vendor's website emphasizes specialty-specific workflows and templates that are ready "out of the box."

The product is used by clinics in all 50 US states, though specific customer counts are not publicly disclosed. Given MicroFour's small size (~21–31 employees), the customer base is likely in the hundreds rather than thousands. Day-to-day users include physicians, clinical staff, billing staff, and practice managers — the product covers the full practice workflow from scheduling through billing.

No notable large-system deployments or case studies were found publicly. The vendor provides on-site training nationwide and telephone support, suggesting direct sales rather than channel partners.

### Modules & Functionality

PracticeStudio is described as a single integrated product, but it encompasses the following functional areas based on vendor materials:

**Clinical / EHR:**
- Touch-based charting with customizable, discipline-specific workflows and templates (vendor website)
- SOAP notes and narrative clinical documentation (vendor website)
- Provider dashboard (vendor "Why PracticeStudio" page)
- e-Prescribing via RxWriter — Surescripts-certified for prescription routing (new and renewals), prescription benefits/formularies, and medication history (certifications page)
- Drug interaction and allergy/adverse reaction checking (vendor website)
- Lab orders and results with bidirectional lab integration (web search results referencing vendor materials)
- Document and media management — upload and manage documents, images, and media files in patient records (web search results)
- Clinical quality measure (CQM) calculation and reporting — certified for 30 CQMs (certifications page)
- Immunization registry reporting (certified criterion (h)(1))

**Practice Management:**
- Appointment scheduling with wave scheduling, recurring appointments, and multi-location support (web search results)
- Patient check-in and check-out workflow — "beginning-to-end patient flow" (vendor website)
- Claims management and scrubbing (vendor "Why PracticeStudio" page)
- Electronic claims submission and remittance processing (vendor family practice page)
- Insurance eligibility verification (web search results)
- Patient ledger and billing (web search results)
- ICD-10 coding support (certifications page mentions ICD-10 readiness)
- Visit statistics and practice analytics with customizable graphical reports (vendor website)
- Inventory tracking and point-of-sale integration (vendor "Why PracticeStudio" page)

**Patient Engagement:**
- Patient Portal (hosted at v2.patientwebportal.com) — allows patients to view visit summaries, lab results, communicate securely with staff, and upload/download medical records (portal page)
- Secure two-way messaging between patients and providers/staff through the portal (portal page)
- Email notifications for portal activity (portal page)
- CCD (Continuity of Care Document) generation and sharing via portal or DIRECT messaging (portal page)
- Text and email appointment reminders (web search results)

**Interoperability:**
- HL7 support (4010 and 5010) — certified HL7 solution provider (vendor website)
- DIRECT SMIME email for transitions of care using phiMail Server (certifications page)
- FHIR API access (certified criteria (g)(7), (g)(9), (g)(10))
- Surescripts network integration for e-prescribing (certifications page)

**Infrastructure:**
- DataVault — automated online backup solution for practice data, HIPAA-compliant (vendor website)
- Cloud and on-premise deployment options (vendor website)

### Data & Content

Based on the product's described functionality, PracticeStudio stores or manages the following categories of data:

- **Patient demographics and registration data** — implied by full practice management and check-in workflows
- **Clinical encounter documentation** — SOAP notes, customizable charting templates, provider notes (vendor website describes touch-based charting)
- **Medication data** — prescriptions via RxWriter, medication history from Surescripts, allergy and adverse reaction records (certifications page, vendor materials)
- **Lab orders and results** — bidirectional lab integration (web search results citing vendor materials)
- **Documents and media** — uploaded images, documents, and media files associated with patient records (web search results)
- **Diagnoses and problem lists** — ICD-10 coding, diagnosis entry during encounters (vendor website)
- **Scheduling data** — appointments, recurring schedules, multi-location scheduling (web search results)
- **Billing and claims data** — charges, claims, remittances, patient ledger, insurance information, eligibility verification (vendor website describes integrated billing and claims management)
- **Inventory and point-of-sale data** — for practices that stock and dispense products (vendor "Why PracticeStudio" page)
- **Patient portal messages** — secure two-way communications between patients and staff (portal page)
- **Clinical quality measure data** — CQM calculations for 30 certified measures (certifications page)
- **CCDs / Continuity of Care Documents** — generated for transitions of care and patient portal sharing (portal page)
- **Immunization records** — implied by immunization registry reporting certification (h)(1)
- **Visit statistics and analytics** — practice performance data and customizable reports (vendor website)

The vendor website does not mention behavioral health, inpatient/hospital workflows, or long-term care functionality. There is no mention of radiology/imaging integration beyond document uploads. The product appears focused entirely on the ambulatory outpatient setting.
