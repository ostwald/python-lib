import os, string

def isDosFile (path):
	s = open(path).read();
	return s.find ("\r\n") != -1

class File:
	def __init__ (self, path):
		self.path = path
		self.filename = os.path.basename(path)
		self.content = open(path).read();
		self.ulines = self.content.split ("\n");
		self.dlines = self.content.split ("\r\n")
		self.blanks = []
		for line in self.ulines:
			if line.strip() == "":
				self.blanks.append (line)

		self.threshold = .29

	def percentCRLF (self):
		return float (len (self.dlines)) / (len (self.ulines) + len (self.dlines))

	def reportVerbose (self):
		print "\t%s lf:%d, crlf:%d (%.2f)" % (self.filename,
											len(self.ulines),
											len (self.dlines),
											self.percentCRLF())
	def report (self):
		if (self.percentCRLF() > self.threshold):
			print "\t*%s (%.2f)" % (self.filename, self.percentCRLF())
		else:
			print "\t %s" % self.filename
		
class Dir:
	def __init__ (self, dir):
		self.path = dir
		self.dirs = []
		self.files = []
		for filename in os.listdir (dir):
			path = os.path.join (dir, filename)
			if os.path.isdir (path):
				if filename != "CVS":
					self.dirs.append (path)
			else:
				if filename[0] != '.':
					self.files.append (File (path))

class Walker:
	def __init__  (self, baseDir):
		self.baseDir = baseDir
		self.walk (self.baseDir)

	def relPath (self, path):
		return path [len (self.baseDir) : ]

	def walk (self, dirpath):
		dir = Dir (dirpath)
		print "\n%s" % self.relPath (dirpath)
		for f in dir.files:
			f.report()
		for d in dir.dirs:
			self.walk (d)
		
if __name__ == "__main__":
	from misc.CvsMerge import cvsTools
	dir = os.path.join (cvsTools, "")
	Walker (dir)
