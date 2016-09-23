"""
dicer -

three sources:
1 - february split: ~/logs/splits/<log_file>/<log_file>-20120301.unresolved
tail indicates date that split file was constructed

2 - unsplit log file: /dls/www/logs/unsplit/<log_file>
we are interested in just those entries that are AFTER last entry in february split

3 - active log file: /dls/www/logs/<log_file>
the FIRST entry here should be directly (~5 second gap) after that LAST entry of unsplit

task:
1 - append feburary split with remainder from unsplit
2 - PREPEND result of #1 to the active logfile

"""
import os, sys, re, time, shutil
from log_file import LogFile, LogFileEntry

class Dicer:

	def __init__ (self, log):
		self.log = log
		
		self.feb_split = '/home/ostwald/logs/splits/%s/%s-20120301.unresolved' % (self.log, self.log)
		if not os.path.exists(self.feb_split):
			raise Exception, 'Feb split does not exist at %s' % self.feb_split
		
		self.unsplit = '/dls/www/logs/unsplit/%s' % (self.log)
		if not os.path.exists(self.unsplit):
			raise Exception, 'UNsplit does not exist at %s' % self.unsplit
		
		self.active_log = '/dls/www/logs/%s' % self.log
		if not os.path.exists(self.active_log):
			raise Exception, 'Active_log does not exist at %s' % self.active_log
		
		self.lastFebSplitEntry = None
		self.unsplitEntriesAfterFeb = None
		
	def getLastFebSplitEntry (self):
		"""
		returns the time of the last entry in the Feburary spit in seconds
		"""
		if self.lastFebSplitEntry is None:
			s = open (self.feb_split, 'r').read().strip()
			lines = s.split('\n')
			print "%d lines in %s" % (len (lines), self.feb_split)
			# print lines[-1]
			log_entry = LogFileEntry(lines[-1])
			self.lastFebSplitEntry = log_entry.getSecs()
		return self.lastFebSplitEntry
	
	
	def getUnsplitEntriesAfterFeb (self):
		"""
		collect entries from the unsplit log file that 
		are AFTER the last entry in the FEB split
		"""
		if self.unsplitEntriesAfterFeb is None:
			entries = []
			report_interval = 100000
			threshold = self.getLastFebSplitEntry()
			
			for i,line in enumerate(open(self.unsplit,'r')):
				if not line.strip():
					break
				try:
					entry = LogFileEntry(line.strip())
				except Exception, e:
					msg = 'COULD NOT PARSE: %s\nCAUSE: %s' % (line, e)
					if self.strict:
						raise Exception, msg
					else:
						print msg
						continue
			
				if entry.getSecs() > threshold:
					entries.append (entry)
			
				if i and i % report_interval == 0:
					print i
		
			self.unsplitEntriesAfterFeb = entries
		return self.unsplitEntriesAfterFeb
	
	def reportActiveLog (self):
		"""
		print info about active log, such as first and last entries
		"""
		lines = open(self.unsplit,'r').read().strip().split('\n')
		first = LogFileEntry(lines[0])
		last = LogFileEntry(lines[-1])
		print 'activeFile for ', self.log
		print '%d entries' % len(lines)
		print 'first: %s (%s)' % (time.ctime(first.getSecs()), first.getSecs())
		print 'last: %s (%s)' % (time.ctime(last.getSecs()), last.getSecs())
		
	def report (self):
		"""
		sanity check - report the following:
		- the LAST entry of the FEB split
		- the UNSPLIT entries that are more RECENT than the feb split
		"""
		
		print '\n** %s **' % self.log
		
		lastFebEntry = self.getLastFebSplitEntry()
		print 'lastFebEntry: %s (%s)' % (time.ctime(lastFebEntry), lastFebEntry)
		entries = self.getUnsplitEntriesAfterFeb()
		
		if entries:
			# print entries[0].data
			# print entries[0].timestamp
			print '%d entries from unsplit to add to split' % len(entries)
			print 'first: %s (%s)' % (time.ctime(entries[0].getSecs()), entries[0].getSecs())
			print 'last: %s (%s)' % (time.ctime(entries[-1].getSecs()), entries[-1].getSecs())
		
		else:
			print 'no entries in unsplit are newer than last entry in feb split'
	
	def makeSpliceFile (self):
		"""
		1 - make a copy of the feb split file - 
			'/home/ostwald/logs/splits/%s/%s-SPLICE' % (self.log,self.log)
		2 - append entries from unsplit that are LATER than latest entry of SPLICE
		"""
		dice = '/home/ostwald/logs/splits/%s/%s-SPLICE' % (self.log, self.log)
		shutil.copyfile (self.feb_split, dice)
		entries = None
		try:
			entries = self.getUnsplitEntriesAfterFeb()
		except Exception, _e:
			print "Error getting entries from unsplit: %s" % _e
			return
			
		fp = open(dice, 'a')
		fp.write ('\n'.join (map (lambda x:x.data, entries)))
		fp.close()
		print 'added %d entries to %s' % (len(entries), dice)
			
if __name__ == '__main__':
	log_files = os.listdir ('/home/ostwald/logs/splits')
	
	if 1:
		for log_file in log_files:
			try:
				dicer = Dicer(log_file)
				dicer.report()
				dicer.makeSpliceFile()
			except Exception, _e:
				print 'Error: %s' % _e
	
	elif 1:
		log_file = log_files[0]
		dicer = Dicer(log_file)
		dicer.report()
		dicer.makeSpliceFile()
	
	else:
		dicer = Dicer ('nsdl.org_access_log')
		dicer.reportActiveLog()
