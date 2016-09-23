"""
This is really all about repoWalker Calibration - a way to ensure that we are 
processing all protectedUrls when we use repoWalker.

curriculum_integrity - assure that a curriculum state is understood.

compares results of two approaches for finding protectedUrls in
curriculum repositories:
- CurriculumScanner - scans all xml files in repository - identifying 
protectedUrls by string search.
- RepoWalker - walks the repository and reads metadata records as XML,
identifying protectedURLs by looking at specific xpaths

We expect the CurriculumScanner to find more records:
- it looks in all directories
- it doesn't care where in the record a protectedUrl occurs.

Approach
- read walker_data (unique ProtectedUrls found by repoWalker)
- read scanner_data (unique ProtectedUrls found by curriculumScanner)

Objective
- use scanner to assure walker's ability to find and rewrite all protectedUrls

- report protectedUrls found in scanner_ but not walker_data
	url, recordId, format

Findings

walker is not catching protectedUrls used as thumbnails in ADN record

e.g.,
<itemRecord>
  ....
  <relations>
    <relation>
      <urlEntry kind="DLESE:Has thumbnail" url="http://ccs.dls.ucar.edu/home/protected/iat/earth_dynamic_geosphere/chap03/ch3a4.jpg"/>
    </relation>
  </relations>
</itemRecord>

When we are sure that walker is finding all protectedUrls, then we can move on to atually doing reorg.
And then we can come back here to test results.

"""

# use CurriculumScanner to resolve protectedUrls to metadata record ids
import os, sys, re
from curriculum_scanner import CurriculumScanner
from protected_urls import ProtectedUrls
from UserList import UserList
import bscs.protected

class UrlListCompare:
	
	def __init__ (self, walker_data, scanner_data):
		baseDir = bscs.protected.getReorgCurriculumRepo()
		self.scanner = CurriculumScanner (baseDir)
		self.walker_urls = ProtectedUrls(walker_data)
		# self.scanner_urls = self.readFile(scanner_data)
		# self.scanner_urls = ProtectedUrls(scanner_data)
		self.scanner_urls = self.scanner.unique_protected_urls
		
		# find the files in scanner_ but not in walker_urls
		self.scanner_only = filter (lambda x:x not in self.walker_urls, self.scanner_urls)
		
		self.walker_only = filter (lambda x:x not in self.scanner_urls, self.walker_urls)
		
	def report(self):
		print "\nURlListCompare results"
		print " - %d walker_urls" % len(self.walker_urls)
		print " - %d scanner_urls" % len(self.scanner_urls)
		self.reportScannerOnly()
		self.reportWalkerOnly()
		
	def reportScannerOnly(self):
		strict = 0
		if len(self.scanner_only) > 0:
			print "\n%d Scanner Only" % len (self.scanner_only)
		for url in self.scanner_only:
			infos = self.scanner.getMetadataInfo(url)
			if infos is None:
				msg = 'WARN: info not found for %s' % url
				if strict:
					raise Exception, msg
				else:
					print msg
					continue
			else:
				# print "- %s\n    %s - %s - %s" % (url, info.recordId, info.collection, info.xmlFormat)
				print "-%s" % url
				for info in infos:
					print "    %s" % info
					
	def reportWalkerOnly(self):
		strict = 0
		if len(self.walker_only) > 0:
			print "\n%d Walker Only" % len (self.walker_only)
		for url in self.walker_only:
			print "-%s" % url
		
	def readFile(self, path):
		lines = open(path, 'r').read().split('\n')
		list = filter (None, map (lambda x:x.strip(), lines))
		return UserList(list)



if __name__ == '__main__':
	walker_data = "REORG_UNIQUE_URLS.txt"
	scanner_data = "CURRICULUM_SCAN_URLS.txt"
	comp = UrlListCompare(walker_data, scanner_data)
	comp.report()
	

		
