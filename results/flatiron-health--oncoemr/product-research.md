# Flatiron Health / OneOncology — Product Research

Researched: 2026-02-16
Developer website: https://flatiron.com

## Overview

Flatiron Health is a healthcare technology company focused exclusively on oncology, describing its mission as "reimagining the infrastructure of cancer care." Founded in 2012, the company was acquired by Roche in 2018 for $1.9 billion. Prior to the Roche acquisition, Flatiron had acquired Altos Solutions in 2014 — the original developer of OncoEMR, which at the time had over 1,300 oncology clinicians and served ~550,000 unique cancer patients annually.

Flatiron operates in two primary areas: (1) point-of-care clinical software for oncology practices, and (2) real-world evidence and data solutions for biopharma research. The EHR/clinical software side — branded as the "OncoCloud" platform — is the basis for the ONC-certified products. As of recent reporting, Flatiron's technology is embedded in approximately 275 oncology practices, supporting ~2,500 providers across ~800 locations managing nearly one million active cancer patients.

**OneOncology** is a separate entity — a network of independent community oncology practices, originally launched in 2018 with a $200 million investment from General Atlantic. Founding practices included Tennessee Oncology, New York Cancer & Blood Specialists, and West Cancer Center. OneOncology uses Flatiron's technology platform. In 2023, TPG and AmerisourceBergen (now Cencora) acquired OneOncology for $2.1 billion. As of late 2025, Cencora is accelerating full acquisition (valued at ~$7.4 billion enterprise), and the network has grown to ~1,750 providers across 565+ care sites nationwide.

The CHPL listing names the developer as "Flatiron Health, OneOncology, LLC" — reflecting the joint relationship. OncoEMR is Flatiron's product; the "OneOncology HIE Integration" is a newer, narrowly-scoped certified module likely created for OneOncology's health information exchange needs.

---

## Product: OncoEMR (part of OncoCloud Suite)

CHPL ID: 11115

### What It Is

OncoEMR is a cloud-based, oncology-specific electronic health record system. It is the clinical EHR component of Flatiron Health's broader "OncoCloud Suite," which also includes OncoBilling, OncoAnalytics, OncoTrials, and the CareSpace patient portal. The certified module is OncoEMR, but the full product platform is the OncoCloud Suite — an integrated oncology practice management and clinical system.

OncoEMR is certified for a wide range of criteria (30+ across clinical, care coordination, patient portal, public health reporting, and FHIR API categories), indicating it is a full-featured clinical EHR rather than a narrow module. Certified criteria include CPOE for medications, labs, and imaging (a)(1-3); drug interaction checks (a)(4); demographics (a)(5); clinical decision support (a)(12); patient portal/VDT (e)(1); transitions of care (b)(1-3); e-prescribing; immunization and cancer registry reporting (f)(1), (f)(4), (f)(5); and FHIR APIs (g)(7-10).

### Users & Market

OncoEMR is used by community oncology/hematology practices — the SED intended user description is "Oncology/Hematology Community Practices." Users include medical oncologists, hematologists, nurses, clinical research coordinators, billing staff, and practice administrators.

The system supports practices ranging from small community oncology groups to larger multi-site networks. Notable customer deployments include:
- **Oncology Consultants** (Houston, TX) — selected OncoEMR per a Flatiron press release
- **South Carolina Oncology Associates** — also announced as an OncoEMR customer
- **OneOncology network practices** — Tennessee Oncology, New York Cancer & Blood Specialists, West Cancer Center, and many others across the growing network

OncoEMR was rated #1 for Overall Satisfaction in the KLAS 2019 Medical Oncology Performance Report, outperforming competitors in 11 of 20 KPIs including "Overall Product Quality" and "Ease of Use."

### Modules & Functionality

The OncoCloud Suite comprises four integrated modules plus a patient portal, based on vendor materials and third-party review sites:

**OncoEMR (Clinical EHR)**
- Oncology-specific charting with customizable templates
- CPOE (Computerized Provider Order Entry) for medications, lab orders, and diagnostic imaging
- 3,000+ NCCN chemotherapy order templates built in
- AJCC staging content integrated into workflows
- First Databank drug information and patient education resources
- Drug-drug and drug-allergy interaction checking
- SureScripts-certified electronic prescribing
- Visit notes and regimen management
- Clinical benchmarking
- 150+ pre-loaded reports (patient wait times, drug utilization tracking, etc.)
- Transitions of care / clinical information reconciliation
- Immunization registry and cancer registry reporting
- MIPS/value-based care quality measure support

**OncoBilling (Revenue Cycle / Billing)**
- Built-in EDI with national clearinghouse
- Claims generation and claims scrubbing
- Real-time claim status viewing
- Electronic receiving of payer remittance and EOBs (Explanation of Benefits)
- Auto-allocation of payments
- Financial reporting

**OncoAnalytics / Flatiron Insight (Analytics)**
- Combines data from OncoEMR and OncoBilling
- Custom dashboards for clinical and operational insights
- Drug usage tracking, patient visit volumes, inbound referral monitoring
- Value-based care reporting (MIPS, OCM/EOM)
- Billing Insights module — identifies missed/incorrectly billed charges (one early user recovered ~$400K in underbilled charges over 12 months)

**OncoTrials (Clinical Research)**
- Patient identification and screening for clinical trials
- EHR-integrated trial matching
- Electronic regulatory binder and CTMS functionality

**CareSpace (Patient Portal)**
- Patient access to health information
- Bill payment
- Appointment scheduling
- Secure communication with care team
- Accessible at carespaceportal.com (login via accounts.flatiron.com)

**OncoAir (Mobile App)**
- Mobile access to patient charts, lab results, notes
- Used by clinicians on call and during hospital rounds

**Flatiron Assist (Clinical Decision Support)**
- Delivers evidence-based treatment options at the point of ordering
- Clinical pathways for 25+ disease areas (built in collaboration with OneOncology)

**Flatiron Clinical Pipe (Research Integration)**
- EHR-to-EDC connector for clinical trial data transfer

### Data & Content

Based on the modules and features described above, OncoEMR / OncoCloud stores and manages:

- **Clinical records**: Patient demographics, diagnoses (with AJCC staging), problem lists, medication lists, allergy lists, clinical notes/visit documentation, treatment plans, chemotherapy regimens and administration records
- **Orders**: Medication orders (including chemotherapy), lab orders, imaging orders — all via CPOE
- **Prescriptions**: E-prescribing data (SureScripts-certified), drug interaction data
- **Lab results**: Referenced in OncoAir mobile app features for reviewing lab results
- **Clinical content**: NCCN order templates, AJCC staging data, First Databank drug info
- **Billing/financial data**: Claims, remittances, EOBs, payment allocations, financial reports (via OncoBilling)
- **Patient portal data**: Patient-facing health information, secure messages, appointment records, bill payment records (via CareSpace)
- **Analytics data**: Aggregated clinical and operational metrics, drug utilization, visit volumes, referral data, quality measures (via OncoAnalytics/Flatiron Insight)
- **Clinical trial data**: Patient trial screening/matching, trial enrollment, regulatory documents (via OncoTrials)
- **Immunization and registry data**: Immunization registry submissions, cancer registry submissions
- **Care coordination data**: Transitions of care documents (C-CDAs), clinical information reconciliation
- **Audit/security data**: Audit logs, access controls, multi-factor authentication logs

The system integrates with external systems including radiology information systems (RIS), laboratories, inventory management, and practice management systems. Natera has publicly announced integration with OncoEMR for genomic test result delivery.

The platform is cloud-based SaaS and is compliant with HIPAA, HITRUST CSF, and SOC 2 Type 2.

---

## Product: OneOncology HIE Integration

CHPL ID: 11640

### What It Is

OneOncology HIE Integration is a much narrower certified product, with certification date of May 2025. It is certified only for (b)(10) — EHI export — plus security/design criteria. It has no clinical, patient portal, API, or public health reporting certifications.

This appears to be a health information exchange (HIE) integration layer built for or by OneOncology to facilitate data exchange across their network of oncology practices. The name "HIE Integration" and the minimal certification footprint suggest it is middleware or a data exchange component rather than a standalone clinical system.

### Users & Market

Given OneOncology's role as a network of 1,750+ providers across 565+ locations, this product likely serves the network's need to aggregate and exchange health information across its disparate member practices. OneOncology uses Flatiron's OncoEMR as its technology backbone, but member practices may also use other systems.

### Modules & Functionality

No detailed feature information was found for this product. The Flatiron certification page at flatiron.com/certification does not mention it. No vendor marketing materials, product pages, or third-party reviews describe it.

The CHPL certification criteria — just (b)(10) plus security requirements — suggest this is a focused data export/exchange tool, not a clinical EHR. It likely exists to meet the ONC Cures Act requirement for EHI export within OneOncology's HIE infrastructure.

### Data & Content

Unknown. Given the (b)(10) certification, this product must support export of all electronic health information it can store at the time of certification. However, without documentation of what data flows through this integration layer, it's unclear what the scope of "all EHI" would be for this product. It could range from a pass-through of data from connected EHR systems to a data aggregation platform with its own stored patient records.

The relationship between this product and OncoEMR is unclear from public sources — it may be a complement to OncoEMR's own (b)(10) certification, providing EHI export for data that flows through OneOncology's network-level HIE rather than residing in OncoEMR directly.
