#!/usr/bin/env python3
"""
Parse OpenEMR SchemaSpy XML schema and HTML column comments into a unified
entity-inventory-full.json and entity-inventory-summary.json.

Inputs:
  ../downloads/enrichment/schema.json    (parsed XML)
  ../downloads/enrichment/html-comments.json  (HTML column comments)

Outputs:
  entity-inventory-full.json
  entity-inventory-summary.json
"""

import json
import os
import re
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS = os.path.join(BASE, "..", "downloads")

# Load XML-parsed schema
with open(os.path.join(DOWNLOADS, "enrichment", "schema.json")) as f:
    schema = json.load(f)

# Load HTML comments
with open(os.path.join(DOWNLOADS, "enrichment", "html-comments.json")) as f:
    html_comments = json.load(f)

# Build HTML comment lookup: table_name -> {col_name: comment}
html_lookup = {}
for entry in html_comments:
    tname = entry.get("table")
    cols = {}
    for c in entry.get("columns", []):
        cols[c["name"]] = c.get("comment", "")
    html_lookup[tname] = cols

# Categorize tables by name prefix / domain
def categorize_table(name):
    """Assign a domain category based on table name patterns."""
    n = name.lower()
    
    # Eye/ophthalmology - must be before generic clinical forms
    if n.startswith("form_eye"):
        return "Ophthalmology (Specialty)"
    
    # Clinical forms
    if n.startswith("form_") or n == "forms":
        return "Clinical Forms"
    
    # Billing/financial
    billing_keywords = ["billing", "claims", "ar_activity", "ar_session", 
                        "payment", "fee_sheet", "x12_", "insurance",
                        "eligibility", "codes", "fee_schedule", "prices",
                        "voids", "edi_sequences", "benefit_eligibility"]
    for kw in billing_keywords:
        if n == kw or n.startswith(kw):
            return "Billing & Insurance"
    
    # Medications/pharmacy
    if n.startswith("drug") or n in ("prescriptions", "lists_medication", "product_warehouse") or n.startswith("erx_"):
        return "Medications & Pharmacy"
    
    # Procedures/labs
    if n.startswith("procedure_") or n in ("clinical_notes_procedure_results",):
        return "Procedures & Labs"
    
    # Documents
    if "document" in n or n in ("categories", "categories_to_documents", "categories_seq",
                                  "onsite_signatures", "esign_signatures"):
        return "Documents & Signatures"
    
    # Patient demographics
    if n in ("patient_data", "patient_history", "history_data", 
             "patient_access_offsite", "patient_access_onsite",
             "patient_portal_menu", "patient_tracker", "patient_tracker_element",
             "patient_birthday_alert", "employer_data", "patient_settings",
             "patient_reminders", "recent_patients", "person", "person_patient_link",
             "address", "addresses", "contact", "contact_address", "contact_relation",
             "contact_telecom", "phone_numbers", "verify_email", "onsite_online"):
        return "Patient Demographics & Contacts"
    
    # Immunizations
    if "immunization" in n:
        return "Immunizations"
    
    # Scheduling
    if "calendar" in n or "postcalendar" in n or n in ("track_events",):
        return "Scheduling"
    
    # Messaging/communications
    if n in ("pnotes", "notification_log", "notifications", "notification_settings",
             "onsite_mail", "onsite_messages", "onsite_portal_activity",
             "secure_chat_room", "secure_chat", "batchcom", "dated_reminders",
             "dated_reminders_link", "email_queue", "notes", "onotes",
             "direct_message_log"):
        return "Messaging & Communications"
    
    # Amendments
    if "amendment" in n:
        return "Amendments"
    
    # Clinical lists & issues (problems, allergies, etc.)
    if n in ("list_options", "lists", "issue_encounter", "issue_types", "lists_touch"):
        return "Clinical Lists & Issues"
    
    # Care teams
    if n.startswith("care_team"):
        return "Care Teams"
    
    # Clinical decision support / rules
    if n.startswith("clinical_") or n.startswith("rule_"):
        return "Clinical Decision Support"
    
    # Transactions (referrals, etc.)
    if n in ("transactions",):
        return "Transactions & Referrals"
    
    # FHIR/Questionnaires/API
    if n.startswith("questionnaire") or n.startswith("api_") or n.startswith("fhir_"):
        return "FHIR & Questionnaires"
    
    # CCDA
    if n.startswith("ccda"):
        return "C-CDA & Interoperability"
    
    # Users/facilities
    if n in ("users", "users_facility", "facility", "facility_user_ids",
             "groups", "user_settings", "users_secure", "login_mfa_registrations",
             "misc_address_book", "pharmacies"):
        return "Users & Facilities"
    
    # Access control
    if n.startswith("gacl_"):
        return "Access Control"
    
    # Layout-based forms
    if n.startswith("lbf_") or n.startswith("lbt_") or n in ("layout_options", "layout_group_properties"):
        return "Layout-Based Forms"
    
    # Logs/audit
    if n in ("log", "log_comment_encrypt", "log_validator", "api_log",
             "extended_log", "audit_details", "audit_master"):
        return "Audit & Logging"
    
    # Reference/terminology data
    if n.startswith("icd") or n.startswith("sct2_") or n.startswith("valueset") or \
       n in ("code_types", "enc_category_map", "supported_external_dataloads"):
        return "Reference & Terminology"
    
    # EHI export itself
    if n.startswith("ehi_export") or n.startswith("export_"):
        return "EHI Export Infrastructure"
    
    # Telehealth
    if n.startswith("comlink_"):
        return "Telehealth"
    
    # Patient experience / PRO
    if n in ("patient_care_experience_preferences", "patient_treatment_intervention_preferences",
             "pro_assessments", "preference_value_sets"):
        return "Patient Preferences & PROs"
    
    # Syndromic surveillance
    if n in ("syndromic_surveillance",):
        return "Public Health Reporting"
    
    # System/config
    config_keywords = ["background_services", "globals", "registry", 
                       "sequences", "standardized_", "module_",
                       "automatic_notification", "lang_", "geo_",
                       "keys", "session", "therapy_", "version",
                       "product_registration", "openemr_module",
                       "multiple_db", "template_users", "modules",
                       "report_", "ip_tracking", "uuid_", "shared_attributes",
                       "dsi_source_attributes", "customlists", "gprelations",
                       "chart_tracker", "onetime_auth", "oauth_",
                       "jwt_grant_history", "amc_misc_data", "medex_",
                       "external_"]
    for kw in config_keywords:
        if n == kw or n.startswith(kw):
            return "System & Configuration"
    
    return "Other"

# Build full inventory
entities = []
total_fields = 0
fields_with_desc = 0
fields_with_type = 0

for table in schema["tables"]:
    tname = table["name"]
    html_cols = html_lookup.get(tname, {})
    category = categorize_table(tname)
    
    fields = []
    for col in table["columns"]:
        cname = col["name"]
        # Merge description: prefer HTML comment, fall back to XML remarks
        xml_remark = col.get("remarks", "")
        html_comment = html_cols.get(cname, "")
        description = html_comment if html_comment else xml_remark
        
        has_fk = len(col.get("parents", [])) > 0
        fk_refs = []
        for p in col.get("parents", []):
            fk_refs.append(f"{p['table']}.{p['column']}")
        
        field = {
            "name": cname,
            "type": col.get("type", ""),
            "size": col.get("size"),
            "nullable": col.get("nullable", True),
            "defaultValue": col.get("defaultValue"),
            "description": description,
            "has_description": bool(description),
            "foreign_keys": fk_refs if fk_refs else None,
            "auto_updated": col.get("autoUpdated", False),
        }
        fields.append(field)
        total_fields += 1
        if description:
            fields_with_desc += 1
        if col.get("type"):
            fields_with_type += 1
    
    entity = {
        "table_name": tname,
        "category": category,
        "table_remarks": table.get("remarks", ""),
        "row_count": table.get("numRows"),
        "field_count": len(fields),
        "fields_with_descriptions": sum(1 for f in fields if f["has_description"]),
        "primary_key": [pk["column"] for pk in table.get("primaryKey", [])],
        "index_count": len(table.get("indexes", [])),
        "relationship_count": sum(
            len(c.get("parents", [])) + len(c.get("children", []))
            for c in table["columns"]
        ),
        "fields": fields,
    }
    entities.append(entity)

# Sort by category then name
entities.sort(key=lambda e: (e["category"], e["table_name"]))

# Full inventory
full_inventory = {
    "product": "OpenEMR",
    "source": "SchemaSpy XML + HTML column comments",
    "database": schema.get("databaseName", ""),
    "database_type": schema.get("databaseType", ""),
    "total_entities": len(entities),
    "total_fields": total_fields,
    "fields_with_descriptions": fields_with_desc,
    "fields_with_types": fields_with_type,
    "description_coverage_pct": round(100 * fields_with_desc / total_fields, 1) if total_fields else 0,
    "entities": entities,
}

with open(os.path.join(BASE, "entity-inventory-full.json"), "w") as f:
    json.dump(full_inventory, f, indent=2)

# Summary: aggregate by category
category_stats = defaultdict(lambda: {"tables": 0, "fields": 0, "fields_with_desc": 0, "example_tables": []})
for e in entities:
    cat = e["category"]
    s = category_stats[cat]
    s["tables"] += 1
    s["fields"] += e["field_count"]
    s["fields_with_desc"] += e["fields_with_descriptions"]
    if len(s["example_tables"]) < 5:
        s["example_tables"].append(e["table_name"])

summary = {
    "product": "OpenEMR",
    "total_entities": len(entities),
    "total_fields": total_fields,
    "fields_with_descriptions": fields_with_desc,
    "description_coverage_pct": round(100 * fields_with_desc / total_fields, 1) if total_fields else 0,
    "fields_with_types": fields_with_type,
    "categories": {
        cat: {
            "tables": s["tables"],
            "fields": s["fields"],
            "fields_with_descriptions": s["fields_with_desc"],
            "description_pct": round(100 * s["fields_with_desc"] / s["fields"], 1) if s["fields"] else 0,
            "example_tables": s["example_tables"],
        }
        for cat, s in sorted(category_stats.items())
    },
    "top_20_largest_tables": sorted(
        [{"table": e["table_name"], "fields": e["field_count"], "category": e["category"], 
          "remarks": e["table_remarks"][:100] if e["table_remarks"] else ""}
         for e in entities],
        key=lambda x: -x["fields"]
    )[:20],
}

with open(os.path.join(BASE, "entity-inventory-summary.json"), "w") as f:
    json.dump(summary, f, indent=2)

# Print summary
print(f"Total entities: {len(entities)}")
print(f"Total fields: {total_fields}")
print(f"Fields with descriptions: {fields_with_desc} ({round(100*fields_with_desc/total_fields,1)}%)")
print(f"Fields with types: {fields_with_type}")
print(f"\nCategories:")
for cat, s in sorted(category_stats.items()):
    pct = round(100 * s["fields_with_desc"] / s["fields"], 1) if s["fields"] else 0
    print(f"  {cat}: {s['tables']} tables, {s['fields']} fields ({pct}% described)")
print(f"\nTop 10 largest tables:")
for t in summary["top_20_largest_tables"][:10]:
    print(f"  {t['table']}: {t['fields']} fields [{t['category']}]")
