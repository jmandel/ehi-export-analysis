#!/usr/bin/env python3
"""Parse AuroraEHR (b)(10) PDF data dictionary into structured JSON."""

import json
import re

with open("pdf-text.txt", "r") as f:
    text = f.read()

# Define entities manually based on careful reading of the PDF
entities = []

def add_entity(name, file_name, format_type, category, fields):
    entities.append({
        "name": name,
        "file_name": file_name,
        "format": format_type,
        "category": category,
        "field_count": len(fields),
        "fields": fields
    })

def f(name, description, value_set=None):
    """Create a field dict."""
    entry = {"name": name, "description": description, "has_description": bool(description.strip())}
    if value_set:
        entry["value_set"] = value_set
    return entry

# 1. Account Data (report) - PDF
add_entity("Account Data", "AccountData.pdf", "PDF", "Demographics / Account", [
    f("Account Information", "Full name, DOB, SS#, Address, contact information, ethnicity, language, and employment status"),
    f("Services", "Practice-specific classifications attributed to the patient"),
    f("Associated Providers/Lawyers", "The list of associated providers and lawyers"),
    f("Billing information", "Account balances and personal statements"),
    f("Clinical Information", "Diagnoses, history of accident/injury, dates of illness, admission, discharge, disability status, and/or return to work"),
    f("Overrides", "Information that overrides default handling of this patient in AuroraEHR. Additionally, contains patient's location, pharmacy, and rounds/census information."),
    f("Audit Details", "History of information changes"),
    f("Emergency Contact", "Information about the contact designated as an emergency contact"),
    f("Account Contacts", "Contact information about the people who are important factors in a patient's care."),
    f("All Account Payors", "The list of payors attached to the patient's account"),
    f("Account Employers", "The list of patient's employers"),
    f("Charges/Payments", "All charges and payments of an account"),
])

# 2. Charges.csv
add_entity("Charges", "Charges.csv", "CSV", "Billing", [
    f("PRACTICE", "Practice name"),
    f("ACCOUNT NO", "Unique ID of the patient in AuroraEHR"),
    f("FIRST NAME", "Patient's first name"),
    f("LAST NAME", "Patient's last name"),
    f("SERVICE DT", "Date of service"),
    f("PROVIDER", "Provider code in AuroraEHR and name"),
    f("LOCATION", "Location code in AuroraEHR and name"),
    f("DIAG 1", "Diagnosis code (ICD10)"),
    f("DIAG 2", "Diagnosis code (ICD10)"),
    f("DIAG 3", "Diagnosis code (ICD10)"),
    f("DIAG 4", "Diagnosis code (ICD10)"),
    f("PROCEDURE", "Procedure code for billing (usually CPT)"),
    f("QUANTITY", "The number of times this procedure was billed for this service date."),
    f("CHARGE AMT", "Amount charged"),
    f("REF PROVIDER", "Referring provider's code in AuroraEHR and name"),
    f("FIRST PAYOR", "Primary payor name"),
    f("RELATIVE VALUE", "Number of RVUs"),
    f("REF PROVIDER 2", "Second referring provider's code in AuroraEHR and name"),
    f("OTHER PROVIDER", "Other provider's code in AuroraEHR and name"),
    f("MODIFIERS", "The list of procedure modifiers"),
    f("CLAIM", "Claim number"),
    f("AGE", "Age of the patient as of the charge's service date"),
    f("STATUS", "Status of the charge", ["A - Active", "I - Inactive", "J - On hold when due from personal", "H - On hold"]),
    f("DOCUMENT NBR", "Document number in the system"),
    f("ZIP CODE", "The patient's zip code"),
    f("CASH", "The total amount paid thus far: includes payments and refunds"),
    f("CREDITS", "The total amount of non-cash payments such as contractual allowances and courtesies"),
    f("INTEREST", "The total amount of interest accumulated"),
    f("BALANCE", "The remaining balance on the charge"),
    f("AUTH", "The reference or authorization number on the charge"),
])

# 3. Payments.csv
add_entity("Payments", "Payments.csv", "CSV", "Billing", [
    f("ACCOUNT NO", "Unique ID of the patient in AuroraEHR"),
    f("CLAIM", "Claim number against which the payment was made"),
    f("SERVICE DATE", "Date of service of the charge"),
    f("PROCEDURE", "Procedure code for billing (usually CPT) of the charge"),
    f("DESCRIPTION", "Procedure description of the charge"),
    f("DIVISION", "Division code from the charge"),
    f("LOCATION", "Location's code in AuroraEHR and name, from the charge"),
    f("PROVIDER", "Provider's code in AuroraEHR and name, from the charge"),
    f("DEPOSIT DT", "Date of deposit"),
    f("FIN CLASS", "Financial class of the payment's payor"),
    f("REPT GRP", "Report group of the payment's payor"),
    f("PAYOR GRP", "Report group of the payment's payor"),
    f("PAYOR", "Payor code of the payment's payor"),
    f("REMIT TYPE", "Code and explanation of the remit type"),
    f("REMIT", "Explanation of the remit type"),
    f("PAY AMOUNT", "Amount of the payment, including cash and non-cash payments."),
    f("INT AMOUNT", "Amount of interest"),
    f("DOCUMENT", "Document number, often the check number"),
    f("NOTE", "Note text, if any"),
    f("ENTRY DT", "Date of entry"),
    f("USER ID", "ID of the user who created the entry"),
    f("STATUS", "Payment status", ["A - Active", "I - Inactive", "H - On hold"]),
])

# 4. ChargeTransactions.csv
add_entity("Charge Transactions", "ChargeTransactions.csv", "CSV", "Billing", [
    f("ACCOUNT NO", "Unique ID of the patient in AuroraEHR"),
    f("CLAIM", "Claim number"),
    f("TRANS DT", "Date of the transaction. Formatted as MM/dd/yyyy"),
    f("TRANS TM", "Time of the transaction. Formatted as HH:mm:ss:mmm"),
    f("PAYOR", "Payor's code in AuroraEHR and name"),
    f("DESCRIPTION", "Description of the transaction"),
    f("PAYOR FROM", "For billing transactions, the name of the payor involved"),
    f("REASON", "The description or reason that the transaction was created"),
    f("FORM", "For billing transactions, the billing form used"),
    f("RUN NO", "For billing transactions, the run number"),
    f("ENTRY DT", "Date of entry. Formatted as MM/dd/yyyy"),
    f("STATUS", "The status of the charge as of the transaction's date/time.", ["A - Active", "I - Inactive", "J - hold when due from personal", "H - hold"]),
])

# 5. AccountNotes.csv
add_entity("Account Notes", "AccountNotes.csv", "CSV", "Notes / Instructions", [
    f("Account#", "Unique ID of the patient in AuroraEHR"),
    f("Note Type", "The note's type or category.", ["Billing", "Family Display", "Medical", "Surgery", "Important"]),
    f("Priority", "Whether the note is marked as important"),
    f("Text", "Text of the note"),
    f("Date Record was Created", "The date the record was created. Formatted MM/dd/yyyy."),
])

# 6. ClinicalInstructions.csv
add_entity("Clinical Instructions", "ClinicalInstructions.csv", "CSV", "Notes / Instructions", [
    f("Account#", "Unique ID of the patient in AuroraEHR"),
    f("Accession#", "The unique ID of the appointment for which these instructions are to be used."),
    f("For Phase", "The phase of the appointment where the instructions should be used."),
    f("Instruction text", "Text of the instruction"),
    f("Date Record was Created", "The date the record was created. Formatted MM/dd/yyyy."),
])

# 7. ClinicalProgressNotes.csv
add_entity("Clinical Progress Notes", "ClinicalProgressNotes.csv", "CSV", "Notes / Instructions", [
    f("Account#", "Unique ID of the patient in AuroraEHR"),
    f("Accession#", "The unique ID of the appointment for which these notes were entered."),
    f("Is an Amendment?", "Indicates whether this note is an amendment for a note entered earlier"),
    f("Amendment Source", "Source of the new information, if not AuroraEHR"),
    f("Primary Signature", "Signature of the user, stating that this note is complete."),
    f("Primary Signature Signed Date", "Date of the signature. Formatted MM/dd/yyyy"),
    f("Primary Signature Signed Time", "Time of the signature. Formatted hh:mm:ss am"),
    f("2nd Signature", "Secondary signature. Needed for certain note types."),
    f("2nd Signature Signed Date", "Date of the second signature. Formatted MM/dd/yyyy"),
    f("2nd Signature Signed Time", "Time of the second signature. Formatted hh:mm:ss am"),
    f("Description", "A brief description of the note type or purpose."),
    f("Progress Note", "The note text itself"),
])

# 8. Appointments.csv
add_entity("Appointments", "Appointments.csv", "CSV", "Encounters", [
    f("ACCOUNT NO", "Unique ID of the patient in AuroraEHR"),
    f("APPT_DATE", "Date of the appointment. Formatted MM/dd/yyyy"),
    f("APPT_TIME", "Time of the appointment. Formatted hh:mm am"),
    f("APPT_MINUTES", "Length of the appointment in minutes"),
    f("REASON", "Purpose of the appointment"),
    f("PROVIDER", "The appointment provider's code in AuroraEHR and name"),
    f("LOCATION", "The code in AuroraEHR and name of the location of the appointment."),
    f("REMARK", "Any notes on the appointment."),
    f("KEPT/FAIL", "Status of the appointment. A value of FAIL means that the patient didn't show up."),
])

# 9. Documents.csv
add_entity("Documents", "Documents.csv", "CSV", "Documents / Scans / Reports", [
    f("Account#", "Unique ID of the patient in AuroraEHR"),
    f("Accession#", "The unique ID of the appointment for which this document is associated."),
    f("Document#", "The document's unique ID. Is a number."),
    f("Document Type", "Type of the document in Rexpert.", ["Medical Report", "Referral Document", "Patient Instructions"]),
    f("Description", "Description of the document"),
    f("Exported File Path", "The path to the document within this export"),
    f("Date & Time Document was Dictated", "The date and time this document was originally dictated"),
    f("Date & Time Patient was Seen", "The date and time of the patient's appointment"),
    f("Date & Time Document was Transcribed", "The date and time this document was originally transcribed"),
    f("Provider", "The code in AuroraEHR and name of the provider responsible for the document's contents"),
    f("Status", "The status of the document. Will always be Signed/Completed Document"),
    f("Date Record was Created", "The date that record was first started"),
])

# 10. Scans.csv
add_entity("Scans", "Scans.csv", "CSV", "Documents / Scans / Reports", [
    f("Account#", "Unique ID of the patient in AuroraEHR."),
    f("Scan#", "The image/scan's unique numeric ID"),
    f("Type", "The file type such as .pdf, .jpg, etc."),
    f("Description", "Description of the image/scan"),
    f("Exported File Path", "Path to the actual image/scan within this export"),
    f("Date Record was Created", "The date that the record of the image/scan was first started."),
])

# 11. Reports.csv
add_entity("Reports", "Reports.csv", "CSV", "Documents / Scans / Reports", [
    f("Account#", "Unique ID of the patient in AuroraEHR"),
    f("Report#", "The report's unique numeric ID"),
    f("Date Report was Written", "Date of the report. Formatted MM/dd/yyyy."),
    f("Summary of Care Date", "If this report is a Summary of Care, indicates the date the care was given."),
    f("Description", "Description of the outside report"),
    f("Report Sent By", "The code in AuroraEHR and name of the referring provider who sent the report."),
    f("Note", "Any further information noted about the outside report"),
    f("Exported File Path", "The path to the actual report within this export."),
    f("Needs Review?", "Indicates whether this incoming report still needs to be reviewed"),
    f("Reviewed By", "The user in AuroraEHR who reviewed the report, if any."),
    f("Reviewed on Date", "The date the report was reviewed. Formatted MM/dd/yyyy."),
    f("Reviewed at Time", "The time the report was reviewed. Formatted hh:mm:ss am."),
    f("Report Hyperlink", "A URL for either the report or other supplemental information"),
    f("Date Record was Created", "The date that this record of the outside report was created."),
])

# 12. ClinicalAlerts.csv
add_entity("Clinical Alerts", "ClinicalAlerts.csv", "CSV", "Clinical", [
    f("Account#", "Unique ID of the patient in AuroraEHR"),
    f("Accession#", "The unique ID of the appointment for which these alerts are associated."),
    f("Alert Code", "Code for this type of alert in AuroraEHR"),
    f("Description", "The description of the alert."),
    f("Comment", "Any additional information beyond the description."),
    f("Date Record was Created", "Date of the record's entry. Formatted MM/dd/yyyy."),
    f("Date Record was last Updated", "Date of the record's last update. Formatted MM/dd/yyyy."),
])

# 13. Allergies.csv
add_entity("Allergies", "Allergies.csv", "CSV", "Clinical", [
    f("Account#", "Unique ID of the patient in AuroraEHR"),
    f("Accession#", "The unique ID of the appointment for which the allergies are associated."),
    f("Allergen Name", "The substance or medication to which the patient has an allergy."),
    f("Onset Date", "Date when allergy was reported to have started. Formatted MM/dd/yyyy"),
    f("Reaction", "Description of the patient's allergic reaction"),
    f("Reaction SNOMED", "SNOMED code of the allergic reaction. May be blank if not known."),
    f("Severity Level", "The severity of the patient's reaction to the allergen.", ["Mild", "Moderate", "Severe", "Unknown"]),
    f("RXNORM Code", "If the allergen is a medication, this column contains medication's RXNORM code."),
    f("Status", "The status of the allergy.", ["Active", "Inactive"]),
    f("Date Record was Created", "Date of the record's entry. Formatted MM/dd/yyyy"),
    f("Date Record was last Updated", "Date of the record's last update. Formatted MM/dd/yyyy."),
])

# 14. Immunizations.csv
add_entity("Immunizations", "Immunizations.csv", "CSV", "Clinical", [
    f("Account#", "Unique ID of the patient in AuroraEHR"),
    f("Accession#", "The unique ID of the appointment with which the immunizations are associated."),
    f("Immunization", "The name and code of the vaccine or presumed immunity"),
    f("Status", "The administration status.", ["Complete", "Refused", "not administered (presumed immunity)", "partially administered", "new immunization record", "ERROR: entered on this charge in error", "historical information - patient", "historical information - source unspecified", "historical information - from other provider", "historical information - from parent's written record", "historical information - from parent's recall", "historical information - from other registry", "historical information - from birth certificate", "historical information - from school record", "historical information - from public agency"]),
    f("Lot Number", "Manufacturer's lot number for a vaccine"),
    f("Manufacturer", "The manufacturer of the vaccine, if known."),
    f("Route", "How the vaccine was administered.", ["intramuscular", "subcutaneous", "nasal", "intradermal", "intravenous", "oral", "transdermal", "other/miscellaneous", "N/A"]),
    f("Site", "Administration site.", ["left arm", "right arm", "left thigh", "right thigh", "left deltoid", "right deltoid", "left gluteous medius", "right gluteous medius", "left vastus lateralis", "right vastus lateralis", "left lower forearm", "right lower forearm", "N/A"]),
    f("Units", "The amount of the vaccine administered (numeric)"),
    f("Administered By", "The name of the person who administered the vaccine."),
    f("Administered Date", "The date the vaccine was administered. Formatted MM/dd/yyyy."),
    f("Administered Time", "The time the vaccine was administered. Formatted hh:mm:ss am."),
    f("Refusal Reason", "If the vaccine was refused, reason for refusal.", ["parental decision", "religious exemption", "patient decision", "other", "N/A"]),
    f("Refusal Note", "Any additional information for vaccine refusal."),
    f("Note", "General, overall, notes."),
    f("Date Record was Created", "Date of the record entry. Formatted MM/dd/yyyy."),
    f("Date Record was last Updated", "Date of the record last update. Formatted MM/dd/yyyy."),
])

# 15. Medications (report) - PDF
add_entity("Medications", "Medications.pdf", "PDF", "Clinical", [
    f("Medication", "Name of the medication, along with dose and unit information."),
    f("Duration", "Describes the length of time during which the medication should be taken."),
    f("Start Date", "Start date of taking the medication. Formatted MM/dd/yyyy."),
    f("Stop Date", "Stop date of taking the medication. Formatted MM/dd/yyyy."),
    f("Number of Refills", "Number of refills allowed for the medications"),
    f("Last Fill Date", "Date of the last refill. Formatted MM/dd/yyyy."),
])

# 16. Problems.csv
add_entity("Problems/Diagnoses", "Problems.csv", "CSV", "Clinical", [
    f("Account#", "Unique ID of the patient in AuroraEHR"),
    f("Accession#", "The unique ID of the appointment for which the problem is associated."),
    f("Problem Code (SNOMED)", "The SNOMED code of the problem."),
    f("Problem Code (ICD10)", "The ICD10 code of the problem."),
    f("Description", "Description of the problem."),
    f("Onset Date", "Onset date of the problem. Formatted MM/dd/yyyy."),
    f("Resolved Date", "If valued, the date the problem was resolved. Formatted MM/dd/yyyy."),
    f("Note", "Any useful information reported by the staff and/or patient."),
    f("Status", "The status of the problem.", ["Active", "Inactive", "Resolved", "Chronic"]),
    f("Date Record was Created", "Date of the record entry. Formatted MM/dd/yyyy."),
    f("Date Record was last Updated", "Date of the record last update. Formatted MM/dd/yyyy."),
])

# 17. ReviewOfSystems.csv
add_entity("Review of Systems", "ReviewOfSystems.csv", "CSV", "Clinical", [
    f("Account#", "Unique ID of the patient in AuroraEHR"),
    f("Accession#", "The unique ID of the appointment for which this section's clinical data is associated."),
    f("ROS", "The review of systems text."),
    f("Date Record was Created", "Date of the record entry"),
    f("Date Record was Last Updated", "Date of record last change"),
])

# 18. SocialHistory.csv
add_entity("Social History", "SocialHistory.csv", "CSV", "History", [
    f("Account#", "Unique ID of the patient in AuroraEHR"),
    f("Accession#", "The unique ID of the appointment with which the Social History is associated."),
    f("Chance of Pregnancy?", "Might the patient be pregnant? Yes or no."),
    f("Last Menstrual Period Date", "If applicable, the date of the patient's last menstrual period. Formatted MM/dd/yyyy."),
    f("IVDA?", "Does the patient have a history of intravenous drug abuse? Yes or no."),
    f("Alcohol Use?", "Does the patient consume alcohol? Yes or no."),
    f("Victim of Abuse?", "Is the patient is a victim of physical or emotional abuse?", ["Patient responded yes", "Patient responded no", "Patient wasn't asked or didn't respond"]),
    f("Smoking Status", "Patient's reported smoking status followed by the appropriate SNOMED code.", ["Current daily smoker", "Current some day smoker", "Former smoker", "Never smoker", "Smoker; current status unknown", "Unknown if ever smoked", "Heavy tobacco smoker (10+ cigarettes a day)", "Light tobacco smoker (<10 cigarettes a day)", "Screening not indicated (situation)"]),
    f("Smoking Status Comment", "Smoking status explanation"),
    f("Family History of Anesthesia Complications?", "Does the patient or the patient's family have a history of anesthesia complications? Yes or no."),
    f("Comment", "Additional remarks or general social history notes."),
    f("Date Record was Created", "Date of the record entry. Formatted MM/dd/yyyy"),
    f("Date Record was Last Updated", "Date of record last change. Formatted MM/dd/yyyy"),
])

# 19. FamilyHistory.csv
add_entity("Family History", "FamilyHistory.csv", "CSV", "History", [
    f("Account#", "Unique ID of the patient in AuroraEHR"),
    f("Accession#", "The unique ID of the appointment for which the family history is associated."),
    f("Condition", "Name of the condition"),
    f("Code", "Code of the condition"),
    f("Code System", "Code system of the condition code"),
    f("Affected Family Member", "Relationship of person with the condition"),
    f("Onset Date", "Date of onset, if known"),
    f("Note", "Comments or notes pertaining to this family history record."),
    f("Date Record was Created", "Date of the record entry. Formatted MM/dd/yyyy."),
    f("Date Record was Last Updated", "Date of record last change. Formatted MM/dd/yyyy."),
])

# 20. SurgicalHistory.csv
add_entity("Surgical History", "SurgicalHistory.csv", "CSV", "History", [
    f("Account#", "Unique ID of the patient in AuroraEHR"),
    f("Accession#", "The unique ID of the appointment for which the surgical history was recorded."),
    f("Code", "Procedure code"),
    f("Code System", "Coding system used, such as SNOMED, CPT, etc."),
    f("Description", "Description of the procedure"),
    f("Date", "Free form field for when the procedure took place."),
    f("Note", "Any additional notes or comments about this procedure."),
    f("Date Record was Created", "Date of the record entry. Formatted MM/dd/yyyy."),
    f("Date Record was Last Updated", "Date of record last change. Formatted MM/dd/yyyy."),
])

# 21. Orders: Test and Results (report) - 4 PDF files
add_entity("Imaging Orders", "ImagingOrders.pdf", "PDF", "Orders", [
    f("Order#", "The unique ID of an imaging order."),
    f("Order Instructions", "Any specific instructions"),
    f("Ordered", "The date and time for when the order was placed."),
    f("Test", "The specific tests in an order."),
    f("Code", "The CPT code of the ordered test."),
])

add_entity("Lab Orders", "LabOrders.pdf", "PDF", "Orders", [
    f("Order#", "The unique ID of a lab order."),
    f("Order Instructions", "Any specific instructions"),
    f("Ordered", "The date and time for when the order was placed."),
    f("Test", "The specific tests in an order."),
    f("Code", "The LOINC code of the ordered test."),
])

add_entity("Pathology Orders", "PathologyOrders.pdf", "PDF", "Orders", [
    f("Order#", "The unique ID of a pathology order."),
    f("Order Instructions", "Any specific instructions"),
    f("Ordered", "The date and time for when the order was placed."),
    f("Test", "The specific tests in an order."),
    f("Code", "The LOINC code of the ordered test."),
])

add_entity("Therapy Orders", "TherapyOrders.pdf", "PDF", "Orders", [
    f("Order#", "The unique ID of a therapy order."),
    f("Order Instructions", "Any specific instructions"),
    f("Ordered", "The date and time for when the order was placed."),
    f("Test", "The specific tests in an order."),
    f("Code", "Code of the ordered test."),
])

# 22. VitalSigns.csv
add_entity("Vital Signs", "VitalSigns.csv", "CSV", "Clinical", [
    f("Account#", "Unique ID of the patient in AuroraEHR"),
    f("Accession#", "The unique ID of the appointment for which the vital signs are associated."),
    f("Capture Date", "Date when the vital signs were captured. Formatted MM/dd/yyyy."),
    f("Capture Time", "Time when the vital signs were captured. Formatted hh:mm:ss am."),
    f("Systolic Blood Pressure", "Numeric value of the patient's systolic blood pressure."),
    f("Diastolic Blood Pressure", "Numeric value of the patient's diastolic blood pressure."),
    f("Blood Pressure Site", "Location of blood pressure measurement. Is a free form text field."),
    f("Blood Pressure Side", "Side of the blood pressure measurement site.", ["Left", "Right", "N/A"]),
    f("Blood Sugar", "Numeric value of the patient's blood sugar."),
    f("Heart Rate", "Numeric value of the patient's heart rate in bpm."),
    f("Height", "The numeric value of the patient's height."),
    f("Height Scale", "Scale (cm/in) used for height"),
    f("Weight", "The numeric value of the patient's weight."),
    f("Weight Scale", "Scale (lbs/kg) used for weight"),
    f("BMI", "Numeric value of the patient's body mass index."),
    f("Oxygen Level", "spO2 reading of the patient's O2 saturation."),
    f("Supplemental O2?", "Is the patient using supplemental oxygen? Yes or no."),
    f("Inhaled O2 Concentration %", "If the patient is taking supplemental oxygen, the percentage of oxygen given."),
    f("Pain Scale", "The reported level of pain the patient is in. A numeric value from zero to 10, including N/A."),
    f("Respiratory Rate", "The patient's respiratory rate in the number of breaths per minute."),
    f("Temperature", "Numeric value of the patient's temperature."),
    f("Temperature Scale", "Scale (C/F) used for temperature"),
    f("Shoe Size", "For podiatry practices, the numeric value of the size of shoe the patient wears."),
    f("Screening Not Done", "If vitals were not captured, the reason why.", ["Patient refused screening", "Procedure contraindicated (situation)", "Medical contraindication"]),
    f("Comment", "Any additional comments that should be noted."),
])

# 23. ImplantedDevices.csv
add_entity("Implanted Devices", "ImplantedDevices.csv", "CSV", "Additional Clinical Data", [
    f("Account#", "Unique ID of the patient in AuroraEHR"),
    f("Accession#", "The unique ID of the appointment with which the implanted devices is associated."),
    f("Device Type (SNOMED Code)", "The SNOMED code of the device's type."),
    f("Description", "Text description of the device"),
    f("Company Name", "Manufacturer of the device"),
    f("Brand Name", "Device brand name"),
    f("Lot Number", "Manufacturer's lot number for the device"),
    f("Catalog Number", "Catalog number of the device"),
    f("Model Number", "Model number of the device"),
    f("Serial Number", "Serial number of the device"),
    f("Unique Device ID", "ID of the implanted device"),
    f("Expiration Date", "Date of implant expiration"),
    f("Manufactured Date", "Date of implant creation"),
    f("Placement Date", "Date of implantation"),
    f("Placement Site", "Location of the implant"),
    f("Placement Laterality", "Indication of location side, if relevant"),
    f("Placement Provider", "Provider who performed the implantation"),
    f("Placement Note", "Any further notes regarding placement"),
    f("MRI Safety", "MRI safety status", ["MRI Safe", "MRI Conditional", "MRI Unsafe"]),
    f("Device ID", "A number or identifier that denotes a specific kind of device."),
    f("Status", "A device has either an active or inactive status."),
    f("Date Record was Created", "Date of the record entry"),
])

# 24. PatientEducation.csv
add_entity("Patient Education", "PatientEducation.csv", "CSV", "Additional Clinical Data", [
    f("Account#", "Unique ID of the patient in AuroraEHR"),
    f("Accession#", "The unique ID of the appointment for which the education material given to the patient is associated."),
    f("Type", "What the educational material is in reference to.", ["general", "patient medication", "patient problem", "patient lab"]),
    f("Description", "Description of the educational material"),
    f("URL", "Link to the material"),
    f("Date/Time Given", "Date and time the educational material was given to the patient. Formatted MM/dd/yyyy hh:mm:ss am"),
    f("Given By", "Name of the user who gave the educational material to the patient."),
    f("Date Record was Created", "The date the record was created. Formatted MM/dd/yyyy."),
    f("Date Record was Last Updated", "The date the record was last updated. Formatted MM/dd/yyyy."),
])

# 25. PostAppointment.csv
add_entity("Post Appointment", "PostAppointment.csv", "CSV", "Additional Clinical Data", [
    f("Account#", "Unique ID of the patient in AuroraEHR"),
    f("Accession#", "The unique ID of the appointment for which this section's clinical data is associated."),
    f("Bleeding", "Patient's response when questioned regarding bleeding"),
    f("Drainage", "Patient's response when questioned regarding drainage"),
    f("Drinking Water", "Patient's response when questioned regarding drinking water"),
    f("Eating/Drinking Changes", "Notes regarding any changes the patient has experienced in fluid or food intake."),
    f("Fever", "Patient's response when questioned regarding fever"),
    f("Nausea", "Patient's response when questioned regarding nausea"),
    f("Needlepoint Redness", "Patient's response when questioned regarding needlepoint redness"),
    f("Pain Medications", "Patient's response when questioned regarding pain medications used"),
    f("Sore Throat", "Patient's response when questioned regarding a sore throat"),
    f("Swelling", "Patient's response when questioned regarding swelling"),
    f("Unusual/Excessive Pain", "Patient's response when questioned regarding any unusual or excessive pain."),
    f("Follow-Up Phone Call Comment", "Comments regarding the follow-up call with the patient"),
    f("Post-Discharge Comment", "Comments regarding any details or events that occurred after discharge."),
    f("Date Record Entered", "Date of the record entry. Formatted MM/dd/yyyy."),
    f("Date Record Last Changed", "Date of record last change. Formatted MM/dd/yyyy."),
])

# 26. PostOp.csv
add_entity("Post Op", "PostOp.csv", "CSV", "Surgical / Procedural", [
    f("Account#", "Unique ID of the patient in AuroraEHR"),
    f("Accession#", "The unique ID of the appointment with which this section's clinical data is associated."),
    f("Anesthesia Given?", "Was anesthesia given to the patient? Yes or no."),
    f("Anesthesia Type", "If given, the type of anesthesia given."),
    f("Activity Arrival", "Patient's ability to move their extremities upon arrival.", ["Able to move 4 extremities", "Able to move 2 extremities", "Able to move 0 extremities", "N/A"]),
    f("Activity Discharge", "Patient's ability to move their extremities upon discharge.", ["Able to move 4 extremities", "Able to move 2 extremities", "Able to move 0 extremities", "N/A"]),
    f("Respiration Arrival", "Patient's ability to breathe upon arrival.", ["Able to cough and breathe deeply", "Dyspnea or limited breathing", "Apnea", "N/A"]),
    f("Respiration Discharge", "Patient's ability to breathe upon discharge.", ["Able to cough and breathe deeply", "Dyspnea or limited breathing", "Apnea", "N/A"]),
    f("Circulation Discharge", "The patient's systolic blood pressure relative to their pre-anesthetic BP.", ["systolic BP +/- 20 mm/hg of pre-anesthetic BP", "systolic BP +/- 21-49 mm/hg of pre-anesthetic BP", "systolic BP +/- 50 mm/hg of pre-anesthetic BP", "N/A"]),
    f("Consciousness Arrival", "The patient's level of consciousness upon arriving.", ["Fully awake", "Arousable on calling", "Not responding", "N/A"]),
    f("Consciousness Discharge", "The patient's level of consciousness upon discharge.", ["Fully awake", "Arousable on calling", "Not responding", "N/A"]),
    f("O2 Saturation Arrival", "The patient's oxygen saturation level upon arrival.", ["Able to maintain SpO2 above 92% on RA", "Needs supplemental O2 to maintain SpO2 > 90%", "SpO2 < than 90% with O2 supplementation", "N/A"]),
    f("O2 Saturation Discharge", "The patient's oxygen saturation level upon discharge.", ["Able to maintain SpO2 above 92% on RA", "Needs supplemental O2 to maintain SpO2 > 90%", "SpO2 < than 90% with O2 supplementation", "N/A"]),
    f("Left Hand Grip", "Vascular assessment of the patient's left hand grip."),
    f("Right Hand Grip", "Vascular assessment of the patient's right hand grip."),
    f("Left Brachial Pulse", "Vascular assessment of the patient's brachial pulse on their left arm."),
    f("Right Brachial Pulse", "Vascular assessment of the patient's brachial pulse on their right arm."),
    f("Left Radial Pulse", "Vascular assessment of the patient's radial pulse on their left wrist."),
    f("Right Radial Pulse", "Vascular assessment of the patient's radial pulse on their right wrist."),
    f("Left Dorsalis Pulse", "Vascular assessment of the patient's dorsalis pulse on their left foot."),
    f("Right Dorsalis Pulse", "Vascular assessment of the patient's dorsalis pulse on their right foot."),
    f("Left Posterior Pulse", "Vascular assessment of the patient's posterior pulse on their left ankle."),
    f("Right Posterior Pulse", "Vascular assessment of the patient's posterior pulse on their right ankle."),
    f("Color & Temp of Left Hand", "The color and temperature of the patient's left hand."),
    f("Color & Temp of Right Hand", "The color and temperature of the patient's right hand."),
    f("Color & Temp of Left Foot", "The color and temperature of the patient's left foot."),
    f("Color & Temp of Right Foot", "The color and temperature of the patient's right foot."),
    f("Number of Sutures", "Number of sutures the patient received"),
    f("Oriented X3 (Person, Place, and Time)", "Is the patient alert and oriented?"),
    f("Discharge Date", "Date of patient's discharge. Formatted MM/dd/yyyy."),
    f("Discharge Time", "Time of patient's discharge. Formatted hh:mm:ss am."),
    f("Dressing On Discharge", "Describes any dressings present at the time of patient discharge."),
    f("Transport to Recovery By", "The method by which the patient was transported to recovery.", ["Independent Ambulation", "Wheel Chair", "Stretcher", "Walker", "Cane"]),
    f("Time Arrived in Recovery", "The time the patient arrived in recovery. Formatted hh:mm:ss am."),
    f("Initial Fluid Intake - Intra Procedure - D5W", "comment format"),
    f("Initial Fluid Intake - Recovery - D5W", "comment format"),
    f("Initial Fluid Intake - Intra Procedure - NS", "comment format"),
    f("Initial Fluid Intake - Recovery - NS", "comment format"),
    f("Initial Fluid Intake - Intra Procedure - Contrast", "comment format"),
    f("Initial Fluid Intake - Recovery - Contrast", "comment format"),
    f("Initial Fluid Intake - Intra Procedure - Oral", "comment format"),
    f("Initial Fluid Intake - Recovery - Oral", "comment format"),
    f("Initial Fluid Intake Comment", "comment format"),
    f("Comment", "Any additional notes regarding the patient's post-op or the values recorded."),
    f("Date Record Entered", "Date of the record entry. Formatted MM/dd/yyyy."),
    f("Date Record Last Changed", "Date of record last change. Formatted MM/dd/yyyy."),
])

# 27. PreOp.csv
add_entity("Pre Op", "PreOp.csv", "CSV", "Surgical / Procedural", [
    f("Account#", "Unique ID of the patient in AuroraEHR"),
    f("Accession#", "The unique ID of the appointment for which this section's clinical data is associated."),
    f("Activity", "Patient's ability to move their extremities upon arrival.", ["Able to move 4 extremities", "Able to move 2 extremities", "Able to move 0 extremities", "N/A"]),
    f("Respiration", "Patient's ability to breathe upon arrival.", ["Able to cough and breathe deeply", "Dyspnea or limited breathing", "Apnea", "N/A"]),
    f("Consciousness", "The patient's level of consciousness upon arriving.", ["Fully awake", "Arousable on calling", "Not responding", "N/A"]),
    f("O2 Saturation", "The patient's oxygen saturation level upon arrival.", ["Able to maintain SpO2 above 92% on RA", "Needs supplemental O2 to maintain SpO2 > 90%", "SpO2 < than 90% with O2 supplementation", "N/A"]),
    f("Dressing On Arrival", "Describes any dressings present at the time of patient arrival."),
    f("Left Hand Grip", "Vascular assessment of the patient's left hand grip."),
    f("Right Hand Grip", "Vascular assessment of the patient's right hand grip."),
    f("NPO?", "This question will have a yes/no answer."),
    f("Last PO", "Last oral intake"),
    f("Left Brachial Pulse", "Vascular assessment of the patient's brachial pulse on their left arm."),
    f("Right Brachial Pulse", "Vascular assessment of the patient's brachial pulse on their right arm."),
    f("Left Radial Pulse", "Vascular assessment of the patient's radial pulse on their left wrist."),
    f("Right Radial Pulse", "Vascular assessment of the patient's radial pulse on their right wrist."),
    f("Left Dorsalis Pulse", "Vascular assessment of the patient's dorsalis pulse on their left foot."),
    f("Right Dorsalis Pulse", "Vascular assessment of the patient's dorsalis pulse on their right foot."),
    f("Left Posterior Pulse", "Vascular assessment of the patient's posterior pulse on their left ankle."),
    f("Right Posterior Pulse", "Vascular assessment of the patient's posterior pulse on their right ankle."),
    f("Color & Temp of Left Hand", "The color and temperature of the patient's left hand."),
    f("Color & Temp of Right Hand", "The color and temperature of the patient's right hand."),
    f("Color & Temp of Left Foot", "The color and temperature of the patient's left foot."),
    f("Color & Temp of Right Foot", "The color and temperature of the patient's right foot."),
    f("Transportation To Procedure Room By", "The method by which the patient was transported to the procedure room.", ["Independent Ambulation", "Wheel Chair", "Stretcher", "Walker", "Cane"]),
    f("Patient Arrived By", "Method of patient's delivery"),
    f("Comment", "Text of the comment for the entry"),
    f("Date Record Entered", "Date of the record entry"),
    f("Date Record Last Changed", "Date of record last change"),
])

# 28. PreopProcedureNotes.csv
add_entity("Preop Procedure Notes", "PreopProcedureNotes.csv", "CSV", "Surgical / Procedural", [
    f("Account#", "Unique ID of the patient in AuroraEHR"),
    f("Accession#", "The unique ID of the appointment for which this section's clinical data is associated."),
    f("Translations Provided By", "Name of the translator, if any"),
    f("Verbal Consent Obtained From", "Name of the person who gave consent"),
    f("Access Fistula?", "yes/no answer"),
    f("Access Graft?", "yes/no answer"),
    f("Access Left Arm?", "yes/no answer"),
    f("Access Right Arm?", "yes/no answer"),
    f("Access Other?", "Place of the other access"),
    f("Catheter Left Subclavian?", "yes/no answer"),
    f("Catheter Right Subclavian?", "yes/no answer"),
    f("Catheter Left Thigh?", "yes/no answer"),
    f("Catheter Right Thigh?", "yes/no answer"),
    f("Catheter Order Given?", "yes/no answer"),
    f("Catheter Provider Vital Signs Aware?", "yes/no answer"),
    f("Anxiety Reduction Explained Procedure?", "yes/no answer"),
    f("Anxiety Reduction Attained?", "yes/no answer"),
    f("Anxiety Reduction Allowed Time for Patient Questions?", "yes/no answer"),
    f("Anxiety Reduction Encouraged to Verbalize Concerns?", "yes/no answer"),
    f("Anxiety Reduction RN Signature", "Stamp of electronic signature with RN name"),
    f("Is a Declot Procedure?", "yes/no answer"),
    f("Declot Procedure Performed By", "ID of the provider"),
    f("Declot Procedure Sterility Monitored/Maintained?", "yes/no answer"),
    f("Declot Procedure No Breaks in Sterility?", "yes/no answer"),
    f("Declot Alteplase Heparin Given Time", "Time of the injection"),
    f("Declot Procedure No Thrombolytics?", "yes/no answer"),
    f("Declot Procedure RN Signature", "Stamp of electronic signature with RN name"),
    f("Antibiotics Ancef Given?", "yes/no answer"),
    f("Antibiotics Clindamycin Given?", "yes/no answer"),
    f("Antibiotics Vancomycin Given?", "yes/no answer"),
    f("Antibiotics Levaquin Given?", "yes/no answer"),
    f("Antibiotics Administered Via", "Place of administering the antibiotics used"),
    f("Antibiotics Administered Time", "Time of administering the antibiotics used"),
    f("Antibiotics RN Signature", "Stamp of electronic signature with RN name"),
    f("Date Record Entered", "Date of the record entry"),
    f("Date Record Last Changed", "Date of record last change"),
])

# 29. ProviderOrders.csv
add_entity("Provider Orders", "ProviderOrders.csv", "CSV", "Surgical / Procedural", [
    f("Account#", "Unique ID of the patient in AuroraEHR"),
    f("Accession#", "The unique ID of the appointment for which this section's clinical data is associated."),
    f("Puncture Left Arm?", "yes/no answer"),
    f("Puncture Right Arm?", "yes/no answer"),
    f("Puncture Left Groin?", "yes/no answer"),
    f("Puncture Right Groin?", "yes/no answer"),
    f("Puncture Left Jugular?", "yes/no answer"),
    f("Puncture Right Jugular?", "yes/no answer"),
    f("Puncture Other", "A description of where the puncture was placed"),
    f("Catheter Left Subclavian?", "yes/no answer"),
    f("Catheter Right Subclavian?", "yes/no answer"),
    f("Catheter Left Thigh?", "yes/no answer"),
    f("Catheter Right Thigh?", "yes/no answer"),
    f("Discharge Disposition", "Patient's disposition at the time of discharge"),
    f("Discharge Diagnoses (SNOMEDCT)", "Diagnoses with their SNOMED codes"),
    f("Refer To", "Referring provider name"),
    f("Refer To Date", "Date of the referral"),
    f("Referral Reason", "Reason for the referral"),
    f("Functional Status", "The SNOMED code and description of the patient's functional status."),
    f("Functional Status Effective Date", "Date for functional status check"),
    f("Functional Status Note", "Note on functional status"),
    f("Cognitive Status Status", "The SNOMED code and description of the patient's cognitive status."),
    f("Cognitive Status Effective Date", "Date for cognitive status check"),
    f("Cognitive Status Note", "Note on cognitive status"),
    f("Free Text Order", "Order of free text"),
    f("Free Text Order Provider Signature", "Stamp of electronic signature with provider name"),
    f("Free Text Order RN Signature", "Stamp of electronic signature with RN name"),
    f("Ancef Medication Given?", "Was 1g of Ancef, in 10ml of sterile water, IV STAT given to the patient? yes/no"),
    f("Clindamycin Medication Given", "Was 600mg of Clindamycin given? yes/no"),
    f("Vancomycin Medication Given", "Was 1g of Vancomycin given? yes/no"),
    f("Tylenol Medication Given", "Was 500mg of Tylenol Extra Strength given? yes/no"),
    f("Antibiotic Provider Signature", "Stamp of electronic signature with provider name"),
    f("Antibiotic RN Signature", "Stamp of electronic signature with RN name"),
    f("Heparin Quantity Given 1000 Units via Arterial Port", "The quantity of 1000 Units/ml of Heparin given via arterial port, post-procedure"),
    f("Heparin Quantity Given 5000 Units via Arterial Port", "The quantity of 5000 Units/ml of Heparin given via arterial port, post-procedure"),
    f("Heparin Quantity Given 1000 Units via Venous Port", "The quantity of 1000 Units/ml of Heparin given via venous port, post-procedure"),
    f("Heparin Quantity Given 5000 Units via Venous Port", "The quantity of 5000 Units/ml of Heparin given via venous port, post-procedure"),
    f("Heparin Provider Signature", "Stamp of electronic signature with provider name"),
    f("Heparin RN Signature", "Stamp of electronic signature with RN name"),
    f("Suture Remove In Minutes", "Suture removal time in minutes"),
    f("Discharge When Stable and Provide Instructions?", "yes/no answer"),
    f("Exempt From Being Discharged into the Company of a Responsible Adult?", "yes/no answer"),
    f("Patient Transferred to Another Facility?", "yes/no answer"),
    f("Discharge Provider Signature", "Stamp of electronic signature with provider name"),
    f("Discharge RN Signature", "Stamp of electronic signature with RN name"),
    f("Date Record Entered", "Date of the record entry"),
    f("Date Record Last Changed", "Date of record last change"),
])

# 30. SurgicalChecklist.csv
add_entity("Surgical Checklist", "SurgicalChecklist.csv", "CSV", "Surgical / Procedural", [
    f("Account#", "Unique ID of the patient in AuroraEHR"),
    f("Accession#", "The unique ID of the appointment for which this section's clinical data is associated."),
    f("Patient Preop Confirmation?", "yes/no answer"),
    f("RN Preop Signature", "Stamp of electronic signature with RN name"),
    f("Patient Procedure Confirmation?", "yes/no answer"),
    f("RN Procedure Signature", "Stamp of electronic signature with RN name"),
    f("RN Postop Signature", "Stamp of electronic signature with RN name"),
    f("Signature", "Stamp of electronic signature with surgeon name"),
    f("Patient Recovery Management Concerns", "A text field containing remarks on recovery management"),
    f("Prophylaxis Given Within 60 Minutes?", "yes/no answer"),
    f("RN History Physical Confirmation?", "yes/no answer"),
    f("RN Instrument Counts Completed?", "yes/no answer"),
    f("RN Preanesthesia Assessment Confirmation?", "yes/no answer"),
    f("Equipment Problems Addressed?", "yes/no answer"),
    f("Site Marked And Visible?", "yes/no answer"),
    f("Team Members Introduced?", "yes/no answer"),
    f("Date Record was Created", "Date of the record entry"),
    f("Date Record was Last Updated", "Date of record last change"),
])

# 31. SutureInfo.csv
add_entity("Suture Info", "SutureInfo.csv", "CSV", "Surgical / Procedural", [
    f("Account#", "Unique ID of the patient in AuroraEHR"),
    f("Accession#", "The unique ID of the appointment for which the suture info is associated."),
    f("Comment", "Text of the comment for the entry"),
    f("Date Captured", "Date of the suture"),
    f("Time Captured", "Time of the suture"),
    f("Signature", "Stamp of electronic signature with surgeon name"),
    f("Dry Intact Dressing?", "yes/no answer"),
    f("Pain or Active Bleeding?", "yes/no answer"),
    f("Redness or Swelling?", "yes/no answer"),
    f("Remove Sutures?", "yes/no answer"),
    f("Date Record was Created", "Date of the record entry"),
    f("Date Record was Last Updated", "Date of record last change"),
])

# Compute summary stats
total_entities = len(entities)
total_fields = sum(e["field_count"] for e in entities)
fields_with_desc = sum(1 for e in entities for field in e["fields"] if field["has_description"])
fields_with_value_sets = sum(1 for e in entities for field in e["fields"] if "value_set" in field)

# Category breakdown
from collections import defaultdict
cat_stats = defaultdict(lambda: {"entities": 0, "fields": 0})
for e in entities:
    cat_stats[e["category"]]["entities"] += 1
    cat_stats[e["category"]]["fields"] += e["field_count"]

summary = {
    "total_entities": total_entities,
    "total_fields": total_fields,
    "fields_with_descriptions": fields_with_desc,
    "description_percentage": round(fields_with_desc / total_fields * 100, 1),
    "fields_with_value_sets": fields_with_value_sets,
    "categories": {k: v for k, v in sorted(cat_stats.items())},
    "entities_by_category": {}
}

for cat in sorted(cat_stats.keys()):
    summary["entities_by_category"][cat] = [
        {"name": e["name"], "file_name": e["file_name"], "format": e["format"], "field_count": e["field_count"]}
        for e in entities if e["category"] == cat
    ]

# Write outputs
with open("entity-inventory-full.json", "w") as f:
    json.dump(entities, f, indent=2)

with open("entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print(f"Entities: {total_entities}")
print(f"Total fields: {total_fields}")
print(f"Fields with descriptions: {fields_with_desc} ({summary['description_percentage']}%)")
print(f"Fields with value sets: {fields_with_value_sets}")
print(f"\nCategory breakdown:")
for cat, stats in sorted(cat_stats.items()):
    print(f"  {cat}: {stats['entities']} entities, {stats['fields']} fields")
