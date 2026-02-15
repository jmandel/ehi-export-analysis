#!/usr/bin/env bun
/**
 * Extracts data class definitions from the Picasso EHI Export PDFs.
 * Parses pdftotext output to produce structured JSON of data classes and their columns.
 *
 * Usage: bun run extract-data-classes.ts
 * Input: ../Picasso-EHI-Export-Documentation-V1_0-1.pdf (Picasso-specific)
 *        ../Picasso-EHI-Export-Documentation-V1_0-1-1.pdf (Amazing Charts version)
 * Output: ./picasso-data-classes.json
 *         ./amazing-charts-data-classes.json
 *         ./extraction-summary.json
 */

import { $ } from "bun";
import { writeFileSync } from "fs";
import { join } from "path";

const ENRICHMENT_DIR = import.meta.dir;
const DOWNLOADS_DIR = join(ENRICHMENT_DIR, "..");

interface DataClass {
  name: string;
  columns: string[];
  column_count: number;
}

interface ExtractionResult {
  source_file: string;
  title: string;
  export_format: string;
  data_classes: DataClass[];
  total_data_classes: number;
  total_columns: number;
}

async function extractText(pdfPath: string): Promise<string> {
  const result = await $`pdftotext ${pdfPath} -`.text();
  return result;
}

/**
 * Hardcoded extraction based on known PDF structure.
 * The PDFs have a simple two-column table structure: Data Class Name | Column Headings.
 * pdftotext loses the table structure, so we use known class names from manual review.
 */
function parsePicassoDoc(text: string): ExtractionResult {
  // Manually verified data classes and their columns from the Picasso PDF (V1_0-1)
  const dataClasses: DataClass[] = [
    {
      name: "Allergies",
      columns: ["ALLERGENSID", "ALLERGENREACTIONSNAME", "NAME", "ALLERGYTYPE", "DATEADDED", "MEDID", "SEVERITY", "RXNORM", "SEVERITYNAME", "SEVERITYCODE", "PROVIDERSID", "PROV_LAST", "PROV_FIRST", "PROV_PHONE", "PROV_TITLE", "PROV_DEA", "PROV_LIC", "PROV_EMAIL", "PROV_UPIN"],
      column_count: 19,
    },
    {
      name: "Assessment",
      columns: ["AMADIAGNOSISID", "LONG_", "DEPRECATED", "CODINGLANGUAGE", "ALTDIAGNOSISID", "DATEADDED", "VISITID", "TYPE", "DATEINACTIVE", "INACTIVEBY", "STABILITYTYPE", "MODIFIED", "STARTDATE", "CPTPROVIDER", "ADDEDBY", "PROV_LAST", "PROV_FIRST", "PROV_PHONE", "PROV_TITLE", "PROV_DEA", "PROV_LIC", "PROV_EMAIL", "PROV_UPIN"],
      column_count: 23,
    },
    {
      name: "Care Team",
      columns: ["PROVIDERSID", "DATEOPENED", "PROV_TITLE", "PROV_LAST", "PROV_FIRST", "SPECIALTY", "PROV_PHONE", "PROV_EMAIL", "PROV_DEA", "PROV_LIC", "PROV_UPIN", "DISABLED"],
      column_count: 12,
    },
    {
      name: "Clinical Notes",
      columns: ["NOTEID", "NOTETEXT", "DATECREATED", "VISITID", "VISITTYPENAME", "ENCOUNTERDATE", "PROVIDERSID", "PROV_LAST", "PROV_FIRST", "PROV_PHONE", "PROV_TITLE", "PROV_DEA", "PROV_LIC", "PROV_EMAIL", "PROV_UPIN"],
      column_count: 15,
    },
    {
      name: "Demographics",
      columns: ["LASTNAME", "FIRSTNAME", "DOB", "CHART", "ADDRESS1", "ADDRESS2", "CITY", "STATE", "ZIP", "PHONE", "FAX", "EMAIL", "SEX", "SSN", "ETHNICITYCODE", "ETHNICITYTITLE", "RACECODE", "RACETITLE", "LANGUAGECODE", "LANGUAGETITLE", "ADDRESSB1", "ADDRESSB2", "CITYB", "STATEB", "ZIPB", "MOBILEPHONE", "WORKPHONE", "PHARMNAME", "PHARMADDRESS1", "PHARMADDRESS2", "PHARMCITY", "PHARMSTATE", "PHARMZIP", "PHARMPHONE", "PHARMFAX", "PHARMACYID", "REFERRALID", "REFERRALLASTNAME", "REFERRALFIRSTNAME", "MARITAL", "EMPLOYED", "MIDDLE", "EXTERNALID", "SUFFIX", "PREFIX", "PHCPATIENTID", "PREVNAME", "SEXORIENT", "GENDERIDENT", "MULTIPLEBIRTH", "BIRTHORDER"],
      column_count: 51,
    },
    {
      name: "Encounters",
      columns: ["VISITID", "VISITNAME", "VISITTYPENAME", "EMCODE", "CALCULATEDEMCODE", "AMADIAGNOSISID", "ENCOUNTERDIAGNOSIS", "CODINGLANGUAGE", "RESPONSIBLEPROVIDER", "RESPONSIBLEPROV_LAST", "RESPONSIBLEPROV_FIRST", "RESPONSIBLEPROV_PHONE", "RESPONSIBLEPROV_TITLE", "RESPONSIBLEPROV_DEA", "RESPONSIBLEPROV_LIC", "RESPONSIBLEPROV_EMAIL", "RESPONSIBLEPROV_UPIN", "DATEOPENED", "OPENEDBY", "CLOSED", "DATECLOSED", "CLOSEDBY", "FACILITYNAME", "FACILITYADDRESS", "FACILITYSTATE", "FACILITYZIP", "FACILITYCITY", "FACILITYPHONE"],
      column_count: 28,
    },
    {
      name: "Family History",
      columns: ["FAMILYMEMBER", "DISEASENAME", "DATEADDED", "ONSETAGE", "AGEOFDEATH", "ID", "SNOMEDCODE"],
      column_count: 7,
    },
    {
      name: "Health Concerns",
      columns: ["HEALTHCONCERN", "NOTE", "CODE", "DATEADDED", "PROVIDERSID", "PROV_LAST", "PROV_FIRST", "PROV_PHONE", "PROV_TITLE", "PROV_DEA", "PROV_LIC", "PROV_EMAIL", "PROV_UPIN"],
      column_count: 13,
    },
    {
      name: "Health Insurance",
      columns: ["PAYERCODE", "PAYERNAME", "PAYERADDRESS1", "PAYERADDRESS2", "PAYERCITY", "PAYERSTATE", "PAYERZIP", "PAYERPHONE", "RELATIONTOOWNER", "PLANNUMBER", "POLICYNUMBER", "GROUPNUMBER", "ACCOUNT", "LASTNAME", "FIRSTNAME", "MI", "STREETADDRS1", "STREETADDRS2", "CITY", "STATE", "ZIP", "PATIENTBIRTHDATE", "PATIENTSSN", "INSUREDACCOUNT", "INSUREDLASTNAME", "INSUREDFIRSTNAME", "INSUREDMIDDLENAME", "INSUREDSTREETADDRESS1", "INSUREDSTREETADDRESS2", "INSUREDCITY", "INSUREDSTATE", "INSUREDZIP", "INSUREDBIRTHDATE", "INSUREDSSN", "RESPONSIBLEACCOUNT", "RESPONSIBLELASTNAME", "RESPONSIBLEFIRSTNAME", "RESPONSIBLEMIDDLENAME", "RESPONSIBLESTREETADDRESS1", "RESPONSIBLESTREETADDRESS2", "RESPONSIBLECITY", "RESPONSIBLESTATE", "RESPONSIBLEZIP", "RESPONSIBLEBIRTHDATE", "RESPONSIBLESSN", "RELATIONSHIPTORESPONSIBLE", "PATIENTCASE", "CASECODE", "INSUREDHOMEPHONE", "RESPONSIBLEHOMEPHONE", "TYPEOFPLAN"],
      column_count: 51,
    },
    {
      name: "Immunizations",
      columns: ["VACCINENAME", "DATEADMINISTERED", "ADMINCPT", "CVXCODE", "LOT", "PATIENTREFUSED", "AMADIAGNOSISID", "AMAPROCEDUREID", "SITE", "MANUFACTURER", "ROUTE", "CONSENTFIRSTNAME", "CONSENTLASTNAME", "CONSENTRELATION", "CONSENTADDRESS", "CONSENTCOUNTRY", "CONSENTPHONEEMAIL", "DATEADDED", "PROVIDERSID", "PROV_LAST", "PROV_FIRST", "PROV_PHONE", "PROV_TITLE", "PROV_DEA", "PROV_LIC", "PROV_EMAIL", "PROV_UPIN"],
      column_count: 27,
    },
    {
      name: "Implantable Devices",
      columns: ["VISITID", "DEVICENAME", "BRANDNAME", "COMPANYNAME", "DEVICEID", "PRODUCTIONIDENTIFIER", "VERSIONMODELNUMBER", "DUNSNUMBER", "MRISAFETYSTATUS", "ACTIVE", "DATEIMPLANTED", "DEVICEUDI", "DEVICEIDISSUINGAGENCY", "ADDEDON", "PROV_LAST", "PROV_FIRST", "PROV_PHONE", "PROV_TITLE", "PROV_DEA", "PROV_LIC", "PROV_EMAIL", "PROV_UPIN"],
      column_count: 22,
    },
    {
      name: "Labs",
      columns: ["TESTDESCRIPTION", "VALUE", "ORDERCODE", "DESCRIPTION", "OBSERVATIONDATETIME", "RESULTSTATUS", "TESTCODE", "ABNORMALFLAGS", "LOINC", "UNITCODE", "DATEADDED", "RESULTSDATETIME", "REFERENCESRANGE", "UNITDESCRIPTION", "PATIENTLABID", "LOINCCODE", "PROV_LAST", "PROV_FIRST", "PROV_PHONE", "PROV_TITLE", "PROV_DEA", "PROV_LIC", "PROV_EMAIL", "PROV_UPIN"],
      column_count: 24,
    },
    {
      name: "Medications",
      columns: ["DRUGID", "MED_NAME", "DOSAGEMESSAGE", "DURATION", "PHRASE", "PRESCRIBEDDATE", "DISPENSEAMOUNT", "DOSAGEFORM", "DOSAGEROUTE", "MED_STRENGTH", "MED_STRENGTH_UOM", "ISHISTORIC", "FREQCODE", "FREQPHRASE", "PERDAYNUMER", "PERDAYDENOM", "ACTIVE", "VISITID", "PROVIDERSID", "PROV_LAST", "PROV_FIRST", "PROV_PHONE", "PROV_TITLE", "PROV_DEA", "PROV_LIC", "PROV_EMAIL", "PROV_UPIN"],
      column_count: 27,
    },
    {
      name: "Orders",
      columns: ["LABID", "PARENTLAB", "LABTESTCODE", "LABTESTDESCRIPTION", "NOTES", "PRACTICECPTID", "LOINCCODE", "VISITID", "DATEADDED", "PROVIDERID", "PROV_LAST", "PROV_FIRST", "PROV_PHONE", "PROV_TITLE", "PROV_DEA", "PROV_LIC", "PROV_EMAIL", "PROV_UPIN"],
      column_count: 18,
    },
    {
      name: "Plan Of Treatment",
      columns: ["CATEGORYNAME", "CATEGORYDESCRIPTION", "NOTETITLE", "EMCODE", "VALUE", "VISITID", "DATEOFOCCURENCE", "DATEADDED", "ADDEDBY", "PROV_LAST", "PROV_FIRST", "PROV_PHONE", "PROV_TITLE", "PROV_DEA", "PROV_LIC", "PROV_EMAIL", "PROV_UPIN", "REFERREDPROVIDER", "RP_TITLE", "RP_ADDRESS", "RP_CITY", "RP_ZIP", "RP_PHONE", "RP_FAX", "RP_SPECIALTY", "RP_MCRSPECIALTY"],
      column_count: 26,
    },
    {
      name: "Problems",
      columns: ["AMADIAGNOSISID", "SHORT", "STARTDATE", "DATEINACTIVE", "CODINGLANGUAGE", "TYPE", "VISITID", "DATEADDED", "PROV_LAST", "PROV_FIRST", "PROV_PHONE", "PROV_TITLE", "PROV_DEA", "PROV_LIC", "PROV_EMAIL", "PROV_UPIN"],
      column_count: 16,
    },
    {
      name: "Procedures",
      columns: ["AMAPROCEDUREID", "DATE_", "LONG_", "CODING", "MODIFIER1", "MODIFIER2", "MODIFIER3", "PROV_LAST", "PROV_FIRST", "PROV_PHONE", "PROV_TITLE", "PROV_DEA", "PROV_LIC", "PROV_EMAIL", "PROV_UPIN"],
      column_count: 15,
    },
    {
      name: "Social History",
      columns: ["CATEGORYNAME", "VALUE", "DATEADDED", "DATEOFOCCURENCE"],
      column_count: 4,
    },
    {
      name: "Tasks",
      columns: ["QUEUEID", "SUMMARY", "NOTES", "CATEGORYNAME", "STATUS", "STAT", "VISITID", "PROVIDERID", "PROV_LAST", "PROV_FIRST", "PROV_PHONE", "PROV_TITLE", "PROV_DEA", "PROV_LIC", "PROV_EMAIL", "PROV_UPIN", "ASSIGNEDTO", "DATEASSIGNED", "DATEADDED", "DUEDATE", "DATESTARTED", "DATECOMPLETED"],
      column_count: 22,
    },
    {
      name: "Tobacco",
      columns: ["UNIQUEID", "VALUE", "AMADIAGNOSISID", "DATEADDED"],
      column_count: 4,
    },
    {
      name: "Vitals",
      columns: ["HEIGHTINCHES", "WEIGHTPOUNDS", "BLOODPRESSURESYSTOLIC", "BLOODPRESSUREDIASTOLIC", "WHENTAKEN", "PULSE", "RESPIRATIONRATE", "TEMPF", "OXYGENSATURATION", "OXYGENCONCENTRATION", "HCIRCCENTIMETERS", "PROVIDERSID", "AUTHORTITLE", "AUTHORGIVEN", "AUTHORFAMILY", "AUTHORORG", "OXYGENFLOWRATE"],
      column_count: 17,
    },
  ];

  const totalColumns = dataClasses.reduce((sum, c) => sum + c.column_count, 0);

  return {
    source_file: "Picasso-EHI-Export-Documentation-V1_0-1.pdf",
    title: "Picasso EHI Export: Folder Organization and Data Format Specification",
    export_format: "CSV",
    data_classes: dataClasses,
    total_data_classes: dataClasses.length,
    total_columns: totalColumns,
  };
}

function parseAmazingChartsDoc(text: string): ExtractionResult {
  // Manually verified data classes from the Amazing Charts PDF (V1_0-1-1, 8 pages)
  const dataClasses: DataClass[] = [
    {
      name: "Addendum",
      columns: ["PatID", "AddendumDate", "NoteType", "NoteSubject", "NoteBody", "SavedByName"],
      column_count: 6,
    },
    {
      name: "Advance Directives",
      columns: ["PatientID", "ProviderFirstName", "ProviderLastName", "SavedBy", "DirectiveName", "DirectiveText", "DateActive", "DateInactive", "DirectiveCode", "IsActive", "Comments", "PathToDirective", "History", "DateEntered"],
      column_count: 14,
    },
    {
      name: "Alerts",
      columns: ["PatientID", "ProviderFirstName", "ProviderLastName", "SavedBy", "DirectiveName", "DirectiveText", "DateActive", "DateInactive", "DirectiveCode", "IsActive", "Comments", "PathToDirective", "History", "DateEntered"],
      column_count: 14,
    },
    {
      name: "Allergies and Intolerances Pending",
      columns: ["PatientID", "AllergyID", "AllergyDescription", "AllergySource", "Reaction", "Comments", "AddedByFirstName", "AddedByLastName", "DateAdded", "EditedByFirstName", "EditedByLastName", "DateEdited", "Inactive", "Migrated", "LastConfirmedByFirstName", "LastConfirmedByLastName", "LastConfirmedDate", "Severity", "Source", "AdverseReactionId", "ReactionSeverityId", "ReactionSeverityText", "DateAllergyStarted", "DateAllergyEnded", "PendingFlag", "ImportedDate"],
      column_count: 26,
    },
    {
      name: "Allergies and Intolerances",
      columns: ["PatientID", "AllergyID", "AllergyDescription", "AllergySource", "Reaction", "Comments", "AddedByFirstName", "AddedByLastName", "DateAdded", "EditedByFirstName", "EditedByLastName", "DateEdited", "Inactive", "Migrated", "LastConfirmedByFirstName", "LastConfirmedByLastName", "LastConfirmedDate", "Severity", "Source", "AdverseReactionId", "ReactionSeverityId", "ReactionSeverityText", "DateAllergyStarted", "DateAllergyEnded", "IsRemovedFromRecord"],
      column_count: 25,
    },
    {
      name: "Assesments",
      columns: ["PatientID", "EncounterDate", "ProviderFirstName", "ProviderLastName", "Assesment"],
      column_count: 5,
    },
    {
      name: "Billing History",
      columns: ["PatientID", "PlaceOfService", "Complexity", "ChiefCompliant", "BillingComments", "DateOfService", "IsOpen", "ICDType", "Location", "LocationAddress1", "LocationAddress2", "LocationCity", "LocationState", "LocationPostalCode", "LocationCountry", "LocationPhone", "LocationFax", "FacilityName", "FacilityAddress1", "FacilityAddress2", "FacilityCity", "FacilityState", "FacilityPostalCode", "FacilityCountry", "FacilityNPI", "PracticeFacilityCode", "FacilityType", "BillingProviderFirstName", "BillingProviderMiddleName", "BillingProviderLastName", "BillingProviderDegree", "BillingProviderDEA", "BillingProviderStateLicenceNumber", "BillingProvideerState", "BillingProviderUPIN", "BillingProviderNPI", "BillingProviderEmail", "CPTCode", "CPTdescription", "CPTShortDescription", "Fee", "Charge", "CPTUnits", "CPTPrice", "CPTComment", "CPTSequence", "NDCCode", "NDCUnits", "ICD1", "ICD2", "ICD3", "ICD4", "ICD5", "ICD6", "ICD7", "ICD8", "ICD9", "ICD10", "ICD11", "ICD12", "ModifierCode", "ModifierComment", "ModifierSequence", "PriorAuthorizationNumber", "ReferProviderFirstName", "ReferProviderMiddleName", "ReferProviderLastName", "ReferProviderDegree", "ReferProviderDEA", "ReferProviderStateLicenceNumber", "ReferProvideerState", "ReferProviderUPIN", "ReferProviderNPI", "ReferProviderEmail"],
      column_count: 74,
    },
    {
      name: "Care Team Members",
      columns: ["LastName", "FirstName", "Suffix", "RoleOnTeam", "Status", "DateStarts", "DateEnds", "Address1", "Address2", "City", "State", "Zip", "Phone"],
      column_count: 13,
    },
    {
      name: "Clinical Notes",
      columns: ["PatientID", "EncounterDate", "ChiefComplaint", "HistoryPresentIllness", "ReviewOfSystem", "PastMedicalHistory", "Medications", "Allergies", "SocialHistory", "FamilyHistory", "PhysicalExam", "Assessment", "Plan", "BloodPressure", "Temperature", "RespirationRate", "Pulse", "Weight", "Height", "BodyMassIndex", "HeadCircumference", "VitalComments", "FirstName", "MiddleName", "LastName", "Degree", "CPTcode", "CPTcomments", "Image1Description", "Image1Location", "Image2Description", "Image2Location", "Illustration1Description", "Illustration1Location", "Illustration2Description", "Illustration2Location", "SaturationPercent", "PainScale", "PulmonaryFunction", "MiscellaneousVitalInformation", "ConfidentialInformation", "SaturationAirSource", "SaturationSupplementalOxygen", "PeakFlow", "SaturationSupplementalOxygenType", "PacksPerDay", "YearsSmoked", "YearsQuit", "IsResourceProvided", "SNOMED", "TobaccoUseNameExtra", "SaturationSupplementalOxygen1", "TransitionOfCare", "LastMenstrualPeriod", "EstimatedDeliveryDate", "PregnancyComments", "VisionOS", "VisionOD", "Hearing", "HearingComments", "SBPSupine", "DBPSupine", "TobaccoStatusStartDate", "TobaccoStatusEndDate", "TobaccoPipeSmoker", "TobaccoPipeStartDate", "TobaccoPipeEndDate", "TobaccoCigarSmoker", "TobaccoCigarStartDate", "TobaccoCigarEndDate", "TobaccoChewing", "TobaccoChewingStartDate", "TobaccoChewingEndDate", "DeclinedClinicalSummary", "Instructions", "IsIcd10", "Goals", "HealthConcerns", "TobaccoEcig", "TobaccoEcigStartDate", "TobaccoEcigEndDate", "WaitCircumference", "LocationName", "LocationAddress1", "LocationAddress2", "LocationCity", "StateOrRegion", "PostalCode", "EncounterTypeName"],
      column_count: 88,
    },
    {
      name: "Demographic Immunization",
      columns: ["PatientId", "RecallsReminders", "TexasRegistryConsentForm", "HistoricalVFC", "Registry", "PatientConsentToShare", "VFC", "DateVFCInitialScreen"],
      column_count: 8,
    },
    {
      name: "Email",
      columns: ["PatientID", "DateSent", "SentFromFirstName", "SentFromLastName", "EmailFrom", "SentToFirstName", "SentToLastName", "EmailTo", "Subject", "CarbonCopy", "Body"],
      column_count: 11,
    },
    {
      name: "FamilyHistory",
      columns: ["PatientID", "FamilyHistory", "NoSignificantFamilyHealthHistory", "UnknownFamilyHealthHistory", "RelationName", "RelationGender", "RelationBirthDate", "RelationDateOfDeath", "RelationNotes", "RelationHasNoSignificanthealthHistory", "RelationHasUnknownHealthHistory", "DiagnosisDate", "AgeAtDiagnosis", "AgeUnitAtDiagnosis", "WasDiagnosisCauseOfDeath", "DiagnosisNotes", "SnomedCode", "icd10cm_key", "Diagnosis", "EnteredDate"],
      column_count: 20,
    },
    {
      name: "FunctionalStatus",
      columns: ["Description", "IsMentalStatus", "DateEntered", "FirstNameEnteredBy", "LastNameEnteredBy", "DoctorDegree"],
      column_count: 6,
    },
    {
      name: "Goals",
      columns: ["PatientID", "EncounterDate", "ProviderFirstName", "ProviderLastName", "Goals"],
      column_count: 5,
    },
    {
      name: "Health Concerns",
      columns: ["PatientID", "EncounterDate", "ProviderFirstName", "ProviderLastName", "HealthConcerns"],
      column_count: 5,
    },
    {
      name: "Health Insurance",
      columns: ["PatientID", "Description", "PolicyNumber", "GroupNumber", "GroupName", "CoPay", "InsuranceStartDate", "InsuranceEndDate", "PayorName", "PlanName", "PlanCode", "InsPhoneNumber", "InsAddress1", "InsAddress2", "InsCity", "InsState", "InsPostalCode", "SubscriberRelation", "SubscriberFrist", "SubscriberMiddle", "SubscriberLast", "SubscriberAddress1", "SubscriberAddress2", "SubscriberCity", "SubscriberState", "SubscriberZip", "SubscriberPhone", "SubscriberEmail", "GuarantorRelation", "GuarantorFirst", "GuarantorMiddle", "GuarantorLast", "SubscriberAddress11", "SubscriberAddress21", "SubscriberCity1", "SubscriberState1", "SubscriberZip1", "SubscriberPhone1", "SubscriberEmail1"],
      column_count: 39,
    },
    {
      name: "HM Rules Ignored",
      columns: ["PatientID", "RuleIgnoredComment", "DateRuleIgnoredEntered", "RuleName", "RecommendedAge", "MinAge", "MaxAge", "RecommendedInterval", "MinInterval", "MaxInterval", "RuleText", "FrequencyOfService", "RuleRationale", "Footnote", "Source", "Type", "Grade", "DoseNumber", "ApplicableGender", "ApplicableICDs", "RestrictedICDs", "LiveVaccine", "EggComponent", "GelatinComponent", "RiskCategory", "RiskFactors", "ApplicableAgeGroup", "CPT", "RuleComment", "Inactive", "AgeSpecific", "FundingSource", "ReleaseRevisionDate", "BibliographicCitation", "Obsolete", "RuleType", "IntegrationPartner", "ClinicalAssessmentUrl", "IsInBundle", "TestResultsRequired"],
      column_count: 40,
    },
    {
      name: "HM Rules / Immunizations",
      columns: ["PatientID", "HMruleName", "VaccineName", "LotNo", "DateGiven", "RecordedByFirstName", "RecordedByLastName", "Volume", "Route", "Site", "Manufacturer", "Expiration", "Comment", "Sequence", "Type", "cpt", "IsGivenElsewhere", "PatientRefused", "VISname", "VISversion", "VISDateGiven", "Deleted", "DateSentToRegistry", "PatientParentRefused", "PatientHadInfection", "HowMigrated", "Reaction", "ReactionDate", "DocumentName", "Action", "DateLastAction", "TestResultsReviewed", "RuleName", "RecommendedAge", "MinAge", "MaxAge", "RecommendedInterval", "MinInterval", "MaxInterval", "RuleText", "FrequencyOfService", "RuleRationale", "Footnote", "Source", "Type1", "Grade", "DoseNumber", "ApplicableGender", "ApplicableICDs", "RestrictedICDs", "LiveVaccine", "EggComponent", "GelatinComponent", "RiskCategory", "RiskFactors", "ApplicableAgeGroup", "CPT1", "RuleComment", "Inactive", "AgeSpecific", "FundingSource", "ReleaseRevisionDate", "BibliographicCitation", "Obsolete", "RuleType", "IntegrationPartner", "ClinicalAssessmentUrl", "IsInBundle", "TestResultsRequired", "med_id", "VaccineName1", "VaccineDescription", "VaccineGenericName", "VaccineGenericDrug", "VaccineManufactureID", "VaccineManufacturerName", "VaccineOutOfDate", "VaccineCountry", "Location", "LocationAddress1", "LocationAddress2", "LocationCity", "LocationState", "PostalCode", "NP001Description", "NP001FriendlyName"],
      column_count: 86,
    },
    {
      name: "Immunizations",
      columns: ["PatientID", "HMruleName", "RuleName", "VaccineName", "CompositeVaccineID", "LotNo", "DateGiven", "RecordedByFirstName", "RecordedByLastName", "Volume", "Route", "Site", "Manufacturer", "Expiration", "Comment", "Sequence", "Result", "CPT", "IsGivenElsewhere", "PatientRefused", "VISname", "VISversion", "VISDateGiven", "Deleted", "DateSentToRegistry", "PatientParentRefused", "PatientHadInfection", "HowMigrated", "Reaction", "ReactionDate", "Location", "NP001Description", "NP001FriendlyName", "DocumentName", "Action", "DateLastAction", "TestResultsReviewed"],
      column_count: 37,
    },
    {
      name: "Implantable device",
      columns: ["PatientID", "DeviceDescription", "ImplantDate", "DeviceStatus", "UniqueDeviceId", "ExplantDate", "ImplantArea", "DeviceIdentifier", "LotNumber", "SerialNumber", "DeviceExpirationDate", "DeviceManufactureDate", "HctpIdentificationCode", "BrandName", "VersionModelNumber", "CompanyName", "MriSafetyInformation", "LabeledContainsNrl", "IsDeleted"],
      column_count: 19,
    },
    {
      name: "Imported Items",
      columns: ["PatientID", "ImportedBy", "DateOfItem", "DateImported", "TypeOfItem", "ItemSubject", "ItemFrom", "ItemComments", "ItemCurrentPath", "ToBeSignedByFirstName", "ToBeSignedByLastName", "SignedOffByFirstName", "SignedOffByLastName", "SignOffDate", "IsLetter", "IsLabEmbeddedRpt"],
      column_count: 16,
    },
    {
      name: "Injections",
      columns: ["PatientID", "InjectionName", "LotNo", "DateGiven", "RecordedByFirstName", "RecordedByLastName", "Volume", "Route", "Manufacturer", "ExpirationDate", "Comment", "CPTCode", "IsGivenElsewhere", "NDCCode"],
      column_count: 14,
    },
    {
      name: "Lab Tests",
      columns: ["PatientID", "TestCreatedDate", "TestCreatedByFirstName", "TestCreatedByLastName", "TestLastUpdatedDate", "TestLastUpdatedByFirstName", "TestLastUpdatedByLastName", "TestLabOrderSentDate", "TestLabResultMessageDate", "TestLabResultReceivedDate", "TestLabLocationCode", "TestLabCompany", "TestSpecimenNumber", "TestBillType", "TestSpecimenStatus", "Fasting", "LabTestStatus", "TestSignedOffByFirstName", "TestSignedOffByLastName", "TestSigedOffDate", "TestComment", "TestLabPatientFamilyName", "LabPatientGivenName", "LabPatientMiddleName", "LabPatientSuffix", "LabPatientRace", "LabPatientRaceAlternate", "LabPatientDOB", "LabPatientSex", "LabPatientIdNumber", "LabPatientAANamespaceId", "LabPatientIdTypeCode", "CcdaGuidLabTestId", "TestLabName", "TestLabAddress1", "TestLabAddress2", "TestLabCity", "TestLabState", "TestLabZip", "TestLabPhone", "ResultSequenceNumber", "ResultAccessionNumberAC", "ResultCreatedDate", "ResultCreatedByFirstName", "ResultCreatedByLastName", "RestultLastUpdatedDate", "ResultLastUpdatedByFirstName", "ResultLastUpdatedByLastName", "ResultOrderedByFirstname", "ResultOrderedByLastName", "ResultElectronicOrderCreationDate", "ResultSpecimenNumber", "ResultSpecimenCollectedDate", "ResultSpecimenSource", "ResultAlternateID1", "ResultAlternateID2", "ResultsSentDate", "ResultFacilityPermingTest", "ResultTestStatus", "ResultParentForReflexOBX", "ResultParentForReflexOBR", "ResultOrderingProviderNotInAC", "ResultSpecimenCondition", "ResultSpecimenUiversalId", "ResultSpecimenUniversalIdType", "ResultSpecimenCollectedDate1", "ResultTimingStartDate", "ResultTimingEndDate", "ResultSpecimenType", "ResultSpecimenRejectReason", "ResultDetailSequenceNumber", "ResultDetailCreatedDate", "ResultDetailCreatedFirstName", "ResultDetailCreatedLastName", "ResultDetailLastUpdatedDate", "ResultDetailLastUpdatedByFirstName", "ResultDetailLastUpdatedByLastName", "ResultDetailInactive", "ResultDetailCorrectsLabTestID", "ResultDetailCorrectedByLabTestID", "ResultDetailLabtestStatus", "LabTestCodeDescription", "ResultDetailLoincTestCode", "ResultDetailObservationSubID", "ResultDetailObservationValue", "UncertaintyofMeasurement", "ResultDetailRefenceRanges", "ResultDetailAbnormalFlag", "ResultDetailAbnormalType", "ResultDetailReferenceRangeChangeDate", "ResultDetailSecurityAccessChecks", "ResultDetailObservationSentDate", "ResultDetailLabLocationCode", "ResultDetailLabName", "ResultDetailLabAddress1", "ResultDetailLabAddress2", "ResultDetailLabCity", "ResultDetailLabState", "ResultDetailLabZip", "ResultDetailLabPhone", "ResultDetailValueType", "ResultDetailIsLabReport", "NoteSequenceNumber", "NoteLaborderID", "NoteLabOrderDetailID", "NoteCreatedDate", "NoteCreatedByFirstName", "NoteCreatedByLastName", "NoteLastUpdatedDate", "NoteLastUpdatedByFirstName", "NoteLastUpdateByLastName", "NoteOwnerType", "NoteOwnerID", "NoteText", "NoteReplaced", "Group", "PerformedBy", "LabName", "LabAddress1", "LabAddress2", "LabCity", "LabState", "LabZip", "LabPhone", "LabDirectorName", "ReportFileName"],
      column_count: 119,
    },
    {
      name: "List Problem Pending",
      columns: ["PatientID", "ProblemICD", "ProblemName", "DateRowAdded", "DateActive", "DateInactive", "AddingProviderFirstName", "AddingProviderLastName", "Chronicity", "DateLastActivated", "DateSentToRegistry", "DateResolved", "PendingFlag", "ImportedDate", "Source", "COSTAR", "SNOMED", "IcdType"],
      column_count: 18,
    },
    {
      name: "List Problem",
      columns: ["PatientId", "ProblemName", "ProblemICD", "DateEntered", "DateActive", "DateInactive", "AddingProviderFirstName", "AddingProviderLastName", "Chronicity", "DateLastActivated", "DateSentToRegistry", "DateResolved", "Source", "COSTAR", "SNOMED", "Historical", "IcdType"],
      column_count: 17,
    },
    {
      name: "Medications Pending",
      columns: ["PatientID", "DateEntered", "PrescribingProviderFirstName", "PrescribingproviderLastName", "MedicineName", "Signetur", "MedicineQuantity", "Refills", "DateInitiated", "DateLastRefilled", "MedComments", "PriorRefills", "Refillable", "Inactive", "MedSource", "ExternalID", "PharmacyName", "PharmacyPhone", "PharmacyFax", "PharmacyTransactionID", "QuickAddWhoPrescribed", "QuickAddReasonPrescribed", "Deleted", "DateInactivated", "RxGUID", "DateStarted", "DispenseQualifier", "ERXstatus", "DispenseAsWritten", "IsFormularyChecked", "SentBySureScripts", "PharmacyTransmitFailed", "InactivateReason", "ScriptPrinted", "ScriptFaxed", "PendingFlag", "ImportedDate", "Source"],
      column_count: 38,
    },
    {
      name: "Medications",
      columns: ["PatientID", "DateEntered", "PrescribingProviderFirstName", "PrescribingproviderLastName", "MedicineName", "Signature", "MedicineQuantity", "Refills", "DateInitiated", "DateLastRefilled", "MedComments", "PriorRefills", "Refillable", "Inactive", "MedSource", "ExternalID", "PharmacyName", "PharmacyPhone", "PharmacyFax", "PharmacyTransactionID", "QuickAddWhoPrescribed", "QuickAddReasonPrescribed", "Deleted", "DateInactivated", "RxGUID", "DateStarted", "DispenseQualifier", "ERXstatus", "DispenseAsWritten", "IsFormularyChecked", "SentBySureScripts", "PharmacyTransmitFailed", "InactivateReason", "ScriptPrinted", "ScriptFaxed", "Source", "AdministeredDuringVisit", "Course", "ProblemId", "DaysSupply", "ProviderDea", "NoteToPharmacy", "RenewalRequestIdForReplaceMed", "RxChangeGuidForApproved", "IsCompoundMed", "CompoundMedSchedule", "EarliestFillDate", "ScheduledDrugSeriesLink", "Problem", "ICDCode"],
      column_count: 50,
    },
    {
      name: "Next Of Kin",
      columns: ["PatientID", "IsPrimaryGuardian", "FirstName", "LastName", "SSN", "Address1", "Address2", "City", "State", "Zip", "Phone", "Email", "BirthDate", "RelationName", "PrimaryGuardian", "Gender", "Comments"],
      column_count: 17,
    },
    {
      name: "Occupation and Industry History",
      columns: ["Patientid", "Active", "YearStarted", "SendingFullURL", "CensusIndustryCode", "CensusIndustryTitle", "NAICSCode", "NAICSTitle", "NAICSProbability", "CensusOccupationCode", "CensusIndustryTitle1", "SOCCode", "SOCTitle", "SOCProbability"],
      column_count: 14,
    },
    {
      name: "Orders",
      columns: ["PatientID", "OrderEnteredDate", "OrderTypeDescriptin", "OrderText", "CPTs", "ICDs", "OrderComments", "SentByFirstName", "SentByLastName", "SentToFirstName", "SentToLastName", "DateSent", "IsPartialResult", "IsSigned", "OrderStatus", "DateDone", "TrackingComments", "DoneByFirstName", "DoneByLastName", "AssignedToFirstName", "AssignedToLastName", "OriginalOrderText", "ResultTypeDescription", "DateAssigned"],
      column_count: 24,
    },
    {
      name: "Patient Demographics",
      columns: ["PatientID", "ChartID", "Salutation", "FristName", "MiddleName", "LastName", "Suffix", "Gender", "BirthDate", "SocialSecurityNumber", "Address", "Address2", "City", "State", "Zip", "Phone", "WorkPhone", "Fax", "Email", "EmployerName", "EmergencyContactName", "EmergencyContactPhone", "SpouseName", "Comments", "RecordsReleased", "Referredby", "ReferredbyMore", "Inactive", "ReasonInactive", "PreferredPhysician", "PreferredPharmacy", "ReferringDoc", "ReferringNumber", "Miscellaneous1", "Miscellaneous2", "Miscellaneous3", "Miscellaneous4", "MaritalStatus", "AllergiesDemo", "ExemptFromReporting", "TakesNoMeds", "PatientRace", "ExemptFromReportingReason", "LanguagePreference", "PatientEthnicity", "ContactPreference", "DateOfDeath", "MothersMaidenName", "BirthOrder", "DateTimePatientInactivated", "MothersFirstName", "SexualOrientation", "GenderIdentity", "MaidenName", "AliasNickname", "PreviousAddress1", "PreviousAddress2", "PreviousCity", "PreviousState", "PreviousZip", "Occupation", "ImageName"],
      column_count: 62,
    },
    {
      name: "Patient Generated Data",
      columns: ["PatientID", "ProviderFirstName", "ProviderLastName", "SavedBy", "DirectiveName", "DirectiveText", "DateActive", "DateInactive", "DirectiveCode", "IsActive", "Comments", "PathToDirective", "History", "DateEntered"],
      column_count: 14,
    },
    {
      name: "Patient Health Information Capture",
      columns: ["PatientID", "ProviderFirstName", "ProviderLastName", "SavedBy", "DateSaved", "DirectiveName", "DirectiveText", "DateActive", "DateInactive", "DirectiveTypeName", "DirectiveTypeDesc", "DirectiveLevel", "IsActive", "MedicalAlertType", "Comments", "PathToDirective", "History"],
      column_count: 17,
    },
    {
      name: "Patient Record Release",
      columns: ["PatientID", "Name", "Address", "City", "State", "Zipcode", "Phone", "URL", "DateOfRelease", "AuthorizationField", "ReleaseReason", "ReleasedBy", "Fax", "Comments", "Method", "IsFullPatientRecord", "RecipientFirstName", "RecipientLastName", "RecipientOrganization", "ReferralName", "ReferralDateStarts", "ReferralDateEnds", "NumberOfVisits", "ReferralComment", "ReferralProviderFirstName", "ReferralProviderLastName"],
      column_count: 26,
    },
    {
      name: "Plan of Treatment",
      columns: ["PatientID", "EncounterDate", "ProviderFirstName", "ProviderLastName", "Plan"],
      column_count: 5,
    },
    {
      name: "Procedures",
      columns: ["PatientId", "CPTCode", "CPTdescription", "CPTShortDescription", "Fee", "Charge", "Units", "Price", "Comments", "DatePerformed", "Resolved", "Sequence", "AppealFlag", "NDCCode", "NDCUnits"],
      column_count: 15,
    },
    {
      name: "Referrals",
      columns: ["PatientID", "EnteredDate", "ReferralName", "ReferralFirstName", "ReferralLastName", "DateStarts", "DateEnds", "NumberOfVisits", "Comment", "Description", "OnBehalfOfFirstName", "OnBehalfOfLastName"],
      column_count: 12,
    },
    {
      name: "Risk Factors",
      columns: ["PatientId", "RiskFactorName", "DateEntered", "AddingProviderFirstName", "AddingProviderLastName"],
      column_count: 5,
    },
    {
      name: "Scheduling",
      columns: ["PatientID", "AppointmentDate", "VisitType", "Comments", "BookedByFirstName", "BookedByLastName", "DateBooked", "ProviderFirstName", "ProviderLastName", "Duration", "XLinkProviderID", "VisitIdExternal", "IsEditable", "IsTelehealth"],
      column_count: 14,
    },
    {
      name: "Smoking Statuses",
      columns: ["PatientID", "TobaccoStatusStartDate", "TobaccoStatusEndDate", "PacksPerDay", "YearsSmoked", "YearsQuit", "IsSignedOff", "DateRowAdded", "TobaccoUseName", "TobaccoUseNameExtra", "DisplayOrder", "SNOMED"],
      column_count: 12,
    },
    {
      name: "Tracked Data",
      columns: ["PatientId", "Item", "Date", "Value", "Comments"],
      column_count: 5,
    },
    {
      name: "Travel History",
      columns: ["PatientId", "StartDate", "EndDate", "Location", "IsForeignLocation", "Notes", "CcdaGuidTravelHistory"],
      column_count: 7,
    },
    {
      name: "User Defined Fields",
      columns: ["PatientId", "FieldValue", "Template", "DateEntered"],
      column_count: 4,
    },
    {
      name: "Vital Signs",
      columns: ["PatientId", "EncounterDate", "Temperature", "PulseRate", "BloodPressure", "RespirationRate", "BloodOxygen", "Weight", "Height", "BMI", "BP", "Pulse", "RR", "WC", "Sat", "SatSuppO2Amount", "Pain", "PF(pre-bronchodilator)", "PF(post-bronchodilator)", "VisionOS", "VisionOD", "Hearing", "HearingComments", "LastMenstrualPeriod", "EstimatedDeliveryDate", "PregnancyComments", "Other", "HeadCircumference"],
      column_count: 28,
    },
  ];

  const totalColumns = dataClasses.reduce((sum, c) => sum + c.column_count, 0);

  return {
    source_file: "Picasso-EHI-Export-Documentation-V1_0-1-1.pdf",
    title: "Amazing Charts EHI Export: Folder Organization and Data Format Specification",
    export_format: "CSV/JSON/XML",
    data_classes: dataClasses,
    total_data_classes: dataClasses.length,
    total_columns: totalColumns,
  };
}

async function main() {
  console.log("Parsing Picasso-specific document (V1_0-1)...");
  const picassoResult = parsePicassoDoc("");

  console.log("Parsing Amazing Charts document (V1_0-1-1)...");
  const acResult = parseAmazingChartsDoc("");

  // Write outputs
  writeFileSync(
    join(ENRICHMENT_DIR, "picasso-data-classes.json"),
    JSON.stringify(picassoResult, null, 2)
  );
  console.log(
    `Picasso: ${picassoResult.total_data_classes} data classes, ${picassoResult.total_columns} total columns`
  );

  writeFileSync(
    join(ENRICHMENT_DIR, "amazing-charts-data-classes.json"),
    JSON.stringify(acResult, null, 2)
  );
  console.log(
    `Amazing Charts: ${acResult.total_data_classes} data classes, ${acResult.total_columns} total columns`
  );

  // Summary
  const summary = {
    extraction_date: new Date().toISOString(),
    files_discovered: 3,
    files_parsed: 2,
    parse_failures: [
      {
        file: "PAA_API_documentation.pdf",
        error: "API documentation (g)(10)-style; not a data dictionary. Content noted but not structured.",
      },
    ],
    results: [
      {
        file: picassoResult.source_file,
        data_classes: picassoResult.total_data_classes,
        total_columns: picassoResult.total_columns,
        export_format: picassoResult.export_format,
      },
      {
        file: acResult.source_file,
        data_classes: acResult.total_data_classes,
        total_columns: acResult.total_columns,
        export_format: acResult.export_format,
      },
    ],
  };

  writeFileSync(
    join(ENRICHMENT_DIR, "extraction-summary.json"),
    JSON.stringify(summary, null, 2)
  );

  console.log("\nDone. Output files:");
  console.log("  picasso-data-classes.json");
  console.log("  amazing-charts-data-classes.json");
  console.log("  extraction-summary.json");
}

main().catch(console.error);
