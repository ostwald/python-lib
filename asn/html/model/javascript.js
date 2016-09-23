var closed_img, opened_img;

function init () {
	alert ("preloading images")
	preloadImages()
}


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
	var objElement = document.getElementById( elementID );
	var imgObj = document.getElementById (elementID+"_img");
	if ( objElement != null ) {
		if ( objElement.style.display == "none" ) {
			objElement.style.display = "block";
			imgObj.src = "images/opened.gif";
			// imgObj.src = opened_img.src;
		}
		else {
			objElement.style.display = "none";
			imgObj.src = "images/closed.gif";
		}
	}
	else {
		alert ("objElement was null for " + elementID);
	}
}

function highlightWidget (id) {
	var std = getParentStd (id);
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
	var std = getParentStd (id);
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

function getParentStd (id) {
	var obj = $(id)
	if (obj == null) {
		alert ("object not found for " + id);
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
		
function formatStandard (std) {
	// var std = getParentStd (id);
	[left, top] = Position.cumulativeOffset (std);
	// alert ("left: " + left + "  top: " + top);
	var stdDims = std.getDimensions();
	std.setStyle ({height:stdDims.height-12})
	var wgt = getStdWidget (std);
	wgt.setStyle ({position:"relative", top:5, left:-5})
	var cnt = getStdContent (std);
	cnt.setStyle ({position:"relative", top:-12, left:20, marginRight:20})
}

function formatStandards () {
	var stds = $A(document.getElementsByClassName ("std"));
	stds.each (function (node) {
		formatStandard (node)});
}
