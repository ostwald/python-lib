from JloXml import MetaDataRecord, XmlUtils
import sys
import string
import os
import re

class DleseCollectRecord (MetaDataRecord):

	xpaths = {
			'key' : "collectionRecord:access:key",
			'id' : "collectionRecord:metaMetadata:catalogEntries:catalog:@entry",
			'libraryFormat' : 'collectionRecord:access:key:@libraryFormat',
			'description' : 'collectionRecord:general:description',
			'fullTitle' : 'collectionRecord:general:fullTitle',
			'shortTitle' : 'collectionRecord:general:shortTitle',
			'collectionLocation' : 'collectionRecord:access:collectionLocation',
			'created' : 'collectionRecord:metaMetadata:dateInfo:@created'
		 }

	catalog_path = "collectionRecord:metaMetadata:catalogEntries:catalog"
	key_path = "collectionRecord:access:key"
	shortTitle_path = "collectionRecord:general:shortTitle"
	fullTitle_path = "collectionRecord:general:fullTitle"
	description_path = "collectionRecord:general:description"
	
	def __init__ (self, xml=None, path=None):

		self.xml_format = None
		self.fn_id = None
		self.md_id = None
		self.filename = ""

		MetaDataRecord.__init__ (self, xml=xml, path=path)
		
		if self.dom:
			self.doc = self.dom.documentElement
			self.xml_format = "dlese_collect"
		
			self.fn_id = self.getFileNameID()
			self.md_id = self.getId()

	def getFileNameID (self):
		return os.path.splitext(self.filename)[0]

	def _getCatalogElement (self):
		catalog_element = self.selectSingleNode (self.dom, self.catalog_path)
		if not catalog_element:
			raise "catalog element not found"
		return catalog_element

	def getShortTitle (self):
		return self.getTextAtPath (self.shortTitle_path);
		
	def setShortTitle (self, value):
		self.setTextAtPath (self.shortTitle_path, value)		
		
	def getFullTitle (self):
		return self.getTextAtPath (self.fullTitle_path);
		
	def setFullTitle (self, value):
		self.setTextAtPath (self.fullTitle_path, value)
		
	def getKey (self):
		return self.getTextAtPath (self.key_path)
		
	def setKey (self, key):
		self.setTextAtPath (self.key_path, key)

	def getDescription (self):
		return self.getTextAtPath (self.description_path)
		
	def setDescription (self, description):
		self.setTextAtPath (self.description_path, description)
		
	def setLibraryFormat (self, xmlFormat):
		try:
			key_element = self.selectSingleNode (self.dom, self.key_path)
			key_element.setAttribute ("libraryFormat", xmlFormat)
		except:
			print "unable to set xmlFormat"
	
	#/collectionRecord/access/key/@libraryFormat
	def getLibraryFormat (self):
		key_element = self.selectSingleNode (self.dom, self.key_path)
		if key_element:
			return key_element.getAttribute ("libraryFormat")
		else:
			print "not able to get libraryFormat"

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
			
	def get_contributors(self, type):
		if not type in ['metaMetadata' , 'lifecycle']:
			raise TypeError, 'Unrecognized type (%s)' % type
		path = 'collectionRecord:%s:contributors:contributor' % type
		return map (contributorFactory, self.selectNodes(self.dom, path))

	def getLifecycleContributors (self):
		return self.get_contributors('lifecycle')

	def getMetadataContributors (self):
		return self.get_contributors('metaMetadata')

	# def getEmailPrimaryContributors(self, type):
		# contribs = [];add=contribs.append
		# contrib_elements = self.get_contributors(type)
		# # print "%d contribs found" % len(contrib_elements)
		# 
		# for el in contrib_elements:
			# if XmlUtils.selectSingleNode(el, 'person:emailPrimary', ':'):
				# add (ContributorPerson(el))
		# 
		# return contribs

	def report (self):
		# print "rec.fn_id: %s" % self.fn_id
		print "shortTitle: %s" % self.getShortTitle()
		print "rec id: %s" % self.getId()
		print "key: " + self.getKey()
		# print "xml_format: %s" % self.xml_format

		# doc = self.doc
		# if doc:
			# print "rootElementName: %s" % doc.tagName
		# else:
			# print "document could not be parsed as xml"

	def getContributorsForContacts(self):
		allcontribs = []
		for type in ['lifecycle', 'metaMetadata']:
			contribs = self.get_contributors(type)
			# print "%d %s contribs found" % (len(contribs), type)
			allcontribs += contribs
			
		# print "\n%d contribs found" % len(allcontribs), type
			
		# filter by email
		dict = {}
		for contrib in allcontribs:
			if contrib.getEmail() == "ginger@ucar.edu": continue
			dict[contrib.getFullName()] = contrib
			
		if 0:
			print "\nafter filter - %d contribs found" % len(dict), type
			for c in dict.values():
				# print c.element.toxml()
				print '-', c
			
		return dict.values()

def contributorFactory (element):
	type = XmlUtils.getChildElements(element)[0].tagName
	# print 'contributor type: ', type
	if type == 'person':
		return ContributorPerson(element)
	elif type == 'organization':
		return ContributorOrganization(element)

class Contributor():
	def __init__ (self, element):
		self.element = element;
		self.role = self.element.getAttribute ("role")
		self.date = self.element.getAttribute ("date")
		self.type = '???'
		
	def getFullName(self):
		raise Exception, 'getFullName not implemented'
		
	def getEmail(self):
		raise Exception, 'getEmail not implemented'
		
	def getType (self):
		return self.type
		
	def __repr__ (self):
		s = "contributor (%s)" % self.getType()
		NL = '\n   '
		# s += NL + 'type: ' + self.getType()
		s += NL + 'fullname: ' + self.getFullName()
		s += NL + 'email: ' + (self.getEmail() or "???")
		return s
		


class ContributorPerson(Contributor):
	"""
	element looks like this:
	  <contributor date="2003-04-28" role="Creator">
        <person>
          <nameTitle>Ms</nameTitle>
          <nameFirst>Katy</nameFirst>
          <nameLast>Ginger</nameLast>
          <instName>University Corporation for Atmospheric Research</instName>
          <instDept>DLESE Program Center</instDept>
          <emailPrimary>ginger@ucar.edu</emailPrimary>
        </person>
      </contributor>
      """
	
	def __init__ (self, element):
		Contributor.__init__ (self, element)
		self.type = 'person'
		person = XmlUtils.getChild('person', element)
		if not person:
			raise Exception, 'person not found in %s' % self.element.toxml()
		self.nameFirst = XmlUtils.getChildText(person, 'nameFirst')
		self.nameLast = XmlUtils.getChildText(person, 'nameLast')
		self.instName = XmlUtils.getChildText(person, 'instName')
		self.instDept = XmlUtils.getChildText(person, 'instDept')
		self.emailPrimary = XmlUtils.getChildText(person, 'emailPrimary')
		
	def getFullName (self):
		name = self.nameLast
		if self.nameFirst:
			name = self.nameFirst + ' ' + name
		return name
		
	def getEmail(self):
		return self.emailPrimary

		
class ContributorOrganization(Contributor):
	"""
	element looks like this:
		<contributor role="Contact" date="2003">
			<organization>
				<instName>University Corporation for Atmospheric Research (UCAR)</instName>
				<instDept>Digital Library for Earth System Education (DLESE)</instDept>
				<instEmail>support@dlese.org</instEmail>
			</organization>
		</contributor>
      """
	
	def __init__ (self, element):
		Contributor.__init__ (self, element)
		self.type = 'organization'
		organization = XmlUtils.getChild('organization', element)
		if not organization:
			raise Exception, 'organization not found in %s' % self.element.toxml()
		self.instName = XmlUtils.getChildText(organization, 'instName')
		self.instDept = XmlUtils.getChildText(organization, 'instDept')
		self.instEmail = XmlUtils.getChildText(organization, 'instEmail')
		
	def getFullName (self):
		return self.instName
		
	def getEmail(self):
		return self.instEmail

def sort (rec1, rec2):
	id1 = rec1.fn_id
	id2 = rec2.fn_id
	return cmp (id1, id2)


if __name__ == "__main__":
	path = "/Users/ostwald/Desktop/DLESE_MIGRATION/dlese_collect/dlese_collect_tester.xml"
	rec = DleseCollectRecord (path=path)
	rec.report()
	# print rec
	if 0:
		contribs = rec.getEmailPrimaryContributors()
		print "%d primary contribs found" % len(contribs)
	if 0:
		allcontribs = []
		for type in ['lifecycle', 'metaMetadata']:
			contribs = rec.get_contributors(type)
			print "%d %s contribs found" % (len(contribs), type)
			allcontribs += contribs
			
		print "\n%d contribs found" % len(allcontribs), type
			
		# filter by email
		dict = {}
		for contrib in allcontribs:
			if contrib.getEmail() == "ginger@ucar.edu": continue
			dict[contrib.getEmail()] = contrib
			
		print "\nafter filter - %d contribs found" % len(dict), type
		for c in dict.values():
			# print c.element.toxml()
			print '-', c
	if 1:
		all = rec.getContributorsForContacts()
		for c in all:
			# print c.element.toxml()
			print '-', c
		print "DONE"
	
