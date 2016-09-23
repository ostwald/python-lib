"""
	adn - http://www.dlese.org/Metadata/adn-item/0.6.50/record.xsd
	adn - http://www.dlese.org/Metadata/adn-item/0.7.00/record.xsd
	dlese_anno - http://www.dlese.org/Metadata/annotation/1.0.00/annotation.xsd
	dlese_collect - http://www.dlese.org/Metadata/collection/1.0.00/collection.xsd
	news_opps - http://www.dlese.org/Metadata/news-opps/1.0.00/news-opps.xsd
	
	
	collection_config - WEB-INF/metadata-frameworks/collection-config/dcsCollectionConfig.xsd
	dcs_data - WEB-INF/metadata-frameworks/dcs-data/dcs-data-v0-0-3.xsd
	framework_config - WEB-INF/metadata-frameworks/framework-config/dcsFrameworkConfig-0.0.2.xsd
	
"""

import sys, os
if (sys.platform == 'win32'):
	sys.path.append ("H:/python-lib")
else:
	sys.path.append ("/home/ostwald/python-lib")

from JloXml import XmlRecord
from PathTool import localize

allSchemaLocs = []

def getSchemaLocation (record):
	sl_attr = record.getSchemaLocation()
	if not sl_attr:
		print "SchemaLocationNotFound", record.path
		return
	try:
		ns, loc = (sl_attr.split()[0], sl_attr.split()[1])
		return loc
	except IndexError:
		print "IndexError: " + sl_attr
	
	
def addSchemaLoc (loc):
	if loc is not None and not loc in allSchemaLocs:
		allSchemaLocs.append (loc)
	
def walk (dir):
	for filename in os.listdir (dir):
		path = os.path.join (dir, filename)
		if os.path.isdir (path):
			print "dir: %s" % path
			walk (path)
		else:
			root, ext = os.path.splitext (filename)
			if not ext.upper() == ".XML":
				continue
			# print "file: %s" % path
			rec = XmlRecord (path=path)
			addSchemaLoc (getSchemaLocation (rec))
	
def testGetSchemaLocation ():
	path = localize ("L:\\ostwald\\tmp\\portableDCS\\records\\oai_dc\\1160751502837\\ES-000-000-000-056.xml")
	record = XmlRecord(path)
	getSchemaLocation (record)	
	
if __name__ == "__main__":
	# path = localize ("L:\\ostwald\\tmp\\portableDCS\\records")
	# path = localize ("/devel/ostwald/SchemEdit/DCS_Installer/records")
	path = localize ("/home/ostwald/tmp/records")
	walk (path)
	print "All Schema Locations"
	for loc in allSchemaLocs:
		print "\t", loc
