from JloXml import XmlRecord, XmlUtils
from UserDict import UserDict
"""
parse an XML doc created from a pdf that lists the AMS publication
abbreviations

create "journal_map" as mapping from journal name to abbr 
"""

path = 'AMSPubs_Abbrev.xml'

class PubNameAbbrev (XmlRecord):
	
	xpath_delimiter = "/"
	journal_map = UserDict()

	def getRows (self):
		return self.selectNodes (self.dom, "TaggedPDF-doc/Table/TR")

	def convertRows (self):
		"""
		change first cell element to TH when there are two elements present for given row
		"""
		rows = self.getRows()
		print "%d rows found" % len(rows)
		if not rows:
			return
		for row in rows:
			children = rec.getElements(row)
			if len(children):
				header = children[0]
				header.tagName = "TH"
				# print header.tagName
		
	def getJournalMap (self):
		for row in self.getRows():
			children = rec.getElements(row)
			if len(children) == 2:
				journal = XmlUtils.getText(children[0])
				abbrev = XmlUtils.getText(children[1])
				if abbrev:
					self.journal_map[journal] = abbrev	
		return self.journal_map
				
	def report (self):
		rows = self.getRows()
		print "%d rows found" % len(rows)
		if not rows:
			return
		for row in rows:
			children = rec.getElements(row)
			if len(children) == 2:
				journal = XmlUtils.getText(children[0])
				abbrev = XmlUtils.getText(children[1])
				if abbrev:
					print "\n%s\n(%s)" % (journal, abbrev)	
				else:
					print "\n -- %s --" % journal
if __name__ == '__main__':
				
	rec = PubNameAbbrev (path=path)
	mapping = rec.getJournalMap ()
	journals = mapping.keys()
	journals.sort()
	for journal in journals:
		print "\n%s\n(%s)" % (journal, mapping[journal]) 


