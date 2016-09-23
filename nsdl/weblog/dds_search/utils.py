import sys, os, shutil


def makeTestDir ():
	srcdir = '/Users/ostwald/devel/NSDL/logs/splits_output/search_queries-2013-05-23.log'
	dstdir = '/Users/ostwald/tmp/mock_dds_search_log'

	for filename in os.listdir(srcdir):
		print filename
		dst = os.path.join (dstdir, filename)
		print dst

		fp = open(dst, 'w')
		fp.write ('fooberry')
		fp.close()

def renameLogFiles(srcdir):
	# srcdir = '/Users/ostwald/tmp/mock_dds_search_log'
	for filename in os.listdir(srcdir):
		print filename
		src = os.path.join (srcdir, filename)
		newname = filename.replace ('-2013-05-23', '')
		print '\t',newname
		dst = os.path.join (srcdir, newname)
		shutil.move(src, dst)

if __name__ == '__main__':
	d = '/Users/ostwald/devel/NSDL/logs/splits_output/search_queries-2013-05-23.log'
	renameLogFiles(d)
