"""
Goal: find all refs in OpenSky (NCAR Library DCS) that a particular person (e.g., "Phil Judge") has contributed to

produce a report of the following fields: record #, title, collection, and status. 
sorted on title (but of course, this could be done in spreadsheet).

Challenge: we have to look across both 'osm' and 'citation' frameworks (any others?).

Approach: start with repository.
- search for all records with an author with same LASTNAME

categories of matches (in order of trustworthiness):
	- matching upid number
	- Matching lastname, firstinitial, lastinitial
	- matching lastname
"""


import codecs, os, sys
from ncar_lib import OsmSearchResult
from author_search_globals import *
from authorSearchResult import AuthorSearchResult, MetadataAuthor
from authorSearcher import AuthorSearcher, ReporterMixin
from author import Author


"""
Use search service to retrieve a batch of records and then process them
"""

class OsmAuthorSearchResult (AuthorSearchResult):
	"""
	AuthorSearchResult specialized for the OSM framework
	- searchResult is a OsmSearchResult
	
	in addition to attributes exposed in AuthorSearchResult, exposes
	- self.recordDate
	- self.publistedDate
	"""
	def __init__ (self, searchResult, Author):
		AuthorSearchResult.__init__ (self, searchResult, Author)
		self.recordDate = searchResult.payload.getRecordDate()
		self.publishedDate = searchResult.payload.getPubDate ()
		
	def getMatchingPerson (self):
		"""
		find the person from the osmRecord that matched the lastName of 
		the Author used for search
		"""
		matches = []
		people = self.searchResult.payload.getContributorPeople() 
		for person in people:
			if person.lastName == self.author.lastname:
				matches.append(person)
				
		if len(matches) > 1:
			try:
				return self.getBestMatch(matches)
			except:
				# if there are no first name matches, then just return one of the matches
				# print sys.exc_info()[1]
				pass
			# raise Exception, 'more than one lastname match found for %s' % self.searchResult.recId
		return matches[0]
		
	def getBestMatch (self, matches):
		"""
		we know the last names match
		"""
		firstnameMatches = []
		for person in matches:
			if person.firstName and person.firstName[0] == self.author.first:
				firstnameMatches.append (person)
		if len(firstnameMatches) != 1:
			raise Exception, "%d firstNameMatches for %s" % (len(firstnameMatches), self.searchResult.recId)
		return firstnameMatches[0]
		
	def getMetadataAuthor (self):
		"""
		we are extracting fields from a osmRecord.ContributorPerson
		"""
		mp = self.getMatchingPerson ()
		return MetadataAuthor (mp.lastName, mp.firstName, mp.middleName, mp.upid)
		
class OsmAuthorSearcher (AuthorSearcher):

	"""
	for each submitter, display the # of sumissions between 2010-8-16 and 2010-10-31
	"""

	numToFetch = 2000
	searchResult_constructor = OsmSearchResult
	verbose = True
	authorSearchResult_class = OsmAuthorSearchResult
			
	def get_params (self, collection, xmlFormat):
		"""
		define the params used to query the search service
		"""
		return {
			"verb": "Search",
			"xmlFormat": xmlFormat or None,
			"storedContent":['dcsstatus', 'dcsstatusNote', 'dcsisValid', 'dcsosmFiscalYear'],
			'q': '/key//record/contributors/person/lastName:"%s"' % self.author.lastname
			}
	
class OsmAuthorReporter (OsmAuthorSearcher, ReporterMixin):
	pass

if __name__ == '__main__':
	
	reporter = OsmAuthorReporter(Author ('Smith', 'Anne', upid='14678'))
	reporter.summarize()
	for result in reporter.results:
		#  result.report()
		pass
	reporter.writeTabDelimited(None, "TEST-REPORT.txt")
	# reporter.writeReports()



