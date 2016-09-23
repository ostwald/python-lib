"""
Group Similar terms together

We create a 'key' for each unique title that contains only the alpha characters, dropping
all others. Unique titles are then groups by this 'key' to put potentially similar titles together.

The TermMap values are basically the titles (and their counts) that map to a particular key (and are
therefore potential dups). To resolve these titles into actual records, we must search for the titles
(see title_searcher.TitleSearcher

"""
import os, sys, codecs
from titleTerms import TermList, Term
# from JloXml import XmlRecord, XmlUtils
from UserDict import UserDict
titles_listing = "title-term-count.xml"	

class TermMapEntry:
	"""
	Groups all Terms that are associated with a particular KEY.
	- docCount - a count of the	records matching that key
	- terms - a list of Term instances whose title matches the KEY
	"""
	
	def __init__ (self, key):
		self.key = key
		self.terms = []
		self.docCount = 0
		
	def addTerm (self, term):
		self.terms.append(term)
		self.docCount = self.docCount + term.docCount
			
	def __cmp__ (self, other):
		docCountCmp = -cmp(self.docCount, other.docCount)
		if docCountCmp != 0:
			return docCountCmp
		else:
			return cmp (self.key, other.key)
			
	def report (self):
		print '\n%d - %s' % (self.docCount, self.key)
		for term in self.terms:
			print ' - %s' % term
		
class TermMap (UserDict):
	"""
	mapping from a specially contructed KEY to all terms matching the key.
	the purpose of the termMap is to group potential dups, even if they do not have
	an identical title. this is done via the KEY, which drops all non-alpha characters
	from the title and casts to lower case.
	"""
	def __init__ (self):
		UserDict.__init__(self)
		termList = TermList()
		map (lambda x: self.addItem(x), termList.terms)

	def getKey (self, term):
		"""
		cast title to lower case and then remove all non-alphas
		"""
		s = ""
		for ch in term.title.lower():
			if ord(ch) >= 97 and ord(ch) <= 122:
				s = s + ch
		return s
		
	def addItem (self, term):
		"""
		create an new entry for this term if there isn't one, or 
		add this term to the existing entry
		"""
		key = self.getKey (term)
		if not self.has_key(key):
			self[key] = TermMapEntry(key)
		self[key].addTerm(term)
		
	def tallyHo (self):
		"""
		output the items in this TermMap as follows:
			<number of close-matches> -> <number of groups having this number of close-matches>
		"""
		tally = {}
		for entry in self.values():
			cnt = entry.docCount
			if tally.has_key(cnt):
				tally[cnt] =  tally[cnt] + 1
			else:
				tally[cnt] = 1
		keys = tally.keys()
		keys.sort()
		keys.reverse()
		for key in keys:
			print '%d -> %d' % (key, tally[key])
		
	def report (self):
		entries = self.values()
		print '\nTermMap (%d unique keys)' % len(self)
		if 1:
			entries.sort()
			for entry in entries:
				if entry.docCount > 1:
					entry.report()

if __name__ == '__main__':
	termMap = TermMap()
	termMap.report()
	termMap.tallyHo()
