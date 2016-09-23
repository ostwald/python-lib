"""
WOS spreadsheet reader
"""
import sys, os
from xls import WorksheetEntry, XslWorksheet
from UserDict import UserDict

class SourceXlsRecord (WorksheetEntry):

	def __init__ (self, data, schema):
		WorksheetEntry.__init__(self, data, schema)
		self.source = self['source (WOS journal) 2011']
		self.pubname = self['Existing OSM pubName'] or self['OSM pubName to Add']
	
class SourceXlsReader (XslWorksheet):
	
	verbose = 1
	linesep = '\r\n' # windows
	encoding = 'utf-8'
	
	def __init__ (self, path):
		XslWorksheet.__init__ (self, entry_class=SourceXlsRecord)
		self.read (path)
		self.lookup = UserDict()
		for item in self:
			self.lookup[item.source] = item.pubname
			
	def getNormalizedPubname (self, source):
		return self.lookup[source]
			
		
if __name__ == '__main__':
	data_path = 'real_data/wosSourceLook-up-2011.txt'
	reader = SourceXlsReader(data_path)
	for item in reader:
		print '%s -> %s' % (item.source, item.pubname)
