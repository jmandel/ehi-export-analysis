# Moyae, Inc. — Product Research

Researched: 2026-02-16
Developer website: https://moyae.com

## Overview

Moyae, Inc. is an early-stage startup that builds a cloud-based, AI-powered Electronic Health Record (EHR) system purpose-built for ophthalmology and optometry practices. The company was founded by Sami Mirimiri (Co-Founder & CEO, formerly director of engineering at EnterMedicare and software engineer at Capital One) and is based in Los Angeles, California. Moyae participated in the Techstars Seattle 2023 accelerator cohort (15th cohort), placing it firmly in the startup/early-stage category.

The company positions itself as "the modern operating system for vision-care" and emphasizes that it was built from the ground up alongside ophthalmologists and optometrists, rather than being adapted from a general-purpose EHR. It is advised by a medical advisory board of six ophthalmologists from institutions including Bascom Palmer Eye Institute, Baylor College of Medicine, Harvard Medical School (Mass Eye and Ear), Stanford, and UT Southwestern. The product is AWS-hosted and ONC-certified (certified August 2023).

Moyae appears to be a very small vendor — there is no public information about customer counts, revenue, or number of deployments. No user reviews were found on Capterra, G2, or other third-party review sites, suggesting the product is still in early market adoption. The vendor's presence in the market is limited to its own website, a LinkedIn page, a Techstars listing, and one significant partnership announcement with AdvancedMD.

## Product: Moyae

CHPL IDs: 11331

### What It Is

Moyae is a cloud-based EMR/EHR designed exclusively for ophthalmology and optometry practices. It is certified as a single product (version 1, certified 2023-08-16). The certified module appears to be the primary product itself — there is no indication that it is a component of a larger platform.

The product's ONC certification covers a focused set of criteria: demographics (a)(5), CPOE for diagnostic imaging (a)(3), implantable device list (a)(14), transitions of care (b)(1), EHI export (b)(10), bulk FHIR (b)(11), FHIR API access (g)(7)-(g)(10), and security/privacy criteria (d). Notably absent from certification are: CPOE for medications (a)(1) and labs (a)(2), clinical decision support (a)(9), drug interaction checking (a)(4), allergy checking, problem list, medication list, patient portal/VDT (e)(1), and all public health reporting criteria (f). This is a relatively narrow certification footprint compared to full-featured EHRs.

### Users & Market

**Target users**: Ophthalmologists, optometrists, and their clinical staff (technicians, front-desk staff, administrators, billers). The CHPL metadata explicitly states the intended users are "medical professionals with knowledge of eyecare."

**Market position**: Moyae is a very early-stage startup (Techstars 2023 cohort). No customer counts, deployment numbers, or case studies are publicly available. The absence of any third-party reviews on Capterra, G2, or similar sites suggests minimal market penetration as of early 2026.

**Clinical settings**: Ambulatory ophthalmology and optometry practices. No evidence of hospital, ASC (ambulatory surgery center), or institutional deployments.

**Go-to-market**: Appears to be direct sales with a partnership strategy. The AdvancedMD integration partnership (announced ~2024) is significant — it positions Moyae as the clinical/EHR layer that pairs with AdvancedMD's established practice management and billing platform.

### Modules & Functionality

Based on vendor website, press releases, and blog posts, Moyae's functionality includes:

**Clinical Documentation & Charting**
- Customizable templates for ophthalmology/optometry encounters
- Optimized workflows for recording objective data (e.g., visual acuity, refraction)
- Anterior and posterior segment findings documentation
- Retina drawings — visual documentation tools for retinal findings
- Care plan notes with template-to-code linkage
- "CachedNotes" feature described as reducing encounter closure time
- AI-suggested diagnostic coding to accelerate documentation

**Ophthalmology-Specific Clinical Features**
- Intraocular pressure (IOP) tracking and monitoring over time
- Intravitreal injection documentation with injection series historical data (highlighted in a June 2024 blog post as a key differentiator)
- Implantable device list tracking (per (a)(14) certification)
- CPOE for diagnostic imaging orders (per (a)(3) certification)

**E-Prescribing (eRx)**
- Embedded electronic prescribing within the EHR
- Access to patient prescription history
- Listed as an add-on with additional monthly fee (per disclosures page)
- Despite e-prescribing being a product feature, the product is NOT certified for CPOE for medications (a)(1), which is notable

**Quality Reporting & Registry**
- IRIS Registry integration (Intelligent Research in Sight), recognized by the American Academy of Ophthalmology
- MIPS compliance support (highlighted in a March 2025 blog post about maximizing MIPS success)

**Interoperability**
- Transitions of care / C-CDA support (per (b)(1) certification)
- FHIR R4 API access (per (g)(7)-(g)(10) certification)
- Bulk FHIR export (per (b)(11) certification)
- EHI export via newline-delimited JSON export of FHIR data (per (b)(10) and disclosures page)
- Direct messaging capability (add-on with additional monthly fee)

**Patient Engagement**
- Patient review request functionality (built into the platform, lets practices request patient reviews without leaving the EHR)
- No patient portal certification — (e)(1) VDT is not part of their certified criteria

**Practice Operations (via AdvancedMD Integration)**
- Moyae integrates with AdvancedMD for billing, scheduling, and patient engagement
- The integration is described as "bi-directional" with:
  - Automatic updates to patient histories within AdvancedMD
  - Encounter documentation synchronized between platforms
  - Claims transmission directly to AdvancedMD's billing ledger
- This partnership suggests Moyae deliberately chose NOT to build its own full practice management/billing system

**What Moyae Describes Itself as Handling (from marketing)**
- Revenue cycle management
- Billing (though this may primarily refer to the AdvancedMD integration)
- Appointment scheduling (unclear if native or via AdvancedMD)
- Patient records

**Features Listed as "Coming Soon"**
- Eligibility checking (noted on the updates page)

### Data & Content

Based on the evidence gathered, Moyae stores or manages the following data:

**Clinical data (strong evidence)**:
- Patient demographics (certified (a)(5))
- Ophthalmic examination data: IOP measurements, visual acuity, refraction data, anterior/posterior segment findings
- Retina drawings/visual documentation
- Intravitreal injection records with series history
- Implantable device records (certified (a)(14))
- Diagnostic imaging orders (certified (a)(3))
- Care plans and encounter notes
- Diagnostic codes (ICD, with AI-suggested coding)

**Prescription data (strong evidence)**:
- e-Prescribing data and prescription history (embedded eRx feature)

**Interoperability data (strong evidence)**:
- C-CDA documents for transitions of care
- FHIR resources (the EHI export is described as "newline-delimited JSON export of FHIR data")

**Quality/registry data (moderate evidence)**:
- IRIS Registry / MIPS reporting data (quality measures for ophthalmology)

**Administrative/scheduling data (unclear)**:
- The vendor's marketing mentions handling "appointment scheduling" and "revenue cycle management," but the AdvancedMD partnership suggests billing and scheduling may primarily reside in AdvancedMD rather than natively in Moyae. It is unclear how much administrative and financial data Moyae stores natively vs. what lives in AdvancedMD.

**What's NOT mentioned or appears absent**:
- Lab results or lab ordering (no (a)(2) certification, no mention of lab workflows)
- Patient portal / patient-facing messaging (no (e)(1) certification)
- Imaging storage (PACS) — the product orders imaging but there's no evidence it stores images
- Structured allergy lists, medication lists, or problem lists are not explicitly called out in marketing (though they likely exist as standard EHR features; the absence of (a)(1), (a)(6)-(a)(8) certifications is notable)
- Public health reporting data (no (f) criteria)
- Clinical decision support rules (no (a)(9) certification)

**Authentication**:
- Multi-factor authentication required
- Remote identity proofing via ID.me

---

## Summary Assessment

Moyae is a very early-stage, specialty-focused EHR for ophthalmology/optometry. It has a narrow but relevant ONC certification footprint. The product focuses on clinical documentation for eye care (charting, IOP tracking, intravitreal injections, retina drawings, e-prescribing) and relies on AdvancedMD for practice management, billing, and scheduling. The company is small (Techstars-backed startup), has no visible market traction in terms of reviews or customer counts, and the product appears to be in early adoption. For EHI export assessment, the key question will be whether the export covers all clinical data the product stores natively — particularly the ophthalmology-specific data (IOP series, injection histories, retina drawings) that wouldn't be covered by standard FHIR resources.
