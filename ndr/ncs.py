"""
collectionAdopter - we have a directory containing xml files of the following structuure:
	
	ndrMetadataInfo
		ndrHandle
		nsdl_dc
			nsdl_dc:nsdl_dc (this is the root of the nsdl_dc record)
		ncs_item
			record (this is the root of the ncs_item recorc)
			
for each record we want to:
	1 - generate a record ID
	2 - create a ncs_item record
		- set recordID
		- save to recordID+'.xml'
	3 - create a dcs_data Record
		- start with a template
		- set recordID
		- set ndrHandle
		- is there any other info this record needs?
		- save to recordID+'.xml'
"""
import os, sys
from JloXml import XmlRecord, XmlUtils

class NcsItemRecord (XmlRecord):

	xpath_delimiter = "/"
	id_path = "record/general/recordID"

	def __init__ (self, xml):
		XmlRecord.__init__ (self, xml=xml)
		self.id = self.getTextAtPath (self.id_path)
		
	def setId (self, newId):
		self.setTextAtPath (self.id_path, newId)
		
		
		
