## EHI Scope Reference: What Is and Isn't Electronic Health Information

EHI is defined at **45 CFR 171.102** as electronic protected health information (ePHI)
**to the extent it would be included in a HIPAA Designated Record Set** (45 CFR 164.501).
This is narrower than "all data in the EHR." The designated record set comprises:

1. **Medical records and billing records** about individuals
2. **Enrollment, payment, claims adjudication, and case/medical management records**
3. **Other records used to make decisions about individuals**

Two explicit statutory carve-outs: **psychotherapy notes** and **litigation compilations**
are excluded from EHI even though they may be in the designated record set.

### The practical test

> If there is a problem with this data, could it affect a patient's treatment
> or the amount a patient or insurer owes?
>
> **Yes** → it is EHI (part of the designated record set).
> **No, it only affects internal operations** → it is NOT EHI.

### What IS EHI (designated record set)

All clinical and patient-facing data used to make decisions about individuals:

- Demographics, contacts, insurance/enrollment info
- Diagnoses, problem lists, conditions
- Medications, prescriptions, medication administration records
- Lab results, diagnostic reports, imaging reports
- Vital signs, clinical observations
- Allergies and adverse reactions
- Immunization records
- Procedures, surgical records
- Clinical notes (all specialties — progress notes, H&P, discharge summaries, consults)
- Care plans, goals, referrals
- Patient-specific billing records, claims, charges, payments
- Custom/specialty clinical data (e.g., behavioral health assessments, oncology protocols,
  correctional intake screenings, dental charts — whatever the product stores about patients)
- Documents, images, and attachments that are part of the patient record
- External records incorporated into the patient's chart

### What is NOT EHI (do NOT flag these as "missing" from exports)

| Category | Why excluded |
|----------|-------------|
| **Audit logs / access logs** | Security compliance data (HIPAA Security Rule §164.312(b)), not used for patient decisions |
| **System configuration** | Technical infrastructure — database settings, user permissions, interface configs |
| **Quality metrics / aggregates** | Business analytics used for organizational improvement, not individual decisions |
| **Provider credentialing** | Records about providers (licensure, education, privileges), not about patients |
| **Peer review / performance evaluations** | Organizational quality oversight, not patient decision-making |
| **Scheduling / appointment logs** | Administrative/operational records — appointment dates, surgery schedules, telephone message pads are generally not part of the DRS even though they contain PHI. Exception: if appointment data is used to document health status or make care decisions (e.g. visit history linked to encounters), that portion may qualify. Do not flag missing appointment schedules as an EHI gap. |
| **Staff scheduling** | Operational data, no PHI |
| **Workflow queue data** | Operational process state, not clinical records |
| **Template definitions** | System configuration for form/note structure |
| **Print/fax transmission logs** | Operational delivery records |
| **De-identified data** | No longer PHI by definition (§164.514(b)) |
| **Psychotherapy notes** | Explicitly carved out of EHI (§171.102) — but note: Rx, session times, diagnoses, treatment plans for mental health ARE still EHI |
| **Litigation compilations** | Explicitly carved out of EHI (§171.102) |

### Key principle for coverage assessment

When evaluating whether an EHI export is complete, compare it against the **clinical
and billing data the product stores about patients** — not against operational or
infrastructure data. A product that exports all patient-facing clinical data, billing
records, and specialty-specific assessments but omits audit logs and system configs
is correctly scoped. A product that only exports USCDI/US Core clinical summaries
but omits billing, custom assessments, or specialty clinical data has genuine gaps.

The question is not "does the export include everything in the database?" but rather
"does the export include everything used to make decisions about patients?"
