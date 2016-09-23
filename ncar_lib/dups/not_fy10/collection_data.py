"""
Obtain not-fy10 collection info data via webservice (see NotFy10RecordsSearcher).

For each record (see RecInfo), collect
	recId, status, title, pubName, fiscalYear, titleKey
	
	
Write results as XML to a collection data file (e.g., 'not-fy10-records.xml')

Collection data will be processed by ... 
"""
import os, sys, time
from ncar_lib.repository import RepositorySearcher, OsmSearchResult
from JloXml import XmlRecord, XmlUtils

class RecInfo:
	"""
	osmResult param is a OsmSearchResult instance
		result.payload is an osmRecord instance
	"""
	def __init__ (self, osmResult):
		self.recId = osmResult.recId
		self.status = osmResult.dcsstatus
		self.title = osmResult.payload.getTitle() or ""
		self.pubName = osmResult.payload.getPubName() or ""
		self.fiscalYear = osmResult.dcsosmFiscalYear or ""
		self.titleKey = osmResult.dcsosmFlattenedTitle or ""
		
	def __repr__ (self):
		return "%s (%s) %s" % (self.recId, self.status, self.title)
		
	def __cmp__ (self, other):
		return cmp (self.recId, other.recId)
		
	def asElement(self):
		element = XmlUtils.createElement("record")
		element.setAttribute ("recId", self.recId)
		element.setAttribute ("status", self.status)
		element.setAttribute ("title", self.title)
		element.setAttribute ("pubName", self.pubName)
		element.setAttribute ("fiscalYear", self.fiscalYear)
		element.setAttribute ("titleKey", self.titleKey)
		return element

class NotFy10RecordsSearcher(RepositorySearcher):
	"""
	searches for all records in not-fy10 collection and outputs xml containing
	info about each record (using info from both metadata and dcs_data)
	"""
	numToFetch = 20000
	batchSize = 200
	searchResult_constructor = OsmSearchResult
	filter_predicate = None
	verbose = True
	
	def __init__ (self):
		RepositorySearcher.__init__ (self, collection="not-fy10", xmlFormat="osm")
		
	def get_params (self, collection, xmlFormat):
		"""
		define the params used to query the search service
		"""
		return {
			"q" : "",
			"verb": "Search",
			"xmlFormat": 'osm',
			"ky": 'not-fy10',
			"storedContent":['dcsstatus', 
							 'dcsstatusNote', 
							 'dcsisValid',
							 'dcsosmFiscalYear',
							 'dcsosmFlattenedTitle'
							 ]
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
			map (self.append, map (RecInfo, results))
			if self.verbose:
				print " ... %d results" % len (self)
			s = s + self.batchSize
		return results
		
	def writeXml (self, path=None):
		"""
		write record info file to disk as xml
		"""
		path = path or "not-fy10-records.xml"
		rec = XmlRecord (xml="<not-fy10-records/>")
		rec.doc.setAttribute ("date", time.asctime(time.localtime()))
		for recInfo in self:
			rec.doc.appendChild (recInfo.asElement())
		rec.write(path)
		print 'wrote to ', path
		
		
if __name__ == '__main__':
	records = NotFy10RecordsSearcher()
	records.data.sort()
	print '%d records read' % len (records)
	# print records[1]
	# print records[1].asElement().toxml()
	records.writeXml()
