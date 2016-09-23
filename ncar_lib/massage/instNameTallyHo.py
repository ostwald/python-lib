import os, sys
from UserDict import UserDict
from tally import Tally
import globals
import callbackProcessor
from listComparator import ListComparator
from instMap import getInstMap

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

# ---------------------------

instNames = Tally ("instNames")
instDivisions = Tally ("instDivisions")
publishers = Tally ("publishers")
scientificDivisions = Tally ("scientificDivisions")

def tally (rp):
	"""
	for each record processed, tallies the following fields
	"""
	instNames.tally (getInstName (rp))
	instDivisions.tally (getInstDivision(rp))
	publishers.tally (getPublisher(rp))
	scientificDivisions.tally (getScientificDivision(rp))
	
	
def doTally (verbose=False):
	mp(tally)
	if verbose:
		instNames.report()
		instDivisions.report()
		publishers.report()
		scientificDivisions.report()
	return instNames, instDivisions, publishers, scientificDivisions
	
def compareInstDivs ():
	instNamesTally, instDivisionsTally, publishers, scientificDivisions = doTally()
	instDivVocab = getInstMap("combo").getInstDivs()
	
	# compare publishers with mapping instDiv
	comparator = ListComparator (instDivisionsTally.keys(), instDivVocab , "metadata", "instDiv vocab")
	comparator.report()
	
if __name__ == "__main__":
	# cp ("manuscripts", hasInstDivision)
	# mp (hasInstDivision)
	compareInstDivs ()
	
