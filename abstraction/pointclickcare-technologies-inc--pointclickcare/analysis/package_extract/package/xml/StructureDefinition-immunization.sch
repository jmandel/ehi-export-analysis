<?xml version="1.0" encoding="UTF-8"?>
<sch:schema xmlns:sch="http://purl.oclc.org/dsdl/schematron" queryBinding="xslt2">
  <sch:ns prefix="f" uri="http://hl7.org/fhir"/>
  <sch:ns prefix="h" uri="http://www.w3.org/1999/xhtml"/>
  <!-- 
    This file contains just the constraints for the profile Immunization
    It includes the base constraints for the resource as well.
    Because of the way that schematrons and containment work, 
    you may need to use this schematron fragment to build a, 
    single schematron that validates contained resources (if you have any) 
  -->
  <sch:pattern>
    <sch:title>f:Immunization</sch:title>
    <sch:rule context="f:Immunization">
      <sch:assert test="count(f:implicitRules) &lt;= 0">implicitRules: maximum cardinality of 'implicitRules' is 0</sch:assert>
      <sch:assert test="count(f:language) &lt;= 0">language: maximum cardinality of 'language' is 0</sch:assert>
      <sch:assert test="count(f:text) &lt;= 0">text: maximum cardinality of 'text' is 0</sch:assert>
      <sch:assert test="count(f:contained) &lt;= 0">contained: maximum cardinality of 'contained' is 0</sch:assert>
      <sch:assert test="count(f:extension[@url = 'https://ehi-export.pointclickcare.com/site/StructureDefinition-ImmunizationStatus.html']) &lt;= 1">extension with URL = 'https://ehi-export.pointclickcare.com/site/StructureDefinition-ImmunizationStatus.html': maximum cardinality of 'extension' is 1</sch:assert>
      <sch:assert test="count(f:modifierExtension) &lt;= 0">modifierExtension: maximum cardinality of 'modifierExtension' is 0</sch:assert>
      <sch:assert test="count(f:encounter) &lt;= 0">encounter: maximum cardinality of 'encounter' is 0</sch:assert>
      <sch:assert test="count(f:location) &lt;= 0">location: maximum cardinality of 'location' is 0</sch:assert>
      <sch:assert test="count(f:reasonCode) &lt;= 0">reasonCode: maximum cardinality of 'reasonCode' is 0</sch:assert>
      <sch:assert test="count(f:reasonReference) &lt;= 0">reasonReference: maximum cardinality of 'reasonReference' is 0</sch:assert>
      <sch:assert test="count(f:isSubpotent) &lt;= 0">isSubpotent: maximum cardinality of 'isSubpotent' is 0</sch:assert>
      <sch:assert test="count(f:subpotentReason) &lt;= 0">subpotentReason: maximum cardinality of 'subpotentReason' is 0</sch:assert>
      <sch:assert test="count(f:programEligibility) &lt;= 0">programEligibility: maximum cardinality of 'programEligibility' is 0</sch:assert>
      <sch:assert test="count(f:fundingSource) &lt;= 0">fundingSource: maximum cardinality of 'fundingSource' is 0</sch:assert>
      <sch:assert test="count(f:reaction) &lt;= 0">reaction: maximum cardinality of 'reaction' is 0</sch:assert>
      <sch:assert test="count(f:protocolApplied) &lt;= 0">protocolApplied: maximum cardinality of 'protocolApplied' is 0</sch:assert>
    </sch:rule>
  </sch:pattern>
</sch:schema>
