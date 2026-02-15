# b10 EHI Export - CCDA

---

**Document Information**

---

**Document Name:** b.10 EHI Export - Patient Data via CCDA

Specifications

**Document The Backend Design**

**Version: v1.0**

**Description:**

---

# Introduction

- **Overview**:
    
    This document describes the structure and syntax of the exported Electronic Health Information (EHI) as per the <span class="s1">**b.10 EHI Export**</span> requirement. It provides details on the export format, file type, data structure, and instructions for accessing the data.
- **Objectives**:
    
    • Define the format and structure of exported EHI.
    
    • Provide a detailed data dictionary of exported elements.
    
    • Outline authentication and access instructions.

<section class="markdown-section" data-markdown-raw="
## API Endpoint Details" data-section-index="2" id="bkmrk-api-endpoint-details">## API Endpoint Details

</section><section class="markdown-section" data-markdown-raw="
### Basic Information" data-section-index="4" id="bkmrk-basic-information">**File Type Details**

• <span class="s1">**Format**</span>: XML

<span class="s2">• </span>**Schema**<span class="s2">: </span>**Consolidated Clinical Document Architecture (C-CDA) 2.1**

• <span class="s1">**Encoding**</span>: UTF-8

<span class="s2">• </span>**File Extension**<span class="s2">: </span><span class="s3">.xml</span>

• <span class="s1">**Schema Reference**</span>: Based on the HL7 CDA R2 standard

<div class="markdown-section-toolbar"><div><div class="markdown-section-toolbar-internal"><div class="markdown-section-toolbar-item dark">  
</div><div class="markdown-section-toolbar-item markdown-section-toolbar-copy dark">  
</div></div></div></div>### Basic Information

</section><section class="markdown-section" data-markdown-raw="
- **HTTP Method**: POST" data-section-index="5" id="bkmrk-http%C2%A0method%3A-post">**<span class="markdown-bold-text">HTTP Method</span>:** POST</section><section class="markdown-section" data-markdown-raw="
- **URL**: `/patient/:idPatient/getPatientCCDAData`" data-section-index="6" id="bkmrk-url%3A%C2%A0%2Fpatient%2F%3Aidpat">**<span class="markdown-bold-text">URL</span>:** <span class="markdown-inline-code">/patient/:idPatient/getPatientCCDAData</span></section><section class="markdown-section" data-markdown-raw="
- **Description**: Retrieves Continuity of Care Document Architecture (CCDA) data for a specific patient" data-section-index="7" id="bkmrk-description%3A-retriev">**<span class="markdown-bold-text">Description</span>:** Retrieves Continuity of Care Document Architecture (CCDA) data for a specific patient</section><section class="markdown-section" data-markdown-raw="
- **Description**: Retrieves Continuity of Care Document Architecture (CCDA) data for a specific patient" data-section-index="7" id="bkmrk--1"></section><section class="markdown-section" data-markdown-raw="
### Authentication & Authorization" data-section-index="9" id="bkmrk-authentication-%26-aut">### Authentication &amp; Authorization

</section><section class="markdown-section" data-markdown-raw="
- **Authentication Required**: Yes" data-section-index="10" id="bkmrk-authentication-requi">**<span class="markdown-bold-text">Authentication Required</span>:** Yes</section><section class="markdown-section" data-markdown-raw="
- **Type**: JWT Bearer Token" data-section-index="11" id="bkmrk-type%3A-jwt-bearer-tok">**<span class="markdown-bold-text">Type</span>:** JWT Bearer Token  
**<span class="markdown-bold-text">Guard</span>**: JwtAuthGuard</section><section class="markdown-section" data-markdown-raw="
### Request Parameters" data-section-index="15" id="bkmrk-request-parameters"><div class="markdown-section-toolbar"><div><div class="markdown-section-toolbar-internal"><div class="markdown-section-toolbar-item markdown-section-toolbar-copy dark">  
</div></div></div></div>### Request Parameters

</section><section class="markdown-section" data-markdown-raw="
#### Path Parameters" data-section-index="17" id="bkmrk-path-parameters">#### Path Parameters

</section><section class="markdown-section" data-markdown-raw="
- `idPatient` (number): Patient ID" data-section-index="18" id="bkmrk-idpatient-%28number%29%3A-">- <span class="markdown-inline-code">idPatient</span> (number): Patient ID

</section><section class="markdown-section" data-markdown-raw="
#### Request Body" data-section-index="20" id="bkmrk-request-body">#### Request Body

</section><section class="markdown-section" data-markdown-raw="
- Type: `PatientCCDADTO`" data-section-index="21" id="bkmrk-type%3A%C2%A0patientccdadto">- **Type:** <span class="markdown-inline-code">PatientCCDADTO</span>

</section><section class="markdown-section" data-markdown-raw="
### Database Interactions" data-section-index="23" id="bkmrk-database%C2%A0interaction"><div class="markdown-section-toolbar"><div><div class="markdown-section-toolbar-internal"><div class="markdown-section-toolbar-item dark">  
</div><div class="markdown-section-toolbar-item markdown-section-toolbar-copy dark">  
</div></div></div></div>### Data Dictionary

</section><section class="markdown-section" data-markdown-raw="
The service interacts with several database tables through the DBPatientsServices:" data-section-index="25" id="bkmrk-the-service-interact"><div class="markdown-section-toolbar"><div><div class="markdown-section-toolbar-internal"><div class="markdown-section-toolbar-item markdown-section-toolbar-copy dark">  
</div></div></div></div>The following table provides an overview of key fields included in the exported C-CDA document:

  
</section><section class="markdown-section" data-markdown-raw="
#### Patient Table" data-section-index="27" id="bkmrk-patient-table"></section><section class="markdown-section" data-markdown-raw="
- Links to encounters and amendments" data-section-index="47" id="bkmrk-links-to-encounters-"></section><section class="markdown-section" data-markdown-raw="
### Response Structure" data-section-index="49" id="bkmrk-response-structure">[![image.png](https://bookstack.careexpandcloud.com/uploads/images/gallery/2025-02/scaled-1680-/Qvqimage.png)](https://bookstack.careexpandcloud.com/uploads/images/gallery/2025-02/Qvqimage.png)

*Note: Additional fields may be included depending on the data available for the patient.*

<div class="markdown-section-toolbar"><div><div class="markdown-section-toolbar-internal"><div class="markdown-section-toolbar-item markdown-section-toolbar-copy dark">  
</div></div></div></div>### Response Structure

</section><section class="markdown-section" data-markdown-raw="
#### Success Response (200 OK)
```json
{
  "patientData": {
    "demographics": {
      "name": string,
      "dob": date,
      "gender": string,
      // ... other demographic fields
    },
    "clinicalData": {
      // Clinical information
    },
    "monitors": [
      // Patient monitoring data
    ]
  }
}
```
" data-section-index="51" id="bkmrk-success-response-%2820"><div class="markdown-section-toolbar"><div><div class="markdown-section-toolbar-internal">  
</div></div></div>#### Success Response (200 OK)

```
{
  "patientData": {
    "demographics": {
      "name": string,
      "dob": date,
      "gender": string,
      // ... other demographic fields
    },
    "clinicalData": {
      // Clinical information
    },
    "monitors": [
      // Patient monitoring data
    ]
  }
}
```

</section><section class="markdown-section" data-markdown-raw="
### Error Responses" data-section-index="52" id="bkmrk-error-responses">### Error Responses

</section><section class="markdown-section" data-markdown-raw="
1. **401 Unauthorized**
```json
{
  "statusCode": 401,
  "message": "You are not Scope authorized to perform the operation"
}
```
" data-section-index="54" id="bkmrk-401-unauthorized-%7B-%C2%A0"><div class="markdown-section-toolbar"><div><div class="markdown-section-toolbar-internal">  
</div></div></div>**<span class="markdown-bold-text">401 Unauthorized</span>**```
{
  "statusCode": 401,
  "message": "You are not Scope authorized to perform the operation"
}
```

<div class="markdown-code-outer-container markdown-block-code" id="bkmrk-403-forbidden"><div><div data-keybinding-context="200" data-mode-id="json"><div class="monaco-editor no-user-select mac  showUnused showDeprecated vs-dark" data-uri="aichat-code-block-anysphere://ryjauzhkdf" role="code"><div class="overflow-guard" data-mprt="3"><div class="monaco-scrollable-element editor-scrollable vs-dark mac" data-mprt="6" role="presentation"><div class="lines-content monaco-editor-background"><div aria-hidden="true" class="view-lines monaco-mouse-cursor-text" data-mprt="8" role="presentation"><div class="view-line">**403 Forbidden**</div></div></div></div></div></div></div></div></div></section><section class="markdown-section" data-markdown-raw="
- When JWT authentication fails" data-section-index="56" id="bkmrk-when-jwt-authenticat"><div class="markdown-section-toolbar"><div><div class="markdown-section-toolbar-internal">  
</div></div></div>When JWT authentication fails</section><section class="markdown-section" data-markdown-raw="
3. **404 Not Found**" data-section-index="58" id="bkmrk-404%C2%A0not-found"><div class="markdown-section-toolbar"><div><div class="markdown-section-toolbar-internal"><div class="markdown-section-toolbar-item markdown-section-toolbar-copy dark">  
</div></div></div></div>**<span class="markdown-bold-text">404 Not Found</span>**</section><section class="markdown-section" data-markdown-raw="
- When patient data is not found" data-section-index="59" id="bkmrk-when-patient-data-is"><div class="markdown-section-toolbar"><div><div class="markdown-section-toolbar-internal">  
</div></div></div>When patient data is not found</section><section class="markdown-section" data-markdown-raw="
4. **500 Internal Server Error**" data-section-index="61" id="bkmrk-500-internal-server-"><div class="markdown-section-toolbar"><div><div class="markdown-section-toolbar-internal"><div class="markdown-section-toolbar-item markdown-section-toolbar-copy dark">  
</div></div></div></div>**<span class="markdown-bold-text">500 Internal Server Error</span>**</section><section class="markdown-section" data-markdown-raw="
- For unexpected server errors" data-section-index="62" id="bkmrk-for-unexpected-serve"><div class="markdown-section-toolbar"><div><div class="markdown-section-toolbar-internal">  
</div></div></div>For unexpected server errors</section><section class="markdown-section" data-markdown-raw="
- For unexpected server errors" data-section-index="62" id="bkmrk--2"></section><section class="markdown-section" data-markdown-raw="
- For unexpected server errors" data-section-index="62" id="bkmrk-download-%26-access-in">### **Download &amp; Access Instructions**

1\. <span class="s1">**Authentication**</span>: Ensure a valid JWT Bearer Token is provided in the request headers.

2\. <span class="s1">**API Call**</span>: Send a <span class="s2">POST</span> request to the specified endpoint with the required parameters.

3\. <span class="s1">**Download File**</span>: If successful, the response will contain a link to download the CCDA <span class="s2">.xml</span> file.

4\. <span class="s1">**Open in a Viewer**</span>: Use a compatible CCDA viewer or parse using an XML library.

</section>