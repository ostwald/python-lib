"""
create an html structure that reflects the lexixon_tree.xml
"""

from JloXml import XmlRecord, XmlUtils
from UserDict import UserDict

default_path = "data/lexicon_tree.xml"

class LexiconTree (XmlRecord):
	xpath_delimiter = "/"
	
	def __init__ (self, path=None):
		XmlRecord.__init__ (self, path=path or default_path)
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
	
	
if __name__ == '__main__':
	LexiconTree ()
		
