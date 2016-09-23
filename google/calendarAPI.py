"""
Test out sending google API requests

To determine: can we submit a successful "watch" request from ssh_acorn, with
the goal of receiving notifactions in ccs-test instance.

I haven't been able to submit a successful "watch" request using Oath Playground
(https://developers.google.com/oauthplayground/) event though I beleive I've set
up everthing properly in see
https://developers.google.com/google-apps/calendar/v3/push
"""
import requests
import json

calendarId = 'jonathan.ostwald@gmail.com'
eventId = 'dainmkmoc3cdv4md7qe8q94sg0'
access_token = 'ya29.AHES6ZTp0f8A5n4pWgB_BfQcaV9E1QxVipxgIN1Ohn2VH1ia';

requestUrl = 'https://www.googleapis.com/calendar/v3/calendars/%s/events' % calendarId


postBody = {
			"start": { 
				"dateTime": "2013-10-06T19:26:56.825Z"
			},
			"end": {
				"dateTime": "2013-10-08T19:26:56.825Z"
			},
			"description":"HELLO WOILD",
			"summary": "Kilroy was here"
		}

def getCalendarList ():
	url = 'https://www.googleapis.com/calendar/v3/users/me/calendarList'
	resp = requests.get(url, params={'access_token': access_token})
	print json.dumps(resp.json(), sort_keys=True,
		indent=2, separators=(',', ': '))
	
if __name__ == '__main__':
	# getCalendarList()
	

