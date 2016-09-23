"""
create an html structure that reflects the lexixon_tree.xml
"""

from JloXml import XmlUtils
from lexicon_tree import LexiconTree
from UserDict import UserDict
from HyperText.HTML import *
from HtmlDocument import MyDocument
		
class LexiconHtml (LexiconTree):
	"""
	read lexicon_tree as xmlRecord
	create HTML by traversing lexicon_tree and converting to an html form
	that supports collapse/expanding nodes
	
	html depends upon styles.css and lexicon.js, which are files residing in "html" directory
	"""
	def __init__ (self):
		LexiconTree.__init__ (self)
		self.html = DIV(id="lexicon_tree")
		for categoryEl in self.categories.values()[:1]:
			self.html.append (self.catToHtml (categoryEl))
		
	def catToHtml (self, element):
		"""
		create html representation of cat, including recursively converting each underlying
		segment to a html form (attaching the html to the catagory
		"""
		node = DIV (klass="node")
		node_widget = IMG(src="btnExpandClsd.gif", klass="widget")
		text = element.getAttribute ("text")
		node_label = SPAN (text, klass="label category")
		
		node_header = DIV (node_widget, node_label)
		node.append (node_header)
		
		node_body = DIV(klass="node_body", style="display:none")
		node.append (node_body)
		
		for child in XmlUtils.getChildElements(element):
			self.segmentToHtml (child, node_body)
		return node
		
	def segmentToHtml (self, element, domParent):
		"""
		recursively convert segment to html and attaching to DomParent
		"""
		text = element.getAttribute ("text")
		children = XmlUtils.getChildElements(element)
		id = element.getAttribute ('id')
		node = DIV (klass="node")
		if id:
			node_label = SPAN ("%s (%s)" % (text, id), klass="term label", id=id)
		else:
			node_label = SPAN (text, klass="label")
			
		if children:
			node_widget = IMG(src="btnExpandClsd.gif", klass="widget")
		else:
			node_widget = IMG(src="clear.gif", klass="no-widget")
			
		node_header = DIV (node_widget, node_label)
			
		node.append (node_header)
		
		if children:
			node_body = DIV(klass="node_body", style="display:none")
			node.append (node_body)
			for child in children:
				self.segmentToHtml (child, node_body)
				
		domParent.append (node)
		return node
		
	def makeHtmlDocument (self):
		"""
		create HTML document
		"""
		# MyDocument (stylesheet=stylesheet, javascript=javascript)
		stylesheet = "styles.css"
		javascript = ["prototype.js", "lexicon.js"]
		doc = MyDocument(stylesheet=stylesheet, javascript=javascript)
		doc.body.append (H1 ("The Teachers' Domain Lexicon"))
		doc.body.append (DIV 
			("This page is a hierarchical representation of the ",
			  Href ('http://www.teachersdomain.org:8086/public/view_all_lex_terms/',
			        'Teacher\'s Domain Lexicon term list', target='_blank'),
			  klass='blurb'))
		doc.body.append (self.html)
		return doc
		
	def writeHtmlDocument (self, outpath=None):
		"""
		write HtmlDocument to file
		"""
		outpath = outpath or "html/lexicon.html"
		doc = self.makeHtmlDocument()
		doc.writeto (outpath)
		print "wrote to ", outpath
		
def foo():
	lexml = LexiconHtml ()
	outpath = "lexicon.html"
	fp = open (outpath, 'w')
	fp.write (lexml.mycat.__str__())
	fp.close()
	print "wrote html to", outpath	
	
if __name__ == '__main__':
	lexml = LexiconHtml ()
	lexml.writeHtmlDocument("TEMP_HTML.html")
		
