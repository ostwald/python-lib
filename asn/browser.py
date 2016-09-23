import os, sys, string
import AsnGlobals
from HyperText.HTML40 import *
from HtmlDocument import MyDocument
from StdDocumentHtml import StdDocumentHtml
from util import makeKey, SortedDict
from docInfo import DocInfo
from toc import Toc, TopicToc
from catServiceClient.asnUriService.asnHelper import AsnHelper
from catServiceClient.asnUriService.offlineAsnHelper import OffLineAsnHelper

# class Browser

class StandardsBrowser (SortedDict):
	"""
	Creates html files and a toc (table of contents) for standards documents
	in "stdsDr". All html (as well as toc.xml) are written to "destDir"
	"""
	stdsDir = AsnGlobals.sourceDir
	# destDir = AsnGlobals.destDir
	destDir = "browser"
	max_items = 2000
	asnHelperClass = AsnHelper # OffLineAsnHelper #
	
	def __init__ (self, destDir=None):
		self.helper = self.asnHelperClass()
		self.destDir = destDir or self.destDir
		self.toc = TopicToc (helper=self.helper)
		SortedDict.__init__ (self)
		self.read()
		print "%d standards documents read" % len (self.data)
		
	def read (self):
		"""
		read all xml files (standards docs) in a directory
		- create a StdDocumentHtml instance for each asn file
		- add the StdDocumentHtml to a map (key produced by "makeKey")
		- create a toc entry
		"""
		count=0
		filenames = os.listdir (self.stdsDir)
		filenames.sort()
		for filename in filenames:
			if not filename.endswith(".xml"): continue
			try:
				src = os.path.join (self.stdsDir, filename)
				print filename
				stdDoc = StdDocumentHtml (src)
				key = makeKey (stdDoc)
				## self[key] = stdDoc
				self.toc.addEntry (DocInfo (stdDoc))
				stdDoc.write (os.path.join (self.destDir, key+".html"))
				self.toc.writeXml(os.path.join (self.destDir, "toc.xml"))
				stdDoc = None
			except:
				print "could not process '%s': %s" % (filename, sys.exc_info()[1])
				import shutil
				bugs = os.path.join (os.path.dirname(src), 'bugs')
				if not os.path.exists(bugs):
					os.mkdir (bugs)
				shutil.move (src, os.path.join(bugs, filename))
			count = count + 1
			if count >= self.max_items:
				break
	
	def write (self):
		if not os.path.exists (self.destDir):
			os.mkdir (self.destDir)
			
		# for key in self.keys():
			# stdDoc = self[key]
			# stdDoc.write (os.path.join (self.destDir, key+".html"))
			
		self.toc.write (os.path.join (self.destDir, "toc.html"))
		self.toc.writeXml(os.path.join (self.destDir, "toc.xml"))

if __name__ == '__main__':
	sb = StandardsBrowser()
	# sb.tocMap()
	sb.write()
		
