import os, sys, codecs
from xml_dec_repair import DeclarationFixer

# dcs_data_dir = 'H:/python-lib/ncar_lib/dups/data/dcs_data'
# dcs_data_dir = '/tomcat/library_data/dcs/records/dcs_data'

dowrites = 1

class Fixer:
	"""
	strips a file of all the non-ascii chars. probably shouldn't be used on metadata
	file, but is okay on dcs_data
	"""
	def __init__ (self, path):
		self.path = path
		self.filename = os.path.basename(self.path)
		print "filename: ", self.filename

		self.collection = os.path.basename(os.path.dirname(self.path))
		print "collection: ", self.collection

		print "outpath: ", self.getOutPath()
		if dowrites:
			self.write()


	def getOutPath (self):
		"""
		hook to write to arbitrary path
		self.path overwites existing file
		"""
		## return os.path.join('fixed', self.collection, self.filename)
		return self.path

	def getFixedContent(self):
		content = open(self.path, 'r').read()

		print "%d characters read" % len(content)
		s=[];add=s.append
		for ch in content:
			if ord(ch) > 31 and ord(ch) < 127:
				add (ch)
		
		return ''.join(s)		


	def write(self, outpath=None):

		content = self.getFixedContent()
		
		outpath = outpath or self.getOutPath()
		if not os.path.exists (os.path.dirname (outpath)):
			os.makedirs (os.path.dirname (outpath))
		fp = codecs.open(outpath, 'w', 'utf-8')
		fp.write (content)
		fp.close()

#		DeclarationFixer (outpath)

		print 'wrote to', outpath

class BigFile:

	def __init__ (self, path):
		self.path = path
		self.name = os.path.basename(self.path)
		self.size = os.path.getsize(self.path)

	def __cmp__ (self, other):
		return -cmp(self.size, other.size)

def processDir (dir):
	"""
	call Fixer on all files bigger than some threshold.
	if dowrites is False, simply list the files we would have fixed
	"""
	files = []
	for filename in os.listdir(dir):
		path = os.path.join (dir, filename)
		file = BigFile(path)
		
		# 500KB is about the threshold, above which is likely to have
		# corrupt files in need of repair
		
		threshold = 500000 # 500KB
		if file.size > threshold:
			files.append(file)
	files.sort()
	for file in files:
		print file.name, file.size
		if dowrites:
			Fixer(file.path)
		
if __name__ == '__main__':
	ams_pubs = '/Users/ostwald/tmp/osgc/'
	if 0:
		#	path = os.path.join (dcs_data_dir, 'osm/osgc/OSGC-000-000-000-089.xml')
		path = os.path.join (ams_pubs, 'AMS-PUBS-000-000-000-109.xml')
		Fixer(path)
	else:
		processDir (ams_pubs)

