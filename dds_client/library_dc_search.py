import os, sys
from serviceclient.ServiceClient import ServiceClient
from search import RecordGetter
from JloXml import XmlRecord, XmlUtils


baseUrl = "http://nldr.library.ucar.edu/schemedit/services/ddsws1-1"

params = {
	"verb": "Search",
	"xmlFormat": "library_dc",
	}
	
client = ServiceClient (baseUrl)

class LibDcRecord (XmlRecord):
	xpath_delimiter = "/"
	
	def __init__ (self, xml):
		XmlRecord.__init__ (self, xml=xml)
	
	def getValues (self, path):
		nodes = self.selectNodes (self.dom, path)
		dates = []
		for node in nodes:
			dates.append (XmlUtils.getText(node))
		return dates
		
	def getId (self):
		return self.getTextAtPath ('record/recordID')
	
class LibDcGetter (RecordGetter):
	numToFetch = 10000
	
	def __init__ (self, service_client, params):
		RecordGetter.__init__ (self, service_client, params, LibDcRecord)
		
		print "%d total recs read" % len (self.recs)
		
		for path in ["record/date", "record/dateDigitized"]:
			uniqueValues = self.get_unique_values(path)
			uniqueValues.sort()
			print "unique values for '%s'" % path
			for d in uniqueValues:
				print "\t", d

		
	def get_unique_values (self, path):
		ud = []
		for rec in self.recs:
			for d in rec.getValues(path):
				if not d in ud:
					ud.append (d)
		return ud
			
if __name__ == '__main__':
	
	LibDcGetter(client, params)
