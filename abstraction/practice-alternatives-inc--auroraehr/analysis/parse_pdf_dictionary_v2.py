#!/usr/bin/env python3
"""Parse AuroraEHR (b)(10) EHI export PDF data dictionary into structured JSON.

Reads the pdftotext -layout output. Uses column-position analysis to separate
field names from descriptions based on the "Field" / "Explanation" header alignment.
"""

import json
import re
import sys

INPUT = "pdf_text.txt"
OUTPUT = "full-entity-inventory.json"

def load_text(path):
    with open(path, "r") as f:
        return f.read()


# Manually curated field lists per entity, derived from reading the PDF text.
# This ensures 100% accuracy vs. heuristic parsing of messy PDF layout.
# Each entry: (field_name, description, [optional_values])

ENTITIES = [
    {
        "entity_name": "Account Data",
        "file_name": "AccountData.pdf",
        "format": "PDF",
        "category": "Account Data",
        "fields": [
            ("Account Information", "Full name, DOB, SS#, Address, contact information, ethnicity, language, and employment status"),
            ("Services", "Practice-specific classifications attributed to the patient"),
            ("Associated Providers/Lawyers", "The list of associated providers and lawyers"),
            ("Billing information", "Account balances and personal statements"),
            ("Clinical Information", "Diagnoses, history of accident/injury, dates of illness, admission, discharge, disability status, and/or return to work"),
            ("Overrides", "Information that 'overrides' default handling of this patient in AuroraEHR. Additionally, contains patient's location, pharmacy, and rounds/census information."),
            ("Audit Details", "History of information changes"),
            ("Emergency Contact", "Information about the contact designated as an emergency contact"),
            ("Account Contacts", "Contact information about the people who are important factors in a patient's care."),
            ("All Account Payors", "The list of payors attached to the patient's account"),
            ("Account Employers", "The list of patient's employers"),
            ("Charges/Payments", "All charges and payments of an account"),
        ]
    },
    {
        "entity_name": "Charges",
        "file_name": "Charges.csv",
        "format": "CSV",
        "category": "Charges/Payments",
        "fields": [
            ("PRACTICE", "Practice name"),
            ("ACCOUNT NO", "Unique ID of the patient in AuroraEHR"),
            ("FIRST NAME", "Patient's first name"),
            ("LAST NAME", "Patient's last name"),
            ("SERVICE DT", "Date of service"),
            ("PROVIDER", "Provider code in AuroraEHR and name"),
            ("LOCATION", "Location code in AuroraEHR and name"),
            ("DIAG 1", "Diagnosis code (ICD10)"),
            ("DIAG 2", "Diagnosis code (ICD10)"),
            ("DIAG 3", "Diagnosis code (ICD10)"),
            ("DIAG 4", "Diagnosis code (ICD10)"),
            ("PROCEDURE", "Procedure code for billing (usually CPT)"),
            ("QUANTITY", "The number of times this procedure was billed for this service date."),
            ("CHARGE AMT", "Amount charged"),
            ("REF PROVIDER", "Referring provider's code in AuroraEHR and name"),
            ("FIRST PAYOR", "Primary payor name"),
            ("RELATIVE VALUE", "Number of RVUs"),
            ("REF PROVIDER 2", "Second referring provider's code in AuroraEHR and name"),
            ("OTHER PROVIDER", "Other provider's code in AuroraEHR and name"),
            ("MODIFIERS", "The list of procedure modifiers"),
            ("CLAIM", "Claim number"),
            ("AGE", "Age of the patient as of the charge's service date as a whole number. Format varies by age (days, weeks, months, years)."),
            ("STATUS", "Status of the charge.", ["A - Active", "I - Inactive", "J - On hold when due from personal", "H - On hold"]),
            ("DOCUMENT NBR", "Document number in the system"),
            ("ZIP CODE", "The patient's zip code"),
            ("CASH", "The total amount paid thus far: includes payments and refunds"),
            ("CREDITS", "The total amount of non-cash payments such as contractual allowances and courtesies"),
            ("INTEREST", "The total amount of interest accumulated"),
            ("BALANCE", "The remaining balance on the charge"),
            ("AUTH", "The reference or authorization number on the charge"),
        ]
    },
    {
        "entity_name": "Payments",
        "file_name": "Payments.csv",
        "format": "CSV",
        "category": "Charges/Payments",
        "fields": [
            ("ACCOUNT NO", "Unique ID of the patient in AuroraEHR"),
            ("CLAIM", "Claim number against which the payment was made"),
            ("SERVICE DATE", "Date of service of the charge"),
            ("PROCEDURE", "Procedure code for billing (usually CPT) of the charge"),
            ("DESCRIPTION", "Procedure description of the charge"),
            ("DIVISION", "Division code from the charge"),
            ("LOCATION", "Location's code in AuroraEHR and name, from the charge"),
            ("PROVIDER", "Provider's code in AuroraEHR and name, from the charge"),
            ("DEPOSIT DT", "Date of deposit"),
            ("FIN CLASS", "Financial class of the payment's payor"),
            ("REPT GRP", "Report group of the payment's payor"),
            ("PAYOR GRP", "Report group of the payment's payor"),
            ("PAYOR", "Payor code of the payment's payor"),
            ("REMIT TYPE", "Code and explanation of the remit type"),
            ("REMIT", "Explanation of the remit type"),
            ("PAY AMOUNT", "Amount of the payment, including cash and non-cash payments. Will be $0.00 if the payment was interest, and thus doesn't affect the charge balance."),
            ("INT AMOUNT", "Amount of interest"),
            ("DOCUMENT", "Document number, often the check number"),
            ("NOTE", "Note text, if any"),
            ("ENTRY DT", "Date of entry"),
            ("USER ID", "ID of the user who created the entry"),
            ("STATUS", "Payment status.", ["A - Active", "I - Inactive", "H - On hold"]),
        ]
    },
    {
        "entity_name": "ChargeTransactions",
        "file_name": "ChargeTransactions.csv",
        "format": "CSV",
        "category": "Charges/Payments",
        "fields": [
            ("ACCOUNT NO", "Unique ID of the patient in AuroraEHR"),
            ("CLAIM", "Claim number"),
            ("TRANS DT", "Date of the transaction. Formatted as MM/dd/yyyy"),
            ("TRANS TM", "Time of the transaction. Formatted as HH:mm:ss:mmm"),
            ("PAYOR", "Payor's code in AuroraEHR and name"),
            ("DESCRIPTION", "Description of the transaction"),
            ("PAYOR FROM", "For billing transactions, the name of the payor involved"),
            ("REASON", "The description or reason that the transaction was created"),
            ("FORM", "For billing transactions, the billing form used"),
            ("RUN NO", "For billing transactions, the run number"),
            ("ENTRY DT", "Date of entry. Formatted as MM/dd/yyyy"),
            ("STATUS", "The status of the charge as of the transaction's date/time.", ["A - Active", "I - Inactive", "J - hold when due from personal", "H - hold"]),
        ]
    },
    {
        "entity_name": "AccountNotes",
        "file_name": "AccountNotes.csv",
        "format": "CSV",
        "category": "Notes/Instructions",
        "fields": [
            ("Account#", "Unique ID of the patient in AuroraEHR"),
            ("Note Type", "The note's type or category.", ["Billing", "Family Display", "Medical", "Surgery", "Important"]),
            ("Priority", "Whether the note is marked as important"),
            ("Text", "Text of the note"),
            ("Date Record was Created", "The date the record was created. Formatted MM/dd/yyyy."),
        ]
    },
    {
        "entity_name": "ClinicalInstructions",
        "file_name": "ClinicalInstructions.csv",
        "format": "CSV",
        "category": "Notes/Instructions",
        "fields": [
            ("Account#", "Unique ID of the patient in AuroraEHR"),
            ("Accession#", "The unique ID of the appointment for which these instructions are to be used."),
            ("For Phase", "The phase of the appointment where the instructions should be used."),
            ("Instruction text", "Text of the instruction"),
            ("Date Record was Created", "The date the record was created. Formatted MM/dd/yyyy."),
        ]
    },
    {
        "entity_name": "ClinicalProgressNotes",
        "file_name": "ClinicalProgressNotes.csv",
        "format": "CSV",
        "category": "Notes/Instructions",
        "fields": [
            ("Account#", "Unique ID of the patient in AuroraEHR"),
            ("Accession#", "The unique ID of the appointment for which these notes were entered."),
            ("Is an Amendment?", "Indicates whether this note is an amendment for a note entered earlier"),
            ("Amendment Source", "Source of the new information, if not AuroraEHR"),
            ("Primary Signature", "Signature of the user, stating that this note is complete. Typically will be of the appointment provider."),
            ("Primary Signature Signed Date", "Date of the signature. Formatted MM/dd/yyyy"),
            ("Primary Signature Signed Time", "Time of the signature. Formatted hh:mm:ss am"),
            ("2nd Signature", "Secondary signature. Needed for certain note types. Typically will be of someone other than the provider, who is able to sign off on notes like a supervising nurse, an RN, etc."),
            ("2nd Signature Signed Date", "Date of the second signature. Formatted MM/dd/yyyy"),
            ("2nd Signature Signed Time", "Time of the second signature. Formatted hh:mm:ss am"),
            ("Description", "A brief description of the note type or purpose."),
            ("Progress Note", "The note text itself"),
        ]
    },
    {
        "entity_name": "Appointments",
        "file_name": "Appointments.csv",
        "format": "CSV",
        "category": "Appointments",
        "fields": [
            ("ACCOUNT NO", "Unique ID of the patient in AuroraEHR"),
            ("APPT_DATE", "Date of the appointment. Formatted MM/dd/yyyy"),
            ("APPT_TIME", "Time of the appointment. Formatted hh:mm am"),
            ("APPT_MINUTES", "Length of the appointment in minutes"),
            ("REASON", "Purpose of the appointment"),
            ("PROVIDER", "The appointment provider's code in AuroraEHR and name"),
            ("LOCATION", "The code in AuroraEHR and name of the location of the appointment."),
            ("REMARK", "Any notes on the appointment. Typically used to indicate if the patient was contacted, if the appointment had to be rescheduled, or reason why the patient couldn't make it."),
            ("KEPT/FAIL", "Status of the appointment. A value of FAIL means that the patient didn't show up, and didn't give prior warning."),
        ]
    },
    {
        "entity_name": "Documents",
        "file_name": "Documents.csv",
        "format": "CSV",
        "category": "Documents/Scans/Reports",
        "fields": [
            ("Account#", "Unique ID of the patient in AuroraEHR"),
            ("Accession#", "The unique ID of the appointment for which this document is associated."),
            ("Document#", "The document's unique ID. Is a number."),
            ("Document Type", "Type of the document in Rexpert.", ["Medical Report", "Referral Document", "Patient Instructions"]),
            ("Description", "Description of the document"),
            ("Exported File Path", "The path to the document within this export"),
            ("Date & Time Document was Dictated", "The date and time this document was originally dictated, typically filled in by a transcription service."),
            ("Date & Time Patient was Seen", "The date and time of the patient's appointment, or when actually seen."),
            ("Date & Time Document was Transcribed", "The date and time this document was originally transcribed, typically filled in by a transcription service"),
            ("Provider", "The code in AuroraEHR and name of the provider responsible for the document's contents"),
            ("Status", "The status of the document. Will always be Signed/Completed Document"),
            ("Date Record was Created", "The date that record was first started"),
        ]
    },
    {
        "entity_name": "Scans",
        "file_name": "Scans.csv",
        "format": "CSV",
        "category": "Documents/Scans/Reports",
        "fields": [
            ("Account#", "Unique ID of the patient in AuroraEHR."),
            ("Scan#", "The image/scan's unique numeric ID"),
            ("Type", "The file type such as .pdf, .jpg, etc."),
            ("Description", "Description of the image/scan"),
            ("Exported File Path", "Path to the actual image/scan within this export"),
            ("Date Record was Created", "The date that the record of the image/scan was first started. This isn't necessarily the same as the date that the contents of the image/scan were created."),
        ]
    },
    {
        "entity_name": "Reports",
        "file_name": "Reports.csv",
        "format": "CSV",
        "category": "Documents/Scans/Reports",
        "fields": [
            ("Account#", "Unique ID of the patient in AuroraEHR"),
            ("Report#", "The report's unique numeric ID"),
            ("Date Report was Written", "Date of the report. Formatted MM/dd/yyyy."),
            ("Summary of Care Date", "If this report is a Summary of Care, indicates the date the care was given. Formatted MM/dd/yyyy."),
            ("Description", "Description of the outside report"),
            ("Report Sent By", "The code in AuroraEHR and name of the referring provider who sent the report."),
            ("Note", "Any further information noted about the outside report"),
            ("Exported File Path", "The path to the actual report within this export."),
            ("Needs Review?", "Indicates whether this incoming report still needs to be reviewed"),
            ("Reviewed By", "The user in AuroraEHR who reviewed the report, if any."),
            ("Reviewed on Date", "The date the report was reviewed. Formatted MM/dd/yyyy."),
            ("Reviewed at Time", "The time the report was reviewed. Formatted hh:mm:ss am."),
            ("Report Hyperlink", "A URL for either the report or other supplemental information such as an image. In either case, the report is not stored within AuroraEHR. Credentials may be required to access the URL."),
            ("Date Record was Created", "The date that this record of the outside report was created."),
        ]
    },
    {
        "entity_name": "ClinicalAlerts",
        "file_name": "ClinicalAlerts.csv",
        "format": "CSV",
        "category": "Clinical Alerts",
        "fields": [
            ("Account#", "Unique ID of the patient in AuroraEHR"),
            ("Accession#", "The unique ID of the appointment for which these alerts are associated. If blank, the alert always pertains to the patient and is used as a default for new/subsequent appointments."),
            ("Alert Code", "Code for this type of alert in AuroraEHR"),
            ("Description", "The description of the alert."),
            ("Comment", "Any additional information beyond the description."),
            ("Date Record was Created", "Date of the record's entry. Formatted MM/dd/yyyy."),
            ("Date Record was last Updated", "Date of the record's last update. Formatted MM/dd/yyyy."),
        ]
    },
    {
        "entity_name": "Allergies",
        "file_name": "Allergies.csv",
        "format": "CSV",
        "category": "Allergies",
        "fields": [
            ("Account#", "Unique ID of the patient in AuroraEHR"),
            ("Accession#", "The unique ID of the appointment for which the allergies are associated. If blank, the allergy is part of the list stored at the patient level, containing the newest information and action as a default for new/subsequent appointments."),
            ("Allergen Name", "The substance or medication to which the patient has an allergy."),
            ("Onset Date", "Date when allergy was reported to have started. Formatted MM/dd/yyyy"),
            ("Reaction", "Description of the patient's allergic reaction"),
            ("Reaction SNOMED", "SNOMED code of the allergic reaction. May be blank if not known."),
            ("Severity Level", "The severity of the patient's reaction to the allergen.", ["Mild", "Moderate", "Severe", "Unknown"]),
            ("RXNORM Code", "If the allergen is a medication, this column contains medication's RXNORM code. May be blank if not known."),
            ("Status", "The status of the allergy.", ["Active", "Inactive"]),
            ("Date Record was Created", "Date of the record's entry. Formatted MM/dd/yyyy"),
            ("Date Record was last Updated", "Date of the record's last update. Formatted MM/dd/yyyy."),
        ]
    },
    {
        "entity_name": "Immunizations",
        "file_name": "Immunizations.csv",
        "format": "CSV",
        "category": "Immunizations",
        "fields": [
            ("Account#", "Unique ID of the patient in AuroraEHR"),
            ("Accession#", "The unique ID of the appointment with which the immunizations are associated. If blank, the immunization is used as a default for new/subsequent appointments."),
            ("Immunization", "The name and code of the vaccine or presumed immunity"),
            ("Status", "The administration status. Used to indicate whether the vaccine was administered, not administered, is historical information, etc.", [
                "Complete", "Refused", "not administered (presumed immunity)", "partially administered",
                "new immunization record", "ERROR: entered on this charge in error",
                "historical information - patient", "historical information - source unspecified",
                "historical information - from other provider", "historical information - from parent's written record",
                "historical information - from parent's recall", "historical information - from other registry",
                "historical information - from birth certificate", "historical information - from school record",
                "historical information - from public agency"
            ]),
            ("Lot Number", "Manufacturer's lot number for a vaccine"),
            ("Manufacturer", "The manufacturer of the vaccine, if known. In the case of vaccines recorded from a patient's verbal report, this might not be available."),
            ("Route", "How the vaccine was administered.", [
                "intramuscular", "subcutaneous", "nasal", "intradermal",
                "intravenous", "oral", "transdermal", "other/miscellaneous", "N/A"
            ]),
            ("Site", "Administration site.", [
                "left arm", "right arm", "left thigh", "right thigh",
                "left deltoid", "right deltoid", "left gluteous medius", "right gluteous medius",
                "left vastus lateralis", "right vastus lateralis",
                "left lower forearm", "right lower forearm", "N/A"
            ]),
            ("Units", "The amount of the vaccine administered (numeric)"),
            ("Administered By", "The name of the person who administered the vaccine."),
            ("Administered Date", "The date the vaccine was administered. Formatted MM/dd/yyyy."),
            ("Administered Time", "The time the vaccine was administered. Formatted hh:mm:ss am."),
            ("Refusal Reason", "If the vaccine was refused, reason for refusal.", [
                "parental decision", "religious exemption", "patient decision", "other", "N/A"
            ]),
            ("Refusal Note", "Any additional information for vaccine refusal."),
            ("Note", "General, overall, notes."),
            ("Date Record was Created", "Date of the record entry. Formatted MM/dd/yyyy."),
            ("Date Record was last Updated", "Date of the record last update. Formatted MM/dd/yyyy."),
        ]
    },
    {
        "entity_name": "Medications",
        "file_name": "Medications.pdf",
        "format": "PDF",
        "category": "Medications",
        "fields": [
            ("Medication", "Name of the medication, along with dose and unit information."),
            ("Duration", "Describes the length of time during which the medication should be taken."),
            ("Start Date", "Start date of taking the medication. Formatted MM/dd/yyyy."),
            ("Stop Date", "Stop date of taking the medication. Formatted MM/dd/yyyy."),
            ("Number of Refills", "Number of refills allowed for the medications"),
            ("Last Fill Date", "Date of the last refill. Formatted MM/dd/yyyy."),
        ]
    },
    {
        "entity_name": "Problems",
        "file_name": "Problems.csv",
        "format": "CSV",
        "category": "Problems/Diagnoses",
        "fields": [
            ("Account#", "Unique ID of the patient in AuroraEHR"),
            ("Accession#", "The unique ID of the appointment for which the problem is associated. If blank, the problem is used as a default for new/subsequent appointments."),
            ("Problem Code (SNOMED)", "The SNOMED code of the problem."),
            ("Problem Code (ICD10)", "The ICD10 code of the problem."),
            ("Description", "Description of the problem. The default value comes from the code above, but the user who entered the problem may have modified the description as needed."),
            ("Onset Date", "Onset date of the problem. Formatted MM/dd/yyyy."),
            ("Resolved Date", "If valued, the date the problem was resolved. Formatted MM/dd/yyyy."),
            ("Note", "Any useful information reported by the staff and/or patient."),
            ("Status", "The status of the problem.", ["Active", "Inactive", "Resolved", "Chronic"]),
            ("Date Record was Created", "Date of the record entry. Formatted MM/dd/yyyy."),
            ("Date Record was last Updated", "Date of the record last update. Formatted MM/dd/yyyy."),
        ]
    },
    {
        "entity_name": "ReviewOfSystems",
        "file_name": "ReviewOfSystems.csv",
        "format": "CSV",
        "category": "Review of Systems",
        "fields": [
            ("Account#", "Unique ID of the patient in AuroraEHR"),
            ("Accession#", "The unique ID of the appointment for which this section's clinical data is associated."),
            ("ROS", "The review of systems text."),
            ("Date Record was Created", "Date of the record entry"),
            ("Date Record was Last Updated", "Date of record last change"),
        ]
    },
    {
        "entity_name": "SocialHistory",
        "file_name": "SocialHistory.csv",
        "format": "CSV",
        "category": "Social/Family/Surgical History",
        "fields": [
            ("Account#", "Unique ID of the patient in AuroraEHR"),
            ("Accession#", "The unique ID of the appointment with which the Social History is associated."),
            ("Chance of Pregnancy?", "Might the patient be pregnant? Yes or no."),
            ("Last Menstrual Period Date", "If applicable, the date of the patient's last menstrual period. Formatted MM/dd/yyyy."),
            ("IVDA?", "Does the patient have a history of intravenous drug abuse? Yes or no."),
            ("Alcohol Use?", "Does the patient consume alcohol? Yes or no. Any additional notes may be recorded in the comments field."),
            ("Victim of Abuse?", "Is the patient a victim of physical or emotional abuse?", [
                "Patient responded yes", "Patient responded no", "Patient wasn't asked or didn't respond"
            ]),
            ("Smoking Status", "Patient's reported smoking status followed by the appropriate SNOMED code.", [
                "Current daily smoker", "Current some day smoker", "Former smoker",
                "Never smoker", "Smoker; current status unknown", "Unknown if ever smoked",
                "Heavy tobacco smoker (10+ cigarettes a day)", "Light tobacco smoker (<10 cigarettes a day)",
                "Screening not indicated (situation)"
            ]),
            ("Smoking Status Comment", "Smoking status explanation"),
            ("Family History of Anesthesia Complications?", "Does the patient or the patient's family have a history of anesthesia complications? Yes or no."),
            ("Comment", "Additional remarks or general social history notes."),
            ("Date Record was Created", "Date of the record entry. Formatted MM/dd/yyyy"),
            ("Date Record was Last Updated", "Date of record last change. Formatted MM/dd/yyyy"),
        ]
    },
    {
        "entity_name": "FamilyHistory",
        "file_name": "FamilyHistory.csv",
        "format": "CSV",
        "category": "Social/Family/Surgical History",
        "fields": [
            ("Account#", "Unique ID of the patient in AuroraEHR"),
            ("Accession#", "The unique ID of the appointment for which the family history is associated."),
            ("Condition", "Name of the condition"),
            ("Code", "Code of the condition"),
            ("Code System", "Code system of the condition code"),
            ("Affected Family Member", "Relationship of person with the condition"),
            ("Onset Date", "Date of onset, if known"),
            ("Note", "Comments or notes pertaining to this family history record."),
            ("Date Record was Created", "Date of the record entry. Formatted MM/dd/yyyy."),
            ("Date Record was Last Updated", "Date of record last change. Formatted MM/dd/yyyy."),
        ]
    },
    {
        "entity_name": "SurgicalHistory",
        "file_name": "SurgicalHistory.csv",
        "format": "CSV",
        "category": "Social/Family/Surgical History",
        "fields": [
            ("Account#", "Unique ID of the patient in AuroraEHR"),
            ("Accession#", "The unique ID of the appointment for which the surgical history was recorded."),
            ("Code", "Procedure code"),
            ("Code System", "Coding system used, such as SNOMED, CPT, etc."),
            ("Description", "Description of the procedure"),
            ("Date", "Free form field for when the procedure took place. The date is the best the user can recall."),
            ("Note", "Any additional notes or comments about this procedure."),
            ("Date Record was Created", "Date of the record entry. Formatted MM/dd/yyyy."),
            ("Date Record was Last Updated", "Date of record last change. Formatted MM/dd/yyyy."),
        ]
    },
    {
        "entity_name": "Orders",
        "file_name": "ImagingOrders.pdf / LabOrders.pdf / PathologyOrders.pdf / TherapyOrders.pdf",
        "format": "PDF",
        "category": "Orders: Tests and Results",
        "fields": [
            ("Order#", "The unique ID of a lab, imaging, pathology, therapy order."),
            ("Order Instructions", "Any specific instructions"),
            ("Ordered", "The date, formatted MM/dd/yy, and time, formatted hh:mm am, for when the order was placed."),
            ("Test", "The specific tests in an order."),
            ("Code", "For labs, the LOINC code of the ordered test. For imaging, the CPT code of the ordered test. For pathology, the LOINC code of the ordered test."),
        ]
    },
    {
        "entity_name": "VitalSigns",
        "file_name": "VitalSigns.csv",
        "format": "CSV",
        "category": "Vital Signs",
        "fields": [
            ("Account#", "Unique ID of the patient in AuroraEHR"),
            ("Accession#", "The unique ID of the appointment for which the vital signs are associated."),
            ("Capture Date", "Date when the vital signs were captured. Formatted MM/dd/yyyy."),
            ("Capture Time", "Time when the vital signs were captured. Formatted hh:mm:ss am."),
            ("Systolic Blood Pressure", "Numeric value of the patient's systolic blood pressure."),
            ("Diastolic Blood Pressure", "Numeric value of the patient's diastolic blood pressure."),
            ("Blood Pressure Site", "Location of blood pressure measurement. Is a free form text field."),
            ("Blood Pressure Side", "Side of the blood pressure measurement site.", ["Left", "Right", "N/A"]),
            ("Blood Sugar", "Numeric value of the patient's blood sugar."),
            ("Heart Rate", "Numeric value of the patient's heart rate in bpm."),
            ("Height", "The numeric value of the patient's height."),
            ("Height Scale", "Scale (cm/in) used for height"),
            ("Weight", "The numeric value of the patient's weight."),
            ("Weight Scale", "Scale (lbs/kg) used for weight"),
            ("BMI", "Numeric value of the patient's body mass index."),
            ("Oxygen Level", "spO2 reading of the patient's O2 saturation."),
            ("Supplemental O2?", "Is the patient using supplemental oxygen? Yes or no."),
            ("Inhaled O2 Concentration %", "If the patient is taking supplemental oxygen, the percentage of oxygen given. A numeric value from zero to 100."),
            ("Pain Scale", "The reported level of pain the patient is in. A numeric value from zero to 10, including N/A."),
            ("Respiratory Rate", "The patient's respiratory rate in the number of breaths per minute."),
            ("Temperature", "Numeric value of the patient's temperature."),
            ("Temperature Scale", "Scale (C/F) used for temperature"),
            ("Shoe Size", "For podiatry practices, the numeric value of the size of shoe the patient wears."),
            ("Screening Not Done", "If vitals were not captured, the reason why they were not captured.", [
                "Patient refused screening", "Procedure contraindicated (situation)", "Medical contraindication"
            ]),
            ("Comment", "Any additional comments that should be noted."),
        ]
    },
    {
        "entity_name": "ImplantedDevices",
        "file_name": "ImplantedDevices.csv",
        "format": "CSV",
        "category": "Additional Clinical Data",
        "fields": [
            ("Account#", "Unique ID of the patient in AuroraEHR"),
            ("Accession#", "The unique ID of the appointment with which the implanted devices is associated."),
            ("Device Type (SNOMED Code)", "The SNOMED code of the device's type."),
            ("Description", "Text description of the device"),
            ("Company Name", "Manufacturer of the device"),
            ("Brand Name", "Device brand name"),
            ("Lot Number", "Manufacturer's lot number for the device"),
            ("Catalog Number", "Catalog number of the device"),
            ("Model Number", "Model number of the device"),
            ("Serial Number", "Serial number of the device"),
            ("Unique Device ID", "ID of the implanted device"),
            ("Expiration Date", "Date of implant expiration"),
            ("Manufactured Date", "Date of implant creation"),
            ("Placement Date", "Date of implantation"),
            ("Placement Site", "Location of the implant"),
            ("Placement Laterality", "Indication of location side, if relevant"),
            ("Placement Provider", "Provider who performed the implantation"),
            ("Placement Note", "Any further notes regarding placement"),
            ("MRI Safety", "MRI safety status.", ["MRI Safe", "MRI Conditional", "MRI Unsafe"]),
            ("Device ID", "A number or identifier that denotes a specific kind of device."),
            ("Status", "A device has either an active or inactive status."),
            ("Date Record was Created", "Date of the record entry"),
        ]
    },
    {
        "entity_name": "PatientEducation",
        "file_name": "PatientEducation.csv",
        "format": "CSV",
        "category": "Additional Clinical Data",
        "fields": [
            ("Account#", "Unique ID of the patient in AuroraEHR"),
            ("Accession#", "The unique ID of the appointment for which the education material given to the patient is associated."),
            ("Type", "What the educational material is in reference to.", ["general", "patient medication", "patient problem", "patient lab"]),
            ("Description", "Description of the educational material"),
            ("URL", "Link to the material"),
            ("Date/Time Given", "Date and time the educational material was given to the patient. Formatted MM/dd/yyyy hh:mm:ss am"),
            ("Given By", "Name of the user who gave the educational material to the patient."),
            ("Date Record was Created", "The date the record was created. Formatted MM/dd/yyyy."),
            ("Date Record was Last Updated", "The date the record was last updated. Formatted MM/dd/yyyy."),
        ]
    },
    {
        "entity_name": "PostAppointment",
        "file_name": "PostAppointment.csv",
        "format": "CSV",
        "category": "Additional Clinical Data",
        "fields": [
            ("Account#", "Unique ID of the patient in AuroraEHR"),
            ("Accession#", "The unique ID of the appointment for which this section's clinical data is associated."),
            ("Bleeding", "Patient's response when questioned regarding bleeding"),
            ("Drainage", "Patient's response when questioned regarding drainage"),
            ("Drinking Water", "Patient's response when questioned regarding drinking water"),
            ("Eating/Drinking Changes", "Notes regarding any changes the patient has experienced in fluid or food intake."),
            ("Fever", "Patient's response when questioned regarding fever"),
            ("Nausea", "Patient's response when questioned regarding nausea"),
            ("Needlepoint Redness", "Patient's response when questioned regarding needlepoint redness"),
            ("Pain Medications", "Patient's response when questioned regarding pain medications used"),
            ("Sore Throat", "Patient's response when questioned regarding a sore throat"),
            ("Swelling", "Patient's response when questioned regarding swelling"),
            ("Unusual/Excessive Pain", "Patient's response when questioned regarding any unusual or excessive pain."),
            ("Follow-Up Phone Call Comment", "Comments regarding the follow-up call with the patient, from the person who contacted the patient."),
            ("Post-Discharge Comment", "Comments regarding any details or events that occurred after discharge."),
            ("Date Record Entered", "Date of the record entry. Formatted MM/dd/yyyy."),
            ("Date Record Last Changed", "Date of record last change. Formatted MM/dd/yyyy."),
        ]
    },
    {
        "entity_name": "PostOp",
        "file_name": "PostOp.csv",
        "format": "CSV",
        "category": "Additional Clinical Data",
        "fields": [
            ("Account#", "Unique ID of the patient in AuroraEHR"),
            ("Accession#", "The unique ID of the appointment with which this section's clinical data is associated."),
            ("Anesthesia Given?", "Was anesthesia given to the patient? Yes or no."),
            ("Anesthesia Type", "If given, the type of anesthesia given."),
            ("Activity Arrival", "Patient's ability to move their extremities upon arrival for the appointment.", [
                "Able to move 4 extremities: voluntarily or on command",
                "Able to move 2 extremities: voluntarily or on command",
                "Able to move 0 extremities: voluntarily or on command", "N/A"
            ]),
            ("Activity Discharge", "Patient's ability to move their extremities upon discharge from the appointment.", [
                "Able to move 4 extremities: voluntarily or on command",
                "Able to move 2 extremities: voluntarily or on command",
                "Able to move 0 extremities: voluntarily or on command", "N/A"
            ]),
            ("Respiration Arrival", "Patient's ability to breathe upon arrival for the appointment.", [
                "Able to cough and breathe deeply", "Dyspnea or limited breathing", "Apnea", "N/A"
            ]),
            ("Respiration Discharge", "Patient's ability to breathe upon discharge from the appointment.", [
                "Able to cough and breathe deeply", "Dyspnea or limited breathing", "Apnea", "N/A"
            ]),
            ("Circulation Discharge", "The patient's systolic blood pressure relative to their pre-anesthetic BP.", [
                "systolic BP +/- 20 mm/hg of pre-anesthetic BP",
                "systolic BP +/- 21-49 mm/hg of pre-anesthetic BP",
                "systolic BP +/- 50 mm/hg of pre-anesthetic BP", "N/A"
            ]),
            ("Consciousness Arrival", "The patient's level of consciousness upon arriving for the appointment.", [
                "Fully awake", "Arousable on calling", "Not responding", "N/A"
            ]),
            ("Consciousness Discharge", "The patient's level of consciousness upon discharge from the appointment.", [
                "Fully awake", "Arousable on calling", "Not responding", "N/A"
            ]),
            ("O2 Saturation Arrival", "The patient's oxygen saturation level upon arrival for the appointment.", [
                "Able to maintain SpO2 above 92% on RA",
                "Needs supplemental O2 to maintain SpO2 > 90%",
                "SpO2 < than 90% with O2 supplementation", "N/A"
            ]),
            ("O2 Saturation Discharge", "The patient's oxygen saturation level upon discharge from the appointment.", [
                "Able to maintain SpO2 above 92% on RA",
                "Needs supplemental O2 to maintain SpO2 > 90%",
                "SpO2 < than 90% with O2 supplementation", "N/A"
            ]),
            ("Left Hand Grip", "Vascular assessment of the patient's left hand grip."),
            ("Right Hand Grip", "Vascular assessment of the patient's right hand grip."),
            ("Left Brachial Pulse", "Vascular assessment of the patient's brachial pulse on their left arm."),
            ("Right Brachial Pulse", "Vascular assessment of the patient's brachial pulse on their right arm."),
            ("Left Radial Pulse", "Vascular assessment of the patient's radial pulse on their left wrist."),
            ("Right Radial Pulse", "Vascular assessment of the patient's radial pulse on their right wrist."),
            ("Left Dorsalis Pulse", "Vascular assessment of the patient's dorsalis pulse on their left foot."),
            ("Right Dorsalis Pulse", "Vascular assessment of the patient's dorsalis pulse on their right foot."),
            ("Left Posterior Pulse", "Vascular assessment of the patient's posterior pulse on their left ankle."),
            ("Right Posterior Pulse", "Vascular assessment of the patient's posterior pulse on their right ankle."),
            ("Color & Temp of Left Hand", "The color and temperature of the patient's left hand."),
            ("Color & Temp of Right Hand", "The color and temperature of the patient's right hand."),
            ("Color & Temp of Left Foot", "The color and temperature of the patient's left foot."),
            ("Color & Temp of Right Foot", "The color and temperature of the patient's right foot."),
            ("Number of Sutures", "Number of sutures the patient received"),
            ("Oriented X3 (Person, Place, and Time)", "Is the patient alert and oriented to who they are, where they are, and the current date?"),
            ("Discharge Date", "Date of patient's discharge. Formatted MM/dd/yyyy."),
            ("Discharge Time", "Time of patient's discharge. Formatted hh:mm:ss am."),
            ("Dressing On Discharge", "Describes any dressings which were present at the time of patient discharge."),
            ("Transport to Recovery By", "The method by which the patient was transported to recovery.", [
                "Independent Ambulation", "Wheel Chair", "Stretcher", "Walker", "Cane"
            ]),
            ("Time Arrived in Recovery", "The time the patient arrived in recovery. Formatted hh:mm:ss am."),
            ("Initial Fluid Intake - Intra Procedure - D5W", "Comment format"),
            ("Initial Fluid Intake - Recovery - D5W", "Comment format"),
            ("Initial Fluid Intake - Intra Procedure - NS", "Comment format"),
            ("Initial Fluid Intake - Recovery - NS", "Comment format"),
            ("Initial Fluid Intake - Intra Procedure - Contrast", "Comment format"),
            ("Initial Fluid Intake - Recovery - Contrast", "Comment format"),
            ("Initial Fluid Intake - Intra Procedure - Oral", "Comment format"),
            ("Initial Fluid Intake - Recovery - Oral", "Comment format"),
            ("Initial Fluid Intake Comment", "Comment format"),
            ("Comment", "Any additional notes regarding the patient's post-op or the values recorded."),
            ("Date Record Entered", "Date of the record entry. Formatted MM/dd/yyyy."),
            ("Date Record Last Changed", "Date of record last change. Formatted MM/dd/yyyy."),
        ]
    },
    {
        "entity_name": "PreOp",
        "file_name": "PreOp.csv",
        "format": "CSV",
        "category": "Additional Clinical Data",
        "fields": [
            ("Account#", "Unique ID of the patient in AuroraEHR"),
            ("Accession#", "The unique ID of the appointment for which this section's clinical data is associated."),
            ("Activity", "Patient's ability to move their extremities upon arrival for the appointment.", [
                "Able to move 4 extremities: voluntarily or on command",
                "Able to move 2 extremities: voluntarily or on command",
                "Able to move 0 extremities: voluntarily or on command", "N/A"
            ]),
            ("Respiration", "Patient's ability to breathe upon arrival for the appointment.", [
                "Able to cough and breathe deeply", "Dyspnea or limited breathing", "Apnea", "N/A"
            ]),
            ("Consciousness", "The patient's level of consciousness upon arriving for the appointment.", [
                "Fully awake", "Arousable on calling", "Not responding", "N/A"
            ]),
            ("O2 Saturation", "The patient's oxygen saturation level upon arrival for the appointment.", [
                "Able to maintain SpO2 above 92% on RA",
                "Needs supplemental O2 to maintain SpO2 > 90%",
                "SpO2 < than 90% with O2 supplementation", "N/A"
            ]),
            ("Dressing On Arrival", "Describes any dressings which were present at the time of patient arrival."),
            ("Left Hand Grip", "Vascular assessment of the patient's left hand grip."),
            ("Right Hand Grip", "Vascular assessment of the patient's right hand grip."),
            ("NPO?", "This question will have a yes/no answer."),
            ("Last PO", "Last oral intake"),
            ("Left Brachial Pulse", "Vascular assessment of the patient's brachial pulse on their left arm."),
            ("Right Brachial Pulse", "Vascular assessment of the patient's brachial pulse on their right arm."),
            ("Left Radial Pulse", "Vascular assessment of the patient's radial pulse on their left wrist."),
            ("Right Radial Pulse", "Vascular assessment of the patient's radial pulse on their right wrist."),
            ("Left Dorsalis Pulse", "Vascular assessment of the patient's dorsalis pulse on their left foot."),
            ("Right Dorsalis Pulse", "Vascular assessment of the patient's dorsalis pulse on their right foot."),
            ("Left Posterior Pulse", "Vascular assessment of the patient's posterior pulse on their left ankle."),
            ("Right Posterior Pulse", "Vascular assessment of the patient's posterior pulse on their right ankle."),
            ("Color & Temp of Left Hand", "The color and temperature of the patient's left hand."),
            ("Color & Temp of Right Hand", "The color and temperature of the patient's right hand."),
            ("Color & Temp of Left Foot", "The color and temperature of the patient's left foot."),
            ("Color & Temp of Right Foot", "The color and temperature of the patient's right foot."),
            ("Transportation To Procedure Room By", "The method by which the patient was transported to the procedure room.", [
                "Independent Ambulation", "Wheel Chair", "Stretcher", "Walker", "Cane"
            ]),
            ("Patient Arrived By", "Method of patient's delivery"),
            ("Comment", "Text of the comment for the entry"),
            ("Date Record Entered", "Date of the record entry"),
            ("Date Record Last Changed", "Date of record last change"),
        ]
    },
    {
        "entity_name": "PreopProcedureNotes",
        "file_name": "PreopProcedureNotes.csv",
        "format": "CSV",
        "category": "Additional Clinical Data",
        "fields": [
            ("Account#", "Unique ID of the patient in AuroraEHR"),
            ("Accession#", "The unique ID of the appointment for which this section's clinical data is associated."),
            ("Translations Provided By", "Name of the translator, if any"),
            ("Verbal Consent Obtained From", "Name of the person who gave consent"),
            ("Access Fistula?", "Yes/no answer"),
            ("Access Graft?", "Yes/no answer"),
            ("Access Left Arm?", "Yes/no answer"),
            ("Access Right Arm?", "Yes/no answer"),
            ("Access Other?", "Place of the other access"),
            ("Catheter Left Subclavian?", "Yes/no answer"),
            ("Catheter Right Subclavian?", "Yes/no answer"),
            ("Catheter Left Thigh?", "Yes/no answer"),
            ("Catheter Right Thigh?", "Yes/no answer"),
            ("Catheter Order Given?", "Yes/no answer"),
            ("Catheter Provider Vital Signs Aware?", "Yes/no answer"),
            ("Anxiety Reduction Explained Procedure?", "Yes/no answer"),
            ("Anxiety Reduction Attained?", "Yes/no answer"),
            ("Anxiety Reduction Allowed Time for Patient Questions?", "Yes/no answer"),
            ("Anxiety Reduction Encouraged to Verbalize Concerns?", "Yes/no answer"),
            ("Anxiety Reduction RN Signature", "Stamp of electronic signature with RN name"),
            ("Is a Declot Procedure?", "Yes/no answer"),
            ("Declot Procedure Performed By", "ID of the provider"),
            ("Declot Procedure Sterility Monitored/Maintained?", "Yes/no answer"),
            ("Declot Procedure No Breaks in Sterility?", "Yes/no answer"),
            ("Declot Alteplase Heparin Given Time", "Time of the injection"),
            ("Declot Procedure No Thrombolytics?", "Yes/no answer"),
            ("Declot Procedure RN Signature", "Stamp of electronic signature with RN name"),
            ("Antibiotics Ancef Given?", "Yes/no answer"),
            ("Antibiotics Clindamycin Given?", "Yes/no answer"),
            ("Antibiotics Vancomycin Given?", "Yes/no answer"),
            ("Antibiotics Levaquin Given?", "Yes/no answer"),
            ("Antibiotics Administered Via", "Place of administering the antibiotics used"),
            ("Antibiotics Administered Time", "Time of administering the antibiotics used"),
            ("Antibiotics RN Signature", "Stamp of electronic signature with RN name"),
            ("Date Record Entered", "Date of the record entry"),
            ("Date Record Last Changed", "Date of record last change"),
        ]
    },
    {
        "entity_name": "ProviderOrders",
        "file_name": "ProviderOrders.csv",
        "format": "CSV",
        "category": "Additional Clinical Data",
        "fields": [
            ("Account#", "Unique ID of the patient in AuroraEHR"),
            ("Accession#", "The unique ID of the appointment for which this section's clinical data is associated."),
            ("Puncture Left Arm?", "Yes/no answer"),
            ("Puncture Right Arm?", "Yes/no answer"),
            ("Puncture Left Groin?", "Yes/no answer"),
            ("Puncture Right Groin?", "Yes/no answer"),
            ("Puncture Left Jugular?", "Yes/no answer"),
            ("Puncture Right Jugular?", "Yes/no answer"),
            ("Puncture Other", "A description of where the puncture was placed if not on the patient's arm, groin, or jugular"),
            ("Catheter Left Subclavian?", "Location of catheter placement; yes/no answer"),
            ("Catheter Right Subclavian?", "Location of catheter placement; yes/no answer"),
            ("Catheter Left Thigh?", "Location of catheter placement; yes/no answer"),
            ("Catheter Right Thigh?", "Location of catheter placement; yes/no answer"),
            ("Discharge Disposition", "Patient's disposition at the time of discharge"),
            ("Discharge Diagnoses (SNOMEDCT)", "Diagnoses with their SNOMED codes"),
            ("Refer To", "Referring provider name"),
            ("Refer To Date", "Date of the referral"),
            ("Referral Reason", "Reason for the referral"),
            ("Functional Status", "The SNOMED code and description of the patient's functional status."),
            ("Functional Status Effective Date", "Date for functional status check"),
            ("Functional Status Note", "Note on functional status"),
            ("Cognitive Status Status", "The SNOMED code and description of the patient's cognitive status."),
            ("Cognitive Status Effective Date", "Date for cognitive status check"),
            ("Cognitive Status Note", "Note on cognitive status"),
            ("Free Text Order", "Order of free text"),
            ("Free Text Order Provider Signature", "Stamp of electronic signature with provider name"),
            ("Free Text Order RN Signature", "Stamp of electronic signature with RN name"),
            ("Ancef Medication Given?", "Was 1g of Ancef, in 10ml of sterile water, IV STAT given to the patient? yes/no"),
            ("Clindamycin Medication Given", "Was 600mg of Clindamycin, in 20ml of normal saline, IV STAT, given to the patient? yes/no"),
            ("Vancomycin Medication Given", "Was 1g of Vancomycin, in 200ml of normal saline, IV over 1 hr, given to the patient? yes/no"),
            ("Tylenol Medication Given", "Was 500mg of Tylenol Extra Strength, as 2 caplets, PO STAT, given to the patient? yes/no"),
            ("Antibiotic Provider Signature", "Stamp of electronic signature with provider name"),
            ("Antibiotic RN Signature", "Stamp of electronic signature with RN name"),
            ("Heparin Quantity Given 1000 Units via Arterial Port", "The quantity of 1000 Units/ml of Heparin given to the patient via their arterial port, post-procedure"),
            ("Heparin Quantity Given 5000 Units via Arterial Port", "The quantity of 5000 Units/ml of Heparin given to the patient via their arterial port, post-procedure"),
            ("Heparin Quantity Given 1000 Units via Venous Port", "The quantity of 1000 Units/ml of Heparin given to the patient via their venous port, post-procedure"),
            ("Heparin Quantity Given 5000 Units via Venous Port", "The quantity of 5000 Units/ml of Heparin given to the patient via their venous port, post-procedure"),
            ("Heparin Provider Signature", "Stamp of electronic signature with provider name"),
            ("Heparin RN Signature", "Stamp of electronic signature with RN name"),
            ("Suture Remove In Minutes", "Suture removal time in minutes"),
            ("Discharge When Stable and Provide Instructions?", "Yes/no answer"),
            ("Exempt From Being Discharged into the Company of a Responsible Adult?", "Yes/no answer"),
            ("Patient Transferred to Another Facility?", "Yes/no answer"),
            ("Discharge Provider Signature", "Stamp of electronic signature with provider name"),
            ("Discharge RN Signature", "Stamp of electronic signature with RN name"),
            ("Date Record Entered", "Date of the record entry"),
            ("Date Record Last Changed", "Date of record last change"),
        ]
    },
    {
        "entity_name": "SurgicalChecklist",
        "file_name": "SurgicalChecklist.csv",
        "format": "CSV",
        "category": "Additional Clinical Data",
        "fields": [
            ("Account#", "Unique ID of the patient in AuroraEHR"),
            ("Accession#", "The unique ID of the appointment for which this section's clinical data is associated."),
            ("Patient Preop Confirmation?", "Yes/no answer"),
            ("RN Preop Signature", "Stamp of electronic signature with RN name"),
            ("Patient Procedure Confirmation?", "Yes/no answer"),
            ("RN Procedure Signature", "Stamp of electronic signature with RN name"),
            ("RN Postop Signature", "Stamp of electronic signature with RN name"),
            ("Signature", "Stamp of electronic signature with surgeon name"),
            ("Patient Recovery Management Concerns", "A text field containing remarks on recovery management"),
            ("Prophylaxis Given Within 60 Minutes?", "Yes/no answer"),
            ("RN History Physical Confirmation?", "Yes/no answer"),
            ("RN Instrument Counts Completed?", "Yes/no answer"),
            ("RN Preanesthesia Assessment Confirmation?", "Yes/no answer"),
            ("Equipment Problems Addressed?", "Yes/no answer"),
            ("Site Marked And Visible?", "Yes/no answer"),
            ("Team Members Introduced?", "Yes/no answer"),
            ("Date Record was Created", "Date of the record entry"),
            ("Date Record was Last Updated", "Date of record last change"),
        ]
    },
    {
        "entity_name": "SutureInfo",
        "file_name": "SutureInfo.csv",
        "format": "CSV",
        "category": "Additional Clinical Data",
        "fields": [
            ("Account#", "Unique ID of the patient in AuroraEHR"),
            ("Accession#", "The unique ID of the appointment for which the suture info is associated."),
            ("Comment", "Text of the comment for the entry"),
            ("Date Captured", "Date of the suture"),
            ("Time Captured", "Time of the suture"),
            ("Signature", "Stamp of electronic signature with surgeon name"),
            ("Dry Intact Dressing?", "Yes/no answer"),
            ("Pain or Active Bleeding?", "Yes/no answer"),
            ("Redness or Swelling?", "Yes/no answer"),
            ("Remove Sutures?", "Yes/no answer"),
            ("Date Record was Created", "Date of the record entry"),
            ("Date Record was Last Updated", "Date of record last change"),
        ]
    },
]


def build_inventory():
    """Build the full entity inventory from manually curated data."""
    total_fields = 0
    fields_with_desc = 0
    fields_with_values = 0
    categories = {}
    
    for entity in ENTITIES:
        fields = []
        for item in entity["fields"]:
            field = {
                "name": item[0],
                "description": item[1],
            }
            if len(item) > 2:
                field["possible_values"] = item[2]
            fields.append(field)
        
        entity_obj = {
            "entity_name": entity["entity_name"],
            "file_name": entity["file_name"],
            "format": entity["format"],
            "category": entity["category"],
            "field_count": len(fields),
            "fields": fields
        }
        
        # Update stats
        total_fields += len(fields)
        for f in fields:
            if f.get("description"):
                fields_with_desc += 1
            if f.get("possible_values"):
                fields_with_values += 1
        
        cat = entity["category"]
        if cat not in categories:
            categories[cat] = {"entity_count": 0, "field_count": 0}
        categories[cat]["entity_count"] += 1
        categories[cat]["field_count"] += len(fields)
        
        # Replace raw tuples with field objects
        entity["fields"] = fields
        entity["field_count"] = len(fields)
    
    summary = {
        "total_entities": len(ENTITIES),
        "total_fields": total_fields,
        "fields_with_descriptions": fields_with_desc,
        "fields_with_possible_values": fields_with_values,
        "description_coverage_pct": round(fields_with_desc / total_fields * 100, 1) if total_fields > 0 else 0,
        "categories": categories
    }
    
    return {
        "source": "AuroraEHR_b10_EHI_Export_Documentation.pdf",
        "pages": 39,
        "summary": summary,
        "entities": ENTITIES
    }


def main():
    inventory = build_inventory()
    
    with open(OUTPUT, 'w') as f:
        json.dump(inventory, f, indent=2)
    
    s = inventory["summary"]
    print(f"Entities: {s['total_entities']}")
    print(f"Total fields: {s['total_fields']}")
    print(f"Fields with descriptions: {s['fields_with_descriptions']} ({s['description_coverage_pct']}%)")
    print(f"Fields with enumerated values: {s['fields_with_possible_values']}")
    print()
    print("Category breakdown:")
    for cat, stats in s['categories'].items():
        print(f"  {cat}: {stats['entity_count']} entities, {stats['field_count']} fields")
    print()
    print("Entity details:")
    for e in ENTITIES:
        print(f"  {e['entity_name']} ({e['file_name']}): {e['field_count']} fields [{e['format']}]")


if __name__ == "__main__":
    main()
