"""
ark_reporter

for a collection an entry for each object:
pid, status, error
"""

import sys, logging, time
from keiths_tools import get_collection_members, get_identifier_metadata
from ark_status import get_ark_status, ArkException
from UserList import UserList

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)

class Entry ():
	
	def __init__ (self, pid):
		self.pid = pid
		self.status = None
		self.error = None
		self.msg = ''
		
	def __repr__ (self):
		s = self.pid
		if self.status:
			s += ' - status: %s' % self.status
		if self.error:
			s += ' - error:  %s' % self.error
		if self.msg:
			s += ' - msg:  %s' % self.msg
		return s

class Reporter (UserList):
	
	MAX_PIDS = 50000
	
	def __init__ (self, collection):
		self.data = []
		self.collection = collection
		ticks = time.time()
		self.process()
		self.elapsed = time.time() - ticks
		
	def report (self, fn=None):
		
		def default_fn (entry):
			print entry
		
		fn = fn or default_fn
		map (fn, self.data)
		
	def process(self):
		pid_num = 0
		for pid in get_collection_members(self.collection):
			print ('- %s'% pid)
			pid_num = pid_num + 1
			n, ark, o =  get_identifier_metadata(pid)
			if ark is not None and ark is not None and o is not None:
				# fo.write("{}|{}|{}|{}\n".format(o,ark,pid,n))
				# print("{}|{}|{}|{}\n".format(o,ark,pid,n))
				entry = Entry(pid)
				status = None
				error = None
				try:
					status = get_ark_status(ark)
				except ArkException:
					error = sys.exc_info()[1]		
					
				except:
					print "ERROR: %s" % sys.exc_info()[1]
					sys.exit(1)
				
				if error:
					print "ERROR (pid: %s) %s" % (pid, error)
					entry.error = error
					
				else:
					entry.status = status
					if status == 0:
						print "ark: %s is reserved but not bound to pid: %s" % (ark, pid)
						
					elif status == 1:
						# activated - do not report
						pass
					else:
						print "WARN: unknown status: '%s'" % status
				self.data.append(entry)	
				
			if pid_num > self.MAX_PIDS:
				break
				
if __name__ == '__main__':
	collection = "opensky:imagegallery"
	rpt = Reporter(collection)
	print "%d entries processed" % len(rpt)
	for e in rpt:
		print e
	print 'elapsed: %f' % rpt.elapsed
