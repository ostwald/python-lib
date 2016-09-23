"""
ingest - tools to pull records either from cache or remote repository into
local DCS

search DDS for ids
get records from cache
put records to local DCS
"""
import os, sys

from updater import UpdateManager
from inst_div_searcher import InstDivSearcher
from data_reader import DataTable, DataRecord

class IngestManager (UpdateManager):
	
	def __init__ (self, config):
		UpdateManager.__init__(self, config)
		

	def ingestFromCache (self, collection):
		"""
		records come from cache and are written to the NCS
		"""
		for id in self.getCachedRecordIds (collection)[11:100]:
			# print id
			rec = self.getCachedRecord(id)
			self.putRemoteRecord(rec)
			
	def ingestRemoteByTerms (self, collection=None):
		for vocab in self.dataTable.getVocabTerms():
			results = self.search (vocab, collection)
			print "%d results found for collection: %s" % (len(results), collection or "All")
			
			for result in results:
				self.putRemoteRecord (result.payload)
				
		
def test ():
	mgr = IngestManager('local_ingest')
	
	if 0: 	#  test that we are looking at the cache
		for col in mgr.getCachedCollectionIds():
			print col
	
	if 0:   # test that we are searching from nldr
		vocab = "Earth Observing Laboratory (EOL)"
		results = mgr.search (vocab)
		print 'found %d records with "%s"' % (len(results), vocab)
		
	if 0:   # test that we can read from cache
		id = 'OSGC-000-000-003-387'
		record = mgr.getCachedRecord(id)
		print record
		
	if 0:  # test that we can write to local dcs
		from test import putRecord
		putRecord('OSGC-000-000-003-387', mgr)
		
if __name__ == '__main__':
	mgr = IngestManager('local_ingest')
	# mgr.ingestRemoteByTerms('osgc')
	mgr.ingestFromCache('osgc')
