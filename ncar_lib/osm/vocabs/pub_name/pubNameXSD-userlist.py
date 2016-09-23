"""
PubNameXSD - supports the following operations
- getTermList
- getHeader
- getFooter

- addTerm
- removeTerm

- write

NOTE: this version of pubNameXSD is superceeded by that
in pubNameXSD. 

"""

import os, sys, codecs, re, string
from UserList import UserList
from termList import VocabTerm


restriction_pat = re.compile ("<xs:restriction base=\"xs:string\">(.*)</xs:restriction>", re.DOTALL)

class PubNameXSD (UserList):
	
	"""
	Items are instances of VocabTerm
	"""
	
	def __init__ (self, path):
		UserList.__init__ (self)
		self.path = path
		self.xsd = codecs.open(path, 'r', 'utf-8').read()
		self.header, self.body, self.footer = self.parse()
		self.terms = self.init_terms()
	
	def init_terms (self):
		# split body into lines, filter empty ones
		lines = map (string.strip, self.body.split('\n'))
		lines = filter (lambda x: x, lines)
		
		self.data = map (VocabTerm, lines)
		
	def addTerm (self, term, comment=None):
		self.append (VocabTerm (term=term, comment=comment))
		
	def deleteTerm (self, term):
		found = None
		for vocabTerm in self:
			if vocabTerm.term == term:
				found = vocabTerm
				# print "found term: %d" % self.index(vocabTerm)
				self.remove(vocabTerm)
				break
		if not found:
			raise KeyError, "vocab term not found for '%s'" % term
		
	def parse(self):
		xsd = self.xsd
		m = restriction_pat.search (xsd)
		if not m:
			raise Exception, "restriction tag contents not found"
		header = xsd[:m.start(1)]
		body = m.group(1)
		footer = xsd[m.end(1):] 
		
		return header, body, footer
		
	def write (self, path="test.xsd"):
		fp = codecs.open(path,'w', 'utf-8')
		self.sort()
		
		# format terms to match source XSD
		terms_toxsd = '\n'.join (map (lambda x: '\t\t\t' + x.toxml(), self))
		
		# format sections to match source XSD
		fp.write (self.header + '\n\n' + terms_toxsd + '\n\n\t'+ self.footer)
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
	print len(pn), 'terms before'
	# pn.deleteTerm ('a FOOBERRY')
	print len(pn), 'terms after'
	# pn.write('pubName-sorted.py')
