# Nextech — Product Research

Researched: 2026-02-16
Developer website: https://www.nextech.com

## Overview

Nextech is a specialty-focused healthcare IT company based in Tampa, FL, providing integrated EHR, practice management, and revenue cycle management software to specialty physician practices. The company serves 16,000+ medical practices and 11,000+ physicians across five primary specialties: dermatology, ophthalmology, orthopedics, plastic surgery, and med spa. Nextech positions itself as the leading specialty-specific alternative to generic EHR platforms, winning Best in KLAS for Ambulatory Specialty EHR in 2024 and 2025, and Best in KLAS for Ambulatory Ophthalmology Solutions in 2025 and 2026.

Nextech has been through several private equity transitions: Francisco Partners sold the company to Thomas H. Lee Partners in 2019 for ~$500M, which in turn sold to TPG in 2023 for $1.4B. The company has grown through acquisitions, notably acquiring SRS Health (an orthopedic-focused EHR) in January 2019 and TouchMD (a visual consultation, marketing, and imaging platform for aesthetic/surgical practices) in October 2022. The company also launched an AI-powered documentation tool called Cora Scribe in January 2026 and has a partnership with Ocuco for integrated optical software.

Nextech operates multiple distinct software platforms under its umbrella, which is critical context for understanding their CHPL certifications. Their developer portal lists four separate platforms with their own APIs: IntelleChartPRO (ICP), NexCloud/Select, SRSPro, and Nextech Practice+ PM. The two CHPL-certified products correspond to two of these: "Nextech EHR (ICP)" is IntelleChartPRO, and "SRS EHR" is SRSPro.

---

## Product: Nextech EHR (ICP) — IntelleChartPRO

CHPL ID: 11724
CHPL Product Number: 15.04.04.2051.Inte.09.02.0.251202
Version: 9
Certification Date: 2025-12-02

### What It Is

IntelleChartPRO (ICP) is Nextech's cloud-based EHR platform. The "ICP" in the CHPL listing stands for IntelleChartPRO, confirmed by the developer portal which lists "ICP (IntelleChartPRO) R4 bundle" as a FHIR endpoint. It is a full-featured clinical EHR with integrated practice management, designed specifically for specialty medical practices. The platform is cloud-based/SaaS, accessible from any device including iPad and mobile apps.

ICP is certified for a broad set of criteria including clinical data management (a)(1)–(a)(5), (a)(12), (a)(14); transitions of care (b)(1)–(b)(2), (b)(10)–(b)(11); patient portal/view-download-transmit (e)(1); clinical quality measures (c)(1)–(c)(3); FHIR API access (g)(7), (g)(9), (g)(10); and syndromic surveillance (f)(5). The (e)(1) certification for patient portal and (g)(10) for Standardized FHIR API are notable — these are present in ICP but absent from SRS EHR.

### Users & Market

IntelleChartPRO serves specialty ambulatory practices, primarily in dermatology, ophthalmology, plastic surgery, orthopedics, and med spa. End users include physicians, clinical staff, billing staff, and practice managers. The platform is used by solo practitioners through multi-site specialty groups. Nextech states its customers include 11,000+ physicians and 60,000+ office staff across their platforms.

The product won Best in KLAS for Ambulatory Specialty EHR (2024, 2025) and Ambulatory Ophthalmology Solutions (2025, 2026). It also holds AAD (American Academy of Dermatology) DataDerm Gold Recognition — a quality registry endorsement specific to dermatology.

### Modules & Functionality

Based on vendor materials, product pages, and third-party reviews, IntelleChartPRO includes:

**Clinical Documentation & Charting:**
- Customizable specialty-specific templates with "Adaptive Template Technology" that selects appropriate templates based on patient context and filters out unrelated information
- Smart stamping for charting efficiency
- IntelleDraw tool for drawing/annotating directly within the EHR (particularly for ophthalmology)
- iPad and mobile provider apps for reviewing charts, signing labs, and charting
- Voice recognition support for documentation
- AI-powered Cora Scribe ambient documentation (launched January 2026) — listens to natural conversations and generates clinical notes

**e-Prescribing:**
- Integrated e-prescribing with pharmacy integration

**Orders & Labs:**
- Lab integration and lab order management
- Lab result review on mobile devices

**Imaging & Photos:**
- Photo management with markup/drawing capabilities integrated into the EHR
- Integration with TouchMD for visual consultation, before/after photos, and patient education imaging
- Image-intensive workflow support (noted as a strength in reviews for dermatology/plastic surgery/ophthalmology)

**Practice Management & Scheduling:**
- Advanced scheduling for multi-location, multi-provider operations
- Appointment management
- Referral management

**Billing & Revenue Cycle:**
- Integrated billing with claims management and coding (EM coding)
- Nextech Payments — integrated payment processing accepting all forms of payment
- Point of sale (POS) functionality
- Recurring transactions and membership program billing
- Payment plans and automated billing
- Inventory management with automated planning, purchasing, and tracking
- ASC (Ambulatory Surgery Center) billing capability
- MIPS compliance monitoring (customers report ~97% average MIPS scores)
- Revenue Cycle Management (RCM) services available

**Patient Engagement:**
- Patient portal with online scheduling, bill pay, and mobile medical record access
- Two-way texting for patient communication
- Telehealth capabilities
- TouchMD integration for visual consultation and patient education

**Specialty-Specific Features:**
- Cosmetic functionality: quotes, packages, gift cards with tracking
- Lead management with automated capture, tracking, and marketing campaign tracking
- Membership and subscription management (med spa/aesthetics)
- CRM (customer relationship management) tools
- Regulatory performance monitoring for reimbursement optimization

**Analytics & Reporting:**
- Advanced analytics and reporting
- Customizable dashboards
- Population health data capabilities

**Integrations:**
- FHIR R4 API (SMART on FHIR compliant)
- HL7 FHIR Standards API
- Ocuco integration for optical software (ophthalmology retail/dispensary)
- Surescripts for e-prescribing (implied by e-prescribing certification)

### Data & Content

Based on the features described above and the certification criteria, IntelleChartPRO stores and manages:

- **Patient demographics** — confirmed by FHIR API documentation and multiple feature descriptions
- **Clinical notes and encounter documentation** — extensive charting templates, smart stamping, AI-generated notes (Cora Scribe)
- **Problem lists, medication lists, allergies** — certified for (a)(1) CPOE meds, (a)(2) CPOE labs, (a)(3) CPOE imaging, (a)(5) demographics, (a)(14) implantable device list
- **Orders** — medication orders, lab orders, imaging orders (certified for CPOE across all three)
- **Prescriptions** — e-prescribing data
- **Lab results** — lab integration with mobile review
- **Clinical images and photos** — before/after photos, annotated drawings (IntelleDraw), TouchMD visual consultation images
- **Documents** — document management referenced in feature lists
- **Scheduling data** — appointments, multi-provider/multi-location scheduling
- **Billing and claims data** — claims, payment history, POS transactions, recurring billing, membership/subscription billing
- **Inventory data** — product/supply tracking with automated purchasing
- **Patient portal content** — patient messages, portal access logs, shared records
- **Patient communications** — two-way text messages
- **Quality measures data** — CQM reporting (c)(1)–(c)(3), MIPS scores
- **Syndromic surveillance data** — certified for (f)(5)
- **Lead/CRM data** — lead tracking, marketing campaign data, patient relationship management
- **Cosmetic/aesthetic data** — quotes, packages, gift cards, cosmetic procedure tracking
- **Telehealth session data** — telehealth visit records
- **Implantable device data** — certified for (a)(14) implantable device list
- **Care plan data** — transitions of care documents (b)(1), (b)(2)

Third-party reviews note that the system is strong on image management and specialty-specific documentation, but weaker on billing/claims management (70% of reviewers in one survey reported problems with billing features) and scheduling reliability.

---

## Product: SRS EHR (SRSPro)

CHPL ID: 11040
CHPL Product Number: 15.04.04.2051.SRSE.12.03.1.221202
Version: 12
Certification Date: 2022-12-02

### What It Is

SRS EHR — also known as SRSPro — is Nextech's second certified EHR platform, originating from SRS Health, which Nextech acquired in January 2019. SRS Health was historically the leading EHR for orthopedic practices, with over 5,000 providers at the time of acquisition. It was also used by ophthalmologists, cardiologists, and other specialists. SRSPro is a distinct platform from IntelleChartPRO, with its own API (Swagger-documented, per the developer portal) and its own CHPL certification.

SRS EHR is certified for clinical data (a)(1)–(a)(5), (a)(9), (a)(12), (a)(14); transitions of care (b)(1)–(b)(2), (b)(10); patient request for data export (e)(3) but NOT (e)(1) patient portal view-download-transmit; clinical quality measures (c)(1)–(c)(3); immunization/syndromic reporting (f)(1), (f)(5); and API access (g)(2)–(g)(7) but NOT (g)(9)–(g)(10) for Standardized FHIR API. It also has (h)(1) for direct secure messaging. The absence of (e)(1) and (g)(10) suggests SRSPro may not have the same level of patient-facing portal or modern FHIR API as IntelleChartPRO.

### Users & Market

SRS EHR was historically the dominant EHR in orthopedic surgery, and SRS Health was described as "preeminent among orthopedists" at the time of acquisition. It also served ophthalmologists, cardiologists, and other surgical specialists. The platform is known for speed and efficiency in high-volume practice settings, with streamlined workflows designed for surgical specialties.

At the time of the 2019 acquisition, SRS Health had 5,000+ providers. It is unclear how many current SRS EHR users exist vs. how many have migrated to IntelleChartPRO or NexCloud, but the product maintains active CHPL certification (certified 2022).

### Modules & Functionality

Less specific information is publicly available about SRSPro's feature set compared to IntelleChartPRO, since Nextech's current marketing focuses on the unified "Nextech" brand. Based on what was found:

**Clinical Documentation:**
- EHR with specialty-specific templates
- Emphasis on speed and efficiency for high-volume surgical practices
- Clinical workflow tools optimized for orthopedics

**Practice Management:**
- Scheduling and appointment management
- PM system with ASC billing capability (per vendor materials about surgical billing)

**Billing:**
- Billing and claims management
- PACS (Picture Archiving and Communication System) integration — SRS Health was described as providing "EHR/EMR, PM, and PACS software solutions"

**Orders & Prescribing:**
- CPOE for medications, labs, and diagnostic imaging (certified (a)(1)–(a)(4))
- e-Prescribing (certified (a)(1))

**Clinical Decision Support:**
- CDS interventions (certified (a)(9))

**Reporting:**
- CQM reporting (c)(1)–(c)(3)
- Immunization reporting (f)(1)
- Syndromic surveillance (f)(5)

**Data Exchange:**
- Direct secure messaging (h)(1)
- Transitions of care (b)(1), (b)(2)

### Data & Content

Based on the certification criteria and available product information, SRS EHR stores:

- **Patient demographics** — (a)(5) certified
- **Clinical documentation** — encounter notes, specialty templates
- **Problem lists, medication lists, allergies** — standard clinical lists
- **Orders** — medication, lab, and imaging orders via CPOE
- **Prescription data** — e-prescribing
- **Imaging data / PACS** — SRS Health was explicitly described as a PACS solution provider
- **Lab results** — lab integration
- **Implantable device data** — (a)(14) certified
- **Scheduling data** — appointment management
- **Billing/claims data** — integrated PM billing
- **Quality measures data** — CQM, immunization, and syndromic reporting
- **Care transitions documents** — C-CDA documents for transitions of care
- **Secure messages** — direct messaging (h)(1)

Notably, SRS EHR is NOT certified for (e)(1) patient portal view-download-transmit, which may mean it either lacks a patient portal or relies on a separate system for patient-facing access. It IS certified for (e)(3) patient health information export request, suggesting patients can request data exports but may not have a self-service portal.

---

## Key Observations for EHI Export Assessment

1. **Two distinct platforms**: IntelleChartPRO (ICP) and SRSPro are separate technical platforms with separate APIs, separate CHPL certifications, and likely separate databases. The EHI export documentation at the shared URL may need to cover both platforms distinctly.

2. **A third platform exists**: NexCloud/Select also has FHIR APIs listed on the developer portal but does not appear in the CHPL metadata provided. It's unclear whether NexCloud is a separate product or a rebranded version of one of the others.

3. **Rich data beyond clinical**: Both platforms — but especially ICP — store significant non-clinical data including billing/claims, inventory, CRM/lead management, cosmetic/aesthetic business data, marketing campaign data, patient communications (text messages), and TouchMD visual consultation content. A complete EHI export should account for all of this.

4. **Specialty-specific data**: The products store specialty-specific clinical data (ophthalmology drawings, dermatology images, orthopedic PACS, cosmetic before/after photos) that may require specialized export handling beyond standard C-CDA documents.

5. **Acquisition history creates complexity**: The SRS Health acquisition (2019) and TouchMD acquisition (2022) mean the "Nextech" product ecosystem includes components with different technical origins, which may affect how comprehensively data can be exported from a unified system.
