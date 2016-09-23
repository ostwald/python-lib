"""
Convert OSM records 
use case: 
- tarup a directory of NLDR osm metadata collections and write to local disk
- set 'osm_records_dir' constants to point to this dir
- run convert OSM collections
- create new tarball of converted collections
- move back to NLDR
- re-index
"""
import os, sys
from osmConverter import convert

test_osm_records_dir = '/home/ostwald/python-lib/ncar_lib/osm_update_11_2010/test-data/osm'

def makeConvertedPath (path):
	return path.replace ("test-data", "converted-data")

def convertOSMcollection (collectionDir):
	outputdir = makeConvertedPath (collectionDir)
	if not os.path.exists (outputdir):
		# if not os.makedirs (outputdir):
			# raise IOError, "Could not create dir at %s" % outputdir
		os.mkdir (outputdir)
	maxcount = 100000
	mycount = 0
	for filename in os.listdir(collectionDir):
		if not filename.endswith('.xml'):
			print 'skipping file', filename
		path = os.path.join (collectionDir, filename)
		
		mycount += 1
		print "%d/%d" % (mycount, maxcount)
		if mycount > maxcount:
			print "returning"
			return
		
		rec = convert (path)

		## only necessary for testing ...
		rec.setSchemaLocation('http://test.nldr.library.ucar.edu/metadata/osm/1.1/schemas/osm.xsd',
	                          'http://nldr.library.ucar.edu/metadata/osm')
		rec.write(makeConvertedPath (path))


def convertOSMcollections (osm_records_dir):
	outputdir = makeConvertedPath (osm_records_dir)
	if not os.path.exists (outputdir):
		# if not os.makedirs (outputdir):
			# raise IOError, "Could not create dir at %s" % outputdir
		os.mkdir (outputdir)
			
	for filename in os.listdir(osm_records_dir):
		if filename.find('.') != -1:
			print 'skipping', filename
			continue
		path = os.path.join (osm_records_dir, filename)
		if not os.path.isdir(path):
			print "%s is not a collection directory: skipping" % filename
			continue
		try:
			print '\nconverting', filename
			convertOSMcollection (path)
			print "%s converted" % filename
		except:
			msg = "Collection conversion error for %s: %s" % (filename, sys.exc_info()[1])
			# print msg
			raise Exception, msg
			
	print "done converting OSM collections"
	

if __name__ == '__main__':
	# convertOSMcollections (test_osm_records_dir)
	convertOSMcollection (os.path.join (test_osm_records_dir, 'osgc'))



