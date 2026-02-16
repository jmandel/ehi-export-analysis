#!/bin/bash
# Verification script: tests accessibility of MD Charts EHI export documentation URLs
# Run date: 2026-02-16

echo "=== MD Charts EHI Export URL Verification ==="
echo "Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo

echo "1. Testing registered EHI documentation URL (port 47102)..."
curl -v "https://mraemr.com:47102/api/DataExportGuidance.asp" \
  -H 'User-Agent: Mozilla/5.0' --connect-timeout 15 --max-time 30 -k 2>&1 | tail -5
echo

echo "2. Testing mraemr.com standard port (443)..."
curl -v "https://mraemr.com" \
  -H 'User-Agent: Mozilla/5.0' --connect-timeout 15 --max-time 30 -k 2>&1 | tail -5
echo

echo "3. Testing DataExportGuidance on standard port..."
curl -sL "https://mraemr.com/api/DataExportGuidance.asp" \
  -H 'User-Agent: Mozilla/5.0' --connect-timeout 15 --max-time 30 -k 2>&1 | head -5
echo

echo "4. Testing vendor marketing site for EHI content..."
curl -sL "https://mdchartsehr.com/why-mdcharts/" \
  -H 'User-Agent: Mozilla/5.0' --connect-timeout 15 --max-time 30 2>&1 | \
  grep -i "ehi\|export\|data.*export\|b.*10\|DataExportGuidance" | head -5
echo "(empty = no EHI export content found)"
echo

echo "5. Checking Wayback Machine for port 47102..."
curl -s "https://web.archive.org/cdx/search/cdx?url=mraemr.com:47102/*&output=json&limit=10" 2>&1
echo
echo "([] = no captures)"

echo
echo "=== Verification Complete ==="
