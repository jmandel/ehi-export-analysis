# ZH Healthcare, Inc. — Product Research

Researched: 2026-02-16
Developer website: https://blueehr.com/

## Overview

ZH Healthcare, Inc. is a healthcare IT company headquartered in Bethesda, MD (formerly McLean, VA in some references), founded around 2008. The company is a major contributor to OpenEMR, the widely-used open-source EMR platform (used in 300,000+ locations in 180 countries). ZH Healthcare built its commercial platform, BlueEHR, on top of OpenEMR, extending it with proprietary modules, cloud hosting, and enterprise features. The company employs over 200 people globally, with a Global Delivery Center in Kerala, India and a subsidiary in Geneva, Switzerland.

The company has gone through several branding iterations: the original product was called BlueEHS, which was rebranded to blueEHR in January 2017 as a unified brand, and more recently (circa 2022) the broader platform was rebranded as **blueBriX** — described as "the building blocks for digital health." The blueehr.com leadership page now redirects to bluebrix.health. BlueEHR remains the name of the certified EHR module within the larger blueBriX platform ecosystem, which also includes blueTeleMed and blueConsole (a low-code/no-code application building tool).

ZH Healthcare positions itself as offering "Health IT as a Service" (HITaaS) — a cloud-based, customizable SaaS platform. Their go-to-market spans direct sales to practices and health systems, as well as a platform play targeting health IT companies and startups who build on top of their infrastructure. They serve customers in 100+ countries and claim to serve over 2 million patients. Known customers include Sanford World Clinic (rural clinics in Ghana), Medisoft East Africa Ltd, EKA Hospital Group, Memits Health IT Solutions, CarePortMD, and RIMS Medical College. The customer base skews toward smaller practices, international deployments, and organizations attracted to the customizable/open-source heritage.

## Product: BlueEHR

CHPL ID: 10797

### What It Is

BlueEHR is a cloud-based, multi-specialty electronic health record and practice management system. It is the ONC-certified EHR module within ZH Healthcare's broader blueBriX digital health platform. The certified product is BlueEHR Version 3, certified on January 19, 2022, through SLI Compliance.

The certification is comprehensive — 32 criteria covering clinical data management (a)(1)-(a)(14), transitions of care (b)(1)-(b)(2), patient portal (e)(1)/(e)(3), public health reporting (f)(1)-(f)(2), FHIR APIs (g)(7)/(g)(9)/(g)(10), and direct messaging (h)(1). This indicates a full-featured EHR, not a narrow module.

BlueEHR is built on OpenEMR and extends it significantly. The platform is described as "a truly customizable healthcare SaaS platform with infrastructure, compliance, and application layers." It is cloud-hosted (also available on-premise for some deployments) and supports web, iOS, and Android access.

### Users & Market

**Target users**: Ambulatory care professionals (per CHPL SED description), but the product also covers acute care, behavioral health, dental, and specialty care settings.

**Specialties served**: Cardiology, dentistry, ophthalmology, radiology, general practice, behavioral health, and others. The system is marketed as multi-specialty with heavy emphasis on customizability to fit any specialty workflow.

**Customer scale**: The vendor claims "thousands of healthcare providers, staff, health systems, startups, and IT companies in 100+ countries" and over 2 million patients served. The platform supports 36 languages. Notable deployments include:
- **Sanford World Clinic**: 20 rural community clinics in Ghana (2017), demonstrating acute and ambulatory care in resource-constrained settings
- **RIMS Medical College**: Academic medical institution in India
- **CarePortMD**: Kiosk-delivered telemedicine initiative
- International deployments across Africa and Asia

**End users**: Physicians, clinical staff, nurses, billing staff, practice managers, and patients (via patient portal). The platform is marketed to organizations ranging from solo practices to health systems.

### Modules & Functionality

BlueEHR is described as having **30–34 modules** (sources vary slightly) covering ambulatory care, acute care, telemedicine, and patient engagement. Based on vendor materials, press releases, review sites, and product documentation:

**Clinical / EHR Core:**
- Electronic health records with customizable clinical workflows
- Computerized Provider Order Entry (CPOE) for medications, lab, and diagnostic imaging (certified criteria (a)(1)-(a)(3))
- Drug-drug and drug-allergy interaction checking (certified (a)(4))
- Clinical decision support (certified (a)(9))
- Clinical documentation including HPI, progress notes, treatment plans
- Customizable form builder (users can create templates with checkboxes, radio buttons, text fields)
- Problem list, medication list, allergy list management
- Demographics recording (certified (a)(5))
- Immunization tracking
- Charting and document management

**E-Prescribing:**
- Electronic prescribing capabilities
- Integration with prescription networks

**Laboratory:**
- Lab orders and results management
- External lab interfaces (HL7-based)
- Lab integration noted across multiple sources; however, some reviewers noted the lab/investigation orders module was "not complete" in some evaluations

**Radiology & Imaging:**
- Radiology module
- PACS integration mentioned
- Diagnostic imaging orders (certified (a)(3))

**Pharmacy & Inventory:**
- Pharmacy module listed among core capabilities
- Inventory management (though reviewers noted this module was incomplete and "does not account for laboratory items")

**ADT (Admission, Discharge, Transfer):**
- ADT module for acute care settings
- Supports inpatient workflows

**Revenue Cycle Management / Billing:**
- Integrated billing and practice management
- Claims management and submission
- Insurance eligibility verification
- Online payments
- CPT and ICD-10 coding
- Denial management and payment posting
- Advanced RCM tools described as part of the blueBriX platform

**Scheduling:**
- Appointment scheduling and management
- Online scheduling capabilities
- Appointment reminders and patient confirmation

**Patient Portal / Patient Engagement:**
- Patient portal allowing patients to view complete medical records (certified (e)(1))
- Patient self-entry for health history, family history, current issues
- Appointment requesting
- Secure messaging between patients and care team
- View, download, and transmit health information to third parties (certified (e)(1))

**Telehealth:**
- blueTeleMed — integrated telemedicine module
- Video conferencing capabilities

**Transitions of Care:**
- C-CDA generation and consumption (certified (b)(1)-(b)(2))
- Direct messaging for secure health information exchange (certified (h)(1))
- Care coordination features

**Public Health Reporting:**
- Immunization registry reporting (certified (f)(1))
- Syndromic surveillance reporting (certified (f)(2))
- Clinical quality measure capture and export (certified (a)(12)-(a)(14), (c)(1))

**APIs & Interoperability:**
- Standardized FHIR API for patient and population services (certified (g)(9)-(g)(10))
- HL7 interface support
- APIs for connecting with diagnostic medical equipment
- Application access capabilities (certified (g)(7))

**Analytics & Reporting:**
- Data analytics and comprehensive reporting tools
- Population health features

**Other Notable Features:**
- Voice recognition functionality
- Mobile apps (iOS and Android)
- Multi-language support (36 languages)
- Low-code/no-code customization via blueConsole
- Configurable workflows per specialty

### Data & Content

Based on the evidence gathered, BlueEHR stores and manages the following types of data:

**Clinical Data (confirmed by certification and vendor materials):**
- Patient demographics
- Problem lists / diagnoses
- Medication lists and prescription history
- Allergy lists with interaction data
- Lab orders and results
- Diagnostic imaging orders
- Clinical notes (progress notes, HPI, treatment plans)
- Immunization records
- Vital signs
- Clinical quality measures
- Care plans
- C-CDA clinical summaries (transitions of care documents)

**Administrative/Financial Data (confirmed by vendor materials and reviews):**
- Appointment/scheduling data
- Billing claims and payment data
- Insurance eligibility and verification records
- CPT/ICD-10 coded encounter data
- Revenue cycle management data (claims, denials, payments)

**Patient-Generated Data (confirmed by patient portal descriptions):**
- Patient self-reported health history
- Family history entries
- Current health issues reported by patients
- Secure messages between patients and care team
- Appointment requests

**Operational Data (implied by modules described):**
- ADT records (for acute care)
- Pharmacy/inventory data (though noted as incomplete by some reviewers)
- Audit logs (certified (d)(2)-(d)(3))
- User access and authentication records

**Telehealth Data:**
- Telehealth visit records (via blueTeleMed integration)

**Interoperability/Exchange Data:**
- FHIR-based API data (patient and population level)
- Direct messaging records
- HL7 interface transaction data
- Public health reports (immunization registry, syndromic surveillance)

**Notable gaps or uncertainties:**
- The inventory management module was described as incomplete by at least one reviewer
- The lab and radiology ordering modules were noted as not fully complete in some evaluations
- It's unclear how much data from the broader blueBriX platform (blueConsole custom applications, analytics dashboards) would be considered part of the BlueEHR certified product for EHI export purposes
- The boundary between BlueEHR and blueTeleMed data is unclear — they are described as separate products within the blueBriX platform but are "integrated"

---
