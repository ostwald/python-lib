import sys, os
from UserList import UserList
from ncar_lib.repository import SearchResult, OsmSearchResult, RepositorySearcher
from serviceclient import ServiceClient, URL
from JloXml import XmlRecord, XmlUtils 

default_baseUrl = "http://nldr.library.ucar.edu/schemedit/services/ddsws1-1"

class LastTouchSearcher (RepositorySearcher):
	"""
	- get_params() - specifies DDS Search service to grab search results
	  search_results are constructed using searchResult_constructor
	- filterResults() is called on initial set of results, allowing subclasses
	  to work with a subset of results returned by search
	- processResults() hook to operate over results (after filtering)
	"""

	numToFetch = 20000
	batchSize = 200
	filter_predicate = None
	verbose = True
	
	def __init__ (self, timeStr, collection=None):
		UserList.__init__ (self)
		self.collection = collection
		self.timeStr = timeStr
		RepositorySearcher.__init__ (self, collection=collection, xmlFormat='osm') 
			
	def get_params (self, collection, xmlFormat):
		"""
		date field: dcslastTouchDate
		fromDate: 2011-01-01
		"""
		return {
			'verb': 'Search',
			'xmlFormat': xmlFormat,
			'sortDescendingBy':'dcslastTouchDate',
			# 'q':'/key//record/general/title:"%s"' % self.title,
			'ky': self.collection,
			'storedContent':['dcsstatus', 'dcsstatusNote', 'dcsisValid', 'dcslastTouchDate']
			}

	def get_params_OFF (self, collection, xmlFormat):
		"""
		date field: dcslastTouchDate
		fromDate: 2011-01-01
		"""
		return {
			'verb': 'Search',
			'xmlFormat': xmlFormat,
			# 'dateField' : 'dcslastTouchDate',
			'dateField' : 'modtime',
			'fromDate' : '2011-02',
			'toDate' : '2011-05',
			# 'q':'/key//record/general/title:"%s"' % self.title,
			'ky': collection,
			'storedContent':['dcsstatus', 'dcsstatusNote', 'dcsisValid']
			}
			
	def getResults (self, numToGet):
		"""
		we don't keep entire results, but instead extract only recid and dcslastTouchDate
		"""
		s = 0
		results = []
		# print "getting %d of %d records" % (numToGet, self.numRecords)
		while s < numToGet:
			thisBatch = min (self.batchSize, numToGet - len(results))
			results = self.get_result_batch (s, thisBatch)
			map (self.append, map (lambda x:{'recId':x.recId, 'lastTouch':x.dcslastTouchDate}, results))
			# map (self.append, results)
			if self.verbose:
				print " ... %d results" % len (self)
			s = s + self.batchSize
		return results
			
	def report (self):
		for result in self:
			print '%s - %s' % (result['recId'], result['lastTouch'])
			# print result.payload
	
	def toxml (self):
		"""
		make an xml document containing id and dcslastTouchDate value for each record
		"""
		rec = XmlRecord(xml="<lastTouchInfo></lastTouchInfo>")
		rec.doc.setAttribute ("collection", self.collection)
		for result in self:
			el = XmlUtils.addElement(rec.dom, rec.doc, 'rec')
			for key in result.keys():
				el.setAttribute (key, result[key])
		
		dest = "RAW_lastTouchData/%s.xml" % self.collection
		rec.write (dest)
		print "wrote to ", dest
			
if __name__ == '__main__':
	timeStr = "2011-01-01"
	collection = 'osgc'
	results = LastTouchSearcher(timeStr, collection)
	print '%d results found' % len(results)
	# results.report()
	results.toxml()

