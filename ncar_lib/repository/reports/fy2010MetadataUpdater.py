"""
read a list of recordIDs, and assign "2010" as fiscal Date for each record
"""
import sys, os
from UserList import UserList
from JloXml import XmlUtils, XmlRecord
from ncar_lib.osm import OsmRecord

dowrites = 0

osgc_dir = '../../osm/vocabs/pub_name'
		
def updateMetadata (recId):
	
	path = os.path.join (osgc_dir, recId+'.xml')
	rec = OsmRecord(path=path)
	
	if rec.getTypedDate("Fiscal"):
		raise ValueError, "%s already has a fiscal date" % recId
	
	rec.setDate ("2010", "Fiscal")
	if dowrites:
		rec.write()
		print "wrote to %s (%s)" % (recId)
	else:
		print "WOULD'VE WRITTEN to %s" % (recId)	
		print rec

class MetadataUpdater(UserList):
	
	def __init__ (self, path="output/fy2010UpdateInfo.txt"):
		UserList.__init__ (self)
		if not os.path.exists(path):
			raise IOError, "upfate info does not exist at %s" % path
		ids = open (path, 'r').read().split('\n')
		print "%d recs read from %s to %s" % (len(ids), ids[0], ids[-1])
		for recId in ids:
			updateMetadata (changeSpec)
			
			
if __name__ == '__main__':
	# MetadataUpdater()
	id = '007'
	updateMetadata (id)
