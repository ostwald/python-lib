"""
Classes to download PDF files pointed to by Hyperion-based metadata records.
"""
from JloXml import XmlRecord, XmlUtils
from UserDict import UserDict
import os, sys
import urllib
import time

## set up for difffernt platforms
if os.getenv("HOST") == "acorn":
	collectionsDir = "/home/ostwald/Documents/NCAR Library/WebCatMetadata-20080828"
	pdfsDir = "/home/ostwald/python-lib/ncar_lib/pdf"
else:
	collectionsDir = "H:/Documents/NCAR Library/WebCatMetadata-20080828"
	pdfsDir = "H:/python-lib/ncar_lib/pdf"

min_size = 50000 # pdfs below this size are suspected of being bogus ...
doPdfWrites = True
verbose = False

## MetadataRecords that are known to have bogus AccessionNumbers (that don't point to PDFs) and
## that are therefore skipped by the retrieval process
## NOTE: this information should also be recorded in the status records for the metadata records in
## the webcat collections.
skiplist = {
	"NCAR Technical Notes" : [ 
		"TECH-NOTE-000-000-000-001", # bogus AcessionNum ("dr1")
		"TECH-NOTE-000-000-000-509", # unavailable in PDF format ...
		"TECH-NOTE-000-000-000-571", # unavailable in PDF format ...
		"TECH-NOTE-000-000-000-237", # STAFF AccessLevel
		"TECH-NOTE-000-000-000-510", # STAFF AccessLevel
		"TECH-NOTE-000-000-000-518", # STAFF AccessLevel
		"TECH-NOTE-000-000-000-570", # STAFF AccessLevel
		"TECH-NOTE-000-000-000-840", # STAFF AccessLevel + bogus (dup) accessionNum (837)
		],
	"Cooperative Theses" : [
		"THESES-000-000-000-788",    # Bogus pdf
		"THESES-000-000-000-786",    # Bogus pdf
		],
	"NCAR Translations" : [
		"TRANSLATION-000-000-000-878" # Bogus pdf
		]
	}

class WebCatRecord (XmlRecord):
	
	def __init__ (self, path):
		XmlRecord.__init__ (self, path=path)
		self.path = path
		self.filename = os.path.basename (self.path)
		self.accessionNum = self._get_field ("accessionNum")
		self.recordID = self._get_field("recordID")
		self.url = self._get_field("url")
	
	def _get_field (self, qName):
		try:
			return XmlUtils.getChildText (self.doc, qName)
		except:
			msg = "_get_field error: %s" % sys.exc_info()[1]
			raise Exception, msg
			
	def download (self, dest):
		try:
			if doPdfWrites:
				(fn, info) = urllib.urlretrieve (self.url, dest)
				print "wrote to %s" % fn
			else:
				print "WOULD HAVE downloaded %s" % self.url
				return
		except:
			msg = sys.exc_info()[1]
			raise Exception, msg
			
		if os.path.getsize(dest) < min_size:
			msg = "Suspected bogus pdf file at %s (%s)" % (os.path.basename(dest), self.filename)
			raise Exception, msg 
	
class PdfCollectionTool (UserDict):

	def __init__ (self, mdDir, pdfDir):
		UserDict.__init__ (self)
		self.mdDir = mdDir  # this collection's metadata directory
		self.pdfDir = pdfDir  # this collection's pdf directory (may not exist)
		self.collName = os.path.basename (mdDir)
		
		## print "%s\n\tmd: %s\n\tpdf: %s" % (self.collName, self.mdDir, self.pdfDir)
		
	def values(self):
		self.read()
		values = []
		for key in self.keys():
			values.append (self[key])
		return values
		
	def keys(self):
		self.read()
		keys = self.data.keys()
		keys.sort()
		return keys
		
	def getPdfPath (self, rec):
		pdfFileName = rec.accessionNum  + ".pdf"
		return os.path.join (self.pdfDir, pdfFileName)
		
	def read (self):
		if self.data: return
		for mdfilename in os.listdir (self.mdDir):
			if not mdfilename.lower().endswith(".xml"):
				continue
			try:
				rec = WebCatRecord (path=os.path.join (self.mdDir, mdfilename))
				self[rec.recordID] = rec
			except:
				msg = "metadata read error (%s): %s" % (mdfilename, sys.exc_info()[1])
				## raise Exception, msg
				print msg
				continue
		
	def status (self):
		missing = []
		records = self.values()
		for rec in records:
			if self.isSkipRec (rec):
				continue
			dest = self.getPdfPath (rec)
			if not os.path.exists (dest):
				flag = "%s (%s)" % (rec.recordID, rec.accessionNum)
				missing.append (flag)
				
		print "%s status" % self.collName
		print "%d records missing pdf files" % len (missing)
		if missing:
			for m in missing:
				print "\t%s" % m
		return missing
			
	def isSkipRec (self, rec):
		if self.collName not in skiplist.keys():
			return False
		colList = skiplist[self.collName]
		return colList and rec.recordID in colList
				
	def retrieve (self):
		# make sure the directory to which we are writing pdfs exists
		if not os.path.exists (self.pdfDir):
			os.makedirs (self.pdfDir)
			
		num = 0
		max = 40
		for rec in self.values():

			if self.isSkipRec (rec):
				print "skipping %s (on skip list)" %  rec.accessionNum
				continue
			
			if not rec.url:
				print "no url found for %s - skipping" % rec.recordID	
				continue
				
			dest = self.getPdfPath (rec)
			if os.path.exists (dest):
				if verbose:
					print "%s exists" % os.path.basename(dest)
				continue
	
			try:
				time.sleep(5)
				print "\n%d: %s" % (num+1, time.ctime())
				rec.download (dest)
			except KeyboardInterrupt:
				print "Keyboard Interrupt: Exiting now ..."
				sys.exit()
			except:
				print "download error: ", sys.exc_info()[1]
				continue
				
			num = num + 1
			if num == max: break

		print "Done retrieving %s" % self.collName

class PdfTool (UserDict):
	
	def __init__ (self, metadataBaseDir=None, pdfBaseDir=None):
		
		UserDict.__init__ (self)
		self.mdBase = metadataBaseDir or collectionsDir # top level metadata directory
		self.pdfBase = pdfBaseDir or pdfsDir # top level pdf directory (may be empty)
		for collectionName in os.listdir (self.mdBase):
			mdDir = os.path.join (self.mdBase, collectionName)
			pdfDir = os.path.join (self.pdfBase, collectionName)
			self[collectionName] = PdfCollectionTool (mdDir, pdfDir)
			
	def retrieve (self, collection=None):
		if collection:
			collections = [self[collection]]
		else:
			collections = self.values()
		for collection in collections:
			collection.retrieve()
			
	def status (self, collection=None):
		if collection:
			collections = [self[collection]]
		else:
			collections = self.values()
		for collection in collections:
			collection.status()

def downloadtester():
	# path ="H:/python-lib/ncar_lib/WebCatMetadata/Monographs/MONOGRAPH-000-000-000-280.xml"
	collection = "NCAR Technical Notes"
	mdFileName = "TECH-NOTE-000-000-000-233.xml"
	mdPath = os.path.join (collectionsDir, collection, mdFileName)
	rec = WebCatRecord (mdPath)
	anum = XmlUtils.getChildText (rec.doc, "accessionNum")
	url =  XmlUtils.getChildText (rec.doc, "url")
	print "Accession #: " + anum
	print "url: " + url
	print "path: " + rec.path
	
	dest = os.path.join ("pdf", rec.accessionNum + ".pdf")
	
	rec.download(dest)
	
def tester():
	tool = PdfTool ()
	collection = "NCAR Technical Notes"
	tool.retrieve (collection)
	# tool.status (collection)

	
if __name__ == "__main__":

	# collectionsDir = "WebCatMetadata"
	collection = "NCAR Technical Notes"
	
	# downloadtester()
	# PdfTool ().status()
	tool = PdfTool ()
	## tool.retrieve(collection)
	tool.status()
	

	

