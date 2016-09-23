"""
Look for same asset files in different collections
"""
import os, sys, time, re
from UserDict import UserDict

class XCollFiles (UserDict):
	
	def add (self, path):
		filename = os.path.basename(path)
		values = self.data.has_key (filename) and self[filename] or []
		values.append (path)
		self[filename] = values
		
	def report (self):
		keys = self.keys()
		keys.sort()
		multiCollKeys = filter (lambda x:len(self[x]) > 1, keys)
		print '%d XCollFiles' % len(multiCollKeys)
		max_times = 0
		for key in multiCollKeys:
			max_times = max(max_times, len(self[key]))
			filename = key
			print filename
			for path in self[key]:
				print '- %s / %s' % (os.path.basename(os.path.dirname(path)), os.path.basename(path))
		print '\n MAX: %d' % max_times
class Scanner:
	"""
	missing attribute holds the paths to uncataloged assets
	"""
	def __init__ (self, root):
		self.root = root
		self.file_cnt = 0
		self.filenames = []
		self.xCollFiles = XCollFiles()
		self.scan (root)
		
	def acceptFilename(self, filename):
		if filename[0] in ['.', '_']:
			return 0
		if filename[-1] in ['~']:
			return 0
		return 1

	def scan (self, dirpath):
		filenames = filter (self.acceptFilename, os.listdir(dirpath))
		print 'scaning %d files for %s ' % (len (filenames), os.path.basename(dirpath))
		for filename in filenames:
			path = os.path.join(dirpath, filename)
			if os.path.isfile(path):
				if filename not in self.filenames:
					self.filenames.append(filename)
				self.xCollFiles.add(path)
				self.file_cnt += 1
				
			elif os.path.isdir(path):
				self.scan (path)
	
def reportMultiCollectionAssets(root):
	scanner = Scanner (root)
	print '%d files found' % scanner.file_cnt
	print '%d unique file names' % len(scanner.filenames)
	print '%d cross-collection file names' % len(scanner.xCollFiles)
	scanner.xCollFiles.report()
			
if __name__ == '__main__':
	protected_dir = '/dls/devweb/ccs-cataloging.dls.ucar.edu/docroot/protected_reorg'
	reportMultiCollectionAssets(protected_dir)

