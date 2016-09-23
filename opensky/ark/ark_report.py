import sys, logging
from keiths_tools import get_collection_members, get_identifier_metadata
from ark_status import get_ark_status, ArkException

# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# collections = ['archives:hao','archives:vinlally','archives:mesalab','archives:nhre','archives:unid']

collections = ['opensky:imagegallery']

MAX_PIDS = 20000
MAX_COLLECTIONS = 2

collection_num = 0
for c in collections: 
	print "COLLECTION: %s" % c
	collection_num = collection_num + 1
	
	pid_num = 0
	print ("here we go")
	for pid in get_collection_members(c):
		pid_num = pid_num + 1
		n, ark, o =  get_identifier_metadata(pid)
		if ark is not None and ark is not None and o is not None:
			# fo.write("{}|{}|{}|{}\n".format(o,ark,pid,n))
			# print("{}|{}|{}|{}\n".format(o,ark,pid,n))
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
				
			elif status == 0:
				print "ark: %s is reserved but not bound to pid: %s" % (ark, pid)
				
			elif status == 1:
				# activated - do not report
				pass
			else:
				print "ERROR: unknown status: '%s'" % status
				
			logger.debug ( 'pid_num: %d' % pid_num )
			if pid_num > MAX_PIDS:
				break
		logger.debug( 'collection_num: %d' % collection_num )
		if collection_num > MAX_COLLECTIONS:
			break
