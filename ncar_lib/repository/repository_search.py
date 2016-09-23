"""
Use search service to retrieve a batch of records and then process them
"""
import time
from UserList import UserList
from serviceclient import ServiceClient, URL, ServiceError
from dds_search_result import SearchResult
from JloXml import XmlRecord, XmlUtils

class NoMatchingRecordsException (Exception):
	pass

class RepositorySearcher (UserList):
	"""
	- get_params() - specifies DDS Search service to grab search results
	  search_results are constructed using searchResult_constructor
	- filterResults() is called on initial set of results, allowing subclasses
	  to work with a subset of results returned by search
	- processResults() hook to operate over results (after filtering)
	"""

	default_baseUrl = "http://nldr.library.ucar.edu/schemedit/services/ddsws1-1"
	numToFetch = 20000
	batchSize = 200
	searchResult_constructor = SearchResult
	filter_predicate = None
	verbose = True
	delay = None
	
	def __init__ (self, collection=None, xmlFormat=None, baseUrl=None):
		UserList.__init__ (self)
		baseUrl = baseUrl or self.default_baseUrl
		if self.verbose:
			print 'baseUrl:', baseUrl
		self.timing = {}
		self.params = self.get_params(collection, xmlFormat)
		self.service_client = ServiceClient (baseUrl)
		self.numRecords = self._get_num_records()
		if self.verbose:
			print "%d total records" % self.numRecords
		s = 0
		numToGet = min (self.numToFetch, self.numRecords)
		
		tics = time.time()
		self.getResults (numToGet)
		self.timing['download'] = time.time() - tics
		
		self.numFetched = len(self)
		
		tics = time.time()
		self.filterResults()
		self.timing['filter'] = time.time() - tics
		
		tics = time.time()
		self.processResults()
		self.timing['processing'] = time.time() - tics
			
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
		
	def filterResults(self):
		"""
		self.filter_predicate is applied to each results, and the data for this searcher
			is replaced with the filtered set.
		
			filter_predicate(result) -> true|false
		
		when the predicate returns false, the result is omitted from the result list.
		I.e., only results that satisfy predicate are kept
		"""
		if self.filter_predicate:
			if self.verbose:
				print "filtering from %d records" % len(self)
			fn = self.filter_predicate
			self.data = filter (lambda rslt:fn(rslt), self.data)
		
	def processResults (self):
		"""
		concrete classes should override this method to do some real processing
		"""
		if 0 and self.verbose:
			print "ProcessRecs"
			print "there are %d records to process" % len (self)
		
	def getResults (self, numToGet):
		"""
		do as many requests (size determined by numToGet) as necessary
		to get all records, or self.numRecords, whichever is smaller.
		
		search hits are stored in self.data
		"""
		s = 0
		results = []
		# print "getting %d of %d records" % (numToGet, self.numRecords)
		while s < numToGet:
			thisBatch = min (self.batchSize, numToGet - len(results))
			results = self.get_result_batch (s, thisBatch)
			if self.delay:
				if self.verbose:
					print " ... delaying for %d seconds" % self.delay
				time.sleep (self.delay)
			map (self.append, results)
			if self.verbose:
				print " ... %d results" % len (self)
			s = s + self.batchSize
		return results
		
	def _get_num_records (self):
		"""
		determine the total number of records that match the search request
		"""
		try:
			doc = self.get_response_doc (0,1)
		except NoMatchingRecordsException, msg:
			return 0
		doc.xpath_delimiter = ":"
		totalNumResults = doc.getTextAtPath ('DDSWebService:Search:resultInfo:totalNumResults')
		# print "%s (%s)" % (totalNumResults, type(totalNumResults))
		if totalNumResults is None:
			return 0
		else:
			return int(totalNumResults)
	
	def get_response_doc (self, start, num):
		client = self.service_client
		self.params.update ({"s":str(start), "n":str(num)})
		request = client.setRequest (self.params)
		if self.verbose:
			print request.getUrl()
		response = client.getResponse()
		# print response.doc
		
		if response.hasError():
			# ignore empty record responses
			error = response.error
			# print 'ERROR: %s (%s)' % (type(error), error.__class__.__name__)
			if isinstance(error, ServiceError): 
				error = str(error)
			# print 'MESSAGE',error
			if error.find('had no matching records') != -1:
				raise NoMatchingRecordsException, 'no matching records'
			else:
				raise Exception, 'WebService Error: %s' % error
		
		else:
			return response.doc
			
	def get_result_batch (self, start, num):
		"""
		get a batch of search results via web service
		returns a list of self.searchResult_constructor instances
		"""
		try:
			responseDoc = self.get_response_doc (start, num)
		except NoMatchingRecordsException, msg:
			return []
		
		responseDoc.xpath_delimiter = ":"
		
		# print "searchResult_constructor:", self.searchResult_constructor.__name__
		return map (self.searchResult_constructor, 
				    responseDoc.selectNodes(responseDoc.dom, "DDSWebService:Search:results:record"))
			
		
	def showParams (self):
		print '\nParams:'
		for key in self.params:
			if key in ['n','s']: continue
			print '  %s: %s' % (key, self.params[key])
	
if __name__ == '__main__':
	xmlFormat = 'osm'
	collection = 'osgc'
	results = RepositorySearcher(collection, xmlFormat)
	for result in results:
		# result.storedContent.report()
		result.report()

