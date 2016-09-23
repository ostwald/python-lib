from serviceclient import ServiceClient, URL
from JloXml import XmlRecord, XmlUtils
from ncar_lib.repository import SearchResult

"""
Use search service to retrieve library_dc and perform tallies over them
"""

class GetRecord:
	
	baseUrl = "http://nldr.library.ucar.edu/schemedit/services/ddsws1-1"
	
	def __init__ (self, recId):
		client = ServiceClient (self.baseUrl)
		params = {
			'verb':'GetRecord',
			'id':recId,
			'storedContent':['dcsstatus','dcsstatusNote']
		}
		request = client.setRequest (params)
		response = client.getResponse()
		if response.hasError():
			raise Exception, response.error
		self.result = self.parseResponse(response)

		
	def parseResponse (self, response):
		doc = response.doc
		errorEl = doc.selectSingleNode (doc.dom, "DDSWebService:error")
		if errorEl:
			raise Exception, doc.getText (errorEl)
		# print doc
		return SearchResult(doc.selectSingleNode (doc.dom, "DDSWebService:GetRecord:record"))

if __name__ == '__main__':
	# id = 'TECH-NOTE-000-000-000-847'
	baseUrl = "http://ttambora.ucar.edu:10160/schemedit/services/ddsws1-1"
	id = 'WOS-000-000-011-816'
	result = GetRecord(id).result
	print "result - id: %s, collection: %s, format: %s" % (result.recId, result.collection, result.xmlFormat)
