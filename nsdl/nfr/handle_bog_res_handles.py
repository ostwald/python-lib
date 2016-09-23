"""
handle Bogus Resource Handles
"""
import sys, os, re
from repo_scanner import MmdScanner, MmdRecord
from nsdl.hrs.HRS_Client import getResourceHandle

handlePat = re.compile ("2200/[0-9]*T")

def handleBogusResourceHandles (mmd):
		parent = mmd.selectSingleNode (mmd.dom, 'metaMetadata/resources')
		for node in mmd.getResourceNodes():
			resHandle = node.getAttribute("resourceHandle")
			if not handlePat.match(resHandle):
				print "BOGUS resourceHandle: %s" % resHandle
				resUrl = node.getAttribute("resourceUrl")
				try:
					newHandle = getResourceHandle (resUrl)
					node.setAttribute ("resourceHandle", newHandle)
				except Exception, e:
					raise 'Unable to assign new resource handle: %s' % e
				print mmd
				sys.exit()

def tester ():
	path = '/home/ostwald/python-lib/nsdl/nfr/testers/meta_meta.xml'
	rec = MmdRecord(path, None, None)
	handleBogusResourceHandles(rec)
	
def scanRepo (repoBase):
	scanner = MmdScanner(repoBase, handleBogusResourceHandles)
	scanner.scan()
	
if __name__ == '__main__':
	repoBase = "/home/ostwald/python-lib/nsdl/nfr/NFR-10-deep"
	tester()
