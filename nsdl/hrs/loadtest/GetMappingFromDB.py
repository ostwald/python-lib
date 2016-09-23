import sys, os
from nsdl.nfr import MmdScanner, MmdRecord

def mmdOperation (mmd):
	print mmd.handle, mmd.partnerId

from nsdl.hrs import HrsDB

def getMetadataMapping (partnerId, setSpec):
	query = """SELECT handle, partner_id, setspec 
			   FROM metadata
			   WHERE partner_id='%s' AND setspec='%s'""" % (partnerId, setSpec)
	db = HrsDB()
	results = db.doSelect(query)
	print "%d results found" % len(results)
	if results:
		for result in results:
			print result
	
def mappingOperation (mmd):
	print mmd.partnerId, mmd.setSpec
	getMetadataMapping (mmd.partnerId, mmd.setSpec)
	sys.exit()
	
if __name__ == '__main__':
	repoBase = "/home/ostwald/python-lib/nsdl/nfr/NFR-10-deep"
	scanner = MmdScanner(repoBase, mappingOperation)
	scanner.scan()
