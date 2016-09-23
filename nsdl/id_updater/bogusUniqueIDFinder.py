"""
for each collection, compare a recordId and the UniqueID of it's Record in the NDSL

NOET: don't we care if the collection is managed in the NDR??
"""
from nsdl.ncs import ItemRecordGetter, NCSCollections
from nsdl.ndr import NdrObject, NdrClient, NdrClientError
from collection_checker import CollectionChecker

NSDL_COLLECTION_RECORDS_KEY = '1201216476279'

class BogusUniqueIDFinder:

	def __init__ (self):
		self.ndrClient = NdrClient()
		self.collections = NCSCollections()
		self.bogus_collections = []
		self.process()
		self.report()
		
	def process (self):
		print 'processing %d keys' % len(self.collections)
		for collection in self.collections:
			key = collection.searchKey
			if key == NSDL_COLLECTION_RECORDS_KEY or collection.xmlFormat == 'dlese_collect':
				continue
			if not CollectionChecker(collection).valid:
				self.bogus_collections.append(collection)

				
	def report (self):
		print "Bogus Collections (%d)" % len (self.bogus_collections)
		for item in self.bogus_collections:
			print item

if __name__ == '__main__':
	BogusUniqueIDFinder()
