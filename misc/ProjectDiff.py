#!/usr/bin/env python

import os, time, sys
from UserDict import UserDict
from shutil import copyfile, copytree

if sys.platform == 'win32':
	sys.path.append ("H:/python-lib")
elif sys.platform == 'linux2':
	sys.path.append ("/home/ostwald/python-lib")
else:
	sys.path.append ("/Users/ostwald/devel/python")

from PathTool import localize
	
class Walker:
	def __init__ (self, srcbase, dstbase):
		self.srcbase = srcbase
		self.dstbase = dstbase
		self.frag = ""

	def walk (self, src, dst):
		dir = Dir (dst)
		for filename in os.listdir (dst):
			path = os.path.join (dst, filename)
			if os.path.isdir (path):
				walk (os.path.join (src, filename), path)
		newer = dirCmp (src, dst)

class DirectoryDiffer:
	"""
	compares files in one "projects" directory against their counter parts in a parallel directory.
		projectsDir -- the working files
		cmpProjectsDir -- the files against which the working files are compared
	"""
	
	default_workingProjectsDir = localize ("/dpc/tremor/devel/ostwald/projects/tmp")
	# cvsProjectsDir = localize ("/dpc/tremor/devel/ostwald/projects/archive/namespaces-051720006")
	default_referenceProjectsDir = localize ("/dpc/tremor/devel/ostwald/projects")
	
	extensions = [".java", ".jsp", ".jspf", ".tag", ".css", ".js", ".xml", ".html"]
	
	def __init__ (self, path, workingProjectsDir=None, refProjectsDir=None, verbose=0, update=0, recursive=0):
		self.path = path
		self.verbose = verbose
		self.update = update
		self.recursive = recursive
		if workingProjectsDir is None:
			self.workingProjectsDir = self.default_workingProjectsDir
		else:
			self.workingProjectsDir = workingProjectsDir
		
		if refProjectsDir is None:
			self.refProjectsDir = self.default_referenceProjectsDir
		else:
			self.refProjectsDir = refProjectsDir
			
		self.relative_path = self._get_relative_path ()
			
		## print "\npyDiffer\n\tworkDir: %s\n\trefDir: %s\n" % (self.workingProjectsDir, self.refProjectsDir)
		
		if update:
			self.updater()
		else:
			self.diff()
			
	def _get_relative_path (self):
		# check that the srcPath is within the projectsDir
		if self.path.find (self.workingProjectsDir) != 0:
			raise "illegal path: \n\t%s\nmust be within\n\t%s" % (self.path, self.workingProjectsDir)
		
		# calculate the delta path from projectsDir to srcPath
		return self.path[len(self.workingProjectsDir)+1:]
		
	def diff (self):
		
		# print "\npath: %s\n" % frag
		
		workPath = self.path
		refPath = os.path.join (self.refProjectsDir, self.relative_path)
		# print "diff\n\t%s\n\t%s\n" % (workPath, refPath)
		if os.path.isdir (self.path):
			# print "Directory: ", path
			self.dir_diff (workPath, refPath)
		else:
			# filename = os.path.split (self.path)[1]
			# print "File: ", filename
			self.file_diff (workPath, refPath)
			
	def file_diff (self, workPath, refPath):
		"""
		changes necessary to make srcPath like cmpPath
		"""
		os.system ("diff %s %s" % (workPath, refPath))
		
	def dir_diff (self, workDir, refDir, verbose=0):
		"""
		do a diff on all files in refDir that are different than the counterpart in workDir
		"""
		# print "comparing directories"
		print "\n------------------------\nDIFF %s\n----" % workDir
		changed = self.changed_files (workDir, refDir)
		if changed:
			print "Files with Differences"
			for filename in changed:
				if self.verbose:
					print "\n%s\n%s" % ("-"*50, filename)
					self.file_diff (os.path.join (workDir, filename), os.path.join (refDir, filename))
					## os.system ("diff %s %s" % (workPath, refPath))
				else:
					print "\t%s" % (filename)
				
		missing_files = self.missing_files (workDir, refDir)
		missing_dirs = self.missing_directories (workDir, refDir)
		if missing_files or missing_dirs:
			print "\nPresent in workDir but not in refDir"
			if missing_files:
				print "\tFiles"
				for f in missing_files:
					print "\t\t" + f
			if missing_dirs:
				print "\tDirectories"
				for f in missing_dirs:
					print "\t\t" + f
					
		missing_files = self.missing_files (refDir, workDir)
		missing_dirs = self.missing_directories (refDir, workDir)
		if missing_files or missing_dirs:
			print "\nPresent in refDir but not workDir"
			if missing_files:
				print "\tFiles"
				for f in missing_files:
					print "\t\t" + f
			if missing_dirs:
				print "\tDirectories"
				for f in missing_dirs:
					print "\t\t" + f
		
		if self.recursive:			
			#recursively call updater on all directories
			for filename in os.listdir (refDir):
				if filename.upper() == "CVS":continue
				path = os.path.join (refDir, filename)
				workPath = os.path.join (workDir, filename)
				if os.path.isdir (path) and os.path.exists (workPath):
					DirectoryDiffer(workPath, verbose=self.verbose, update=self.update, recursive=self.recursive)
		
	def updater (self):
		
		workDir = self.path
		refDir = os.path.join (self.refProjectsDir, self.relative_path)		
		
		print "\n------------------------\nUPDATER - %s\n----" % workDir
		print "updating changed files in work directory"
		changed = self.changed_files (workDir, refDir)
		if changed:
			for filename in changed:
				copyfile (os.path.join (refDir, filename), os.path.join (workDir, filename))
				print "\t%s" % filename
		else:
			print "\tno changed files found"
			
		print "inserting missing files into work directory"
		missing = self.missing_files (refDir, workDir)
		if missing:
			for filename in missing:
				copyfile (os.path.join (refDir, filename), os.path.join (workDir, filename))
				print "\t%s" % filename
		else:
			print "\tthere are no missing files"
			
		if self.recursive:
			# get missing directory trees
			for filename in self.missing_directories (refDir, workDir):
				copytree (os.path.join (refDir, filename), os.path.join (workDir, filename))
				print "\n\tcopied tree to ", filename
			
			#recursively call updater on all directories
			for filename in os.listdir (workDir):
				if filename.upper() == "CVS":continue
				path = os.path.join (workDir, filename)
				if os.path.isdir (path):
					DirectoryDiffer(path, verbose=self.verbose, update=self.update, recursive=self.recursive)
				
			
		
			
	def changed_files (self, dir1, dir2):
		changed = []
		for filename in os.listdir (dir1):
			# print "\t", filename
			path1 = os.path.join (dir1, filename)
			root, ext = os.path.splitext (filename)
			if os.path.isdir (path1) or \
			   filename[0] in ['.', '#'] or \
			   filename[-1] in ['~']  or \
			   ext not in self.extensions: continue
			path2 = os.path.join (dir2, filename)

			if os.path.exists (path2) and \
				open (path1, 'r').read() !=  open(path2, 'r').read():
					changed.append (filename)
		return changed
			
	def missing_files (self, dir1, dir2):
		"""
		return list of files that are present in dir1 but missing in dir2
		"""
		missing = []
		if not os.path.exists(dir1): return missing
		for filename in os.listdir (dir1):
			# print "\t", filename
			path = os.path.join (dir1, filename)
			root, ext = os.path.splitext (filename)
			if os.path.isdir (path) or \
			   filename[0] in ['.', '#'] or \
			   filename[-1] in ['~']  or \
			   ext not in self.extensions: continue
			
			if not os.path.exists (os.path.join (dir2, filename)):
				missing.append (filename)
		return missing
	
	def missing_directories (self, dir1, dir2):
		"""
		return list of files that are present in dir1 but missing in dir2
		"""
		missing = []
		if not os.path.exists (dir1):return missing
		for filename in os.listdir (dir1):
			if filename.upper() == "CVS":continue
			# print "\t", filename
			path = os.path.join (dir1, filename)
			root, ext = os.path.splitext (filename)
			if not os.path.isdir (path): continue
			
			if not os.path.exists (os.path.join (dir2, filename)):
				missing.append (filename)
		return missing
		
class Dir (UserDict):
 
	def __init__ (self, path, parent):
		UserMap.__init__ (self)
		self.name = os.path.split(path)[1]
		self.parent = parent

	def addFile (self, path):
		self[path] = File (path, self)

	def addDir (self, path, parent):
		self[path] = Dir (path, self)

	def isEmpty (self):
		return len(self) == 0

class File:
	def __init__ (self, path, dir):
		self.dir, self.name = os.path.split(path)
		self.last_mod = os.stat(path).st_mtime


def dirCmp (src, dst):
	"""
	list FILES from dst that are newer (or don't exist) in src
	"""
	newer = []
	for filename in os.listdir (dst):
		dstpath = os.path.join (dst, filename)
		root, ext = os.path.splitext (filename)
		if os.path.isdir (dstpath) or \
		   filename[0] in ['.', '#'] or \
		   filename[-1] in ['~'] or \
		   ext not in extenensions:
			continue
		srcpath = os.path.join (src, filename)

		if not os.path.exists (srcpath):
			newer.append (dstpath)
			continue
		if  os.stat(dstpath).st_mtime >  os.stat(srcpath).st_mtime:
			newer.append (dstpath)
			print "%s\n%s" % ("-"*50, dstpath)
			os.system ("diff %s %s" % (srcpath, dstpath))
	return newer
	
def dirDiff (src, dst):
	diff = []
	for filename in os.listdir (dst):
		dstpath = os.path.join (dst, filename)
		if os.path.isdir (dstpath) or \
		   filename[0] in ['.', '#'] or \
		   filename[-1] in ['~'] :
			continue
		srcpath = os.path.join (src, filename)

		if not os.path.exists (srcpath):
			diff.append (dstpath)
			continue
		if  open (dstpath, 'r').read() !=  open(srcpath, 'r').read():
			diff.append (dstpath)
			print "%s\n%s" % ("-"*50, dstpath)
			os.system ("diff %s %s" % (srcpath, dstpath))
	return diff

def test ():
	# srcbase = "/Users/ostwald/devel/projects/dlese-tools-project/"
	# dstbase = "/Users/ostwald/devel/projects/tmp/dlese-tools-project/"
	
#	srcbase = localize ("/devel/ostwald/projects/dlese-tools-project/")
#   dstbase = localize ("/devel/ostwald/projects/archive/namespaces-051720006/dlese-tools-project/")

	srcbase = localize ("/devel/ostwald/projects/roles")
	dstbase = localize ("/devel/ostwald/projects/tmp/roles/")

	frag = "src/org/dlese/dpc/schemedit/action"
	src = os.path.join (srcbase, frag)
	dst = os.path.join (dstbase, frag)
	if 0:
		newer = dirCmp (src, dst)
		for path in newer:
			print os.path.split(path)[1]
	if 1:
		dirDiff (src, dst)

if __name__ == "__main__":
	cwd = os.getcwd()
	# print "current directory: ", cwd
	
	# default flags
	verbose = 0
	update = 0
	recursive = 0
	# consume flags
	if len(sys.argv) > 1 and "-" in sys.argv[1]:
		flags = sys.argv[1]
		if "v" in flags:
			verbose = 1
		if "u" in flags:
			update = 1		
		if "r" in flags:
			recursive = 1
		del sys.argv[1]
		
	if len (sys.argv) == 1:
		path = cwd
	else:
		path = os.path.join (cwd, sys.argv[1])

	print "\n%s\n" % ("="*100)
	print "DirectoryDiffer args\n\tpath: %s\n\tverbose: %d\n\tupdate: %d\n\trecursive: %d" % (path, verbose, update, recursive)
		
	DirectoryDiffer(path, verbose=verbose, update=update, recursive=recursive)



