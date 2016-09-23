"""

NOTE - This should be in dds_search, since there is nothing specific to ncs, nsdl, etc here!

find collections managed in the NCS for which the NDR metadata object UniqueID
property is different from the NCS ID.

update the UniqueID in the NDR Metadata Objects for the items in these
collections to match the NCS ID

"""
import os, sys
from JloXml import XmlRecord, XmlUtils
from UserList import UserList
from serviceclient import ServiceClient

default_baseUrl = "http://ncs.nsdl.org/mgr/services/ddsws1-1"

class ListCollectionsResult(XmlRecord):
	"""
	exposes:
		- recId
		- xmlFormat
		- fileLastModified
		- collection, collectionName
		- storedContent
		- dcsstatus, dcsstatusNote, dcsisValid
		- payload (an XmlRecord instance)
	"""
	
	def __init__ (self, element):
		XmlRecord.__init__ (self, xml=element.toxml())
		self.searchKey = self.getTextAtPath("collection:searchKey")
		self.recordId = self.getTextAtPath("collection:recordId")
		self.xmlFormat = self.getTextAtPath("collection:additionalMetadata:dlese_collect:formatOfRecords")
		self.numRecords = self.getTextAtPath("collection:additionalMetadata:dlese_collect:numRecords")
		self.name = self.getTextAtPath("collection:renderingGuidelines:label")
		
	def __repr__ (self):
		s=[];add=s.append
		for attr in ['name', 'searchKey', 'recordId', 'xmlFormat', 'numRecords']:
			add ('%s: %s' % (attr, getattr(self, attr)))
		return u'\n'.join(s)


class NCSCollections(UserList):

	"""
	does a list collections search
	results are ListCollectionsResult instances
	"""

	response_constructor = ListCollectionsResult
	debug = False
	
	def __init__ (self, baseUrl=default_baseUrl):
		self.params = {'verb':'ListCollections'}
		self.service_client = ServiceClient (baseUrl)
		self.data = self.getResults()
			
	def getResults (self):
		responseDoc = self.get_response_doc()
		responseDoc.xpath_delimiter = ":"
		collectionElements = responseDoc.selectNodes(responseDoc.dom, 'DDSWebService:ListCollections:collections:collection')
		return map (ListCollectionsResult, collectionElements)
		
	def getKeys (self):
		return map (lambda x:x.searchKey, self.data)
		
	def get_response_doc (self):
		client = self.service_client
		request = client.setRequest (self.params)
		if self.debug:
			print request.report()
		response = client.getResponse()
		if self.debug:
			print response.doc
		if response.hasError():
			raise response.error
		
		else:
			return response.doc

			
if __name__ == '__main__':
	colkey = '1200091746382'
	searcher = NCSCollections ()
	print 'searcher found %d results' % len(searcher)
	# for result in searcher.results:
		# result.report()
	for col in searcher:
		print '\n%s' % col
