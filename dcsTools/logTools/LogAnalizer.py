"""
 tool for analyzing catalina.out log files
 e.g., "C:/Documents and Settings/ostwald/My Documents/DCS/Log Analysis/Catalina Logs/dcc-log.txt"

 parses the log file and returns a list of Request objects

"""

import string
import sys
import os
import re
from time import strptime, strftime, gmtime, localtime, asctime, time, mktime
from Request import Request, logTimeToSecs

pat = re.compile ("\n\n")

def getRequests (path, filters=None):
	"""
	split the log file into "blobs" which are defined as chunks of text separated by a blank line

	if the blob contains output from the RequestProcessor, create a Request object

	optionally, a sessionID can be passed to look for Requests from that session only
	"""
	if type (filters) == type ("blah"):
		filters = [filters]
		
	s = open (path, 'r').read()
	blobs = s.split ("\n\n")
	print "processing %d blobs" % len (blobs)
	requests = []
	for blob in blobs:
		line1 = blob.split("\n")[0]
		if string.find (line1, "org.apache.struts.action.RequestProcessor process") != -1:
			try:
				request = Request (blob)
			except:
				print "failed to contstruct Request:", sys.exc_type, sys.exc_value
				continue
			if filters:
				if (eval (string.join (filters, " and "))):
					requests.append (request)
## 				accept = True
## 				for filter in filters:
## 					if not (eval (filter)):
## 						accept = False
## 						break
## 				if accept:
## 					requests.append (request)
			else:
				requests.append (request)
	return requests

if __name__ == "__main__":

	t1 = "Aug 12, 2005 12:00:01 AM"
	t2 = "Aug 13, 2005 5:00:00 PM"
	t1secs = logTimeToSecs (t1)
	t2secs = logTimeToSecs (t2)
	filters = None
	path = "C:/Documents and Settings/ostwald/My Documents/DCS/Log Analysis/Catalina Logs/dcc-log.txt"
	sessionId = "1DE5755F9DE662AD2D1615E23801027B"
	filter1 = "request.sessionId == '%s'" % sessionId
	filter2 = "request.time_stamp > %s and request.time_stamp < %s" % (t1secs, t2secs)
	filter3 = "request.isStatusEvent()"
	filters = (filter3,filter2)
	requests = getRequests(path, filters)
	if filters:
		print "filters"
		for f in filters:
			print "\t" + f
	print "%d requests extracted" % len (requests)
	for i in range (min (len (requests), 10)):
		print "\n-- %d / %d --\n%s" % ( i, len (requests), requests[i].log_entry)
		## print "\n-- %d --%s" % ( i, requests[i].time_stamp)
	
