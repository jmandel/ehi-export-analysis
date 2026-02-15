# Dexter Solutions Inc — Product Research

Researched: 2026-02-14
Developer website: http://www.dexter-solutions.com/

## Overview

Dexter Solutions Inc is a small healthcare IT company based in Warrenville, Illinois (a Chicago suburb), with approximately 28 employees and estimated revenue around $1M. The company develops and sells cloud-based EHR/EMR and practice management software targeted at small to medium-sized medical practices. Their primary product is eZDocs, a cloud-hosted EMR system, and they also offer eZBill, a medical billing/revenue cycle management service. The company also provides Remote Patient Monitoring (RPM) and Chronic Care Monitoring (CCM) services. Dexter Solutions appears to be a small, privately-held vendor with a regional presence, particularly in the Chicago area.

The CHPL metadata lists the intended user description as "Internal Medicine - Neurologist," suggesting the product was tested/certified with neurology and internal medicine workflows, though marketing materials indicate the system supports many specialties including cardiology, dermatology, and family medicine.

## Product: eZDocs

CHPL ID: 11432

### What It Is

eZDocs is a cloud-based, full-featured Electronic Medical Records (EMR) system designed for small to medium-sized medical practices. It is described as a "simple yet secured full featured cloud-based EHR" that allows physicians to manage their practice from any location and any device. The system is delivered as a multi-tenant SaaS application (hosted at *.ezdocs.app subdomains), with each practice getting its own subdomain (e.g., agha.ezdocs.app, mpmc.ezdocs.app, abcp.ezdocs.app, dhpl.ezdocs.app). The current version is 5.5 (login page shows build 5.5.9529.2992).

The product is certified for a broad set of ONC criteria (38 criteria) covering clinical data management (a)(1)-(a)(15), transitions of care (b)(1)-(b)(3), patient portal (e)(1), public health reporting (f)(1)-(f)(2), FHIR APIs (g)(7)-(g)(10), and direct messaging (h)(1). This indicates a comprehensive ambulatory EHR, not a narrow module.

### Users & Market

**Target users**: Physicians, clinical staff, and billing staff at small to medium-sized ambulatory medical practices. The SED intended user description focuses on "Internal Medicine - Neurologist."

**Supported specialties**: The vendor claims support for a wide range of specialties including internal medicine, neurology, cardiology, dermatology, and family medicine, among others.

**Customer base**: Observable client instances on ezdocs.app include at least 6+ practice tenants. One identifiable customer is American Health Centers/AHCC (ezdocs.ahccenters.com), a multi-location medical and surgical practice in the Chicagoland area — consistent with Dexter Solutions' Illinois base. The company is small (~28 employees) and appears to serve a limited number of practices, likely concentrated in the Chicago area and surrounding regions.

**Clinical settings**: Ambulatory/outpatient clinics and medical practices. No evidence of hospital, inpatient, or long-term care use.

### Modules & Functionality

Based on vendor marketing materials, the login page inspection, and third-party listings, eZDocs includes the following functionality:

**Scheduling & Patient Management**:
- Patient scheduling and appointment management
- Appointment rescheduling
- Appointment reminders (automated)
- Insurance eligibility checking

**Clinical Documentation / Encounters**:
- Patient history and past encounters access
- Current encounter management
- Practice-relevant templates (to reduce data entry)
- Medications and allergies tracking

**Order Management**:
- Order management (general)
- DME (Durable Medical Equipment) ordering with commenting (seen in login page code)
- E-prescribing capabilities

**Task Management**:
- Task management features (mentioned in product descriptions)

**Remote Patient Monitoring (RPM)**:
- RPM capabilities (visible in login page application code)
- The vendor also markets RPM services separately

**Chronic Care Management (CCM)**:
- Chronic Care Monitoring services are listed among the company's offerings

**Billing Integration**:
- eZDocs integrates with other billing software companies
- The vendor also offers eZBill, their own billing/revenue cycle management service (at 3% of collections)
- The login page code references "billing admin" and "read-only access" roles, suggesting some billing functionality may be built into or accessible from eZDocs

**Patient Portal (eZHealthInfo)**:
- Separate patient portal at ezhealthinfo.com
- Patients can view health records
- Request medication refills online
- View upcoming and past appointments
- Receive appointment notifications
- Book appointments online
- Patients must be registered by their doctor via email to access

**Government Reporting & Compliance**:
- Automatic records and reports for government reporting requirements
- Clinical quality measures support (certified for CQMs)
- Immunization registry submission (certified for (f)(1))
- Syndromic surveillance reporting (certified for (f)(2))

**Interoperability**:
- Connections to third-party registries, labs, and hospitals
- FHIR API access (certified for (g)(7)-(g)(10))
- Direct messaging (certified for (h)(1))
- C-CDA document exchange (certified for (b)(1)-(b)(3))

**Other**:
- API QR code generation (seen in login page)
- Splashtop integration for screen sharing/remote support
- 24/7 customer support

### Data & Content

Based on the certified criteria and feature descriptions, eZDocs stores and manages:

**Clinical data** (confirmed by certification criteria):
- Patient demographics (a)(5)
- Problems/conditions list (a)(5)
- Medication list (a)(5), (a)(1)
- Medication allergy list (a)(5), (a)(1)
- Clinical notes and encounter documentation
- Vital signs
- Lab results/orders (a)(2), (a)(3)
- Diagnostic imaging orders/results (a)(3)
- Drug-drug and drug-allergy interactions (a)(4)
- Implantable device list (a)(14)
- Clinical decision support data (a)(9)
- Smoking status and social history (a)(12)
- Family health history (a)(12)

**Prescription data**:
- E-prescriptions (a)(1)
- Medication history

**DME ordering data**:
- DME orders with comments (seen in application code)

**RPM/CCM data**:
- Remote patient monitoring readings (RPM module)
- Chronic care management records

**Patient portal data**:
- Patient-accessible health records
- Medication refill requests
- Appointment booking and history
- Patient notifications

**Administrative/scheduling data**:
- Appointment schedules
- Insurance eligibility information

**Reporting data**:
- Clinical quality measures
- Immunization records (for registry submission)
- Syndromic surveillance data

**Interoperability/exchange data**:
- C-CDA documents (transitions of care)
- FHIR resources
- Direct messages

**Unclear/not confirmed**:
- Whether billing data (claims, charges, payments) is stored within eZDocs itself vs. only in the separate eZBill service or third-party billing integrations. The login page references "billing admin" roles, suggesting some billing functionality may exist within eZDocs, but the marketing materials describe billing as an integration or separate service.
- The extent of lab interface data stored (the vendor mentions "connections to labs" but details are thin).
- Whether the system stores scanned documents or images beyond what's in clinical notes.
- The depth of RPM/CCM data stored (vital readings from devices, care plans, time tracking, etc.).

---

## Research Gaps

- The vendor website (dexter-solutions.com) is a Wix-based site that renders poorly for content extraction — most pages returned only JavaScript/CSS framework code rather than readable content.
- No reviews were found on G2, Capterra, or Software Advice for eZDocs.
- The emrconsultant.com listing was not reachable.
- Very limited third-party coverage or press about this vendor — consistent with its small size.
- The eZBill billing service details are sparse; it's unclear how deeply integrated it is with eZDocs or what billing data resides within the EHR itself.
- No documentation or screenshots were accessible to verify the full scope of clinical data fields beyond what's implied by certification criteria and feature descriptions.
