"""
rename pdf files to replace PREFIX with "nldr-asset"
"""
import os, sys

pdfBase = "/home/ostwald/Documents/NCAR Library/pdf"
new_prefix = "asset"
doWrite = 1

def getPrefix (name):
	"""
	extract prefix from name
	"""
	return name[:name.index ("-000")]

def getNewFilename (filename):
	try:
		prefix = getPrefix (filename)
	except:
		raise Exception, "prefix not found"
	# print prefix
	return filename.replace (prefix, new_prefix)

def processAll ():
	for collection in os.listdir (pdfBase):
		processCollection (collection)

def processCollection (collection):
	dir = os.path.join (pdfBase, collection)
	filenames = os.listdir (dir);
	filenames.sort()
	for filename in filenames:
		src = os.path.join (dir, filename)
		newfilename = getNewFilename (filename)
		dst = os.path.join (dir, newfilename)
		if doWrite:
			os.rename (src, dst)
			print "renamed %s to %s" % (filename, newfilename)
		else:
			print "WOULD HAVE renamed %s to %s" % (filename, newfilename)
		
		
if __name__ == "__main__":
	# processCollection ("theses")
	processAll()
