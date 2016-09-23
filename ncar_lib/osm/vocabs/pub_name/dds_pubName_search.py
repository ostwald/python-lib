import os, sys
from dds_client import ServiceClient, URL, RecordGetter
from ncar_lib.repository.dds_search_result import SearchResult
from ncar_lib.osm import OsmRecord
from JloXml import XmlRecord, XmlUtils
	
class PubNameRecordGetterException (Exception):
	pass

class PubNameRecordGetter:
	
	# stop_collections = ["staffnotes"]
	stop_collections = []
	baseUrl = "http://nldr.library.ucar.edu/schemedit/services/ddsws1-1"
	# baseUrl = "http://ttambora.ucar.edu:10160/schemedit/services/ddsws1-1"
	
	def __init__ (self, pubName):
		self.pubName = pubName
		service_client = ServiceClient (self.baseUrl)
		
		params = {
			"verb": "Search",
			'q':'/key//record/general/pubName:"%s"' % self.pubName,
			'storedContent':['dcsstatus','dcsstatusNote'],
			## 'q':anyAssetQuery,
			## 'xmlFormat': 'osm',
			's': '0',
			'n': '100'
		}
		request = service_client.setRequest (params)
		# print request.report ()
		# sys.exit()
		response = service_client.getResponse()
		# print response.doc
		if response.hasError():
			raise PubNameRecordGetterException, response.error
		self.results = self.parseResponse(response)
		
	def parseResponse (self, response):
		doc = response.doc
		errorEl = doc.selectSingleNode (doc.dom, "DDSWebService:error")
		if errorEl:
			# raise Exception, doc.getText (errorEl)
			results = []
		## print doc
		else:
			results = map (SearchResult, doc.selectNodes(doc.dom, "DDSWebService:Search:results:record"))
			
			## don't even consider results that are in the "stop_collections"
			results = filter(lambda x:x.collection not in self.stop_collections, results)
		
		return results

		
	def report (self):
		print "%d results found for %s" % (len (self.results), self.pubName)
		for result in self.results:
			result.report()
		
def getterTester(pubName):
	# asset = "asset-000-000-000-040"

	try:
		getter = PubNameRecordGetter(pubName)
		# print getter.result
		# getter.result.report()	
	except:
		print sys.exc_info()[1]

			
if __name__ == '__main__':
	pubName = 'National Radio Science Meeting'
	# getterTester (pubName)
	getter = PubNameRecordGetter(pubName)
	getter.report()


