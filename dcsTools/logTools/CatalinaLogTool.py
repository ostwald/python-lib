"""
 tool for analyzing catalina.out log files
 e.g., "C:/Documents and Settings/ostwald/My Documents/DCS/Log Analysis/Catalina Logs/dcc-log.txt"

 parses the log file and returns a list of Request objects

"""

import string
import sys
import os
import re
import time
from Request import Request
from utils import logTimeToSecs, secsToLogTime

def log (s): sys.stdout.write ("CatalinaLogTool: " + s + "\n")

hr = "-"*50

class CatalinaLogTool:

	def __init__ (self, path=None, filters=[]):
		self.path = path
		self.master_filter = ""
		self.requests = []
		self.results = []
		if type (filters) == type ("blah"):
			filters = [filters]
		else:
			self.filters = filters
		self.update_master_filter ()
		if self.path:
			self.read ()
			self.applyFilters()

	def __len__ (self):
		return len(self.requests)

	def changePath (self, path):
		self.path = path
		self.read()
		self.applyFilters()
		log ("changed path to %s" % self.path)

	def update_master_filter (self):
		exprs = []
		for f in self.filters:
			exprs.append (f.expr)
		self.master_filter = string.join (exprs, " and ")

	def addFilter (self, filter):
		if filter:
			self.filters.append (filter)
			self.update_master_filter()

	def _accept (self, request):
		if not self.filters:
			# print "\t\t-- %s" % "no filters returning true"
			return True
		else:
			try:
				ret = eval (self.master_filter)
				# print "\t\t-- eval returning %s" % ret
				return ret
			except:
				print sys.exc_info()[0], sys.exc_info()[1]
				print "\n%s\nmaster filter:\n%s" % (hr, self.master_filter)
				print "\nrequest\n%s" % request
				raise "_accept error - aborting\n%s" % hr

	def applyFilters (self, filterList=[]):
		log ("applyFilters")
		if filterList:
			log ("%d filters provided" % len (filterList))
			self.filters = []
			self.results = []
			for filter in filterList:
				print " -- %s" % filter
				self.addFilter (filter)
		log ("master filter: %s" % self.master_filter)
		results = []
		if not self.requests:
			self.read()
		if not self.requests:
			log ("could not find any requests ... bailing")
			self.results = results

		for request in self.requests:
			try:
				if self._accept (request):
					results.append (request)
			except:
				print sys.exc_info()[1]
				print request
				return
		log ("returning from query (%d) results" % len (results))
		self.results = results

	def read (self):
		"""
		split the log file into "blobs" which are defined as chunks of text
		separated by a blank line.

		if the blob contains output from the RequestProcessor, create a Request object

		append Requests only if they pass filters (if defined)
		"""
		s = open (self.path, 'r').read()
		print "reading from %s" % self.path
		blobs = s.split ("\n\n")
		print "processing %d blobs" % len (blobs)

		## requestHeaderPattern = "DCS RequestProcessor: PROCESS"
		
		requestHeaderPattern = "org.apache.struts.action.RequestProcessor process"
		requests = []
		for blob in blobs:
			line1 = blob.split("\n")[0]
			if string.find (line1, requestHeaderPattern) != -1:
				try:
					request = Request (blob)
					requests.append (request)
				except:
					print "failed to contstruct Request:", sys.exc_type, sys.exc_value
					continue
				
			else:
				## print "%s not found" % requestHeaderPattern
				## print "\tfirst line: \n%s" % line1
				pass
		self.requests = requests

	def filters_toString (self):
		s=[];add=s.append
		if self.filters:
			add ("Filters:")
			for f in self.filters: add(str(f))
		else:
			add ("No Filters defined")
		return string.join (s, "\n\t")

	def formatResults (self, display_fn=None):
		"""
		display a list of requests using display_fn if provided, or
		some default function otherwise.

		display_fn can be any function that takes a Request instance as a parameter
		"""
		s=[];add=s.append
		
		if not self.results:
			return ""
		
		for i in range (len (self.results)):
			result = self.results[i]
			if display_fn:
				display = display_fn (result)
			else:
				display = str (result)
			add ("\n-- %d / %d --\n%s" % ( i, len (self), display))
		return string.join (s, '\n')

	def report (self, display_fn=None):
		return self.__repr__(display_fn)
	
	def __repr__ (self, display_fn=None):
		s=[];add=s.append
		## add (self.filters_toString())

		add ("\n%d/%d Results Found" % (len(self.results) , len (self)))

		add (self.formatResults (display_fn))

		return string.join (s, '\n')

class Filter:
	def __init__ (self, attr, val=None):
		self.attr = attr
		self.val = val
		self.expr = self._get_expr ()

	def _get_expr (self):
		if self.val:
			return "request.%s == '%s'" % (self.attr, self.val)
		else:
			return "request.%s" % (self.attr)

	def __repr__ (self):
		if self.val:
			return "%s == %s" % (self.attr, self.val)
		else:
			return self.attr

class DateFilter (Filter):
	"""
		accepts dates in the form of logTime (e.g., "Aug 12, 2005 12:00:01 AM"),
		which is the format used in the catalina log files, and converts to seconds
		send epoch, and then produces a string that can be evaluated against a
		request object
	"""
	def __init__ (self, date1, date2=None):
		self.date1 = date1
		self.date2 = date2
		self.expr = self._get_expr()

	def _get_expr(self):
		secs1 = logTimeToSecs (self.date1)
		if self.date2 is not None:
			secs2 = logTimeToSecs (self.date2)
		else:
			secs2 = time.time()

		if secs2 < secs1:
			raise "DateFilterError", "date2 comes before date1"

		return "request.time_stamp >= %s and request.time_stamp <= %s" % (secs1, secs2)

	def __repr__ (self):
		return "TimeStamp between %s and %s" % \
			   (self.date1, self.date2)

def sampleDisplayRequest(request):
	if not request.isStatusEvent():
		return ""
	return request.work_flow_info['id']

if __name__ == "__main__":

	path = "catalina.out.sample"
	logTool = CatalinaLogTool (path)


	t1 = "Feb 2, 2006 9:42:32 AM"
	t2 = "Feb 10, 2006 9:42:32 AM"

 	logTool.addFilter (DateFilter (t1,t2))
	logTool.addFilter (Filter ("isStatusEvent()"))
	logTool.addFilter (Filter ("sessionId", "A09C651853EA6B440BA893F3CC68D1EB"))
	logTool.applyFilters()
	## print logTool.__repr__(sampleDisplayRequest)

	print logTool.__repr__()


	
