"""
Splicer -

Dicer.py created a SPLICE field in the splits directory for each log_file

this module will append the splice file with the live log file, after confirming that
the SPLICE file preceeds the active log file

"""
import os, sys, re, time, shutil
from log_file import LogFile, LogFileEntry

dowrites = 1

class Splicer:

	def __init__ (self, log):
		self.log = log
		
		self.splice = '/home/ostwald/logs/splits/%s/%s-SPLICE' % (self.log, self.log)
		if not os.path.exists(self.splice):
			raise Exception, 'Splice file does not exist at %s' % self.splice
		
		self.active_log = '/dls/www/logs/%s' % self.log
		if not os.path.exists(self.active_log):
			raise Exception, 'Active_log does not exist at %s' % self.active_log
		
		self.lastSpliceEntry = None
		self.firstActiveLogEntry = None
		
	def getLastSpliceEntry (self):
		"""
		returns the time of the last entry in the Feburary spit in seconds
		"""
		if self.lastSpliceEntry is None:
			s = open (self.splice, 'r').read().strip()
			lines = s.split('\n')
			print "%d lines in %s" % (len (lines), self.splice)
			# print lines[-1]
			log_entry = LogFileEntry(lines[-1])
			self.lastSpliceEntry = log_entry.getSecs()
		return self.lastSpliceEntry
	
	
	def getFirstActiveLogEntry (self):
		"""
		collect entries from the unsplit log file that 
		are AFTER the last entry in the FEB split
		"""
		if self.firstActiveLogEntry is None:
			entries = []
			report_interval = 100000
			threshold = self.getLastSpliceEntry()
			
			for i,line in enumerate(open(self.active_log,'r')):
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

			self.firstActiveLogEntry = entry.getSecs()
			
		return self.firstActiveLogEntry
	
		
	def report (self):
		"""
		sanity check - report the following:
		- the LAST entry of the SPLICE
		- the FIRST entry of the active file
		"""
		
		print '\n** %s **' % self.log
		
		lastSpliceEntry = self.getLastSpliceEntry()
		# print 'lastSpliceEntry: %s (%s)' % (time.ctime(lastSpliceEntry), lastSpliceEntry)
		print '(%s) lastSpliceEntry: %s ' % (time.ctime(lastSpliceEntry), self.splice)
		firstActiveEntry = self.getFirstActiveLogEntry()
		print '(%s) firstActiveEntry: %s ' % (time.ctime(firstActiveEntry), self.active_log)
		# print 'firstActiveEntry: %s (%s)' % (time.ctime(firstActiveEntry), firstActiveEntry)

	
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
		dest = self.active_log
		
		shutil.copyfile (self.active_log, dest+"_BAK")
		
		splice_content = open(self.splice).read()
		active_log_content = open(self.active_log).read()
		
		if dowrites:
			fp = open(dest, 'w')
			fp.write (splice_content)
			fp.write (active_log_content)
			fp.close()
			print 'wrote spliced log to ', dest
		else:
			print 'WOULD HAVE written to', dest
			
if __name__ == '__main__':
	log_files = os.listdir ('/home/ostwald/logs/splits')
	active_logs = filter (lambda x:x.endswith('_access_log'), os.listdir('/dls/www/logs'))
	
	log_files = active_logs
	
	if 1:
		for log_file in log_files:
			try:
				splicer = Splicer(log_file)
				splicer.report()
				splicer.makeSplicedFile()
			except Exception, _e:
				print 'Error: %s' % _e
	
	elif 0:
		# log_file = 'beyondpenguins.nsdl.org_access_log'
		log_file = 'harvest.nsdl.org_access_log'
		splicer = Splicer(log_file)
		splicer.report()
		splicer.makeSplicedFile()
	
	else:
		splicer = Splicer ('nsdl.org_access_log')
		
