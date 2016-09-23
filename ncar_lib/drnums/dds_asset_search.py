import os, sys
import utils
from dds_client import ServiceClient, URL, RecordGetter
from ncar_lib.osm import OsmRecord
from JloXml import XmlRecord, XmlUtils
	
"""
'/text//record/resources/primaryAsset/@url:'+self.asset
'/text//record/resources/primaryAsset/@url:'+self.asset
"""

class AssetRecordGetterException (Exception):
	pass

class AssetRecordGetter:
	
	stop_collections = ["staffnotes"]
	# stop_collections = []
	baseUrl = "http://nldr.library.ucar.edu/schemedit/services/ddsws1-1"
	
	def __init__ (self, asset):
		self.asset = asset
		service_client = ServiceClient (self.baseUrl)
		
		anyAssetQuery = '/text//record/resources/primaryAsset/@url:'+self.asset
		anyAssetQuery += ' OR /text//record/resources/otherAsset/@url:'+self.asset
		
		params = {
			"verb": "Search",
			'q':'/text//record/resources/primaryAsset/@url:'+self.asset,
			## 'q':anyAssetQuery,
			's': '0',
			'n': '100'
		}
		request = service_client.setRequest (params)
		# print request.report ()
		# sys.exit()
		response = service_client.getResponse()
		if response.hasError():
			raise AssetRecordGetterException, response.error
		self.result = self.parseResponse(response)
		# self.report(response)
		
	def report (self, response):
		doc = response.doc
		errorEl = doc.selectSingleNode (doc.dom, "DDSWebService:error")
		if errorEl:
			# raise Exception, doc.getText (errorEl)
			results = []
		## print doc
		else:
			results = map (Result, doc.selectNodes(doc.dom, "DDSWebService:Search:results:record"))
			
			## don't even consider results that are in the "stop_collections"
			results = filter(lambda x:x.collection not in self.stop_collections, results)
		
		if len(results) == 0:
			print "%s - no results found" % self.asset
			
		elif len(results) > 1:
			print "%s - %d results found" % (self.asset, len(results))
			for result in results:
				print "\t %s / %s" % (result.collection, result.recId)
				
		else:
			result = results[0]
			# print "%s -> %s / %s" % (self.asset, result.collection, result.recId)
		
	def parseResponse (self, response):
		doc = response.doc
		errorEl = doc.selectSingleNode (doc.dom, "DDSWebService:error")
		if errorEl:
			# raise Exception, doc.getText (errorEl)
			results = []
		## print doc
		else:
			results = map (Result, doc.selectNodes(doc.dom, "DDSWebService:Search:results:record"))
			
			## don't even consider results that are in the "stop_collections"
			results = filter(lambda x:x.collection not in self.stop_collections, results)
		
		if len(results) == 0:
			raise AssetRecordGetterException, "could not find result for %s" % self.asset
			
		if len(results) > 1:
			raise AssetRecordGetterException, "multiple results found for %s (%s)" % (self.asset, map(lambda x:x.collection, results))
		
		return results[0]


class Result(XmlRecord):
	
	def __init__ (self, element):
		XmlRecord.__init__ (self, xml=element.toxml())
		# self.recId = self.getTextAtPath("head:id")
		self.recId = self.getTextAtPath("record:head:id")
		self.collection = self._get_collection()
		
	def _get_collection (self):
		node = self.selectSingleNode (self.dom, "record:head:collection")
		if node:
			return node.getAttribute("key")
			
	def report(self):
		print self.recId, self.collection
		
def getterTester(asset):
	# asset = "asset-000-000-000-040"

	try:
		getter = AssetRecordGetter(asset)
		# print getter.result
		getter.result.report()	
	except:
		print sys.exc_info()[1]

def reportAllDrNumbersToRecords():
	from dr_mappings import DRMappings
	for drNumber in DRMappings().keys():
		asset = utils.makeId ("asset", utils.getIdNum (drNumber))
		recId = AssetRecordGetter(asset)
		
def matchAllDrNumbersToRecords():
	from dr_mappings import DRMappings
	for drNumber in DRMappings().keys():
		asset = utils.makeId ("asset", utils.getIdNum (drNumber))
		try:
			recId = AssetRecordGetter(asset).result.recId
			# print asset, recId
		except:
			print sys.exc_info()[1]
			
			
if __name__ == '__main__':
	# getterTester ("asset-000-000-000-006")
	reportAllDrNumbersToRecords ()


