"""
encapsulates the ASN URI Resolver service.

given an asn identifier (purl) returns information about that standard and it's document
"""

import sys, os, site, urllib
import string
import time
import exceptions

from serviceclient import ServiceClient
from JloXml import XmlRecord, XmlUtils
from UserDict import UserDict
from asnHelper import AsnHelper, HelperResponse

basePath = "/home/ostwald/python-lib/catServiceClient/asnUriService/static-asn-files"

class OffLineHelper (HelperResponse):
	
	url = None
	kludge_mappings = None
	
	def __init__ (self):
		UserDict.__init__ (self, self.kludge_mappings)
		self.rec = XmlRecord (self.path)
		self.rec.xpath_delimiter = "/"
		self.root = self.rec.doc
		self.processRec ()
			
class OffLineTopicHelper  (OffLineHelper):
	
	path = os.path.join (basePath, "ASNTopic.xml")
	
class OffLineAuthorHelper  (OffLineHelper):
	
	path = os.path.join (basePath, "ASNJurisdiction.xml")
	
	kludge_mappings = {
		'NAEP':'NAEP'
		}

class OffLineAsnHelper (AsnHelper):
	
	def __init__ (self):
		self.topics = OffLineTopicHelper()
		self.authors = OffLineAuthorHelper()
	
		
def offLineAsnHelperTester ():
	# TopicHelper().report()
	helper = OffLineAsnHelper()

	print "\nAUTHORS"
	helper.authors.report()

	print "\nTOPICS"
	helper.topics.report()
	
def offLIneTopicHelper ():
	topics = OffLineTopicHelper()
	topics.report()
	
if __name__ == '__main__':
	offLineAsnHelperTester()

	



