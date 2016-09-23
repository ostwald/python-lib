"""
scan all the records in a DDS repository and perform an operation on different objects
"""
import os, sys, re, time
from ncar_lib.repository.repo_scanner import *
from JloXml.DcsDataRecord import DcsDataRecord


class Dcs_Data_CollectionScanner (CollectionScanner):
	
	item_class = DcsDataRecord
	
	def __init__ (self, path, parent=None, itemFn=None):
		# self.record_action = recordAction
		# log ("Collection: " + os.path.basename(path));
		log ('<collection key="%s">' % os.path.basename(path))
		if not itemFn:
			itemFn = recordAction
		CollectionScanner.__init__ (self, path, parent, itemFn)
		log ('</collection>')
		
class Dcs_Data_FormatScanner (FormatScanner):
	
	item_name = "collections"
	item_class = Dcs_Data_CollectionScanner

	def __init__ (self, path, parent=None):
		log ('<format name="%s">' % os.path.basename(path))
		DirectoryScanner.__init__ (self, path, parent);
		log ('</format>')

# RepositoryScanner.item_class = Dcs_Data_FormatScanner
# FormatScanner.item_class = Dcs_Data_CollectionScanner
		
class Dcs_Data_RepositoryScanner (RepositoryScanner):
	
	item_class = Dcs_Data_FormatScanner
	
	def __init__ (self, path, parent=None):
		log ('<repository name="%s">' % os.path.basename(path))
		DirectoryScanner.__init__ (self, path, parent);
		log ('</repository>')
		
def recordActionTally (dcsDataRecord):
	"""
	record the records that have a status entry in a single file
	"""
	statusEntries = dcsDataRecord.entryList
	for entry in statusEntries:
		# print '- %s (%s)' %  (entry.changeDate, entry.timeStamp)
		if entry.timeStamp < threshold:
			log ("%s (%s)" % (dcsDataRecord.getId(),  entry.changeDate) )
			return;
	
def printStatusHistory (dcsDataRecord):
	statusEntries = dcsDataRecord.entryList
	print "\n%s" % dcsDataRecord.getId()
	for entry in statusEntries:
		print "- %s (%s) - %s" % (entry.changeDate, entry.editor, entry.status)
		print '  "%s"' % entry.statusNote
	
def logStatusHistory (dcsDataRecord):
	statusEntries = dcsDataRecord.entryList
	if 0: # textual
		log ("\n%s" % dcsDataRecord.getId())
		for entry in statusEntries:
			log ("- %s (%s) - %s" % (entry.changeDate, entry.editor, entry.status))
			log ('  "%s"' % entry.statusNote)
	else:
		entriesElement = dcsDataRecord.entriesElement
		entriesElement.setAttribute ("recordId", dcsDataRecord.getId())
		log (dcsDataRecord.entriesElement.toxml())
	
def recordAction (dcsDataRecord):
	"""
	record the records that have a status entry in a single file
	"""
	statusEntries = dcsDataRecord.entryList
	for i, entry in enumerate(statusEntries):
		# print '- %s (%s)' %  (entry.changeDate, entry.timeStamp)
		if entry.timeStamp < threshold:
			
			logStatusHistory(dcsDataRecord)
			# recordActionTally(dcsDataRecord)
			# print ("-%d: %s (%s)" % (i, dcsDataRecord.getId(),  entry.changeDate))
			return;
		else:
			# print "-%d: %s" % (i, entry.changeDate)
			pass

		
timestamp_fmt = "%Y-%m-%dT%H:%M:%SZ"
## thresholdStr = "2012-05-25T00:00:0Z"
thresholdStr = "1990-01-01T00:00:00Z"
threshold = time.mktime(time.strptime (thresholdStr, timestamp_fmt))
		
print 'threshold: %s' % thresholdStr
		
class Log:
	
	def __init__ (self, path, append=False):
		self.path = path
		if not append and os.path.exists(path):
			os.remove (self.path)
			
	def log (self, s):
		fp = open (self.path, 'a')
		fp.write ("%s\n" % s)
		fp.close()
		# print ("wrote to " + self.path)
		
		
logger = Log("repo_scanner_output.txt")
log = lambda x:logger.log(x)
		
	
if __name__ == '__main__':
	# repo = 'nsdl_prod2_dcs_data'
	repo = 'dlese_dcs_data'
	# repo = 'lib_dcs_data'
	repo_base = os.path.join("/Users/ostwald/Documents/corrupt_dcs_data_11_2012", repo)
	test_collection = "math_path/1290084883129"
	
	if 0: # test collection scanner
		path = os.path.join (repo_base, test_collection)
		Dcs_Data_CollectionScanner (path)
		
	if 0: # test format scanner
		path = os.path.join (repo_base, 'msp2')
		Dcs_Data_FormatScanner(path)
		
	if 0: # test recordAction
		# path = os.path.join (repo_base, test_collection, 'BWWC-000-000-000-003.xml')
		path = os.path.join (repo_base, 'math_path/1290084883129', 'MATH-PATH-000-000-001-297.xml')
		rec = DcsDataRecord (path=path)
		recordAction (rec)
		
	if 1: # test repo scanner
		path = os.path.join (repo_base)
		Dcs_Data_RepositoryScanner(path)
