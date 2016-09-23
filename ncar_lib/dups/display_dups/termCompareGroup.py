"""
Obtains search results for each term contained in a TermMapEntry.
Search results are used to compare records and ultimately to display records for human inspection
"""
import os, sys
from JloXml import XmlUtils
from UserList import UserList
from title_searcher import TitleSearcher
from mockTermMapEntry import getMockTermMapEntry

class DupCompareGroup (UserList):
	"""
	Holds a list of records (few at most) for comparison.
	Used to compare records that are suspected of being dups or at least very similar
	"""
	def __init__ (self, search_results):
		UserList.__init__ (self)
		self.data = search_results
	
	
class TermCompareGroup (DupCompareGroup):
	"""
	Use dds (via TitleSearcher) to obtain records for the terms
	in a TermMapEntry
	"""
	def __init__ (self, termMapEntry):
		self.termMapEntry = termMapEntry
		# get the metadata associated with the terms in this entry
		DupCompareGroup.__init__(self, self.getSearchResults())

		print "%d results found for %s" % (len(self), self.termMapEntry.key)
		if not len(self) == self.termMapEntry.docCount:
			raise Exception, '%d search results found, %d expected' % (len(self), self.termMapEntry.docCount)
		
	def getSearchResults (self):
		results = []
		for term in self.termMapEntry.terms:
			results = results + TitleSearcher(term.title).data
		return results
			
def getTermCompareGroup():
	return TermCompareGroup (getMockTermMapEntry())

if __name__ == '__main__':
			
	comp = TermCompareGroup (getMockTermMapEntry())
	for item in comp:
		print item.recId

