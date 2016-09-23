"""
read an xml doc of pubSpecInfos
"""
import sys, os
from UserList import UserList
from JloXml import XmlUtils, XmlRecord
from ncar_lib.osm import OsmRecord

dowrites = 0

class ChangeSpec:
	
	attrs = ['recId', 'collection', 'xmlFormat']
	
	def __init__ (self, element):
		self.term = XmlUtils.getText(element)
		for attr in self.attrs:
			setattr (self, attr, element.getAttribute (attr));
		
	def __repr__ (self):
		s = "\n%s" % self.term
		for attr in self.attrs:
			s+= "\n - " + getattr(self, attr)
		return s
		
class MetadataUpdater(UserList):
	
	osgc_dir = '/home/ostwald/Documents/NCAR Library/OpenSky/NLDR REPO Update - 11_2010/2010_11_26/records_backup/ttambora/osgc'
	
	def __init__ (self, path="output/MetadataModifySpecs.xml"):
		UserList.__init__ (self)
		if not os.path.exists(path):
			raise IOError, "output does not exist at %s" % path
		updateInfoDoc = XmlRecord(path=path)
		updateInfos = updateInfoDoc.selectNodes (updateInfoDoc.dom, "changeSpecs:pubNameSpec")
		print "%d specs found" % len(updateInfos)
		for info in updateInfos:
			changeSpec = ChangeSpec (info)
			print changeSpec
			self.updateMetadata (changeSpec)
			
	def updateMetadata (self, spec):
		
		path = os.path.join (self.osgc_dir, spec.recId+'.xml')
		rec = OsmRecord(path=path)
		rec.setPubName (spec.term, "Proceedings")
		if dowrites:
			rec.write()
			print "wrote to %s (%s)" % (spec.recId, spec.collection)
		else:
			print "WOULD'VE WRITTEN to %s (%s)" % (spec.recId, spec.collection)			

			
if __name__ == '__main__':
	MetadataUpdater()
