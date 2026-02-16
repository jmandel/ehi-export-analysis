# MDOps Corporation — Product Research

Researched: 2026-02-16
Developer website: https://www.mdops.com/

## Overview

MDOps Corporation is a small, privately held health IT company focused on voice-controlled clinical documentation for long-term care (LTC) and post-acute care practitioners. The company's sole product, MDLog, is a cloud-based, mobile-first EHR designed primarily for physicians who round at skilled nursing facilities (SNFs), long-term care facilities, and other in-patient settings. The company appears to be a small niche vendor — the website features testimonials from individual physician practices (e.g., a geriatrics practice in Cincinnati, an Alzheimer's clinic in El Paso), and pricing is listed transparently on the website starting at $249/month per provider, suggesting a self-service sales model targeting solo practitioners and small groups. MDOps is headquartered in the US and reached out to sales at 800-349-7001.

MDOps positions MDLog as a complement to facility-level EHRs like PointClickCare and MatrixCare, which are the dominant nursing facility EHR platforms. MDLog is the physician's documentation tool that integrates with these facility systems, rather than replacing them. This is an important architectural distinction: the facility EHR holds the comprehensive patient record (medications, orders, nursing notes, assessments), while MDLog is the physician's mobile charting layer that syncs data back and forth.

## Product: MDLog

CHPL ID: 10792

### What It Is

MDLog is a cloud-based, voice-controlled clinical documentation and EHR system for long-term care physicians and nurse practitioners. The certified version is 5.0 with certification date January 17, 2022. The product is designed around an iPhone/iPad app that allows clinicians to dictate clinical notes at the bedside using speech recognition, with a web-based backend for administrative and billing functions.

The product is certified across a meaningful range of ONC criteria including: CPOE for medications (a)(1) and labs (a)(2), demographics (a)(5), implantable device list (a)(14), transitions of care (b)(1), care plan (b)(9), clinical decision support (b)(11), e-prescribing via NewCrop integration, clinical quality measures (c)(1), FHIR APIs (g)(7)/(g)(9)/(g)(10), and Direct messaging (h)(1) via EMR Direct. The mandatory disclosures page lists NewCrop and EMR Direct as required additional software.

### Users & Market

MDLog targets LTC/post-acute care practitioners — primarily physicians and nurse practitioners who round at nursing homes, SNFs, assisted living, and similar in-patient facilities. The CHPL metadata describes intended users as "Healthcare users in long term care settings." The mandatory disclosures page lists the practice setting as "Ambulatory," which reflects the practitioner's practice type rather than the facility setting.

Testimonials on the website reference:
- Dr. S. Moqueet, Syamoq Eldercare, Cincinnati, OH
- Dr. Susan Berner, Comprehensive Geriatric Care, Dayton, OH
- Radu Ciubuc, MD PA, Alzheimers and Senior Care Clinic, El Paso, TX

These suggest the customer base consists of small geriatrics, elder care, and LTC-focused physician practices. The product supports multi-facility workflows — a single provider can manage patients across multiple nursing facilities. No information was found about the total number of customers or market share. The company appears to be a small/micro vendor in the LTC niche.

### Modules & Functionality

Based on the vendor website (pricing page and LTC solutions page), MDLog offers the following modules:

**Core Clinical Documentation** ($249/month per provider):
- Mobile voice-controlled dictation of clinical notes via iPhone/iPad app
- Speech recognition with machine learning adaptation to provider voices/accents
- Admissions and discharge documentation
- Interaction checks (drug-drug interactions)
- Billing portal for charge capture
- Web-based backend interface

**Full EMR** ($299/month per provider):
- All clinical documentation features plus ONC-certified EHR capabilities
- HIPAA compliance certified
- ONC Standards certified
- CPOE for medications and labs
- Demographics management
- Implantable device list
- Care plan documentation
- Clinical decision support interventions

**PointClickCare Interface** ($100/month per provider group per facility):
- Bidirectional integration with PointClickCare facility EHR
- Imports patient demographic and clinical data (medications, lab results) from PCC
- Posts dictated clinical notes back to PCC instantly
- Automated rounding list generation from facility census

**MatrixCare Integration** (pricing not listed separately):
- Similar bidirectional integration with MatrixCare facility EHR
- Downloads patient demographic and medical information
- Posts encounter notes back to MatrixCare
- Billing information sent to biller

**ePrescribing** ($50/month per provider):
- Voice-controlled electronic prescribing via NewCrop integration
- Medication interaction checks
- Simplified mobile ePrescribe workflow

**Patient Portal (MDPortal)** ($30/month per provider):
- Patient/family/caregiver access to medical information
- Viewable/downloadable health information in CCDA format
- Secure messaging between patients and providers
- Available as soon as notes are posted

**Chronic Care Management (CCM)** ($50/month per provider, up to 2 nurses):
- Identification of chronic care patients
- Built-in timer for measuring encounter duration (for billing time-based services)
- Nurse review/documentation of periodic non-face-to-face encounters
- Provider review and sign-off via iPhone
- CCM notes integrated alongside other encounter notes

**Direct Messaging** ($250/year per user plus setup):
- Encrypted Direct messaging via EMR Direct
- Care coordination across healthcare systems
- Transitions of care document exchange

**Clinical Quality Measures / PQRS Reporting**:
- CQM recording and export (certified for CMS75, CMS117, CMS122, CMS129, CMS147, CMS165)
- Prompts during documentation for quality measure data capture
- Integration with CMS-qualified registry for submission

**ACO Data Sharing**:
- Automated sharing of patient data with LTC ACO (third-party organization)
- Support for quality measures like HbA1c, depression screening, blood pressure

**Wound Care Documentation** (described in marketing but pricing not found):
- Specialized note templates for wound assessments
- Wound care progress and consult notes

### Data & Content

Based on the feature descriptions and integrations documented on the vendor website, MDLog stores or manages the following types of data:

**Clinical Notes**: The core of MDLog — dictated encounter notes, progress notes, consult notes, wound care notes, CCM encounter notes, admission and discharge documentation. These are the primary data objects.

**Patient Demographics**: Name, contact info, facility assignment, and demographic data (certified for (a)(5)). Patients can be imported via CSV from billing systems or synced from PointClickCare/MatrixCare.

**Medication Data**: Drug orders via CPOE (a)(1), e-prescribing history via NewCrop, medication interaction check records.

**Lab Orders**: CPOE for laboratory (a)(2), lab results imported from facility EHR integrations.

**Care Plans**: Certified for (b)(9) care plan documentation.

**Implantable Device List**: Certified for (a)(14).

**Billing/Charges**: Charge capture at point of care, billing submissions to facilities. The pricing page mentions "Billing Portal" as part of the basic package. However, MDLog does not appear to be a full practice management/billing system — it captures charges and submits them to facility billers or external billing systems.

**Patient Portal Data**: Messages between patients/families and providers, health information shared via MDPortal in CCDA format.

**Clinical Quality Measure Data**: Quality measure reporting data for CMS measures.

**Audit Data**: Certified for audit events (d)(2), audit reports (d)(3), and amendments (d)(4).

**Transitions of Care Documents**: C-CDA documents for care transitions (b)(1), consolidated CDA creation (g)(6).

**FHIR API Data**: Patient data exposed via standardized FHIR APIs (g)(10)).

**Notable gaps or uncertainties**:
- MDLog does not appear to store comprehensive facility-level nursing data (vitals, nursing assessments, MDS data) — that stays in the facility EHR (PointClickCare/MatrixCare). MDLog is the physician's charting layer.
- No mention of imaging or radiology data.
- No mention of scheduling or appointment management.
- The billing functionality appears to be charge capture and submission, not full claims processing or accounts receivable management.
- The website doesn't mention allergy management specifically, though it would likely be part of the medication management workflow.

---
