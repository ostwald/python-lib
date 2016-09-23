"""
WebCatFolders - 

Scrapes folder data from WebCat system as a list of WebCatFolder instances.
"""
import os, sys, re, traceback
from ncar_lib.webcat_scrape.WebCat import WebCat
from WebCatFolder import WebCatFolder

class FolderScraper:
	"""
	url must be higher in the WebCat hierarchy than "collection" (which must a
	collection name in the hierarchy
	"""
	
	def __init__ (self, url, collection, callback):
		self.callback = getattr (self, callback)
		self.url = url
		self.collection = collection
		self.records = self._get_records()
		
		self.showRecords ()
		
		# self.process()

	def showFolders (self):
		print "\n%s folders" % self.collection
		for folder in self.folders:
			print "\t%s" % folder.title
	
	def showRecords (self):
		print "\n%s folders" % self.collection
		for rec in self.records:
			print "\t%s -> %s" % (rec.tn_issue, rec.title)
			
	def get_dest_dir (self):
		destDir = "WebCatFolderData/%s" % self.collection
		if not os.path.exists (destDir):
			os.makedirs(destDir)
		return destDir
			
	def _get_records(self):
		try:
			self.folders = self._get_folder_nodes ()
		except:
			print "could not get folder nodes: %s" % sys.exc_info()[1]
			traceback.print_tb (sys.exc_info()[2])
			sys.exit()
		records = []
		errors = []
		count = len (self.folders)
		for node in self.folders:
			try:
				url = node.metadatapath
				rec = WebCatFolder (url, node)
				records.append (rec)
			except:
				errors.append (sys.exc_info()[1])
				traceback.print_tb (sys.exc_info()[2])
			
		if errors:
			print "\ngetRecords ERRORS:\n" + "\n".join (map (str, errors))
		return records
		
	def process (self):
		print ("processing ...")
		errors = []
		count = len (self.records)
		for i, rec in enumerate (self.records):
			try:
				self.callback (rec, i)
				## indicate progress
				print "%d/%d" % (i, count)

			except:
				errors.append ( "%d/%d: %s" % (i, count, sys.exc_info()[1]))
				# traceback.print_tb (sys.exc_info()[2])
		if errors:
			print "\nProcess ERRORS:\n" + "\n".join (errors)
			
	def _get_folder_nodes (self):
		
		cat = WebCat (self.url)
		root = cat.getNode (self.collection)
		# cat.hierarchy()
		return cat.getComposites (root)
	
	def showRec (self, folderRec, i):
		print "showRec"
		print folderRec.tn_issue
		
	def writeRec (self, folderRec, i):
		destDir = self.get_dest_dir ()
		folderRec.write(str(i), destDir)
		
callback = "writeRec"
	
def run ():
	url = "http://library.ucar.edu/uhtbin/cgisirsi/SCbAaTeMM6/SIRSI/116600007/503/8094"
	collection = "NCAR/TN-85+STR - A Microfilm atlas of magnetic fields in the solar corona."
	folders = FolderScraper (url, collection, callback)
	folders.process()
	

	
if __name__ == '__main__':
	run()
