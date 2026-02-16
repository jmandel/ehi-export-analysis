# Tenzing Medical LLC — Product Research

Researched: 2026-02-15
Developer website: http://www.tenzingmedical.com (note: SSL certificate expired at time of research)

## Overview

Tenzing Medical LLC is a very small healthcare IT company based in Oroville, California, that emerged directly from Oroville Hospital's pioneering self-implementation of the open-source VistA electronic health record system. The company was effectively co-founded by Oroville Hospital CEO Robert J. Wentz, who discovered VistA (Veterans Health Information Systems and Technology Architecture) — the VA's open-source EHR — as a cost-effective alternative to proprietary EHR systems. After implementing VistA at Oroville Hospital, the "Tenzing Medical concept began" as a vehicle to productize and certify their VistA adaptation.

Tenzing Medical is extremely small — likely fewer than 10 employees, closely tied to Oroville Hospital's internal development team. The company's contact email (dlefevre@orohosp.com) is an Oroville Hospital email address, underscoring the tight coupling between the company and the hospital. The company appears to be a niche VistA integrator/certifier rather than a broadly marketed commercial EHR vendor. Their website (tenzingmedical.com) had an expired SSL certificate at the time of research, suggesting limited active web presence maintenance.

Oroville Hospital is a 133-bed (some sources say 153-bed) private non-profit acute care facility in Northern California, classified as a 340B disproportionate share hospital. The hospital was among the first 100 hospitals nationally to achieve Meaningful Use Stage 1 certification through VistA. Their total VistA implementation cost was approximately $10-13 million — roughly half the industry average for a hospital of their size.

## Product: Tenzing VistA

CHPL ID: 10799

### What It Is

Tenzing VistA is an adaptation of the U.S. Department of Veterans Affairs' open-source VistA (Veterans Health Information Systems and Technology Architecture) EHR system, customized for use in a community hospital setting. VistA itself is a comprehensive, integrated health information system originally developed for the VA's 168 hospitals and 1,000+ clinics, consisting of over 100 integrated software modules covering clinical, administrative, and financial functions.

The certified product is a full-scope EHR, not a component or module. The CHPL certification covers an extensive set of criteria — 40+ certified criteria spanning clinical data (a-criteria), care coordination (b-criteria), clinical quality measures (c-criteria), patient portal (e-criteria), public health reporting (f-criteria), and API/FHIR access (g-criteria). The SED intended user description confirms it targets both "Ambulatory and Inpatient Licensed medical professional and staff."

The system runs on a FOSS (Free/Open Source Software) stack on Linux, using YottaDB (formerly GT.M) as the underlying database. The clinical user interface is CPRS (Computerized Patient Record System) — the same GUI used across VA hospitals — which Tenzing has extended with custom web-based applications built using the Enterprise Web Developer (EWD) framework.

### Users & Market

**Primary (and possibly only) customer:** Oroville Hospital and its affiliated clinics (approximately 15 clinics mentioned in connection with ePrescribing rollout). No other Tenzing VistA customers were identified in research. The product appears to be primarily an in-house system that was certified for regulatory compliance rather than a broadly marketed commercial product.

**End users:** Physicians, nurses, pharmacists, laboratory staff, dietary staff, and other clinical and administrative personnel at a community hospital. The system is used by both inpatient and ambulatory care providers.

**Clinical settings:** Acute care hospital (inpatient), outpatient/ambulatory clinics, laboratory, pharmacy, radiology, surgery, dietary services, and emergency care. Oroville Hospital notably added pediatric capabilities that aren't part of the original VA VistA (since the VA doesn't typically treat children).

**Market position:** Tenzing Medical is a micro-vendor in the EHR market. They do not appear to actively market the product to other hospitals. The open-source VistA ecosystem includes other organizations (WorldVistA, OSEHRA, various international implementers), but Tenzing's specific certified product appears to be used primarily at Oroville Hospital.

### Modules & Functionality

Tenzing VistA inherits VistA's comprehensive module architecture. Based on vendor materials, press releases, case studies, and VistA's known architecture, the following modules and capabilities have been documented:

**Core Clinical (confirmed in use at Oroville Hospital / Tenzing):**
- **CPRS (Computerized Patient Record System):** The primary clinical interface providing access to patient records, with tabs for cover sheet, problems, medications, orders, notes, consults, surgery, discharge summaries, labs, and reports
- **CPOE (Computerized Physician Order Entry):** Oroville Hospital was the first individual US hospital to adapt CPOE from VistA. Supports medication orders, lab orders, radiology orders, diet orders, and consult requests
- **Pharmacy (Inpatient & Outpatient):** Custom-configured pharmacy system including controlled substances tracking and drug accountability
- **ePrescribing (eRx VistA):** Custom-built module integrating with Surescripts, Newcrop, First Data Databank, and RxHub for electronic prescribing with drug-drug interaction checking, drug-allergy checking, dosage checking, formulary checking, medication history retrieval (up to 2 years via Surescripts), and generic alternatives
- **Laboratory:** Interface with Sunquest lab system; Valley Clinical Laboratory is a full-service lab offering clinical chemistry, special chemistry, microbiology, anatomic pathology, serology, hematology, urinalysis, blood banking, and cytology
- **VistA Imaging:** Document imaging and clinical image capture
- **Problem List:** Active problem tracking
- **Progress Notes / TIU (Text Integration Utilities):** Clinical documentation
- **Vital Signs:** Vital measurements documentation
- **Allergy/Adverse Reaction Tracking**
- **Consult/Request Tracking**
- **Radiology/Nuclear Medicine**
- **ADT (Admission/Discharge/Transfer)**
- **Scheduling:** Initially adopted a scheduling application from Indian Health Service; later developed a custom GUI scheduling package (won second prize in a VA Medical Appointment Scheduling Contest)
- **Dietetics**
- **Surgery**

**Custom Applications Developed by Oroville/Tenzing:**
- Real-time patient dashboard application
- Pediatric growth chart application
- Flow sheet application (basis for anesthesia, obstetrical, and infusion center flow sheets)
- Centralized bed control application
- Custom scheduling GUI

**Patient Portal:**
- HealtheMe integration (for Meaningful Use Stage II compliance)
- Currently appears to use Bridge Patient Portal (based on Oroville Hospital's current website)

**Additional VistA Modules Available (from VistA's 85+ module catalog — unclear which are active at Oroville):**
The full VistA platform includes modules for: Registration, Integrated Billing, Mental Health, Social Work, Nursing Service, Oncology, Prosthetics, Women's Health, Dental, Medicine, Engineering, Fee Basis, Integrated Patient Funds, Order Entry/Results Reporting, PCE (Patient Care Encounter), Record Tracking, Visit Tracking, Health Summary, Clinical Monitoring, Quality Assurance, Occurrence Screen, Incident Reporting, Patient Representative, and many infrastructure/utility modules.

### Data & Content

Based on documented capabilities, Tenzing VistA manages the following data:

**Clinical Data (confirmed):**
- Patient demographics and registration information
- Problem lists (active/inactive diagnoses)
- Medication lists (inpatient and outpatient prescriptions)
- Allergy and adverse reaction records
- Vital signs measurements
- Laboratory results (full clinical lab menu including chemistry, hematology, microbiology, pathology, blood bank, cytology)
- Radiology/imaging orders and results
- Clinical notes (progress notes, discharge summaries)
- Orders (medications, labs, radiology, diets, consults, procedures)
- Consult requests and tracking
- Surgical records
- Dietary/nutrition orders
- Immunization records
- Clinical images and scanned documents (VistA Imaging)
- Encounter/visit data

**Pharmacy Data (confirmed):**
- Prescription records (both inpatient and outpatient)
- Electronic prescription transmissions via Surescripts
- Drug interaction checking data
- Formulary information
- Controlled substance tracking
- Medication history (up to 2 years from external sources)

**Administrative Data (confirmed or likely based on VistA architecture):**
- ADT (admission, discharge, transfer) records
- Scheduling/appointment data
- Patient flow/bed management data
- Registration and eligibility data

**Patient Portal Data (confirmed):**
- Patient-facing health records (via Bridge Patient Portal / previously HealtheMe)

**Data Architecture:**
All data is stored in a YottaDB (MUMPS-based) database on Linux. The hospital runs a Logical Multi-Site (LMS) configuration with disaster recovery replication to a remote data center 600 miles away. The system uses VistA's traditional FileMan data dictionary structure — a hierarchical, non-relational database.

**Unclear/Unknown:**
- Whether integrated billing is actively used (VistA includes Integrated Billing module, but Oroville Hospital may use a separate billing system)
- Extent of mental health, social work, and other specialty module deployment
- Whether claims/billing data is stored within VistA or in a separate system
- What patient messaging/communication data exists beyond the patient portal
