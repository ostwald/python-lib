"""
handle empty resourceUrls
"""
import sys, os
from repo_scanner import MmdScanner, MmdRecord

def handleEmptyResources (mmd):
	for mapping in mmd.resourceMappings:
		if not mapping.url:
			mmd.removeEmtpyResources()
			print mmd
			sys.exit()

def tester ():
	path = '/home/ostwald/python-lib/nsdl/nfr/testers/meta_meta.xml'
	rec = MmdRecord(path, None, None)
	handleEmptyResources(rec)
	
def scanRepo (repoBase):
	scanner = MmdScanner(repoBase, handleEmptyResources)
	scanner.scan()
	
if __name__ == '__main__':
	repoBase = "/home/ostwald/python-lib/nsdl/nfr/NFR-10-deep"
	tester()
