"""
we have a list of missing DR numbers in "backfill-notes.txt"
create a filtered version of the "DR numbers for TN parts" spreadsheet
that contains only the records for the missing DR numbers
"""
import os, sys
from filler_imports import *
from ncar_lib.lib import globals, webcatUtils
from techNotePartsReader import TNSheetReader
from spreadSheetReader import SpreadSheetReader

path = os.path.join (globals.docBase, "backfill/backfill-status.txt")
SpreadSheetReader.errorOnDups = True
reader = SpreadSheetReader (path)

for key in reader.keys():
	entry = reader[key]
	drNum = entry.getFieldValue(reader.schema[0])
	exists = entry.getFieldValue("record status")
	if not exists:
		id = drNum2RecId(drNum)
		path = webcatUtils.getRecordPath(id)
		if os.path.exists (path):
			entry.setFieldValue ("record status", 'yup')
		else:
			entry.setFieldValue ("record status", 'nope')
			
for key in reader.keys():
	entry = reader[key]
	drNum = entry.getFieldValue(reader.schema[0])
	exists = entry.getFieldValue("record status")
	print "%s\t%s" % (drNum, exists)
	
