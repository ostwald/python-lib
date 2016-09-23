"""
ConceptsRecord - 
reads and writes values to a 'concept' record
"""

from JloXml import MetaDataRecord, XmlUtils

class Relation:
	"""
	<relation object="Concept" 
			  relationship="Has part" 
			  num="1" 
			  objectTitle="Contribution of Archimedes">
      <id type="CCS">BP-CON-000-000-000-001</id>
    </relation>
	"""
	def __init__ (self, element=None, data=None):
		self.object = self.relationship = self.num = self.objectTitle = self.id = self.idType = ''
		if element:
			self.object = element.getAttribute ('object') or ''
			self.relationship = element.getAttribute ('relationship') or ''
			self.num = element.getAttribute ('num') or ''
			self.objectTitle = element.getAttribute ('objectTitle')
			idEl = XmlUtils.getChild('id', element)
			if idEl:
				self.id = XmlUtils.getText (idEl) or ""
				self.idType = idEl.getAttribute ('type') or ''
				
		if data:
			for attr in data.keys():
				setattr (self, attr, data[attr])
				
	def asElement (self):
		element = XmlUtils.createElement('relation')
		element.setAttribute ('relationship', self.relationship)
		if self.num:
			element.setAttribute ('num', self.num)
		element.setAttribute ('objectTitle', unicode(self.objectTitle))
		element.setAttribute ('object', self.object)
		idEl = element.appendChild (XmlUtils.createElement ('id'))
		# idEl = XmlUtils.addElement(doc, parent, tagName)
		# idEl.setAttribute ('id', self.id)
		XmlUtils.setText (idEl, self.id)
		idEl.setAttribute ('type', self.idType)
		return element
				
	def __repr__ (self):
		s=[];add=s.append
		for attr in self.__dict__.keys():
			add ("%s: %s" % (attr, getattr(self, attr)))
		return '\n\t'.join(s)

class ConceptsRecord (MetaDataRecord):
	
	xpath_delimiter = '/'
	xpaths = {
		'id' : 'concept/recordID',
		'shortTitle' : 'concept/shortTitle',
		'longTitle' : 'concept/longTitle',
		'object' : 'concept/contents/@object',
		'contents' : 'concept/contents/content/text'
	}
	id_path = xpaths['id'] # unfortunate backwards-compatibility
	
	def __init__ (self, path=None, xml=None):
		MetaDataRecord.__init__ (self, path=path, xml=xml)
		self.relations = self.get_relations()
	
	def getShortTitle (self):
		return self.get('shortTitle')
	
	def setShortTitle (self, value):
		self.set ('shortTitle', value)

	def getLongTitle (self):
		return self.get('longTitle')
	
	def setLongTitle (self, value):
		self.set ('longTitle', value)
		
	def getObject (self):
		return self.get('object')
	
	def setObject (self, value):
		self.set ('object', value)
		
	def get_relations (self):
		return map (Relation, self.selectNodes (self.dom, 'concept/relations/relation'))
		
	def addRelation(self, relation):
		relationsNode = self.selectSingleNode (self.dom, 'concept/relations')
		if not relationsNode:
			raise Exception, "addRelation couldn't find the relations node"
		return relationsNode.appendChild (relation.asElement())
	
		
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
	rec = ConceptsRecord (path)
	rec.setShortTitle ("i am a short title")
	rec.setObject ("OBJECT-TyPE")
	addRelationTester (rec)
	print rec
	
	if 0:
		print 'there are %d relations' % len(rec.relations)
		for rel in rec.relations:
			print rel.asElement().toxml()
