"""
	Version 1.0 upgrader
	
	- new class for working with dcs_data version1.0 records
		1.0 records have ndrInfo element with children:
			- ndrHandle
			- lastSync
			- syncError
	- also includes conversion utility that will upgrade a directory
	  tree of 0.0.4 records to 1.0. This utility should be run before
	  starting DCS with new DcsData readers, etc installed.
	  - create new element "ndrInfo"
	  - populate ndrHandle if present in original record
	    - delete old ndrHandle element
		- set lastSyncDate to "lastTouchDate"
      - update schemaLocation to point to new schema

   NOTE: at some point, we'll have to again run through the dcs-data records
   to change the schemaLocation to "genericize" it??
"""
import os, string
from JloXml.DcsDataRecord import DcsDataRecord

class BatchUpdaterOFF:
	
	def __init__ (self, basedir):
		self.basedir = basedir
		self.update (self.basedir)
		
	def update (self, dir):
		print "updating %s" % os.path.split(dir)[1]
		for filename in os.listdir(dir):
			root, ext = os.path.splitext (filename)
			path = os.path.join (dir, filename)
			if os.path.isdir (path):
				self.update (path)
			else:
				if ext.upper() != ".XML" or root[0] == '.': continue
				# print "file: %s" % filename
				rec = DcsDataRecord_v1 (path=path)
				if 0:
					rec.update()
					rec.write ()
					print "\tupdated " + filename
				else:
					rec.probe()
			

class DcsDataRecord_v1 (DcsDataRecord):
	schemaUri = "http://www.dpc.ucar.edu/people/ostwald/Metadata/dcs-data/dcs-data-v1-0-0.xsd"
		
	def getOldNdrHandle (self):
		return self.selectSingleNode (self.dom, DcsDataRecord.ndrHandle_path)
		
	def update (self):
		self.setNoNamespaceSchemaLocation (self.schemaUri)
		oldHandleElement = self.getOldNdrHandle()
		if oldHandleElement:
			ndrHandle = self.getText (oldHandleElement)
			oldHandleElement.parentNode.removeChild(oldHandleElement).unlink()
			self.makeNdrInfo (ndrHandle)
			
		isValid_el = self.selectSingleNode (self.dom, "dcsDataRecord:isValid")
		if isValid_el:
			isValid_el.parentNode.removeChild(isValid_el).unlink()
		badChars_el = self.selectSingleNode (self.dom, "dcsDataRecord:badChars")
		if badChars_el:
			badChars_el.parentNode.removeChild(badChars_el).unlink()

		self.removeExtraNDRInfos ()

	def removeExtraNDRInfos (self):
		ndrInfos = self.selectNodes (self.dom, "dcsDataRecord:ndrInfo")
		print "%d ndrInfos found" % len (ndrInfos)

		if len(ndrInfos) > 1:
			for info in ndrInfos[1:]:
				print "removing: %s" % info.toxml()
				info.parentNode.removeChild(info).unlink()

def updateTester(path):
	rec = DcsDataRecord_v1 (path)
	rec.update()
	print rec

def batchUpdateTester ():
	baseDir = "dcs_data"
	BatchUpdater(baseDir)
	
if __name__ == "__main__":
	path = "test.xml"
	updateTester(path)

