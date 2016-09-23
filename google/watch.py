
"""
# SAMPLE CODE pattern
url = 'http://www.someserver.com/cgi-bin/register.cgi'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
values = {'name' : 'Michael Foord',
          'location' : 'Northampton',
          'language' : 'Python' }
headers = { 'User-Agent' : user_agent }

data = urllib.urlencode(values)
req = urllib2.Request(url, data, headers)
response = urllib2.urlopen(req)
the_page = response.read()
"""
import sys, demjson, time
import urllib
import urllib2

access_token = 'ya29.AHES6ZTvggTsWI2SqEJUNUmzun2jnU15rZPKPvEhsS2KdM7cmgol72c'

def getChannelId():
    return 'JLO_channel_id_%s' % str(int(time.time()))

def calendarList():

    baseUrl = 'https://www.googleapis.com/calendar/v3/users/me/calendarList'

    data = {}
    headers = {}
    url = baseUrl + "?" + urllib.urlencode({'access_token':access_token})

    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    content = response.read()
    # print content

    try:
        json = demjson.decode(content)
        print content
    except JSONDecodeError, e:
        print e

def watch (calendarId):


    url = 'https://www.googleapis.com/calendar/v3/calendars/%s/events/watch' % calendarId

    data = {
        'id':getChannelId(),
        'type' : 'web_hook',
        'address' : 'https://ccs-test.dls.ucar.edu/home/notification.do'
    }
    execute(url, data)

def stop(id, resourceId):
    data = {
        'id': id,
        'resourceId' : resourceId
        }
    url = 'https://www.googleapis.com/calendar/v3/channels/stop'
    execute(url, data)

def execute(baseUrl, postData):
    
    headers = {
#        'Authorization' : 'Bearer %s' % access_token,
#        'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
        'Content-type' : 'application/json'
        }

    data = demjson.encode(postData)

    url = baseUrl + "?" + urllib.urlencode({'access_token':access_token})
    req = urllib2.Request(url, data, headers)

#    print dir(req)

    print '\nREQUEST --------------'
    print 'method', req.get_method()
    print 'headers', headers
    print 'data', data
    print 'baseUrl', baseUrl

    #sys.exit()

    try:
        response = urllib2.urlopen(req)
    except urllib2.URLError, e:
        print e.code
        print e.read()
        sys.exit()
        
    content = response.read()
    print content

    try:
        json = demjson.decode(content)
        print content
    except JSONDecodeError, e:
        print e

if __name__ == '__main__':
		
	#calendarList()
	if 0:
		calendarId = 'jonathan.ostwald@gmail.com'
		watch(calendarId)
	if 1:
		channelId = None
		if len(sys.argv) > 0:
			channelId = sys.argv[1]
		else:
			print 'channelId arg required'
			sys.exit()
		
		# channelId = 'CCS-Channel-1381886911863'
		resourceId = 'Pzvf-9bKBeIdZuOgX-PUCR4w9rc'
		stop(channelId, resourceId)
	
	

