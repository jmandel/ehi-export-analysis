-------------------- CROSSWALK TAB 1: EVENTS --------------------
-- Returns ALL people-based events in the system, regardless of whether they have been used or not.
SELECT
    edv.category_name,
    edv.category_code,
    edv.event_name,
    edv.event_definition_id,
    edv.event_category_id,
    edv.table_name,
    edv.form_name,
    edv.form_code
FROM 
    event_definition_view edv
LEFT JOIN 
    event_log el
ON 
    edv.event_definition_id = el.event_definition_id
ORDER BY
    edv.category_name,
    edv.event_name;


-------------------- CROSSWALK TAB 2: EVENTS + COLUMNS --------------------
-- Returns ALL people-based events in the system, including their respective data columns

select distinct event_definition_id 
into #eventsInUse
from event_log

select
    ec.category_name,							-- category (ie:allergies)
    ec.category_code,							-- category code
    ed.event_name,								-- name of event.  may be in json depending on form config
    ed.event_definition_id,						-- identifier that would be in the json
    table_name,									-- not in json but useful
    fh.form_name,								-- name of form in UI
    fh.form_code,								-- form identifier in json
	fl.column_name as jsonPropertyName,			-- name of json property
	fl.caption as formFieldCaption,				-- name of form field
	fl.type_code as typeCode,					-- field type code
	-- Will only be populated on subforms:
	sfh.form_name as subformName,				-- name of subform 
	sfh.form_code as subFormCode,				-- subform code 
	sfl.column_name as subFormJsonPropertyName, -- name of json property for subform field 
	sfl.caption as subFormFieldCaption,			-- name of form field for subform field 
	sfl.type_code as typeCode,					-- subform field type code 
	-- Will only be populated on assessments:
	tsh.test_header_name as assessmentName,							-- Test name
	tsh.test_header_code as assessmentCode,							-- Test code
	tsd.test_setup_details_id as assessmentQuestionID,				-- ID for test question
	tsd.test_setup_details_caption as assessmentQuestionCaption		-- Caption in UI for test question

from 
	#eventsInUse e
    inner join event_definition ed
		on e.event_definition_id = ed.event_definition_id
	inner join event_category ec
		on ec.event_category_id = ed.event_category_id
	inner join dd_table_header t
		on t.dd_table_header_id = ec.data_table
	inner join form_header fh
		on fh.form_header_id = ed.form_header_id
	inner join form_lines fl
		on fl.form_header_id = fh.form_header_id
			and fl.belongs_to is not null -- Exclude section headers
	left outer join form_header sfh
		on sfh.form_header_id = fl.sub_form_header_id
	left outer join form_lines sfl
		on sfh.form_header_id = sfl.form_header_id
			and sfl.belongs_to is not null -- Exclude section headers
	left outer join test_setup_header tsh
		on tsh.test_setup_header_id = fl.sub_test_header_id
	left outer join test_setup_details tsd
		on tsd.test_setup_header_id = tsh.test_setup_header_id
WHERE
	fl.type_code not in 
	(
		'DIVLINE',
		'FORMLAUNCH',
		'LABEL',
		'RSF'
	)
Order By
    category_name,
    event_name

drop table #eventsInUse


-------------------- CROSSWALK TAB 3: NON-EVENTS --------------------
-- Returns all people-based non-events (forms) in the system

SELECT form_name, form_code, form_family_name, form_family_id, form_family_code
FROM form_header_view fhv 
WHERE fhv.table_name = 'people'

order by
form_name,
form_code, 
form_family_id

-------------------- CROSSWALK TAB 4: NON-EVENTS + COLUMNS --------------------
-- Returns ALL people-based non-events in the system, including their respective data columns

create table #nonEventForms (form_header_id uniqueidentifier)

insert into #nonEventForms (form_header_id)
SELECT fhv.form_header_id
FROM form_header_view fhv 
WHERE fhv.table_name = 'people' 
	AND fhv.list_program = 'eventform.asp' 
	AND fhv.is_print_bundle = 0 
	AND fhv.is_active = 1 
UNION
SELECT fhv.form_header_id
FROM form_header_view fhv 
WHERE fhv.is_print_bundle = 1  
	AND fhv.is_active = 1 

-- Output form info
select
    'n/a' as category_name,							-- category (ie:allergies)
    'n/a' as category_code,							-- category code
    'n/a' as event_name,								-- name of event.  may be in json depending on form config
    'n/a' as event_definition_id,						-- identifier that would be in the json
    table_name,									-- not in json but useful
    fh.form_name,								-- name of form in UI
    fh.form_code,								-- name of form code
	fh.form_family_id,							-- not in json but useful
	fl.column_name as jsonPropertyName,			-- name of json property
	fl.caption as formFieldCaption,				-- name of form field
	fl.type_code as typeCode,					-- field type code
	-- Only be populated on subforms:
	sfh.form_name as subformName,				-- name of subform 
	sfh.form_code as subFormCode,				-- subform code 
	sfl.column_name as subFormJsonPropertyName, -- name of json property for subform field 
	sfl.caption as subFormFieldCaption,			-- name of form field for subform field 
	sfl.type_code as typeCode,					-- subform field type code 
	-- Will only be populated on assessments:
	tsh.test_header_name as assessmentName,							-- Test name
	tsh.test_header_code as assessmentCode,							-- Test code
	tsd.test_setup_details_id as assessmentQuestionID,				-- ID for test question
	tsd.test_setup_details_caption as assessmentQuestionCaption		-- Caption in UI for test question

from 
	#nonEventForms e
	inner join form_header fh
		on fh.form_header_id = e.form_header_id
	inner join form_family ff 
		on ff.form_family_id = fh.form_family_id
	inner join dd_table_header t
		on t.dd_table_header_id = ff.data_table
	inner join form_lines fl
		on fl.form_header_id = fh.form_header_id
			and fl.belongs_to is not null -- Exclude section headers
	left outer join form_header sfh
		on sfh.form_header_id = fl.sub_form_header_id
	left outer join form_lines sfl
		on sfh.form_header_id = sfl.form_header_id
			and sfl.belongs_to is not null -- Exclude section headers
	left outer join test_setup_header tsh
		on tsh.test_setup_header_id = fl.sub_test_header_id
	left outer join test_setup_details tsd
		on tsd.test_setup_header_id = tsh.test_setup_header_id
WHERE
	fl.type_code not in 
	(
		'DIVLINE',
		'FORMLAUNCH',
		'LABEL',
		'RSF'
	)
Order By
    form_name,
	form_code

drop table #nonEventForms  