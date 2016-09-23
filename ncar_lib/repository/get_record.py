"""
http://nldr.library.ucar.edu/schemedit/services/ddsws1-1?verb=GetRecord&id=PUBS-000-000-005-040
"""

import os, sys
from serviceclient import ServiceClient
from dds_search_result import SearchResult, OsmSearchResult
from JloXml import XmlRecord, XmlUtils

default_baseUrl = "http://nldr.library.ucar.edu/schemedit/services/ddsws1-1"

class GetRecord:
	"""

	"""

	response_constructor = OsmSearchResult
	debug = False
	
	def __init__ (self, recId, baseUrl=default_baseUrl):
		self.recId = recId
		self.params = self.get_params()
		self.service_client = ServiceClient (baseUrl)
		self.response = self.getResult()
			
	def get_params (self):
		"""
		define the params used to query the search service
		"""
		return {
			"verb": "GetRecord",
			"id": self.recId,
			"storedContent":['dcsstatus', 'dcsstatusNote', 'dcsisValid']
			}
	
	def getResult (self):
		responseDoc = self.get_response_doc()
		
		# print 'getResult:', responseDoc
		responseDoc.xpath_delimiter = ":"
			
		responseElement = responseDoc.selectSingleNode(responseDoc.dom, 'DDSWebService:GetRecord:record')
		# print responseElement.toxml()
		return self.response_constructor (responseElement)

			
	def get_response_doc (self):
		client = self.service_client
		request = client.setRequest (self.params)
		if self.debug:
			print request.report()
		response = client.getResponse()
		if self.debug:
			print response.doc
		if response.hasError():
			raise Exception, 'WebService Error: %s' % response.error
		
		else:
			return response.doc
	
if __name__ == '__main__':
	# recId = 'PUBS-000-000-005-040'
	recId = 'PUBS-NOT-FY2010-000-000-002-800'
	response = GetRecord(recId).response
	print response.recId
	pubsId = response.payload.getPubsId()
	if pubsId:
		print 'PubsID:', pubsId
	else:
		print response.payload
		print "WHERE IS PUBS ID??"
	


