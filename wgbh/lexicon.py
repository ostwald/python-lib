"""
reads lexicon from text file that was created from table at
"http://www.teachersdomain.org:8086/public/view_all_lex_terms/"

this table contains the same terms that the WGBH service provides, but
provides additional information, most importantly a "category" ("Lexicon" column in the table)
that provides another level by which the terms can be handled.

"""
import string, urllib, time
from xls import XslWorksheet, WorksheetEntry
from UserDict import UserDict
from UserList import UserList
from JloXml import XmlRecord, XmlUtils

# category labels come from 
# http://www.teachersdomain.org/tdwiki/doku.php/partner:the_teachers_domain_educational_standards_api
lexicon_set_map = {
	'SciTech' : 'Science (with Technology and Engineering)',
	'math' : 'Math',
	'language_arts' : 'English Language Arts',
	'socst' : 'Social Studies/History',
	'arts' : 'Fine Arts'
	}

class LexiconEntry (WorksheetEntry):
	"""
	one line of the lexicon xls, representing a single lexicon term
	e.g., socst	7179	14th Century :: Europe :: Economics :: Agriculture
	 category^    ^id    ^term (segments)
	
	first item (e.g. "socst" is the "category"
	 - "lexicon_set_map" provides mapping from category value to human-readable form
	
	terms look like: "14th Century :: Europe :: Economics :: Agriculture"
	the terms parts are called "segments". segments are not consistently formatted
	(some have leading space, some don't), so "prettyTerm" normalizes the segments and reassembles
	
	"""
	
	def __init__ (self, textline, schema):
		WorksheetEntry.__init__ (self, textline, schema)
		self.category = self['Lexicon']
		self.term = self._make_term()
		self.id = self['ID']
		self.segments = self.term.split("::")
		self.prettyTerm = " :: ".join(self.segments)
		
		# ensure there are no underscores in this term
		if '_' in self.term:
			raise KeyError, "UNDERSCORE found in %s" % self.id
		
		# self.xpath = self.category + "/" + "/".join(map (lambda x:x.replace(' ', '_'), self.segments))
		normalize = lambda x:x.replace(' ', '_').replace (',', '')
		self.xpath = self.category + "/" + "/".join(map (normalize, self.segments))
		
		# raw_path uses original (not normalized) segements and is used in lexicon_stds_doc
		self.raw_xpath = self.category + "/" + "/".join(self.segments)
		
	def __len__ (self):
		return len (self.segments)
		
	def _make_term (self):
		"""
		normalize term by stripping the components and rejoining
		"""
		return '::'.join (map(string.strip, self['Term'].split('::')))

	def report (self):
		print "(%s) %s, id: %s (%d)" % (self.category, self.xpath, self.id, len(self))
		
class LexiconWorkSheet (XslWorksheet):
	"""
	reads the lexicon worksheet (tab-delimited created from xls file that was
	created from "all lexicon term" web page
	
	"""
	verbose = 1
	data_path = 'data/Teachers Domain - All Lexicon Terms.txt'
	
	def __init__ (self):
		XslWorksheet.__init__ (self, entry_class=LexiconEntry)
		self.read(self.data_path)

	def accept (self, term):
		"""
		don't accept terms that do not have a category
		"""
		return term.category
		
	def reportTermSegments (self):
		lengths = []
		for item in self:
			mylen = len (item[0].split ('::'))
			if not mylen in lengths:
				lengths.append (mylen)
				
		print lengths
		
class Lexicon2Tree (XmlRecord):
	"""
	organize Lexicon as a xml tree of LexiconNodes
	
	top-level are the "categories", and then all others represesent "segments"
	
	some "segments" have ids, some don't (segments with ids are not always leaf nodes!)
	"""
	
	def __init__ (self):
		XmlRecord.__init__ (self, xml="<wgbh_lexicon/>")
		self.doc.setAttribute ("timestamp", time.asctime())
		self.terms = LexiconWorkSheet()
		for i, term in enumerate (self.terms):
			# some terms have no category, skip these!
			if term.category:
				if i % 100 == 0:
					print '%d/%d - %s' % (i, len(self.terms), term.prettyTerm)
				xpath = term.xpath
				parent = self.doc
				term_parts = term.segments
				term_parts.insert(0, term.category)
				for j, part in enumerate (term_parts):
					isLeaf = self._is_leaf_segment (j, term)
					isCategory = j == 0
					
					itemText = isCategory and lexicon_set_map[part] or part
					
					child = self.findChild (parent, itemText)
					nodeName = isCategory and "category" or "segment"
					if not child:
						child = self.addElement (parent, nodeName)
						# print 'added %s' % nodeName

						child.setAttribute ("text", itemText)
						if isLeaf:
							child.setAttribute ("id", term.id)
							child.setAttribute ("term", term.prettyTerm)
							# XmlUtils.setText (child, term.prettyTerm)
					parent = child
					
			if i > 10000: break
			# parent = categoryNode
			# for segment in term.categories:
			
	def _is_leaf_segment (self, segment_index, term):
		return segment_index == len(term.segments) - 1
			
	def findChild (self, parent, term):
		for node in XmlUtils.getChildElements(parent):
			if node.getAttribute ("text") == term:
				return node
			
	def getCategoryNode (self, category):
		node = self.selectSingleNode (self.dom, category)
		if not node:
			node = self.addElement (self.doc, category)
		return node
	
 
		
if __name__ == '__main__':
	# lex = LexiconWorkSheet()

	tree = Lexicon2Tree()
	# for i in range(0, 10):
		# tree.terms[i].report()		
	# tree.write ("data/lexicon_tree.xml", pretty=False)





