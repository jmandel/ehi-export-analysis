#!/usr/bin/env python3
"""Parse the Healthie EHI export HTML documentation page into structured JSON.

Reads the HTML data dictionary from downloads/ehi-export-page.html and produces:
  - full-entity-inventory.json: complete field-level inventory
  - summary-stats.json: aggregate statistics
"""

import json
import sys
from pathlib import Path
from bs4 import BeautifulSoup

HTML_PATH = Path(__file__).parent.parent.parent.parent / "results/healthie--healthie/downloads/ehi-export-page.html"
OUT_DIR = Path(__file__).parent

def parse():
    soup = BeautifulSoup(HTML_PATH.read_text(), "lxml")
    article = soup.select_one("#fullArticle") or soup

    import re
    entities = []
    all_ps = article.find_all("p")

    # Parse CSV files: each has a <p> "X.csv format and data elements:" followed
    # optionally by intervening <p> tags, then a <table> with columns.
    for p in all_ps:
        text = p.get_text(strip=True)
        m = re.match(r"^([\w.]+\.csv)\s+format and data elements:?", text)
        if not m:
            continue
        filename = m.group(1)

        # Walk forward collecting intervening <p> and the next <table>
        description = None
        row_semantics = None
        columns = []
        sib = p.find_next_sibling()
        while sib and sib.name != "table":
            if sib.name == "p":
                st = sib.get_text(strip=True)
                # Stop if we hit the next file's heading
                if re.match(r"^[\w.]+\.(csv|pdf|html)\s+", st) or "folder" in st.lower()[:20]:
                    break
                if "row in the CSV" in st:
                    row_semantics = st
                elif not description:
                    description = st
            sib = sib.find_next_sibling()

        if sib and sib.name == "table":
            rows = sib.find_all("tr")
            for row in rows[1:]:
                cells = [td.get_text(strip=True) for td in row.find_all(["td", "th"])]
                if cells:
                    col = {"name": cells[0]}
                    col["data_notes"] = cells[1] if len(cells) >= 2 and cells[1] else None
                    columns.append(col)

        entities.append({
            "filename": filename,
            "type": "csv",
            "description": description,
            "row_semantics": row_semantics,
            "columns": columns,
            "column_count": len(columns),
        })

    # Parse non-CSV files (PDFs, HTML, folder)
    # These follow the pattern: <p>X format and data elements:</p> <p>description</p>
    for p in all_ps:
        text = p.get_text(strip=True)
        for pattern, ftype in [
            (r"^(Charting\.pdf)\s+format and data elements:?", "pdf"),
            (r"^(journal_entries\.pdf)\s*$", "pdf"),
            (r"^(format\.html)\s*$", "html"),
            (r"^(Documents folder)\s+format and data elements:?", "folder"),
        ]:
            m = re.match(pattern, text)
            if not m:
                continue
            filename = m.group(1)
            if any(e["filename"] == filename for e in entities):
                continue
            # Description is in the next sibling <p>
            desc = None
            nxt = p.find_next_sibling("p")
            if nxt:
                nxt_text = nxt.get_text(strip=True)
                if not re.match(r"^[\w.]+\.(csv|pdf|html)\s+format", nxt_text):
                    desc = nxt_text
            entities.append({
                "filename": filename,
                "type": ftype,
                "description": desc,
                "row_semantics": None,
                "columns": [],
                "column_count": 0,
            })

    # Compute stats
    total_files = len(entities)
    csv_files = [e for e in entities if e["type"] == "csv"]
    total_csv = len(csv_files)
    total_columns = sum(e["column_count"] for e in entities)
    columns_with_notes = sum(
        1 for e in entities for c in e["columns"] if c.get("data_notes")
    )
    total_field_count = sum(len(e["columns"]) for e in entities)

    # Categorize entities by domain
    categories = {}
    for e in entities:
        cat = categorize(e["filename"])
        categories.setdefault(cat, []).append(e["filename"])

    # Identify journal entry files (shared schema)
    journal_files = [e["filename"] for e in entities if e["filename"].endswith("Entry.csv")]
    # Verify they share the same schema
    journal_schemas = {}
    for e in entities:
        if e["filename"] in journal_files:
            cols = tuple(c["name"] for c in e["columns"])
            journal_schemas[e["filename"]] = cols
    unique_journal_schemas = set(journal_schemas.values())

    summary = {
        "total_files": total_files,
        "csv_files": total_csv,
        "pdf_files": sum(1 for e in entities if e["type"] == "pdf"),
        "html_files": sum(1 for e in entities if e["type"] == "html"),
        "folder_files": sum(1 for e in entities if e["type"] == "folder"),
        "total_columns": total_columns,
        "columns_with_data_notes": columns_with_notes,
        "columns_without_data_notes": total_columns - columns_with_notes,
        "pct_columns_with_notes": round(100 * columns_with_notes / total_columns, 1) if total_columns else 0,
        "journal_entry_files": journal_files,
        "journal_schemas_identical": len(unique_journal_schemas) == 1,
        "categories": {k: {"count": len(v), "files": v} for k, v in sorted(categories.items())},
        "entities_by_column_count": sorted(
            [{"filename": e["filename"], "columns": e["column_count"]} for e in entities],
            key=lambda x: -x["columns"]
        ),
    }

    # Write outputs
    (OUT_DIR / "full-entity-inventory.json").write_text(json.dumps(entities, indent=2))
    (OUT_DIR / "summary-stats.json").write_text(json.dumps(summary, indent=2))

    print(f"Total files: {total_files}")
    print(f"CSV files: {total_csv}")
    print(f"Total columns across all CSVs: {total_columns}")
    print(f"Columns with data notes: {columns_with_notes} ({summary['pct_columns_with_notes']}%)")
    print(f"Journal entry files: {len(journal_files)}, schemas identical: {len(unique_journal_schemas) == 1}")
    print(f"\nCategories:")
    for cat, info in sorted(summary["categories"].items()):
        print(f"  {cat}: {info['count']} files")
    print(f"\nTop entities by column count:")
    for item in summary["entities_by_column_count"][:10]:
        print(f"  {item['filename']}: {item['columns']} columns")


def categorize(filename):
    """Assign a domain category to each file."""
    fn = filename.lower()
    if fn in ("client_overview.csv", "addresses.csv", "family_and_contacts.csv"):
        return "Demographics & Contacts"
    if fn in ("diagnoses.csv",):
        return "Clinical - Conditions"
    if fn in ("medications.csv",):
        return "Clinical - Medications"
    if fn in ("allergies.csv", "food_intolerances.csv", "food_preferences.csv", "food_sensitivities.csv"):
        return "Allergies & Food Sensitivities"
    if fn in ("careplans.csv", "goals.csv", "recommendations.csv"):
        return "Care Plans & Goals"
    if fn in ("charting.pdf",):
        return "Clinical Notes"
    if fn in ("cms1500s.csv", "superbills.csv", "insurance.csv", "insurance_authorizations.csv", "policies.csv", "payments.csv", "packages.csv"):
        return "Billing & Insurance"
    if fn in ("messages.csv",):
        return "Communications"
    if fn in ("provider.csv", "other_care_team_members.csv", "referring_physicians.csv"):
        return "Care Team"
    if fn in ("client_metrics.csv",):
        return "Biometric Metrics"
    if fn in ("client_user_groups.csv",):
        return "Administrative"
    if fn.endswith("entry.csv"):
        return "Journal Entries (Wellness)"
    if fn in ("documents folder",):
        return "Documents"
    if fn in ("format.html",):
        return "Export Metadata"
    if fn in ("journal_entries.pdf",):
        return "Journal Entries (Wellness)"
    return "Other"


if __name__ == "__main__":
    parse()
