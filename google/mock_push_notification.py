"""
Using requests package

Create and send a mock GoogleCalendar API Push Notification to a ccs instance
- https://developers.google.com/google-apps/calendar/v3/push

- handled by NotificationAction in cc
"""

import requests

url = 'http://ccs-test.dls.ucar.edu/home/notification.do'
# url = 'http://localhost:8080/home/notification.do'


#user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
user_agent = 'Gonzo'
headers = { 
	'User-Agent' : user_agent,
	'X-Goog-Channel-Id' : '12345',
	'X-Goog-Message-Number' : '22',
	'X-Goog-Resource-ID' : 'ret08u3rv24htgh289g',
	'X-Goog-Resource-State' : 'exists',  # 'sync'
	'X-Goog-Resource-URI' : 'https://www.googleapis.com/calendar/v3/calendars/jonathan.ostwald@gmail.com/events'
	}

channels = {
	'jlo' : 'jonathan.ostwald@gmail.com',
	'edtrex' : 'edtrexhub@gmail.com'
	}

def send (messageNum = 0, resourceID=channels['jlo'] ):

	headers['X-Goog-Message-Number'] = messageNum
	headers['X-Goog-Resource-ID'] = resourceID

	
	form_fields = {}
#	data = urllib.urlencode(form_fields)

	#Get
	resp = requests.get (url, headers=headers)


	# look at the response
	print 'response:'
	print dir (resp)
	print ''


	print "- status_code (%s)" % resp.status_code
	# print dir(response)

	print '- content\n%s\n' % resp.content
	
if __name__ == '__main__':

	send (32, channels['jlo'])
	# send (35, channels['edtrex'])
