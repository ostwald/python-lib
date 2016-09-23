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
from recordIdListProcessor import UnchangedRecordsProcessor

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
	
if __name__ == "__main__":
	UnchangedRecordsProcessor (diff)
