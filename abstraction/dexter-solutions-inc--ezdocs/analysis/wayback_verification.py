"""
Document what the Wayback Machine shows for the certification URL.
All captures show the v5.0 certification page with (b)(6) Data Export,
NOT the v5.5 certification with (b)(10) EHI Export.
"""
import json

# Based on CDX API query and manual verification on 2026-02-15
wayback_captures = [
    {"timestamp": "20220706123403", "url": "https://dexter-solutions.com/certification", "status": 200, "content": "v5.0 certification, (b)(6) Data Export"},
    {"timestamp": "20221130232023", "url": "https://dexter-solutions.com/certification", "status": 200, "content": "v5.0 certification, (b)(6) Data Export"},
    {"timestamp": "20230208063351", "url": "https://dexter-solutions.com/certification", "status": 200, "content": "v5.0 certification, (b)(6) Data Export"},
    {"timestamp": "20230322022812", "url": "https://dexter-solutions.com/certification", "status": 200, "content": "v5.0 certification, (b)(6) Data Export"},
    {"timestamp": "20240304105528", "url": "https://dexter-solutions.com/certification", "status": 200, "content": "v5.0 certification, (b)(6) Data Export"},
    {"timestamp": "20240702003059", "url": "https://dexter-solutions.com/certification", "status": 200, "content": "v5.0 certification, (b)(6) Data Export"},
    {"timestamp": "20240702200037", "url": "http://dexter-solutions.com/certification", "status": 301, "content": "redirect"},
    {"timestamp": "20240712102501", "url": "https://dexter-solutions.com/certification", "status": 200, "content": "v5.0 certification, (b)(6) Data Export"},
    {"timestamp": "20240804232517", "url": "https://dexter-solutions.com/certification", "status": 200, "content": "v5.0 certification, (b)(6) Data Export"},
]

output = {
    "url_checked": "https://dexter-solutions.com/certification",
    "total_captures": len(wayback_captures),
    "date_range": "2022-07-06 to 2024-08-04",
    "finding": "All captures show eZDocs v5.0 certification page with 170.315 (b)(6) Data Export. "
               "None show the v5.5 certification with 170.315 (b)(10) EHI Export. "
               "The v5.5 page (certified 2024-01-02) was apparently updated after the last Wayback capture "
               "and then removed during a site rebuild before being re-captured.",
    "current_state": "URL redirects to vendor homepage (Wix SPA catch-all). No certification content.",
    "v5_certification_key_info": {
        "version": "5.0",
        "certification_date": "2019-12-30",
        "relevant_criteria": "170.315 (b)(6) Data Export (predecessor to b(10))",
        "no_ehi_export_documentation": True,
    },
    "v55_certification_key_info": {
        "version": "5.5",
        "certification_date": "2024-01-02",
        "relevant_criteria": "170.315 (b)(10) Electronic Health Information Export",
        "chpl_product_number": "15.02.04.2708.eZDo.05.02.1.240102",
        "documentation_accessible": False,
        "search_engine_snippets": "Snippets reference CDA (XML) and PDF export for single and multiple patients, and a downloadable PDF titled '170.315 (b)(10) Electronic Health Information Export'",
    },
    "captures": wayback_captures,
}

output_path = "/home/jmandel/hobby/ehi-export-analysis/abstraction/dexter-solutions-inc--ezdocs/analysis/wayback_verification.json"
with open(output_path, "w") as f:
    json.dump(output, f, indent=2)

print("Wayback verification saved.")
print(f"Total captures: {len(wayback_captures)}")
print(f"All show v5.0 with (b)(6) - none show v5.5 with (b)(10)")
print(f"Current state: URL redirects to homepage, no documentation accessible")
