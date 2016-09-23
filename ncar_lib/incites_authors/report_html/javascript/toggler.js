function log (s) {
	if (window.console)
		window.console.log(s);
}

function doToggler(id,closeOthersOfClass) {
	var labelElm = $('toggler-lnk-'+id);
	var toggleElm = $('toggler-con-'+id);
	if(toggleElm) {
		var labelElm = $('toggler-lnk-'+id);
		if(!toggleElm.visible() && closeOthersOfClass) {
			$$('.'+closeOthersOfClass).each(function(otherElm) {
				if(otherElm.hasClassName('togglerOpen') && otherElm.id != 'toggler-lnk-'+id) {
					var otherId = otherElm.id.sub('toggler-lnk-','');
					toggleAction('toggler-con-'+otherId,otherElm,'close');
				}
			});
		}
		toggleAction(toggleElm,labelElm);		
	}	
}

function doTogglerOpen(id) {
	toggleAction($('toggler-con-'+id),$('toggler-lnk-'+id),'open');	
	return false;
}
function doTogglerClose(id) {
	toggleAction($('toggler-con-'+id),$('toggler-lnk-'+id),'close');
	return false;
}

// Internal helper function for toggle, open, close
function toggleAction(toggleElmId,labelElmId,action) {
	// log ("toggleAction: " + toggleElmId.identify() + ", " + labelElmId.identify() + ", " + action);
	var labelElm = $(labelElmId);
	if(!action || action == 'toggle') {
		if($(toggleElmId).visible()) {
			Effect.BlindUp(toggleElmId, { duration: 0.2 });
			labelElm.removeClassName('togglerOpen');
		}
		else {
			Effect.BlindDown(toggleElmId, { duration: 0.2 });
			labelElm.addClassName('togglerOpen');
		}	
	}
	else if (action == 'close' && labelElm.hasClassName('togglerOpen')) {
		Effect.BlindUp(toggleElmId, { duration: 0.2 });
		labelElm.removeClassName('togglerOpen');
	}
	else if (action == 'open' && labelElm && !labelElm.hasClassName('togglerOpen')) {
		Effect.BlindDown(toggleElmId, { duration: 0.2 });
		labelElm.addClassName('togglerOpen');
	}		
}

/* initialize all elements of class "toggler" */
function initializeTogglers () {
	log ('initializeTogglers');
	$$('.toggler').each (function (toggler) {
		var id = toggler.identify();
		// log ("toggler: " + id);
		var lnk = $('toggler-lnk-'+id);
		var con = $('toggler-con-'+id);
		if (lnk.hasClassName('togglerClosed'))
			doTogglerClose (id);
		else
			doTogglerOpen(id);
			
		lnk.observe ('click', function (event) {
			// log ("click on " + event.element().identify());
			doToggler(id);
			return false;
		});
		lnk.observe ('mouseover', function (event) {
			lnk.addClassName('togglerOver');
		});
		lnk.observe ('mouseout', function (event) {
			lnk.removeClassName('togglerOver');
		});
	});
}	

Event.observe (window, 'load', initializeTogglers);

