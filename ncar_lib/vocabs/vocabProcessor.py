import os, sys, re
from ncar_lib.osm import PubNameXSD, VocabTerm
VocabReader = PubNameXSD
del PubNameXSD
from vocabTermRecord import VocabTermRecord
from termSearch import TermSearcher, TermCounter

pubName = 'data/pubName.xsd'
instName = 'data/instName.xsd'

class DateError (Exception):
	pass

class VocabProcessor:
	
	datePat = re.compile("[\d]+-[\d]+-[\d]+")
	dateCheckPat = re.compile("[\d]{4}-[\d]{2}-[\d]{2}")
	dowrites = 1
	
	searchField = None
	prefix = None
	destdir = None
	
	def __init__ (self, path):
		self.path = path
		self.reader = VocabReader(path)
		self.recnum = 1
		print 'read %d terms' % len(self.reader)
		self.process()

	def process (self):
		vocabTerms = self.reader.values()
		vocabTerms.sort()
		for vocabTerm in vocabTerms:
			rec = self.makeRecord (vocabTerm)
			
	def setVocabType (self, rec):
		pass
			
	def makeRecord (self, vocabTerm):
		rec = VocabTermRecord()
		recId = rec.makeRecordId (self.prefix, self.recnum)
		rec.setId (recId)
		self.recnum += 1
		rec.setFullName (vocabTerm.term)
		
		if self.dowrites:
			recordsAffected = TermCounter(vocabTerm.term, self.searchField).numRecords
			rec.setRecordsAffected (str(recordsAffected))
		
		try:
			date = self.extractDate(vocabTerm.comment)
		except DateError:
			print "date error: %s (%s)" % (vocabTerm.term, sys.exc_info()[1])
			sys.exit()
		if date:
			rec.setDateVerified (date)
			rec.setAuthority ("NCAR Library")
		
		self.setVocabType (rec)
			
		if self.dowrites:
			rec.write (os.path.join (self.destdir, recId+'.xml'))
			
		return rec
		
	def extractDate (self, comment):
		if not comment:
			return
		m = self.datePat.search(comment)
		if m:
			raw = m.group()
			if not self.dateCheckPat.match(m.group()):
				raise DateError, raw
			return raw
		
class PubNameProcessor (VocabProcessor):
	
	searchField = '/key//record/general/pubName'
	prefix = 'PUBNAME'
	destdir = 'pubname'
	
class InstNameProcessor (VocabProcessor):
	
	searchField = [
		'/key//record/contributors/organization/affiliation/instName',
		'/key//record/contributors/person/affiliation/instName'
	]
	prefix = 'INST'
	destdir = 'inst'
	
	def setVocabType (self, rec):
		rec.setType ('Institutional name')
	
if __name__ == '__main__':
	# InstNameProcessor (instName)
	PubNameProcessor (pubName)
	


			
				
