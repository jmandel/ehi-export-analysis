"""Re-fetch failed tables with latin-1 encoding."""
import json
import os
import subprocess

with open('table_index.json') as f:
    data = json.load(f)

all_tables = [(t['name'], 'jehr') for t in data['jehr']['tables']] + \
             [(t['name'], 'rtvx') for t in data['rtvx']['tables']]

fixed = 0
for name, schema in all_tables:
    cache_file = f"cache/{schema}/{name}.html"
    if not os.path.exists(cache_file) or os.path.getsize(cache_file) == 0:
        url = f"https://ehiexports.junohealth.com/{schema}/{name}.html"
        try:
            result = subprocess.run(
                ['curl', '-sL', url, '-H', 'User-Agent: Mozilla/5.0', '--max-time', '15'],
                capture_output=True, timeout=20
            )
            html_bytes = result.stdout
            if html_bytes and len(html_bytes) > 100:
                # Try latin-1 decoding
                html = html_bytes.decode('latin-1')
                with open(cache_file, 'w', encoding='utf-8') as f:
                    f.write(html)
                fixed += 1
                print(f"Fixed: {name}")
        except Exception as e:
            print(f"Still failed: {name}: {e}")

print(f"\nFixed {fixed} tables")
