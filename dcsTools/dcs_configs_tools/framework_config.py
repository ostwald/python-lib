import sys

from config_utils import *

## FrameworkConfigRecord's location has been changed!
from dcsTools.xmlFormats import FrameworkConfigRecord

class FrameworkConfigDir (ConfigDir):
	configClass = FrameworkConfigRecord
	masterKey = "framework_config"
	
	def getKey (self, rec):
		return rec.getXmlFormat()
		
	def getMaster (self):
		return self[self.masterKey]
		
	def getSlaves1 (self):
		slaves = []
		for key in self.keys():
			if key != self.masterKey:
				slaves.append ( self[key] )
		return slaves
		
	def getSlaves (self):
		slaves = self.data.keys()
		slaves.remove(self.masterKey)
		return slaves
		
	def fixall (self):
		for rec in self.values():
			recFixer ( rec )
			
	def showFile (self, key):
		print self[key]
			
	def updateSlaves (self):
		"""
		update noNamespaceSchemaLocation to match master's schemaURI
		"""
		for key in self.getSlaves():
			rec = fcd[key]
			rec.setNoNamespaceSchemaLocation (self.getMaster().getSchemaURI())
			rec.write()
		
	def integrityCheck (self):
		msgs=[];add=msgs.append
		master = self.getMaster()
		if master.getNoNamespaceSchemaLocation() != master.getSchemaURI():
			add ("Master noNamespaceSchemaLocation does not match master schemaURI")
			
		for slave_key in self.getSlaves():
			slave = self[slave_key]
			if slave.getNoNamespaceSchemaLocation() != master.getSchemaURI():
				add ("%s - SchemaLocation mismatch with master schemaURI" % slave_key)
				add ("\t" + slave.getNoNamespaceSchemaLocation())
			
		print "Integrity Check"
		if not msgs:
			print "No problems found"
		else:
			print '\n'.join (msgs)
			
	def report (self):
		master = self.getMaster()
		print "MASTER"
		print "\tnoNamespaceSchemaLocation: %s" % master.getNoNamespaceSchemaLocation()
		print "\tschemaURI: %s" % master.getSchemaURI()
		for key in self.getSlaves():
			rec = self[key]
			print "%s\n\t%s" % (os.path.basename(rec.path), rec.getNoNamespaceSchemaLocation())
			
def recFixer (rec):
	"""
	operation to perform on a framework config record
	"""
	xmlFormat = rec.getXmlFormat()
	
	if xmlFormat == "collection_config":
		rec.setSchemaURI (collection_config_schemaURI)
	elif xmlFormat == "framework_config":
		rec.setSchemaURI (framework_config_schemaURI)
	elif xmlFormat == "dcs_data":
		rec.setSchemaURI (dcs_data_schemaURI)
		
	fix_namespace(rec, framework_config_namespace, framework_config_schemaURI)
		
if __name__ == "__main__":
	dir = getFrameworksDir ("mast")
	fcd = FrameworkConfigDir (dir, 1)
	fcd.integrityCheck()
	fcd.report()
	fcd.showFile ("framework_config")

	

	
