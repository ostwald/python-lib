
var standards = null;

function pageInit () {
	
	// Activate Widgets
	standards = document.getElementsByClassName ("node");
	
	standards.each (function (node) {
		var widget = $Std(node).getWidget();
		Event.observe (widget, 'click', wigitClick, false);
		Event.observe (widget, 'mouseover', function (evnt) {
			widget.setStyle({cursor:"pointer"})
			}, false);
		Event.observe (widget, 'mouseout', function (evnt) {
			widget.setStyle({cursor:"default"})
			}, false);
	});
	
	Event.observe ($('search-button'), 'click', doSearch, false);
	
	$('tool-bar-form').onsubmit = doSearch;
	
	exposeToLevel(0);
	
	// handle id param by executing a find
	params = this.location.search.toQueryParams();
	// alert ("id: " + params["id"])
	if (params["id"]) {
		id = params["id"];
		$("search-str").value = id;
		doFind (id);
	}
}

function doFind (id) {
	var hit = standards.find ( 
		function (std) {
			return (std.id == id);
		});
	if (hit) {
		hit = $Std(hit).highlight();
	}
	else {
		alert (id + " not found");
	}
}
function doSearch (evnt) {
	var s = $F("search-str");
	Event.stop(evnt);
	if (!s) {
		alert ("no string")
	}
	else {
		doFind (s);
	}
}

/* if called without an element, removed current hightlight */
function highlight (element) {
	$('root').getElementsBySelector('[class~="highlight"]').each (
		function (e) { e.removeClassName ('highlight')});
	if ( element ) {
		$(element).addClassName("highlight");
		Event.observe (document,"click", 
			function (e) { 
				$(element).removeClassName("highlight");
			}, false);
	}
}

/* we are called from a node-control, and return the first "node"
above us in the ancestor list.
*/
function wigitClick (evnt) {

	highlight()
	Event.stop(evnt);
	var std = $Std(findStandard (Event.element(evnt)));
	if (std.isLeaf()) {
		var parent = findStandard (std)
		parent.highlight ();
	}
	else {
		if (evnt.shiftKey) {
			// hide or show siblings
			if (std.getChildrenBox().visible()) {
				std.hideChildren();
				std.siblings().each ( function (sib) {	
					sib.hideChildren();
				});
			}
			else {
				std.showChildren();
				std.siblings().each ( function (sib) {	
					sib.showChildren();
				});				
			
			}
			std.highlight();
		}
		else {
			std.toggleVisibility();
		}
	}
}

function findStandard (element) {
	var std = $(element).ancestors().find ( 
		function (e) { return e.hasClassName ("node") });
	return $Std(std);
}

function exposeToLevel (level) {
	$R(0,6).each (function (i) {
		var klass = "level-" + i;
		document.getElementsByClassName (klass).each ( function (box) {
			var std = findStandard(box);
			if (i < level) {
				std.showChildren();
			}
			else {
				std.hideChildren();
			}
		});
	});
}

var Std = Class.create();
Object.extend (Std, Element)

Std.addMethods({
  	getHead: function (std) {
		var std = $Std(std);
		return $A(std.childNodes).find ( function (child) {
			return (child.nodeType == 1) && (child.hasClassName("node-head"));
			});
	},
	getText: function (std) {
		var head = $Std(std).getHead();
		if (head)
			return head.getElementsByClassName ("node-text")[0];
	},
		
	getControl: function (std) {
		var head = $Std(std).getHead();
		if (head)
			return head.getElementsByClassName ("node-control")[0];
	},
	
	getWidget: function (std) {
		var head = $Std(std).getHead();
		if (head)
			return head.getElementsByClassName ("widget")[0];
	},
	
 	getChildrenBox: function (std) {
		return $A($Std(std).childNodes).find ( function (child) {
			return (child.nodeType == 1) && (child.hasClassName("box"));
		});
	},
	
	toggleVisibility: function (std) {
		std = $Std(std);
		var box = std.getChildrenBox();
		var widget = std.getWidget();
		if ( box ) {
			widget.src = box.visible() ? "images/closed.gif" : "images/opened.gif";
			box.toggle();
		}
		else {
			alert ("boxObj was null for " + std.id);
		}
	},
	
	showChildren: function (std) {
		std = $Std(std);
		var box = std.getChildrenBox();
		var widget = std.getWidget();
		if ( box ) {
			widget.src = "images/opened.gif";
			box.show();
		}
		else {
			alert ("boxObj was null for " + std.id);
		}
	},
	
	hideChildren: function (std) {
		std = $Std(std);
		var box = std.getChildrenBox();
		var widget = std.getWidget();
		if ( box ) {
			widget.src = "images/closed.gif";
			box.hide();
		}
		else {
			alert ("boxObj was null for " + std.id);
		}
	},
	
	isLeaf: function (std) {
		return $Std(std).getChildrenBox() ? false : true;
	},
	
	expose: function (std) {
		$Std(std).ancestors().each ( function (a) {
			if (a.hasClassName ("node")) {
				$Std(a).showChildren() 
			}
		});
	},
	
	highlight: function (std) {
		std = $Std(std);
		std.expose();
		highlight (std.getHead());
		std.scrollTo();
	}
		
});

function $Std(element) {
  if (arguments.length > 1) {
    for (var i = 0, elements = [], length = arguments.length; i < length; i++)
      elements.push($Std(arguments[i]));
    return elements;
  }
  if (typeof element == 'string')
    element = $(element);
  return Std.extend(element);
}


/* NOT USED */
function getControls () {
	var controls = standards.collect ( 
		function (node) {
			// get the head
			var head = $A(node.childNodes).find ( function (child) {
				return (child.nodeType == 1) && (child.hasClassName("node-head"));
			});
			return head.getElementsByClassName ("node-control")[0];
		});
	alert (controls.length + " controls found");
	return controls;
}

function debug (s, clear) {
	var dbStr = "<div>"+s+"</div>";
	if (clear)
		$('debug').innerHTML = dbStr
	else
		new Insertion.Bottom ($('debug'), dbStr);
}
			
Event.observe (window, 'load', pageInit, false);
