"""
new terms tester
"""
import sys
from pubNamesWorksheet import PubNamesWorkSheet, data_worksheeet_path
from pubNameXSD import PubNameXSD, VocabTerm

class DataTester:

	add_term_comment = "2010-12-02:added per Jamaica's spreadsheet"
	
	def __init__ (self, path=data_worksheeet_path):
		self.ws = PubNamesWorkSheet (path)
		print "%d worksheet records read" % len(self.ws)
		self.pubs = PubNameXSD ('pubName.xsd')
		print "%d pubName terms read" % len(self.pubs)

class SanityTester (DataTester):

	
	def __init__ (self, path=data_worksheeet_path):
		DataTester.__init__ (self, path)
		self.report()

	def report (self):
		print "the following items have identical bad and good terms"
		for item in self.ws:
			if item.term == item.badterm:
				print item.term
		
class AddCorrectTerms (DataTester):
	
	def __init__ (self, path=data_worksheeet_path):
		DataTester.__init__ (self, path)
		
		self.added_terms = []
		self.errors = []
		
		self.addAllTerms()
		self.report()
	
	def addAllTerms (self):
		self.added_terms = []
		for entry in self.ws:
			term = entry.term
			vocabTerm = VocabTerm (term=entry.term, comment=self.add_term_comment)
			if vocabTerm in self.added_terms:
				# print 'skipping', term
				continue
			# print term
			try:
				# vocabTerm = VocabTerm (term=term, comment=self.add_term_comment)
				self.pubs.addVocabTerm (vocabTerm)
				self.added_terms.append (vocabTerm)
				
			except KeyError:
				# print sys.exc_info()[1]
				self.errors.append(vocabTerm)
				
		self.errors.sort()
		
	def report (self):
		print "\n======================="
		print "AddCorrectTerms Report"
		print "\nTerms added to pubName (%d)" % len(self.added_terms)
		self.added_terms.sort()
		for vocabTerm in self.added_terms:
			# print " - %s" % vocabTerm.term.encode('utf-8')
			print " - %s" % vocabTerm.term

		print "\n%d terms after adding" % len(self.pubs)
		print '\nTerms already in pubName (%d):' % len (self.errors)
		for msg in self.errors:
			print ' - ',msg
			
class DeleteIncorrectTerms (DataTester):
	
	def __init__ (self, path=data_worksheeet_path):
		DataTester.__init__ (self, path)
		
		self.added_terms = []
		self.errors = []
		
		self.deleteBadTerms()
		self.report()
	
	def deleteBadTerms (self):
		self.deleted_terms = []
		for entry in self.ws:
			badterm = entry.badterm
			
			# skip empty badterms
			if not badterm:
				continue
				
			# skip terms with equal term and badterm
			if entry.term == entry.badterm:
				continue
				
			# skip those we've already attempted to delete
			if badterm in self.deleted_terms:
				# print 'skipping', term
				continue
				
			# print term
			try:
				# vocabTerm = VocabTerm (term=term, comment=self.add_term_comment)
				self.pubs.deleteTerm (badterm)
				self.deleted_terms.append (badterm)
				
			except KeyError:
				# print sys.exc_info()[1]
				self.errors.append(badterm)
				
		self.errors.sort()
		self.deleted_terms.sort()
		
	def report (self):
		print "\n======================="
		print "Delete Bad Terms Report"
		print "\nTerms deleted from pubName (%d)" % len(self.deleted_terms)
		for term in self.deleted_terms:
			print " - %s" % term

		print "\n%d terms after deleting" % len(self.pubs)
		print '\nBad terms not found in pubName (%d):' % len (self.errors)
		for msg in self.errors:
			print ' - ',msg
			
if __name__ == '__main__':
	if 1:
		tester = AddCorrectTerms()
		# tester.pubs.write ("afterAddCorrectTerms.xsd")
	elif 0:
		SanityTester()
	else:
		tester = DeleteIncorrectTerms()
		tester.pubs.write ("afterDeleteBadTerms.xsd")
		
