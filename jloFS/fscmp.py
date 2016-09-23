"""
This module supports the comparison between a "working directory" and a "reference directory"
The files (WorkingFile) can compare by content or attribute, such as last modified.
The directories (WorkingDirectory) store data about the comparisons between their items
and the corresonding items in the reference Directory (which is implemented as a JloDirectory).

So the comparison between working and reference directories is stored in the flags data struture, 
which is used to create listing of files with specified relations, such as "new", "modified" and "missing"
"""
import sys, os
import myglobals
from UserDict import UserDict
from UserList import UserList
from fsobj import JloFile, JloDirectory



class WorkingFile (JloFile):
	"""
	A JloFile specialized to do file comparisons.
	The main reason for this class is that my working files are encoded PC-style, while
	the stuff i check out from CVS is unix-encoded.
	
	So, this class is currently HARDCODED to read files from DOS-end-lines and
	converted to unix.

	The write method writes the unix-encoded contents to a file 
	
	- therefore, when we write a file, we must write the content (not just copy it).
	"""
	
	dowrites = 0
	
	def __init__ (self, path, level=0):
		# print "File: " + path
		JloFile.__init__ (self, path, level)
		
class ObjStatus:
	"""
	Caches the results of comparisons between files, along with the
	WorkingFile instance.
	Flags are computed by fileCmp and include "new", "modified", and "missing"
	"""
	def __init__ (self, fsObj, flag):
		self.fsObj = fsObj
		self.name = fsObj.name
		self.level = fsObj.level
		self.flag = flag
		
	def __cmp__(self, other):
		"""
		comparison method that allows ObjStatus lists to be sorted by name
		"""
		return cmp (self.name, other.name)
		
	
class ComparisonFlags (myglobals.SortedUserDict):
	"""
	Mapping of filename to ObjStatus instance for all items in a directory
	
	Populated by WorkingDirectory._setFlags()
	"""
	
	""" what does this do?"""
	# what does this do?
	def __init__ (self):
		myglobals.SortedUserDict.__init__(self)
		self.empty = None  # if we see None, we know its not initialized
	
	def getFlag (self, name):
		if self.has_key (name):
			return self[name].name
			
	def isempty (self):
		if self.empty is None:
			empty = 1
			for status in self.values():
				if isinstance (status.fsObj, JloFile):
					print "file found at " + status.fsObj.path
					empty = 0
					break
			if empty == 1:
				for status in self.values():
					if isinstance (status.fsObj, WorkingDirectory):
						if not status.fsObj.flags.isempty():
							empty = 0
							break
			self.empty = empty
		return self.empty
			
	def report (self):
		print "\nflags report"
		for name in self.keys():
			status = self[name]
			print "\t%s  (%s)" % (name, status.flag)

class Selections (UserList):
	"""
	Records the results of a "select" operation as a list of
	fs objects (files and directories)
	"""
	empty = None
	
	def add (self, item):
		self.append (item)
		
	def isempty(self):
		"""
		recursively determine whether there are any File objects
		below us in the structure
		"""
		if self.empty is None:
			empty = 1
			for status in self:
				if isinstance (status.fsObj, JloFile):
					empty = 0
					break
			if empty == 1:
				for status in self:
					if isinstance (status.fsObj, WorkingDirectory):
						if not status.fsObj.selected.isempty():
							empty = 0
							break
			self.empty = empty
		return self.empty
	
all_extensions = []
		
class WorkingDirectory (JloDirectory):
	"""
	After reading its items, this class runs the _setFlags method
	to make and record the comparisons between the working and reference items.
	
	The flags (ComparisonFlags) strucure stores the comparisons.
	
	The select method ...
	"""
	def __init__ (self, path, refpath, level=0):
		self.flags = ComparisonFlags()
		# print "refpath: %s" % refpath
		if refpath and os.path.exists (refpath):
			self.refdir = JloDirectory (refpath)
		else:
			self.refdir = None
		JloDirectory.__init__ (self, path, level)
		if self.level == 0:
			print "\n"
			print "path: %s" % path
			print "refpath: %s\n" % refpath
		if path == refpath:
			raise Exception, "work dir can't be reference dir!"
		if not os.path.exists (path):
			raise Exception, "work dir does not exist at %s" % path
		# if not os.path.exists (refpath):
			# raise Exception, "ref dir does not exist at %s" % refpath
		
		self._setFlags ()
		# self.flags.report()
		self.selected = None
		self.flagset = None
		self.select (self.flagset)
		# self.flags.report()
	
	def _accept_file (self, filename):
		if not JloDirectory._accept_file (self, filename):
			return 0
		root, ext = os.path.splitext(filename)
		if not ext in all_extensions:
			all_extensions.append (ext)
		return 1
		
	def _accept_for_flag (self, filename):
		"""
		predicate determining which files will be ignored
		(why do we need a separate pred??)
		"""
		root, ext = os.path.splitext(filename)
		if not ext:
			return 1
		else:
			binary_extensions = ['.jpg', '.gif', '.png', '.jar' ]
			return ext not in ['.bak', '.off','.old', '.works', '.clean', '.obs', '.log', '.db'] + binary_extensions
	
	def _setFlag (self, obj, flag):
		# print "%s -> %s" % (filename, flag)
		if self._accept_for_flag (obj.name):
			self.flags[obj.name] = ObjStatus (obj, flag)
			
	def getDirectory (self, path):
		if self.refdir:
			newRefPath = os.path.join (self.refdir.path, os.path.basename(path))
		else:
			newRefPath = None
		return WorkingDirectory (path, newRefPath, self.level + 1)
			
	def getFile (self, path):
		return WorkingFile (path, self.level+1)
		
	def isempty (self):
		if self.flags:
			return 0
		for subdir in self.getsubdirs():
			if not subdir.isempty():
				return 0
		return 1
		
	def __repr__ (self, depth=None):
		"""
		use the SELECTED structure to recursively list
		the selected items in this Working Directory
		"""
		s=[];add=s.append
		
		add ("%s%s" % (myglobals.getIndent(self.level), self.name))
		if depth is None or self.level < depth:
			for status in self.selected:
				obj = status.fsObj
				# if obj.level > depth:
					# # print 'level (%d) exceeds depth, skipping' % obj.level
					# continue
				if isinstance (obj, WorkingDirectory):
					# print "DIRECTORY %s" % obj.name
					if not obj.selected.isempty():
						add (str(obj))
				elif isinstance (obj, JloFile):
					if os.path.exists(obj.path):
						add ("%s  (%s)!!!" % ( str(obj), status.flag))
						# add ("%s%s  (%s)!!!" % (myglobals.getIndent(self.level), str(obj), status.flag))
					else:
						add ("%s%s  (%s)???" % (myglobals.getIndent(self.level), str(obj), status.flag))
				else:
					## missing directory
					add ("%s%s (missing)##" % (myglobals.getIndent(self.level+1), obj.name))
		return '\n'.join (s)
				
	def _setFlags (self):
		self.flags = ComparisonFlags()
		refdir = self.refdir
		# print "setting flags (%s)" % self.name
		for workingFile in self.dir():
			
			filename = workingFile.name
			# print '\t', filename
			if not refdir:
				refFile = None
			else:
				refFile = refdir.getitem (filename)
			flag = ""
			if not refFile:
				flag = "new"
				# self._setFlag (filename, "new")
				
			# elif isinstance (workingFile, JloFile):
			else:
				flag = fileCmp (workingFile, refFile, 0)
			# print "\t --> %s" % flag
			self._setFlag (workingFile, flag)
			
		## refFiles that aren't in workingDir	
		if refdir:
			for refFile in refdir.dir():
				filename = refFile.name
				if not self.hasitem(filename):
					self._setFlag (refFile, fileCmp (None, refFile, 0))
				
	def select (self, flagset=None):
		"""
		select statusObjs that match provided flagset (i.e., delete the flags that don't match)
		"""
		# print "select (%s) flagset: %s" % (self.name, flagset)
		selected = Selections()
		if type(flagset) == type(""):
			flagset = [flagset,]
		self.flagset = flagset
		flags = self.flags
		for filename in flags.keys():
			status = flags[filename]
			# print "\t%s: %s" % (filename, status.flag)
			if isinstance (status.fsObj, WorkingDirectory):
				# print "\t  dir"
				selected.add (status)
				status.fsObj.select(self.flagset)
			elif not self.flagset or status.flag in self.flagset:
				selected.add (status)
				# print "\t\tADDED"
		selected.sort(ObjStatus.__cmp__)
		self.selected = selected

							 
	
# Testers below here ------------------------------			  
	
def list (flag_set, rel_path=None, title=None):
	"""
	print a WorkingDirectory listing to output
	"""
	title = title or "list for %s" %  flag_set
	rel_path = rel_path or 'dlese-tools-project/src/org/dlese/dpc/schemedit'

	working = os.path.join (myglobals.working_repo, rel_path)
	reference = os.path.join (myglobals.reference_repo, rel_path)
	dircmp = WorkingDirectory (working, reference)
	dircmp.select(flag_set)
	
	#listing header
	print "\n%s" % title
	print "%s" % '-'*len(title)
	print (dircmp)
	
def fullListing (rel_path=None):
	rel_path = rel_path or 'dlese-tools-project/src/org/dlese/dpc/schemedit'
	working = os.path.join (myglobals.working_repo, rel_path)
	reference = os.path.join (myglobals.reference_repo, rel_path)
	dircmp = WorkingDirectory (working, reference)
	# dircmp.select()
	print (dircmp)
	
def fileCmpTester (working, reference, filename):
	filename = "AsnCatalog.java"
	rel_path = "dlese-tools-project/src/org/dlese/dpc/standards/asn/util"
	working = os.path.join (myglobals.working_repo, rel_path, filename)
	reference = os.path.join (myglobals.reference_repo, rel_path, filename)
	workingFile = WorkingFile (working)
	# print "** workingFle: %s" % workingFile.name
	refFile = JloFile (reference)
	verbose = 1
	print fileCmp (workingFile, refFile, verbose)	
	if 1:
		chars_to_show = 300
		print "\n-- working file --\n%s" % workingFile.getContent()[:chars_to_show]
		print "---------------"
		print "\n-- reference file --\n%s" % refFile.getContent()[:chars_to_show]
	
class FSCompare:
	"""
	compares two files, working and reference, and 
	sets flags to store comparison results
	"""
	def __init__ (self, working_path, reference_path):
		self.workingPath = working_path
		self.referencePath = reference_path
		self.dircmp = WorkingDirectory (working_path, reference_path)
		self.dircmp.select(['new','missing'])
		
	def list (self, depth=None):
		print self.dircmp
		
def fileCmp (working, ref, compare_content=0, verbose=0):
	"""
	compare two JSFile objects and comparison flag (cmp-flag)
	("new", "modified", "missing")
	"""
	if verbose and working and ref:
		print "fileCmp\n\t working: %s\n\tref: %s" % (
			working.path or "no working path", 
			ref.path or "no reference path")
		
	flag = "UNASSIGNED"
	debugging = 0
	
	if ref and not working:
		flag = "missing"
	
	elif not ref: #  or not os.path.exists(ref.path):
		flag = "new"
		
	elif isinstance (working, JloFile):
		# print "ref: %s" % ref.__class__.__name__
		if debugging:
			if not working.equals (ref):
				print "working file is different"
				
			if not working.newerthan (ref):
				print "working file has same date as ref"
		
			if working.modtime == ref.modtime:
				print "mods dates match"
			else:
				# print "wrk: %d  ref: %d" % (working.modtime,ref.modtime)
				print "wrk: %s  ref: %s" % \
					(working.ppDate (working.modtime),
					 working.ppDate (ref.modtime))
		
		if compare_content:
			if working.equals (ref):
				flag = ""
			else:
				flag = "modified"
				
		else:
			flag = ""

			
			
			# elif not working.newerthan (ref):
			# flag = "obsolete-check"
		# elif working.newerthan (ref) and not working.equals (ref):
			# flag = "modified"
		# elif not working.equals (ref):
			# print "not modified"
			# flag = "different"
		# elif working.newerthan (ref):
			# flag = "modified"
	if verbose and working:
		print "%s --> %s" % (working.name, flag)
	return flag

		
if __name__ == "__main__":
	
	working = "/Volumes/Video Backup/Raw Video as iMovie Projects"
	reference = "/Volumes/Video Storage"
	cmp = FSCompare(working, reference)
	cmp.list()


