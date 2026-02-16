# Practice Alternatives, Inc. — Product Research

Researched: 2026-02-16
Developer website: http://practice-alt.com

## Overview

Practice Alternatives, Inc. (PAI) is a small, privately held healthcare IT company founded in 1982 and headquartered in Tinton Falls, NJ. The company has 11–50 employees (21 on LinkedIn) and serves over 500 physicians across more than 70 specialties, in settings ranging from solo practices to hospital systems. Their management team claims over 80 years of combined healthcare experience in hospital and private practice settings.

PAI positions itself as a "one-stop" solution for medical practices, offering a bundled suite of medical billing services, practice management software (Rexpert), electronic health records (AuroraEHR), medical transcription, and practice development consulting. Their primary geographic focus is New Jersey, New York, and Pennsylvania, though the about page claims national reach. The company operates as a partnership and appears to function as both a software vendor and a managed billing services provider — they bundle free practice management software with their billing services. This is a very small, regional vendor serving ambulatory practices.

## Product: AuroraEHR

CHPL IDs: 11128

### What It Is

AuroraEHR is an ambulatory electronic health record system designed for office-based physicians and nurses. It is certified under ONC 2015 Edition (certification date 2022-12-27) with a broad set of criteria covering clinical documentation (CPOE for medications, labs, and imaging), clinical quality measures, transitions of care, patient portal, FHIR APIs, and immunization registry reporting. The CHPL metadata identifies the intended users as "Ambulatory doctors & nurses."

AuroraEHR is part of a larger integrated product suite. It is designed to work alongside Rexpert, PAI's practice management and billing software. The vendor describes AuroraEHR as "fully integrated" with Rexpert, meaning the EHR and practice management/billing systems are distinct but tightly coupled products from the same vendor. The certified module (AuroraEHR) is the clinical EHR component; the full product experience for a PAI customer includes Rexpert for scheduling, billing, and practice management.

### Users & Market

AuroraEHR serves ambulatory medical practices — the vendor mentions solo practitioners through hospital-affiliated practices. With over 500 doctors across 70+ specialties, PAI is a small vendor by any measure. The website specifically markets to practices in NJ, NY, and PA. The 40+ specialties mentioned in the billing services page range from cardiology to thoracic surgery, suggesting a general-purpose ambulatory system rather than a specialty-specific one.

No third-party reviews were found on G2, Capterra, or KLAS for AuroraEHR specifically. The product does not appear in major EHR comparison sites, consistent with its small market footprint. A SoftwareFinder page for Aurora EHR existed but returned a 410 (gone) error, suggesting it may have been delisted.

### Modules & Functionality

Based on the vendor website, AuroraEHR includes the following capabilities:

**Clinical Documentation:**
- Point-and-click templates for clinical notes
- "Traditional chart flow" documentation approach
- Customizable templates for specialty-specific workflows
- A physician testimonial notes it "greatly simplified History and Physicals, as well as progress notes, and nursing orders"

**Computerized Provider Order Entry (CPOE):**
- Certified for CPOE for medications, laboratory, and diagnostic imaging orders — criteria (a)(1), (a)(2), (a)(3)
- Drug interaction checking

**Coding & Diagnosis:**
- CPT and ICD-10 code input (mentioned in the iPad app context)
- Integration with Rexpert for billing code flow

**Mobile Access:**
- iPad application for bedside/exam room use
- Supports vitals capture, photo capture, consent signing on mobile

**Document Management:**
- Supports multiple file types: PDF, JPG, Word, TIF, GIF, BMP
- Image management within patient records

**Interoperability & Care Coordination:**
- Electronic receipt and sharing of health information
- Supports orders, results, referrals, consults, medical histories, and care summaries
- Can share patient clinical information with hospitals, next providers of care, and health information exchanges
- Certified for transitions of care (b)(1), (b)(2)

**Patient Portal:**
- Secure, HIPAA-compliant online portal
- Patients can access medical records, receive visit summaries and results, communicate with providers
- The mandatory disclosures page notes a "monthly patient portal fee" as a separate cost item
- Certified for (e)(1) — view, download, transmit (implied by the presence of g(10) FHIR API and patient portal references, though (e)(1) is not explicitly in the criteria list)

**Clinical Quality Measures:**
- Certified for CQM recording, calculation, and reporting — criteria (c)(1), (c)(2), (c)(3)
- Supports 9 specific clinical quality measures including hypertension management, diabetes tracking, and preventive care screening

**Public Health Reporting:**
- Certified for immunization registry transmission — criterion (h)(1)

**FHIR API Access:**
- Certified for (g)(7)–(g)(10) standardized API criteria
- API documentation and terms of use referenced on the disclosures page

**Patient Education:**
- Care plans and patient education materials mentioned on the features page

### Data & Content

Based on the certified criteria and vendor-described features, AuroraEHR stores and manages:

- **Clinical notes** (H&P, progress notes, nursing orders — per physician testimonial)
- **Patient demographics** (implied by (a)(5) demographics criteria and standard EHR function)
- **Medication data** (CPOE for medications, drug interaction checking)
- **Laboratory orders and results** (CPOE for labs, interoperability for results receipt)
- **Diagnostic imaging orders** (CPOE for imaging)
- **Vital signs** (captured via iPad app and standard charting)
- **Documents and images** (multi-format document management: PDF, JPG, Word, TIF, GIF, BMP)
- **Photos** (captured via iPad app)
- **Patient consent records** (electronic consent signing)
- **Care coordination data** (referrals, consults, care summaries sent/received)
- **Clinical quality measure data** (CQM calculations for 9 measures)
- **Immunization records** (immunization registry reporting)
- **Patient portal communications** (secure messaging between patients and providers)
- **CPT and ICD-10 codes** (mentioned in mobile app context; flows to Rexpert for billing)

**What's less clear:**
- **E-prescribing**: The website does not explicitly mention e-prescribing or Surescripts integration, though CPOE for medications is certified. It's unclear if prescriptions are sent electronically or just ordered within the system.
- **Allergies and problem lists**: Not explicitly described on the vendor website, but (a)(5) certification and standard EHR function implies these are present. The certification for (a)(4) (drug-drug, drug-allergy interaction checks) confirms allergy data is stored.
- **Scheduling data**: Scheduling is handled by Rexpert, not AuroraEHR. Whether the EHR has its own appointment/scheduling data or pulls it from Rexpert is unclear.
- **Billing/claims data**: Billing is handled by Rexpert and PAI's managed billing services. The EHR captures CPT/ICD-10 codes but billing claims and financial data appear to reside in Rexpert.

---

## Product: Rexpert (Practice Management)

*Not separately certified on CHPL, but relevant as AuroraEHR's companion product.*

Rexpert is PAI's practice management software, described as "The Reimbursement Expert." It handles the business/administrative side of medical practices and integrates with AuroraEHR. Key capabilities include:

- **Scheduling**: Advanced appointment scheduler with capacity management
- **Medical billing**: Claims processing, coding support, ICD-10 compliance
- **Eligibility verification**: Automatic batch or ad-hoc insurance eligibility checks
- **Patient recalls**: Automated recall/follow-up processing for appointments and procedures
- **Reporting**: Over 300 customizable financial and operational reports
- **Radiology Information System (RIS)**: Can function as an RIS for compatible practices
- **Data backup and storage**: Automated backup and secure storage

Rexpert is bundled free with PAI's medical billing services. The fact that it includes 300+ reports and RIS functionality suggests it stores significant financial, scheduling, and operational data. Since AuroraEHR is "fully integrated" with Rexpert, the boundary between what data lives in the EHR vs. the practice management system is important for evaluating EHI export completeness.

---

## Research Gaps

- **No third-party reviews found.** AuroraEHR does not appear on G2, Capterra, KLAS, or other major review platforms, limiting insight into real-world usage and data.
- **The vendor website is basic.** Marketing materials are thin — the product pages are brief and lack detailed feature documentation or screenshots.
- **E-prescribing status unclear.** CPOE for medications is certified but explicit e-prescribing functionality is not described.
- **Data architecture unclear.** It's not clear whether AuroraEHR and Rexpert share a database or are separate systems with an integration layer. This matters for understanding what the (b)(10) EHI export would cover.
- **Cloud vs. on-premise unclear.** The website mentions "24/7/365" access via internet connection, suggesting cloud-hosted or web-based, but this isn't explicitly stated.
- **Customer count ambiguity.** "Over 500 doctors" is mentioned multiple times but it's unclear how many are AuroraEHR users vs. billing-services-only or Rexpert-only customers.
