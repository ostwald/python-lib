"""
given an xml file with mappings from drNum to RecordID, e.g., 

<dr_2_recId_mappings date="Tue Oct  5 11:35:27 2010">
    <mapping drNumber="DR000768" recordID="ASR-000-000-000-032"/>
	
we want to provide not only the recordID by the collection

<dr_2_recId_mappings date="Tue Oct  5 11:35:27 2010">
    <mapping drNumber="DR000768" recordID="ASR-000-000-000-032" collection="asr"/>
	
we determine the collection from the prefix of the recordID, e.g.,

collection = utils.getCollectionFromId (id)

and then simply add it as an attribute
"""
import os, sys, time
from dr_2_record_ids import DR2RecIdMappings
import utils

class URLResolverMappings (DR2RecIdMappings):

	rootElementName = "accessionNumberMappings"
	
	def __init__ (self):
		DR2RecIdMappings.__init__ (self)
		self.populate()
		
	def populateMappingElement (self, element, drNum):
		element.setAttribute ("drNumber", drNum)
		recId = self[drNum]
		queryString = "collId=%s&itemId=%s" % (utils.getCollectionFromId(recId), recId)
		element.setAttribute ("queryString", queryString)
		
			
if __name__ == '__main__':
	mappings = URLResolverMappings()
	xml = mappings.asXml()
	print xml
	# mappings.report()
	xml.write ('FINAL-accessionNumberMappings.xml')
		

	
