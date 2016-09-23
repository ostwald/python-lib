"""
Splicer -

this module will append the start file with the end file, after confirming that
the start file preceeds the end log file

"""
import os, sys, re, time, shutil
from log_file import LogFile, LogFileEntry

dowrites = 1

def getReportTime (entry):
	timestampFmt = '%d/%b/%Y %H:%M:%S'
	# return time.strftime(LogFileEntry.timestampFmt, entry.timestamp)
	return time.strftime(timestampFmt, entry.timestamp)

class Splicer:

	def __init__ (self, start, end):
		self.strict = True
		self.baseLog = start
		self.recentLog = end
		
		if not os.path.exists(self.baseLog):
			raise Exception, 'Splice file does not exist at %s' % self.baseLog
		
		if not os.path.exists(self.recentLog):
			raise Exception, 'Active_log does not exist at %s' % self.recentLog
		
		self.lastBaseLogEntry = None
		self.firstRecentLogEntry = None
		
	def getLastBaseLogEntry (self):
		"""
		returns the time of the last entry in the Feburary spit in seconds
		"""
		if self.lastBaseLogEntry is None:
			s = open (self.baseLog, 'r').read().strip()
			lines = s.split('\n')
			print "%d lines in %s" % (len (lines), self.baseLog)
			# print lines[-1]
			log_entry = LogFileEntry(lines[-1])
			# self.lastBaseLogEntry = log_entry.getSecs()
			self.lastBaseLogEntry = log_entry
		return self.lastBaseLogEntry
	
	def filterRecentLog (self):
		"""
		collect entries from the XXX log file that 
		are AFTER the last entry in the XXX file
		"""
		entries = []
			
		report_interval = 100000
		threshold = self.getLastBaseLogEntry()
		print 'filtering on %s ...' % getReportTime(threshold)

		for i,line in enumerate(open(self.recentLog,'r')):
			if not line.strip():
				continue
			try:
				entry = LogFileEntry(line.strip())
			except Exception, e:
				msg = 'COULD NOT PARSE: %s\nCAUSE: %s' % (line, e)
				if self.strict:
					raise Exception, msg
				else:
					print msg
					continue
			# print '- entry date: ', entry.date
			if entry.isAfter(threshold):
				entries.append(entry)
			
		return entries
	
	
	def getFirstRecentLogEntry (self):
		"""
		collect entries from the XXX log file that 
		are AFTER the last entry in the XXX file
		"""
		if self.firstRecentLogEntry is None:
			entry = None
			report_interval = 100000
			threshold = self.getLastBaseLogEntry()
			
			for i,line in enumerate(open(self.recentLog,'r')):
				if not line.strip():
					continue
				try:
					entry = LogFileEntry(line.strip())
					break
				except Exception, e:
					msg = 'COULD NOT PARSE: %s\nCAUSE: %s' % (line, e)
					if self.strict:
						raise Exception, msg
					else:
						print msg
						continue

			# self.firstRecentLogEntry = entry.getSecs()
			self.firstRecentLogEntry = entry
			
		return self.firstRecentLogEntry
	
	def report (self):
		"""
		sanity check - report the following:
		- the LAST entry of the BASE
		- the FIRST entry of the RECENT file
		"""
		
		lastBaseLogEntry = self.getLastBaseLogEntry()
		print '(%s) lastBaseLogEntry: %s ' % (getReportTime(lastBaseLogEntry), self.baseLog)
		firstRecentEntry = self.getFirstRecentLogEntry()
		print '(%s) firstRecentEntry: %s ' % (getReportTime(firstRecentEntry), self.recentLog)

	
	def makeSplicedFile (self):
		"""
		combine the active log file with the SPLICE file
		not sure about timing, etc, since of course the active file is getting writes all the time.
		approach:
			1 - get this method debugged
			2 - stop httpd
			3 - backup active logs
			4 - run script for all active logs
			5 - start httpd
		"""

				
		
		dest = 'TEST-SPLICE_log'
		# dest = self.recentLog
		
		shutil.copyfile (self.recentLog, dest+"_BAK")
		
		baseLog_content = open(self.baseLog).read()
		recentLog_content = '\n'.join(map (lambda x:x.data, self.filterRecentLog()))
		
		if dowrites:
			fp = open(dest, 'w')
			fp.write (baseLog_content)
			fp.write (recentLog_content)
			fp.close()
			print 'wrote spliced log to ', dest
		else:
			print 'WOULD HAVE written to', dest
			
if __name__ == '__main__':
	splicedir = '/Users/ostwald/devel/NSDL/logs/splice'
	base = os.path.join (splicedir, 'search_queries.log-20131101')
	recent = os.path.join (splicedir, 'search_queries.tail-100000')
	
	splicer = Splicer (base, recent)
	splicer.report()
	if 0:
		recents = splicer.filterRecentLog()
		print '%d filtered recents' % len(recents)
		print 'first filtered: ' + getReportTime(recents[0])
	splicer.makeSplicedFile()
		
