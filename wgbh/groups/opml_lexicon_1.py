"""
create an html structure that reflects the lexixon_tree.xml
"""

from JloXml import XmlRecord, XmlUtils
from UserDict import UserDict
from HyperText.HTML import *
from HtmlDocument import MyDocument

class LexiconTree (XmlRecord):
	xpath_delimiter = "/"
	
	def __init__ (self):
		XmlRecord.__init__ (self, path="../data/lexicon_tree.xml")
		self.categories = self.get_categories()
		print "%d categories found" % len (self.categories)
		
	def get_categories (self):
		"""
		return dict (category_text -> categoryElement
		"""
		categories = UserDict()
		categoryNodes = self.selectNodes (self.dom, "wgbh_lexicon/category")
		for node in categoryNodes:
			text = node.getAttribute ("text")
			categories[text] = node
		return categories
	
class LexiconOPML (XmlRecord):
	
	xpath_delimiter = "/"
	
	def __init__ (self):
		XmlRecord.__init__ (self, xml="<body/>")
		self.lexicon_tree = LexiconTree ()
		self.body = self.doc
		self.makeOPML()
		
	def makeOPML (self):
		
		for category in self.lexicon_tree.categories.values():
			# print category
			catOutline = self.addElement (self.body, 'outline')
			catOutline.setAttribute ("type", "group")
			catOutline.setAttribute ("collapsible", "true")
			catOutline.setAttribute ("text", category.getAttribute("text"))
			
			for segment in XmlUtils.getChildElements(category):
				self.segmentToOpml (segment, catOutline)
				break
		
		
	def segmentToOpml (self, segment, opmlParent):
		text = segment.getAttribute ("text")
		id = segment.getAttribute ("id")
		children = XmlUtils.getChildElements(segment)
		
		segOutline = self.addElement (opmlParent, 'outline')
		segOutline.setAttribute ("text", text)
		if id:
			segOutline.setAttribute ("type", "vocab")
			segOutline.setAttribute ("vocab", id)
		else:
			segOutline.setAttribute ("type", "group")
			
		if children:
			segOutline.setAttribute ("collapsible", "true")
			for child in children:
				self.segmentToOpml (child, segOutline)
	
if __name__ == '__main__':
	opml = LexiconOPML ()
	print opml
		
