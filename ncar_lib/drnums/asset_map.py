"""
read files
  - named for collection (e.g., technotes.txt)
  - containing asset file names (e.g., "asset-000-000-000-022.pdf") one per line
  
exposes:
	items = list of all asset file names
	mapping of collection name (e.g., "technotes" to assets in that collection)
"""
  
import os, sys
import utils
from line_data_reader import LineDataReader
from UserDict import UserDict
from UserList import UserList

class AssetMap (UserDict):
	
	def __init__ (self, data_dir):
		UserDict.__init__(self)
		self.items = UserList()
		for datafilename in os.listdir (data_dir):
			collection = os.path.splitext (datafilename)[0]
			
			# strip the ".pdf" off of each item
			items = map (lambda x:os.path.splitext(x)[0], 
				LineDataReader(os.path.join (data_dir, datafilename)))
			self[collection] = items
			self.items += items
			
		self.items.sort()
		
	
def findUnmatchedDRNumbers ():
	"""
	Find DR numbers for which no asset is currently located
	"""
	am_items = AssetMap("nldr_data").items
	print "%d asset map items" % len(am_items)
	# print "\n e.g. '%s'" % am_items[2]
	
	from dr_mappings import DRMappings
	drmap = DRMappings()
	drnums = drmap.keys()
	print "%d dr numbers" % len (drnums)
	
	drlookup = {}
	unmatched_DRs = []
	for dr in drmap.keys():
		idNum = utils.getIdNum (dr)
		#print "idNum: ", idNum
		assetId = utils.makeId ("asset", idNum)
		#print "assetId: ", assetId
		if assetId not in am_items:
			unmatched_DRs.append (dr)
			
	unmatched_DRs.sort()
	return unmatched_DRs
		
			
if __name__ == '__main__':
	un = findUnmatchedDRNumbers()
	for dr in un:
		print dr

