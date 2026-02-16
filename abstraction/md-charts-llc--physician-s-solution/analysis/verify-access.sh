#!/bin/bash
# Verify accessibility of MD Charts EHI export documentation URL
# Run: bash verify-access.sh

echo "=== Testing registered EHI documentation URL ==="
echo "URL: https://mraemr.com:47102/api/DataExportGuidance.asp"
curl -sI -L "https://mraemr.com:47102/api/DataExportGuidance.asp" \
  -H 'User-Agent: Mozilla/5.0' --connect-timeout 10 --max-time 15 -k 2>&1
echo "Exit code: $?"

echo ""
echo "=== Testing mraemr.com standard port ==="
curl -sI "https://mraemr.com" -H 'User-Agent: Mozilla/5.0' --connect-timeout 10 -k 2>&1
echo "Exit code: $?"

echo ""
echo "=== Checking Wayback Machine for port 47102 ==="
curl -s "https://web.archive.org/cdx/search/cdx?url=mraemr.com:47102/*&output=json&limit=20" --connect-timeout 10 2>&1

echo ""
echo "=== Checking vendor marketing site for EHI references ==="
curl -sL "https://mdchartsehr.com/why-mdcharts/" -H 'User-Agent: Mozilla/5.0' --connect-timeout 10 2>&1 | grep -i -E "ehi|export|data.dictionary|b\(10\)|b\.10" || echo "No EHI export references found"
