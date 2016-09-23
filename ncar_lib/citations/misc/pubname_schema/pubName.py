"""
todo: 

1 - extract a list of values from the "pubName.xsd" schema
(ttambora.ucar.edu:/web/nldr/metadata/osm/1.0/schemas/vocabs/pubName.xsd)

- PubNameXSD (path="pubName.xsd").getPubNames()

2 - collect the WOS pubname values* that aren't in pubName.xsd
* titlecase, then entity-encode '&'s, the WOS pubnames

- save this list (uniqueWOSpubnames)

3 - merge and alphabetize

- save this list as mergedPubnames

4 - make new version of pubName.xsd with complet list

"""
import string
from PubNameXSD import PubNameXSD, getPubNames, setPubNames
from utils import *

class ListWorker:
	
	def __init__ (self):
		self.wosValues = getWOSValues()
		self.pubNames = getPubNames()
		self.newPubNames = mergeLists (self.pubNames, self.wosValues)
	
	def sanityCheck (self):
		diff = diffLists (self.newPubNames, self.wosValues)
		self.report (diff, "Items in NEW pubNames that aren't in WosValues")
		
		diff = diffLists (self.newPubNames, self.pubNames)
		self.report (diff, "Items in NEW pubNames that aren't in pubNames")
			
	def reportList (self, listName, showItems=0):
		self.report (getattr (self, listName), listName, showItems)
		
	def report (self, l, label, showItems=0):
		print "\n%s (%d)" % (label, len(l))
		if showItems:
			for item in l:
				print item

	def getSchema (self):
		return setPubNames (self.newPubNames)
				
if __name__ == '__main__':
	lw = ListWorker()
	# lw.reportList ("wosValues")
	# lw.reportList ("pubNames")
	lw.reportList ("newPubNames", 1)
	# lw.sanityCheck()
	
	rec = lw.getSchema()
	rec.write("newPubName.xsd")

	
