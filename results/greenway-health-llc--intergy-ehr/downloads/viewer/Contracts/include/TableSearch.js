

function Table(_name, _description)
{
	this.name = _name;
	this.description = this.name + " -\n" + _description;
}

var Tables = new Array();

/*function BodyLoad()
{
<!-- #include file="DBDescriptions.inc" -->
}*/

function getDescription(pageURL)
{
	var entityName = pageURL.substring(0, pageURL.length - 4);
	
	for(var i=0; i<Tables.length; i++)
	{
		if(Tables[i].name == entityName)
		{
			return Tables[i].description;		
		}
	}
}

function loadSubject () {
        if ((document.DBaseTOC.DBaseList.selectedIndex > -1) &&
            (document.DBaseTOC.DBaseList.selectedIndex <= document.DBaseTOC.DBaseList.options.length)) {

		var navigatePage = document.DBaseTOC.DBaseList.options [document.DBaseTOC.DBaseList.selectedIndex].value;

		//document.DBaseTOC.desc.innerHTML = getDescription(navigatePage);
		parent.subj.location.href = navigatePage;           
         }
    }

// Select a value in a SELECT input, based on the value of a
// TEXT field.  Allows a user to jump to a value in a long
// drop-down list based on text typed into a text input.

function selectValue(field,dropdown)
	{

	//If the user enters a space then return

	if (field.value.keycode == 32 || field.value.keycode == 12)
	  {
		alert ("No spaces allowed");
		return;
	  }
	else
	 {

		// first, check for value.  If none, set focus to index 0 and return

		if ( field.value == "" )
		  {
			dropdown.options[0].selected = true;
			loadSubject();
			return;
		  }
		// otherwise, we have a value and can move on.

		var textValue = field.value.toUpperCase();

		// loop through items: whichever has the closest, but not greater than, value to the typed text wins.

		// alternate method: split list in half each time.

		var length = dropdown.options.length;	// find out how many options we have

		//var index = dropdown.selectedIndex;	// start wherever the drop-down is selected from

		var index = 0;

		if ( index == 0 ) index = 1;		// always skip the first item

		// IF the user types A then increment by to to compensate for the selectvalue

		// Always start at the first item

		var bottomIndex = 1;			// lowest value to check
		var topIndex = length;			// highest value to check
		var textLength = textValue.length;	// how many characters to compare

		while ( 1 == 1 )
		   {

			// get the value of the current drop-down

			var selectValue = dropdown.options[index].text.substring( 0, textLength ).toUpperCase();
			var fullSelectValue = dropdown.options[index].text.toUpperCase();

			if ( selectValue < textValue )						// if it's lower than what we're looking for....
			{
				bottomIndex = index;										// ...bring the bottom of the search up to the current.
			}
			else if ( selectValue > textValue )				// if it's higher than what we're looking for...
			{
				topIndex = index;												// ...bring the top of the search down to th current
			}

			// look for exact matches

			if ( selectValue == textValue )						// if it's a match...
				{

					// ...scoot to the first (lowest) matching item.
					while (dropdown.options[index-1].text.substring( 0, textLength ).toUpperCase() == textValue )
						{

						if ( index > 1 )
							index = index - 1;
					    else
					    	return;
		                }

					// mark The table and then show it in the browser
					dropdown.options[index].selected = true;
					loadSubject();
					return;																	// ...and quit.
				}

			// Other ways to know when to stop
			if ( bottomIndex + 1 >= topIndex )				// if our bounds have met...
				{																					// then we're almost as close as we're going to get this time.
				 // We need to move to the top or bottom of the "close"
				 // list.  e.g. if the typed value if greater than the select value,
				 // and other items in the list match as well, move to the last item
				 // that matches.

					var direction = 1;							// default to move to lower items

					var closeIndex = bottomIndex;			 // default to move the bottom index

					if ( fullSelectValue > textValue )		// however, if the typed value doesn't match up to the select value...
						{
							direction = -1;												// ...then move to lower items
							closeIndex = topIndex;								// ...and use the top index.
						}
					var matchValue = 												// the value we're trying to match
						dropdown.options[closeIndex].text.substring( 0, textLength ).toUpperCase();
					while ( dropdown.options[closeIndex].text.substring( 0, textLength ).toUpperCase()
						 == dropdown.options[closeIndex + direction].text.substring( 0, textLength ).toUpperCase() )
						{	// while they are equivalent, keep moving
							closeIndex = closeIndex + direction;
						}
					// if we've been scooting up, then drop one so that we always end as close to, but below, the typed value

					if ( direction == -1 )
						closeIndex = closeIndex - 1;

					// we're now really as close as we're going to get.  Select it and show in the browse

					dropdown.options[closeIndex].selected = true;
					loadSubject();
					return;																	// ...and quit.
				}

			// if we make it here, we're OK to continue.  Split the difference between our bounds and try again.
			index = Math.round( bottomIndex + ((topIndex-bottomIndex)/2) );
		}
	}
}