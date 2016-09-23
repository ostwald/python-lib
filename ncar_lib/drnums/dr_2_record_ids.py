"""
Map DR Numbers to NCS Record IDs

1 - get list of DR numbers from DRMappings
2 - for each DR Number
	if we have a hand-mapping, use that
	otherwise, 
	- convert DR to AssetId
	- use search service to locate the record with the assetUd
	- associate DR with found record
"""
import os, sys, re
from dr_mappings_maker import DRMappings
from line_data_reader import LineDataReader
from UserDict import UserDict
from dds_asset_search import AssetRecordGetter, AssetRecordGetterException
import utils

class SortedUserDict (UserDict):
			
	def keys(self):
		sorted = self.data.keys()
		sorted.sort()
		return sorted
		
class HandMappings (SortedUserDict):
	# use LineDataReader to get lines
	
	def __init__ (self):
		UserDict.__init__ (self)
		lines = LineDataReader ("input/DR_Num_Hand_mappings.txt")
		# lines.report()
		for line in lines:
			splits = line.split(' - ')
			drNum = splits[0].strip()
			recId = splits[1].strip()
			self[drNum] = recId

		
class DR2RecIdMappings(UserDict):
	
	rootElementName = "dr_2_recId_mappings"
	
	def __init__ (self):
		UserDict.__init__ (self)
		self.errors = []
		self.handMappings = HandMappings()
		self.drNumbers = DRMappings().keys()
		
	def keys (self):
		sorted = self.data.keys()
		sorted.sort()
		return sorted
		
	def populate (self):
		"""
		populate the composite DR map
		- handmapped DRs are taken as is
		
		- DRMappings try to find the RecordID associated with a DR number by
		converting DR to asset id and then using webservice to find the record
		in which this asset is cataloged
		"""
		for drNum in self.drNumbers:
			if drNum in self.handMappings.keys():
				# take handMappings verbatim
				self[drNum] = self.handMappings[drNum]
			else:
				idNum = utils.getIdNum (drNum)
				assetId = utils.makeId ("asset", idNum)
				try:
					result = AssetRecordGetter (assetId).result
					self[drNum] = result.recId
					print "%s -> %s" % (drNum, self[drNum])
				except AssetRecordGetterException:
					self.errors.append(sys.exc_info()[1])

	def report(self):
		print "there were %d errors" % len(self.errors)
		for err in self.errors:
			print err
				
	def populateMappingElement (self, element, drNum):
			element.setAttribute ("drNumber", drNum)
			element.setAttribute ("recordID", self[drNum])
			
	def asXml (self):
		from JloXml import XmlRecord, XmlUtils
		import time
		rec = XmlRecord (xml="<%s />" % self.rootElementName)
		root = rec.doc
		root.setAttribute ("date", time.asctime())
		for drNum in self.keys():
			mappingEl = rec.addElement (root, "mapping")
			self.populateMappingElement (mappingEl, drNum)
		
		return rec
			
def tester ():
	mappings = DR2RecIdMappings()
	mappings.update ({
		'DR000799' : 'MANUSCRIPT-000-000-000-799',
		'DR000800' : 'MANUSCRIPT-000-000-000-800',
		'DR000801' : 'MANUSCRIPT-000-000-000-801'
		})
	print mappings.asXml()
	
if __name__ == '__main__':
	mappings = DR2RecIdMappings()
	mappings.populate()
	print mappings.asXml()
	mappings.report()
