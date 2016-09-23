"""
1 - get user names
2 - get all records involving users
-- what formats??
3 - (eventually) change usernames in all records
"""
import sys, os
from ncar_lib.repository import RepositorySearcher, SearchResult

class RecordsForUserSearcher (RepositorySearcher):

	default_baseUrl = "http://localhost:7248/dds/services/ddsws1-1"
	numToFetch = 2000
	batchSize = 200
	searchResult_constructor = SearchResult
	filter_predicate = None
	verbose = False
	
	def __init__ (self, username):
		self.username = username
		RepositorySearcher.__init__ (self)
	
	def get_params (self, collection, xmlFormat):
		"""
		define the params used to query the search service
		"""
		return {
			"verb": "Search",
			# "q" : self.username
			"q" : '%s OR /text//annotationRecord/annotation/contributors/contributor/person/nameLast:"%s"' %
						(self.username, self.username)
			}
			
	def getFormats (self):
		return map (lambda x:x.xmlFormat, self)
		
if __name__ == '__main__':
	user = "flores"
	searcher = RecordsForUserSearcher(user)
	print '%d results found for %s' % (len(searcher), user)
	print searcher.getFormats()
