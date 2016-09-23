"""
Finds Done records in support of the fiscalYear update (for non-Archive and non-Oral History collections
"""
import os, sys
from ncar_lib.repository import RepositorySearcher, SummarySearcher
from dds_client import ListCollections
import updater_globals

class DoneRecordsSearcher (RepositorySearcher):
	"""
	find all records in specified collection that are DONE
	stores only IDs of hits (in results);
	"""
	verbose = 1
	numToFetch = 20000
	
	def __init__ (self, collection):
		self.collection = collection
		RepositorySearcher.__init__ (self, collection=collection)
		ids = []
	
	def get_params (self, collection, xmlFormat):
		"""
		define the params used to query the search service
		"""
		return {
			"verb": "Search",
			"ky" : self.collection,
			"xmlFormat": 'osm',
			"dcsStatus": 'Done',
			"storedContent":['dcsstatus', 'dcsstatusNote', 'dcsisValid']
			}
			
	def getResults (self, numToGet):
		"""
		do as many requests (size determined by numToGet) as necessary
		to get all records, or self.numRecords, whichever is smaller.
		
		search hits are stored in self.data
		"""
		s = 0
		results = []
		# print "getting %d of %d records" % (numToGet, self.numRecords)
		while s < numToGet:
			thisBatch = min (self.batchSize, numToGet - len(results))
			results = self.get_result_batch (s, thisBatch)
			map (self.append, map(lambda x:x.recId, results))
			if self.verbose:
				print " ... %d results" % len (self)
			s = s + self.batchSize
		return results
			
class DoneRecordsSummarizer (SummarySearcher):
	"""
	find DONE records with no fiscalYear value
	"""
	
	def __init__ (self, collection=None):
		self.collection = collection
		SummarySearcher.__init__ (self, collection=collection)
	
	def get_params (self, collection, xmlFormat):
		"""
		define the params used to query the search service
		"""
		
		noFiscalYear='allrecords:true NOT indexedXpaths:/record/coverage/fiscalYear'
		noArchivals = []

		
		q='%s NOT (ky:%s OR ky:%s' % ('allrecords:true', 'osgc', 'not-fy10')
			
		return {
			"verb": "Search",
			"ky" : self.collection,
			"xmlFormat": 'osm',
			"dcsStatus": 'Done',
			"storedContent":['dcsstatus', 'dcsstatusNote', 'dcsisValid']
			}
			
	def report (self, total_recs=None):
		summary = self.summary
		print "\n-----------------------"
		print "SUMMARY - %s" % self.collection
		if total_recs:
			print "%d records in collection" % total_recs
		print "%d records are DONE" % summary.totalNumResults
		for faceted_field in summary.faceted_fields:
			faceted_field.report()

def summarizeNonArchivalCollections ():
	osmCollectionsInfo = filter (lambda x:x.xmlFormat=='osm', ListCollections().results)
	for colInfo in osmCollectionsInfo:
		if colInfo.key in updater_globals.archival_collections:
			# print 'skipping %s (%s)' % (colInfo.key, colInfo.xmlFormat)
			continue

		summarizer = DoneRecordsSummarizer(colInfo.key)
		summarizer.report(colInfo.numRecords)
			
def getDoneRecordIds (collection):
	results = DoneRecordsSearcher(collection)
	print '%d Done records in %s' % (len(results), collection)
	results.data.sort()
	return results.data
		
if __name__ == '__main__':
	# summarizeNonArchivalCollections()
	ids = getDoneRecordIds("osgc")
	print '%d done records' % len(ids)
	for id in ids:
		print ' - ', id

