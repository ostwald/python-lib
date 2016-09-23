"""
DcsDataUpdater - insert a "setSpec" into the dcs_data record for all NSDL Collections
 - required data is in "collection_data.xml"
 - dcs_data records for NSDL Collections is in "collect" directory
""" 
import os, sys
from JloXml import XmlRecord, XmlUtils, DcsDataRecord

class CollectionInfo:
	"""
	exposes all element values in provided "collection" element
	"""
	def __init__ (self, element):
		for child in XmlUtils.getChildElements (element):
			setattr (self, child.tagName, XmlUtils.getText(child))

	def __repr__ (self):
		s=[];add=s.append
		add (self.title)
		for attr in ['recordID', 'setSpec', 'ncsStatus', 'nativeFormat', 'metadataProvider']:
			add ("  %s: %s" % (attr, getattr (self, attr)))
		return '\n'.join(s)
			
class UpdaterData (XmlRecord):
	"""
	reads XML data file and creates a list of CollectionInfo instances
	
	- also provides reports so we can examine the data
	"""
	xpath_delimiter = "/"
	data_path = 'all_collections_data.xml'
	
	def __init__ (self):
		XmlRecord.__init__ (self, path=self.data_path)
		collections = self.selectNodes (self.dom, "ncsCollections/collection")
		print '%d collections found' % len(collections)
		self.collectionInfos = []
		for collection in collections:
			info = CollectionInfo (collection)
			# recordID = XmlUtils.getChildText (collection, "recordID")
			# setSpec = XmlUtils.getChildText (collection, "setSpec")
			self.collectionInfos.append (info)
			
	def getItemsWithMissingField (self, field):
		"""
		returns list of collections that do not have a value for
		specified field
		"""
		myfilter = lambda info: not getattr(info, field).strip()
		return filter(myfilter, self.collectionInfos)
			
	def filterCollections(self, filterFn):
		return filter(filterFn, self.collectionInfos)
		
	def report (self, infos=None, verbose=1):
		"""
		print string representation of provided collection infos
		if no infos are provided, use all collection infos
		"""
		if infos is None:
			infos = self.collectionInfos
			
		print '\nReporting on %d collection infos' % len (infos)
		for info in infos:
			if verbose:
				print "\n%s" % (info)
	
def missingFieldFilter (field):
	return lambda info: not getattr(info, field).strip()
			
class Updater:
	"""
	insert set spec in the dcs_data_record
	"""
	dcs_data_dir = "1201216476279"
	max_updates = 500
	
	def __init__ (self):
		data = UpdaterData()
		for i, collection in enumerate (data.collectionInfos):
			recordID = collection.recordID
			setSpec = collection.setSpec
			self.update (recordID, setSpec)
			if i + 1 >= self.max_updates:
				break
			
	def update (self, recordID, setSpec):
		print "\nUpdating %s" % recordID
		path = os.path.join (self.dcs_data_dir, recordID + ".xml")
		dcs_data_rec = DcsDataRecord (path=path)
		ndrInfo = dcs_data_rec.getNdrInfo()
		dcs_data_rec.setSetSpec (setSpec)
		# print ndrInfo.toxml()
		if 1:
			print dcs_data_rec
		else:
			dcs_data_rec.write()
			print 'wrote %s' % recordID
			
class Verifier:
	"""
	insert set spec in the dcs_data_record
	"""
	dcs_data_dir = "1201216476279"
	max_updates = 500
	
	def __init__ (self):
		data = UpdaterData()
		for i, collection in enumerate (data.collectionInfos):
			recordID = collection.recordID
			setSpec = collection.setSpec
			self.verify (recordID, setSpec)
			if i + 1 >= self.max_updates:
				break
			
	def verify (self, recordID, setSpec):
		print "\nVerifying %s" % recordID
		path = os.path.join (self.dcs_data_dir, recordID + ".xml")
		dcs_data_rec = DcsDataRecord (path=path)
		assert dcs_data_rec.getSetSpec() == setSpec
		print "\tverified!"
	
def updaterDataTester ():
	data = UpdaterData()
	if 0:
		myFilter = missingFieldFilter('setSpec')
		noFormat = data.filterCollections()
		data.report(noFormat, 1)
	else:
		data.report()
	
if __name__ == '__main__':
	# updaterDataTester()
	# Updater()
	Verifier()
