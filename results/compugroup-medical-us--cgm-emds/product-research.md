# CompuGroup Medical US — Product Research

Researched: 2026-02-15
Developer website: https://www.cgm.com/us

## Overview

CompuGroup Medical SE & Co. KGaA (CGM) is a large German healthcare IT company headquartered in Koblenz, Germany. It is one of the world's largest e-health companies, with EUR 1.15 billion in 2024 revenue, over 8,700 employees globally, presence in 19 countries, and products used in 60 countries by more than 1.6 million users (physicians, dentists, pharmacists, healthcare institutions). The company was founded in 1987 by Frank Gotthardt and originally focused on dental information systems before expanding broadly. CGM delisted from the stock exchange in June 2025 after CVC Capital Partners took a ~28% stake.

CGM's US operations (CompuGroup Medical US) are headquartered in Austin, Texas. The US business grew significantly through the **acquisition of eMDs in November 2020 for $240 million**. eMDs itself had previously been acquired by Marlin Equity Partners in 2015, and under Marlin's ownership had consolidated several ambulatory EHR products: it acquired McKesson's ambulatory software portfolio (Medisoft, Lytec, Practice Partner) in 2016 and Aprima Medical Software in 2019. By the time CGM acquired eMDs, the combined entity served 60,000+ providers across 32,000+ facilities in 70+ medical specialties with approximately 1,400 employees.

Today, CGM US offers a portfolio of EHR and practice management products (CGM APRIMA, CGM eMDs, CGM CLINICAL, CGM ENTERPRISE EHR, CGM PLUS, CGM PRACTICE PARTNER), laboratory information systems (CGM LABDAQ, CGM MEDICUS, CGM SCHUYLAB), billing/RCM services (ARIA, eMEDIX clearinghouse), telehealth (CGM ELVI), and AI documentation (CGM AMBI). CGM positions itself as a top-4 provider in the US ambulatory information systems market.

## Product: CGM eMDs

CHPL ID: 11133
CHPL Product Number: 15.04.04.2700.eMDs.10.02.1.221227
Version: v10
Certification Date: 2022-12-27
Certification Body: Drummond Group

### What It Is

CGM eMDs (formerly "e-MDs Solution Series") is an **integrated EHR and practice management suite** designed for ambulatory/outpatient medical practices. It was originally created in 1996 by Dr. David Winn and a group of family practitioners in Austin, Texas, with a philosophy of being "designed by physicians, for physicians." It was one of the first six ambulatory systems certified by CCHIT in 2007 and has historically received strong rankings in AAFP Family Practice Management surveys.

The product is a single certified module that encompasses clinical charting, e-prescribing, scheduling, practice management, billing, and patient engagement. It is not a component of a larger product — it is itself the full product, though it integrates with several CGM add-on products and services (eMEDIX clearinghouse, ARIA RCM services, CGM AMBI ambient AI, CGM PAY payment processing, CGM CONNECTION patient communications).

The product is certified across 28 ONC criteria covering clinical documentation (a)(1)-(a)(5), (a)(12), (a)(14)-(a)(15); transitions of care (b)(1)-(b)(3); patient access (e)(3); public health reporting (f)(1), (f)(5); FHIR APIs (g)(7), (g)(9)-(g)(10); and EHI export (b)(10). This is a broadly certified product.

### Users & Market

**Target users**: Providers and clinical support staff (per CHPL listing). In practice, the system is used by physicians, nurses, medical assistants, front desk staff, billing staff, and practice managers.

**Clinical settings**: Small to medium ambulatory practices primarily, but also supports larger multi-site organizations, Community Health Centers (CHCs), Federally Qualified Health Centers (FQHCs), Rural Health Clinics (RHCs), and Patient-Centered Medical Homes (PCMHs).

**Specialties**: Supports 70+ medical specialties with customizable templates. Strong in primary care, family medicine, internal medicine, cardiology, dermatology, podiatry, OB/GYN, nephrology, and others. Includes a dedicated OB module.

**Scale**: At the time of the CGM acquisition (2020), eMDs served 60,000+ providers in 32,000+ facilities. CGM eMDs is one product within that portfolio, so the CGM eMDs-specific numbers are a subset, though exact breakdown is not publicly available.

**Deployment**: Available cloud-hosted or on-premise.

**Reviews**: User sentiment is mixed. On Capterra (46 reviews), the product has an overall rating of 2.2/5, with particularly low scores for value for money (1.9/5) and customer support (2/5). Positive reviews praise ease of use, fast learning curve ("new employees can learn in a couple of days"), highly customizable chart note templates, and flexibility. Negative reviews cite hidden costs, slow customer support, reliability issues with updates, and unexpected billing. ARIA RCM Services (a separate but related CGM offering) has won KLAS Best in KLAS for ambulatory RCM three consecutive years (2023-2025).

### Modules & Functionality

Based on vendor product pages, feature lists, and third-party descriptions, CGM eMDs includes the following modules:

**Clinical Documentation / Chart Module**
- Point-of-care note entry with multiple input methods: point-and-click, dictation, voice recognition
- Extensive template library covering 70+ specialties, customizable without programming
- Clinical decision support integrated into charting workflow
- Structured data: problem lists, allergies, vitals, immunizations, procedures, medication lists
- Social history and smoking status tracking
- Optional AI-enabled documentation via **CGM AMBI** (ambient AI that transcribes entire patient encounters, suggests diagnoses, orders, and billing codes)

**E-Prescribing (CGM PRESCRIBE)**
- Award-winning electronic prescribing module
- Electronic Prior Authorization (ePA)
- PDMP (Prescription Drug Monitoring Program) integration
- Benefit information at point of care
- Surescripts integration for medication history and routing
- EPCS (Electronic Prescribing for Controlled Substances) support

**Scheduling**
- Physician and equipment scheduling with complex rule enforcement
- Front office workflow optimization
- Patient satisfaction tracking

**Practice Management / Billing**
- Full integrated practice management system
- Billing and accounts receivable management
- Claims management and submission
- Automated common billing office functions
- Integrated with **eMEDIX clearinghouse**: real-time eligibility verification, electronic remittance advice (ERA) posting, advanced claims edits/scrubbing, claim status automation, denial management and analysis
- **CGM PAY**: Integrated patient payment processing with card-on-file capabilities
- Optional **ARIA RCM Services**: Outsourced revenue cycle management

**Patient Portal / Patient Engagement**
- Integrated patient portal with health record access, appointment requests/confirmations, secure messaging, healthcare results sharing
- Bilingual interface
- Intake forms, medical history, screening questionnaires, surveys
- Full clinical record access for patients
- **CGM CONNECTION**: Automated text, email, and phone communications — appointment reminders, blast messaging (promotions, birthday messages, announcements), clinical engagement campaigns

**Document Management (DocMan)**
- Electronic document management for scanning paper documents, importing electronic files/images
- Central repository of all patient information from external sources

**Internal Messaging / Task Management (TaskMan)**
- Internal messaging and task assignment system
- Integrated with DocMan
- Enables sending messages/tasks with attached medical records, visit notes, and images

**Quality Reporting (CGM MEASURES)**
- MIPS dashboard for eCQM (electronic Clinical Quality Measures) reporting
- Real-time MACRA dashboard for MIPS/APM tracking

**Population Health**
- Population-focused care tools
- Preventive and chronic care tracking

**Mobile (nMotion)**
- iPad application for mobile care delivery

**Interoperability**
- FHIR API (certified under g(10))
- Surescripts RLE health information exchange
- CommonWell Health Alliance network compatibility
- Lab integrations with third-party lab systems
- C-CDA generation and consumption for transitions of care
- Supporting software integrations: NLM Access GUDI API, Updox, First Databank, Updox Direct, eCR Now, Cloverleaf

**Credentialing (ARIA)**
- Provider enrollment and credentialing services

### Data & Content

Based on the product's modules, certified criteria, and described features, CGM eMDs manages the following types of data:

**Clinical data** (strongly evidenced by ONC certification and product descriptions):
- Patient demographics (including language, race, ethnicity, preferred language)
- Clinical encounter notes / visit documentation
- Problem lists (diagnoses with ICD codes)
- Medication lists and prescription history
- Allergy and adverse reaction records
- Vital signs
- Immunization records
- Procedures
- Lab orders and results
- Social history and smoking status
- Care plans and clinical decision support alerts
- Referral information

**Prescribing data** (evidenced by CGM PRESCRIBE module and Surescripts integration):
- Electronic prescriptions (including controlled substances)
- Prior authorization records
- PDMP query results
- Medication benefit information

**Administrative/scheduling data** (evidenced by scheduling module):
- Appointment records
- Provider schedules
- Equipment scheduling

**Billing/financial data** (evidenced by integrated PM and eMEDIX clearinghouse):
- Insurance and guarantor information
- Claims data and submission history
- Eligibility verification records
- Electronic remittance advice (ERA)
- Patient payment records (via CGM PAY)
- Denial management data

**Document management data** (evidenced by DocMan module):
- Scanned paper documents
- Imported electronic files and images
- External source documents

**Communication data** (evidenced by TaskMan, patient portal, and CGM CONNECTION):
- Internal staff messages and task assignments
- Patient portal messages
- Patient communication logs (texts, emails, phone calls)
- Appointment reminders

**Quality/reporting data** (evidenced by CGM MEASURES):
- eCQM measure calculations
- MIPS/MACRA tracking data

**Interoperability documents**:
- C-CDA documents (sent and received)
- Care transition summaries

**Gaps/uncertainties**: The vendor website does not provide detailed database schema documentation publicly. The relationship between CGM eMDs core data and data held by add-on services (eMEDIX, ARIA RCM, CGM PAY, CGM CONNECTION) is unclear — some of this data may reside in separate systems rather than within the CGM eMDs database itself.
