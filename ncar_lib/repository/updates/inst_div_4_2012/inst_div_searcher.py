"""

Search NLDR for occurances of selected vocab terms.

in the case of inst_div, we are talking about more than one field ...

- /record/contributors/person/affiliation/instDivision
- /record/contributors/organization/affiliation/instDivision

/key//record/contributors/organization/affiliation/instDivision:"Advanced Study Program (ASP)"

"""

import os, sys
from ncar_lib.repository import RepositorySearcher, OsmSearchResult


class InstDivSearcher (RepositorySearcher) :
	
	numToFetch = 2000
	batchSize = 200
	searchResult_constructor = OsmSearchResult
	filter_predicate = None
	verbose = False
	# default_baseUrl = "http://localhost:8080/schemedit/services/ddsws1-1"
	default_baseUrl = "http://nldr.library.ucar.edu/schemedit/services/ddsws1-1"
	
	def __init__ (self, value=None, collection=None, baseUrl=None):
		"""
		value - the vocab value (e.g., "Advanced Study Program (ASP)"
		"""
		self.collection = collection
		
		if self.verbose:
			print "InstDivSearcher"
		if not value:
			raise Exepction, "Vocab Searcher requires field and value params"
		
		self.value = value
		
		RepositorySearcher.__init__ (self, self.collection, baseUrl=baseUrl)
		
		
	def get_params (self, collection, xmlFormat):
		"""
		define the params used to query the search service
		"""
		person_path = 'record/contributors/person/affiliation/instDivision'
		org_path = 'record/contributors/organization/affiliation/instDivision'
		
		query = '/key//%s:"%s" OR /key//%s:"%s"' % (person_path, self.value,
												  org_path, self.value)
		
		# org_query = '/key//%s:"%s"' % (org_path, self.value)
		# query = org_query
		
		if self.verbose:
			print 'query', query
		
		return {
			"q" : query,
			"ky" : self.collection,
			"verb": "Search",
			"xmlFormat": 'osm'
			# "storedContent":['dcsstatus', 'dcsstatusNote', 'dcsisValid']
		}
		
if __name__ == '__main__':
	field = '/record/contributors/person/affiliation/instDivision'
	value = 'Research Aviation Facility (RAF)'
	
	valueOFF = ':'.join([
		'University Corporation For Atmospheric Research (UCAR)',
		'National Center for Atmospheric Research (NCAR)',
		'High Altitude Observatory (HAO)'
	])
	
	print "value: " + value
	
	searcher = InstDivSearcher(value)
	
	print 'searcher found %d results' % len (searcher)
	for result in searcher:
		print result.recId
	
