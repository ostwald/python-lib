function pageInit () {
	
	var filename = $A(window.location.href.split('/')).last();
	var dirName = filename.split('.')[0]+'_data';
	
	var groupNum = $H(window.location.href.toQueryParams()).get('groupNum')
	if (groupNum) {
		var group = $(groupNum).up('table');
		group.scrollTo();
		group.addClassName ("highlighted-group");
		new PeriodicalExecuter ( function (pe) {
			group.removeClassName ("highlighted-group");
			pe.stop();
		}, 1);
	}
	
	$$('.compare-button').each (function (icon) {
		icon.observe ('mouseover', function () {icon.addClassName ("button-over")});
		icon.observe ('mouseout', function () {icon.removeClassName ("button-over")});
		icon.observe ('click', function () {
			window.location = dirName + "/" + icon.identify()+'.html';
		});
	});
}

document.observe ('dom:loaded', pageInit)
