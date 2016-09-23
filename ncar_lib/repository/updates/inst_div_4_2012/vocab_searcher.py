"""

Search NLDR for occurances of selected vocab terms.

in the case of inst_div, we are talking about more than one field ...

- /record/contributors/person/affiliation/instDivision
- /record/contributors/organization/affiliation/instDivision

/key//record/contributors/organization/affiliation/instDivision:"Advanced Study Program (ASP)"

"""

import os, sys
from ncar_lib.repository import RepositorySearcher, OsmSearchResult

class VocabSearcher (RepositorySearcher) :
	
	numToFetch = 2000
	batchSize = 200
	searchResult_constructor = OsmSearchResult
	filter_predicate = None
	verbose = False
	default_baseUrl = "http://localhost:8080/schemedit/services/ddsws1-1"
	
	def __init__ (self, field=None, value=None, collection=None):
		"""
		field - xpath (e.g., /record/contributors/organization/affiliation/instDivision)
		value - the vocab value (e.g., "Advanced Study Program (ASP)"
		"""
		print "VocabSearcher"
		if not field and value:
			raise Exepction, "Vocab Searcher requires field and value params"
		
		self.field = field
		self.value = value
		
		RepositorySearcher.__init__ (self, collection)
		
		
	def get_params (self, collection, xmlFormat):
		"""
		define the params used to query the search service
		"""
		
		query = '/key//%s:"%s"' % (self.field, self.value)
		
		return {
			"q" : query,
			"verb": "Search",
			"xmlFormat": 'osm'
			# "storedContent":['dcsstatus', 'dcsstatusNote', 'dcsisValid']
			}
		
if __name__ == '__main__':
	field = '/record/contributors/person/affiliation/instDivision'
	# value = 'Advanced Study Program (ASP)'
	
	value = ':'.join([
		'University Corporation For Atmospheric Research (UCAR)',
		'National Center for Atmospheric Research (NCAR)',
		'High Altitude Observatory (HAO)'
	])
	
	print "value: " + value
	
	searcher = VocabSearcher(field, value)
	
	print 'searcher found %d results' % len (searcher)
	for result in searcher:
		print result.recId
	
