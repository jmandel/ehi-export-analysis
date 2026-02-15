# Sai Systems Digital LLC — Product Research

Researched: 2026-02-14
Developer website: https://thesnfist.com/

## Overview

Sai Systems Digital LLC operates under the brand "Saisystems Health," a division of Saisystems International, Inc. — a broader IT consulting and technology company headquartered in Shelton, Connecticut, established in 1987. Saisystems International has two main divisions: Saisystems Health (post-acute healthcare) and Saisystems Technology (IT consulting, AI automation, custom app development). The parent company is a Microsoft Azure Solutions Partner and donates 25% of annual profit to charitable causes. The company has been recognized as a Hartford Business Journal Best Place to Work from 2018–2025.

Saisystems Health focuses exclusively on Post-Acute Long-Term Care (PALTC) providers — physicians, nurse practitioners, and other clinicians who provide bedside care in skilled nursing facilities (SNFs), assisted living facilities, rehabilitation centers, and home health settings. The company has over 35 years of experience in the LTPAC industry, though the original business was medical billing and credentialing; PacEHR, their EHR product, was launched in 2021. The company reports providing services in 39 states. Their go-to-market is a "TheSNFist® Suite" — a bundled platform combining their EHR with revenue cycle management and practice support services.

This is a small, niche vendor. The PALTC practitioner market is small — as the company notes, these practitioners comprise less than 5% of U.S. medical professionals. In the SNF EHR market more broadly, PointClickCare dominates (~70-80% market share) and MatrixCare holds much of the rest. PacEHR targets the practitioners who work *in* SNFs, not the SNFs themselves — a narrower niche of mobile clinicians who visit multiple facilities. No customer count is published; the product has only 4 reviews on SoftwareFinder (4.8/5 stars) and no reviews on FindEMR, suggesting a small user base.

## Product: PacEHR

CHPL IDs: 11177

### What It Is

PacEHR (version v20) is a cloud-based electronic health record system designed specifically for post-acute long-term care (PALTC) practitioners. It was launched in March 2021 and is described as "the first EHR designed for post-acute long-term care professionals." The product targets clinicians who provide bedside services in skilled nursing facilities, long-term care facilities, assisted living communities, rehabilitation centers, and home health agencies.

The certified module (PacEHR) is part of a larger ecosystem called the "TheSNFist® Suite," which bundles the EHR with additional products and managed services:
- **PacEHR®** — the EHR itself (the certified product)
- **billEHR®** — a mobile point-of-care charge capture app
- **SNFConnect** — a communication system for practice coordination
- **navigatEHR** — business intelligence dashboards
- Revenue Cycle Management (RCM) managed services
- Medical Coding and Billing services
- Payor Enrollment and Credentialing services
- Chronic Care Management (CCM) services

It's important to note that PacEHR targets *practitioners* (physicians, NPs, APRNs) who visit SNFs, not the SNF facilities themselves. The SNF facility typically has its own EHR (usually PointClickCare). PacEHR is for the visiting clinician's documentation and billing workflow. The product integrates with PointClickCare, suggesting it pulls patient data from the facility EHR.

### Users & Market

**Primary users**: Physicians, nurse practitioners (APRNs), and other clinicians who provide medical services in post-acute and long-term care settings. These are often mobile practitioners who visit multiple facilities.

**Clinical settings**: Skilled nursing facilities, assisted living communities, rehabilitation centers, long-term care facilities, home health agencies. The product supports data sharing across multiple PALTC facilities from a unified documentation platform.

**Practice size**: Small to medium practices. The pricing tiers reference "Small, Medium, Large Organization" but no specific prices are published — custom quotes are required.

**Geographic reach**: Saisystems Health reports services in 39 states.

**Customer base size**: Unclear. The very small number of third-party reviews (4 total on SoftwareFinder, zero on FindEMR) suggests a small installed base. User reviews include at least one APRN and one Nurse Practitioner.

**Notable**: A user review on SoftwareFinder praised it as "Pacer for LTC" — all 4 reviews were positive (4-5 stars).

### Modules & Functionality

Based on vendor materials, third-party review sites, and the CHPL certification criteria, PacEHR includes the following functionality:

**Clinical Documentation**
- Template-driven encounter documentation with customizable macros (vendor website)
- Voice-to-text / speech recognition for rapid note creation (FindEMR, SoftwareFinder)
- Pre-populated past patient data — auto-fills unchanged information from previous encounters (FindEMR)
- Simultaneous multi-patient record access for workflow efficiency (SoftwareFinder)
- Patient census sorting by facility for practitioners visiting multiple sites (thesnfist.com)
- Simplified patient navigation between encounters and between different patient records (vendor materials)

**Clinical Decision Support & Quality**
- Certified for (a)(1) CPOE for medications, (a)(5) demographics, (a)(14) implantable device list
- Certified for (c)(1) clinical quality measures — MIPS/CCM reporting and documentation built-in (vendor website)
- AI-powered coding suggestions based on patient's place of service (press release, vendor website)

**E-Prescribing**
- Electronic prescriptions sent directly to pharmacies (search results mention e-prescribing as a feature)
- Certified for (a)(1) CPOE for medications

**Transitions of Care**
- Certified for (b)(1) transitions of care — C-CDA document exchange
- Certified for (h)(1) direct project — secure health information exchange via Direct messaging

**Patient Portal**
- Listed on FindEMR as a feature — patient access to health records, appointment scheduling, and secure messaging with providers
- Note: Not certified for (e)(1) view-download-transmit, so the patient portal functionality may be limited or handled externally

**Billing & Coding**
- Coding recommendation assistance based on place of service (press release)
- Point of Care Charge Capture via billEHR® mobile app (separate from PacEHR but part of the suite)
- Built-in encounter billing integration (thesnfist.com mentions "integrated billing for encounters")
- Claims management listed as a feature on FindEMR

**Scheduling**
- Appointment scheduling listed as a feature on FindEMR

**Document Management**
- Document management listed as a feature on FindEMR

**Compliance & Reporting**
- Compliance tracking (FindEMR)
- Automated quality reporting for MIPS and CCM programs (FindEMR)
- Business intelligence dashboards via navigatEHR (part of the suite)

**API Access**
- Certified for (g)(7)–(g)(10) including FHIR API access — Standardized API for patient and population services
- Certified for (b)(11) bulk FHIR export

**Integrations**
- Integration with PointClickCare (the dominant SNF facility EHR) mentioned on the PALTC practice support page
- Mobile device support

### Data & Content

Based on the certified criteria and described functionality, PacEHR manages:

**Clinical data** (evidenced by certification criteria and product descriptions):
- Patient demographics (a)(5)
- Clinical encounter notes and documentation (core product function — this is the primary use case)
- Medication orders / CPOE (a)(1) — and e-prescribing
- Implantable device list (a)(14)
- Clinical quality measure data (c)(1)
- Transitions of care documents — C-CDA (b)(1)

**Billing/coding data** (evidenced by vendor descriptions):
- Encounter-level billing codes and charge capture (integrated billing, billEHR app)
- Coding suggestions and recommendations
- Claims data (listed on FindEMR)

**Administrative data** (evidenced by feature listings):
- Appointment scheduling data
- Document management
- Patient census/facility assignments

**Communication data** (evidenced by product ecosystem):
- Direct messaging for transitions of care (h)(1) certification
- SNFConnect communication system (part of suite)
- Patient portal messaging (described on FindEMR, though extent is unclear)

**What's less clear**:
- **Lab orders/results**: One user review on a search result noted the "inability to directly add lab values" as a drawback. The product is not certified for (a)(2) CPOE for lab orders or (a)(3) CPOE for diagnostic imaging. This suggests lab data management may be limited or absent.
- **Imaging/radiology**: No certification criteria for imaging orders. No mention of imaging in vendor materials.
- **Allergy lists, problem lists, medication lists**: The product is not explicitly certified for (a)(6) problem list, (a)(7) medication list, or (a)(8) allergy list — though these may still be tracked as part of clinical documentation without specific CCDS certification.
- **Vitals**: Not certified for (a)(4) vital signs. Given the PALTC use case where practitioners visit facilities that have their own EHR tracking vitals, PacEHR may rely on the facility system for vitals.
- **Patient education, care plans**: Not mentioned in available materials.
- **Revenue cycle detail**: The RCM services (claims processing, denial management, payment posting) are managed services offered alongside PacEHR but may use separate systems. The boundary between data in PacEHR vs. data in the RCM service workflow is unclear.

**Key architectural note**: PacEHR is designed for mobile practitioners visiting SNFs that run their own EHR (typically PointClickCare). This means PacEHR likely stores the practitioner's encounter documentation and billing for visits, while the facility EHR holds the comprehensive patient record (nursing notes, vitals, medication administration, etc.). PacEHR integrates with PointClickCare to pull relevant patient context but is not the primary system of record for the facility. This has implications for EHI export completeness — the EHI export from PacEHR would be expected to contain the practitioner's documentation and billing data, not the facility's full patient record.
