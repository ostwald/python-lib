"""
Wrap the DDS ListCollections service to obtain collection-level info from a repository
"""
from serviceclient import ServiceClient, URL
from JloXml import XmlRecord, XmlUtils

default_baseUrl = "http://nldr.library.ucar.edu/schemedit/services/ddsws1-1"

class CollectionInfo:
	"""
	Reads collection-level element of ListCollections response
	exposes:
		- key
		- recordId
		- xmlFormat
		- numRecords
	"""
	def __init__ (self, element):
		"""
		"""
		self.key = XmlUtils.getTextAtPath (element, 'searchKey')
		self.recordId = XmlUtils.getTextAtPath (element, 'recordId')
		
		self.xmlFormat = XmlUtils.getTextAtPath  (element, 'additionalMetadata/dlese_collect/formatOfRecords')
		self.numRecords = XmlUtils.getTextAtPath (element, 'additionalMetadata/dlese_collect/numRecords')
		if self.numRecords:
			try:
				self.numRecords = int(self.numRecords)
			except:
				print "could not convert numRecords (%s) to integer: %s" % (self.numRecords, sys.exc_info()[1])
		if not self.numRecords:
			self.numRecords = 0
		
	def __repr__ (self):
		return "%s (format: %s, numRecords: %d)" % (self.key, self.xmlFormat, self.numRecords)
		
class ListCollections:
	"""
	self.results are CollectionInfo instances
	"""
	def __init__ (self, baseUrl=default_baseUrl):
		client = ServiceClient (baseUrl)
		params = {
			'verb':'ListCollections'
		}
		request = client.setRequest (params)
		response = client.getResponse()
		if response.hasError():
			raise Exception, response.error
		self.results = self.parseResponse(response)

	def getCollectionInfo (self, key):
		for info in self.results:
			if info.key == key:
				return info
				
		
	def parseResponse (self, response):
		doc = response.doc
		doc.xpath_delimiter = '/' # this is required to use XmlUtils.getTextAtPath gracefully
		errorEl = doc.selectSingleNode (doc.dom, "DDSWebService/error")
		if errorEl:
			raise Exception, doc.getText (errorEl)
		nodes = doc.selectNodes (doc.dom, "DDSWebService/ListCollections/collections/collection")
		return map (CollectionInfo, nodes)

if __name__ == '__main__':
	collections = ListCollections().results
	print "%d collections found" % len(collections)
	for col in collections:
		print col
