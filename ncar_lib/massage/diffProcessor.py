"""

Make file containing mappings from library_dc records to webcat records, including accessionNums

- Walk a collection directory. For each library_dc record:
-- getID, derive accessionNum from url
-- get corresponding webcat record. from webcat record, 
--- getID, accessionNum

if accession nums don't match - throw exception

"""

import os, sys
import globals, utils
from frameworks import LibraryDCRec, WebcatRec
import baseProcessor
from callbackProcessor import CallbackCollectionProcessor, CallbackMetadataProcessor
from recordIdListProcessor import UnchangedRecordsProcessor, ChangedRecordsProcessor

class RecordProcessor (baseProcessor.RecordProcessor):
	"""
	compare current and old library_dc records!
	"""

	def isDifferent (self):
		return cmp (self.lib_dc_rec.doc.toxml(), self.ncar_rec.doc.toxml())		
	
class CollectionProcessor (CallbackCollectionProcessor):
	rpClass = RecordProcessor
				
class MetadataProcessor (CallbackMetadataProcessor):
	cpClass = CollectionProcessor
			
def different (rp):
	if rp.isDifferent ():
		print "\n%s" % rp.recId
		print diff(rp)
		
def getFields ():
	skip_fields = [
		'dc:subject',
		'library_dc:instDivision',
		'library_dc:instName',
		'dc:contributor',
		'dc:date',
		'dc:creator',
		'library_dc:date_digitized',
		'dc:language',
		'dc:rights'
		]
	fields = []
	for field in globals.library_dc_fields:
		if not field in skip_fields:
			fields.append(field)
	return fields
		
def diff (rp):
	utils.library_dc_diff (rp.lib_dc_rec, rp.ncar_rec, "working", "ncar", getFields())
	
callback = diff
	
def recordProcessorTester ():
	id = "TECH-NOTE-000-000-000-006"
	utils.getRecordPath (id)
	rp = RecordProcessor (path)
	print "id: %s, accessionNum: %s" % (rp.recId, rp.accessionNum)
	diff(rp)	
		
def collectionProcessorTester():
	CollectionProcessor ("manuscripts", diff)
	
def diffUnchangedRecords():
	UnchangedRecordsProcessor (diff)
	
if __name__ == "__main__":
	# collectionProcessorTester()
	# MetadataProcessor(diff)
	# changedRecords.report()
	diffUnchangedRecords()
