# Indian Health Service — Product Research

Researched: 2026-02-15
Developer website: https://www.ihs.gov/promotinginteroperability/certificationoverview/

## Overview

The Indian Health Service (IHS) is a federal agency within the U.S. Department of Health and Human Services responsible for providing healthcare to approximately 2.6 million members of 574 federally recognized American Indian and Alaska Native (AI/AN) tribes. IHS is not a commercial vendor — it is a government healthcare provider and developer that built its own health information system beginning in the early 1980s. The agency operates 45 hospitals and over 600 other facilities (clinics, health stations, etc.) across 12 service areas, primarily in rural and remote locations.

IHS developed the Resource and Patient Management System (RPMS) as a comprehensive, decentralized health information system. RPMS is built on the same technology foundation as the VA's VistA system — both descend from the VA's Decentralized Hospital Computer Program (DHCP) and run on MUMPS (M) programming language atop InterSystems Caché/IRIS databases. RPMS was first deployed around 1984 and has been continuously developed and maintained by IHS since then.

The system serves three user communities (the "I/T/U" community): IHS-operated federal facilities, tribal health programs operating under self-governance compacts, and urban Indian health organizations. Some tribal programs have transitioned to commercial EHRs (Cerner, NextGen, athenahealth), and in November 2023, IHS selected General Dynamics Information Technology (GDIT) to implement a new enterprise EHR using Oracle Cerner technology — a potential $2.5 billion, 10-year contract. As of 2025-2026, RPMS remains operational and certified while the modernization effort proceeds.

## Product: Resource and Patient Management System Electronic Health Record

CHPL IDs: 11717

### What It Is

RPMS EHR is a comprehensive, integrated health information system covering clinical, administrative, and financial functions. It is not a single application but a suite of approximately 50-100 software packages running on a shared MUMPS/FileMan database. The certified module (version BCERv9.0, certified 2025-11-24) encompasses the full breadth of RPMS functionality — clinical documentation, pharmacy, laboratory, radiology, scheduling, billing, immunizations, public health reporting, and more.

The EHR graphical interface is built on the VueCentric framework (owned by Medsphere Systems Corporation), which provides a Windows-based GUI client that communicates with the RPMS server via Remote Procedure Call (RPC) Broker. The underlying database layer uses VA FileMan for data management, with VA Kernel providing the runtime environment.

RPMS was the first VistA-related EHR certified for Meaningful Use Stage I and holds broad ONC certification across 42 criteria covering clinical data (a)(1)-(a)(14), transitions of care (b)(1)-(b)(3), clinical quality measures (c)(1)-(c)(3), security (d)(1)-(d)(13), patient access (e)(1), public health reporting (f)(1)-(f)(6), APIs including FHIR (g)(7)-(g)(10), and immunization registry exchange (h)(1).

### Users & Market

**Primary users** (per the SED description): medical providers, nursing staff, health information management staff, pharmacy staff, and imaging and laboratory personnel at clinics and hospitals.

**Scale**: IHS serves 2.6 million AI/AN patients across 574 tribes. As of the most recent assessments, hundreds of IHS and tribal sites run RPMS. A 1993 GAO report documented 229 operational sites; deployment expanded significantly through the 2000s. The system is also used at some Hawaii public health sites and select American Guam clinics.

**Clinical settings**: The system supports both ambulatory clinics and hospitals, including emergency departments, inpatient wards, dental clinics, behavioral health, optometry, and public health programs. IHS facilities tend to be in rural and remote areas, often serving as the sole healthcare provider for their communities.

**User satisfaction is low**: A Regenstrief Institute assessment found 60.3% of users believe RPMS needs "significant improvements or a complete overhaul," 30.3% rated overall quality as "poor" or "very poor," and 93% agreed it was time to replace the system. The planned Oracle Cerner transition reflects this assessment.

**Notable departures**: Alaska Native Medical Center switched to Cerner in the mid-2000s. Multiple California tribal sites have adopted NextGen. Community Health Clinics of West Virginia used RPMS via Medsphere but later transitioned to athenahealth.

### Modules & Functionality

RPMS comprises a large suite of packages organized into clinical, administrative, and infrastructure categories. The following is based on the IHS RPMS applications pages and historical documentation.

**Core Clinical Applications:**
- **Patient Care Component (PCC)**: The clinical heart of RPMS — a centralized clinical data repository using a "V-file" architecture (V MEASUREMENT, V PROVIDER, V POV, V LAB, V MICROBIOLOGY, V BLOOD BANK, V HOSPITALIZATION, etc.) where all visit-related data links to a central VISIT file. PCC was revolutionary when designed in 1983-85 and its fundamental structure has remained stable since. It enables population health queries and integrated billing through its relational visit-file design.
- **Electronic Health Record GUI (EHR)**: Graphical user interface built on VueCentric framework providing the clinician-facing application.
- **Text Integration Utility (TIU)**: Template-based clinical note authoring for clinic notes and other documentation.
- **Outpatient Pharmacy (PSO)**: Management and reporting of outpatient medication regimens.
- **IHS Pharmacy MOD (APSP)**: IHS-specific modifications to VA pharmacy packages.
- **Electronic Prescribing of Controlled Substances (BEPC)**: DEA-compliant e-prescribing for controlled substances.
- **e-Prescribing Productions (BEPR)**: Ensemble interface engine for pharmacy network integration and Surescripts connectivity.
- **Pharmacy - National Drug File (PSN)**: Drug data management from FDA sources.
- **Pharmacy - Controlled Drug Export System (BPDM)**: Export files for controlled substance dispensing.
- **Laboratory (LR)**: Comprehensive laboratory/pathology data and record keeping across all pathology areas.
- **Electronic Laboratory Reporting (BLE)**: HL7 message generation for lab result reporting (including COVID-19).
- **Adverse Reaction Tracking (GMRA)**: Allergy and adverse reaction documentation.
- **Immunization Tracking System (BI)**: Immunization data compilation, reporting, and adverse reaction tracking — described as "the crown jewel of RPMS."
- **Immunization Interface Management (BYIM)**: Bidirectional HL7 interface with state immunization registries.
- **Consult/Request Tracking (GMRC)**: Consultation and referral management.
- **Dental Data System (ADE)**: Dental care data capture.
- **Dental/EDR Interface (BADE)**: Bidirectional data exchange with Electronic Dental Record systems.
- **Behavioral Health System (AMH)**: Encounters, group services, treatment plans, case management for behavioral health.
- **Women's Health (WH)**: Women's health tracking and reporting.
- **Diabetes Management System (BDM)**: Specialized diabetic patient tracking and treatment assessment.
- **HIV Management System (BKM)**: HIV case management.
- **Emergency Room System (AMER)**: ER registration, admission, discharge, and management reporting.
- **Emergency Department Dashboard (BEDD)**: Emergency/urgent care operations management.
- **Chronic Disease Management (BCDM)**: Chronic condition management.
- **Care Management Event Tracking (CMET/BTPW)**: Routine patient event follow-up for care management.
- **Case Management System (ACM)**: Patient registers for managing select patient groupings.
- **Community Health Representative System (BCH)**: Documentation of community health activities.
- **Prenatal Module**: Prenatal care documentation.
- **Well-Child Module**: Questionnaire-oriented pediatric well-child visit forms.
- **Optometry**: Structured optometry reading documentation.

**Administrative and Financial Applications:**
- **Patient Registration (AG)**: Patient demographic and insurance eligibility database.
- **Patient Information Management System (PIMS)**: ADT (Admission/Discharge/Transfer), clinic scheduling, and sensitive patient tracking.
- **Third Party Billing (ABM)**: Insurance claims generation for Medicare, Medicaid, and private insurance (CMS-1500, UB-04, ASC X12 837).
- **Accounts Receivable (BAR)**: Third-party billing transaction processing and follow-up.
- **Pharmacy Point of Sale (ABSP)**: Online pharmacy claims submission to third-party payers.
- **Contract Health Services/Management Info System (ACHS)**: Document and fiscal management for outside provider referrals (now called Purchased/Referred Care).
- **Administrative Resource Management System (ACR)**: Requisitions and purchase orders.
- **Practice Management Application Suite (BPRM)**: Browser-based GUI for business functions.

**Population Health and Quality Reporting:**
- **Clinical Reporting System (BGP)**: GPRA (Government Performance and Results Act) and clinical performance measure data production.
- **iCare Population Management GUI (BQI)**: Windows-based tool for population health data retrieval.
- **eCQM Engine and Export Tool**: Clinical quality measure calculation and QRDA CAT-I export for CMS.
- **Computerized Public Health Activity Data System (BNI)**: Public health activities documentation.
- **Data Warehouse Export System (BDW)**: Export to IHS National Data Warehouse.

**Interoperability:**
- **Consolidated Clinical Document Architecture (BCCD)**: C-CDA Release 2.1 document generation.
- **C32/CCD Clinical Summary (BJMD)**: HITSP-format clinical summary generation.
- **Generic Interface System (GIS)**: HL7-based demographic and PCC data exchange.
- **IHS Support for HL7 Interfaces (BHL)**: HL7 data exchange with commercial and other applications.
- **Personal Health Record (BPHR)**: Patient Health Record and Direct Secure Messaging.
- **Master Patient Index (AGMP)**: Cross-facility patient identity management.
- **RPMS EHI Export (BREH)**: ONC-compliant EHI export using predefined national schema.

**Infrastructure:**
- VA FileMan (database management), VA Kernel (runtime), MailMan (internal messaging), RPC Broker (client-server communication), BMXNet (.NET framework utilities), IHS Code Mapping (SNOMED/LOINC mapping), and various toolkit extensions.

### Data & Content

Based on the module inventory and PCC architecture, RPMS stores an exceptionally broad range of health data:

**Clinical data**: Patient demographics and insurance eligibility, visit/encounter records (via PCC V-file structure), clinical notes (via TIU templates), problem lists with coded diagnoses, medication records (outpatient pharmacy, controlled substances, e-prescribing), allergies and adverse reactions, laboratory results across all pathology areas, radiology orders and results, immunization records including adverse reactions, vital signs and measurements, dental care records, behavioral health encounters and treatment plans, women's health data, diabetes management data, HIV case management, prenatal care, well-child visit data, optometry readings, surgical/day surgery data, emergency department records, and consult/referral tracking.

**Administrative and financial data**: ADT records, scheduling/appointments, insurance claims (Medicare, Medicaid, private — CMS-1500, UB-04, X12 837 formats), accounts receivable and third-party billing transactions, pharmacy point-of-sale claims, contract/purchased referred care documentation, requisitions and purchase orders.

**Population health and reporting data**: GPRA performance measures, eCQM quality measures (QRDA CAT-I), community health representative activity data, epidemiological data accumulated over decades, public health activity data, national data warehouse exports.

**Interoperability artifacts**: C-CDA documents, HL7 messages (demographic and clinical), immunization registry exchange messages, FHIR API data (per g(10) certification), Direct Secure Messaging, EHI export files.

**Internal system data**: MailMan messages (internal electronic mail), user security audit logs, site tracking data, code mapping tables (SNOMED, LOINC, ICD, CPT).

The PCC V-file architecture is the central repository linking all clinical data to visits. This design — unchanged since the mid-1980s — is what enables RPMS's population health query capabilities and integrated billing. The EHI Export package (BREH) generates exports using a nationally defined schema published at the IHS FTP site, with schema definition documents and versioned schema text files (2023, 2024, 2025).

**Notable**: RPMS has decades of accumulated population health data for AI/AN communities. A key concern in the Oracle Cerner transition is that only 24 months of recent clinical data will migrate — the rest will be archived in a "Four Directions Warehouse" with API-based access.

---

## Relationship to VistA

RPMS and VistA share the same foundational infrastructure (Kernel, FileMan, MailMan, drug files, code sets) but diverged significantly in clinical data architecture. RPMS was originally focused on outpatient/ambulatory care for diverse AI/AN populations; VistA was focused on inpatient/hospital care for veterans. The most significant divergence is between PCC (RPMS's clinical repository) and PCE (Patient Care Encounter — the VA's adaptation of PCC, which was heavily rewritten). Many RPMS packages originated as VistA imports (Pharmacy, Lab, Radiology, Scheduling) but have been extensively modified. Conversely, the VA adopted RPMS innovations including the Problem List and PCC concept. A convergence analysis found varying difficulty levels: some packages differ in only a few routines, while Lab has 819 of 1,132 routines modified plus 197 IHS extensions, and PCC vs PCE represents a fundamentally different clinical philosophy.
