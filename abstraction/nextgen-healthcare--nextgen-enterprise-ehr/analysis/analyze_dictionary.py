#!/usr/bin/env python3
"""
Analyzes the NextGen Enterprise EHR data dictionary (from enrichment JSON).
Produces entity-inventory-full.json and entity-inventory-summary.json.

Uses the enrichment/data-dictionary.json as the parsed source (which was
extracted from the raw PDF via pdftotext). We verify key stats independently.
"""

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

WORK_DIR = Path(__file__).parent.parent
DD_PATH = WORK_DIR / "downloads" / "enrichment" / "data-dictionary.json"
OUT_FULL = Path(__file__).parent / "entity-inventory-full.json"
OUT_SUMMARY = Path(__file__).parent / "entity-inventory-summary.json"

# Load the parsed data dictionary
with open(DD_PATH) as f:
    tables = json.load(f)

# ============================================================
# Categorize tables by domain based on naming patterns
# ============================================================

CATEGORY_RULES = [
    # Specialty clinical categories (most specific first)
    (r'(?i)^AB_', 'Reproductive Health'),
    (r'(?i)^ADHD', 'Behavioral Health'),
    (r'(?i)^ACEs_', 'Behavioral Health'),
    (r'(?i)^bh_|^BH_', 'Behavioral Health'),
    (r'(?i)^depression', 'Behavioral Health'),
    (r'(?i)^Asthma_', 'Respiratory / Pulmonary'),
    (r'(?i)^PUL_|^pul_', 'Respiratory / Pulmonary'),
    (r'(?i)^audiogram', 'Audiology'),
    (r'(?i)^CARD_|^card_|^Card_|^Cardiac|^Coronar|^CABG|^Coumadin|^CVSurg|^AFib|^Aortic', 'Cardiology'),
    (r'(?i)^oph_|^eye|^OPK_|^opk_', 'Ophthalmology'),
    (r'(?i)^Contactlens', 'Ophthalmology'),
    (r'(?i)^womens_|^well_woman|^gyn_|^GYN_', 'OB/GYN / Women\'s Health'),
    (r'(?i)^OB_|^ob_|^birth_|^prenatal|^labor_|^delivery', 'OB/GYN / Women\'s Health'),
    (r'(?i)^well_child|^PEDS_|^peds_', 'Pediatrics'),
    (r'(?i)^zika_', 'Infectious Disease'),
    (r'(?i)^hiv_|^HIV_', 'Infectious Disease'),
    (r'(?i)^derm_|^Derm_', 'Dermatology'),
    (r'(?i)^chiro_', 'Chiropractic'),
    (r'(?i)^ent_|^ENT_', 'ENT'),
    (r'(?i)^gastro|^gi_|^GI_', 'Gastroenterology'),
    (r'(?i)^neuro_', 'Neurology'),
    (r'(?i)^ortho_|^ort_|^ORT_', 'Orthopedics'),
    (r'(?i)^pain_', 'Pain Management'),
    (r'(?i)^podiatry_', 'Podiatry'),
    (r'(?i)^rheum_|^rhe_|^RHE_', 'Rheumatology'),
    (r'(?i)^sleep_', 'Sleep Medicine'),
    (r'(?i)^urology_|^uro_|^URO_', 'Urology'),
    (r'(?i)^nephro_', 'Nephrology'),
    (r'(?i)^onc_|^ONC_|^Cancer_', 'Oncology'),
    (r'(?i)^dental_', 'Dental'),
    (r'(?i)^wound_', 'Wound Care'),
    (r'(?i)^nsg_|^NSG_', 'Nursing'),
    (r'(?i)^dm_|^DM_|^BetterDiab|^Diabetes', 'Diabetes / Endocrine'),
    (r'(?i)^Anticoagulation', 'Anticoagulation'),
    (r'(?i)^ASC_|^asc_|^Asc_', 'Ambulatory Surgery Center'),

    # Clinical content by type
    (r'(?i)^hpi_|^HPI_|^hpi\d', 'HPI (History of Present Illness)'),
    (r'(?i)^pe_|^PE_', 'Physical Exam'),
    (r'(?i)^ros_|^ROS_', 'Review of Systems'),
    (r'(?i)^sub_|^SUB_', 'Subjective (Clinical)'),
    (r'(?i)^tis_|^TIS_', 'Clinical Templates (TIS)'),
    (r'(?i)^chm_|^CHM_', 'Clinical Templates (CHM)'),
    (r'(?i)^fts_|^FTS_', 'Clinical Templates (FTS)'),
    (r'(?i)^rinf_|^RINF_', 'Clinical Templates (RINF)'),
    (r'(?i)^DCE_|^dce_', 'Data Collection / Clinical'),
    (r'(?i)^generic_', 'Generic Clinical Forms'),
    (r'(?i)^graph_', 'Clinical Graphing'),
    (r'(?i)^histories_', 'Medical History'),
    (r'(?i)^SHx_|^shx_|^social_', 'Social History / SDOH'),

    # Core clinical
    (r'(?i)vital|^VS_|^vs_', 'Vitals'),
    (r'(?i)allerg', 'Allergies'),
    (r'(?i)immun|^imm_|vaccine', 'Immunizations'),
    (r'(?i)diagnos|^dx_|problem_list', 'Diagnoses / Problems'),
    (r'(?i)medic|prescri|pharma|^rx_', 'Medications / Prescriptions'),
    (r'(?i)^lab_|^Lab_|^ainf_ord_lab|^CBC_|^MLTS_|^mlts_', 'Laboratory'),
    (r'(?i)^order_|^ainf_ord|^ord_', 'Orders'),
    (r'(?i)referral|refer_', 'Referrals'),
    (r'(?i)^proc_|^PROC_', 'Procedures'),
    (r'(?i)encounter|^enc_|^ainf_.*enc', 'Encounters'),
    (r'(?i)note_|progress_note|soap_|clinical_note|^ChartNotes', 'Clinical Notes'),
    (r'(?i)care_plan|careplan|^care_', 'Care Plans / Goals'),
    (r'(?i)consent|^AuthRelease', 'Consents / Authorization'),
    (r'(?i)assessment|screen|survey|questionnaire', 'Assessments / Screening'),
    (r'(?i)family_h|famhx|family_history', 'Family History'),
    (r'(?i)growth_chart|growth_', 'Growth Charts'),
    (r'(?i)education|patient_ed', 'Patient Education'),
    (r'(?i)^telephone_|^CallComplete|^CallNotes', 'Communications / Calls'),
    (r'(?i)^task_|^Task_', 'Tasks / Workflow'),

    # Documents & media
    (r'(?i)document|doc_|attachment|image_|scan_', 'Documents / Media'),

    # Billing & financial
    (r'(?i)billing|bill_|charge|claim|superbill|fee_|payment|remit|eob|revenue|financial|collection|^ar_|account_rec|^CPTII|^CPT_', 'Billing / Financial'),
    (r'(?i)insurance|insur_|eligib|coverage|payer|preauth|prior_auth|authorization', 'Insurance / Authorization'),
    (r'(?i)icd_|hcpcs|coding', 'Coding'),

    # Administrative
    (r'(?i)^patient_|^person_|^demograph|^ainf_patient', 'Demographics / Patient'),
    (r'(?i)^provider_|^practitioner|^staff_|^physician', 'Provider / Staff'),
    (r'(?i)^practice_|^facility|^location_|^site_|^clinic_', 'Practice / Facility'),
    (r'(?i)schedul|appoint|calendar', 'Scheduling'),
    (r'(?i)^message_|^inbox|^secure_msg|portal|^ngweb_|^NGWEB_', 'Patient Portal / Web'),
    (r'(?i)^Chart_|^ChartRequest', 'Chart Management'),
    (r'(?i)^nxmd_|^NXMD_', 'NextGen Mobile / Digital'),
    (r'(?i)^mng_|^MNG_', 'Management / Admin'),

    # Integration & system
    (r'(?i)interface|hl7|fhir|ccd|ccda|interop|mirth|^intrf_|^hie_|^HIE_', 'Interoperability / Interface'),
    (r'(?i)^ngkbm_|^NGKBM_', 'Knowledge Base / Clinical Content'),
    (r'(?i)audit|access_log', 'Audit / Logging'),
    (r'(?i)config|setting|preference|template_|^master_|lookup|code_set', 'Configuration / Reference'),

    # NextGen-specific prefixes
    (r'(?i)^AINF_|^ainf_', 'Clinical Forms (AINF)'),
    (r'(?i)^IORTS', 'Surgical / Procedural (IORTS)'),
    (r'(?i)^WelchAllyn', 'Device Integration'),
    (r'(?i)^chronic_', 'Chronic Conditions'),
    (r'(?i)^barriers_', 'Barriers to Care'),
    (r'(?i)^additional_', 'Additional Clinical Data'),
    (r'(?i)^cm_|^CM_', 'Care Management'),
    (r'(?i)^Coordinator_', 'Care Coordination'),
    (r'(?i)^ClinicalPlan', 'Clinical Plans'),
    (r'(?i)^edr_|^EDR_', 'Emergency / Urgent Care'),
    (r'(?i)^opt_|^OPT_', 'Optometry'),
    (r'(?i)^frw_|^FRW_', 'Framework / System'),

    # Broad clinical content catch-alls (last resort before uncategorized)
    (r'(?i)^info_', 'Clinical Information Forms'),
    (r'(?i)^pt_', 'Patient-Specific Data'),
    (r'(?i)^diff_', 'Differential Diagnosis'),

    # Catch-alls for tables with person_id / enc_id (probably clinical)
    (r'(?i)symptom_master', 'Symptom Reference'),
    (r'(?i)activity_detail', 'Activity Tracking'),
]

def categorize_table(table_name):
    """Categorize a table based on its name using pattern matching."""
    for pattern, category in CATEGORY_RULES:
        if re.search(pattern, table_name):
            return category
    return 'Other / Uncategorized'


# Build full inventory
full_inventory = []
category_stats = defaultdict(lambda: {'table_count': 0, 'field_count': 0, 'tables': []})
data_type_counts = Counter()
tables_by_size = []

for t in tables:
    table_name = t['table']
    columns = t['columns']
    category = categorize_table(table_name)

    entity = {
        'table': table_name,
        'category': category,
        'field_count': len(columns),
        'fields': []
    }

    for c in columns:
        field = {
            'name': c['name'],
            'dataType': c.get('dataType', ''),
            'default': c.get('default'),
            'notNull': c.get('notNull', False),
            'description': None  # No descriptions in the PDF
        }
        entity['fields'].append(field)
        if c.get('dataType'):
            data_type_counts[c['dataType']] += 1

    full_inventory.append(entity)
    category_stats[category]['table_count'] += 1
    category_stats[category]['field_count'] += len(columns)
    category_stats[category]['tables'].append(table_name)
    tables_by_size.append((table_name, len(columns), category))

# Sort tables by size (descending)
tables_by_size.sort(key=lambda x: x[1], reverse=True)

# Write full inventory
with open(OUT_FULL, 'w') as f:
    json.dump(full_inventory, f, indent=2)

# ============================================================
# Build summary
# ============================================================

total_tables = len(tables)
total_fields = sum(len(t['columns']) for t in tables)
fields_with_types = sum(1 for t in tables for c in t['columns'] if c.get('dataType'))
fields_with_defaults = sum(1 for t in tables for c in t['columns'] if c.get('default'))
fields_with_descriptions = 0  # No descriptions in the PDF

# Category breakdown (sorted by field count)
category_breakdown = []
for cat, stats in sorted(category_stats.items(), key=lambda x: -x[1]['field_count']):
    category_breakdown.append({
        'category': cat,
        'table_count': stats['table_count'],
        'field_count': stats['field_count'],
        'sample_tables': stats['tables'][:5]
    })

# Top 20 largest tables
top_20_tables = [
    {'table': name, 'field_count': count, 'category': cat}
    for name, count, cat in tables_by_size[:20]
]

# Average fields per table
avg_fields = total_fields / total_tables if total_tables > 0 else 0

# Tables with fewer than 5 fields (thin tables)
thin_tables = sum(1 for _, count, _ in tables_by_size if count < 5)

summary = {
    'total_tables': total_tables,
    'total_fields': total_fields,
    'fields_with_types': fields_with_types,
    'fields_with_types_pct': round(fields_with_types / total_fields * 100, 1) if total_fields else 0,
    'fields_with_defaults': fields_with_defaults,
    'fields_with_descriptions': fields_with_descriptions,
    'fields_with_descriptions_pct': 0.0,
    'avg_fields_per_table': round(avg_fields, 1),
    'thin_tables_lt5_fields': thin_tables,
    'data_type_distribution': dict(data_type_counts.most_common(20)),
    'category_breakdown': category_breakdown,
    'top_20_largest_tables': top_20_tables,
    'categorization_coverage': {
        'categorized': sum(1 for e in full_inventory if e['category'] != 'Other / Uncategorized'),
        'uncategorized': sum(1 for e in full_inventory if e['category'] == 'Other / Uncategorized'),
    }
}

with open(OUT_SUMMARY, 'w') as f:
    json.dump(summary, f, indent=2)

print(f"Total tables: {total_tables}")
print(f"Total fields: {total_fields}")
print(f"Fields with types: {fields_with_types} ({summary['fields_with_types_pct']}%)")
print(f"Fields with descriptions: {fields_with_descriptions} (0%)")
print(f"Avg fields/table: {avg_fields:.1f}")
print(f"Thin tables (<5 fields): {thin_tables}")
print(f"\nCategories: {len(category_breakdown)}")
for cb in category_breakdown[:15]:
    print(f"  {cb['category']}: {cb['table_count']} tables, {cb['field_count']} fields")
print(f"\nTop 10 largest tables:")
for t in top_20_tables[:10]:
    print(f"  {t['table']}: {t['field_count']} fields ({t['category']})")
print(f"\nCategorized: {summary['categorization_coverage']['categorized']}, Uncategorized: {summary['categorization_coverage']['uncategorized']}")
