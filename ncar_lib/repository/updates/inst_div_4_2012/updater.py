"""
updater

/Users/ostwald/devel/python/python-lib/ncar_lib/repository/updates/inst_div_4_2012/record_manager.py
"""
import os, sys, time
from record_manager import MyRecordManager
from record_manager import ConfiguredRecordManager
from inst_div_searcher import InstDivSearcher
from ncar_lib.repository.put_record import PutRecordClient
from data_reader import DataTable, DataRecord
from JloXml import XmlUtils

class UpdateManager (ConfiguredRecordManager):
	
	verbose = False
	
	def __init__ (self, config):
		ConfiguredRecordManager.__init__(self, config)
		self.dataTable = DataTable (self.config['data_path'])
		self.indexedSearchBaseUrl = self.config['indexedSearchBaseUrl']
		
	def getPrefixMap (self):
		prefixMap = ConfiguredRecordManager.getPrefixMap(self)
		prefixMap['TESTO'] = 'testosm'
		
		# prefixMap.report()
		return prefixMap
		
	def search (self, vocab, collection=None):
		searcher = InstDivSearcher(vocab, collection, baseUrl=self.indexedSearchBaseUrl)
	
		print 'searcher found %d results for "%s"' % (len (searcher.data), vocab)
		if self.verbose:
			for result in searcher:
				print result.recId
		return searcher

				
	def putRemoteRecord (self, osmRecord):
		id = osmRecord.getId()
		# osmRecord = self.getRemoteRecord(id)
		# osmRecord = self.getCachedRecord(id)
		
		params = {
			'collection' : self.getCollectionKey(id),
			'id' : id,
			'xmlFormat' : 'osm',
			'recordXml' : osmRecord.doc.toxml(),
			'dcsStatusNote' : 'instDiv vocab updated'
			}
			
		putRecord = PutRecordClient (params, self.putBaseUrl)
		print 'putRecord took %d tics' % putRecord.elapsed
		print 'put %s' % putRecord.id

class Updater:
	
	data_path = 'division-name-changes.txt'
	person_field = 'record/contributors/person/affiliation/instDivision'
	org_field = 'record/contributors/organization/affiliation/instDivision'
	
	dowrites = True
	
	def __init__ (self, config):

		self.mgr = UpdateManager(config)
		self.dataTable = DataTable (self.data_path)
		print 'dataTable has %d entries' % len(self.dataTable)
		
	def update (self, collection=None):
		for dataRecord in self.dataTable:
			before = dataRecord.before
			after = dataRecord.after
			
			for xpath in [self.person_field, self.org_field]:
			
				searcher = InstDivSearcher (before, collection, baseUrl=self.mgr.indexedSearchBaseUrl)
				for result in searcher:
					# osmRecord = self.mgr.getCachedRecord (result.recId)
					osmRecord = result.payload
					# print osmRecord
					updatedOsmRecord = self.updateOsmRecord (osmRecord, before, after)
					# print updatedOsmRecord
					
					if not self.dowrites:
						print 'would have put ' + osmRecord.getId()
					else:
						self.mgr.putRemoteRecord (updatedOsmRecord)
			
	def countDirtyRecords (self, collection=None):
		
		vocabTerms = self.dataTable.getVocabTerms()
		print 'countDirtyRecords() %d vocabTerms' % len(vocabTerms)
		count = 0
		for vocab in vocabTerms:
			print vocab
			searcher = InstDivSearcher (vocab, collection, baseUrl=self.mgr.indexedSearchBaseUrl)
			count = count + searcher.numRecords
		return count
		
	# field: 'record/contributors/person/affiliation/instDivision'
	def updateOsmRecord (self, osmRecord, before, after):
		
		for xpath in [self.person_field, self.org_field]:
			nodes = osmRecord.selectNodes (osmRecord.dom, xpath)
			for node in nodes:
				value = XmlUtils.getText(node)
				if self.dataTable.beforeMap.has_key(value):
					XmlUtils.setText(node, self.dataTable.getAfter(value))
					# print '- before: %s, after: %s\n' % (before, XmlUtils.getText(node))
		
		return osmRecord
		
if __name__ == '__main__':
	updater = Updater ("tambora_update")
	if 0:
		print "%d dirty records found" % updater.countDirtyRecords()
	if 0:
		
		rec = updater.mgr.getRemoteRecord('TESTO-000-000-000-088')
		if not rec:
			print "record not retreived"
		else:
			rec.setTitle ("automatically updated at " + time.ctime())
			print rec
			updater.mgr.putRemoteRecord (rec)
	if 1:
		print 'start: ', time.ctime()
		updater.update()
		print 'end: ', time.ctime()
