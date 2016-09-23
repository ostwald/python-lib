"""
teach record
"""
import os, sys, re
from JloXml import XmlRecord,XmlUtils, MetaDataRecord

class TeachRecord(MetaDataRecord):
	
	def getInstructionalTagNodes (self, globalSymbol=None):
		nodes = self.selectNodes(self.dom, 'teach:instructionalTag')
		if globalSymbol is not None:
			nodes = filter (lambda x: x.getAttribute('globalSymbol') == globalSymbol, nodes)
		return nodes
	
def teachTester(path=None):
	path = path or 'teach.xml'
	globalSymbol = '+'
	rec = TeachRecord(path=path)
	# print rec
	print '%d instructionalTag Nodes found' % len(rec.getInstructionalTagNodes(globalSymbol))	
		
if __name__ == '__main__':
	dirname = '/dls/devweb/ccs-test.dls.ucar.edu/records/teach/dps'
	for filename in os.listdir(dirname):
		if not filename.endswith('.xml'):
			continue
		path = os.path.join (dirname, filename)
		teachTester( path )
