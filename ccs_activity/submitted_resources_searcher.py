import os, sys, re
from ncar_lib.repository import RepositorySearcher, SearchResult
from JloXml import AdnRecord, XmlUtils
		
ddswsBaseUrlForUserContent = "http://acorn.dls.ucar.edu:17248/dds/services/ddsws1-1"

class SubmittedResourceResult (SearchResult):
	
	"""
	in addition to fields exposed by SearchResult, exposes:
		- pubName
		- pubNameType
		- payload (ADN instance)
	"""
	default_payload_constructor = AdnRecord
	
	def __init__ (self, element, payload_constructor=None):
		SearchResult.__init__ (self, element, payload_constructor)
		self.created = self.payload.getCreated()
		self.modified = self.payload.getModified()
		
	def __repr__ (self):
		# return "%s (%s) created: %s modified: %s" % (self.recId, self.collection, self.created, self.modified)
		return "%s - modified: %s" % (self.recId, self.modified)

class SubmittedResourceSearcher (RepositorySearcher):
	
	default_baseUrl = ddswsBaseUrlForUserContent
	searchResult_constructor = SubmittedResourceResult
	
	verbose=True
	numToFetch=100
	
	def __init__ (self):
		collection = 'ccsusersubmittedresources'
		xmlFormat = 'adn'
		self.get_params = self.get_filtered
		RepositorySearcher.__init__ (self, collection=collection, xmlFormat=xmlFormat, baseUrl=self.default_baseUrl)
		# print self.service_client.request.getUrl()
		
	def get_filtered(self, collection, xmlFormat):
		"""
		define the params used to query the search service
		
		/text//itemRecord/metaMetadata/dateInfo/@created
		/text//itemRecord/metaMetadata/dateInfo/@lastModified
		
		"""
		start = "2012-05-01T00:00:00Z"
		end = "2012-05-20T00:00:00Z"
		query = '/text//itemRecord/metaMetadata/dateInfo/@lastModified:[%s TO %s]' % (start, end)
		
		return {
			'q' : query,
			"verb": "Search",
			"xmlFormat": xmlFormat,
			"ky": collection,
			'sortDescending' : '/text//itemRecord/metaMetadata/dateInfo/@lastModified'
			}
			
	def get_sorted(self, collection, xmlFormat):
		"""
		define the params used to query the search service
		
		sortAscendingBy
		
		# 'sortDescending' : '/text//annotationRecord/service/date/@modified',
		"""
		return {
			"verb": "Search",
			"xmlFormat": xmlFormat,
			'sortDescending' : '/text//itemRecord/metaMetadata/dateInfo/@lastModified',
			"ky": collection
			}
			
		
	# def filter_predicate (self, result):
		# return result.collection == 'ccsprivateannos'
			
if __name__ == '__main__':
	searcher = SubmittedResourceSearcher()
	for result in searcher:
		print result
