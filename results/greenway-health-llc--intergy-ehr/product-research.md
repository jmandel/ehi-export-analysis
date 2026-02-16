# Greenway Health, LLC — Product Research

Researched: 2026-02-16
Developer website: https://www.greenwayhealth.com/

## Overview

Greenway Health, LLC is a privately held health IT vendor headquartered in Tampa, Florida, with offices in Carrollton, Georgia and Bangalore, India. The company has approximately 1,000 employees and serves over 10,000 healthcare organizations with 55,000+ providers across 40+ medical specialties. It is owned by Vista Equity Partners.

Greenway Health's history is complex, involving multiple acquisitions and rebrands. The lineage traces back to Medical Manager, founded in 1977. Sage Group acquired the healthcare software division from Emdeon for $565 million in 2006 and operated it as Sage Software Healthcare, Inc. In November 2011, Vista Equity Partners acquired it for $320 million and renamed it Vitera Healthcare Solutions. In June 2013, Vitera acquired SuccessEHS, Inc. (a Birmingham-based EHR company). Separately, Greenway Medical Technologies, founded in 1999, had developed an EHR product called PrimeSUITE and went public in February 2012. In late 2013, Vista Equity Partners acquired Greenway Medical Technologies for approximately $644 million ($20.35/share) and combined it with Vitera and SuccessEHS under the new brand "Greenway Health, LLC." This merger brought together three distinct EHR product lines: Intergy (from the Vitera/Sage lineage), PrimeSuite (from Greenway Medical Technologies), and SuccessEHS.

Today Greenway Health markets two primary EHR platforms — Intergy and Prime Suite — along with a suite of shared services including revenue cycle management, patient engagement, analytics, and cloud infrastructure. The company focuses exclusively on ambulatory healthcare practices, from solo providers to large multi-specialty groups, with particular strength in primary care, OB-GYN, orthopedics, pediatrics, FQHCs, and tribal health organizations.

## Product: Intergy EHR

CHPL IDs: 11351 (v21, certified 2023-10-03), 11682 (v22, certified 2025-08-14)

### What It Is

Intergy is a cloud-based (AWS-hosted) integrated Electronic Health Record (EHR) and Practice Management (PM) platform designed for ambulatory healthcare practices of all sizes. It is one of Greenway Health's two flagship EHR products — Intergy comes from the Vitera/Sage/Medical Manager product lineage and is architecturally distinct from PrimeSuite, which came from the original Greenway Medical Technologies acquisition.

The certified module covers the full Intergy platform — both EHR and practice management capabilities are part of the same product. The CHPL metadata lists the SED intended users as "Healthcare providers in an outpatient ambulatory setting."

Both v21 and v22 are certified across a broad range of ONC criteria: clinical data management ((a)(1)-(a)(5), (a)(12), (a)(14)-(a)(15)), care transitions ((b)(1)-(b)(3)), EHI export ((b)(10)), care plan updates ((b)(9) in v21, (b)(11) in both), patient request for electronic access ((e)(3)), public health reporting ((f)(1)), FHIR API access ((g)(7), (g)(9), (g)(10)), and direct messaging ((h)(1)). This is a full-featured ambulatory EHR with integrated practice management.

### Users & Market

Greenway Health serves 10,000+ organizations and 55,000+ providers. Intergy is one of the two main platforms (alongside Prime Suite) supporting this customer base. Specific Intergy customer breakdowns are not publicly disclosed separately.

**Primary users**: Physicians, clinical staff, billing specialists, practice administrators, and front-desk/scheduling staff in ambulatory settings.

**Settings**: Solo practices, small-to-medium group practices, multi-specialty organizations, FQHCs, and tribal health organizations. The product is positioned for ambulatory care broadly rather than a narrow specialty niche.

**Notable mentions**: HealthLinc (FQHC) and New Era Medicine are cited as customers in Greenway testimonials. Greenway won KLAS "Most Improved Physician Practice Product" in 2022 for Intergy PM, and was named a top 3 patient portal by KLAS.

**Deployment**: Primarily cloud-based (hosted on AWS), though some sources mention on-premises deployment as an option. Mobile access supported on iPhone, iPad, and Android devices.

### Modules & Functionality

Based on vendor materials, product pages, brochures, and third-party review sites, Intergy includes the following integrated modules and capabilities:

**Clinical / EHR:**
- Clinical charting and encounter documentation with 500+ customizable templates and forms
- Specialty-specific template library (configurable to different specialties)
- Electronic prescribing (e-Rx) including Electronic Prescribing of Controlled Substances (EPCS)
- In-workflow Prescription Drug Monitoring Program (PDMP) checking
- Real-time prescription benefit information
- Health reminders — upcoming, due, and overdue care gaps displayed per patient
- Clinical alerts
- Lab ordering and results integration (Greenway Lab Interface integrates with Intergy for ordering lab tests and receiving results)
- Imaging ordering
- Clinical decision support
- Greenway Clinical Assist — AI-powered clinical documentation tool
- Greenway Document Manager — digital document workflows (scanning, indexing, storing documents)
- Patient photo ID and insurance card imaging
- USPS Web Tools integration for accurate patient address recording
- CommonWell Health Alliance integration for health data exchange across organizations

**Practice Management / Administrative:**
- Patient scheduling and appointment management across multiple locations
- Rules-based scheduling to optimize patient attendance
- Patient check-in workflows
- Resource management across sites
- Insurance eligibility verification at check-in (automated eligibility verification)
- Multi-location support with centralized scheduling

**Billing / Revenue Cycle:**
- Comprehensive billing and claims management
- Claim scrubbing (checking insurance claims before submission)
- Charge posting
- Accounts receivable tracking
- Financial reporting
- Integration with Greenway Revenue Services (clearinghouse services) — clearinghouse for claim submission, payment posting, and denial management
- Medical coding support
- Greenway Health Pay (integrated payment processing)

**Patient Engagement:**
- Greenway Patient Portal — patients can view medical records, lab results, medications; send secure messages to providers; schedule appointments; request prescription refills; pay bills online; access health history forms. Portal is SMART-on-FHIR powered and VDT (View-Download-Transmit) compliant. Supports health advocate access (one account for multiple practices).
- Greenway Patient Connect — online appointment scheduling and patient self-service
- Multi-channel customizable patient reminders and notifications
- Patient messaging (appointment reminders, procedure instructions)
- Secure messaging between patients and providers

**Telehealth:**
- Greenway Telehealth — HIPAA-compliant, device-agnostic telehealth integrated with the EHR. Providers can launch telehealth visits and manage visit workflows directly within Intergy.

**Care Coordination:**
- Chronic Care Management (CCM) — integrated solution with dedicated health coaching teams to manage patients with chronic conditions
- Remote Patient Monitoring (RPM) — real-time health data capture and transmission from monitoring devices, enabling continuous assessment
- Behavioral health guidance, medication compliance support
- Automated claim creation and eligibility checks for CCM/RPM billing

**Analytics & Reporting:**
- Intergy Practice Analytics — 5,000 reportable clinical and financial fields
- Performance dashboards tracking diagnoses, lab results, vitals, visits, risk levels
- Population health insights
- Quality measure performance (MIPS reporting support)
- Regulatory reporting (public health syndromic surveillance, immunization registries)

**Interoperability & Integrations:**
- FHIR API (g)(10) certified — standardized API access for third-party apps
- CommonWell Health Alliance membership for cross-network data exchange
- Direct messaging ((h)(1)) for secure provider-to-provider communication
- C-CDA document exchange for transitions of care
- Lab interface integrations (bidirectional: orders out, results in)
- Pharmacy integrations via Surescripts (e-prescribing network)
- Integration partners include PatientPop, Clearwave, Ambra Health (imaging), CareTrack

### Data & Content

Based on the modules and features described above, Intergy stores and manages a broad range of data:

**Clinical data** (well-documented): Patient demographics, encounter notes/clinical documentation (using 500+ templates), problem lists, medication lists, allergy lists, vital signs, lab orders and results, imaging orders, immunization records, clinical alerts, health reminders/care gap tracking, clinical decision support data, patient health history, and clinical documents (scanned/indexed via Document Manager).

**Prescription data** (well-documented): e-Prescribing records, controlled substance prescriptions (EPCS), PDMP check results, prescription benefit information, medication history.

**Administrative/scheduling data** (well-documented): Appointment schedules, patient check-in records, resource allocation, multi-site scheduling data.

**Billing/financial data** (well-documented): Insurance eligibility verification records, claims data (including scrubbed claims), charge records, payment records, accounts receivable, denial management data, clearinghouse transaction records, medical coding data.

**Patient engagement data** (well-documented): Patient portal messages, appointment requests, prescription refill requests, patient-submitted health history forms, patient bill payments.

**Telehealth data** (moderately documented): Telehealth visit records integrated into the EHR workflow. The extent of stored telehealth session metadata (vs. just charting the encounter) is not detailed.

**Care coordination data** (moderately documented): Chronic care management records, remote patient monitoring data (device readings, health metrics), care coordination notes, health coaching records.

**Analytics/reporting data** (moderately documented): Practice analytics with 5,000 reportable fields spanning clinical and financial data, quality measure calculations, population health metrics.

**Interoperability data** (moderately documented): C-CDA documents sent/received for transitions of care, CommonWell health data exchange records, Direct messages, FHIR API access logs.

**Document management data** (mentioned but not deeply detailed): Scanned documents, faxes, and other digitized records managed through Greenway Document Manager. The types of documents stored (consent forms, referral letters, external records, etc.) are not enumerated but the capability to scan, index, and store arbitrary documents is described.

**What's unclear**: The degree to which certain add-on services (Revenue Services clearinghouse, Clinical Assist AI documentation) store data within the Intergy database vs. in separate systems. The vendor markets these as integrated but the data architecture boundaries are not publicly documented.

---

*Note: Greenway Health also offers Prime Suite (from the original Greenway Medical Technologies product line), which is a separate EHR platform with its own architecture. Prime Suite has separate CHPL certifications and is not covered in this research, as the target product is Intergy EHR specifically.*
