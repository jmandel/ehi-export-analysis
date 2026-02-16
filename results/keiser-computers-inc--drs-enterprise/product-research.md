# Keiser Computers, Inc. — Product Research

Researched: 2026-02-16
Developer website: https://www.drsdoc.com

## Overview

Keiser Computers, Inc. is a small, privately held software company founded in 1985 and based in Fort Lauderdale, Florida (6350 N. Andrew Ave, Suite 100). The company develops and sells Drs Enterprise, an ambulatory EHR system targeted at general and specialized medical practices. The company's primary contact is Jeffrey Keiser (jkeiser@drsdoc.com). The older company website at keisercomputers.com has an expired SSL certificate; the active product site is drsdoc.com.

Keiser Computers appears to be a very small vendor — likely a handful of employees — serving small to medium-sized physician practices. The company has been operating for over 40 years, though the product itself appears to date from roughly 2003 based on customer testimonials. They sell through both direct sales and channel partners; Office Management Solutions (OMS), a member of AIMSVAR (Association of Independent Medical Software Value Added Resellers), is one such reseller. There is no indication of VC funding, acquisitions, or public company status.

## Product: Drs Enterprise

CHPL IDs: 11072

### What It Is

Drs Enterprise is a certified Complete Ambulatory EHR system designed primarily for small to medium-sized medical practices. It is described as "a revolutionary new concept in electronic health records" that is built around the patient chart rather than progress notes or rigid workflow templates. The product emphasizes flexibility and customization — allowing practices to maintain their existing workflows rather than conforming to a fixed system design.

The product uses a Microsoft ribbon-style toolbar interface with drag-and-drop functionality, and supports touch screen, voice recognition, and handwriting recognition input. It integrates with Nuance DAX Copilot and Nuance Dragon Medical One for AI-powered clinical documentation and voice dictation.

The certified module appears to be the core EHR product itself. The certification covers a broad range of criteria: clinical data ((a)(1)–(a)(5), (a)(12), (a)(14)), transitions of care ((b)(1)–(b)(2)), patient portal ((e)(1)), clinical quality measures ((c)(1)), public health reporting ((f)(1)–(f)(2)), and FHIR APIs ((g)(7), (g)(9)–(g)(10)). The intended users are "general and specialized medical practices."

### Users & Market

Drs Enterprise targets small to medium-sized ambulatory practices across multiple specialties. Third-party review sites list specific target specialties including orthopedics, ophthalmology, sports medicine, and OB/GYN — though the product is positioned as general-purpose enough for any ambulatory practice.

Customer numbers are not publicly disclosed. Based on the small vendor size, limited web presence, and roughly 10 user reviews across aggregator sites, this appears to be a niche product with a modest installed base. Customer testimonials on the vendor site mention physicians who have used the system since its inception (~2003) and for over 10 years, suggesting a loyal but small customer base. Reviews on SoftwareFinder give it a 4.6/5 rating based on 10 reviews. Users praise the customization and user-friendliness; one negative review cited difficulties and limited post-sale resources.

The product is cloud-based (per SourceForge listing), with online support and in-person training offered. Custom pricing — no standard tiers are publicly listed.

### Modules & Functionality

Based on the vendor's features page (drsdoc.com/Home/Features), reseller materials (OMS), and third-party review sites, Drs Enterprise includes the following modules and capabilities:

**Clinical Documentation / Narrative Writer:**
- "Clicktation"-style clinical narrative generation
- Customizable, WYSIWYG templates that can mirror paper forms
- Support for Word documents, PDFs, photographs, and rich text files
- Integration with Nuance DAX Copilot for AI-powered encounter documentation
- Integration with Nuance Dragon Medical One for voice dictation

**Document Management:**
- Scan and categorize documents without manual typing
- Customizable chart categories, folders, and icons
- Multiple file cabinets for organizational needs
- Drag-and-drop filing technology
- QR code scanning for automated document filing (templates print with embedded QR codes)
- Unlimited discrete user fields and categories

**e-Prescribing:**
- Certified through SureScripts, GoldRx, and SafeRx
- Drug-to-drug and drug-to-allergy interaction checking
- Dosage validation
- Duplicate therapy alerts

**Telemedicine:**
- Integrated HIPAA-compliant video conferencing
- Described as "one of the least expensive telemedicine offerings in the market"

**Task / Workflow Management:**
- Outlook-style interface for task management
- Task tracking with view and completion dates
- Automatic user notifications
- Customizable phone message fields
- Priority-based task management

**Secure Messaging / Instant Messaging:**
- Internal secure text messaging between users

**Charge Capture:**
- Charges and problems posted during a visit can be automatically exported to billing systems
- Described as reducing data entry time for posting charges

**EOB Manager:**
- Explanation of Benefits processing module

**Forms Processing:**
- Auto-population of commonly used forms
- Support for Medicaid forms and hospital forms

**Integrated Fax System:**
- Streamlined fax management

**Lab Interface:**
- HL7 lab interface with dual presentation formats (discrete data and scanned images)

**Patient Portal:**
- Certified for (e)(1) View, Download, Transmit
- Listed in feature aggregations but not prominently described on the vendor site

**Scheduling:**
- Calendar-based appointment scheduling (mentioned by third-party sources; not prominently featured on vendor site)

**Practice Management Interfaces:**
- Integration with third-party PM/billing systems including MicroMD, Medical Manager, Medisoft, MedFX, and PCN
- Real-time patient and insurance data import from these systems

**Public Health Reporting:**
- Certified for immunization registry transmission ((f)(1)) and syndromic surveillance ((f)(2))

**Clinical Quality Measures:**
- Certified for CQM recording and export ((c)(1))

**Security & Compliance:**
- 128-bit encryption (HIPAA standard)
- Two-factor authentication and smart card support
- Emergency access ("break glass") protocols
- Automatic logoffs and password management
- Comprehensive audit trails
- Granular role-based permissions

### Data & Content

Based on the features and modules described above, Drs Enterprise stores and manages the following types of data:

**Clinical data** — patient charts including clinical narratives/progress notes (via the Narrative Writer/Clicktation module), customizable clinical templates, problems lists, and clinical documentation. The (a)(1)–(a)(5) certification confirms storage of CPOE, demographics, problem lists, medication lists, medication allergy lists, and clinical decision support data.

**Prescriptions** — e-prescribing data via SureScripts integration, including drug interaction and allergy checking data. The (a)(14) certification indicates implantable device list support.

**Documents** — scanned documents, PDFs, Word files, photographs, rich text files, and faxes stored in customizable folder/category structures. QR-code-based automated document filing suggests significant document volume.

**Lab results** — received via HL7 lab interface and stored in both discrete and scanned formats.

**Charges and billing codes** — captured during clinical visits via the charge capture module, then exported to external billing systems. The EOB Manager indicates storage of explanation of benefits data.

**Tasks and messages** — internal workflow tasks, phone messages, and instant messages between users.

**Forms** — auto-populated clinical and administrative forms (Medicaid, hospital forms).

**Scheduling data** — appointment scheduling data (mentioned by third-party sources).

**Patient portal data** — patient-facing data for view/download/transmit, though the portal's specific data content is not well-described by the vendor.

**Public health reports** — immunization registry and syndromic surveillance data.

**Audit trails** — comprehensive logging of system access and actions.

**Important note on billing:** Drs Enterprise does NOT appear to include a full built-in practice management or billing system. Instead, it integrates with third-party PM systems (MicroMD, Medisoft, Medical Manager, MedFX, PCN) and exports charge data to them. The charge capture module and EOB Manager handle the clinical-billing interface, but the core billing, claims submission, and accounts receivable appear to reside in external systems. This is a critical distinction for EHI export assessment — claims and financial data may not be within the scope of the Drs Enterprise product itself, though charge capture data and EOBs are.

**Information gaps:** The vendor website is fairly detailed about document management and clinical documentation but thin on specifics about the patient portal's capabilities, scheduling depth, and what exactly the "forms processing" module stores vs. generates. The product's approach to structured vs. unstructured clinical data is somewhat unclear — the emphasis on document management and customizable templates suggests a more document-centric approach than a highly structured discrete-data model, though the HL7 lab interface and e-prescribing modules clearly handle structured data.
