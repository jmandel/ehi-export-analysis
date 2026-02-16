<?xml version="1.0" encoding="UTF-8"?>
<sch:schema xmlns:sch="http://purl.oclc.org/dsdl/schematron" queryBinding="xslt2">
  <sch:ns prefix="f" uri="http://hl7.org/fhir"/>
  <sch:ns prefix="h" uri="http://www.w3.org/1999/xhtml"/>
  <!-- 
    This file contains just the constraints for the profile ServiceRequest
    It includes the base constraints for the resource as well.
    Because of the way that schematrons and containment work, 
    you may need to use this schematron fragment to build a, 
    single schematron that validates contained resources (if you have any) 
  -->
  <sch:pattern>
    <sch:title>f:ServiceRequest</sch:title>
    <sch:rule context="f:ServiceRequest">
      <sch:assert test="count(f:implicitRules) &lt;= 0">implicitRules: maximum cardinality of 'implicitRules' is 0</sch:assert>
      <sch:assert test="count(f:language) &lt;= 0">language: maximum cardinality of 'language' is 0</sch:assert>
      <sch:assert test="count(f:contained) &lt;= 0">contained: maximum cardinality of 'contained' is 0</sch:assert>
      <sch:assert test="count(f:extension) &lt;= 0">extension: maximum cardinality of 'extension' is 0</sch:assert>
      <sch:assert test="count(f:modifierExtension) &lt;= 0">modifierExtension: maximum cardinality of 'modifierExtension' is 0</sch:assert>
      <sch:assert test="count(f:identifier) &lt;= 0">identifier: maximum cardinality of 'identifier' is 0</sch:assert>
      <sch:assert test="count(f:instantiatesCanonical) &lt;= 0">instantiatesCanonical: maximum cardinality of 'instantiatesCanonical' is 0</sch:assert>
      <sch:assert test="count(f:instantiatesUri) &lt;= 0">instantiatesUri: maximum cardinality of 'instantiatesUri' is 0</sch:assert>
      <sch:assert test="count(f:basedOn) &lt;= 0">basedOn: maximum cardinality of 'basedOn' is 0</sch:assert>
      <sch:assert test="count(f:replaces) &lt;= 0">replaces: maximum cardinality of 'replaces' is 0</sch:assert>
      <sch:assert test="count(f:requisition) &lt;= 0">requisition: maximum cardinality of 'requisition' is 0</sch:assert>
      <sch:assert test="count(f:category) &lt;= 0">category: maximum cardinality of 'category' is 0</sch:assert>
      <sch:assert test="count(f:priority) &lt;= 0">priority: maximum cardinality of 'priority' is 0</sch:assert>
      <sch:assert test="count(f:doNotPerform) &lt;= 0">doNotPerform: maximum cardinality of 'doNotPerform' is 0</sch:assert>
      <sch:assert test="count(f:orderDetail) &lt;= 0">orderDetail: maximum cardinality of 'orderDetail' is 0</sch:assert>
      <sch:assert test="count(f:quantity[x]) &lt;= 0">quantity[x]: maximum cardinality of 'quantity[x]' is 0</sch:assert>
      <sch:assert test="count(f:encounter) &lt;= 0">encounter: maximum cardinality of 'encounter' is 0</sch:assert>
      <sch:assert test="count(f:occurrence[x]) &lt;= 0">occurrence[x]: maximum cardinality of 'occurrence[x]' is 0</sch:assert>
      <sch:assert test="count(f:asNeeded[x]) &lt;= 0">asNeeded[x]: maximum cardinality of 'asNeeded[x]' is 0</sch:assert>
      <sch:assert test="count(f:authoredOn) &lt;= 0">authoredOn: maximum cardinality of 'authoredOn' is 0</sch:assert>
      <sch:assert test="count(f:requester) &lt;= 0">requester: maximum cardinality of 'requester' is 0</sch:assert>
      <sch:assert test="count(f:performerType) &lt;= 0">performerType: maximum cardinality of 'performerType' is 0</sch:assert>
      <sch:assert test="count(f:performer) &lt;= 0">performer: maximum cardinality of 'performer' is 0</sch:assert>
      <sch:assert test="count(f:locationCode) &lt;= 0">locationCode: maximum cardinality of 'locationCode' is 0</sch:assert>
      <sch:assert test="count(f:locationReference) &lt;= 0">locationReference: maximum cardinality of 'locationReference' is 0</sch:assert>
      <sch:assert test="count(f:reasonCode) &lt;= 0">reasonCode: maximum cardinality of 'reasonCode' is 0</sch:assert>
      <sch:assert test="count(f:insurance) &lt;= 0">insurance: maximum cardinality of 'insurance' is 0</sch:assert>
      <sch:assert test="count(f:supportingInfo) &lt;= 0">supportingInfo: maximum cardinality of 'supportingInfo' is 0</sch:assert>
      <sch:assert test="count(f:specimen) &lt;= 0">specimen: maximum cardinality of 'specimen' is 0</sch:assert>
      <sch:assert test="count(f:bodySite) &lt;= 0">bodySite: maximum cardinality of 'bodySite' is 0</sch:assert>
      <sch:assert test="count(f:note) &lt;= 0">note: maximum cardinality of 'note' is 0</sch:assert>
      <sch:assert test="count(f:patientInstruction) &lt;= 0">patientInstruction: maximum cardinality of 'patientInstruction' is 0</sch:assert>
      <sch:assert test="count(f:relevantHistory) &lt;= 0">relevantHistory: maximum cardinality of 'relevantHistory' is 0</sch:assert>
    </sch:rule>
  </sch:pattern>
</sch:schema>
