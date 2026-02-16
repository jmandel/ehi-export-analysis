"""
Parse all EHI export artifacts for ASP.MD Medical Office System.
Extracts content from the export page and disclosures page to produce
structured summaries of what the vendor documents about their EHI export.
"""

import json
import re
from html.parser import HTMLParser
from pathlib import Path

DOWNLOADS = Path("../downloads")
OUTPUT = Path(".")


class ContentExtractor(HTMLParser):
    """Extract text content from HTML, skipping script/style/nav."""
    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.skip_tags = {"script", "style"}
        self.skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.skip_tags:
            self.skip_depth += 1

    def handle_endtag(self, tag):
        if tag in self.skip_tags and self.skip_depth > 0:
            self.skip_depth -= 1

    def handle_data(self, data):
        if self.skip_depth == 0:
            stripped = data.strip()
            if stripped:
                self.text_parts.append(stripped)

    def get_text(self):
        return "\n".join(self.text_parts)


def parse_export_page():
    """Parse the WP API JSON for the export page content."""
    with open(DOWNLOADS / "export-page-wp-api.json") as f:
        data = json.load(f)

    content_html = data.get("content", {}).get("rendered", "")
    # Strip HTML tags
    text = re.sub(r"<[^>]+>", " ", content_html)
    text = re.sub(r"\s+", " ", text).strip()

    return {
        "source": "export-page-wp-api.json",
        "source_url": "https://www.asp.md/export/",
        "title": data.get("title", {}).get("rendered", ""),
        "published": data.get("date", ""),
        "modified": data.get("modified", ""),
        "content_text": text,
        "content_html": content_html,
        "word_count": len(text.split()),
    }


def parse_disclosures_page():
    """Parse the disclosures page for b(10) and pricing info."""
    with open(DOWNLOADS / "disclosures-page.html") as f:
        html = f.read()

    extractor = ContentExtractor()
    extractor.feed(html)
    full_text = extractor.get_text()

    # Extract b(10) mention
    b10_lines = [
        line for line in full_text.split("\n")
        if "b)(10" in line.lower() or "export" in line.lower()
    ]

    # Extract pricing info
    pricing_lines = [
        line for line in full_text.split("\n")
        if any(k in line.lower() for k in ["pricing", "fee", "cost", "charge"])
    ]

    return {
        "source": "disclosures-page.html",
        "source_url": "https://www.asp.md/disclosures-2/",
        "b10_mentions": b10_lines,
        "pricing_info": pricing_lines,
    }


def build_summary():
    """Build the complete artifact analysis."""
    export_page = parse_export_page()
    disclosures = parse_disclosures_page()

    summary = {
        "vendor": "ASP.MD Inc.",
        "product": "ASP.MD Medical Office System",
        "artifacts": [
            {
                "file": "export-page.html / export-page-wp-api.json",
                "type": "EHI Export Documentation Page",
                "source_url": export_page["source_url"],
                "published": export_page["published"],
                "modified": export_page["modified"],
                "word_count": export_page["word_count"],
                "content": export_page["content_text"],
                "informative": True,
                "notes": "Entire export documentation is a single paragraph. No data dictionary, no schema, no field list.",
            },
            {
                "file": "export-page-screenshot.png",
                "type": "Screenshot",
                "source_url": export_page["source_url"],
                "size_bytes": (DOWNLOADS / "export-page-screenshot.png").stat().st_size,
                "informative": False,
                "notes": "Visual confirmation of the export page content.",
            },
            {
                "file": "disclosures-page.html",
                "type": "Mandatory Disclosures Page",
                "source_url": disclosures["source_url"],
                "b10_mentions": disclosures["b10_mentions"],
                "pricing_info": disclosures["pricing_info"],
                "informative": True,
                "notes": "Confirms b(10) certification. States no additional fees. No export-specific documentation.",
            },
        ],
        "export_documentation": {
            "formats_mentioned": ["C-CDA", "Text files", "PDF files"],
            "data_dictionary": False,
            "schema": False,
            "sample_data": False,
            "field_list": False,
            "entity_list": False,
            "total_words_of_documentation": export_page["word_count"],
            "external_reference": "http://www.hl7.org/ccdasearch/pdfs/Companion_Guide.pdf",
            "folder_naming": "LASTNAME_FIRSTNAME_DOB_MRN (DOB=YYYYMMDD, MRN=integer)",
        },
    }

    return summary


if __name__ == "__main__":
    summary = build_summary()

    with open(OUTPUT / "artifact-analysis.json", "w") as f:
        json.dump(summary, f, indent=2)

    print(f"Total artifacts: {len(summary['artifacts'])}")
    print(f"Export page word count: {summary['export_documentation']['total_words_of_documentation']}")
    print(f"Data dictionary present: {summary['export_documentation']['data_dictionary']}")
    print(f"Formats mentioned: {', '.join(summary['export_documentation']['formats_mentioned'])}")
    print(f"\nExport page content:\n{summary['artifacts'][0]['content']}")
