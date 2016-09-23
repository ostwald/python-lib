"""
split a log file up into a bunch of individual files by day.

per-day files written to directory specified by "baseDir"
"""
import os, sys, re, time
from UserList import UserList

baseDir = '/home/ostwald/logs/harvest_logs'

class LogFileEntry:
	"""
	exposes:
	- data
	- date - the date string from entry
	- timestamp - a date struct
	- host
	- month
	"""
	datePat = re.compile(".*?\[(.*?):")
	timestampPat = re.compile(".*?\[(.*?)\]")
	timestampFmt = '%d/%b/%Y:%H:%M:%S'

	def __init__ (self, data):
		self.data = data
		self.date = self.getDate()
		self.timestamp = self.getTimestamp()
		self.host = self.getHost()
		self.month = self.timestamp[1]

	def getTimestamp(self):
		"""
		returns TIME_STRUCT for this entry
		"""
		m = self.timestampPat.match(self.data)
		if m:
			dateStr = m.group(1).split(' ')[0]
			return time.strptime(dateStr, self.timestampFmt)
		else:
			raise Exception, 'parsable date not found in %s' % self.data

	def getDate (self):
	
		m = self.datePat.match(self.data)
		if m:
			return m.group(1)
		else:
			raise Exception, 'date not found in %s' % self.data

	def getHost (self):
		return self.data.split(' ')[0]

	def getSecs (self):
		return time.mktime(self.timestamp)
		
	def isBefore (self, other):
		return self.getSecs() < other.getSecs()
		
	def isAfter (self, other):
		return self.getSecs() > other.getSecs()

class LogFile(UserList):
	"""
	parses a log file into a list of entries

	splits the log file into entries for each day/date, and then writes
	the entries for each day into a log file in "baseDir"
	"""
	
	verbose = 1


	def __init__ (self, path):
		self.data = []
		self.filename = os.path.basename(path)
		self.baseFilename = os.path.basename(path)
		self.path = path
		self.read()

	def read (self):
		self.lines = filter (None, map (lambda x:x.strip(), open(self.path, 'r').read().split('\n')))
		self.data = map (LogFileEntry, self.lines)
	

	def getUniqueHosts(self):
		hosts = []
		if self.verbose:
			print 'getting uniqueHosts'
		for i,line in enumerate(self.data):
			if not line.host in hosts:
				hosts.append (line.host)
		hosts.sort()
		return hosts
		
	def reportUniqueHosts (self):
		for host in self.getUniqueHosts():
			print host
		   
if __name__ == '__main__':
	filename = 'harvest.nsdl.org_access_log'
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	print 'filename', filename

	if host == 'rs1':
		log_file_dir = '/home/ostwald/logs/log_files'
		## log_file_dir = '/home/ostwald/logs/ns_logs'
	elif host == 'acorn':
		log_file_dir = 'log_files'
	path = os.path.join (log_file_dir, filename)
	log = LogFile (path)
	print '%d lines read in %s' % (len(log), filename)


