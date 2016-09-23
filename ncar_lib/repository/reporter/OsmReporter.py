"""
OsmReporter
"""
import sys, os
from ncar_lib import OsmSearchResult
from Reporter import ReportSearcher, Reporter, ReportResultMixin

class OsmReportResult (OsmSearchResult, ReportResultMixin):
	"""
	Exposeds OsmSearchResult attributes as well as those defined here
	"""
	# default_payload_constructor = XmlRecord 
	verbose=0
	
	def __init__ (self, element):
		"""
		expose attributes that are needed as column names (see OsmReporter.default_columns)
		"""
		OsmSearchResult.__init__ (self, element)
		
		self.recordID = self.recId
		self.title = self.payload.getTitle()
		self.authors = self.getAuthors()
		self.osmDatePublished = self.storedContent.get('osmDatePublished')
		self.publishedDate = self.osmDatePublished or self.payload.getPubDate()
		self.status = self.dcsstatus
		
		# defined for RAL queries
		self.date = self.payload.getTextAtPath ('record/coverage/date')
		self.instName = self.payload.getTextAtPath ('record/contributors/organization/affiliation/instName')
		self.pageSpan = self.payload.getPageSpan()
		self.doi = self.payload.getDoi()
		self.volume = self.payload.getVolume()
		self.issue = self.payload.getIssue()
		
		
	def getAuthorsLastFirst (self):
		"""
		return authors as string (Jones, R.U., Smith, A.U)
		build the string from a list of ContributorPeople
		"""
		contributors = self.payload.getContributorPeople('Author')
		authors = [];add=authors.append
		
		for contributor in contributors:
			lastname = contributor.lastName
			firstname = contributor.firstName
			middlename = contributor.middleName
			
			author = lastname
			if firstname or middlename:
				author += ', '
				if firstname:
					author += firstname[0] + '.'
				if middlename:
					author += middlename[0] + '.'
			add (author)
		return ', '.join (authors)

	def getAuthors (self):
		"""
		return authors as string (R.U. Jones, A.U. Smith)
		build the string from a list of ContributorPeople
		"""
		contributors = self.payload.getContributorPeople('Author')
		authors = [];add=authors.append
		
		for contributor in contributors:
			lastname = contributor.lastName
			firstname = contributor.firstName
			middlename = contributor.middleName
			
			author = ''
			if firstname or middlename:
				if firstname:
					author += firstname[0] + '.'
				if middlename:
					author += middlename[0] + '.'
			author += " " + lastname
			add (author)
		return ', '.join (authors)

class OsmReportSearcher (ReportSearcher):
	"""
	for each submitter, display the # of sumissions between 2010-8-16 and 2010-10-31
	"""

	searchResult_constructor = OsmReportResult
	verbose = 0
	numToFetch = 20

	def __init__ (self, propsFile):
		if self.verbose:
			print 'OsmReportSearcher INIT'
			print ' - numToFetch', self.numToFetch
		ReportSearcher.__init__(self, propsFile)

class OsmReporter (Reporter):
	
	default_columns = ['recordID', 'collection', 'title', 'authors', 'pubName']
	searcher_class = OsmReportSearcher
	
		
if __name__ == '__main__':
	reporter = OsmReporter ('myprops.properties')
	print reporter.results[0]
	# reporter.writeTabDelimited()
	# print reporter.getTabDelimited()
