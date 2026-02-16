# Infinx Solutions, LLC — Product Research

Researched: 2026-02-16
Developer website: https://www.infinx.com/

## Overview

Infinx Solutions, LLC is the CHPL-listed developer for "Infinx EHR," but the product's lineage is complex and involves multiple acquisitions. Infinx Healthcare (founded 2012, headquartered in Cupertino, CA / Spring, TX) is primarily an AI-powered revenue cycle management (RCM) and patient access solutions company — not an EHR vendor. The certified EHR product traces back to **iMed Software Corp** (founded 2002 in Louisiana), which built **iMedEMR**, a cloud-based ambulatory EHR and practice management system.

**Acquisition chain:**
1. **iMed Software Corp** built iMedEMR (certified by Drummond Group).
2. **i3 Verticals (NASDAQ: IIIV)** acquired iMed Software on April 30, 2022. The product was rebranded as **i3Med** and became part of i3 Verticals Healthcare's broader platform alongside their existing billing products (HPlusPro/Healthpac).
3. **Infinx Healthcare** acquired i3 Verticals' entire Healthcare Revenue Cycle Management business in May 2025 for $96 million. This acquisition brought the EHR product (and its ONC certification) under Infinx's umbrella.

The CHPL product number for v5.3 (`15.04.04.2621.iMed.53.02.1.241219`) still contains "iMed" in the identifier, confirming the product's origin. The v5.4 listing (`15.04.04.2621.Infi.54.03.1.260128`) has transitioned to "Infi," reflecting the rebrand to Infinx EHR.

Infinx's core business (infinx.com) focuses on AI-driven prior authorization, eligibility verification, claims management, and denial management — not clinical EHR functionality. The EHR product appears to be a secondary/inherited asset from the i3 Verticals acquisition rather than Infinx's core offering. The mandatory disclosures URL points to i3verticals.com/ehr-certification, further confirming the product's i3 Verticals origins (though this page returned a 404 at the time of research).

## Product: Infinx EHR (formerly iMedEMR / i3Med)

CHPL IDs: 11554 (v5.3, certified 2024-12-19), 11759 (v5.4, certified 2026-01-28)

### What It Is

Infinx EHR is a **cloud-based ambulatory electronic health records and practice management system** originally built by iMed Software Corp. It is a fully integrated EHR + PM solution designed for ambulatory medical organizations, providing clinical documentation, practice management, scheduling, billing, and patient engagement in a single platform. The CHPL metadata indicates intended users are "Nurses, Doctors, Administrative" staff.

The product is certified for a substantial set of ONC criteria including:
- **Clinical data**: (a)(2) CPOE for medications, (a)(3) CPOE for diagnostic imaging, (a)(5) demographics, (a)(12) family health history, (a)(14) implantable device list
- **Transitions of care**: (b)(1) and (b)(2) for clinical information exchange via C-CDA
- **Patient portal**: (e)(1) view, download, transmit
- **Public health reporting**: (f)(3) electronic case reporting, and (f)(5) electronic reporting for cancer registries (v5.4 only)
- **FHIR/API access**: (g)(7)-(g)(10) for standardized API access
- **Clinical quality**: (c)(1) clinical quality measures

### Users & Market

**Target users**: Primary care physicians, specialists in multi-disciplinary ambulatory practices, nurses, and administrative/billing staff. The platform is described as suitable for organizations of all sizes, from single-provider practices to large multi-site provider groups.

**Specialties**: Primarily ambulatory/outpatient. i3 Verticals Healthcare (the prior owner) served a broader range including anesthesiology, behavioral health, radiology, pathology, emergency rooms, and laboratories — though not all these specialties necessarily used the EHR module (some used billing-only products like HPlusPro).

**Market position**: Small/niche vendor. 360Quadrants ranked iMedEMR 123rd in the EHR software category with annual revenue below $10 million. The product had very few public reviews (about 10 across review sites). The acquisition by Infinx ($96M for the entire healthcare RCM business, not just the EHR) brought it into a larger organization, but the EHR is clearly a minor component of Infinx's overall business, which is focused on RCM/prior authorization AI.

**Notable integrations mentioned in reviews**: Advanced MD, DrFirst (e-prescribing), Athenahealth, Duxware, Meditech, Labcorp, Boston Heart Diagnostics, Allscripts, CGM LABDAQ, Nexus EHR, Polytech LIS.

### Modules & Functionality

Based on vendor materials, review sites, and i3 Verticals' product pages:

**Electronic Health Records / Clinical Documentation:**
- Patient charting with medical history, personal details, allergies, medications (softwarefinder.com, findemr.com)
- Clinical notes and encounter documentation
- Single-screen patient view with "intelligent scheduling technology" (360quadrants.com)
- Family health history recording (implied by (a)(12) certification)
- Implantable device list (implied by (a)(14) certification)

**Computerized Provider Order Entry (CPOE):**
- Medication ordering (certified for (a)(2))
- Diagnostic imaging ordering (certified for (a)(3))

**E-Prescribing:**
- Electronic prescribing with DrFirst integration (findemr.com, softwarefinder.com)

**Lab & Test Management:**
- Lab ordering and results management
- Integrations with Labcorp, Boston Heart Diagnostics, CGM LABDAQ, Polytech LIS (findemr.com, sourceforge.net)

**Document Management:**
- Digital document storage for scanned letters, reports, X-rays, dictation audio, typed letters, and lab results (360quadrants.com)
- Microsoft Word and OpenOffice integration for template-based documentation (360quadrants.com)

**Scheduling & Registration:**
- Appointment management with scheduling tools
- Online patient registration — patients can provide demographics and insurance information before visits or via kiosk/tablet (i3verticals.com clinical operations page)
- Appointment reminders via email and text with add-to-calendar links (i3verticals.com)

**Billing & Revenue Cycle Management:**
- Integrated billing and RCM functionality
- Electronic superbill and E&M coding (search results from multiple review sites)
- Claims processing
- Insurance eligibility verification
- Fee schedules and accounts receivable management

**Patient Portal:**
- Secure patient access to medical and administrative data (i3verticals.com patient engagement page)
- Lab results viewing
- Secure messaging between patients and providers
- Ability for providers to post materials and information to the portal from encounters

**Clinical Decision Support & Quality:**
- Population health management tools with predictive analytics (findemr.com)
- Dashboard showing patients due for screenings with reminder campaigns (search results)
- Automated data capture for MIPS quality reporting (findemr.com)
- Advanced Payment Model (APM) evaluation modules (findemr.com — described as a distinguishing feature)

**Transitions of Care:**
- Secure Direct Messaging for exchanging patient health information with other providers (i3verticals.com)
- C-CDA document exchange (implied by (b)(1) and (b)(2) certification)
- Legacy EHR/PM data migration via CCD format (i3verticals.com)

**Reporting & Analytics:**
- Custom reporting and data mining capabilities
- Dashboard analytics for monitoring operations
- Clinical quality measure reporting

**Messaging & Task Management:**
- Internal messaging and task management between staff (softwarefinder.com)

**Telemedicine:**
- Mobile app and telemedicine functionality mentioned (findemr.com)

**Multi-Site Coordination:**
- Central platform for consultants and physicians to coordinate multiple sites, practices, and staff (360quadrants.com)

### Data & Content

Based on the certified criteria and described features, the product manages:

- **Patient demographics** — certified for (a)(5), plus online registration collects demographics and insurance info
- **Clinical encounter notes** — core EHR charting functionality
- **Medication lists and prescriptions** — e-prescribing with DrFirst integration, CPOE for medications
- **Allergy lists** — described in multiple review sites as core patient data
- **Medical history** — patient medical history management described
- **Family health history** — certified for (a)(12)
- **Implantable device list** — certified for (a)(14)
- **Lab orders and results** — lab/test management module with Labcorp and other integrations
- **Diagnostic imaging orders** — CPOE for diagnostic imaging certified
- **Scanned documents** — document management stores X-rays, letters, reports, dictation audio, lab results
- **Patient portal messages** — secure messaging between patients and providers
- **Scheduling data** — appointment scheduling and reminders
- **Billing/claims data** — integrated RCM with superbill, claims, eligibility verification
- **Clinical quality measure data** — MIPS reporting with automated data capture
- **Population health data** — screening queues, reminder campaigns, analytics
- **Transition of care documents** — C-CDA documents via Direct messaging
- **Task/messaging data** — internal staff messaging and task management

**Gaps in information**: The vendor's own website (infinx.com) contains zero information about the EHR product — it only describes RCM/prior authorization solutions. The i3verticals.com/ehr-certification page returned 404 at time of research. The i3verticalshealthcare.com site returned 403. Most detailed information came from third-party review sites and cached descriptions from i3 Verticals' now-inaccessible product pages. It's unclear how actively developed the EHR module is under Infinx's ownership versus the RCM components that were the primary driver of the $96M acquisition.

---

## Product Ecosystem & Business Context

**i3 Verticals Healthcare** (prior to Infinx acquisition) offered a broader suite:
- **HPlusPro** (from Healthpac Computer Systems, founded 1981): A medical billing and practice management solution — primarily billing/claims, not clinical EHR. This was the more established product. Starting at $275/user/month.
- **i3Med / iMedEMR**: The clinical EHR component (the certified product).
- **Evolution Scheduling**: Real-time physician schedule management.
- **Dashboard Analytics**: Revenue cycle monitoring and reporting.
- **Patient Portal**: Integrated with the EHR.
- **vantagehealth.ai**: AI-powered analytics (partnership/integration mentioned on i3verticalshealthcare.com).

The combined platform served multi-location medical practices, laboratories, hospital-based physicians, radiology imaging centers, and medical billing companies. The billing products appear to have a larger footprint than the EHR component.

Under **Infinx** ownership (post-May 2025), the strategic focus is clearly on AI-powered RCM — the EHR product is inherited rather than core to Infinx's mission. The product has been rebranded from i3Med to "Infinx EHR" on the CHPL listing, but Infinx's website makes no mention of an EHR product.
