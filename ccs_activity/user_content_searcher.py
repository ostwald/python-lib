import os, sys, re
from ncar_lib.repository import RepositorySearcher, SearchResult
from JloXml import MetaDataRecord, XmlUtils

ddswsBaseUrlForUserContent = "http://acorn.dls.ucar.edu:17248/dds/services/ddsws1-1"
purgBaseUrlForUserContent = "http://localhost:8070/dds/services/ddsws1-1"
ccsDevDDS = "http://acorn.dls.ucar.edu:17248/dds/services/ddsws1-1"

class DleseAnnoRecord (MetaDataRecord):

	xpath_delimiter = '/'
	
	id_path = 'annotationRecord/service/recordID'
	
	xpaths = {
		'id' : 'annotationRecord/service/recordID',
		'createdDate' : 'annotationRecord/service/date/@created',
		'modifiedDate' : 'annotationRecord/service/date/@modified'
	}
	
	# defined by schema but unfortunately hard-coded here
	root_child_order = [
		'service',
		'itemID',
		'annotation',
		'moreInfo'
	]
	
	
	def __init__ (self, path=None, xml=None):
		MetaDataRecord.__init__ (self, path=path, xml=xml)

	def getCreated (self):
		return self.get ('createdDate')
		
	def getModified(self):
		return self.get ('modifiedDate')
		
class UserContentResult (SearchResult):
	
	"""
	in addition to fields exposed by SearchResult, exposes:
		- pubName
		- pubNameType
		- payload (OsmRecord instance)
	"""
	default_payload_constructor = DleseAnnoRecord
	
	def __init__ (self, element, payload_constructor=None):
		SearchResult.__init__ (self, element, payload_constructor)
		self.created = self.payload.getCreated()
		self.modified = self.payload.getModified()
		
	def __repr__OFF (self):
		# return "%s (%s) created: %s modified: %s" % (self.recId, self.collection, self.created, self.modified)
		return "%s - modified: %s" % (self.recId, self.modified)

class UserContentSearcher (RepositorySearcher):
	
	default_baseUrl = purgBaseUrlForUserContent
	searchResult_constructor = UserContentResult
	
	verbose=True
	numToFetch=100
	
	def __init__ (self):
		collection = 'ccsprivateannos'
		xmlFormat = 'dlese_anno'
		self.get_params = self.get_filtered
		RepositorySearcher.__init__ (self, collection=collection, xmlFormat=xmlFormat, baseUrl=self.default_baseUrl)
		# print self.service_client.request.getUrl()
		
	def get_filtered(self, collection, xmlFormat):
		"""
		define the params used to query the search service
		"""
		start = "2012-05-01T00:00:00Z"
		end = "2012-05-20T00:00:00Z"
		query = '/text//annotationRecord/service/date/@modified:[%s TO %s]' % (start, end)
		
		return {
			'q' : query,
			"verb": "Search",
			"xmlFormat": xmlFormat,
			"ky": collection,
			'sortDescending' : '/text//annotationRecord/service/date/@modified'
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
			'sortDescending' : '/text//annotationRecord/service/date/@modified',
			"ky": collection
			}
			
		
	def filter_predicate (self, result):
		return result.collection == 'ccsprivateannos'
			
if __name__ == '__main__':
	searcher = UserContentSearcher()
	for result in searcher:
		print result
