"""
Steps through all data files in specified directory (dataDir), calling
WOSProcessor on each, and writing all metadata records to specified
directory (destDir)
"""

import sys, os, re
from WOS_Processor import WOSProcessor

class WOS_Batch_Processor:
	dataDir = 'WOS_data_files'
	destDir = 'WOS_metadata'
	idpat = re.compile("WOS_([0-9]*?)-.*")
	
	def __init__ (self):
	
		if not os.path.exists (self.destDir):
			os.mkdir (self.destDir)
		
		filenames = os.listdir(self.dataDir)
		filenames.sort()
		for filename in filenames:
			m = self.idpat.match (filename)
			if m:
				startid = int(m.group(1))
			else:
				raise Exception, "id not found in %s" %  filename
			root, ext = os.path.splitext (filename)
			print root, startid
			path = os.path.join (self.dataDir, filename)
			self.processFile (path, startid)
			
	def processFile (self, path, startid):
		WOSProcessor.id_prefix = "WOS"
		WOSProcessor.destDir = self.destDir
		# print "dest: " + WOSProcessor.destDir
		WOSProcessor (path, startid)


		
if __name__ == '__main__':
	WOS_Batch_Processor() # normal invokation

