function decorateUpids () {
	$$('.peopleDBmatch').each (function (row) {
		var upid = row.readAttribute ('id');
		// log (upid);
		row.writeAttribute('title', 'click to see this person\'s record in peopleDB');
		row.observe ('mouseover', function (event) {
			row.addClassName('over');
		});
		row.observe ('mouseout', function (event) {
			row.removeClassName('over');
		});
		row.observe ('click', function (event) {
			popup (upid, 'peopleDB');
		});
	});
}

function popup (upid, win) {
	https://people.ucar.edu/#peopleSearch?
	params = {
		upid : upid,
		searchScope : 'all',
		includeActive : 'true',
		includeInactive : 'true',
		searchType : 'advancedSearch'
	}

	
	url = 'https://people.ucar.edu/#peopleSearch?' + $H(params).toQueryString();
	var features = "innerHeight=800,height=800,innerWidth=750,width=750,resizable=yes,scrollbars=yes";
	features += ",locationbar=yes,menubar=yes,location=yes,toolbar=yes";
	win = win || "_blank";
	var targetwin = window.open (url, win, features);
	targetwin.focus();
}

Event.observe (window, 'load', decorateUpids);
