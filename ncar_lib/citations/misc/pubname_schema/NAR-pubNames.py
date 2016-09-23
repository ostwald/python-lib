"""
pubName updater

gathers pubnames from a directory of Citation records, and adds them to the 
pubName.xsd schema file
"""
import os, sys
from UserDict import UserDict
from PubNameXSD import PubNameXSD
from ncar_lib.citations import CitationReader

nar_data = "/home/ostwald/Documents/NCAR Library/Citations project/narPubNames/1259799073928"
pubname_ref_path = "/home/ostwald/Documents/NCAR Library/Citations project/narPubNames/pubName.xsd"

def getPubNameXSDValues (verbose=0):
	rec = PubNameXSD (path=pubname_ref_path)
	pubNames = rec.getPubNames()
	if verbose:
		print '%d pubNames found' % len(pubNames)
		for pn in pubNames:
			print pn
	return pubNames
	
class NarPubnames (UserDict):
	"""
	dict structure of unique pubnames and their occurrence count
	also keeps track of record ids that don't have pubnames
	"""
	def __init__ (self):
		UserDict.__init__ (self)
		self.ids = []
		self.process()
		
	def process (self):
		filenames = os.listdir (nar_data)
		for filename in filenames:
			if not filename.endswith('.xml'):
				print "!" + filename
			path = os.path.join (nar_data, filename)
			rec = CitationReader (path=path)
			pubname = rec.getPubname()
			if not pubname:
				self.ids.append (rec.getId())
			else:
				self.add (pubname)
	
	def add (self, key):
		if self.has_key (key):
			self[key] = self[key] + 1
		else:
			self[key] = 1
			
	def keys (self):
		sorted = self.data.keys()
		sorted.sort()
		return sorted
		
	def reportIds(self):
		self.ids.sort()
		print "\n(%d) Records having NO pubname" % len (self.ids)
		for id in self.ids:
			print id
			
	def getPubnames (self):
		return self.keys()
		
	def reportPubnames (self):
		print "\nUnique Pubnames"
		for pubname in self.keys():
			print "(%d) %s" % (self[pubname], pubname)
			
def getMasterList ():
	"""
	compile list of pubName values from pubName.xsd and nar pubnames
	"""
	pubNames = getPubNameXSDValues()
	npn = NarPubnames()
	for name in npn.getPubnames():
		if not name in pubNames:
			pubNames.append (name)
	pubNames.sort(lambda a, b:cmp(a.lower(),b.lower()))
	return pubNames
	
def newPubnameXSD ():
	"""
	create a new pubName.xsd with combo of unique values in masterList
	"""
	rec = PubNameXSD (path=pubname_ref_path)
	rec.setPubNames (getMasterList())
	rec.write (path="NEW_pubName.xsd")
	
	
def narTester ():
	npn = NarPubnames()
	npn.reportIds()
	npn.reportPubnames()	
	
if __name__ == '__main__':
	# newPubnameXSD()
	NarPubnames().reportIds()
