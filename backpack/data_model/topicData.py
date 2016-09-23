"""
Topic Data was originally contained in a worksheet (a TAB of the chapter spreadsheet)
and after saving the chapter spreadsheet as html is a single html file (e.g., "sheet2.htm")

TopicData reads this TAB level spreadsheet and extracts a TOPIC SENTENCE and TOP-PICK DATA

The topic-pick data is used to create TopPickData instances

"""
import os, sys, codecs, re
from JloXml import XmlRecord, XmlUtils, RegExUtils
from xls import WorksheetEntry
from topicRecord import TopicRecord
import utils

class TopPickData (WorksheetEntry):
	
	def __init__ (self, data, schema, num=None):
		"""
		worksheet schema: 
			Search Topic, 
			Top 10 Results (Heading+website by clicking), 
			URL, 
			Summary, 
			Key words

		exposed attributes:
			title, url, summary, keywords, num
		"""
		WorksheetEntry.__init__ (self, data, schema) 
		self.title = self['Top 10 Results (Heading+website by clicking)']
		self.url = self['url']
		self.summary = self['Summary']
		self.keywords = self['Key words'] and map (lambda x:x.strip(), self['Key words'].split(','))
		self.num = num or 0
		
	def __repr__ (self):
		s=[];add=s.append
		# for attr in ['title', 'url', 'summary', 'keywords']:
		for attr in ['title', 'num']:
			val = getattr(self, attr)
			# print ('type val: %s' % type(val))
			if type(val) == type(u''):
				val = val.encode('utf-8')
			add ("%s: %s" % (attr, val))
		return '\n\t'.join(s)

class TopicData:
	"""
	input:
		- topic data html file path
	
	read topic-data file and expose:
		- topicName
		- topicSentence
		- topPicData
	"""
	def __init__ (self, html_data_path, num):
		self.num = num
		self.data = self.getTopicData(html_data_path)
		self.schema = self.data.pop(0)
		searchTopic = None
		self.topPicks = []
		for i, row in enumerate (self.data):
			topPickData = TopPickData (row, self.schema, num=i+1)
			if topPickData.title:
				self.topPicks.append(topPickData)
			if i == 0:
				searchTopic = topPickData['Search Topic']
			
		self.topicName,  self.topicSentence = self.processSearchTopic (searchTopic)
		
		if not self.topicSentence:
			raise Exception, "topic sentence not found for %s (%s)" % \
				(self.topicName, html_data_path)

	def processSearchTopic (self, searchTopic):
		"""
		search topic in the first data row, first cell
		- e.g., "yaba: adfiadfm"
		topicName is first split(':'), topicSentence is remainder
		"""
		if not ':' in searchTopic:
			return searchTopic, searchTopic
		i = searchTopic.find(':')
		if i != -1:
			topicName = searchTopic[:i].strip()
			topicSentence = searchTopic[i+1:].strip()
		else:
			topicName = searchTopic
			topicSentence = searchTopic
		return topicName, topicSentence
				
	def __repr__ (self):
		s=[];add=s.append
		add ('\nTopic Data')
		add ('- topicName: "%s"' % self.topicName.encode('utf-8'))
		add ('- topicSentence: "%s"' % self.topicSentence.encode('utf-8'))
		add ('\nTop Picks')
		for tp in self.topPicks:
			# add ('\t%s' % tp.__repr__().encode('utf-8'))
			# foo = unicode(str(tp))
			# print 'topPick as string: %s' % type(foo)
			add ('\t%s' % tp)
		return '\n'.join(s)
				
	def getTopicData (self, path):
		"""
		read an html file
		extract a table containing topicData
		use the table data to instantiate a TopPickData instance
		"""
		
		html = utils.getHtml(path)
		tablePat = RegExUtils.getTagPattern('table')
		m = tablePat.search(html)
	
		if not m:
			raise Exception, "Data Table not found!"
		xml = m.group()
		
		
		# xml = stripConditionals (xml)
		xml = utils.xcelHtml2Xml (xml)
		# print xml
		return TopicRecord(xml).parsed_data
		
	
if __name__ == '__main__':
	# data_path = os.path.join (utils.ingest_data_dir, "Pathways & Advance Engineering/Physics 2.6.0 Part 1_v2_files/sheet010.htm")
	# relpath = 'Pathways & Aerospace Rocketry/Aerodynamic Engineering 2.5.1_v2_files/sheet006.htm'
	# relpath = "Pathways & Advance Engineering/Physics 2.6.0 Part 1_v2_files/sheet006.htm"
	relpath = 'Aerospace Technology Class/Astronomy 3.0b_v2_files/sheet012.htm'
	data_path = os.path.join (utils.ingest_data_dir, relpath)
	data_path = '/home/ostwald/Documents/NSDL/Backpack/curriculum-data/html-2011-5-5/Aerospace Technology Class/Astronomy 3.0b_v2_files/sheet012.htm'
	topicData = TopicData(data_path, 3)
	print topicData
