"""
schema for vocabTerm framework is http://nldr.library.ucar.edu/metadata/vocabs/1.0/schemas/vocab.xsd
"""

from JloXml import MetaDataRecord, XmlUtils

class VocabTermRecord (MetaDataRecord):

	xpath_delimiter = '/'
	template_path = 'data/vocab-template.xml'

	id_path = 'vocabTerm/recordID'
	
	xpaths = {
		'id' : 'vocabTerm/recordID',
		'recordDate' : 'vocabTerm/recordDate',
		'fullName' : 'vocabTerm/fullName',
		'supersedes' : 'vocabTerm/otherRecords/supersedes',
		'replaces' : 'vocabTerm/otherRecords/replaces',
		'recordsAffected' : 'vocabTerm/recordsAffected',
		'authority' : 'vocabTerm/sourceInfo/authority',
		'dateVerified' : 'vocabTerm/sourceInfo/dateVerified',
		'type' : 'vocabTerm/type'
		}
	
	def __init__ (self, path=None, xml=None):
		if path is None and xml is None:
			path = self.template_path
		MetaDataRecord.__init__ (self, path=path, xml=xml)
		
	def setFullName (self, term):
		self.set('fullName', term)
		
	def getFullName (self):
		return self.get ('fullName')
		
	def setAuthority (self, auth):
		self.set ('authority', auth)
		
	def setDateVerified (self, date):
		self.set ('dateVerified', date)
		
	def getDateVerified (self):
		return self.get ('dateVerified')
		
	def setRecordsAffected (self, num):
		self.set ('recordsAffected', num)
		
	def getRecordsAffected (self):
		return self.get ('recordsAffected')
		
	def setType (self, vocabType):
		self.set ('type', vocabType)
		
	def getType (self):
		return self.get ('type')
		
	def getSupersedes (self):
		return self.get ('supersedes')
		
	def getReplaces (self):
		return self.get ('replaces')
		
if __name__ == '__main__':
	rec = VocabTermRecord()
	rec.setDateVerified ("2010")
	rec.setFullName ("I am a fullName")
	rec.setAuthority ("NCAR Library")
	rec.setDateVerified ("2012")
	rec.setType ("Institutional name")
	print rec
