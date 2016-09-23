import os, sys

host = os.getenv("HOST")
# print host
if host == "acorn" or host == "oak":
	productionDataPath = "/home/ostwald/Documents/NCAR Library/metadata/production-data"
elif host is None or host == "dls-sanluis":
	productionDataPath = "H:/Documents/NCAR Library/metadata/production-data"
else:
	# raise Exception, "Unknown host: %s" % host
	print 'WARNING host not recognized (%s)' % host


library_dc_path = os.path.join (productionDataPath, 'library_dc')

technotes_path = os.path.join (library_dc_path, 'technotes')

rec_path = os.path.join (technotes_path, "TECH-NOTE-000-000-000-736.xml")

sample_rec = "c:/tmp/NCAR_LIB/lib_dc_rec.xml"

field_specs = {
	'recordID' : 0,
	'dateCataloged' : 0,
	'URL' : 0,
	'volume' : 0,
	'issue' : 0,
	'source' : 1,
	'title' : 1,
	'altTitle' : 1,
	'earlierTitle' : 1,
	'laterTitle' : 1,
	'creator' : 1,
	'contributor' : 1,
	'description' : 1,
	'date' : 1,
	'dateDigitized' : 0,
	'subject' : 1,
	'instName' : 1,
	'instDivision' : 1,
	'libraryType' : 1,
	'otherType' : 1,
	'format' : 1,
	'identifier' : 1,
	'language' : 1,
	'relation' : 1,
	'coverage' : 1,
	'rights' : 1,
	'publisher' : 1
}
