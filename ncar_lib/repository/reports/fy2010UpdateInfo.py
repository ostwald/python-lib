"""
Generate report of all records in osgc and ams-pubs collections that do NOT have
a dateType of "Fiscal".

Report recordID, resourceType, dcsstatus, dcsstatusNote, other date info
"""

import os, sys, codecs, time
from ncar_lib import RepositorySearcher, OsmSearchResult, unionDateToSecs, OsmRecord
from JloXml import XmlUtils
from no_fiscal_date_12_5 import NoFiscalDateSearcher

def noFiscalDatePredicate (searcher, result):
	return not result.payload.getTypedDate("Fiscal")
	
	
def unionDateToStruct (dateStr):
	struct = None
	for format in [ "%Y-%m-%d", "%Y-%m", "%Y" ]:
		try:
			struct = time.strptime (dateStr, format)
			break
		except:
			# print "couldn't parse as ", format
			pass
		
	if not struct:
		raise ValueError, 'could not parse "%s" as a date' % dateStr
				
	# print time.asctime(struct)
	return struct

def unionDateToSecs (dateStr):
	struct = unionDateToStruct(dateStr)
	return int (time.mktime(struct))
	
class FY2010Result (OsmSearchResult):
	
	start = unionDateToSecs ("2009-10-01")
	end = unionDateToSecs ("2010-09-30")
	
	def isFY2010Date (self, dateStr):
		secs = unionDateToSecs (dateStr)
		return secs >= self.start and secs <= self.end
	
	def hasFY2010Date (self):
		"""
		return True if any date is between self.start and self.end
		"""
		dateMap = self.payload.getDateMap()
		if dateMap:
			for dateType in dateMap.keys():

				values = dateMap[dateType]
				if not values:
					return False
				if not type(values) == type([]):
					values = [values]
				for val in values:
					if self.isFY2010Date (val):
						# print "%s -> %s" % (dateType, val)
						return True
					else:
						# print "NOPE: %s -> %s" % (dateType, val)
						pass
		
	
class FY2010Updater (RepositorySearcher):
	"""
	search for all records having no fiscal date
	for each result, try to find ANY date that is between
	2009-10-01 and 2010-09-30, and add fiscal Date = 2010.
	so we just need a list of RecordIds ...
	"""
	numToFetch = 2000
	batchSize = 200
	searchResult_constructor = FY2010Result
	filter_predicate = noFiscalDatePredicate
	verbose = True
	dowrite = 0
	
	def __init__ (self, collection='oscg', xmlFormat='osm'):
		RepositorySearcher.__init__(self, collection, xmlFormat)
		self.recordIds = []
		
	def get_params (self, collection, xmlFormat):
		return {
			"verb": "Search",
			"collection" : "osgc",
			'storedContent':['dcsstatus','dcsstatusNote'],
			"ky": collection
		}

	def processResults (self):
		print "processing %d results" % len (self)
		self.recordIds = self.getRecordIds()
		
		if not self.dowrite:
			print self.report()
		else:
			self.write()

	def getRecordIds(self):
		ids = []
		for result in self:
			if result.hasFY2010Date():
				ids.append (result.recId)
		return ids
			
			
	def report (self):
		s=[];add = s.append
		self.recordIds.sort()
		for recId in self.recordIds:
			add (recId)
		return '\n'.join(s)
		
	def write (self):
		outpath = "output/fy2010UpdateInfo.txt"
		fp = codecs.open (outpath, 'w', 'utf-8')
		fp.write (self.report())
		fp.close()
		print "wrote to %s" % outpath
		
if __name__ == '__main__':
	results = FY2010Updater(['osgc'])

	


