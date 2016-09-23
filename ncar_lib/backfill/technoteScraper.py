"""
scrapes TECHNOTE metadata from provided url and writes record to a file
named for accessionNum
"""
import os, sys
import urllib
from filler_imports import globals, webcatUtils
from ncar_lib.webcat_scrape.WebCatMetadata import WebCatMetadata
from ncar_lib.conversion.webcatframework import WebcatRec
from ncar_lib.conversion.converter import Converter
from ncar_lib.massage.massagingProcessor import MassagingRecordProcessor
from ncar_lib.conversion.mapping.mapper import Mapper

class TechnoteScraper (MassagingRecordProcessor):
	
	doPdfWrites = True
	
	def __init__ (self, url):
		self.mapper = Mapper()
		self.collection = "technotes"
		scraped = WebCatMetadata (url)
		# print scraped
		self.webcat_rec = WebcatRec (xml=scraped.doc.toxml())
		# print webcat_rec
		self.lib_dc_rec = Converter (self.webcat_rec).dest
		# print dc_rec
		self.recId = self.lib_dc_rec.getId()
		self.massage()
		
	def write (self, dirName="backfill-scrapes"):
		path = os.path.join (globals.metadata, dirName, self.recId+'.xml')
		# xml = self.lib_dc_rec.doc.toprettyxml ("\t","\n")
		xml = self.lib_dc_rec.doc.toxml ()
		if not os.path.exists (os.path.dirname (path)):
			os.mkdir (os.path.dirname (path))
		fp = open (path, 'w')
		fp.write (xml)
		fp.close ()
		print "wrote to %s" % path
		
	def getPdf (self):
		min_size = 50000 # pdfs below this size are suspected of being bogus ...
		pdfURL = "http://www.library.ucar.edu/uhtbin/hyperion-image/%s" % self.webcat_rec.accessionNum
		dest = os.path.join (globals.docBase, 'pdf/scraped-technotes', self.recId+'.pdf')
		try:
			if self.doPdfWrites:
				(fn, info) = urllib.urlretrieve (pdfURL, dest)
				print "wrote to %s" % fn
			else:
				print "WOULD HAVE downloaded %s" % pdfURL
				return
		except:
			msg = sys.exc_info()[1]
			raise Exception, msg
			
		if os.path.getsize(dest) < min_size:
			msg = "Suspected bogus pdf file at %s" % (os.path.basename(dest))
			raise Exception, msg

		
if __name__ == '__main__':
	
	url = "http://library.ucar.edu/uhtbin/cgisirsi/fKsl55Cfjj/SIRSI/116600007/511/8097"
	scraper = TechnoteScraper(url)
	scraper.write()
	scraper.getPdf()
	# print scraper.id
