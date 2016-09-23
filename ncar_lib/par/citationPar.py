"""
Goal: find all refs in OpenSky (NCAR Library DCS) that a particular person (e.g., "Phil Judge") has contributed to

produce a report of the following fields: record #, title, collection, and status. 
sorted on title (but of course, this could be done in spreadsheet).

Challenge: we have to look across both 'osm' and 'citation' frameworks (any others?).

Approach: start with repository.
"""

from ncar_lib.repository.dds_search_result import CitationSearchResult
from parResult import ParResult, MetadataAuthor
from par_globals import *
from parReport import ParReport

class CitationParResult (ParResult):
	"""
	ParResult specialized for the OSM framework.
	- searchResult is a CitationSearchResult
	"""
	def __init__ (self, searchResult, parAuthor):
		ParResult.__init__ (self, searchResult, parAuthor)
		self.recordDate = None # no such data in Citation
		self.publishedDate = searchResult.payload.get('year') 
		
	def getMatchingPerson (self):
		matches = []
		for person in self.searchResult.payload.getAuthors():
			if person.lastName == self.parAuthor.lastname:
				matches.append(person)
		if len(matches) > 1:
			raise Exception, 'more than one lastname match found for %s' % self.searchResult.recId
		return matches[0]
		
	def getMetadataAuthor (self):
		"""
		we are extracting fields from a list of CitationAuthors
		"""
		mp = self.getMatchingPerson ()
		return MetadataAuthor (mp.lastName, mp.firstName, mp.middleName)

class CitationParReport (ParReport):
	"""
	for each submitter, display the # of sumissions between 2010-8-16 and 2010-10-31
	"""

	numToFetch = 2000
	verbose = True
	
	searchResult_constructor = CitationSearchResult
	parResult_class = CitationParResult
	
			
	def get_params (self, collection, xmlFormat):
		"""
		define the params used to query the search service
		"""
		return {
			"verb": "Search",
			"xmlFormat": 'citation',
			"storedContent":['dcsstatus', 'dcsstatusNote', 'dcsisValid'],
			'q': '/key//record/authors/author/lastName:"%s"' % self.parAuthor.lastname
			}
	
if __name__ == '__main__':
	reporter = CitationParReport(TESTER)
	reporter.summarize()
	reporter.writeReports()
	for item in reporter.name_matches:
		# print item.asTabDelimited()
		print item.publishedDate


