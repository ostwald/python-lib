"""

TASK 11. Update the SOARS collection to have copyright like 6(a). Because per
the Oct 5th OSM working group, student work, unpublished work should have the
UCAR copyright. This should occur because checked on 2011-12-12 to make sure
everything is a manuscript.

"""

from nsdl.updates import getPrefix
from JloXml import XmlUtils
from globals import copyrightBlurb, termsOfUseUrl

verbose = 1
	 
def predicate (osmRecord):
	"""
	just apply the action to all records
	"""
	return getPrefix(osmRecord.getId()) == "SOARS"

	
def action (osmRecord):
	"""
	- remember the status value
	- remove the status node
	- ?? create an empty date element if one does not exist for this status value ??
	"""
	
	if verbose:
		print '\n-- task 11 action ---'
	
	modified = False
	
	copyrightNotice = osmRecord.selectSingleNode (osmRecord.dom, "record/rights/copyrightNotice")
	if not copyrightNotice:
		# raise Exception, "I have to have a copyright!"
		rights = osmRecord.selectSingleNode (osmRecord.dom, 'record/rights')
		if not rights:
			rights = XmlUtils.addElement(osmRecord.dom, osmRecord.doc, 'rights')
		copyrightNotice = XmlUtils.addElement(osmRecord.dom, rights, 'copyrightNotice')
		copyrightNotice.setAttribute ('holder', 'UCAR')
		copyrightNotice.setAttribute ('url', termsOfUseUrl)
		
	if verbose:
		print copyrightNotice.toxml()
	XmlUtils.setText (copyrightNotice, copyrightBlurb)
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
		# path = 'test-recs/SOARS-000-000-000-123.xml'
		path = 'test-recs/SOARS-000-000-000-FOO.xml'
		rec = OsmRecord(path=path)
		if predicate(rec):
			if action(rec):
				print 'would have updated!'
		print rec
