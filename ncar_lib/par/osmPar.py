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
from par_globals import *
from parResult import ParResult, MetadataAuthor
from parReport import ParReport


"""
Use search service to retrieve a batch of records and then process them
"""

class OsmParResult (ParResult):
	"""
	ParResult specialized for the OSM framework
	- searchResult is a OsmSearchResult
	
	in addition to attributes exposed in ParResult, exposes
	- self.recordDate
	- self.publistedDate
	"""
	def __init__ (self, searchResult, parAuthor):
		ParResult.__init__ (self, searchResult, parAuthor)
		self.recordDate = searchResult.payload.getRecordDate()
		self.publishedDate = searchResult.payload.getPubDate ()
		
	def getMatchingPerson (self):
		"""
		find the person from the osmRecord that matched the lastName of 
		the ParAuthor used for search
		"""
		matches = []
		people = self.searchResult.payload.getContributorPeople() 
		for person in people:
			if person.lastName == self.parAuthor.lastname:
				matches.append(person)
				
		if len(matches) > 1:
			try:
				return self.getBestMatch(matches)
			except:
				# if there are no first name matches, then just return one of the matches
				print sys.exc_info()[1]
			# raise Exception, 'more than one lastname match found for %s' % self.searchResult.recId
		return matches[0]
		
	def getBestMatch (self, matches):
		"""
		we know the last names match
		"""
		firstnameMatches = []
		for person in matches:
			if person.firstName and person.firstName[0] == self.parAuthor.first:
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
		
class OsmParReport (ParReport):
	"""
	for each submitter, display the # of sumissions between 2010-8-16 and 2010-10-31
	"""

	numToFetch = 2000
	searchResult_constructor = OsmSearchResult
	verbose = True
	parResult_class = OsmParResult
			
	def get_params (self, collection, xmlFormat):
		"""
		define the params used to query the search service
		"""
		return {
			"verb": "Search",
			"xmlFormat": xmlFormat or None,
			"storedContent":['dcsstatus', 'dcsstatusNote', 'dcsisValid'],
			'q': '/key//record/contributors/person/lastName:"%s"' % self.parAuthor.lastname
			}
		

if __name__ == '__main__':
	
	reporter = OsmParReport(ParAuthor ('Smith', 'Anne', upid='14678'))
	reporter.summarize()
	# report.reportRejects()
	# reporter.writeTabDelimited("TEST-REPORT.txt")
	# reporter.writeReports()



