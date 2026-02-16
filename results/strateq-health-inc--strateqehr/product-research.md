# Strateq Health, Inc. — Product Research

Researched: 2026-02-16
Developer website: https://www.strateqhealth.com

## Overview

Strateq Health, Inc. is a healthcare IT company focused on providing a cloud-based Hospital Information System (HIS) / EHR to critical access hospitals, rural and small community hospitals, and freestanding emergency rooms. The company is a subsidiary or division of Strateq Group, a Malaysia-based technology conglomerate that has been "redefining industries since 1983." Strateq Group operates across offices in Malaysia, Singapore, Thailand, Hong Kong, China, and the USA. Their healthcare division claims 22+ years of experience building and operating hospital information systems across 30+ hospitals internationally (primarily Malaysia, with expansion into the US market).

The US entity, Strateq Health, Inc., is headquartered in Plano, Texas (previously referenced as Houston in some materials). Co-founders are Datuk Tan Seng Kit (CEO) and CheeSiong Yee (COO & CTO). A 2019 press release via GlobeNewsWire cited 600+ employees globally, though the US team appears much smaller — the about page lists roughly six named leadership positions. The Strateq Group parent site references a product called "37 Degrees" as their cloud HIS offering, which appears to be the same underlying platform marketed as "StrateqEHR" in the US market.

The company's go-to-market targets the financially constrained rural/critical access hospital segment, emphasizing SaaS pricing (monthly fee, no upfront CapEx) and AWS cloud hosting secured by ARMOR. Named customers include ADHS and Nutex Health. Strateq exhibited at the 2019 TORCH (Texas Organization of Rural & Community Hospitals) conference, consistent with their rural hospital focus.

## Product: StrateqEHR

CHPL ID: 10778 (15.05.05.3097.STRQ.01.00.1.220105)
Version: 5
Certified: 2022-01-05
SED Intended Users: Inpatient physicians and nurses

### What It Is

StrateqEHR is described as "the first fully integrated, native cloud-based HIS" — a comprehensive hospital information system, not just an EHR module. It is designed to serve as a single platform covering clinical, financial/revenue cycle, and ancillary/departmental functions for small hospitals and freestanding ERs. The product is cloud-native on AWS, SaaS-delivered, and accessible from any web-enabled device.

The certified product appears to be the full HIS platform — not a component of something larger. The certification criteria are broad (30+ criteria spanning clinical data, care transitions, CQMs, public health reporting, APIs, and patient data access), consistent with a comprehensive inpatient system.

### Users & Market

**Primary users**: Inpatient physicians, nurses, HIM staff, registration/admitting staff, pharmacy, billing/revenue cycle staff, and hospital administrators.

**Target settings**: Critical access hospitals, rural hospitals, small community hospitals, and freestanding emergency rooms. The system explicitly advertises configurations for both inpatient hospital and freestanding ER workflows.

**Customer base**: The vendor claims 30+ hospital deployments internationally (across the Strateq Group parent). Named US references include ADHS and Nutex Health (a freestanding ER chain). Customer count in the US specifically is unclear — this appears to be a small-footprint vendor in the US market.

**Reviews**: A Capterra listing exists but was inaccessible. A few reviews on Five.Reviews show mixed feedback — some praising customer service, others complaining about pricing and performance. No G2 or KLAS profiles were found, which is consistent with a small/niche vendor.

### Modules & Functionality

The vendor website organizes the product into four solution areas: Clinical Solutions, Revenue Cycle, Ancillary Solutions, and Freestanding ER. Here is what the vendor describes:

**Patient Administration / ADT**
- Patient registration and quick registration (ER)
- Admission, discharge, transfer (ADT) workflows
- Bed management
- Insurance verification and pre-authorization
- Scheduling (including perioperative resource scheduling)

**Clinical Documentation**
- Patent-pending "Dynamic Form Engine" that renders clinical forms (H&P, care plans, admission assessments, nursing shift assessments) on-the-fly based on definitions by clinical informatics
- Provider documentation and nursing documentation
- Nursing care plans
- Dictation notes
- CCDA record generation

**CPOE (Computerized Provider Order Entry)**
- Close-loop CPOE for nursing orders, procedure orders, medication orders, laboratory orders, and radiology orders
- Complaint-specific order sets (particularly for ED workflows)
- Drug interaction and allergy checking

**Pharmacy / Medication Management**
- Integrated pharmacy module
- First Databank (FDB) drug database integration
- SureScripts integration for e-prescribing
- Allergy and drug interaction checking
- Medication reconciliation
- Home medication management
- eMAR (electronic medication administration record)

**Emergency Department**
- ED tracking board (updates patient location, arrival time, ESI level, vital signs, provider, length of stay, disposition, order status)
- Triage documentation
- ED-specific nursing documentation templates
- ED daily log reporting
- Process turnaround time reports
- State and local reporting
- Integrated discharge workflow with ePrescribing

**Nursing**
- Care plans
- Assessments
- eMAR
- Patient and unit worklists
- Nursing Kardex

**Perioperative**
- Patient and resource scheduling
- Operative checklists
- Clinical documentation
- Order entry

**HIM / Medical Records**
- Patient master record management
- Document scanning and management
- Deficiency tracking
- Release of information (ROI)

**Revenue Cycle Management**
- Integrated with Waystar for claims processing
- Clinical data capture and charge capture at point of care
- Real-time eligibility checking via Waystar (hundreds of payers)
- 3M CRS coding integration with automatic claim generation
- Electronic remittance processing and manual paper remit entry
- Credit card and check authorization with real-time posting
- Daily automated claim submission to Waystar
- Denial management with pre-defined denial templates via Waystar
- Patient statement generation (email and USPS via Waystar)
- Patient portal for credit/debit card payments
- Real-time GL journal entries
- Reporting: patient accounts, claims, remittance, payer data

**Patient Portal**
- Via Bridge Patient Portal (third-party integration)
- Supports patient payment (credit/debit)

**Interoperability / Data Exchange**
- CCDA generation and exchange for transitions of care
- Clinical information reconciliation
- e-Prescribing via SureScripts/NewCrop
- FHIR API access (g)(7)–(g)(10) certified
- Public health reporting: immunization registry and syndromic surveillance
- Clinical Quality Measures (CQMs) including antithrombotic therapy and opioid safety measures

**Third-party Integrations Referenced on Certification Page**
- FDB (First Databank) — drug database
- Aspyra CyberLAB — laboratory information system
- Bridge Patient Portal — patient portal
- NewCrop — e-prescribing
- Waystar — revenue cycle / claims clearinghouse
- 3M CRS — coding
- ARMOR — cloud security

### Data & Content

Based on the vendor's described modules and features, StrateqEHR stores and manages:

- **Patient demographics and registration data** (including insurance information, pre-authorization data)
- **Clinical documentation** (H&P, assessments, care plans, nursing notes, dictation notes, operative notes — rendered via their Dynamic Form Engine)
- **Orders** (medications, labs, radiology, nursing, procedures — via close-loop CPOE)
- **Medication data** (prescriptions, medication lists, home medications, medication reconciliation, eMAR administration records, allergy lists)
- **Lab results** (via Aspyra CyberLAB integration — unclear if StrateqEHR stores results directly or interfaces to a separate LIS)
- **Vital signs and clinical observations** (referenced in patient dashboard and ED tracking board)
- **ED tracking data** (location, ESI level, arrival times, disposition, length of stay)
- **Scanned documents and images** (via HIM document scanning module)
- **Medical record deficiency tracking data**
- **Billing and claims data** (charges, claims, remittance, eligibility, denials, GL journal entries, patient account balances)
- **Scheduling data** (patient appointments, perioperative resource scheduling)
- **CCDA documents** (transitions of care)
- **Immunization records** (for registry reporting)
- **Syndromic surveillance data**
- **Clinical quality measure data** (CQMs)
- **Audit logs** (required by (d)(1)–(d)(9) certification)
- **Patient portal data** (via Bridge — messages, payments; exact data stored in StrateqEHR vs. Bridge is unclear)

**Gaps/Uncertainties**:
- **Laboratory**: The integration with Aspyra CyberLAB is listed as additional third-party software. It's unclear how deeply lab data is stored within StrateqEHR versus the external LIS. The close-loop CPOE handles lab ordering, and results presumably flow back, but the boundary is unclear.
- **Radiology/Imaging**: CPOE supports radiology orders, but no PACS or radiology module is described. Radiology likely involves an external system with order/result interfaces.
- **Patient portal content**: Bridge Patient Portal is a third-party product. What data is stored in Bridge vs. StrateqEHR (e.g., patient messages, portal activity logs) is unclear.
- **Implantable device data**: Certified for (a)(14) which requires tracking unique device identifiers (UDIs), so this data should be stored.
- **Specific ancillary department data**: The "Ancillary Solutions" area is mentioned as a category on the solutions page but no detail was found on what specific ancillary modules (dietary, respiratory therapy, etc.) are included.

---
