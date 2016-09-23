"""

TASK 5. Update /record/rights/copyrightNotice/@type = "Public domain",
"Publisher", "UCAR Open Access Policy", "UCAR ownership", "Unknown". 

a. For 
entry, delete the contents of /record/rights/copyrightNotice/@type and remove
the attribute because it is optional.


<copyrightNotice holder="Author" type="UCAR ownership">1966 Copyright Warren Washington</copyrightNotice>
should go to
<copyrightNotice holder="Author">1966 Copyright Warren Washington</copyrightNotice>


"""

from JloXml import XmlUtils

typesToRemove = ["Public domain", "Publisher", "UCAR Open Access Policy", "UCAR ownership", "Unknown"]

verbose = 1

def predicate (osmRecord):
	"""
	action will fire if there is ANY "record/rights/copyrightNotice/@type" node
	in the record. The action will only operate on those having type in typesToRemove
	"""
	if verbose > 1:
		print '... task 5 predicate'
	
	attr = osmRecord.selectSingleNode (osmRecord.dom, "record/rights/copyrightNotice/@type")
	if attr:
		# print osmRecord.getId()
		return True

	return False
	
def action (osmRecord):
	"""
	
	For each copyrightNotice node with a "type" attribute in typesToRemove, 
	remove the type attribute from the copyrightNotice element
	"""
	
	if verbose:
		print '\n-- task 5 action ---'
		
	modified = False
		
	copyrightNotice = osmRecord.selectSingleNode (osmRecord.dom, "record/rights/copyrightNotice")
	if copyrightNotice:
		typeAttr = copyrightNotice.getAttribute('type') 
		if typeAttr in typesToRemove:
			if verbose > 1:
				print "\n", copyrightNotice.toxml()
			copyrightNotice.removeAttribute("type")
			if verbose > 1:
				print "\n", copyrightNotice.toxml()
			modified = True

	# print osmRecord
	return modified
	
if __name__ == '__main__':
	
	# osmPath = '/Users/ostwald/devel/dcs-repos/tiny/records/osm/'
	# format = OsmUpdater(osmPath)
	# collection = format.getCollection (collection)
	# collection.scan (predicate, action)
	
	verbose = 2
	from ncar_lib import OsmRecord
	path = 'test-recs/SOARS-000-000-000-123.xml'
	rec = OsmRecord (path=path)
	if predicate(rec):
		action(rec)
	print rec
