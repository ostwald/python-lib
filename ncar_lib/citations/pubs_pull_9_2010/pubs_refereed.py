"""
pubs_refereed.py - get the ids of the "Citations - PUBS Refereed" collection (id = "pubs-ref")

there are 2838 records

"""
from dds_client import  ServiceClient, URL, RecordGetter
from ncar_lib.osm import OsmRecord

idFile = "pubs_refd_ids.txt"

class GetIdsFromWebService:
	"""
	use dds search service to get ids of all records in pubs-ref collection
	- write ids to disk
	"""
	
	def __init__ (self, recordsToGet=1000):
		self.records = self.getRecords (recordsToGet)
		self.ids = self.getIds()
		# self.writePubsIds()
	
	def getRecords (self, recordsToGet=10000):
	
		baseUrl = 'http://nldr.library.ucar.edu/schemedit/services/ddsws1-1'
		
		params = {
			"verb": "Search",
			"ky": "pubs-ref",
			}
		
		client = ServiceClient (baseUrl)
		RecordGetter.numToFetch = recordsToGet
		getter = RecordGetter(client, params, OsmRecord)
		print "%d records found" % len(getter.recs)
		return getter.recs
		
	def getIds (self):
		ids = map (lambda rec:rec.get('pub_id'), self.records)
		ids.sort()
		return ids
		
	def writePubsIds(self, dest=idFile):
		for id in self.getIds():
			print id
		fp = open (dest, "w")
		fp.write ("\n".join(ids))
		fp.close()
		
class IdFileReader:
	"""
	read ids from file created by GetIdsFromWebService
	"""
	def __init__ (self, src=idFile):
		s = open(idFile).read()
		self.ids = s.split('\n')
		self.ids.sort()
		
def getPubsRefdIds():
	return IdFileReader().ids
	
def getIdsFromWebServiceTester():
	for id in GetIdsFromWebService(10).ids:
		print id
		
def idFileReaderTester():
	ids = IdFileReader().ids
	print "%d ids read" % len(ids)
	for id in ids:
		print id	
		

		
if __name__ == '__main__':
	pass

