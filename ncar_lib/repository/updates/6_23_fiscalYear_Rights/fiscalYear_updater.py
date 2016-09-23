"""
Fiscal Year Updater

- see https://wiki.ucar.edu/x/RLqTB

For the Archives and Oral Histories collections, add N/A to EVERY record to
/record/coverage/fiscalYear

For all other OSM formated collections act only on DONE records and use fiscal.
If no fiscal, then use published first. If no published, use created.

case 1 - archives
  - scope - Archives and Oral Histories collections
  - action - set fiscalYear to N/A for EVERY record
  
case 2 - all other OSM collections

  - scope - done records in all other OSM collections
  - action - use the record's date field (/record/coverage/date) to determine fiscalYear:

    * use fiscal if possible (converting to YYYY if necessary)
    * If no fiscal, then use published first.
    * If no published, use created.
	
"""
import os, sys
from ncar_lib.repository import RepositorySearcher, SummarySearcher, CachingRecordManager
from dds_client import ListCollections
from done_recordsSearcher import getDoneRecordIds
from osmRecordUpdater import OsmRecordUpdater, ArchiveRecordUpdater
import updater_globals

CURRENT_HOST = "acorn" # "taos"

class RecordsManager (CachingRecordManager):
	"""
	inialized for the CURRENT_HOST using config data in update_globals
	
	is able to get collection (keys) from web service
	"""
	
	def __init__ (self):
		config = updater_globals.host_configs[CURRENT_HOST]
		if not config:
			raise Exception, "config not found for current host: %s" % CURRENT_HOST

		## Note: disabling puts to DCS for now
		CachingRecordManager.__init__ (self, searchBaseUrl=config['searchBaseUrl'], putBaseUrl=None, baseCachePath=config['records_cache'])
		print "RecordsManager instantiated"
		
	def getCollectionsFromService (self):
		"""
		get collection keys from the web service
		"""
		keys = map (lambda x:x.xmlFormat, ListCollections().results)
		
		return keys
		
	def getArchivalCollectionsFromService():
		return filter (lambda x:x in updater_globals.archival_collections, self.getCollectionsFromService())

		
	def getNonArchivalCollectionsFromService():
		return filter (lambda x:x not in updater_globals.archival_collections, self.getCollectionsFromService()) 
		
class FiscalYearUpdater:
	
	"""
	Update the fiscalYear field for each record in the given collection

	record_updater_class - specifies the osmRecord-based class that will perform
	the update action on each record
	
	"""
	default_updater_class = OsmRecordUpdater
	allow_remote_put = 0 # we won't be writing to remote DCS for now ...
	dowrites = 1
	records_manager_instance = None
	
	def __init__ (self, collection):
		print "\nUpdating %s" % collection
		if not self.dowrites:
			print "  NOTE: no records will be written (dowrites is off)"
		self.collection = collection
		
		if self.records_manager_instance is None:
			# print ("instantiating RecordsManager")
			self.records_manager_instance = RecordsManager()
		self.records_manager = self.records_manager_instance
		
		if collection in updater_globals.archival_collections:
			self.updater_class = ArchiveRecordUpdater
		else:
			self.updater_class = self.default_updater_class
		print "... updater_class: %s" % self.updater_class.__name__
		
		# self.recIds = getDoneRecordIds(collection) # if we're using search to get DONE records
		# if we're using cache to process ALL recs in a collection
		
		self.recIds = self.records_manager.getCachedRecordIds(self.collection)
		
		# do the work - update all records using recIds
		map (self.updateRecord, self.recIds)
		print "... updated %d records" % len (self.recIds)
		
	def updateRecord (self, recId):
		"""
		instantiates either OsmRecordUpdater or ArchiveRecordUpdater, depending 
		self.collection, and then calls updateFiscalYear on it.
		
		only writes when self.dowrites is True
		"""
		if self.collection in updater_globals.archival_collections:
			record = self.records_manager.getCachedRecord(recId, ArchiveRecordUpdater)
		else:
			record = self.records_manager.getCachedRecord(recId, OsmRecordUpdater)
			
		record.updateFiscalYear()
		if self.dowrites:
			self.records_manager.cacheRecord(record)
		else:
			## print "WOULD HAVE cached %s" % record.getId()
			pass

		
def updateArchivalCollections():
	for key in updater_globals.archival_collections:
		ArchiveFiscalYearUpdater (key)
	
skip_collections = []
		
def doUpdate():
	recordsManager = RecordsManager()
	collectionIds = recordsManager.getCachedCollectionIds()
	collectionIds.sort()
	for collectionId in collectionIds:
		if collectionId in updater_globals.archival_collections:
			continue
		if collectionId in skip_collections: 
			print 'skipping %s' % collectionId
			continue
		FiscalYearUpdater (collectionId)
	
def updateOsmCollections():
	"""
	update each of the collections in the cache
	"""
	recordsManager = RecordsManager()
	collections = recordsManager.getCachedCollectionIds()
	map (FiscalYearUpdater, collections)
		
if __name__ == '__main__':
	# FiscalYearUpdater("testosm")
	# updateOsmCollections()
	# updateNotArchivalCollections()
	doUpdate()


