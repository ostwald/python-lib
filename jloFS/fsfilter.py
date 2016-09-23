"""
OBSOLETE - should probably be scrapped. But look first for any useful stuff.

Currently filtering means deleting items from the working directory. but the result of
filtering could also to make other data structures and leave the primary ones intact.
How is filtering beter or worse than selection in fscmp.
"""

import sys, os, time
import myglobals
from UserDict import UserDict
from fsobj import JloFile, JloDirectory
from fscmp import WorkingFile, fileCmp
from time_helper import TimeHelper

class JloFilterFile (WorkingFile):
	"""
	currently HARDCODED that working file is DOS encoded, while reference is not
	
	- therefore, when we write a file, we must write the content (not just copy it).
	"""
	
	dowrites = 1
	
	def listing (self):
		# return ("%s %s" % (self.name, self.ppDate (self.modtime)))	
		return "%s%s (%s)" % (myglobals.getIndent(self.level), 
							   self.name, 
							   self.ppDate (self.modtime))
							   # self.modtime)
							   
	def ppDate (self, secs):
		return time.asctime(time.localtime(secs))
	
REJECTED = []
		
class WorkingFilterDirectory (JloDirectory):
	
	def __init__ (self, path, level=0):
		# path has to exist or what are we filtering?
		if not os.path.exists (path):
			raise Exception, "WorkingFilterDirectory: path does not exist at %s" % path
		
		JloDirectory.__init__ (self, path, level)
	
	def _accept_file (self, filename):
		
		if filename[0] in ['.', '#'] or filename[-1] in ['~']:
			return 0
		
		if filename == "CVS": return 0
			
		root, ext = os.path.splitext(filename)
		if not ext:
			return 1
		if ext in [".bak", '.off','.sav', '.obs']:
			return 0
		return 1
			
	def getDirectory (self, path):
		return WorkingFilterDirectory (path, self.level + 1)
			
	def getFile (self, path):
		return JloFilterFile (path, self.level+1)
		
	def isempty (self):
		if self.getfiles():return 0
		for subdir in self.getsubdirs():
			if not subdir.isempty():
				return 0
		return 1
		
	def filter (self, pred):
		for file in self.getfiles():
			# print "filter: %s" % file.name
			if not pred(file):
				# print "\t filter returned FALSE"
				del[self[file.name]]
				
		for sub in self.getsubdirs():
			sub.filter (pred)
		
	def listingOld (self):
		s=[];add=s.append
		add ("%s%s" % (myglobals.getIndent(self.level), self.name))
		for obj in self.dir():
			if isinstance (obj, JloDirectory):
				# print "DIRECTORY %s" % obj.name
				if not obj.isempty ():
					# print "\t NOT empty"
					add (obj.listing())
				else:
					# print "\t EMPTY"
					pass
			elif  isinstance (obj, JloFilterFile):
				# print "obj: " + obj.__class__.__name__
				add (obj.listing())
			else:
				add ("??? %s ???" % obj.name)
		return '\n'.join (s)
	
	def listing (self):
		"""
		NOTE: this method of defining sort may not work for
		more recent versions of python. 
		check version with sys.version_info
		the sort method below is known to work for v < 2.7.x
		"""
		s=[];add=s.append
		add ("%s%s/" % (myglobals.getIndent(self.level), self.name))
		files = self.getfiles()

		files.sort (lambda x,y:-cmp(x.modtime, y.modtime))
		for file in files:
			add (file.listing())
		for subdir in self.getsubdirs():
			if not subdir.isempty ():
				add (subdir.listing())
		return '\n'.join (s)
		
	def fssync (self, syncdir):
		"""
		This approach was abandoned in favor of fscmp because it relied
		to heavily on last mod, which is not a reliable way to judge whether a
		working file should replace a reference file.
		"""
		## print "%s%s" % (myglobals.getIndent(self.level), self.name)
		for file in self.getfiles():
			# print "sync: %s" % file.name
			refFilePath = os.path.join (syncdir, file.name)
			refFile = None
			try:
				refFile = JloFile (refFilePath)
			except:
				# print "no reference file for " + file.name
				pass
			if not refFile or not file.equals (refFile):
				file.write (syncdir)
				if not file.dowrites:
					print "%s (NOT WRITTEN)" % file.listing()
				else:
					print file.listing()
			else:
				REJECTED.append (file)
		for subdir in self.getsubdirs():
			if not subdir.isempty ():
				path = os.path.join (syncdir, subdir.name)
				listing =  "%s%s/" % (myglobals.getIndent(subdir.level), subdir.name)
				if not os.path.exists (path):
					listing =  "%s*%s/" % (myglobals.getIndent(subdir.level), subdir.name)
					if JloFilterFile.dowrites:
						listing = listing + " (created)"
						# print "\ncreating dir: " + path
						os.mkdir (path)
					else:
						listing = listing + " (new)"
				print listing
						
				subdir.fssync (path)
		
# filters - predicates: operations on files that return 0 or 1

	

def newerThan (path, threshold):
	d = WorkingFilterDirectory (path)
	d.filter (lambda obj: (obj.modtime > threshold))
	print d.listing()	
	
def synco (rel_path, threshold):
	workpath = os.path.join (myglobals.working_repo, rel_path)
	syncpath = os.path.join (myglobals.reference_repo, rel_path)
	d = WorkingFilterDirectory (workpath)
	d.filter (lambda obj: (obj.modtime > threshold))
	d.fssync (syncpath)
	if REJECTED:
		print "%d rejected files" % len(REJECTED)
		for r in REJECTED:
			print "\t%s    %s" % (r.name, r.path[len (myglobals.working_repo):])
	else:
		print "no rejects"
	
if __name__ == "__main__":
	rel_path = 'dlese-tools-project/src/org/dlese/dpc/schemedit/standards'
	dateStr = '6/10/09'
	threshold = TimeHelper().getTime (dateStr)
	synco (rel_path, threshold)

	
