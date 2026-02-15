# CloudCraft, LLC — Product Research

Researched: 2026-02-15
Developer website: http://www.naiacorp.com (SSL misconfigured; actual domain appears to be naiacorp.net)

## Overview

CloudCraft, LLC is a product of NAIA Corporation, a small IT services and consulting firm founded in 1997 by Terry Lee in Birmingham, Alabama. NAIA originally focused on manufacturing/distribution ERP software ("iERP") and IT consulting for small-to-midsize businesses. The company has offices in Birmingham AL, Birmingham UK, and Dubai, with a development center in Hyderabad, India. ZoomInfo estimates 11–50 employees and under $5M in revenue. At some point NAIA expanded into healthcare IT, building "CloudCraft Software" as a cloud-hosted EHR platform. The CloudCraft product is branded separately from NAIA's other business lines and has its own website (cloudcraftsoftware.com), though all infrastructure runs on naiacorp.net domains and contact emails point to naiacorp.com/naiacorp.net.

CloudCraft appears to be a very small EHR vendor. It does not appear on industry lists of top healthcare software companies in Alabama, has no reviews on G2, Capterra, or Software Advice (the Capterra listing for "Cloudcraft" is a completely different product — an AWS diagramming tool by Datadog), and has essentially no press coverage. The only confirmed customer visible through research is Goshen Medical Center, a Federally Qualified Health Center (FQHC) with 38 service locations in eastern North Carolina, which uses CloudCraft's EHR and patient portal.

## Product: CloudCraft Software

CHPL ID: 11150 (15.04.04.3071.Clou.09.01.1.221227)
Version: 9.0
Certified: 2022-12-27

### What It Is

CloudCraft Software is described on its website as "your all-in-one solution for electronic health records, practice management, billing, and human resources." It is a cloud-hosted, web-based EHR system accessible via Google Chrome and Mozilla Firefox. The certified module appears to be the full product — there is no indication that CloudCraft Software is a component of a larger suite.

The product has a broad ONC certification covering 36 criteria, including:
- **Clinical data**: (a)(1) CPOE, (a)(2) CPOE lab, (a)(3) CPOE diagnostic imaging, (a)(4) drug-drug/drug-allergy interaction checks, (a)(5) demographics, (a)(9) clinical decision support, (a)(12) family health history, (a)(14) implantable device list
- **Transitions of care**: (b)(1) transitions of care, (b)(2) clinical information reconciliation
- **Patient access**: (e)(3) patient health information capture — but notably **not** (e)(1) view/download/transmit, suggesting the patient portal may not be part of the certified module
- **Clinical quality measures**: (c)(1)–(c)(4)
- **Public health**: (f)(1) immunization registry, (f)(5) electronic case reporting, (f)(7) syndromic surveillance
- **FHIR API**: (g)(7) application access — patient selection, (g)(9) application access — all data request, (g)(10) standardized API
- **Direct messaging**: (h)(1) direct project
- **EHI export**: (b)(10)

This is a comprehensive ambulatory EHR certification. The intended users per CHPL are "Users at a healthcare office or facility."

### Users & Market

CloudCraft appears to target small-to-midsize ambulatory practices and community health centers. The only confirmed deployment found is **Goshen Medical Center**, an FQHC in eastern North Carolina with 38 service locations. Goshen Medical Center's website links directly to the naiacorp.net patient portal for patient access to records.

The presence of a **sliding fee schedule module** (cloudcraft-slidingfee.naiacorp.net) is a strong signal that the product is designed for or commonly used by FQHCs, which are required to offer sliding fee discounts based on patient income. This aligns with the FQHC customer base.

There is no information available about total number of customers, clinicians, or sites beyond Goshen Medical Center. The vendor's extremely small web footprint, lack of third-party reviews, and minimal marketing suggest a very small customer base.

### Modules & Functionality

The CloudCraft website describes the product as covering four main areas but provides almost no detail about specific modules or features. Information is pieced together from multiple sources:

**Electronic Health Records (EHR):**
- Clinical charting and documentation (implied by broad (a) criteria certification)
- CPOE for medications, lab orders, and diagnostic imaging orders
- Drug-drug and drug-allergy interaction checking
- Clinical decision support
- Problem lists, medication lists, medication allergy lists (implied by (b)(2) reconciliation certification)
- Demographics recording
- Family health history
- Implantable device tracking
- C-CDA generation (USCDI v3 format, per the EHI export page)
- Document management — storage of scanned paper records, digital faxes, images (JPEG, GIF, TIF), Word documents
- Internal correspondence system (tasks, notes)

**Practice Management:**
- Described on the homepage but no specific features are detailed
- Scheduling is not explicitly mentioned but is typical for this category

**Billing:**
- Listed as a core module on the homepage but no specific features are described
- The sliding fee schedule module suggests income-based discount management for FQHCs

**Human Resources:**
- Listed as a core module on the homepage but no details provided; unusual for an EHR product

**Patient Portal:**
- A patient portal exists at ehrpatientportal.naiacorp.net (confirmed in use by Goshen Medical Center)
- Not certified under (e)(1) view/download/transmit, so unclear what portal capabilities are formally certified
- The (e)(3) certification suggests patients can submit health information into the system

**FHIR API:**
- FHIR R4 server (version R4-6.0.87) accessible at fhirapitest.naiacorp.net
- Supports FHIR R4 DocumentReference resources for patient export
- Compatible with SMART on FHIR apps (MyLinks, Apple Health mentioned)
- Endpoints exposed for both "CloudCraft Practice" (base) and specific customer organizations (e.g., Goshen Medical Center)

**Public Health Reporting:**
- Immunization registry reporting (f)(1)
- Electronic case reporting (f)(5)
- Syndromic surveillance reporting (f)(7)

**Clinical Quality:**
- CQM reporting capabilities (c)(1)–(c)(4)

**Direct Messaging:**
- Direct project messaging for secure health information exchange (h)(1)

### Data & Content

Based on what was found, CloudCraft stores and manages:

- **Clinical records**: Patient demographics, problem lists, medication lists, medication allergy lists, family health history, implantable device information, clinical notes, clinical orders (medications, lab, imaging) — all implied by the certified criteria
- **Documents**: C-CDA documents (USCDI v3), PDFs (including scanned paper records and digital faxes), images (JPEG, GIF, TIF), Word documents — explicitly described on the EHI export page
- **Internal correspondence**: Tasks and notes — explicitly listed on the EHI export page as part of the exportable data
- **Immunization data**: Required for (f)(1) immunization registry reporting
- **Case report data**: Required for (f)(5) electronic case reporting
- **Clinical quality measure data**: Required for CQM reporting
- **Sliding fee/financial data**: The sliding fee module suggests income-related patient financial data

**Gaps in information:**
- The website provides almost no detailed feature descriptions. The four-area description (EHR, PM, billing, HR) is the only product information on the main site.
- Billing capabilities are not described in any detail — it's unclear whether CloudCraft includes claim submission, ERA/EOB processing, charge capture, or other standard billing features, or if "billing" refers to simpler invoicing.
- Scheduling is never explicitly mentioned, though it would be expected in a practice management system.
- The "human resources" module is unusual for an EHR product and is not described at all. It's unclear what HR functionality is included (staff scheduling? credentialing? payroll?).
- Lab results management is not discussed (though CPOE for lab is certified, result handling is not explicitly described).
- E-prescribing is notably absent — no (b)(3) certification and no mention of Surescripts integration.
- No information about reporting or analytics capabilities beyond CQM reporting.
- No information about referral management, prior authorization, or other common ambulatory workflows.

---
