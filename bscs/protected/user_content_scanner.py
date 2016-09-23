"""
simple scanner
- count files
- count unique names
"""

import os, sys, re
import bscs.protected
from simple_scanner import SimpleScanner

class UserContentScanner (SimpleScanner):
	
	def __init__ (self, baseDir, pattern=None):
		SimpleScanner.__init__(self, baseDir, pattern)
		
	def acceptFileToScan (self, path):
		"""
		bolean determining whether this file is scanned
		e.g., typically look for xml files when processing metadata
		"""
		return os.path.isfile(path) and os.path.basename(path).endswith('.xml')
	
	def processPath (self, path):
		SimpleScanner.processPath(self, path)

def doScan (baseDir, pattern):
	scanner = SimpleScanner (baseDir, pattern)
	print '%d files in %s' % (scanner.filecount, scanner.baseDir)
	print '%d unique filenames' % len(scanner.unique_names)
	if scanner.pattern:
		print '%s hits for "%s"' % (len(scanner.hits), scanner.pattern)
	
if __name__ == '__main__':
	
	pattern = "http://ccs.dls.ucar.edu/home/protected"
	baseDir = bscs.protected.getReorgUserContentRepo()
	scanner = UserContentScanner (baseDir, pattern)
	scanner.report()

