#!/usr/bin/env python3
"""Parse all HTML table documentation pages from TouchWorks EHI Export Definition.
Produces entity-inventory-full.json and entity-inventory-summary.json"""

import os, json, re, html
from pathlib import Path
from collections import defaultdict

INPUT_DIR = Path("../downloads/twehr-2026.1/Touchworks/User_databases")

def parse_html_table(filepath):
    """Parse a single table HTML file into structured data."""
    content = filepath.read_text(encoding='utf-8')
    
    # Extract title/table name
    title_m = re.search(r'<title>([^<]+)</title>', content)
    if not title_m:
        return None
    full_name = html.unescape(title_m.group(1))
    
    parts = full_name.split('.')
    schema = parts[0] if len(parts) > 1 else 'dbo'
    table_name = '.'.join(parts[1:]) if len(parts) > 1 else parts[0]
    
    # Extract database from path
    rel = filepath.relative_to(INPUT_DIR)
    database = rel.parts[0] if rel.parts else 'unknown'
    
    # Extract MS_Description
    desc_m = re.search(r'<a name="description">MS_Description</a>[\s\S]*?<div class="panel-body">([\s\S]*?)</div>', content)
    description = re.sub(r'<[^>]*>', '', desc_m.group(1)).strip() if desc_m else ''
    description = html.unescape(description)
    
    # Parse columns
    columns = []
    col_section = re.search(r'<a name="columns">Columns</a>[\s\S]*?<table[\s\S]*?</table>', content)
    if col_section:
        rows = re.findall(r'<tr>([\s\S]*?)</tr>', col_section.group(0))
        has_default = '<th>Default</th>' in content
        
        for i, row in enumerate(rows):
            if i == 0:  # header
                continue
            cells = re.findall(r'<td>([\s\S]*?)</td>', row)
            if not cells:
                continue
            
            key_cell = cells[0] if cells else ''
            is_pk = 'pkcluster' in key_cell or 'pknocluster' in key_cell
            has_fk = 'fk.png' in key_cell
            
            # FK target
            fk_target = None
            fk_m = re.search(r'Foreign Keys [^:]+: ([^"]+)', key_cell)
            if fk_m:
                fk_target = html.unescape(fk_m.group(1))
            
            def clean(idx):
                if idx < len(cells):
                    return html.unescape(re.sub(r'<[^>]*>', '', cells[idx])).strip()
                return ''
            
            if has_default:
                col = {
                    'name': clean(1),
                    'dataType': clean(2),
                    'maxLengthBytes': clean(3),
                    'nullability': clean(4),
                    'default': clean(5),
                    'description': clean(6),
                    'isPrimaryKey': is_pk,
                    'hasForeignKey': has_fk,
                    'foreignKeyTarget': fk_target,
                }
            else:
                col = {
                    'name': clean(1),
                    'dataType': clean(2),
                    'maxLengthBytes': clean(3),
                    'nullability': clean(4),
                    'default': '',
                    'description': clean(5),
                    'isPrimaryKey': is_pk,
                    'hasForeignKey': has_fk,
                    'foreignKeyTarget': fk_target,
                }
            columns.append(col)
    
    # Parse foreign keys section
    foreign_keys = []
    fk_section = re.search(r'<a name="foreignkeys">Foreign Keys</a>[\s\S]*?<table[\s\S]*?</table>', content)
    if fk_section:
        rows = re.findall(r'<tr>([\s\S]*?)</tr>', fk_section.group(0))
        for i, row in enumerate(rows):
            if i == 0:
                continue
            cells = re.findall(r'<td>([\s\S]*?)</td>', row)
            if len(cells) < 3:
                continue
            def clean(idx):
                return html.unescape(re.sub(r'<[^>]*>', '', cells[idx])).strip()
            foreign_keys.append({
                'name': clean(0),
                'columns': clean(1),
                'referencedTable': clean(2),
            })
    
    return {
        'database': database,
        'schema': schema,
        'tableName': table_name,
        'fullName': full_name,
        'description': description,
        'columns': columns,
        'foreignKeys': foreign_keys,
        'columnCount': len(columns),
        'sourceFile': str(rel),
    }

def categorize_table(table):
    """Assign a domain category based on table name patterns."""
    name = table['tableName'].lower()
    db = table['database']
    
    if db == 'AHSCharge':
        return 'Billing / Charges'
    if db == 'IntegratedScan':
        return 'Document Scanning'
    if db == 'Impact':
        return 'Impact / Reporting'
    if db == 'Quippe':
        return 'Quippe (Clinical Content)'
    if db == 'WorksArchive':
        return 'Archive'
    if db == 'WorksCDSAggregatorArchive':
        return 'CDS Archive'
    if db == 'chMedcinSearch':
        return 'Medcin Search'
    
    # Works database categorization
    if any(x in name for x in ['allerg', 'allergen']):
        return 'Allergies'
    if any(x in name for x in ['medication', 'prescription', 'rx_', 'drug', 'pharma', 'med_', 'medispan']):
        return 'Medications / Prescriptions'
    if any(x in name for x in ['immuniz', 'vaccine', 'vacc_']):
        return 'Immunizations'
    if any(x in name for x in ['lab_', 'laboratory', 'labresult', 'specimen']):
        return 'Laboratory'
    if any(x in name for x in ['vital', 'bp_', 'height', 'weight', 'bmi']):
        return 'Vitals'
    if any(x in name for x in ['problem', 'diagnosis', 'dx_', 'condition']):
        return 'Problems / Diagnoses'
    if any(x in name for x in ['encounter', 'visit', 'appt', 'appointment', 'schedule']):
        return 'Encounters / Visits'
    if any(x in name for x in ['order', 'ord_']):
        return 'Orders'
    if any(x in name for x in ['note', 'document', 'clinical_doc', 'transcription', 'act_hdr', 'act_']):
        return 'Clinical Notes / Documents'
    if any(x in name for x in ['patient', 'person', 'guardian', 'contact', 'demographic']):
        return 'Demographics / Patient'
    if any(x in name for x in ['insurance', 'coverage', 'payer', 'eligib', 'benefit']):
        return 'Insurance / Coverage'
    if any(x in name for x in ['charge', 'claim', 'billing', 'payment', 'invoice', 'fee', 'superbill', 'cpt_']):
        return 'Billing / Charges'
    if any(x in name for x in ['referral', 'refer_']):
        return 'Referrals'
    if any(x in name for x in ['care_plan', 'careplan', 'goal']):
        return 'Care Plans / Goals'
    if any(x in name for x in ['message', 'communication', 'inbox', 'task']):
        return 'Communications / Tasks'
    if any(x in name for x in ['cds_', 'clinical_decision', 'recommendation']):
        return 'Clinical Decision Support'
    if any(x in name for x in ['consent', 'directive', 'advance_directive']):
        return 'Consents / Directives'
    if any(x in name for x in ['image', 'radiology', 'imaging']):
        return 'Imaging'
    if any(x in name for x in ['procedure', 'surgery']):
        return 'Procedures'
    if any(x in name for x in ['result', 'observation']):
        return 'Results / Observations'
    if any(x in name for x in ['scan', 'attach', 'blob']):
        return 'Document Scanning'
    if any(x in name for x in ['_de', 'dictionary', 'lookup', 'code_']):
        return 'Dictionary / Reference'
    if any(x in name for x in ['template', 'form', 'questionnaire']):
        return 'Templates / Forms'
    if any(x in name for x in ['audit', 'log', 'access']):
        return 'Audit / Logging'
    if any(x in name for x in ['user', 'security', 'role', 'permission']):
        return 'Users / Security'
    if any(x in name for x in ['interface', 'integration', 'hl7', 'fhir']):
        return 'Interfaces / Integration'
    if any(x in name for x in ['item_']):
        return 'Items (Master Data)'
    
    return 'Other / Uncategorized'

def main():
    # Find all table HTML files
    all_html = []
    for root, dirs, files in os.walk(INPUT_DIR):
        for f in files:
            if f.endswith('.html'):
                all_html.append(Path(root) / f)
    
    # Filter to table files (in Tables/ dirs, not index/Tables.html)
    table_files = [f for f in all_html 
                   if '/Tables/' in str(f) 
                   and f.name not in ('Tables.html', 'index.html')]
    
    print(f"Total HTML files: {len(all_html)}")
    print(f"Table HTML files: {len(table_files)}")
    
    tables = []
    failures = []
    for tf in sorted(table_files):
        try:
            t = parse_html_table(tf)
            if t:
                t['category'] = categorize_table(t)
                tables.append(t)
            else:
                failures.append({'file': str(tf), 'error': 'Could not parse'})
        except Exception as e:
            failures.append({'file': str(tf), 'error': str(e)})
    
    print(f"Parsed: {len(tables)}, Failures: {len(failures)}")
    
    # Compute stats
    total_cols = sum(t['columnCount'] for t in tables)
    cols_with_desc = sum(1 for t in tables for c in t['columns'] if c['description'])
    cols_with_fk = sum(1 for t in tables for c in t['columns'] if c['hasForeignKey'])
    cols_with_pk = sum(1 for t in tables for c in t['columns'] if c['isPrimaryKey'])
    
    # Category breakdown
    cat_stats = defaultdict(lambda: {'tables': 0, 'columns': 0, 'described': 0})
    for t in tables:
        cat = t['category']
        cat_stats[cat]['tables'] += 1
        cat_stats[cat]['columns'] += t['columnCount']
        cat_stats[cat]['described'] += sum(1 for c in t['columns'] if c['description'])
    
    # Database breakdown
    db_stats = defaultdict(lambda: {'tables': 0, 'columns': 0})
    for t in tables:
        db_stats[t['database']]['tables'] += 1
        db_stats[t['database']]['columns'] += t['columnCount']
    
    # Write full inventory
    with open('entity-inventory-full.json', 'w') as f:
        json.dump(tables, f, indent=2)
    
    # Build summary
    summary = {
        'totalTables': len(tables),
        'totalColumns': total_cols,
        'columnsWithDescriptions': cols_with_desc,
        'descriptionPercent': round(cols_with_desc / total_cols * 100, 1) if total_cols else 0,
        'columnsWithForeignKeys': cols_with_fk,
        'columnsWithPrimaryKeys': cols_with_pk,
        'parseFailures': len(failures),
        'failureDetails': failures,
        'byDatabase': {k: v for k, v in sorted(db_stats.items(), key=lambda x: -x[1]['tables'])},
        'byCategory': {k: v for k, v in sorted(cat_stats.items(), key=lambda x: -x[1]['tables'])},
        'largestTables': sorted(
            [{'name': t['fullName'], 'database': t['database'], 'columns': t['columnCount'], 'category': t['category']} 
             for t in tables],
            key=lambda x: -x['columns']
        )[:30],
    }
    
    with open('entity-inventory-summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Print summary
    print(f"\n=== Summary ===")
    print(f"Tables: {len(tables)}")
    print(f"Columns: {total_cols}")
    print(f"Columns with descriptions: {cols_with_desc} ({summary['descriptionPercent']}%)")
    print(f"Columns with FK: {cols_with_fk}")
    print(f"\nBy Database:")
    for db, s in sorted(db_stats.items(), key=lambda x: -x[1]['tables']):
        print(f"  {db}: {s['tables']} tables, {s['columns']} columns")
    print(f"\nBy Category:")
    for cat, s in sorted(cat_stats.items(), key=lambda x: -x[1]['tables']):
        desc_pct = round(s['described']/s['columns']*100, 1) if s['columns'] else 0
        print(f"  {cat}: {s['tables']} tables, {s['columns']} cols, {desc_pct}% described")
    print(f"\nTop 15 largest tables:")
    for t in summary['largestTables'][:15]:
        print(f"  {t['name']} ({t['database']}): {t['columns']} cols [{t['category']}]")

if __name__ == '__main__':
    main()
