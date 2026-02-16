<?xml version="1.0" encoding="UTF-8"?>
<sch:schema xmlns:sch="http://purl.oclc.org/dsdl/schematron" queryBinding="xslt2">
  <sch:ns prefix="f" uri="http://hl7.org/fhir"/>
  <sch:ns prefix="h" uri="http://www.w3.org/1999/xhtml"/>
  <!-- 
    This file contains just the constraints for the profile Patient
    It includes the base constraints for the resource as well.
    Because of the way that schematrons and containment work, 
    you may need to use this schematron fragment to build a, 
    single schematron that validates contained resources (if you have any) 
  -->
  <sch:pattern>
    <sch:title>f:Patient</sch:title>
    <sch:rule context="f:Patient">
      <sch:assert test="count(f:extension[@url = 'http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex']) &lt;= 1">extension with URL = 'http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex': maximum cardinality of 'extension' is 1</sch:assert>
      <sch:assert test="count(f:extension[@url = 'http://hl7.org/fhir/us/core/StructureDefinition/us-core-genderIdentity']) &lt;= 1">extension with URL = 'http://hl7.org/fhir/us/core/StructureDefinition/us-core-genderIdentity': maximum cardinality of 'extension' is 1</sch:assert>
      <sch:assert test="count(f:extension[@url = 'http://hl7.org/fhir/us/core/StructureDefinition/us-core-race']) &lt;= 1">extension with URL = 'http://hl7.org/fhir/us/core/StructureDefinition/us-core-race': maximum cardinality of 'extension' is 1</sch:assert>
      <sch:assert test="count(f:extension[@url = 'http://hl7.org/fhir/StructureDefinition/individual-pronouns']) &lt;= 1">extension with URL = 'http://hl7.org/fhir/StructureDefinition/individual-pronouns': maximum cardinality of 'extension' is 1</sch:assert>
      <sch:assert test="count(f:extension[@url = 'http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity']) &lt;= 1">extension with URL = 'http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity': maximum cardinality of 'extension' is 1</sch:assert>
      <sch:assert test="count(f:extension[@url = 'http://hl7.org/fhir/us/core/StructureDefinition/us-core-sex']) &lt;= 1">extension with URL = 'http://hl7.org/fhir/us/core/StructureDefinition/us-core-sex': maximum cardinality of 'extension' is 1</sch:assert>
      <sch:assert test="count(f:extension[@url = 'http://hl7.org/fhir/us/core/StructureDefinition/us-core-sex']) &lt;= 1">extension with URL = 'http://hl7.org/fhir/us/core/StructureDefinition/us-core-sex': maximum cardinality of 'extension' is 1</sch:assert>
      <sch:assert test="count(f:extension[@url = 'http://hl7.org/fhir/us/core/StructureDefinition/us-core-tribal-affiliation']) &lt;= 1">extension with URL = 'http://hl7.org/fhir/us/core/StructureDefinition/us-core-tribal-affiliation': maximum cardinality of 'extension' is 1</sch:assert>
      <sch:assert test="count(f:extension[@url = 'http://terminology.hl7.org/CodeSystem/soc']) &lt;= 1">extension with URL = 'http://terminology.hl7.org/CodeSystem/soc': maximum cardinality of 'extension' is 1</sch:assert>
      <sch:assert test="count(f:extension[@url = 'http://terminology.hl7.org/CodeSystem/v2-0200']) &lt;= 1">extension with URL = 'http://terminology.hl7.org/CodeSystem/v2-0200': maximum cardinality of 'extension' is 1</sch:assert>
      <sch:assert test="count(f:maritalStatus) &lt;= 0">maritalStatus: maximum cardinality of 'maritalStatus' is 0</sch:assert>
      <sch:assert test="count(f:multipleBirth[x]) &lt;= 0">multipleBirth[x]: maximum cardinality of 'multipleBirth[x]' is 0</sch:assert>
      <sch:assert test="count(f:link) &lt;= 0">link: maximum cardinality of 'link' is 0</sch:assert>
    </sch:rule>
  </sch:pattern>
</sch:schema>
