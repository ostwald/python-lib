import os, sys
from JloXml import MetaDataRecord, XmlUtils

data_path = '/home/ostwald/Documents/NCAR Library/osm-massage-2010-03-23'

# rec_path = os.path.join (data_path, '1264439680246/MLC-000-000-000-035.xml')

# rec_path = os.path.join (data_path, '1261600535691/NAB-000-000-000-001.xml')

class Affiliation:
	def __init__ (self, element):
		self.instName = XmlUtils.getChildText (element, "instName")
		self.instDivisions = self.get_inst_divs (element)
		self.instProject = XmlUtils.getChildText (element, "instProject")
		
	def get_inst_divs (self, element):
		return map (XmlUtils.getText, XmlUtils.getChildElements(element, "instDivision"))

	def __repr__ (self):
		s = [];add=s.append
		if self.instName:
			add ("instName: %s" % self.instName)
		if self.instDivisions:
			for div in self.instDivisions:
				add ("- %s" % div)
		if self.instProject:
			add ("instProject: %s" % self.instProject)
		return '\n\t'.join(s)

class ContributorPerson:
	"""
	represent information found at the /record/contributors/person node
	"""
	def __init__ (self, element):
		self.lastName = XmlUtils.getChildText (element, "lastName")
		self.firstName = XmlUtils.getChildText (element, "firstName")
		try:
			self.order = int(element.getAttribute ("order"))
		except:
			self.order = 1000
		self.role = element.getAttribute ("role")
		self.upid = element.getAttribute ("UCARid")
		self.affiliations = map (Affiliation, XmlUtils.getChildElements (element, 'affiliation'))
		
	def __repr__ (self):
		s = "%d - %s, %s (%s)" % (self.order, self.lastName, self.firstName, self.role)
		if self.affiliations:
			for aff in self.affiliations:
				s += '\n\t%s' % aff
		return s
		
	def __cmp__ (self, other):
		return cmp (self.order, other.order)
		
class OsmRecord (MetaDataRecord):

	xpath_delimiter = '/'
	id_prefix = "OSM-RECORD"
	
	id_path = 'record/general/recordID'
	
	xpaths = {
		'id' : 'record/general/recordID',
		'recordDate' : 'record/general/recordDate',
		'title' : 'record/general/title',
		'pubName' : 'record/general/pubName',
		'lastName' : 'record/contributors/person/lastName',
		'firstName' : 'record/contributors/person/firstName',
		'middleName' : 'record/contributors/person/middleName',
		'suffix' : 'record/contributors/person/suffix',
		'coverageDate' : 'record/coverage/date',
		'volume' : 'record/general/volume',
		'pages' : 'record/general/pages',
		'pub_id' : 'record/classify/idNumber'
	}
	
	def __init__ (self, path=None, xml=None):
		MetaDataRecord.__init__ (self, path=path, xml=xml)
		
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
		
	def getAuthors (self):
		authors = []
		people = self.selectNodes (self.dom, "record/contributors/person")
		for person in people:
			if person.getAttribute("role") == "Author":
				authors.append (person)
		return authors
		
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
		
	def getContributorPeople (self):
		contributorPeople = []
		people = self.selectNodes (self.dom, "record/contributors/person")
		for personNode in people:
			contributorPeople.append (ContributorPerson (personNode))

		contributorPeople.sort()			
		return contributorPeople
			
	def getPubDate (self):
		"""
		/record/coverage/date[@type='published'
		"""
		dates = self.selectNodes (self.dom, "record/coverage/date")
		for date in dates:
			if date.getAttribute ("type") == "Published":
				return XmlUtils.getText (date)
		
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
		# Do something here!
			
if __name__ == '__main__':
	path = 'C:/Documents and Settings/ostwald/devel/dcs-instance-data/local-ndr/records/osm/osm_recs/OSM-000-000-000-002.xml'
	rec = OsmRecord (path=path)
	print rec.getPubDate()
	for contrib in rec.getContributorPeople():
		print contrib
