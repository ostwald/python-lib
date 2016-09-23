"""
traverse the protected directory

for each asset FILE
- derive a protectedURL
- see if this occurs in the metadata
-- NOTE: before reorg many protectedUrls will NOT be found because
the derived protectedURL is normalized to (ccs.dls.ucar.edu) but the metadata
is not normlized until REORG

protectedUrls are urls cataloged in metadata used to determine orphans.
NOTE: curriculum protectedUrls must be cached previously to running ProtectedScanner.
see curricula_reorg_tools.doCacheUrls()

DEPENDENCY - protectedUrls must first be cached using
curricula_reorg_tools.doCacheUrls()

"""
import os, sys, time, re
from UserList import UserList
from bscs.protected import getMergeProtectedDir, getProtectedUrlForPath, \
						   isBscsProtectedUrl, isCcsProtectedUrl, curriculum_view, \
						   getProtectedDir
from protected_urls import ProtectedUrls
	
class ProtectedScanner:
	"""
	Attributes:
	- orphans - holds the paths to uncataloged assets (assets in protectedDir that
				are not referenced in metadata)
	- file_cnt - number of files in protectedDir
	- unique_names - unique filenames found in protectedDir
	"""
	def __init__ (self, root, url_data_path):
		
		print "instantiating ProtectedScanner"
		print ' - root: %s' % root
		print ' - url_data_path: %s' % url_data_path
		
		self.url_data_path = url_data_path
		self.protectedUrls = ProtectedUrls (url_data_path)
		print '\n%d protectedUrls read from %s' % (len(self.protectedUrls), url_data_path)
		self.root = root
		self.file_cnt = 0
		self.orphans = []
		self.unique_names = {}
		self.scan (root)
		
	def acceptFilename(self, filename):
		if filename in ['_notes', 'UPLOADED']:
			return 0
		if filename[0] in ['.', '_']:
			return 0
		if filename[-1] in ['~']:
			return 0
		return 1

	def scan (self, dirpath):
		for filename in filter (self.acceptFilename, os.listdir(dirpath)):
			path = os.path.join(dirpath, filename)
			if os.path.isfile(path):
				assetUrl = getProtectedUrlForPath(path)
				if assetUrl not in self.protectedUrls.data:
					self.orphans.append(path)
					# print " - assetUrl (%s) not found in data(%s)" % (assetUrl, self.url_data_path)
				cnt = self.unique_names.has_key(filename) and self.unique_names[filename] or 0
				self.unique_names[filename] = cnt + 1
					
				self.file_cnt += 1

				
			elif os.path.isdir(path):
				self.scan (path)
	
	def reportDupNames (self):
		
		print "\n%d Unique Names" % len (self.unique_names.keys())
		dups = {}
		for key in self.unique_names.keys():
			cnt = self.unique_names[key]
			if cnt > 1:
				dups[key] = cnt
				
		keys = dups.keys()
		print ' ... %d duplicate filenames' % len(keys)
		keys.sort (key=lambda x:-dups[x])
		dup_total = 0
		
		for key in keys:
			cnt = dups[key] - 1
			# print (" - %s: %d" % (key, cnt))
			dup_total += cnt
			
		print '\n%d total duplicate assets' % dup_total
	
	
def report(root, url_data):
	"""
	root - the protectedDirectory to scan
	url_data - path to file containing uniqueUrls found in the metadata
		of root.
	
	reports
	- total asset files scanned
	- number of unique filenames found
	- number of asset files that were not cataloged by metadata
	"""
	scanner = ProtectedScanner (root, url_data)
	print '\nProtected Scanner Report'
	print '  root: %s' % root
	print '  reading unique url data from %s\n' % url_data
	print '%d asset files found' % scanner.file_cnt
	print '%d unique filenames' % len(scanner.unique_names.keys())
	print '%d files were not cataloged' % len(scanner.orphans)
	if 0:
		scanner.orphans.sort()
		for m in scanner.orphans:
			print '-',m
	scanner.reportDupNames()
	
	if 0:
		outfile = "SCANNER_OUT.txt"
		fp = open(outfile,'w')
		filenames = scanner.unique_names.keys()
		filenames.sort()
		fp.write('\n'.join(filenames))
		fp.close()
		print 'Wrote filenames to ', outfile
	
	# scanner.protectedUrls.report()
			
if __name__ == '__main__':
	import bscs.protected
	bscs.protected.curriculum_view = "reorg"
	if bscs.protected.curriculum_view == "merge": # before reorg
		root = getMergeProtectedDir()
		url_data = "MERGE_UNIQUE_URLS.txt"
	else: # after reordg
		root = getProtectedDir()
		url_data = "REORG_UNIQUE_URLS.txt"
	report(root, url_data)

