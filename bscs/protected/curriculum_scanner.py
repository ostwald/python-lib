"""
curriculum scanner - traverses (scans) a directory structure
- count files
- count unique names
"""

import os, sys, re
import bscs.protected
from simple_scanner import SimpleScanner
from UserDict import UserDict

class RecordInfo:
	def __init__ (self, path):
		self.path = path
		self.recordId = os.path.basename(self.path).replace('.xml','')
		self.collection = os.path.basename(os.path.dirname(self.path))
		self.xmlFormat = os.path.basename(os.path.dirname(os.path.dirname (self.path)))
		
	def __repr__ (self):
		# return "- %s - %s - %s" % (self.recordId, self.collection, self.xmlFormat)
		return "- %s - %s - %s \n    - %s" % (self.recordId, self.collection, self.xmlFormat, self.path)

class CurriculumScanner (SimpleScanner):
	
	counter = 0
	
	def __init__ (self, baseDir):
		self.unique_protected_urls = []
		self.protected_url_count = 0
		self.unique_asset_filenames = []
		self.metadata_info = UserDict()
		SimpleScanner.__init__(self, baseDir)
		
	def acceptFileToScan (self, path):
		"""
		bolean determining whether this file is scanned
		e.g., typically look for xml files when processing metadata
		"""
		return os.path.isfile(path) and os.path.basename(path).endswith('.xml')
	
	def processPath (self, path):
		SimpleScanner.processPath(self, path)
		
		content = open(path, 'r').read()
		
		urlPattern= 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
		
		for m in re.finditer(urlPattern, content):
			url = m.group()
			# urlPattern doesn't catch the tag ending at the tail of urls
			for ending in [
				'</primaryURL>', 
				'</url>',
				'</urlEntry>',
				'</standardURL>'
			]:
				if url.endswith(ending):
					url = url.replace(ending,'')
			# print '-m: ' + m.group()
			if bscs.protected.isAnyProtectedUrl (url):
				filename = os.path.basename(url)
				if not url in self.unique_protected_urls:
					self.unique_protected_urls.append(url)
					
				if not filename in self.unique_asset_filenames:
					self.unique_asset_filenames.append(filename)
					
				self.protected_url_count = self.protected_url_count + 1
				infos = self.metadata_info.has_key(url) and self.getMetadataInfo(url) or []
				info = RecordInfo(path)
				infos.append(info)
				self.metadata_info[url] = infos
				# print 'just assigned 

	def report (self):
		SimpleScanner.report(self)
		print '\nunique protected URLs: %d (out of %d total)' % (len(self.unique_protected_urls), self.protected_url_count)
		print 'unique asset filenames: %d' % len(self.unique_asset_filenames)
		
	def getMetadataInfo (self, url):
		"""
		returns a LIST of metadata infos for given url
		"""
		if not self.metadata_info.has_key(url):
			return None
		return self.metadata_info[url]
		
	def writeProtectedUrls (self):
		out = 'CURRICULUM_SCAN_URLS.txt'
		self.unique_protected_urls.sort()
		fp = open(out, 'w')
		fp.write ('\n'.join(self.unique_protected_urls))
		fp.close()
		print 'wrote unique protected URLs to ', out

def doScan (baseDir, pattern):
	scanner = SimpleScanner (baseDir, pattern)
	print '%d files in %s' % (scanner.filecount, scanner.baseDir)
	print '%d unique filenames' % len(scanner.unique_names)
	if scanner.pattern:
		print '%s hits for "%s"' % (len(scanner.hits), scanner.pattern)
	
if __name__ == '__main__':
	bscs.protected.curriculum_view = 'reorg'
	baseDir = bscs.protected.getCurriculumRepo()
	scanner = CurriculumScanner (baseDir)
	scanner.report()
	scanner.writeProtectedUrls()
