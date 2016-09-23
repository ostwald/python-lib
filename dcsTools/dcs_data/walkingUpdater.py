"""
updates editor if the editor listed in the most recent status entry is obsolete. 
"""
import os, string
from nsdlToLdap_Globals import *


class Updater:
	
	def __init__ (self, path):
		self.rec = DcsDataRecord (path)
		print self.rec.getId();
		# print path;
		
class WalkingUpdater:
	"""
	recursively visits an entire directory structure and update all the .xml
	files it finds
	"""
	
	UPDATER_CLASS = Updater
	verbose = 0
	
	def __init__ (self, basePath, updaterClass=None):
		if not os.path.exists (basePath):
			raise IOError, "Directory does not exist at %s" % basePath
		
		if updaterClass:
			self.UPDATER_CLASS = updaterClass	
		self.visit (basePath)
		
	def acceptFile (self, fileName):
		"""
		determines which files are acted upon
		"""
		baseName, ext = os.path.splitext (fileName)
		if ext.lower() == '.xml':
			return 1
		
	def acceptDir (self, dirName):
		"""
		determine whether to visit this directory
		"""
		return 1
			
	def prtln (self, s):
		if self.verbose:
			print s
			
			
	def visit (self, baseDir):
		"""
		visits each file under baseDir (what order)
		calls UPDATER_CLASS, 
		which pereforms its action in it's __init__ method
		"""
		## print "visiting %s" % baseDir
		for root, dirs, files in os.walk (baseDir):
			for name in dirs:
				if not self.acceptDir (name):
					dirs.remove (name)
				else:
					self.prtln (name)
					pass
			for name in files:
				if self.acceptFile (name):
					## print "\t updating " + name
					self.UPDATER_CLASS (os.path.join (root, name))
					self.prtln ("\t walker updated %s" % name)
				


if __name__ == "__main__":
	print TEST_DATA_DIR
	# start = os.path.join (DCS_DATA_DIR, 
	startingPoint = TEST_DATA_DIR
	WalkingUpdater (startingPoint)
	

