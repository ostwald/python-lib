"""
assign statuses - traverse the dcs_data tree and assign a done status
to all records. do we have to consult the collection config to obtain the 
proper status for each collection?
"""
import os, sys, re, shutil, time
from JloXml import DcsDataRecord

host = os.environ['HOST']
# print "HOST", host

dowrites = 1
verbose = 0
	
def getDirs (path):
	return filter (lambda x:os.path.isdir(os.path.join(path, x)), os.listdir(path))
	
def updateCollection (dir_path):
	def accept (filename):
		if filename[0] == '.': return 0;
		if not filename.endswith('.xml'): return 0;
		return 1
	
	for filename in filter (accept, os.listdir(dir_path)):
		path = os.path.join (dir_path, filename)
		updateRecord(path)
		
	
def updateRecord (path):
	rec = DcsDataRecord (path=path)
	fmt = "%Y-%m-%dT%H:%M:%SZ"
	changeDate = time.strftime(fmt, time.gmtime())
	statusNote = "Set status to Done";
	editor = "admin"
	rec.addStatusEntry (changeDate=changeDate, status="Done", statusNote=statusNote, editor=editor);
	if dowrites:
		rec.write()
	else:
		print 'would have written', os.path.basename(path)
	
def walkRepo (path):
	"""
	skip dcs_data for now. it should be called as a repo, so we should call walkRepo
	with the dcs_data directory (EVENTUALLY)
	"""
	if not os.path.basename(path) == 'dcs_data':
		raise Exception, 'path must point to a dcs_data directory (%s)' % path
	
	for xmlFormat in filter (lambda x:x != 'dcs_data', getDirs(path)):
		print '\n', xmlFormat
		xmlFormatPath = os.path.join (path, xmlFormat)
		for collection in getDirs (xmlFormatPath):
			print '- ', collection
			collectionPath = os.path.join (xmlFormatPath, collection)
			updateCollection (collectionPath);

def statusTester (path):
	rec = DcsDataRecord (path=path)
	fmt = "%Y-%m-%dT%H:%M:%SZ"
	changeDate = time.strftime(fmt, time.gmtime())
	statusNote = "Set status to Done";
	editor = "admin"
	rec.addStatusEntry (changeDate=changeDate, status="Done", statusNote=statusNote, editor=editor);
	print rec
	
if __name__ == '__main__':
	print '\n-----------------------------------'
	base_path = '/Users/ostwald/devel/dcs-repos/merge-workspace/dcs-merged/records/dcs_data'
	walkRepo(base_path)
	# statusTester ()
	
	# updateCollection (os.path.join (base_path, 'concepts/chap_bscs'));

