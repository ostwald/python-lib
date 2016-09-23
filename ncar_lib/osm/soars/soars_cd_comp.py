import os

new = "D:/"
old = "H:/Documents/NCAR Library/SOARS Data/Assets"

class FilesGetter:

	def __init__ (self, base):
		self.files = []

		self.getFiles (base)

		self.files.sort()

	def getFiles (self, myDir):
		for filename in os.listdir(myDir):
			path = os.path.join (myDir, filename)
			if os.path.isdir (path):
				self.getFiles (path)
			else:
				if filename.endswith(".pdf"):
					self.files.append (filename)

class Comparer:

	def __init__ (self, newdir, olddir):
		self.newfiles = FilesGetter (new).files
		self.oldfiles = FilesGetter (old).files

		print "new: %d" % len (self.newfiles)
		print "old: %d" % len (self.oldfiles)

		self.compare ('newfiles', 'oldfiles')
		self.compare ('oldfiles', 'newfiles')

	def compare (self, list1, list2):
		print 'files in %s that are not in %s' % (list1, list2)

		files1 = getattr (self, list1)
		files2 = getattr (self, list2)
		
		for pdf in files1:
			if not pdf in files2:
				print pdf
			

def getterTester ():
	newfiles = FilesGetter (new).files

	for f in newfiles:
		print os.path.basename (f)



if __name__ == '__main__':
	Comparer(new, old)
