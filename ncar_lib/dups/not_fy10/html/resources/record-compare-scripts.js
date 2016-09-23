function pageInit () {
	
	$$('.edit-button').each (function (button) {
		button.observe ('click', function () {
			var recId = button.identify();
			editRecord (recId);
		});
	});
	
	$$('.find-button').each (function (button) {
		button.observe ('click', function () {
			var recId = button.identify();
			findRecord (recId);
		});
	});
	
}

var popup_featureMap = {
		innerHeight : 700, height : 700,
		innerWidth : 800, width : 800,
		resizable : 'yes', scrollbars : 'yes',
		locationbar : 'yes', menubar : 'yes', location : 'yes', toolbar : 'yes'
	};

function editRecord (recId) {

	var features = $A()
	$H(popup_featureMap).each ( function (pair) {
		features.push (pair.key + "=" + pair.value);
	});
	
	var params = {
		command : 'edit',
		recId : recId
	}
	var baseUrl = 'http://nldr.library.ucar.edu/schemedit/editor/edit.do'
	var url = baseUrl + '?' + $H(params).toQueryString();
	
	var dcswin = window.open (url, "dcs", features.join (','));
	dcswin.focus();
	return false;
}

function findRecord (recId) {

	var features = $A()
	$H(popup_featureMap).each ( function (pair) {
		features.push (pair.key + "=" + pair.value);
	});
	
// s=0&searchMode=id&q=para-000-000-000-001&vld=&resultsPerPage=10
	
	var params = {
		s : '0',
		searchMode : 'id',
		// command : 'edit',
		q :  recId
	}
	var baseUrl = 'http://nldr.library.ucar.edu/schemedit/browse/query.do'
	var url = baseUrl + '?' + $H(params).toQueryString();
	
	var dcswin = window.open (url, "dcs", features.join (','));
	dcswin.focus();
	return false;
}

document.observe ('dom:loaded', pageInit)
