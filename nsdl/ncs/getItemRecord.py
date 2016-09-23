"""
Get item record - gets an item record from specified collection
"""
import os, sys
from serviceclient import ServiceClient
from JloXml import XmlRecord, XmlUtils
from ncar_lib.repository import SearchResult
default_baseUrl = "http://ncs.nsdl.org/mgr/services/ddsws1-1"

class ItemRecordGetter:
	"""
	Do a search to get a single item record from specified collection
	- record is obtained by doing a search over the collection for a single result
	"""
	
	searchResult_constructor = SearchResult
	
	def __init__ (self, collectionKey, baseUrl=default_baseUrl):
		client = ServiceClient (baseUrl)
		params = {
			'n' : '1',
			's' : '0',
			'verb':'Search',
			'ky': collectionKey,
			"storedContent":['dcsndrHandle']
		}
		request = client.setRequest (params)
		self.result = None
		# print request.report()
		try:
			response = client.getResponse()
		except:
			raise Exception, "couldn't parse result for collectionKey='%s'\nRoot cause: %s" % (collectionKey, sys.exc_info()[1])
		if response.hasError():
			raise Exception, response.error
		self.result = self.parseResponse(response)

		
	def parseResponse (self, response):
		doc = response.doc
		errorEl = doc.selectSingleNode (doc.dom, "DDSWebService:error")
		if errorEl:
			raise Exception, doc.getText (errorEl)
		recordEl = doc.selectSingleNode (doc.dom, 'DDSWebService:Search:results:record')
		if recordEl:
			return self.searchResult_constructor (recordEl)
		
def tester (collectionKey):
	# collection = '1290084892596'
	searcher = ItemRecordGetter(collectionKey)
	if searcher.result:
		print 'ndrHandle: ', searcher.result.dcsndrHandle
	
if __name__ == '__main__':
	bog_key = '1228333818803' # the reponse from this can't be parsed??
	tester(bog_key)
