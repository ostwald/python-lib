"""
do gap-analysis of mapped DR numbers by counting contiguous DRNumbers and 
listing those that are not yet mapped
"""
import os, sys
from JloXml import XmlRecord, XmlUtils
import utils

class Verifier:
	
	def __init__ (self, path, mappingsXpath):
		self.path = path
		self.mappingsXpath = mappingsXpath

	def getDrNumbers(self):
		rec = XmlRecord(path=self.path)
	
		mappings = rec.selectNodes(rec.dom, self.mappingsXpath)
		print '%d mappings found' % len (mappings)
		return map (lambda x: x.getAttribute("drNumber"), mappings)
	
	def reportGaps (self):
		drNumbers = self.getDrNumbers()
		drNumbers.sort()
		drIds = map (int, map (lambda x:utils.getIdNum(x), drNumbers))
	
		for i in range (min (drIds), max(drIds)):
			if i not in drIds:
				print "DR%06d" % i

def verifyOriginal ():
	path = path="output/dr_2_recId_mappings.xml"
	xpath = 'dr_2_recId_mappings:mapping'
	Verifier (path, xpath).reportGaps()

				
if __name__ == '__main__':
	path = "output/FINAL-accessionNumberMappings.xml"
	xpath = 'accessionNumberMappings:mapping'
	Verifier(path,xpath).reportGaps()
