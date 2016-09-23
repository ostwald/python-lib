from time import strptime, strftime, gmtime, localtime, asctime, time, mktime
from HyperText.HTML40 import *

timestamp_fmt = "%b %d, %Y %I:%M:%S %p"

header_font = ("arial", 11, "bold")
normal_font = ("helvetica", 10, "normal")

hour_secs = 60 * 60 * 1000
day_secs = hour_secs * 24
week_secs = day_secs * 7

def logTimeToSecs (logTime):
	"""
	logTime is a string of the format: "%b %d, %Y %I:%M:%S %p"
	e.g., "Aug 15, 2005 1:19:06 PM"

	returns secs since the millineum
	"""

	time_tuple = strptime (logTime, timestamp_fmt)   # a tuple representing the timestr
	return mktime(time_tuple)

def secsToLogTime (secs):
	return strftime (timestamp_fmt, localtime(secs))
		
def convert_time (timestr):
	"""
	converts the time stamps found in the logs to other representations
	"""
	time_tuple = strptime (timestr, timestamp_fmt)   # a tuple representing the timestr
	secs = mktime(time_tuple)

	print "time_tuple", time_tuple
	print "secs", secs
	print "asci", asctime (time_tuple)

def yesterday ():
	t = TimeTool (time())
	t['tm_mday'] = 	t['tm_mday'] - 1
	print "yesterday: " + t.logTime()
	return t.timeStamp()

def yesterday2 ():
	secs = time() - (24 * 60 * 60)
	t = TimeTool (secs)

	print "yesterday2: " + t.logTime()
	return t.timeStamp()

def lastweek ():
	t = TimeTool (time())
	t['tm_mday'] = 	t['tm_mday'] - 7
	print "last week: " + t.logTime()
	return t.timeStamp ()

def nextweek ():
	t = TimeTool (time())
	t.inc ('tm_mday', 7)
	print "**next week: " + t.logTime()
	return t.timeStamp ()

def lastmonth ():
	t = TimeTool (time())
	t.inc('tm_mon', -2)
	print "last month: " + t.logTime()
	return t.timeStamp ()

class TimeTool:

	tm_year = 0
	tm_mon = 1
	tm_mday = 2
	tm_hour = 3
	tm_min = 4
	tm_sec = 5

	blank = [0,1,1,0,0,0,0,1,0]

	def __init__ (self, secs=None):
		self.data = self.blank
		if secs:
			lt = localtime (secs)
			for i in range (len(lt)):
				self.data[i] = lt[i]

	def inc (self, item, value):
		self[item] = self[item] + value

	def __getitem__ (self, item):
		i = getattr (self, item)
		return self.data[i]

	def __setitem__ (self, item, value):
		i = getattr (self, item)
		self.data[i] = value

	def _get_tuple (self):
		# refresh the 
		return localtime(mktime (self.data))

	def logTime (self):
		return strftime (timestamp_fmt, self._get_tuple())
		
	def timeStamp (self):
		return mktime (self._get_tuple())

	def __repr__ (self):
		return self.logTime()
		
if __name__ == "__main__":
	nextweek()
	yesterday()
	yesterday2()
	lastweek()
	lastmonth()
