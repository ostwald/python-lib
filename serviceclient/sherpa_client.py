from ServiceClient import *
from JloXml import XmlUtils
verbose = 0

baseUrl = "http://www.sherpa.ac.uk/romeo/api24.php"

## different forms of params to test ServiceRequest ...
paramsMap = {
	'pub' : "university press",
	'qtype' : 'all'
	}
	
# set the params_obj pased to ServiceRequest
params = paramsMap

def tester ():
	client = ServiceClient (baseUrl)
	request = client.setRequest (params)
	if verbose:
		print request.getUrl()
		print ""
		print request.report()
		
	if 1:
		response = client.getResponse()
		if response.hasError():
			print response.error
	
		if response.doc:
			# print response.doc
			report (response.doc)

class Publisher:
	
	def __init__ (self, element):
		self.id = element.getAttribute("id")
		self.name = XmlUtils.getChildText (element, "name")
		self.homeurl = XmlUtils.getChildText (element, "homeurl")
			
	def __repr__ (self):
		return "(%s) %s - %s" % (self.id, self.name, self.homeurl)
		
def report(rec):
	rec.xpath_delimiter = "/"
	publisherNodes = rec.selectNodes (rec.dom, "romeoapi/publishers/publisher")
	
	print "%d publishers found" % len(publisherNodes)
	publishers = map (Publisher, publisherNodes)
	for pub in publishers:
		print pub.__repr__()
	
			
if __name__ == "__main__":
	tester()
