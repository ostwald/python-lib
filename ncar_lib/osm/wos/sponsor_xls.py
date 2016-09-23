"""
WOS spreadsheet reader
"""
import sys, os
from xls import WorksheetEntry, XslWorksheet
from UserDict import UserDict

class SponsorXlsRecord (WorksheetEntry):

	def __init__ (self, data, schema):
		WorksheetEntry.__init__(self, data, schema)
		self.sponsor = self['sponsor (wos 2011)']
		self.instname = self['Existing OSM instName']
	
class SponsorXlsReader (XslWorksheet):
	
	verbose = 1
	linesep = '\r\n' # windows
	encoding = 'utf-8'
	
	def __init__ (self, path):
		XslWorksheet.__init__ (self, entry_class=SponsorXlsRecord)
		self.read (path)
		self.lookup = UserDict()
		for item in self:
			self.lookup[item.sponsor] = item.instname
			
	def getInstName (self, sponsor):
		return self.lookup[sponsor]
			
		
if __name__ == '__main__':
	data_path = 'real_data/wosSponsorLook-up-2011.txt'
	reader = SponsorXlsReader(data_path)
	for item in reader:
		print '%s -> %s' % (item.sponsor, item.instname)
