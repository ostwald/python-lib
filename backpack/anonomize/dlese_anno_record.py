"""
Subclass of MetaDataRecord for dlese_anno framework
"""
import sys, os
from JloXml import MetaDataRecord, XmlUtils

class ContributorPerson:
	
	attrs = ['nameFirst', 'nameLast']
	
	def __init__ (self, element):
		self.element = element
		
	def getNameFirst (self):
		return XmlUtils.getChildText(self.element, 'nameFirst')
	
	def setNameFirst (self, name):
		node = XmlUtils.getChild ('nameFirst', self.element)
		if not node:
			node = XmlUtils.createElement('nameFirst')
			self.element.appendChild(node)
		XmlUtils.setText(node, name)
		
	def getNameLast(self):
		return XmlUtils.getChildText(self.element, 'nameLast')
		
	def setNameLast (self, name):
		node = XmlUtils.getChild ('nameLast', self.element)
		if not node:
			node = XmlUtils.createElement('nameLast')
			self.element.appendChild(node)
		XmlUtils.setText(node, name)
		
	def __repr__ (self):
		return '%s %s' % (self.getNameFirst(), self.getNameLast())

class DleseAnnoRecord (MetaDataRecord):
	"""
	the xmlFormat used to represent users in the CCS
	"""
	xpaths = {
		'id' : "annotationRecord/service/recordID",
		'itemID' : "annotationRecord/recordID",
		'contributors' : 'annotationRecord/annotation/contributors/contributor'
	}
	
	xpath_delimiter = '/'
	id_path = xpaths['id']
	
	def getContributorNodes (self):
		return self.selectNodes(self.dom, self.xpaths['contributors'])
		
	def getContributorPeople (self):
		personFilter = lambda x:XmlUtils.getChild ('person', x)
		nodes = filter (personFilter, self.getContributorNodes())
		return map (ContributorPerson, nodes)
		
	def getPerson (self, firstName=None, lastName=None):
		"""
		ensure that either first or last name is specified.
		then return the first person that matches the provided params.
		e.g., if only firstName is provided, return first match. if both
		are provided, return first person matching both
		"""
		if not (firstName or lastName):
			return None
		for person in self.getContributorPeople():
			if firstName and firstName != person.getNameFirst():
				continue
			if lastName and lastName != person.getNameLast():
				continue
			return person
	
if __name__ == '__main__':
	path = 'dlese_anno_sample.xml'
	rec = DleseAnnoRecord(path=path)
	print rec.getId()
	print 'contribs: %d' % (len (rec.getContributorNodes()))
	people = rec.getContributorPeople()
	print 'people: %d' % (len (people))
	for person in people:
		print person
		
	p = rec.getPerson (firstName="Ronald", lastName="McDonald")
	p.setNameFirst('Ronaldo')
	p.setNameLast('McDonaldo')
	print p
	print rec
