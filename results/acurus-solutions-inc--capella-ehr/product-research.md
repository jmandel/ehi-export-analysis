# Acurus Solutions, Inc. — Product Research

Researched: 2026-02-16
Developer website: https://www.acurussolutions.com

## Overview

Acurus Solutions, Inc. is a subsidiary of Akido Labs, Inc., a Los Angeles-based AI and healthcare company founded in 2015 out of USC's Digital Health Lab by Jared Goodner and Prashant Samant. Akido Labs is a Y Combinator (W15) company that has raised $95.6M in total funding, including a $60M Series B led by Oak HC/FT in May 2025, with investors including Jeff Dean (Chief Scientist, Google DeepMind), Soma Capital, and Future Communities Capital.

The corporate structure spans two countries: Acurus Solutions, Inc. is headquartered in Pomona, California, while Acurus Solutions Private Limited operates out of Chennai, India (founded 1999 per corporate records, though some sources say 2006) with approximately 371 employees. The India entity is described as a "100% export oriented company" providing healthcare BPO, revenue cycle management, health information management, and technology development services to US healthcare customers. Acurus India's IndiaMART profile explicitly describes it as part of "U.S.-based Akido."

Akido Labs has evolved significantly. It started as a healthcare API middleware company (per a 2015 TechCrunch article describing a "standardized API layer for hospital app developers") and has grown into a vertically integrated care delivery + AI company. Today, Akido operates "Akido Care," a bicoastal medical network with 240+ providers across 26 specialties in approximately 100 clinics, serving over 500,000 patients across California, Rhode Island, and New York. Their flagship AI product "ScopeAI" is trained on 10M+ real patient cases and acts as a clinical co-pilot that guides medical assistants through patient visits, generates clinical documentation, and drafts diagnoses and care plans for physician review.

Capella EHR is the internally-developed electronic health record system that underpins this operation. It is certified under the Acurus Solutions brand but used within the broader Akido Labs ecosystem. Revenue for Akido Labs is reported at $18.3M (per DevCuration), and Outsource Accelerator reports Acurus Solutions' annual revenue at approximately $15.7M.

## Product: Capella EHR

CHPL ID: 10807

### What It Is

Capella EHR is described as an "integrated EHR + Practice Management" system designed for ambulatory/outpatient clinical settings. The certification page describes it as facilitating "data access, patient engagement and patient safety" with interoperability capabilities. It is certified as an ambulatory EHR under ONC's 2015 Edition Cures Update, version 6.1, certified January 31, 2022.

The product has broad ONC certification coverage — 40+ criteria spanning clinical data (a)(1)-(a)(5), (a)(12), (a)(14); transitions of care (b)(1)-(b)(3); patient portal/view-download-transmit (e)(1); public health reporting (f)(1), (f)(2), (f)(5); FHIR APIs (g)(7), (g)(10); and Direct messaging (h)(1). This breadth signals a full-featured ambulatory EHR rather than a niche or specialty module.

The SED (Safety Enhanced Design) intended user description identifies "Providers and Clinical Staff members of practices with various specialty including Internal Medicine, Family Medicine, etc." — indicating a multi-specialty ambulatory EHR.

It appears that Capella EHR is both a product sold to external practices and the EHR used internally by Akido Care's clinical network. The Akido Labs support site hosts Capella EHR documentation and release notes, confirming the tight integration between the two entities.

### Users & Market

**Internal use:** Capella EHR is used within Akido Care's own clinical network — 240+ providers, 100 clinics, 500,000+ patients. This is likely its primary deployment. ScopeAI integrates with the EHR and is described as "EHR integrated" in press coverage.

**External sales:** The certification page lists implementation costs (lab interfaces, e-prescription services, secure messaging), suggesting it is also offered to external practices. The MedicalRecords.com listing describes it as available software for practices. However, there is very little third-party review presence — no Capterra, G2, or Software Advice reviews were found, suggesting limited market penetration outside Akido's own network.

**Target users:** Ambulatory providers in Internal Medicine, Family Medicine, and other outpatient specialties. The support team includes "physicians, healthcare business analysts, IT professionals, certified coders, and billers," suggesting end users span clinical and administrative staff.

**Customer count:** Unclear how many external customers exist. The product's primary footprint appears to be Akido Care's own clinical operations.

### Modules & Functionality

Based on the certification page, vendor website, API documentation listing, and marketing materials:

**EHR / Clinical:**
- Patient record documentation with "easy-to-click" features for automated documentation
- Patient demographics and clinical data management
- CPOE (Computerized Provider Order Entry) — certified for (a)(1)-(a)(3)
- Clinical Decision Support — certified for (a)(9) implied by the broad criteria set
- Problem list, medication list, medication allergy list — certified (a)(1)-(a)(5)
- Drug interaction checking — certified (a)(4)
- Demographics recording — certified (a)(5)
- Clinical quality measures (10 eCQMs including CMS22v11, CMS68v12, etc.) — certified (c)(1)-(c)(3)
- Implantable device list — certified (a)(14)
- Family health history — certified (a)(12)
- Care plan generation (via ScopeAI integration in Akido Care deployments)

**Practice Management:**
- Appointment scheduling (described as "intuitive appointment scheduling" and "quick creation of patient appointments")
- Patient record storage and retrieval
- Revenue Cycle Management (RCM) — described as a module in the Capella suite
- HCC Coding support (per marketing materials)
- Claims and referral management (per Acurus Solutions service descriptions)
- The certification page mentions "PM (Practice Management)" as part of the Capella suite

**Interoperability & Data Exchange:**
- Transitions of care / C-CDA document exchange — certified (b)(1)-(b)(3)
- FHIR API (US Core) — certified (g)(7), (g)(10)
- Direct secure messaging — certified (h)(1)
- Integration capability with Epic, Cerner (per marketing materials — described as able to "integrate multiple EHRs into a common depository")
- API services for external application integration (documented in Capella Services API Documentation)
- Duplicate patient identification

**Patient Engagement:**
- Patient portal / View-Download-Transmit — certified (e)(1)
- Patient engagement tools — certified (e)(3)
- Secure messaging to patients

**Public Health Reporting:**
- Immunization registry reporting — certified (f)(1)
- Syndromic surveillance reporting — certified (f)(2)
- Cancer case reporting — certified (f)(5)

**E-Prescribing:**
- The certification page lists e-prescription services among implementation costs, and the certified criteria include (b)(3) for electronic prescribing, strongly suggesting e-prescribing is integrated. However, explicit mention of Surescripts integration was not found in available materials.

**Lab Integration:**
- The certification page lists "lab interface" among implementation costs, indicating lab ordering and results integration capability.

**Security & Access:**
- Role-based access control with "granular need-to-know access"
- AI-powered contextual access policies (per marketing materials)
- Audit logging — certified (d)(2)
- Automatic session timeout — certified (d)(5)
- Encryption — certified (d)(7)

### Data & Content

Based on the certified criteria and feature descriptions, Capella EHR stores and manages:

**Clinical data (confirmed by certification criteria):**
- Patient demographics (a)(5)
- Problem lists (a)(6) — implied by clinical data criteria
- Medication lists (a)(1)
- Medication allergy lists (a)(1)
- Clinical notes and visit documentation
- Lab orders and results (lab interface listed as implementation cost)
- Implantable device data (a)(14)
- Family health history (a)(12)
- Vital signs (implied by eCQMs like CMS22v11 for blood pressure screening)
- Smoking status (implied by Meaningful Use support)
- Care plans and clinical decision support outputs

**Practice management data (confirmed by product descriptions):**
- Appointment/scheduling data
- Billing and claims data (RCM module)
- HCC coding data
- Referral information
- Revenue cycle data

**Exchange and reporting data (confirmed by certification):**
- C-CDA documents (transitions of care)
- Immunization records (f)(1)
- Syndromic surveillance data (f)(2)
- Cancer case reports (f)(5)
- FHIR resources per US Core profiles
- Direct messages
- Patient portal messages and downloaded records

**AI-generated data (in Akido Care deployments):**
- ScopeAI-generated clinical reports including preliminary diagnoses and treatment plans
- Justification logs for AI recommendations
- AI-assisted documentation from voice-enabled encounters

**Notable gaps in available information:**
- The vendor website is extremely sparse — a near-empty landing page with just a phone number and an image. Almost all product information comes from the certification page, support site, and third-party descriptions.
- No user reviews were found on major review sites (G2, Capterra, Software Advice), making it difficult to understand real-world usage patterns.
- The exact boundaries between what Capella EHR stores vs. what ScopeAI stores separately are unclear.
- Whether the product includes a patient portal as a built-in module or relies on a separate component is not explicitly stated, though (e)(1) certification implies patient-facing data access exists.
- Whether billing/claims are fully integrated or handled by the separate Acurus RCM BPO service is ambiguous — the product is described as "EHR + Practice Management" which typically includes billing, and RCM is listed as part of the "Capella suite," but Acurus also offers RCM as a BPO service.
