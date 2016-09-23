import os, sys, codecs

def convertRec (path):
	s = codecs.open(path, 'r', 'utf-8').read()
	print s.encode('utf-8')

	outpath = 'converted.xml'
	f = codecs.open (outpath, 'w', 'utf-8')
	f.write(s)
	f.close()
	print "wrote to", outpath

if __name__ == '__main__':
	basedir = "c:/tmp/python-tmp/collections"
	filename = 'COLLECTION-000-000-000-024.xml'
	path = os.path.join (basedir, filename)
	convertRec(path)
