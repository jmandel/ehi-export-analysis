"""
Comprehensive artifact inventory for MedicsDocAssistant EHI export analysis.
Produces a JSON summary of all artifacts and their characteristics.
"""
import json
import os

RESULTS = "/home/jmandel/hobby/ehi-export-analysis/results/advanced-data-systems-corporation--medicsdocassistant"
DOWNLOADS = os.path.join(RESULTS, "downloads")

artifacts = []

for fname in sorted(os.listdir(DOWNLOADS)):
    fpath = os.path.join(DOWNLOADS, fname)
    size = os.path.getsize(fpath)
    ext = os.path.splitext(fname)[1].lower()
    
    info = {
        "filename": fname,
        "size_bytes": size,
        "extension": ext,
    }
    
    if ext in ('.html', '.htm'):
        with open(fpath, 'r', errors='replace') as f:
            content = f.read()
        info["line_count"] = content.count('\n') + 1
        info["char_count"] = len(content)
        
        # Check for data dictionary indicators
        table_count = content.lower().count('<table')
        info["html_tables"] = table_count
        
    elif ext == '.json':
        try:
            with open(fpath, 'r') as f:
                data = json.load(f)
            if isinstance(data, dict):
                info["top_level_keys"] = list(data.keys())
                if 'entry' in data:
                    info["entry_count"] = len(data['entry'])
        except:
            info["parse_error"] = True
    
    elif ext == '.png':
        info["type"] = "screenshot"
    
    artifacts.append(info)

# Summary
summary = {
    "total_artifacts": len(artifacts),
    "by_type": {},
    "artifacts": artifacts,
}

for a in artifacts:
    ext = a["extension"]
    summary["by_type"][ext] = summary["by_type"].get(ext, 0) + 1

print(json.dumps(summary, indent=2))
