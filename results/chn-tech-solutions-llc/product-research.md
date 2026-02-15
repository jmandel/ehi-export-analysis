# CHN Tech Solutions LLC — Product Research

Researched: 2026-02-14
Developer website: https://chntechsolutions.com

## Overview

CHN Tech Solutions LLC is a small healthcare technology company based in the Houston, Texas area. The company develops and supports the Integrated Care EHR (ICE), a cloud-based electronic health record system built on the open-source OpenEMR platform. The company appears to be closely tied to MyCHN (Community Health Network), a Federally Qualified Health Center (FQHC) operating 19 locations across the greater Houston and Gulf Coast areas (Brazoria, Galveston, and Harris County). The ICE login portal is hosted at ic-ehr.mychn.org, and the product's feature set is heavily oriented toward FQHC workflows — including UDS reporting, FQHC facility billing, and social determinants of health screening. The contact name on the CHPL listing (Dennis Shelton) appears to have a LinkedIn profile linking him to Community Health Network.

CHN Tech Solutions appears to be a very small vendor, possibly a single-organization developer that built its EHR primarily for use at MyCHN and potentially offers it to other community health centers. There are no third-party reviews on G2, Capterra, or Software Advice, no press releases or media coverage, and no indication of a broader customer base beyond MyCHN. The vendor website is functional but sparse, typical of a small or internal-use health IT developer.

## Product: Integrated Care EHR (ICE)

CHPL ID: 11067

### What It Is

Integrated Care EHR (ICE) is a cloud-based EHR system built on top of OpenEMR, the popular open-source electronic health record platform. The login page at ic-ehr.mychn.org explicitly references OEMR (the nonprofit behind OpenEMR) and encourages installations to "Register your installation with OEMR to receive important notifications, such as security fixes and new release announcements." The product is ONC-certified (version 3, certified 2022-12-13) and is designed for ambulatory primary care settings, particularly FQHCs.

The certified module covers a moderate range of criteria: clinical data (CPOE for lab, demographics, clinical decision support, implantable device list, social determinants of health), transitions of care, clinical quality measures, patient health information capture, FHIR API access, and direct messaging. Notably absent from certification are: patient portal view-download-transmit (e)(1), e-prescribing criteria, and all public health reporting criteria (f)(1)–(f)(7) — though the vendor website describes e-prescribing and immunization reporting as product features.

The product is cloud-hosted (compatible with AWS) and requires no on-premise hardware.

### Users & Market

The primary (and possibly only significant) deployment is at MyCHN (Community Health Network), a nonprofit FQHC in the greater Houston area. MyCHN operates 19 locations and provides:
- Primary care for adults and children
- Women's health / OBGYN (including high-risk pregnancy)
- Pediatrics
- Behavioral health (psychiatry and counseling, in-person and virtual)
- Dental services
- Pharmacy services

The intended users per the CHPL listing are "Physicians, Nurses, Medical Assistants, Health Care Administrators and Staff." The login page offers English and Spanish language options, consistent with serving a diverse Houston-area patient population.

There is no evidence of other customers. The product does not appear on any major EHR review or comparison sites. No customer count, case studies, or testimonials are available beyond the MyCHN deployment.

### Modules & Functionality

Based on the vendor website (chntechsolutions.com/integrated-health-ehr-ice/) and the underlying OpenEMR platform:

**Clinical Documentation**
- SOAP note-based documentation module
- Specialty modules for: Primary Care, Pediatrics, Women's Health, Psychiatry, Therapy, and Medication Assisted Therapy (MAT)
- Disaster response module with simplified intake documentation
- Chronic care management tracking, reporting, and billing

**Screening & Assessment Tools**
- Integrated screening tools for: Social Determinants of Health (SDOH), Drug/Alcohol Abuse, Dental Care, Fall Risk, Human Trafficking, Lead Poisoning, Vision, TB, Smoking/Tobacco, Depression, and Zika Virus
- The vendor also offers a separate "SDOH Platform" and "Elevations" product for community-level social care coordination and closed-loop referrals

**Patient Engagement**
- Patient portal with secure messaging
- iOS and Android mobile applications
- Bidirectional SMS/text messaging
- Forms integration

**Billing & Financial**
- Specialized FQHC facility billing
- Traditional fee-for-service billing (customizable)
- Financial reports: payments collected by user, patient ledger, payor aging report, encounter detail with charges and collections

**E-Prescribing**
- Electronic prescribing via Allscripts ePrescribe (now VeraDigm); the login page notes VeraDigm was discontinued May 2024 and the system transitioned to NewCrop (via SureScripts)

**Lab & Imaging Interfaces**
- Interfaces with over 20 laboratories
- Radiology connectivity

**Interoperability**
- Health Information Exchange (HIE) capability
- Immunization reporting
- Bidirectional interfaces where supported
- FHIR API (documented at onc.chntechsolutions.com)
- Direct messaging (h)(1) certified
- CCD operations via FHIR

**Reporting**
- UDS (Uniform Data System) data collection and reporting — critical for FQHC compliance
- Meaningful Use / Promoting Interoperability reporting
- Patient-Centered Medical Home (PCMH) reporting
- Practice operational reports: cycle times, appointments/encounters by hour, patient no-show rates

**Scheduling**
- Inherited from OpenEMR base platform (patient scheduling is a core OpenEMR feature)
- Appointment tracking and reporting

**Infrastructure**
- Cloud-based (AWS-compatible), no on-premise hardware required
- Nightly maintenance window (11:30 PM – 1:00 AM per login page)

### Data & Content

Based on the features described above and the OpenEMR foundation, ICE stores:

- **Clinical records**: SOAP notes, encounter documentation across multiple specialties (primary care, pediatrics, women's health, psychiatry, therapy, MAT)
- **Patient demographics**: Including SDOH data (certified for (a)(5) and (a)(15))
- **Screening/assessment data**: Extensive screening tool results for SDOH, substance abuse, depression, fall risk, human trafficking, lead poisoning, vision, TB, smoking, dental, and Zika
- **Medication data**: Prescriptions and e-prescribing records (historically via VeraDigm/Allscripts, now via NewCrop/SureScripts)
- **Lab results**: From 20+ interfaced laboratories
- **Radiology/imaging orders and results**
- **Implantable device data**: Certified for (a)(14)
- **Billing/claims data**: FQHC facility billing, fee-for-service claims, payment records, patient ledgers, payor aging
- **Scheduling data**: Appointments, encounter tracking, no-show tracking
- **Patient portal communications**: Secure messages between patients and providers
- **Transitions of care documents**: CCDs, certified for (b)(1)
- **Clinical quality measure data**: Certified for (c)(1)
- **Chronic care management records**: Tracking, reporting, and billing data

**What's unclear:**
- The vendor website does not specifically mention dental EHR functionality, even though MyCHN provides dental services. It's unclear whether dental records are managed in ICE or in a separate system.
- The vendor website does not mention pharmacy management, though MyCHN operates pharmacies.
- The relationship between the core ICE product and the ancillary products (Elevations, SDOH Platform, Resource Manager, Data Warehouse, Remote Patient Monitoring) is not well-documented — it's unclear how much data flows between them or whether they share a database.

---

## Other Products in the CHN Tech Solutions Ecosystem

The vendor website lists several additional products beyond the core EHR:

- **Elevations**: A community care coordination platform for "whole-person care" — closed-loop referrals, social care funding, community partnership management. Appears to be a separate product focused on social services coordination rather than clinical EHR.
- **SDOH Platform**: Training-focused platform related to social determinants of health screening and data. Appears connected to the SDOH screening tools within ICE.
- **Remote Patient Monitoring**: Listed as a product but no details available on the website.
- **Resource Manager**: Listed as a product but no details available.
- **Data Warehouse**: Listed as a product but no details available.

The degree of integration between these products and the core Integrated Care EHR is unclear from available sources.
