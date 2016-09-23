from lxml import etree

class OAIRecordReader: 
	namespaces = {
		'ns0': 'http://www.openarchives.org/OAI/2.0/',
		'mods' : "http://www.loc.gov/mods/v3",
		'xlink' : "http://www.w3.org/1999/xlink",
		'dc': 'http://purl.org/dc/elements/1.1/'
	}
	
	def __init__ (self, path):
		self.root = etree.XML(open(path, 'r').read())
		
		self.title = self.getXpath('//mods:mods/mods:titleInfo/mods:title')
		self.abstract = self.getXpath('//mods:mods/mods:abstract')
		self.setSpec = self.getXpath('//ns0:setSpec')
		
		names = self.root.xpath('//mods:mods/mods:name', namespaces=self.namespaces)
		for name_el in names:
			self.process_contributor (name_el)
		
	def getXpath (self, xpath, namespaces=None):
		namespaces = namespaces or self.namespaces
		try:
			return self.root.xpath(xpath,
								   namespaces=namespaces)[0].text
		except IndexError, msg:
			# nothing found at path
			return None
			
	def process_contributor(self, name_el):
		print etree.tostring(name_el)
		
		print 'type: ' + name_el.get('type')
		family = name_el.xpath('mods:namePart[@type="family"]', namespaces=self.namespaces)[0].text
		print 'family: %s' % family

class ModsReader:
	
	namespaces = {
		'ns0': 'http://www.openarchives.org/OAI/2.0/',
		'mods' : "http://www.loc.gov/mods/v3",
		'xlink' : "http://www.w3.org/1999/xlink"
	}
	
	def __init__ (self, path):
		self.root = etree.XML(open(path, 'r').read())
		self.titleOFF = self.root.xpath('//mods:title',
			namespaces=self.namespaces)[0].text
		
		self.title = self.getXpath('/mods:mods/mods:titleInfo/mods:title')
		self.abstract = self.getXpath('/mods:mods/mods:abstract')
		
	def getXpath (self, xpath, namespaces=None):
		namespaces = namespaces or self.namespaces
		try:
			return self.root.xpath(xpath,
								   namespaces=namespaces)[0].text
		except IndexError, msg:
			# nothing found at path
			return None
		
def modsReaderTester (self):
	path = 'sample-mods.xml'
	reader = ModsReader (path)
	mods = reader.root
	print 'title: %s' % reader.title
	print 'abstract: %s' % reader.abstract
	print 'setSpec: %s' % reader.setSpec
	## print etree.tostring(mods)	
		
if __name__ == '__main__':
	path = 'sample-oai-result.xml'
	reader = OAIRecordReader (path)
	# print etree.tostring(reader.root)
	if 0:
		print 'title: %s' % reader.title
		print 'abstract: %s' % reader.abstract
		print 'setSpec: %s' % reader.setSpec
