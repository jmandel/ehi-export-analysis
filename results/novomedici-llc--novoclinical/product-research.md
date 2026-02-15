# NovoMedici, LLC — Product Research

Researched: 2026-02-14
Developer website: https://www.novomedici.com/

## Overview

NovoMedici, LLC is a small EHR vendor based in Ogden, Utah, that develops and sells NovoClinical, a cloud-based electronic health record and practice management platform. The company describes nearly 20 years of research and development preceding the product's launch. NovoMedici is very small — ZoomInfo lists approximately 5–9 employees across the NovoMedici and NovoClinical entities. The company positions NovoClinical as a "fully integrated EMR system designed by practicing physicians," targeting small to mid-sized ambulatory medical practices. The vendor emphasizes a modular, scalable pricing model ("pay only for what is needed") and a user interface modeled after traditional paper charts to ease adoption. NovoClinical is cloud-hosted and accessible across devices including tablets and iPads. The company has no publicly noted acquisition history, parent company, or rebranding — it appears to be an independent, bootstrapped operation.

## Product: NovoClinical

CHPL IDs: 10805

### What It Is

NovoClinical is an all-in-one ambulatory EHR and practice management system. It combines clinical documentation, billing/revenue cycle management, scheduling, e-prescribing, patient portal, telemedicine, and chronic care management into a single integrated platform. The certified module (NovoClinical version 1.0, certified 2022-01-31) appears to be the whole product — there is no indication of separate products or platforms. It is certified against a broad set of ONC criteria spanning clinical (a)(1)–(a)(5), (a)(12), (a)(14); care coordination (b)(1)–(b)(3), (b)(10)–(b)(11); patient portal (e)(1); CQMs (c)(1)–(c)(3); public health reporting (f)(1), (f)(2), (f)(5); APIs (g)(7), (g)(9), (g)(10); and direct messaging (h)(1).

### Users & Market

The CHPL metadata describes intended users as "Providers, Nurses and Medical assistant." Third-party review sites describe the target market as small to mid-sized medical practices, including solo practitioners, independent clinics, and multi-provider practices. Supported specialties include general practice, cardiology, immunology, gastroenterology, OB/GYN, pediatrics, and dermatology. The product is priced at $99–$385/provider/month depending on module selection (specific features only vs. EMR only vs. EMR + practice management). No specific customer counts or notable deployments were found in any source. The company does not appear to have significant market share — it has a modest number of reviews on Capterra and other directories (around 30 reviews on FindEMR, with 85% excellent ratings). Users praise customer service and the intuitive interface but note that billing/RCM features could be improved.

### Modules & Functionality

Based on vendor materials, third-party review sites, and the features page, NovoClinical includes the following modules and capabilities:

**Clinical Documentation / EHR:**
- Charting with customizable templates and reports
- Voice recognition technology for dictation
- Decision support (clinical decision support / CPOE — certified (a)(1)–(a)(5))
- Order and result tracking
- Problem lists, medication lists, medication allergy lists (certified (a)(1)–(a)(4))
- Clinical information reconciliation (certified (a)(12))
- Implantable device list (certified (a)(14))

**E-Prescribing:**
- Electronic prescribing (e-Rx), implied integration with Surescripts or similar network via API/HL7 integrations described on the features page

**Scheduling & Check-in:**
- Appointment scheduling
- Auto check-in via iPad/tablet with automatic EHR syncing
- Appointment reminders

**Practice Management:**
- Patient registration and demographic management
- Check-ins, referrals, and reporting
- Patient eligibility verification

**Billing & Revenue Cycle Management (RCM):**
- Medical billing and coding
- UB-04 billing support
- Claim scrubbing
- Durable Medical Equipment (DME) billing
- Medical accounting
- Statement generation
- Credit card payment integration
- Claims processing and payment collection

**Patient Portal:**
- Secure patient messaging
- Access to visit summaries, lab results, and medication details
- Online appointment scheduling
- Patient input of demographics and medical history
- E-signature for documents
- Offered free with the EHR

**Telemedicine:**
- Virtual visit capabilities for patients with limited mobility or scheduling constraints

**Chronic Care Management (CCM):**
- Monitoring and tracking for patients with chronic conditions (diabetes, hypertension, heart disease)

**Communication & Messaging:**
- Built-in e-fax
- Text messaging (SMS)
- Alerts and notifications
- Task management
- Direct messaging (certified (h)(1))

**Integrations:**
- API/HL7 integrations with laboratories, imaging centers, e-prescribing networks
- Radiology Information Systems (RIS) integration
- Picture Archiving and Communication Systems (PACS) integration
- ICD-10 coding support

**Public Health Reporting:**
- Immunization registry reporting (certified (f)(1))
- Syndromic surveillance (certified (f)(2))
- Cancer case reporting (certified (f)(5))

**Interoperability & Data Exchange:**
- Transitions of care (certified (b)(1)–(b)(3))
- FHIR API access (certified (g)(7), (g)(9), (g)(10))
- Patient portal view/download/transmit (certified (e)(1))

### Data & Content

Based on the features described above and the certification criteria, NovoClinical stores and manages the following categories of data:

**Clinical data:** Patient demographics, medical history, problem lists, medication lists, medication allergy lists, implantable device lists, clinical notes/charting, visit summaries, lab orders and results, imaging orders and results (via RIS/PACS integration), vital signs, immunization records.

**Prescribing data:** E-prescriptions, medication history (implied by e-prescribing and medication list features).

**Scheduling and administrative data:** Appointments, patient check-in records, referrals, tasks, alerts/notifications.

**Billing and financial data:** Claims, billing codes (ICD-10, UB-04), payment records, credit card transactions, statements, accounts receivable, DME billing records. Multiple sources confirm billing is built into the platform, not a separate product.

**Patient portal data:** Patient-entered demographics and medical history, secure messages between patients and providers, e-signed documents, appointment requests.

**Telemedicine data:** Virtual visit records (how these are stored — as notes, separate encounters, or otherwise — is not specified in available materials).

**Chronic care management data:** Care plans, monitoring data for chronic conditions (specifics not detailed in available materials).

**Communication records:** E-faxes, text messages, direct messages (via Direct protocol).

**Public health reporting data:** Immunization registries, syndromic surveillance data, cancer case reports.

**Gaps and uncertainties:** The vendor website is relatively sparse on deep technical details. Third-party integration specifics are limited — FindEMR notes the vendor "has not specified the details about its specific third-party integrations." There is no publicly available data dictionary or schema documentation beyond the EHI export format PDF. The exact scope of data stored for telemedicine encounters and chronic care management is not well-documented in publicly available materials. Review sites note some limitations in the RCM module, suggesting it may not be as feature-complete as the clinical side.
