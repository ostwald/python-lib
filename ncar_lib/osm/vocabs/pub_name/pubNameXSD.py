"""
PubNameXSD - supports the following operations
 - getTermList
 - getHeader
 - getFooter

 - addTerm
 - removeTerm

 - write
 
PubNameXSD is a UserDict mapping term to "VocabTerm"
 
"""

import os, sys, codecs, re, string
from UserDict import UserDict
from termList import VocabTerm


restriction_pat = re.compile ("<xs:restriction base=\"xs:string\">(.*)</xs:restriction>", re.DOTALL)

class PubNameXSD (UserDict):
	
	"""
	Items are instances of VocabTerm
	"""
	
	def __init__ (self, path):
		UserDict.__init__ (self)
		self.path = path
		self.xsd = codecs.open(path, 'r', 'utf-8').read()
		self.header, self.body, self.footer = self.parse()
		self.terms = self.init_terms()
	
	def init_terms (self):
		# split body into lines, filter empty ones
		lines = map (string.strip, self.body.split('\n'))
		lines = filter (lambda x: x, lines)
		
		for vocabTerm in map (VocabTerm, lines):
			self[vocabTerm.term] = vocabTerm
		
	def addTerm (self, term, comment=None):
		if self.has_key (term):
			raise KeyError, "attempting to overwrite term (%s)" % term
		if type (term) == type(""):
			err = 0
			try:
				unicode(term)
			except:
				print sys.exc_info()[1]
				err = 1
			term = unicode(term, "utf-8", "replace")
			if err:
				print " ->",  term
		vocabTerm = VocabTerm (term=term, comment=comment)
		self[term] = vocabTerm
		
	def addVocabTerm (self, vocabTerm):
		self.addTerm (vocabTerm.term, vocabTerm.comment)
		
	def deleteTerm (self, term):
		if not self.has_key (term):
			raise KeyError, "attempting to delete non-existing term (%s)" % term
		del self[term]
		
	def parse(self):
		xsd = self.xsd
		m = restriction_pat.search (xsd)
		if not m:
			raise Exception, "restriction tag contents not found"
		header = xsd[:m.start(1)]
		body = m.group(1)
		footer = xsd[m.end(1):] 
		
		return header, body, footer
		
	def getSortedTerms (self):
		"""
		returns list of sorted string representations (VocabTerm.term)
		"""
		values = self.values()
		values.sort()
		return map (lambda x:x.term, values)
		
	def getTermListXSD (self):
		values = self.values()
		print "sorting values"
		values.sort()
		# format terms to match source XSD
		return '\n'.join (map (lambda x: '\t\t\t' + x.toxml(), values))
		
		
	def write (self, path="test.xsd"):
		term_as_xsd = self.getTermListXSD() # do it here so an exception doesnt wreck source!
		fp = codecs.open(path,'w', 'utf-8')
		# format sections to match source XSD
		fp.write (self.header + '\n\n' + term_as_xsd + '\n\n\t'+ self.footer)
		print "wrote PubNameXSD to " + path
		
	def report (self):
		for name in ['header',  'footer']:
			self.printSection (name)
			
	def printSection (self, name):
		"""
		append the sections (debugging)
		"""
		if not name in ['header', 'body', 'footer']:
			raise Exception, "unknown section name: %s" % name
		print "--------------%s-----------------\n" % name
		print getattr(self, name)
		print "----------- end of %s------------\n" % name
		
		
if __name__ == '__main__':
	pn = PubNameXSD ('pubName.xsd')
	for term in pn.getSortedTerms():
		if term.lower().startswith ("la m"):
			print term
	# pn.write()
