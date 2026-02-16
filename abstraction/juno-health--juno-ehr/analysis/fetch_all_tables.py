"""Fetch ALL individual table pages for JEHR and RxTracker in parallel."""

import json
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

with open('table_index.json') as f:
    data = json.load(f)

def fetch_table(schema, table_name):
    base_url = f"https://ehiexports.junohealth.com/{schema}/"
    url = f"{base_url}{table_name}.html"
    cache_dir = f"cache/{schema}"
    cache_file = f"{cache_dir}/{table_name}.html"
    
    if os.path.exists(cache_file) and os.path.getsize(cache_file) > 0:
        return table_name, True, 'cached'
    
    try:
        result = subprocess.run(
            ['curl', '-sL', url, '-H', 'User-Agent: Mozilla/5.0', '--max-time', '15'],
            capture_output=True, text=True, timeout=20
        )
        html = result.stdout
        if html and len(html) > 100:
            with open(cache_file, 'w') as f:
                f.write(html)
            return table_name, True, 'fetched'
    except Exception as e:
        return table_name, False, str(e)
    return table_name, False, 'empty response'

os.makedirs('cache/jehr', exist_ok=True)
os.makedirs('cache/rtvx', exist_ok=True)

# Fetch all tables
all_tasks = []
for t in data['jehr']['tables']:
    all_tasks.append(('jehr', t['name']))
for t in data['rtvx']['tables']:
    all_tasks.append(('rtvx', t['name']))

print(f"Fetching {len(all_tasks)} table pages...")
success = 0
failed = 0
cached = 0

with ThreadPoolExecutor(max_workers=20) as executor:
    futures = {executor.submit(fetch_table, schema, name): (schema, name) 
               for schema, name in all_tasks}
    
    for i, future in enumerate(as_completed(futures)):
        name, ok, status = future.result()
        if ok:
            if status == 'cached':
                cached += 1
            else:
                success += 1
        else:
            failed += 1
            print(f"  FAILED: {name}: {status}")
        
        if (i + 1) % 100 == 0:
            print(f"  Progress: {i+1}/{len(all_tasks)} (fetched={success}, cached={cached}, failed={failed})")

print(f"\nDone: {success} fetched, {cached} cached, {failed} failed out of {len(all_tasks)}")
