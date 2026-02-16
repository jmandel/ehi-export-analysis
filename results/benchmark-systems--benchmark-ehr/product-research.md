# Benchmark Systems — Product Research

Researched: 2026-02-16
Developer website: https://www.benchmarksystems.com

## Overview

Benchmark Systems (now operating as **Benchmark Solutions, a division of Harris**) is a US-based healthcare IT vendor headquartered in Forest, VA. The company has operated for over 40 years, serving independent medical practices and small healthcare organizations. In **July 2023**, Benchmark was acquired by **Harris Healthcare** (part of Harris Computer, itself owned by publicly traded Constellation Software). The company rebranded to "Benchmark Solutions" but maintained its existing products, team, and client contracts.

Benchmark Solutions provides an integrated, modular, cloud-based suite for ambulatory practices: EHR, Practice Management, and Revenue Cycle Management. They position themselves as serving independent and small practices across 27+ medical specialties. They are a relatively small vendor in the ambulatory EHR space — exact customer counts are not disclosed publicly, but the Harris acquisition announcement referenced "thousands of practices across North America." Capterra/Software Advice shows ~170 reviews with a 4.7/5 rating, suggesting a modest but established user base. Pricing starts around $147/month per the third-party listing on EMRSystems.net.

## Product: Benchmark EHR

CHPL ID: 9098

### What It Is

Benchmark EHR is a cloud-based, ONC-certified electronic health records system designed for outpatient ambulatory clinics. It is part of a broader integrated product suite that includes Benchmark PM (Practice Management) and Benchmark RCM (Revenue Cycle Management). While the EHR is the certified module, the full Benchmark product is the combined EHR + PM + RCM suite — these are sold as modular products that integrate tightly with each other.

The certification is comprehensive: 50+ criteria covering clinical documentation (a)(1)–(a)(15), transitions of care (b)(1)–(b)(5), clinical quality measures (c)(1)–(c)(4), patient portal (e)(1)–(e)(3), public health reporting (f)(1),(f)(2),(f)(5),(f)(7), and API/FHIR access (g)(7),(g)(9),(g)(10)). This is a full-featured ambulatory EHR certification.

### Users & Market

- **Target users**: Physicians, clinical staff, and practice administrators at independent and small ambulatory practices
- **Clinical settings**: Outpatient clinics across 27+ specialties including family practice, internal medicine, pediatrics, cardiology, dermatology, OB/GYN, gastroenterology, orthopedics, urology, neurology, oncology/hematology, pulmonology, rheumatology, ENT, pain management, endocrinology, nephrology, infectious disease, general surgery, surgery centers, urgent care, FQHCs/community health centers, occupational medicine, allergy/immunology, physical therapy, speech therapy, and neurosurgery
- **Market size**: Small-to-mid vendor; "thousands of practices" per acquisition announcement. ~170 reviews on Capterra/Software Advice with 4.7/5 rating
- **Geography**: North America (US-focused)
- **Go-to-market**: Direct sales; now backed by Harris/Constellation Software's resources
- **End users day-to-day**: Physicians (charting, prescribing, ordering), clinical staff (documentation, lab review), billing staff (coding, claims), practice managers (scheduling, reporting), and patients (portal access)

### Modules & Functionality

The Benchmark product suite consists of three main modules plus ancillary services. Based on vendor website, third-party reviews, and feature pages:

**Benchmark EHR (the certified module):**
- **Clinical documentation**: Progress notes generated during encounters, automatically added to patient medical records. Speech recognition/dictation capability. Customizable templates, dashboards, and forms for 40+ specialties (per vendor website).
- **Order sets & quick phrases**: Configurable workflow shortcuts
- **E-prescribing (eRx)**: Prescriptions sent directly to pharmacies natively within EHR
- **Lab results management**: Results accessible within patient charts and via patient portal
- **Automated coding recommendations**: E&M code suggestions based on type of care, time spent, and complexity — transferred to billing/PM for claims processing
- **Patient portal**: Patients can access lab results, order prescription refills, message providers, view appointments, complete intake forms. Distributes patient education materials from MedlinePlus aligned with diagnoses.
- **MIPS support**: Merit-Based Incentive Payment System reporting capabilities
- **Clinical quality measures**: CQM calculation and reporting (certified for (c)(1)–(c)(4))
- **Transitions of care**: C-CDA document creation and exchange (certified for (b)(1)–(b)(3))
- **Public health reporting**: Immunization registries, syndromic surveillance, cancer case reporting, electronic case reporting (certified for (f)(1),(f)(2),(f)(5),(f)(7))
- **FHIR/API access**: (g)(7),(g)(9),(g)(10) certified — supports standardized API access
- **Direct messaging**: (h)(1) certified — Direct protocol for secure health information exchange

**Benchmark PM (Practice Management — separate product, tightly integrated):**
- **Appointment scheduling**: Multi-resource filtering (providers, equipment, locations), automatic first-available finding, patient self-scheduling
- **Appointment reminders**: Automated via text, email, and voice
- **Patient demographics & insurance**: Captures and manages patient demographic data, auto-ports to EHR
- **Insurance verification**: Automated post-encounter insurance verification
- **Billing & claims**: Real-time claim status tracking for private insurers, Medicare, Medicaid. Integrated clearinghouse partnership. Paper and digital patient statements/superbills. CPT and ICD-10 coding.
- **Benchmark Pay**: Embedded patient payment portal for online bill payment/electronic collections
- **Mobile provider portal**: Allows providers on rounds (hospital, dialysis) to capture charges with integrated CPT/ICD-10 coding
- **Reporting & dashboards**: Customizable report templates, operational dashboards showing A/R, reimbursement days, collections comparisons

**Benchmark RCM (Revenue Cycle Management — service + software, offered as add-on):**
- Patient registration and eligibility verification
- Charge entry and ICD/CPT coding review
- Claim submission (97% first-pass rate claimed)
- Payment posting from insurance remittance
- Denial management and resubmission
- Patient statement generation and collections coordination
- Claims agency coordination
- Reports 108% net collections and <33 day average A/R

**Benchmark ProTech**: IT support and hardware services (not a data-generating clinical product)

### Data & Content

Based on the features documented above, the Benchmark product suite manages the following categories of data:

**Clinical data (in Benchmark EHR):**
- Patient medical records / charts
- Progress notes and encounter documentation
- Problems/diagnoses
- Medications and prescription history (e-prescribing data)
- Lab results
- Allergies (implied by clinical criteria certification)
- Immunization records (certified for (f)(1) immunization registry reporting)
- Clinical quality measure data
- Order sets
- Patient demographics (shared with PM)
- Patient-provider messages (via portal)
- Patient intake forms
- Patient education materials distributed
- C-CDA documents (transitions of care)
- Direct messages
- Social histories (mentioned on EMRSystems.net: "access to patient records, social histories, labs, specialty specific templates")
- Specialty-specific templates and data

**Administrative/financial data (in Benchmark PM, integrated with EHR):**
- Appointment scheduling data
- Patient demographics and insurance information
- Billing records, superbills, and claims
- CPT and ICD-10 codes per encounter
- Insurance eligibility and verification records
- Payment records and remittance
- Denial and resubmission records
- Patient statements
- Accounts receivable data
- Collections data
- Practice operational reports

**Key uncertainty**: The line between what's stored in the "EHR" module vs the "PM" module is blurred. The vendor describes them as tightly integrated — coding recommendations flow from EHR to PM, demographics auto-port between them, and they share patient records. For (b)(10) EHI export purposes, the relevant question is whether the export covers data from the full product (EHR + PM) or just the EHR module. The certification is under "Benchmark EHR" but the product as used includes PM and potentially RCM data that flows through the same patient record.

**What the website doesn't clarify:**
- Whether imaging/radiology data is stored (no mention found)
- Document scanning/attachment storage capabilities (not mentioned)
- Detailed audit log content
- How referral tracking data is managed
- Whether the system stores clinical decision support rules/alerts as data
