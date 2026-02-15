# Healogics, Inc. — Product Research

Researched: 2026-02-15
Developer website: http://www.healogics.com/

## Overview

Healogics, Inc. is the nation's largest provider of advanced wound care services, headquartered in Jacksonville, Florida. Founded in 1996, the company operates over 600 hospital-based outpatient Wound Care Centers across the United States — roughly one-third of all hospital outpatient wound care centers in the country. Healogics treats more than 300,000 patients annually and has healed nearly 4 million wounds over its 30-year history. The company employs approximately 3,000 people and works with about 4,000 affiliated physicians plus a Healogics Specialty Physician practice group of nearly 300.

Healogics is not a traditional EHR vendor selling software to external customers. Rather, it is a wound care services company that built its own proprietary EHR (i-heal) for use within its own network of managed wound care centers. The company partners with hospitals to operate wound care centers within their facilities, and also partners with over 300 skilled nursing facilities and provides inpatient consults at more than 80 partner hospitals.

**Ownership history:** Healogics was acquired by Clayton, Dubilier & Rice (CD&R) from Metalmark Capital and Scale Venture Partners in 2014 in a transaction valued at $910 million. At the time, the company had approximately $300 million in revenue and 2,000 employees. In 2015, Healogics acquired Accelecare Wound Centers from Revelstoke Capital Partners, expanding its network. In 2021, the company announced a $240 million equity investment to support future growth. CD&R remains the current owner.

Healogics also maintains one of the world's largest wound-specific longitudinal outcomes databases, containing data on more than five million wounds, which it uses for research, evidence-based care protocols, and quality measurement through its Wound Science Initiative.

## Product: i-heal

CHPL ID: 10140

### What It Is

i-heal 2.0 is Healogics' proprietary, web-based electronic medical records (EMR) and disease management system designed specifically for wound care. It is not sold as a standalone product on the open market — it is used internally across Healogics' network of 600+ Wound Care Centers. The system integrates wound science into clinical workflows to support clinical decision making, simplify documentation, and reinforce the use of evidence-based medicine.

i-heal is one component of a broader software suite called **WoundSuite**, which comprises three applications:

1. **i-heal** — the core documentation management / EMR system, focused on clinical documentation, accurate claims, and maximum reimbursements
2. **Clinical Optimization** — automates clinical processes aligned with Healogics' Patient Care Process (a six-sigma lean productivity methodology), including strategic scheduling, productivity planning, pre-clinic huddles, intake/discharge assignments, staff communication, physician/case manager collaboration, an Interdisciplinary Care Management Guide (ICMG), and Medical Surveillance Review (MSR) process
3. **Healogics Photo+** — a mobile application for digital wound measurement, wound photography, and access to evidence-based data. Uses planimetric measurement to capture wound dimensions within seconds, supports pre- and post-debridement documentation, and uploads images to the cloud with HIPAA compliance

The certified module (i-heal 2.0) has a broad set of ONC certifications covering clinical data (CPOE, demographics, problem list, medication list, medication allergy list, clinical decision support, drug interaction checks, implantable device list), transitions of care (ToC send/receive, C-CDA creation/incorporation), patient portal (view/download/transmit), clinical quality measures (CQM reporting), public health reporting (direct project), and FHIR API access.

### Users & Market

i-heal is used by wound care physicians, clinicians, case managers, and front office support staff across the Healogics network. The SED intended user description is: "Ambulatory, Wound Care Physicians, Clinicians and Front Office Support Staff."

The system is deployed across 600+ Wound Care Centers nationwide, with more than 330,000 patients treated annually through the platform. It is used in every patient encounter across the Healogics network. The primary clinical settings are hospital-based outpatient wound care centers, though Healogics also has inpatient programs and partnerships with skilled nursing facilities.

Healogics is not competing in the general EHR market — i-heal is a captive, internal-use system. There are no external customer reviews on platforms like G2 or Capterra for i-heal specifically. The closest competitor product would be Net Health's WoundExpert, which is a commercially available wound care EHR.

Notably, Healogics has partnered with Net Health since 2012 and expanded the relationship in 2023 to integrate Net Health's Tissue Analytics (an AI-powered wound imaging platform) into Healogics' operations. This suggests that while i-heal handles core EMR/documentation, Healogics supplements it with third-party wound imaging and analytics technology.

### Modules & Functionality

Based on vendor materials, press releases, and the certified EHR technology page:

**Clinical Documentation & Wound Care:**
- Wound assessment documentation
- Wound photography and planimetric measurement (via Healogics Photo+)
- Pre- and post-debridement documentation
- Treatment plan creation and tracking
- Healing progress monitoring and outcome tracking
- Evidence-based clinical decision support
- Medical Surveillance Review (MSR) — a process to monitor patient healing progress
- Interdisciplinary Care Management Guide (ICMG)

**Prescribing:**
- Electronic prescribing (e-prescribing) integrated with Surescripts for transmitting prescriptions to pharmacies
- Drug-drug and drug-allergy interaction checks (certified for (a)(4))
- Medication list management (certified for (a)(1))
- Medication allergy list (certified for (a)(1))

**Clinical Data Management (per ONC certification criteria):**
- CPOE for medications, laboratory, and diagnostic imaging (certified for (a)(1))
- Patient demographics (certified for (a)(5))
- Problem list (certified for (a)(5))
- Medication list (certified for (a)(1))
- Medication allergy list (certified for (a)(1))
- Clinical decision support (certified for (a)(2))
- Implantable device list (certified for (a)(14))
- Family health history (certified for (a)(12))

**Care Coordination & Interoperability:**
- Transitions of Care — send and receive C-CDA documents (certified for (b)(1), (b)(2))
- Clinical information reconciliation — medications, allergies, problems (certified for (b)(3))
- Direct messaging for secure health information exchange (certified for (h)(1))
- FHIR API access for patient and population services (certified for (g)(7), (g)(9), (g)(10))
- Integration API for authentication, patient search, demographics, and common data sets

**Patient Portal:**
- Patient portal with view, download, and transmit capabilities (certified for (e)(1))
- Patient-generated health data support (certified for (e)(3))

**Quality & Compliance:**
- Clinical Quality Measure (CQM) reporting (certified for (c)(1), (c)(2), (c)(3))
- MIPS (Merit-based Incentive Payment System) certification capabilities
- Real-world testing attestation

**Billing & Claims:**
- Documentation manager for "accurate claims and maximum reimbursements" (described on WoundSuite page)
- E&M level CPT code documentation support
- Billing and coding tools with CMS guideline references
- Modifier reference and compliance
- Hard stops and warnings supporting appropriate documentation (mentioned in physician communication)

**Scheduling & Operations (via Clinical Optimization module):**
- Strategic scheduling
- Productivity planning
- Pre-clinic huddle workflows
- Intake and discharge assignments
- Staff communication tools
- Physician/case manager collaboration

**Analytics & Outcomes:**
- Wound healing outcomes tracking
- One of the largest wound care databases in the world (5M+ wounds)
- Research data services leveraging the longitudinal outcomes database
- Outcomes reporting and quality measurement

### Data & Content

Based on the evidence gathered:

**Directly evidenced data types:**
- Patient demographics (certified criterion, API documentation confirms patient search and demographics)
- Wound assessments and wound measurement data (core product function, Photo+ integration)
- Wound photographs and images (Photo+ cloud-based image upload with HIPAA compliance)
- Problem lists, medication lists, medication allergy lists (ONC-certified criteria)
- Prescription data (e-prescribing via Surescripts integration)
- Treatment plans and healing progress tracking (core wound care workflow)
- Clinical notes and documentation (EMR function)
- Implantable device lists (certified criterion (a)(14))
- Family health history (certified criterion (a)(12))
- Lab orders and results (CPOE certification for laboratory)
- Diagnostic imaging orders (CPOE certification for diagnostic imaging)
- C-CDA documents — both sent and received (transitions of care certification)
- Patient portal messages and patient-generated health data (e)(1) and (e)(3) certification)
- Clinical quality measure data (CQM reporting certification)
- Billing/claims documentation and E&M coding data (WoundSuite description, physician page)
- Scheduling and appointment data (Clinical Optimization module)
- Hyperbaric oxygen therapy session data (HBO is a core Healogics service)
- Vital signs (HBO technicians take vitals)
- Provider/staff communication data (Clinical Optimization)

**Inferred but not directly confirmed:**
- The website doesn't clearly distinguish what data lives in i-heal versus the Clinical Optimization module versus other systems. Since WoundSuite is described as "fully integrated," the data likely flows across these components.
- It is unclear whether i-heal stores full billing/claims data or just supports documentation for billing done through hospital systems. Given that Healogics operates within hospital facilities, claims may be submitted through the hospital's billing system rather than i-heal directly.
- The integration with hospital EMRs is mentioned but details about what data is exchanged (beyond C-CDA) are sparse.
- Nutrition, physical therapy, and other interdisciplinary care data is referenced in clinical workflows but it's unclear if this is documented in i-heal or in the host hospital's systems.

**Gaps in research:**
- The EHI export documentation PDF could not be read in detail (binary PDF). This would be the definitive source for what data i-heal actually exports.
- The Real World Testing documents were also unreadable as binary PDFs.
- No third-party reviews (G2, KLAS, Capterra) exist for this product since it's internal-use only.
- The Net Health partnership (Tissue Analytics integration since 2023) raises questions about whether wound imaging data now lives in Net Health's system rather than (or in addition to) i-heal.
