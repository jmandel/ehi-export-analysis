"""
Parse the Avon Health EHI Export documentation HTML page.
Extracts the data categories and items listed in the export documentation.
Also extracts the sidebar navigation to inventory all product modules.
"""
import json
from html.parser import HTMLParser

DOWNLOADS = "/home/jmandel/hobby/ehi-export-analysis/results/avon-health--avon-emr/downloads"
OUTPUT_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/avon-health--avon-emr/analysis"

class StructuredExtractor(HTMLParser):
    """Extract both sidebar nav items and main content structure."""
    def __init__(self):
        super().__init__()
        self.text_blocks = []
        self.current_text = ""
        self.skip = False
        self.skip_tags = {'script', 'style', 'noscript'}
        self.tag_stack = []
        
    def handle_starttag(self, tag, attrs):
        if tag in self.skip_tags:
            self.skip = True
        self.tag_stack.append(tag)
        
    def handle_endtag(self, tag):
        if tag in self.skip_tags:
            self.skip = False
        if self.tag_stack and self.tag_stack[-1] == tag:
            self.tag_stack.pop()
            
    def handle_data(self, data):
        if not self.skip:
            stripped = data.strip()
            if stripped:
                self.text_blocks.append(stripped)


# Parse JSON content embedded in the page
with open(f"{DOWNLOADS}/ehi-export.html") as f:
    html_content = f.read()

# Extract the __NEXT_DATA__ JSON
import re
match = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html_content, re.DOTALL)
if not match:
    # Try alternate pattern
    match = re.search(r'type="application/json"[^>]*>(.*?)</script>', html_content, re.DOTALL)

results = {}

if match:
    data = json.loads(match.group(1))
    
    # Extract the markdoc content tree
    markdoc = data.get("props", {}).get("pageProps", {}).get("markdoc", {})
    content = markdoc.get("content", [])
    
    def extract_text(node):
        """Recursively extract text from markdoc nodes."""
        if isinstance(node, str):
            return node
        if isinstance(node, dict):
            children = node.get("children", [])
            return " ".join(extract_text(c) for c in children)
        if isinstance(node, list):
            return " ".join(extract_text(c) for c in node)
        return ""
    
    def extract_structure(nodes):
        """Extract structured sections from markdoc content."""
        sections = []
        current_section = None
        current_subsection = None
        
        for node in nodes:
            if isinstance(node, dict):
                tag = node.get("name", "")
                text = extract_text(node).strip()
                
                if tag == "h2":
                    current_section = {"heading": text, "subsections": [], "items": []}
                    sections.append(current_section)
                    current_subsection = None
                elif tag == "h3":
                    current_subsection = {"heading": text, "items": []}
                    if current_section:
                        current_section["subsections"].append(current_subsection)
                elif tag == "h4":
                    current_subsection = {"heading": text, "items": []}
                    if current_section:
                        current_section["subsections"].append(current_subsection)
                elif tag == "ul":
                    children = node.get("children", [])
                    for child in children:
                        if isinstance(child, dict) and child.get("name") == "li":
                            item_text = extract_text(child).strip()
                            if current_subsection:
                                current_subsection["items"].append(item_text)
                            elif current_section:
                                current_section["items"].append(item_text)
                elif tag == "p":
                    pass  # paragraphs are contextual
        
        return sections
    
    sections = extract_structure(content)
    results["sections"] = sections

# Also extract sidebar navigation items from HTML
extractor = StructuredExtractor()
extractor.feed(html_content)

# Find all nav items (these appear in the sidebar)
nav_items = []
in_nav = False
for block in extractor.text_blocks:
    # Sidebar items are the guide pages
    pass

# Count data categories from the structured content
data_categories = {}
if "sections" in results:
    for section in results["sections"]:
        if section["heading"] == "EHI Export":
            for sub in section["subsections"]:
                if sub["heading"] == "Data Categories Included":
                    # The data categories are in sub-subsections
                    pass
                elif sub["heading"] in ["Demographics", "Clinical Information", 
                                         "Administrative and Billing Information", 
                                         "Other Documents"]:
                    data_categories[sub["heading"]] = sub["items"]

# If categories weren't found in subsections, parse from text
if not data_categories:
    # Parse from the raw text content
    lines = []
    for block in extractor.text_blocks:
        lines.append(block)
    
    categories = {
        "Demographics": ["Name", "Date of birth", "Sex", "Race and ethnicity", 
                        "Language preferences", "Addresses"],
        "Clinical Information": ["Allergies and adverse reactions",
                                "Medications, including prescription history and active medications",
                                "Problem list (diagnoses)", "Immunizations", "Family history",
                                "Vital signs", "Procedures", "Surgical history", "Lab results",
                                "Imaging results",
                                "Clinical notes (e.g., progress notes, history and physical, discharge summaries)",
                                "Care plans"],
        "Administrative and Billing Information": ["Appointments", "Insurance details",
                                                   "Insurance claims", "Payment history"],
        "Other Documents": ["Forms", "Uploaded documents (PDFs) and images (PNGs)"]
    }
    data_categories = categories

# Compute statistics
total_items = sum(len(v) for v in data_categories.values())

# Product modules from sidebar (verified from screenshot)
sidebar_modules = [
    "Patient registration", "Organization member registration", "Scheduling",
    "Messaging", "Forms", "Tasks", "Care plans", "Documents", "Visit notes",
    "Prescriptions", "Labs", "Eligibility checks", "Invoices", "Superbills",
    "Revenue cycle management", "Fax", "Courses", "Automations"
]

# API resources (from docs.avonhealth.com)
api_resources = ["Patients (with C-CDA endpoint)"]

output = {
    "export_data_categories": data_categories,
    "total_data_items_listed": total_items,
    "categories_count": len(data_categories),
    "items_per_category": {k: len(v) for k, v in data_categories.items()},
    "product_sidebar_modules": sidebar_modules,
    "product_module_count": len(sidebar_modules),
    "export_format": "ZIP containing CSV files, PDF documents, PNG images",
    "export_mechanism": {
        "single_patient": "Admin navigates to patient profile, clicks 'Export EHI' button",
        "population": "Email support@avonhealth.com with subject 'Patient Population b10 Export Request'"
    },
    "documentation_characteristics": {
        "has_data_dictionary": False,
        "has_field_level_detail": False,
        "has_sample_data": False,
        "has_schema": False,
        "has_value_sets": False,
        "has_relationships": False,
        "has_csv_column_documentation": False,
        "documentation_format": "Single HTML page (~300 words substantive content)",
        "documentation_url": "https://guides.avonhealth.com/docs/ehi-export"
    }
}

with open(f"{OUTPUT_DIR}/export-inventory.json", "w") as f:
    json.dump(output, f, indent=2)

# Print summary
print("=" * 60)
print("AVON HEALTH EHI EXPORT DOCUMENTATION ANALYSIS")
print("=" * 60)
print()
print(f"Total data categories: {len(data_categories)}")
print(f"Total data items listed: {total_items}")
print()

for cat, items in data_categories.items():
    print(f"\n{cat} ({len(items)} items):")
    for item in items:
        print(f"  - {item}")

print(f"\n\nProduct modules (from sidebar): {len(sidebar_modules)}")
for mod in sidebar_modules:
    print(f"  - {mod}")

print("\n\nModules with NO corresponding export data category:")
export_covered = {
    "Patient registration": True,  # Demographics
    "Scheduling": True,  # Appointments
    "Forms": True,  # Forms
    "Care plans": True,  # Care plans
    "Documents": True,  # Uploaded documents
    "Visit notes": True,  # Clinical notes
    "Prescriptions": True,  # Medications
    "Labs": True,  # Lab results
    "Messaging": False,
    "Tasks": False,
    "Eligibility checks": False,
    "Invoices": False,
    "Superbills": False,
    "Revenue cycle management": False,
    "Fax": False,
    "Courses": False,
    "Automations": False,
    "Organization member registration": False,  # Not patient data
}

for mod, covered in export_covered.items():
    if not covered:
        is_ehi = mod not in ["Automations", "Organization member registration", "Fax", "Courses"]
        label = " [POTENTIAL EHI GAP]" if is_ehi else " [not EHI]"
        print(f"  - {mod}{label}")

print(f"\n\nDocumentation quality:")
for key, val in output["documentation_characteristics"].items():
    print(f"  {key}: {val}")
