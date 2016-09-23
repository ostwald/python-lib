from serviceclient import ServiceClient, URL
from JloXml import XmlRecord, XmlUtils
baseUrl = "http://nldr.library.ucar.edu/schemedit/services/ddsws1-1"

"""
Use search service to retrieve library_dc and perform tallies over them
"""

class RecordGetter:

	numToFetch = 10000
	batchSize = 50
	
	def __init__ (self, service_client, params, item_record_class):
		self.total = None
		self.recs = []
		self.item_record_class = item_record_class
		self.service_client = service_client
		self.params = params
		self.numRecords = self._get_num_records()
		print "%d total records" % self.numRecords
		s = 0
		numToGet = min (self.numToFetch, self.numRecords)
		self.recs = self.getRecords (numToGet)
			
	def getRecords (self, numToGet):
		s = 0
		recs = []
		# print "getting %d of %d records" % (numToGet, self.numRecords)
		while s < numToGet:
			thisBatch = min (self.batchSize, numToGet - len(recs))
			recs = recs + self._get_record_batch (s, thisBatch)
			print " ... %d recs" % len (recs)
			s = s + self.batchSize
		return recs
		
	def _get_num_records (self):
		doc = self.getResponseDoc (0,1)
		doc.xpath_delimiter = ":"
		totalNumResults = doc.getTextAtPath ('DDSWebService:Search:resultInfo:totalNumResults')
		# print "%s (%s)" % (totalNumResults, type(totalNumResults))
		if totalNumResults is None:
			return 0
		else:
			return int(totalNumResults)
	
	def getResponseDoc (self, start, num):
		client = self.service_client
		self.params.update ({"s":str(start), "n":str(num)})
		# print params
		request = client.setRequest (self.params)
		# print request.report()
		response = client.getResponse()
		if response.hasError():
			print response.error
		
		else:
			return response.doc
			
	def _get_record_batch (self, start, num):
		doc = self.getResponseDoc (start, num)
		doc.xpath_delimiter = ":"
		nodes = doc.selectNodes (doc.dom, 'DDSWebService:Search:results:record:metadata:record')
		# print "%d nodes found" % len(nodes)
		records = []
		for node in nodes:
			rec = self.item_record_class (xml=node.toxml())
			records.append (rec)
		return records
	
if __name__ == '__main__':
	params = {
		"verb": "Search",
		"xmlFormat": "library_dc",
		}

	client = ServiceClient (baseUrl)
	getter = RecordGetter(client, params, XmlRecord)
	print getter.recs[3]

