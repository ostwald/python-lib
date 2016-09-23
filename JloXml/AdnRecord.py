from JloXml import MetaDataRecord, XmlUtils
import sys
import string
import os
import re

class AdnRecord (MetaDataRecord):

	contentStandards_path ="educational:contentStandards"
	keyword_path = "general:keywords:keyword"
	
	xpaths = {
		'id' : "metaMetadata:catalogEntries:catalog:@entry",
		'title' : 'itemRecord:general:title',
		'contentStandards' :"educational:contentStandards",
		'keyword' : "general:keywords:keyword",
		'additionalInfo' : "itemRecord:general:additionalInfo",
		'eduDescription' : "itemRecord:educational:description",
		'description' : "itemRecord:general:description",
		'primaryUrl' : "itemRecord:technical:online:primaryURL",
		'lastModified' : 'itemRecord:metaMetadata:dateInfo:@lastModified',
		'created' : 'itemRecord:metaMetadata:dateInfo:@created',
	}
	
	versions = ["0_6_50", "0_7_00"]

	schemaUri_v0_6_50 = "http://www.dlese.org/Metadata/adn-item/0.6.50/record.xsd"
	schemaUri_v0_7_00 = "http://www.dlese.org/Metadata/adn-item/0.7.00/record.xsd"
	
	def __init__ (self, xml=None, path=None):

		self.xml_format = None
		self.fn_id = None
		self.md_id = None
		self.filename = ""

		MetaDataRecord.__init__ (self, xml=xml, path=path)
		
		if self.dom:
			self.doc = self.dom.documentElement
			self.xml_format = "adn"
		
			self.fn_id = self.getFileNameID()
			self.md_id = self.getId()
			# self.localize()
			self.setNameSpaceInfo()

	def getTitle (self):
		return self.get('title')
		
	def setTitle (self, title):
		self.set('title', title)


	def getDescription (self):
		return self.getTextAtPath (self.description_path)
		
	def setDescription (self, description):
		self.setTextAtPath (self.description_path, description)
		
	def setNameSpaceInfo (self):
		self.doc.setAttribute ("xmlns", self.DLESE_NAMESPACE_URI)
		self.doc.setAttribute ("xmlns:"+self.schema_instance_namespace, \
								self.SCHEMA_INSTANCE_URI)
		slNode = self.doc.getAttributeNode ("schemaLocation")
		

		if slNode:
			schemaLocation = self.doc.getAttribute ("schemaLocation")
			# print "schemaLocation: " + schemaLocation
			self.doc.removeAttribute ("schemaLocation")
			self.doc.setAttribute (self.qualify ("schemaLocation"), schemaLocation)
		else:
			self.setSchemaLocation (self.schemaUri_v0_6_50, self.DLESE_NAMESPACE_URI)

	def getVersion (self):
		schemaLocation = self.getSchemaLocation ()
		## print "  ... getVersion schemaLocation: " + schemaLocation
		if schemaLocation and len(schemaLocation.split(' ')) == 2:
			schemaUri = schemaLocation.split(' ')[1]
			for version in self.versions:
				locTry =  getattr (self, "schemaUri_v" + version)
				if locTry == schemaUri:
					## print "getVersion returning %s (%s)" % (version, locTry)
					return version
			# looked through all the versions without finding
			raise "FrameworkVersion", "unrecognized version spec: *%s*" % version

	def setVersion (self, version):

		if version in ["0_6_50", "0_7_00"]:
			schemaUri =  getattr (self, "schemaUri_v" + version)
			self.setSchemaLocation (schemaUri)
		else:
			raise "FrameworkVersion", "unrecognized version spec: *%s*" % version

	def getFileNameID (self):
		return os.path.splitext(self.filename)[0]


	def _getCatalogElement (self):
		catalog_element = self.selectSingleNode (self.dom, "itemRecord:metaMetadata:catalogEntries:catalog")
		if not catalog_element:
			raise "catalog element not found"
		return catalog_element

	def getAdditionalInfo (self):
		return self.get('additionalInfo')
		
	def setAdditionalInfo (self, text):
		return self.set('additionalInfo', text)	
	
	def getEduDescription (self):
		return self.get('eduDescription')
		
	def setEduDescription (self, text):
		return self.set('eduDescription', text)	
		
	def getPrimaryUrl (self):
		return self.get('primaryUrl')
		
	def setPrimaryUrl (self, text):
		return self.set ('primaryUrl', text)
		
	def setId (self, id):
		try:
			self._getCatalogElement().setAttribute ("entry", id)
		except:
			print "unable to set ID"
			
	def getId (self):
		catalog_element = self._getCatalogElement()
		if catalog_element:
			return catalog_element.getAttribute ("entry")
		else:
			print "not able to get ID"


	def report (self):
		print "rec.fn_id: %s" % self.fn_id
		print "rec.md_id: %s" % self.md_id
		print "xml_format: %s" % self.xml_format

		doc = self.doc
		if doc:
			print "rootElementName: %s" % doc.tagName
			print "there are %d keywords" % \
				  len(self.get_keywords())
			## print self.dom.toxml()
		else:
			print "document could not be parsed as xml"

	def keywords_path (self):
		return self.keyword_path

	def keywords_element (self):
		elementList = self.selectNodes (self.doc, "general:keywords")
		if elementList:
			return elementList[0]

	def keyword_elements (self):
		elementList = []
		if self.doc:
			elementList =  self.selectNodes (self.doc, self.keywords_path())
		return elementList

	def remove_standards (self):
		"""
		remove the educational standards element, including all children
		"""
		standards_node = self.selectSingleNode (self.doc, self.contentStandards_path)

		if standards_node:
			## print "standards to remove: %s" % standards_node.toxml()
			parent = standards_node.parentNode
			if parent:
				parent.removeChild (standards_node)
				standards_node.unlink()
				
	def empty_standards (self):
		"""
		remove assigned educational standards leaving the standards node empty
		"""
		standards_node = self.selectSingleNode (self.doc, self.contentStandards_path)
		# if not standards_node:
			# print "standards_node not found"
			# return
		# self.remove_children (standards_node)
		self.clearElement (standards_node);
		
	def add_standards (self, stds):
		if stds is None: 
			stds = []
		if type (stds) != type([]):
			stds = [stds]
		if not stds: return
		
		standards_node = self.selectSingleNode (self.doc, self.contentStandards_path)
		if (standards_node):
			for std in stds:
				new = self.addElement (standards_node, "contentStandard")
				self.setText (new, std)

	def get_standards (self):
		stds = []
		
		nodes = self.selectNodes (self.doc, self.contentStandards_path + ":contentStandard")
		if (nodes):
			map (stds.append, map (self.getText, nodes))
			
		return stds
				
	def remove_keyword (self, target):
		if not self.doc:
			return
		
		keywords_element = self.keywords_element()
		if not keywords_element:
			return

		for keyword in self.keyword_elements():
			if self.getText (keyword) == target:
				keywords_element.removeChild(keyword)
				keyword.unlink()
				break
		# if there are no keywords remaining remove the keyword element
		if not self.keyword_elements():
			# print "about to remove keywords element"
			parent = keywords_element.parentNode
			parent.removeChild (keywords_element)
			keywords_element.unlink()

			
	def localize (self):
			self.doc.setAttribute (self.qualify ("schemaLocation"),
								   "http://adn.dlese.org file:///Users/ostwald/Devel/metadata-frameworks/adn-item-project/record.xsd")

	def add_keyword (self, keyword):
		keywords_element = self.keywords_element()
		el = XmlUtils.addChild(self.dom, "keyword", keyword, keywords_element)
								   
	def get_keywords (self):
		keywords = []
		keyword_elements = self.keyword_elements()
		if keyword_elements:
			for element in keyword_elements:
				keywords.append(self.getText (element))
		return keywords

	def getSubjects(self):
		return self.getValuesAtPath("itemRecord:general:subjects:subject")
		
	def getGradeRanges(self):
		return self.getValuesAtPath("itemRecord:educational:audiences:audience:gradeRange")
		
	def getResourceTypes(self):
		return self.getValuesAtPath("itemRecord:educational:resourceTypes:resourceType")
		
	def getCreated (self):
		return self.get ('created')
		
	def getModified (self):
		return self.get ('lastModified')
		
def sort (rec1, rec2):
	id1 = rec1.fn_id
	id2 = rec2.fn_id
	return cmp (id1, id2)




if __name__ == "__main__":

	path = '/Users/ostwald/tmp/adn.xml'
	rec = AdnRecord(path=path)
	print rec
	print 'id: ', rec.getId()
	print 'title: ', rec.getTitle()
	print 'created: ' + rec.getCreated()
	print 'modified: ' + rec.getModified()
