"""
task9 - reporter

we want to know if there are records in the repository that have a status that
is NOT reflected in the coverage dates

"""
import sys, os
from ncar_lib import OsmRecord

def isBogRecord (osmRecord):
	"""
	returns TRUE if the record does NOT have a date element corresponding to its status
	"""
	status = osmRecord.getStatus()
	if status:
		hasCoverage = osmRecord.getDate(status)
		return not hasCoverage
	return False
	
def reportOsmRecords (osmPath):
	bogRecords = []
	for collection in os.listdir(osmPath):
		print 'Processing', collection
		coldir = os.path.join (osmPath, collection)
		recfilenames = os.listdir(coldir)
		num_recs = len(recfilenames)
		for i, recfilename in enumerate(recfilenames):
			recpath = os.path.join (coldir, recfilename)
			rec = OsmRecord(path=recpath)
			if isBogRecord(rec):
				bogRecords.append(rec.getId())
			if i and i % 500 == 0:
				print '%d/%d' % (i, num_recs)
	print "\nREPORT"
	for id in bogRecords:
		print id
	
if __name__ == '__main__':
	if 0:
		path = 'test_recs/pre-task9_tester.xml'
		rec = OsmRecord(path=path)
		print "isBogus? %s" % isBogRecord(rec)
	else:
		osmPath = '/home/ostwald/tmp/osm-2012-02-02'
		reportOsmRecords (osmPath)
