from UserList import UserList
from UserDict import UserDict
from serviceclient import ServiceClient, URL
from JloXml import XmlRecord, XmlUtils
from ncar_lib import RepositorySearcher, OsmSearchResult, unionDateToSecs


"""
Use search service to retrieve a batch of records and then process them
"""

default_baseUrl = "http://nldr.library.ucar.edu/schemedit/services/ddsws1-1"

start_secs = unionDateToSecs ("2010-08-16")
end_secs = unionDateToSecs ("2010-11-1")

def submitterFilter (None, result):
	submitters = result.payload.getContributorPeople("Submitter")
	recordDate = unionDateToSecs(result.payload.getRecordDate())
	return submitters and start_secs <= recordDate and recordDate < end_secs

class Submission:
	
	def __init__ (self, contributor, recId, date):
		self.contributor = contributor
		self.recId = recId
		self.date = date
		self.timestamp = unionDateToSecs(date)
		
	def __cmp__ (self, other):
		return cmp (self.timestamp, other.timestamp)
		
	def __repr__ (self):
		return "%s - %s (%s)" % (self.contributor, self.date, self.recId)
	
class SubmissionMap (UserDict):
	
	def __init__(self):
		UserDict.__init__(self)

	def keys(self):
		sorted = self.data.keys()
		sorted.sort()
		return sorted
		
	def add (self, submission):
		name = "%s, %s" % (submission.contributor.lastName, submission.contributor.firstName)
		value = self.has_key (name) and self[name] or []
		value.append (submission)
		self[name] = value
		
	def report (self, verbose=True):
		for key in self.keys():
			print "%s (%d)" % (key, len(self[key]))
			if verbose:
				items = self[key]
				items.sort()
				for item in items:
					print " - %s - %s" % (item.recId, item.date)
				
		
class SubmitterReport (RepositorySearcher):
	"""
	for each submitter, display the # of sumissions between 2010-8-16 and 2010-10-31
	"""

	numToFetch = 2000
	batchSize = 200
	searchResult_constructor = OsmSearchResult
	filter_predicate = submitterFilter
	verbose = True
	
	def __init__ (self, collection='osgc', xmlFormat='osm', baseUrl=default_baseUrl):
		self.submissionMap = SubmissionMap()
		RepositorySearcher.__init__(self, collection, xmlFormat, baseUrl)
			
	def get_params (self, collection, xmlFormat):
		"""
		define the params used to query the search service
		"""
		return {
			"verb": "Search",
			"xmlFormat": xmlFormat,
			"ky": collection,
			"storedContent":['dcsstatus', 'dcsstatusNote', 'dcsisValid']
			}
		
	def processResults (self):
		"""
		concrete classes should override this method to do some real processing
		"""
		print "ProcessRecs"
		print "there were %d records submitted between 2010-8-16 and 2010-10-31" % len (self)
		for result in self:
			date = result.payload.getRecordDate()
			recId = result.recId
			submitters = result.payload.getContributorPeople("Submitter")
			for contrib in submitters:
				self.submissionMap.add(Submission (contrib, recId, date))
		
	def report1 (self):
		submissions = self.submissionMap.values()
		submissions.sort() # by date
		for submission in self.submissions:
			print submission
			
	def report (self, verbose=0):
		self.submissionMap.report(verbose)
	
if __name__ == '__main__':

	SubmitterReport().report(False)


