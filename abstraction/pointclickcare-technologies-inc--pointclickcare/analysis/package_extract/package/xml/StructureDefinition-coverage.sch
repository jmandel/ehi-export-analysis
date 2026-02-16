<?xml version="1.0" encoding="UTF-8"?>
<sch:schema xmlns:sch="http://purl.oclc.org/dsdl/schematron" queryBinding="xslt2">
  <sch:ns prefix="f" uri="http://hl7.org/fhir"/>
  <sch:ns prefix="h" uri="http://www.w3.org/1999/xhtml"/>
  <!-- 
    This file contains just the constraints for the profile Coverage
    It includes the base constraints for the resource as well.
    Because of the way that schematrons and containment work, 
    you may need to use this schematron fragment to build a, 
    single schematron that validates contained resources (if you have any) 
  -->
  <sch:pattern>
    <sch:title>f:Coverage</sch:title>
    <sch:rule context="f:Coverage">
      <sch:assert test="count(f:implicitRules) &lt;= 0">implicitRules: maximum cardinality of 'implicitRules' is 0</sch:assert>
      <sch:assert test="count(f:language) &lt;= 0">language: maximum cardinality of 'language' is 0</sch:assert>
      <sch:assert test="count(f:contained) &lt;= 0">contained: maximum cardinality of 'contained' is 0</sch:assert>
      <sch:assert test="count(f:extension[@url = 'https://ehi-export.pointclickcare.com/site/StructureDefinition-MedicareAdvantagePlan.html']) &lt;= 1">extension with URL = 'https://ehi-export.pointclickcare.com/site/StructureDefinition-MedicareAdvantagePlan.html': maximum cardinality of 'extension' is 1</sch:assert>
      <sch:assert test="count(f:extension[@url = 'https://ehi-export.pointclickcare.com/site/StructureDefinition-CompanyName.html']) &lt;= 1">extension with URL = 'https://ehi-export.pointclickcare.com/site/StructureDefinition-CompanyName.html': maximum cardinality of 'extension' is 1</sch:assert>
      <sch:assert test="count(f:extension[@url = 'https://ehi-export.pointclickcare.com/site/StructureDefinition-ProviderNumber.html']) &lt;= 1">extension with URL = 'https://ehi-export.pointclickcare.com/site/StructureDefinition-ProviderNumber.html': maximum cardinality of 'extension' is 1</sch:assert>
      <sch:assert test="count(f:extension[@url = 'https://ehi-export.pointclickcare.com/site/StructureDefinition-PayerType.html']) &lt;= 1">extension with URL = 'https://ehi-export.pointclickcare.com/site/StructureDefinition-PayerType.html': maximum cardinality of 'extension' is 1</sch:assert>
      <sch:assert test="count(f:extension[@url = 'https://ehi-export.pointclickcare.com/site/StructureDefinition-PayerDescription.html']) &lt;= 1">extension with URL = 'https://ehi-export.pointclickcare.com/site/StructureDefinition-PayerDescription.html': maximum cardinality of 'extension' is 1</sch:assert>
      <sch:assert test="count(f:dependent) &lt;= 0">dependent: maximum cardinality of 'dependent' is 0</sch:assert>
      <sch:assert test="count(f:order) &lt;= 0">order: maximum cardinality of 'order' is 0</sch:assert>
      <sch:assert test="count(f:network) &lt;= 0">network: maximum cardinality of 'network' is 0</sch:assert>
      <sch:assert test="count(f:costToBeneficiary) &lt;= 0">costToBeneficiary: maximum cardinality of 'costToBeneficiary' is 0</sch:assert>
      <sch:assert test="count(f:subrogation) &lt;= 0">subrogation: maximum cardinality of 'subrogation' is 0</sch:assert>
      <sch:assert test="count(f:contract) &lt;= 0">contract: maximum cardinality of 'contract' is 0</sch:assert>
    </sch:rule>
  </sch:pattern>
  <sch:pattern>
    <sch:title>f:Coverage/f:class/f:type</sch:title>
    <sch:rule context="f:Coverage/f:class/f:type">
      <sch:assert test="count(f:id) &lt;= 1">id: maximum cardinality of 'id' is 1</sch:assert>
      <sch:assert test="count(f:coding) &gt;= 1">coding: minimum cardinality of 'coding' is 1</sch:assert>
      <sch:assert test="count(f:text) &lt;= 1">text: maximum cardinality of 'text' is 1</sch:assert>
    </sch:rule>
  </sch:pattern>
  <sch:pattern>
    <sch:title>f:Coverage/f:class/f:type/f:coding</sch:title>
    <sch:rule context="f:Coverage/f:class/f:type/f:coding">
      <sch:assert test="count(f:id) &lt;= 1">id: maximum cardinality of 'id' is 1</sch:assert>
      <sch:assert test="count(f:system) &lt;= 1">system: maximum cardinality of 'system' is 1</sch:assert>
      <sch:assert test="count(f:version) &lt;= 1">version: maximum cardinality of 'version' is 1</sch:assert>
      <sch:assert test="count(f:code) &gt;= 1">code: minimum cardinality of 'code' is 1</sch:assert>
      <sch:assert test="count(f:code) &lt;= 1">code: maximum cardinality of 'code' is 1</sch:assert>
      <sch:assert test="count(f:display) &lt;= 1">display: maximum cardinality of 'display' is 1</sch:assert>
      <sch:assert test="count(f:userSelected) &lt;= 1">userSelected: maximum cardinality of 'userSelected' is 1</sch:assert>
    </sch:rule>
  </sch:pattern>
</sch:schema>
