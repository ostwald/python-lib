import os, sys, time

from ncar_lib.repository import *
from record_manager import MyRecordManager
from ncar_lib.repository.put_record import PutRecordClient

searchBaseUrl = "http://localhost:8080/schemedit/services/ddsws1-1"
putBaseUrl = 'http://localhost:8080/schemedit/services/dcsws1-0'
baseCachePath = "/Users/ostwald/tmp/updateCache/osm"

def getRecordManager():
	mgr = MyRecordManager(searchBaseUrl=searchBaseUrl, putBaseUrl=putBaseUrl, baseCachePath=baseCachePath)
	return mgr
	
def putRecord (id, mgr=None):
	if mgr is None:
		mgr = getRecordManager ()
	
	# osmRecord = mgr.getRemoteRecord(id)
	osmRecord = mgr.getCachedRecord(id)
	osmRecord.setTitle(time.ctime())
	# print osmRecord
	
	params = {
		'collection' : mgr.getCollectionKey(id),
		'id' : id,
		'xmlFormat' : 'osm',
		'recordXml' : osmRecord.doc.toxml(),
		'dcsStatusNote' : 'instDiv vocab updated',
		# 'dcsStatus' : 'Final',
		# 'dcsAgent' : "yo mama"
		}
		
	printDict (params, 'put record params')
	
	putRecord = PutRecordClient (params, putBaseUrl)
	print 'putRecord took %d tics' % putRecord.elapsed
	print putRecord.id
	
def printDict (data, name=None):
	if name:
		print "\n%s" % name
	else:
		print ''
	for key in data:
		if key != 'recordXml':
			print '- %s: %s' % (key, data[key])
	
def getRemoteRecord (id):
	mgr = getRecordManager ()
	return mgr.getRemoteRecord(id)
	
if __name__ == '__main__':
	id = 'OSGC-000-000-006-043'
	# rec = osmRecord = getRemoteRecord(id)
	# print rec
	putRecord(id)
