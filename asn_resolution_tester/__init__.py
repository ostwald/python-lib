"""
given a data file with a bunch of entries of the following form:

<GatheredIds>
  <id stdId="http://asn.jesandco.org/resources/S101B8AE" 
  	  docId="http://asn.jesandco.org/resources/D100010D"/>
  ...
</GatheredIds>

	
	
"""

import sys, os
from JloXml import XmlRecord, XmlUtils
from UserDict import UserDict
from asnResolutionClient import AsnResolutionClient

class AsnResolutionTester(UserDict):
	
	def __init__ (self, path):
		self.data = {}
		rec = XmlRecord (path=data)
		## print rec
		rec.xpath_delimiter = "/"
		nodes = rec.selectNodes (rec.dom, 'GatheredIds/id')
		self.asnResolutionClient = AsnResolutionClient()
		print "%d nodes found" % len(nodes)
		
		for node in nodes:
			stdId = node.getAttribute("stdId");
			docId = node.getAttribute ("docId");
			stdIds = []
			if self.has_key(docId):
				stdIds = self[docId]
			stdIds.append(stdId)
			self[docId] = stdIds
			
	def writeIdFile (self, path=None):
		path = path or "asn_id_data.txt"
		ids = [];add=ids.append
		for docId in self.keys():
			add (self[docId][0])
		fp = open(path, 'w')
		fp.write ('\n'.join(ids))
		fp.close()
		print 'wrote to', path
		
	def hitAllDocs (self, path=None):
		for docId in self.keys():
			self.getStandard(self[docId][0])
		
		
	def getStandard (self, asnId):
		self.asnResolutionClient.getStandard(asnId);
		

	
if __name__ == '__main__':
	# data = "HAND-GATHERED.xml"
	data = "gathered-ids.xml"
	tester = AsnResolutionTester(data)
	
	print "ids contains data from %d docs" % len(tester)
	tester.hitAllDocs()


