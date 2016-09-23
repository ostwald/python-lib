"""
title searcher uses DDS search to find all records having a particular title
"""
import sys, os
from UserList import UserList
from ncar_lib.repository import SearchResult, OsmSearchResult
from serviceclient import ServiceClient, URL
from JloXml import XmlRecord, XmlUtils 

default_baseUrl = "http://nldr.library.ucar.edu/schemedit/services/ddsws1-1"

class TitleSearcher (UserList):
	"""
	- get_params() - params used by DDS Search service to grab search results
	  search_results are constructed using searchResult_constructor
	- filterResults() is called on initial set of results, allowing subclasses
	  to work with a subset of results returned by search
	- processResults() hook to operate over results (after filtering)
	"""

	numToFetch = 2000
	batchSize = 200
	searchResult_constructor = OsmSearchResult
	filter_predicate = None
	verbose = True
	
	def __init__ (self, title, collections=None, baseUrl=default_baseUrl):
		UserList.__init__ (self)
		self.title = title
		self.params = self.get_params()
		self.service_client = ServiceClient (baseUrl)
		self.data = self.getResults ()
		
		# self.filterResults()
		# self.processResults()
			
	def get_params (self):
		"""
		define the params used to query the search service
		"""
		return {
			'verb': 'Search',
			's':'0',
			'n':'200',
			'xmlFormat': 'osm',
			'q':'/key//record/general/title:"%s"' % self.title,
			## 'ky': collection,
			'storedContent':['dcsstatus', 'dcsstatusNote', 'dcsisValid']
			}
		
	def filterResults(self):
		"""
		self.filter_predicate is applied to each results. 
		
			filter_predicate(result) -> true|false
		
		when the predicate returns false, the result is omitted from the result list.
		I.e., only results that satisfy predicate are kept
		"""
		if self.filter_predicate:
			fn = self.filter_predicate
			self.data = filter (lambda rslt:fn(rslt), self.data)
		
	def processResults (self):
		"""
		concrete classes should override this method to do some real processing
		"""
		if self.verbose:
			print "processResults"
			print "there are %d records to process" % len (self)
		
	def getResults (self):
		"""
		get a batch of search results via web service
		returns a list of self.searchResult_constructor instances
		"""
		client = self.service_client
		request = client.setRequest (self.params)
		#print request.report()
		response = client.getResponse()
		if response.hasError():
			raise response.error
		
		responseDoc = response.doc
			
		responseDoc.xpath_delimiter = ":"
		
		recordPath = "DDSWebService:Search:results:record"
		return map (self.searchResult_constructor, responseDoc.selectNodes(responseDoc.dom, recordPath))
		
	def report (self):
		for result in self:
			print '---------------------------------'
			print result.payload
			
	
if __name__ == '__main__':
	title = "A call to action for coral reefs"
	results = TitleSearcher(title)
	print '%d results found' % len(results)
	results.report()

