"""

Make file containing mappings from library_dc records to webcat records, including accessionNums

- Walk a collection directory. For each library_dc record:
-- getID, derive accessionNum from url
-- get corresponding webcat record. from webcat record, 
--- getID, accessionNum

if accession nums don't match - throw exception

"""

import os, sys
import globals
from frameworks import LibraryDCRec, WebcatRec
from callbackProcessor import CallbackIdListProcessor
from baseProcessor import RecordProcessor

class FileIdListProcessor (CallbackIdListProcessor):
	rpClass = RecordProcessor
	
	def __init__ (self, filename, rpFunction):
		self.idFileName = filename
		self.idList = self.getIdList ()
		print "Processing %d ids" % len (self.idList)
		CallbackIdListProcessor.__init__ (self, self.idList, rpFunction)
		
	def getIdList(self):
		ids=[]
		path = os.path.join (globals.idListDir, self.idFileName)
		for line in open (path, 'r').read().splitlines():
			if line:
				ids.append (line.strip())
		return ids

class UnchangedRecordsProcessor (FileIdListProcessor):

	idFile = 'unChangedRecords.txt'

	def __init__ (self, rpFunction):
		print "\nUNchanged RecordProcessor"
		FileIdListProcessor.__init__ (self, self.idFile, rpFunction)
		
class ChangedRecordsProcessor (FileIdListProcessor):
	idFile = 'changedRecords.txt'

	def __init__ (self, rpFunction):
		print "\nCHANGED RecordProcessor"
		FileIdListProcessor.__init__ (self, self.idFile, rpFunction)
		
if __name__ == "__main__":
	# collectionProcessorTester()
	# MetadataProcessor(changed)
	IdListProcessor (lambda rp: 1)


