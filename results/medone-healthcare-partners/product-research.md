# MedOne Healthcare Partners — Product Research

Researched: 2026-02-14
Developer website: https://www.medonehp.com/

## Overview

MedOne Healthcare Partners (formerly Central Ohio Hospitalists) is a physician-owned hospital medicine practice founded in 2000 in Columbus, Ohio. It is **not a traditional health IT vendor** — it is a clinical practice that built its own EHR software to support its operations. The organization has grown to be the largest hospital medicine practice in central Ohio, with over 100 physicians, 75+ advanced practice clinicians, and 40+ administrative staff. They partner with 4 acute hospital systems, 4 long-term acute care hospital partners, and approximately 150 skilled nursing, assisted living, and independent living facilities across Ohio.

MedOne's founder, Dr. Joseph Mack, is both a physician and programmer. In 2012, he also founded a separate entity, **MedOne Systems, LLC** (based in Marietta, OH), which develops the **BOLT** clinical software platform — an EHR overlay/enhancement tool designed to augment existing enterprise EHRs. The certified product **OneConnect** appears to be a related but distinct tool from BOLT, specifically focused on post-acute care documentation and workflow. Both products share the same origin and development philosophy: clinician-built software designed for hospitalist and post-acute care workflows.

MedOne Healthcare Partners is a very small vendor from a health IT certification perspective. OneConnect appears to be primarily used internally by MedOne's own clinicians to document care across the post-acute facilities they serve — it is not marketed as a commercial EHR product for external customers. The company has approximately $3M in annual revenue (MedOne Systems) and no presence on standard EHR review platforms (G2, KLAS, Capterra).

## Product: OneConnect

CHPL IDs: 11426

### What It Is

OneConnect is a **custom clinical documentation tool** designed for post-acute care settings. According to MedOne's own description, it is "a custom documentation tool that enables providers to streamline workflows, communicate effectively and improve patient care and experience." Critically, it is **designed to integrate seamlessly with a post-acute facility's existing EMR** — meaning OneConnect is not a standalone full-featured EHR but rather a documentation overlay used by MedOne's physicians as they round across skilled nursing facilities, assisted living facilities, rehab hospitals, and long-term acute care hospitals.

The certified module (Version 0, certified 2023-12-27) covers a focused set of ONC criteria — 24 criteria in total, including CPOE for medications (a)(1), demographics (a)(5), implantable device list (a)(14), transitions of care (b)(1), EHI export (b)(10), clinical quality measures (c)(1), standardized FHIR APIs (g)(7)/(g)(9)/(g)(10), and Direct messaging (h)(1). It does NOT certify for many common EHR criteria such as medication lists (a)(6), allergy lists (a)(8), clinical decision support (a)(9), e-prescribing (a)(10)-(a)(11), or patient portal/view-download-transmit (e)(1).

The CHPL product number format indicates this is certified by Drummond Group (ONC-ACB code "04").

### Users & Market

OneConnect's intended users are **"Post acute, rehab and other ambulatory clinicians"** per its CHPL metadata. In practice, this means MedOne's own hospitalist physicians and advanced practice clinicians who provide medical services across approximately 150 post-acute facilities in Ohio.

This is an **internally-developed, internally-used tool**. There is no evidence that OneConnect is sold or licensed to external customers. It supports MedOne's care model of embedding physician teams in skilled nursing facilities, assisted living communities, long-term acute care hospitals, and inpatient rehabilitation hospitals.

Key deployment sites include OhioHealth Riverside Methodist Hospital, Genesis Hospital (Zanesville), Memorial Hospital (Marysville), Marietta Memorial Hospital, OhioHealth Rehabilitation Hospital, and Select Specialty Hospital (Columbus), plus approximately 150 post-acute facilities.

### Modules & Functionality

Based on the certification criteria and vendor disclosures, OneConnect provides:

**Clinical Documentation:**
- The core function — streamlining clinical documentation for providers rounding in post-acute facilities
- Clinical notes (fast to generate, with cloud-based voice recognition, templates, and shorthand options per BOLT/MedOne Systems descriptions)
- Multiple users can work on the same patient record simultaneously

**CPOE — Medications:**
- Certified for computerized provider order entry for medications, (a)(1)
- The BOLT platform (related product) claims physician order entry is "up to five times faster than other leading EHRs"

**Patient Demographics & Device Tracking:**
- Demographics management (a)(5)
- Implantable device list tracking (a)(14)

**Transitions of Care:**
- Certified for transitions of care (b)(1) — critical for a product used across post-acute settings
- Direct messaging support via EMR Direct Interoperability Engine 2017 (h)(1)

**Clinical Quality Measures:**
- Certified for CQM recording and export (c)(1)
- 68 clinical quality measures (version 12) certified

**FHIR APIs:**
- Standardized API for patient and population services (g)(7), (g)(9), (g)(10)

**Third-Party Integrations:**
- **RXNT** (Version 4.56) — used for e-prescribing services (separate fees apply)
- **EMR Direct Interoperability Engine 2017** (versions H.1 and B.1) — for Direct messaging / health information exchange
- **Medline Plus Connect NLM API** — for context-aware clinical knowledge retrieval
- **PCC (likely PointClickCare) integration** — monthly per-interface charges at facility level, confirming integration with post-acute facility EHRs

**Billing/Coding (from related BOLT platform):**
- CPT code capture for procedures and notes
- Automatic export to accounting systems for billing
- (Note: it is unclear whether these BOLT-specific features are in OneConnect or are separate)

**Clinical Safety (from related BOLT platform):**
- Automatic VTE risk assessment with treatment display
- Patient photos for safety identification
- Present-on-admission documentation reminders

### Data & Content

Based on the certified criteria, third-party dependencies, and vendor descriptions, OneConnect stores or manages:

1. **Clinical notes/documentation** — the primary data type; provider documentation of patient encounters across post-acute settings
2. **Patient demographics** — certified (a)(5)
3. **Medication orders** — certified CPOE for medications (a)(1); e-prescribing via RXNT
4. **Implantable device information** — certified (a)(14)
5. **Transitions of care documents** — CCDAs or similar documents for care transitions (b)(1)
6. **Clinical quality measure data** — 68 CQMs certified (c)(1)
7. **Audit logs** — required for (d) criteria certification
8. **User/access data** — multi-factor authentication, access controls, etc.

**What is NOT evident from the certification or vendor materials:**
- **No medication list management** — (a)(6) not certified
- **No allergy list management** — (a)(8) not certified
- **No clinical decision support** — (a)(9) not certified
- **No e-prescribing module** (uses third-party RXNT instead)
- **No patient portal** — (e)(1) not certified
- **No lab orders or results** — (a)(2), (a)(3) not certified
- **No vital signs management** — (a)(4) not certified
- **No problem list management** — (a)(7) not certified
- **No imaging** — (a)(12)-(a)(13) not certified
- **No public health reporting** — (f) criteria not certified (except indirectly through CQMs)

The product's narrow certification scope is consistent with it being a focused documentation and workflow tool rather than a comprehensive EHR. The vendor's website does not describe billing data management, scheduling, messaging, or other common EHR functions as part of OneConnect specifically — though the related BOLT product does mention billing/coding features.

**Important ambiguity:** The relationship between OneConnect (the certified product) and BOLT (the MedOne Systems product) is unclear. They may share code, data, or infrastructure. BOLT is described as an EHR overlay that enhances existing enterprise EHRs, while OneConnect is described as a documentation tool that integrates with facility EMRs. They could be the same product under different names, or genuinely separate tools serving different clinical settings (BOLT for acute hospital settings, OneConnect for post-acute settings).

---

## Related Product: BOLT (MedOne Systems)

While not the certified product under review, BOLT is worth noting because it shares the same developer/founder and may share architecture or data with OneConnect.

BOLT is described as "a brilliantly simple software solution that enhances your existing enterprise EHR, augmenting its clinical functionality." It is designed for hospitalist workflows in acute care settings and includes:
- Fast clinical documentation with voice recognition
- Intelligent team assignment and rounding list management
- CPOE (claimed 5x faster than leading EHRs)
- VTE risk assessment and clinical safety features
- Billing/CPT code capture with accounting system export
- Multi-user concurrent charting

MedOne Systems (~$3M revenue) develops and maintains BOLT. It is unclear whether BOLT and OneConnect share a common codebase or database.
