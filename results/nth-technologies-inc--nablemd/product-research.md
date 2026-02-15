# Nth Technologies, Inc. — Product Research

Researched: 2026-02-14
Developer website: https://www.nablemd.com/

## Overview

Nth Technologies, Inc. is a small health IT company founded in 1999 and headquartered in Houston, Texas (12 Greenway Plaza, Suite 1100). The company has 11–50 employees and was founded after the founder's wife encountered difficulties managing a small Ob/Gyn practice, which motivated building an integrated EMR/PM solution. The company develops and sells nAbleMD, a cloud-based EHR and practice management platform, and nAble IVF, a specialized fertility clinic management system. Both operate under the "nAble" brand.

Nth Technologies positions itself as serving small to medium-sized ambulatory practices across multiple specialties. The company has a notable concentration in fertility/IVF clinics, where it reports 200+ providers, 1 million+ completed cycles, and $800M+ in payments processed. The general nAbleMD product serves a broader range of specialties. The company operates with no long-term contracts and inclusive pricing (no fees for upgrades, support, data migration, or configuration). The contact for certification matters is Fredrick Knieper (fknieper@nthtechnology.com).

## Product: nAbleMD

CHPL ID: 11118 (version 6.0c, certified 2022-12-21)

### What It Is

nAbleMD is a cloud-based, integrated electronic medical records (EMR) and practice management (PM) platform designed for ambulatory practices. It was "designed from the ground up as a web-based system" and includes native mobile apps for iPad and Android tablets, plus iPhone and Android patient portal apps. The certified product encompasses both the clinical EMR and the practice management/billing modules as a single integrated platform.

The product is certified for 38 ONC criteria spanning clinical documentation (a)(1)–(a)(14), transitions of care (b)(1)–(b)(3), patient portal (e)(1), clinical quality measures (c)(1)–(c)(4), public health reporting (f)(1), FHIR R4 APIs (g)(7)–(g)(10), and Direct messaging (h)(1). This is a broad certification footprint indicating a full-featured ambulatory EHR.

### Users & Market

nAbleMD targets small to medium-sized ambulatory practices. The vendor's website and third-party listings indicate support for the following specialties through specialty-specific modules:

- **Fertility/IVF** (primary specialty focus — separate nAble IVF product with dedicated website)
- **Obstetrics & Gynecology**
- **Family Medicine**
- **Internal Medicine**
- **Pediatrics**
- **Cardiology**
- **Gastroenterology**
- **ENT (Otolaryngology)**
- **Urology**
- **General Surgery**
- **Urgent Care**
- **Behavioral Health**

Each specialty gets customized templates, picklists, and workflows. Named customers include Houston Fertility Institute, Memorial OB-GYN, Bloom Fertility (INVO Fertility), Palm Beach Fertility, Tree of Life Fertility, Idaho Fertility Center, and Fertility Treatment Services — skewing heavily toward fertility and Ob/Gyn practices. The IVF-specific product reports 200+ providers; the total nAbleMD user base across all specialties is not publicly disclosed but appears modest given the small company size.

User reviews are sparse. SelectHub gives it a 96% user satisfaction rating based on 8 reviews. Capterra lists it but had no accessible reviews. Users highlight the integrated design and customer support as strengths; the patient portal has been criticized as less intuitive than expected.

### Modules & Functionality

Based on vendor materials (nablemd.com, nablesupport.com, nableivf.com) and third-party listings:

**Clinical EMR:**
- Patient charting and clinical documentation with specialty-specific templates
- HPI (History of Present Illness) templates
- Physical exam diagrams with annotation and color markers
- Medication and allergy documentation with interaction alerts
- e-Prescribing (integrated with NewCrop/Surescripts)
- Lab ordering and results management (LabCorp interface mentioned specifically)
- Radiology and procedure ordering
- Customizable wellness plans
- Patient analytics
- Growth charts (pediatrics)
- Physician orders that auto-generate nursing tasks
- Referral management
- Meaningful Use / Promoting Interoperability dashboard

**Practice Management & Billing:**
- Appointment scheduling with automated patient reminders
- Patient check-in (including iPad kiosk)
- Eligibility verification
- ICD-10 coding
- Charge capture with E&M codes
- Automated claims submission (clearinghouse integration)
- Revenue cycle management
- Financial, collections, and administrative reporting
- Statement generation

**Patient Portal:**
- Secure messaging between patients and providers
- Self-scheduling
- Online health history forms
- Access to medical records and lab results
- Consent form management (send, sign, track)

**Document Management:**
- Scanned chart/document management
- Photograph and image storage
- Built-in fax send/receive capabilities
- Physician signature on documents

**Communication & Interoperability:**
- Direct messaging (h)(1) via Surescripts
- FHIR R4 API (documented at nablemd.com/api_fhir/)
- Secure intra-office messaging
- Transitions of care (C-CDA) document exchange

**IVF/Fertility-Specific Features** (via nAble IVF module/product):
- Interactive cycle management with treatment plans and stimulation protocols
- Oocyte tracking from retrieval through embryo transfer
- Semen analysis documentation
- Cryostorage management (tanks, cylinders, canes) with barcode scanning
- Witnessing app for cell tracking and identification
- Embryology module with daily task management
- Donor evaluations and portal
- SART reporting support
- GAAP-compliant accrual accounting
- AWS QuickSight analytics integration
- 30+ integrations with industry partners
- KPI tracking and data analytics

**ENT-Specific Features:**
- ENT-specific picklists and templates
- Specialty exam diagrams with annotation

**Mobile Access:**
- Native iPad and Android tablet apps for clinical workflows
- iPhone and Android patient portal apps
- nAble Witness app (IVF barcode scanning)
- nAble IVF EMR mobile app

### Data & Content

Based on the feature descriptions and certification criteria, nAbleMD stores and manages:

- **Patient demographics and registration data** — implied by all clinical and PM functions
- **Clinical notes and encounter documentation** — charting, HPI, exam documentation, specialty templates
- **Problems, medications, and allergies** — certified (a)(1)–(a)(5); medication/allergy alerts mentioned
- **Medication prescriptions** — e-Prescribing via NewCrop/Surescripts
- **Lab orders and results** — lab interfaces (LabCorp), certified criteria
- **Vital signs** — certified (a)(3)
- **Immunizations** — certified (a)(14)
- **Clinical decision support data** — certified (a)(4)
- **Diagnostic images and scanned documents** — photographs, scanned charts, exam diagrams with annotations
- **Faxes** — built-in fax send/receive, stored in the system
- **Referral records** — referral management mentioned
- **Care plan / wellness plans** — customizable wellness plans feature
- **Patient portal messages** — secure messaging between patients and providers
- **Intra-office messages** — secure messaging between staff
- **Appointment/scheduling data** — scheduling module
- **Billing and claims data** — automated claims, eligibility, charge capture, E&M codes, ICD-10
- **Financial and revenue cycle data** — RCM, collections, financial reporting, statement generation
- **Consent forms** — digital consent management (especially IVF)
- **Clinical quality measure data** — certified (c)(1)–(c)(4), 13 CQM measure sets
- **Public health reporting data** — certified (f)(1) immunization reporting
- **Transitions of care documents** — C-CDA, certified (b)(1)–(b)(3)
- **Audit logs** — certified (d)(2)

For IVF practices specifically:
- **IVF cycle data** — stimulation protocols, monitoring, cycle progress, dosages, outcomes
- **Embryology records** — oocyte/embryo tracking, daily lab tasks
- **Cryostorage inventory** — frozen specimens (sperm, eggs, embryos), tank/cylinder/cane locations, barcode data
- **Semen analysis results**
- **Donor records and evaluations**
- **SART reporting data**

The mandatory disclosures page notes that "images and non-standard documentation require separate one-time fees for bulk export," which suggests that the system stores a meaningful volume of image/document data that is handled differently from structured clinical data during export.

---

## Notes

- nAbleMD and nAble IVF appear to share the same underlying platform (the IVF app connects to "nAbleMD's database" per the App Store listing) but are marketed as distinct products. The IVF product has its own dedicated website (nableivf.com) and appears to be the vendor's strongest market position.
- The company is small (11–50 employees) and appears to be a niche vendor. Research materials are limited compared to larger EHR vendors. Review data is sparse.
- The support site (nablesupport.com) reveals an "app market" structure suggesting specialty modules are add-on apps to the core platform.
- The FHIR API documentation is listed at nablemd.com/api_fhir/ but was not explored in this phase.
