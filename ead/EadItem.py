import sys, os
from JloXml import XmlUtils
from EadFoundation import EadComponent, getEadRecord
import codecs

class DigitalObject:
	
	def __init__ (self, element):
		self.element = element
		self.href = self.element.getAttribute("ns2:href")
		self.title = self.element.getAttribute("ns2:title")
		
		
	def __repr__ (self):
		return "\t%s\n\t%s" % (self.title, self.href)
		# return self.element.toprettyxml()

class EadItem (EadComponent):
	
	"""
	almost all containers have 'Box' and 'Folder' information
	- ASSUMPTION: items have 1 Box and 1 Folder
	"""
	
	box = "Unknown"
	folder = "Unknown"
	extent = "Unknown"
	
	def __init__ (self, element, parent):
		EadComponent.__init__ (self, element, parent)
		self.collection = self.parent
		self.dao = self._get_dao()
		if self.did.containerElements:
			self.box = self._get_box()
			self.folder = self._get_folder()
		if self.did.physdescElements:
			self.extent = self._get_phy_extent ()
		
	def _get_dao (self):
		daoElement = XmlUtils.selectSingleNode (self.element, "dao")
		if daoElement:
			return DigitalObject (daoElement)
		
	def hasDigitalObject (self):
		return self.dao is not None
		
	def _get_box (self):
		if not self.did.containerElements:
			return None
		for c in self.did.containerElements:
			if c.getAttribute ("type") == "Box":
				return XmlUtils.getText (c)
				
	def _get_folder (self):
		if not self.did.containerElements:
			return None
		for c in self.did.containerElements:
			if c.getAttribute ("type") == "Folder":
				return XmlUtils.getText (c)
		
	def _get_phy_extent (self):
		if not self.did.physdescElements:
			return self.extent # default
		if len (self.did.physdescElements) > 1:
			raise Exception, "item %d has %d physdescElements" % (self.id, len (self.did.physdescElements))
		physdesc = self.did.physdescElements[0]
		extent = XmlUtils.getChildText (physdesc, "extent")
		if extent:
			return extent.strip()
				
	def report (self):
		EadComponent.report (self)
		print "id: %s" % self.id
		print "box: %s" % self.box
		print "folder: %s" % self.folder
		print "extent: %s" % self.extent
		if self.hasDigitalObject():
			print self.dao
			
	def asXml (self, prefix=None):
		doc = XmlUtils.createDocument ("record")
		root = doc.documentElement
		addChild = XmlUtils.addChild
		
		addChild (doc, "id", self.getRecordId (prefix))
		addChild (doc, "title", self.title)
		addChild (doc, "box", self.box)
		addChild (doc, "folder", self.box)
		addChild (doc, "extent", self.extent)
		if self.hasDigitalObject():
			digi = XmlUtils.addElement (doc, root, "digitalObject")
			addChild (doc, "href", self.dao.href, digi)
			addChild (doc, "title", self.dao.title, digi)
		return doc
			
	def getRecordId (self, prefix=None):
		recordid = self.id
		if prefix:
			recordid = "%s-%s" % (prefix, self.id)
		return recordid
		
		
def itemLevelReport (ead):
	ead.archdesc.report()
	for col in ead.collections:
		col.report()
		for item in col.getItems():
			# item.report()
			try:
				print item.asXml().toxml()
			except:
				print 'could not print ', item.id
				item.report()
				sys.exit()

def titleTester (id, ead):	
	item = ead.getItem (id)
	title0 = item.title
	title1 = unicode(item.title.decode ("utf8")) ## works
	title2 = item.title.decode ("utf8") ## test (seems to work)
	title3 = unicode (item.title, "utf8") ## test2
	
	if title1 == title2:
		print "1 == 2"
		
	if title1 == title3:
		print "1 == 3"
		
	if title2 == title3:
		print "2 == 3"
		
	print title1
	for ch in title1:
		print ord(ch), ch
						
if __name__ == "__main__":
	ead = getEadRecord()
	item = ead.getItem ('ref186')
	print item.asXml().toxml()
