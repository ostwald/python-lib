"""
LabReportResult - extends OsmAuthorSearchResult to provide the information required for the LabReport

The fields we need are

"""

import os, sys
import utils
from ncar_lib.repository.author_search import OsmAuthorSearchResult

class LabReportResult (OsmAuthorSearchResult):
	
	report_fields = [
	'title',
	'pubName',
	# 'Volume, issue, page numbers (as available)'
	'volume',
	'issue',
	'pageSpan',
	'pages',
	'doi', 
	'confidence',
	'classification',
	'status', # (published, in press, etc)'
	'recId',
	# 'fiscalDate', # mostly just for debugging
	'authors',  # requires special attn
	]
	
	def __init__ (self, searchResult, parAuthor):
		OsmAuthorSearchResult.__init__ (self, searchResult, parAuthor)
		self.osmRecord = searchResult.get_payload()
		self.authors = self.makeAuthorsString()
		self.pubName = self.osmRecord.get('pubName')
		self.doi = self.osmRecord.getDoi()
		self.confidence = "unkown"
		self.volume = self.osmRecord.get('volume')
		self.issue = self.osmRecord.get('issue')
		self.pageSpan = self.osmRecord.get('pageSpan')
		self.pages = self.osmRecord.get('pages')
		self.fiscalDate = self.osmRecord.getDate ("Fiscal")
		self.classification = self.osmRecord.get('classification')
		self.status = self.osmRecord.get('status')
		
	def makeAuthorsString (self):
		"""
		i assume we grab all contributors???
		"""
		authors = self.osmRecord.getContributorPeople()
		authors.sort()  # put them in ORDER
		
		names = []
		for author in authors:
			#name = "%s" % author
			name = author.lastName
			if author.firstName:
				name = "%s, %s." % (name, author.firstName[0])
				if author.middleName:
					name = "%s %s." % (name, author.middleName[0])
			names.append (name)
		
		# names = map (lambda x:x.__repr__(), authors)
		return u', '.join(names)
		
	def setConfidence (self, confidence):
		self.confidence = confidence
		
	def asTabDelimited (self):
		try:
			return '\t'.join(map (self.getAttr, self.report_fields))
		except KeyError, msg:
			print sys.exc_info ()[1]
			print '*%s*' % msg
