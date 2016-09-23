# from time import mktime, strptime, strftime, localtime, gmtime

import os, time

class TimeHelper:

	full_format = "%m/%d/%y %H:%M"
	short_format = "%m/%d/%y"
	hour_format = "%H:%M"
	
	## convert string into tuple
	def parseDateString (self, s):
		try:
			return time.strptime (s, self.full_format)
		except:
			pass
		try:
			return time.strptime (s, self.short_format)
		except:
			pass
	
		## build up a time by appending 
		now = time.localtime()
		## print "now: ", now
		tuple = []
		for d in now:
			tuple.append  (d)
		## print "tuple: ", tuple
		hours = time.strptime  (s, self.hour_format)
		## print "hours: ", hours
		tuple[3] = hours[3]
		tuple[4] = hours[4]
		tuple[5] = 0
		return tuple
		
	## convert string into secs
	def getTime (self, dateString):
		t = self.parseDateString (dateString)
		return int (time.mktime(t))
	
	def pp (self, secs):
		return time.asctime(time.localtime(secs))
		
	def _roundtrip (self, dateStr):
		secs = self.getTime (dateStr)
		print self.pp(secs)

if __name__ == "__main__":
	dateStr = "6/23/09"
	helper = TimeHelper()
	helper._roundtrip (dateStr)
