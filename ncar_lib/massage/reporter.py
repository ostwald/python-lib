#!/usr/bin/env python
"""


"""

import os, sys
import globals, utils
import recordIdListProcessor
import massagingProcessor
import messagedRecordCallbacks
import callbackProcessor
	
#--------------------------------------------------
# Define classes to process sets of records

# The record processing class for all is MassagingRecordProcessor
rpClass = massagingProcessor.MassagingRecordProcessor

class ChangedRecordsProcessor (recordIdListProcessor.ChangedRecordsProcessor):
	rpClass = rpClass

class UnchangedRecordsProcessor (recordIdListProcessor.UnchangedRecordsProcessor):
	rpClass = rpClass
	
class CollectionRecordsProcessor (callbackProcessor.CallbackCollectionProcessor):
	rpClass = rpClass
	
class AllRecordsProcessor (callbackProcessor.CallbackMetadataProcessor):
	cpClass = CollectionRecordsProcessor
	
# -------- end of recordS processing classes -----------------------------
	

rpClass.preprocess = 0 # are we massaging (pre-processing) the records?
default_callback = messagedRecordCallbacks.recId
	
def showArgs ():
	for i in range(len (sys.argv)):
		print "arg[%d]: %s" % (i, sys.argv[i])
		
# select the set of records to report over
def getRecordsProcessor (num):
	if num is 0:
		return AllRecordsProcessor
	if num == 1:
		return UnchangedRecordsProcessor
	if num == 2:
		return ChangedRecordsProcessor
	if num == 3:
		return CollectionRecordsProcessor
	else:
		msg = "could not determine recordsProcessor from '%s'" % num
		raise Exception, msg
	
usage = """Usage:
1 - callback (name of function)
2 - preprocess (anything but 0 means preprocess)
3 - records processor class (e.g., 'ChangedRecordsProcessor')
4 - collection (arg 3 must be 'CollectionRecordsProcessor' when collection is specified)
"""
		
def processCommandLine ():
	recordsProcessor = AllRecordsProcessor
	callback = default_callback
	callback_name = "default_callback"
	collection = None
	
	# showArgs()
	
	if len(sys.argv) == 1:
		print usage
		sys.exit()
	try:
		if len (sys.argv) >  1:
			callback_name = sys.argv[1]
			callback = getattr (messagedRecordCallbacks, callback_name)
		if len (sys.argv) > 2:
			rpClass.preprocess = int(sys.argv[2])
		if len (sys.argv) > 3:
			recordsProcessor = getRecordsProcessor (int(sys.argv[3]))
		if len (sys.argv) > 4:
			if recordsProcessor != CollectionRecordsProcessor:
				raise Exception, "CollectionRecordsProcessor required when collection is specified"
			collection = sys.argv[4]
			
		if recordsProcessor == CollectionRecordsProcessor and not collection:
			raise Exception, "collection must be specified when processor is CollectionRecordsProcessor"
			
		print ("\n-----------------------------------------")
		print "Reporter"
		print "\t callback: %s" % callback_name
		print "\t preprocess: %s" % rpClass.preprocess
		print "\t records processor: %s" % recordsProcessor.__name__
	except:
		print "Input error: %s" % sys.exc_info()[1]
		print "\n", usage
		sys.exit()
	
	if collection:
		print "\t collection: %s" % collection
		recordsProcessor (collection, callback)
	else:
		recordsProcessor (callback)
		pass
		
if __name__ == "__main__":
	# showArgs()
	processCommandLine ()

		
