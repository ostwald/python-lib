import os, sys
from UserDict import UserDict
import globals
import callbackProcessor
from tally import Tally

cp = callbackProcessor.CollectionProcessor
mp = callbackProcessor.MetadataProcessor
callbackProcessor.RecordProcessor.preprocess = 0

class FieldList (UserDict):
	
	def __init__ (self):
		UserDict.__init__ (self)
	
	def keys(self):
		sorted = self.data.keys()
		sorted.sort()
		return sorted

class MultiFields:
	"""
	
	webcat and library_dc are mappings of multivalue fields to their number of
	occurances
	
	"""
	def __init__ (self, webcat, library_dc):
		self.webcat = webcat
		self.library_dc = library_dc
		
	def isEmpty (self):
		return len(self.webcat) == 0 and len(self.library_dc) == 0
		
## --------- Accessor functions --------------
	
def getMultiValueFields (rp):
	"""
	returns mapping of field to numFieldValues
	"""
	webcat = FieldList()
	for field in globals.webcat_fields:
		count = rp.webcat_rec.numFieldValues(field)
		if count > 1:
			webcat[field] = count
			
	library_dc = FieldList()
	for field in globals.library_dc_fields:
		count = rp.lib_dc_rec.numFieldValues(field)
		if count > 1:
			library_dc[field] = count
	return MultiFields (webcat, library_dc)
		
## --------- Reporting functions --------------	

def showMultiValueFields (rp):
	multiFields = getMultiValueFields (rp)
	if not multiFields.isEmpty():
		print "\n%s" % rp.recId
		if multiFields.webcat:
			print "webcat multifields"
			for field in multiFields.webcat.keys():
				print "\t%s (%d)" % (field, multiFields.webcat[field])
		if multiFields.library_dc:
			print "library_dc multifields"
			for field in multiFields.library_dc.keys():
				print "\t%s (%d)" % (field, multiFields.library_dc[field])

		
## -------- Tally stuff --------------
""" which webcat fields had multiple values?? """
webcatMultiFieldTally = Tally ("webcatMultiFields")

def tallyMultiFields (rp):
	multiFields = getMultiValueFields (rp)
	if not multiFields.webcat: return
	for field in multiFields.webcat.keys():
		webcatMultiFieldTally.tally (field)
		
def webCatMultiFieldTally ():
	cp ("technotes", tallyMultiFields)
	mp(tallyMultiFields)
	for key in webcatMultiFieldTally.keys():
		print "\t%s (%d)" % (key, webcatMultiFieldTally[key])
				
if __name__ == "__main__":
	# cp ("technotes", showMultiValueFields)
	# mp (hasInstDivision)
	webCatMultiFieldTally()
