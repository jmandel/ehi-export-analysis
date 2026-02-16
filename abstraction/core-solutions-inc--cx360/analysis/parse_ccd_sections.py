#!/usr/bin/env python3
"""Parse the enrichment JSON from the CCD sections data dictionary and produce
a full entity inventory and summary statistics."""

import json
import os

ENRICHMENT_PATH = os.path.join(
    os.path.dirname(__file__),
    "../../../results/core-solutions-inc--cx360/downloads/enrichment/ccd-sections.json",
)
OUTPUT_DIR = os.path.dirname(__file__)


def main():
    with open(ENRICHMENT_PATH) as f:
        data = json.load(f)

    sections = data["ccd_sections"]
    total_elements = 0
    elements_with_code_system = 0
    elements_with_xpath = 0
    sections_with_template = 0

    inventory = []

    for sec in sections:
        elements = sec["data_elements"]
        n = len(elements)
        total_elements += n

        has_template = sec.get("template_id") is not None
        if has_template:
            sections_with_template += 1

        sec_cs = sum(1 for e in elements if e.get("code_system_oid"))
        sec_xpath = sum(1 for e in elements if e.get("xpath_entry"))
        elements_with_code_system += sec_cs
        elements_with_xpath += sec_xpath

        inventory.append({
            "section_name": sec["section_name"],
            "template_id": sec.get("template_id"),
            "effective_date": sec.get("effective_date"),
            "field_count": n,
            "fields_with_code_system": sec_cs,
            "fields_with_xpath": sec_xpath,
            "fields": [
                {
                    "name": e["name"],
                    "xpath_entry": e.get("xpath_entry"),
                    "code_system_oid": e.get("code_system_oid"),
                    "code_system_name": e.get("code_system_name"),
                    "has_code_system": e.get("code_system_oid") is not None,
                    "has_xpath": e.get("xpath_entry") is not None,
                    # No descriptions, types, or value sets exist in the source
                    "description": None,
                    "type": None,
                }
                for e in elements
            ],
        })

    full_inventory = {
        "vendor": data.get("vendor"),
        "product": data.get("product"),
        "version": data.get("version"),
        "export_format": data.get("export_format"),
        "export_modes": data.get("export_modes"),
        "selectable_sections": data.get("selectable_sections"),
        "summary": {
            "total_sections": len(sections),
            "total_fields": total_elements,
            "sections_with_template_id": sections_with_template,
            "fields_with_code_system": elements_with_code_system,
            "fields_with_xpath": elements_with_xpath,
            "fields_with_descriptions": 0,  # None exist in source
            "fields_with_types": 0,  # None exist in source
        },
        "sections": inventory,
    }

    # Write full inventory
    inv_path = os.path.join(OUTPUT_DIR, "full-entity-inventory.json")
    with open(inv_path, "w") as f:
        json.dump(full_inventory, f, indent=2)
    print(f"Wrote {inv_path}")

    # Write summary stats
    stats_path = os.path.join(OUTPUT_DIR, "summary-stats.txt")
    with open(stats_path, "w") as f:
        f.write("CCD Sections Data Dictionary Summary\n")
        f.write("=" * 40 + "\n\n")
        f.write(f"Total C-CDA sections:           {len(sections)}\n")
        f.write(f"Total data elements (fields):    {total_elements}\n")
        f.write(f"Sections with template IDs:      {sections_with_template}\n")
        f.write(f"Fields with code system OIDs:    {elements_with_code_system}\n")
        f.write(f"Fields with XPATH entries:       {elements_with_xpath}\n")
        f.write(f"Fields with descriptions:        0 (none in source)\n")
        f.write(f"Fields with data types:          0 (none in source)\n")
        f.write(f"Fields with value sets:          0 (none in source)\n\n")

        f.write("Per-Section Breakdown\n")
        f.write("-" * 70 + "\n")
        f.write(f"{'Section':<45} {'Fields':>6} {'CodeSys':>8} {'XPath':>6}\n")
        f.write("-" * 70 + "\n")
        for s in inventory:
            f.write(
                f"{s['section_name']:<45} {s['field_count']:>6} "
                f"{s['fields_with_code_system']:>8} {s['fields_with_xpath']:>6}\n"
            )
        f.write("-" * 70 + "\n")
        f.write(
            f"{'TOTAL':<45} {total_elements:>6} "
            f"{elements_with_code_system:>8} {elements_with_xpath:>6}\n"
        )

    print(f"Wrote {stats_path}")

    # Print summary to stdout
    with open(stats_path) as f:
        print(f.read())


if __name__ == "__main__":
    main()
