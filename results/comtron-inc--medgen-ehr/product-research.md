# Comtron Inc. — Product Research

Researched: 2026-02-14
Developer website: http://www.medgenehr.com/

## Overview

Comtron Inc. (doing business as Comtron USA) is a healthcare software company founded in 1987 and based in Great Neck, New York. The company develops Medgen EHR and LABGEN LIS (Laboratory Information System), along with revenue cycle management (RCM) services. In August 2024, MEDFAR Clinical Solutions — a Canadian EMR company that develops the MYLE Integrated Care Platform (described as the fastest-growing EMR in Canada) — announced the successful integration of Comtron, marking MEDFAR's entry into the U.S. primary care market. The Medgen EHR website now carries MEDFAR branding, and the About page describes the combined entity as serving "over 15,000 providers and supporting 20 million patient interactions each year."

Comtron/MEDFAR targets ambulatory physician practices across multiple specialties, with particular emphasis on two niche markets: **addiction medicine / opioid treatment programs** (OTPs) and **OB/GYN practices**. The company also offers specialty-specific templates for behavioral health, cardiology, gastroenterology, internal medicine, psychiatry, podiatry, pediatrics, pulmonary, and sleep medicine. The primary contact listed on CHPL is David DeBlasio (deblasio@comtronusa.com). The company is small — with only 3 reviews on Capterra and limited third-party analyst coverage, it appears to be a niche vendor rather than a major market player.

## Product: Medgen EHR

CHPL ID: 10986 (Version 9, certified 2022-09-15)

### What It Is

Medgen EHR is a cloud-based, ONC-certified electronic health record system with integrated billing and practice management. It is certified for 35+ criteria spanning clinical data management (a)(1)–(a)(5), (a)(12), (a)(14); transitions of care (b)(1)–(b)(3); patient portal/view-download-transmit (e)(1); public health reporting (f)(1), (f)(2), (f)(5), (f)(7); and FHIR API access (g)(10). The SED intended user description is "Healthcare Prescribers, Nurses & Configuration Analysts."

The certified module appears to encompass the full product — Medgen EHR is not a component of a larger system. However, Comtron also produces LABGEN LIS as a separate but integrable product, and offers RCM services that work alongside the EHR. Post-acquisition, MEDFAR's MYLE platform is a separate Canadian EMR product; the two products are distinct.

### Users & Market

Medgen EHR targets ambulatory physician practices. Based on vendor materials and third-party listings, the primary user settings include:

- **Opioid Treatment Programs (OTPs) / Substance abuse centers** — a major focus area with deep specialty features for methadone and buprenorphine dispensing
- **OB/GYN practices** — with dedicated pregnancy monitoring and antepartum/postpartum workflows
- **General ambulatory clinics** — internal medicine, pediatrics, cardiology, gastroenterology, psychiatry, behavioral health, podiatry, pulmonary, and sleep medicine

Day-to-day users include physicians, nurses, counselors (in addiction medicine settings), billing staff, and practice managers. The MEDFAR About page claims over 15,000 providers across the combined Comtron/MEDFAR entity, though it's unclear how many are Medgen vs. MYLE users. No notable large-system deployments or case studies were found. On Capterra, the product has only 3 reviews (rating: 3.7/5), suggesting a small installed base in the U.S.

### Modules & Functionality

Based on vendor website pages, third-party listings, and review sites, Medgen EHR includes the following modules and capabilities:

**Core Clinical EHR:**
- Clinical documentation with customizable templates per specialty
- Problem lists, medication lists, allergies (implied by (a)(1)–(a)(5) certification)
- Mobile app with Nuance-powered voice dictation for documentation
- Disease management workflows with patient compliance tracking
- CPOE (computerized provider order entry) — implied by (a)(1)–(a)(3) certification
- Clinical decision support — implied by (a)(14) certification
- Drug interaction checking — implied by (a)(4) certification

**E-Prescribing:**
- Electronic prescribing including controlled substances (EPCS)
- Pharmacy refill request management

**Patient Portal:**
- Web-based patient portal for viewing charts and lab results
- Secure electronic messaging with patients
- Appointment reminders (vendor page mentions "choice of modality")

**Scheduling:**
- Full patient and provider scheduling (up to 9 provider view simultaneously)
- Wait list management
- Procedure/surgical scheduling
- Group meeting scheduling (for addiction medicine)
- Real-time scheduling analytics

**Billing & Practice Management:**
- Integrated medical billing with EDI electronic claim submission
- Automated charge capture at point of care
- Electronic payment reconciliation
- Patient invoice generation
- Instant insurance eligibility verification
- Referral authorization tracking

**Reporting & Analytics:**
- Business intelligence reporting (payer mix, net receipts, gross charges)
- Provider productivity reporting
- Charge capture and reconciliation reports
- PQRS/MIPS quality reporting
- Meaningful Use reporting

**Document Management:**
- Integrated document scanning (MedScan)
- Complete audit trails
- Internal secure messaging and e-fax (message center)

**Lab & Imaging Integration:**
- Lab interfaces (can connect to multiple labs simultaneously)
- Radiology interfaces
- HIE (Health Information Exchange) interfaces
- Ultrasound DICOM interface (for OB/GYN)
- Lab result tracking and import

**Public Health Reporting:**
- Immunization registry reporting — (f)(1)
- Syndromic surveillance — (f)(2)
- Cancer case reporting — (f)(5)
- Public health clinical registry — (f)(7)

**Transitions of Care:**
- C-CDA document generation and consumption — (b)(1)–(b)(3)

**Addiction Medicine Specialty Module:**
- Controlled substance inventory management (methadone, buprenorphine)
- Dispensing pump interfaces with automated checks and balances
- Drug screening panels
- Lot number and bottle tracking
- Spillage and residual amount tracking
- Patient dosing records
- Service plans with alerts and bio-psychosocial assessments
- Counselor and specialist personalized dashboards
- Incident management
- Discharge coding with CPT linkage
- Pre-populated release authorization templates
- Case load activity alerts

**OB/GYN Specialty Module:**
- Electronic antepartum and postpartum forms
- Pregnancy progress tracking with per-visit documentation
- Estimated fetal weight (EFW) calculators (Hadlock, Williams, Brenner, Shepard)
- EFW graphs/visualization
- EDD (estimated due date) calculator
- Automated care plans for high-risk pregnancies
- Pre-visit OB questionnaires (English and Spanish)
- Ultrasound DICOM integration and report generation
- Patient education based on potential complications

**Telemedicine:**
- The vendor website lists telemedicine capabilities, though one third-party article (iFax) stated it lacks telehealth. The EMR Industry listing confirms telemedicine functionality.

### Data & Content

Based on the features described above, Medgen EHR stores and manages:

- **Clinical records**: Patient demographics, problem lists, medication lists, allergy lists, vital signs, clinical notes (with voice dictation), clinical assessments, care plans, and clinical decision support alerts
- **Orders & results**: Lab orders, radiology orders, lab results, imaging results (including DICOM ultrasound images for OB/GYN)
- **Prescriptions**: Electronic prescriptions including controlled substances, pharmacy refill requests, drug interaction data
- **Scheduling data**: Appointments, wait lists, procedure schedules, group session schedules
- **Billing & financial data**: Claims, charges, payments, insurance eligibility records, EDI transactions, invoices, referral authorizations, CPT-coded procedures
- **Documents**: Scanned documents (MedScan), faxes, clinical forms, consent/authorization templates
- **Patient portal data**: Patient-facing messages, portal access records, appointment reminders
- **Addiction medicine data**: Controlled substance inventory (lot numbers, bottle volumes, dispensing records, spillage), drug screening results, dosing records, service plans, incident reports, bio-psychosocial assessments, counselor notes, discharge records
- **OB/GYN data**: Antepartum/postpartum records, pregnancy progress notes, EFW calculations, EDD records, ultrasound reports, high-risk pregnancy care plans, OB questionnaires
- **Public health data**: Immunization records, syndromic surveillance data, cancer case reports
- **Transitions of care**: C-CDA documents (sent and received)
- **Audit data**: Complete audit trails per the vendor website
- **Internal communications**: Secure messages, faxes via message center

The billing and practice management features are described as fully integrated into the EHR, not as a separate product. LABGEN LIS is a separate product with its own interfaces but does integrate with Medgen EHR for result delivery. Revenue cycle management services are offered as a service layer on top of the billing module.

---

## Related Product: LABGEN LIS

LABGEN LIS is a separate Laboratory Information System product from Comtron/MEDFAR. It is not part of the Medgen EHR certification but is marketed alongside it and integrates with it. LABGEN includes physician, sales rep, and patient portals; interfaces with lab analyzers; and supports clinical, molecular, and pathology testing modules. It has its own RCM billing portal. LABGEN is relevant context because lab data may flow between LABGEN and Medgen EHR, but the EHI export obligation falls on the certified Medgen EHR product, not on LABGEN separately.

## Research Gaps

- **Customer count**: The "15,000 providers" figure is for the combined MEDFAR/Comtron entity across the U.S. and Canada; the Medgen-specific U.S. install base is unclear.
- **Telehealth**: Conflicting information on whether telemedicine is included (vendor says yes, one third-party says no).
- **Behavioral health depth**: While behavioral health is listed as a supported specialty, the vendor doesn't describe behavioral-health-specific features as deeply as addiction medicine or OB/GYN. It's unclear whether there are dedicated behavioral health assessment tools or just general templates.
- **No KLAS or Definitive Healthcare coverage found** — consistent with this being a small/niche vendor.
- **Pricing**: Not publicly available; one review complained about $250/month to access old records after cancellation.
