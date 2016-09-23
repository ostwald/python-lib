#!/usr/bin/env python

import os, time, sys, string

from shutil import copyfile, copytree

from UserDict import UserDict
from UserList import UserList

mergeDir = "/dls/devel/ostwald/tmp/merge"
toolsPath = "src/org/dlese/dpc"

cvsProject = os.path.join (mergeDir, "cvs-dir", "dlese-tools-project")
svnProject = os.path.join (mergeDir, "svn", "dlese-tools-project")

cvsTools = os.path.join (cvsProject, toolsPath)
svnTools = os.path.join (svnProject, toolsPath)
	
class Walker:
	def __init__ (self, command, relPath=""):
		print "%s\nWalker\n\tstarting at '%s'\n\texecuting *%s*" % ("="*50, 
			os.path.join (mergeDir, cvsTools), 
			command.__name__)
		self.command = command
		self.relPath = relPath
		self.walk (self.relPath)

	def walk (self, relPath):
		dirCompare = DirCompare (relPath)
		
		self.command (dirCompare);
		
		if 0:
			dirCompare.report()

		if 0:
			dirCompare.update()

		if 0:
			dirCompare.changed_files()
		
		cvsPath = os.path.join (cvsTools, relPath)
		dirs = DirList (cvsPath)
		if dirs:
			for filename in dirs:
				self.walk (os.path.join (relPath, filename))

class FileList (UserList):

	extensions = ['.java', '.properties', ".xml", ".xls", ".js", ".jsp", ".html"]
	
	def __init__ (self, path):
		UserList.__init__ (self, [])
		self.path = path

		data = []
		if os.path.exists(path):
			for filename in os.listdir (path):
				if self._accept (filename):
					data.append (filename)
			data.sort(self._cmp)
			self.data = data

	def _accept (self, filename):
		path = os.path.join (self.path, filename)
		root, ext = os.path.splitext (filename)
		return not os.path.isdir(path) and not root[0] == '.' and ext.lower() in self.extensions
		
	def _cmp (self, s1, s2):
		return cmp (s1.upper(), s2.upper())

	def list (self):
		print "\nFiles in %s (%d)" % (self.path, len (self))
		for filename in self.data:
			print "\t", filename

	def contains (self, f):
		return f in self.data

class DirList (FileList):

	skipdirs = ['CVS', '.svn']
	
	def _accept (self, filename):
		path = os.path.join (self.path, filename)
		root, ext = os.path.splitext (filename)
		return os.path.isdir(path) and not filename in self.skipdirs	

	def list (self):
		print "\nDirectories in %s (%d)" % (self.path, len (self))
		for filename in self.data:
			print "\t", filename

class Dir:
	
	def __init__ (self, path):
		self.path = path
		self.filelist = FileList (path)
		self.dirlist = DirList (path)

class DirCompare:
	
	dowrites = 0
	
	def __init__ (self, relPath):
		self.relPath = relPath
		svnPath = os.path.join (svnTools, relPath)
		cvsPath = os.path.join (cvsTools, relPath)
		self.svn = Dir(svnPath)
		self.cvs = Dir(cvsPath)
		
		self.unionfiles = self._getUnion(self.svn.filelist, self.cvs.filelist)
		self.uniondirs = self._getUnion(self.svn.dirlist, self.cvs.dirlist)
		
	def _getUnion (self, list1, list2):
		files = []
		for dir in [list1, list2]:
			for f in dir:
				if f not in files:
					files.append (f)
		return files

	def _diff (self, list1, list2):
		diff=[];add=diff.append
		for f in list1:
			if f not in list2:
				add (f)
		return diff

	def changed_files (self):
		changed = []
		for filename in self.svn.filelist:
			## print "\t", filename
			svn_file_path = os.path.join (self.svn.path, filename)
			cvs_file_path = os.path.join (self.cvs.path, filename)
			root, ext = os.path.splitext (filename)
			
			if not os.path.exists(cvs_file_path):
				print "ALERT: cvs file %s does not exist" % filename
				continue

			if open (svn_file_path, 'r').read() !=  open(cvs_file_path, 'r').read():
				changed.append (filename)
				if self.dowrites:
					copyfile (svn_file_path, cvs_file_path)
		if changed:
			print "\nchanged files - " + self.relPath
			if self.dowrites:
				print '\t ** Files written **'
			for f in changed:
				print "\t" + f
				file_diff (self.relPath, f)
		return changed
		
	def update (self):
		"""
		copy all files in svn to cvs
		copy directory trees missing from cvs
		"""

		svn_dirs_to_copy = self._diff (self.svn.dirlist, self.cvs.dirlist)
		svn_files_to_copy = self._diff (self.svn.filelist, self.cvs.filelist)
		
		if svn_dirs_to_copy or svn_files_to_copy:
			print "\n** " + self.relPath
			
		if svn_dirs_to_copy:
			print "\n  dirs"
			for f in svn_dirs_to_copy:
				print "\t" + f
				src = os.path.join (self.svn.path, f)
				dst = os.path.join (self.cvs.path, f)			
				# print "\tCopyTree: %s\n\t\tfrom: %s\n\t\tto: %s" % (f, src, dst)
				if self.dowrites:
					copytree (src, dst)
			

		if svn_files_to_copy:
			print "\n  files"
			for file in svn_files_to_copy:
				print "\t" + file
				src = os.path.join (self.svn.path, file)
				dst = os.path.join (self.cvs.path, file)
				# print "\tcopy: %s\n\t\tfrom: %s\n\t\tto: %s" % (file, src, dst)
				if self.dowrites:
					copyfile (src, dst)
	
	def report (self):

		s=[];add=s.append
		if 1:
			diff = self._diff (self.svn.filelist, self.cvs.filelist)
			if diff:
				add ("files that are in svn but not in cvs")
				for f in diff:
					add ( "\t" + f)

		if 1:
			diff = self._diff (self.cvs.filelist, self.svn.filelist)
			if diff:
				# add ( "files that are in cvs but not in svn")
				add ("files to delete from CVS")
				for f in diff:
					add ( "\t" + f)

		if 1:
			diff = self._diff (self.svn.dirlist, self.cvs.dirlist)
			if diff:
				add ( "directories that are in svn but not in cvs")
				for f in diff:
					add ( "\t" + f)
		if 1:
			diff = self._diff (self.cvs.dirlist, self.svn.dirlist)
			if diff:		
				# add ( "directories to that are in cvs but not in svn")
				add ("dirs to delete from CVS")			
				for f in diff:
					add ( "\t" + f)

		if s:
			s.insert (0, "\n* " + self.relPath + " *")
			print string.join (s, "\n")

def differ ():
	relpath = "action"

	d = DirCompare (relpath)
	diffs = d.changed_files()

	for f in diffs[:1]:
		file_diff (relpath, f)

def file_diff (relPath, filename):
	print "\n\n", filename
	
	svn = os.path.join (svnTools, relPath, filename)
	cvs = os.path.join (cvsTools, relPath, filename)
	command = "diff %s %s" % (svn, cvs)
	# print command
	print os.system(command)
	
if __name__ == "__main__":
	DirCompare.dowrites = 0
	commandName = "update"
	command = getattr (DirCompare, commandName)
	relPath = "schemedit/ndr"
	w = Walker (command, relPath)
	# differ()

