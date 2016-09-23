import time, demjson, urllib
from serviceclient import SimpleClient, SimpleClientError

# baseUrl = 'http://nldr.library.ucar.edu/metadata/osm/1.1/schemas/vocabs/instName.xsd'
baseUrl = 'https://script.google.com/macros/s/AKfycbzepoQF3eUKk2SwMGd6p3ubFehtxmiYgoNeZi0bsvr5W-QQE-g/exec' # ecosurvey workspace

def batchTester():
	params = {
	  'section' : 'section tester',
	  'teacher' : 'jlo',
	  'command' : 'batch'
	}
	
	post_data = [
		{ 
			'parameter' : {
				'command' : 'addRow',
				'data_type' : 'data'
			},
			'postData' : demjson.encode(['myid', '444', 'my type'])
		}
	]
	
	encoded = demjson.encode(post_data)
	return timedRequest(params, encoded)

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
	return resp
	
if __name__ == '__main__':
	resp = batchTester()
	print 'resp is a %s' % type(resp)
	response_json = demjson.decode(resp)
	print 'response_json is a %s' % type(response_json)
	for item_resp in response_json:
		print "- %s" % item_resp

