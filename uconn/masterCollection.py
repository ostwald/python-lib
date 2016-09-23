"""
Ecaspulates a collection of collection records, including

- the underlying dlese_collect collections that define the 
  collections for the DDS. These collections are not visible
  in the DCS UI.
  
- the collectionOfCollections that are maintained in the DCS.
  These special collections are used by other services (such
  as vitality) to specify the available collections and provide
  detailed information about the collections.
"""
import os, sys, time
from nsdl import NCSCollectRecord
from JloXml import DleseCollectRecord, XmlUtils
from UserList import UserList

class MasterCollection (UserList):
	"""
	exposes the items as list of instance records of
	specified record_class (e.g., NCSCollectRecord or
	DleseCollectRecord)
	"""
	def __init__ (self, masterDir, record_class):
		"""
		read in data from specified masterDir and
		instantiate items using provided record_class
		"""
		self.masterDir = masterDir
		self.record_class = record_class
		self.masterKey = os.path.basename(masterDir)
		self.data = []  # these will be record_class instances
		
		# populate data with records
		add = self.data.append
		for filename in os.listdir (self.masterDir):
			if not filename.endswith('.xml'):
				print 'skipping', filename
				continue
			path = os.path.join (self.masterDir, filename)
			add (self.record_class(path=path))	
	
	def getValues (self, field):
		"""
		returns list of field values collected from all
		item records
		"""
		# vals = filter (None, map (lambda x:x.get(self.field), self.getRecords()))
	
		vals = [];add=vals.append
		for record in self.getRecords():
			add (record.get(field))

		return filter (None, vals)
		
	def getRecords(self):
		return self.data
		
def testerGetValues():
	master = '/Users/ostwald/Desktop/DLESE_MIGRATION/NSDL/records/ncs_collect/1201216476279'
	field = 'collSetSpec'
	plucker = MasterCollection(master, NCSCollectRecord)
	values = plucker.getValues(field)
	print '%d %s values found' % ( len(values), field)
	for v in values:
		print '-', v

def getDcrPath(key):
	dcr_master = '/Users/ostwald/Desktop/DLESE_MIGRATION/DLESE/records/dlese_collect/dcr'
	master = MasterCollection(dcr_master, DleseCollectRecord)
	for col in master:
		if key == col.get('key'):
			return col.path
		
if __name__ == '__main__':
	getDcrPath('dccs')

