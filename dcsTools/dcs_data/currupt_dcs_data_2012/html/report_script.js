function log (s) {
	if (window.console)
		console.log (s);
}

function pageInit () {
	$$('.format').each (function (formatEl) {
		formatEl.observe('click', log (formatEl.identify() + " clicked"));
	});

	$('about-toggler-lnk').observe ('click', function () {
		var content = $('about-toggler-con');
		var toggler = $('about-toggler');
		if (!content) log ("content not found");

		if (!content.visible()) {
			toggler.removeClassName ('togglerClosed');
			toggler.addClassName ('togglerOpen');
			content.show();
		}
		else {
			toggler.removeClassName ('togglerOpen');
			toggler.addClassName ('togglerClosed');
			content.hide();	
		}
	});
}

Event.observe (window, 'load', pageInit)


