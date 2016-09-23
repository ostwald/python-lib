"""
Unit
"""
import os, sys
import bp_share

from backPackModelObject import BackPackModelObject, SortedValuesDict
from backPackMetadataMixin import BackPackMetadataMixin
from backpack import ConceptsRecord, Relation
from topic import Topic
from backpack.data_model import ChapterData, utils
from chapter import Chapter
from JloXml import XmlUtils

class UnitRecord (BackPackMetadataMixin, ConceptsRecord):
	id_prefix = 'BP-UNIT'
	xmlFormat = 'concepts'
	collection = 'units_bp'
	xmlTemplate = 'UNIT-Template.xml'
	xmlRecordClass = ConceptsRecord
	
	def makeRelation (self, chapter):
		"""
		making relation from chapter to topic/concept
		"""
		num = chapter.num and "%02d" % chapter.num or ""
		print "%s (%s)" % (chapter.shortTitle, type(chapter.shortTitle))
		data = {
			'object' : 'Chapter',
			'relationship': 'Requires',
			'objectTitle' : unicode(chapter.shortTitle),
			'num' : num,
			'id' : chapter.getId(),
			'idType' : 'CCS'
		}
		print "Unit making a relation with data:%s" % data
		return Relation (data=data)
	
class Unit (BackPackModelObject):
	"""

	"""
	xmlRecord_constructor = UnitRecord
	
	def __init__(self, unitData, parent=None):
		"""
		path is a tab-delimited curriculum data file
		"""
		BackPackModelObject.__init__ (self, parent)
		self.name = unitData.name
		self.chapters = unitData.data
		self.shortTitle = self.name
		self.longTitle = self.name
		self.description = unitData.blurb
	
	def getChildren (self):
		if self._children is None:
			self._children = SortedValuesDict()
			for chapterInfo in self.chapters:
				chapterData = ChapterData(chapterInfo['data_path'])
				chapter = Chapter (chapterData)
				chapterId = chapter.getId()
				self._children[chapterId] = chapter
				print 'made chapter', chapterId
				
		return self._children
		
	def getRecord (self):
		"""
		get template record, and then populate with chapter data
		NOTEs:
			- 'object' is set in template
			- ID has to be set before the record can be written
		"""
		if not self.record:
			rec = BackPackModelObject.getRecord(self)
			rec.setShortTitle (self.shortTitle)
			rec.setLongTitle (self.longTitle)
			
			rec.set('contents', self.description)
			
			for topic in self.getChildren().values(): # TabData instances
				topicRelation = rec.makeRelation(topic)
				rec.addRelation (topicRelation)
					
			self.record = rec
			print "*** about to print ***"
			print rec
			self.write()
			
		return self.record
		
if __name__ == '__main__':
	from backpack.data_model.utils import ingest_data_dir
	from backpack.data_model import UnitData
	
	unit = 'Engineering Class'
	#unit = 'Aerospace Technology Class'
	
	data_path = os.path.join (utils.ingest_data_dir, unit)
	unitData = UnitData(data_path)
	
	unit = Unit (unitData)
	rec = unit.getRecord()
	unit.write()

	
	
