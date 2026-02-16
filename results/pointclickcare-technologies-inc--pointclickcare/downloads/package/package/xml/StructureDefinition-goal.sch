<?xml version="1.0" encoding="UTF-8"?>
<sch:schema xmlns:sch="http://purl.oclc.org/dsdl/schematron" queryBinding="xslt2">
  <sch:ns prefix="f" uri="http://hl7.org/fhir"/>
  <sch:ns prefix="h" uri="http://www.w3.org/1999/xhtml"/>
  <!-- 
    This file contains just the constraints for the profile Goal
    It includes the base constraints for the resource as well.
    Because of the way that schematrons and containment work, 
    you may need to use this schematron fragment to build a, 
    single schematron that validates contained resources (if you have any) 
  -->
  <sch:pattern>
    <sch:title>f:Goal</sch:title>
    <sch:rule context="f:Goal">
      <sch:assert test="count(f:statusReason) &lt;= 0">statusReason: maximum cardinality of 'statusReason' is 0</sch:assert>
      <sch:assert test="count(f:expressedBy) &lt;= 0">expressedBy: maximum cardinality of 'expressedBy' is 0</sch:assert>
      <sch:assert test="count(f:addresses) &lt;= 0">addresses: maximum cardinality of 'addresses' is 0</sch:assert>
      <sch:assert test="count(f:note) &lt;= 0">note: maximum cardinality of 'note' is 0</sch:assert>
      <sch:assert test="count(f:outcomeCode) &lt;= 0">outcomeCode: maximum cardinality of 'outcomeCode' is 0</sch:assert>
      <sch:assert test="count(f:outcomeReference) &lt;= 0">outcomeReference: maximum cardinality of 'outcomeReference' is 0</sch:assert>
    </sch:rule>
  </sch:pattern>
</sch:schema>
