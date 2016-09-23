"""
Check OSM records for the case of:
	when instDiv info is present, but there is no instName
	(in this case we will add UCAR as instName when converting)
"""
import os, sys
from ncar_lib.osm import OsmRecord

test_osm_records_dir = '/home/ostwald/python-lib/ncar_lib/osm_update_11_2010/test-data/osm'

class MissingUCARInstName (Exception):
	pass

def testOSMrecord (path):
	rec = OsmRecord (path=path)
	for contrib in rec.getContributorPeople() + rec.getContributorOrgs():
		for suffix in contrib.affiliationSuffixes:
			if contrib.needsUcarInstName(suffix):
				raise MissingUCARInstName, "instDivision present but no instName"

def testOSMcollection (collectionDir):
	
	maxcount = 10000
	mycount = 0
	failcount = 0
	failedids = []
	for filename in os.listdir(collectionDir):
		if not filename.endswith('.xml'):
			print 'skipping file', filename
		path = os.path.join (collectionDir, filename)
		
		mycount += 1
		# print "%d/%d" % (mycount, maxcount)
		if mycount > maxcount:
			break
		
		try:
			testOSMrecord (path)
		except MissingUCARInstName:
			failcount += 1
			failedids.append (os.path.splitext(os.path.basename (path))[0])
	print "%s: %d/%d instName errors" % (os.path.basename(collectionDir), failcount, mycount)
	if 1:
		failedids.sort()
		for f in failedids:
			print f

def testOSMcollections (osm_records_dir):

	for filename in os.listdir(osm_records_dir):
		if filename.find('.') != -1:
			print 'skipping', filename
			continue
		path = os.path.join (osm_records_dir, filename)
		if not os.path.isdir(path):
			print "%s is not a collection directory: skipping" % filename
			continue
		try:
			print '\ntesting', filename
			testOSMcollection (path)
		except:
			msg = "Collection testing error for %s: %s" % (filename, sys.exc_info()[1])
			# print msg
			raise Exception, msg
			
	print "done testing OSM collections"
	

if __name__ == '__main__':
	# testOSMcollections (test_osm_records_dir)
	testOSMcollection (os.path.join (test_osm_records_dir, "osgc"))
	# testOSMrecord ('test-OSM-record.xml')



