
"""
Use search service to do a query and summarize results (without fetching matches)
"""

from UserDict import UserDict
from serviceclient import ServiceClient, URL
from dds_search_result import SearchResult
from JloXml import XmlRecord, XmlUtils, MetaDataRecord

default_baseUrl = "http://nldr.library.ucar.edu/schemedit/services/ddsws1-1"

class Facet:
	"""
	structure holding two attrs
	- term
	- count
	"""
	def __init__ (self, term, count):
		self.term = term
		self.count = count

class FacetedField (UserDict):
	"""
	a mapping from vocab terms to 'count', the number of term 
	occurrances in the repository
	
	facets - a list of Facet Instances
	data - a mapping from term to count
	
	element param contains a "category" element, which in turn
	holds the facet "results"
	the Facet instances are added one at a time, created from the 'result' elements
	"""
	verbose = 0
	
	def __init__ (self, element=None):
		"""
		facet[term] returns the record count for that term
		countMap provided reverse mapping - count -> terms having that count
		"""
		self.data = {}
		self.countMap = UserDict()  # e.g., 5 -> "my term"
		self.facets = []
		self.facetMap = UserDict()
		self.name = None
		
		## termNodes = XmlUtils.getChildElements(element)

		if element is not None:
			self.process_element(element)
			
	def process_element(self, element):
		self.name = element.getAttribute("name")
		
		termNodes = XmlUtils.selectNodes(element, 'term')
		if self.verbose:
			print "%s (%d terms)" % (self.name, len(termNodes))

		for node in termNodes:
			term = XmlUtils.getText (node)
			count = int (node.getAttribute("count"))
		
			self.add (term, count)
		if self.verbose:
			print '%d facets read' % len(self)

		
	def add (self, term, count):
		"""
		add this term if it is not yet in the mapping, and
		increment it's count
		"""
		self[term] = count
		facet = Facet (term, count)
		self.facets.append(facet)
		self.facetMap[term] = facet
		# add term to countMap
		terms = []
		if self.countMap.has_key(count):
			terms = self.countMap[count]
		terms.append (term)
		self.countMap[count] = terms
		
	def getCount (self, term):
		"""
		return the count for provided term
		"""
		return self[term]
		
	def getTermsForCount (self, count=None):
		"""
		get the terms having specific "count" (i.e., all the terms that have the
		given number of counts)
		"""
		return self.countMap[count]
		
	def getFacet (self, term):
		if self.facetMap.has_key(term):
			return self.facetMap[term]
		return None
		
	def getTerms (self):
		"""
		get all the terms in this facet
		"""
		return self.keys()
		
	def term_cmp (self, x, y):
		"""
		terms are compared by their lower case versions
		"""
		return cmp(x.lower(), y.lower())
		
	def keys (self):
		sorted = self.data.keys()
		sorted.sort(self.term_cmp)
		# sorted.sort(lambda x,y:cmp(x.lower(), y.lower()))
		return sorted
		
	def report (self, verbose=0):
		
		# print '%d total facets' % (len(self))
		notEmptyFacets = filter (lambda x:self[x] > 0, self.keys())
		print '\n%d facets for %s' % (len(notEmptyFacets), self.category)
		if verbose:
			for term in notEmptyFacets:
				if self[term] > 0:
					print ' - %s (%d)' % (term, self[term])

class FacetCategory (FacetedField):
	
	def process_element(self, element):
		self.category = element.getAttribute("category")
		
		termNodes = XmlUtils.selectNodes(element, 'result')
		if self.verbose:
			print "%s (%d terms)" % (self.category, len(termNodes))

		for node in termNodes:
			term = node.getAttribute("path")
			count = int (node.getAttribute("count").replace(',', ''))
		
			self.add (term, count)
		if self.verbose:
			print '%d facets read' % len(self)

class SummaryResult (MetaDataRecord):
	"""
	parses the ResponseDoc from a SummarySearcher
	
	exposes
	- totalNumResults
	- faceted_fields (a list of FacetedField instances, one per faceted field in the request). usually
	there will only be one faceted_field
	"""
	verbose = True
	xpath_delimiter = "/"
	
	def __init__ (self, responseDoc):
		XmlRecord.__init__ (self, xml=responseDoc.doc.toxml())
		self.totalNumResults = self.get_num_records()
		if self.verbose:
			print "total NumResults: %s" % self.totalNumResults
		self.faceted_fields = self.read_faceted_fields()
		
	def get_num_records (self):
		"""
		determine the total number of records that match the search request
		"""
		totalNumResults = self.getTextAtPath ('DDSWebService/Search/resultInfo/totalNumResults')
		# print "%s (%s)" % (totalNumResults, type(totalNumResults))
		if totalNumResults is None:
			return 0
		else:
			return int(totalNumResults)
		
	def read_faceted_fields (self):
		# faceted_fields = []
		print "READING"
		facetFieldEls = self.selectNodes(self.dom, 'DDSWebService/Search/facetFields/field')
		if facetFieldEls:
			print 'making FacetedFields'
			return map (FacetedField, facetFieldEls)
			
		facetCategoryEls = self.selectNodes(self.dom, 'DDSWebService/Search/facetResults/facetResult')
		if facetCategoryEls:
			print 'making FacetCategories'
			return map (FacetCategory, facetCategoryEls)
		
		# for el in facetFieldEls:
			# faceted_fields.append (FacetedField (el))
			# 
		# if self.verbose:
			# print "%d facet fields initialzed" % len(faceted_fields)
		# return faceted_fields
	
	def getFacetedField (self, category):
		for field in self.faceted_fields:
			if field.category == category:
				return field

class SummarySearcher (UserDict):
	"""
	- get_params() - specifies DDS Search service to grab search results
	- only the summary information is parsed - see SummaryResult
	"""
	
	verbose = False
	
	def __init__ (self, collection=None, xmlFormat=None, baseUrl=default_baseUrl):
		UserDict.__init__ (self)
		
		self.params = self.get_params(collection, xmlFormat)
		self.service_client = ServiceClient (baseUrl)
		self.responseDoc = self.get_response_doc()
		self.responseDoc.xpath_delimiter = "/"
		print "CALLING SummaryResult"
		self.summary = SummaryResult (self.responseDoc)
		if self.verbose:
			print "%d total records" % self.summary.totalNumResults
		
	def get_summary (self):
		"""
		extract summary information from the responseDoc
		"""
		pass
			
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
			
	def get_response_doc (self):
		client = self.service_client
		self.params.update ({'s':'0', 'n':'1'})
		request = client.setRequest (self.params)
		if self.verbose:
			print request.report()
		response = client.getResponse()
		if response.hasError():
			raise Exception, response.error
		
		else:
			# print response.doc
			return response.doc
			
	
if __name__ == '__main__':
	xmlFormat = 'osm'
	collection = 'osgc'
	searcher = SummarySearcher(collection, xmlFormat)
	print '%d results' % searcher.summary.totalNumResults
	## summary = searcher.summary
	

	

