"""
29623 records read
8314 peids are unique


"""
import sys, os, re, time
from tabdelimited import TabDelimitedFile, TabDelimitedRecord
from UserDict import UserDict

default_data = "data/ramey_Location_History_April2012_FINAL.txt"

class iVantageRecord (TabDelimitedRecord):
	
	def __init__ (self, data, parent):
		TabDelimitedRecord.__init__ (self, data, parent)
		self.name = self['Name']
		self.peid = self.getInt('PEID')
		self.start = self['Location Start Date']
		self.end = self['Location End Date']
		self.entity = self['Entity']
		self.lab = self['Lab']
		self.org = self['Org Unit']
		self.divProg = self['DivProg']
		self.divCode = self['Div Code']
		
	def getInt (self, attr):
		try:
			return int(self[attr])
		except:
			return 0

	def __repr__ (self):
		return '%s\t%s' % (self.peid, self.name)
		
class iVantageDataTable (TabDelimitedFile):
	verbose = 0
	linesep = "\r"
	# how files are read and written (prefer utf-8, but sometimes only ISO-8859-1 works)
	encoding = 'ISO-8859-1' # utf-8
	max_to_read = None
	
	def __init__ (self, path=None):
		self.path = path or default_data
		self.uniquePeids = []
		TabDelimitedFile.__init__ (self, entry_class=iVantageRecord)
		print "max to read: ", self.max_to_read
		self.read(self.path)
		print "%d ivantage records read" % len(self)

	def add (self, rec):
		self.append (rec)
		if rec.peid not in self.uniquePeids:
			self.uniquePeids.append(rec.peid)
		
if __name__ == '__main__':
	table = iVantageDataTable()
	print "%d records read" % len(table)
	print "%d peids are unique" % len(table.uniquePeids)
