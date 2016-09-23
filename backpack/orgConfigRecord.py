"""
OrgConfigRecord - 
reads and writes values to a 'concept' record
"""

from JloXml import MetaDataRecord, XmlUtils

class CurricularUnitElement:
	
	tagName = None # abstract
	
	def __init__ (self, id, name):
		self.id = id
		self.name = name
		self.children = []
		
	def addChild (self, child):
		# print '%s adding child (%s)' % (self.__class__.__name__, child.__class__.__name__)
		self.children.append(child)
		
	def asElement(self):
		# print "\n%s creating element: %s" % (self.__class__.__name__, self.tagName)
		element = XmlUtils.createElement(self.tagName)
		element.setAttribute ('recordId', self.id)
		element.setAttribute ('name', self.name)
		for child in self.children:
			element.appendChild (child.asElement())
		return element
		
class CurriculumElement (CurricularUnitElement):
	tagName = 'curriculum'
	
class UnitElement (CurricularUnitElement):
	tagName = 'unit'

class ChapterElement (CurricularUnitElement):
	tagName = 'chapter'	
	
class OrgConfigRecord (MetaDataRecord):
	
	xpath_delimiter = '/'
	xpaths = {
		'id' : 'orgConfig/recordID',
		'title' : 'orgConfig/title',
		'abbrevTitle' : 'orgConfig/abbrevTitle',
		'orgEntity' : 'orgConfig/orgEntity'
	}
	id_path = xpaths['id'] # unfortunate backwards-compatibility
	
	def __init__ (self, path=None, xml=None):
		MetaDataRecord.__init__ (self, path=path, xml=xml)
		self.setDateCreated ()
		
	def setDateCreated (self):
		dateEl = self.selectSingleNode (self.dom, 'orgConfig/date')
		if not dateEl:
			dateEl = self.doc.appendChild (XmlUtils.createElement('date'))
		dateEl.setAttribute ('created', self.getXsdDate())
		
	def get_curricula(self):
		return self.selectNodes(self.dom, 'orgConfig/curricularSelections/curriculum')
		
	def addCurriculumElement(self, curriculumElement):
		curriculumsNode = self.selectSingleNode (self.dom, 'orgConfig/curricularSelections')
		if not curriculumsNode:
			raise Exception, "addCurriculum couldn't find the curriculums node"
		return curriculumsNode.appendChild (curriculumElement.asElement())
	
	def setOrgEntity (self, orgEntity, key):
		orgEntityEl = self.selectSingleNode (self.dom, self._xpath ('orgEntity'))
		if not orgEntityEl:
			orgEntityEl = self.doc.appendChild (XmlUtils.createElement('orgEntity'))
		self.set ('orgEntity', orgEntity)
		orgEntityEl.setAttribute ('key', key)
		
	def setTitle(self, title):
		self.set('title', title)
		
	def setAbbrevTitle (self, abbrev):
		self.set('abbrevTitle', abbrev)
		
def addRelationTester (rec):
	params = {
		'id' : 'MY-FARGIN-ID',
		'object' : 'CHAPTER'
	}
	rel = Relation(data=params)
	print rel
	print rel.asElement().toxml()
	rec.addRelation (rel)
	
	
		
if __name__ == '__main__':
	path = 'templates/CHAPTER-Template.xml'
	rec = OrgConfigRecord (path)
	rec.setShortTitle ("i am a short title")
	rec.setObject ("OBJECT-TyPE")
	addRelationTester (rec)
	print rec
	
	if 0:
		print 'there are %d relations' % len(rec.relations)
		for rel in rec.relations:
			print rel.asElement().toxml()
