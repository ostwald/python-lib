import os, sys, string
from UserList import UserList

class Dir (UserList):
	def __init__ (self, path):
		UserList.__init__ (self, [])
		self.path = path

		data = []
		for filename in os.listdir (path):
			filepath = os.path.join (path, filename)
			## if not os.path.isdir (filepath) and not filename[0] == '.':
			if self.acceptFile (filename):
				data.append (filename)
		data.sort(self._cmp)
		self.data = data

	def acceptFile (self, filename):
		root, ext = os.path.splitext(filename)
		if filename[0] == '.':
			return 0
		if ext in ['.pyc']:
			return 0
		return 1

	def _cmp (self, s1, s2):
		return cmp (s1.upper(), s2.upper())

	def list (self):
		print "\n%s (%d)" % (self.path, len (self))
		for filename in self.data:
			print "\t", filename

	def contains (self, f):
		return f in self.data
	
			
	def compareDir (self, otherDir):
		common = []
		diff = []
		for filename in self.data:
			if otherDir.contains (filename):
				common.append (filename)
			else:
				diff.append (filename)


		print "\n%s (%d)" % (self.path, len (self))
		
		print "common (%d):" % len (common)
		for c in common:
			print '\t', c
			
		print "missing (%d):" % len (diff)
		for m in diff:
			print '\t', m

class DirCompare:
	def __init__ (self, path1, path2):
		self.dir1 = Dir(path1)
		self.dir2 = Dir(path2)
		print 'comparing %s and %s' % (path1, path2)
		
		self.union = self._getUnion()
		
	def _getUnion (self):
		files = []
		for dir in [self.dir1, self.dir2]:
			for f in dir:
				if f not in files:
					files.append (f)
		return files
		
	def report (self):
		
		print "files that are in dir1 but not in dir2"
		for f in self.dir1:
			if f not in self.dir2:
				print "\t", f
		
		print "files that are in dir2 but not in dir1"
		for f in self.dir2:
			if f not in self.dir1:
				print "\t", f
			
if __name__ == "__main__":
	p1 = '/Users/ostwald/devel/python-lib/ncar_lib'
	p2 = '/Users/ostwald/devel/python-lib-old/ncar_lib'

	c = DirCompare (p1, p2)
	c.report()
		
