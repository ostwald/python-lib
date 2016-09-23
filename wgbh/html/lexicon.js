function log (s) {
	if (window.console)
		window.console.log (s);
}

var Node = Class.create ({
	initialize: function (element, baseUrl) {
		this.element = element;
		this.baseUrl = baseUrl;
		this.widget = this.element.down('div').down('img.widget', 0);
		this.segment = this.element.down('div').down('.segment', 0);
		this.body = this.element.down('.node_body', 0)
		this.label = null;
		
		
		this.closedImgSrc = this.baseUrl + '/btnExpandClsd.gif';
		this.openedImgSrc = this.baseUrl + '/btnExpand.gif';
		this.children = null;
		
		if (this.widget) {
			this.label = this.widget.next();
			// log (this.label.innerHTML);
			this.widget.observe ('click', this.toggle.bindAsEventListener(this));
			this.widget.observe ('mouseover', function () { 
				this.label.addClassName ('over');
			}.bind(this));
			this.widget.observe ('mouseout', function () { 
				this.label.removeClassName ('over');
			}.bind(this));
			
		}
		
		if (this.label) {
			this.label.observe ('click', this.toggle.bindAsEventListener(this));
			this.label.observe ('mouseover', function () { 
				this.label.addClassName ('over');
			}.bind(this));
			this.label.observe ('mouseout', function () { 
				this.label.removeClassName ('over');
			}.bind(this));
		}
	},
	
	toggle: function () {
		this.widget.src = this.widget.src == this.closedImgSrc ? this.openedImgSrc : this.closedImgSrc;
		
		/* lazy node initialization ... */
		if (!this.children) {
			this.children = this.body.childElements().inject ([], function (acc, nodeEl) {
				var node = new Node (nodeEl, this.baseUrl);
				acc.push (node);
				return acc;
			}.bind(this));
		}
		this.body.toggle();
	}
});

function getBaseUrl () {
	var splits = $A(window.location.href.split('/'));
	return splits.slice(0, splits.length-1).join ('/')
}

function pageInit (event) {
	
	var baseUrl = getBaseUrl();
	log ("baseUrl: " + baseUrl);
	
	var tree = $('lexicon_tree');
	if (!tree)
		log ("tree not found");
	else
		log ("tree found");
	
	/* Lazy node initialization - init nodes for the top-level terms (categories)
	   here, and then init the children only when the parent "toggle" function
	   is executed.
	*/
 	$('lexicon_tree').childElements().each (function (nodeEl) {
		new Node (nodeEl, baseUrl);
	});
	
	log ("initialized");
}

document.observe ('dom:loaded', pageInit)
