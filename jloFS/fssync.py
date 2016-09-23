"""
Builds upon the objects of fscmp to update the reference directory, thereby syncing it with the working
directory.

Used for example to update a local directory with a newer version.

I don't think anything is deleted, so 
"""

import sys, os
import myglobals
from UserDict import UserDict
from UserList import UserList
from fscmp import WorkingFile, WorkingDirectory
from fsobj import FS_OBJ_CACHE, JloFSObj, JloFile, JloDirectory

class SyncWorkingFile (WorkingFile):
	"""
	extends the WorkFile to enable writing to disk
	
	dowrites - controls whether files are actually written
	
	"""
	dowrites = 1
	
	def write (self, dstdir, verbose=1):
		"""
		write the contents to disk in a like-named file in the
		destination directory
		the verbose flag enables output if desired
		"""
		content = self.getContent()
		path = os.path.join (dstdir, self.name)
		if self.dowrites:
			fp = open (path, 'w')
			fp.write (content)
			fp.close()
			if verbose:
				print "%s written to %s" % (os.path.basename(path), 
										os.path.dirname (path))
		else:
			if verbose:
				print "%s WOULD HAVE BEEN written to %s" % (os.path.basename(path), 
															os.path.dirname (path))

class SyncingWorkDirectory (WorkingDirectory):
	"""
	"""
	def __init__ (self, path, refpath, level=0):
		# print "refpath", refpath, " path", path
		WorkingDirectory.__init__(self, path, refpath, level)
		# if not self.refdir:
			# print "creating refdir and linking with parent"
			# myparent = FS_OBJ_CACHE.get(self.path)
			# if not myparent:
				# raise Exception, "parent not found for " + self.path
			# if not myparent.refdir:
				# raise Exception, "parent (%s)  has no refdir!" % myparent.name
			# myrefpath = os.path.join (myparent.refdir.dirname, self.name)
			# os.mkdir (myrefpath)
			# self.refdir = JloDirectory (myrefpath)
			# parent.refdir[self.name] = self.refdir
				
	def getDirectory (self, path):
		newRefPath = os.path.join (self.refdir.path, os.path.basename(path))
		if not os.path.exists (newRefPath):
			os.mkdir (newRefPath)
			print "created directory at " + newRefPath
		syncdir =  SyncingWorkDirectory (path, newRefPath, self.level + 1)
		
		# myparent = FS_OBJ_CACHE.get(self.path)
			# if not myparent:
				# raise Exception, "parent not found for " + self.path
			# if not myparent.refdir:
				# raise Exception, "parent (%s)  has no refdir!" % myparent.name
			# myrefpath = os.path.join (myparent.refdir.dirname, self.name)
			# os.mkdir (myrefpath)
			# self.refdir = JloDirectory (myrefpath)
			# parent.refdir[self.name] = self.refdir
		
		
		FS_OBJ_CACHE.add (syncdir)
		return syncdir
		
	def getFile (self, path):
		file = SyncWorkingFile (path, self.level+1)
		FS_OBJ_CACHE.add (file)
		return file
		
	def sync (self):
		"""
		workingi over the items selected by "new" and "modified"
		sync new and modified files to repository,
		creating new reference directories when necessary
		"""
		
		
		# print "\nUpdating reference dir"
		self.select (["modified", "new"])
		# print '%d selected for "modified", "new"' % len(self.selected)
		print "%s%s" % (myglobals.getIndent(self.level), self.name)
		for status in self.selected:
			obj = status.fsObj
			# print "status: %s\n\t%s" % (obj.__class__.__name__, obj.path)
			if isinstance (obj, SyncingWorkDirectory):
				# print "DIRECTORY %s" % obj.name
				if not obj.selected.isempty():
					# print "\t NOT empty"
					print "%s%s/" % (myglobals.getIndent(obj.level), obj.name)
					obj.sync ()
			elif  isinstance (obj, SyncWorkingFile):
				print "obj: " + obj.__class__.__name__
				print "%s  (%s)" % (str(obj), status.flag)
				obj.write (self.refdir.path, 1)
			elif isinstance (obj, JloDirectory):
				# this is a reference directory or file, which we don't touch during sync for mow
				pass
			else:
				raise Exception,  "sync encountered unrecognized object %s\n\t%s" % (obj.__class__.__name__, obj.path)
		

		
# Testers below here ------------------------------			  
def list (flag_set, rel_path=None, title=None):
	"""
	print a WorkingDirectory listing to output
	"""
	title = title or "list for %s" %  flag_set
	rel_path = rel_path or 'dlese-tools-project/src/org/dlese/dpc/schemedit'

	working = os.path.join (myglobals.working_repo, rel_path)
	reference = os.path.join (myglobals.reference_repo, rel_path)
	dircmp = SyncingWorkDirectory (working, reference)
	dircmp.select(flag_set)
	
	#listing header
	print "\n%s" % title
	print "%s" % '-'*len(title)
	print dircmp
	
def filesToSync (rel_path=None):
	flags = ["modified", "new"]
	list (flags, rel_path, "Files to Sync")

def filesToDelete (rel_path=None):
	list ("missing", rel_path, "Files to Delete from CVS")
	
def fullListing (rel_path=None):
	list (None, rel_path, "Full Listing")
	
def sync (rel_path=None):
	rel_path = rel_path or 'dlese-tools-project/src/org/dlese/dpc/schemedit'
	working = os.path.join (myglobals.working_repo, rel_path)
	reference = os.path.join (myglobals.reference_repo, rel_path)
	dircmp = SyncingWorkDirectory (working, reference)
	dircmp.sync()

	
def command ():
	path = os.getcwd()
	work_repo = myglobals.working_repo # working_repo
	
	if len (sys.argv) > 1:
		path = os.path.join (path, sys.argv[1])
			
		if path.startswith(work_repo):
			rel_path = path[len(work_repo):]
		else:
			raise Exception, "This command can only be called within! %s" % path
			
if __name__ == "__main__":
	# rel_path = "dlese-tools-project/src/org/dlese/dpc/standards"
	rel_path = "dcs-project"
	# rel_path = "dlese-tools-project"
	

	
	# fullListing(rel_path)
	# rel_path = "dcs-project"
	# filesToSync(rel_path)
	# filesToDelete(rel_path)
	sync(rel_path)
