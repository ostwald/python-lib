"""
replace worksheet - reads tab-delimited file for a given vocab field
(pubName, instName, eventName), having two columns ("Bad Term", "Good Term")
"""
import string, os, sys, codecs
from xls import WorksheetEntry, XslWorksheet

data_worksheeet_path = "PubNames_ADD_20101202.txt"

class ReplaceEntry (WorksheetEntry):
	
	"""
	an entry from the spread sheet - two columns ("Bad Term", "Good Term")
	"""
	
	def __init__ (self, textline, schema):
		WorksheetEntry.__init__(self, textline, schema)
		self.badTerm = self['Bad Term']
		self.goodTerm = self['Good Term']
		

class ReplaceWorkSheet (XslWorksheet):
	
	linesep = "\r\n"
	# encoding = 'ISO-8859-1' # utf-8
	encoding = 'utf-8'
	
	def __init__ (self, path):
		self.path = path
		self.filename = os.path.basename (path)
		self.root, self.ext = os.path.splitext(self.filename)
		XslWorksheet.__init__ (self, entry_class=ReplaceEntry)
		self.read (path)
		# print "%d records read" % len(self)
		
	def report(self):
		print "%d records read" % len(ws)
		for rec in ws:
			print "%s -> %s" % (rec.badTerm, rec.goodTerm)
				
if __name__ == '__main__':
	path = "replace_data/eventName.txt"
	ws = ReplaceWorkSheet (path)
	ws.report()
	
