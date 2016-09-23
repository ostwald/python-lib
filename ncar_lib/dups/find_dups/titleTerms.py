"""
Objective: Identify dups

1 - use dds-search to make lists of all indexed titles.

Try to determine the collections we're interested in:
	PUBS Not FY10
	OpenSky General Collection
	Citations - PUBs Refereed
	Citations - WOS
	
Question: What does a dup look like? How many are in the PUBS Not FY10 collection?
	
DATA: listTermsServiceOutput.xml - response to "list terms" for /key//record/general/title
How can we use this data?
1 - make a list of all titles with multiple occurrences - this is where we start looking for dups
2 - from the list of titles can we find any that are REALLY dups but have some little difference? 

"""
import os, sys, codecs
from JloXml import XmlRecord, XmlUtils
from UserDict import UserDict
from UserList import UserList
titles_listing = "listTermsServiceOutput.xml"	

class Term:
	"""
	Encapsulate an item from the ListTerms dds response
	e.g., <term termCount="1" docCount="1">A Planet in Peril</term>
	"""
	def __init__ (self, element):
		self.termCount = int (element.getAttribute ('termCount'))
		self.docCount = int (element.getAttribute ('docCount'))
		self.title = XmlUtils.getText (element)
		
	def __repr__ (self):
		## return "%s (%d, %d)" % (self.title.encode('utf-8'), self.termCount, self.docCount)
		return "%s (%d)" % (self.title.encode('utf-8'), self.docCount)

class TermList (XmlRecord):
	"""
	reads a "ListTerms" response from the DDS (stored as a file), and parses into
	Term instances.
	- terms - all Terms
	- multiTerms - Terms appearing in more than one record
	- termMap - see TermMap below
	"""
	
	xpath_delimiter = '/'
	
	def __init__ (self):
		XmlRecord.__init__ (self, path=titles_listing)
		termElements = self.selectNodes (self.dom, 'DDSWebService/ListTerms/terms/term')
		print '%d termElements found' % len(termElements)

		self.terms = map (Term, termElements)
		# print self.terms[2]
		
		self.multiTerms = filter (lambda x:x.docCount > 1, self.terms)
		print '%d multiTerms found' % len(self.multiTerms)
		
		
	def showMultiTerms (self):
		for m in self.multiTerms:
			print m



if __name__ == '__main__':
	terms = TermList()
	terms.showMultiTerms()

