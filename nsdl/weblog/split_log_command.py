#!/usr/bin/python
from nsdl.weblog import ProtoSpliter

def splitLog (path, dest):
	ProtoSplitter.write_buffer_size = 1000
	
	log = ProtoSplitter (path, dest)
	print "entries processeed %d" % log.entry_count
	print "write_buffer_size: %d" % log.write_buffer_size
	
if __name__ == '__main__':
	
	# nsdl.org_access_log_10_25_1022'  # rs1
	# nsdl.org_access_log_frag'  # acorn
	filename = 'harvest.nsdl.org_access_log'
	if len(sys.argv) > 1:
		filename = sys.argv[1]
		print 'filename', filename

	
	host = 'acorn'
	if host == 'rs1':
		log_file_dir = '/home/ostwald/logs/log_files'
		# log_file_dir = '/dls/www/logs/"
		dest = '/home/ostwald/logs/splits/nsdl.org_access_log'
	elif host == 'acorn':
		log_file_dir = 'log_files'
		
		dest = 'splits/harvest.nsdl.org_access_log-SPLITS'
		
	
	path = os.path.join(log_file_dir, filename)
	
	splitLog(path, dest)

