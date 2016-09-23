"""
data reader
"""
import os, sys
from tabdelimited import TabDelimitedFile, TabDelimitedRecord
from vocab_counter import VocabCounter

class DataRecord (TabDelimitedRecord):
	"""
	exent WorksheetEntry to specify field delmiter, 
	to give class-specific attributes, etc
	"""
	def __init__ (self, data, parent):
		TabDelimitedRecord.__init__ (self, data, parent)
		
		# custom code for this class goes here
		self.before = self['Change from and remove from schema']
		self.after = self['Change to']
 
        
class DataTable (TabDelimitedFile):
	"""
	extend XslWorksheet to overwrite methods such as 'accept'
	- specify the entry class constructor
	"""
	linesep = '\n'
	
	def __init__ (self, path):
		print 'DataTable: "%s"' % path
		TabDelimitedFile.__init__ (self, entry_class=DataRecord)
		self.read (path)
		self.beforeMap = {}
		for record in self:
			self.beforeMap[record.before] = record
			
	def getAfter (self, before):
		return self.beforeMap[before].after
		
	def getVocabTerms (self):
		terms = self.beforeMap.keys();
		terms.sort()
		return terms
		
def reportVocabOccurances (field, dataTable):
	print 'VocabOccurances Report'
	print '   field: %s\n' % field
	for item in dataTable:
		counter = VocabCounter(field, item.before)
		print "%d - %s" % (counter.numRecords, item.before)
		
if __name__ == '__main__':
	person_field = '/record/contributors/person/affiliation/instDivision'
	org_field = '/record/contributors/organization/affiliation/instDivision'
	path = 'division-name-changes.txt'
	dataTable = DataTable (path)
	print 'data table has %d records' % len(dataTable)
	# for rec in dataTable:
		# print '\nbefore: %s\nafter:%s' % (rec.before, rec.after)
	if 0:	
		for field in [person_field, org_field]:
			reportVocabOccurances (field, dataTable)
