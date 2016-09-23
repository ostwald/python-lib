"""
BackPackModelObject -
	collects information about a curricular object
	- metadata record
	- type
	- collection
	- xmlFormat
"""
import os, sys
from backPackModelObject import BackPackModelObject
from backPackMetadataMixin import BackPackMetadataMixin
from backpack import ConceptsRecord
from JloXml import XmlUtils, AdnRecord

class TopPickRecord (BackPackMetadataMixin, AdnRecord):
	
	id_prefix = 'BP-PICK'
	xmlFormat = 'adn'
	collection = 'top_picks_bp'
	xmlTemplate = 'TOP-PICK-Template.xml'
	xmlRecordClass = AdnRecord

class TopPick (BackPackModelObject):
	"""
	instantiated using the data from one row of the 
	curriculum data spreadsheet
	
	see data_model.topicData.topPickData
	"""
	xmlFormat = 'adn'
	objectType = 'Resource'
	xmlRecord_constructor = TopPickRecord
	
	def __init__(self, topPickData=None, parent=None):
		"""
		path is a tab-delimited curriculum data file`
		"""
		self.title = self.url = self.summary = self.keywords = ""
		BackPackModelObject.__init__ (self, parent)
		if topPickData:
			self.title = topPickData.title
			self.url = topPickData.url
			self.summary = topPickData.summary
			self.keywords = topPickData.keywords
		self.record = self.getRecord()
		self.num = topPickData.num
	
		if not self.url:
			raise Exception, 'url not supplied for %s' % self.title
		
		# print "my title: " + self.title
		
	def getChildren(self):
		return {}
		
	def __cmp__ (self, other):
		return cmp(self.num, other.num)
		
	def getRecord (self):
		"""
		get template record, and then populate with topPick data
		NOTEs:
			- ID has to be set before the record can be written
		"""
		if not self.record:
			rec = BackPackModelObject.getRecord(self)
			rec.xpath_delimiter = ':'
			rec.setTitle(self.title)
			
			rec.setPrimaryUrl (self.url)
			rec.setDescription (self.summary)
			for kw in self.keywords:
				rec.add_keyword(kw)
		return self.record
		
class MockData:
	
	def __init__ (self, url, title, summary, keywords):
		self.url = url
		self.title = title
		self.summary = summary
		self.keywords = keywords
		
def whatThe ():
	path = '/Documents/Work/NSDL/BackPack/curricul-data-working/Physics 2.6.0 Part 1.txt'
	data = MockData ('my URL', 'MY TItLE', 'MY SUmmARY', ['keword 1', 'keywoprd 2'])
	parent = None
	topPick = TopPick (data, parent)
	rec = topPick.getRecord()
	print rec
	rec.write ('validate_me.xml')
	
if __name__ == '__main__':
	rec = TopPickRecord()
	print "id:", rec.getId()
	rec.write()
