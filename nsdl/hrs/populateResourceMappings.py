"""
read tabdelimited file, extract resourceHandle to resourceUrl mappings, and insert into handleResolution DB
"""
import sys, os
from tabdelimited import TabDelimitedFile, TabDelimitedRecord
from HandlesDB import HandlesDB
from HrsDB import HrsDB, ResourceMappingTable

class ResourceMapping (TabDelimitedRecord):
	"""
	exent WorksheetEntry to specify field delmiter, 
	to give class-specific attributes, etc
	"""
	def __init__ (self, data, parent):
		TabDelimitedRecord.__init__ (self, data, parent)
		self.resourceHandle = self['resourceHandle']
		self.resourceUrl = self['resourceUrl']
		# custom code for this class goes here
		
class ResourceMappings (TabDelimitedFile):
	"""
	extend XslWorksheet to overwrite methods such as 'accept'
	- specify the entry class constructor
	"""
	def __init__ (self, path):
		TabDelimitedFile.__init__ (self, entry_class=ResourceMapping)
		self.read (path)



def populate (dataPath, max_cnt=None):

	resourcesTable = ResourceMappingTable (HrsDB())
	resourcesTable.empty()
	errors = []
	mappings = ResourceMappings(dataPath)
	max_cnt = max_cnt is not None and max_cnt or len(mappings)
	cnt = 0
	for mapping in mappings.data:
		if not mapping.resourceUrl:
			continue
		try:
			# print 'inserting handle: %s, url: %s' % (mapping.resourceHandle, mapping.resourceUrl)
			resourcesTable.insert (mapping.resourceHandle, mapping.resourceUrl)
		except Exception, exc:
			# errors.add (exc)
			print exc
		cnt = cnt + 1
		if cnt >= max_cnt:
			break
		if cnt % 100 == 0:
			print '%d/%d' % (cnt, max_cnt)
			
if __name__ == '__main__':
	path = 'data/resourceMappings.txt'
	populate (path, 1000)
