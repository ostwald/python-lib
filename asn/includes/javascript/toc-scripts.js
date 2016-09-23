function pageInit () {
	$$('.toc-link > A').each (function (link) {
		link = $(link);
		link.observe ('click', highlightLink.bind (link));
	});
}

function highlightLink (event) {
	
	var currentLink = this;
	
	$$('.toc-link > A').each (function (link) {
		link = $(link);
		if (link == currentLink)
			link.addClassName ('current-link')
		else
			link.removeClassName ('current-link')
	});
}


Event.observe (window, 'load', pageInit);
