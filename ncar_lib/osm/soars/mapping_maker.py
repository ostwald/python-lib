import os, sys, re
from UserDict import UserDict

class MappingMaker (UserDict):
	source = "data/missing-assets-1.txt"
	
	def __init__ (self):
		UserDict.__init__ (self)
		contents = open(self.source).read();
		for item in contents.split("\n\n"):
			self.processMapping (item)
			
	def keys (self):
		sorted = self.data.keys()
		sorted.sort(lambda a, b: cmp(int(a), int(b)))
		return sorted
			
	def processMapping (self, item):
		lines = item.split('\n')
		researchID = lines[0].split(':')[0].strip()
		assetID = lines[2].split(':')[1]
		if assetID and assetID.strip():
			self[researchID] = assetID.strip()
			
	def report (self):
		for key in self.keys():
			print "%s: %s" % (key, self[key])
			
	def getAssetID (self, key):
		key = str(key)
		if self.has_key(key):
			return self[key]


if __name__ == '__main__':
	mm = MappingMaker()
	mm.report()
	print mm.getAssetID(129)
	print mm.getAssetID(130)
