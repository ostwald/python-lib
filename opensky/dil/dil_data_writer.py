"""

	use case:  resolver has DIL_ID and has to look up ark_id

	pid_map headers: accession_num, ark, pid
	dil_data fields: AccAccession Number, DIL_ID, ark_id

"""
import os, sys, re, time
from UserDict import UserDict
from tabdelimited import TabDelimitedFile, TabDelimitedRecord
from JloXml import XmlRecord, XmlUtils

class MappingXml (XmlRecord):
	
	def __init__ (self):
		stub = '<dil_data timestamp="%s"></dil_data>' % time.asctime()
		XmlRecord.__init__ (self, xml=stub)
		
	def addMapping (self, table_rec):
		el = self.addElement(self.doc, 'mapping')
		el.setAttribute('ark', table_rec['ark'])
		el.setAttribute('accession_num', table_rec['accession_num'])
		el.setAttribute('pid', table_rec['pid'])
		el.setAttribute('dil', table_rec['dil_id'])
		
	def __len__ (self):
		return len(self.getElements(self.doc))
		
	def write (self, path):
		XmlRecord.write(self, path)
		print 'wrote to ', path


class PidMappingTable (TabDelimitedFile):
	linesep = '\n'
	fieldsep = ','
	fields = ['accession_num', 'ark', 'dil_id', 'pid']
	
	def __init__ (self, file):
		TabDelimitedFile.__init__(self)
		self.file = file
		self.read(file)
		self.accession_numMap = None
		print '--%d' % len(self)
	
	def splitline (self, line):
		"""
		split the line of data into fields.
		override for csv, etc
		"""
		return line.split(self.fieldsep)
	
	def preprocess (self, filecontents):
		headers = self.fieldsep.join(self.fields)
		return headers + self.linesep + filecontents
	
	def getMappingsXml (self):
		mappings = MappingXml()
		for record in self:
			# self.mapping[record['id']] = record['ark']
			mappings.addMapping(record)
		print 'processed %s (%d)' % (self.file, len(self.data))
		return mappings

	def writeMappingsFile(self, outpath=None):
		outpath = outpath or 'DIL_MAPPINGS.xml'
		mappings = self.getMappingsXml()
		mappings.write (outpath)

if __name__ == '__main__':
	table = PidMappingTable ('EXTRACTED_DIL_DATA.csv')
	print table.writeMappingsFile()

	
