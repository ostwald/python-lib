"""

TASK 7. Update /record/rights/copyrightNotice when /record/general/title/@type =
"Interactive resource"

a. make the contents of /record/rights/copyrightNotice be: 

	global.copyrightBlurb
	
REVISION

-----------
appears not to be happening at all
so when title type =Interactive resource
 <title type="Interactive resource">Report, Status evalution of numerical weather prediction in Communist China</title>

then make the content of /record/rights/copyrightNotice/ be Copyright. All rights reserved. University Corporation for Atmospheric Research (UCAR). The user is granted the right to use this resource for non-commercial, non-profit research, or educational purposes only, as are more fully described in the UCAR Library Terms of Use.

then make the content of /record/rights/copyrightNotice/@url be http://www.ucar.edu/legal/terms_of_use.shtml


"""
from ncar_lib.osm import OsmRecord
from JloXml import XmlUtils
from updater import OsmCollectionUpdater, OsmUpdater
from globals import copyrightBlurb, termsOfUseUrl

verbose = 1

def predicate (osmRecord):
	"""
	select osmRecords that have a /record/general/title/@type == "Interactive resource"
	"""
	if verbose > 1:
		print ' ... task7 predicate'
	typeAttr = osmRecord.selectSingleNode (osmRecord.dom, "record/general/title/@type")
	
	if typeAttr:
		print "typeAttr!!"
		val = typeAttr.nodeValue
		print "val: %s!!" % val
		if val == "Interactive resource":
			# print "selecting %s" % osmRecord.getId()
			return True

	return False
	
def action (osmRecord):
	"""
	set the copyright blurb
	set /record/rights/copyrightNotice/@url to http://www.ucar.edu/legal/terms_of_use.shtml
	"""
	
	if verbose:
		print '\n-- task 7 action ---'
	
	copyrightNotice = osmRecord.selectSingleNode (osmRecord.dom, "record/rights/copyrightNotice")
	if verbose:
		print copyrightNotice.toxml()
	
	osmRecord.setCopyrightNotice (copyrightBlurb)
	copyrightNotice.setAttribute ("url", termsOfUseUrl)
	
	if verbose:
		print copyrightNotice.toxml()
		
	return True
	
if __name__ == '__main__':
	collection = 'my-osm'
	osmPath = '/Users/ostwald/devel/dcs-repos/tiny/records/osm/'
	# format = OsmUpdater(osmPath)
	# collection = format.getCollection (collection)
	# print 'scanning...'
	# collection.scan (predicate, action)
	
	path = 'test-recs/TEST-interactive.xml'
	rec = OsmRecord (path=path)
	if predicate(rec):
		action(rec)
		print (rec)
