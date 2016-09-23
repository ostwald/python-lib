"""

Reads in an originalDRMappings file, which contains mappings from DR_number
to RecordIds, e.g.,
	DR000659 : TECH-NOTE-000-000-000-659
	

These DR numbers were contained in the original webcat metadata, and were used
to name the NLDR Metadata Record (containing scraped metadata), as well as the
corresponding asset.

DRMappings creates a mapping from DR number to ID, and also
provides a "getId" method for obtaining the metadataID for a given DR num
"""

import os, sys
from UserDict import UserDict
from line_data_reader import LineDataReader
from dds_client import GetRecord

default_data = 'input/originalDRMappings.txt'

class DRMappings (UserDict):
	def __init__ (self, mapping_data=default_data):
		UserDict.__init__ (self)
		# lines = open(mapping_data, 'r').read().split('\n')
		# print len(lines), 'lines read'
		for line in LineDataReader (mapping_data):
			splits = line.split(':')
			dr = splits[0].strip()
			id = splits[1].strip()
			self[dr] = id
			
	def getId(self, dr):
		return self[dr]
		
	def keys(self):
		sorted = self.data.keys()
		sorted.sort()
		return sorted
		
	def get_missing_records (self):
		"""
		build list of record IDs that are in the DR Mapping but NOT
		in the NLDR/NCS
		"""
		missing = []
		for recId in self.values():
			if not recordExists(recId):
				missing.append(recId)
		return missing
		
def recordExists (recId):
	"""
	using dds_search.GetRecord, determine whether a given record exists in the NLDR (production NCS)
	"""
	baseUrl = "http://nldr.library.ucar.edu/schemedit/services/ddsws1-1"
	id = 'TECH-NOTE-000-000-000-847'
	try:
		return GetRecord(baseUrl, recId).result != None
	except:
		# print sys.exc_info()[1]
		return 0
		
if __name__ == '__main__':
	mappings = DRMappings()
	missing = mappings.get_missing_records()
	missing.sort()
	for recId in missing:
		print recId
