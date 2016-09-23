
var standards = null;
var author = "Unknown";
var topic = "Unknown";
var created = "Unknown";

function pageInit () {
	// Activate Widgets
	standards = $$(".node");
	
	// console.log ('%d nodes', standards.size())
	
	
	standards.each (function (node) {
		var widget = $StdNode(node).getWidget();
		if (!widget)
			throw ("wigit not found by pageInit");
		widget.observe ('click', wigitClick);
		widget.observe ('mouseover', function (evnt) {
			widget.setStyle({cursor:"pointer"})
			});
		widget.observe ('mouseout', function (evnt) {
			widget.setStyle({cursor:"default"})
			});
			
		stdLink = $StdNode(node).getAsnIdLink();
		if (stdLink)
			stdLink.observe ('click', handleAsnIdClick);
	});
	
	$('search-button').observe ('click', doSearch);
	
	$('tool-bar-form').onsubmit = doSearch;
	
	// exposeToLevel(0);
	
	// handle id param by executing a find
	params = this.location.search.toQueryParams();
	// alert ("id: " + params["id"])
	if (params["id"]) {
		id = params["id"];
		$("search-str").value = id;
		doFind (id);
	}
	
	var filename = $A(window.location.href.split('/')).last();
	author = filename.split('.')[0];
	topic = filename.split('.')[1];
	created = filename.split('.')[2];
}

function doFind (id) {
	var hit = standards.find ( 
		function (std) {
			return (std.id == id);
		});
	if (hit) {
		hit = $StdNode(hit).highlight();
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
		doFind (s.strip());
	}
}

/* if called without an element, removed current hightlight */
function highlight (element) {
	$('root').select('.highlight').each (
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
	var stdNode = $StdNode(findStandard (Event.element(evnt)));
	
	if (stdNode.isLeaf()) {
		var parent = findStandard (stdNode)
		parent.highlight ();
	}
	else {
		if (evnt.shiftKey) {
			// hide or show siblings
			if (stdNode.getChildrenBox().visible()) {
				stdNode.hideChildren();
				stdNode.siblings().each ( function (sib) {	
					sib.hideChildren();
				});
			}
			else {
				stdNode.showChildren();
				stdNode.siblings().each ( function (sib) {	
					sib.showChildren();
				});				
			
			}
			stdNode.highlight();
		}
		else {
			stdNode.toggleVisibility();
		}
	}
}

function findStandard (element) {
	var stdNode = $(element).ancestors().find ( 
		function (e) { return e.hasClassName ("node") });
	return $StdNode(stdNode);
}

function exposeToLevel (level) {
	$(document.body).setStyle ({cursor:'progress'});
	$R(0,6).each (function (i) {
		var klass = "level-" + i;
		$$ ('.'+klass).each ( function (box) {
			var stdNode = findStandard(box);
			if (i < level) {
				stdNode.showChildren();
			}
			else {
				stdNode.hideChildren();
			}
		});
	});
	$(document.body).setStyle ({cursor:'default'});
}

/* StdNode extends prototype Element to provide specialized support for standards 

Typical Standard HTML:
   <DIV class="node-head">
      <DIV class="node-control">
         <IMG src="images/opened.gif" class="widget" 
              title="click to hide/show children; shift-click to hide/show siblings">
      </DIV>
      <DIV class="node-text">
         Strand 1:  Writing, Speaking, and Visual Expression
         <SPAN class="std-id">
            [ <A href="http://purl.org/ASN/resources/S103F088">S103F088</A> ]
         </SPAN>
         <SPAN class="std-id">[9&mdash;12]</SPAN>
      </DIV>
   </DIV>
</DIV>
*/
var StdNode = Class.create();
Object.extend (StdNode, Element)

StdNode.addMethods({
  	getHead: function (stdNode) {
		var stdNode = $StdNode(stdNode);
		return $A(stdNode.childNodes).find ( function (child) {
			child = $(child);
			return (child.nodeType == 1) && (child.hasClassName("node-head"));
			});
	},
	getTextElement: function (stdNode) {
		var head = $StdNode(stdNode).getHead();
		if (head)
			return head.select (".node-text")[0];
	},
	
	getAlignText: function (stdNode) {
		stdNode = $StdNode(stdNode)
		var textParts = $A()
		
		textParts.push (stdNode.getText());
		var parent = findStandard(stdNode)
		while (parent) {
			textParts.push (parent.getText());
			parent = findStandard (parent);
		}
		//doc title
		textParts.push ($('root').select('.doc-title')[0].innerHTML);
		
		var text = textParts.reverse().join ('; ');
		
		// add asnId
		text += " ASNID[" + stdNode.getAsnId() + "]";
		return text;
	},
	
	getGradeRange: function (stdNode) {
		try {
			var textElement = stdNode.getTextElement();
			return textElement.select ('.std-id')[1].innerHTML;
		} catch (error) {
			return "unknown";
		}
	},
	
	getText: function (stdNode) {
		// remove the two "span" elements
		text = $StdNode(stdNode).getTextElement().innerHTML
		text = text.gsub(/<span.*?<\/span>/, '').strip();
		text = text.gsub(/<SPAN.*?<\/SPAN>/, '').strip();   // for IE
		return text;
	},
		
	getControl: function (stdNode) {
		var head = $StdNode(stdNode).getHead();
		if (head)
			return head.select (".node-control")[0];
	},
	
	getWidget: function (stdNode) {
		var head = $StdNode(stdNode).getHead();
		if (head) {
			// return head.getElementsByClassName ("widget")[0];
			return head.select (".widget")[0]
		}
	},
	
	getAsnId: function (stdNode) {
		var link = $StdNode(stdNode).getAsnIdLink();
		if (link) {
			return link.innerHTML.strip();
		}
	},
	
	getAsnIdLink: function (stdNode) {
		var stdId = $StdNode(stdNode).getHead();
		if (stdId)
			return stdId.select('A')[0]
	},
	
 	getChildrenBox: function (stdNode) {
		return $A($StdNode(stdNode).childNodes).find ( function (child) {
			child = $(child);
			return (child.nodeType == 1) && (child.hasClassName("box"));
		});
	},
	
	toggleVisibility: function (stdNode) {
		stdNode = $StdNode(stdNode);
		var box = stdNode.getChildrenBox();
		var widget = stdNode.getWidget();
		if ( box ) {
			widget.src = box.visible() ? "images/closed.gif" : "images/opened.gif";
			box.toggle();
		}
		else {
			alert ("boxObj was null for " + stdNode.id);
		}
	},
	
	showChildren: function (stdNode) {
		stdNode = $StdNode(stdNode);
		var box = stdNode.getChildrenBox();
		var widget = stdNode.getWidget();
		if ( box ) {
			widget.src = "images/opened.gif";
			box.show();
		}
		else {
			alert ("boxObj was null for " + stdNode.id);
		}
	},
	
	hideChildren: function (stdNode) {
		stdNode = $StdNode(stdNode);
		var box = stdNode.getChildrenBox();
		var widget = stdNode.getWidget();
		if ( box ) {
			widget.src = "images/closed.gif";
			box.hide();
		}
		else {
			alert ("boxObj was null for " + stdNode.id);
		}
	},
	
	isLeaf: function (stdNode) {
		return $StdNode(stdNode).getChildrenBox() ? false : true;
	},
	
	expose: function (stdNode) {
		$StdNode(stdNode).ancestors().each ( function (a) {
			if (a.hasClassName ("node")) {
				$StdNode(a).showChildren() 
			}
		});
	},
	
	highlight: function (stdNode) {
		stdNode = $StdNode(stdNode);
		stdNode.expose();
		highlight (stdNode.getHead());
		stdNode.scrollTo();
	}
		
});

function $StdNode(element) {
  if (arguments.length > 1) {
    for (var i = 0, elements = [], length = arguments.length; i < length; i++)
      elements.push($StdNode(arguments[i]));
    return elements;
  }
  if (typeof element == 'string')
    element = $(element);
  return StdNode.extend(element);
}


/* NOT USED */
function getControls () {
	var controls = standards.collect ( 
		function (node) {
			// get the head
			var head = $A(node.childNodes).find ( function (child) {
				return (child.nodeType == 1) && (child.hasClassName("node-head"));
			});
			return head.select (".node-control")[0];
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
	
// EXPERIMENTAL

function handleAsnIdClick (event) {
	// console.log ("handleAsnClick");
	var std = findStandard (event.element());

	//console.log (std.getGradeRange());
	
	
	popUpAlignWin (std.getAlignText(), std.getGradeRange());
	
 	event.stop();
}

function fireFoxAlignText (alignText, gr) {
	var popup = $('align-popup');
	popup.update (std.getAlignText());
	var scrollOffsets = document.viewport.getScrollOffsets();
	var vpHeight = document.viewport.getHeight();
	popup.setStyle ({top:scrollOffsets.top, left:scrollOffsets.left});
	popup.show();
}

function popUpAlignWin (alignText, gr) {
	var features = "innerHeight=300,height=300,innerWidth=550,width=550,resizable=1,scrollbars=1";
	features += ",location=0,menubar=0,toolbar=0,status=0,locationbar=0";
	var win = window.open ("align-pop-up.html", "align", features);
	win.title = "fooberry";
	var doc = win.document;
	
	doc.write ('<html>');
	doc.write ('<head>');
	doc.write ('<title>Alignment Text</title>');
	doc.write ('<LINK href="styles.css" type="text/css" rel="stylesheet">');
	
	var preamble = "This resource supports the following " + author + " " + topic + 
				   " standard for grades " + gr + ": ";
	
	doc.write ('</head>');
	doc.write ('<body>');
	doc.write ('<div class="align-text">' + preamble + " " + alignText + '</div>');
	doc.write ('<div class="closer"><input type="button" value="close" onclick="window.close()" /></div>');
	doc.write ('<div class="instr">-- copy ALL the text within the box and paste it into the comments form --</div>');
	doc.write ('</body>');
	doc.write ('</html>');
	doc.title = "Alignment Text"
	
	win.document.close()
	win.focus();
}

Event.observe (window, 'load', pageInit);
