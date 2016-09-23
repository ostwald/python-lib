"""
propcess pairs (these are KNOWN DUPLICATES since they have the same pubsID)

fetch record infos from 'not-fy10' and 'pubs-ref'
match them up by their pubsIds

report
eventually, if useful, view side-by-side
"""
from rec_info import CollectionInfo
from UserDict import UserDict

class CollectionMap (UserDict):
	
	def __init__ (self, key):
		self.data = {}
		self.key = key
		collection = CollectionInfo (self.key)
		for rec in collection:
			if rec.pubsId:
				self[rec.pubsId] = rec
				
	def __getitem__ (self, attr):
		if not self.data.has_key(attr):
			return None
		return self.data[attr]

notFy10 = CollectionMap ('not-fy10')
pubsRef = CollectionMap ('pubs-ref')

for pubsId in notFy10.keys():
	notFy10Rec = notFy10[pubsId]
	pubsRefRec = pubsRef[pubsId]
	
	if notFy10Rec and pubsRefRec:
		print '\n%s\n\t%s\n\t%s' % (pubsId, notFy10Rec, pubsRefRec)
