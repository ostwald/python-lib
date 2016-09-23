"""
libraryDCProcessor

implements a different RecordProcessor that doesn't care about anything but the library_dc recs
"""

import os, sys
from ncar_lib.lib import globals, webcatUtils, frameworks
import callbackProcessor

## callback functions (taking RecordProcessor instance, rp, as argument)

class LibraryDCRecordProcessor:
	"""
	first, test for correspondence between id numbers of library_dc and webcat_dc recs
	
	NOTE: an error will be raised if any library_dc records do not have corresponding webcat records
	
	"""
	def __init__ (self, library_dc_path):
		self.lib_dc_rec = frameworks.LibraryDCRec (library_dc_path)
		self.recId = self.lib_dc_rec.getId()
		self.collection = os.path.basename (os.path.dirname (library_dc_path))
		self.issue = self.lib_dc_rec.getIssue()
		self.url = self.lib_dc_rec.getUrl()

CollectionProcessor = callbackProcessor.CallbackCollectionProcessor
CollectionProcessor.rpClass = LibraryDCRecordProcessor

MetadataProcessor = callbackProcessor.CallbackMetadataProcessor
MetadataProcessor.cpClass = CollectionProcessor
		
IdListProcessor = callbackProcessor.CallbackIdListProcessor
IdListProcessor.rpClass = LibraryDCRecordProcessor	

def callback (rp):
	print rp.recId
	
def missingIssue (rp):
	if not rp.issue:
		print "\n%s (%s)" % (rp.recId, rp.url)
			
if __name__ == "__main__":

	# CollectionProcessor ("manuscripts", callback)
	MetadataProcessor (missingIssue)
	# IdListProcessor (["TECH-NOTE-000-000-000-006"], callback)

	

