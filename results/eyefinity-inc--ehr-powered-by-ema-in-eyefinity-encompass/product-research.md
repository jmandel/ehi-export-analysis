# Eyefinity, Inc. — Product Research

Researched: 2026-02-15
Developer website: http://www.eyefinity.com

## Overview

Eyefinity, Inc. is a subsidiary of VSP Vision (formerly VSP Global), the largest not-for-profit vision benefits company in the United States. Based in Rancho Cordova, California, Eyefinity provides practice management and electronic health record software specifically for the eye care industry — primarily optometry practices, but also ophthalmology. The company was created around 2000–2001, initially as a claims clearinghouse for VSP. It expanded through a series of acquisitions and partnerships, including merging with OfficeMate Software Solutions (via Marchon) in 2008 and acquiring AcuityLogic in 2010.

Eyefinity claims to be the most widely used PM and EHR solutions provider in optometry, with over 7,000 independent optometric clinical practices using its platform and solutions deployed in over 20,000 offices. Notable large customers include MyEyeDr, a major national eye care chain (their EHR login at `myeyedr.eyefinityehr.com/ema/Login.action` confirms usage). The company is the only optometric software vendor with a direct connection to VSP insurance, which is a significant market advantage. Eyefinity achieved SOC 2 Type 2 certification, described as a first for optometry software.

In 2013, Eyefinity announced a strategic technology partnership with Modernizing Medicine, Inc. (ModMed) to bring ModMed's cloud-based Electronic Medical Assistant (EMA) platform to the optometry market. This resulted in the product "Eyefinity EHR, powered by EMA" — essentially a white-labeled/customized version of ModMed's EMA adapted for optometry and integrated with Eyefinity's practice management system. This is the certified product.

In 2025, Eyefinity rebranded its flagship cloud-based products — Eyefinity EHR and Eyefinity Practice Management — under a unified brand: **Eyefinity Encompass**, positioning it as an all-in-one integrated PM and EHR platform.

## Product: EHR powered by EMA in Eyefinity Encompass

CHPL ID: 11088

### What It Is

"EHR powered by EMA in Eyefinity Encompass" is a cloud-based electronic health records system for eye care (optometry and ophthalmology) practices. The EHR component is built on Modernizing Medicine's EMA (Electronic Medical Assistant) platform — a specialty-specific, iPad-native, cloud-based EHR with an adaptive learning engine. Eyefinity has customized and branded this as "Eyefinity EHR" and integrated it tightly with its own Practice Management system. Together, under the Eyefinity Encompass brand, they form an all-in-one platform for eye care practices.

The certified module covers the EHR component (clinical documentation, CPOE, e-prescribing, patient portal, care transitions, clinical decision support, etc.) but the full product encompasses practice management, billing, scheduling, optical ordering, inventory management, patient engagement, and analytics — all of which store data that may be relevant for EHI export assessment.

The product is certified for a broad set of 2015-edition criteria including:
- **(a)(1)–(a)(5), (a)(12), (a)(14)**: CPOE for medications, labs, and imaging; drug interaction checks; demographics; problem list; medication list; medication allergy list; clinical decision support; implantable device list
- **(b)(1)–(b)(3), (b)(10)–(b)(11)**: Transitions of care (CCDA), clinical information reconciliation, EHI export, care plan
- **(c)(1)**: Clinical quality measures
- **(e)(1), (e)(3)**: Patient portal (view/download/transmit), patient health information capture
- **(f)(5)**: Electronic case reporting (public health)
- **(g)(2)–(g)(10)**: Automated numerator recording, safety-enhanced design, quality management, accessibility, consolidated CDA creation, application access (FHIR APIs)
- **(h)(1)**: Direct messaging

### Users & Market

**Target users** (from CHPL metadata): Providers, Medical Assistants (MAs), Ophthalmic Technicians, Administrators.

**Clinical settings**: Independent optometry practices (the core market), multi-location optometry groups, ophthalmology practices, and large national chains like MyEyeDr. The product scales from solo practitioners to national chains with 100+ rooms per location.

**Market position**: Eyefinity is the dominant player in the optometry PM/EHR market. Over 7,000 independent practices use the platform, with the broader Eyefinity ecosystem deployed in 20,000+ offices. Being a subsidiary of VSP Vision (the largest US vision benefits company) gives Eyefinity unique integration with VSP insurance — the only optometry software with a direct VSP connection.

**Pricing**: Subscription-based, approximately $200–$400/user/month depending on practice size.

### Modules & Functionality

Based on vendor materials, release notes, help documentation, and reviews, the Eyefinity Encompass platform includes:

**Clinical Documentation (EHR powered by EMA)**
- Eye exam documentation with customizable exam protocols/templates (per the vendor: "predefined templates that you can apply to any ocular exam... prepopulate with your preferred procedures")
- Adaptive learning engine that remembers provider charting patterns and preferences (inherited from ModMed EMA)
- Comprehensive ocular exam fields including manifest refraction, specialty contact lens parameters (SAG, Skirt, OAD, HVID), over-refraction documentation, soft and specialty contact lens prescribing
- iPad-native app with same functionality as web version for bedside/exam room use
- Auto-save for exam and demographic data
- Visit notes with version history, ability to unfinalize and edit, watermarked original vs. corrected versions
- Patient discharge status documentation (for larger ophthalmic centers: home, left against advice, other healthcare facility)
- Problem list, medication list, allergy list, medical history, ocular history, social history, family history, implantable devices
- Immunization documentation
- Refractive counseling and follow-up plan generation

**Computerized Provider Order Entry (CPOE)**
- Medication prescribing with e-prescribing via Surescripts (implied by certification)
- Lab ordering and results tracking
- Diagnostic test ordering with National Coverage Determination (NCD) warnings for Medicare non-covered tests
- IOL (intraocular lens) options tracking (Alcon, Panoptix toric variants, etc.)

**Diagnostic Equipment Integration**
- Integration with "virtually every popular equipment used in optometry" including Alcon, Bausch & Lomb, Carl Zeiss Meditec, NIDEK, Optos, and many more
- Diagnostic images accessible, reviewed, annotated, and shared from within the EHR
- OCT and visual field data pulled directly into charts

**Patient Portal**
- Secure messaging (intramail) between patients and practice staff
- Patient access to: visit notes, medications, allergies, problem list, prescriptions (eyeglass and contact lens), lab results, CCDAs, appointment history
- Pre-visit medical history forms (demographics, insurance, pharmacy, medications, allergies, past medical history, ocular history, social history, family history)
- Patient-initiated updates requiring provider approval
- Telehealth video visit capability
- Contact lens and eyeglass prescription viewing/printing with watermarks

**Practice Management (Eyefinity PM)**
- Appointment scheduling with integrated online 24/7 patient self-scheduling
- Insurance eligibility verification — including VSP-specific real-time eligibility and authorization (up to 7 days in advance)
- Claims management and billing to insurance carriers and patients
- Electronic Remittance Advice (ERA) with automatic pull into Encompass via partnerships with VSP Vision and TriZetto
- VSP claims and orders submitted automatically
- Barcode printing and scanning
- Accounting management

**Optical Orders & Inventory Management**
- Optical lab orders management with barcode-based shipping, receiving, and tracking
- Inventory management with pricing screens showing retail and discounted rates
- Integration with frames, lenses, and labs from all major manufacturers

**Patient Engagement**
- Automated appointment reminders via text and voice messages
- Recall reminders
- Two-way texting for order and appointment updates
- Electronic consent forms
- Inbound fax linking with patient DOB and MRN verification

**Coding & Compliance**
- Automatic ICD-10 and CPT code updates
- Medical coding calculator for CMS guidelines validation
- MIPS credit tracking
- Maryland-specific sensitive health information flagging
- Patient data restriction request management

**Transitions of Care**
- CCDA generation and exchange (USCDI v3 compliant per release notes)
- Clinical information reconciliation (medications, problems, allergies)
- Direct messaging (health information exchange)
- Filtered CCD option for sensitive data exclusion

**Analytics & Reporting**
- Analytics broken down by exams, patients, and insurance
- Various claims and billing reports
- Quality management system reporting

**OfficeFlow** (workflow management)
- Customizable patient statuses and timers
- Room management (supports 100+ rooms)
- Visual workflow tracking for patient progression through the practice

### Data & Content

Based on the features documented above, the product stores the following types of data:

**Clinical data** (via EHR powered by EMA): Patient demographics, insurance and pharmacy information, problem lists, medication lists (with prescribing history), allergy lists, clinical visit notes (with version history), eye exam results (refraction, visual acuity, contact lens parameters, specialty lens data), diagnostic imaging data/references (OCT, visual fields, fundus photos), immunization records, implantable device information, lab orders and results, medication orders, social history, family history, ocular history, past medical history, care plans, clinical decision support alerts, patient discharge status.

**Prescription data**: Eyeglass prescriptions, contact lens prescriptions (soft and specialty), medication prescriptions (e-prescribed), IOL specifications.

**Practice management data**: Appointments and scheduling data, insurance eligibility and authorization records (especially VSP), claims and billing data, ERA/remittance records, patient contact information, optical orders, inventory records with barcodes, accounting data.

**Patient engagement data**: Secure messages (intramail), patient portal activity, telehealth visit records, electronic consent forms, patient-submitted forms and history updates (pending provider approval), inbound faxes linked to patients.

**Transitions of care data**: CCDAs (sent and received), reconciliation records, Direct messages.

**Compliance/regulatory data**: MIPS quality measures, clinical quality measure data, sensitive health information flags, patient data restriction requests.

**Notable**: The EHI export documentation URL points to `modmed.com` (a "Data Dictionary for ModMed EMA EHI Export"), confirming that the underlying EHR data structure is ModMed's EMA. However, the full product includes Eyefinity's own practice management system, which stores scheduling, billing, claims, optical orders, inventory, and insurance data — these may or may not be covered by the ModMed-sourced EHI export. This will be a key question for Phase 2 analysis.

**Legacy products**: Eyefinity also has legacy server-based products (OfficeMate for practice management, ExamWRITER for EHR) that are distinct from the cloud-based Encompass platform. The certified product here is the cloud-based "EHR powered by EMA" — not ExamWRITER. However, some review sources conflate the two, and some practices may use a mix.
