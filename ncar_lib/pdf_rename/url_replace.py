"""
compare the pdf files to find missing files
"""
import os, sys
from ncar_lib.lib import globals, webcatUtils
from ncar_lib.massage.libDCProcessor import MetadataProcessor, IdListProcessor, LibraryDCRecordProcessor, CollectionProcessor 
from pdf_rename import getNewFilename


CollectionProcessor.rpClass = LibraryDCRecordProcessor
MetadataProcessor.cpClass = CollectionProcessor
IdListProcessor.rpClass = LibraryDCRecordProcessor

def getNewUrl (oldUrl):
	if not oldUrl:
		raise Exception, "No url provided"
	dir, filename = os.path.split(oldUrl)
	newfilename = getNewFilename (filename)
	# print prefix
	return os.path.join (dir, newfilename)

def getNewUrlX (oldUrl):
	if not oldUrl:
		raise Exception, "No url provided"
	filename = os.path.basename(oldUrl)
	try:
		prefix = webcatUtils.getPrefix (filename)
	except:
		raise Exception, "prefix not found"
	# print prefix
	return oldUrl.replace (prefix, new_prefix)

def showId (rp):
	print rp.recId
	
def showUrl (rp):
	print rp.lib_dc_rec.getUrl()
	
def replaceUrl (rp):
	rec = rp.lib_dc_rec
	url = rec.getUrl()
	if not url:
		print "NO URL: " + rp.recId
		return
	try:
		rec.setUrl (getNewUrl (url))
		rec.write()
	except:
		msg = "URL error (%s)\n\turl: %s\n\t--> %s" % (rp.recId, url, sys.exc_info()[1])
		print msg
		sys.exit()
	# print rec.getUrl()
	
if __name__ == "__main__":
	# CollectionProcessor ("manuscripts", replaceUrl)
	MetadataProcessor (showUrl)
	# IdListProcessor (["TECH-NOTE-000-000-000-006"], showUrl)
