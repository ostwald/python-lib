"""
Generate report of all records in osgc and ams-pubs collections that do NOT have
a dateType of "Fiscal".

Report recordID, resourceType, dcsstatus, dcsstatusNote, other date info
"""

import os, sys, codecs
from ncar_lib.repository import RepositorySearcher, OsmSearchResult
from ncar_lib.osm import OsmRecord
from JloXml import XmlRecord, XmlUtils
	
# see http://nldr.library.ucar.edu/metadata/osm/1.1/schemas/vocabs/dateType.xsd
dateTypeVocabs =     [
		"Fiscal",
		"Published",
		"Accepted",
		"Created",
		"Digitized",
		"In press",
		"Modified",
		"Reviewer assigned",
		"Submitted"
	]

reportFields = ['recId', 'dcsstatus', 'resourceType'] + dateTypeVocabs

def noFiscalDatePredicate (searcher, result):
	return not result.payload.getTypedDate("Fiscal")
		

	
class NoFiscalResult (OsmSearchResult):
	
	def __init__ (self, element):
		OsmSearchResult.__init__ (self, element)
		self.resourceType = self.payload.getTitleType()
	
	def report (self):
		fields = "recId"
		
		"""
		fields are id, dcsstatus, dcsstatusNote, <other dates>
		"""
		s=[];add=s.append
		for attr in ['recId', 'dcsstatus', 'resourceType']:
			add (getattr (self, attr))
			
		#report the other dateFields for this osmRecord
		dateMap = self.payload.getDateMap()
		if dateMap:
			for dateType in dateTypeVocabs:
				if not dateMap.has_key(dateType):
					add ("")
					continue
				values = dateMap[dateType]
				if not type(values) == type([]):
					values = [values]
				add (', '.join (values))
		return '\t'.join(s)

	
class NoFiscalDateSearcher (RepositorySearcher):
	
	numToFetch = 2000
	batchSize = 200
	searchResult_constructor = NoFiscalResult
	filter_predicate = noFiscalDatePredicate
	baseUrl = "http://nldr.library.ucar.edu/schemedit/services/ddsws1-1"
	verbose = True
	dowrite = 0
	
	def __init__ (self, collection=None, xmlFormat='osm'):
		RepositorySearcher.__init__(self, collection, xmlFormat)
		
	def get_params (self, collection, xmlFormat):
		return {
			"verb": "Search",
			"collection" : "osgc",
			"dcsStatus" : "Done",
			'storedContent':['dcsstatus','dcsstatusNote'],
			"ky": collection
		}

	def processResults (self):
		if self.dowrite:
			self.write()
		else:
			print self.report()
		
	def report (self):
		s=[];add = s.append
		add ('\t'.join (reportFields))
		for result in self:
			add (result.report())
		return '\n'.join(s)
		
	def write (self):
		outpath = "output/noFiscalDateReport.txt"
		fp = codecs.open (outpath, 'w', 'utf-8')
		fp.write (self.report())
		fp.close()
		print "wrote to %s" % outpath
		
if __name__ == '__main__':
	# results = NoFiscalDateSearcher('ams-pubs')
	results = NoFiscalDateSearcher(['osgc'])
	results.report()

	


