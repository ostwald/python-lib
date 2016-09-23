"""
rights_reporter -

In order to evaluate what programmatic changes need to be made to the copyright type field, Michael and I would appreciate a spreadsheet with the following fields:

//record/general/recordID
//record/rights/copyrightNotice
//record/rights/copyrightNotice/@holder
//record/rights/copyrightNotice/@type 

Approach
use repository searcher to get all records in specified collection

for each result:
	extract each field
	write as tab delimited form

"""
import os, sys, codecs, time
from ncar_lib.repository import RepositorySearcher, OsmSearchResult

report_schema = ['recId', 'copyrightNotice', 'rightsType', 'rightsHolder']

def truncate (s, size=100):
	if len(s) > size:
		return s[:size-4] + ' ...'
	return s

class RightsInfo:
	
	def __init__ (self, osmSearchResult):
		self.recId = osmSearchResult.recId
		osmRecord = osmSearchResult.payload
		for attr in report_schema[1:]:
			# self.copyrightNotice = osmRecord.get('
			setattr (self, attr, osmRecord.get(attr) or '')
			
		self.copyrightNotice = truncate (self.copyrightNotice)
			
	def asTabDelimited (self):
		return '\t'.join(map (lambda x:getattr(self, x), report_schema))
			
class RightsSearcher (RepositorySearcher):
	
	numToFetch = 10000
	batchSize = 400
	searchResult_constructor = OsmSearchResult
	
	def __init__ (self, collection):
		self.collection = collection
		RepositorySearcher.__init__ (self, collection=collection)
	
	def get_params (self, collection, xmlFormat):
		"""
		define the params used to query the search service
		"""
		return {
			"verb": "Search",
			"ky": collection,
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
			map (self.append, map (RightsInfo, results))
			if self.verbose:
				print " ... %d results" % len (self)
			s = s + self.batchSize
		return results
			
	def writeReport (self, outpath=None):
		if outpath is None:
			outpath = "%s-rights-report.xls" % self.collection
		fp = codecs.open(outpath, 'w', 'utf-8')
		lines=[];add=lines.append
		add ('\t'.join(report_schema))
		# for info in self.data:
			# # print info.recId, info.rightsType
			# add (info.asTabDelimited())
		# fp.write ('\n'.join (lines))
		fp.write ('\n'.join (map (lambda x:x.asTabDelimited(), self.data)))
		fp.close ()
		print 'wrote to ', outpath
			
def tester ():
	col = 'ams-pubs'
	searcher = RightsSearcher(col)
	print '%d items found' % len(searcher)
	for result in searcher:
		info = RightsInfo (result)
		# print info.recId, info.rightsType
		print info.asTabDelimited()	
		
if __name__ == '__main__':
	col = 'ams'
	searcher = RightsSearcher(col)
	print '%d items found' % len(searcher)
	searcher.writeReport()

