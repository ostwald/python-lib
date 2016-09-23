"""
simple scanner
- count files
- count unique names
"""

import os, sys, re
import bscs.protected

class SimpleScanner:

	def __init__ (self, baseDir, pattern=None):
		self.baseDir = baseDir
		self.filecount = 0	
		self.unique_names = []
		self.pattern = pattern
		self.hits = []

		self.scan(baseDir)
		
	def acceptFileName(self, filename):
		"""
		first cut at rejected a file we encounter as we traverse
		"""
		if filename is None or len(filename) == 0:
			return False
		if filename[0] in ['.', '#','_']:
			return False
		if filename[-1] in ['.', '#', '~']:
			return False
		return True

	def acceptFileToScan (self, path):
		"""
		bolean determining whether this file is scanned
		e.g., typically look for xml files when processing metadata
		"""
		# return os.path.isfile(path) and os.path.basename(path).endswith('.xml')
		return os.path.isfile(path)
		
	def acceptDir(self, path):
		if os.path.basename(path) == 'trash':
			return 0
		return 1

	def processPath (self, path):
		
		filename = os.path.basename(path)
		self.filecount += 1
		if not filename in self.unique_names:
			self.unique_names.append(filename)
		content = open(path, 'r').read()
			
		if self.pattern:
			if content.find(self.pattern) != -1:
				self.hits.append(path)
				
	def scan (self, dirname):
		for filename in os.listdir(dirname):
			# print filename
			if not self.acceptFileName (filename):
				continue
			path = os.path.join (dirname, filename)
			if self.acceptFileToScan(path):
				self.processPath(path)
			if os.path.isdir(path) and self.acceptDir(path):
				self.scan(path)	
			
	def report (self):
		print '%d files in %s' % (self.filecount, self.baseDir)
		print '%d unique filenames' % len(self.unique_names)
		if self.pattern:
			print '%s hits for "%s"' % (len(self.hits), self.pattern)
				
if __name__ == '__main__':
	scanner = SimpleScanner (bscs.protected.getReorgProtectedDir())
	print '%d files in %s' % (scanner.filecount, scanner.baseDir)
	print '%d unique filenames' % len(scanner.unique_names)
