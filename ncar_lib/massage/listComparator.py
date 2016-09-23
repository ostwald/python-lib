"""
list comparator - tools for comparing lists

doTally - returns two Tally instances:
	instNames
	instDivisions
	
	to get the unique values for a Tally, call getKeys()
"""
import os, sys
from UserList import UserList
import instMap
from instNameReporter import doTally    #see doc above about doTally

class MyList (UserList):
	
	def __init__ (self, members, name):
		UserList.__init__ (self, members)
		self.name = name

class ListComparator:
	
	def __init__ (self, list1, list2, list1_name=None, list2_name=None):
		self.list1 = MyList (list1, list1_name or "list1")
		self.list2 = MyList (list2, list2_name or "list2")
		
	def compareLength (self):
		print "length comparison"
		len1 = len (self.list1)
		len2 = len (self.list2)
		if len1 != len2:
			print "\t %s: %d, %s: %d" % (self.list1.name, len1, self.list2.name, len2)
		else:
			print "\t EQUAL (%d)" % len1
		return len1.__cmp__(len2)
			
	def reportOverlap (self):
		self.reportMissing (self.list1, self.list2)
		self.reportMissing (self.list2, self.list1)
		
	def getCommon (self):
		common=[];add=common.append
		for item in self.list1:
			if item in self.list2:
				add (item)
		return common
		
	def reportCommon (self):
		common = self.getCommon()
		if common:
			print "\nPresent in BOTH lists (%d)" % len(common)
			for item in common:
				print '\t', item
		else:
			print "\nThere were NO COMMON values"
		
	def getMissing (self, a, b):
		missing=[];add=missing.append
		for item in a:
			try:
				if not item in b:
					add (item)
			except:
				print "choked with ", item
				sys.exist()
		return missing
		
	def reportMissing (self, a, b):
		missing = self.getMissing (a, b)
		if missing:
			missing.sort()
			print '\nthe following %d items are present in "%s" but missing in "%s"' % (len(missing), a.name, b.name)
			for m in missing:
				print "\t", m
		else:
			print 'all items in "%s" are present in "%s"' % (a.name, b.name)
			
	def report (self):
		if self.compareLength ():
			self.reportOverlap ()
		self.reportCommon()
		
def compareMappings (field=None):
	katy = instMap.getKatyMap()
	faith = instMap.getFaithMap()
	katyList = field and katy.getMappingValues(field) or katy.values()
	faithList = field and faith.getMappingValues(field) or faith.values()
	comparator = ListComparator (katyList, faithList, katy.name, faith.name)
	comparator.report()
	
def getInstMap ():	
	return instMap.getInstMap ("combo")
	
def compareDataWithMap ():
	instNamesTally, instDivisionsTally, publishers, scientificDivisions = doTally()

	dataInstNames = instNamesTally.keys()
	# mapInstNames = getInstMap ().getInstNames()
	# comparator = ListComparator (mapInstNames, dataInstNames, "mapping Inst Names", "metadata Inst Names")
	mapOriginals = getInstMap ().getOriginalNames()
	comparator = ListComparator (mapOriginals, dataInstNames, "mapping Originals", "metadata Inst Names")
	comparator.report()
	
def publisherVsOriginals ():
	instNamesTally, instDivisionsTally, publishers, scientificDivisions = doTally()
	# publishers.report()
	# scientificDivisions.report()
	
	# compare publishers with mapping instDiv
	comparator = ListComparator (publishers.keys(), getInstMap().getOriginalNames(), "publishers", "orginals")
	comparator.report()
	
if __name__ == '__main__':
	publisherVsOriginals()
	

