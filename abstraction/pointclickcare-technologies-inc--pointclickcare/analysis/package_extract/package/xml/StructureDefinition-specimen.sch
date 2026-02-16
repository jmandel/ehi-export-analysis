<?xml version="1.0" encoding="UTF-8"?>
<sch:schema xmlns:sch="http://purl.oclc.org/dsdl/schematron" queryBinding="xslt2">
  <sch:ns prefix="f" uri="http://hl7.org/fhir"/>
  <sch:ns prefix="h" uri="http://www.w3.org/1999/xhtml"/>
  <!-- 
    This file contains just the constraints for the profile Specimen
    It includes the base constraints for the resource as well.
    Because of the way that schematrons and containment work, 
    you may need to use this schematron fragment to build a, 
    single schematron that validates contained resources (if you have any) 
  -->
  <sch:pattern>
    <sch:title>f:Specimen</sch:title>
    <sch:rule context="f:Specimen">
      <sch:assert test="count(f:accessionIdentifier) &lt;= 0">accessionIdentifier: maximum cardinality of 'accessionIdentifier' is 0</sch:assert>
      <sch:assert test="count(f:status) &lt;= 0">status: maximum cardinality of 'status' is 0</sch:assert>
      <sch:assert test="count(f:receivedTime) &lt;= 0">receivedTime: maximum cardinality of 'receivedTime' is 0</sch:assert>
      <sch:assert test="count(f:parent) &lt;= 0">parent: maximum cardinality of 'parent' is 0</sch:assert>
      <sch:assert test="count(f:request) &lt;= 0">request: maximum cardinality of 'request' is 0</sch:assert>
      <sch:assert test="count(f:collection) &lt;= 0">collection: maximum cardinality of 'collection' is 0</sch:assert>
      <sch:assert test="count(f:processing) &lt;= 0">processing: maximum cardinality of 'processing' is 0</sch:assert>
      <sch:assert test="count(f:container) &lt;= 0">container: maximum cardinality of 'container' is 0</sch:assert>
      <sch:assert test="count(f:condition) &lt;= 0">condition: maximum cardinality of 'condition' is 0</sch:assert>
      <sch:assert test="count(f:note) &lt;= 0">note: maximum cardinality of 'note' is 0</sch:assert>
    </sch:rule>
  </sch:pattern>
</sch:schema>
