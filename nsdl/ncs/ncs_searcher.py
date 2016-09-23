"""
find collections managed in the NCS for which the NDR metadata object UniqueID property is different
from the NCS ID.

update the UniqueID in the NDR Metadata Objects for the items in these collections to match the NCS ID
"""
import os, sys
from ncar_lib.repository import RepositorySearcher, SearchResult

default_baseUrl = "http://ncs.nsdl.org/mgr/services/ddsws1-1"

class NCSSearchResult (SearchResult):

	def __init__ (self, element, payload_constructor=None):
		SearchResult.__init__ (self, element, payload_constructor)
		self.ndrHandle = self.storedContent.get('dcsndrHandle')
		
	def report(self):
		print self.recId, self.collection, self.ndrHandle
		# self.storedContent.report()
		# print self.payload
	
class NCSSearcher (RepositorySearcher):

	numToFetch = 2
	batchSize = 200
	searchResult_constructor = NCSSearchResult
	filter_predicate = None
	verbose = True
	
	def __init__ (self, collection, baseUrl=default_baseUrl):
		RepositorySearcher.__init__ (self, collection=collection, baseUrl=default_baseUrl)
	
	def get_params (self, collection, xmlFormat):
		"""
		define the params used to query the search service
		"""
		return {
			"verb": "Search",
			"ky": collection,
			"storedContent":['dcsstatus', 'dcsstatusNote', 'dcsisValid', 'dcsndrHandle']
			}
			
			
if __name__ == '__main__':
	colkey = '1200091746382'
	searcher = NCSSearcher (collection=colkey)
	print 'searcher found %d results' % len(searcher)
	for result in searcher:
		result.report()
