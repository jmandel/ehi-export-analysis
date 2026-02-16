#!/usr/bin/env python3
"""Parse SolidPractice b10 exportable data content PDF and produce structured inventory.

Column assignments verified using pdftotext -bbox analysis of exact X-mark coordinates:
- Header "Computable PDF Export" at xMin=455-556
- Header "CCD XML Export" at xMin=565-635
- Header "JSON" at xMin=667-691
- X at xMin≈597 → CCD XML Export (within 565-635 range)
- X at xMin≈676 → JSON (within 667-691 range)
- X at xMin≈503 → Computable PDF Export (within 455-556 range)

Each data element is marked for export in exactly ONE format.
"""

import json

categories = {
    (1, 29): "Demographics",
    (30, 30): "Medications",
    (31, 35): "Pharmacy",
    (36, 37): "Social History",
    (38, 38): "Immunizations",
    (39, 39): "Problems",
    (40, 40): "Procedures",
    (41, 41): "Vitals",
    (42, 42): "Allergies",
    (43, 44): "Providers/Care Team",
    (45, 47): "Labs & Imaging",
    (48, 48): "Uploaded Documents",
    (49, 56): "Insurance",
    (57, 65): "Guarantor",
    (66, 71): "Appointments",
    (72, 87): "Billing/Receipts",
}

def get_category(num):
    for (lo, hi), cat in categories.items():
        if lo <= num <= hi:
            return cat
    return "Unknown"

# Format: (number, name, description, computable_pdf, ccd_xml, json)
# Column assignments based on bbox coordinate analysis
raw_elements = [
    # Page 1: items 1-30, all at xMin=597 → CCD XML Export
    (1, "Patient ID", "Patient ID from Solid Practice EMR", False, True, False),
    (2, "First Name", "First name of patient", False, True, False),
    (3, "Last Name", "Last name of patient", False, True, False),
    (4, "Middle Name", "Middle name of patient", False, True, False),
    (5, "Suffix", "Suffix of patient name", False, True, False),
    (6, "Date of Birth", "Patient date of birth", False, True, False),
    (7, "Gender", "Gender of patient", False, True, False),
    (8, "Race", "Patient race", False, True, False),
    (9, "Ethnicity", "Patient ethnicity", False, True, False),
    (10, "Marital Status", "Marital status of patient", False, True, False),
    (11, "Language", "Primary language of patient", False, True, False),
    (12, "Contact Method", "Preferred contact method", False, True, False),
    (13, "Address Line 1", "Patient address line 1", False, True, False),
    (14, "Address Line 2", "Patient address line 2", False, True, False),
    (15, "City", "Patient address city", False, True, False),
    (16, "State", "Patient address state", False, True, False),
    (17, "Zip", "Patient address zip code", False, True, False),
    (18, "Email", "Patient email", False, True, False),
    (19, "Home Phone", "Patient home phone number", False, True, False),
    (20, "Cell Phone", "Patient cell phone number", False, True, False),
    (21, "Work Phone", "Patient work phone number", False, True, False),
    (22, "Emergency Contact First Name", "Patient emergency contact first name", False, True, False),
    (23, "Emergency Contact Last Name", "Patient emergency contact last name", False, True, False),
    (24, "Emergency Contact Relationship", "Patient emergency contact relationship", False, True, False),
    (25, "Emergency Contact Address Line 1", "Patient emergency contact address line 1", False, True, False),
    (26, "Emergency Contact City", "Patient emergency contact address city", False, True, False),
    (27, "Emergency Contact State", "Patient emergency contact address state", False, True, False),
    (28, "Emergency Contact Zip", "Patient emergency contact address zip code", False, True, False),
    (29, "Emergency Contact Phone", "Patient emergency contact phone number", False, True, False),
    (30, "Prescriptions", "Patient's current and past Medications", False, True, False),
    # Page 2: items 31-43 at xMin=597 → CCD XML Export
    (31, "Preferred Pharmacy", "Preferred Pharmacy", False, True, False),
    (32, "Preferred Pharmacy Address", "Preferred Pharmacy Address", False, True, False),
    (33, "Preferred Pharmacy City", "Preferred Pharmacy City", False, True, False),
    (34, "Preferred Pharmacy State", "Preferred Pharmacy State", False, True, False),
    (35, "Preferred Pharmacy Zip", "Preferred Pharmacy Zip", False, True, False),
    (36, "Smoking status", "Patient smoking status", False, True, False),
    (37, "Social history", "Social history", False, True, False),
    (38, "Patient Immunization history", "Patient immunization history", False, True, False),
    (39, "Problem List", "Patient problems", False, True, False),
    (40, "Procedures", "Patient procedures", False, True, False),
    (41, "Vitals", "Patient Vitals", False, True, False),
    (42, "Allergies", "Patient allergies", False, True, False),
    (43, "Primary Provider", "Primary provider", False, True, False),
    # Page 2: items 44-46 at xMin=676 → JSON
    (44, "Providers List", "Care team members", False, False, True),
    (45, "Lab Results", "Lab Results", False, False, True),  # lowercase x in PDF
    (46, "Lab Order, Imaging Order", "Order sent by provider for patient", False, False, True),  # lowercase x
    # Page 2: items 47-48 at xMin=503 → Computable PDF Export
    (47, "Imaging Reports", "Imaging results and documents", True, False, False),
    (48, "Uploaded Documents", "Files uploaded to the patient chart - insurance cards, consent form etc.", True, False, False),
    # Page 2: items 49-62 at xMin=676 → JSON
    (49, "Primary Carrier Name", "Patient primary carrier name", False, False, True),
    (50, "Primary Subscriber ID", "Patient primary subscriber ID - insurance", False, False, True),
    (51, "Primary Group No", "Patient primary group number - insurance", False, False, True),
    (52, "Primary Plan Name", "Patient plan name - insurance", False, False, True),
    (53, "Secondary Carrier Name", "Patient secondary carrier name - insurance", False, False, True),
    (54, "Secondary Subscriber ID", "Patient secondary subscriber ID - insurance", False, False, True),
    (55, "Secondary Group No", "Patient secondary group number - insurance", False, False, True),
    (56, "Secondary Plan Name", "Patient secondary plan name - insurance", False, False, True),
    (57, "Guarantor First Name", "Guarantor for Patient Payment", False, False, True),
    (58, "Guarantor Last Name", "Guarantor for Patient Payment", False, False, True),
    (59, "Guarantor Middle Name", "Guarantor for Patient Payment", False, False, True),
    (60, "Guarantor Address", "Guarantor for Patient Payment", False, False, True),
    (61, "Guarantor Phone", "Guarantor for Patient Payment", False, False, True),
    (62, "Guarantor Relationship", "Guarantor for Patient Payment", False, False, True),
    # Page 3: items 63-87 at xMin=676 → JSON
    (63, "Guarantor City", "Guarantor for Patient Payment", False, False, True),
    (64, "Guarantor State", "Guarantor for Patient Payment", False, False, True),
    (65, "Guarantor Zip", "Guarantor for Patient Payment", False, False, True),
    (66, "Appointment Type", "Type of Appointment", False, False, True),
    (67, "Appointment Date/Time", "Date and time of appointments", False, False, True),
    (68, "Appointment Status", "Status of Appointment", False, False, True),
    (69, "Appointment Description", "Description of Appointment", False, False, True),
    (70, "Scheduled Provider", "Provider name of the appointment", False, False, True),
    (71, "Appointment Duration", "Time duration of the appointment scheduled", False, False, True),
    (72, "Receipt - Service date", "Date of service", False, False, True),
    (73, "Receipt - Service - Copay", "Paid copay amount of service", False, False, True),
    (74, "Receipt - Service - Deductible", "Paid deductible amount", False, False, True),
    (75, "Receipt - Service - Outstanding balance (with Claim#)", "Paid claim's outstanding balance amount", False, False, True),
    (76, "Receipt - Service - Credit account", "Credit amount (if any) to patient account", False, False, True),
    (77, "Receipt - Amount", "Service's amount", False, False, True),
    (78, "Receipt - Patient Name", "Receipt's patient name", False, False, True),
    (79, "Receipt - Patient Address", "Receipt's patient address", False, False, True),
    (80, "Receipt - Bill Date", "Receipt's originally created date", False, False, True),
    (81, "Receipt - Account No", "Receipt's patient account number", False, False, True),
    (82, "Receipt - Amount Paid", "Receipt's total amount", False, False, True),
    (83, "Receipt - Transaction Number", "Receipt's transaction number", False, False, True),
    (84, "Receipt - Paid Method", "Receipt's paid by method", False, False, True),
    (85, "Receipt - Billing Facility Name", "Billing facility name", False, False, True),
    (86, "Receipt - Billing Facility Address", "Billing facility address", False, False, True),
    (87, "Receipt - Billing Facility Contact Info", "Billing facility contact info", False, False, True),
]

elements_data = []
for num, name, desc, comp_pdf, ccd_xml, json_fmt in raw_elements:
    cat = get_category(num)
    elements_data.append({
        "number": num,
        "name": name,
        "description": desc,
        "has_description": bool(desc and desc.strip()),
        "computable_pdf": comp_pdf,
        "ccd_xml": ccd_xml,
        "json": json_fmt,
        "category": cat
    })

total = len(elements_data)
with_desc = sum(1 for e in elements_data if e["has_description"])
comp_pdf_count = sum(1 for e in elements_data if e["computable_pdf"])
ccd_xml_count = sum(1 for e in elements_data if e["ccd_xml"])
json_count = sum(1 for e in elements_data if e["json"])

print(f"=== SolidPractice b(10) Export Data Elements ===")
print(f"Total data elements: {total}")
print(f"Elements with descriptions: {with_desc} ({100*with_desc/total:.0f}%)")
print(f"\n=== Export Format Distribution ===")
print(f"CCD XML Export: {ccd_xml_count} elements (items 1-43)")
print(f"JSON: {json_count} elements (items 44-46, 49-87)")
print(f"Computable PDF Export: {comp_pdf_count} elements (items 47-48)")
print(f"Total: {comp_pdf_count + ccd_xml_count + json_count}")
print(f"(Each element in exactly ONE format)")
print()

# Category breakdown
cat_stats = {}
for e in elements_data:
    cat = e["category"]
    if cat not in cat_stats:
        cat_stats[cat] = {"count": 0, "with_desc": 0, "ccd_xml": 0, "json": 0, "computable_pdf": 0}
    cat_stats[cat]["count"] += 1
    if e["has_description"]:
        cat_stats[cat]["with_desc"] += 1
    if e["ccd_xml"]:
        cat_stats[cat]["ccd_xml"] += 1
    if e["json"]:
        cat_stats[cat]["json"] += 1
    if e["computable_pdf"]:
        cat_stats[cat]["computable_pdf"] += 1

print("=== Category Breakdown ===")
print(f"{'Category':<25} {'Count':>5} {'CCD XML':>8} {'JSON':>5} {'PDF':>4}")
print("-" * 50)
for cat in ["Demographics", "Medications", "Pharmacy", "Social History",
            "Immunizations", "Problems", "Procedures", "Vitals", "Allergies",
            "Providers/Care Team", "Labs & Imaging", "Uploaded Documents",
            "Insurance", "Guarantor", "Appointments", "Billing/Receipts"]:
    if cat in cat_stats:
        s = cat_stats[cat]
        print(f"{cat:<25} {s['count']:>5} {s['ccd_xml']:>8} {s['json']:>5} {s['computable_pdf']:>4}")

print()

# Data Access API sections
api_sections = [
    "allergiesAndIntolerances", "medications", "problem", "procedures",
    "immunizations", "vitalSigns", "socialHistory", "results",
    "medicalEquipment", "assessment", "planOfTreatment", "reasonForReferral",
    "goals", "healthConcerns", "functionalStatus", "cognitiveStatus"
]
print(f"=== Data Access API (CCD XML) ===")
print(f"Total selectable sections: {len(api_sections)}")
for s in api_sections:
    print(f"  - {s}")

# Save full inventory as JSON
output = {
    "total_elements": total,
    "elements_with_descriptions": with_desc,
    "description_percentage": round(100*with_desc/total),
    "format_counts": {
        "ccd_xml": ccd_xml_count,
        "json": json_count,
        "computable_pdf": comp_pdf_count
    },
    "format_note": "Each element is marked for exactly ONE export format",
    "column_verification_method": "pdftotext -bbox coordinate analysis: CCD XML header at x=565-635, X marks at x=597; JSON header at x=667-691, X marks at x=676; Computable PDF header at x=455-556, X marks at x=503",
    "categories": {cat: stats for cat, stats in cat_stats.items()},
    "elements": elements_data,
    "api_sections": api_sections
}

output_path = "/home/jmandel/hobby/ehi-export-analysis/abstraction/solidpractice-technologies-llc--solidpractice/analysis/full-entity-inventory.json"
with open(output_path, "w") as f:
    json.dump(output, f, indent=2)
print(f"\nFull inventory saved to: {output_path}")
