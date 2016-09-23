import os, sys
from JloXml import MetaDataRecord, XmlUtils

data_path = '/home/ostwald/Documents/NCAR Library/osm-massage-2010-03-23'

# rec_path = os.path.join (data_path, '1264439680246/MLC-000-000-000-035.xml')

# rec_path = os.path.join (data_path, '1261600535691/NAB-000-000-000-001.xml')

class OsmRecord (MetaDataRecord):

	xpath_delimiter = '/'
	id_prefix = "OSM-RECORD"
	
	id_path = 'record/general/recordID'
	
	xpaths = {
		'id' : 'record/general/recordID',
		'recordDate' : 'record/general/recordDate',
		'title' : 'record/general/title',
		'lastName' : 'record/contributors/person/lastName',
		'firstName' : 'record/contributors/person/firstName',
		'middleName' : 'record/contributors/person/middleName',
		'suffix' : 'record/contributors/person/suffix',
		'coverageDate' : 'record/coverage/date'
	}
	
	def __init__ (self, path):
		MetaDataRecord.__init__ (self, path=path)
		
	def _xpath (self, field):
		try:
			return self.xpaths[field]
		except:
			raise KeyError, "path not defined for '%s'" % field
		
	def getId(self):
		# return self.getTextAtPath (self.id_path)
		return self.get ('id')
		
	def setId(self, id):
		# self.setTextAtPath (self.id_path, id)
		self.set ('id', id)
		
	def get (self, field):
		"""
		general getter - requires 'field' path is defined in self.xpaths
		"""
		return self.getTextAtPath (self._xpath(field))
		
	def set (self, field, value):
		"""
		general-purpose setter - requires 'field' path is defined in self.xpaths
		"""
		self.setTextAtPath (self._xpath(field), value)
		
	def deleteElementsAtPath (self, xpath):
		"""
		removes all elements at specified xpath
			for example, to remove record/rights/access field
		"""
		elements = self.selectNodes (self.dom, xpath)
		if elements:
			print '%d elements found at %s' % (len(elements), xpath)
			for el in elements:
				self.deleteElement (el)
			self.write()
			print "updated %s" % self.getId()
		
def updateCollection (collection):
	"""
	update all records in collection
	"""
	dirpath = os.path.join (data_path, collection)
	for filename in os.listdir (dirpath):
		if not filename.endswith (".xml"):
			continue
		path = os.path.join (dirpath, filename)
		rec = OsmRecord(path)
		rec.deleteElementsAtPath ('record/rights/access')
		
def updateOldSoars ():
	# basedir = 'C:/Documents and Settings/ostwald/devel/dcs-instance-data/local-ndr/records/osm/soars_old'
	basedir = '/home/ostwald/tmp/soars_old'
	for filename in os.listdir (basedir):
		if not filename.endswith (".xml"):
			continue
		path = os.path.join (basedir, filename)
		rec = OsmRecord(path)
		id = rec.getId()
		# print id
		if id.startswith ("SOARS-OLD"):
			continue
		newId = id.replace ('SOARS', 'SOARS-OLD')
		rec.setId(newId)
		print ("writing %s" % newId)
		try:
			rec.write()
		except:
			print 'couldnt process %s' % id

	
			
if __name__ == '__main__':
	collection = "1261600535691"
	# collection = "1264439680246"
	# updateCollection (collection)
	updateOldSoars()
