# URL Verification Log

Date: 2026-02-15

## Registered EHI Export Documentation URL
- URL: https://mraemr.com:47102/api/DataExportGuidance.asp
- Result: Connection refused (curl exit code 7)
- Details: Port 47102 is not accepting TCP connections

## mraemr.com Standard HTTPS (port 443)
- URL: https://mraemr.com
- Result: "No route to host" after ~3 seconds
- Note: Prior report (2026-02-14) claimed port 443 was reachable; it is now also down

## mraemr.com HTTP (port 80)
- URL: http://mraemr.com
- Result: 200 OK — default IIS 8.5 page
- Note: Only port 80 is responsive; shows default IIS landing, not EHR application

## mraemr.com /api/DataExportGuidance.asp (port 443)
- URL: https://mraemr.com/api/DataExportGuidance.asp
- Result: Connection failed (same "No route to host" on port 443)

## Marketing Site
- URL: https://mdchartsehr.com/why-mdcharts/
- Result: 200 OK
- Content: ONC certification section links to CHPL listing and mandatory disclosures
- Mandatory disclosures link: https://mraemr.com:47102/api/mandatory_disclosure.asp (same dead port)
- No EHI export documentation, data dictionary, or export-related content found

## Wayback Machine
- mraemr.com:47102/*: No captures exist
- mraemr.com/api/DataExportGuidance*: No captures exist
- mraemr.com/*DataExport*: No captures exist

## DNS
- mraemr.com resolves to 75.99.93.174
- Mail handled by mx.noip.com (dynamic DNS service)

## Conclusion
The registered EHI export documentation is completely inaccessible. No alternative
source for the documentation exists. The server appears to be partially down
(only port 80 responding with a default IIS page). Both the EHI export documentation
and mandatory disclosures are unreachable.
