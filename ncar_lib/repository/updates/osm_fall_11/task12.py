"""

TASK 12. Remove all entries of /record/classify/idNumber/@type='PUBID' (remove
values and the type attribute).

"""

from updater import OsmCollectionUpdater, OsmUpdater
from JloXml import XmlUtils


verbose = 1

def predicate (osmRecord):
	"""
	just apply the action to all records
	"""
	return True

	
def action (osmRecord):
	"""
	- remember the status value
	- remove the status node
	- ?? create an empty date element if one does not exist for this status value ??
	"""
	
	if verbose:
		print '\n-- task 12 action ---'
	
	modified = False
	idNumberNodes = osmRecord.selectNodes(osmRecord.dom, 'record/classify/idNumber')
	for node in idNumberNodes:
		if node.getAttribute("type") == 'PUBID':
			osmRecord.deleteElement(node)
			modified = True
	return modified
	
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
		path = 'test_recs/task_12_tester.xml'
		rec = OsmRecord(path=path)
		if predicate(rec):
			action(rec)
		print rec
