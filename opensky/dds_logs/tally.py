import os, sys
from UserDict import UserDict
from opensky.dds_logs import DDSLogFile
import globals

class Tally(UserDict):

	def __init__ (self, path, field, ip):
		self.logFile = DDSLogFile(path)
		self.tally = self.doTally(field, ip)
		self.report ()
		
	def doTally (self, field, ip):
		tally = UserDict()
		
		filtered = self.logFile.filter (lambda x: x['IP'] == ip)
		print '%d filtered entries' % len (filtered)
		# for logLine in self.logFile:
		for logLine in filtered:
			# if logLine.has_key (field):
				# val = logLine[field]
			# else:
				# continue
			val = logLine[field]
			tally_cnt = tally.has_key(val) and tally[val] or 0
			tally[val] = tally_cnt + 1
			
		return tally

		
	def report (self):
		total = 0
		for key in self.tally.keys():
			print '%s (%d)' % (key, self.tally[key])
			total = total + self.tally[key]
		print "%d total" % total
			
class TallyMgr:
	
	def __init__ (self, path, field):
		for ip in globals.server_map:
			host = globals.server_map[ip]
			print '\n%s (%s)' % (host, ip)
			tally = Tally(path, field, ip)

			break
	
def tallyTester():
	pass
	
if __name__ == '__main__':
	host = os.getenv ("HOST") or os.getenv("COMPUTERNAME")
	platform = sys.platform
	
	# print "HOST: " + host
	if host == 'iis-executor.dls.ucar.edu':
		logdir ='/Users/ostwald/devel/opensky2/library-dds-weblogs/'
	else:
		logdir = '/Users/ostwald/Documents/Work/OpenSky/nldr_logs/library-dds-weblogs/' # purg
	filename = 'access.log'	
	
	path = os.path.join (logdir, filename)
	# tally = Tally(path, 'request')
	tally = TallyMgr(path, 'request')

