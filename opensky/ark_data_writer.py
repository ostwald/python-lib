"""
OBSOLETE as of 10/14/15

Read a single arkData file (cloned from libroot repo) and output a arkMapping file
that is used by nldr citableURL resolver (see nldr-project)
"""

import os, sys, re, time
from UserDict import UserDict
from tabdelimited import TabDelimitedFile, TabDelimitedRecord
from JloXml import XmlRecord, XmlUtils

class MappingRecord (XmlRecord):
	
	def __init__ (self):
		stub = '<arkMappings date="%s"></arkMappings>' % time.asctime()
		XmlRecord.__init__ (self, xml=stub)
		
	def addMapping (self, ark_id, osm_id):
		el = self.addElement(self.doc, 'mapping')
		el.setAttribute('arkId', ark_id)
		el.setAttribute('osmId', osm_id)
		
	def __len__ (self):
		return len(self.getElements(self.doc))
		
	def write (self, path):
		XmlRecord.write(self, path)
		print 'wrote to ', path

class ArkDataTable (TabDelimitedFile):
	linesep = '\n'
	fieldsep = ','
	fields = ['id', 'ark', 'islandora', 'citableUrl']
	
	def __init__ (self, file):
		TabDelimitedFile.__init__(self)
		self.file = file
		self.read(file)
	
	def splitline (self, line):
		"""
		split the line of data into fields.
		override for csv, etc
		"""
		return line.split(self.fieldsep)
	
	def preprocess (self, filecontents):
		headers = self.fieldsep.join(self.fields)
		return headers + '\n' + filecontents
	
	
	def getMappingsXml (self):
		mappings = MappingRecord()
		for record in self:
			# self.mapping[record['id']] = record['ark']
			mappings.addMapping(record['ark'],record['id'])
		print 'processed %s (%d)' % (self.file, len(self.data))
		return mappings

	def writeMappingsFile(self, outpath=None):
		outpath = outpath or 'ARK_MAPPINGS.xml'
		mappings = self.getMappingsXml()
		mappings.write (outpath)

def tableTester (file):
	table = ArkDataTable (file)
	print 'table has %d records' % len(table.data)

	for i, row in enumerate(table):
		print '%d - %s -> %s' % (i, row['id'], row['ark'])
	table.writeMappingsFile()

if __name__ == '__main__':
	# path = '/Users/ostwald/devel/github/libroot/production/identifiers/archives_ezid_pid_production_map.csv'
	path = '/Users/ostwald/devel/git/libroot/production/identifiers/archives_ezid_pid_production_map.csv'
	tableTester (path)
