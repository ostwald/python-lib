"""
Generate report of all records in osgc and ams-pubs collections that do NOT have
a dateType of "Fiscal".

Report recordID, dcsstatus, dcsstatusNote, other date info
"""

import os, sys, codecs
from ncar_lib.repository import RepositorySearcher, OsmSearchResult
from ncar_lib.osm import OsmRecord
from JloXml import XmlRecord, XmlUtils
	
def noFiscalDatePredicate (searcher, result):
	return not result.payload.getTypedDate("Fiscal")
		
class NotFiscalDateSearcher (RepositorySearcher):
	
	numToFetch = 20
	batchSize = 200
	searchResult_constructor = OsmSearchResult
	filter_predicate = noFiscalDatePredicate
	baseUrl = "http://nldr.library.ucar.edu/schemedit/services/ddsws1-1"
	verbose = True
	dowrite = 0
	
	def __init__ (self, collection=None, xmlFormat='osm'):
		RepositorySearcher.__init__(self, collection, xmlFormat)
		
	def get_params (self, collection, xmlFormat):
		return {
			"verb": "Search",
			'storedContent':['dcsstatus','dcsstatusNote'],
			"ky": collection
		}

	def processResults (self):
		if self.dowrite:
			self.write()
		else:
			print self.report()
		
	def reportResult (self, result):
		"""
		fields are id, dcsstatus, dcsstatusNote, <other dates>
		"""
		s=[];add=s.append
		for attr in ['recId', 'dcsstatus', 'dcsstatusNote']:
			add (getattr (result, attr))
			
		#report the other dateFields for this osmRecord
		dateMap = result.payload.getDateMap()
		if dateMap:
			dateTypes = dateMap.keys()
			dateTypes.sort()
			for dateType in dateTypes:
				# there can be multiple values for a give type ...
				values = dateMap[dateType]
				if not type(values) == type([]):
					values = [values]
				for val in values:
					add ("%s: %s" % (dateType, val))
		return '\t'.join(s)
					
	def report (self):
		s=[];add = s.append
		for result in self:
			add (self.reportResult(result))
		return '\n'.join(s)
	
	def write (self):
		outpath = "output/noFiscalDateReport.txt"
		fp = codecs.open (outpath, 'w', 'utf-8')
		fp.write (self.report())
		fp.close()
		print "wrote to %s" % outpath
		
if __name__ == '__main__':
	# results = NotFiscalDateSearcher('ams-pubs')
	results = NotFiscalDateSearcher(['osgc', 'ams-pubs'])

	


