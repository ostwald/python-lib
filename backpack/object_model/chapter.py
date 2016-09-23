"""
Chapter 
"""
import os, sys
import bp_share

from backPackModelObject import BackPackModelObject, SortedValuesDict
from backPackMetadataMixin import BackPackMetadataMixin
from topic import Topic
from backpack import ConceptsRecord, Relation
from backpack.data_model import TopicData, NoTopPickDataError, utils
from JloXml import XmlUtils

class ChapterRecord (BackPackMetadataMixin, ConceptsRecord):
	"""
	responsible for creating, modifying and writing Chapter records
	"""
	id_prefix = 'BP-CHAPTER'
	xmlFormat = 'concepts'
	collection = 'chapters_bp'
	xmlTemplate = 'CHAPTER-Template.xml'
	xmlRecordClass = ConceptsRecord
	
	def makeRelation (self, topic):
		"""
		making relation from chapter to topic/concept
		"""
		num = topic.num and "%02d" % topic.num or ""
		data = {
			'object' : 'Concept',
			'relationship': 'Has part',
			'objectTitle' : topic.topicName,
			'num' : num,
			'id' : topic.getId(),
			'idType' : 'CCS'
		}
		# print "Chapter making a relation with data:%s" % data
		return Relation (data=data)
	
class Chapter (BackPackModelObject):
	"""
	Construct a chapter object and all children
	"""
	xmlRecord_constructor = ChapterRecord
	
	def __init__(self, chapterData, parent=None):
		"""
		path is a tab-delimited curriculum data file`
		"""
		BackPackModelObject.__init__ (self, parent)
		self.shortTitle = chapterData.chapter
		self.num = chapterData.num
		self.longTitle = chapterData.chapter
		self.topics = chapterData.data
		self.unit = chapterData.unit
	
	def getChildren (self):
		# myRec = self.getRecord()
		if self._children is None:
			self._children = SortedValuesDict()
			for tabData in self.topics:
				try:
					topicData = TopicData(tabData.data_path, tabData.num)
				except NoTopPickDataError:
					print "No Data Found in %s" % tabData.data_path
					continue
				topic = Topic (topicData)
				topicId = topic.getId()
				self._children[topicId] = topic
				print 'made topic', topicId
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
			
			for topic in self.getChildren().values(): # TabData instances
				topicRelation = rec.makeRelation(topic)
				rec.addRelation (topicRelation)
					
			self.record = rec
			self.write()
			
		return self.record
		
if __name__ == '__main__':
	from backpack.data_model.utils import ingest_data_dir
	from backpack.data_model.chapterData import ChapterData
	# path = '/Documents/Work/NSDL/BackPack/html/Pathways & Advance Engineering/Physics 2.6.0 Part 1.htm'
	unit = 'Pathways & Advanced Engineering'
	unit = 'Engineering Class'
	filename = '14_Engineering Bridges.htm'
	path = os.path.join (utils.ingest_data_dir, unit, filename)
	chapterData = ChapterData(path)
	chapterData.report()
	chapter = Chapter (chapterData)
	rec = chapter.getRecord()
	chapter.write()
	
	
