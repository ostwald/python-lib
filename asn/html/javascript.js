var closed_img, opened_img;

/* preload collapsible node images */
function preloadImages () {
	if (document.images)
		{
			closed_img = new Image(11,11);
			closed_img.src = "images/closed.gif";
			
			opened_img = new Image(11,11);
			opened_img.src = "images/opened.gif";
		}
	else {
		alert ("document.images not found!")
	}
}

function toggleVisibility( elementID ) {
	// alert ("toggleVisiblity(" + elementID + ")");
	var boxObj = $( elementID+"_box" );
	var imgObj = $(elementID+"_img");
	if ( boxObj != null ) {
		if ( boxObj.style.display == "none" ) {
			boxObj.style.display = "block";
			imgObj.src = "images/opened.gif";
			// imgObj.src = opened_img.src;
		}
		else {
			boxObj.style.display = "none";
			imgObj.src = "images/closed.gif";
		}
	}
	else {
		alert ("boxObj was null for " + elementID);
	}
}

function highlightWidget (id) {
	var std = getParentStd ($(id));
	if (std == null) {
		alert ("parent standard not found for " + id);
		return;
	}
	var widget = getStdWidget (std);
	if (widget == null) {
		alert ("widget not found for standard");
		return;
	}
	widget.setStyle ({backgroundColor:"yellow"});
}

function highlightContent (id) {
	var std = getParentStd ($(id));
	if (std == null) {
		alert ("parent standard not found for " + id);
		return;
	}
	var stdContent = getStdContent (std);
	if (stdContent == null) {
		alert ("stdContent not found for standard");
		return;
	}
	stdContent.setStyle ({backgroundColor:"blue"});
}

function getStdContent (std) {
	return getChildByClass (std, "std-content");
}

function getStdWidget (std) {
	return getChildByClass (std, "widget");
}

function getChildByClass (e, klass) {

	var children = $A(e.getElementsByTagName ("div"));
	// alert (children.length + " child divs found");
	return children.find (function (node) {
		// alert (node.nodeName);
		return node.hasClassName (klass)
	});
}

function getParentStd (obj) {

	if (obj == null) {
		alert ("object not found for " + obj.toString());
		return;
	}
	while (!obj.hasClassName("std")) {
		// alert (obj.nodeName)
		obj = obj.parentNode;
		if (obj == null)
			break;
		// obj = $(obj)
	}
	return obj;
}
		
function formatStandardById (id) {
	var std = getParentStd ($(id));
	if (std == null) {
		alert ("standard not found for " + id);
		return;
	}
	formatStandard ($(id));
}

function formatStandard (std) {
	offset = Position.cumulativeOffset (std);
	left = offset[0];
	top = offset[1];
	
	// the following assignment seems to work in most browsers except mac firefox
	// [left, top] = Position.cumulativeOffset (std);
	// alert ("left: " + left + "  top: " + top);
	
	var stdDims = std.getDimensions();
	std.setStyle ({height:stdDims.height-12})

}

function formatStandards () {
	var stds = $A(document.getElementsByClassName ("std"));
	stds.each (function (node) {
		formatStandard (node)});
}

/* does NOT work and is not called */
function myScrollTo (id) {
	// alert ("x myScrollTo: \"" + id + "\"");

	var obj = $(id);
	if (obj != null) {
		alert ("scrolling to \"" + id + "\"");
		// return $("hierarchy").scrollTo(id);
		$("hierarchy").scrollTo(id);
		// new Element.scrollTo(id);
	}
	else {
		alert ("object not found for \"" + id + "\"");
	}
}
/*
	mousing over collapse/bullet widget displays info
*/
function activateWidgetInfo () {
	var stds = $A(document.getElementsByClassName ("std"));
	stds.each (function (node) {
		var id = node.id
		new Event.observe (id+"_stats", 'mouseover', showStats, true);
		var widget = $(id+"_widget")
		new Event.observe (widget, 'mouseover', showStats, true);
		$A(widget.childNodes).each (function (child) {
			new Event.observe (child, 'mouseover', showStats, true);
		})
	});
	
	// $('stats-overlay').setStyle ({display:"none"});
	new Event.observe ('stats-overlay', 'mouseout', hideStats, true);
}

function init () {
	preloadImages()
	
	// activateWidgetInfo();
}
		
var current_stats = null;

function showStats (evnt) {
	var target = $(evnt.target)
	var std_stats = getStdStats ($(evnt.target));
	if (std_stats == null)
		return;
	// alert ("showStats: " + std_stats.id);
	// std_stats.show();
	
	current_stats = std_stats;
	var stats_pos = Position.cumulativeOffset(std_stats);
	var stats_dims = std_stats.getDimensions();
	var extra = 20;
	$('stats-overlay').setStyle ({display:"block", left:stats_pos[0] - (extra / 2), 
								  top:stats_pos[1] - (extra / 2), 
								  width:stats_dims.width + extra,
								  height:stats_dims.height + extra});
	std_stats.setStyle ({display:"block"});
}
	
function hideStats (evnt) {
/* 	var target = $(evnt.target)
	var std_stats = getStdStats ($(evnt.target)); */
	if (current_stats == null)
		return;
	// std_stats.hide();
	current_stats.setStyle ({display:"none"});
	$('stats-overlay').setStyle({display:"none"});
	current_stats = null;
}

function getStdStats (obj) {
	var std = getParentStd ($(obj))
	if (std == null) {
		alert ("std not found");
		return null;
	}
	var std_stats = $(std.id+"_stats");
	if (std_stats == null) {
		// alert ("std stats not found for " + std.id);
	}
	return std_stats;
}

function hideStatsOld () {
	$("stats").hide();
}

/* positions a div element in proximity to widget, sets content, and displays
- problem - sometimes the id was not obtained??
*/
function showStatsOld (evnt) {
	var s= evnt.type + " event captured";
	s += "x: " + evnt.pageX + "  y: " + evnt.pageY;
	var icon = $(evnt.target)
	var std_id = icon.id.split("_")[0]
	// alert (s);
	var stats = $("stats")
	var xDelta = 11
	var yDelta = -20
	var x = Position.cumulativeOffset(icon)[0] + xDelta; // evnt.pageX + 2;
	var y = Position.cumulativeOffset(icon)[1] + yDelta; // evnt.pageY -30;
	var std = $(std_id)
	if (std == null) {
		alert ("std not found for " + std_id);
		return;
	}
	var std_stats = $(std_id+"_stats");
	if (std_stats == null) {
		alert ("std stats not found for " + std_id);
		return;
	}
	stats.innerHTML = std_stats.innerHTML;
	stats.setStyle ({display:"block", left:x, top:y});
}
