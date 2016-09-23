"""
Using urllib2 package

Create and send a mock GoogleCalendar API Push Notification to a ccs instance
- https://developers.google.com/google-apps/calendar/v3/push

- handled by NotificationAction in cc
"""
import sys, time
from datetime import datetime
import urllib2

users = {
	'jlo' : ('jonathan.ostwald@gmail.com','1247065132457'),
	'edtrex' : ('edtrexhub@gmail.com', '1376938899816')
	}

def getExpirationStr (time_to_live_minutes):
	timestamp = time.time() + (6 * 3600) + (time_to_live_minutes * 60)
	return time.asctime(time.localtime(timestamp))
		
class Channel:

	url = 'http://localhost:8080/home/notification.do'
	user_agent = 'CCS/Google (testing agent)'
	attrs = [
			'channelID', 'resourceID', 'calendarID', 'userID', 'ttl'
			]
	
	def __init__ (self, args, sync=True):

		for attr in self.attrs:
			if args.has_key(attr):
				setattr (self, attr, args[attr])
			else:
				raise KeyError, "required attribute not defined: '%s'" % attr

		self.expiration = time.time() + (6 * 3600) + (self.ttl* 60)
		# self.expirationStr = time.asctime(time.localtime(self.expiration))
		self.expirationStr = time.ctime(self.expiration)
		self.messageNum = -1
		self.resourceURI = 'https://www.googleapis.com/calendar/v3/calendars/%s/events?alt=json' % self.calendarID

		if sync:
			self.send ('sync')
		
	def send (self, state="exists", messageNum=None):
		"""
		if no messageNum is provided, this is a sync request
		"""
		
		if state == 'exists':
			if messageNum is None:
				self.messageNum = self.messageNum + 1
			else:
				self.messageNum = messageNum
		else:
			self.messageNum = 1
		# self.saveMessageNum(self.messageNum)

		print "send: state: %s, messageNum: %s" % (state, messageNum)

		headers = {
			'User-Agent' : self.user_agent,
			'X-Goog-Message-Number' : self.messageNum,
			'X-Goog-Resource-ID' : self.resourceID,
			'X-Goog-Resource-URI' : self.resourceURI,
			'X-Goog-Channel-ID' : self.channelID,
			'X-Goog-Resource-State' : state,
			'X-Goog-Channel-Token' : 'userId=%s' % self.userID,
			'X-Goog-Channel-Expiration' : self.expirationStr
			}
			
		request = urllib2.Request(self.url, None, headers)
		response = urllib2.urlopen (request)
	
		# look at the response
		# print dir(response)
		print ' - responseCode:',response.code
		return response

		
	def __repr__ (self):
		lines = [];add=lines.append
		attrs = ['channelID','calendarID', 'userID', 'messageNum', 'expirationStr'] 
		for attr in attrs:
			add ('%s: %s' % (attr, getattr (self, attr)))

		return '\n'.join(lines)
		
class Notifier:

	defaults = {
	
		# url = 'http://ccs-test.dls.ucar.edu/home/notification.do'
		'url' : 'http://localhost:8080/home/notification.do',
		#user_agent : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
		'user_agent' : 'CCS/Google (testing agent)',
		
		# time to live for expiration in minutes
		'ttl' : 1
	}
	
	def __init__ (self, url=None):
		self.url = url or self.defaults['url']
	
	def getExpiration (self, ttl=None):
		if ttl is None:
			ttl = self.defaults['ttl']
		# timestamp includes tz offset and ttl
		timestamp = time.time() + (6 * 3600) + (ttl * 60)
		return time.asctime(time.localtime(timestamp))
		
	def getUserID (self, user):
		return users[user][1]
	
	def send (self, user, calendarID, messageNum=None, ttl=None):
		"""
		if no messageNum is provided, this is a sync request
		"""
		if calendarID is None:
			calendarID = users[user][0]
		if messageNum is None:
			state = "sync"
			messageNum = 1
		else:
			state = "exists"
		headers = {
			'User-Agent' : self.defaults['user_agent'],
			'X-Goog-Message-Number' : messageNum,
			'X-Goog-Resource-ID' : 'resourceID-%s' % users[user][0],
			'X-Goog-Resource-URI' : 'https://www.googleapis.com/calendar/v3/calendars/%s/events?alt=json' % calendarID,
			'X-Goog-Channel-ID' : 'channelID-%s-2' % user,
			'X-Goog-Resource-State' : state,
			'X-Goog-Channel-Token' : 'userId=%s' % self.getUserID(user),
			'X-Goog-Channel-Expiration' : self.getExpiration(ttl)
			}
			
		request = urllib2.Request(self.defaults['url'], None, headers)
		response = urllib2.urlopen (request)
	
		# look at the response
		# print dir(response)
		print ' - responseCode:',response.code
		return response

def oldInvocation():

	# send (user, num) 
	notifier = Notifier()

	calendar = users['edtrex'][0]

	if 1:
		notifier.send ('jlo', calendar, None)
	else:
		notifier.send ('edtrex', calendar, 4)
		
if __name__ == '__main__':
	Channel ({'foo':"farb"})

