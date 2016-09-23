"""
exports 
	TabDelimitedFile.TabDelimitedFile, TabDelimitedFile.getFieldValues
	TabDelimitedRecord.TabDelimitedRecord
	
Sample Usage:
	
class MyRecord (TabDelimitedRecord):
	\"""
	exent WorksheetEntry to specify field delmiter, 
	to give class-specific attributes, etc
	\"""
	def __init__ (self, data, parent):
		TabDelimitedRecord.__init__ (self, data, parent)
		
		# custom code for this class goes here

	
class MyTable (TabDelimitedFile):
	\"""
	extend XslWorksheet to overwrite methods such as 'accept'
	- specify the entry class constructor
	
	note on encoding: we prefer utf-8, but ISO-8859-1 seems to work 
	most often ...
	\"""
	
	verbose = 0
	linesep = "\\r"  # for macs to override os.linesep
	max_to_read = None
	encoding = 'ISO-8859-1' # utf-8
	
	def __init__ (self, path):
		TabDelimitedFile.__init__ (self, entry_class=MyRecord)
		self.read (path)
	
"""

from TabDelimitedRecord import TabDelimitedRecord
from TabDelimitedFile import TabDelimitedFile, getFieldValues, FieldList, ColumnFieldList


from csv import CsvFile, CsvRecord
