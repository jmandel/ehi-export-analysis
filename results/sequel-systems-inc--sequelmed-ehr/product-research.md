# Sequel Systems, Inc. — Product Research

Researched: 2026-02-14
Developer website: https://www.sequelmed.com

## Overview

Sequel Systems, Inc. is a privately held medical software company headquartered in Melville, NY, founded in 1995. They market themselves as having "20+ Years of Excellence in Healthcare Solutions." The company develops SequelMed, an integrated EHR and practice management platform targeting ambulatory physician practices, health organizations, hospitals, and billing companies. SequelMed can be sold as a combined EHR + PM suite or as standalone applications.

The company appears to be a small vendor — no employee count, customer count, or revenue figures are publicly available. Third-party review sites show only 7–9 user reviews total across platforms, suggesting a modest user base. Pricing starts at ~$148/month. The product is ONC-certified, Drummond-certified, HIPAA 5010-compliant, and SureScripts-certified. The product can be deployed on-premise or cloud-hosted.

SequelMed serves a broad range of ambulatory specialties (24+ per vendor claims) including cardiology, dermatology, gastroenterology, geriatrics, internal medicine, neurology, obstetrics, orthopedics, pediatrics, physical therapy, podiatry, psychiatry, urgent care, urology, gynecology, and chiropractic. There is no indication of inpatient/hospital-focused functionality despite the marketing mention of "hospitals" — the feature set and certified criteria are ambulatory-oriented.

No evidence of recent acquisitions, mergers, or rebranding. The company contact listed on CHPL is Tehmas Akhtar. The product has been through multiple versions — V8 is referenced on the EHR feature page, while V12 is the current ONC-certified version (certified December 2022).

## Product: SequelMed EHR (with integrated Practice Management)

CHPL ID: 11143

### What It Is

SequelMed EHR is described as "an all-in-one, fully integrated electronic health records solution" that combines clinical EHR, practice management, document management, and medical billing into a single platform. The certified module is the EHR, but the product as sold is the combined EHR + PM suite. The CHPL certification covers the EHR component (SequelMed EHR V12), but the product is marketed and used as an integrated clinical-administrative-financial system.

The certification is broad: clinical criteria (a)(1) through (a)(14) covering CPOE, demographics, problem lists, medication lists, clinical decision support, and implantable device lists; transitions of care (b)(1)-(b)(3); patient portal (e)(1); public health reporting (f)(1)-(f)(3) for immunizations, syndromic surveillance, and electronic case reporting; and FHIR APIs (g)(7)-(g)(10).

### Users & Market

The primary users are ambulatory physician practices across 24+ specialties. The product serves both small practices (starting price ~$148/mo suggests budget-friendly positioning) and multi-site groups (the PM module includes enterprise-wide roll-up reporting across multiple locations). One review described it as "a solid option for budget clinics."

End users include physicians (clinical documentation, e-prescribing, orders), clinical staff (charting, vitals, patient management), billing staff (claims, payments, A/R management), and patients (patient portal). The vendor also markets a separate billing company-facing PM product, suggesting third-party billing companies are also users.

No specific customer counts, notable deployments, or case studies were found. The low number of reviews across third-party sites (7-9 total) and the absence of press releases about customer wins suggest a small to very small market footprint.

### Modules & Functionality

Based on vendor website pages, disclosure statements, and third-party review sites, SequelMed includes the following modules and features:

**Clinical / EHR:**
- Patient problem lists, history & physical exams, vital signs (vendor EHR page)
- Allergies, immunizations, and medication records (vendor EHR page)
- Lab and pharmacy orders, diagnostic results and images (vendor EHR page)
- Customizable specialty-specific clinical templates for 24+ specialties (vendor physician practices page, user reviews)
- Clinical decision support with alerts (vendor EHR page)
- E-prescribing via SureScripts integration (vendor physician practices page, certifications)
- Voice recognition and transcription for clinical notes (EMRFinder, emrsystems.net)
- E&M coding — built-in evaluation & management coder (vendor physician practices page)

**Practice Management / Financial:**
- Billing, charges, payments — fully automated (vendor EHR page, PM page)
- Patient A/R, collections, and follow-up including denials management (vendor EHR page)
- Extensive claim scrubbing — electronic analysis of eligibility, authorization, and coding accuracy (vendor PM page)
- Automated batch processing for records maintenance and administrative reports (vendor PM page)
- Plan-specific edits and regulatory compliance (vendor PM page)
- Revenue cycle management (RCM) (EMRFinder, search results)
- Enterprise-wide roll-up reporting across multiple locations (vendor PM page)
- Scheduling (SoftwareFinder)

**Administrative / Document Management:**
- Admission, discharge, and transfer management (vendor EHR page — though this seems incongruent with an ambulatory-only product; may refer to ambulatory procedure tracking)
- Quality management and outcomes analysis (vendor EHR page)
- Automated and integrated document management with electronic archiving (vendor PM page)
- Paperless office operations (vendor physician practices page)
- Multi-office coordination for group practices (vendor physician practices page)

**Patient Engagement:**
- Patient portal with real-time communication (vendor physician practices page, EMRFinder)
- Online patient registration (EMRFinder)
- Active medication lists and immunization schedules via portal (EMRFinder)
- Direct messaging via Data Motion (HISP vendor) integration (disclosure statement)

**Interoperability:**
- HL7 interfaces for lab and system integration (EMRFinder, emrsystems.net)
- DICOM interfaces for imaging systems and medical devices (EMRFinder, emrsystems.net)
- Health Information Exchange (HIE) integration with labs, pharmacies, and referring physicians (vendor EHR page)
- SureScripts for e-prescribing (certifications)
- Integrations with Quest Diagnostics, Oracle, Microsoft, and InstaMed (SoftwareFinder)
- FHIR API access (certified criteria g(7)-(g)(10))
- Transitions of care / C-CDA exchange (certified criteria (b)(1)-(b)(3))

**Public Health Reporting:**
- Immunization registry submission (certified criteria (f)(1), disclosure mentions integration fee)
- Syndromic surveillance reporting (certified criteria (f)(2))
- Electronic case reporting (certified criteria (f)(3))

### Data & Content

Based on vendor materials and feature descriptions, SequelMed stores and manages:

- **Clinical data**: Patient demographics, problem lists, medication lists, allergy lists, immunization records, vital signs, history & physical exam notes, clinical encounter notes (via customizable templates), clinical decision support alerts
- **Orders and results**: Lab orders, pharmacy orders, diagnostic imaging orders, lab results, diagnostic results and images (DICOM integration suggests radiology/imaging data)
- **Medications**: Prescription records (e-prescribing via SureScripts), medication lists, medication history
- **Documents**: Clinical documents, scanned/archived documents (document management module), care coordination documents (C-CDA transitions of care)
- **Financial/billing data**: Claims, charges, payments, patient A/R, collections records, eligibility verification data, authorization records, denials, plan-specific billing edits
- **Scheduling data**: Appointment scheduling (mentioned on SoftwareFinder, physician practices page)
- **Patient portal data**: Patient messages, patient-submitted registration information, patient-accessible medication lists and immunization records
- **Public health data**: Immunization registry submissions, syndromic surveillance reports, electronic case reports
- **Administrative data**: ADT records (per vendor EHR page), quality management metrics, outcomes analysis data, enterprise reporting data across multiple locations

**Gaps and uncertainties:**
- The vendor website mentions "admission, discharge and transfer management" which is unusual for an ambulatory product — this may refer to ambulatory procedure workflows rather than inpatient ADT, or it may be aspirational marketing language. It's unclear whether SequelMed has actual hospital/inpatient capabilities.
- No mention of specific referral management beyond "streamlined referral processes" on the physician practices page — unclear what referral data is stored.
- Imaging: DICOM interface suggests image viewing/exchange but unclear whether the system stores images directly or just integrates with PACS.
- The patient portal runs through Data Motion (third-party vendor) per the disclosure statement, with monthly charges — this means some patient communication data may be stored in a third-party system.
- No mention of patient education materials, consent forms, or advance directives as distinct stored data types.
- InstaMed integration (SoftwareFinder) suggests payment processing, but unclear if credit card transaction data is stored in SequelMed or only in InstaMed.
