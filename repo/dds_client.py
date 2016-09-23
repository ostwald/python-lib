"""
DDSClient - based on simple search client

makes requests on dds web service and returns responses
as XmlRecords.

Parses responses and  - HOW WILL RESPOND TO ERRORS?

NOTE: we should be able to use ServiceResponse if we need to

----
http://nldr.library.ucar.edu/schemedit/services/ddsws1-1?q=%28xkcd+OR+xkcd%29+OR+%28%28title:%28xkcd%29^15+OR+title%28xkcd%29^10+OR+titlestems:%28xkcd%29^5%29+OR+titlestems:%28xkcd%29^3%29&verb=Search&s=0&n=10

"""
from JloXml import XmlRecord, XmlUtils
from serviceclient import SimpleClient, SimpleClientError, ServiceResponse

class DDSClient (SimpleClient):
	
	
	"""
	Implements DDS error checking on responses 
	
	"""
	def getResponseDoc (self, params=None, opts=None):
		"""
		returns response as XmlRecord
		"""
		# print 'params: %s' % params
		# return XmlRecord(xml=self.getData(params, opts))
		responseDoc = None
		try:
			# responseText = data.read()
			# responseText = unicode (data.read(), 'iso-8859-1') # universal?
			# responseText = unicode (data.read(), 'utf-8') # experimental 12/2/2010
			
			data = self.getData(params, opts)
			# print data
			responseDoc = XmlRecord (xml=data)
			
			webResponseErrorNode = responseDoc.selectSingleNode (responseDoc.dom, 'DDSWebService:error')
			if webResponseErrorNode:
				errorCode = webResponseErrorNode.getAttribute('code');
				if errorCode == 'noRecordsMatch':
					return None
				print 'errorCode', errorCode
				raise SimpleClientError, XmlUtils.getText(webResponseErrorNode)
		except Exception, msg:
			## self.error = ServiceError (sys.exc_info())
			# self.error = ServiceError (["ServiceResponse: Could not parse XML", sys.exc_info()[1]])
			raise SimpleClientError, "DDSClient: Could not parse XML: %s" % msg
			
		return responseDoc

if __name__ == '__main__':
	baseUrl = 'http://ncs.nsdl.org/mgr/services/ddsws1-1?verb=Search&s=0&n=50&ky=X1290084883129&q=algebra'
	# baseUrl = 'http://ncs.nsdl.org'
	client = DDSClient(baseUrl)
	print client.getResponseDoc()
