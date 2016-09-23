"""
read tabdelimited file, 
extract metadataHandle mappings (metadataHandle	setSpec	partnerId), 
and insert into handleResolution DB
"""
import sys, os
from tabdelimited import TabDelimitedFile, TabDelimitedRecord
from HandlesDB import HandlesDB
from HrsDB import HrsDB, MetadataMappingTable

class MetadataMapping (TabDelimitedRecord):
	"""
	exent WorksheetEntry to specify field delmiter, 
	to give class-specific attributes, etc
	"""
	def __init__ (self, data, parent):
		TabDelimitedRecord.__init__ (self, data, parent)
		self.metadataHandle = self['metadataHandle']
		self.setSpec = self['setSpec']
		self.partnerId = self['partnerId']
		# custom code for this class goes here
		
class MetadataMappings (TabDelimitedFile):
	"""
	extend XslWorksheet to overwrite methods such as 'accept'
	- specify the entry class constructor
	"""
	
	linesep = '\r\n'
	
	def __init__ (self, path):
		TabDelimitedFile.__init__ (self, entry_class=MetadataMapping)
		self.read (path)

def populate (dataPath, max_cnt=None):

	metadataTable = MetadataMappingTable (HrsDB())
	metadataTable.empty()
	errors = []
	mappings = MetadataMappings(dataPath)
	max_cnt = max_cnt is not None and max_cnt or len(mappings)
	cnt = 0
	for mapping in mappings.data:
		try:
			# print 'inserting handle: %s, url: %s' % (mapping.metadataHandle, mapping.metadataUrl)
			metadataTable.insert (mapping.metadataHandle, mapping.partnerId, mapping.setSpec)
		except Exception, exc:
			# errors.add (exc)
			print exc
		cnt = cnt + 1
		if cnt >= max_cnt:
			break
		if cnt % 100 == 0:
			print '%d/%d' % (cnt, max_cnt)

def tabdelimitedTester(path):
	mappings = MetadataMappings(path)
	rec = mappings[4]
	print rec.partnerId
	
def indexTester (path):
	metadataTable = MetadataMappingTable (HrsDB())
	metadataTable.empty()
	mappings = MetadataMappings(path)
	mapping = mappings[3]
	metadataTable.insert (mapping.metadataHandle, mapping.partnerId, mapping.setSpec)
	metadataTable.insert ('2200/20061002150104003T', mapping.partnerId, mapping.setSpec)
			
if __name__ == '__main__':
	path = 'data/metadataMappings.txt'
	# tabdelimitedTester(path)
	populate (path, 1000)
	# indexTester (path)
