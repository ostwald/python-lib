"""
Topic is a Key-concept in CCS-speak, and is assocated with a number of
TopPick instances

TopicRecord extends ConceptsRecord and is responsible for creating, 
populating and writing the XML record to the repository
"""
import os, sys
from backPackModelObject import BackPackModelObject, SortedValuesDict
from backPackMetadataMixin import BackPackMetadataMixin
from backpack import ConceptsRecord, Relation
from backpack.nsdl_ids import CachingNsdlIdService
from JloXml import XmlUtils
from UserDict import UserDict

nsdlIdService = CachingNsdlIdService()

class TopicRecord (BackPackMetadataMixin, ConceptsRecord):
	id_prefix = 'BP-TOPIC'
	xmlFormat = 'concepts'
	collection = 'topics_bp'
	xmlTemplate = 'TOPIC-Template.xml'
	xmlRecordClass = ConceptsRecord
	
	def makeRelation (self, topPickdata):
		"""
		inserts a relation into this TopicRecord for a TopPickData instance.
		In this version, the topPick is an ID Reference to an NSDL record.
		the NSDL ID is obtained by getNsdlId
		"""
		nsdlID = nsdlIdService.getId(topPickdata.url)
		num = topPickdata.num and "%02d" % topPickdata.num or ""
		data = {
			'object' : 'Resource',
			'relationship': 'Is aligned with',
			'objectTitle' : topPickdata.title,
			'num' : num,
			'id' : nsdlID,
			'idType' : 'NSDL'
		}
		# print "making a relation with data:%s" % data
		return Relation (data=data)		

class Topic (BackPackModelObject):
	"""
	reads worksheet containing the curriculum data
	Topic object creates Resource instances for each record in the data.
	"""
	xmlRecord_constructor = TopicRecord
	
	def __init__(self, topicData, parent=None):
		"""
		path is a tab-delimited curriculum data file`
		"""
		BackPackModelObject.__init__ (self, parent)
		self.topicName = topicData.topicName
		self.topicSentence = topicData.topicSentence
		self.topPicks = topicData.topPicks
		self.num = topicData.num
		
		print "worksheet %s has %d records" % (self.topicName, len(self.topPicks))	
		
		
	def getChildren (self):
		return {}
		
	def getRecord (self):
		"""
		get template record, and then populate with topic data
		NOTEs:
			- 'object' is set in template
			- ID has to be set before the record can be written
		"""
		if not self.record:
			rec = BackPackModelObject.getRecord(self)
			rec.setShortTitle (self.topicName)
			rec.setLongTitle (self.topicName)
			rec.set ('contents', self.topicSentence)
			
			for topPickData in self.topPicks:
				topPickRelation = rec.makeRelation (topPickData)
				rec.addRelation (topPickRelation)
			self.record = rec
			self.write()
		return self.record
		
def whatThe ():
	path = '/Documents/Work/NSDL/BackPack/curricul-data-working/Physics 2.6.0 Part 1.txt'
	topic = Topic (path, 'Physics Part 1')
	# print topic.getRecord()
	print 'shortTitle:', topic.shortTitle
	print 'longTitle:', topic.longTitle
	print 'topicSentence', topic.topicSentence
	
if __name__ == '__main__':
	if 1:
		from backpack.data_model.topicData import TopicData
		from backpack.data_model.utils import ingest_data_dir
		# data_path = os.path.join (ingest_data_dir, "Pathways & Advance Engineering/Physics 2.6.0 Part 1_files/sheet005.htm")
		data_path = os.path.join (ingest_data_dir, "Pathways & Advance Engineering/Physics 2.6.0 Part 1_v2_files/sheet005.htm")
		topicData = TopicData(data_path, 99)
		topic = Topic (topicData)
		print topic.getRecord()
		topic.write ()
	else:
		rec = TopicRecord()
		print "id:", rec.getId()
		rec.write()
