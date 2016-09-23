"""
for each collection, compare a recordId and the UniqueID of it's Record in the NDSL

NOET: don't we care if the collection is managed in the NDR??
"""
from nsdl.ncs import ItemRecordGetter, NCSCollections
from nsdl.ndr import NdrObject, NdrClient

NSDL_COLLECTION_RECORDS_KEY = '1201216476279'

class BogusUniqueIDFinder:

	def __init__ (self):
		self.ndrClient = NdrClient()
		self.collections = NCSCollections()
		self.bogus_items = []
		self.process()
		self.report()
		
	def process (self):
		print 'processing %d keys' % len(self.collections)
		for collection in self.collections:
			key = collection.searchKey
			if key == NSDL_COLLECTION_RECORDS_KEY or collection.xmlFormat == 'dlese_collect':
				continue
			result = ItemRecordGetter(key).result
			if not result:
				raise 'item record not found for %s' % key
			# print '%s - %s' % (result.recId, result.dcsndrHandle)
			if not result.dcsndrHandle:
				continue
			uniqueID = self.ndrClient.get(result.dcsndrHandle).uniqueID
			print '%s - %s - %s' % (collection.name, result.recId, uniqueID)
			if uniqueID != result.recId:
				self.bogus_items.append ('%s %s - (%s - %s)' % (collection.name, key, result.recId, uniqueID))
				
	def report (self):
		print "Bogus Collections (%d)" % len (self.bogus_items)
		for item in self.bogus_items:
			print item

if __name__ == '__main__':
	BogusUniqueIDFinder()
