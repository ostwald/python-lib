"""

TASK 13. Remove attributes at /record/contributors/person/@PUBSid (remove values
and the attribute).
"""

from updater import OsmCollectionUpdater
from JloXml import XmlUtils

verbose = 1

def predicate (osmRecord):
	"""
	just apply the action to all records
	"""
	return True

	
def action (osmRecord):
	"""
	remove the PUBSid attribute from all contributors/person elements
	"""
	
	if verbose:
		print '\n-- task 13 action ---'
		
	modified = False
	
	personNodes = osmRecord.selectNodes(osmRecord.dom, 'record/contributors/person')
	for node in personNodes:
		if node.hasAttribute('PUBSid'):
			node.removeAttribute('PUBSid')
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
