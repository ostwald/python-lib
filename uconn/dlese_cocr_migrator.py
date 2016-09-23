"""
migrate Dlese Collection of Collection Records to NSDL rep

NOTE: 
if the collection key is NOT already cataloged as an ingest setSpec,
we make a new ncs_collect record

"""
import sys, os, time
from masterCollection import MasterCollection
from nsdl import NCSCollectRecord
from JloXml import DleseCollectRecord, XmlUtils
from dleseToNcsCollectTransform import DleseToNcsCollectTransform

#Util

## Hard coded variables for NSDL collectionOfCollection recordIDs 
prefix = "NSDL-COLLECTION"
idnum_init = 3112118

def makeRecordId (prefix, idnum):
	"""
	Return a recordID to be used in NSDL collectionOfCollection
	using provided metadata prefix and id number.
	e.g., SDL-COLLECTION-000-031-121-117
	(lifted from MetaDataRecord)
	"""
	try:
		idnum = int(idnum)
	except:
		raise ValueError, "could not treat idnum (%s) as integer" % idnum
		
	if idnum > 999999999:
		raise ValueError, "idnum (%d) exceeds 999999" % idnum
	hunthousands = idnum / 1000000
	idnum = idnum - (hunthousands * 1000000)
	thousands = idnum / 1000
	# print 'thousands', thousands
	ones = idnum % 1000
	return '%s-000-%03d-%03d-%03d' % (prefix, hunthousands, thousands, ones)

class Migrator:
	
	def __init__ (self, dlese_cocr_dir, nsdl_cocr_dir):
		self.dlese_cocr = MasterCollection (dlese_cocr_dir, DleseCollectRecord)
		self.nsdl_cocr = MasterCollection (nsdl_cocr_dir, NCSCollectRecord)
		self.nsdl_setSpec_map = self.getNsdlSetSpecMap()
		self.nsdl_setSpecs = self.nsdl_setSpec_map.keys()
		self.idnum = idnum_init
	
	def getNsdlSetSpecMap (self):
		nsdl_setSpec_map = {}
		for col in self.nsdl_cocr:
			setSpec = col.get('oaiSetSpec')
			if setSpec:
				nsdl_setSpec_map[setSpec] = col
			
		return nsdl_setSpec_map
	
	def printSetSpecs(self):
		print 'nsdl setSpecs (%d)' % len(self.nsdl_setSpecs)
		if 0:
			for key in self.nsdl_setSpecs:
				print '-', key
		
	def migrate (self):
		"""
		for each dlese_collect record
		if the collection is not already cataloged in nsdl
		create a new ncs_collect record and insert in nsdl
		"""
		
		for dcr in self.dlese_cocr:
			key = dcr.get('key')
			display = key
			if key in self.nsdl_setSpecs:
				continue;
				
			# transform and write
			recordId = makeRecordId(prefix, self.idnum)
			self.idnum += 1
			# print 'transform %s - %s' % (key, recordId)
			# print ' - path: %s' % dcr.path
			transform = DleseToNcsCollectTransform(dcr.path, recordId)
			transform.write()	
			print 'transformed and wrote ', recordId
			
			
	
if __name__ == '__main__':
	ncs_collect_master = '/Users/ostwald/Desktop/DLESE_MIGRATION/NSDL/records/ncs_collect/1201216476279/'
	dlese_collect_master = '/Users/ostwald/Desktop/DLESE_MIGRATION/DLESE/records/dlese_collect/dcr'
	migrator = Migrator (dlese_collect_master, ncs_collect_master)
	migrator.printSetSpecs()
	migrator.migrate()
