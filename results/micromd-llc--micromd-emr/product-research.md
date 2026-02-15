# MicroMD, LLC — Product Research

Researched: 2026-02-14
Developer website: https://www.micromd.com/certified/

## Overview

MicroMD, LLC is a healthcare IT company based in Youngstown, Ohio, founded in 1982. The company was acquired by Henry Schein, Inc. in October 2006 and now operates as a subsidiary of Henry Schein Medical Systems, Inc. Henry Schein is a Fortune 500 healthcare distribution company (publicly traded on NASDAQ: HSIC). MicroMD develops practice management, electronic medical records, document management, and patient engagement software for independent medical practices and community health centers across the United States.

MicroMD targets small-to-medium independent practices, multi-specialty groups, community health centers (CHCs), Federally Qualified Health Centers (FQHCs), and Rural Health Centers (RHCs). The company claims a 12-year average customer retention rate and 98% support satisfaction rating. They were recognized in the 2017 KLAS Awards as Best Ambulatory EMR/PM. MicroMD supports eight named specialties: Cardiology, Dermatology, ENT, Gastroenterology, Ob-Gyn, Pediatrics, Primary Care, and Urology. The product is available as client-server (on-premise) or web-based ASP (cloud) deployment.

The CHPL listing names the developer as "MicroMD, LLC" but press releases and investor relations materials consistently refer to "Henry Schein Medical Systems" as the certifying entity. The Drummond Group certifies the product.

## Product: MicroMD EMR

CHPL IDs: 11281

### What It Is

MicroMD EMR is a 2015 Edition CEHRT (Certified EHR Technology) ambulatory electronic medical records system. It is part of a broader MicroMD product suite that includes separate but tightly integrated modules for Practice Management (PM), Document Management (DMS), electronic prescribing (e-Rx), and the Secure Chart patient portal. The certified EMR module is one component of a larger product ecosystem — the practice management, document management, and patient portal modules are separate products that share data through integration interfaces.

The EMR is certified for a broad range of criteria: clinical data capture (a)(1)–(a)(5), (a)(12), (a)(14)–(a)(15); transitions of care (b)(1)–(b)(3); clinical quality measures (c)(1)–(c)(3); public health reporting (f)(1)–(f)(2), (f)(4); FHIR APIs (g)(7), (g)(10); and the EHI export criterion (b)(10). The SED intended user description is "Ambulatory."

### Users & Market

MicroMD serves independent ambulatory practices ranging from solo providers to larger multi-specialty groups and community health centers. Key user segments include:

- **Independent practices**: Small-to-medium physician offices across multiple specialties
- **Community health centers**: CHCs, FQHCs, and RHCs with specialized features like sliding fee schedules, UDS reporting, and dental billing
- **Multi-specialty groups**: Practices across cardiology, dermatology, ENT, gastroenterology, Ob-Gyn, pediatrics, primary care, and urology

Day-to-day users include physicians (clinical documentation, ordering, prescribing), clinical staff (documentation, health maintenance), front office staff (scheduling, registration, eligibility verification), billing staff (claims management, payment posting, collections), and practice managers (reporting, analytics). Patients interact through the Secure Chart patient portal.

The vendor distributes through Henry Schein's sales network. No specific customer count was found on the website, but the 12-year average retention and KLAS recognition suggest a stable installed base. Pricing starts at approximately $200/month per user (per third-party reviews), suggesting a mid-market positioning.

### Modules & Functionality

**Clinical Documentation (EMR Core)**
- Multiple documentation methods: SOAP format, free-text entry, templates, forms, and speech recognition (Dragon Premier Partner integration)
- ICD-10 code search and assignment
- Image management with anatomical diagram annotation
- Customizable templates at no additional cost
- Specialty-specific workflows for eight named specialties

**e-Prescribing**
- Two-way e-prescribing through Surescripts
- Controlled substance prescribing via MicroMD EPCS Gold
- Drug interaction checking and medication safety alerts

**Clinical Decision Support**
- Health maintenance alerts and reminders
- Drug interaction and allergy checking
- Immunization tracking and status display
- Patient overview dashboard with customizable alerts

**Lab Integration**
- Interfaces with major labs: LabCorp, Quest Diagnostics, Fletcher-Flora Health Care, 4Medica, Schulyer House
- Electronic lab ordering and results delivery
- Demographic data export to labs

**Medical Device Integration**
- Real-time connectivity with devices from Welch Allyn, Midmark, and Burdick
- Supports ECGs, Holter monitors, and spirometers
- Direct data capture from devices into patient records

**Telehealth**
- Medpod virtual video visit integration (launched with Version 17)
- HIPAA-secure video visits documented in the EMR
- Available as pay-per-encounter or annual subscription

**Practice Management (Separate PM Module, Integrated)**
- Appointment scheduling with intelligent waiting lists
- Patient registration with OCR scanning of ID/insurance cards
- Automated eligibility verification with insurance effective date tracking
- Claims management with EDI processing through clearinghouse partners (ECP, Gateway EDI, RealMed, Practice Insight)
- Code scrubbing to flag errors before submission
- Payment posting via electronic remittance, manual entry, or batch processing
- Patient statements, payment plans, and credit card processing
- Accounts receivable reporting and RBRVS benchmarking
- Direct EDI connections with Medicare, Medicaid, and Blues plans
- Collections account export functionality

**Community Health / FQHC Features**
- Sliding fee schedule calculations for patients at various income levels
- UDS reporting for grant compliance
- ADA dental billing integration (Dentrix compatibility)
- Temporary patient registration

**Document Management (MicroMD DMS — Separate Module)**
- Electronic document filing, scanning, and indexing
- Stores patient account charts, pathology results, labs, and non-patient documents (staff, vendor, correspondence)
- Drag-and-drop sorting, markup and annotation tools
- Integration with external documents and e-faxes

**Patient Portal (Secure Chart — Separate Module)**
- Two-way patient-to-practice secure messaging
- Online appointment scheduling and requests
- Lab results and document sharing
- Digital patient intake forms
- Appointment reminders via email, text, and voice
- Post-visit surveys
- Two-way texting

**Reporting & Analytics**
- Accounts receivable, claims tracking, financial analysis reports
- Export to Excel/Access formats with graphical display
- ODBC-compliant database for third-party reporting (Crystal Reports, etc.)
- Clinical quality measure reporting for MIPS

**Interoperability**
- HL7 standard, XML specification, Internet protocols
- Published Windows APIs for integration
- FHIR API access (certified for g(7) and g(10))
- C-CDA document support for transitions of care
- Public health reporting: immunization registries, electronic case reporting, syndromic surveillance

### Data & Content

Based on the features and modules described above, MicroMD EMR and its integrated product suite manage the following data:

**Clinical data (EMR)**: Patient demographics, encounter notes (SOAP format), problem lists, medication lists, allergy lists, immunization records, vital signs, clinical images and annotated anatomical diagrams, lab orders and results, medical device data (ECGs, spirometry, Holter), health maintenance records, clinical alerts, referral information, ICD-10 diagnoses, care plans, and clinical quality measure data.

**Prescribing data**: Medication orders, prescription history, controlled substance prescriptions (EPCS), drug interaction alerts, pharmacy routing information (via Surescripts).

**Practice management data (PM module)**: Appointment schedules, patient registration and demographic data, insurance information and eligibility history, claims and billing records, payment history (remittance, patient payments), accounts receivable data, fee schedules (including sliding fee for FQHCs), provider staffing and utilization data.

**Document management data (DMS module)**: Scanned documents, e-faxes, pathology results, correspondence, staff and vendor records, intake forms, Microsoft Word templates.

**Patient portal data (Secure Chart)**: Secure messages between patients and practice, appointment requests, patient-entered intake forms, published lab results and documents.

**Public health data**: Immunization registry submissions, electronic case reports, syndromic surveillance data.

**Important note on product boundaries**: The certified module is "MicroMD EMR" but the full product ecosystem includes separate PM, DMS, and Secure Chart modules that share data through integration interfaces. It is unclear from the vendor's materials exactly which data is stored within the EMR module versus the PM, DMS, or portal modules. The PM and EMR share demographic data, insurance information, scheduling details, referrals, and charges. The EHI export requirement under (b)(10) covers "all electronic health information that can be stored at the time of certification by the product, of which the Health IT Module is a part" — which would encompass the full product, not just the certified EMR module.

**User reviews on Capterra (3.2/5 from ~20 reviews)** note that reporting capabilities are "antiquated and cumbersome" and that the system "struggles with integrations, lacking the ability to build flat-file transfers." Users praise the intuitive interface and tight lab/device integration.
