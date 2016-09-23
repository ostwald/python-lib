"""
prints out the different values for copyright notice across a collection
(using facets)
"""
import os, sys
from ncar_lib.repository import RepositorySearcher, SummarySearcher
from dds_client import ListCollections
			
class CopyrightSummarizer (SummarySearcher):
	"""
	find all records in not-fy2010 that don't have rights/coverage
	"""
	def __init__ (self, collection):
		self.collection = collection
		SummarySearcher.__init__ (self, collection=collection)
	
	def get_params (self, collection, xmlFormat):
		"""
		define the params used to query the search service
		"""
		hasCopyrightNotice='indexedXpaths:/record/rights/copyrightNotice'
		noCopyrightNotice='allrecords:true NOT indexedXpaths:/record/rights/copyrightNotice'
		
		return {
			"q":hasCopyrightNotice,
			"verb": "Search",
			"ky": self.collection,
			'facet' : 'true',
			'facet.field' : '/key//record/rights/copyrightNotice',
			"storedContent":['dcsstatus', 'dcsstatusNote', 'dcsisValid']
			}
			
	def report (self, total_recs=None):
		summary = self.summary
		print "\n-------------------------------\n"
		print "SUMMARY - %s" % self.collection
		if total_recs:
			print "%d records in collection" % total_recs
		print "%d records found" % summary.totalNumResults
		for faceted_field in summary.faceted_fields:
			faceted_field.report(0)

def processOsmCollections ():
	collections = filter (lambda x:x.xmlFormat == 'osm', ListCollections().results)
	# collections = filter (lambda x:x.key == 'testosm', ListCollections().results)
	
	for col in collections:
		# print "%s (%s) - %d records" % (col.key, col.xmlFormat, col.numRecords)
		summarizer = CopyrightSummarizer(col.key)
		summarizer.report(col.numRecords)
		
		
if __name__ == '__main__':
	if 1:
		processOsmCollections ()
	else:
		collection = 'testosm'
		summarizer = CopyrightSummarizer(collection)
		summarizer.report()
		print summarizer.service_client.request.getUrl()
