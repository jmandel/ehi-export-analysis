# SMARTMD Technologies, Inc. — Product Research

Researched: 2026-02-16
Developer website: https://www.smartmd.com/

## Overview

SMARTMD Technologies, Inc. is a privately held healthcare technology company headquartered in Whitefish Bay, Wisconsin, with additional offices in Georgia and Florida. Founded in 1999, the company originally focused on medical transcription and dictation services for physicians. Over time, SMARTMD expanded into a broader healthcare IT platform encompassing EHR, billing, referral management, and CRM tools, with a particular focus on the hospice, palliative care, and PACE (Program of All-Inclusive Care for the Elderly) markets.

The company's CEO is Nandip Kothari (since 2008), who holds an MBA from Kellogg School of Management. Employee counts vary across sources — LinkedIn lists 201–500 employees, while other directories (ZoomInfo, Owler, ContactOut) suggest a smaller actual workforce of approximately 28–37 employees, suggesting the LinkedIn figure may include contracted transcriptionists or be outdated. SMARTMD was named second in the U.S. for "Trust, Accountability, and Transparency" by Black Book Research in 2017 for Medical Transcription. The company's specialties as listed on LinkedIn include: Medical Transcription Services, Dictation Platform, Medical Billing and Collections, EHR Scribe Services, Referral Management, MACRA/MIPS Registry, Hospice, Palliative Care, and PACE.

## Product: SMARTMD Palliative

CHPL ID: 11476

### What It Is

SMARTMD Palliative is a palliative care-specific EHR and practice management system, certified as ONC Health IT Module version 6 (certified 2024-05-31). The product is described as an "EMR, intake, and Medicare Part B" system "designed exclusively for palliative care" that "works with your existing hospice EMR." This positions it as a specialty-focused clinical platform intended to complement (not replace) a hospice organization's primary EMR system, while providing palliative care-specific documentation, billing, and workflow tools.

The certified module carries a substantial set of ONC criteria: clinical data management ((a)(1), (a)(2), (a)(5), (a)(14)), transitions of care ((b)(1)), EHI export ((b)(10)), receive/display C-CDA ((b)(11)), clinical quality measures ((c)(1)), FHIR API access ((g)(7), (g)(9), (g)(10)), and direct messaging ((h)(1)). This breadth suggests the product functions as a fairly complete clinical EHR, not just a documentation overlay.

SMARTMD appears to be part of a broader product ecosystem that includes:
- **SMARTMD Palliative** — the palliative care EHR (this certified product)
- **Accelerate CRM** — a hospice/palliative-specific CRM for managing referral sources and sales
- **VIP (Virtual Intake Platform)** — a mobile-friendly patient admissions/enrollment tool used for PACE and hospice
- **Medical Transcription Services** — the company's original business, available standalone or integrated
- **Medical Billing & Collections** — billing services, likely partly integrated with the EHR

It is unclear which of these are separate products vs. modules within a single platform. The CHPL certification applies specifically to "SMARTMD Palliative" but the broader ecosystem likely shares data and infrastructure.

### Users & Market

SMARTMD Palliative targets palliative care programs, particularly those operated by or alongside hospice organizations. The product is designed for:
- **Palliative care providers** (physicians, nurse practitioners) who document patient visits
- **Social workers and chaplains** on interdisciplinary care teams
- **Administrative/billing staff** who manage chronic care billing and reimbursement
- **Field-based providers** who need mobile access for home visits

The product emphasizes support for the CMS GUIDE (Guiding an Improved Dementia Experience) payment model, automatically generating documentation and spreadsheets formatted per CMS requirements. This suggests the customer base includes organizations participating in CMS value-based care demonstrations.

No specific customer counts were found. The company's market appears to be small-to-mid-size hospice organizations that are adding palliative care programs and need a specialized EHR that integrates with their existing hospice EMR. The integration with Axxess Palliative Care (a major hospice platform) suggests SMARTMD serves as a complementary tool rather than a standalone enterprise system.

### Modules & Functionality

Based on vendor materials and search results, the following modules and features are described:

**Clinical Documentation:**
- Clinical notes designed by palliative care providers with specialty-specific templates
- Standard palliative assessments built in: PPS (Palliative Performance Scale), FAST (Functional Assessment Staging Tool), ESAS (Edmonton Symptom Assessment System)
- Key quality measures (acuity, PPS score, pain levels) automatically extracted from notes and plotted on trend graphs to show patient trajectory toward hospice
- Voice documentation with speech-to-text engine that transcribes and summarizes dictation
- Mobile documentation via native iOS and Android apps with offline capability and autosync
- Ability to scan forms, capture consent documentation, and manage files

**Scheduling & Patient Management:**
- Provider schedules pushed to mobile phones with one-tap directions to patient homes
- Appointment scheduling at bedside; system can auto-place placeholder appointments based on clinical notes
- Patient boards with real-time status updates visible to the care team
- Dashboards for providers, admin staff, and management

**Billing & Reimbursement:**
- Designed for chronic care billing — PCM (Principal Care Management), TCM (Transitional Care Management), CCM (Chronic Care Management), and PIN codes
- Time-tracking for patient conversations to ensure every billable minute is captured
- Custom time-based billing reports that recommend CPT codes based on chronic care coding rules
- Month-end billing generation
- Medicare Part B billing support

**Team Communication:**
- HIPAA-compliant secure messaging platform for interdisciplinary care team communication
- Designed to support multiple providers, social workers, and chaplains on the same patient

**Integrations:**
- Integration with Axxess Palliative Care for patient demographics, admissions, discharges, diagnoses, and location data exchange
- Designed to work alongside existing hospice EMR systems
- C-CDA receive/display capability (certified (b)(11))
- FHIR API access (certified (g)(7), (g)(9), (g)(10))
- Direct messaging capability (certified (h)(1))

**CRM & Referral Management (Accelerate CRM):**
- Referral source management connecting sales, referral, and admissions processes
- Account prioritization and market data to identify new referral partnerships
- Complete view of organizational relationships from initial partner contact to facility census

**Intake & Admissions (VIP):**
- Virtual Intake Platform for fully mobile-friendly enrollment
- Supports patients, caregivers, families, and admissions teams
- Used for PACE enrollments with implementation in 4–6 weeks

**Quality & Compliance:**
- MACRA/MIPS registry and reporting capabilities
- CMS GUIDE model documentation support with auto-generated compliance spreadsheets
- Clinical quality measure tracking (certified (c)(1))

### Data & Content

Based on the features and certifications described, the product manages the following data types (supported by evidence):

- **Patient demographics and status** — evidenced by Axxess integration exchanging demographics, admissions, discharges, diagnoses, and locations
- **Clinical encounter notes** — palliative-specific documentation with structured assessments (PPS, FAST, ESAS)
- **Quality measure data** — acuity scores, PPS scores, pain levels extracted and trended over time
- **Audio dictation recordings** — voice documentation feature with transcription (confirmed by App Store listing)
- **Schedules and appointments** — provider scheduling with mobile access
- **Billing/charge data** — time-based chronic care billing, CPT codes, monthly billing reports, Medicare Part B
- **Secure messages** — HIPAA-compliant team messaging
- **Scanned documents and images** — consent forms, scanned documents (per App Store listing)
- **Referral source and CRM data** — if Accelerate CRM is part of the certified product ecosystem
- **MIPS/quality reporting data** — per App Store listing and MACRA/MIPS registry capability
- **Care plans** — implied by palliative care workflows and CMS GUIDE model support, though not explicitly described as a standalone feature
- **C-CDA documents** — receive and display capability certified under (b)(11)
- **FHIR resources** — exposed via certified API ((g)(10))

**Gaps/Uncertainties:**
- The website does not mention e-prescribing, which is consistent with the absence of (a)(10) certification. Palliative care may rely on the primary hospice EMR for medication management.
- No patient portal or patient-facing view-download-transmit feature is mentioned, and (e)(1) is not among the certified criteria.
- It is unclear whether the Accelerate CRM and VIP intake platform data are part of the certified product's data scope or are separate products.
- The website is heavily JavaScript-rendered, making it difficult to extract detailed content; some features may be described on the site but not captured in this research.
- Lab results, imaging, and other diagnostic data are not mentioned — palliative care programs may rely on other systems for these.

---
