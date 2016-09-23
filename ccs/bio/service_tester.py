import time, demjson, urllib
from serviceclient import SimpleClient, SimpleClientError

# baseUrl = 'http://nldr.library.ucar.edu/metadata/osm/1.1/schemas/vocabs/instName.xsd'
baseUrl = 'https://script.google.com/macros/s/AKfycbzhwHruL45lO_1sJoXd6XIbnoxWysWFybw8OTd3bEJpXv9ipsKf/exec'


def getSurveyDataTest ():
	params = {
		'section' : 'Section 1',
		'teacher' : 'dls',
		'command' : 'data',
		'data_type' : 'data',
		'data_version' : '1',
		'force' : 'false'
		}
	timedRequest(params)

def addRowTester():
	params = {
      'section' : 'Section 1',
      'teacher' : 'dls',
      'command' : 'addRow',
      'data_type' : 'data'
    }
	
	row_data = ['007', '12', 'preys upon', '26']
	# print 'row_data is a %s' % type(row_data)
	encoded = demjson.encode(row_data)
	timedRequest(params, encoded)

def timedRequest (params, opts=None):
    
	clicks = time.time()
	client = SimpleClient(baseUrl)
	resp = client.getData(params, opts)
	print '%d bytes transfered' % len(resp)
	print 'responseCode: ', client.responseCode
	if len(resp) > 300:
		print resp[:300] + ' ....' 
	else:
		print resp
	print 'time elapsed: %f seconds' % (time.time() - clicks)
	
if __name__ == '__main__':
	for i in range(0,5):
		tics = time.time()
		print i
		getSurveyDataTest()
		addRowTester()
		print '\nTOTAL - %s' % (time.time() - tics)
		print '-----------'
	if 0:
		row_data = {'payload' : ['007', '12', 'preys upon', '26']}
		# data = urllib.urlencode(row_data)
		data = urllib.urlencode(row_data)
		print data
