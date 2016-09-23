from serviceclient import ServiceClient, URL
from JloXml import XmlRecord, XmlUtils

"""
Use search service to retrieve library_dc and perform tallies over them
"""

class GetRecord:
	
	def __init__ (self, baseUrl, recId, item_record_class=XmlRecord):
		client = ServiceClient (baseUrl)
		params = {
			'verb':'GetRecord',
			'id':recId
		}
		request = client.setRequest (params)
		response = client.getResponse()
		if response.hasError():
			raise Exception, response.error
		self.result = self.parseResponse(response, item_record_class)

		
	def parseResponse (self, response, item_record_class):
		doc = response.doc
		errorEl = doc.selectSingleNode (doc.dom, "DDSWebService:error")
		if errorEl:
			raise Exception, doc.getText (errorEl)
		recordEl = doc.selectSingleNode (doc.dom, "DDSWebService:GetRecord:record:metadata:record")
		return item_record_class (xml=recordEl.toxml())

if __name__ == '__main__':
	# baseUrl = "http://nldr.library.ucar.edu/schemedit/services/ddsws1-1"
	# id = 'TECH-NOTE-000-000-000-847'
	baseUrl = "http://ttambora.ucar.edu:10160/schemedit/services/ddsws1-1"
	id = 'WOS-000-000-011-816'
	record = GetRecord(baseUrl, id).result
	print record
