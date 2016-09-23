"""

TASK 6. Update /record/rights/copyrightNotice when /record/general/title/@type =
"Presentation/webcast" or "Poster" or "Newsletter"

For each entry, 

a. set the contents of /record/rights/copyrightNotice be: 
 
	 see globals.copyrightBlurb
 
b.  make the contents of 
	/record/rights/copyrightNotice/@url
	be:
	http://www.ucar.edu/legal/terms_of_use.shtml

"""
from ncar_lib.osm import OsmRecord
from updater import OsmCollectionUpdater, OsmUpdater
from globals import copyrightBlurb, termsOfUseUrl
from JloXml import XmlUtils

verbose = 1

typesToSelect = ["Presentation/webcast", "Poster", "Newsletter"]

def predicate (osmRecord):
	"""
	action will fire if the osmRecord has a title type in typesToSelect
	"""
	
	if verbose > 1:
		print '... task6 predicate'
	
	typeAttr = osmRecord.selectSingleNode (osmRecord.dom, "record/general/title/@type")
	if typeAttr:
		val = typeAttr.nodeValue
		if val in typesToSelect:
			# print "%s - %s" % (val, osmRecord.getId())
			return True


	return False
	
def action (osmRecord):
	"""
	1 - set the copyright blurb
	2 - set /record/rights/copyrightNotice/@url to http://www.ucar.edu/legal/terms_of_use.shtml
	"""
	if verbose:
		print '\n-- task 6 action ---'
	
	copyrightNotice = osmRecord.selectSingleNode (osmRecord.dom, "record/rights/copyrightNotice")
	if not copyrightNotice:
		return False  # but we would expect there to be one ....
		
	if verbose:
		print copyrightNotice.toxml()
	XmlUtils.setText (copyrightNotice, copyrightBlurb)
	copyrightNotice.setAttribute ("url", termsOfUseUrl)
					
	return True
	
if __name__ == '__main__':
	# collection = 'my-osm'
	# osmPath = '/Users/ostwald/devel/dcs-repos/tiny/records/osm/'
	# format = OsmUpdater(osmPath)
	# collection = format.getCollection (collection)
	# collection.scan (predicate, action)
	
	path = 'test-recs/TEST-presentation.xml'
	rec = OsmRecord(path=path)
	if (predicate (rec)):
		action(rec)
		print (rec)
