"""
NcsCollectRecord

among other things managed contacts:
Contact schema
<xs:complexType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="contactType">
  <xs:attribute name="name" type="xs:string" use="optional"/>
  <xs:attribute name="ldapId" type="xs:string" use="optional"/>
  <xs:attribute name="email" type="xs:string" use="optional"/>
  <xs:attribute name="active" type="xs:boolean" use="required"/>
  <xs:attribute name="urlReport" type="xs:boolean" use="optional"/>
</xs:complexType>


"""

from JloXml import MetaDataRecord, XmlUtils
import sys
import string
import os
import re

class NCSCollectRecord (MetaDataRecord):

	id_path = "record:general:recordID"

	# fields (name:xpath)
	xpaths = {
		'id' : 'record:general:recordID',
		'description' : 'record:general:description',
		'url' : 'record:general:url',
		'title' : 'record:general:title',
		'dateTime' : 'record:collection:dateTime',
		'brandURL' : 'record:collection:brandURL',
		'ncsFormat' : 'record:collection:ingest:ncs:@ncsFormat',
		# 'libraryFormat' : 'record:collection:ingest:ncs:@libraryFormat',
		'libraryFormat' : 'record:collection:ingest:oai:@libraryFormat',
		'metadataPrefix' : 'record:collection:ingest:oai:@metadataPrefix',
		'collSetSpec' : 'record:collection:setSpec',
		'oaiSetSpec' : 'record:collection:ingest:oai:set:@setSpec'
	}

	key_path = "collectionRecord:access:key"
	shortTitle_path = "collectionRecord:general:shortTitle"
	fullTitle_path = "collectionRecord:general:fullTitle"
	description_path = "collectionRecord:general:description"
	
	def __init__ (self, xml=None, path=None):

		self.xml_format = None
		self.filename = ""

		MetaDataRecord.__init__ (self, xml=xml, path=path)
		
		if self.dom:
			self.doc = self.dom.documentElement
			self.xml_format = "dlese_collect"
	# TITLE	
	def getTitle (self):
		return self.get('title');
		
	def setTitle (self, value):
		self.set('title', value)

	# URL	
	def getUrl (self):
		return self.get('url')
		
	def setUrl (self, value):
		self.set('url', value)

	# DateTime	
	def getDateTime (self):
		return self.get('dateTime');
		
	def setDateTime (self, value):
		self.set('dateTime', value)

	# Description
	def getDescription (self):
		return self.get('description')
		
	def setDescription (self, desc):
		self.set ('description', desc)
		
	def addDleseSupportContact(self):
		contacts_el = self.selectSingleNode(self.dom, 'record:collection:contacts')
		if not contacts_el:
			raise Exception, 'contacts node not found'
		el = XmlUtils.addElement(self.dom, contacts_el, 'contact')
		
		el.setAttribute ("email",'support@dlese.org');
		el.setAttribute ("name", 'DLESE Support');
		el.setAttribute ("urlReport", 'false');
		el.setAttribute ("active", 'true');		
		
	def addContact (self, dleseContributor):
		"""
		assumes there is a "contacts" node
		this is what a contact node looks like
		  <contact email="support@dlese.org" name="DLESE Support" urlReport="false" active="true"/>
	
		hey ... should ALL the dlese contacts be DLESE support??
		"""
		contacts_el = self.selectSingleNode(self.dom, 'record:collection:contacts')
		if not contacts_el:
			raise Exception, 'contacts node not found'
		el = XmlUtils.addElement(self.dom, contacts_el, 'contact')
		
		el.setAttribute ("email",dleseContributor.getEmail());
		el.setAttribute ("name", dleseContributor.getFullName());
		el.setAttribute ("urlReport", 'false');
		el.setAttribute ("active", 'false');

	def addViewContext (self, vc):
		vcParent = self.selectSingleNode (self.dom,'record:collection:viewContexts')
		vcNodes = XmlUtils.getChildElements(vcParent)	
		print '%d vc nodes found' % len(vcNodes)
		vcValues = map(lambda x:XmlUtils.getText(x), vcNodes)
		for val in vcValues:
			print '-', val
		if not vc in vcValues:
			XmlUtils.addChild (self.dom, 'viewContext', vc, vcParent)
		

def testId(rec):
	print 'the id is %s' % rec.getId()
	rec.setId("fooberry")
	print 'now it is %s' % rec.getId()
	
def testTitle(rec):
	print 'the title is "%s"' % rec.getTitle()
	rec.setTitle("fooberry")
	print '.. now it is "%s"' % rec.getTitle()
	
def testUrl(rec):
	print 'the url is "%s"' % rec.getUrl()
	rec.setUrl("fooberry")
	print '.. now it is "%s"' % rec.getUrl()

def testDateTime(rec):
	print 'the dateTime is "%s"' % rec.getDateTime()
	rec.setDateTime("fooberry")
	print '.. now it is "%s"' % rec.getDateTime()
	
def testDescription(rec):
	print 'the description is "%s"' % rec.getDescription()
	rec.setDescription("fooberry")
	print '.. now it is "%s"' % rec.getDescription()

if __name__ == '__main__':
	path = '/Users/ostwald/Desktop/DLESE_MIGRATION/ncs_collect/ncs_collect_msp2.xml'
	rec = NCSCollectRecord(path=path)
	testDateTime(rec)
