from serviceclient import ServiceClient, URL
from JloXml import XmlRecord, XmlUtils
from ncar_lib.osm import OsmRecord
baseUrl = "http://nldr.library.ucar.edu/schemedit/services/ddsws1-1"
# baseUrl = "http://nldr.library.ucar.edu/dds/services/ddsws1-1"

"""
Use search service to retrieve library_dc and perform tallies over them
"""

class Tally:
	
	def __init__ (self):
		self.contrib_count = 0
		self.record_count = 0
		self.level_total = 0
		self.level_tally = {}
		
	def tally_recs (self, rec_list):
		for rec in rec_list:
			self.record_count += 1
			for contrib in rec.getContributorPeople():
				self.contrib_count += 1
				maxLevel = contrib.maxAffiliationLevel()
				self.level_total += maxLevel
				self.tally_level (maxLevel)
				
	def tally_level (self, level):
		"""
		keep count of the number of times each level is encountered
		 level -> occurrances
		"""
		old_val = self.level_tally.has_key (level) and self.level_tally[level] or 0
		self.level_tally[level] = old_val + 1
				
	def report (self):
		
		# print "level_total: %d (%s)" % (self.level_total, type(self.level_total))
		# print "contrib_count: %d (%s)" % (self.contrib_count, type(self.contrib_count))
		
		print "%d records processed" % self.record_count
		print "%d contributors processed" % self.contrib_count
		# print "  average affiliation level: %1.2f" % (float(self.level_total / self.contrib_count))
		print "level tally"
		keys = self.level_tally.keys()
		keys.sort()
		for level in keys:
			print '\t%d -> %d' % (level, self.level_tally[level])

class RecordGetter:

	numToFetch = 30000
	batchSize = 300
	
	def __init__ (self, service_client, params, item_record_class):
		self.tally = Tally()
		self.total = None
		self.recs = []
		self.item_record_class = item_record_class
		self.service_client = service_client
		self.params = params
		self.numRecords = self._get_num_records()
		print "%d total records to get" % self.numRecords
		s = 0
		numToGet = min (self.numToFetch, self.numRecords)
		self.recs = self.getRecords (numToGet)
			
	def getRecords (self, numToGet):
		s = 0
		recs = []
		rec_count = 0
		# print "getting %d of %d records" % (numToGet, self.numRecords)
		while s < numToGet:
			thisBatchSize = min (self.batchSize, numToGet - len(recs))
			record_batch = self._get_record_batch (s, thisBatchSize)
			# recs = recs + record_batch
			rec_count = rec_count + len(record_batch)
			self.tally.tally_recs (record_batch)
			print " ... %d recs" % rec_count
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
		"xmlFormat": "osm",
		}

	client = ServiceClient (baseUrl)
	getter = RecordGetter(client, params, OsmRecord)
	getter.tally.report()

