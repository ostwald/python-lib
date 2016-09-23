"""

TASK 10. Remove /record/coverage/fiscalYear. Do not move to
/record/coverage/date/@type='fiscalYear' and /record/coverage/date. Rather let
fiscal year be calculated using the only date types of published. If want other
fiscal year stuff then will have to specify date range and type.

"""

from JloXml import XmlUtils
from updater import OsmCollectionUpdater, OsmUpdater


verbose = 1

def predicate (osmRecord):
	"""
	return true if this record has a status node
	"""
	if verbose > 1:
		print ' ... task 10 predicate'
	return osmRecord.selectSingleNode (osmRecord.dom, 'record/coverage/fiscalYear')

	
def action (osmRecord):
	"""
	- remember the status value
	- remove the status node
	- ?? create an empty date element if one does not exist for this status value ??
	"""
	
	if verbose:
		print '\n-- task 10 action ---'
	
	fyNode = osmRecord.selectSingleNode (osmRecord.dom, 'record/coverage/fiscalYear')
	osmRecord.deleteElement(fyNode)
	return True
	
if __name__ == '__main__':
	if 0:
		collection = 'osgc'
		osmPath = '/home2/ostwald/tmp/repo/osm'
		# format = OsmUpdater(osmPath)
		# collection = format.getCollection (collection)
		# print 'scanning...'
		# collection.scan (predicate, action)
	else:
		from ncar_lib.osm import OsmRecord
		path = 'test_recs/task9_tester.xml'
		rec = OsmRecord(path=path)
		if predicate(rec):
			action(rec)
		print rec
