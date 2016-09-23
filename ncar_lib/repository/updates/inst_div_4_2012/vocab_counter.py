"""

Search NLDR for occurances of selected vocab terms.

in the case of inst_div, we are talking about more than one field ...

- /record/contributors/person/affiliation/instDivision
- /record/contributors/organization/affiliation/instDivision

/key//record/contributors/organization/affiliation/instDivision:"Advanced Study Program (ASP)"

"""

import os, sys
from ncar_lib.repository import SummarySearcher, OsmSearchResult

class VocabCounter (SummarySearcher) :
	
	local_BaseUrl = "http://localhost:8080/schemedit/services/ddsws1-1"
	verbose = False
	
	def __init__ (self, field=None, value=None, collection=None):
		"""
		field - xpath (e.g., /record/contributors/organization/affiliation/instDivision)
		value - the vocab value (e.g., "Advanced Study Program (ASP)"
		"""
		if self.verbose:
			print "VocabCounter"
		if not field and value:
			raise Exepction, "Vocab Searcher requires field and value params"
		
		self.field = field
		self.value = value
		
		SummarySearcher.__init__ (self, collection, baseUrl=self.local_BaseUrl)
		self.numRecords = self.summary.totalNumResults
		
	def get_params (self, collection, xmlFormat):
		"""
		define the params used to query the search service
		"""
		
		query = '/key/%s:"%s"' % (self.field, self.value)
		
		return {
			"q" : query,
			"verb": "Search",
			"xmlFormat": 'osm',
			"ky": collection,
			"storedContent":['dcsstatus', 'dcsstatusNote', 'dcsisValid']
			}
		
if __name__ == '__main__':
	person_field = '/record/contributors/person/affiliation/instDivision'
	org_field = '/record/contributors/organization/affiliation/instDivision'
	# value = 'Advanced Study Program (ASP)'
	value = ':'.join([
		'University Corporation For Atmospheric Research (UCAR)',
		'National Center for Atmospheric Research (NCAR)',
			'High Altitude Observatory (HAO)'
			])
	
	print "value: " + value
			
	counter = VocabCounter(person_field, value)
	
	print 'counter found %d results' % counter.numRecords
	
