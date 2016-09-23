"""
check all items of a collection to find a bogus id
"""

import os, sys
from nsdl.ncs import NCSSearcher
from nsdl.ndr import NdrObject, NdrClient

default_baseUrl = "http://ncs.nsdl.org/mgr/services/ddsws1-1"

class ItemRecords (NCSSearcher):
	
	numToFetch = 100
	
	def __init__ (self, collection, baseUrl=default_baseUrl):
		NCSSearcher.__init__ (self, collection=collection, baseUrl=default_baseUrl)
		
class CollectionChecker:
	def __init__ (self, collection):
		print '\nchecking', collection.name
		self.valid = 1
		self.recs = ItemRecords(collection.searchKey)
		ndrClient = NdrClient()
		for rec in self.recs:
			ndrHandle = rec.dcsndrHandle
			if not ndrHandle:
				print 'ndrHandle not found for ', rec.recId
				continue
			print ndrHandle
			uniqueID = ndrClient.get(ndrHandle).uniqueID
			if uniqueID != rec.recId:
				print ('%s - %s' % (rec.recId, uniqueID))
				self.valid = 0
				break
				

