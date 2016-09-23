"""
for each WOS record, search for dups in the osgc collection

- use titleKey to match on titles
- refine results using pubName
"""

import sys, os, re, codecs
from tabdelimited import TabDelimitedFile, TabDelimitedRecord
from ncar_lib.repository import RepositorySearcher, OsmSearchResult
from ncar_lib.osm.wos import SourceXlsReader
from UserDict import UserDict
from UserList import UserList

report_schema = ['title', 'pubName', 'wosId', 'titleMatches', 'titleAndPubnameMatches', 'authors']

def getTitleKey (title):
	"""
	cast title to lower case and then remove all non-alphas
	"""
	s = ""
	for ch in title.lower():
		if ord(ch) >= 97 and ord(ch) <= 122:
			s = s + ch
	return s

class WosRecord (TabDelimitedRecord):
	"""
	represents a record from the WOS data spreadsheet
	exposes:
		- title
		- wosId
		- pubName
	"""
	
	def __init__ (self, data, parent):
		TabDelimitedRecord.__init__ (self, data, parent)
		self.title = self['title']
		self.pubName = self.parent.sourceToPubName(self['source'])
		self.wosId = self['wos id']
		self.titleKey = getTitleKey(self.title)
		self.authors = self['author full name']

class WosDataFile (TabDelimitedFile):
	
	verbose = 1
	linesep = '\r\n' # windows
	encoding = 'utf-8'
	
	source_data_path = '../real_data/wosSourceLook-up-2011.txt'
	
	def __init__ (self, path):
		self.source_reader = SourceXlsReader(self.source_data_path)
		TabDelimitedFile.__init__ (self, entry_class=WosRecord)
		self.read (path)
		
	def sourceToPubName (self, source):
		return self.source_reader.getNormalizedPubname(source)

class RecordDupsFinder (RepositorySearcher):
	"""
	filter out records having dcs status of "Deaccessioned" (see filter_predicate)
	"""
	searchResult_constructor = OsmSearchResult
	verbose = 0
	
	def __init__ (self, titleKey):
		self.titleKey = titleKey
		RepositorySearcher.__init__ (self, collection='osgc', xmlFormat='osm')
		
	filter_predicate = lambda self,x:x.dcsstatus != 'Deaccessioned'
		
	def get_params (self, collection, xmlFormat):
		"""
		define the params used to query the search service
		"""
		return {
			'q':'dcsosmFlattenedTitle:"%s"' % self.titleKey,
			"verb": "Search",
			"xmlFormat": xmlFormat,
			"ky": collection,
			"storedContent":['dcsstatus', 'dcsstatusNote', 'dcsisValid']
			}
		
class DupReportRec:
	"""
	stores information to create dup report
	
	title, pubName (from WOS)
	wosId
	title matches (recordId's separated by commas)
	titleAndPubName matches (recordId's separated by commas)
	"""
	
	def __init__ (self, wosRecord):
		self.wosId = wosRecord.wosId
		self.title = wosRecord.title
		self.pubName = wosRecord.pubName
		self.titleMatches = []
		self.titleAndPubnameMatches = []
		self.authors = wosRecord.authors
			
	def toTabDelimited (self):
		fields = []
		for attr in report_schema:
			value = getattr(self, attr)
			if type(value) == type([]):
				value = ','.join(value)
			fields.append(value)
		return '\t'.join(fields)
			
		
class WosDupsFinder (UserList):
	"""
	traverse the WOS data spreadsheet to find dups for each record
	"""
	
	dowrites = 1
	
	def __init__ (self):
		self.data = []

		data_path = '../real_data/wos_ncar-ucar_fy11.txt'
		reader = WosDataFile(data_path)
		recs_to_report = reader.data
		for i, wosRecord in enumerate(recs_to_report):
			# print item.titleKey
			dupReportRec = DupReportRec (wosRecord)
			titledups = RecordDupsFinder(wosRecord.titleKey)
			dupReportRec.titleMatches = map (lambda x:x.recId, titledups.data)
			# print '%d dups found' % len(dups)
			
			# find which of the records match BOTH titleKey and pubName
			titleAndPubnameMatches = []
			for dup in titledups:
				if dup.payload.getPubName() == wosRecord.pubName:
					titleAndPubnameMatches.append(dup.recId)
			dupReportRec.titleAndPubnameMatches = titleAndPubnameMatches
			
			## print dupReportRec.toTabDelimited()
			self.append(dupReportRec)
			if i % 50 == 0:
				print '%d/%d' % (i, len(recs_to_report))

	def toTabDelimited (self):
		lines = []
		lines.append ('\t'.join(report_schema))
		for rec in self:
			lines.append(rec.toTabDelimited())
		content = '\n'.join (lines)
		if self.dowrites:
			fp = codecs.open ("DUPS.xls", 'w', 'utf-8')
			fp.write (content)
			fp.close()
		else:
			print content
		
		
		
if __name__ == '__main__':

	if 1:
		df = WosDupsFinder()
		df.toTabDelimited()
	
	if 0:
		# title='Coupling between the Arctic middle and upper atmosphere during the IPY 2007-2008 winter'
		title='A frequent-updating analysis system based on radar, surface, and mesoscale model data for the Beijing 2008 forecast demonstration project'
		dups = RecordDupsFinder(getTitleKey(title))
		print '%d dups found' % len(dups)
		print map (lambda x:x.recId, dups)
			
				
