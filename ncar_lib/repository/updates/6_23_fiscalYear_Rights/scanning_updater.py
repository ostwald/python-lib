"""
OSM Fiscal Year and Rights information updater

This module calls the repository scanner classes, AFTER having set
the CollectionScanner.record_action method to call a function on each record
in the collection.

for now, updateFiscalYear is called.


"""
import os, sys
# from ncar_lib.repository import RepositoryScanner, FormatScanner, CollectionScanner, Record
from ncar_lib.repository.repo_scanner import CollectionScanner, FormatScanner
from osmRecordUpdater import OsmRecordUpdater

# Action definitions

# repo_base = '/Users/ostwald/devel/python-lib/ncar_lib/repository/updates/6_23_fiscalYear_Rights/records'
repo_base = '/home/ostwald/python-lib/ncar_lib/repository/updates/6_23_fiscalYear_Rights/records'

## --- SET-Up - define action functions that will get called for the appropriate scanners
## NOTE: action functions are called with a scanner as first param
def showCollectionName (collectionScanner):
	print 'updating collection: %s' % collectionScanner.name

def updateFiscalYear (scanner, osmRecord):
	# print "updateFiscalYear %s" % osmRecord.getId()
	recordUpdater = OsmRecordUpdater (xml=osmRecord.doc.toxml())
	print 'record updater instantiated for %s' % osmRecord.getId()

CollectionScanner.my_action = showCollectionName
CollectionScanner.record_action = updateFiscalYear
	
if __name__ == '__main__':
	print
	path = os.path.join (repo_base, 'osm/jkuettner')
	CollectionScanner(path)
		

