"""Extract RWT Measure #3 (b)(10) data from the CY 2025 Real World Testing PDF."""
import subprocess, json

result = subprocess.run(
    ["pdftotext", "-layout", 
     "/home/jmandel/hobby/ehi-export-analysis/results/patient-first--pas/downloads/PatientFirst_Real_World_Test_Results_CY2025.pdf",
     "-"],
    capture_output=True, text=True
)
text = result.stdout

# Find the b(10) section
b10_start = text.find("RWT Measure #3")
b10_end = text.find("RWT Measure #4")
b10_section = text[b10_start:b10_end] if b10_start > -1 and b10_end > -1 else "NOT FOUND"

data = {
    "measure": "RWT Measure #3. Number of EHI Exports Run",
    "criteria": "315(b)(10)",
    "methodology": "Reporting/Logging",
    "metric_label": "Number of C-CDA Batch Exports Sent",  # NOTE: This is what they call it
    "reporting_interval": "3 months (Jan 1, 2025 through Mar 31, 2025)",
    "results": {
        "VA": 20,
        "MD": 6,
        "PA": 5,
        "NJ": 0,
        "total": 31
    },
    "annualized_estimate": 124,
    "analysis_quote": "While not every site uses the EHI export functionality, we do have some which do, and it worked as certified.",
    "notable_finding": "The metric is labeled 'Number of C-CDA Batch Exports Sent' even though it tracks b(10) EHI exports. This may indicate the EHI export is C-CDA-centric, or it may be a labeling oversight."
}

print(json.dumps(data, indent=2))

with open("/home/jmandel/hobby/ehi-export-analysis/abstraction/patient-first--pas/analysis/rwt-b10-data.json", "w") as f:
    json.dump(data, f, indent=2)

print(f"\nKey finding: b(10) metric labeled as '{data['metric_label']}'")
print(f"Q1 2025 volume: {data['results']['total']} exports across ~79 clinics")
