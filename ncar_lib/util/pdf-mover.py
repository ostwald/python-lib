import os, sys, shutil
import math
"""
for all the pdf files within a given top-level directory:
- generate ID
- move to dest (renamed according to ID)
"""


## pdfBase = "H:/Documents/NCAR Library/staffnotes
pdfBase = "/home/ostwald/Documents/NCAR Library/staffnotes"


print "destParent: %s" % os.path.dirname(pdfBase)
destBase = os.path.join (os.path.dirname(pdfBase), 'RENAMED_STAFFNOTES')

class DirMover:

	id_template = "asset-000-000-%03d-%03d"

	def __init__ (self, base):
		self.base = base
		self.dirname = os.path.basename(base)
		self.dest = self._dest_setup()
		self.files = []
		self.walk (self.base)
		self.files.sort()
		self.counter = 1
		# self.move()

	def _dest_setup (self):
		dest = destBase
		print "dest: %s" % dest
		if os.path.exists (dest):
			os.rmdir (dest)
			# raise Exception, "dest exists at %s" % dest
		
		os.mkdir (dest)
		return dest
	
	def walk (self, dir):
		for filename in os.listdir(dir):
			path = os.path.join (dir, filename)
			if os.path.isdir (path):
				self.walk (path)
			else:
				if filename.lower().endswith('.pdf'):
					self.files.append(path)

	def report (self):
		print "%d files in %s" % (len(self.files), self.base)
		for path in self.files:
			print path[len(self.base)+1:], self.nextId()

	def nextId (self):
		thous = int (math.floor (self.counter / 1000))
		if thous > 999:
			raise Exception, "cannot handle id: %s" % self.counter
		ones = self.counter % 1000
		self.counter = self.counter + 1
		return self.id_template % (thous, ones)

	def move (self):
		for path in self.files:
			filename = self.nextId() + ".pdf"
			if 1:
				shutil.copyfile (path, os.path.join (self.dest, filename))
				sys.stdout.write('.')
			else:
				print os.path.join (self.dest, filename)
			if self.counter > 100000:
				break


def moverTest ():
	start = os.path.join (pdfBase, 'NEWSSCDI')
	dm = DirMover (start)
	dm.report()
	
def batchMove (pdfBase):
	"""
	moves a directory of top-level directories
	"""
	dirnames = os.listdir (pdfBase)
	i = 1
	for dirname in dirnames:
		print "%d/%d %s" % (i, len(dirnames), dirname)
		DirMover (os.path.join (pdfBase, dirname))
		i = i + 1
		
if __name__ == '__main__':
	dm = DirMover (os.path.join (pdfBase))
	# dm.report()
	dm.move()
	
