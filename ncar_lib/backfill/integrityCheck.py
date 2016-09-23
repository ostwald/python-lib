"""
check the accessionNums in the spreadsheet for RECORDS against those known to backfiller
"""
import os, sys
from filler_imports import *
from UserDict import UserDict
from backfiller import BackFiller
from techNotePartsReader import TNSheetReader

class DuplicateKeyException (Exception):
	pass

class UniqueDict (UserDict):
	
	def __setitem__ (self, key, value):
		if self.has_key(key):
			# raise DuplicateKeyException, key
			print "Duplicate key: %s" % key
		else:
			self.data[key] = value
			
	def keys (self):
		sorted = self.data.keys()
		sorted.sort()
		return sorted

class MapComparer:
	def __init__ (self, map1, map2):
		self.map1 = map1
		self.map2 = map2
		self.allkeys = self.get_all_keys()
		
	def get_all_keys (self):
		all = self.map1.keys()
		for key in self.map2.keys():
			if not key in all:
				all.append (key)
		all.sort()
		return all
		
	def compare (self):
		"""
		report on all keys (accessionNums) that are present in one map and missing in
		another
		"""
		s = [];add=s.append
		for key in self.allkeys:
			inMap1 = key in self.map1.keys()
			inMap2 = key in self.map2.keys()
			if not inMap1 or not inMap2:
				val1 = inMap1 and self.map1[key].getIssue() or "N0"
				val2 = inMap2 and self.map2[key].issue or "N0"
				print "%s\t%25s\t%s" % (key, val1, val2)
				
	def missingLibDc (self):
		"""
		report on the accessionNums that were not retreived in the scrape
		NOTE: due to duplicate keys, all items under "NCAR/TN-85+STR" were not scraped
		"""
		for key in self.map1.keys():
		
			if not key in self.map2.keys():
				id = drNum2RecId (key)
				path = webcatUtils.getRecordPath (id)
				try:
					lib_dc_rec = LibraryDCRec (path=path)
					print "%s - %s" % (key, lib_dc_rec.getFieldValue ("dc:title"))
				except IOError:
					print "%s - no record found" % key
		
# make a map of spreadSheetItems
path = os.path.join (globals.docBase, "backfill/DR numbers for TN parts.txt")
reader = TNSheetReader (path)
itemMap = UniqueDict()
folders = reader.getFolders()
for folder in folders:
	for item in folder.children:
		drNum = item.getFieldValue("DR Number")
		if drNum != "no DR number":
			itemMap[drNum] = item
			
# make a map of folderRecords
backfiller = BackFiller()
childMap = UniqueDict()
for rec in backfiller.records:
	for child in rec.children:
		# print child.accessionNum
		childMap[child.accessionNum] = child

if __name__ == '__main__':
	# MapComparer (itemMap, childMap).missingLibDc()
	MapComparer (itemMap, childMap).compare()
		
