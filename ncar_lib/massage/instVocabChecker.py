"""
	verify that all instName and instDivision values are contained in the
	controlled vocab as defined by "comp" and "katy" mappings
"""

import os, sys
from UserDict import UserDict
import instMap
import globals
import callbackProcessor

cp = callbackProcessor.CollectionProcessor
mp = callbackProcessor.MetadataProcessor
callbackProcessor.RecordProcessor.preprocess = 0

## --------- Accessor functions --------------
	
def getPublisher (rp):
	return rp.webcat_rec.getPublisher()
	
def getScientificDivision (rp):
	return rp.webcat_rec.getScientificDivision()
	
def getInstName (rp):
	return rp.lib_dc_rec.getInstName()
	
def getInstDivision (rp):
	return rp.lib_dc_rec.getInstDivision()

def hasInstDivision (rp):
	if getInstDivision(rp):
		showInstName(rp)
		
## --------- Reporting functions --------------	

def showInstName (rp):
	print "\n%s" % rp.recId
	print "\tinstName: %s" % getInstName(rp)
	print "\tinstDivision: %s" % getInstDivision(rp)

def showInstName (rp):
	print "\n%s" % rp.recId
	print "\tinstName: %s" % getInstName(rp)
	print "\tinstDivision: %s" % getInstDivision(rp)

def verifyRecInstVocab (rp):
	
	badInstNames = None
	badInstDivs = None
	
	# comment following to skip that check
	# badInstNames = getBadInstNames(rp)
	badInstDivs = getBadInstDivs (rp)

	if badInstNames or badInstDivs:
		print "\n", rp.recId
		if badInstNames:
			print "bad InstNames"
			for name in badInstNames:
				print "\t'%s'" % name
		if badInstDivs:
			print "bad InstDivisions"
			for name in badInstDivs:
				print "\t'%s'" % name
				
def getBadInstNames (rp):
	badInstNames = []
	recInstNames = rp.lib_dc_rec.getFieldValues ("library_dc:instName")
	for name in recInstNames:
		if not name in originals + instNames:
			badInstNames.append (name)
	return badInstNames
	
				
def getBadInstDivs (rp):
	badInstDivs = []
	recInstDivs = rp.lib_dc_rec.getFieldValues ("library_dc:instDivision")
	for name in recInstDivs:
		if not name in instDivs:
			badInstDivs.append (name)
	return badInstDivs

"""
find records having either a instName or an instDivision that isn't on
the respective controlled vocablist
"""
mapping = "combo"
vocab = instMap.getInstMap (mapping)
originals = vocab.getOriginalNames()
instNames = vocab.getInstNames()

instDivs = vocab.getInstDivs()

def checkSingleRecord ():
	path = os.path.join (globals.metadata, "library_dc/technotes", "TECH-NOTE-000-000-000-022.xml")
	rp = callbackProcessor.RecordProcessor (path)
	verifyRecInstVocab(rp)
	
if __name__ == "__main__":
	## cp ("manuscripts", verifyRecInstVocab)
	mp (verifyRecInstVocab)
	# checkSingleRecord ()


