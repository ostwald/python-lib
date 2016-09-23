#!/usr/bin/env python
"""


"""

import os, sys
import globals, utils
from recordIdListProcessor import ChangedRecordsProcessor, UnchangedRecordsProcessor
from mergingProcessor import MergingRecordProcessor
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
	
# field_list = ['dc:publisher']
field_list = MergingRecordProcessor.ncar_keep_fields

def diff (rp):
	utils.library_dc_diff (rp.lib_dc_rec, rp.ncar_rec, "working", "ncar", field_list)
	
callback = diff
	
def showArgs ():
	for i in range(len (sys.argv)):
		print "arg[%d]: %s" % (i, sys.argv[i])
		
if __name__ == "__main__":
	# showArgs()
	if len(sys.argv) > 1:
		field_list = [sys.argv[1]]
	print "\nfield_list", field_list
	for field in field_list:
		if not field in globals.library_dc_fields:
			msg = "illegal field: " + field
			raise Exception, msg
	if len (sys.argv) >  2:
		UnchangedRecordsProcessor (diff)
	else:
		ChangedRecordsProcessor (diff)

		
