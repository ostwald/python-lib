"""
split a log file up into individual files by MONTH.

file is named for the first day of the month following the month of the entries (simulating
how the logrotate files are named)

per-month files are written to directory specified by "spltsDir"
"""
import os, sys, re, time
from log_file import LogFileEntry


class MonthSplitter:
	"""
	parses a log file into a list of entries

	splits the log file into entries for each month, and then writes
	the entries for each month into a log file in "splitsDir"
	"""

	dowrites = 1
	strict = 0
	report_interval = 10000
	verbose = 0
	
	def __init__ (self, path, destDir):
		self.path = path
		self.baseFilename = os.path.basename(path)
		if not os.path.exists(self.path):
			raise IOError, 'Log file does not exist at %s' % self.path

		self.destDir = destDir
		if not os.path.exists(self.destDir):
			os.mkdir(self.destDir)

		start = time.time()
		self.split()
		self.elapsed = time.time() - start
		print "split finished - elapsed time: %d millis" % (self.elapsed * 1000)
		

	def split (self):
		"""
		process the lines/entries of the log file, writing the entries for each
		day into its own file
		"""
		current_month = None
		entries = []
		self.entry_count = 0

		for i,line in enumerate(open(self.path,'r')):
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
			mydate = entry.month
			# print '%d/%d/%d' % (entry.month, entry.timestamp[2], entry.timestamp[0])
			if mydate == current_month:
				entries.append(entry)
			else:
				if self.dowrites:
					self.writeEntries(entries)
				else:
					print 'would have written %d entries with date = %s' % (len(entries), current_date)
				current_month = mydate
				entries = []

			if i and i % self.report_interval == 0:
				print i

		if entries:
			if self.dowrites:
				self.writeEntries(entries)
			else:
				print 'would have written %d entries with date = %s' % (len(entries), current_date)

	def getDateTag (self, timestamp):
		"""
		time stamp is a tuple.
		dateTag is of the form YYYYMMDD, but it is for the first day of the month
		FOLLOWING the month of timestamp
		e.g., if timestamp is for 10/26/2011, the dateTag will look like: 20111101
		"""
		year = timestamp.tm_year
		month = timestamp.tm_mon + 1
		if month > 12:
			month = 1
			year += 1
		return '%d%02d01' % (year, month)
		

	def writeEntries (self, entries):	
		if not entries:
			return
		self.entry_count = self.entry_count + len(entries)
		
		timestamp = entries[0].timestamp
		# filename = '%s-%d%02d01' % (self.baseFilename, timestamp[0], timestamp[1]+1)
		filename = '%s-%s' % (self.baseFilename,self.getDateTag(timestamp))
		outpath = os.path.join (self.destDir, filename)
		if self.dowrites:
			fp = open(outpath, 'w')
			fp.write ('\n'.join(map(lambda x:x.data, entries)))
			fp.close()
			if self.verbose:
				print 'wrote to', outpath
		else:
			print 'WOULD HAVE written to %s' % outpath

def splitLog (src, dest):
	MonthSplitter (src, dest)
			
if __name__ == '__main__':
	
	# nsdl.org_access_log_10_25_1022'  # rs1
	# nsdl.org_access_log_frag'  # acorn
	filename = 'search_queries-2013-05-23.log'
	if len(sys.argv) > 1:
		filename = sys.argv[1]
		print 'filename', filename

	log_file_dir = '/Users/ostwald/devel/logs'
	splits_dir = '/Users/ostwald/devel/logs/splits_output'
		
	dest = os.path.join (splits_dir, filename)
	src = os.path.join(log_file_dir, filename)
	log = MonthSplitter (src, dest)
	print "entries processeed %d" % log.entry_count

