"""

TASK 9. Remove /record/classify/status and move the contents to
/record/coverage/date/@type if appropriate and not already present.

Status is a singleton. Possible values are:
	- Accepted
    - In press
    - Presented
    - Published
    - Submitted
    - Unpublished

/record/coverage/date/@type values:
	- Accepted
	- Circa
	- Created
	- Digitized
	- In press
	- Modified
	- Presented
	- Published
	- Reviewer assigned
	- Submitted
	- Unpublished

----------------
from katy 12-16:
We took a look at this yesterday and it turns out we do not need to worry about
the status of unpublished nor worry about the record if it is in the
PUBS-NOT-FY10 collection. So this takes care of all the records. Do NOT map the
status of unpublished to the date type field.
---------------
	
"""

from JloXml import XmlUtils
from updater import OsmCollectionUpdater, OsmUpdater


verbose = 1

def predicate (osmRecord):
	"""
	return true if this record has a status node
	"""
	if verbose > 1:
		print ' ... task 9 predicate'
	return osmRecord.selectSingleNode (osmRecord.dom, "record/classify/status")

	
def action (osmRecord):
	"""
	- remember the status value
	- remove the status node
	- if status value is "unpublished" - do nothing after removing
	- if record is in PUBS-NOT-FY10 collection - do nothing after removing
	- DO create an empty date element if one does not exist for this status value!!
	"""
	
	if verbose:
		print '\n-- task 9 action ---'
	
	modified = False
	statusNode = osmRecord.selectSingleNode (osmRecord.dom, "record/classify/status")
	statusValue = osmRecord.getStatus()

	osmRecord.deleteElement(statusNode)
	modified = True
	if verbose > 1:
		print 'status: %s' % statusValue
	
	if statusValue == None or statusValue.strip() == '' or \
	   statusValue == 'Unpublished' or osmRecord.getId().startswith('PUBS-NOT-FY2010'):
		return modified
	
	if osmRecord.getDate(statusValue) and verbose > 1:
		print 'date found for "%s"' % statusValue
	else:
		osmRecord.setDate ("", statusValue) # empty date value
		
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
		# path = 'test_recs/task9_tester.xml'
		path = '/home/ostwald/tmp/osm-update-testing/osgc/OSGC-000-000-004-410.xml'
		rec = OsmRecord(path=path)
		print rec,'\n-----------------'
		if predicate(rec):
			action(rec)
		print rec
