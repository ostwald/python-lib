"""
update metadata based on vocab terms which are being changed.

input spreadsheets for various vocab fields (instName, pubName, eventName). 
  each spreadsheet has two columns:
    Bad Term | Good Term

affect: all osm records in the repository containing given Bad Term must be 
modified to replace it for Good Term
"""
import os, sys
from JloXml import XmlUtils
from ncar_lib.osm import osmRecord
from ncar_lib.repository import RepositorySearcher, OsmSearchResult
from ncar_lib.vocabs.termSearch import TermSearcher
from ncar_lib.repository.reports.vocabs import vocab_data
from ncar_lib.repository import CachingRecordManager, CachedRecordError
from vocabWorksheet import ReplaceWorkSheet

def getVocabField (vocabName):
	"""
	returns an index field for the vocab specified by vocabName
	- e.g., getVocabField ('eventname')  
		returns '/key//record/general/eventName'
	
	in the case of pubName, we have two sets of params. but both
	have same vocab_field, which is all we care about. so we simply
	use the first ...
	
	vocab_field may be a list (e.g., in the case of instName) so the consumers
	of this function have to handle both a string and a list of index fields
	- e.g., getVocabField ('instname')  
		returns [
				'/key//record/contributors/person/affiliation/instName',
				'/key//record/contributors/organization/affiliation/instName'
				]
	"""
	try:
		vocab_params = vocab_data.collection_params[vocabName.lower()]

		if type(vocab_params) == type([]):
			vocab_params = vocab_params[0]
		
	except:
		raise Exception, "vocab data not found for %s" % vocabName
	return vocab_params['vocab_field']

def getFieldXpath (indexField):
	"""
	indexField: e.g., '/key//record/contributors/organization/affiliation/instName'
	chop the '/key//' off
	"""
	return indexField[len('/key//'):]
	
def replaceVocabTerm (badTerm, goodTerm, vocab, osmRec):
	"""
	field used to obtain vocab info from vocab_data
	"""
	vocabField = getVocabField (vocab)
	
	# say the field is 'instName'
	# print 'type of indexField: %s' % type(vocabField)
	# print vocabField
	if type(vocabField) == type('') or  type(vocabField) == type(u''):
		vocabField = [vocabField]
	
	for indexField in vocabField:
		xpath = getFieldXpath (indexField)
		# print 'xpath: %s' % xpath
		vocabNodes = osmRec.selectNodes (osmRec.dom, xpath)
		# print '%d vocabNodes found' % len(vocabNodes)
		for node in vocabNodes:
			value = XmlUtils.getText(node)
			if value == badTerm:
				# print 'old:', value
				XmlUtils.setText(node, goodTerm)
				# print 'new:', XmlUtils.getText(node).encode('utf-8')
				print ' .. replaced'
	return osmRec
	
def getXlsDataPath (vocab):
	xlsPath = None
	if vocab.lower() == 'eventname': return 'replace_data/eventName.txt'
	if vocab.lower() == 'instname': return 'replace_data/instName.txt'
	if vocab.lower() == 'pubname': return 'replace_data/pubName.txt'
	
	raise Exception, "could not find xlsDataPath for '%s'" % vocab
	
def updateOsmRecordsForVocab (vocab, verbose=False):
	"""
	update all the records in the repository for the specified vocab
	
	1 - (badTerm, goodTerm) pairs are read from a spreadsheet
	2 - for each pair, find all records containing the badTerm
	3   - for each record found, replace all occurances of badTerm with goodTerm
	"""
	if not verbose:
		stdout = sys.stdout
		logFile = vocab + '_log'
		print 'writing to %s' % logFile
		sys.stdout = open(vocab + '_log', 'w')
	
	recMgr = getRecordManager()
	xlsPath = getXlsDataPath (vocab)
	termPairs = ReplaceWorkSheet (xlsPath)
	
	for i, pair in enumerate(termPairs):
		recIds = findRecordsContainingTerm (pair.badTerm, vocab)
		stdout.write('%d/%d - %s (%d recs)\n' % (i, len(termPairs), pair.badTerm.encode('utf-8'), len(recIds)))
		# print '%d records found for %s' % (len(recIds), pair.badTerm)
		print '\n"%s" (%d)' % (pair.badTerm.encode('utf-8'), len(recIds))
		print ' replacing with "%s"' % pair.goodTerm.encode('utf-8')
		for recId in recIds:
			try:
				osmRec = recMgr.getCachedRecord(recId)
				replaceVocabTerm (pair.badTerm, pair.goodTerm, vocab, osmRec)
				print ' %s' % osmRec.getId()
				recMgr.cacheRecord(osmRec)
			except CachedRecordError, msg:
				print 'CachedRecordError: %s' % msg
		
	if not verbose:
		sys.stdout = stdout
	
def findRecordsContainingTerm (term, vocab):
	vocabField = getVocabField (vocab)
	ids = []
	def add (id):
		# print 'add', id
		if not id in ids:
			ids.append(id)
		else:
			print '  DUP (%s)' % id
	if type(vocabField) == type("") or type(vocabField) == type(u""):
		vocabField = [vocabField]
	for indexField in vocabField:
		searcher = TermSearcher (term, indexField)
		for recId in map (lambda x:x.recId, searcher.data):
			add(recId)
	return ids
	
	
def getRecordsContainingTerm():
	term = "Journal of Geophysical Research - Atmospheres"
	vocab = "pubName"
	vocabField = getVocabField (vocab)
	searcher = TermSearcher (term, vocabField)
	print (searcher.report())
	
	#osm-7-28.tgz

def getRecordManager():
	searchBaseUrl = "http://nldr.library.ucar.edu/schemedit/services/ddsws1-1"
	baseCachePath = "records/osm"
	return CachingRecordManager(searchBaseUrl=searchBaseUrl, baseCachePath=baseCachePath)
	
def updateAll ():
	for vocab in ['eventName', 'instName', 'pubName']:
		updateOsmRecordsForVocab (vocab)
		
if __name__ == '__main__':
	# term = 'The American Astronomical Society'
	vocab = 'eventName'
	# vocab = 'instName'
	# vocab = 'pubName'
	# updateOsmRecordsForVocab (vocab)
	updateAll()
	

