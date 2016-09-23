import sys, os, string
from ncar_lib.lib import globals, webcatUtils, AccessNumMapping
import utils

pdfDir = globals.pdf
path = globals.mappingDataPath

class PdfAccessNumMapping (AccessNumMapping):
	
	failOnKeyError = True  # fail if there are duplicate accessionNumbers
	failOnValueError = True # fail if there are dup ids
	verbose = True
	
	def __init__ (self, data_path, pdfDir):
		AccessNumMapping.__init__ (self, data_path)
		self.pdfDir = pdfDir
		self.verifyKeys()
		self.verifyPdfFiles()

	def verifyKeys (self):
		"""
		does a pdf file exist for each mapping/key?
		"""
		
		missing = []
		for num in self.keys():
			id = self[num]
			path = self.getPdfPath (id, num)
			if not os.path.exists (path):
				# print "pdf does not exist for %s (%s)" % (id, num)
				missing.append (num)
		if missing:
			print "\nKeys without corresponding PDF files"
			for num in missing:
				print "\t", num
		else:
			print "\nAll keys have corresponding PDF files"
			
	def verifyPdfFiles (self):
		"""
		does a key exist for each pdf file?
		"""
		missing = []
		for dirname in os.listdir (self.pdfDir):
			dirpath = os.path.join (self.pdfDir, dirname)
			for pdffile in os.listdir (dirpath):
				if not pdffile.endswith ('.pdf'):
					continue
				path = os.path.join (dirpath, pdffile)
				root, ext = os.path.splitext (pdffile)
				#print root
				if not self.has_key(root):
					print ("missing key: " + root)
					missing.append (path)
		if missing:
			print "\nfiles with no key"
			for path in missing:
				print "\t", path
		else:
			print "\nAll pdf files have corresponding keys"
			
	def getPdfPath (self, id, accessionNum):
		"""
		get path to the pdf file specified by "pdfName"
		- pdfName defaults to the basename of the library_dc URL
		"""
		
		collectionKey = webcatUtils.getCollection (id)
		collection = globals.collectionNameMap[collectionKey]
		return os.path.join (self.pdfDir, collection, accessionNum + ".pdf")
		
	def rename (self, key):
		id = self[key]
		src = self.getPdfPath (id, key)
		dst = os.path.join (os.path.dirname (src), id+'.pdf')
		os.rename (src, dst)
		
			
if __name__ == '__main__':
	am = PdfAccessNumMapping (path, pdfDir)
	# am.rename ('DR000830')
