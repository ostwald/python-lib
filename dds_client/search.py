from serviceclient import ServiceClient, URL
from JloXml import XmlRecord, XmlUtils
from nsdl.ncs import NCSCollectRecord

NLDR_DDS_URL = "http://nldr.library.ucar.edu/schemedit/services/ddsws1-1"
UCONN_DCS_URL = "https://uc.dls.ucar.edu:443/dcs/services/ddsws1-1"


"""
Use search service to retrieve library_dc and perform tallies over them
"""

class RecordGetter:

	numToFetch = 10000
	batchSize = 50
	
	def __init__ (self, service_client, params, item_constructor):
		self.total = None
		self.recs = []
		self.item_constructor = item_constructor

		print 'constructor: %s' % item_constructor

		self.service_client = service_client
		self.params = params
		if not self.params.has_key('q'):
			self.params['q'] = ''
		self.numRecords = self._get_num_records()
		try:
			print "%d total records" % self.numRecords
		except Exception, msg:
			raise Exception, 'RecordGetter Could not parse service response: %s' % msg
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
		print request.report()
		response = client.getResponse()
		if response.hasError():
			print response.error
		
		else:
			return response.doc
			
	def _get_record_batch (self, start, num):
		"""
		returns a batch of objects (via item_constructor
		(e.g., XML Record)
		"""
		doc = self.getResponseDoc (start, num)
		doc.xpath_delimiter = ":"
		nodes = doc.selectNodes (doc.dom, 'DDSWebService:Search:results:record:metadata:record')
		# print "%d nodes found" % len(nodes)
		records = []
		for node in nodes:
			rec = self.item_constructor (xml=node.toxml())
			records.append (rec)
		return records

def formatSearch ():
	# we're getting collection records - use NCSCollectRecord
	baseUrl = NLDR_DDS_URL
	params = {
	"verb": "Search",
	"xmlFormat": "library_dc",
	}

	client = ServiceClient (baseUrl)
	item_constructor = XmlRecord
	getter = RecordGetter(client, params, item_constructor)
	print getter.recs[3]

if __name__ == '__main__':

	baseUrl = UCONN_DCS_URL
	CMC = '1201216476279' # key for Ucar Collection Management Collection

	# query for specific view Context
	q='/key//record/collection/viewContexts/viewContext:"DLESECollections"'
	params = {
		"verb" : "Search",
		"ky" : CMC,
		"q" : q
	}

	client = ServiceClient (baseUrl)
	item_constructor = NCSCollectRecord
	getter = RecordGetter(client, params, item_constructor)
	print "%d records returned" % len(getter.recs)
	# sort the recs by title
	getLabel = lambda x:x.getTitle()
	getter.recs.sort(key=getLabel)
	for rec in getter.recs:
		print '-', getLabel(rec)

