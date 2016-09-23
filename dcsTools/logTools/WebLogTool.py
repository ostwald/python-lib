"""

tool for analysing web log files using NCSA format

e.g.,  
C:/Documents and Settings/ostwald/My Documents/DCS/Log Analysis/Web Logs/dcs.dlese.org.2005.08.log

"""
import os
import string
from UserDict import UserDict
from urlparse import urlparse
import cgi


class NCSALogEntry (UserDict):
	def __init__ (self, linetext):
		dict = self.make_dict (linetext)
		self.linetext = linetext
		UserDict.__init__ (self, dict)

	def make_dict (self, line):
		dict = {}
		try:
			fields = line.split (" ")
			dict["remote_host_addr"] = fields[0]
			dict["user_name"] = fields[2]
			dict["date_stamp"] = string.join (fields[3:5], ' ')
			dict["request"] = string.join (fields[5:7], ' ')
			dict["protocol_version"] = fields[7]
			dict["status_code"] = fields[8]
			dict["bytes_sent"] = fields[9]
		except:
			##print "couldn't parse line:\n\t" + line
			pass
		return dict

	def getUrl (self):
		try:
			urlStr = self["request"].split(' ')[1]
			return urlparse (urlStr)
		except:
			return None

	def getPath (self):
		url = self.getUrl()
		if url and len(url) > 2:
			return self.getUrl()[2]

	def isServiceCall (self):
		if self.getPathSeg(2) == "services":
			return 1
		else:
			return 0

	def getPathSeg (self, index):
		path = self.getPath()
		if path:
			splits = path.split("/")
			if len(splits) > index:
				return splits [index]

	def getInstance (self):
		return self.getPathSeg (1)

	def getParams (self):
		qs = self.getUrl()[4]
		if qs:
			return cgi.parse_qsl(qs)

	def pp (self):
		s=[];add=s.append
		for key in self.keys():
			add ("%s: %s" % (key, self[key]))
		return string.join (s, "\n")

def instance_count (entryList):
	"""
	print tally the number of log entries for each instance
	"""
	instanceDict = {}
	for entry in entryList[:]:
		instance = entry.getInstance()
		if instanceDict.has_key(instance):
			instanceDict[instance] += 1;
		else:
			instanceDict[instance] = 1;

	for key in instanceDict.keys():
		print "%s: %d" % (key, instanceDict[key])

def filter_entries_by_instance (entryList, instance=None):
	instanceList = []
	filtered = []
	if type(instance) == type("foo"):
		instanceList = [instance,]
	if type(instance) == type ([]):
		instanceList = instance
	filtered = []
	for entry in entryList:
		if entry.getInstance() in instanceList:
			filtered.append (entry)
	return filtered

def news_nonservice_lines (entryList):
	lines = []
	for entry in entryList:
		if entry.getInstance() != "news":
			continue
		if not entry.isServiceCall():
			lines.append (entry.linetext)
	print "** %d non-service entries found for NEWS instance ***" % len (lines)
	print "\n" + string.join (lines, "\n")

def showRobots (entryList):
	robots = filter_entries_by_instance (entryList, "robots.txt")
	print " ** showRobots : %d entries **" % len(robots)
	for bot in robots:
		print bot.linetext

if __name__ == "__main__":
	logFile = "C:/Documents and Settings/ostwald/My Documents/DCS/Log Analysis/Web Logs/dcs.dlese.org.2005.08.log"
	s = open (logFile, 'r').read()
	lines = s.split ("\n")
	print "%d lines read" % len (lines)
	entryList = []
	for line in lines[:]:
		entryList.append (NCSALogEntry (line))
	## instance_count (entryList)
	## news_nonservice_lines (entryList)
	showRobots (entryList)




	
## 	fields = entry.split(" ")
## 	print "%d fields read" % len (fields)
## 	for field in fields:
## 	print "\t", field
